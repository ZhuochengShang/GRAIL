import argparse
import csv
from pathlib import Path
from typing import Dict, Iterable, List
import warnings

import geopandas as gpd
import numpy as np
import rasterio
from rasterio.mask import mask

NLCD_NODATA = 250

NLCD_CLASS_NAMES = {
    11: "Open Water",
    12: "Perennial Ice/Snow",
    21: "Developed, Open Space",
    22: "Developed, Low Intensity",
    23: "Developed, Medium Intensity",
    24: "Developed, High Intensity",
    31: "Barren Land",
    41: "Deciduous Forest",
    42: "Evergreen Forest",
    43: "Mixed Forest",
    52: "Shrub/Scrub",
    71: "Grassland/Herbaceous",
    81: "Pasture/Hay",
    82: "Cultivated Crops",
    90: "Woody Wetlands",
    95: "Emergent Herbaceous Wetlands",
}

DEVELOPED_CLASSES = {21, 22, 23, 24}
IMPERVIOUS_CLASSES = {22, 23, 24}
HIGH_INTENSITY_CLASSES = {23, 24}
FOREST_CLASSES = {41, 42, 43}
WETLAND_CLASSES = {90, 95}
AGRICULTURAL_CLASSES = {81, 82}
WATER_CLASSES = {11, 12}
SHRUB_GRASS_CLASSES = {52, 71}
BARREN_CLASSES = {31}

DEFAULT_RASTER_PATH = Path(
    "/Users/clockorangezoe/Downloads/Annual_NLCD_LndCov_2024_CU_C1V1/Annual_NLCD_LndCov_2024_CU_C_1V1_clip.tif"
)
DEFAULT_SHAPEFILE_PATH = Path(
    "/Users/clockorangezoe/Downloads/boston_neighborhood_boundaries/Boston_Neighborhood_Boundaries_sample.shp"
)


def calculate_land_use_percentages(
    raster_values,
    raster_nodata,
) -> Dict[int, Dict[str, float]]:
    band = raster_values[0]

    if np.ma.isMaskedArray(band):
        valid_mask = ~np.ma.getmaskarray(band)
        valid_mask &= band.data != NLCD_NODATA
        if raster_nodata is not None:
            valid_mask &= band.data != raster_nodata
        valid_values = band.data[valid_mask]
    else:
        valid_mask = band != NLCD_NODATA
        if raster_nodata is not None:
            valid_mask &= band != raster_nodata
        valid_mask &= np.isfinite(band)
        valid_values = band[valid_mask]

    if valid_values.size == 0:
        return {}

    class_values = valid_values.reshape(-1).astype(int, copy=False)
    unique_values, counts = np.unique(class_values, return_counts=True)
    total = int(counts.sum())

    return {
        int(class_value): {
            "pixel_count": int(count),
            "percent": (int(count) / total) * 100.0,
        }
        for class_value, count in zip(unique_values.tolist(), counts.tolist())
    }


def inspect_shapefile(shape_path: Path) -> None:
    gdf = gpd.read_file(shape_path)
    print(f"Shapefile: {shape_path.name}")
    print(f"CRS: {gdf.crs}")
    print(f"Features: {len(gdf)}")
    print(f"Columns: {list(gdf.columns)}")
    non_geometry = [col for col in gdf.columns if col != "geometry"]
    if non_geometry:
        print("\nFirst 5 rows:")
        print(gdf[non_geometry].head().to_string(index=False))


def load_vector(shape_path: Path, raster_crs) -> gpd.GeoDataFrame:
    gdf = gpd.read_file(shape_path)
    if gdf.empty:
        raise ValueError(f"Shapefile has no features: {shape_path}")
    if gdf.crs is None:
        raise ValueError(f"Shapefile CRS is missing: {shape_path}")
    if gdf.crs != raster_crs:
        gdf = gdf.to_crs(raster_crs)
    gdf = gdf[gdf.geometry.notnull() & ~gdf.geometry.is_empty].copy()
    if gdf.empty:
        raise ValueError("No valid geometries found in shapefile")
    return gdf


def summarize_geometry(src, geometry) -> Dict[int, Dict[str, float]]:
    out_img, _ = mask(src, [geometry], crop=True, filled=False)
    return calculate_land_use_percentages(out_img, src.nodata)


def geometry_overlaps_raster(bounds, geometry) -> bool:
    minx, miny, maxx, maxy = geometry.bounds
    return not (
        maxx < bounds.left
        or minx > bounds.right
        or maxy < bounds.bottom
        or miny > bounds.top
    )


def build_output_rows(
    zone_id: str,
    zone_name: str,
    stats: Dict[int, Dict[str, float]],
) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for class_value, class_stats in sorted(stats.items()):
        rows.append(
            {
                "zone_id": zone_id,
                "zone_name": zone_name,
                "class_value": class_value,
                "class_name": NLCD_CLASS_NAMES.get(class_value, "Unknown"),
                "pixel_count": class_stats["pixel_count"],
                "percent": round(class_stats["percent"], 4),
            }
        )
    return rows


