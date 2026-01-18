# NID Evaluation Module

Comprehensive evaluation of NID data entry results against ground truth data with detailed quality metrics.

## Overview

This module:
1. **Merges** results from both Person 1 and Person 2 CSV files
2. **Matches** records with ground truth data (nid-data-140126.csv)
3. **Calculates** accuracy metrics including:
   - **Accuracy**: Field-level and overall match percentage
   - **CER (Character Error Rate)**: Character-level differences
   - **WER (Word Error Rate)**: Word-level differences
4. **Generates** detailed CSV report with all comparisons

## Features

- ✅ Automatic record matching by NID number or image ID
- ✅ Per-field accuracy analysis
- ✅ Character and word-level error metrics
- ✅ Comprehensive statistical summaries
- ✅ Quality tier classification (Excellent/Good/Fair/Poor)

## Installation

```bash
cd evaluation
pip install -r requirements.txt
```

## Usage

### Quick Start (CLI)

Run the full evaluation:
```bash
python evaluator.py
```

View summary statistics:
```bash
python summary.py
```

### As a Python Module

```python
from evaluation import ResultsEvaluator, print_summary

# Run evaluation
evaluator = ResultsEvaluator(
    person1_csv='data/nid-data-entry-results-person1.csv',
    person2_csv='data/nid-data-entry-results-person2.csv',
    ground_truth_csv='data/nid-data-140126.csv'
)

# Generate report
results_df = evaluator.generate_report('data/evaluation_results.csv')

# Print summary
print_summary('data/evaluation_results.csv')
```

## Output Format

### CSV Columns

**Actual Values (Entered Data):**
- `image_id` - Image identifier
- `actual_english_name` - English name entered
- `actual_bangla_name` - Bangla name entered
- `actual_father_spouse` - Father/Spouse name entered
- `actual_mother` - Mother name entered
- `actual_dob` - Date of birth entered
- `actual_nid_no` - NID number entered
- `actual_address` - Address entered

**Predicted Values (Ground Truth):**
- `predicted_english_name` - Ground truth English name
- `predicted_bangla_name` - Ground truth Bangla name
- `predicted_father_spouse` - Ground truth father/spouse name
- `predicted_mother` - Ground truth mother name
- `predicted_dob` - Ground truth date of birth
- `predicted_nid_no` - Ground truth NID number
- `predicted_address` - Ground truth address

**Metrics (for each field):**
- `{field}_accuracy` - Similarity percentage (0-100%)
- `{field}_cer` - Character Error Rate (0-100%)
- `{field}_wer` - Word Error Rate (0-100%)

**Overall Metrics:**
- `overall_accuracy` - Average accuracy across all fields
- `overall_cer` - Average Character Error Rate
- `overall_wer` - Average Word Error Rate

## Metrics Explanation

### Accuracy (0-100%)
Similarity ratio between actual and predicted values:
- 100% = Exact match
- 0% = Completely different
- Calculated using sequence matching algorithm

### CER - Character Error Rate (0-100%)
Measures character-level differences:
- 0% = Perfect match at character level
- Higher % = More character-level differences
- Useful for detecting typos and small errors

### WER - Word Error Rate (0-100%)
Measures word-level differences:
- 0% = All words match
- 100% = No words match
- Useful for detecting structural differences

## Example Output

```
====================================================================================================
DETAILED EVALUATION SUMMARY
====================================================================================================

📊 OVERALL STATISTICS
Total Records Evaluated: 133

Accuracy Metrics:
  • Average Accuracy:   91.60%  (min:  84.90%, max:  95.36%)
  • Average CER:         8.40%  (min:   4.64%, max:  15.10%)
  • Average WER:        41.02%  (min:  29.41%, max:  68.05%)

📋 FIELD-BY-FIELD ANALYSIS

English Name:
  Accuracy:  99.86%  | CER:   0.14%  | WER:   1.04%

Bangla Name:
  Accuracy:  96.57%  | CER:   3.43%  | WER:  15.75%

Father/Spouse Name:
  Accuracy:  94.31%  | CER:   5.69%  | WER:  21.87%

Mother Name:
  Accuracy:  97.16%  | CER:   2.84%  | WER:  15.19%

Date of Birth:
  Accuracy:  80.00%  | CER:  20.00%  | WER: 100.00%

NID Number:
  Accuracy:  91.03%  | CER:   8.97%  | WER: 100.00%

Address:
  Accuracy:  82.26%  | CER:  17.74%  | WER:  33.27%

🎯 ACCURACY DISTRIBUTION
   90% - 100%:  90 records ( 67.7%) 
   80% -  90%:  43 records ( 32.3%)

📈 QUALITY ASSESSMENT
Quality Tiers:
  • Excellent (≥95%):    6 records (  4.5%)
  • Good (80-95%):     127 records ( 95.5%)
  • Fair (60-80%):       0 records (  0.0%)
  • Poor (<60%):         0 records (  0.0%)
```

## Files

- `evaluator.py` - Main evaluation logic
- `summary.py` - Statistical summary and visualization
- `__init__.py` - Module initialization
- `requirements.txt` - Python dependencies
- `README.md` - This file

## Output Files

- `data/evaluation_results.csv` - Detailed evaluation report with all metrics
- Console output - Summary statistics and quality assessment

## Performance Interpretation

- **Excellent (≥95%)**: High-quality data entry, minimal errors
- **Good (80-95%)**: Acceptable data entry, minor errors
- **Fair (60-80%)**: Data entry needs review, significant errors
- **Poor (<60%)**: Data entry needs correction

## Troubleshooting

### No matching records found
- Image IDs may not match between datasets
- Check that NID numbers are present in both files
- Verify data alignment between person 1/2 results and ground truth

### Low accuracy for specific fields
- Check field format consistency
- Look for extra spaces, punctuation differences
- Verify date format (YYYY-MM-DD)
- Review address field formatting

## License

Internal use only - NID verification project

