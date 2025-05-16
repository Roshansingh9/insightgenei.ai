import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os


load_dotenv()
# 1. Your PostgreSQL connection URL (from Railway or other host)
DATABASE_URL = os.getenv("DATABASE_URL")

# 2. Path to your CSV file
CSV_PATH = "bike_sales_india.csv"  # change this to your actual file path

# 3. Clean column mapping
column_mapping = {
    "State": "state",
    "Avg Daily Distance (km)": "avg_daily_distance_km",
    "Brand": "brand",
    "Model": "model",
    "Price (INR)": "price_inr",
    "Year of Manufacture": "year_of_manufacture",
    "Engine Capacity (cc)": "engine_capacity_cc",
    "Fuel Type": "fuel_type",
    "Mileage (km/l)": "mileage_kmpl",
    "Owner Type": "owner_type",
    "Registration Year": "registration_year",
    "Insurance Status": "insurance_status",
    "Seller Type": "seller_type",
    "Resale Price (INR)": "resale_price_inr",
    "City Tier": "city_tier"
}

# 4. Read and clean the CSV
df = pd.read_csv(CSV_PATH)
df = df[list(column_mapping.keys())]  # only keep the 15 expected columns
df.rename(columns=column_mapping, inplace=True)

# 5. Upload to PostgreSQL
engine = create_engine(DATABASE_URL)


df.to_sql("motorcycle_sales", engine, if_exists="replace", index=False)

print(" CSV data uploaded to PostgreSQL successfully.")
