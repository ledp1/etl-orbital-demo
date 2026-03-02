"""Data quality and validation layer."""
import pandas as pd
from typing import Optional


class ValidationError(Exception):
    """Raised when data quality checks fail."""

    def __init__(self, message: str, failures: Optional[list[str]] = None):
        super().__init__(message)
        self.failures = failures or []


def validate_schema(df: pd.DataFrame, required_cols: list[str]) -> None:
    """Ensure required columns exist."""
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValidationError(f"Missing required columns: {missing}", failures=missing)


def validate_not_null(df: pd.DataFrame, cols: list[str]) -> None:
    """Ensure critical columns have no nulls."""
    failures = []
    for col in cols:
        if col in df.columns and df[col].isna().any():
            failures.append(f"{col} has null values")
    if failures:
        raise ValidationError("Null values in required columns", failures=failures)


def validate_ranges(df: pd.DataFrame) -> None:
    """Validate physical constraints on orbital parameters."""
    failures = []

    if "semi_major_axis_km" in df.columns:
        invalid = (df["semi_major_axis_km"] <= 0).sum()
        if invalid > 0:
            failures.append(f"semi_major_axis_km: {invalid} rows with non-positive values")

    if "eccentricity" in df.columns:
        invalid = ((df["eccentricity"] < 0) | (df["eccentricity"] > 1)).sum()
        if invalid > 0:
            failures.append(f"eccentricity: {invalid} rows outside [0, 1]")

    if failures:
        raise ValidationError("Range validation failed", failures=failures)


def run_validation(df: pd.DataFrame) -> None:
    """Run full validation suite. Raises ValidationError on failure."""
    required = ["object_id", "semi_major_axis_km", "eccentricity", "inclination_deg"]
    validate_schema(df, required)
    validate_not_null(df, ["object_id", "semi_major_axis_km"])
    validate_ranges(df)
