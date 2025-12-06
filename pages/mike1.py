import streamlit as st
import pandas as pd

st.title("Mike 1 Inventory Page (Cleaned)")

# Load Excel file
df = pd.read_excel("TEST 1.xlsx")

# ---------------------------------------------
# 🔥 1. REMOVE ROWS WHERE CS2 HAS ANY VALUE
#    (Keep only CS1 rows or empty rows)
# ---------------------------------------------
if "CS2" in df.columns:
    df = df[df["CS2"].isna() | (df["CS2"] == "")]

# ---------------------------------------------
# 🔥 2. REMOVE CS2 COLUMN COMPLETELY
# ---------------------------------------------
df = df.drop(columns=["CS2"], errors="ignore")

# ---------------------------------------------
# 🔥 3. REMOVE UNWANTED COLUMNS
# ---------------------------------------------
cols_to_remove = ["FCL NO", "PO", "UID NO"]
df = df.drop(columns=[col for col in cols_to_remove if col in df.columns], errors="ignore")

# ---------------------------------------------
# 🔥 4. FORMAT DATE COLUMNS → DD-MM-YYYY
# ---------------------------------------------
for col in df.columns:
    if "date" in col.lower():
        df[col] = pd.to_datetime(df[col], errors="coerce").dt.strftime("%d-%m-%Y")

# ---------------------------------------------
# Display cleaned data
# ---------------------------------------------
st.dataframe(df)





