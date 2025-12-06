import streamlit as st
import pandas as pd

st.title("Mike 1 Inventory Page")

# Load Excel file directly
df = pd.read_excel("TEST 1.xlsx")

# ---------- FIX DATE FORMAT ----------
def fix_date(val):
    try:
        return pd.to_datetime(val).strftime("%d-%m-%Y")
    except:
        return ""

if "DATE OF REPACK" in df.columns:
    df["DATE OF REPACK"] = df["DATE OF REPACK"].apply(fix_date)

if "DATE OF PRODUCTION" in df.columns:
    df["DATE OF PRODUCTION"] = df["DATE OF PRODUCTION"].apply(fix_date)

# ---------- CLEAN CS1 ----------
if "CS1" in df.columns:
    df["CS1"] = df["CS1"].astype(str).str.strip()

    df = df[
        (df["CS1"] != "--") &
        (df["CS1"] != "") &
        (df["CS1"] != "None") &
        (df["CS1"] != "nan")
    ]

# ---------- REMOVE COLUMNS ----------
cols_to_remove = ["FCL NO.", "UID NO.", "PO"]  # remove unwanted columns
df = df.drop(columns=[c for c in cols_to_remove if c in df.columns])

# ---------- REORDER COLUMNS ----------
desired_columns = [
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

final_cols = [c for c in desired_columns if c in df.columns]

df = df[final_cols]

st.dataframe(df)











