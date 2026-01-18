"""
Find unpaired images (front without back or back without front).
"""

import os
from pathlib import Path
from collections import defaultdict
import re


def extract_base_name(filename: str) -> str:
    """Extract base name from image filename (remove extension and trailing numbers)."""
    name_without_ext = Path(filename).stem
    base_name = re.sub(r'_\d+$', '', name_without_ext)
    return base_name


def find_unpaired_images(front_dir: str, back_dir: str):
    """Find images that don't have a corresponding pair."""
    
    # Get all base names from front images
    front_base_names = set()
    for filename in os.listdir(front_dir):
        if os.path.isfile(os.path.join(front_dir, filename)):
            base_name = extract_base_name(filename)
            front_base_names.add(base_name)
    
    # Get all base names from back images
    back_base_names = set()
    for filename in os.listdir(back_dir):
        if os.path.isfile(os.path.join(back_dir, filename)):
            base_name = extract_base_name(filename)
            back_base_names.add(base_name)
    
    # Find unpaired
    front_only = front_base_names - back_base_names
    back_only = back_base_names - front_base_names
    paired = front_base_names & back_base_names
    
    print(f"Front images: {len(front_base_names)} unique base names")
    print(f"Back images: {len(back_base_names)} unique base names")
    print(f"Paired images: {len(paired)}")
    print(f"Front-only (no back pair): {len(front_only)}")
    print(f"Back-only (no front pair): {len(back_only)}")
    
    if front_only:
        print(f"\nFront images without back pair ({len(front_only)}):")
        for name in sorted(front_only)[:20]:  # Show first 20
            print(f"  {name}")
        if len(front_only) > 20:
            print(f"  ... and {len(front_only) - 20} more")
    
    if back_only:
        print(f"\nBack images without front pair ({len(back_only)}):")
        for name in sorted(back_only)[:20]:  # Show first 20
            print(f"  {name}")
        if len(back_only) > 20:
            print(f"  ... and {len(back_only) - 20} more")


if __name__ == "__main__":
    front_dir = "data/images/nid_front_image"
    back_dir = "data/images/nid_back_image"
    
    find_unpaired_images(front_dir, back_dir)
