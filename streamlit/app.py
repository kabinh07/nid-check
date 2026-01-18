import streamlit as st
import pandas as pd
import os
from datetime import datetime
from pathlib import Path

# Set page config
st.set_page_config(page_title="NID Data Entry Form", layout="wide")

st.title("NID Data Entry & Verification Form")

# Define CSV files and paths
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)

input_csv = os.path.join(project_root, "data", "nid-data-last-15-days.csv")
output_csv = os.path.join(project_root, "data", "nid-data-entry-results.csv")
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
        st.metric("Total Entries", len(csv_data))
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

    col1, col2 = st.columns(2)
    with col1:
        english_name = st.text_input(
            "English Name:",
            value=st.session_state.form_data.get("english_name", ""),
            key="english_name_input"
        )
        bangla_name = st.text_input(
            "Bangla Name:",
            value=st.session_state.form_data.get("bangla_name", ""),
            key="bangla_name_input"
        )
        father_spouse_name = st.text_input(
            "Father/Spouse Name:",
            value=st.session_state.form_data.get("father_spouse_name", ""),
            key="father_spouse_name_input"
        )

    with col2:
        mother_name = st.text_input(
            "Mother Name:",
            value=st.session_state.form_data.get("mother_name", ""),
            key="mother_name_input"
        )
        dob = st.text_input(
            "Date of Birth (YYYY-MM-DD):",
            value=st.session_state.form_data.get("dob", ""),
            key="dob_input"
        )
        nid_no = st.text_input(
            "NID Number:",
            value=st.session_state.form_data.get("nid_no", ""),
            key="nid_no_input"
        )

    plain_address = st.text_area(
        "Address:",
        value=st.session_state.form_data.get("plain_address", ""),
        height=100,
        key="plain_address_input"
    )

    st.divider()

    # Navigation and Save buttons
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        if st.button("⬅ Previous", use_container_width=True):
            if st.session_state.current_index > 0:
                st.session_state.current_index -= 1
                st.session_state.form_data = {}
                st.rerun()

    with col2:
        if st.button("Save & Next ➡", use_container_width=True):
            # Save current entry
            new_entry = {
                "image_id": image_id,
                "english_name": english_name,
                "bangla_name": bangla_name,
                "father_spouse_name": father_spouse_name,
                "mother_name": mother_name,
                "dob": dob,
                "nid_no": nid_no,
                "plain_address": plain_address
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
            
            # Move to next
            if st.session_state.current_index < len(csv_data) - 1:
                st.session_state.current_index += 1
                st.session_state.form_data = {}
                st.success("Entry saved! Moving to next...")
                st.rerun()
            else:
                st.success("✅ All entries completed!")

    with col3:
        if st.button("Skip ⏭", use_container_width=True):
            if st.session_state.current_index < len(csv_data) - 1:
                st.session_state.current_index += 1
                st.session_state.form_data = {}
                st.rerun()
            else:
                st.info("Already at the last entry")

    with col4:
        if st.button("Clear Form", use_container_width=True):
            st.session_state.form_data = {}
            st.rerun()

    with col5:
        if st.button("View All Entries", use_container_width=True):
            st.session_state.show_entries = not st.session_state.get("show_entries", False)

    # Display all entries
    if st.session_state.get("show_entries", False):
        st.divider()
        st.subheader("All Completed Entries")
        if os.path.exists(output_csv):
            df = pd.read_csv(output_csv)
            st.dataframe(df, use_container_width=True)
            st.metric("Total Completed", len(df))
        else:
            st.info("No entries saved yet")

else:
    st.warning("No data found in nid-data-last-15-days.csv")
