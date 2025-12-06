import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Inventory Cleaner", layout="wide")

st.title("📦 Inventory Cleaner Dashboard")

# -----------------------------
# YOUR TEST DATA HERE
# -----------------------------
st.subheader("Using Test Data (No CSV Required)")

data = {
    "Date": pd.date_range(end=pd.Timestamp.today(), periods=9),
    "Value": [1,2,3,4,5,6,7,8,9]     # <-- YOUR TEST DATA
}

df = pd.DataFrame(data)

st.write("### Test Data Preview")
st.dataframe(df)

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
# DISPLAY CHARTS
# -----------------------------
show_chart("📅 Daily Activity", daily, "Date", "Count")
show_chart("📆 Weekly Activity", weekly, "Week", "Count")
show_chart("🗓 Monthly Activity", monthly, "Date", "Count")


















