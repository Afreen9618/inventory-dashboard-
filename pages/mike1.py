import streamlit as st
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Inventory Cleaner Dashboard",
    layout="wide",
    page_icon="📦"
)

# --- HEADER ---
st.markdown(
    """
    <h1 style='font-size: 52px; font-weight: 800; margin-bottom: -10px;'>
        📦 Inventory Cleaner Dashboard
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown("## Upload CSV File")
st.write("Upload CSV")

# --- FILE UPLOAD AREA ---
uploaded_file = st.file_uploader(
    "Drag and drop file here",
    type=["csv"],
    accept_multiple_files=False,
    help="Limit 200MB per file • CSV",
)

# --- IF NO FILE ---
if uploaded_file is None:
    st.info("📄 Please upload a CSV file to continue.")
    st.stop()

# --- PROCESS CSV ---
try:
    df = pd.read_csv(uploaded_file)
    st.success("✅ File uploaded successfully!")
    st.write("### Preview of CSV Data")
    st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"❌ Error reading file: {e}")















