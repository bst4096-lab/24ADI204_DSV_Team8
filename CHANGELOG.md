# Changelog

This file records changes to the project structure and analysis workflow.

## Unreleased

### Added
- `final_project/` layer for reusable analysis code, scripts, tests, and generated outputs.
- Dataset audit script to compare weekly datasets without silently changing them.
- Reusable cleaning helpers for duplicate rows, empty columns, whitespace, and common missing-value markers.
- Reusable, schema-aware housing feature engineering.
- EDA runner that exports missingness and numeric summaries, correlations, and basic figures.
- Unit tests for cleaning and feature-engineering behavior.

### Changed
- Updated the root README to document the actual Week 1–Week 6 layout and the reproducible workflow.
- Added `scikit-learn`, Jupyter, and `pytest` to the dependency list because the existing Week 6 work uses scikit-learn and the new workflow uses notebooks and tests.

### Notes
- Existing weekly coursework is intentionally preserved.
- The row-count discrepancy between saved notebook outputs is not declared resolved by this release. Run the audit on the actual files and inspect the cleaning steps before deciding which dataset is authoritative.
