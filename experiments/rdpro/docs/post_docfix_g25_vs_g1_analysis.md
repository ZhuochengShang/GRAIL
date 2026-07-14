# Post-docfix Gemini 2.5 Pro vs Codex g1 Baseline

## HEADLINE — fair, within-model, doc-only comparison (read this first)

The clean test holds the AUDIENCE model fixed (Gemini 2.5 Pro) and changes ONLY
the README it reads. Source-aware repair (Gemini 3.1 Pro) improved it:

| Gemini 2.5 Pro audience | README it read | raw | scored |
|---|---|---|---|
| g1 (pre-docfix) | its own fresh README | 90/218 = 41.3% | 90/207 = **43.5%** |
| post-docfix | Gemini-3.1-repaired README | 101/205 = 49.3% | 101/198 = **51.0%** |
| **delta** | | **+8.0 pp** | **+7.5 pp** |

Transfer: **25/36 = 69.4%** of the sections Gemini 3.1 Pro source-fixed later
passed under Gemini 2.5 Pro. This is the defensible claim.

CAVEAT — the cross-model comparison below (post-docfix Gemini 2.5 vs Codex g1)
is NOT the doc-only test: it changes the audience model AND the README at once,
so its -2.4 pp confounds doc-repair with a model swap. Use it only as context,
never as the headline. (Minor: the pre-docfix Gemini run executed 218 APIs on
the pre-dedup surface vs 205 post-dedup; the SCORED fraction 43.5%->51.0%
normalizes for that count shift, so it is the cleaner of the two deltas.)

## Files

- g1 baseline: `results/bench/20260707_125142_g1_codex_flat.gpt-5.3-codex.json`
- docfix report: `docs/docfix_gemini_3_1_pro_from_g1.json`
- post-docfix run: `docs/comprehension_run.post_docfix_g25.json`

## Overall

- g1 baseline: **106/205 = 51.7%**
- post-docfix Gemini 2.5 Pro: **101/205 = 49.3%**
- score field: g1 **0.546**, post **0.510**
- score_with_infra: g1 **0.517**, post **0.493**
- pass-count delta: **-5**
- pass-rate delta: **-2.4 pp**
- post run wall time: **2.95 h**
- post run tokens: **in=1,073,012, out=904,790, calls=463**

## Gemini 3.1 Pro README Docfix

- attempted from g1 failures: **99**
- doc-fixed entries kept: **36**
- not-testable: **32**
- rewrite-rejected: **8**
- still-failing/reverted during docfix: **23**

## Did Fixed README Help?

- failed in g1 -> passed after fixed README: **30**
- doc-fixed AND recovered: **25**
- doc-fixed but still failed after: **11**
- previously passed but failed after: **35**
- docfix transfer success over fixed entries: **25/36 = 69.4%**
- total recovery over g1 failures: **30/99 = 30.3%**

Recovered APIs by docfix outcome:
- doc-fixed: 25
- docfix-still-failing: 3
- rewrite-rejected: 1
- not-testable: 1

## Recovered: failed in g1, passed after fixed README (30)

`area`, `computePointHistogramSparse`, `createPartitions`, `createSummaryAccumulator`, `createTileIDFilter`, `crsToSRID`, `end`, `envelope`, `geometryType`, `getBoolean`, `getFeatureReaderClass`, `isDefined`, `isEmptyAt`, `lastNFiles`, `mapPixels`, `metadata`, `modelToGrid`, `numFields`, `numPartitions`, `numPoints`, `overlay`, `part`, `partitionFeatures2`, `readConfigurationXML`, `readPartition`, `rescale`, `reshapeAverage`, `retile`, `splitGeometryAcrossDateLine`, `uniformHistogramSize`

## Strongest evidence: doc-fixed and recovered (25)

