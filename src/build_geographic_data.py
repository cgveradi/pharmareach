import pandas as pd
import sqlite3
import numpy as np
from pathlib import Path
from sklearn.preprocessing import MinMaxScaler

# 1. STANDARDIZED PATH LOGIC
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DB = BASE_DIR / "data" / "processed" / "PharmaReach_2024.db"
GOLD_DB = BASE_DIR / "data" / "processed" / "HVT_Analysis_Final.db"


def build_geographic_table():
    print(f"--- PHARMAREACH STANDARD: STRATEGIC GEOGRAPHIC BUILD ---")

    # 2. DATABASE CONNECTIONS
    if not RAW_DB.exists():
        print(f"Error: Raw database not found at {RAW_DB}")
        return

    conn_raw = sqlite3.connect(str(RAW_DB))
    conn_gold = sqlite3.connect(str(GOLD_DB))

    # --- STEP 1: EXTRACT GEOGRAPHIC METADATA ---
    print("Step 1: Extracting & Cleaning Raw Metadata...")
    geo_metadata = pd.read_sql("""
        SELECT DISTINCT 
            Covered_Recipient_Profile_ID as id, 
            Recipient_State as state, 
            Recipient_City as city 
        FROM payments
    """, conn_raw)

    # Standardize Casing and Strip Whitespace
    geo_metadata['city'] = geo_metadata['city'].str.strip().str.title()
    geo_metadata['state'] = geo_metadata['state'].str.strip().str.upper()

    # Deduplicate IDs (Primary Location Rule)
    geo_metadata = geo_metadata.drop_duplicates(subset=['id'], keep='first')

    # --- STEP 2: LOAD CLUSTERING RESULTS ---
    print("Step 2: Loading Cluster Strategy...")
    try:
        df_clusters = pd.read_sql(
            "SELECT * FROM Physician_Nexus_Final_Strategy", conn_gold)
    except Exception as e:
        print(
            f"❌ Error: Could not find Strategy table. Run Notebook 03 first! \n{e}")
        return

    # --- STEP 3: INITIAL MERGE ---
    print("Step 3: Merging Clusters with Geography...")
    df_merged = pd.merge(df_clusters, geo_metadata, on='id', how='left')

    # --- STEP 4: ENTITY RESOLUTION (CONSOLIDATING GHOST IDs) ---
    # This combines records for doctors like who have multiple IDs
    print("Step 4: Consolidating duplicate names (Entity Resolution)...")

    # We group by name and specialty to merge different IDs of the same human
    df_consolidated = df_merged.groupby(['full_name', 'specialty']).agg({
        'id': 'first',                # Keep a reference ID
        'city': 'first',              # Keep primary city
        'state': 'first',             # Keep primary state
        'segment_name': 'first',      # Keep assigned segment
        'commercial_spend': 'sum',    # Combine their money
        'research_spend': 'sum',      # Combine their research
        'total_spend': 'sum',         # Total combined wallet
        'primary_manufacturer': 'first',
        'influence_ratio': 'max',     # Take their highest scientific profile
        'mfg_loyalty_pct': 'mean',    # Average their loyalty
        'log_total_spend': 'max'      # Use highest intensity log
    }).reset_index()

    # --- STEP 5: GENERATE STRATEGIC LEAD SCORES ---
    print("Step 5: Generating Strategic Lead Scores...")
    # Refresh log_total_spend after sum to ensure accuracy
    df_consolidated['log_total_spend'] = np.log1p(
        df_consolidated['total_spend'])

    scaler = MinMaxScaler(feature_range=(0, 100))
    # Flatten to avoid a 300GB MemoryError
    scaled_spend = scaler.fit_transform(
        df_consolidated[['log_total_spend']]).flatten()

    # Calculate Lead Score: 70% Financial Scale + 30% Scientific Influence
    df_consolidated['lead_score'] = (
        scaled_spend * 0.7) + (df_consolidated['influence_ratio'] * 30)

    # --- STEP 6: SAVE TO GOLD DATABASE ---
    print("Step 6: Saving Consolidated Gold Table...")
    df_consolidated.to_sql('Physician_Nexus_Geographic',
                           conn_gold, if_exists='replace', index=False)

    conn_raw.close()
    conn_gold.close()

    print(
        f"SUCCESS: Strategic Gold Table created with {len(df_consolidated)} unique individuals.")
    print(
        f"Top National Lead Score: {df_consolidated['lead_score'].max():.2f}")


if __name__ == "__main__":
    build_geographic_table()
