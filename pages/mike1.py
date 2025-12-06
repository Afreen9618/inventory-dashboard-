import streamlit as st
import pandas as pd

st.title("Mike 1 Inventory Page")

# Load Excel file
df = pd.read_excel("TEST 1.xlsx")

# 1️⃣ Remove all rows where CS2 has data (not empty)
if "CS2" in df.columns:
    df = df[df["CS2"].isna() | (df["CS2"] == "")]

# 2️⃣ Remove CS2 column completely
if "CS2" in df.columns:
    df = df.drop(columns=["CS2"])

# Show cleaned data
st.dataframe(df)


