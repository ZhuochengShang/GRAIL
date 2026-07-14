# RDPro documentation experiment memo

## A1 — original documentation, shared API set

- Treatment: original `beast/README.md` plus `beast/doc` material, relevant-document scope
- Frozen comparison manifest: 88 APIs
- Snippet repair rounds: 0
- Result: 37/88 passed (42.0%); 51/88 failed (58.0%)
- Infrastructure failures: 0
- Failure categories: 27 compile, 24 runtime/correctness
- Authoritative result: `docs/comprehension_A1_original.json`
- Per-API runnable programs: `.aideal_exec/run_<API>/ApiTest.scala`
- Append-only execution history: `logs/error_log.jsonl`
- Detailed per-API failure audit: `docs/A1_FAILURE_DETAILS.md`

Compile failures (27): append, computeForFeatures,
computeForFeaturesWithOutputSize, count, create, envelope,
eulerHistogramCount, hdfFile, numPoints, plotFeatures, rangeQuery,
rasterizePixels, rasterizePoints, reproject, rescale, reshapeAverage,
reshapeNN, retile, run, saveAsGeoJSON, saveAsIndex, saveTiles, size, x1,
x2, y1, y2.

Runtime or correctness failures (24): config, eulerHistogramSize, explode,
filterPixels, getValue, id, isSpatiallyPartitioned, mapPixels, metadata,
overlay, part, pixelType, pixels, plotAllTiles, plotImage, raptorJoin,
readCSVPoint, saveAsCSVPoints, saveAsGeoTiff, saveAsKML,
saveTilesCompact, sierpinski, uniformHistogramSize, using.

The A1 score is the fixed baseline for comparison with A2. Do not replace it
with a rerun or mix it with repaired-snippet results.

## A2 — generated documentation

The all-generated-API run was started on 2026-07-14. Report both its complete
execution-set pass rate and the pass rate restricted to the same frozen 88 APIs.
Only the restricted 88-API result is the direct A1-versus-A2 comparison.
