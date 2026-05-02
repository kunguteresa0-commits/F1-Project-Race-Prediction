import streamlit as st
import pandas as pd
from src.utils.db import get_engine
import joblib
import os
from sqlalchemy import create_engine

st.set_page_config(page_title="F1 Podium Predictor", page_icon="🏎️")

st.title("🏎️ F1 Podium Probability Predictor")
st.markdown("Select a Race ID to see the predicted podium probabilities.")

# 1. Connect and get available races
# We override the engine here to ensure it uses the local port 5434 when running on Windows
try:
    # This tries to connect via the mapped port 5434
    engine = create_engine("postgresql://f1user:f1password@localhost:5434/f1db")
    races_df = pd.read_sql("SELECT DISTINCT race_id FROM features", engine)
    races = races_df['race_id'].tolist()
except Exception:
    # Fallback to the default utility if local connection fails
    engine = get_engine()
    races = pd.read_sql("SELECT DISTINCT race_id FROM features", engine)['race_id'].tolist()

selected_race = st.selectbox("Select Race", sorted(races, reverse=True))

if st.button("Predict Podium"):
    # 2. Load Model
    model = joblib.load("models/f1_model.joblib")
    if isinstance(model, dict): 
        model = model['model']

    # 3. Get Data
    query = f"SELECT * FROM features WHERE race_id = '{selected_race}'"
    df = pd.read_sql(query, engine)
    
    if not df.empty:
        feature_cols = ['grid', 'driver_form', 'team_form', 'career_races']
        # Ensure only existing features are used
        available_features = [c for c in feature_cols if c in df.columns]
        
        df['podium_probability'] = model.predict_proba(df[available_features])[:, 1]
        
        results = df[['driver_id', 'podium_probability']].sort_values(
            by='podium_probability', ascending=False
        )

        # 4. Display Results
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Probability Table")
            st.dataframe(results.style.format({'podium_probability': '{:.2%}'}))

        with col2:
            st.subheader("Visualized Odds")
            st.bar_chart(results.set_index('driver_id'))
    else:
        st.error("No features found for this race. Run the pipeline first!")