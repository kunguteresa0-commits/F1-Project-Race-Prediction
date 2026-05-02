import pandas as pd
import fastf1
import requests
import logging
from pathlib import Path
from src.utils.io_utils import load_settings, save_csv, save_parquet

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class F1Ingestor:
    def __init__(self):
        self.settings = load_settings()
        self.raw_path = Path(self.settings["paths"]["raw_data"])

    def fetch_history(self, start_year=2021, end_year=2025):
        """Fetches historical race results using the Jolpica (Ergast) API."""
        logger.info(f"🚀 Starting ingestion for seasons {start_year} through {end_year}...")
        all_data = []
        
        for year in range(start_year, end_year + 1):
            # Using a limit of 1000 to ensure we capture all results for the season in one call
            url = f"https://api.jolpi.ca/ergast/f1/{year}/results.json?limit=1000"
            try:
                response = requests.get(url)
                response.raise_for_status()
                r = response.json()
                races = r['MRData']['RaceTable']['Races']
                
                logger.info(f"📅 {year}: Found {len(races)} races")
                
                for race in races:
                    # Create a unique race_id for SQL indexing (e.g., '2023_1')
                    race_id = f"{year}_{race['round']}"
                    for res in race['Results']:
                        all_data.append({
                            'race_id': race_id,
                            'season': year, 
                            'round': int(race['round']),
                            'circuit_id': race['Circuit']['circuitId'],
                            'driver_id': res['Driver']['driverId'],
                            'grid': int(res['grid']),
                            'position': int(res['position']) if res['position'].isdigit() else 20
                        })
            except Exception as e:
                logger.error(f"❌ Failed to fetch data for {year}: {e}")

        if all_data:
            df = pd.DataFrame(all_data)
            output_file = self.raw_path / "historical_results.csv"
            save_csv(df, output_file)
            logger.info(f"✅ Success! Saved {len(df)} rows to {output_file}")
        else:
            logger.warning("⚠️ No data was collected.")

    def fetch_telemetry(self, year=2024, race_round=1):
        """Fetches detailed lap timing from FastF1."""
        fastf1.Cache.enable_cache(self.settings["paths"]["fastf1_cache"])
        session = fastf1.get_session(year, race_round, 'R')
        session.load()
        laps = session.laps
        save_parquet(laps, self.raw_path / f"laps_{year}_{race_round}.parquet")

if __name__ == "__main__":
    ingestor = F1Ingestor()
    # We fetch from 2021 to 2025 to give the model plenty of "experience"
    ingestor.fetch_history(start_year=2021, end_year=2025)