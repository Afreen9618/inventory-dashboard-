import streamlit as st

st.set_page_config(page_title="Inventory Dashboard", layout="wide")

st.markdown("<h1 style='text-align:center;'>Select Inventory Dashboard</h1>", unsafe_allow_html=True)
st.write("")

col1, col2 = st.columns(2)

with col1:
    if st.button("📦 MIKE 1 INVENTORY", use_container_width=True):
        st.switch_page("pages/mike1.py")

with col2:
    if st.button("📦 MIKE 2 INVENTORY", use_container_width=True):
        st.switch_page("pages/mike2.py")
