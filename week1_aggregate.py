from pathlib import Path

import pandas as pd


# ---------------------------------------------------------
# 1. Define project folders
# ---------------------------------------------------------

# This script is stored inside the scripts folder.
PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "outputs"

# Create outputs folder if it does not already exist.
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------
# 2. Define the required month range: 202401 to 202604
# ---------------------------------------------------------

months = pd.period_range(
    start="2024-01",
    end="2026-04",
    freq="M"
).strftime("%Y%m").tolist()


# ---------------------------------------------------------
# 3. Build the Listing file list
# ---------------------------------------------------------

listing_files = []

for month in months:
    file_path = DATA_DIR / f"CRMLSListing{month}.csv"

    if not file_path.exists():
        raise FileNotFoundError(
            f"Missing Listing file for {month}: {file_path.name}"
        )

    listing_files.append(file_path)


# ---------------------------------------------------------
# 4. Build the Sold file list
# ---------------------------------------------------------

sold_files = []

for month in months:
    regular_file = DATA_DIR / f"CRMLSSold{month}.csv"
    filled_file = DATA_DIR / f"CRMLSSold{month}_filled.csv"

    # Prefer the regular file.
    if regular_file.exists():
        sold_files.append(regular_file)

    # Use the filled version only if the regular file is unavailable.
    elif filled_file.exists():
        sold_files.append(filled_file)

    else:
        raise FileNotFoundError(
            f"Missing Sold file for {month}. "
            f"Expected {regular_file.name} or {filled_file.name}."
        )


# ---------------------------------------------------------
# 5. Function for loading and combining monthly files
# ---------------------------------------------------------

def combine_monthly_files(file_paths, dataset_name):
    """
    Read monthly CSV files and concatenate them into one DataFrame.
    A SourceMonth column is added so each row can be traced back
    to its original monthly file.
    """

    monthly_dataframes = []

    for file_path in file_paths:
        print(f"Reading {dataset_name}: {file_path.name}")

        df = pd.read_csv(
            file_path,
            low_memory=False
        )

        # Extract YYYYMM from the filename.
        source_month = file_path.stem[-6:]

        # Handle filenames ending with "_filled".
        if file_path.stem.endswith("_filled"):
            source_month = file_path.stem.replace("_filled", "")[-6:]

        df["SourceMonth"] = source_month
        monthly_dataframes.append(df)

        print(f"  Rows loaded: {len(df):,}")

    combined_df = pd.concat(
        monthly_dataframes,
        ignore_index=True,
        sort=False
    )

    return combined_df


# ---------------------------------------------------------
# 6. Concatenate Listing and Sold datasets separately
# ---------------------------------------------------------

listing_combined = combine_monthly_files(
    listing_files,
    dataset_name="Listing"
)

sold_combined = combine_monthly_files(
    sold_files,
    dataset_name="Sold"
)


# ---------------------------------------------------------
# 7. Confirm row counts after concatenation
# ---------------------------------------------------------

# Row count after concatenating all monthly Listing files.
listing_rows_after_concat = len(listing_combined)

# Row count after concatenating all monthly Sold files.
sold_rows_after_concat = len(sold_combined)

print("\nROW COUNTS AFTER CONCATENATION")
print("--------------------------------")
print(f"Listing rows: {listing_rows_after_concat:,}")
print(f"Sold rows:    {sold_rows_after_concat:,}")


# ---------------------------------------------------------
# 8. Validate that PropertyType exists
# ---------------------------------------------------------

for dataset_name, dataframe in [
    ("Listing", listing_combined),
    ("Sold", sold_combined)
]:
    if "PropertyType" not in dataframe.columns:
        raise KeyError(
            f"'PropertyType' column was not found in the "
            f"{dataset_name} dataset."
        )


# ---------------------------------------------------------
# 9. Inspect PropertyType values
# ---------------------------------------------------------

print("\nLISTING PROPERTY TYPES")
print(listing_combined["PropertyType"].value_counts(dropna=False).head(20))

print("\nSOLD PROPERTY TYPES")
print(sold_combined["PropertyType"].value_counts(dropna=False).head(20))


# ---------------------------------------------------------
# 10. Filter both datasets to Residential only
# ---------------------------------------------------------

# Row counts immediately before applying the Residential filter.
listing_rows_before_filter = len(listing_combined)
sold_rows_before_filter = len(sold_combined)

listing_residential = listing_combined[
    listing_combined["PropertyType"]
    .astype(str)
    .str.strip()
    .eq("Residential")
].copy()

sold_residential = sold_combined[
    sold_combined["PropertyType"]
    .astype(str)
    .str.strip()
    .eq("Residential")
].copy()

# Row counts after applying the Residential filter.
listing_rows_after_filter = len(listing_residential)
sold_rows_after_filter = len(sold_residential)


# ---------------------------------------------------------
# 11. Print the required row-count confirmation
# ---------------------------------------------------------

print("\nRESIDENTIAL FILTER SUMMARY")
print("--------------------------------")
print(
    f"Listing: {listing_rows_before_filter:,} rows before filter, "
    f"{listing_rows_after_filter:,} rows after filter"
)

print(
    f"Sold: {sold_rows_before_filter:,} rows before filter, "
    f"{sold_rows_after_filter:,} rows after filter"
)


# ---------------------------------------------------------
# 12. Save the final combined datasets
# ---------------------------------------------------------

listing_output = OUTPUT_DIR / "listings.csv"
sold_output = OUTPUT_DIR / "sold.csv"

listing_residential.to_csv(
    listing_output,
    index=False
)

sold_residential.to_csv(
    sold_output,
    index=False
)

print("\nFILES SAVED")
print("--------------------------------")
print(f"Listing output: {listing_output}")
print(f"Sold output:    {sold_output}")

