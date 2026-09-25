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
lgas = gpd.read_file(PROCESSED / "lgas_4states_with_flood.gpkg")

lgas["exposed"] = lgas["RP100_female_pop_30cm"].fillna(0)

# Order of states for the panels
state_order = ["Lagos", "Imo", "Rivers", "Cross River"]

print("Creating 4-panel map...")

fig, axes = plt.subplots(2, 2, figsize=(14, 12))
axes = axes.flatten()

for i, state_name in enumerate(state_order):
    ax = axes[i]
    
    # Filter data for this state
    state_gdf = states[states["adm1_name"] == state_name]
    lgas_state = lgas[lgas["adm1_name"] == state_name]
    fac_state = facilities[facilities["state"] == state_name]
    
    # Plot LGAs
    lgas_state.plot(
        column="exposed",
        ax=ax,
        cmap="YlOrRd",
        edgecolor="gray",
        linewidth=0.5,
        legend=False
    )
    
    # State boundary
    state_gdf.boundary.plot(ax=ax, color="black", linewidth=1.4)
    
    # Facilities
    fac_state.plot(ax=ax, color="#1a3a6b", markersize=8, alpha=0.8)
    
    ax.set_title(f"{state_name} State", fontsize=13, fontweight="bold", pad=8)
    ax.set_axis_off()

# Add a single shared colorbar
import matplotlib as mpl
sm = plt.cm.ScalarMappable(
    cmap="YlOrRd",
    norm=mpl.colors.Normalize(
        vmin=lgas["exposed"].min(),
        vmax=lgas["exposed"].max()
    )
)
sm._A = []
cbar = fig.colorbar(sm, ax=axes, shrink=0.55, location="right", pad=0.03)
cbar.set_label("Female Population Exposed to Flooding (RP100)", fontsize=10)

# Main title
fig.suptitle(
    "Healthcare Facilities and Flood-Exposed Female Population\nCross River, Imo, Lagos & Rivers States, Nigeria",
    fontsize=15,
    fontweight="bold",
    y=0.98
)

# Footer
fig.text(
    0.5, 0.02,
    "Data: GRID3 Health Facilities • WorldPop • HDX Flood Exposure Indicators  |  Analysis: Original work",
    ha="center",
    fontsize=8,
    color="gray"
)

plt.tight_layout(rect=[0, 0.04, 0.92, 0.95])

output = MAPS / "four_panel_facilities_flood_map.png"
plt.savefig(output, dpi=300, bbox_inches="tight", facecolor="white")
print(f"\n4-panel map saved to: {output}")
plt.close()
print("Done.")