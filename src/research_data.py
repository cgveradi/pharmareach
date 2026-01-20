import pandas as pd
import sqlite3
import time
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_RESEARCH = BASE_DIR / "data" / "raw" / \
    "OP_DTL_RSRCH_PGYR2024_P06302025_06162025.csv"
DB_PATH = BASE_DIR / "data" / "processed" / "PharmaReach_2024.db"


def ingest_research():
    start_time = time.time()

    cols = [
        'Applicable_Manufacturer_or_Applicable_GPO_Making_Payment_Name',
        'Total_Amount_of_Payment_USDollars',
        'Covered_Recipient_Profile_ID',
        'Recipient_City',
        'Recipient_State',
        'Covered_Recipient_Specialty_1',
        'Date_of_Payment'
    ]

    conn = sqlite3.connect(DB_PATH)
    print("🧪 Ingesting Research Engine...")

    # Research file chunk for safety
    reader = pd.read_csv(RAW_RESEARCH, usecols=cols,
                         chunksize=100000, low_memory=False)

    for i, chunk in enumerate(reader):
        chunk.to_sql('research_payments', conn,
                     if_exists='append', index=False)
        if i % 5 == 0:
            print(f"Processed {i * 100000} research rows...")

    conn.close()
    print(f"✅ Research Ingested in {(time.time() - start_time)/60:.2f} mins")


if __name__ == "__main__":
    ingest_research()
