from pathlib import Path
import geopandas as gpd
import rasterio
from rasterio import features
from rasterio.transform import from_bounds
import numpy as np
from scipy.ndimage import distance_transform_edt
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED = PROJECT_ROOT / "data" / "processed"
OUTPUTS = PROJECT_ROOT / "outputs" / "tables"
OUTPUTS.mkdir(parents=True, exist_ok=True)

print("Loading data...")
states = gpd.read_file(PROCESSED / "states_4.gpkg")
facilities = gpd.read_file(PROCESSED / "health_facilities_4states_clean.gpkg")

print(f"Facilities: {len(facilities)}")
print(f"States: {list(states['adm1_name'])}")

# Open the clipped population raster
pop_path = PROCESSED / "population_4states.tif"
with rasterio.open(pop_path) as src:
    pop_data = src.read(1)
    transform = src.transform
    crs = src.crs
    nodata = src.nodata
    shape = src.shape
    res = src.res[0]  # approximate pixel size in degrees

print(f"Population raster shape: {shape}")
print(f"Pixel resolution (approx): {res:.6f} degrees")

# ---- 1. Create a facility presence raster ----
print("\nCreating facility raster...")
# Reproject facilities if needed
if facilities.crs != crs:
    facilities = facilities.to_crs(crs)

facility_mask = features.rasterize(
    [(geom, 1) for geom in facilities.geometry if geom is not None],
    out_shape=shape,
    transform=transform,
    fill=0,
    dtype=np.uint8
)

print(f"Pixels with facilities: {facility_mask.sum()}")

# ---- 2. Calculate Euclidean distance (in pixels) ----
print("Calculating distance to nearest facility...")
# Distance transform: distance from non-facility pixels to nearest facility pixel
distance_pixels = distance_transform_edt(facility_mask == 0)

# Convert pixel distance to approximate kilometres
# 1 degree ≈ 111 km. We use average latitude correction later if needed.
pixel_size_km = res * 111  # rough conversion
distance_km = distance_pixels * pixel_size_km

print(f"Max distance found: {distance_km.max():.1f} km")

# ---- 3. Summarise population by distance bands ----
print("\nCalculating population in distance bands...")

# Mask valid population
valid_pop = np.where((pop_data > 0) & (~np.isnan(pop_data)), pop_data, 0)

bands = {
    "0 - 1 km": (distance_km >= 0) & (distance_km < 1),
    "1 - 2 km": (distance_km >= 1) & (distance_km < 2),
    "2 - 5 km": (distance_km >= 2) & (distance_km < 5),
    "5 - 10 km": (distance_km >= 5) & (distance_km < 10),
    "10+ km": (distance_km >= 10)
}

results = []
total_pop = valid_pop.sum()

for band_name, mask in bands.items():
    pop_in_band = valid_pop[mask].sum()
    pct = (pop_in_band / total_pop * 100) if total_pop > 0 else 0
    results.append({
        "Distance band": band_name,
        "Population": int(pop_in_band),
        "Percentage": round(pct, 1)
    })
    print(f"{band_name}: {pop_in_band:,.0f} people ({pct:.1f}%)")

# Save summary table
df = pd.DataFrame(results)
df.to_csv(OUTPUTS / "accessibility_summary.csv", index=False)
print(f"\nSummary saved to: {OUTPUTS / 'accessibility_summary.csv'}")

# ---- 4. Save distance raster (optional but useful) ----
distance_meta = {
    "driver": "GTiff",
    "height": shape[0],
    "width": shape[1],
    "count": 1,
    "dtype": "float32",
    "crs": crs,
    "transform": transform,
    "nodata": -9999
}

dist_path = PROCESSED / "distance_to_facility_km.tif"
with rasterio.open(dist_path, "w", **distance_meta) as dst:
    # Set nodata where population was nodata
    dist_out = distance_km.astype("float32")
    dist_out[np.isnan(pop_data)] = -9999
    dst.write(dist_out, 1)

print(f"Distance raster saved to: {dist_path}")
print("\nAccessibility analysis complete.")