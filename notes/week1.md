## Project change (Tue Nov 24)
- Switched from generated pole-inspection data to real public data:
  US grid demand (EIA) + weather (Open-Meteo)
- Business question: how does weather drive electricity demand across US grid
  regions, and how accurate are the grid operators' day-ahead forecasts?
- Skipped Postgres/Docker for now; loading straight into Snowflake in Week 2.
  Docker comes back in Week 6 for Airflow.

## Data source: EIA grid data
- Route: /v2/electricity/rto/region-data
- Frequencies: hourly (UTC), local-hourly
- Filters (facets): respondent (region), type (measure)
- Types: D = Demand, DF = Day-ahead demand forecast, NG = Net generation,
  TI = Total interchange
- 83 respondents in total

## Regions
Starting with the 7 major grid operators (ISOs/RTOs):

| Code | Operator | Weather city |
|---|---|---|
| ISNE | ISO New England | Boston |
| NYIS | New York ISO | New York City |
| PJM | PJM Interconnection | Philadelphia |
| MISO | Midcontinent ISO | Indianapolis |
| ERCO | ERCOT (Texas) | Dallas |
| CISO | California ISO | San Francisco |
| SWPP | Southwest Power Pool | Oklahoma City |

Why these:
- They cover most US electricity demand and very different climates.
- Excluded summary rows (US48, and regions like NE, NY, CAL, TEX, FLA) because
  they are totals of other respondents; including them would double count.

Known simplifications (v1):
- One weather city per region. Large regions like PJM and MISO span many
  climates. Future improvement: population-weighted average of several cities.
- City choice matters at borders: LA and Sacramento are separate operators
  (LDWP, BANC), not CISO, so San Francisco was picked for California.


  ## Data quality finding: ISNE Aug 1 – Nov 1, 2026
- Expected 8,836 rows (2,209 hours × 4 measures); got 8,833
- Total interchange (TI) missing for 3 hours (UTC):
  2026-09-11T18, 2026-10-14T20, 2026-10-14T21
- D, DF, NG complete
- Plan: in the transform step, derive missing TI as NG − D and flag it as derived
- Future automated check: every region-hour should have all 4 measures

