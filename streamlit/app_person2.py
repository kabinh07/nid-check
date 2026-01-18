import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime
from pathlib import Path

# Set page config
st.set_page_config(page_title="NID Data Entry Form - Person 2", layout="wide")

st.title("👥 Person 2 - NID Data Entry & Verification Form")

# Define CSV files and paths
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)

input_csv = os.path.join(project_root, "data", "nid-data-part2.csv")
output_csv = os.path.join(project_root, "data", "nid-data-entry-results-person2.csv")
image_base_path = os.path.join(project_root, "data", "images")

# Load input data
@st.cache_data
def load_csv():
    if os.path.exists(input_csv):
        return pd.read_csv(input_csv, sep='\t')
    return pd.DataFrame()

def image_exists(image_id):
    """Check if both front and back images exist"""
    front_path = os.path.join(image_base_path, "nid_front_image", f"{image_id}.jpg")
    back_path = os.path.join(image_base_path, "nid_back_image", f"{image_id}.jpg")
    return os.path.exists(front_path) and os.path.exists(back_path)

csv_data = load_csv()

# Initialize session state
if "current_index" not in st.session_state:
    st.session_state.current_index = 0
if "form_data" not in st.session_state:
    st.session_state.form_data = {}

# Get current row
if len(csv_data) > 0:
    # Find next row with images
    while st.session_state.current_index < len(csv_data):
        current_row = csv_data.iloc[st.session_state.current_index]
        
        # Extract image_id from front_image path
        front_image_col = current_row.get('front_image', '')
        if isinstance(front_image_col, str) and '/' in front_image_col:
            image_id = front_image_col.split('/')[-1].replace('.jpg', '')
        else:
            image_id = str(front_image_col).replace('.jpg', '')
        
        # Check if images exist
        if image_exists(image_id):
            break
        else:
            st.session_state.current_index += 1
    
    if st.session_state.current_index >= len(csv_data):
        st.warning("⚠️ No more entries with available images!")
        st.stop()
    
    current_row = csv_data.iloc[st.session_state.current_index]
    
    # Extract image_id from front_image path
    front_image_col = current_row.get('front_image', '')
    if isinstance(front_image_col, str) and '/' in front_image_col:
        image_id = front_image_col.split('/')[-1].replace('.jpg', '')
    else:
        image_id = str(front_image_col).replace('.jpg', '')
    
    # Display progress
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        st.metric("Current Entry", st.session_state.current_index + 1)
    with col2:
        st.metric("Total Entries (Part 2)", len(csv_data))
    with col3:
        st.metric("Completed", len(pd.read_csv(output_csv)) if os.path.exists(output_csv) else 0)
    
    st.divider()
    
    # Create two columns for images
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Front Image")
        front_image_path = os.path.join(image_base_path, "nid_front_image", f"{image_id}.jpg")
        if os.path.exists(front_image_path):
            st.image(front_image_path, use_column_width=True)
        else:
            st.error(f"❌ Front image not found")

    with col2:
        st.subheader("Back Image")
        back_image_path = os.path.join(image_base_path, "nid_back_image", f"{image_id}.jpg")
        if os.path.exists(back_image_path):
            st.image(back_image_path, use_column_width=True)
        else:
            st.error(f"❌ Back image not found")
    
    st.divider()

    # Create form fields
    st.subheader("NID Information")
    
    # JSON Parser Section - Simple input and save
    json_input = st.text_area(
        "Paste JSON to save:",
        placeholder='{"english_name": "", "bangla_name": "", "father_spouse_name": "", "mother_name": "", "dob": "", "nid_no": "", "plain_address": ""}',
        height=100,
        key="json_input"
    )
    
    col_parse1, col_parse2, col_parse3 = st.columns(3)
    with col_parse1:
        if st.button("Save JSON ✓", use_container_width=True):
            if json_input.strip():
                try:
                    parsed_data = json.loads(json_input)
                    # Save current entry with image_id
                    new_entry = {
                        "image_id": image_id,
                        "english_name": parsed_data.get("english_name", ""),
                        "bangla_name": parsed_data.get("bangla_name", ""),
                        "father_spouse_name": parsed_data.get("father_spouse_name", ""),
                        "mother_name": parsed_data.get("mother_name", ""),
                        "dob": parsed_data.get("dob", ""),
                        "nid_no": parsed_data.get("nid_no", ""),
                        "plain_address": parsed_data.get("plain_address", "")
                    }
                    
                    # Load existing data or create new
                    if os.path.exists(output_csv):
                        df = pd.read_csv(output_csv)
                        # Check if image_id already exists
                        if image_id in df["image_id"].values:
                            df.loc[df["image_id"] == image_id] = new_entry
                        else:
                            df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
                    else:
                        df = pd.DataFrame([new_entry])
                    
                    # Save to CSV
                    df.to_csv(output_csv, index=False)
                    st.success("✅ Saved!")
                    
                    # Move to next
                    if st.session_state.current_index < len(csv_data) - 1:
                        st.session_state.current_index += 1
                        st.rerun()
                except json.JSONDecodeError as e:
                    st.error(f"❌ Invalid JSON: {str(e)}")
            else:
                st.error("❌ Please paste JSON data")
    
    with col_parse2:
        if st.button("Skip ⏭", use_container_width=True):
            if st.session_state.current_index < len(csv_data) - 1:
                st.session_state.current_index += 1
                st.rerun()
            else:
                st.info("Already at the last entry")
    
    with col_parse3:
        if st.button("View Results", use_container_width=True):
            st.session_state.show_entries = not st.session_state.get("show_entries", False)

    st.divider()
    
    # Display all entries
    if st.session_state.get("show_entries", False):
        st.subheader("All Completed Entries")
        if os.path.exists(output_csv):
            df = pd.read_csv(output_csv)
            st.dataframe(df, use_container_width=True)
            st.metric("Total Completed", len(df))
        else:
            st.info("No entries saved yet")

else:
    st.warning("No data found in nid-data-part2.csv")
