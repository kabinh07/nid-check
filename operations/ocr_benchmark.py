"""Main script to perform OCR on NID image pairs and save to CSV."""

import os
import time
import re
from pathlib import Path
from typing import List, Tuple
from gemini_ocr import GeminiOCR
from csv_handler import CSVHandler
from config import FRONT_DIR, BACK_DIR, BENCHMARK_CSV


class OCRBenchmark:
    """Main class to orchestrate OCR processing of NID images."""

    def __init__(self):
        """Initialize OCR benchmark processor."""
        self.ocr = GeminiOCR()
        self.csv_handler = CSVHandler(str(BENCHMARK_CSV))
        self.front_dir = Path(FRONT_DIR)
        self.back_dir = Path(BACK_DIR)
        self.quota_wait_time = 90  # Default wait time in seconds (1.5 mins)

    def get_image_pairs(self) -> List[Tuple[str, Path, Path]]:
        """
        Get list of matching front and back image pairs.

        Returns:
            List of tuples (image_id, front_path, back_path)
        """
        pairs = []

        # Get all front images
        front_images = {f.stem: f for f in self.front_dir.glob("*.jpg")}
        back_images = {f.stem: f for f in self.back_dir.glob("*.jpg")}

        # Find matching pairs
        for image_id in front_images:
            if image_id in back_images:
                pairs.append(
                    (image_id, front_images[image_id], back_images[image_id])
                )

        return pairs

    def extract_retry_delay(self, error_message: str) -> int:
        """
        Extract retry delay from error message.
        
        Args:
            error_message: The error message from the API
            
        Returns:
            Retry delay in seconds, or self.quota_wait_time as default
        """
        # Look for "retryDelay" with format like 39.647s
        match = re.search(r'(\d+(?:\.\d+)?)\s*s(?:ec)?', error_message)
        if match:
            delay = int(float(match.group(1))) + 5  # Add 5 seconds buffer
            return min(delay, 600)  # Cap at 10 minutes
        return self.quota_wait_time

    def process_all_pairs(self, limit: int = None) -> None:
        """
        Process all image pairs and save results to CSV.
        Handles quota limits by waiting and retrying.

        Args:
            limit: Maximum number of pairs to process (None for all)
        """
        pairs = self.get_image_pairs()

        # Get already processed IDs to avoid reprocessing
        processed_ids = self.csv_handler.get_processed_ids()
        pairs = [(id, fp, bp) for id, fp, bp in pairs if id not in processed_ids]

        if not pairs:
            print("All images have already been processed!")
            return

        total_pairs = len(pairs)
        if limit:
            pairs = pairs[:limit]

        print(f"Found {total_pairs} image pairs")
        print(f"Processing {len(pairs)} new pairs...")
        print(f"Results will be saved to: {BENCHMARK_CSV}")
        print("-" * 60)

        index = 1
        while index <= len(pairs):
            image_id, front_path, back_path = pairs[index - 1]
            
            try:
                print(f"Processing [{index}/{len(pairs)}] {image_id}...", end=" ", flush=True)

                # Process the image pair
                ocr_data = self.ocr.process_image_pair(
                    str(front_path), str(back_path)
                )
                
                # Ensure no None values - use empty string instead
                for key in ocr_data:
                    if ocr_data[key] is None:
                        ocr_data[key] = ""

                # Immediately save to CSV
                self.csv_handler.append_row(image_id, ocr_data)

                print("✓ Saved")
                index += 1

            except Exception as e:
                error_str = str(e)
                
                # Check if it's a quota exceeded error
                if "RESOURCE_EXHAUSTED" in error_str or "429" in error_str:
                    retry_delay = self.extract_retry_delay(error_str)
                    print(f"✗ Quota exceeded!")
                    print(f"⏳ Waiting {retry_delay} seconds before retrying...")
                    
                    # Wait with countdown
                    for remaining in range(retry_delay, 0, -1):
                        print(f"\r⏳ Waiting {remaining}s...", end="", flush=True)
                        time.sleep(1)
                    print("\n✓ Resuming processing...")
                    # Retry same image without incrementing index
                    
                else:
                    print(f"✗ Error: {error_str[:100]}")
                    # Save with empty values on error
                    self.csv_handler.append_row(image_id, {
                        "english_name": "",
                        "bangla_name": "",
                        "father_spouse_name": "",
                        "mother_name": "",
                        "dob": "",
                        "nid_no": "",
                        "plain_address": "",
                    })
                    index += 1

        print("-" * 60)
        print(f"✓ Processing complete! Results saved to {BENCHMARK_CSV}")

    def get_stats(self) -> None:
        """Print statistics about processed images."""
        processed_ids = self.csv_handler.get_processed_ids()
        pairs = self.get_image_pairs()

        print(f"\nStatistics:")
        print(f"  Total image pairs available: {len(pairs)}")
        print(f"  Already processed: {len(processed_ids)}")
        print(f"  Remaining: {len(pairs) - len(processed_ids)}")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Perform OCR on NID images and save to CSV"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limit number of images to process (default: all)",
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Show statistics and exit",
    )

    args = parser.parse_args()

    benchmark = OCRBenchmark()

    if args.stats:
        benchmark.get_stats()
    else:
        print("\n" + "="*60)
        print("NID OCR Benchmark - Gemini Vision API")
        print("="*60)
        print("\nNote: Free tier has rate limits (~15 req/min)")
        print("Processing will pause if rate limits are approached.")
        print("="*60 + "\n")
        
        try:
            benchmark.process_all_pairs(limit=args.limit)
        except KeyboardInterrupt:
            print("\n\n⚠️  Processing interrupted by user")
            print("Your progress has been saved. Run the script again to resume.")
        except Exception as e:
            print(f"\n\n✗ Fatal error: {str(e)}")
            print("Your progress has been saved. Run the script again to resume.")


if __name__ == "__main__":
    main()
