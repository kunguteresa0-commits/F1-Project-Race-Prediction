import pandas as pd
from src.utils.db import get_engine
import joblib

def validate_race(race_id):
    engine = get_engine()
    
    # 1. Get features and actual results
    query = f"""
        SELECT f.*, r.position as actual_position 
        FROM features f
        JOIN results r ON f.driver_id = r.driver_id AND f.race_id = r.race_id
        WHERE f.race_id = '{race_id}'
    """
    df = pd.read_sql(query, engine)

    if df.empty:
        print(f"❌ No data found for {race_id}")
        return

    # 2. Load Model
    model = joblib.load("models/f1_model.joblib")
    if isinstance(model, dict): model = model['model']

    # 3. Predict
    feature_cols = ['grid', 'driver_form', 'team_form', 'career_races']
    df['prob'] = model.predict_proba(df[feature_cols])[:, 1]
    
    # 4. Compare
    df = df.sort_values('prob', ascending=False)
    print(f"\n--- Validation for {race_id} ---")
    print(df[['driver_id', 'prob', 'actual_position']].head(10).to_string(index=False))
    
    # Check if Top 3 predicted were actual Top 3
    top_3_pred = df.head(3)['driver_id'].tolist()
    top_3_actual = df[df['actual_position'] <= 3]['driver_id'].tolist()
    
    hits = len(set(top_3_pred) & set(top_3_actual))
    print(f"\n🎯 Accuracy: {hits}/3 podium finishers correctly identified in Top 3.")

if __name__ == "__main__":
    # Test on a known 2021 race from your CSV
    validate_race('2021_1')