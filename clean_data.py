
from pathlib import Path
import pandas as pd

# Find the project folder and original dataset
folder = Path(__file__).parent

files = [
    f for f in folder.glob("*.csv")
    if f.name != "hospital_cleaned.csv"
]

if not files:
    raise FileNotFoundError(
        "Original hospital CSV not found in the project folder."
    )

file_path = files[0]
output_file = folder / "hospital_cleaned.csv"

print("Loading original dataset...")
df = pd.read_csv(file_path, low_memory=False)

# Standardise column-name spacing
df.columns = df.columns.str.strip()

print("\n--- ORIGINAL DATASET ---")
print("Rows:", f"{len(df):,}")
print("Columns:", len(df.columns))

# Convert relevant numerical columns
numeric_columns = [
    "Length of Stay",
    "Total Charges",
    "Total Costs",
    "Birth Weight",
]

for column in numeric_columns:
    if column in df.columns:
        before = df[column].isna().sum()

        df[column] = pd.to_numeric(
            df[column].astype("string").str.replace(
                ",", "", regex=False
            ).str.strip(),
            errors="coerce"
        )

        after = df[column].isna().sum()

        print(f"\n{column}")
        print("Missing before conversion:", f"{before:,}")
        print("Missing after conversion:", f"{after:,}")

# Report missing values
print("\n--- MISSING VALUES ---")
missing = df.isna().sum()
missing = missing[missing > 0].sort_values(ascending=False)

if missing.empty:
    print("No missing values found.")
else:
    print(missing.to_string())

# Report duplicates, but do not remove them automatically
print("\n--- DUPLICATE CHECK ---")
print("Exact duplicate rows:", f"{df.duplicated().sum():,}")

# Save prepared data separately
print("\nSaving prepared dataset...")
df.to_csv(output_file, index=False)

print("\n--- CLEANING SUMMARY ---")
print("Prepared file:", output_file.name)
print("Rows retained:", f"{len(df):,}")
print("Columns retained:", len(df.columns))
print("Data types converted where possible.")
print("Original file unchanged.")
print("\nInitial cleaning completed!")
