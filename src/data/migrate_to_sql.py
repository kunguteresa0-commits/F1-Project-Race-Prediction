import pandas as pd
import os
from src.utils.db import get_engine
from sqlalchemy import text

CONSTRUCTOR_MAP = {
    'McLaren': 'mclaren', 'Red Bull': 'red_bull', 'Ferrari': 'ferrari',
    'Mercedes': 'mercedes', 'Aston Martin': 'aston_martin', 'RB F1 Team': 'rb',
    'Haas F1 Team': 'haas', 'Alpine F1 Team': 'alpine', 'Williams': 'williams',
    'Kick Sauber': 'sauber'
}

def migrate():
    engine = get_engine()
    csv_path = "data/raw/historical_results.csv"
    
    if not os.path.exists(csv_path):
        print(f"❌ Error: {csv_path} not found.")
        return

    df = pd.read_csv(csv_path)
    
    # 1. Clean existing data to avoid UniqueViolations
    with engine.connect() as conn:
        conn.execute(text("TRUNCATE TABLE results CASCADE;"))
        conn.execute(text("TRUNCATE TABLE drivers CASCADE;"))
        conn.commit()

    # 2. Re-register Drivers
    drivers = pd.DataFrame(df['driver_id'].unique(), columns=['driver_id'])
    drivers.to_sql('drivers', engine, if_exists='append', index=False, method='multi')

    # 3. Map Constructors
    if 'team_name' in df.columns:
        df['constructor_id'] = df['team_name'].map(CONSTRUCTOR_MAP).fillna('unknown')
    
    # 4. Upload Results
    df.to_sql('results', engine, if_exists='append', index=False, method='multi')
    print("✅ Migration Successful! Database refreshed from CSV.")

if __name__ == "__main__":
    migrate()