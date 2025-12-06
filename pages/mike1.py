import streamlit as st
import pandas as pd

st.title("Mike 1 Inventory Page")

df = pd.read_excel("TEST 1.xlsx")

# Remove CS2 rows
if "LOCATION" in df.columns:
    df = df[df["LOCATION"] != "CS2"]

# Correct column names to drop
columns_to_drop = ["FCL NO.", "PO", "UID NO."]

df = df.drop(columns=[c for c in columns_to_drop if c in df.columns])

# Fix date format
date_columns = ["DATE OF REPACKING", "DATE OF PRODUCTION"]

for col in date_columns:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors="coerce").dt.strftime("%d-%m-%Y")

st.dataframe(df)







