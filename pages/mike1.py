import streamlit as st
import pandas as pd

st.title("Inventory Cleaner")

uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    # ---------- FIX DATE FORMAT ----------
    def fix_date(val):
        try:
            return pd.to_datetime(val).strftime("%d-%m-%Y")
        except:
            return ""

    if "DATE OF REPACK" in df.columns:
        df["DATE OF REPACK"] = df["DATE OF REPACK"].apply(fix_date)

    if "DATE OF PRODUCTION" in df.columns:
        df["DATE OF PRODUCTION"] = df["DATE OF PRODUCTION"].apply(fix_date)

    # ---------- CLEAN CS1 ----------
    if "CS1" in df.columns:
        df["CS1"] = df["CS1"].astype(str).str.strip()

        df = df[
            (df["CS1"] != "--") &
            (df["CS1"] != "") &
            (df["CS1"] != "None") &
            (df["CS1"] != "nan")
        ]

    # ---------- REORDER COLUMNS ----------
    desired_columns = [
        "STATUS",
        "FCL NO.",
        "ENTERED BY",
        "DATE OF REPACK",
        "DATE OF PRODUCTION",
        "PRODUCT ID",
        "PACKING STYLE",
        "PRODUCT",
        "GRADE",
        "PACK SIZE",
        "BRAND",
        "CARTONS",
        "LOT NO",
        "TRACE ID",
        "DAY CODE",
        "LOOSE BAGS",
        "KG LOOSE",
        "PALLET ID",
        "CS1",
        "REMARKS",
        "NAV ID",
        "KGs",
        "POUNDS",
        "COLUMN1"
    ]

    final_cols = [c for c in desired_columns if c in df.columns]

    df = df[final_cols]

    st.success("File cleaned successfully!")

    st.dataframe(df)

    # DOWNLOAD CLEANED FILE
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download Cleaned CSV", csv, "cleaned_output.csv")

else:
    st.info("Upload a CSV file to continue.")










