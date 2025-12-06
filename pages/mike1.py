import streamlit as st
import pandas as pd

st.title("Mike 1 Inventory Page")

# Load Excel
df = pd.read_excel("TEST 1.xlsx")

# Remove CS2 column if it exists
if "CS2" in df.columns:
    df = df.drop(columns=["CS2"])

# Show dataframe without CS2
st.dataframe(df)

