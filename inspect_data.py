from pathlib import Path
import pandas as pd

# Locate the project folder
folder = Path(__file__).parent

# Find CSV and Excel files
files = [
    f for f in folder.iterdir()
    if f.suffix.lower() in [".csv", ".xlsx", ".xls"]
    and not f.name.startswith("~$")
]

if not files:
    print("No dataset found!")
    print("Please copy your hospital CSV or Excel file")
    print("into the HOSPITAL-DISCHARGES-DASHBOARD folder.")

else:
    print("\nAvailable datasets:")

    for i, file in enumerate(files, start=1):
        print(f"{i}. {file.name}")

    choice = int(input("\nEnter the dataset number: "))
    file_path = files[choice - 1]

    # Read only a small sample first
    if file_path.suffix.lower() == ".csv":
        df = pd.read_csv(file_path, nrows=1000)
    else:
        df = pd.read_excel(file_path, nrows=1000)

    print("\n--- FIRST 5 ROWS ---")
    print(df.head().to_string())

    print("\n--- COLUMN NAMES ---")
    print(df.columns.tolist())

    print("\n--- DATA TYPES ---")
    print(df.dtypes)

    print("\n--- MISSING VALUES ---")
    print(df.isnull().sum())

    print("\n--- DATASET SIZE INSPECTED ---")
    print("Rows:", len(df))
    print("Columns:", len(df.columns))

    print("\nInspection completed!")