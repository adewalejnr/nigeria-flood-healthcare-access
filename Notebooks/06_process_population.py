from pathlib import Path
import geopandas as gpd
import rasterio
from rasterio.mask import mask
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW = PROJECT_ROOT / "data" / "raw"
PROCESSED = PROJECT_ROOT / "data" / "processed"

print("Loading states...")
states = gpd.read_file(PROCESSED / "states_4.gpkg")

# Population raster path
pop_raster_path = RAW / "NGA_population_v3_0_gridded.tif"
print(f"\nPopulation raster: {pop_raster_path}")
print("Exists:", pop_raster_path.exists())

if not pop_raster_path.exists():
    # Check if it's inside a folder
    possible = list(RAW.glob("**/NGA_population*.tif"))
    print("Possible population files found:", possible)
    if possible:
        pop_raster_path = possible[0]
        print("Using:", pop_raster_path)

print("\nOpening population raster...")
with rasterio.open(pop_raster_path) as src:
    print("CRS:", src.crs)
    print("Bounds:", src.bounds)
    print("Resolution:", src.res)
    print("Shape:", src.shape)
    print("NoData:", src.nodata)

    # Reproject states if needed
    states_proj = states.to_crs(src.crs) if states.crs != src.crs else states

    print("\nClipping population raster to the 4 states...")
    # Mask (clip) the raster
    out_image, out_transform = mask(src, states_proj.geometry, crop=True, nodata=src.nodata)
    
    out_meta = src.meta.copy()
    out_meta.update({
        "driver": "GTiff",
        "height": out_image.shape[1],
        "width": out_image.shape[2],
        "transform": out_transform,
        "nodata": src.nodata
    })

    # Save clipped raster
    output_raster = PROCESSED / "population_4states.tif"
    with rasterio.open(output_raster, "w", **out_meta) as dest:
        dest.write(out_image)

    print(f"\nSaved clipped population raster to: {output_raster}")

    # Quick statistics
    data = out_image[0]
    valid = data[data != src.nodata] if src.nodata is not None else data
    valid = valid[valid > 0]  # remove zeros / nodata
    print(f"\nApproximate total population in the 4 states: {valid.sum():,.0f}")
    print(f"Min pixel value: {valid.min():.2f}")
    print(f"Max pixel value: {valid.max():.2f}")