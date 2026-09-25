from pathlib import Path
import geopandas as gpd

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW = PROJECT_ROOT / "data" / "raw"
PROCESSED = PROJECT_ROOT / "data" / "processed"
PROCESSED.mkdir(parents=True, exist_ok=True)

print("Loading state boundaries...")
states = gpd.read_file(RAW / "nga_admin1.shp")

print("CRS:", states.crs)
print("Total states:", len(states))

# Use the correct column
name_col = "adm1_name"
print(f"\nUsing name column: {name_col}")
print("\nAvailable states:")
print(sorted(states[name_col].unique()))

# Target states
target = ["Cross River", "Imo", "Rivers", "Lagos"]

# Filter (case-insensitive partial match to be safe)
mask = states[name_col].str.contains("|".join(target), case=False, na=False)
states_4 = states[mask].copy()

print(f"\nFiltered to {len(states_4)} features:")
print(states_4[name_col].tolist())

# Save
output_path = PROCESSED / "states_4.gpkg"
states_4.to_file(output_path, driver="GPKG")
print(f"\nSaved filtered states to: {output_path}")