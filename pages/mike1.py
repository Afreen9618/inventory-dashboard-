import streamlit as st
import pandas as pd

st.title("Mike 1 Inventory Page (CS1 Inventory)")

# -----------------------------------------
# 1. LOAD EXCEL
# -----------------------------------------
df = pd.read_excel("TEST 1.xlsx")

# -----------------------------------------
# 2. REMOVE CS2 ROWS
# -----------------------------------------
if "LOCATION" in df.columns:
    df = df[df["LOCATION"] != "CS2"]

# -----------------------------------------
# 3. REMOVE CS2 COLUMN (if present)
# -----------------------------------------
df = df.drop(columns=["CS2"], errors="ignore")

# -----------------------------------------
# 4. REMOVE PO + UID NO. COLUMNS
# -----------------------------------------
columns_to_drop = ["PO", "UID NO."]
df = df.drop(columns=[c for c in columns_to_drop if c in df.columns])

# -----------------------------------------
# 5. REMOVE EMPTY CS1 ROWS
# -----------------------------------------
if "CS1" in df.columns:
    df = df[df["CS1"].notna() & (df["CS1"] != "") & (df["CS1"] != "None")]

# -----------------------------------------
# 6. FIX DATE FORMAT TO DD-MM-YYYY
# -----------------------------------------
date_columns = ["DATE OF REPACK", "DATE OF PRODUCTION"]

for col in date_columns:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors="coerce").dt.strftime("%d-%m-%Y")

# -----------------------------------------
# 7. FINAL COLUMN REARRANGEMENT
# -----------------------------------------
desired_order = [
    "STATUS",
    "FCL NO.",
    "ENTERED BY",
    "DATE OF REPACK",
    "DATE OF PRODUCTION",
    "PRODUCT ID",
    "PACKING STYLE",
    "PRODUCT",
    "GRADE",
    "PACK SIZE",
    "BRAND",
    "CARTONS",
    "LOT NO",
    "TRACE ID",
    "DAY CODE",
    "LOOSE BAGS",
    "KG LOOSE",
    "PALLET ID",
    "CS1",
    "REMARKS",
    "NAV ID",
    "KGs",
    "POUNDS",
    "COLUMN1"
]

# Reorder columns (only keep those that exist)
df = df[[col for col in desired_order if col in df.columns]]

# -----------------------------------------
# 8. SHOW CLEANED FINAL TABLE
# -----------------------------------------
st.dataframe(df)
# REMOVE EMPTY / NONE / "--" ROWS IN CS1
if "CS1" in df.columns:
    df = df[
        df["CS1"].notna() &
        (df["CS1"] != "") &
        (df["CS1"] != "None") &
        (df["CS1"] != "--")
    ]









