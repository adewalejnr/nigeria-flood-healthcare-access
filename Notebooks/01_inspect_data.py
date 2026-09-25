from pathlib import Path
import geopandas as gpd

# More robust path handling
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW = PROJECT_ROOT / "data" / "raw"
PROCESSED = PROJECT_ROOT / "data" / "processed"
PROCESSED.mkdir(parents=True, exist_ok=True)

print("Project root:", PROJECT_ROOT)
print("Looking in:", RAW)
print()

print("=== Files found in data/raw ===")
files = list(RAW.glob("*"))
if not files:
    print("No files found.")
else:
    for f in sorted(files):
        print("-", f.name)

print("\n=== Looking for useful layers ===")

# Admin boundaries (prefer admin1 or admin2)
admin_candidates = list(RAW.glob("nga_admin1*.shp")) + list(RAW.glob("nga_admin2*.shp"))
print("Admin candidates:", [f.name for f in admin_candidates])

# Health facilities
health_candidates = list(RAW.glob("*health*.gpkg")) + list(RAW.glob("*health*.shp"))
print("Health facilities candidates:", [f.name for f in health_candidates])