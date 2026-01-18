#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║           NID DATA ENTRY & EVALUATION SYSTEM - REFERENCE CARD            ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝

Three Streamlit Apps for the Complete NID Workflow
"""

print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                         📱 THREE STREAMLIT APPS                           ║
╚════════════════════════════════════════════════════════════════════════════╝


┌─ APP 1: DATA ENTRY - PERSON 1 ─────────────────────────────────────────┐
│ File:     streamlit/app_person1.py                                      │
│ Port:     8501                                                          │
│ Purpose:  Enter NID data for first 153 records                         │
│ Features:                                                               │
│   • Image preview (front/back)                                         │
│   • Manual form entry                                                  │
│   • JSON paste & auto-fill                                            │
│   • Save & navigate                                                    │
│ Output:   data/nid-data-entry-results-person1.csv                     │
│                                                                        │
│ Launch:   streamlit run streamlit/app_person1.py                      │
│ URL:      http://localhost:8501                                        │
└────────────────────────────────────────────────────────────────────────┘


┌─ APP 2: DATA ENTRY - PERSON 2 ─────────────────────────────────────────┐
│ File:     streamlit/app_person2.py                                      │
│ Port:     8502                                                          │
│ Purpose:  Enter NID data for second 154 records                        │
│ Features:                                                               │
│   • Image preview (front/back)                                         │
│   • Manual form entry                                                  │
│   • JSON paste & auto-fill                                            │
│   • Save & navigate                                                    │
│ Output:   data/nid-data-entry-results-person2.csv                     │
│                                                                        │
│ Launch:   streamlit run streamlit/app_person2.py --server.port=8502   │
│ URL:      http://localhost:8502                                        │
└────────────────────────────────────────────────────────────────────────┘


┌─ APP 3: REVIEW & EVALUATION ───────────────────────────────────────────┐
│ File:     streamlit/app_review.py                                       │
│ Port:     8501 (or custom with --server.port=XXXX)                    │
│ Purpose:  Review data entry results vs ground truth                   │
│ Features:                                                               │
│   ✓ Image preview (front/back)                                        │
│   ✓ Side-by-side comparison (actual vs predicted)                     │
│   ✓ Metrics display (accuracy, CER, WER)                              │
│   ✓ Color-coded quality (🟢🔵🟡🔴)                                      │
│   ✓ Statistics dashboard                                              │
│   ✓ Record navigation                                                 │
│   ✓ CSV export                                                        │
│ Input:    data/evaluation_results.csv (133 matched records)           │
│                                                                        │
│ Launch:   streamlit run streamlit/app_review.py                       │
│ URL:      http://localhost:8501                                        │
└────────────────────────────────────────────────────────────────────────┘


╔════════════════════════════════════════════════════════════════════════════╗
║                          🔄 WORKFLOW SEQUENCE                              ║
╚════════════════════════════════════════════════════════════════════════════╝

STEP 1: DATA ENTRY (Parallel Work)
──────────────────────────────────
Person 1:                           Person 2:
├─ App: app_person1.py              ├─ App: app_person2.py
├─ Port: 8501                       ├─ Port: 8502
├─ Records: 1-153                   ├─ Records: 154-307
├─ Method: Manual entry or JSON     ├─ Method: Manual entry or JSON
└─ Output: person1.csv              └─ Output: person2.csv

Command:
$ streamlit run streamlit/app_person1.py &
$ streamlit run streamlit/app_person2.py --server.port=8502 &


STEP 2: RUN EVALUATION
──────────────────────
$ python evaluation/evaluator.py

Process:
├─ Merge: person1.csv + person2.csv
├─ Match: Against ground truth (nid-data-140126.csv)
├─ Normalize: DOB (YYYY-MM-DD) & NID (integer)
├─ Calculate: Accuracy, CER, WER for all fields
└─ Output: evaluation_results.csv (133 matched records)


STEP 3: REVIEW RESULTS
──────────────────────
$ streamlit run streamlit/app_review.py

Features:
├─ Browse all 133 records
├─ View images (front/back)
├─ Compare actual vs predicted
├─ See metrics per field
├─ Check quality indicators
└─ Export results


╔════════════════════════════════════════════════════════════════════════════╗
║                     📊 DATA FORMATS (AS REQUIRED)                         ║
╚════════════════════════════════════════════════════════════════════════════╝

DATE OF BIRTH (DOB)
───────────────────
Format:        YYYY-MM-DD (no time)
Examples:      2001-11-21 ✓
               1973-08-31 ✓
Auto-convert:  2001/11/21 → 2001-11-21
               20011121 → 2001-11-21
Accuracy:      100% (after normalization)
Status:        ✅ CONFIRMED


NID NUMBER
──────────
Format:        Full integer (no decimals)
Examples:      6032068741 ✓
               1923701856 ✓
Auto-convert:  6032068741.0 → 6032068741
               6032 0687 41 → 6032068741
Accuracy:      100% (after normalization)
Status:        ✅ CONFIRMED


╔════════════════════════════════════════════════════════════════════════════╗
║                        📈 CURRENT METRICS                                  ║
╚════════════════════════════════════════════════════════════════════════════╝

Records Evaluated:    133 (matched against ground truth)
Average Accuracy:     95.74%
Average CER:          4.26% (Character Error Rate)
Average WER:          12.45% (Word Error Rate)

Quality Distribution:
  🟢 Excellent (≥95%):   63 records (47.4%)
  🔵 Good (80-95%):      70 records (52.6%)
  🟡 Fair (60-80%):       0 records (0%)
  🔴 Poor (<60%):         0 records (0%)

Per-Field Results (Best to Worst):
  1️⃣  DOB & NID:        100.00% (normalized perfectly)
  2️⃣  English Name:      99.86% (one of best fields)
  3️⃣  Mother Name:       97.16% (excellent)
  4️⃣  Bangla Name:       96.57% (very good)
  5️⃣  Father/Spouse:     94.31% (good)
  6️⃣  Address:           82.26% (needs review)


╔════════════════════════════════════════════════════════════════════════════╗
║                      🎨 QUALITY INDICATORS                                 ║
╚════════════════════════════════════════════════════════════════════════════╝

🟢 EXCELLENT (≥95%)
   └─ Perfect or near-perfect matches
   └─ No action needed
   └─ Green background in app

🔵 GOOD (80-95%)
   └─ Minor differences (formatting, spacing)
   └─ Review if time permits
   └─ Blue background in app

🟡 FAIR (60-80%)
   └─ Noticeable differences
   └─ Should investigate
   └─ Gold background in app

🔴 POOR (<60%)
   └─ Major differences
   └─ Requires correction
   └─ Red background in app


╔════════════════════════════════════════════════════════════════════════════╗
║                    ⚡ QUICK COMMAND REFERENCE                             ║
╚════════════════════════════════════════════════════════════════════════════╝

ACTIVATE ENVIRONMENT
$ cd /home/kabin/Polygon/github/nid_check
$ source .venv/bin/activate


LAUNCH DATA ENTRY APPS (Sequential)
$ streamlit run streamlit/app_person1.py
$ streamlit run streamlit/app_person2.py --server.port=8502


LAUNCH DATA ENTRY APPS (Background, Parallel)
$ nohup streamlit run streamlit/app_person1.py > logs/person1.log 2>&1 &
$ nohup streamlit run streamlit/app_person2.py --server.port=8502 > logs/person2.log 2>&1 &


RUN EVALUATION
$ python evaluation/evaluator.py


LAUNCH REVIEW APP
$ streamlit run streamlit/app_review.py


CHECK PROCESS STATUS
$ ps aux | grep streamlit


STOP ALL STREAMLIT APPS
$ pkill -f streamlit


VIEW EVALUATION RESULTS
$ python evaluation/summary.py


CHECK CSV DATA
$ head -2 data/evaluation_results.csv


EXPORT FOR ANALYSIS
$ python3 -c "import pandas as pd; df=pd.read_csv('data/evaluation_results.csv'); print(df[['image_id','overall_accuracy']].head(10))"


╔════════════════════════════════════════════════════════════════════════════╗
║                         📁 KEY FILE LOCATIONS                              ║
╚════════════════════════════════════════════════════════════════════════════╝

Data Entry Results:
  - Person 1: data/nid-data-entry-results-person1.csv
  - Person 2: data/nid-data-entry-results-person2.csv

Ground Truth:
  - Main: data/nid-data-140126.csv

Evaluation Output:
  - Results: data/evaluation_results.csv (133 records, 39 columns)

Images:
  - Front: data/images/nid_front_image/{image_id}.jpg
  - Back:  data/images/nid_back_image/{image_id}.jpg

App Files:
  - Person 1: streamlit/app_person1.py
  - Person 2: streamlit/app_person2.py
  - Review:   streamlit/app_review.py

Documentation:
  - Quick Start:      REVIEW_APP_QUICK_START.md
  - Setup Guide:      REVIEW_APP_SETUP.md
  - Architecture:     SYSTEM_ARCHITECTURE.py
  - App Details:      streamlit/APP_REVIEW_README.md


╔════════════════════════════════════════════════════════════════════════════╗
║                         🔍 TROUBLESHOOTING                                 ║
╚════════════════════════════════════════════════════════════════════════════╝

Q: Images not showing in review app?
A: Check that files exist in data/images/nid_front_image/ and nid_back_image/
   Image filename should match the image_id in the CSV

Q: Metrics look wrong?
A: Re-run: python evaluation/evaluator.py
   (This regenerates evaluation_results.csv)

Q: Port already in use?
A: Use --server.port=XXXX or kill existing: pkill -f streamlit

Q: Need to re-enter data?
A: Simply restart the entry app - existing entries are saved in CSV

Q: How to download all results?
A: Use the "Download All Records CSV" button in review app

Q: Data format wrong (DOB/NID)?
A: Review app and evaluator auto-normalize:
   - DOB: Converts any format to YYYY-MM-DD
   - NID: Converts to integer (removes decimals)


╔════════════════════════════════════════════════════════════════════════════╗
║                     ✅ SYSTEM READY FOR USE!                              ║
╚════════════════════════════════════════════════════════════════════════════╝

All components verified:
  ✓ Evaluation data: 133 records
  ✓ Images available: Front & Back for all records
  ✓ Data formats correct: DOB (YYYY-MM-DD), NID (integer)
  ✓ Metrics calculated: Accuracy (95.74%), CER (4.26%), WER (12.45%)
  ✓ Review app ready: Images, comparison, metrics, dashboard
  ✓ All documentation: Quick start, setup, system overview

NEXT STEPS:
1. Launch review app: streamlit run streamlit/app_review.py
2. Browse through records using sidebar
3. Review images and compare data
4. Check metrics and quality indicators
5. Export results as needed

Questions? Check documentation files:
  - REVIEW_APP_QUICK_START.md (for quick reference)
  - SYSTEM_ARCHITECTURE.py (for system overview)
  - streamlit/APP_REVIEW_README.md (for detailed docs)

""")
