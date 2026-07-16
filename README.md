# COVID-19 Data Pipeline

## Project Structure
- `exploration.ipynb` — data investigation and quality checks (see Data Quality Notes above)
- `pipeline.py` — the finalized, callable data pipeline

**Technology Used:** 
- **Python 3**
- **Pandas**
- **Requests library**
- **CDC Socrata Open Data API**

**Implementation:** Built a program that pulls live COVID-19 surveillance data directly from CDC's public API, cleans it, and calculates cumulative incidence rates by state.

## Data Source

[Weekly United States COVID-19 Cases and Deaths by State](https://data.cdc.gov/Case-Surveillance/Weekly-United-States-COVID-19-Cases-and-Deaths-by-/pwn4-m3yp) — pulled directly via CDC's Socrata API (`data.cdc.gov/resource/pwn4-m3yp.json`). Narrowed scope to 2021 and four states (AZ, CA, NY, FL) after data quality checks — see below.

## Key Implementations

- **Live API Pull:** Queried CDC's SODA API with `requests`, converting the JSON response directly into a pandas DataFrame and confirmed dataset size with a `count(*)` query before pulling to avoid coming up with an incomplete sample.
- **Type Conversion:** Cast API response strings to proper `datetime` and numeric types (`pd.to_datetime()`, `pd.to_numeric()`). API responses return everything as text by default, so this step has to be done before any calculation.
- **Column Selection After Investigation:** Rejected the dataset's `new_historic_cases`/`new_historic_deaths` columns after confirming they're a backfill field, not the actual weekly counts. Also identified that a single end-of-dataset reconciliation week distorts the `new_cases`/`new_deaths` weekly columns, and switched to the `tot_cases`/`tot_deaths` cumulative columns instead.
- **Cumulative Incidence Calculation:** Computed cases as a proportion of state population (cases ÷ population, scaled to cases per 1,000) which is the standard epidemiological measure for disease burden over a defined period.
- **State Comparison:** Used `.groupby("state").last()` and `.index.map()` to calculate incidence rates for all four states in a single pass, instead of repeating the same calculation per state.

## Data Quality Notes

Real government data often has reporting gaps and this dataset was no exception:
- **Death counts were too sparsely and inconsistently reported** across most states in the weekly field to support a reliable rate calculation; several states reported 0 for most of the dataset's duration because of documented reporting issues on CDC's end.
- **A large single-week spike in several states' data** (e.g., Florida) lines up with CDC's documented final reconciliation update before this dataset was discontinued in 2023. This is why the analysis is scoped to 2021 rather than the dataset's full, messier multi-year range.
- These findings shaped the final column and time-window choices above.

## Key Findings
- Out of the four states surveyed (AZ, CA, FL, and NY) California had the highest total number of COVID-19 cases in 2021 for the population under 18 years old (with 5,412,140 cases), but Arizona had the highest cumulative incidence rate per population, with about 185 cases per 1000 people.
- New York had the lowest cumulative incidence rate of the four, with only 95 cases per 1000 people. 

## Requirements

```
pandas
requests
```

## Limitations

- Death rate analysis excluded due to unreliable underlying data (see Data Quality Notes).
- Population figures are approximate 2021 estimates, hardcoded for four states — not pulled from a live Census source.
- Scoped to 2021 only; does not reflect the dataset's full multi-year range.
