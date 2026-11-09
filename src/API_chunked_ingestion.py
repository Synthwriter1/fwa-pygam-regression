import os
import time
import requests
import pandas as pd

dataset_id = "335e5f35-eca6-482d-87b3-f99883e213e3"
base_url = f"https://data.cms.gov/data-api/v1/dataset/{dataset_id}/data"
output_file = "ca_medicare_claims.csv"

state_filter = "CA"
page_size = 5000
offset = 0  # Starting fresh from zero

params = {
    "filter[Rndrng_Prvdr_State_Abrvtn]": state_filter,
    "size": page_size,
    "offset": offset
}

print(f"Starting memory-safe download for {state_filter}...")

while True:
    response = requests.get(base_url, params=params)
    
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        time.sleep(5) # Wait and retry on server error
        continue
        
    batch = response.json()
    
    if not batch:
        print("Download complete! All rows safely on disk.")
        break
        
    df_batch = pd.DataFrame(batch)
    
    # Write to disk immediately. Only write headers on the very first batch.
    write_header = not os.path.exists(output_file)
    df_batch.to_csv(output_file, mode="a", index=False, header=write_header)
    
    offset += len(batch)
    params["offset"] = offset
    print(f"Saved {len(batch)} rows to disk. Total progress: {offset:,} rows")
    
    time.sleep(0.3) # Be polite to the API
