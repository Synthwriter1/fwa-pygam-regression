import pandas as pd
import numpy as np

def run_penalty_box_audit(claims_path, leie_path, output_path):
    print("Initializing Phase 4: LEIE Deterministic Penalty Box Audit...")

    # 1. Load the LEIE Exclusion Database
    print("Loading September 2026 LEIE dataset...")
    leie_df = pd.read_csv(leie_path, dtype={'NPI': str}, low_memory=False)
    leie_df['NPI'] = leie_df['NPI'].fillna('0').str.strip()
    leie_npi_list = leie_df[leie_df['NPI'] != '0'].copy()
    
    leie_npi_list = leie_npi_list[['NPI', 'LASTNAME', 'FIRSTNAME', 'EXCLTYPE', 'EXCLDATE']]
    leie_npi_list['EXCLDATE'] = pd.to_datetime(leie_npi_list['EXCLDATE'], format='%Y%m%d', errors='coerce')
    leie_npi_list.rename(columns={'EXCLTYPE': 'LEIE_EXCLUSION_TYPE', 'EXCLDATE': 'LEIE_EXCLUSION_DATE'}, inplace=True)
    
    # 2. Load the CMS Medicare Claims
    print("Loading 2024 CMS Medicare Claims (802,000 records)...")
    claims_df = pd.read_csv(claims_path, dtype=str, low_memory=False) 
    
    # --- THE FIX ---
    # Rename the specific CMS column to standard 'NPI' for the merge
    claims_df.rename(columns={'Rndrng_NPI': 'NPI'}, inplace=True)
    
    claims_df['NPI'] = claims_df['NPI'].astype(str).str.strip()

    # 3. The Deterministic Match
    print("Executing NPI inner merge...")
    fraud_hits = pd.merge(claims_df, leie_npi_list, on='NPI', how='inner')

    if not fraud_hits.empty:
        # Bounding to the end of the year to account for CMS Temporal Fog
        fraud_hits['ILLEGAL_BILLING_FLAG'] = fraud_hits['LEIE_EXCLUSION_DATE'] <= pd.to_datetime('2024-12-31')
        confirmed_violations = fraud_hits[fraud_hits['ILLEGAL_BILLING_FLAG'] == True]
        
        hit_count = len(confirmed_violations)
        unique_providers = confirmed_violations['NPI'].nunique()
        
        if hit_count > 0:
            print(f"\nCRITICAL: Found {hit_count} anomalous claims tied to {unique_providers} actively excluded providers.")
            confirmed_violations.to_csv(output_path, index=False)
            print(f"Audit log saved to {output_path}")
        else:
            print("\nMatches found, but no temporal overlaps (all exclusions occurred after 2024).")
    else:
        print("\nAudit Complete: No NPIs in the claims dataset matched the LEIE database.")

if __name__ == "__main__":
    # Updated paths to match the modular repository architecture
    CMS_CLAIMS_FILE = '../data/ca_medicare_claims.csv' 
    LEIE_DB_FILE = '../data/data09-2026-Updated-LEIE-Database.csv'
    AUDIT_OUTPUT = 'results/phase_4_leie_hits_anonymized.csv'
    
    run_penalty_box_audit(CMS_CLAIMS_FILE, LEIE_DB_FILE, AUDIT_OUTPUT)
