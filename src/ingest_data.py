import pandas as pd
import sqlite3
import time
from pathlib import Path

# Windows path management
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA = BASE_DIR / "data" / "raw" / \
    "OP_DTL_GNRL_PGYR2024_P06302025_06162025.csv"
DB_PATH = BASE_DIR / "data" / "processed" / "PharmaReach_2024.db"


def run_ingestion():
    start_time = time.time()

    cols = [
        'Applicable_Manufacturer_or_Applicable_GPO_Making_Payment_Name',
        'Total_Amount_of_Payment_USDollars',
        'Covered_Recipient_Specialty_1',
        'Recipient_City',
        'Recipient_State',
        'Nature_of_Payment_or_Transfer_of_Value',
        'Covered_Recipient_Profile_ID',
        'Covered_Recipient_First_Name',
        'Covered_Recipient_Last_Name',
        'Date_of_Payment'
    ]

    conn = sqlite3.connect(DB_PATH)
    print(f"--- Starting Ingestion of 8.6 GB Dataset ---")

    # Chunking to prevent 'MemoryError'
    reader = pd.read_csv(RAW_DATA, usecols=cols,
                         chunksize=200000, low_memory=False)

    for i, chunk in enumerate(reader):
        # Standardizing column names for SQL queries later
        chunk.columns = [c.replace(' ', '_').replace('.', '')
                         for c in chunk.columns]

        chunk.to_sql('payments', conn, if_exists='replace', index=False)

        if i % 5 == 0:
            print(f"Processed {i * 200000} rows...")

    conn.close()
    end_time = time.time()
    print(
        f"--- ✅ Success! Total Time: {(end_time - start_time) / 60:.2f} minutes ---")
    print(f"Database located at: {DB_PATH}")


if __name__ == "__main__":
    run_ingestion()