def build_summary_row(
    zone_id: str,
    zone_name: str,
    stats: Dict[int, Dict[str, float]],
) -> Dict[str, object]:
    if not stats:
        return {
            "zone_id": zone_id,
            "zone_name": zone_name,
            "dominant_class": "",
            "dominant_label": "",
            "dominant_pct": 0.0,
            "pct_developed": 0.0,
            "pct_impervious": 0.0,
            "pct_high_intensity": 0.0,
            "pct_forest": 0.0,
            "pct_wetland": 0.0,
            "pct_water": 0.0,
            "pct_agricultural": 0.0,
            "pct_shrub_grass": 0.0,
            "pct_barren": 0.0,
        }

    def sum_pct(classes: set[int]) -> float:
        return round(sum(value["percent"] for key, value in stats.items() if key in classes), 2)

    dominant_class, dominant_stats = max(stats.items(), key=lambda item: item[1]["percent"])
    return {
        "zone_id": zone_id,
        "zone_name": zone_name,
        "dominant_class": dominant_class,
        "dominant_label": NLCD_CLASS_NAMES.get(dominant_class, "Unknown"),
        "dominant_pct": round(dominant_stats["percent"], 2),
        "pct_developed": sum_pct(DEVELOPED_CLASSES),
        "pct_impervious": sum_pct(IMPERVIOUS_CLASSES),
        "pct_high_intensity": sum_pct(HIGH_INTENSITY_CLASSES),
        "pct_forest": sum_pct(FOREST_CLASSES),
        "pct_wetland": sum_pct(WETLAND_CLASSES),
        "pct_water": sum_pct(WATER_CLASSES),
        "pct_agricultural": sum_pct(AGRICULTURAL_CLASSES),
        "pct_shrub_grass": sum_pct(SHRUB_GRASS_CLASSES),
        "pct_barren": sum_pct(BARREN_CLASSES),
    }


def aggregate_stats(
    stats_iterable: Iterable[Dict[int, Dict[str, float]]],
) -> Dict[int, Dict[str, float]]:
    class_counts: Dict[int, int] = {}

    for stats in stats_iterable:
        for class_value, class_stats in stats.items():
            class_counts[class_value] = class_counts.get(class_value, 0) + int(class_stats["pixel_count"])

    total = sum(class_counts.values())
    if total == 0:
        return {}

    return {
        class_value: {
            "pixel_count": count,
            "percent": (count / total) * 100.0,
        }
        for class_value, count in sorted(class_counts.items())
    }


def zonal_land_use_by_feature(
    cdl_tif: Path,
    shape_path: Path,
    zone_field: str,
) -> tuple[List[Dict[str, object]], List[Dict[str, object]]]:
    output_rows: List[Dict[str, object]] = []
    summary_rows: List[Dict[str, object]] = []
    all_zone_stats: List[Dict[int, Dict[str, float]]] = []

    with rasterio.open(cdl_tif) as src:
        if src.crs is None:
            raise ValueError(f"Raster CRS is missing: {cdl_tif}")
        if src.count < 1:
            raise ValueError(f"Raster has no bands: {cdl_tif}")
        if src.width <= 0 or src.height <= 0:
            raise ValueError(f"Invalid raster dimensions: {src.width}x{src.height}")
        if src.transform is None:
            raise ValueError("Raster transform is missing")

        gdf = load_vector(shape_path, src.crs)
        if zone_field not in gdf.columns:
            raise ValueError(f"Field '{zone_field}' not found in {shape_path.name}. Available fields: {list(gdf.columns)}")

        for zone_index, row in gdf.iterrows():
            zone_name = str(row[zone_field])
            zone_id = str(zone_index)
            if not geometry_overlaps_raster(src.bounds, row.geometry):
                warnings.warn(f"Geometry out of raster bounds: {zone_name}")
                continue
            try:
                stats = summarize_geometry(src, row.geometry)
            except Exception as exc:
                warnings.warn(f"Mask failed for {zone_name}: {exc}")
                continue
            if not stats:
                warnings.warn(f"No valid pixels found for {zone_name}")
                continue
            all_zone_stats.append(stats)
            output_rows.extend(build_output_rows(zone_id, zone_name, stats))
            summary_rows.append(build_summary_row(zone_id, zone_name, stats))

        # Avoid rasterizing one giant dissolved geometry for the "ALL" row.
        # That path can require several GB of memory on large extents.
        merged_stats = aggregate_stats(all_zone_stats)
        output_rows.extend(build_output_rows("ALL", "Boston_All_Neighborhoods", merged_stats))
        summary_rows.append(build_summary_row("ALL", "Boston_All_Neighborhoods", merged_stats))

    return output_rows, summary_rows


def write_csv(rows: Iterable[Dict[str, object]], output_csv: Path) -> None:
    rows = list(rows)
    if not rows:
        raise ValueError("No output rows were generated")

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Calculate NLCD land-cover composition for each polygon in a shapefile.",
    )
    parser.add_argument(
        "--raster",
        type=Path,
        default=DEFAULT_RASTER_PATH,
        help=f"Path to the NLCD raster GeoTIFF. Default: {DEFAULT_RASTER_PATH}",
    )
    parser.add_argument(
        "--shapefile",
        type=Path,
        default=DEFAULT_SHAPEFILE_PATH,
        help=f"Path to the neighborhood boundary shapefile. Default: {DEFAULT_SHAPEFILE_PATH}",
    )
    parser.add_argument(
        "--zone-field",
        default="name",
        help="Attribute field used to name each polygon zone. Default: name",
    )
    parser.add_argument(
        "--output-csv",
        type=Path,
        default=Path("boston_land_use_by_neighborhood_sample.csv"),
        help="Path to the output CSV file.",
    )
    parser.add_argument(
        "--summary-csv",
        type=Path,
        default=Path("boston_land_use_summary_sample.csv"),
        help="Path to the grouped summary CSV file.",
    )
    parser.add_argument(
        "--inspect-only",
        action="store_true",
        help="Print shapefile metadata and exit.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    if args.inspect_only:
        inspect_shapefile(args.shapefile)
    else:
        rows, summary_rows = zonal_land_use_by_feature(args.raster, args.shapefile, args.zone_field)
        write_csv(rows, args.output_csv)
        write_csv(summary_rows, args.summary_csv)
        print(f"Wrote {len(rows)} rows to {args.output_csv}")
        print(f"Wrote {len(summary_rows)} rows to {args.summary_csv}")
