import pandas as pd

from final_project.src.data_cleaning import clean_tabular_data, data_quality_report
from final_project.src.feature_engineering import add_housing_features


def test_cleaning_normalizes_whitespace_missing_markers_and_duplicates():
    df = pd.DataFrame({"Neighborhood": ["  NA ", "CollgCr", "CollgCr"], "SalePrice": [100, 200, 200]})
    result = clean_tabular_data(df)
    assert len(result) == 2
    assert pd.isna(result.loc[0, "Neighborhood"])
    assert result.loc[1, "Neighborhood"] == "CollgCr"


def test_cleaning_does_not_drop_rows_with_missing_values():
    df = pd.DataFrame({"SalePrice": [100, None], "LotArea": [5000, 6000]})
    result = clean_tabular_data(df)
    assert len(result) == 2


def test_drops_fully_empty_columns():
    result = clean_tabular_data(pd.DataFrame({"empty": [None, None], "x": [1, 2]}))
    assert list(result.columns) == ["x"]


def test_feature_engineering_uses_sale_year_and_handles_invalid_negative_age():
    df = pd.DataFrame({
        "YrSold": [2010, 2010],
        "YearBuilt": [2000, 2020],
        "YearRemodAdd": [2005, 2021],
        "FullBath": [2, 1],
        "HalfBath": [1, 0],
        "BsmtFullBath": [1, 0],
        "BsmtHalfBath": [0, 1],
        "OpenPorchSF": [10, 20],
        "WoodDeckSF": [30, 40],
        "GrLivArea": [1500, 1000],
        "TotalBsmtSF": [500, 400],
        "SalePrice": [200000, 150000],
    })
    result = add_housing_features(df)
    assert result.loc[0, "HouseAge"] == 10
    assert pd.isna(result.loc[1, "HouseAge"])
    assert result.loc[0, "TotalBathrooms"] == 3.5
    assert result.loc[0, "TotalPorchArea"] == 40
    assert result.loc[0, "TotalHouseArea"] == 2000
    assert result.loc[0, "LogSalePrice"] > 0


def test_quality_report_has_missingness_columns():
    report = data_quality_report(pd.DataFrame({"a": [1, None], "b": ["x", "y"]}))
    assert {"column", "missing_count", "missing_percent", "distinct_non_null"}.issubset(report.columns)
    assert report.loc[report["column"] == "a", "missing_count"].iloc[0] == 1
