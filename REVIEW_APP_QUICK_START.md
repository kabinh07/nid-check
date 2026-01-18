# 📊 New Review App - Quick Start

## What's New?

A brand new Streamlit app that lets you **review data entry results with visual comparisons**.

## App Details

**File**: `streamlit/app_review.py`  
**Purpose**: View images + compare actual vs predicted data + see metrics

## Launch It

```bash
cd /home/kabin/Polygon/github/nid_check
source .venv/bin/activate
streamlit run streamlit/app_review.py
```

**URL**: http://localhost:8501

Or run on port 8503:
```bash
streamlit run streamlit/app_review.py --server.port=8503
```

## What It Shows

### 1. **Images** (Top)
```
[Front Image]  [Back Image]
```
- NID card front and back preview
- Based on record ID

### 2. **Data Comparison** (Middle)
```
English Name          Bangla Name
┌──────────────────┐ ┌──────────────────┐
│ ACTUAL DATA:     │ │ PREDICTED DATA:  │
│ Mohammad Nashib  │ │ Mohammad Nashib  │
│                  │ │                  │
│ METRICS:         │ │ METRICS:         │
│ 99.86% Accuracy  │ │ CER: 0.14%       │
│ WER: 1.04%       │ │                  │
└──────────────────┘ └──────────────────┘
```

- Left: What users entered
- Right: Ground truth from CSV
- Color-coded accuracy (🟢 Good / 🔵 Excellent / etc.)

### 3. **Metrics Summary** (Bottom)
```
OVERALL: 95.74% Accuracy | 4.26% CER | 12.45% WER
```

Plus charts showing quality distribution and per-field accuracy.

## Navigation

**Sidebar Options:**
- 🔢 Select record number (1 to 133)
- 🎯 Filter by quality tier
- 📊 View total records

**Buttons:**
- ⬅️ Previous Record
- ➡️ Next Record
- 🔄 Refresh
- 📥 Download Report (all records as CSV)

## Format Details

### Date of Birth
- **Format**: `YYYY-MM-DD` (no time)
- **Examples**: 2001-11-21, 1973-08-31
- **Auto-normalized** from: 2001/11/21, 20011121, etc.

### NID Number
- **Format**: Full integers only
- **Examples**: 6032068741, 1923701856
- **Auto-normalized** (removes decimals, spaces, dashes)

## Quality Indicators

🟢 **Excellent** (≥95%)
- Perfect or near-perfect match
- Green background

🔵 **Good** (80-95%)
- Minor differences (formatting, spelling)
- Blue background

🟡 **Fair** (60-80%)
- Noticeable differences
- Gold background

🔴 **Poor** (<60%)
- Major differences
- Red background

## Metrics Explained

| Metric | Meaning | Good Value |
|--------|---------|-----------|
| **Accuracy** | How similar are the values? | >95% |
| **CER** | Character Error Rate | <5% |
| **WER** | Word Error Rate | <20% |

## Example Workflow

1. **Open app** → http://localhost:8501
2. **Pick record** → Use sidebar (or Next button)
3. **See images** → Front and back cards
4. **Compare data** → Actual vs Predicted
5. **Check metrics** → Accuracy, CER, WER
6. **Note issues** → If quality is poor
7. **Move on** → Next Record button
8. **Export** → Download CSV when done

## Files Generated

After running `evaluator.py`:
- ✅ `data/evaluation_results.csv` - Main evaluation data
- ✅ All 133 records with metrics
- ✅ Ready for the review app

## Key Improvements in New Data

✅ **DOB Accuracy**: 100% (was 80%)
- Normalized to YYYY-MM-DD format
- All date formats converted consistently

✅ **NID Accuracy**: 100% (was 91%)
- Normalized to integer (no decimals)
- Removed all non-digit characters

✅ **Overall Accuracy**: 95.74% (was 91.60%)
- Better data quality insight
- More accurate metrics

## Performance

- Load time: ~2-3 seconds
- Image display: <1 second per record
- Responsive navigation
- Tested with 133+ records

## Files Involved

```
streamlit/
├── app_review.py              ← NEW: Review and compare app
├── APP_REVIEW_README.md       ← NEW: Detailed documentation
├── app_person1.py             (existing)
├── app_person2.py             (existing)
└── ...

data/
├── evaluation_results.csv     ← Updated with normalized formats
└── images/
    ├── nid_front_image/
    └── nid_back_image/

evaluation/
└── evaluator.py               ← Updated with normalization functions
```

## Quick Commands

**View the app:**
```bash
streamlit run streamlit/app_review.py
```

**Re-run evaluation:**
```bash
python evaluation/evaluator.py
```

**Check DOB/NID formats:**
```bash
python3 -c "import pandas as pd; df = pd.read_csv('data/evaluation_results.csv'); print(df[['actual_dob', 'actual_nid_no']].head())"
```

---

**New Features Summary:**
- 📸 Image preview
- 👀 Side-by-side comparison
- 📊 Visual metrics
- 🎨 Color-coded quality
- 🔄 Easy navigation
- ⬇️ Download export
- 📈 Quality dashboard

Enjoy! 🚀
