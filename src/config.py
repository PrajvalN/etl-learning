"""Project settings: which regions to extract, their weather locations, and the date range.

Edit this file to change what the pipeline extracts. The scripts read from here.
"""

# Date range for extraction (EIA hourly periods are in UTC, format YYYY-MM-DDTHH)
START = "2026-08-01T00"
END = "2026-11-01T00"

# The 7 major US grid operators and the city used for each one's weather.
# One city per region is a v1 simplification (see notes/week1.md).
REGIONS = {
    "ISNE": {
        "name": "ISO New England",
        "city": "Boston",
        "lat": 42.3601,
        "lon": -71.0589,
        "tz": "America/New_York",
    },
    "NYIS": {
        "name": "New York ISO",
        "city": "New York City",
        "lat": 40.7128,
        "lon": -74.0060,
        "tz": "America/New_York",
    },
    "PJM": {
        "name": "PJM Interconnection",
        "city": "Philadelphia",
        "lat": 39.9526,
        "lon": -75.1652,
        "tz": "America/New_York",
    },
    "MISO": {
        "name": "Midcontinent ISO",
        "city": "Indianapolis",
        "lat": 39.7684,
        "lon": -86.1581,
        "tz": "America/Indiana/Indianapolis",
    },
    "ERCO": {
        "name": "ERCOT (Texas)",
        "city": "Dallas",
        "lat": 32.7767,
        "lon": -96.7970,
        "tz": "America/Chicago",
    },
    "CISO": {
        "name": "California ISO",
        "city": "San Francisco",
        "lat": 37.7749,
        "lon": -122.4194,
        "tz": "America/Los_Angeles",
    },
    "SWPP": {
        "name": "Southwest Power Pool",
        "city": "Oklahoma City",
        "lat": 35.4676,
        "lon": -97.5164,
        "tz": "America/Chicago",
    },
}
