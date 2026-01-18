"""Debug full image pair processing."""

import json
from pathlib import Path
from gemini_ocr import GeminiOCR

# Get first pair
front_images = list(Path("../data/images/nid_front_image").glob("*.jpg"))
front_path = front_images[0]
back_path = Path("../data/images/nid_back_image") / front_path.name

print(f"Testing image pair: {front_path.name}")
print(f"Front: {front_path}")
print(f"Back: {back_path}")
print(f"Back exists: {back_path.exists()}")

ocr = GeminiOCR()

print("\n" + "=" * 60)
print("Extracting FRONT...")
print("=" * 60)
front_data = ocr.extract_front_ocr(str(front_path))
print(f"Front data type: {type(front_data)}")
print(f"Front data: {json.dumps(front_data, ensure_ascii=False, indent=2)}")

print("\n" + "=" * 60)
print("Extracting BACK...")
print("=" * 60)
back_data = ocr.extract_back_ocr(str(back_path))
print(f"Back data type: {type(back_data)}")
print(f"Back data: {json.dumps(back_data, ensure_ascii=False, indent=2)}")

print("\n" + "=" * 60)
print("Processing PAIR...")
print("=" * 60)
combined = ocr.process_image_pair(str(front_path), str(back_path))
print(f"Combined type: {type(combined)}")
print(f"Combined data: {json.dumps(combined, ensure_ascii=False, indent=2)}")
