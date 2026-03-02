"""Extract: read raw data from source (CSV, API, etc.)."""
import pandas as pd
from pathlib import Path


def extract_csv(path: str | Path) -> pd.DataFrame:
    """Extract data from CSV source."""
    return pd.read_csv(path)


def extract_sample_data() -> pd.DataFrame:
    """
    Extract sample orbital parameters for demo.
    In production, this would connect to S3, API, or streaming source.
    """
    data_dir = Path(__file__).parent.parent / "data"
    data_dir.mkdir(exist_ok=True)
    raw_path = data_dir / "raw_orbital_params.csv"

    if not raw_path.exists():
        # Generate sample data if not present
        df = pd.DataFrame({
            "object_id": ["ISS", "Hubble", "TESS", "JWST", "Starlink-1"],
            "semi_major_axis_km": [6771, 6910, 108000, 1500000, 550],
            "eccentricity": [0.0001, 0.0003, 0.55, 0.97, 0.001],
            "inclination_deg": [51.6, 28.5, 37.0, 0.0, 53.0],
            "orbital_period_min": [93, 97, 1440, 525600, 95],
        })
        df.to_csv(raw_path, index=False)

    return extract_csv(raw_path)