`area`, `computePointHistogramSparse`, `createSummaryAccumulator`, `createTileIDFilter`, `crsToSRID`, `end`, `envelope`, `geometryType`, `getBoolean`, `isDefined`, `isEmptyAt`, `mapPixels`, `metadata`, `modelToGrid`, `numFields`, `numPartitions`, `overlay`, `part`, `partitionFeatures2`, `readConfigurationXML`, `readPartition`, `reshapeAverage`, `retile`, `splitGeometryAcrossDateLine`, `uniformHistogramSize`

## Doc-fixed but still failed (11)

`addFeature`, `createDateFilter`, `flatten`, `getPointValue`, `listFilesInZip`, `pixels`, `pointSample`, `raptorJoin`, `rasterizePixels`, `readTile`, `using`

## Still not helped: g1 failed, not doc-fixed, still failed (58)

`addTile`, `build`, `checkOptions`, `compress`, `copyResource`, `createRingsForOccupiedPixels`, `decodeSpatialParquet`, `decompress`, `divideScene`, `encodeGeoParquet`, `encodeSpatialParquet`, `extractTables`, `findIntersections`, `getOperationParams`, `getPartition`, `getTileIDAtPoint`, `getTitle`, `getValue`, `hdfFile`, `initialized`, `isCW`, `locateResource`, `name`, `numNonEmptyGeometries`, `plotAllTiles`, `plotImage`, `plotSingleTileParallel`, `printOperationUsage`, `process`, `rangeQuery`, `rasterizeGeometry`, `readCSVPoint`, `readFile`, `readTextResource`, `readWKTFile`, `reproject`, `reshapeNN`, `runDuplicateAvoidance`, `saveAsCSVPoints`, `saveAsIndex`, `saveIndex2`, `saveTilesCompact`, `selectFiles`, `setPixelValue`, `simplifyGeometry`, `skipDuplicateAvoidance`, `slidingWindow`, `sparkContext`, `sparkSession`, `spatialJoinDJ`, `spatialJoinIntersectsPlaneSweepFeatures`, `spatialJoinRepJ`, `trimLineSegment`, `uniform`, `value`, `y1`, `zonalStats2`, `zonalStatsLocal`

## Regressed: g1 passed, post failed (35)

`call`, `compute`, `computeForFeaturesWithOutputSize`, `decompressDatasetFiles`, `eulerHistogramCount`, `explode`, `filterPixels`, `findTransformationInfo`, `getAttributeName`, `getTileIDAtPixel`, `gridToModel`, `makeBoxes`, `mbr`, `mergeZip`, `numTiles`, `pixelType`, `plot`, `rasterHeight`, `rasterWidth`, `run`, `saveAsGeoTiff`, `saveAsWKTFile`, `saveTiles`, `seek`, `setup`, `sierpinski`, `size`, `sumSideLength`, `summarizeData`, `summary`, `tileIDs`, `uniformHistogramCount`, `visualize`, `x1`, `x2`

## Not-testable in docfix but passed in post run (1)

`lastNFiles`

## Rewrite-rejected in docfix but passed in post run (1)

`getFeatureReaderClass`

## Still-failing during docfix but passed in post run (3)

`createPartitions`, `numPoints`, `rescale`

## Failure Categories

| category | g1 failures | post failures | delta |
|---|---:|---:|---:|
| compile | 62 | 78 | +16 |
| infra | 11 | 7 | -4 |
| runtime | 25 | 19 | -6 |
| timeout | 1 | 0 | -1 |

## Fixed But Still Failed: Error Categories

| API | post category | attempts | source |
|---|---|---:|---|
| `addFeature` | compile | 4 | beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/IntermediateVectorTile.scala:82 |
| `createDateFilter` | runtime | 4 | beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/HDF4Reader.scala:299 |
| `flatten` | compile | 4 | beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsGlobal.scala:69 |
| `getPointValue` | runtime | 4 | beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/ITile.scala:93 |
| `listFilesInZip` | runtime | 5 | beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/util/ZipUtil.scala:478 |
| `pixels` | compile | 4 | beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/ITile.scala:84 |
| `pointSample` | compile | 4 | beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/synopses/PointSampler.scala:47 |
| `raptorJoin` | compile | 4 | beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RaptorMixin.scala:87 |
| `rasterizePixels` | compile | 4 | beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RaptorMixin.scala:58 |
| `readTile` | runtime | 4 | beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/IRasterReader.scala:60 |
| `using` | compile | 4 | beast/commontest/src/main/scala/org/apache/spark/test/ScalaSparkTest.scala:475 |


