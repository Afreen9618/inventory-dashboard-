import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

st.set_page_config(page_title="Inventory Cleaner", layout="wide")

st.title("📦 Inventory Cleaner Dashboard")

# -----------------------------
# GENERATE DUMMY DATA (NO CSV NEEDED)
# -----------------------------
st.write("Demo Mode: Showing dashboard without CSV upload.")

# Create 60 days of dummy data
dates = pd.date_range(end=pd.Timestamp.today(), periods=60)

data = {
    "Date": dates,
    "STATUS": np.random.choice(["SOLD", "UNSOLD", "PENDING"], size=60),
    "PRODUCT": np.random.choice(["Item A", "Item B", "Item C"], size=60),
    "QTY": np.random.randint(1, 50, size=60),
}

df = pd.DataFrame(data)

# -----------------------------
# GROUPING
# -----------------------------
daily = df.groupby(df["Date"].dt.date).size().reset_index(name="Count")
weekly = df.groupby(df["Date"].dt.isocalendar().week).size().reset_index(name="Count")
weekly.rename(columns={"week": "Week"}, inplace=True)
monthly = df.groupby(df["Date"].dt.strftime("%b")).size().reset_index(name="Count")

# -----------------------------
# CHART FUNCTION
# -----------------------------
def show_chart(title, data, x, y):
    st.subheader(title)
    chart = (
        alt.Chart(data)
        .mark_bar()
        .encode(
            x=x,
            y=y,
            tooltip=[x, y]
        )
        .properties(height=300)
    )
    st.altair_chart(chart, use_container_width=True)

# -----------------------------
# SHOW DASHBOARD
# -----------------------------
show_chart("📅 Daily Activity", daily, "Date", "Count")
show_chart("📆 Weekly Activity", weekly, "Week", "Count")
show_chart("🗓 Monthly Activity", monthly, "Date", "Count")

st.subheader("Raw Data")
st.dataframe(df)

















