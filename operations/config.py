"""Configuration module for loading environment variables."""

import os
from pathlib import Path
from dotenv import load_dotenv

# First try to get from environment variable (exported)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# If not in environment, load from .env file
if not GEMINI_API_KEY:
    env_path = Path(__file__).parent / ".env"
    load_dotenv(env_path)
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found in environment or .env file. "
        "Please set GEMINI_API_KEY environment variable or create a .env file with your Gemini API key."
    )

# Paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data" / "images"
FRONT_DIR = DATA_DIR / "nid_front_image"
BACK_DIR = DATA_DIR / "nid_back_image"
BENCHMARK_CSV = BASE_DIR / "benchmark_ocr_results.csv"
