import joblib
import pandas as pd
from pathlib import Path
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from src.utils.db import get_engine

def run_training():
    # 1. Load data from SQL
    engine = get_engine()
    query = "SELECT * FROM features"
    df = pd.read_sql(query, engine)
    
    if df.empty:
        print("❌ No features found in SQL. Run build_features first!")
        return

    # 2. Setup Features and Target
    feature_cols = ['grid', 'driver_form', 'team_form', 'career_races']
    
    # --- FIX: Ensure all features are numeric for XGBoost ---
    # This prevents the 'object' dtype error for team_form
    for col in feature_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(10.0)

    X = df[feature_cols]
    y = df['is_podium'].astype(int)
    
    # 3. Split Data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 4. Train High-Resolution Model
    print("Training high-resolution XGBoost model (500 trees) with Team Form...")
    model = XGBClassifier(
        n_estimators=500,     # High number of trees for detail
        max_depth=6,          # Depth to capture non-linear relationships
        learning_rate=0.01,   # Slow learning for better generalization
        subsample=0.8,        # Prevent overfitting
        colsample_bytree=0.8, 
        scale_pos_weight=5,   # Handle class imbalance for podium finishes
        gamma=0.1,            # Minimum loss reduction for splits
        random_state=42
    )
    model.fit(X_train, y_train)
    
    # 5. Save model and metadata
    model_dir = Path("models")
    model_dir.mkdir(parents=True, exist_ok=True)
    model_path = model_dir / "f1_model.joblib"
    
    payload = {
        "model": model,
        "feature_names": feature_cols
    }
    joblib.dump(payload, model_path)
    
    # 6. Evaluate and Print Accuracy
    accuracy = model.score(X_test, y_test)
    print(f"🚀 Training complete! Model saved to: {model_path}")
    print(f"✅ Accuracy: {accuracy}")

if __name__ == "__main__":
    run_training()