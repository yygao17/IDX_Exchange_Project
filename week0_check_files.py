from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = PROJECT_ROOT / "data"

print("Project root:", PROJECT_ROOT)
print("Data directory:", DATA_DIR)
print("Data directory exists:", DATA_DIR.exists())

listing_files = sorted(DATA_DIR.glob("CRMLSListing*.csv"))
sold_files = sorted(DATA_DIR.glob("CRMLSSold*.csv"))

print(f"\nListing files found: {len(listing_files)}")
print(f"Sold files found: {len(sold_files)}")

print("\nFirst few listing files:")
for file in listing_files[:5]:
    print(file.name)

print("\nFirst few sold files:")
for file in sold_files[:5]:
    print(file.name)

if listing_files:
    listing_sample = pd.read_csv(listing_files[0])
    print("\nListing sample shape:", listing_sample.shape)
    print(listing_sample.head())

if sold_files:
    sold_sample = pd.read_csv(sold_files[0])
    print("\nSold sample shape:", sold_sample.shape)
    print(sold_sample.head())



############
# Open and preview the first listing CSV
listing_sample = pd.read_csv(listing_files[0])

print("\nColumns:")
print(listing_sample.columns.tolist())

print("\nFirst 5 rows:")
print(listing_sample.head())

print("\nDataset shape:")
print(listing_sample.shape)


sold_sample = pd.read_csv(sold_files[0])

print("\nSold columns:")
print(sold_sample.columns.tolist())

print("\nFirst 5 sold rows:")
print(sold_sample.head())

print("\nSold dataset shape:")
print(sold_sample.shape)