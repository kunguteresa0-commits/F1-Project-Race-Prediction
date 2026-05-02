import pandas as pd
from pathlib import Path

def load_settings():
    """Returns a dictionary of project paths and model settings."""
    return {
        "paths": {
            "raw_data": "data/raw",
            "processed_data": "data/processed",
            "fastf1_cache": "data/fastf1_cache",
            "artifacts": "artifacts"
        },
        "model": {
            "rolling_window": 5,
            "track_window": 3
        }
    }

def save_csv(df, path):
    """Saves a DataFrame as a CSV file, ensuring the directory exists."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    print(f"File saved to: {path}")

def save_parquet(df, path):
    """Saves a DataFrame as a Parquet file for faster loading."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path, index=False)
    print(f"File saved to: {path}")

def load_parquet(path):
    """Loads a Parquet file from a given path."""
    return pd.read_parquet(path)