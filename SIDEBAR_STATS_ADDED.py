#!/usr/bin/env python3
"""
Sidebar Overall Statistics Preview
"""

print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║               ✅ SIDEBAR OVERALL STATISTICS ADDED                         ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝


📊 SIDEBAR LAYOUT (Updated)
════════════════════════════════════════════════════════════════════════════

[Streamlit Sidebar]

📍 Navigation
   ├─ Select Record # [_____]

───────────────────────────────────────

📊 Overall Statistics        ← NEW
   ├─ Total Records: 133
   ├─ Avg Accuracy: 95.74%
   ├─ Avg CER: 4.26%
   ├─ Avg WER: 12.45%
   │
   ├─ Quality Distribution:
   │  ├─ 🟢 Excellent: 87 (65.4%)
   │  ├─ 🔵 Good: 46 (34.6%)
   │  ├─ 🟡 Fair: 0 (0.0%)
   │  └─ 🔴 Poor: 0 (0.0%)
   │
   └─ Per-Field Accuracy:     ← Sorted by accuracy
      ├─ 🟢 DOB: 100.0%
      ├─ 🟢 NID: 100.0%
      ├─ 🟢 English Name: 99.9%
      ├─ 🟢 Mother: 97.2%
      ├─ 🟢 Bangla Name: 96.6%
      ├─ 🔵 Father/Spouse: 94.3%
      └─ 🔵 Address: 82.3%

───────────────────────────────────────

🔍 Filters
   ├─ Filter by Quality Tier
   │  ├─ ☑ 🟢 Excellent (≥95%)
   │  ├─ ☑ 🔵 Good (80-95%)
   │  ├─ ☑ 🟡 Fair (60-80%)
   │  └─ ☑ 🔴 Poor (<60%)
   
───────────────────────────────────────
ℹ️  Data Source: evaluation_results.csv


🎨 FEATURES
════════════════════════════════════════════════════════════════════════════

✓ Total Records Count
  └─ Shows 133 records in dataset

✓ Overall Accuracy Metrics
  ├─ Average Accuracy (95.74%)
  ├─ Average CER (4.26%)
  └─ Average WER (12.45%)

✓ Quality Distribution
  ├─ Excellent count & percentage
  ├─ Good count & percentage
  ├─ Fair count & percentage
  └─ Poor count & percentage

✓ Per-Field Accuracy Ranking
  ├─ Sorted from highest to lowest
  ├─ Color-coded indicators (🟢🔵🟡🔴)
  └─ All 7 fields displayed

✓ Easy at-a-glance Summary
  └─ All stats visible without scrolling


💡 HOW TO USE
════════════════════════════════════════════════════════════════════════════

1. Open the Review App
   $ streamlit run streamlit/app_review.py

2. Look at the SIDEBAR (left side)
   - You'll see the new "📊 Overall Statistics" section at the top
   - Shows stats for ALL 133 records

3. Use Navigation
   - Select individual records (1-133)
   - Browse through with Next/Previous buttons
   - Review specific data

4. Apply Filters
   - Use quality tier filters below the statistics
   - Filter to show only Excellent, Good, Fair, or Poor records


📱 WHAT YOU'LL SEE
════════════════════════════════════════════════════════════════════════════

ALWAYS VISIBLE in Sidebar:
  ✓ Total Records: 133
  ✓ Avg Accuracy: 95.74%
  ✓ Avg CER: 4.26%
  ✓ Avg WER: 12.45%
  ✓ 4 Quality metrics
  ✓ 7 Per-field scores
  ✓ Quality distribution

CHANGES WITH RECORD SELECTION:
  • Main view shows selected record's data
  • Images change (front/back)
  • Field comparison updates
  • Individual metrics update
  • SIDEBAR STATS STAY THE SAME (all 133 stats)


🎯 BENEFITS
════════════════════════════════════════════════════════════════════════════

1. Quick Overview
   └─ All 133 records stats visible at a glance

2. Context Aware
   └─ Understand overall quality while reviewing individual records

3. Performance Ranking
   └─ See which fields perform best/worst

4. Quality Assessment
   └─ Quickly identify data quality distribution

5. Comparison Point
   └─ Compare individual record to overall average

6. No Need to Scroll
   └─ Stats compact and always visible


✅ VERIFICATION
════════════════════════════════════════════════════════════════════════════

File Updated:     streamlit/app_review.py ✓
Lines Added:      ~80 lines ✓
New Section:      📊 Overall Statistics ✓
Position:         Sidebar (left panel) ✓
Visibility:       Always displayed ✓
Data Source:      evaluation_results.csv ✓
Metrics Shown:    10+ different stats ✓

Quality Indicators:
  🟢 Green:   ≥95% accuracy
  🔵 Blue:    80-95% accuracy
  🟡 Gold:    60-80% accuracy
  🔴 Red:     <60% accuracy


════════════════════════════════════════════════════════════════════════════

To launch and see the changes:

  $ cd /home/kabin/Polygon/github/nid_check
  $ source .venv/bin/activate
  $ streamlit run streamlit/app_review.py

The sidebar will show all overall statistics for the 133 records!

════════════════════════════════════════════════════════════════════════════
""")
