import pandas as pd
import numpy as np
from src.utils.db import get_engine

def build_features():
    engine = get_engine()
    df = pd.read_sql("SELECT * FROM results", engine)

    # Sort to ensure chronological order
    df = df.sort_values(['driver_id', 'season', 'round'])

    # Weighted Rolling Average Function
    # Weights: [0.1, 0.1, 0.15, 0.25, 0.4] (Total = 1.0)
    weights = np.array([0.1, 0.1, 0.15, 0.25, 0.4])
    
    def weighted_rolling(x):
        if len(x) < 5:
            return x.mean() # Fallback for new drivers
        return np.dot(x, weights)

    # Apply weighted form
    df['driver_form'] = df.groupby('driver_id')['position'].transform(
        lambda x: x.rolling(window=5, min_periods=1).apply(weighted_rolling, raw=True)
    )
    
    df['team_form'] = df.groupby('constructor_id')['position'].transform(
        lambda x: x.rolling(window=5, min_periods=1).apply(weighted_rolling, raw=True)
    )

    # Add career_races counter
    df['career_races'] = df.groupby('driver_id').cumcount()

    # Fill NaNs with neutral midfield value
    df[['driver_form', 'team_form']] = df[['driver_form', 'team_form']].fillna(10.5)

    df.to_sql('features', engine, if_exists='replace', index=False)
    print("🚀 Advanced weighted features built!")

if __name__ == "__main__":
    build_features()