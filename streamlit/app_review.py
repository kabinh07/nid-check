import streamlit as st
import pandas as pd
import os
from PIL import Image
import numpy as np

# Set page config
st.set_page_config(page_title="NID Data Review & Evaluation", layout="wide")

# Get absolute path to project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGES_DIR = os.path.join(PROJECT_ROOT, 'data', 'images')
EVALUATION_CSV = os.path.join(PROJECT_ROOT, 'data', 'evaluation_results.csv')

# Load evaluation results
@st.cache_data
def load_evaluation_data():
    return pd.read_csv(EVALUATION_CSV)

# Load image
def load_image(image_id, image_type='front'):
    """Load front or back image"""
    if image_type == 'front':
        img_dir = os.path.join(IMAGES_DIR, 'nid_front_image')
    else:
        img_dir = os.path.join(IMAGES_DIR, 'nid_back_image')
    
    img_path = os.path.join(img_dir, f'{image_id}.jpg')
    
    if os.path.exists(img_path):
        return Image.open(img_path)
    return None

# Format value for display
def format_value(val):
    if pd.isna(val):
        return "N/A"
    if isinstance(val, float):
        # Check if it's an integer stored as float (like NID)
        if val == int(val):
            return str(int(val))
        return str(val)
    return str(val)

# Get quality tier
def get_quality_tier(accuracy):
    if accuracy >= 95:
        return "🟢 Excellent"
    elif accuracy >= 80:
        return "🔵 Good"
    elif accuracy >= 60:
        return "🟡 Fair"
    else:
        return "🔴 Poor"

# Color comparison based on accuracy
def get_color_code(accuracy):
    if accuracy >= 95:
        return ("#2ecc71", "#ffffff")  # Dark green, white text
    elif accuracy >= 80:
        return ("#3498db", "#ffffff")  # Dark blue, white text
    elif accuracy >= 60:
        return ("#f39c12", "#ffffff")  # Dark orange, white text
    else:
        return ("#e74c3c", "#ffffff")  # Dark red, white text

# Load data
df = load_evaluation_data()

# Sidebar
st.sidebar.title("📊 NID Review")
record_index = st.sidebar.number_input("Record #", min_value=1, max_value=len(df), value=1) - 1

# Quick stats in sidebar
st.sidebar.metric("Total Samples", f"{len(df)}")
total_acc = df['overall_accuracy'].mean()
st.sidebar.metric("Avg Accuracy", f"{total_acc:.1f}%")

# Field-wise metrics
st.sidebar.divider()
st.sidebar.markdown("**Field-wise Overall Metrics:**")

fields_info = [
    ('english_name', 'English Name'),
    ('bangla_name', 'Bangla Name'),
    ('father_spouse', 'Father/Spouse'),
    ('mother', 'Mother'),
    ('dob', 'DOB'),
    ('nid_no', 'NID'),
    ('address', 'Address')
]

for field_key, field_label in fields_info:
    acc = df[f'{field_key}_accuracy'].mean()
    cer = df[f'{field_key}_cer'].mean()
    
    st.sidebar.markdown(f"""
    <div style="padding: 8px; border-left: 3px solid #2c5aa0; margin: 5px 0;">
        <b>{field_label}</b><br>
        <small>Acc: {acc:.1f}% | CER: {cer:.1f}%</small>
    </div>
    """, unsafe_allow_html=True)

# Get current record
record = df.iloc[record_index]
image_id = str(int(record['image_id']))

st.title(f"Record #{record_index + 1} | {get_quality_tier(record['overall_accuracy'])}")

# Display doc date
if 'predicted_doc_date' in record and pd.notna(record['predicted_doc_date']):
    st.markdown(f"📅 **Doc Date:** {record['predicted_doc_date']}")

# Images
col_front, col_back = st.columns(2)
with col_front:
    front_img = load_image(image_id, 'front')
    if front_img:
        st.image(front_img, use_container_width=True)

with col_back:
    back_img = load_image(image_id, 'back')
    if back_img:
        st.image(back_img, use_container_width=True)

st.divider()

# Data Comparison - Compact Table
fields = [
    ('english_name', 'English Name'),
    ('bangla_name', 'Bangla Name'),
    ('father_spouse', 'Father/Spouse'),
    ('mother', 'Mother'),
    ('dob', 'DOB'),
    ('nid_no', 'NID'),
    ('address', 'Address')
]

comparison_data = []
for field_key, field_label in fields:
    actual_val = record[f'actual_{field_key}']
    predicted_val = record[f'predicted_{field_key}']
    accuracy = record[f'{field_key}_accuracy']
    
    comparison_data.append({
        'Field': field_label,
        'Ground Truth': format_value(actual_val),
        'Polygon OCR': format_value(predicted_val),
        'Accuracy': f"{accuracy:.0f}%"
    })

st.dataframe(pd.DataFrame(comparison_data), use_container_width=True, hide_index=True)


st.divider()

# Overall Metrics - Compact
col1, col2, col3 = st.columns(3)
overall_accuracy = record['overall_accuracy']
overall_cer = record['overall_cer']

with col1:
    bg_color, text_color = get_color_code(overall_accuracy)
    st.markdown(f"""<div style="background: #1f4788; color: white; padding: 15px; border-radius: 8px; text-align: center;">
        <b style="font-size: 20px;">{overall_accuracy:.1f}%</b><br><small>Accuracy</small></div>""", unsafe_allow_html=True)

with col2:
    st.markdown(f"""<div style="background: #2c5aa0; color: white; padding: 15px; border-radius: 8px; text-align: center;">
        <b style="font-size: 20px;">{overall_cer:.1f}%</b><br><small>CER</small></div>""", unsafe_allow_html=True)

with col3:
    st.markdown(f"""<div style="background: #2c5aa0; color: white; padding: 15px; border-radius: 8px; text-align: center;">
        <b style="font-size: 14px;">{get_quality_tier(overall_accuracy)}</b><br><small>Quality</small></div>""", unsafe_allow_html=True)

# Navigation
nav_col1, nav_col2, nav_col3 = st.columns(3)
with nav_col1:
    if st.button("⬅️ Previous", use_container_width=True):
        st.session_state['idx'] = max(0, record_index - 1)
        st.rerun()

with nav_col2:
    if st.button("➡️ Next", use_container_width=True):
        st.session_state['idx'] = min(len(df) - 1, record_index + 1)
        st.rerun()

with nav_col3:
    csv = df.to_csv(index=False)
    st.download_button("📥 CSV", data=csv, file_name="evaluation_results.csv", mime="text/csv", use_container_width=True)