## DEEP FINDING — how the LLM reads the codebase (reachability, not vocabulary)

The pass/fail pattern after repair is effectively a REACHABILITY classifier.
Four behaviors, each grounded in the 99-failure accounting above:

1. Reasons about reachability, not domain words. The 25 recovered are all
   reachable+exercisable APIs whose DOCS were wrong (receiver / entry-point /
   import). The 69 unhelped are dominated by UNREACHABLE APIs: 31 protected/
   private + 20 non-compiling. Confirms the genericity result — the gap is
   visibility, not domain vocabulary.

2. Separates a doc-bug from a structural barrier. 32 not-testable verdicts
   quote access control verbatim ("compress is protected[raptor], cannot be
   invoked from an external harness outside the raptor package") and DECLINE to
   fabricate a call path — the behavior that keeps the catalog non-worse.

3. Still pattern-completes FAKE members. 7 rewrites invented a plausible-but-
   nonexistent member (toGeometry, getRasterExtent, samplePoints), all caught
   by the fabricated-member guard. The LLM's "understanding" is plausible
   completion that REQUIRES source-grounding + a guard to be trusted.

4. Source + cross-language type context is the enabler. Given the real source
   window + type defs located across the whole repo (incl JAVA types invisible
   to Scala import mining — the "not found: type Collector" case) diagnosis
   becomes correct; without it the LLM redirects to cousin APIs (.convolve,
   .build). It nails the static API but cannot fix runtime/fixture defects via
   docs (the 11 doc-fixed-but-still-fail cases).

One line: source-grounded doc-repair turns plausible-completion into verified
fixes, and the LLM's refusals map the true API ceiling.

## SECOND-READER CHECK — Codex 5.3 on the repaired catalog (cleanest doc-only test)

Run: `docs/comprehension_codex53_on_gemini31_fixed_readme.json`
(audience=fixer=codex:gpt-5.3-codex, --max-fix-rounds 3, --timeout 300).

The SAME model (Codex 5.3) that authored the original catalog re-reads the
Gemini-3.1-repaired one — only the catalog changed, so the delta is 100% the
doc-repair (no model swap):

| Codex 5.3 audience reads | raw | scored |
|---|---|---|
| own PRE-docfix catalog (g1) | 106/205 = 51.7% | 106/194 = 54.6% |
| Gemini-3.1 REPAIRED catalog | 139/205 = 67.8% | 139/195 = **71.3%** |
| **delta** | **+16.1 pp** | **+16.7 pp** |

Transition vs Codex g1: fail->pass 42, pass->fail 9, net **+33**. Of the 36
entries the LLM doc-fixed, **31 (86.1%) now pass under Codex** — higher transfer
than Gemini 2.5's 25/36 (69%), and far cleaner (9 regressions vs the 35 in the
cross-model Gemini comparison).

Cross-reader robustness of the 36 fixes: **25 pass under BOTH** Codex & Gemini
2.5, 6 Codex-only, **0 Gemini-only**, 5 neither. Zero gemini-only ⇒ the repairs
are not reader-specific — they encode source truth any strong reader benefits
from. The 6 Codex-only (addFeature, createDateFilter, getPointValue, pointSample,
rasterizePixels, using) were "doc-fixed-but-failed" under Gemini 2.5: the doc was
correct, Codex is just a stronger coder for them. Only 5 stay runtime/fixture-
blocked under both (flatten, listFilesInZip, pixels, raptorJoin, readTile).

Bottom line: two independent readers improve on the repaired catalog (Gemini
+7.5 pp, Codex +16.7 pp). The within-model deltas are the doc-repair effect;
the cross-model -2.4 pp was an artifact of swapping the reader.
