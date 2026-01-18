# NID Data Review & Evaluation Viewer

A comprehensive Streamlit application for reviewing and comparing NID (National ID) data entry results against ground truth with visual metrics.

## Features

✅ **Image Preview**
- Display front and back NID card images side-by-side
- Auto-load images based on record ID

✅ **Side-by-Side Comparison**
- **Left Column**: Actual data (entered by users)
- **Right Column**: Predicted data (ground truth from original CSV)
- **Metrics**: Accuracy, Character Error Rate (CER), Word Error Rate (WER)

✅ **Color-Coded Quality Indicators**
- 🟢 **Excellent**: ≥95% accuracy (light green)
- 🔵 **Good**: 80-95% accuracy (sky blue)
- 🟡 **Fair**: 60-80% accuracy (gold)
- 🔴 **Poor**: <60% accuracy (light red)

✅ **Record Navigation**
- Select any record by number
- Previous/Next buttons for sequential browsing
- Current position display (Record #X of Total)

✅ **Statistical Dashboard**
- Overall evaluation metrics summary
- Quality distribution chart
- Per-field accuracy breakdown
- Average CER and WER statistics

✅ **Data Download**
- Export all evaluation results as CSV
- Full metrics available for further analysis

## Running the App

### Option 1: Direct Launch
```bash
cd /home/kabin/Polygon/github/nid_check
source .venv/bin/activate
streamlit run streamlit/app_review.py
```

### Option 2: Background Process
```bash
nohup streamlit run streamlit/app_review.py --server.port=8503 > app_review.log 2>&1 &
```

Default URL: `http://localhost:8501`

## Data Structure

The app reads from `data/evaluation_results.csv` which contains:

### Columns (per record):
- `image_id`: Unique identifier from NID image
- `actual_*`: Data entered by user (7 fields)
- `predicted_*`: Ground truth from original dataset (7 fields)
- `*_accuracy`: Similarity percentage (0-100%)
- `*_cer`: Character Error Rate (0-100%)
- `*_wer`: Word Error Rate (0-100%)
- `overall_*`: Averages across all 7 fields

### Fields Evaluated:
1. **English Name** - Person's name in English
2. **Bangla Name** - Person's name in Bangla
3. **Father/Spouse** - Father or spouse name
4. **Mother** - Mother's name
5. **Date of Birth** - YYYY-MM-DD format
6. **NID Number** - Full integer (no decimals)
7. **Address** - Complete address

## Metrics Explained

### Accuracy (%)
- **Definition**: Similarity ratio between actual and predicted values
- **Scale**: 0-100%
- **Interpretation**:
  - 100% = Perfect match
  - 95%+ = Excellent quality
  - 80%+ = Good quality
  - <60% = Needs review

### Character Error Rate (CER, %)
- **Definition**: Percentage of characters that differ at character level
- **Scale**: 0-100%
- **Interpretation**:
  - 0% = No character differences
  - <5% = Excellent
  - <10% = Good
  - >20% = Significant issues

### Word Error Rate (WER, %)
- **Definition**: Percentage of words that differ when split by spaces
- **Scale**: 0-100%
- **Interpretation**:
  - 0% = All words match
  - <20% = Good
  - 50%+ = Many word mismatches
  - 100% = Completely different word lists

## Quality Tiers

### 🟢 Excellent (≥95%)
- Minimal differences
- No manual review needed
- High confidence in entry quality

### 🔵 Good (80-95%)
- Minor differences likely due to formatting
- Review recommended but not critical
- Examples: "2001-11-21" vs "2001/11/21"

### 🟡 Fair (60-80%)
- Noticeable differences
- Should be reviewed
- May require data correction

### 🔴 Poor (<60%)
- Significant differences
- Requires immediate review
- Likely data entry errors or OCR issues

## Special Formatting

### Date of Birth
- **Format**: YYYY-MM-DD (e.g., 2001-11-21)
- **Normalization**: App automatically converts:
  - 2001/11/21 → 2001-11-21
  - 20011121 → 2001-11-21
  - Other formats as detected

### NID Number
- **Format**: Full integer, no decimals (e.g., 6032068741)
- **Normalization**: App automatically:
  - Removes decimal points (6032068741.0 → 6032068741)
  - Removes spaces and dashes
  - Keeps only digits

## Navigation & UI

### Sidebar
- **Record Selector**: Jump to any record (1 to Total)
- **Quality Filter**: Show only certain quality tiers
- **Info Display**: Total records count

### Main View
1. **Images Section**: Front and back NID cards
2. **Comparison Section**: Detailed field-by-field comparison
3. **Metrics Section**: Overall accuracy summary
4. **Statistics Section**: Dashboard with charts
5. **Navigation Buttons**: Move through records

### Color Scheme
- **Header**: Dark blue
- **Excellent**: Light green (#90EE90)
- **Good**: Sky blue (#87CEEB)
- **Fair**: Gold (#FFD700)
- **Poor**: Light red (#FFB6C1)

## Usage Tips

### Review Workflow
1. Open the app: `streamlit run streamlit/app_review.py`
2. Navigate to a record using the sidebar selector
3. Check images on top
4. Review field-by-field comparison
5. Note any discrepancies for follow-up

### Finding Problem Records
1. Look for 🔴 Poor quality indicators
2. Focus on fields with <80% accuracy
3. Check CER/WER for detailed differences
4. Images help understand OCR vs entry errors

### Batch Review
1. Use "Previous" and "Next" buttons
2. Quickly scan through all records
3. Mark problematic ones for investigation
4. Use download button to export for analysis

## Performance Notes

- **Load Time**: 2-3 seconds (first load, cached after)
- **Image Loading**: Depends on disk I/O (typically <1s)
- **Large Datasets**: Tested with 130+ records, scales well
- **Memory**: ~200MB for typical dataset

## Troubleshooting

### Images Not Loading
- Check images exist in `data/images/nid_front_image/` and `nid_back_image/`
- Verify image filename matches record image_id
- Check file permissions

### CSV Not Found
- Verify `evaluation_results.csv` exists in `data/` directory
- Run evaluation module first: `python evaluation/evaluator.py`
- Check file path in code if moved

### Metrics Not Calculating
- Verify CSV format with all required columns
- Check for missing values (NaN)
- Ensure normalization functions are working

### Slow Performance
- Clear Streamlit cache: `rm -rf ~/.streamlit/cache`
- Restart the app
- Check system resources (RAM, CPU)

## Example Records

### Excellent Record (98% Accuracy)
```
English Name: "MOHAMMAD NASHIB SIAM" (Actual) = "MOHAMMAD NASHIB SIAM" (Predicted)
Bangla Name: "মোহাম্মদ নাশিব সিয়াম" (Actual) = "মোহাম্মদ নাশিব সিয়াম" (Predicted)
DOB: 2001-11-21 (Perfect match, normalized)
NID: 6032068741 (Perfect match, no decimals)
Overall Accuracy: 98%+ → 🟢 Excellent
```

### Good Record (87% Accuracy)
```
English Name: "MEHNAZ MANNAN" (Actual) vs "MEHNAZ MANNAH" (Predicted)
Address: Slightly different text (abbreviations, spacing)
Overall Accuracy: 87% → 🔵 Good
```

## Advanced Features

### Filters (Sidebar)
- Select multiple quality tiers at once
- Combine with record selector for targeted review

### Statistics Dashboard
- Real-time calculation of all metrics
- Per-field accuracy ranking (best to worst)
- Quality distribution visualization

### Download Export
- Click "Download All Records CSV"
- Use for external analysis, reporting, or appeals

## System Requirements

- **Python**: 3.8+
- **Streamlit**: 1.28+
- **Pandas**: 2.0+
- **PIL**: Latest
- **RAM**: 512MB minimum
- **Display**: Any modern browser (Chrome, Firefox, Safari)

## File Dependencies

```
nid_check/
├── data/
│   ├── evaluation_results.csv      (Required)
│   └── images/
│       ├── nid_front_image/        (Required)
│       └── nid_back_image/         (Required)
└── streamlit/
    └── app_review.py               (This file)
```

## Support

For issues or questions:
1. Check troubleshooting section above
2. Verify all data files exist and are readable
3. Check app logs for error messages
4. Review evaluation module documentation

---

**Created**: January 2026
**Purpose**: NID Data Entry Quality Review & Evaluation
**Status**: Production Ready
