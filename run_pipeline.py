import subprocess
import sys

def run_command(command):
    print(f"Executing: {command}")
    process = subprocess.run(command, shell=True)
    if process.returncode != 0:
        print(f"❌ Error during: {command}")
        sys.exit(1)

def main():
    # Get race_id from command line or default to 2025_5
    target_race = sys.argv[1] if len(sys.argv) > 1 else '2025_5'

    print(f"🚀 Starting F1 Prediction Pipeline for {target_race}...")
    
    # Step 1: Migrate Data
    run_command("docker-compose run --rm f1-app python -m src.data.migrate_to_sql")
    
    # Step 2: Build Features
    run_command("docker-compose run --rm f1-app python -m src.features.build_features")
    
    # Step 3: Run Prediction
    run_command(f"docker-compose run --rm f1-app python -m src.models.predict {target_race}")

    print("\n✅ Pipeline Complete!")

if __name__ == "__main__":
    main()