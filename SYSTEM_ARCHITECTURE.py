"""
Complete NID Data Entry & Evaluation System Architecture
========================================================

This document outlines the entire workflow from data filtering through
final quality assessment with image-based review.
"""

SYSTEM_OVERVIEW = """
┌─────────────────────────────────────────────────────────────────────────────┐
│                    NID DATA PROCESSING PIPELINE                             │
└─────────────────────────────────────────────────────────────────────────────┘

PHASE 1: DATA PREPARATION
├─ Input: nid-data-140126.csv (original full dataset, 307 filtered to last 15 days)
├─ Process: filter_last_15_days.py
│   └─ Filters by doc_date column
│   └─ Output: 307 records in CSV format
├─ Storage: data/nid-data-140126.csv (ground truth)
└─ Image Assets: data/images/nid_front_image/ + nid_back_image/

PHASE 2: DATA SPLITTING FOR PARALLEL WORK
├─ Input: nid-data-140126.csv (307 records)
├─ Process: Split into two equal parts
│   ├─ Part 1: nid-data-part1.csv (153 records)
│   └─ Part 2: nid-data-part2.csv (154 records)
├─ Purpose: Two people work simultaneously on same dataset
└─ Storage: data/nid-data-part*.csv

PHASE 3: DATA ENTRY (TWO PARALLEL STREAMLIT APPS)

App Person 1 (Port 8501)                App Person 2 (Port 8502)
├─ File: streamlit/app_person1.py       ├─ File: streamlit/app_person2.py
├─ Input: nid-data-part1.csv            ├─ Input: nid-data-part2.csv
├─ Features:                            ├─ Features:
│  ├─ Image preview (front/back)        │  ├─ Image preview (front/back)
│  ├─ JSON text area for paste          │  ├─ JSON text area for paste
│  ├─ Auto-fill from JSON               │  ├─ Auto-fill from JSON
│  ├─ Manual form entry                 │  ├─ Manual form entry
│  └─ Navigation (Prev/Save/Next/Skip)  │  └─ Navigation (Prev/Save/Next/Skip)
└─ Output: nid-data-entry-results-      └─ Output: nid-data-entry-results-
   person1.csv                             person2.csv

PHASE 4: EVALUATION & METRICS CALCULATION

Input Files:
├─ nid-data-entry-results-person1.csv (entered data from person 1)
├─ nid-data-entry-results-person2.csv (entered data from person 2)
└─ nid-data-140126.csv (ground truth)

Process: evaluation/evaluator.py
├─ Merge Results
│  └─ Combines both person's results into single dataset
├─ Record Matching
│  ├─ Primary: Match by image_id
│  └─ Fallback: Match by NID number
├─ Field Normalization
│  ├─ DOB: Convert to YYYY-MM-DD (handles YYYY/MM/DD, YYYYMMDD, etc.)
│  └─ NID: Convert to integer (removes decimals, spaces, dashes)
├─ Metric Calculation (per field)
│  ├─ Accuracy: Similarity ratio (0-100%)
│  ├─ CER: Character Error Rate (0-100%)
│  └─ WER: Word Error Rate (0-100%)
└─ Output: data/evaluation_results.csv

Output Structure:
┌──────────────────────────────────────────────────────────────────┐
│ image_id │ actual_* (7 fields) │ predicted_* (7 fields) │ metrics │
├──────────────────────────────────────────────────────────────────┤
│ For Each of 7 Fields:                                            │
│ ├─ *_accuracy (0-100%)                                          │
│ ├─ *_cer (0-100%)                                               │
│ └─ *_wer (0-100%)                                               │
├──────────────────────────────────────────────────────────────────┤
│ Overall Statistics:                                              │
│ ├─ overall_accuracy (avg of 7 fields)                           │
│ ├─ overall_cer (avg of 7 fields)                                │
│ └─ overall_wer (avg of 7 fields)                                │
└──────────────────────────────────────────────────────────────────┘

PHASE 5: DATA REVIEW & VISUALIZATION

File: streamlit/app_review.py (Port 8501 or custom)

Features:
├─ Image Display
│  ├─ Front NID card
│  └─ Back NID card
├─ Data Comparison (Side-by-Side)
│  ├─ Left: Actual (entered data)
│  ├─ Right: Predicted (ground truth)
│  └─ Metrics: Accuracy, CER, WER per field
├─ Quality Indicators
│  ├─ 🟢 Excellent (≥95%)
│  ├─ 🔵 Good (80-95%)
│  ├─ 🟡 Fair (60-80%)
│  └─ 🔴 Poor (<60%)
├─ Navigation
│  ├─ Record selector (1-133)
│  ├─ Previous/Next buttons
│  └─ Quality filters
└─ Statistics Dashboard
   ├─ Overall metrics
   ├─ Quality distribution chart
   ├─ Per-field accuracy ranking
   └─ Download export button
"""

