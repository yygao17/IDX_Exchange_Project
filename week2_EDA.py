# check the files from first week (check on the first 5 rows)

import pandas as pd
from pathlib import Path

project_folder = Path("/Users/liu_caiyu/Projects/IDX Exchange Internship")
output_folder = project_folder / "outputs"

listings_path = output_folder / "listings.csv"
sold_path = output_folder / "sold.csv"

# Load only first 5 rows for quick testing
listings_sample = pd.read_csv(listings_path, nrows=5)
sold_sample = pd.read_csv(sold_path, nrows=5)

print("Listings sample shape:", listings_sample.shape)
print("Sold sample shape:", sold_sample.shape)

print("\nListings columns:")
print(listings_sample.columns.tolist())

print("\nSold columns:")
print(sold_sample.columns.tolist())

print("\nListings preview:")
print(listings_sample.head())

print("\nSold preview:")
print(sold_sample.head())

print("\nListings PropertyType sample:")
print(listings_sample["PropertyType"])

print("\nSold PropertyType sample:")
print(sold_sample["PropertyType"])

# -----------------------------------------------
# week 2 code

# Use the same actual file paths from above
listings = pd.read_csv(listings_path, low_memory=False)
sold = pd.read_csv(sold_path, low_memory=False)

# Dataset Understanding
# get rows, columns, data types, and missing values for listings
def inspect_structure(df, name):
    print(f"\n===== {name.upper()} STRUCTURE =====")
    print("Rows:", df.shape[0])
    print("Columns:", df.shape[1])
    print("\nColumn names:")
    print(df.columns.tolist())
    print("\nData types:")
    print(df.dtypes)
    print("\nPreview:")
    print(df.head())

inspect_structure(listings, "listings")
inspect_structure(sold, "sold")


# Missing Values Analysis
# Folder for Week 2 reports
week2_report_folder = output_folder / "week2_reports"
week2_report_folder.mkdir(exist_ok=True)

# -----------------------------------------------
# Missing Value Analysis

def create_missing_value_report(csv_path, dataset_name, chunksize=50000):
    """
    Create a missing value report for a large CSV file without loading
    the entire file into memory.

    Output includes:
    - column name
    - missing count
    - total row count
    - missing percentage
    - whether missing percentage is above 90%
    """

    print(f"\n===== Creating missing value report for {dataset_name.upper()} =====")

    total_rows = 0
    missing_counts = None

    # Read CSV in chunks
    for chunk in pd.read_csv(csv_path, chunksize=chunksize, low_memory=False):
        total_rows += len(chunk)

        chunk_missing = chunk.isna().sum()

        if missing_counts is None:
            missing_counts = chunk_missing
        else:
            missing_counts = missing_counts.add(chunk_missing, fill_value=0)

        print(f"Processed {total_rows:,} rows...")

    # Create report dataframe
    report = pd.DataFrame({
        "column": missing_counts.index,
        "missing_count": missing_counts.values,
        "total_rows": total_rows,
        "missing_percent": (missing_counts.values / total_rows * 100).round(2)
    })

    # Flag high-missing columns
    report["above_90_percent_missing"] = report["missing_percent"] > 90

    # Sort from most missing to least missing
    report = report.sort_values("missing_percent", ascending=False)

    # Save report
    output_path = week2_report_folder / f"{dataset_name}_missing_value_report.csv"
    report.to_csv(output_path, index=False)

    print(f"\nSaved missing value report to: {output_path}")

    print(f"\nColumns above 90% missing in {dataset_name}:")
    print(report[report["above_90_percent_missing"]])

    return report


listings_missing_report = create_missing_value_report(
    listings_path,
    dataset_name="listings"
)

sold_missing_report = create_missing_value_report(
    sold_path,
    dataset_name="sold"
)

