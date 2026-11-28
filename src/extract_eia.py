import json
import os
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

from config import END, REGIONS, START   # NEW: settings come from config.py

load_dotenv()
API_KEY = os.getenv("EIA_API_KEY")

URL = "https://api.eia.gov/v2/electricity/rto/region-data/data/"
PAGE_SIZE = 5000                 # EIA's maximum rows per call
RAW_DIR = Path("data/raw/eia")   # raw layer: data exactly as the API returned it


def fetch_region(region: str, start: str, end: str) -> list[dict]:
    """Get all hourly rows for one region and date range, page by page."""
    rows = []
    offset = 0
    while True:
        params = {
            "api_key": API_KEY,
            "frequency": "hourly",
            "data[0]": "value",
            "facets[respondent][]": region,
            "start": start,
            "end": end,
            "sort[0][column]": "period",
            "sort[0][direction]": "asc",
            "offset": offset,
            "length": PAGE_SIZE,
        }
        response = requests.get(URL, params=params, timeout=60)
        response.raise_for_status()
        payload = response.json()["response"]

        page = payload["data"]
        rows.extend(page)
        total = int(payload["total"])
        print(f"  {region}: fetched {len(rows):,} of {total:,} rows")

        if len(rows) >= total or not page:
            break
        offset += PAGE_SIZE
        time.sleep(0.5)

    return rows


def raw_path(region: str, start: str, end: str) -> Path:   # NEW
    """The file path for one region's raw data. One place decides the naming."""
    return RAW_DIR / f"{region}_{start[:10]}_{end[:10]}.json"


def save_raw(rows: list[dict], path: Path) -> None:        # CHANGED: takes the path
    """Save rows as a JSON file, unchanged."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(rows))


if __name__ == "__main__":                                  # CHANGED: loop over regions
    print(f"Extracting {len(REGIONS)} regions from {START} to {END}\n")
    for region in REGIONS:
        path = raw_path(region, START, END)
        if path.exists():
            print(f"{region}: already extracted, skipping ({path})")
            continue
        rows = fetch_region(region, START, END)
        save_raw(rows, path)
        print(f"{region}: saved {len(rows):,} rows to {path}\n")
    print("Done.")