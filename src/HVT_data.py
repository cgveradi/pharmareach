import sqlite3
import pandas as pd
from pathlib import Path

# Paths
SOURCE_DB = Path(r'data/processed/PharmaReach_2024.db')
TARGET_DB = Path(r'data/processed/HVT_Analysis_2024.db')

# 1. Connect to the source
source_conn = sqlite3.connect(SOURCE_DB)

# 2. Extract data into a DataFrame

query = """
SELECT * FROM payments
WHERE Covered_Recipient_Specialty_1 LIKE '%Oncology%'
   OR Covered_Recipient_Specialty_1 LIKE '%Cardiovascular Disease%'
   OR Covered_Recipient_Specialty_1 LIKE '%Neurology%';
"""

hvt_df = pd.read_sql(query, source_conn)

# 3. Save to a BRAND NEW database file
target_conn = sqlite3.connect(TARGET_DB)
hvt_df.to_sql('hvt_payments', target_conn, if_exists='replace', index=False)

print(f"✅ Success!")
print(f"Created a fresh, lightweight analysis file: {TARGET_DB}")
print(f"Total rows in new file: {len(hvt_df)}")

# Close connections
source_conn.close()
target_conn.close()
