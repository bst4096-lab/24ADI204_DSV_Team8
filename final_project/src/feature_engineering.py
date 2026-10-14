"""Schema-aware derived features for Ames-style housing data."""

from __future__ import annotations

import pandas as pd


def add_housing_features(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy with derived features when their source columns exist.

    Invalid negative age values become missing. No source columns are removed.
    """
    result = df.copy()

    if {"YrSold", "YearBuilt"}.issubset(result.columns):
        result["HouseAge"] = pd.to_numeric(result["YrSold"], errors="coerce") - pd.to_numeric(
            result["YearBuilt"], errors="coerce"
        )
        result.loc[result["HouseAge"] < 0, "HouseAge"] = pd.NA

    if {"YrSold", "YearRemodAdd"}.issubset(result.columns):
        result["RemodAge"] = pd.to_numeric(result["YrSold"], errors="coerce") - pd.to_numeric(
            result["YearRemodAdd"], errors="coerce"
        )
        result.loc[result["RemodAge"] < 0, "RemodAge"] = pd.NA

    bathroom_columns = [
        column
        for column in ("FullBath", "HalfBath", "BsmtFullBath", "BsmtHalfBath")
        if column in result.columns
    ]
    if bathroom_columns:
        weights = {
            "FullBath": 1.0,
            "HalfBath": 0.5,
            "BsmtFullBath": 1.0,
            "BsmtHalfBath": 0.5,
        }
        result["TotalBathrooms"] = sum(
            pd.to_numeric(result[column], errors="coerce").fillna(0) * weights[column]
            for column in bathroom_columns
        )

    porch_columns = [
        column
        for column in ("OpenPorchSF", "EnclosedPorch", "3SsnPorch", "ScreenPorch", "WoodDeckSF")
        if column in result.columns
    ]
    if porch_columns:
        result["TotalPorchArea"] = sum(
            pd.to_numeric(result[column], errors="coerce").fillna(0) for column in porch_columns
        )

    area_columns = [column for column in ("GrLivArea", "TotalBsmtSF") if column in result.columns]
    if len(area_columns) == 2:
        result["TotalHouseArea"] = sum(
            pd.to_numeric(result[column], errors="coerce").fillna(0) for column in area_columns
        )

    if "SalePrice" in result.columns:
        price = pd.to_numeric(result["SalePrice"], errors="coerce")
        result["LogSalePrice"] = price.where(price > 0).map(
            lambda value: __import__("math").log1p(value) if pd.notna(value) else pd.NA
        )

    return result
