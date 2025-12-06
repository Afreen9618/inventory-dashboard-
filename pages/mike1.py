import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime

st.set_page_config(page_title="Inventory Cleaner Dashboard", layout="wide")

# ---- TITLE ----
st.markdown(
    """
    <h1 style='text-align:center; color:white;'>
        📦 Inventory Cleaner Dashboard
    </h1>
    """,
    unsafe_allow_html=True
)

# ---- UPLOAD FILE ----
st.markdown(
    """
    <div style="
        border:2px dashed #555;
        background:#1A1F29;
        padding:40px;
        border-radius:15px;
        text-align:center;
        color:white;">
        
        <h2>📤 Upload CSV File</h2>
        <p>Drag & Drop or Browse • Max 200MB • CSV only</p>
    </div>
    """,
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader("", type=["csv"])

# Stop if no file
if not uploaded_file:
    st.info("⬆ Upload a CSV file to continue.")
    st.stop()

# ---- READ CSV ----
df = pd.read_csv(uploaded_file)

st.success(f"✔ Uploaded: {uploaded_file.name}")

# Ensure Date column exists
if "Date" not in df.columns:
    st.error("❌ ERROR: Your CSV must contain a 'Date' column.")
    st.stop()

# Convert Date column
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# ---- PREVIEW TABLE ----
st.markdown("### 🔎 Preview (first 10 rows)")
st.dataframe(df.head(10))

# ---- PROCESS DATA ----
df["Day"] = df["Date"].dt.date
df["Week"] = df["Date"].dt.strftime("Week-%U")
df["Month"] = df["Date"].dt.strftime("%b")

daily = df.groupby("Day").size().reset_index(name="Count")
weekly = df.groupby("Week").size().reset_index(name="Count")
monthly = df.groupby("Month").size().reset_index(name="Count")

# ---- CHART CREATOR ----
def create_chart(data, x, y):
    return (
        alt.Chart(data)
        .mark_bar()
        .encode(
            x=alt.X(x, sort=None, axis=alt.Axis(labelColor="white", titleColor="white")),
            y=alt.Y(y, axis=alt.Axis(labelColor="white", titleColor="white")),
            tooltip=[x, y]
        )
        .properties(height=300)
        .configure_axis(grid=False)
    )

# ---- CHARTS SECTION ----
st.markdown("## 📊 Inventory Charts")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### Daily Activity")
    st.altair_chart(create_chart(daily, "Day", "Count"), use_container_width=True)

with col2:
    st.markdown("### Weekly Activity")
    st.altair_chart(create_chart(weekly, "Week", "Count"), use_container_width=True)

with col3:
    st.markdown("### Monthly Activity")
    st.altair_chart(create_chart(monthly, "Month", "Count"), use_container_width=True)






















