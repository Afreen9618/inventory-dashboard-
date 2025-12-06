import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="MIKE 1 Inventory Dashboard", layout="wide")

st.title("📦 MIKE 1 Inventory Dashboard")

# -------------------------------
# Load Excel file
# -------------------------------
uploaded_file = st.file_uploader("Upload TEST 1.xlsx file", type=["xlsx"])

if uploaded_file is None:
    st.info("Please upload TEST 1.xlsx to continue.")
    st.stop()

# Read Excel
df = pd.read_excel(uploaded_file)

# -------------------------------
# Remove CS2 completely
# -------------------------------
if "CS 2" in df.columns:
    df = df.drop(columns=["CS 2"])

# -------------------------------
# Remove rows where CS1 is empty or "-"
# -------------------------------
df = df[df["CS 1"].notna()]
df = df[df["CS 1"].astype(str).str.strip() != "-"]

# -------------------------------
# Remove unwanted columns
# -------------------------------
remove_cols = ["UID NO", "PO"]
df = df.drop(columns=[c for c in remove_cols if c in df.columns], errors="ignore")

# -------------------------------
# Format dates
# -------------------------------
date_cols = ["DATE OF REPACK", "DATE OF PRODUCE"]
for col in date_cols:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors="coerce")

# -------------------------------
# Reorder columns
# -------------------------------
final_order = [
    "STATUS", "FCL-NO", "ENTERED BY", "DATE OF REPACK", "DATE OF PRODUCE",
    "PRODUCT ID", "PACKING STYLE", "PRODUCT", "GRADE", "PACK SIZE", "BRAND",
    "CARTONS", "LOT NO", "TRACE ID", "DAY CODE", "LOOSE BAGS", "KG LOOSE",
    "PALLET ID", "CS 1", "REMARKS", "NAV ID", "KGs", "POUNDS"
]

df = df[[col for col in final_order if col in df.columns]]

# -------------------------------
# Show total cartons
# -------------------------------
total_cartons = df["CARTONS"].sum()
st.metric(label="📦 Total Cartons", value=total_cartons)

# -------------------------------
# Show cleaned table
# -------------------------------
st.subheader("Cleaned Inventory Data")
st.dataframe(df, use_container_width=True)

# -------------------------------
# Chart data preparation
# -------------------------------
if "DATE OF REPACK" in df.columns:
    df["DATE_CHART"] = pd.to_datetime(df["DATE OF REPACK"], errors="coerce")

    # DAILY
    daily = df.groupby(df["DATE_CHART"].dt.date).size().reset_index(name="COUNT")

    # WEEKLY
    weekly = df.groupby(df["DATE_CHART"].dt.isocalendar().week).size().reset_index(name="COUNT")
    weekly.rename(columns={"week": "WEEK"}, inplace=True)

    # MONTHLY (Fix)
    monthly = df.groupby(df["DATE_CHART"].dt.strftime("%b")).size().reset_index(name="COUNT")
    monthly.rename(columns={monthly.columns[0]: "MONTH"}, inplace=True)

    # -------------------------------
    # Display charts
    # -------------------------------
    st.subheader("📊 Inventory Charts")

    # Daily chart
    st.write("### Daily Activity")
    chart_daily = alt.Chart(daily).mark_bar().encode(
        x="DATE_CHART:T",
        y="COUNT:Q",
        tooltip=["DATE_CHART", "COUNT"]
    ).properties(height=300)
    st.altair_chart(chart_daily, use_container_width=True)

    # Weekly chart
    st.write("### Weekly Activity")
    chart_weekly = alt.Chart(weekly).mark_bar().encode(
        x="WEEK:O",
        y="COUNT:Q",
        tooltip=["WEEK", "COUNT"]
    ).properties(height=300)
    st.altair_chart(chart_weekly, use_container_width=True)

    # Monthly chart
    st.write("### Monthly Activity")
    chart_monthly = alt.Chart(monthly).mark_bar().encode(
        x="MONTH:N",
        y="COUNT:Q",
        tooltip=["MONTH", "COUNT"]
    ).properties(height=300)
    st.altair_chart(chart_monthly, use_container_width=True)




























