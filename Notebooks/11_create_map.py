from pathlib import Path
import geopandas as gpd
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED = PROJECT_ROOT / "data" / "processed"
MAPS = PROJECT_ROOT / "outputs" / "maps"
MAPS.mkdir(parents=True, exist_ok=True)

print("Loading data...")
states = gpd.read_file(PROCESSED / "states_4.gpkg")
facilities = gpd.read_file(PROCESSED / "health_facilities_4states_clean.gpkg")
lgas_flood = gpd.read_file(PROCESSED / "lgas_4states_with_flood.gpkg")

# Keep original CRS (WGS84 is fine for this static map)
print("Creating clean map (no basemap)...")

fig, ax = plt.subplots(1, 1, figsize=(12, 10))

# Plot LGAs coloured by female population exposed
if "RP100_female_pop_30cm" in lgas_flood.columns:
    lgas_flood["exposed_female"] = lgas_flood["RP100_female_pop_30cm"].fillna(0)
else:
    lgas_flood["exposed_female"] = 0

lgas_flood.plot(
    column="exposed_female",
    ax=ax,
    legend=True,
    cmap="YlOrRd",
    edgecolor="gray",
    linewidth=0.4,
    legend_kwds={
        "label": "Female Population Exposed (RP100)",
        "shrink": 0.6
    }
)

# State boundaries
states.boundary.plot(ax=ax, color="black", linewidth=1.5)

# Health facilities
facilities.plot(
    ax=ax,
    color="navy",
    markersize=6,
    alpha=0.7,
    label="Health Facilities"
)

# Title and clean styling
ax.set_title(
    "Healthcare Facilities & Flood-Exposed Population\nCross River, Imo, Lagos & Rivers States, Nigeria",
    fontsize=14,
    pad=15
)
ax.set_axis_off()
ax.legend(loc="lower left", frameon=True)

# Save high-quality version
output_path = MAPS / "facilities_and_flood_exposure_clean.png"
plt.tight_layout()
plt.savefig(output_path, dpi=300, bbox_inches="tight", facecolor="white")
print(f"\nClean map saved to: {output_path}")

plt.close()
print("Done.")