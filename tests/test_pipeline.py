"""Tests for ETL pipeline and data quality."""
import pandas as pd
import pytest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.transform import transform_orbital_data
from src.validate import run_validation, validate_schema, validate_ranges, ValidationError


def test_transform_produces_expected_columns():
    """Transform adds derived fields and normalizes schema."""
    df = pd.DataFrame({
        "object_id": ["ISS"],
        "semi_major_axis_km": [6771],
        "eccentricity": [0.0001],
        "inclination_deg": [51.6],
        "orbital_period_min": [93],
    })
    result = transform_orbital_data(df)
    assert "orbital_velocity_km_s" in result.columns
    assert "orbit_type" in result.columns
    assert result["orbit_type"].iloc[0] == "LEO"


def test_validate_schema_rejects_missing_columns():
    """Schema validation catches missing required columns."""
    df = pd.DataFrame({"object_id": [1], "semi_major_axis_km": [6771]})
    with pytest.raises(ValidationError) as exc:
        validate_schema(df, ["object_id", "semi_major_axis_km", "eccentricity"])
    assert "eccentricity" in str(exc.value)


def test_validate_ranges_rejects_invalid_eccentricity():
    """Range validation catches invalid eccentricity."""
    df = pd.DataFrame({
        "object_id": ["X"],
        "semi_major_axis_km": [6771],
        "eccentricity": [1.5],
        "inclination_deg": [51.6],
    })
    with pytest.raises(ValidationError):
        validate_ranges(df)


def test_full_pipeline_runs():
    """End-to-end pipeline produces Parquet output."""
    from src.pipeline import run
    out = run(output_dir="data/output")
    assert out.exists()
    df = pd.read_parquet(out)
    assert len(df) > 0
    assert "orbital_velocity_km_s" in df.columns
