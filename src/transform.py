"""Transform: clean, enrich, and normalize data."""
import pandas as pd


def transform_orbital_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transform raw orbital params into analytics-ready format.
    - Normalize column names
    - Compute derived fields (e.g., orbital velocity proxy)
    - Filter invalid rows
    """
    df = df.copy()

    # Normalize: lowercase, snake_case
    df.columns = df.columns.str.lower().str.replace(" ", "_")

    # Derived field: approximate orbital velocity (km/s) from vis-viva
    # v ≈ sqrt(GM/a) simplified as sqrt(398600/a) for Earth orbit
    df["orbital_velocity_km_s"] = (398600 / df["semi_major_axis_km"]).pow(0.5).round(2)

    # Classify orbit type
    df["orbit_type"] = df["semi_major_axis_km"].apply(_classify_orbit)

    # Drop rows with invalid eccentricity (must be 0–1)
    df = df[(df["eccentricity"] >= 0) & (df["eccentricity"] <= 1)]

    return df


def _classify_orbit(a_km: float) -> str:
    """Classify orbit by semi-major axis (Earth radius ~6371 km)."""
    if a_km < 8500:   # LEO: up to ~2000 km altitude
        return "LEO"
    if a_km < 42000:  # MEO: up to geostationary
        return "MEO"
    if a_km < 500000:
        return "HEO"
    return "Deep Space"
