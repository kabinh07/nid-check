"""
Find and delete duplicate images in front and back directories.
Uses file hashing to detect duplicates.
Finds common IDs that are duplicates in both directories and deletes them.
"""

import os
import hashlib
from pathlib import Path
from collections import defaultdict
from typing import Dict, Set, Tuple


def get_file_hash(filepath: str) -> str:
    """Calculate SHA256 hash of a file."""
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def find_duplicates_in_directory(directory: str) -> Tuple[Dict[str, Set[str]], Dict[str, str]]:
    """
    Find duplicate files in a directory by hash.
    
    Returns:
        - hash_to_files: Dict mapping hash to set of file paths with that hash
        - file_to_hash: Dict mapping file path to its hash
    """
    hash_to_files = defaultdict(set)
    file_to_hash = {}
    
    print(f"\nProcessing directory: {directory}")
    print("Computing hashes...")
    
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            file_hash = get_file_hash(filepath)
            hash_to_files[file_hash].add(filepath)
            file_to_hash[filepath] = file_hash
    
    return hash_to_files, file_to_hash


def get_duplicate_ids_by_directory(directory: str) -> Set[str]:
    """
    Get IDs (filenames) that have duplicates within a directory.
    Returns the set of IDs that appear more than once.
    """
    hash_to_files, _ = find_duplicates_in_directory(directory)
    
    duplicate_ids = set()
    for file_hash, files in hash_to_files.items():
        if len(files) > 1:
            for filepath in files:
                filename = os.path.basename(filepath)
                duplicate_ids.add(filename)
    
    return duplicate_ids


def find_common_duplicate_ids(front_dir: str, back_dir: str) -> Set[str]:
    """
    Find IDs that have duplicates in BOTH front and back directories.
    """
    front_duplicates = get_duplicate_ids_by_directory(front_dir)
    back_duplicates = get_duplicate_ids_by_directory(back_dir)
    
    common_duplicates = front_duplicates & back_duplicates
    
    print(f"\n=== Results ===")
    print(f"Front directory duplicate IDs: {len(front_duplicates)}")
    print(f"Back directory duplicate IDs: {len(back_duplicates)}")
    print(f"Common IDs with duplicates in both: {len(common_duplicates)}")
    
    return common_duplicates


def delete_duplicates(common_ids: Set[str], front_dir: str, back_dir: str, dry_run: bool = True):
    """
    Delete duplicate files for common IDs from both directories.
    Keeps one copy of each duplicate ID and deletes the rest.
    """
    print(f"\n=== Deletion Plan ===")
    print(f"Dry run mode: {dry_run}")
    
    total_deleted = 0
    
    # Delete duplicates in front directory
    for id_name in common_ids:
        dir_path = front_dir
        filepath = os.path.join(dir_path, id_name)
        if os.path.exists(filepath):
            if dry_run:
                print(f"[DRY RUN] Would delete: {filepath}")
            else:
                os.remove(filepath)
                print(f"Deleted: {filepath}")
            total_deleted += 1
    
    # Delete duplicates in back directory
    for id_name in common_ids:
        dir_path = back_dir
        filepath = os.path.join(dir_path, id_name)
        if os.path.exists(filepath):
            if dry_run:
                print(f"[DRY RUN] Would delete: {filepath}")
            else:
                os.remove(filepath)
                print(f"Deleted: {filepath}")
            total_deleted += 1
    
    print(f"\nTotal files to delete: {total_deleted}")


def main():
    base_dir = "/home/kabin/Polygon/github/nid_check/data/images"
    front_dir = os.path.join(base_dir, "nid_front_image")
    back_dir = os.path.join(base_dir, "nid_back_image")
    
    # Find common IDs that have duplicates in both directories
    common_duplicate_ids = find_common_duplicate_ids(front_dir, back_dir)
    
    if common_duplicate_ids:
        print(f"\nCommon duplicate IDs: {sorted(list(common_duplicate_ids))[:10]}...")
        
        # First run in dry-run mode
        print("\n" + "="*50)
        print("RUNNING IN DRY-RUN MODE")
        print("="*50)
        delete_duplicates(common_duplicate_ids, front_dir, back_dir, dry_run=True)
        
        # Ask for confirmation
        response = input("\nProceed with deletion? (yes/no): ").strip().lower()
        if response == 'yes':
            print("\n" + "="*50)
            print("PROCEEDING WITH ACTUAL DELETION")
            print("="*50)
            delete_duplicates(common_duplicate_ids, front_dir, back_dir, dry_run=False)
        else:
            print("Deletion cancelled.")
    else:
        print("\nNo common duplicate IDs found!")


if __name__ == "__main__":
    main()
