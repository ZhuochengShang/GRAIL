# Codex Fresh g1 README vs Gemini 3.1 Source-Fixed README

- Baseline used for g1: `LLM_readme.codex_fresh_before_docfix.md` (660.7 KiB)
- Current fixed README: `LLM_readme.md` (640.5 KiB)
- Repaired sections kept in README: 36

| API | old chars | new chars | diff +/- lines | main change signal |
|---|---:|---:|---:|---|
| `addFeature` | 3212 | 2601 | +31/-47 | failure modes, fix hint, grounded, call pattern |
| `area` | 1871 | 1934 | +23/-33 | failure modes, fix hint, grounded, call pattern |
| `computePointHistogramSparse` | 4397 | 3316 | +44/-57 | failure modes, fix hint, grounded, call pattern |
| `createDateFilter` | 2928 | 2801 | +34/-36 | failure modes, fix hint, grounded, call pattern |
| `createSummaryAccumulator` | 3385 | 2813 | +45/-41 | failure modes, fix hint, grounded, call pattern |
| `createTileIDFilter` | 3264 | 2983 | +42/-44 | failure modes, fix hint, grounded, call pattern |
| `crsToSRID` | 3858 | 2531 | +28/-54 | failure modes, fix hint, grounded, call pattern |
| `end` | 1891 | 2360 | +39/-31 | failure modes, fix hint, grounded, call pattern |
| `envelope` | 2972 | 2423 | +28/-44 | failure modes, fix hint, grounded, call pattern |
| `flatten` | 3775 | 3213 | +34/-47 | failure modes, fix hint, grounded, call pattern |
| `geometryType` | 2913 | 1961 | +22/-36 | failure modes, fix hint, grounded, call pattern |
| `getBoolean` | 2871 | 2580 | +31/-47 | failure modes, fix hint, grounded, call pattern |
| `getPointValue` | 3153 | 2061 | +24/-42 | failure modes, fix hint, grounded, call pattern |
| `isDefined` | 2610 | 2357 | +50/-38 | failure modes, fix hint, grounded, call pattern |
| `isEmptyAt` | 3228 | 2470 | +36/-50 | failure modes, fix hint, grounded, call pattern |
| `listFilesInZip` | 3236 | 2428 | +29/-54 | failure modes, fix hint, grounded, call pattern |
| `mapPixels` | 3873 | 3055 | +36/-51 | failure modes, fix hint, grounded, call pattern |
| `metadata` | 2921 | 2780 | +50/-57 | failure modes, fix hint, grounded, call pattern |
| `modelToGrid` | 3321 | 3148 | +42/-50 | failure modes, fix hint, grounded, call pattern |
| `numFields` | 1955 | 2544 | +42/-34 | failure modes, fix hint, grounded, call pattern |
| `numPartitions` | 2819 | 2290 | +29/-41 | failure modes, fix hint, grounded, call pattern |
| `overlay` | 3187 | 3111 | +37/-44 | failure modes, fix hint, grounded, call pattern |
| `part` | 1774 | 2736 | +39/-34 | failure modes, fix hint, grounded, call pattern |
| `partitionFeatures2` | 4674 | 3074 | +36/-53 | failure modes, fix hint, grounded, call pattern |
| `pixels` | 2384 | 2623 | +40/-35 | failure modes, fix hint, grounded, call pattern |
| `pointSample` | 4133 | 3155 | +45/-59 | failure modes, fix hint, grounded, call pattern |
| `raptorJoin` | 4102 | 3372 | +37/-48 | failure modes, fix hint, grounded, call pattern |
| `rasterizePixels` | 4143 | 3674 | +52/-58 | failure modes, fix hint, grounded, call pattern |
| `readConfigurationXML` | 3835 | 3072 | +36/-51 | failure modes, fix hint, grounded, call pattern |
| `readPartition` | 4054 | 3432 | +40/-51 | failure modes, fix hint, grounded, call pattern |
| `readTile` | 3275 | 3087 | +40/-48 | failure modes, fix hint, grounded, call pattern |
| `reshapeAverage` | 4810 | 3282 | +52/-38 | failure modes, fix hint, grounded, call pattern |
| `retile` | 3941 | 2070 | +21/-50 | failure modes, fix hint, grounded, call pattern |
| `splitGeometryAcrossDateLine` | 3881 | 3342 | +43/-44 | failure modes, fix hint, grounded, call pattern |
| `uniformHistogramSize` | 3789 | 2453 | +24/-49 | failure modes, fix hint, grounded, call pattern |
| `using` | 3940 | 2702 | +34/-62 | failure modes, fix hint, grounded, call pattern |

## Repaired APIs

`addFeature`, `area`, `computePointHistogramSparse`, `createDateFilter`, `createSummaryAccumulator`, `createTileIDFilter`, `crsToSRID`, `end`, `envelope`, `flatten`, `geometryType`, `getBoolean`, `getPointValue`, `isDefined`, `isEmptyAt`, `listFilesInZip`, `mapPixels`, `metadata`, `modelToGrid`, `numFields`, `numPartitions`, `overlay`, `part`, `partitionFeatures2`, `pixels`, `pointSample`, `raptorJoin`, `rasterizePixels`, `readConfigurationXML`, `readPartition`, `readTile`, `reshapeAverage`, `retile`, `splitGeometryAcrossDateLine`, `uniformHistogramSize`, `using`

## Notes

- The fixed README is smaller overall because docfix entries are compact and remove several verbose or wrong examples.
- Only entries that passed validation were kept. Failed rewrites were reverted, so they are not marked as repaired.
- Each repaired entry contains `_Grounding: doc-repaired from source (docfix)._`.
