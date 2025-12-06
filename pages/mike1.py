import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime

st.set_page_config(page_title="Inventory Cleaner Dashboard", layout="wide")

st.title("📊 Inventory Cleaner Dashboard")

# ============================
# FILE UPLOAD
# ============================
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is None:
    st.info("⬆ Please upload TEST 1 CSV file to see the dashboard.")
    st.stop()

# Read CSV
df = pd.read_csv(uploaded_file)

# ============================
# PARSE DATE COLUMN
# ============================
if "Date" not in df.columns:
    st.error("❌ CSV must contain a column named **Date**")
    st.stop()

df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# ============================
# PREVIEW TABLE
# ============================
st.subheader("🔍 Preview Data")
st.dataframe(df.head(10))

# ============================
# PROCESS DAILY / WEEKLY / MONTHLY
# ============================
df["Day"] = df["Date"].dt.date
df["Week"] = df["Date"].dt.isocalendar().week
df["Month"] = df["Date"].dt.strftime("%b")

daily = df.groupby("Day").size().reset_index(name="Count")
weekly = df.groupby("Week").size().reset_index(name="Count")
monthly = df.groupby("Month").size().reset_index(name="Count")

# ============================
# CHART FUNCTION
# ============================
def render_chart(data, x, y, title):
    chart = (
        alt.Chart(data)
        .mark_bar()
        .encode(
            x=x,
            y=y,
            tooltip=[x, y]
        )
        .properties(height=300, title=title)
    )
    st.altair_chart(chart, use_container_width=True)

# ============================
# SHOW CHARTS
# ============================
st.subheader("📅 Daily Activity")
render_chart(daily, "Day:T", "Count:Q", "Daily Activity")

st.subheader("📆 Weekly Activity")
render_chart(weekly, "Week:O", "Count:Q", "Weekly Activity")

st.subheader("📈 Monthly Activity")
render_chart(monthly, "Month:O", "Count:Q", "Monthly Activity")
























