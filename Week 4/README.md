# Week 4 – EDA Deep Dive

This folder completes Week 4 of the 24ADI204 Data Science & Visualization plan.

## Files

- `EDA Deep Dive.ipynb` – complete executable notebook for univariate and bivariate EDA.
- `Week 4 Report.docx` – submission-ready report describing the methodology, analysis and observations to be finalized after execution.
- `README.md` – instructions and submission checklist.

## Dataset

The notebook first looks for the Week 3 cleaned dataset:

`../Week 3/AmesHousing_Uncleaned_Cleaned.csv`

If that file is not present, it can fall back to:

`../Week 3/AmesHousing_Uncleaned.csv`

and perform conservative median/mode imputation without modifying the original file.

## Run

From the repository root:

```bash
jupyter notebook
```

Then open:

`Week 4/EDA Deep Dive.ipynb`

Required Python packages are already listed in the repository-level `requirements.txt`.

## Week 4 coverage

- Dataset overview
- Numerical descriptive statistics
- Histograms and KDE distributions
- Boxplots
- Categorical frequency plots
- Scatter plots
- SalePrice comparisons
- Neighborhood analysis
- Correlation matrix
- Correlation heatmap
- Final EDA observations
