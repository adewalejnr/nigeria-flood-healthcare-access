from pathlib import Path
import geopandas as gpd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED = PROJECT_ROOT / "data" / "processed"

print("Loading facilities...")
facilities = gpd.read_file(PROCESSED / "health_facilities_4states.gpkg")

target_states = ["Lagos", "Imo", "Cross River", "Rivers"]

print("Before cleaning:")
print(facilities["state"].value_counts())

# Keep only the four target states
facilities_clean = facilities[facilities["state"].isin(target_states)].copy()

print("\nAfter cleaning:")
print(facilities_clean["state"].value_counts())
print(f"\nTotal clean facilities: {len(facilities_clean)}")

# Save cleaned version
output = PROCESSED / "health_facilities_4states_clean.gpkg"
facilities_clean.to_file(output, driver="GPKG")
print(f"\nSaved cleaned facilities to: {output}")