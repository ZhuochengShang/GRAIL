# Updated Fixed-README Comparison

## Run Table

| condition | model | README condition | pass/raw | raw % | score | score+infra | infra excluded | wall h |
|---|---|---|---:|---:|---:|---:|---:|---:|
| Gemini g1 | Gemini 2.5 Pro | pre-docfix/generated | 90/218 | 41.3% | 0.435 | 0.413 | 11 | 3.64 |
| Gemini on fixed | Gemini 2.5 Pro | Gemini 3.1 fixed README | 101/205 | 49.3% | 0.510 | 0.493 | 7 | 2.95 |
| Codex g1 | Codex 5.3 | Codex fresh README | 106/205 | 51.7% | 0.546 | 0.517 | 11 | 1.07 |
| Codex on fixed | Codex 5.3 | Gemini 3.1 fixed README | 139/205 | 67.8% | 0.713 | 0.678 | 10 | 1.55 |

## Key Deltas

- Gemini 2.5 Pro: **90/218 -> 101/205**, score **0.435 -> 0.510** (**+7.5 score points**).
- Codex 5.3: **106/205 -> 139/205**, score **0.546 -> 0.713** (**+16.7 score points**).
- Gemini 3.1 Pro docfix kept **36** fixed README entries from the g1 failure set.

## Codex 5.3 on Fixed README

- recovered APIs, failed in Codex g1 but passed on fixed README: **42**
- doc-fixed and recovered: **31/36 = 86.1%**
- regressed APIs, passed in Codex g1 but failed on fixed README: **9**
- net pass gain: **+33**

### Codex recovered APIs

`addFeature`, `addTile`, `area`, `computePointHistogramSparse`, `createDateFilter`, `createPartitions`, `createSummaryAccumulator`, `createTileIDFilter`, `crsToSRID`, `end`, `envelope`, `geometryType`, `getBoolean`, `getFeatureReaderClass`, `getPointValue`, `isDefined`, `isEmptyAt`, `lastNFiles`, `mapPixels`, `metadata`, `modelToGrid`, `name`, `numFields`, `numPartitions`, `overlay`, `part`, `partitionFeatures2`, `plotImage`, `pointSample`, `rasterizePixels`, `readConfigurationXML`, `readPartition`, `rescale`, `reshapeAverage`, `reshapeNN`, `retile`, `selectFiles`, `splitGeometryAcrossDateLine`, `uniformHistogramSize`, `using`, `value`, `y1`

### Codex doc-fixed and recovered APIs

`addFeature`, `area`, `computePointHistogramSparse`, `createDateFilter`, `createSummaryAccumulator`, `createTileIDFilter`, `crsToSRID`, `end`, `envelope`, `geometryType`, `getBoolean`, `getPointValue`, `isDefined`, `isEmptyAt`, `mapPixels`, `metadata`, `modelToGrid`, `numFields`, `numPartitions`, `overlay`, `part`, `partitionFeatures2`, `pointSample`, `rasterizePixels`, `readConfigurationXML`, `readPartition`, `reshapeAverage`, `retile`, `splitGeometryAcrossDateLine`, `uniformHistogramSize`, `using`

### Codex regressions

`buildIndex`, `computeForFeatures`, `decompressDatasetFiles`, `getTileIDAtPixel`, `pixelType`, `saveAsShapefile`, `seek`, `sierpinski`, `x1`

## Gemini 2.5 on Fixed README

- recovered APIs, failed in Gemini g1 but passed on fixed README: **36**
- doc-fixed and recovered: **18/36 = 50.0%**
- regressed APIs, passed in Gemini g1 but failed on fixed README: **20**
- net raw pass gain vs Gemini g1: **+11**

## reshapeNN Stress

- Gemini 3.1 Pro Preview `reshapeNN` stress docfix status: **doc-fixed**
- Report: `docs/stress_docfix_reshapeNN_gemini31_r30.json`

## Interpretation

- The fixed README clearly helps Codex: same Codex 5.3 audience improves from 106 to 139 passes.
- Gemini 2.5 also improves relative to its own g1, but remains below Codex on the same fixed README.
- The strongest evidence is same-model before/after: Codex +33 net passes; Gemini +11 raw passes despite denominator changes.
