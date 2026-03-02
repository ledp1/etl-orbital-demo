"""Load: write processed data to sink (Parquet, warehouse, etc.)."""
import pandas as pd
from pathlib import Path


def load_parquet(df: pd.DataFrame, path: str | Path) -> Path:
    """
    Write DataFrame to Parquet (columnar format).
    Parquet is efficient for analytics and compatible with Glue, Redshift, Snowflake.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path, index=False)
    return path
