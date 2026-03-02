"""Orchestrate ETL: extract → transform → validate → load."""
from pathlib import Path

from .extract import extract_sample_data
from .transform import transform_orbital_data
from .validate import run_validation
from .load import load_parquet


def run(output_dir: str | Path = "data/output") -> Path:
    """
    Run full ETL pipeline.
    Returns path to output Parquet file.
    """
    output_dir = Path(output_dir)

    # Extract
    raw = extract_sample_data()

    # Transform
    transformed = transform_orbital_data(raw)

    # Validate (data quality gate)
    run_validation(transformed)

    # Load
    out_path = output_dir / "orbital_params.parquet"
    load_parquet(transformed, out_path)

    return out_path


if __name__ == "__main__":
    result = run()
    print(f"Pipeline complete. Output: {result}")
