# 24ADI204 - Data Science & Visualization

## Team 8 | House Price Analysis

This repository contains the team's weekly coursework and a reproducible final-analysis layer for the Ames Housing dataset. The existing `Week 1` through `Week 6` folders are retained as coursework history; reusable code and final outputs live in `final_project/`.

## Course information

| Item | Details |
|---|---|
| Course code | 24ADI204 |
| Course | Data Science & Visualization |
| Team | Team 8 |
| Academic year | 2026 |

## Team

| Name | Register number | Primary contribution |
|---|---|---|
| Tarun | 25BAD123 | Data analysis, visualization and project work |
| Santhosh P | 25BAD101 | Data cleaning and preprocessing |
| Siva Chandran | 25BAD108 | Feature engineering and statistical modeling |
| Santhosh M | 25BAD100 | Documentation, reporting and presentation |

## Project workflow

1. Keep the original weekly submissions in `Week 1/` through `Week 6/`.
2. Use `final_project/src/` for reusable data-cleaning, feature-engineering and visualization code.
3. Run the data audit before interpreting differences between weekly datasets.
4. Generate reproducible summaries and figures from a selected CSV.
5. Record assumptions and interpret results as associations, not proof of causation.

## Repository structure

```text
24ADI204_DSV_Team8/
├── Week 1/ ... Week 6/       # Original weekly coursework and reports
├── final_project/
│   ├── src/
│   │   ├── data_cleaning.py
│   │   ├── feature_engineering.py
│   │   └── visualization.py
│   ├── scripts/
│   │   ├── audit_dataset.py
│   │   └── run_eda.py
│   ├── tests/
│   │   └── test_pipeline.py
│   └── README.md
├── requirements.txt
├── .gitignore
├── CHANGELOG.md
└── README.md
```

## Fedora setup

Run these commands from the repository root:

```bash
sudo dnf install -y git python3 python3-pip
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Audit the weekly data

The project previously showed different row counts in saved notebook outputs. Do not silently pick a count and call the mystery solved; inspect the actual files first.

```bash
python final_project/scripts/audit_dataset.py "Week 3/AmesHousing_Uncleaned.csv" "Week 5/Cleaned_AmesHousing_Week5.csv"
```

Add more paths as needed. The audit reports shape, duplicate rows, missing values, and whether `SalePrice` is present.

## Run the final EDA

```bash
python final_project/scripts/run_eda.py "Week 3/AmesHousing_Uncleaned.csv" --output-dir final_project/outputs
```

The script writes CSV summaries and PNG figures under `final_project/outputs/`. Outputs are generated locally and should be reviewed before committing.

## Run tests

```bash
python -m pytest final_project/tests -q
```

## Important analysis rules

- The audit does not automatically delete rows or fill missing values.
- Cleaning and feature engineering are explicit functions, so notebook work can reuse them instead of copying slightly different versions.
- `HouseAge` and `RemodAge` require a sale-year column. Negative ages are treated as invalid and changed to missing values.
- `TotalHouseArea` is a derived proxy, not an official property measurement. Avoid using it together with all of its component columns without checking for redundancy.
- If predictive modeling is added later, split into train/test sets before fitting imputers, scalers, encoders, or feature selection. Fit preprocessing on training data only.
- Correlation is not causation. Housing prices have confounders; a heatmap is not a tiny oracle.

## Dependencies

See `requirements.txt`. Use a virtual environment so the system Python installation remains untouched.
