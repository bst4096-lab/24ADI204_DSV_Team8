# 24ADI204 – Data Science & Visualization

**Team 8 | Ames Housing Analysis**

Repository for the 24ADI204 Data Science & Visualization course project. The project uses the Ames Housing dataset to explore data quality, clean and prepare data, engineer features, and communicate findings through statistical summaries and visualizations.

## Course and Team

| Item | Details |
|---|---|
| Course | 24ADI204 – Data Science & Visualization |
| Project | Ames Housing Analysis |
| Team | Team 8 |

### Team members

| Name | Register number | Main contribution |
|---|---|---|
| Tarun | 25BAD123 | Data analysis, visualization, and project work |
| Santhosh P | 25BAD101 | Data cleaning and preprocessing |
| Siva Chandran | 25BAD108 | Feature engineering and statistical analysis |
| Santhosh M | 25BAD100 | Documentation, reporting, and presentation |

## Project objectives

- Inspect the dataset's structure, data types, missing values, and duplicate records.
- Clean and prepare data while avoiding unnecessary loss of information.
- Explore relationships between housing attributes and sale prices.
- Create derived features when the required source columns are available.
- Produce reproducible summaries and visualizations.
- Document the workflow so another team member can rerun and review it.

## Project workflow

The weekly coursework develops the analysis continuously from initial inspection through later-stage analytical techniques. Each week's output directly serves as the input foundation for subsequent weeks.

### Weekly Data Pipeline & Continuity Matrix

| Week | Focus Area | Input File | Key Operations / Transforms | Output File | Dataset Shape | Pipeline Status |
|---|---|---|---|---|---|---|
| **Week 1** | Team Formation & Data Hunting | `AmesHousing_Uncleaned.xlsx` | Raw data ingestion, preliminary schema inspection, identifying target `SalePrice` | *(raw baseline)* | (3,130, 82) | Verified Raw Source |
| **Week 2** | "Know Your Data" & Preliminary EDA | `AmesHousing_Uncleaned.xlsx` | Data type mapping, initial missing value profiling, distribution overview | *(exploratory)* | (3,130, 82) | Continuous from W1 |
| **Week 3** | Data Cleaning & Outlier Profiling | `AmesHousing_Uncleaned.xlsx` / `.csv` | Deduplication (200 duplicate rows dropped), domain-informed imputation (None/0 for structural absences, median/mode for incidental nulls) | `AmesHousing_Uncleaned_Cleaned.csv` | (2,930, 82) | Continuous clean baseline |
| **Week 4** | Deep Dive EDA | `Week 3/AmesHousing_Uncleaned_Cleaned.csv` | Univariate distributions, neighborhood price dispersion, correlation analysis | *(visualizations)* | (2,930, 82) | Ingests W3 Cleaned |
| **Week 5** | Statistical Analysis & Data Audit | `Week 3/AmesHousing_Uncleaned_Cleaned.csv` | Formal data auditing (0 nulls verified), parametric normality tests, hypothesis testing | `Cleaned_AmesHousing_Week5.csv` | (2,930, 82) | Ingests W3, saves W5 baseline |
| **Week 6** | Feature Engineering | `Week 5/Cleaned_AmesHousing_Week5.csv` | Domain features (`HouseAge`, `TotalBathrooms`, etc.), `log1p(SalePrice)`, MinMax/Standard/Robust scaling, One-Hot & Ordinal encoding | `Feature_Engineered_AmesHousing.csv` | (2,930, 284) | Ingests W5 Cleaned |
| **Week 7** | Dimensionality Reduction & PCA | `Week 6/Feature_Engineered_AmesHousing.csv` | Variance Threshold filtering, Supervised selection (Random Forest & F-regression), PCA (95% variance) | `Selected_Features_AmesHousing.csv`<br>`PCA_Transformed_AmesHousing.csv` | (2,930, 44)<br>(2,930, 180) | Ingests W6 Engineered |


## Repository structure

The repository contains weekly coursework files and a separate `final_project/` workflow. The exact files in each weekly folder may evolve as coursework is updated.

