"""
Module to keep only images that correspond to NIDs in the CSV file.
Remove all other images.
"""

import os
import csv
from pathlib import Path
from typing import Set, Dict, List
import re


class CSVImageFilter:
    """Filter and remove images based on CSV NIDs."""
    
    def __init__(self, dry_run: bool = True):
        """
        Initialize the filter.
        
        Args:
            dry_run: If True, don't actually delete files, just report what would be deleted
        """
        self.dry_run = dry_run
        self.files_removed = 0
    
    @staticmethod
    def read_valid_filenames_from_csv(csv_file: str, 
                                      front_column: str = 'front_image', 
                                      back_column: str = 'back_image') -> Set[str]:
        """
        Read valid image filenames from CSV file.
        
        Args:
            csv_file: Path to the CSV file
            front_column: Name of the column containing front image filenames
            back_column: Name of the column containing back image filenames
            
        Returns:
            Set of valid filenames (full path as stored in CSV)
        """
        valid_filenames = set()
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f, delimiter='\t')
                
                for row in reader:
                    # Extract front image path
                    if front_column in row and row[front_column]:
                        front_path = str(row[front_column]).strip()
                        if front_path and front_path != '\\N':
                            # Extract just the filename from the path
                            filename = os.path.basename(front_path)
                            if filename:
                                valid_filenames.add(filename)
                    
                    # Extract back image path
                    if back_column in row and row[back_column]:
                        back_path = str(row[back_column]).strip()
                        if back_path and back_path != '\\N':
                            # Extract just the filename from the path
                            filename = os.path.basename(back_path)
                            if filename:
                                valid_filenames.add(filename)
            
            print(f"Read {len(valid_filenames)} valid image filenames from CSV")
            return valid_filenames
        
        except FileNotFoundError:
            print(f"Error: CSV file not found: {csv_file}")
            return set()
        except Exception as e:
            print(f"Error reading CSV: {e}")
            return set()
    
    @staticmethod
    def extract_nid_from_filename(filename: str) -> str:
        """
        Extract filename from image path.
        
        Args:
            filename: Image filename
            
        Returns:
            Filename without directory
        """
        return os.path.basename(filename)
    
    def scan_and_filter_directory(self, directory: str, valid_filenames: Set[str]) -> Dict:
        """
        Scan directory and identify files to remove.
        
        Args:
            directory: Path to the directory
            valid_filenames: Set of valid filenames from CSV
            
        Returns:
            Dictionary with statistics
        """
        if not os.path.isdir(directory):
            print(f"Error: {directory} is not a valid directory")
            return {'directory': directory, 'total_files': 0, 'valid_files': 0, 'invalid_files': 0}
        
        total_files = 0
        valid_files = 0
        invalid_files = 0
        files_to_remove = []
        
        print(f"\nScanning directory: {directory}")
        
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            
            if not os.path.isfile(file_path):
                continue
            
            # Only process image files
            if Path(filename).suffix.lower() not in {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp', '.tiff'}:
                continue
            
            total_files += 1
            
            if filename in valid_filenames:
                valid_files += 1
            else:
                invalid_files += 1
                files_to_remove.append(file_path)
        
        return {
            'directory': directory,
            'total_files': total_files,
            'valid_files': valid_files,
            'invalid_files': invalid_files,
            'files_to_remove': files_to_remove
        }
    
    def remove_invalid_images(self, directories: List[str], csv_file: str) -> Dict:
        """
        Remove images that don't correspond to filenames in CSV.
        
        Args:
            directories: List of image directories to process
            csv_file: Path to the CSV file
            
        Returns:
            Dictionary with overall statistics
        """
        # Read valid filenames from CSV
        valid_filenames = self.read_valid_filenames_from_csv(csv_file)
        
        if not valid_filenames:
            print("Error: No valid filenames found in CSV")
            return {'error': 'No valid filenames found in CSV', 'files_removed': 0}
        
        all_files_to_remove = []
        results_by_dir = {}
        
        # Scan all directories
        for directory in directories:
            result = self.scan_and_filter_directory(directory, valid_filenames)
            results_by_dir[directory] = result
            all_files_to_remove.extend(result['files_to_remove'])
            
            print(f"  Total images: {result['total_files']}")
            print(f"  Valid (in CSV): {result['valid_files']}")
            print(f"  Invalid (not in CSV): {result['invalid_files']}")
        
        total_to_remove = len(all_files_to_remove)
        print(f"\nTotal files to remove: {total_to_remove}")
        
        # Show sample of files to be removed
        if all_files_to_remove:
            print("\nSample of files to be removed (first 10):")
            for file_path in all_files_to_remove[:10]:
                print(f"  {os.path.basename(file_path)}")
            if total_to_remove > 10:
                print(f"  ... and {total_to_remove - 10} more")
        
        # Perform removal
        self.files_removed = 0
        for file_path in all_files_to_remove:
            if not self.dry_run:
                try:
                    os.remove(file_path)
                    self.files_removed += 1
                except OSError as e:
                    print(f"Error removing {os.path.basename(file_path)}: {e}")
            else:
                self.files_removed += 1
        
        return {
            'csv_file': csv_file,
            'valid_filenames_count': len(valid_filenames),
            'total_files': sum(r['total_files'] for r in results_by_dir.values()),
            'valid_files': sum(r['valid_files'] for r in results_by_dir.values()),
            'invalid_files': sum(r['invalid_files'] for r in results_by_dir.values()),
            'files_removed': self.files_removed,
            'dry_run': self.dry_run,
            'by_directory': results_by_dir
        }


def main():
    """Example usage of the CSVImageFilter."""
    import sys
    
    # Configuration
    csv_file = "data/nid-data-140126.csv"
    directories = [
        "data/images/nid_front_image",
        "data/images/nid_back_image",
    ]
    
    # Check if CSV exists
    if not os.path.isfile(csv_file):
        print(f"Error: CSV file not found: {csv_file}")
        return
    
    # Check for --confirm flag to skip confirmation
    confirm_delete = '--confirm' in sys.argv
    
    # Perform dry run first (no actual deletion)
    print("=" * 70)
    print("DRY RUN - No files will be deleted")
    print("=" * 70)
    
    filter_dry = CSVImageFilter(dry_run=True)
    result_dry = filter_dry.remove_invalid_images(directories, csv_file)
    
    # Print summary
    print("\n" + "=" * 70)
    print("SUMMARY (DRY RUN)")
    print("=" * 70)
    print(f"Valid image filenames in CSV: {result_dry['valid_filenames_count']}")
    print(f"Total images: {result_dry['total_files']}")
    print(f"Valid images (matching CSV): {result_dry['valid_files']}")
    print(f"Invalid images (not in CSV): {result_dry['invalid_files']}")
    print(f"Files to be removed: {result_dry['files_removed']}")
    
    # Ask for confirmation or use flag
    if result_dry['files_removed'] > 0:
        if confirm_delete:
            response = 'yes'
            print(f"\n--confirm flag detected. Proceeding with deletion...")
        else:
            response = input("\nProceed with actual deletion? (yes/no): ").strip().lower()
        
        if response in ['yes', 'y']:
            print("\n" + "=" * 70)
            print("ACTUAL RUN - Deleting invalid image files")
            print("=" * 70)
            
            filter_actual = CSVImageFilter(dry_run=False)
            result = filter_actual.remove_invalid_images(directories, csv_file)
            
            print("\n" + "=" * 70)
            print("SUMMARY (ACTUAL RUN)")
            print("=" * 70)
            print(f"Valid image filenames in CSV: {result['valid_filenames_count']}")
            print(f"Total images processed: {result['total_files']}")
            print(f"Valid images (kept): {result['valid_files']}")
            print(f"Invalid images (removed): {result['invalid_files']}")
            print(f"Files actually removed: {result['files_removed']}")
        else:
            print("Deletion cancelled.")
    else:
        print("\nNo invalid images to remove.")


if __name__ == "__main__":
    main()
