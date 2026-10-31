# Compustat controls for the T4 regressions

`compustat_controls.csv` is the Compustat Fundamentals Annual extract that `T4.1.5 - Panel - Build the Firm-Year Panel for the Privacy Patent Regression.ipynb` reads to build the lagged controls (log total assets and log of one plus R&D expense at t − 1). It is kept here so that the section folder holds the regression inputs; the same file sits in the section's `Raw` folder on scratch.

One row per Compustat firm (`gvkey`) and fiscal year (`fyear`), fiscal 1997 to 2026, 360,986 rows, all Compustat firms (not only the sample). Columns:

| Column | Meaning |
|---|---|
| `costat` | Company status (A active, I inactive) |
| `curcd` | Currency (USD or CAD); T4.1.5 keeps USD |
| `datafmt` | Data format (STD) |
| `indfmt` | Industry format (INDL industrial or FS financial services); T4.1.5 keeps INDL |
| `consol` | Consolidation level (C) |
| `gvkey` | Compustat firm identifier; T4.1.5 reads it as a six-character string |
| `datadate` | Fiscal year-end date |
| `conm` | Company name |
| `ipodate` | IPO date where Compustat has one (about 40 percent of rows) |
| `naics` | NAICS code |
| `fyear` | Fiscal year |
| `at` | Total assets, millions of US dollars |
| `xrd` | Research and development expense, millions of US dollars; missing for about two thirds of rows |

Firm age in T4.1.5 does not come from this file; it uses the first CRSP link date in `crsp_compustat_link.dta` (section `Raw` folder on scratch, also in `/project2/mmiric_1435/acroh/llm_method/data/interim/repo_data/raw/01_firm_id/`).
