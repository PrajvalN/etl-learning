import json
import os
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("EIA_API_KEY")

URL = "https://api.eia.gov/v2/electricity/rto/region-data/data/"
PAGE_SIZE = 5000  # EIA's maximum rows per call
RAW_DIR = Path("data/raw/eia")  # raw layer: data exactly as the API returned it


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
            "offset": offset,  # where this page starts
            "length": PAGE_SIZE,  # how many rows per page
        }
        response = requests.get(URL, params=params, timeout=60)
        response.raise_for_status()
        payload = response.json()["response"]

        page = payload["data"]
        rows.extend(page)
        total = int(payload["total"])
        print(f"  {region}: fetched {len(rows):,} of {total:,} rows")

        if len(rows) >= total or not page:  # got everything (or an empty page): stop
            break
        offset += PAGE_SIZE  # move to the next page
        time.sleep(0.5)  # be polite to the API between calls

    return rows


def save_raw(rows: list[dict], region: str, start: str, end: str) -> Path:
    """Save rows as a JSON file in the raw folder, unchanged."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    path = RAW_DIR / f"{region}_{start[:10]}_{end[:10]}.json"
    path.write_text(json.dumps(rows))
    return path


if __name__ == "__main__":
    region, start, end = "ISNE", "2026-08-01T00", "2026-11-01T00"
    print(f"Extracting {region} from {start} to {end}")
    rows = fetch_region(region, start, end)
    path = save_raw(rows, region, start, end)
    print(f"Saved {len(rows):,} rows to {path}")
