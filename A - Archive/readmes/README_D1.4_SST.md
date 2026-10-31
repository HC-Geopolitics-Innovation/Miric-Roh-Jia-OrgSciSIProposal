# SST Sample Construction

This folder contains script logic for selecting and constructing targeted demonstration and evaluation samples.

---

## Data Lifecycle & Notebook Pipeline

### Sample Selection (`05_build_sst_sample.ipynb`)
- **Logic**: Filters parsed congressional hearing corpora and corporate filings down to specific demonstration subsets (e.g. SST benchmark sample), balancing committee representation, digitised transcript presence, and text volume requirements.
