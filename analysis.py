"""
BrainLat Dictionary CSV - Quick Analysis
---------------------------------------
Reads your data-dictionary CSV (Term, Definition, Code, Table)
and prints an easy summary + quick checks.
"""

import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 120)

FILE = "BrainLat_dataset_dictionary.csv"

# 1) Load (handles spaces after commas)
df = pd.read_csv(FILE, encoding="latin1", skipinitialspace=True)

print("\nLoaded:", FILE)
print("Rows:", len(df), " | Columns:", len(df.columns))
print("Columns:", df.columns.tolist())

# 2) Preview
print("\n--- Preview (first 10 rows) ---")
print(df.head(10).to_string(index=False))

# 3) Missing values
print("\n--- Missing values per column ---")
print(df.isna().sum())

# 4) Duplicate terms
if "Term" in df.columns:
    dup = df[df.duplicated("Term", keep=False)].sort_values("Term")
    print("\n--- Duplicate Term rows ---")
    if len(dup) == 0:
        print("No duplicate terms!")
    else:
        print(dup.to_string(index=False))

# 5) What tables exist + how many terms in each table
if "Table" in df.columns:
    # Table field can contain multiple tables separated by commas
    # Example: "BrainLat_Demographic, BrainLat_Cognition, BrainLat_records"
    table_series = (
        df["Table"]
        .dropna()
        .astype(str)
        .str.split(",")
        .explode()
        .str.strip()
    )

    print("\n--- Unique tables listed ---")
    print(sorted(table_series.unique()))

    print("\n--- Number of terms per table ---")
    print(table_series.value_counts())

# 6) Which terms have codebooks / ranges etc.
if "Code" in df.columns:
    code_present = df["Code"].fillna("").astype(str).str.strip().ne("")
    print("\n--- Code field ---")
    print("Rows with a Code:", code_present.sum(), "/", len(df))

    print("\nExamples with Code:")
    print(df.loc[code_present, ["Term", "Code"]].head(15).to_string(index=False))

print("\nDone!")
