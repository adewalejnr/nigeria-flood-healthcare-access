from pathlib import Path
import geopandas as gpd
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW = PROJECT_ROOT / "data" / "raw"
PROCESSED = PROJECT_ROOT / "data" / "processed"
OUTPUTS = PROJECT_ROOT / "outputs" / "tables"
OUTPUTS.mkdir(parents=True, exist_ok=True)

print("Loading data...")

# 1. Load LGA boundaries (admin2)
lgas = gpd.read_file(RAW / "nga_admin2.shp")
print(f"Total LGAs in Nigeria: {len(lgas)}")
print("LGA columns:", list(lgas.columns)[:12])

# 2. Load the four states so we can filter
states_4 = gpd.read_file(PROCESSED / "states_4.gpkg")
target_states = ["Cross River", "Imo", "Lagos", "Rivers"]

# Filter LGAs to the four states
# First identify the correct state name column in LGA file
state_col = None
for col in ["adm1_name", "ADM1_EN", "admin1Name", "STATE", "state"]:
    if col in lgas.columns:
        state_col = col
        break

if state_col is None:
    print("Available columns in LGA file:")
    print(list(lgas.columns))
    raise ValueError("Could not find state name column in LGA file")

print(f"\nUsing state column in LGAs: {state_col}")
lgas_4 = lgas[lgas[state_col].isin(target_states)].copy()
print(f"LGAs in the 4 states: {len(lgas_4)}")

# 3. Load flood exposure CSV
flood_csv = RAW / "NGA_ADM2_flood_exposure.csv"
flood = pd.read_csv(flood_csv)
print(f"\nFlood exposure records: {len(flood)}")
print("Flood CSV columns:", list(flood.columns))

# 4. Try to join flood data to LGAs
# We need a common key (usually ADM2_PCODE or similar)
print("\nLooking for join key...")
print("LGA pcode-like columns:", [c for c in lgas_4.columns if "pcode" in c.lower() or "code" in c.lower()])
print("Flood pcode-like columns:", [c for c in flood.columns if "pcode" in c.lower() or "code" in c.lower() or "ADM" in c])

# Save intermediate files so we can inspect
lgas_4.to_file(PROCESSED / "lgas_4states.gpkg", driver="GPKG")
print(f"\nSaved LGAs for 4 states to: {PROCESSED / 'lgas_4states.gpkg'}")

# Show sample of both for diagnosis
print("\nSample LGA rows:")
print(lgas_4[[state_col] + [c for c in lgas_4.columns if "pcode" in c.lower() or "name" in c.lower()][:4]].head(3))

print("\nSample Flood rows:")
print(flood.head(3))