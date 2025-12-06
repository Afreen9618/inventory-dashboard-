import pandas as pd
import streamlit as st
df = pd.read_excel("TEST 1.xlsx")

# Remove rows belonging to CS2
if "CS2" in df.columns:
    df = df[df["CS2"].isna() | (df["CS2"] == "")]

# Remove CS2 column
df = df.drop(columns=["CS2"], errors="ignore")

# Remove columns FCL NO, PO, UID NO
cols_to_remove = ["FCL NO", "PO", "UID NO"]
df = df.drop(columns=[col for col in cols_to_remove if col in df.columns], errors="ignore")

# REMOVE ROWS WHERE CS1 IS EMPTY OR NONE
df = df[df["CS1"].notna() & (df["CS1"] != "") & (df["CS1"] != "None")]

# Convert date columns to DD-MM-YYYY
for col in df.columns:
    if "date" in col.lower():
        df[col] = pd.to_datetime(df[col], errors="coerce").dt.strftime("%d-%m-%Y")

st.dataframe(df)