SYSTEM_COMPONENTS = """
FILE INVENTORY
==============

ROOT DIRECTORY
├─ filter_last_15_days.py              [PHASE 1] Data filtering
├─ find_unpaired_images.py             Support utility
├─ find_delete_duplicates.py            Support utility
├─ filter_images_by_csv.py             Support utility
├─ REVIEW_APP_QUICK_START.md           [NEW] Quick reference
├─ benchmark_ocr_results.csv           Support data

DATA DIRECTORY (data/)
├─ nid-data-140126.csv                 [Phase 1] Ground truth (307 records)
├─ nid-data-part1.csv                  [Phase 2] First half (153 records)
├─ nid-data-part2.csv                  [Phase 2] Second half (154 records)
├─ nid-data-entry-results-person1.csv  [Phase 3] Person 1 entries
├─ nid-data-entry-results-person2.csv  [Phase 3] Person 2 entries
├─ evaluation_results.csv              [Phase 4] Final evaluation (133 matched)
└─ images/
   ├─ nid_front_image/                 Front images (named by image_id)
   └─ nid_back_image/                  Back images (named by image_id)

STREAMLIT DIRECTORY (streamlit/)
├─ app_person1.py                      [Phase 3] Data entry for person 1
├─ app_person2.py                      [Phase 3] Data entry for person 2
├─ app_review.py                       [Phase 5] Review & comparison viewer
└─ APP_REVIEW_README.md                [Phase 5] Detailed documentation

EVALUATION DIRECTORY (evaluation/)
├─ evaluator.py                        [Phase 4] Main evaluation engine
├─ summary.py                          Support statistics
├─ __init__.py                         Module interface
├─ requirements.txt                    Dependencies
├─ README.md                           Module documentation
├─ QUICKSTART.py                       Quick reference guide
└─ LANGCHAIN_MIGRATION.md              Legacy notes

OPERATIONS DIRECTORY (operations/)
├─ config.py                           Configuration
├─ csv_handler.py                      CSV utilities
├─ gemini_ocr.py                       OCR integration
├─ ocr_benchmark.py                    OCR testing
├─ debug_*.py                          Debugging utilities
├─ test_api_key.py                     API testing
└─ ...
"""

DATA_FLOW = """
DATA FLOW DIAGRAM
=================

Input Data
    ↓
[Phase 1: Filter by Date]
    ↓
307 Records (Last 15 Days)
    ↓
┌───────────────────────────────────────────┐
│          [Phase 2: Split Data]            │
└───────────────────────────────────────────┘
    ↙                                   ↘
153 Records                            154 Records
    ↓                                      ↓
┌─────────────────────┐            ┌─────────────────────┐
│  [Phase 3: Entry]   │            │  [Phase 3: Entry]   │
│  app_person1.py     │            │  app_person2.py     │
│  + Images           │            │  + Images           │
│  + JSON Parser      │            │  + JSON Parser      │
└─────────────────────┘            └─────────────────────┘
    ↓                                      ↓
Entry Results 1                     Entry Results 2
(Actual Data)                       (Actual Data)
    ↓                                      ↓
    └──────────────────────┬───────────────┘
                           ↓
        ┌──────────────────────────────────┐
        │     [Phase 4: Evaluation]        │
        │ Merge + Match + Calculate Metrics │
        │     evaluator.py                 │
        └──────────────────────────────────┘
                           ↓
        Ground Truth (nid-data-140126.csv)
        (Predicted Data)
                           ↓
        ┌──────────────────────────────────┐
        │   evaluation_results.csv         │
        │   133 Matched Records             │
        │   + Normalization                │
        │   + Metrics (21 columns)         │
        └──────────────────────────────────┘
                           ↓
        ┌──────────────────────────────────┐
        │     [Phase 5: Review]            │
        │      app_review.py               │
        │   + Image Preview                │
        │   + Side-by-side Comparison      │
        │   + Color-coded Metrics          │
        │   + Statistics Dashboard         │
        └──────────────────────────────────┘
                           ↓
                    Final Review
                   & Validation
"""

FORMATS_AND_STANDARDS = """
DATA FORMATS & STANDARDS
========================

CSV Format
├─ Encoding: UTF-8
├─ Separator: Tab (\\t) for main data, Comma for results
├─ Quote char: "
└─ No time stamps

Field Formats
├─ English Name
│  └─ Free text (mixed case)
│  └─ Example: "MOHAMMAD NASHIB SIAM"
├─ Bangla Name
│  └─ Bengali characters (UTF-8)
│  └─ Example: "মোহাম্মদ নাশিব সিয়াম"
├─ Father/Spouse Name
│  └─ Bengali or English
│  └─ Example: "মোহাম্মদ ফরহাদ কামাল"
├─ Mother Name
│  └─ Bengali or English
│  └─ Example: "মাসুমা বেগম"
├─ Date of Birth
│  └─ Format: YYYY-MM-DD (no time)
│  └─ Auto-normalized from: YYYY/MM/DD, YYYYMMDD, etc.
│  └─ Example: "2001-11-21"
├─ NID Number
│  └─ 17-digit integer (no decimals)
│  └─ Auto-normalized (removes .0, spaces, dashes)
│  └─ Example: "6032068741"
└─ Address
   └─ Bengali or English
   └─ Example: "বাসা/হোল্ডিং: ১২৩১, গ্রাম/রাস্তা: সেনপাড়া..."

Image Naming
├─ Front image: {image_id}.jpg
│  └─ Location: data/images/nid_front_image/
│  └─ Example: 1767118881785862.jpg
└─ Back image: {image_id}.jpg
   └─ Location: data/images/nid_back_image/
   └─ Example: 1767118881785862.jpg

Metrics Standards
├─ Accuracy: 0-100% (similarity ratio)
├─ CER: 0-100% (character error rate, lower is better)
├─ WER: 0-100% (word error rate, lower is better)
└─ All metrics rounded to 2 decimal places
"""

