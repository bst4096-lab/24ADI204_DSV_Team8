"""Conservative, reusable cleaning helpers for tabular datasets."""

from __future__ import annotations

import pandas as pd

DEFAULT_MISSING_MARKERS = {"", "NA", "N/A", "na", "n/a", "NULL", "null", "None", "?"}


def normalize_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy with surrounding whitespace removed and common markers set to NA."""
    result = df.copy()
    for column in result.select_dtypes(include=["object", "string"]).columns:
        series = result[column].astype("string").str.strip()
        result[column] = series.replace(list(DEFAULT_MISSING_MARKERS), pd.NA)
    return result


def clean_tabular_data(
    df: pd.DataFrame,
    *,
    drop_duplicates: bool = True,
    drop_all_empty_columns: bool = True,
) -> pd.DataFrame:
    """Apply only low-risk cleaning; do not impute values or drop incomplete rows."""
    result = normalize_missing_values(df)
    if drop_duplicates:
        result = result.drop_duplicates().copy()
    if drop_all_empty_columns:
        result = result.dropna(axis=1, how="all").copy()
    return result.reset_index(drop=True)


def data_quality_report(df: pd.DataFrame) -> pd.DataFrame:
    """Return one row per column with dtype, missing count/rate, and distinct count."""
    total = len(df)
    return pd.DataFrame(
        {
            "column": df.columns,
            "dtype": [str(df[col].dtype) for col in df.columns],
            "missing_count": [int(df[col].isna().sum()) for col in df.columns],
            "missing_percent": [
                round(float(df[col].isna().mean() * 100), 2) if total else 0.0
                for col in df.columns
            ],
            "distinct_non_null": [int(df[col].nunique(dropna=True)) for col in df.columns],
        }
    ).sort_values(["missing_percent", "column"], ascending=[False, True], ignore_index=True)
