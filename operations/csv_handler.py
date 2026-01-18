"""CSV handler for storing OCR results."""

import csv
from pathlib import Path
from typing import Dict, Optional


class CSVHandler:
    """Handles reading and writing OCR results to CSV."""

    FIELDNAMES = [
        "image_id",
        "english_name",
        "bangla_name",
        "father_spouse_name",
        "mother_name",
        "dob",
        "nid_no",
        "plain_address",
    ]

    def __init__(self, csv_path: str):
        """Initialize CSV handler."""
        self.csv_path = Path(csv_path)
        self.file_exists = self.csv_path.exists()
        self._init_csv()

    def _init_csv(self) -> None:
        """Initialize CSV file with headers if it doesn't exist."""
        if not self.file_exists:
            with open(self.csv_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=self.FIELDNAMES)
                writer.writeheader()

    def append_row(self, image_id: str, ocr_data: Dict[str, Optional[str]]) -> None:
        """
        Append a single row to the CSV file.

        Args:
            image_id: The image ID (filename without extension)
            ocr_data: Dictionary containing OCR extracted data
        """
        row = {"image_id": image_id}
        for field in self.FIELDNAMES[1:]:  # Skip image_id as it's already set
            row[field] = ocr_data.get(field, None)

        with open(self.csv_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.FIELDNAMES)
            writer.writerow(row)

    def get_processed_ids(self) -> set:
        """Get set of image IDs already processed."""
        if not self.file_exists or not self.csv_path.exists():
            return set()

        processed_ids = set()
        try:
            with open(self.csv_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get("image_id"):
                        processed_ids.add(row["image_id"])
        except Exception as e:
            print(f"Error reading processed IDs: {e}")

        return processed_ids
