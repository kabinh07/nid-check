import pandas as pd
from datetime import datetime, timedelta
import os

# Load the CSV file (tab-separated)
csv_file = 'data/nid-data-140126.csv'
df = pd.read_csv(csv_file, sep='\t')

# Convert doc_date to datetime
df['doc_date'] = pd.to_datetime(df['doc_date'], errors='coerce')

# Get the maximum date in the dataset
max_date = df['doc_date'].max()
print(f"Maximum date in dataset: {max_date}")

# Calculate the date 15 days ago from the maximum date
cutoff_date = max_date - timedelta(days=15)
print(f"Cutoff date (15 days ago from max): {cutoff_date}")

# Filter data for the last 15 days
filtered_df = df[df['doc_date'] >= cutoff_date]

print(f"\nOriginal data rows: {len(df)}")
print(f"Filtered data rows (last 15 days): {len(filtered_df)}")
print(f"Date range: {filtered_df['doc_date'].min()} to {filtered_df['doc_date'].max()}")

# Save filtered data to a new CSV file
output_file = 'data/nid-data-last-15-days.csv'
filtered_df.to_csv(output_file, index=False, sep='\t')
print(f"\nFiltered data saved to: {output_file}")

# Display sample of filtered data
print("\nSample of filtered data:")
print(filtered_df[['id', 'name_english', 'doc_date']].head(10))
