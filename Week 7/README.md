# Week 7 – Dimensionality Reduction: Feature Selection & PCA

This folder completes **Week 7** of the **24ADI204 – Data Science & Visualization** coursework, mapped to **Unit 4** of the syllabus.

## Milestone Objectives
- Implement **Feature Selection** techniques:
  - Variance Threshold filtering (removing sparse quasi-constant one-hot attributes)
  - Correlation analysis with target variable `SalePrice_Log` and multicollinearity pruning
  - Univariate ANOVA F-test (`f_regression` / `SelectKBest`)
  - Random Forest Regressor tree-based feature importance
- Implement **Principal Component Analysis (PCA)**:
  - Standardizing the 279-dimensional numeric predictor space
  - Computing eigenvalues, eigenvectors, and explained variance ratios
- **Visualize Variance**:
  - Scree plot of top individual components (Elbow method)
  - Cumulative explained variance curve with 80%, 90%, and 95% retention thresholds
- 2D PCA projection scatter plot colored by `SalePrice`
- Component loadings (eigenvector contributions) analysis for PC1 and PC2
- Export reduced datasets:
  - `Selected_Features_AmesHousing.csv` (40 curated features)
  - `PCA_Transformed_AmesHousing.csv` (175 orthogonal PCs retaining 95% variance)

---

## Folder Structure

```text
Week 7/
│
├── Figures/
│   ├── Variance_Explained_Scree.png
│   ├── PCA_2D_Projection.png
│   ├── Feature_Importance_Selection.png
│   ├── Correlation_Reduction_Heatmap.png
│   └── PCA_Loadings_Biplot.png
│
├── Week 7 Dimensionality Reduction.ipynb
├── Week 7 Report.docx
├── Selected_Features_AmesHousing.csv
├── PCA_Transformed_AmesHousing.csv
├── README.md
└── generate_week7_data.py
```

---

## Dataset Reference
The pipeline loads `Feature_Engineered_AmesHousing.csv` from `../Week 6/` (or local folder). Week 6 files are preserved untouched.

## How to Run

1. Open the notebook:
   ```bash
   jupyter notebook "Week 7/Week 7 Dimensionality Reduction.ipynb"
   ```
2. Or re-run the generation script:
   ```bash
   python "Week 7/generate_week7_data.py"
   ```

---

## Syllabus Mapping
- **Course:** 24ADI204 – Data Science & Visualization
- **Unit:** Unit 4 (Dimensionality Reduction, Feature Selection & PCA)
- **Team:** Team 8 (Tarun, Santhosh P, Siva Chandran, Santhosh M)
