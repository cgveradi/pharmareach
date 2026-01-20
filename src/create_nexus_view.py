import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path("data/processed/PharmaReach_2024.db")
NEXUS_DB_PATH = Path("data/processed/HVT_Analysis_Final.db")


def fix_nexus_view():
    conn = sqlite3.connect(DB_PATH)

    # We'll use a slightly different approach: Create the DataFrame first, then save.
    print("🛰️ Extracting data and calculating 'Primary_Manufacturer'...")

    query = """
    SELECT 
        Covered_Recipient_Profile_ID as ID, 
        MAX(Covered_Recipient_First_Name) as First_Name, 
        MAX(Covered_Recipient_Last_Name) as Last_Name,
        CASE 
             WHEN Covered_Recipient_Specialty_1 LIKE '%Oncology%' THEN 'Oncology'
             WHEN Covered_Recipient_Specialty_1 LIKE '%Cardiovascular%' THEN 'Cardiology'
             WHEN Covered_Recipient_Specialty_1 LIKE '%Neurology%' THEN 'Neurology'
        END as Specialty,
        SUM(Total_Amount_of_Payment_USDollars) as Total_Spend,
        (SELECT Applicable_Manufacturer_or_Applicable_GPO_Making_Payment_Name 
         FROM payments p2 
         WHERE p2.Covered_Recipient_Profile_ID = payments.Covered_Recipient_Profile_ID 
         GROUP BY 1 ORDER BY SUM(Total_Amount_of_Payment_USDollars) DESC LIMIT 1) as Primary_Manufacturer
    FROM payments
    WHERE Specialty IS NOT NULL
    GROUP BY ID;
    """

    df = pd.read_sql(query, conn)

    # Save to your analysis database
    target_conn = sqlite3.connect(NEXUS_DB_PATH)
    df.to_sql('Physician_Nexus_View', target_conn,
              if_exists='replace', index=False)
    print(f"✅ Success! Nexus View created with {len(df)} rows.")

    conn.close()
    target_conn.close()


if __name__ == "__main__":
    fix_nexus_view()