CURRENT_STATUS = """
COMPLETION STATUS
=================

✅ COMPLETED PHASES
├─ Phase 1: Data Filtering
│  └─ filter_last_15_days.py working
│  └─ 307 records extracted from last 15 days
├─ Phase 2: Data Splitting
│  └─ Split into 153 + 154 records
│  └─ Ready for parallel work
├─ Phase 3: Data Entry Apps
│  └─ app_person1.py (port 8501) - Functional
│  └─ app_person2.py (port 8502) - Functional
│  └─ JSON parser implemented
│  └─ Image preview working
│  └─ Results saved to CSV
├─ Phase 4: Evaluation Module
│  └─ evaluator.py - Complete
│  └─ Metrics calculation - All 3 types
│  └─ Record matching - Image ID + NID fallback
│  └─ DOB normalization - YYYY-MM-DD format
│  └─ NID normalization - Integer format
│  └─ 133 records matched & evaluated
│  └─ Results saved with 21 metric columns
└─ Phase 5: Review App
   └─ app_review.py - NEW & WORKING
   └─ Image preview - Both sides
   └─ Side-by-side comparison - Full
   └─ Color-coded quality - Implemented
   └─ Statistics dashboard - Complete
   └─ Navigation - Full support

📊 CURRENT METRICS (from latest evaluation run)
├─ Total Matched Records: 133
├─ Average Accuracy: 95.74%
├─ Average CER: 4.26%
├─ Average WER: 12.45%
├─ Quality Distribution:
│  ├─ Excellent (≥95%): 63 records (47.4%)
│  ├─ Good (80-95%): 70 records (52.6%)
│  ├─ Fair/Poor: 0 records (0%)
└─ Per-Field Best to Worst:
   ├─ Best: DOB & NID (100% - normalized)
   ├─ Excellent: English Name (99.86%)
   ├─ Good: Mother (97.16%), Bangla Name (96.57%)
   ├─ Average: Father/Spouse (94.31%)
   └─ Needs Work: Address (82.26%)

🚀 READY TO USE APPS
├─ Entry Apps (Streamlit):
│  ├─ Person 1: streamlit run streamlit/app_person1.py
│  ├─ Person 2: streamlit run streamlit/app_person2.py
│  └─ Review: streamlit run streamlit/app_review.py
├─ Evaluation Engine:
│  └─ python evaluation/evaluator.py
└─ Statistics:
   └─ python evaluation/summary.py
"""

QUICK_START = """
GETTING STARTED
===============

1. RUN EVALUATION (if data entry is complete)
   ──────────────────────────────────────────
   $ cd /home/kabin/Polygon/github/nid_check
   $ source .venv/bin/activate
   $ python evaluation/evaluator.py
   ↓ Generates: data/evaluation_results.csv

2. LAUNCH REVIEW APP
   ────────────────────
   $ streamlit run streamlit/app_review.py
   ↓ Opens: http://localhost:8501

3. REVIEW RECORDS
   ───────────────
   • Use sidebar to select record
   • View images (front/back)
   • Compare actual vs predicted
   • Check accuracy metrics
   • Navigate with Previous/Next buttons

4. EXPORT RESULTS
   ───────────────
   • Click "Download All Records CSV"
   • Use for reports or further analysis

PRODUCTION SETUP
================

Run Entry Apps in Background:

$ nohup streamlit run streamlit/app_person1.py --server.port=8501 > logs/person1.log 2>&1 &
$ nohup streamlit run streamlit/app_person2.py --server.port=8502 > logs/person2.log 2>&1 &
$ nohup streamlit run streamlit/app_review.py --server.port=8503 > logs/review.log 2>&1 &

Check Status:
$ ps aux | grep streamlit

Stop All:
$ pkill -f streamlit
"""

if __name__ == "__main__":
    print(__doc__)
    print("\n" + "="*80)
    print(SYSTEM_OVERVIEW)
    print("\n" + "="*80)
    print(SYSTEM_COMPONENTS)
    print("\n" + "="*80)
    print(DATA_FLOW)
    print("\n" + "="*80)
    print(FORMATS_AND_STANDARDS)
    print("\n" + "="*80)
    print(CURRENT_STATUS)
    print("\n" + "="*80)
    print(QUICK_START)
