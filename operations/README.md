# NID OCR Benchmark using LangChain

This module performs OCR on NID (National ID) images using Google's Gemini API via LangChain and saves the results to a CSV file.

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Key

Create a `.env` file in the operations directory:

```bash
cp .env.example .env
```

Edit `.env` and add your Gemini API key:

```
GEMINI_API_KEY=your_actual_api_key_here
```

Get your Gemini API key from: https://aistudio.google.com/app/apikey

## Usage

### Process all image pairs (777 pairs)

```bash
python3 ocr_benchmark.py
```

### Process limited number of images

```bash
python3 ocr_benchmark.py --limit 10
```

### Check statistics

```bash
python3 ocr_benchmark.py --stats
```

## How It Works

1. **Image Pair Detection**: Finds matching front and back images with the same filename
2. **Incremental Processing**: Processes one pair at a time and immediately saves to CSV
3. **Token Expiry Handling**: Each result is saved immediately after extraction, so you won't lose data if the token expires
4. **Resume Support**: Can resume from where it left off by skipping already processed IDs
5. **LangChain Integration**: Uses LangChain's ChatGoogleGenerativeAI for robust API handling
6. **Rate Limiting**: Automatically manages free tier rate limits (~15 requests/minute)

## Output

Results are saved to `../benchmark_ocr_results.csv` with the following columns:

- `image_id`: The ID of the image pair
- `english_name`: Name in English from front image
- `bangla_name`: Name in Bengali from front image
- `father_spouse_name`: Father's or spouse's name from front image
- `mother_name`: Mother's name from front image
- `dob`: Date of birth in yyyy-mm-dd format from front image
- `nid_no`: NID number from front image
- `plain_address`: Address from back image

## Features

- ✓ LangChain integration for robust API handling
- ✓ Extracts specific fields from NID images
- ✓ Processes front and back images as pairs
- ✓ Saves results immediately after each inference
- ✓ Resume capability if processing is interrupted
- ✓ Error handling with fallback to None values
- ✓ Progress tracking
- ✓ Automatic rate limiting for free tier

