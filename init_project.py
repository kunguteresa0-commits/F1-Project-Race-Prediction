import os

# Define folders
folders = ["data/raw", "data/processed", "src/data", "src/features", "src/models", "src/utils", "artifacts"]

# Create folders and __init__.py files (makes them readable by Python)
for folder in folders:
    os.makedirs(folder, exist_ok=True)
    Path = folder.split('/')
    # Create __init__.py in each level
    full_path = ""
    for part in Path:
        full_path = os.path.join(full_path, part)
        with open(os.path.join(full_path, "__init__.py"), "a"): pass

print("✅ Folders and Python packages ready!")