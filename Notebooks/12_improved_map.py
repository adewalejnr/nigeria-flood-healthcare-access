from pathlib import Path
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import matplotlib.patches as mpatches

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED = PROJECT_ROOT / "data" / "processed"
MAPS = PROJECT_ROOT / "outputs" / "maps"
MAPS.mkdir(parents=True, exist_ok=True)

print("Loading data...")
states = gpd.read_file(PROCESSED / "states_4.gpkg")
facilities = gpd.read_file(PROCESSED / "health_facilities_4states_clean.gpkg")
lgas = gpd.read_file(PROCESSED / "lgas_4states_with_flood.gpkg")

# Prepare flood column
lgas["exposed"] = lgas["RP100_female_pop_30cm"].fillna(0)

# Separate Lagos for inset
lagos_state = states[states["adm1_name"] == "Lagos"]
other_states = states[states["adm1_name"] != "Lagos"]
lagos_lgas = lgas[lgas["adm1_name"] == "Lagos"]
other_lgas = lgas[lgas["adm1_name"] != "Lagos"]
lagos_fac = facilities[facilities["state"] == "Lagos"]
other_fac = facilities[facilities["state"] != "Lagos"]

print("Creating improved map with Lagos inset...")

fig = plt.figure(figsize=(14, 10))

# Main axis for the three eastern states
ax_main = fig.add_axes([0.05, 0.05, 0.65, 0.85])

# Plot other LGAs
other_lgas.plot(
    column="exposed",
    ax=ax_main,
    cmap="YlOrRd",
    edgecolor="gray",
    linewidth=0.4,
    legend=True,
    legend_kwds={
        "label": "Female Population Exposed to Flooding (RP100)",
        "orientation": "vertical",
        "shrink": 0.55,
        "anchor": (1.0, 0.4)
    }
)

other_states.boundary.plot(ax=ax_main, color="black", linewidth=1.3)
other_fac.plot(ax=ax_main, color="#1a3a6b", markersize=5, alpha=0.75)

# Add state labels
for idx, row in other_states.iterrows():
    ax_main.annotate(
        text=row["adm1_name"],
        xy=row.geometry.centroid.coords[0],
        ha="center",
        fontsize=11,
        fontweight="bold",
        color="#222222"
    )

ax_main.set_axis_off()
ax_main.set_title("Imo, Rivers & Cross River States", fontsize=13, pad=10)

# Inset for Lagos
ax_inset = fig.add_axes([0.68, 0.55, 0.28, 0.35])

lagos_lgas.plot(
    column="exposed",
    ax=ax_inset,
    cmap="YlOrRd",
    edgecolor="gray",
    linewidth=0.4
)
lagos_state.boundary.plot(ax=ax_inset, color="black", linewidth=1.3)
lagos_fac.plot(ax=ax_inset, color="#1a3a6b", markersize=6, alpha=0.8)

ax_inset.set_title("Lagos State (Inset)", fontsize=11, pad=6)
ax_inset.set_axis_off()

# Main title
fig.suptitle(
    "Healthcare Facilities and Flood-Exposed Female Population\nCross River, Imo, Lagos & Rivers States, Nigeria",
    fontsize=15,
    fontweight="bold",
    y=0.97
)

# Footer / source
fig.text(
    0.5, 0.015,
    "Data: GRID3 Health Facilities, WorldPop Population, HDX Flood Exposure Indicators  |  Analysis: Original work",
    ha="center", fontsize=8, color="gray"
)

# Save
output = MAPS / "improved_facilities_flood_map.png"
plt.savefig(output, dpi=300, bbox_inches="tight", facecolor="white")
print(f"\nImproved map saved to: {output}")
plt.close()
print("Done.")