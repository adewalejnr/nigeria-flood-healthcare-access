from pathlib import Path
import geopandas as gpd
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED = PROJECT_ROOT / "data" / "processed"
OUTPUTS = PROJECT_ROOT / "outputs" / "tables"
OUTPUTS.mkdir(parents=True, exist_ok=True)

print("Loading data...")

# 1. Clean facilities
facilities = gpd.read_file(PROCESSED / "health_facilities_4states_clean.gpkg")
fac_summary = facilities.groupby("state").size().reset_index(name="health_facilities")
fac_summary = fac_summary.rename(columns={"state": "State"})

# 2. Flood exposure
lgas_flood = gpd.read_file(PROCESSED / "lgas_4states_with_flood.gpkg")

print("Available RP100 columns:")
print([c for c in lgas_flood.columns if "RP100" in c])

# Build aggregation dictionary only with existing columns
agg_dict = {}
if "RP100_female_pop_30cm" in lgas_flood.columns:
    agg_dict["RP100_female_pop_30cm"] = "sum"
if "RP100_primary_healthcare_30cm_count" in lgas_flood.columns:
    agg_dict["RP100_primary_healthcare_30cm_count"] = "sum"
if "RP100_hospitals_30cm_count" in lgas_flood.columns:
    agg_dict["RP100_hospitals_30cm_count"] = "sum"

flood_summary = lgas_flood.groupby("adm1_name").agg(agg_dict).reset_index()

# Rename columns
rename_map = {
    "adm1_name": "State",
    "RP100_female_pop_30cm": "Female_pop_exposed_RP100",
    "RP100_primary_healthcare_30cm_count": "Primary_HC_exposed_RP100",
    "RP100_hospitals_30cm_count": "Hospitals_exposed_RP100"
}
flood_summary = flood_summary.rename(columns=rename_map)

# 3. Merge
summary = fac_summary.merge(flood_summary, on="State", how="left")

# Round
if "Female_pop_exposed_RP100" in summary.columns:
    summary["Female_pop_exposed_RP100"] = summary["Female_pop_exposed_RP100"].round(0).astype("Int64")

print("\n=== COMBINED SUMMARY TABLE ===")
print(summary.to_string(index=False))

# Save
output_csv = OUTPUTS / "combined_summary_by_state.csv"
summary.to_csv(output_csv, index=False)
print(f"\nSaved to: {output_csv}")