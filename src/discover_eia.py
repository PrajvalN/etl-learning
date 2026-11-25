import os

import requests
from dotenv import load_dotenv

load_dotenv()
KEY = os.getenv("EIA_API_KEY")
BASE = "https://api.eia.gov/v2/electricity/rto/region-data"

# 1. Route metadata: what does this route support?
meta = requests.get(BASE, params={"api_key": KEY}, timeout=30).json()["response"]
print("Frequencies:", [f["id"] for f in meta["frequency"]])
print("Facets (filters):", [f["id"] for f in meta["facets"]])
print("Data columns:", list(meta["data"].keys()))

# 2. Allowed values for the 'type' filter (the measures)
types = requests.get(f"{BASE}/facet/type", params={"api_key": KEY}, timeout=30).json()[
    "response"
]
print("\nTypes:")
for t in types["facets"]:
    print(f"  {t['id']:4} {t['name']}")

# 3. Allowed values for the 'respondent' filter (the grid regions)
resp = requests.get(
    f"{BASE}/facet/respondent", params={"api_key": KEY}, timeout=30
).json()["response"]
print(f"\nRespondents ({resp.get('totalFacets')}):")
for r in sorted(resp["facets"], key=lambda x: x["id"]):
    print(f"  {r['id']:6} {r['name']}")
