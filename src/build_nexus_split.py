import sqlite3
import pandas as pd
from pathlib import Path

RAW_DB_PATH = Path("data/processed/PharmaReach_2024.db")
FINAL_DB_PATH = Path("data/processed/HVT_Analysis_Final.db")


def build_nexus_split():
    print("Step 1: Connecting to Raw Database...")
    conn = sqlite3.connect(RAW_DB_PATH)

    # 1. Get Commercial Spend & Physician Info
    print("Extracting Commercial Spend & Profiles...")
    comm_df = pd.read_sql("""
        SELECT Covered_Recipient_Profile_ID as ID, 
               Covered_Recipient_First_Name as First_Name, 
               Covered_Recipient_Last_Name as Last_Name,
               CASE 
                 WHEN Covered_Recipient_Specialty_1 LIKE '%Oncology%' THEN 'Oncology'
                 WHEN Covered_Recipient_Specialty_1 LIKE '%Cardiovascular%' THEN 'Cardiology'
                 WHEN Covered_Recipient_Specialty_1 LIKE '%Neurology%' THEN 'Neurology'
               END as Specialty,
               Applicable_Manufacturer_or_Applicable_GPO_Making_Payment_Name as Manufacturer,
               Total_Amount_of_Payment_USDollars as Amount
        FROM payments 
        WHERE Specialty IS NOT NULL
    """, conn)

    # 2. Get Research Spend
    print("Extracting Research Spend...")
    res_df = pd.read_sql("""
        SELECT Covered_Recipient_Profile_ID as ID, 
               SUM(Total_Amount_of_Payment_USDollars) as Research_Spend
        FROM research_payments 
        GROUP BY ID
    """, conn)

    conn.close()

    print("Processing Primary Manufacturers...")
    # Find which manufacturer paid each doctor the most
    # We group by ID and Manufacturer, sum the amount, and pick the top one
    mfg_focus = comm_df.groupby(['ID', 'Manufacturer'])[
        'Amount'].sum().reset_index()
    primary_mfg = mfg_focus.sort_values(
        'Amount', ascending=False).drop_duplicates('ID')
    primary_mfg = primary_mfg[['ID', 'Manufacturer']].rename(
        columns={'Manufacturer': 'Primary_Manufacturer'})

    print("Aggregating Commercial Totals...")
    # Now we collapse the commercial data into one row per doctor
    comm_final = comm_df.groupby(['ID', 'First_Name', 'Last_Name', 'Specialty'])[
        'Amount'].sum().reset_index()
    comm_final = comm_final.rename(columns={'Amount': 'Commercial_Spend'})

    print("Final Merge...")
    # Join everything together
    final_df = pd.merge(comm_final, res_df, on='ID', how='left')
    final_df = pd.merge(final_df, primary_mfg, on='ID', how='left')

    # Fill empty research spend with 0 and calculate Total
    final_df['Research_Spend'] = final_df['Research_Spend'].fillna(0)
    final_df['Total_Spend'] = final_df['Commercial_Spend'] + \
        final_df['Research_Spend']

    # 3. Save to Final DB
    print("Saving to HVT_Analysis_Final.db...")
    target_conn = sqlite3.connect(FINAL_DB_PATH)
    final_df.to_sql('Physician_Nexus_Raw', target_conn,
                    if_exists='replace', index=False)
    target_conn.close()

    print(f"SUCCESS! Physician_Nexus_Raw created with {len(final_df)} rows.")


if __name__ == "__main__":
    build_nexus_split()
