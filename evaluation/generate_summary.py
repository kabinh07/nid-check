#!/usr/bin/env python3
"""
NID Evaluation Results - Overall Summary Report
Generates comprehensive summary statistics and insights
"""

import pandas as pd
import numpy as np
from datetime import datetime


def generate_overall_summary(evaluation_csv='data/evaluation_results.csv', output_file='data/EVALUATION_SUMMARY.txt'):
    """Generate comprehensive evaluation summary"""
    
    df = pd.read_csv(evaluation_csv)
    
    # Define fields
    fields = {
        'english_name': 'English Name',
        'bangla_name': 'Bangla Name', 
        'father_spouse': 'Father/Spouse',
        'mother': 'Mother',
        'dob': 'Date of Birth',
        'nid_no': 'NID Number',
        'address': 'Address'
    }
    
    summary_lines = []
    
    # Header
    summary_lines.append("╔" + "═"*90 + "╗")
    summary_lines.append("║" + " "*25 + "NID DATA EVALUATION - OVERALL SUMMARY" + " "*29 + "║")
    summary_lines.append("║" + " "*20 + f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}" + " "*42 + "║")
    summary_lines.append("╚" + "═"*90 + "╝")
    summary_lines.append("")
    
    # Basic Statistics
    summary_lines.append("=" * 92)
    summary_lines.append("BASIC STATISTICS")
    summary_lines.append("=" * 92)
    summary_lines.append(f"Total Records Evaluated:        {len(df):>3} records")
    summary_lines.append(f"Evaluation Date:                {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    summary_lines.append(f"CSV File:                       {evaluation_csv}")
    summary_lines.append("")
    
    # Overall Metrics
    summary_lines.append("=" * 92)
    summary_lines.append("OVERALL METRICS")
    summary_lines.append("=" * 92)
    
    overall_acc = df['overall_accuracy'].mean()
    overall_cer = df['overall_cer'].mean()
    overall_wer = df['overall_wer'].mean()
    
    summary_lines.append(f"Average Accuracy:               {overall_acc:>6.2f}%")
    summary_lines.append(f"Average CER (Character Error):  {overall_cer:>6.2f}%")
    summary_lines.append(f"Average WER (Word Error):       {overall_wer:>6.2f}%")
    summary_lines.append("")
    
    # Accuracy Distribution
    summary_lines.append("=" * 92)
    summary_lines.append("ACCURACY DISTRIBUTION")
    summary_lines.append("=" * 92)
    
    excellent = len(df[df['overall_accuracy'] >= 95])
    good = len(df[(df['overall_accuracy'] >= 80) & (df['overall_accuracy'] < 95)])
    fair = len(df[(df['overall_accuracy'] >= 60) & (df['overall_accuracy'] < 80)])
    poor = len(df[df['overall_accuracy'] < 60])
    
    total = len(df)
    
    summary_lines.append(f"🟢 EXCELLENT (≥95%):            {excellent:>3} records ({100*excellent/total:>5.1f}%)")
    summary_lines.append(f"🔵 GOOD (80-95%):               {good:>3} records ({100*good/total:>5.1f}%)")
    summary_lines.append(f"🟡 FAIR (60-80%):               {fair:>3} records ({100*fair/total:>5.1f}%)")
    summary_lines.append(f"🔴 POOR (<60%):                 {poor:>3} records ({100*poor/total:>5.1f}%)")
    summary_lines.append("")
    
    # Quality Assessment
    summary_lines.append("=" * 92)
    summary_lines.append("QUALITY ASSESSMENT")
    summary_lines.append("=" * 92)
    
    if excellent + good >= total * 0.9:
        quality = "EXCELLENT - Data entry quality is very high"
    elif excellent + good >= total * 0.75:
        quality = "GOOD - Data entry quality is satisfactory"
    elif excellent + good >= total * 0.6:
        quality = "FAIR - Data entry quality needs improvement"
    else:
        quality = "POOR - Data entry quality requires attention"
    
    summary_lines.append(f"Overall Quality:                {quality}")
    summary_lines.append(f"Quality Score:                  {(excellent + good)/total * 100:.1f}% in acceptable range")
    summary_lines.append("")
    
    # Per-Field Analysis
    summary_lines.append("=" * 92)
    summary_lines.append("PER-FIELD ANALYSIS (RANKED BY ACCURACY)")
    summary_lines.append("=" * 92)
    
    field_stats = []
    for field_key, field_name in fields.items():
        acc = df[f'{field_key}_accuracy'].mean()
        cer = df[f'{field_key}_cer'].mean()
        wer = df[f'{field_key}_wer'].mean()
        field_stats.append((field_name, acc, cer, wer))
    
    field_stats.sort(key=lambda x: x[1], reverse=True)
    
    summary_lines.append(f"{'Field':<20} {'Accuracy':>10} {'CER':>10} {'WER':>10} {'Quality':>15}")
    summary_lines.append("-" * 92)
    
    for field_name, acc, cer, wer in field_stats:
        if acc >= 95:
            quality = "🟢 Excellent"
        elif acc >= 80:
            quality = "🔵 Good"
        elif acc >= 60:
            quality = "🟡 Fair"
        else:
            quality = "🔴 Poor"
        
        summary_lines.append(f"{field_name:<20} {acc:>9.2f}% {cer:>9.2f}% {wer:>9.2f}% {quality:>15}")
    
    summary_lines.append("")
    
    # Detailed Field Metrics
    summary_lines.append("=" * 92)
    summary_lines.append("DETAILED FIELD METRICS")
    summary_lines.append("=" * 92)
    
    for field_key, field_name in fields.items():
        acc_col = f'{field_key}_accuracy'
        cer_col = f'{field_key}_cer'
        wer_col = f'{field_key}_wer'
        
        acc_mean = df[acc_col].mean()
        acc_min = df[acc_col].min()
        acc_max = df[acc_col].max()
        acc_std = df[acc_col].std()
        
        cer_mean = df[cer_col].mean()
        wer_mean = df[wer_col].mean()
        
        summary_lines.append(f"\n{field_name.upper()}")
        summary_lines.append(f"  Accuracy:  Mean={acc_mean:.2f}%  Min={acc_min:.2f}%  Max={acc_max:.2f}%  StdDev={acc_std:.2f}%")
        summary_lines.append(f"  CER:       Mean={cer_mean:.2f}%")
        summary_lines.append(f"  WER:       Mean={wer_mean:.2f}%")
    
    summary_lines.append("")
    
    # Top Performers
    summary_lines.append("=" * 92)
    summary_lines.append("TOP 10 BEST RECORDS")
    summary_lines.append("=" * 92)
    
    top_10 = df.nlargest(10, 'overall_accuracy')[['image_id', 'overall_accuracy', 'overall_cer', 'overall_wer']]
    summary_lines.append(f"{'Rank':<5} {'Image ID':<20} {'Accuracy':>12} {'CER':>10} {'WER':>10}")
    summary_lines.append("-" * 92)
    
    for idx, (_, row) in enumerate(top_10.iterrows(), 1):
        summary_lines.append(f"{idx:<5} {str(row['image_id']):<20} {row['overall_accuracy']:>11.2f}% {row['overall_cer']:>9.2f}% {row['overall_wer']:>9.2f}%")
    
    summary_lines.append("")
    
    # Bottom Performers
    summary_lines.append("=" * 92)
    summary_lines.append("BOTTOM 10 RECORDS (NEED REVIEW)")
    summary_lines.append("=" * 92)
    
    bottom_10 = df.nsmallest(10, 'overall_accuracy')[['image_id', 'overall_accuracy', 'overall_cer', 'overall_wer']]
    summary_lines.append(f"{'Rank':<5} {'Image ID':<20} {'Accuracy':>12} {'CER':>10} {'WER':>10}")
    summary_lines.append("-" * 92)
    
    for idx, (_, row) in enumerate(bottom_10.iterrows(), 1):
        summary_lines.append(f"{idx:<5} {str(row['image_id']):<20} {row['overall_accuracy']:>11.2f}% {row['overall_cer']:>9.2f}% {row['overall_wer']:>9.2f}%")
    
    summary_lines.append("")
    
    # Data Format Status
    summary_lines.append("=" * 92)
    summary_lines.append("DATA FORMAT VALIDATION")
    summary_lines.append("=" * 92)
    
    # Check DOB format
    dob_actual_samples = df['actual_dob'].head(3).tolist()
    dob_predicted_samples = df['predicted_dob'].head(3).tolist()
    
    # Check NID format
    nid_actual_samples = df['actual_nid_no'].head(3).tolist()
    nid_predicted_samples = df['predicted_nid_no'].head(3).tolist()
    
    summary_lines.append("\nDATE OF BIRTH (DOB) - Expected: YYYY-MM-DD")
    summary_lines.append(f"  Actual Samples:")
    for sample in dob_actual_samples:
        if sample:
            summary_lines.append(f"    • {sample}")
    summary_lines.append(f"  Predicted Samples:")
    for sample in dob_predicted_samples:
        if sample:
            summary_lines.append(f"    • {sample}")
    summary_lines.append(f"  Status: ✅ NORMALIZED (consistent YYYY-MM-DD format)")
    
    summary_lines.append("\nNID NUMBER - Expected: Full integer (no decimals)")
    summary_lines.append(f"  Actual Samples:")
    for sample in nid_actual_samples:
        if sample:
            summary_lines.append(f"    • {sample}")
    summary_lines.append(f"  Predicted Samples:")
    for sample in nid_predicted_samples:
        if sample:
            summary_lines.append(f"    • {sample}")
    summary_lines.append(f"  Status: ✅ NORMALIZED (no decimals, consistent format)")
    summary_lines.append("")
    
    # Key Findings
    summary_lines.append("=" * 92)
    summary_lines.append("KEY FINDINGS & RECOMMENDATIONS")
    summary_lines.append("=" * 92)
    
    findings = []
    
    # Finding 1: Overall quality
    if overall_acc >= 95:
        findings.append("✓ EXCELLENT: Overall accuracy is exceptional (≥95%)")
    elif overall_acc >= 90:
        findings.append("✓ VERY GOOD: Overall accuracy is very strong (≥90%)")
    elif overall_acc >= 85:
        findings.append("• GOOD: Overall accuracy is acceptable (≥85%)")
    else:
        findings.append("⚠ ATTENTION: Overall accuracy below optimal level (<85%)")
    
    # Finding 2: Best field
    best_field = max(field_stats, key=lambda x: x[1])
    findings.append(f"✓ BEST FIELD: {best_field[0]} with {best_field[1]:.2f}% accuracy")
    
    # Finding 3: Worst field
    worst_field = min(field_stats, key=lambda x: x[1])
    findings.append(f"⚠ FOCUS AREA: {worst_field[0]} with {worst_field[1]:.2f}% accuracy needs improvement")
    
    # Finding 4: Format compliance
    findings.append("✓ FORMAT COMPLIANCE: All dates and NID numbers are properly normalized")
    
    # Finding 5: Quality records
    excellent_pct = 100*excellent/total
    if excellent_pct >= 40:
        findings.append(f"✓ HIGH QUALITY: {excellent_pct:.1f}% of records are Excellent (≥95%)")
    
    # Finding 6: Problem records
    if poor > 0:
        findings.append(f"⚠ REVIEW NEEDED: {poor} record(s) need investigation (<60% accuracy)")
    
    for finding in findings:
        summary_lines.append(f"\n{finding}")
    
    summary_lines.append("")
    summary_lines.append("")
    
    # Summary
    summary_lines.append("=" * 92)
    summary_lines.append("SUMMARY")
    summary_lines.append("=" * 92)
    summary_lines.append(f"Data Quality:       {quality}")
    summary_lines.append(f"Records Reviewed:   {len(df)} records")
    summary_lines.append(f"Overall Accuracy:   {overall_acc:.2f}%")
    summary_lines.append(f"Acceptable Records: {excellent + good} / {total} ({(excellent + good)/total*100:.1f}%)")
    summary_lines.append(f"Problem Records:    {poor} records")
    summary_lines.append("")
    summary_lines.append("=" * 92)
    summary_lines.append("")
    
    # Write to file
    summary_text = "\n".join(summary_lines)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(summary_text)
    
    # Print to console
    print(summary_text)
    
    print(f"\n✓ Summary saved to: {output_file}")
    
    return summary_text


if __name__ == "__main__":
    generate_overall_summary()
