# Generic vs customized APIs — who does the LLM actually understand?

Buckets are AUTOMATIC: 60% weight = fraction of signature types defined in this
codebase; 40% = name tokens outside general programming vocabulary. No hand labels.

Surface mix: {'mixed': 95, 'domain-specific': 58, 'generic': 52}

## 20260707_125142_g1_codex_flat.gpt-5.3-codex.json  (audience: codex:gpt-5.3-codex)

| bucket | pass | fail | pass rate | dominant failure |
|---|---|---|---|---|
| generic | 27 | 25 | 52% | compile |
| mixed | 52 | 43 | 55% | compile |
| domain-specific | 27 | 31 | 47% | compile |

- generic PASS examples: available, bit, buildIndex, count, decompressDatasetFiles, gaussian
- generic FAIL examples: build, compress, copyResource, createDateFilter, createTileIDFilter, decompress

- domain-specific PASS examples: append, call, config, distribution, eulerHistogramSize, generateSpatialData
- domain-specific FAIL examples: addFeature, addTile, createPartitions, createSummaryAccumulator, divideScene, envelope

## comprehension_run.json  (audience: google:gemini-2.5-pro)

| bucket | pass | fail | pass rate | dominant failure |
|---|---|---|---|---|
| generic | 18 | 34 | 35% | compile |
| mixed | 40 | 55 | 42% | compile |
| domain-specific | 19 | 39 | 33% | compile |

- generic PASS examples: bit, buildIndex, count, createTileIDFilter, gaussian, generate
- generic FAIL examples: available, build, compress, copyResource, createDateFilter, decompress

- domain-specific PASS examples: append, createSummaryAccumulator, distribution, generateSpatialData, geoTiff, metadata
- domain-specific FAIL examples: addFeature, addTile, call, config, createPartitions, divideScene

## Takeaway (against the naive hypothesis)

The generic→domain pass-rate gap is SMALL (codex 52%→47%, gemini 35%→33%).
Name familiarity is NOT the failure driver. The deceptive class is
**generic-NAMED APIs with domain-typed receivers**: `compress`/`decompress`
read like vocabulary words but are `protected[raptor]` methods on
`MemoryTile` — every model fails them; `available`, `build`, `copyResource`
fail the same way. Meanwhile truly domain-named APIs with clean entry points
(`geoTiff`, `generateSpatialData`, `eulerHistogramSize`) pass. What the LLM
lacks is not vocabulary — it is RECEIVER/VISIBILITY knowledge: how to obtain
the right object and whether the method is even callable from outside. That
is exactly the information the doc-repair loop injects, and why compile
(wrong receiver/member) dominates every bucket's failures.

## Evidence tables (codex g1 run; visibility read from beast source; errors verbatim from logs)

### Cell 1 — GENERIC name, FAIL: the deceptive class. Mechanism = unreachable receiver/visibility
| API | real definition | why it fails |
|---|---|---|
| `compress` | `protected[raptor] def compress: Unit` — MemoryTile.scala:211 | model calls it on `ITile[Float]` → "value compress is not a member of ITile[Float]"; even the right receiver would be blocked by `protected[raptor]` |
| `decompress` | `protected def decompress: Unit` — MemoryTile.scala:231 | same trap; snippet even tried tuple access `._2` on the tile |
| `copyResource` | instance method on `ScalaSparkTest` (a TEST helper shipped in main) — ScalaSparkTest.scala:251 | model wrote `this.copyResource` inside the harness object → "not a member of object GeoJob" |
| `build` | `def build(): VectorTile.Tile.Layer` — VectorLayerBuilder.scala:133 (public!) | dies on infra: protobuf classes missing from classpath — environment, not comprehension |

### Cell 2 — GENERIC name, PASS: plain public members
`count` (GeoTiffWriter, public), `gaussian` (SpatialGeneratorBuilder, public builder chain).
Caveat: `buildIndex` passed although its canonical def is `private` — the witness was satisfied
via another path; single-name attribution has limits.

### Cell 3 — DOMAIN name, FAIL: two distinct mechanisms
| API | real definition | why it fails |
|---|---|---|
| `addTile` | `private[raptor] def addTile[U](tile: ITile[U])` — ConvolutionTile.scala:52 | compiler: "cannot be accessed in ConvolutionTileSingleBand" — genuinely not callable from outside; correct verdict is NOT-TESTABLE, not a doc bug |
| `envelope` | `def envelope: Envelope` — RasterMetadata.scala:170 (public) | model invented `.rasterFeature` on RasterRDD instead of the real hop rdd → metadata → envelope: a RECEIVER-PATH failure |
| `zonalStats2`, `divideScene` | public, correct-looking calls | compile fine, die at Spark RUNTIME (stage failures) — fixture/pixel-type semantics, not API misunderstanding |

### Cell 4 — DOMAIN name, PASS: the mixin pattern
`geoTiff` (`RaptorMixin.scala:40`, public, defaults), `generateSpatialData`
(`ReadWriteMixin.scala:139`), `eulerHistogramSize` (`CGOperationsMixin.scala:109`) — all
PUBLIC MIXIN methods reachable directly from the harness bindings (`sc.`, `rdd.`) with
default parameters. Domainness of the name is irrelevant when the entry point is one hop away.
Counter-example: `raptorJoin` FAILED under codex at RUNTIME — `ClassCastException: [F cannot
be cast to java.lang.Float` (the float-array/pixel-type trap) — while passing under gemini:
even the flagship API is unstable across models on runtime type semantics.

### Refined thesis (with receipts)
Pass/fail is governed by (1) REACHABILITY — is the method public and one hop from a harness
binding (mixins pass; `private[pkg]`/`protected`/test-helper receivers fail regardless of how
generic the name sounds) — and (2) RUNTIME TYPE SEMANTICS (pixel types, partitioning
preconditions). Name genericity contributes almost nothing (52%→47% codex). The LLM's gap in
"understanding the customized codebase" is concentrated in HOW TO REACH functionality and
WHAT THE DATA MUST LOOK LIKE — both fixable in docs, which is what the doc-repair loop does.
