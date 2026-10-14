#!/usr/bin/env python3
"""Compare basic data-quality indicators across CSV files without modifying them."""

from __future__ import annotations

import argparse
from pathlib import Path
import pandas as pd


def audit(path: Path) -> dict:
    df = pd.read_csv(path, low_memory=False)
    return {
        "file": str(path),
        "rows": len(df),
        "columns": len(df.columns),
        "duplicate_rows": int(df.duplicated().sum()),
        "cells_missing": int(df.isna().sum().sum()),
        "columns_with_missing": int(df.isna().any().sum()),
        "has_SalePrice": "SalePrice" in df.columns,
        "SalePrice_missing": int(df["SalePrice"].isna().sum()) if "SalePrice" in df else None,
        "column_names_match_first_file": None,
        "readable": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_files", nargs="+", type=Path, help="One or more CSV files to compare")
    args = parser.parse_args()

    reports = []
    reference_columns = None
    for path in args.csv_files:
        try:
            df = pd.read_csv(path, low_memory=False)
            report = audit(path)
            columns = list(df.columns)
            report["column_names_match_first_file"] = (
                columns == reference_columns if reference_columns is not None else True
            )
            if reference_columns is None:
                reference_columns = columns
            reports.append(report)
        except Exception as exc:
            reports.append({"file": str(path), "readable": False, "error": str(exc)})

    output = pd.DataFrame(reports)
    with pd.option_context("display.max_columns", None, "display.width", 180):
        print(output.to_string(index=False))
    if not output["readable"].all():
        raise SystemExit(1)


if __name__ == "__main__":
    main()
