import streamlit as st
import pandas as pd
import altair as alt

st.title("Inventory Cleaner")

uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # -------------------------------
    # 1. REMOVE CS2 ROWS COMPLETELY
    # -------------------------------
    if "CS2" in df.columns:
        df = df[df["CS2"].isna()]  # keep only rows where CS2 is empty
        df = df.drop(columns=["CS2"])  # remove CS2 column

    # -------------------------------
    # 2. REMOVE COLUMNS: FCL NO, PO, UID NO
    # -------------------------------
    for col in ["FCL NO", "PO", "UID NO"]:
        if col in df.columns:
            df = df.drop(columns=[col])

    # -------------------------------
    # 3. FIX DATE FORMAT
    # -------------------------------
    df["DATE"] = pd.to_datetime(df["DATE"], errors="coerce")
    df["DATE"] = df["DATE"].dt.strftime("%d-%m-%Y")

    # -------------------------------
    # 4. REMOVE ROWS WHERE CS1 == "--"
    # -------------------------------
    df = df[df["CS1"] != "--"]

    # -------------------------------
    # 5. REARRANGE COLUMNS
    # -------------------------------
    desired_order = [
        "STATUS", "FCL NO.", "ENTERED BY", "DATE OF REPACK", "DATE OF PRODUCTION",
        "PRODUCT ID", "PACKING STYLE", "PRODUCT", "GRADE", "PACK SIZE", "BRAND",
        "CARTONS", "LOT NO", "TRACE ID", "DAY CODE", "LOOSE BAGS", "KG LOOSE",
        "PALLET ID", "CS1", "REMARKS", "NAV ID", "KGs", "POUNDS", "COLUMN1"
    ]

    # Keep only existing columns from desired order
    existing_cols = [c for c in desired_order if c in df.columns]
    other_cols = [c for c in df.columns if c not in existing_cols]
    df = df[existing_cols + other_cols]

    # -------------------------------
    # 6. SUMMARY — TOTAL CARTONS
    # -------------------------------
    if "CARTONS" in df.columns:
        total_cartons = df["CARTONS"].sum()
        st.subheader(f"📦 Total Cartons: **{total_cartons}**")

    # -------------------------------
    # 7. DISPLAY CLEANED DATA
    # -------------------------------
    st.write("### Cleaned Inventory Data")
    st.dataframe(df)

    # -------------------------------
    # 8. CHARTS (Daily, Weekly, Monthly)
    # -------------------------------

    # Convert date for grouping
    df_chart = df.copy()
    df_chart["DATE"] = pd.to_datetime(df_chart["DATE"], format="%d-%m-%Y", errors="coerce")

    if "CARTONS" not in df_chart.columns:
        st.warning("CARTONS column missing — charts cannot be generated.")
    else:
        st.subheader("📅 Daily Cartons Chart")
        daily = df_chart.groupby("DATE")["CARTONS"].sum().reset_index()
        daily_chart = alt.Chart(daily).mark_bar().encode(
            x="DATE:T", y="CARTONS:Q"
        )
        st.altair_chart(daily_chart, use_container_width=True)

        st.subheader("📆 Weekly Cartons Chart")
        df_chart["WEEK"] = df_chart["DATE"].dt.to_period("W").apply(lambda r: r.start_time)
        weekly = df_chart.groupby("WEEK")["CARTONS"].sum().reset_index()
        weekly_chart = alt.Chart(weekly).mark_bar().encode(
            x="WEEK:T", y="CARTONS:Q"
        )
        st.altair_chart(weekly_chart, use_container_width=True)

        st.subheader("📅 Monthly Cartons Chart")
        df_chart["MONTH"] = df_chart["DATE"].dt.to_period("M").dt.to_timestamp()
        monthly = df_chart.groupby("MONTH")["CARTONS"].sum().reset_index()
        monthly_chart = alt.Chart(monthly).mark_bar().encode(
            x="MONTH:T", y="CARTONS:Q"
        )
        st.altair_chart(monthly_chart, use_container_width=True)

else:
    st.info("Upload a CSV file to continue.")













