from pathlib import Path
import geopandas as gpd
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW = PROJECT_ROOT / "data" / "raw"
PROCESSED = PROJECT_ROOT / "data" / "processed"
OUTPUTS = PROJECT_ROOT / "outputs" / "tables"
OUTPUTS.mkdir(parents=True, exist_ok=True)

print("Loading LGAs for 4 states...")
lgas = gpd.read_file(PROCESSED / "lgas_4states.gpkg")
print(f"LGAs: {len(lgas)}")

print("Loading flood exposure CSV...")
flood = pd.read_csv(RAW / "NGA_ADM2_flood_exposure.csv")
print(f"Flood records: {len(flood)}")

# Standardise the join key
lgas["join_key"] = lgas["adm2_pcode"].astype(str).str.strip()
flood["join_key"] = flood["ADM2_PCODE"].astype(str).str.strip()

print("\nSample join keys from LGAs:", lgas["join_key"].head(3).tolist())
print("Sample join keys from Flood:", flood["join_key"].head(3).tolist())

# Join
lgas_flood = lgas.merge(flood, on="join_key", how="left")

print(f"\nAfter join: {len(lgas_flood)} LGAs")
print(f"LGAs with flood data: {lgas_flood['ADM2_PCODE'].notna().sum()}")

# Select useful flood columns (focusing on population exposure and health facilities)
useful_cols = [
    "adm1_name", "adm2_name", "adm2_pcode", "geometry",
    "RP10_female_pop_30cm", "RP10_children_u5_30cm", "RP10_elderly_30cm",
    "RP10_hospitals_30cm_count", "RP10_primary_healthcare_30cm_count",
    "RP50_female_pop_30cm", "RP50_hospitals_30cm_count", "RP50_primary_healthcare_30cm_count",
    "RP100_female_pop_30cm", "RP100_hospitals_30cm_count", "RP100_primary_healthcare_30cm_count",
    "RP500_female_pop_30cm", "RP500_hospitals_30cm_count", "RP500_primary_healthcare_30cm_count"
]

# Keep only columns that actually exist
existing_cols = [c for c in useful_cols if c in lgas_flood.columns]
lgas_flood_clean = lgas_flood[existing_cols].copy()

# Save
output_gpkg = PROCESSED / "lgas_4states_with_flood.gpkg"
lgas_flood_clean.to_file(output_gpkg, driver="GPKG")
print(f"\nSaved joined layer to: {output_gpkg}")

# Quick summary by state
print("\n=== Summary: Primary Healthcare facilities exposed (RP100) by State ===")
if "RP100_primary_healthcare_30cm_count" in lgas_flood_clean.columns:
    summary = lgas_flood_clean.groupby("adm1_name")["RP100_primary_healthcare_30cm_count"].sum()
    print(summary)

print("\n=== Summary: Female population exposed (RP100) by State ===")
if "RP100_female_pop_30cm" in lgas_flood_clean.columns:
    summary = lgas_flood_clean.groupby("adm1_name")["RP100_female_pop_30cm"].sum()
    print(summary.round(0))