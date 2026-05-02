import pandas as pd
import joblib
from src.utils.db import get_engine
import sys

def make_predictions(race_id='2024_6'):
    engine = get_engine()
    
    # 1. Pull the features for the specified race
    # Using a parameterized query to prevent injection and handle strings correctly
    query = f"SELECT * FROM features WHERE race_id = '{race_id}'"
    df = pd.read_sql(query, engine)

    if df.empty:
        print(f"❌ No data found for race_id: {race_id}")
        print("Check your CSV formatting or run build_features again.")
        return

    # 2. Define features used during training
    feature_cols = ['grid', 'driver_form', 'team_form', 'career_races']
    
    # 3. Data Cleaning: Ensure all features are numeric
    for col in feature_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(10.5)
        else:
            # Fallback if a column is missing entirely
            df[col] = 10.5

    # 4. Load Model
    model_path = "models/f1_model.joblib"
    try:
        payload = joblib.load(model_path)
    except FileNotFoundError:
        print(f"❌ Model file not found at {model_path}")
        return
    
    # Handle both direct model files and dictionary payloads
    model = payload['model'] if isinstance(payload, dict) else payload
    
    # 5. Generate Predictions
    X = df[feature_cols]
    # Get probability of class 1 (Podium)
    df['podium_probability'] = model.predict_proba(X)[:, 1]
    
    # 6. Sort and Print Results
    predictions = df[['driver_id', 'podium_probability']].sort_values(
        by='podium_probability', 
        ascending=False
    )
    
    print(f"\n--- 🏎️ {race_id} Full Podium Predictions ---")
    if len(predictions) < 20:
        print(f"⚠️ Warning: Only showing {len(predictions)} drivers. Check your data sources.")
    
    print(predictions.to_string(index=False))

if __name__ == "__main__":
    # Allows you to run: python -m src.models.predict 2024_06 
    # Defaulting to 2024_6 if no argument is passed
    target_race = sys.argv[1] if len(sys.argv) > 1 else '2024_6'
    make_predictions(target_race)