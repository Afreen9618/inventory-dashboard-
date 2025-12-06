import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="MIKE 1 Inventory Dashboard", layout="wide")

st.title("📦 MIKE 1 Inventory Dashboard")

uploaded_file = st.file_uploader("Upload TEST 1.xlsx file", type=["xlsx"])

if uploaded_file is None:
    st.info("Please upload TEST 1.xlsx to continue.")
    st.stop()

df = pd.read_excel(uploaded_file)

# -------------------------------
# FIX: Normalize column names
# -------------------------------
original_columns = df.columns.copy()

df.columns = (
    df.columns
    .str.strip()
    .str.upper()
    .str.replace(" ", "")
    .str.replace("-", "")
    .str.replace("_", "")
)

# -------------------------------
# Identify CS1 column automatically
# -------------------------------
cs1_candidates = [col for col in df.columns if "CS1" in col]

if not cs1_candidates:
    st.error("❌ ERROR: Could not find a column matching CS1 in file.\n\n"
             f"Columns found:\n{list(original_columns)}")
    st.stop()

cs1_col = cs1_candidates[0]  # use the first detected

# -------------------------------
# Remove rows where CS1 is empty
# -------------------------------
df = df[df[cs1_col].notna()]
df = df[df[cs1_col].astype(str).str.strip() != "-"]

# -------------------------------
# Drop CS2 column if exists
# -------------------------------
cs2_candidates = [col for col in df.columns if "CS2" in col]
if cs2_candidates:
    df = df.drop(columns=[cs2_candidates[0]])

# -------------------------------
# Convert dates (normalize names)
# -------------------------------
date_cols = {
    "DATEOFREPACK": "DATE OF REPACK",
    "DATEOFPRODUCE": "DATE OF PRODUCE"
}

for normalized_col, display_name in date_cols.items():
    if normalized_col in df.columns:
        df[display_name] = pd.to_datetime(df[normalized_col], errors="coerce")

# -------------------------------
# Show cleaned table
# -------------------------------
st.subheader("Cleaned Inventory Data")
st.dataframe(df, use_container_width=True)

# ===============================
# CHARTS
# ===============================
if "DATE OF REPACK" in df.columns:
    df["DATE_CHART"] = pd.to_datetime(df["DATE OF REPACK"], errors="coerce")

    # Daily
    daily = df.groupby(df["DATE_CHART"].dt.date).size().reset_index(name="COUNT")

    # Weekly
    weekly = df.groupby(df["DATE_CHART"].dt.isocalendar().week).size().reset_index(name="COUNT")
    weekly.rename(columns={"week": "WEEK"}, inplace=True)

    # Monthly
    monthly = df.groupby(df["DATE_CHART"].dt.strftime("%b")).size().reset_index(name="COUNT")
    monthly.rename(columns={monthly.columns[0]: "MONTH"}, inplace=True)

    st.subheader("📊 Inventory Charts")

    st.write("### Daily")
    st.altair_chart(
        alt.Chart(daily).mark_bar().encode(
            x="DATE_CHART:T", y="COUNT:Q", tooltip=["DATE_CHART", "COUNT"]
        ).properties(height=300),
        use_container_width=True
    )

    st.write("### Weekly")
    st.altair_chart(
        alt.Chart(weekly).mark_bar().encode(
            x="WEEK:O", y="COUNT:Q", tooltip=["WEEK", "COUNT"]
        ).properties(height=300),
        use_container_width=True
    )

    st.write("### Monthly")
    st.altair_chart(
        alt.Chart(monthly).mark_bar().encode(
            x="MONTH:N", y="COUNT:Q", tooltip=["MONTH", "COUNT"]
        ).properties(height=300),
        use_container_width=True
    )



























