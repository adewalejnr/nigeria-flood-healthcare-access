from pathlib import Path
import geopandas as gpd

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW = PROJECT_ROOT / "data" / "raw"
PROCESSED = PROJECT_ROOT / "data" / "processed"

print("Loading filtered states...")
states_4 = gpd.read_file(PROCESSED / "states_4.gpkg")
print(f"States loaded: {list(states_4['adm1_name'])}")

print("\nLoading health facilities...")
facilities = gpd.read_file(RAW / "nga_health_facilities_v2_0.gpkg")
print(f"Total facilities in Nigeria: {len(facilities)}")
print("CRS of facilities:", facilities.crs)
print("Columns:", list(facilities.columns)[:15])  # first 15 columns

# Make sure both are in the same CRS
if facilities.crs != states_4.crs:
    print("\nReprojecting facilities to match states CRS...")
    facilities = facilities.to_crs(states_4.crs)

print("\nClipping facilities to the 4 states...")
facilities_4 = gpd.clip(facilities, states_4)
print(f"Facilities within the 4 states: {len(facilities_4)}")

# Save
output_path = PROCESSED / "health_facilities_4states.gpkg"
facilities_4.to_file(output_path, driver="GPKG")
print(f"\nSaved clipped facilities to: {output_path}")

# Quick summary by state (if possible)
if "adm1_name" in facilities_4.columns or any("state" in c.lower() for c in facilities_4.columns):
    print("\nSample of facilities:")
    print(facilities_4.head(3))
else:
    # Spatial join to get state name
    facilities_with_state = gpd.sjoin(facilities_4, states_4[["adm1_name", "geometry"]], how="left", predicate="within")
    print("\nFacilities per state:")
    print(facilities_with_state["adm1_name"].value_counts())