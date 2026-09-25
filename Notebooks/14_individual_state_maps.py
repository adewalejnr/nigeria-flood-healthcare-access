from pathlib import Path
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED = PROJECT_ROOT / "data" / "processed"
MAPS = PROJECT_ROOT / "outputs" / "maps"
MAPS.mkdir(parents=True, exist_ok=True)

print("Loading data...")
states = gpd.read_file(PROCESSED / "states_4.gpkg")
facilities = gpd.read_file(PROCESSED / "health_facilities_4states_clean.gpkg")
lgas = gpd.read_file(PROCESSED / "lgas_4states_with_flood.gpkg")

lgas["exposed"] = lgas["RP100_female_pop_30cm"].fillna(0)

state_list = ["Lagos", "Imo", "Rivers", "Cross River"]

# Global min/max for consistent colour scale across maps
vmin = lgas["exposed"].min()
vmax = lgas["exposed"].max()

print("Creating individual state maps...")

for state_name in state_list:
    print(f"  → {state_name}")
    
    # Filter data
    state_gdf = states[states["adm1_name"] == state_name]
    lgas_state = lgas[lgas["adm1_name"] == state_name]
    fac_state = facilities[facilities["state"] == state_name]
    
    # Create figure
    fig, ax = plt.subplots(1, 1, figsize=(10, 9))
    
    # Plot LGAs with flood exposure
    lgas_state.plot(
        column="exposed",
        ax=ax,
        cmap="YlOrRd",
        edgecolor="gray",
        linewidth=0.6,
        vmin=vmin,
        vmax=vmax,
        legend=True,
        legend_kwds={
            "label": "Female Population Exposed to Flooding\n(100-year return period, 30 cm depth)",
            "shrink": 0.7,
            "orientation": "vertical",
            "pad": 0.02
        }
    )
    
    # State boundary
    state_gdf.boundary.plot(ax=ax, color="black", linewidth=1.6)
    
    # Health facilities
    fac_state.plot(
        ax=ax,
        color="#0d2b4e",
        markersize=12,
        alpha=0.85,
        label="Health Facilities",
        zorder=5
    )
    
    # Title
    ax.set_title(
        f"{state_name} State\nHealthcare Facilities and Flood-Exposed Female Population",
        fontsize=14,
        fontweight="bold",
        pad=12
    )
    
    # Clean axes
    ax.set_axis_off()
    
    # Legend for facilities
    ax.legend(loc="lower left", frameon=True, fontsize=9)
    
    # Source note
    fig.text(
        0.5, 0.02,
        "Data: GRID3 Health Facilities • WorldPop • HDX Flood Exposure Indicators  |  Original analysis",
        ha="center",
        fontsize=8,
        color="dimgray"
    )
    
    # Save individual map
    output_file = MAPS / f"map_{state_name.lower().replace(' ', '_')}.png"
    plt.tight_layout(rect=[0, 0.04, 1, 0.96])
    plt.savefig(output_file, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close()
    
    print(f"     Saved: {output_file.name}")

print("\nAll four individual maps created successfully.")