import streamlit as st
import pandas as pd
import altair as alt

# -----------------------------
# Page Setup
# -----------------------------
st.set_page_config(page_title="Inventory Cleaner Dashboard", layout="wide")

st.title("📦 Inventory Cleaner Dashboard")

# -----------------------------
# File Upload
# -----------------------------
st.subheader("Upload CSV File")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file is None:
    st.info("Please upload a CSV file to continue.")
    st.stop()

# -----------------------------
# Read CSV
# -----------------------------
try:
    df = pd.read_csv(uploaded_file)
except Exception as e:
    st.error("❌ Could not read CSV. Error: " + str(e))
    st.stop()

st.success(f"File uploaded: {uploaded_file.name}")

# Show preview
st.subheader("Preview Data")
st.dataframe(df.head(20))

# -----------------------------
# Validate CSV
# -----------------------------
if "Date" not in df.columns:
    st.error("❌ Your CSV must contain a column named 'Date'.")
    st.stop()

# Convert Date column
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df = df.dropna(subset=["Date"])

# -----------------------------
# Aggregations
# -----------------------------
daily = df.groupby(df["Date"].dt.date).size().reset_index(name="Count")
weekly = df.groupby(df["Date"].dt.isocalendar().week).size().reset_index(name="Count")
weekly.rename(columns={"week": "Week"}, inplace=True)
monthly = df.groupby(df["Date"].dt.strftime("%b")).size().reset_index(name="Count")

# -----------------------------
# Chart Function
# -----------------------------
def show_chart(title, data, x, y):
    st.subheader(title)
    chart = (
        alt.Chart(data)
        .mark_bar()
        .encode(
            x=x,
            y=y,
            tooltip=[x, y]
        )
        .properties(height=300)
    )
    st.altair_chart(chart, use_container_width=True)

# -----------------------------
# Display Charts
# -----------------------------
show_chart("📅 Daily Activity", daily, "Date", "Count")
show_chart("📆 Weekly Activity", weekly, "Week", "Count")
show_chart("🗓 Monthly Activity", monthly, "Date", "Count")





















