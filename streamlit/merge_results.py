import pandas as pd
import os

# Define paths
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
person1_csv = os.path.join(project_root, "data", "nid-data-entry-results-person1.csv")
person2_csv = os.path.join(project_root, "data", "nid-data-entry-results-person2.csv")
merged_csv = os.path.join(project_root, "data", "nid-data-entry-results-merged.csv")

# Load both files
df_person1 = pd.read_csv(person1_csv) if os.path.exists(person1_csv) else pd.DataFrame()
df_person2 = pd.read_csv(person2_csv) if os.path.exists(person2_csv) else pd.DataFrame()

# Combine
merged_df = pd.concat([df_person1, df_person2], ignore_index=True)

# Save merged
merged_df.to_csv(merged_csv, index=False)

print(f"Person 1 entries: {len(df_person1)}")
print(f"Person 2 entries: {len(df_person2)}")
print(f"Total merged entries: {len(merged_df)}")
print(f"\nMerged file saved to: {merged_csv}")
