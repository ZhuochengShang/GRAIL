#!/usr/bin/env python3
"""
Threshold-mask a raster: keep pixels ABOVE a cutoff, set the rest to nodata.

Single-machine reference implementation (rasterio). The GRAIL demo agent should
translate this to an RDPro `filterPixels` job that writes a GeoTIFF.

Usage:
  python raster_threshold_mask.py --raster ../fixtures/nldas_boston_30m.tif \
      --threshold 300 --output-tif masked.tif
"""
import argparse
from pathlib import Path

import numpy as np
import rasterio

DEFAULT_RASTER = Path(__file__).resolve().parent.parent / "fixtures" / "nldas_boston_30m.tif"
NODATA_VALUE = -9999.0


def threshold_mask(raster_path: Path, threshold: float, output_tif: Path) -> None:
    with rasterio.open(raster_path) as src:
        if src.count < 1:
            raise ValueError(f"Raster has no bands: {raster_path}")
        band = src.read(1).astype(np.float32)
        src_nodata = src.nodata

        keep = band > threshold
        if src_nodata is not None:
            keep &= band != src_nodata
        keep &= np.isfinite(band)

        out = np.where(keep, band, NODATA_VALUE).astype(np.float32)

        profile = src.profile.copy()
        profile.update(count=1, dtype="float32", nodata=NODATA_VALUE)

    output_tif.parent.mkdir(parents=True, exist_ok=True)
    with rasterio.open(output_tif, "w", **profile) as dst:
        dst.write(out, 1)

    kept = int(np.count_nonzero(out != NODATA_VALUE))
    print(f"Kept {kept} pixels above {threshold}; wrote {output_tif}")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Keep raster pixels above a threshold, mask the rest.")
    p.add_argument("--raster", type=Path, default=DEFAULT_RASTER)
    p.add_argument("--threshold", type=float, required=True,
                   help="Pixels with value > threshold are kept; others become nodata.")
    p.add_argument("--output-tif", type=Path, default=Path("masked.tif"))
    return p.parse_args()


if __name__ == "__main__":
    args = parse_args()
    threshold_mask(args.raster, args.threshold, args.output_tif)
