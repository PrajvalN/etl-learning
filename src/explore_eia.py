import os

import pandas as pd
import requests
from dotenv import load_dotenv

# 1. Load the API key from .env (never hard-code it)
load_dotenv()
API_KEY = os.getenv("EIA_API_KEY")

# 2. The EIA endpoint for hourly grid data by region
URL = "https://api.eia.gov/v2/electricity/rto/region-data/data/"

# 3. What we're asking for
params = {
    "api_key": API_KEY,
    "frequency": "hourly",
    "data[0]": "value",
    "facets[respondent][]": "ISNE",  # ISO New England (your grid)
    "start": "2026-11-20T00",  # from this hour (UTC)
    "end": "2026-11-21T00",  # to this hour
    "sort[0][column]": "period",
    "sort[0][direction]": "asc",
    "length": 200,  # max rows to return
}

# 4. Call the API
response = requests.get(URL, params=params, timeout=30)
print("HTTP status:", response.status_code)
response.raise_for_status()  # stop with an error if the call failed

# 5. Look at what came back
payload = response.json()["response"]
print("Rows matching the query:", payload.get("total"))

df = pd.DataFrame(payload["data"])
print("\nColumns:", list(df.columns))
print("\nFirst 8 rows:")
print(df.head(8).to_string())
print("\nRows per data type:")
print(df["type-name"].value_counts())
