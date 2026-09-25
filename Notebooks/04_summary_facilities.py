from pathlib import Path
import geopandas as gpd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED = PROJECT_ROOT / "data" / "processed"

print("Loading clipped facilities and states...")
facilities = gpd.read_file(PROCESSED / "health_facilities_4states.gpkg")
states = gpd.read_file(PROCESSED / "states_4.gpkg")

print(f"Total facilities: {len(facilities)}")

# Check if 'state' column already exists and is usable
if "state" in facilities.columns:
    print("\nFacilities per state (using existing 'state' column):")
    print(facilities["state"].value_counts())
else:
    print("\nPerforming spatial join to assign state names...")
    facilities = gpd.sjoin(facilities, states[["adm1_name", "geometry"]], how="left", predicate="within")
    print(facilities["adm1_name"].value_counts())

print("\nColumns available in facilities:")
print(list(facilities.columns))