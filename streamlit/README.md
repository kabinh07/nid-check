# NID Data Entry Streamlit Apps

Streamlit applications for filling out and verifying NID (National ID) data with image previews. The data has been split into two parts so two people can work simultaneously.

## Features

- **Image Preview**: Display front and back NID images based on image_id
- **Data Entry Form**: Input fields for all NID information fields
- **Continuous Saving**: Results are automatically saved to CSV continuously
- **Data Viewing**: View all previously entered entries
- **Update Existing**: Edit entries by using the same image_id
- **Split Data**: Two separate apps for two people to work in parallel

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Make sure you have the image folders in the correct location:
```
../data/images/
    nid_front_image/
    nid_back_image/
```

## Data Split

The original CSV has been split into two equal parts:
- **Person 1**: `nid-data-part1.csv` (153 entries)
- **Person 2**: `nid-data-part2.csv` (154 entries)

Results are saved separately:
- **Person 1 Results**: `nid-data-entry-results-person1.csv`
- **Person 2 Results**: `nid-data-entry-results-person2.csv`

## Running the Apps

### Person 1:
```bash
streamlit run app_person1.py
```
This will open at `http://localhost:8501`

### Person 2 (in a different terminal):
```bash
streamlit run app_person2.py -- --server.port=8502
```
This will open at `http://localhost:8502`

Or run both in the background:
```bash
nohup streamlit run app_person1.py > person1.log 2>&1 &
nohup streamlit run app_person2.py -- --server.port=8502 > person2.log 2>&1 &
```

## Usage

1. Enter the Image ID to load the front and back images
2. Fill in the NID information fields:
   - English Name
   - Bangla Name
   - Father/Spouse Name
   - Mother Name
   - Date of Birth (YYYY-MM-DD format)
   - NID Number
   - Address

3. Click **Save & Next ➡** to save the data and move to next entry
   - If the image_id already exists, it will update that entry
   - If it's new, it will add a new entry

4. Click **Previous ⬅** to go back to previous entry

5. Click **Skip ⏭** to skip the current entry without saving

6. Click **Clear Form** to reset all fields

7. Click **View All Entries** to see all saved entries in a table

## Output

Results are saved to separate files:
- Person 1: `../data/nid-data-entry-results-person1.csv`
- Person 2: `../data/nid-data-entry-results-person2.csv`

Each CSV file includes all fields and updates continuously as you add/edit entries.

## Merging Results

To combine results from both people after they complete their work:
```bash
python3 merge_results.py
```

This will create a combined file with all entries.
