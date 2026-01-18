"""
Quick Reference Guide - NID Evaluation Module
"""

print("""
╔════════════════════════════════════════════════════════════════════════════════════╗
║                        NID EVALUATION MODULE - QUICK START                         ║
╚════════════════════════════════════════════════════════════════════════════════════╝

📁 LOCATION: /evaluation/

📋 FILES:
  • evaluator.py     - Main evaluation engine
  • summary.py       - Statistical analysis and reporting
  • __init__.py      - Module interface
  • requirements.txt - Dependencies
  • README.md        - Full documentation
  
🚀 QUICK START:

1. Run full evaluation:
   $ python evaluator.py
   
2. View summary statistics:
   $ python summary.py

3. Use as Python module:
   from evaluation import ResultsEvaluator
   evaluator = ResultsEvaluator(person1, person2, ground_truth)
   results = evaluator.generate_report('output.csv')

📊 OUTPUT:
  • evaluation_results.csv - Detailed results with metrics
  • Summary statistics     - Printed to console
  • Quality assessment     - Accuracy distribution

📈 METRICS EXPLAINED:

  ACCURACY (0-100%)
  └─ Similarity ratio between entered vs ground truth
     • 100% = Perfect match
     • 90%+ = Excellent
     • 80%+ = Good

  CER - Character Error Rate (0-100%)
  └─ Character-level differences
     • 0% = No errors
     • <5% = Excellent
     • <10% = Good

  WER - Word Error Rate (0-100%)
  └─ Word-level differences
     • 0% = All words match
     • <20% = Good
     • >50% = Many word differences

🎯 QUALITY TIERS:
  • Excellent: ≥95% accuracy
  • Good: 80-95% accuracy
  • Fair: 60-80% accuracy
  • Poor: <60% accuracy

📝 RESULTS CSV STRUCTURE:

  Entered Data          Ground Truth           Metrics
  ├─ image_id          ├─ predicted_*_name    ├─ *_accuracy
  ├─ actual_english    ├─ predicted_*         ├─ *_cer
  ├─ actual_bangla     └─ predicted_address   ├─ *_wer
  ├─ actual_father                            └─ overall_*
  ├─ actual_mother
  ├─ actual_dob
  ├─ actual_nid_no
  └─ actual_address

🔍 EXAMPLE USAGE IN CODE:

from evaluation import ResultsEvaluator, print_summary

# Initialize
evaluator = ResultsEvaluator(
    person1_csv='data/nid-data-entry-results-person1.csv',
    person2_csv='data/nid-data-entry-results-person2.csv',
    ground_truth_csv='data/nid-data-140126.csv'
)

# Run evaluation
results_df = evaluator.evaluate()
print(f"Matched records: {len(results_df)}")

# Generate report with stats
evaluator.generate_report('data/evaluation_results.csv')

# Print summary
print_summary('data/evaluation_results.csv')

💡 TIPS:

✓ Merge happens automatically when running evaluator.py
✓ Records matched by NID number if image IDs don't align
✓ Missing matches are logged as warnings
✓ All metrics are normalized to 0-100 scale
✓ Results CSV is comma-separated, quoted fields

⚠️  NOTES:

• Date formats must be consistent (YYYY-MM-DD)
• Names are case-insensitive for comparison
• Address comparison is word-level
• CER/WER may be 100% for numeric fields due to word splitting

📞 SUPPORT:

For issues or questions:
1. Check README.md for detailed documentation
2. Review evaluator.py source code for algorithm details
3. Check data format in evaluation_results.csv

═══════════════════════════════════════════════════════════════════════════════════════
""")