```text
24ADI204_DSV_Team8/
├── Week 1/
├── Week 2/
├── Week 3/
├── Week 4/
├── Week 5/
├── Week 6/
├── Week 7/                 # If maintained as a separate folder
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
│   ├── outputs/
│   └── README.md
├── requirements.txt
├── .gitignore
├── CHANGELOG.md
└── README.md
```

Weekly folders may contain notebooks, reports, spreadsheets, or presentation files. Use the actual contents of each folder as the source of truth.

## Technology stack

- Python
- pandas and NumPy for data manipulation
- Matplotlib and Seaborn for visualization
- Jupyter Notebook for interactive coursework
- pytest for automated checks
- Git and GitHub for version control

## Setup

Python 3.10 or newer is recommended.

### 1. Clone the repository

```bash
git clone https://github.com/bst4096-lab/24ADI204_DSV_Team8.git
cd 24ADI204_DSV_Team8
```

### 2. Create and activate a virtual environment

On Linux, including Fedora:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Run checks

```bash
python -m pytest final_project/tests -q
git diff --check
```

Run Python commands while the virtual environment is active. Otherwise, your system Python may not have the project's dependencies installed.

## Final-project scripts

Run commands from the repository root.

### Audit a dataset

```bash
python final_project/scripts/audit_dataset.py --help
```

Use the help output to confirm supported arguments and provide the dataset path. The audit reports dimensions, duplicate rows, missing-value information, and whether expected target/schema elements are present.

### Run exploratory analysis

```bash
python final_project/scripts/run_eda.py --help
```

Use the displayed arguments to select the input dataset and output location. The EDA workflow produces summary tables and plots, including target-distribution and missingness views where supported by the input data.

### Run tests

```bash
python -m pytest final_project/tests -q
```

Tests check selected cleaning and feature-engineering behavior. Passing tests do not prove every notebook result or dataset is correct; they verify only the behaviors covered by the tests.

## Module overview

- **`data_cleaning.py`** — cleaning helpers for normalizing missing-value markers and optionally handling duplicate rows or entirely empty columns.
- **`feature_engineering.py`** — creates derived housing features when the necessary source columns are available.
- **`visualization.py`** — reusable plotting functions for exploratory analysis.
- **`audit_dataset.py`** — reports structural and data-quality information.
- **`run_eda.py`** — runs the supported exploratory-analysis workflow and writes outputs.
- **`test_pipeline.py`** — automated checks for selected pipeline behavior.

Generated tables and plots are stored under `final_project/outputs/`. Regenerate them when input data or analysis changes rather than assuming existing outputs are current.

## Data and interpretation notes

- Missing values should be examined in context. A blank value can mean “not applicable” rather than a value that should automatically be imputed.
- The project includes multiple versions of the Ames Housing data. Matching row and column counts or missing-value totals alone do **not** prove that two files contain identical records.
- Some coursework columns contain spaces, such as `Year Built` and `Gr Liv Area`, while reusable feature-engineering code expects unspaced names, such as `YearBuilt` and `GrLivArea`. Align column names before relying on those derived features; otherwise, some features may be skipped.
- Correlation does not prove causation.
- When building predictive models, fit preprocessing steps using training data only. Learning transformations from the full dataset can cause data leakage.
- Results depend on the exact input file and preprocessing steps. Record those choices when reporting results.

## Version control workflow

The active development branch for reproducibility and analysis improvements is:

```bash
git switch feature/reproducible-final-analysis
git pull
```

Changes have been pushed to GitHub on this branch. Review them against `main` through a pull request before merging.

For future changes:

```bash
git status
git diff --check
python -m pytest final_project/tests -q
git add <files-to-include>
git commit -m "Describe the change"
git push
```

Avoid committing virtual environments, Python cache files, temporary notebook checkpoints, or generated files that are not intended to be version-controlled.

## Future improvements

- Make feature engineering handle spaced and unspaced column names consistently.
- Add tests for missing columns, unexpected data types, and edge cases.
- Record dataset provenance and preprocessing decisions more explicitly.
- Add automated checks through GitHub Actions.
- Keep notebook outputs, reports, and generated artifacts synchronized with the scripts and documented workflow.

## Repository

GitHub: https://github.com/bst4096-lab/24ADI204_DSV_Team8
