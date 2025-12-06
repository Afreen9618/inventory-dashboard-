import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Inventory Cleaner", layout="wide")

st.title("📦 Inventory Cleaner Dashboard")

# ----- Upload Section -----
st.subheader("Upload CSV File")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file is None:
    st.info("Please upload a CSV file to continue.")
    st.stop()

# ----- Read CSV -----
df = pd.read_csv(uploaded_file)
st.success(f"File uploaded: {uploaded_file.name}")

# Show preview
st.subheader("Preview Data")
st.dataframe(df.head(10))

# Ensure "Date" column exists
if "Date" not in df.columns:
    st.error("❌ Error: CSV must contain a 'Date' column.")
    st.stop()

# Convert to datetime
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df = df.dropna(subset=["Date"])

# ----- Daily, Weekly, Monthly groups -----

# DAILY
daily = df.groupby(df["Date"].dt.date).size().reset_index(name="Count")

# WEEKLY
weekly = df.groupby(df["Date"].dt.isocalendar().week).size().reset_index(name="Count")
weekly.rename(columns={"week": "Week"}, inplace=True)

# MONTHLY
monthly = df.groupby(df["Date"].dt.strftime("%b")).size().reset_index(name="Count")

# ----- Chart function -----
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

# ----- Display charts -----
show_chart("📅 Daily Activity", daily, "Date", "Count")
show_chart("📆 Weekly Activity", weekly, "Week", "Count")
show_chart("🗓 Monthly Activity", monthly, "Date", "Count")
















