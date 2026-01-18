import pandas as pd
import os

def print_summary(evaluation_csv):
    """Print summary statistics from evaluation results"""
    if not os.path.exists(evaluation_csv):
        print(f"File not found: {evaluation_csv}")
        return
    
    df = pd.read_csv(evaluation_csv)
    
    print("\n" + "="*100)
    print("DETAILED EVALUATION SUMMARY")
    print("="*100)
    
    print(f"\n📊 OVERALL STATISTICS")
    print("-" * 100)
    print(f"Total Records Evaluated: {len(df)}")
    print(f"\nAccuracy Metrics:")
    print(f"  • Average Accuracy:  {df['overall_accuracy'].mean():>6.2f}%  (min: {df['overall_accuracy'].min():>6.2f}%, max: {df['overall_accuracy'].max():>6.2f}%)")
    print(f"  • Average CER:       {df['overall_cer'].mean():>6.2f}%  (min: {df['overall_cer'].min():>6.2f}%, max: {df['overall_cer'].max():>6.2f}%)")
    print(f"  • Average WER:       {df['overall_wer'].mean():>6.2f}%  (min: {df['overall_wer'].min():>6.2f}%, max: {df['overall_wer'].max():>6.2f}%)")
    
    print(f"\n\n📋 FIELD-BY-FIELD ANALYSIS")
    print("-" * 100)
    
    fields = [
        ('english_name', 'English Name'),
        ('bangla_name', 'Bangla Name'),
        ('father_spouse', 'Father/Spouse Name'),
        ('mother', 'Mother Name'),
        ('dob', 'Date of Birth'),
        ('nid_no', 'NID Number'),
        ('address', 'Address'),
    ]
    
    for field_key, field_label in fields:
        acc_col = f'{field_key}_accuracy'
        cer_col = f'{field_key}_cer'
        wer_col = f'{field_key}_wer'
        
        print(f"\n{field_label}:")
        print(f"  Accuracy: {df[acc_col].mean():>6.2f}%  | CER: {df[cer_col].mean():>6.2f}%  | WER: {df[wer_col].mean():>6.2f}%")
        print(f"    (Accuracy range: {df[acc_col].min():.2f}% - {df[acc_col].max():.2f}%)")
    
    print(f"\n\n🎯 ACCURACY DISTRIBUTION")
    print("-" * 100)
    
    # Accuracy buckets
    buckets = [(90, 100), (80, 90), (70, 80), (60, 70), (50, 60), (0, 50)]
    for lower, upper in buckets:
        count = len(df[(df['overall_accuracy'] >= lower) & (df['overall_accuracy'] < upper)])
        percentage = (count / len(df)) * 100
        bar = "█" * int(percentage / 5)
        print(f"  {lower:>3}% - {upper:>3}%: {count:>3} records ({percentage:>5.1f}%) {bar}")
    
    print(f"\n\n📈 QUALITY ASSESSMENT")
    print("-" * 100)
    
    excellent = len(df[df['overall_accuracy'] >= 95])
    good = len(df[(df['overall_accuracy'] >= 80) & (df['overall_accuracy'] < 95)])
    fair = len(df[(df['overall_accuracy'] >= 60) & (df['overall_accuracy'] < 80)])
    poor = len(df[df['overall_accuracy'] < 60])
    
    print(f"\nQuality Tiers:")
    print(f"  • Excellent (≥95%):  {excellent:>3} records ({excellent/len(df)*100:>5.1f}%)")
    print(f"  • Good (80-95%):     {good:>3} records ({good/len(df)*100:>5.1f}%)")
    print(f"  • Fair (60-80%):     {fair:>3} records ({fair/len(df)*100:>5.1f}%)")
    print(f"  • Poor (<60%):       {poor:>3} records ({poor/len(df)*100:>5.1f}%)")
    
    print(f"\n\n💾 OUTPUT FILE")
    print("-" * 100)
    print(f"Detailed evaluation results saved to:")
    print(f"  {evaluation_csv}")
    print(f"  File size: {os.path.getsize(evaluation_csv) / 1024:.1f} KB")
    
    print("\n" + "="*100 + "\n")
    
    return df


if __name__ == "__main__":
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    evaluation_csv = os.path.join(project_root, "data", "evaluation_results.csv")
    print_summary(evaluation_csv)
