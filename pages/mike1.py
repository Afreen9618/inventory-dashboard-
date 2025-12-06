import pandas as pd
from datetime import datetime

# --------- LOAD YOUR DATA ----------
df = pd.read_csv("your_file.csv")

# --------- FIX DATE FORMAT ----------
def fix_date(date_value):
    try:
        return pd.to_datetime(date_value).strftime("%d-%m-%Y")
    except:
        return ""

if "DATE OF REPACK" in df.columns:
    df["DATE OF REPACK"] = df["DATE OF REPACK"].apply(fix_date)

if "DATE OF PRODUCTION" in df.columns:
    df["DATE OF PRODUCTION"] = df["DATE OF PRODUCTION"].apply(fix_date)

# --------- CLEAN CS1 COLUMN ----------
if "CS1" in df.columns:
    df["CS1"] = df["CS1"].astype(str).str.strip()

    df = df[
        (df["CS1"] != "--") &
        (df["CS1"] != "") &
        (df["CS1"] != "None") &
        (df["CS1"] != "nan")
    ]

# --------- REORDER COLUMNS ----------
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

# Keep only columns that exist
final_columns = [col for col in desired_columns if col in df.columns]

df = df[final_columns]

# --------- SAVE CLEANED FILE ----------
df.to_csv("cleaned_output.csv", index=False)
print("✔ Completed: cleaned_output.csv generated")









