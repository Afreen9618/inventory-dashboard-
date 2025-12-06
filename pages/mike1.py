import streamlit as st
import pandas as pd

st.title("Mike 1 Inventory Page (CS1 Only)")

# Load Excel file
df = pd.read_excel("TEST 1.xlsx")

# Keep only CS1 rows
df = df[df["Location"] == "CS1"]

# Remove unwanted columns if they exist
columns_to_drop = ["FCL No", "PO", "UID No", "CS2", "cs2", "Cs2"]

for col in columns_to_drop:
    if col in df.columns:
        df = df.drop(columns=[col])

# Fix date formatting if column exists
date_columns = ["Date", "Received Date", "Updated Date"]

for col in date_columns:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors="coerce").dt.strftime("%d-%m-%Y")

st.subheader("Filtered Inventory Data (CS1 Only)")
st.dataframe(df)



