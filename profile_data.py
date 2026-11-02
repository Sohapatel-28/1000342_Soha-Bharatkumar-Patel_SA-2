
from pathlib import Path
import pandas as pd

folder = Path(__file__).parent

files = [
    f for f in folder.iterdir()
    if f.suffix.lower() in [".csv", ".xlsx", ".xls"]
    and not f.name.startswith("~$")
]

if not files:
    print("Dataset not found.")
else:
    file_path = files[0]

    print("Loading dataset. Please wait...")

    # Read the complete dataset
    if file_path.suffix.lower() == ".csv":
        df = pd.read_csv(file_path, low_memory=False)
    else:
        df = pd.read_excel(file_path)

    print("\n========== DATASET OVERVIEW ==========")
    print("File:", file_path.name)
    print("Total rows:", f"{len(df):,}")
    print("Total columns:", len(df.columns))

    print("\n========== COLUMN NAMES ==========")
    for column in df.columns:
        print("-", column)

    print("\n========== DATA TYPES ==========")
    print(df.dtypes.to_string())

    print("\n========== MISSING VALUES ==========")
    missing = df.isnull().sum()
    missing = missing[missing > 0].sort_values(ascending=False)
    print(missing.to_string() if not missing.empty else "No missing values.")

    print("\n========== DUPLICATE ROWS ==========")
    print(df.duplicated().sum())

    print("\n========== NUMERICAL SUMMARY ==========")
    print(df.describe().to_string())

    print("\nInspection completed!")
