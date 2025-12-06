import streamlit as st
import pandas as pd

st.title("Mike 1 Inventory Page (CS1 Only)")

df = pd.read_excel("TEST 1.xlsx")

# Show columns for debugging
# st.write(df.columns)

# Filter using the correct column name
df = df[df["CS2"] == "CS1"]

# Remove unwanted columns
columns_to_drop = ["FCL No", "PO", "UID No", "CS2"]

for col in columns_to_drop:
    if col in df.columns:
        df = df.drop(columns=[col])

# Fix dates
for col in df.columns:
    if "date" in col.lower():
        df[col] = pd.to_datetime(df[col], errors="coerce").dt.strftime("%d-%m-%Y")

st.dataframe(df)




