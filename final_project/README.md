# Final analysis layer

This folder supplements, rather than replaces, the weekly coursework.

## Contents

- `src/data_cleaning.py`: conservative cleaning helpers and a cleaning report.
- `src/feature_engineering.py`: schema-aware Ames-style housing features.
- `src/visualization.py`: reusable plotting helpers.
- `scripts/audit_dataset.py`: compare one or more CSV datasets.
- `scripts/run_eda.py`: generate summaries and figures from a CSV.
- `tests/`: small automated tests for the reusable functions.
- `outputs/`: generated locally by the EDA runner; review before committing.

## Example

```bash
python final_project/scripts/audit_dataset.py "Week 3/AmesHousing_Uncleaned.csv" "Week 5/Cleaned_AmesHousing_Week5.csv"
python final_project/scripts/run_eda.py "Week 3/AmesHousing_Uncleaned.csv" --output-dir final_project/outputs
python -m pytest final_project/tests -q
```

The code does not guess which dataset is correct and does not automatically impute missing values. Make those decisions based on documented analysis.
