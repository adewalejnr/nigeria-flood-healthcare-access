# Mapping Healthcare Access Gaps in High Flood-Risk Communities in Nigeria

**Focus States:** Cross River, Imo, Lagos, and Rivers

## Project Overview

This project analyses the spatial relationship between healthcare facilities and flood-exposed populations in four high-risk Nigerian states. It uses open geospatial data to identify areas where flooding may disrupt access to healthcare services.

The analysis is original and was developed as a portfolio project with relevance to flood risk management and public health planning in Nigeria.

## Key Findings

### Healthcare Facilities
- **Total facilities analysed:** 6,869
  - Lagos: 2,795
  - Imo: 1,775
  - Cross River: 1,516
  - Rivers: 783

### Accessibility (normal conditions)
- **81.8%** of the population lives within 1 km of a health facility
- **95.8%** lives within 2 km
- Only **0.6%** lives more than 5 km away

### Flood Exposure (100-year return period, 30 cm depth)
Female population living in flood-exposed areas:
- **Lagos:** ≈ 1.25 million
- **Rivers:** ≈ 1.09 million
- **Cross River:** ≈ 152,000
- **Imo:** ≈ 39,000

**Main insight:** While most people live relatively close to a health facility under normal conditions, a large number of people (especially women) in Lagos and Rivers live in areas that can be flooded, creating potential access barriers during flood events.

## Repository Contents

- `Notebooks/` — Analysis scripts (01 to 14)
- `Data/Processed/` — Cleaned GeoPackage layers
- `Outputs/Maps/` — Final maps (individual state maps)
- `Outputs/Tables/` — Summary tables
- `.gitignore` — Excludes large raw data files

## Data Sources

| Dataset                    | Source                          | Notes |
|---------------------------|----------------------------------|-------|
| Health Facilities         | GRID3 Nigeria                   | Included (processed) |
| Administrative Boundaries | HDX COD-AB                      | Included (processed) |
| Flood Exposure            | HDX Risk Assessment Indicators  | Included (CSV) |
| Population Raster         | WorldPop / GRID3 2025           | **Not included** (large file) |
| OpenStreetMap extract     | Geofabrik                       | **Not included** (large file) |

### How to Download the Excluded Files

Because of GitHub file size limits, the following large files were not uploaded:

1. **Population Raster** (`NGA_population_v3_0_gridded.tif`)
   - Download from: [WorldPop / GRID3 Nigeria Population](https://wopr.worldpop.org/?NGA/Population)
   - Place it in `Data/Raw/`

2. **OpenStreetMap Nigeria extract** (`nigeria-*.osm.pbf`)
   - Download from: [Geofabrik Nigeria](https://download.geofabrik.de/africa/nigeria.html)
   - Place it in `Data/Raw/`

3. **Original Admin Boundaries and Health Facilities**
   - Admin boundaries: [HDX COD-AB Nigeria](https://data.humdata.org/dataset/cod-ab-nga)
   - Health facilities: [GRID3 Health Facilities](https://data.humdata.org/dataset/grid3-nga-health-facilities-v2-0)

After downloading, place the files in the `Data/Raw/` folder to reproduce the full analysis.

## Methods

1. Filtered administrative boundaries to the four target states
2. Cleaned and clipped health facilities
3. Clipped population raster to the study area
4. Calculated Euclidean distance to the nearest health facility
5. Joined flood exposure indicators to LGA boundaries
6. Produced summary statistics and individual state maps

## How to Reproduce

1. Clone this repository
2. Create a Conda environment:
   ```bash
   conda create -n floodgis python=3.12
   conda activate floodgis
   conda install -c conda-forge geopandas rasterio shapely fiona pyproj pandas numpy matplotlib scipy
3. Download the excluded large files (see above) into Data/Raw/
4. Run the scripts in the Notebooks/ folder in order (01 → 14)
