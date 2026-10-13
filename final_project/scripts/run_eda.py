#!/usr/bin/env python3
"""Generate reproducible summary tables and plots from a CSV dataset."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from final_project.src.data_cleaning import clean_tabular_data, data_quality_report
from final_project.src.feature_engineering import add_housing_features
from final_project.src.visualization import plot_missingness, plot_target_distribution


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_file", type=Path, help="Input CSV file")
    parser.add_argument("--output-dir", type=Path, default=Path("final_project/outputs"))
    parser.add_argument("--target", default="SalePrice", help="Numeric target column for distribution/correlation")
    args = parser.parse_args()

    raw = pd.read_csv(args.csv_file, low_memory=False)
    cleaned = clean_tabular_data(raw)
    engineered = add_housing_features(cleaned)
    out = args.output_dir
    out.mkdir(parents=True, exist_ok=True)

    data_quality_report(cleaned).to_csv(out / "data_quality_report.csv", index=False)
    numeric = engineered.select_dtypes(include="number")
    numeric.describe().T.to_csv(out / "numeric_summary.csv")
    if args.target in numeric.columns:
        numeric.corr(numeric_only=True)[[args.target]].sort_values(
            args.target, ascending=False
        ).to_csv(out / "target_correlations.csv")
        plot_target_distribution(engineered, out / f"{args.target.lower()}_distribution.png", args.target)
    plot_missingness(cleaned, out / "missingness.png")

    print(f"Input: {args.csv_file}")
    print(f"Raw shape: {raw.shape}")
    print(f"After conservative cleaning: {cleaned.shape}")
    print(f"Feature-engineered shape: {engineered.shape}")
    print(f"Outputs: {out.resolve()}")
    print("Note: correlations are descriptive associations, not causal effects.")


if __name__ == "__main__":
    main()
