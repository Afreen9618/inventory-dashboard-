import streamlit as st
import pandas as pd

st.title("Mike 2 Inventory Page")

df = pd.read_excel("TEST 1.xlsx")

st.dataframe(df)
