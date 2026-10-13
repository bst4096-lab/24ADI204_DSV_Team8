"""Small reusable plots for exploratory housing-data analysis."""

from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def plot_missingness(df: pd.DataFrame, output_path: str | Path, top_n: int = 25) -> None:
    """Save a bar chart of columns with the highest percentage of missing values."""
    rates = (df.isna().mean() * 100).sort_values(ascending=False)
    rates = rates[rates > 0].head(top_n)
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(10, max(4, 0.32 * len(rates))))
    if rates.empty:
        ax.text(0.5, 0.5, "No missing values detected", ha="center", va="center")
        ax.set_axis_off()
    else:
        sns.barplot(x=rates.values, y=rates.index, ax=ax)
        ax.set_xlabel("Missing values (%)")
        ax.set_ylabel("Column")
        ax.set_title(f"Columns with most missing values (top {len(rates)})")
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def plot_target_distribution(df: pd.DataFrame, output_path: str | Path, target: str = "SalePrice") -> bool:
    """Save the target distribution if the requested numeric target exists."""
    if target not in df.columns:
        return False
    values = pd.to_numeric(df[target], errors="coerce").dropna()
    if values.empty:
        return False

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(values, kde=True, ax=ax)
    ax.set_title(f"Distribution of {target}")
    ax.set_xlabel(target)
    ax.set_ylabel("Number of properties")
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return True
