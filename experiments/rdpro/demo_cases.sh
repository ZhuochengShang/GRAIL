# Shared demo case lists — sourced by run_demo_suite.sh and
# run_demo_stability.sh so the two runners can never drift apart.
# Format: "id short-name|payload" (payload = NL text or python example path).

TEXT_CASES=(
  "1.1 zonal-mean-min-max|Using a raptor join between the raster and the Boston neighborhood polygons, compute the mean, minimum, and maximum pixel value for each neighborhood. Write one row per neighborhood (name, mean, min, max, pixel_count) to CSV in the output directory."
  "1.2 hottest-neighborhood|For each Boston neighborhood polygon, count how many raster pixels fall inside it and compute the average value, then report the single neighborhood with the highest average value."
  "1.3 zonal-sum|Compute the sum of all raster pixel values that fall within each neighborhood polygon and save neighborhood name and total to CSV."
  "2.1 kelvin-to-celsius|Convert every raster pixel from Kelvin to Celsius by subtracting 273.15, and write the converted raster as a GeoTIFF to the output directory."
  "2.2 reproject-raster|Reproject the raster to EPSG:4326 and save it as a GeoTIFF in the output directory."
  "2.3 threshold-mask|Keep only raster pixels whose value is greater than 300, set all other pixels to nodata, and write the masked raster as a GeoTIFF."
  "2.4 raster-to-points|Convert every non-empty raster pixel into a point feature carrying its value as an attribute, and save the points as GeoJSON."
  "3.1 area-rank|Compute the area of each Boston neighborhood polygon and write neighborhood name and area to CSV, sorted by area descending."
  "3.2 range-query|Return only the neighborhood polygons that intersect the bounding box minx=-71.10, miny=42.30, maxx=-71.05, maxy=42.35, and save the matches as GeoJSON."
  "3.3 reproject-polygons|Reproject the Boston neighborhood polygons to EPSG:3857 and save them as a shapefile in the output directory."
  "4.1 csv-attribute-join|Load the land-use summary CSV, join it to the neighborhood polygons on the neighborhood name (CSV column zone_name = polygon field name), attach each polygon's dominant land-use label as an attribute, and save the enriched polygons as GeoJSON."
)
PY_CASES=(
  "P1 threshold-mask|../../grail-agent/examples/python/raster_threshold_mask.py"
  "P2 area-rank|../../grail-agent/examples/python/polygon_area_rank.py"
  "P3 range-query|../../grail-agent/examples/python/bbox_clip.py"
  "P4 raster-to-points|../../grail-agent/examples/python/raster_to_points.py"
  "P5 csv-join|../../grail-agent/examples/python/csv_join_polygons.py"
  "P6 zonal-minmax|../../grail-agent/examples/python/zonal_stats_minmax.py"
)
