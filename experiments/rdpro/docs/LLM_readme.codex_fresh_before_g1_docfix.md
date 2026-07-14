# RDPro — LLM_readme

LLM-facing API documentation. Generated from the API surface, project profile, and distilled docs.

## API Test: `add`

### Signature
```scala
override def add(f: IFeature): Unit
override def add(v: PointND): Unit
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/synopses/SummaryAccumulator.scala:54  (+1 more definition site/overload)_

### Goal
Add one spatial item (feature or point) into a `SummaryAccumulator` so the accumulator can build an aggregate spatial summary over a dataset.

### Parameters
- `f` (`IFeature`): one input feature to include in the running summary (for the `add(f: IFeature)` overload).

### Input
Caller must provide a `SummaryAccumulator` instance and pass either:
- an `IFeature` via `add(f: IFeature)`, or
- a `PointND` via `add(v: PointND)`.

In documented usage, `IFeature` values come from loaded vector datasets (for example via `sparkContext.shapefile(...)`), then are added inside a transformation before an action triggers execution.

### Output
Returns `Unit` — the call mutates accumulator state (side effect) and does not return a per-call value. The accumulated result is retrieved later using `accumulator.value`.

### Valid Call Patterns
```scala
var features = sparkContext.shapefile("input.zip")
val accumulator = Summary.createSummaryAccumulator(sparkContext)
features = polygons.map(f=> {accumulator.add(f); f})
// ... run an action on features
val summary = accumulator.value
```

### LLM Instruction Prompt
- Use the receiver-qualified form exactly as documented: `accumulator.add(f)`.
- Pass exactly one argument, matching one overload: `IFeature` or `PointND`.
- Do not expect a return value from `add`; read final aggregate via `accumulator.value`.
- Ensure an action is executed on the transformed dataset; otherwise accumulator updates may not run.

### Prompt Snippet
```text
Create a SummaryAccumulator, call accumulator.add(f) inside a map over IFeature records, then trigger an action and read accumulator.value. Do not assign add(...) to a variable (it returns Unit).
```

### Common Failure Modes
- Calling `add` without a receiver (e.g., bare `add(f)`), which usually will not compile in user code.
- Passing the wrong type to an overload (non-`IFeature` and non-`PointND`).
- Expecting immediate computed output from `add`; it returns `Unit`.
- Forgetting to run a Spark action after `map`, so accumulator updates are never materialized.

### Fix Code Hint
```scala
val accumulator = Summary.createSummaryAccumulator(sparkContext)
val updated = features.map(f => { accumulator.add(f); f })
updated.count() // trigger execution
val summary = accumulator.value
```

## API Test: `addFeature`

### Signature
```scala
def addFeature(feature: IFeature): IntermediateVectorTile
def addFeature(feature: IFeature): Unit
def addFeature(feature: Row, geometry: LiteGeometry): Unit
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/VectorLayerBuilder.scala:92  (+2 more definition site/overload)_

### Goal
Add one vector feature into the current tile/layer builder so it is encoded in the output vector tile.

### Parameters
- `feature` (`Row`): attribute row to add when using the `(Row, LiteGeometry)` overload; for the `IFeature` overload, the feature object contains geometry + attributes together.
- `geometry` (`LiteGeometry`): geometry paired with the `Row` attributes in the `(Row, LiteGeometry)` overload.

### Input
Caller provides an in-memory feature (or row+geometry pair), not a file path.  
From the authoritative doc: the feature is either added as-is, or rasterized and aggregated, depending on the internal state of the tile.  
Verified usage in tests uses `VectorLayerBuilder` as receiver and `Feature.create(...)` to build an `IFeature`.

### Output
Returns `Unit` — for the shown test-backed call form on `VectorLayerBuilder`, this means the builder is mutated by appending the feature.  
For the documented overload `def addFeature(feature: IFeature): IntermediateVectorTile`, the returned value represents the same tile object to support chaining.

### Valid Call Patterns
```scala
val factory = FeatureReader.DefaultGeometryFactory
val builder = new VectorLayerBuilder(100, "test")
builder.addFeature(Feature.create(factory.createPoint(new CoordinateXY(50, 50)), Array("id", "name"),
  null, Array(10, "pt")))
```

```scala
val factory = FeatureReader.DefaultGeometryFactory
val builder = new VectorLayerBuilder(100, "test")
builder.addFeature(Feature.create(factory.createPoint(new CoordinateXY(50, 50)), Array("id", "name"),
  null, Array(10, null)))
```

### LLM Instruction Prompt
- Use an instance receiver (for example, `builder.addFeature(...)`), not a bare `addFeature(...)`.
- Pass exactly one `IFeature` for the verified call form, or `(Row, LiteGeometry)` for that overload.
- Do not invent file-based inputs; this API consumes already-created in-memory feature objects.
- Keep geometry and attributes aligned when constructing the feature.

### Prompt Snippet
```text
Create a VectorLayerBuilder, construct an IFeature with Feature.create(...), then call builder.addFeature(feature). Do not use file paths as arguments.
```

### Common Failure Modes
- Calling `addFeature(...)` without a receiver object (won’t resolve).
- Passing the wrong argument shape (e.g., `Row` alone, or geometry alone).
- Assuming a return value when using a `Unit` overload.
- Expecting this call to read shapefiles/GeoJSON directly (it does not; input must already be parsed into feature objects).

### Fix Code Hint
```scala
val factory = FeatureReader.DefaultGeometryFactory
val builder = new VectorLayerBuilder(100, "test")

val f: IFeature =
  Feature.create(factory.createPoint(new CoordinateXY(50, 50)),
    Array("id", "name"), null, Array(10, "pt"))

builder.addFeature(f) // mutate builder, then build later
val layer = builder.build()
```

## API Test: `addGeometry`

### Signature
```scala
def addGeometry(geometry: Geometry, title: String): Boolean
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/VectorCanvas.scala:169_

_Source doc:_ Adds the given geometry to the canvas. This method might simplify, drop, or combine geometries to accommodate the given geometry without getting too big. @param geometry the geometry to add @param title an optional title to attach to the geometry in the SVG file @return `true` if the state of the canvas was modified.

### Goal
Add a JTS geometry to a `VectorCanvas` for visualization, while allowing the canvas to simplify/drop/combine content to stay within size limits.

### Parameters
- `geometry` (`Geometry`): the geometry object to insert into the canvas (e.g., points created from a geometry factory in tests).
- `title` (`String`): optional SVG title/label attached to that geometry; tests pass `null` when no title is needed.

### Input
A caller must provide:
- A `VectorCanvas` instance (receiver in tested usage).
- A valid `Geometry` instance.
- A `String` title (or `null` as shown in tests).

Preconditions/behavior notes from source doc and tests:
- The method is for in-memory canvas geometry ingestion (not file I/O).
- The canvas may simplify, combine, or drop geometries as it gets too big.
- Therefore, adding a geometry does **not** guarantee it will remain as a distinct stored geometry afterward.

### Output
Returns `Boolean` — `true` if adding this geometry modified the canvas state, `false` otherwise.

### Valid Call Patterns
```scala
val canvas = new VectorCanvas(new Envelope(0, 256, 0, 256),
  256, 256, 0, 1)
val factory = GeometryReader.DefaultGeometryFactory
canvas.addGeometry(factory.createPoint(new CoordinateXY(0, 0)), null)
canvas.addGeometry(factory.createPoint(new CoordinateXY(5, 5)), null)
```

### LLM Instruction Prompt
- Call as an instance method on a `VectorCanvas`: `canvas.addGeometry(geometry, title)`.
- Pass a `Geometry` object as first argument and a `String`/`null` title as second argument.
- Do not assume one call equals one retained geometry; the canvas may merge/drop/simplify.
- Check the returned `Boolean` to detect whether state changed.

### Prompt Snippet
```text
Given an existing VectorCanvas `canvas` and a JTS Geometry `g`, call:
`canvas.addGeometry(g, null)` (or provide a title string).
Treat the Boolean return as "canvas changed?" and do not assume geometry count increases by 1.
```

### Common Failure Modes
- Calling `addGeometry` without a `VectorCanvas` receiver (bare call shape) instead of `canvas.addGeometry(...)`.
- Passing non-`Geometry` input as `geometry`.
- Assuming all inserted geometries are preserved individually; in heavy point loads, geometries can be rasterized/dropped (tests show `canvas.geometries.isEmpty` after many inserts).
- Ignoring the Boolean result when downstream logic depends on whether the canvas changed.

### Fix Code Hint
```scala
val canvas = new VectorCanvas(new Envelope(0, 256, 0, 256), 256, 256, 0, 1)
val factory = GeometryReader.DefaultGeometryFactory

val changed1 = canvas.addGeometry(factory.createPoint(new CoordinateXY(0, 0)), null)
val changed2 = canvas.addGeometry(factory.createPoint(new CoordinateXY(1, 1)), "pt-1")

println(s"Canvas changed? ${changed1 || changed2}")
```

## API Test: `addTile`

### Signature
```scala
private[raptor] def addTile[U](tile: ITile[U]): Unit
def addTile(tile: ITile[T]): Unit
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/ConvolutionTile.scala:52  (+2 more definition site/overload)_

_Source doc:_ Adds the given input tile into this partial convolution tile @param tile the tile to compute into this tile

### Goal
Add one raster tile (`ITile`) into an in-progress convolution tile so the convolution result accumulates contributions from that tile.

### Parameters
- `tile` (`ITile[U]`): the input raster tile to be incorporated into the current partial convolution tile.

### Input
`addTile` is an internal Raptor/RDPro tile-level operation (not a file-loading API).  
Caller must provide:

- A constructed convolution-tile receiver (for example `ConvolutionTileSingleBand` or `ConvolutionTileMultiBand`).
- An `ITile[...]` instance compatible with that receiver’s expected pixel type and band structure.

Grounded preconditions from passing tests:

- Single-band path uses `MemoryTile[Float]` with `ConvolutionTileSingleBand`, then `convWindow1.addTile(tile1)`.
- Multi-band path uses `MemoryTile[Array[Float]]` with `ConvolutionTileMultiBand`, then `convWindow1.addTile(tile1)`.
- In tests, tiles and convolution windows are built with matching `RasterMetadata`; keeping metadata compatible is required for correct spatial alignment.

No direct GeoTIFF/HDF path is passed to this method.

### Output
Returns `Unit` — the method mutates/updates the receiver convolution tile state in place; no standalone value is returned.

### Valid Call Patterns
```scala
val convWindow1 = new ConvolutionTileSingleBand(0, metadata, tile1.rasterFeature,1, Array.fill(9)(0.11f), tile1.tileID)
convWindow1.addTile(tile1)
```

```scala
val convWindow1 = new ConvolutionTileMultiBand(0, metadata, RasterFeature.create(Array("fileName"),Array("testFile.tif")), 2, 1, Array.fill(9)(0.11f), tile1.tileID)
convWindow1.addTile(tile1)
```

### LLM Instruction Prompt
- Call `addTile` as an instance method on a convolution tile object (`value.addTile(tile)`), not as a standalone function.
- Pass an `ITile` whose pixel type matches the convolution receiver type (`Float` for single-band test pattern, `Array[Float]` for multi-band test pattern).
- Ensure tile spatial metadata is compatible with the convolution context; mismatched geometry/metadata can make results invalid.
- Do not expect a return value; use subsequent reads (`getPixelValue`, `isDefined`, `isEmpty`) or merge operations to inspect effects.

### Prompt Snippet
```text
Given an existing ConvolutionTileSingleBand or ConvolutionTileMultiBand instance, call addTile using the exact instance form:
convWindow.addTile(tile)
Use a tile type compatible with the receiver (e.g., MemoryTile[Float] for single-band, MemoryTile[Array[Float]] for multi-band). Treat addTile as in-place update (Unit return).
```

### Common Failure Modes
- Passing a tile with incompatible pixel type/band layout relative to the convolution tile implementation.
- Calling `addTile` and expecting a returned raster/result object (it returns `Unit`).
- Using inconsistent raster metadata between source tile and convolution window, leading to wrong alignment/values.
- Attempting to use this as a public end-user file I/O API; it is `private[raptor]` in the authoritative signature.

### Fix Code Hint
```scala
// Single-band compatible pattern
val tile1 = new MemoryTile[Float](0, metadata, RasterFeature.create(Array("fileName"), Array("testFile.tif")))
val convWindow1 = new ConvolutionTileSingleBand(0, metadata, tile1.rasterFeature, 1, Array.fill(9)(0.11f), tile1.tileID)
convWindow1.addTile(tile1) // in-place update; returns Unit
```

## API Test: `affineTransform`

### Signature
```scala
def affineTransform(matrix: AffineTransform): SpatialGeneratorBuilder
def affineTransform(geometry: Geometry): Geometry
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/generator/SpatialGeneratorBuilder.scala:85  (+1 more definition site/overload)_

_Source doc:_ Sets the affine transformation for the generated data. @param matrix the affine transformation matrix @return

### Goal
Apply an affine transformation either to a spatial data generator configuration (`AffineTransform` overload) or directly to a single `Geometry` (`Geometry` overload).

### Parameters
- `matrix` (`AffineTransform`): the affine transformation matrix to set on the spatial generator builder (e.g., scale/translate as configured on `java.awt.geom.AffineTransform`).

### Input
For the documented README call form, you provide:
- a `SpatialGeneratorBuilder` receiver (`sparkContext.generateSpatialData`)
- an `AffineTransform` instance passed to `.affineTransform(transform)`

For the other overload (from API facts), input is:
- `geometry: Geometry` to transform using the generator’s configured affine transformation.

No file format input is required by this method itself.  
No additional preconditions are explicitly documented for this API in the provided sources.

### Output
Returns `SpatialGeneratorBuilder` — the same builder chain with affine transformation configured, so you can continue generator calls such as `.uniform(...)`.

(Overload behavior from API facts: `affineTransform(geometry: Geometry)` returns a transformed `Geometry`.)

### Valid Call Patterns
```scala
val transform = new AffineTransform()
transform.scale(2.0, 1.0)
transform.translate(0.0, 3.0)
println(sparkContext.generateSpatialData
  .affineTransform(transform)
  .uniform(1000)
  .summary)
```

### LLM Instruction Prompt
- Use the instance call form exactly as documented: `sparkContext.generateSpatialData.affineTransform(transform)`.
- Pass an `AffineTransform` object to the builder overload.
- Do not invent extra parameters.
- If you need geometry-to-geometry transformation, use the separate overload `affineTransform(geometry: Geometry): Geometry` as listed in API facts.

### Prompt Snippet
```text
Create an AffineTransform, configure it (e.g., scale/translate), then call:
sparkContext.generateSpatialData.affineTransform(transform)
and continue builder chaining (such as .uniform(1000)).
Do not add unsupported arguments.
```

### Common Failure Modes
- Calling `affineTransform` with the wrong argument type (neither `AffineTransform` nor `Geometry`).
- Using a non-builder receiver for the `AffineTransform` overload (the documented form is on `sparkContext.generateSpatialData`).
- Assuming undocumented behavior (e.g., CRS conversion or raster metadata alignment); none is specified for this method in the provided API facts.

### Fix Code Hint
```scala
import java.awt.geom.AffineTransform

val transform = new AffineTransform()
transform.scale(2.0, 1.0)
transform.translate(0.0, 3.0)

val builder = sparkContext.generateSpatialData.affineTransform(transform)
// continue, e.g.
val summary = builder.uniform(1000).summary
println(summary)
```

## API Test: `append`

### Signature
```scala
def append(feature: IFeature, value: Any, name: String = null, dataType: DataType = null): IFeature
def append(rasterFeature: RasterFeature, name: String, value: Any): RasterFeature
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/Feature.scala:405  (+1 more definition site/overload)_

_Source doc:_ Appends an additional attribute to the given feature and returns a new feature @param feature the feature to append to. This feature is not modified. @param value the value to append. @param name (Optional) the name of the new attribute @param dataType (Optional) the type of the additional attribute. @return a new feature that contains the geometry and all attributes of the input feature + the new attribute.

### Goal
Add one new attribute (column) to an existing Beast feature record (`IFeature`)—commonly after joins/IDs in Spark geospatial workflows—without mutating the original feature.

### Parameters
- `feature` (`IFeature`): The input feature to extend (geometry + existing attributes). This input feature is not modified.
- `value` (`Any`): The value to store in the new appended attribute.
- `name` (`String`), default `null`: Optional name for the new attribute.
- `dataType` (`DataType`), default `null`: Optional Spark SQL type for the appended attribute.

### Input
- You must already have an `IFeature` in memory (e.g., from a spatial join, generated data, or mapped feature RDD).  
- `append` is not a file loader/writer; no direct file-format argument is used here.
- In distributed Spark usage, this is typically called inside `RDD.map`, e.g., after `zipWithUniqueId` or join output mapping.
- From provided docs/tests, no extra CRS/raster compatibility precondition is specific to `append`; it works at feature-schema level.

### Output
Returns `IFeature` — a **new** feature containing:
1. the same geometry as the input feature,  
2. all original attributes, and  
3. one additional appended attribute (from `value`, optionally named/typed).

### Valid Call Patterns
```scala
val addRecordID: ((IFeature, Long)) => IFeature = fid => Feature.append(fid._1, fid._2, "ID")
```

```Scala
val finalResults: RDD[IFeature] = sjResults.map(pip => {
  val polygon: IFeature = pip._1
  val point: IFeature = pip._2
  Feature.append(point, polygon.getAs[String]("NAME"), "state")
})
```

### LLM Instruction Prompt
- Use the receiver exactly as documented: `Feature.append(...)`.
- Keep argument order exactly: `(feature, value, name, dataType)` for the `IFeature` overload.
- Do not mutate input features; assign/use the returned `IFeature`.
- Only use values already available in the pipeline (e.g., IDs from `zipWithUniqueId`, attributes from joined features).
- If you do not need explicit typing, omit `dataType` and use the 3-argument form shown in tests/README.

### Prompt Snippet
```text
Given an IFeature `f`, append one attribute using Beast as:
`Feature.append(f, newValue, "new_col")`.
Use this inside Spark RDD.map and keep the returned IFeature.
Do not change receiver or parameter order.
```

### Common Failure Modes
- Calling `append(...)` without `Feature.` qualifier in contexts where no implicit import provides it.
- Ignoring the returned value (input feature is not modified).
- Swapping argument order (e.g., passing name/value in wrong positions).
- Assuming this API writes data to disk; it only returns transformed in-memory features.
- Using a call shape not shown in project usage when generating code (must follow `Feature.append(feature, value, name)` pattern).

### Fix Code Hint
```scala
// Correct pattern: keep Feature qualifier, correct argument order, and capture the return value
val withID: SpatialRDD = input.zipWithUniqueId().map { fid =>
  Feature.append(fid._1, fid._2, "ID")
}
```

## API Test: `area`

### Signature
```scala
def area: Double
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/LiteGeometry.scala:115_

### Goal
Compute the area of a geometry value as a `Double` in Beast/RDPro geospatial workflows.

### Parameters
_None._

### Input
Call `area` on an existing geometry instance (instance method form).  
No file path or format is passed directly to this method.

Preconditions from available facts:
- The call shape is inferred from the signature (`def area: Double`) because no README or test snippet in the provided material shows a direct `area` invocation.
- No CRS/unit semantics are explicitly documented in the provided sources for this method, so unit interpretation is not specified here.

### Output
Returns `Double` — the computed area numeric value for the receiver geometry.

### Valid Call Patterns
```scala
val a: Double = geometry.area
```

### LLM Instruction Prompt
- Use instance-call form: `value.area` (no arguments).
- Ensure the receiver is a geometry object that defines `area`.
- Do not add parameters; signature is exactly `def area: Double`.
- If CRS/units are required by the task, state they are not specified in the provided API facts and must be validated in surrounding pipeline code.

### Prompt Snippet
```text
Given a geometry instance `g`, call `g.area` and store the result as Double.
Do not pass arguments to `area`.
If area units are needed, note that units are not documented in the provided API facts.
```

### Common Failure Modes
- Calling `area()` with arguments or extra options (not supported by signature).
- Calling `area` on a non-geometry receiver.
- Assuming specific units (e.g., square meters) without documented CRS/unit guarantees for this method.

### Fix Code Hint
```scala
// Correct: instance call, no arguments
val areaValue: Double = geometry.area
```

## API Test: `available`

### Signature
```scala
override def available(): Int
```
_Source: beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/util/BufferedFSDataInputStream.scala:99  (+1 more definition site/overload)_

### Goal
Report how many bytes can be read immediately from a `BufferedFSDataInputStream` without blocking, for low-level stream handling in Beast/RDPro file I/O pipelines.

### Parameters
_None._

### Input
Call this method on an existing `BufferedFSDataInputStream` instance (for example, `bufStream`) that wraps an open Hadoop `FSDataInputStream`, as in the tested call style for sibling methods on the same class.

Preconditions:
- The stream instance must already be created and open.
- This is a byte-stream API (not a raster operation like `sc.geoTiff[T]`), so raster type-selection rules (e.g., `Int` vs `Float` pixels) do not apply directly here.
- No GeoTIFF/HDF format-specific argument is passed to `available`; any format handling happens earlier when opening the stream.

### Output
Returns `Int` — the number of bytes currently available for immediate read from the stream without blocking.

### Valid Call Patterns
```scala
// Inferred from signature (no direct available() usage shown in tests/README),
// using the same receiver style as tested sibling calls on BufferedFSDataInputStream.
val n: Int = bufStream.available()
```

### LLM Instruction Prompt
- Call as an instance method on `BufferedFSDataInputStream` (e.g., `bufStream.available()`), not as a standalone function.
- Do not add parameters; signature is exactly `available(): Int`.
- Ensure the stream is open before calling.
- Treat result as an immediate-availability byte count, not total file length.

### Prompt Snippet
```text
Given an open BufferedFSDataInputStream named bufStream, call:
val n: Int = bufStream.available()
Do not pass arguments. Use n only as currently readable byte count.
```

### Common Failure Modes
- Calling `available` on a closed/uninitialized stream.
- Assuming the returned `Int` is the full remaining file size.
- Using a different call shape (e.g., static/global `available()`), which does not match the instance API.

### Fix Code Hint
```scala
// Ensure stream exists and is open, then call instance method with no args
val bufSize = 16 * 1024
val bufStream = new BufferedFSDataInputStream(fileSystem.open(filePath), bufSize)

val availableNow: Int = bufStream.available()
```

## API Test: `bit`

### Signature
```scala
def bit(cardinality: Long, digits: Int = 10, probability: Double = 0.2): JavaSpatialRDD
def bit(cardinality: Long, digits: Int = 10, probability: Double = 0.2): SpatialRDD
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/generator/JavaSpatialGeneratorBuilder.scala:139  (+1 more definition site/overload)_

_Source doc:_ Generate data from the bit distribution @param cardinality the number of records to generate @param digits the number of digits to set per coordinate @param probability the probability of setting each bit @return the RDD that contains the generated data

### Goal
Generate synthetic spatial data in Spark using a bit distribution, with control over record count and per-bit activation behavior.

### Parameters
- `cardinality` (`Long`): the number of records to generate.
- `digits` (`Int`), default `10`: the number of digits to set per coordinate.
- `probability` (`Double`), default `0.2`: the probability of setting each bit.

### Input
`bit` does not read raster/vector files directly.  
You call it from a spatial data generator receiver (documented usage: `sc.generateSpatialData`) in a Spark context.  
A practical precondition from sibling tested patterns is to configure the generator first (for example, an MBR via `.mbr(...)`) when you need output constrained to a known spatial extent.

### Output
Returns `JavaSpatialRDD` — an RDD-based spatial dataset containing the generated records from the bit distribution.  
(Scala overload returns `SpatialRDD` with the same arguments.)

### Valid Call Patterns
```scala
sc.generateSpatialData
  .bit(1000, digits = 10, probability = 0.2)
  .plotImage(300, 300, "bit.png",
    opts = Seq(GeometricPlotter.PointSize -> 0))
```

### LLM Instruction Prompt
- Use the receiver-qualified call form exactly (`sc.generateSpatialData.bit(...)`), not a bare `bit(...)`.
- Pass arguments in the documented order: `cardinality`, `digits`, `probability`.
- Use only the documented parameters and defaults; do not invent extra options.
- Return/chain the result as a spatial RDD pipeline step (e.g., plotting or further spatial ops).

### Prompt Snippet
```text
Using RDPro/Beast Scala API, generate synthetic spatial data with bit distribution from `sc.generateSpatialData`.
Call:
`bit(cardinality: Long, digits: Int = 10, probability: Double = 0.2)`
Use only these parameters. Keep the receiver-qualified form exactly.
```

### Common Failure Modes
- Calling `bit(...)` without a generator receiver, which typically will not compile.
- Supplying unsupported/unknown named arguments (only `cardinality`, `digits`, `probability` are defined).
- Assuming it reads GeoTIFF/HDF/GeoJSON inputs; this API is a generator, not a file loader.
- Expecting raster-specific typed-loading rules (`sc.geoTiff[T]`) to apply here; they are unrelated to this API.

### Fix Code Hint
```scala
val generated = sc.generateSpatialData
  .bit(cardinality = 1000L, digits = 10, probability = 0.2)
```

## API Test: `build`

### Signature
```scala
def build(): VectorTile.Tile.Layer
override def build(): Scan
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/VectorLayerBuilder.scala:133  (+4 more definition site/overload)_

_Source doc:_ Finalize the layer and return it @return

### Goal
Finalize a `VectorLayerBuilder` after features were added and return the produced Mapbox Vector Tile layer object for downstream visualization/inspection.

### Parameters
_None._

### Input
A prepared `VectorLayerBuilder` instance (for example, `new VectorLayerBuilder(100, "test")`) that has already received vector features via `addFeature(...)`.

Preconditions from verified usage:
- Call form is instance-based: `builder.build()`.
- `build()` is used after one or more `addFeature(...)` calls.
- Attributes may include `null`; tested behavior shows null attributes can be skipped while still producing a valid layer.

No file path or raster input is required by this method itself.

### Output
Returns `VectorTile.Tile.Layer` — a finalized in-memory vector-tile layer containing the encoded features/keys/values accumulated in the builder.

### Valid Call Patterns
```scala
val factory = FeatureReader.DefaultGeometryFactory
val builder = new VectorLayerBuilder(100, "test")
builder.addFeature(Feature.create(factory.createPoint(new CoordinateXY(50, 50)), Array("id", "name"),
  null, Array(10, "pt")))
val layer = builder.build()
```

```scala
val factory = FeatureReader.DefaultGeometryFactory
val builder = new VectorLayerBuilder(100, "test")
builder.addFeature(Feature.create(factory.createPoint(new CoordinateXY(50, 50)), Array("id", "name"),
  null, Array(10, null)))
val layer = builder.build()
```

### LLM Instruction Prompt
- Use the instance call exactly as validated: `builder.build()`.
- Ensure `builder` is a `VectorLayerBuilder` that has had features added before finalizing.
- Do not invent parameters; `build` takes none.
- Treat the return as `VectorTile.Tile.Layer` (not a raster type, not CSV/GeoTIFF).

### Prompt Snippet
```text
Given a VectorLayerBuilder named builder that already received features via addFeature, finalize it with:
val layer = builder.build()
Use no arguments, and treat layer as VectorTile.Tile.Layer.
```

### Common Failure Modes
- Calling `build` with arguments (invalid; signature is empty parameter list).
- Calling `build` on the wrong receiver type (must be a `VectorLayerBuilder` in this API usage).
- Expecting raster output formats (GeoTIFF/CSV) from this method; it returns a vector-tile layer object.
- Building before adding any meaningful features may produce an empty/minimal layer (exact empty-layer behavior is not specified here).

### Fix Code Hint
```scala
val factory = FeatureReader.DefaultGeometryFactory
val builder = new VectorLayerBuilder(100, "test")

// Add at least one feature before finalizing
builder.addFeature(
  Feature.create(factory.createPoint(new CoordinateXY(50, 50)),
    Array("id", "name"), null, Array(10, "pt"))
)

// Correct: no-arg instance call
val layer: VectorTile.Tile.Layer = builder.build()
```

## API Test: `buildIndex`

### Signature
```scala
def buildIndex(sparkContext: SparkContext, dir: String, indexFile: String): Unit
private def buildIndex(sparkContext: SparkContext, fs: FileSystem, basePath: String): Map[String, (Int, String)]
private def buildIndex(fs: FileSystem, basePath: String): Map[String, (Int, String)]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterFileRDD.scala:186  (+2 more definition site/overload)_

_Source doc:_ Build a raster index on all GeoTIFF files in a directory. @param sparkContext spark context to parallelize index creation @param dir the directory that contains raster files @param indexFile the path of the index file to write

### Goal
Build an index file for GeoTIFF rasters in a directory so later raster file selection (e.g., spatial filtering) can be done efficiently.

### Parameters
- `sparkContext` (`SparkContext`): Spark context used to parallelize index creation.
- `dir` (`String`): Directory path that contains raster files (GeoTIFFs) to index.
- `indexFile` (`String`): Output path for the generated index file (in tests, `_index.csv` is used).

### Input
A directory of GeoTIFF files must be provided via `dir`.  
The call form verified by tests uses `RasterFileRDD.buildIndex(sparkContext, dir, indexFile)`.

Preconditions from available facts:
- The directory should exist and contain GeoTIFF files to index.
- A valid `SparkContext` and Hadoop filesystem configuration are expected.
- Paths must be valid for the configured filesystem (local FS/HDFS depends on Spark/Hadoop configuration).

### Output
Returns `Unit` — the method writes an index file to `indexFile` as a side effect.  
From source docs/overloads, indexed entries are based on file name with associated SRID and bounding-box information.

### Valid Call Patterns
```scala
RasterFileRDD.buildIndex(sparkContext, dir.toString, new File(dir, "_index.csv").toString)
```

### LLM Instruction Prompt
- Use the tested receiver and argument order exactly: `RasterFileRDD.buildIndex(sparkContext, dir, indexFile)`.
- Pass a directory containing GeoTIFF files.
- Provide an explicit output index file path.
- Do not invent alternate parameters or return handling; this overload returns `Unit`.

### Prompt Snippet
```text
Build a raster index for all GeoTIFF files in `dir` by calling:
RasterFileRDD.buildIndex(sparkContext, dir, indexFile)
where `indexFile` is the output index path (for example, dir + "/_index.csv").
```

### Common Failure Modes
- `dir` does not exist or is not readable.
- `dir` contains no GeoTIFF files to index.
- `indexFile` path is invalid or not writable.
- Using a different/unverified call shape (wrong receiver or argument order).

### Fix Code Hint
```scala
val dirPath = dir.toString
val indexPath = new File(dir, "_index.csv").toString
RasterFileRDD.buildIndex(sparkContext, dirPath, indexPath)
```

## API Test: `call`

### Signature
```scala
override def call(f: IFeature): Int
```
_Source: beast/beast-spark/src/main/scala/edu/ucr/cs/bdlab/beast/operations/FeatureWriterSize.scala:31_

_Source doc:_ For Java callers

### Goal
Provide a Java-function callback that takes one spatial feature (`IFeature`) and returns an `Int` value (used in Java-facing Spark/Beast APIs).

### Parameters
- `f` (`IFeature`): The input feature passed by the caller framework into the callback.

### Input
A valid `IFeature` object must be provided by the calling API (typically Spark Java function invocation in Beast).  
From the verified test usage, this is used as an implementation of `org.apache.spark.api.java.function.Function[IFeature, Int]` passed to `IndexHelper.partitionFeatures(...)`.

### Output
Returns `Int` — an integer computed by the callback implementation for the given feature (in the test, constant `1`).

### Valid Call Patterns
```scala
new org.apache.spark.api.java.function.Function[IFeature, Int]() {
  override def call(v1: IFeature): Int = 1
}
```

### LLM Instruction Prompt
- Use `call` only as an override inside a Java Spark `Function[IFeature, Int]` implementation.
- Keep the method shape exactly `override def call(<feature>: IFeature): Int`.
- Pass that function object to APIs that require `Function[IFeature, Int]` (verified: `IndexHelper.partitionFeatures(...)`).
- Do not invent extra parameters or different return types.

### Prompt Snippet
```text
Create a Java Spark function object for Beast that overrides `call(v1: IFeature): Int` and returns an Int. Use this object as the third argument to `IndexHelper.partitionFeatures(...)`.
```

### Common Failure Modes
- Using the wrong function interface/type (not `org.apache.spark.api.java.function.Function[IFeature, Int]`).
- Returning a non-`Int` value from `call`.
- Changing the method signature (extra args, different arg type, different return type).
- Passing non-`IFeature` data into a callback expecting `IFeature`.

### Fix Code Hint
```scala
val partitionedFeatures: JavaPartitionedSpatialRDD =
  IndexHelper.partitionFeatures(
    JavaRDD.fromRDD(features),
    classOf[RSGrovePartitioner],
    new org.apache.spark.api.java.function.Function[IFeature, Int]() {
      override def call(v1: IFeature): Int = 1
    },
    new BeastOptions()
  )
```

## API Test: `checkOptions`

### Signature
```scala
def checkOptions(options: ParsedCommandLineOptions, out: PrintStream): Boolean
```
_Source: beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/util/OperationHelper.scala:293_

_Source doc:_ Check if the user options are valid. This means that the user did not add any unexpected options or leave out any required option @param options parsed command line options. @return

### Goal
Validate parsed Beast/RDPro CLI-style options and report whether they satisfy expected option constraints (no unexpected options, no missing required options).

### Parameters
- `options` (`ParsedCommandLineOptions`): Parsed command-line options object (typically produced by `OperationHelper.parseCommandLineArguments(...)`) to validate.
- `out` (`PrintStream`): Output stream where validation messages/errors can be written during option checking.

### Input
`checkOptions` does not read raster/vector files directly; it validates an already parsed options structure.

Preconditions:
- `options` must be a valid `ParsedCommandLineOptions` instance.
- In real usage shown by tests, `options` is created via:
  `OperationHelper.parseCommandLineArguments(...)`.
- The option set should match the target command/subcommand expectations; otherwise validation fails (e.g., unexpected parameter or missing required parameter).

### Output
Returns `Boolean` — `true` if options are valid; `false` if invalid (such as containing unexpected options or omitting required options).

### Valid Call Patterns
```scala
// from beast/common/src/test/scala/edu/ucr/cs/bdlab/beast/util/OperationHelperTest.scala — test("Check user options")
{
    // Unexpected parameters
    val commandLineOptions = OperationHelper.parseCommandLineArguments("test", "path1",
      "option1:value1", "-option2", "-no-option3", "path2", "option4[0]:1", "-option4[1]")
    assert(!OperationHelper.checkOptions(commandLineOptions, new PrintStream(new NullOutputStream)))
    // Correct!
    val parsedOptions2 = OperationHelper.parseCommandLineArguments("subtest1", "path1", "sparam2:1",
        "-sparam", "-no-param1[0]", "path2")
    assert(OperationHelper.checkOptions(parsedOptions2, new PrintStream(new NullOutputStream)))
    // Required parameter not found
    val parsedOptions3 = OperationHelper.parseCommandLineArguments("subtest1", "path1",
        "-sparam", "-no-param1[0]", "path2")
    assert(!OperationHelper.checkOptions(parsedOptions3, new PrintStream(new NullOutputStream)))
  }
```

### LLM Instruction Prompt
- Always call with receiver/qualifier exactly as tested: `OperationHelper.checkOptions(options, out)`.
- Pass a `ParsedCommandLineOptions` instance, not raw argument strings.
- Create `options` first using `OperationHelper.parseCommandLineArguments(...)` when following known working patterns.
- Treat `false` as validation failure (unexpected option or missing required option) and correct arguments before running downstream operations.

### Prompt Snippet
```text
Parse CLI-style arguments with OperationHelper.parseCommandLineArguments(...), then call
OperationHelper.checkOptions(parsed, outStream). Continue only if it returns true.
If false, revise arguments to remove unexpected options and include required ones.
```

### Common Failure Modes
- Passing raw strings/arrays directly to `checkOptions` instead of `ParsedCommandLineOptions`.
- Including unexpected options in parsed arguments → returns `false`.
- Omitting required options/parameters for the selected command/subcommand → returns `false`.
- Ignoring the boolean result and proceeding with invalid options.

### Fix Code Hint
```scala
val parsed = OperationHelper.parseCommandLineArguments(
  "subtest1", "path1", "sparam2:1", "-sparam", "-no-param1[0]", "path2"
)
val ok = OperationHelper.checkOptions(parsed, new PrintStream(new NullOutputStream))
if (!ok) {
  // revise CLI arguments: remove unexpected options and add required ones
}
```

## API Test: `compress`

### Signature
```scala
protected[raptor] def compress: Unit
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/MemoryTile.scala:211_

### Goal
Compress the in-memory pixel storage of a Raptor `MemoryTile` while preserving pixel values for later read/write access in distributed raster processing workflows.

### Parameters
_None._

### Input
Call this on an existing `MemoryTile` instance (as shown in tests: `tile.compress`) after pixel values are already loaded or written (e.g., via `setPixelValue`).

Grounded preconditions from available context:
- This is an internal API (`protected[raptor]`), not a public RDPro user-facing operation.
- No file path or raster format argument is passed to `compress`; it operates on the tile object’s current in-memory state.
- Test-verified behavior indicates automatic decompression on subsequent `getPixelValue` and `setPixelValue` calls.

### Output
Returns `Unit` — no direct return value; the effect is state change on the tile (compressed internal representation), with pixel content still readable/writable afterward via automatic decompression.

### Valid Call Patterns
```scala
tile.compress
```

### LLM Instruction Prompt
- Use the receiver form exactly as verified in tests: `tile.compress`.
- Do not add arguments (the method takes none).
- Do not present this as a public top-level RDPro raster API; it is internal to `raptor` (`protected[raptor]`).
- If generating end-user pipelines, prefer documented public raster APIs (`geoTiff`, `mapPixels`, `reshapeNN`, `saveAsGeoTiff`) unless you are explicitly working inside Raptor internals/tests.

### Prompt Snippet
```text
Given a MemoryTile instance named tile, call compression with:
tile.compress
Do not pass parameters. This mutates tile state and returns Unit.
```

### Common Failure Modes
- Calling `compress` from outside allowed visibility scope (`protected[raptor]`) and getting an access error.
- Incorrectly invoking it like `tile.compress()` with expected return data; it returns `Unit` and is used for side effects.
- Treating `compress` as a file compression/export API (it does not write GeoTIFF/CSV and takes no path).

### Fix Code Hint
```scala
// Internal Raptor usage pattern (as verified by tests)
tile.compress
// Then continue normal pixel access; decompression is automatic on read/write
val v = tile.getPixelValue(0, 0)
tile.setPixelValue(tile.x2, tile.y2, Array[Byte](10, 20, 30))
```

## API Test: `compute`

### Signature
```scala
override def compute(split: Partition, context: TaskContext): Iterator[ITile[T]]
protected def compute(geometries: Array[_<:Geometry], metadata: RasterMetadata): Unit
def compute(pID: Int, ring: CoordinateSequence, w: Int, h: Int): Unit
override def compute(split: Partition, context: TaskContext): Iterator[IFeature]
override def compute(split: Partition, context: TaskContext): Iterator[(EnvelopeNDLite, (Iterator[IFeature], Iterator[IFeature]))]
override def compute(split: Partition, context: TaskContext): Iterator[(Iterator[T], Iterator[U])]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/PixelsInside.scala:119  (+8 more definition site/overload)_

_Source doc:_ Compute the intersections for the given linear ring @param pID the ID of the polygon @param ring the list of coordinates that make the ring already projected to the raster space @param w the width of the raster in pixels @param h the height of the raster in pixels

### Goal
Compute polygon–raster intersections for one linear ring (already in raster pixel space) and store/update internal intersection state for later raster-vector processing.

### Parameters
- `pID` (`Int`): ID of the polygon this ring belongs to.
- `ring` (`CoordinateSequence`): Coordinates of the linear ring, already projected/transformed to raster space.
- `w` (`Int`): Raster width in pixels.
- `h` (`Int`): Raster height in pixels.

### Input
Caller must provide:
- A valid polygon ID (`pID`) used to track which polygon owns computed intersections.
- A `CoordinateSequence` representing a ring geometry in **raster-space coordinates** (not raw geographic CRS coordinates).
- Raster dimensions `w` and `h` in pixels for the target raster grid.

Preconditions from available docs/context:
- The ring must already be projected to raster space (explicitly stated in source doc).
- `w` and `h` should match the target raster metadata dimensions used by the surrounding workflow.
- This method is part of overloaded internal compute pipelines; ensure you call the intended overload by receiver + argument types.

### Output
Returns `Unit` — no direct return value.  
Effect: updates internal intersection results/state for the receiver object (as implied by source doc and related `Intersections.compute(...)` usage in tests).

### Valid Call Patterns
```scala
val intersections1 = new Intersections
intersections1.compute(geometries1, metadata)
```

### LLM Instruction Prompt
- Use the receiver-qualified call form exactly (e.g., `intersections1.compute(...)`).
- Do not call a bare `compute(...)` without an instance/object.
- Match overload by exact argument types; for this documented API, the target overload is `compute(pID: Int, ring: CoordinateSequence, w: Int, h: Int)`.
- Ensure `ring` is already in raster space before calling.
- Use raster pixel dimensions for `w` and `h`, not map-unit extents.

### Prompt Snippet
```text
Call the `compute` overload on an existing intersections/pixels-inside style instance, not as a standalone function. 
Pass polygon ID (Int), a raster-space linear ring (CoordinateSequence), and raster width/height in pixels.
If your geometry is still in map CRS, transform it to raster space first.
```

### Common Failure Modes
- Calling the wrong overload of `compute` due to ambiguous method name.
- Passing ring coordinates in geographic/projected CRS instead of raster pixel space.
- Using incorrect raster dimensions (`w`, `h`) that do not match the raster metadata/context.
- Expecting a returned collection/value; this overload returns `Unit` and works by side effect on receiver state.

### Fix Code Hint
```scala
// Verified receiver-qualified pattern from tests (different overload):
val intersections = new Intersections
intersections.compute(geometries, metadata)

// For the target overload, keep the same receiver-qualified style and exact argument order:
// intersections.compute(pID, ring, w, h)
```

## API Test: `computeForFeatures`

### Signature
```scala
def computeForFeatures(features: SpatialRDD, synopsisSize: Long = 1024 * 1024): Synopsis
def computeForFeatures(features: SpatialRDD, sizeFunction: IFeature => Int = f => f.getStorageSize) : Summary
def computeForFeatures(features : JavaSpatialRDD) : Summary
def computeForFeatures(features: SpatialRDD, numPartitions: Int*): (Summary, RDD[(Array[Int], Summary)])
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/synopses/Synopsis.scala:34  (+3 more definition site/overload)_

### Goal
Compute dataset summary/synopsis statistics for a `SpatialRDD`, including an overload that returns one global summary plus per-grid-cell local summaries over the input bounding box.

### Parameters
- `features` (`SpatialRDD`): the input set of spatial features to summarize.
- `synopsisSize` (`Long`), default `1024 * 1024`: target synopsis size for the `Synopsis`-returning overload.

### Input
`computeForFeatures` operates on an in-memory `SpatialRDD` (or `JavaSpatialRDD` for the Java overload), not directly on file paths.  
For the `numPartitions: Int*` overload, `numPartitions` is interpreted as “either the total number of cells or an array of number of partitions along each dimension” (per source doc).  
No additional file-format or CRS compatibility preconditions are documented for this method in the provided sources.

### Output
Returns `Synopsis` — a computed synopsis object for the input `SpatialRDD` when using the `(features, synopsisSize)` overload.

For other overloads (per signature):
- `(features, sizeFunction)` returns `Summary`
- `(features: JavaSpatialRDD)` returns `Summary`
- `(features, numPartitions: Int*)` returns `(Summary, RDD[(Array[Int], Summary)])`, i.e., a global summary plus local summaries keyed by grid-cell index.

### Valid Call Patterns
```scala
IndexHelper.partitionFeatures(features, new GridPartitioner(Summary.computeForFeatures(features), 1))

val summary = Summary.computeForFeatures(features, f => f.getGeometry.getNumPoints * 2 * 4)
```

### LLM Instruction Prompt
- Use an actual `SpatialRDD` variable as input; do not pass file paths to `computeForFeatures`.
- Pick the overload intentionally:
  - `Summary.computeForFeatures(features)`-style for `Summary` use (as shown in tests/README patterns),
  - `Summary.computeForFeatures(features, f => ...)` when custom feature size logic is needed.
- If using the varargs overload, pass integer partition arguments only; semantics are total cell count or per-dimension partition counts.
- Do not invent extra parameters or return fields beyond the declared overloads.

### Prompt Snippet
```text
Given a SpatialRDD variable `features`, call Summary.computeForFeatures(features) to get a Summary for partitioning logic. If custom sizing is required, call Summary.computeForFeatures(features, f => ...). Do not pass file paths or unsupported arguments.
```

### Common Failure Modes
- Passing a path/string instead of a `SpatialRDD`.
- Using the wrong overload for the expected return type (`Synopsis` vs `Summary` vs tuple with `RDD[(Array[Int], Summary)]`).
- Supplying non-`Int` values to `numPartitions: Int*`.
- Assuming undocumented behaviors (e.g., CRS/file parsing behavior) that are not specified for this API.

### Fix Code Hint
```scala
// features must already be a SpatialRDD
val globalSummary: Summary = Summary.computeForFeatures(features)

// Custom sizing overload (README example)
val sizedSummary: Summary =
  Summary.computeForFeatures(features, f => f.getGeometry.getNumPoints * 2 * 4)

// Grid-based summaries overload (returns global + local)
val (overall, byCell) = Summary.computeForFeatures(features, 16)
```

## API Test: `computeForFeaturesWithOutputSize`

### Signature
```scala
def computeForFeaturesWithOutputSize(features: JavaSpatialRDD, opts: BeastOptions) : Summary
def computeForFeaturesWithOutputSize(features : SpatialRDD, opts : BeastOptions) : Summary
```
_Source: beast/beast-spark/src/main/scala/edu/ucr/cs/bdlab/beast/operations/GeometricSummary.scala:49  (+1 more definition site/overload)_

_Source doc:_ Java shortcut

### Goal
Compute a geometric summary for input features, including an estimate of output size based on writer options (for example, estimating size if written as GeoJSON).

### Parameters
- `features` (`JavaSpatialRDD`): The input spatial feature RDD to summarize (Java-facing overload; Scala overload accepts `SpatialRDD`).
- `opts` (`BeastOptions`): Beast options used by the summary computation, including output-format-related options that affect estimated output size.

### Input
A populated feature RDD (`JavaSpatialRDD` or `SpatialRDD`) and a `BeastOptions` instance.  
From documented usage, output size estimation depends on options such as output/input format keys (example uses `"iformat" -> "geojson"`).  
No additional preconditions for this specific method are documented in the provided sources.

### Output
Returns `Summary` — an in-memory summary object for the input features, including computed statistics and output-size estimation driven by `opts`.

### Valid Call Patterns
```scala
// Estimate the output size if the records are written to GeoJSON
val summary = GeometricSummary.computeForFeaturesWithOutputSize(features, "iformat" -> "geojson")
```

### LLM Instruction Prompt
- Use the object-qualified call form exactly as documented: `GeometricSummary.computeForFeaturesWithOutputSize(...)`.
- Pass a feature RDD as the first argument and options as the second argument.
- Do not invent extra parameters or different return types.
- If you need Java interop, use the `JavaSpatialRDD` overload; for Scala pipelines, use the `SpatialRDD` overload.

### Prompt Snippet
```text
Given a SpatialRDD/JavaSpatialRDD named `features`, call
GeometricSummary.computeForFeaturesWithOutputSize(features, opts)
to get a Summary. Use BeastOptions-compatible key/value options (e.g., format options) because output-size estimation depends on opts.
```

### Common Failure Modes
- Passing a non-spatial RDD instead of `JavaSpatialRDD`/`SpatialRDD`.
- Using an unqualified or different receiver (the documented form is `GeometricSummary.computeForFeaturesWithOutputSize(...)`).
- Supplying options in a form that is not accepted as `BeastOptions` in your language binding.

### Fix Code Hint
```scala
import edu.ucr.cs.bdlab.beast._

// If your code has key/value options, make sure they are provided in a BeastOptions-compatible form
val summary = GeometricSummary.computeForFeaturesWithOutputSize(features, "iformat" -> "geojson")
```

## API Test: `computePointHistogramSparse`

### Signature
```scala
@varargs def computePointHistogramSparse(features: SpatialRDD, sizeFunction: IFeature => Int, mbb: EnvelopeNDLite, numBuckets: Int*): UniformHistogram
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/synopses/HistogramOP.scala:72_

_Source doc:_ Compute a point histogram for sparse histograms. It maps each record to a bucket and then aggregate by bucket. This method can be helpful for very large histograms to avoid moving the entire histogram during the reduce step. @param features the features to compute their histogram @param sizeFunction the function that evaluates the size of each feature @param mbb the minimum bounding box of the histogram, typically, this is the same as the input MBB @param numBuckets the number of buckets in the histogram @return the computed histogram

### Goal
Compute a sparse point histogram from a `SpatialRDD` by assigning each feature to histogram buckets within an `mbb` and aggregating per-bucket values, which is useful for large histogram sizes in distributed Spark execution.

### Parameters
- `features` (`SpatialRDD`): The spatial features (points in the documented tests) to bin into histogram buckets.
- `sizeFunction` (`IFeature => Int,
                                          mbb: EnvelopeNDLite, numBuckets: Int*`): A function applied to each `IFeature` that returns an `Int` contribution (e.g., `_ => 1` for count-style histograms); `mbb` defines histogram bounds; `numBuckets` specifies bucket counts per dimension (varargs).

### Input
- A Spark `SpatialRDD` of features.
- A valid `EnvelopeNDLite` (`mbb`) defining the histogram extent (typically the dataset MBB, e.g., `points.summary` in tests).
- One or more integer bucket counts through `numBuckets`.
- A per-feature sizing function `IFeature => Int`.
- From tests, points outside `mbb` can be present; the method still computes a histogram for the specified bounds.

### Output
Returns `UniformHistogram` — an in-memory histogram object with uniform bucket partitioning over the provided `mbb`, containing aggregated bucket values computed from `sizeFunction`.

### Valid Call Patterns
```scala
val points: SpatialRDD = sparkContext.parallelize(Array(
  Feature.create(null, new PointND(new GeometryFactory, 2, 1.0, 1.0)),
  Feature.create(null, new PointND(new GeometryFactory, 2, 3.0, 3.0))))
val mbr = points.summary
val h: UniformHistogram = HistogramOP.computePointHistogramSparse(points, _=>1, mbr, 4)
```

```scala
val points: SpatialRDD = sparkContext.parallelize(Array(
  Feature.create(null, new PointND(new GeometryFactory, 2, 1.0, 1.0)),
  Feature.create(null, new PointND(new GeometryFactory, 2, 3.0, 3.0)),
  Feature.create(null, new PointND(new GeometryFactory, 2, 5.0, 5.0)),
))
val mbr = new EnvelopeNDLite(2, 1.0, 1.0, 3.0, 3.0)
val h: UniformHistogram = HistogramOP.computePointHistogramSparse(points, _=>1, mbr, 4)
```

### LLM Instruction Prompt
- Use the exact qualified call form from verified tests: `HistogramOP.computePointHistogramSparse(features, sizeFunction, mbb, numBuckets...)`.
- Pass a `SpatialRDD` as `features`.
- Pass a function of type `IFeature => Int` for `sizeFunction` (use `_=>1` for simple counts).
- Provide an `EnvelopeNDLite` for `mbb` (often `features.summary`).
- Provide bucket counts as `Int` varargs (e.g., `4`).
- Do not invent overloads, extra parameters, or different return types.

### Prompt Snippet
```text
Given a SpatialRDD `points`, compute a sparse histogram with:
- size function `_=>1`
- histogram bounds `points.summary` (or a provided EnvelopeNDLite)
- bucket count `4`
Use this exact form:
`val h: UniformHistogram = HistogramOP.computePointHistogramSparse(points, _=>1, mbr, 4)`
```

### Common Failure Modes
- Calling an unqualified or wrong receiver form (e.g., bare `computePointHistogramSparse(...)`) when `HistogramOP.computePointHistogramSparse(...)` is required by the shown call pattern.
- Passing a wrong `sizeFunction` type (must be `IFeature => Int`).
- Passing non-`SpatialRDD` input as `features`.
- Using an invalid or mismatched `mbb` object type (must be `EnvelopeNDLite`).
- Omitting bucket arguments in `numBuckets` when histogram partitioning is needed.

### Fix Code Hint
```scala
val mbr: EnvelopeNDLite = points.summary
val h: UniformHistogram =
  HistogramOP.computePointHistogramSparse(points, _=>1, mbr, 4)
```

## API Test: `config`

### Signature
```scala
def config(key: String, value: Any): JavaSpatialGeneratorBuilder
def config(opts: BeastOptions): JavaSpatialGeneratorBuilder
def config(key: String, value: Any): SpatialGeneratorBuilder
def config(opts: BeastOptions): SpatialGeneratorBuilder
def config: Map[String, String]
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/generator/JavaSpatialGeneratorBuilder.scala:32  (+4 more definition site/overload)_

_Source doc:_ Set configuration of the generated data

### Goal
Set generator-specific options on a spatial data generator builder before producing synthetic spatial data (for example, boxes/polygons within an MBR).

### Parameters
- `key` (`String`): Configuration option name (in real usage, constants such as `UniformDistribution.MaxSize`, `UniformDistribution.NumSegments`, `UniformDistribution.GeometryType`, `SpatialGenerator.Seed` are used).
- `value` (`Any`): Configuration option value for that key (real usage shows both `String` values like `"0.2,0.1"` / `"box"` / `"polygon"` and numeric values like `10` / `1794`).

### Input
`config` is called on an existing generator builder instance (e.g., `new SpatialGeneratorBuilder(sparkContext).mbr(desiredMBR)`), not as a standalone function.

Preconditions from verified usage:
- You must have a `SpatialGeneratorBuilder` (or Java counterpart) instance.
- Use valid key/value combinations for the selected generator/distribution.  
- `config` itself does not load raster/vector files; it configures synthetic data generation settings.

### Output
Returns `JavaSpatialGeneratorBuilder` — the same builder type with updated configuration, enabling fluent chaining of more `.config(...)` calls and a terminal generation call such as `.uniform(...)`.

### Valid Call Patterns
```scala
val desiredMBR = new EnvelopeNDLite(2, 2, 3, 9, 8)
val randomPoints: SpatialRDD = new SpatialGeneratorBuilder(sparkContext).mbr(desiredMBR)
  .config(UniformDistribution.MaxSize, "0.2,0.1")
  .config(UniformDistribution.NumSegments, 10)
  .config(UniformDistribution.GeometryType, "box")
  .config(SpatialGenerator.Seed, 1794)
  .uniform(10)
```

```scala
val desiredMBR = new EnvelopeNDLite(2, 2, 3, 9, 8)
val randomPoints: SpatialRDD = new SpatialGeneratorBuilder(sparkContext).mbr(desiredMBR)
  .config(UniformDistribution.MaxSize, "0.2,0.1")
  .config(UniformDistribution.NumSegments, 10)
  .config(UniformDistribution.GeometryType, "polygon")
  .config(SpatialGenerator.Seed, 1794)
  .uniform(100)
```

### LLM Instruction Prompt
- Call `config` as an instance method on a builder (`value.config(...)`), preserving fluent chaining.
- Prefer tested key constants and value shapes shown above.
- Do not invent unsupported keys or claim validation rules not documented.
- If key semantics are unknown, state that explicitly instead of guessing.

### Prompt Snippet
```text
Given a SpatialGeneratorBuilder, configure generation by chaining:
.config(UniformDistribution.MaxSize, "0.2,0.1")
.config(UniformDistribution.NumSegments, 10)
.config(UniformDistribution.GeometryType, "box")
.config(SpatialGenerator.Seed, 1794)
then call .uniform(n).
```

### Common Failure Modes
- Calling `config(...)` without a builder receiver (won’t match the tested call form).
- Passing arbitrary/unsupported key names for the chosen generator.
- Passing value types/formats that don’t match what a key expects (e.g., malformed size string for `MaxSize`).
- Expecting `config` alone to generate output; generation occurs only after terminal calls like `.uniform(...)`.

### Fix Code Hint
```scala
val builder = new SpatialGeneratorBuilder(sparkContext).mbr(desiredMBR)

val generated: SpatialRDD = builder
  .config(UniformDistribution.MaxSize, "0.2,0.1")
  .config(UniformDistribution.NumSegments, 10)
  .config(UniformDistribution.GeometryType, "polygon")
  .config(SpatialGenerator.Seed, 1794)
  .uniform(100)
```

## API Test: `construct`

### Signature
```scala
def construct(out: DataOutput, entries: Array[(Long, Long, Int)]): Unit
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/DiskTileHashtable.scala:38_

_Source doc:_ Construct a compact hashtable for the given list of entries and write to the given output @param out the data output to write the hashtable to @param entries the list of entries in the form (key=tileID, val1=Offset, val2=Length)

### Goal
Build a compact on-disk hashtable from tile index entries `(tileID, offset, length)` and serialize it to a provided binary output stream.

### Parameters
- `out` (`DataOutput`): destination binary writer to receive the serialized compact hashtable bytes.
- `entries` (`Array[(Long, Long, Int)]`): hashtable entries encoded as `(key=tileID, val1=Offset, val2=Length)`.

### Input
A caller must provide:
- A valid, writable `DataOutput` (e.g., an opened Hadoop/FS output stream as used in tests).
- An `Array[(Long, Long, Int)]` where each tuple is exactly:
  - `Long` key: tile ID
  - `Long` value1: offset
  - `Int` value2: length

Preconditions from observed usage:
- `out` must be open and writable when `construct` is called.
- The call form is object-qualified as `DiskTileHashtable.construct(out, entries)` (verified in test suite).

### Output
Returns `Unit` — the method writes the compact hashtable binary representation to `out`; no Scala value is returned.

### Valid Call Patterns
```scala
val rand = new Random(0)
val entries = new Array[(Long, Long, Int)](100).map(_ => (rand.nextLong().abs, rand.nextLong().abs, rand.nextInt().abs))
val file = new Path(scratchPath, "test")
val fileSystem = file.getFileSystem(sparkContext.hadoopConfiguration)
val out = fileSystem.create(file)
DiskTileHashtable.construct(out, entries)
out.close()
```

### LLM Instruction Prompt
- Use the exact qualified call form: `DiskTileHashtable.construct(out, entries)`.
- Pass `entries` as `Array[(Long, Long, Int)]` in `(tileID, offset, length)` order.
- Ensure `out` is an open `DataOutput` before calling, and close it after writing.
- Do not invent additional parameters or return handling; return type is `Unit`.

### Prompt Snippet
```text
Create/open a DataOutput, prepare entries as Array[(Long, Long, Int)] where each tuple is (tileID, offset, length), then call DiskTileHashtable.construct(out, entries). Close out after the call.
```

### Common Failure Modes
- Passing tuples in wrong order or wrong types (must be exactly `(Long, Long, Int)`).
- Calling with a closed or invalid `DataOutput`.
- Using a different/unqualified call shape not shown by verified usage.

### Fix Code Hint
```scala
val out = fileSystem.create(file) // DataOutput-compatible stream
val entries: Array[(Long, Long, Int)] = Array(
  (123L, 4096L, 512),
  (124L, 4608L, 256)
)
DiskTileHashtable.construct(out, entries)
out.close()
```

## API Test: `copyResource`

### Signature
```scala
def copyResource(resourcePath: String, filePath: File, overwrite: Boolean): Unit
def copyResource(resourcePath: String, filePath: File): Unit
```
_Source: beast/commontest/src/main/scala/org/apache/spark/test/ScalaSparkTest.scala:251  (+1 more definition site/overload)_

_Source doc:_ Copy a resource to a temporary file to allow reading it as a file. @param resourcePath the path of the resource to read @param filePath     the path of the file to write @param overwrite    set this flag to automatically overwrite the output file.

### Goal
Copy a classpath test/resource file (for example `"/test.points"`) to a concrete filesystem `File` path so downstream Beast/RDPro/Spark code can read it as a normal file.

### Parameters
- `resourcePath` (`String`): Path to the bundled resource to read (test usage shows values like `"/test.points"`).
- `filePath` (`File`): Destination file path to write to (e.g., `new File(path, "input.txt")`).
- `overwrite` (`Boolean`): If `true`, automatically overwrite an existing destination file.

### Input
- A valid resource path string that resolves to an available resource.
- A writable destination `File` path (parent directory should exist or be created by caller; tests call `mkdirs()` first).
- If destination may already exist, use the 3-argument overload and set `overwrite = true` when replacement is intended.

### Output
Returns `Unit` — the method performs a side effect (writes/copies the resource to `filePath`) and does not return a value.

### Valid Call Patterns
```scala
copyResource("/test.points", new File(path, "input.txt"))
copyResource("/test.points", new File(path, "_input.txt"))
copyResource("/test.points", new File(path, ".input.txt"))
```

### LLM Instruction Prompt
- Use the tested call shape exactly: `copyResource(resourcePath, new File(...))` (or the 3-arg overload when overwrite control is needed).
- Pass a resource-style path string (example from tests: `"/test.points"`).
- Ensure destination directories are prepared before copying (tests do `path.mkdirs()` / `subdir.mkdirs()`).
- Do not invent extra parameters or return handling; this API returns `Unit`.

### Prompt Snippet
```text
Create the output directory, then call copyResource("/test.points", new File(path, "input.txt")).
If the destination might exist and must be replaced, use copyResource(resourcePath, filePath, overwrite = true).
```

### Common Failure Modes
- Resource not found at `resourcePath` (bad/missing classpath resource).
- Destination directory not created or not writable.
- Existing destination file conflicts when overwrite is not enabled (use 3-arg overload with `true` when replacement is required).

### Fix Code Hint
```scala
val path = new File(scratchDir, "subdir")
path.mkdirs()

// Basic copy (tested form)
copyResource("/test.points", new File(path, "input.txt"))

// If replacing an existing file is required:
copyResource("/test.points", new File(path, "input.txt"), overwrite = true)
```

## API Test: `count`

### Signature
```scala
def count: Int
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/GeoTiffWriter.scala:860_

### Goal
Return the number of elements in the current dataset/RDD result so you can summarize raster/vector processing outputs (for example, after filtering or joins).

### Parameters
_None._

### Input
A receiver object that defines a zero-argument `count` method returning `Int` (for example, the tested call forms `filteredData.count()` and `joined.count()`).

From the provided context, `count` itself takes no files/formats directly; required formats and preprocessing are determined by how the receiver was produced (e.g., `readCSVPoint`, `spatialFile`, partitioning, range query, join).

Preconditions from documented workflows that commonly affect whether upstream steps produce a valid receiver:
- For raster overlay/reshape workflows, metadata compatibility (CRS/resolution/tile size) must be handled before later operations.
- For typed raster loading, `sc.geoTiff[T]` type must match true pixel type.
- For disjoint partitioning workflows, duplicate handling may be required upstream.

### Output
Returns `Int` — the total number of records/elements in the receiver collection/result.

### Valid Call Patterns
```scala
assertResult(5)(filteredData.count())
```

```scala
assert(joined.count() == 6)
```

### LLM Instruction Prompt
- Use the instance call form on an existing value, e.g., `value.count()`.
- Do not add parameters; this API is zero-argument.
- Ensure the receiver is already constructed by a prior valid pipeline step (load/query/join/etc.).
- Do not assume this method reads/writes files directly.

### Prompt Snippet
```text
Given an existing result object (e.g., filteredData or joined), call count as value.count() with no arguments, and treat the returned Int as the element count.
```

### Common Failure Modes
- Calling `count` on the wrong object (e.g., before producing `filteredData`/`joined`).
- Passing arguments to `count` even though signature is zero-argument.
- Assuming `count` performs file I/O or schema conversion; those must happen upstream.
- Upstream incompatibility issues (CRS/type/metadata/partitioning rules) causing pipeline failure before `count` is reached.

### Fix Code Hint
```scala
val filteredData = partitionedData.rangeQuery(new GeometryFactory(new PrecisionModel(), 3857)
  .toGeometry(new Envelope(-11131949.07932735607028, -10018754.171394621953368,
    3503549.843504375312477, 4865942.279503175057471)))

val n: Int = filteredData.count()
println(n)
```

## API Test: `create`

### Signature
```scala
def create[T](tiles: Array[MemoryTile[T]]): MemoryTileWindow[T]
def create[T: ClassTag](tileID: Int, metadata: RasterMetadata, rasterFeature: RasterFeature, numValues: Int): MemoryTileWindow[T]
def create(row: Row, geometry: Geometry): Feature
def create(geometry: Geometry, _names: Array[String], _types: Array[DataType], _values: Array[Any]): Feature
def create(x1: Double, y1:Double, x2: Double, y2:Double, srid: Int, rasterWidth: Int, rasterHeight: Int, tileWidth: Int, tileHeight: Int): RasterMetadata
def create(names: Array[String], values: Array[Any]): RasterFeature
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/RasterMetadata.scala:324  (+5 more definition site/overload)_

_Source doc:_ Create a raster metadata that represents a geographical region provided by a rectangle. @param x1 the x-coordinate of the left edge of the pixel at (0, 0) @param y1 the y-coordinate of the top edge of the pixel at (0, 0) @param x2 the x-coordinate of the right edge of the pixel at (rasterWidth - 1, rasterHeight - 1) @param y2 the y-coordinate of the bottom edge of the pixel at (rasterWidth - 1, rasterHeight - 1) @param srid the SRID that represents the coordinate reference system of the raster @param rasterWidth the number of columns in the entire raster @param rasterHeight the number of rows in the entire raster @param tileWidth the width of each tile in pixels @param tileHeight the height of each tile in pixels @return a raster metadata wit the given information

### Goal
Create a `RasterMetadata` object that defines a raster grid’s georeferenced extent, CRS (via SRID), full raster dimensions, and tile dimensions for RDPro raster operations.

### Parameters
- `x1` (`Double`): x-coordinate of the **left edge** of pixel `(0, 0)`.
- `y1` (`Double`): y-coordinate of the **top edge** of pixel `(0, 0)`.
- `x2` (`Double`): x-coordinate of the **right edge** of pixel `(rasterWidth - 1, rasterHeight - 1)`.
- `y2` (`Double`): y-coordinate of the **bottom edge** of pixel `(rasterWidth - 1, rasterHeight - 1)`.
- `srid` (`Int`): SRID identifying the raster coordinate reference system.
- `rasterWidth` (`Int`): total number of columns in the raster.
- `rasterHeight` (`Int`): total number of rows in the raster.
- `tileWidth` (`Int`): width of each tile in pixels.
- `tileHeight` (`Int`): height of each tile in pixels.

### Input
This overload takes scalar numeric inputs only (no file input directly).  
Caller must provide:
- A consistent geographic rectangle (`x1`, `y1`, `x2`, `y2`) in the CRS identified by `srid`.
- Positive raster dimensions (`rasterWidth`, `rasterHeight`) and tile dimensions (`tileWidth`, `tileHeight`) as integers.

Preconditions/compatibility context from RDPro workflows:
- This metadata is often used to prepare rasters for later operations (e.g., rasterization/reshape/overlay).
- For `overlay`, rasters must share compatible metadata (resolution/CRS/tile size); otherwise convert first using reshape operations.

### Output
Returns `RasterMetadata` — an in-memory metadata object describing raster georeferencing, CRS, total raster size, and tile layout, suitable for downstream RDPro raster processing.

### Valid Call Patterns
```scala
val metadata = RasterMetadata.create(x1 = -50, y1 = 40, x2 = -60, y2 = 30, srid = 4326,
  rasterWidth = 10, rasterHeight = 10, tileWidth = 10, tileHeight = 10)
val pixels = sc.parallelize(Seq(
  (0, 0, 100),
  (3, 4, 200),
  (8, 9, 300)
))
val raster = sc.rasterizePixels(pixels, metadata)

val metadata = RasterMetadata.create(x1 = -50, y1 = 40, x2 = -60, y2 = 30, srid = 4326,
  rasterWidth = 10, rasterHeight = 10, tileWidth = 10, tileHeight = 10)
val pixels = sc.parallelize(Seq(
  (-51.3, 30.4, 100),
  (-55.2, 34.5, 200),
  (-56.4, 39.2, 300)
))
val raster = sc.rasterizePoints(pixels, metadata)
```

### LLM Instruction Prompt
- Use the receiver exactly as `RasterMetadata.create(...)` for this overload.
- Pass exactly 9 arguments with the documented types/order (or named arguments as shown).
- Do not mix this overload with other `create` overloads (`Feature`, `RasterFeature`, `MemoryTileWindow`).
- Ensure the coordinate values and SRID describe the same CRS.
- If later doing raster `overlay`, ensure compared rasters use compatible metadata; otherwise suggest reshape first.

### Prompt Snippet
```text
Create raster metadata with RasterMetadata.create(x1, y1, x2, y2, srid, rasterWidth, rasterHeight, tileWidth, tileHeight), then reuse it in rasterizePixels/rasterizePoints. Keep CRS consistent with srid and keep dimensions/tile sizes as Int values.
```

### Common Failure Modes
- Calling the wrong overload of `create` due to overload ambiguity.
- Supplying coordinates that do not match the intended SRID/CRS.
- Using incompatible metadata across rasters, then failing later in operations like `overlay`.
- Providing invalid dimensions (non-sensical or non-positive sizes) leading to unusable metadata (exact runtime validation behavior is not specified in provided docs).

### Fix Code Hint
```scala
val metadata = RasterMetadata.create(
  x1 = -124, y1 = 42, x2 = -114, y2 = 32,
  srid = 4326,
  rasterWidth = 1000, rasterHeight = 1000,
  tileWidth = 100, tileHeight = 100
)
```

## API Test: `createDateFilter`

### Signature
```scala
def createDateFilter(dateStart: String, dateEnd: String): PathFilter
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/HDF4Reader.scala:299_

_Source doc:_ Creates a filter for paths that match the given range of dates inclusive of both start and end dates. Each date is in the format "yyyy.mm.dd". @param dateStart the start date as a string in the "yyyy.mm.dd" format (inclusive) @param dateEnd   the end date (inclusive) @return a PathFilter that will match all dates in the given range

### Goal
Create a Hadoop `PathFilter` that accepts only paths whose date string falls within an inclusive date range (`dateStart` to `dateEnd`) using the `yyyy.mm.dd` format.

### Parameters
- `dateStart` (`String`): Start date of the allowed range, inclusive, in `yyyy.mm.dd` format.
- `dateEnd` (`String`): End date of the allowed range, inclusive, in `yyyy.mm.dd` format.

### Input
Two date strings provided by the caller:
- Both are expected in the exact format `yyyy.mm.dd` per the source doc.
- The filter is intended to be used against `Path` values whose date component is represented in the same `yyyy.mm.dd` form (as shown in tests with paths like `"2001.02.15"`).

### Output
Returns `PathFilter` — a Hadoop path filter object that evaluates each `Path` and returns `true` for dates inside the inclusive range `[dateStart, dateEnd]`, and `false` otherwise.

### Valid Call Patterns
```scala
val dateFilter = HDF4Reader.createDateFilter("2001.02.15", "2005.02.11")
assert(dateFilter.accept(new Path("2001.02.15")))
assert(dateFilter.accept(new Path("2005.02.11")))
assert(dateFilter.accept(new Path("2003.07.15")))
assert(!dateFilter.accept(new Path("2005.02.12")))
assert(!dateFilter.accept(new Path("2001.01.31")))
```

### LLM Instruction Prompt
- Use the receiver exactly as validated in tests: `HDF4Reader.createDateFilter(start, end)`.
- Pass both arguments as `String` in `yyyy.mm.dd` format.
- Treat both bounds as inclusive.
- Apply the returned `PathFilter` to Hadoop `Path` objects.

### Prompt Snippet
```text
Create a date range filter with HDF4Reader.createDateFilter("YYYY.MM.DD", "YYYY.MM.DD"), then use filter.accept(new Path("YYYY.MM.DD")) to test whether a path date is within the inclusive range.
```

### Common Failure Modes
- Using a date format other than `yyyy.mm.dd`.
- Assuming the end date is exclusive (it is inclusive).
- Calling the method without the `HDF4Reader` qualifier shown in compiled tests.
- Applying the filter to paths that do not contain comparable date strings in the expected format.

### Fix Code Hint
```scala
import org.apache.hadoop.fs.Path

val start = "2001.02.15"
val end = "2005.02.11"
val dateFilter = HDF4Reader.createDateFilter(start, end)

// Inclusive bounds
val inRange = dateFilter.accept(new Path("2005.02.11"))  // true
val outOfRange = dateFilter.accept(new Path("2005.02.12")) // false
```

## API Test: `createPartitioner`

### Signature
```scala
def createPartitioner(features: SpatialRDD, partitionerClass: Class[_ <: SpatialPartitioner], numPartitions: NumPartitions, sizeFunction: IFeature=>Int, opts: BeastOptions ): SpatialPartitioner
def createPartitioner(features: JavaSpatialRDD, partitionerClass: Class[_ <: SpatialPartitioner], pcriterion: String, pvalue: Long, sizeFunction: org.apache.spark.api.java.function.Function[IFeature, Int] = {_.getStorageSize}, opts: BeastOptions ): SpatialPartitioner
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/indexing/IndexHelper.scala:136  (+1 more definition site/overload)_

_Source doc:_ Constructs a spatial partitioner for the given features. Returns an instance of the spatial partitioner class that is given which is initialized based on the given features. @param features the features to create the partitioner on @param partitionerClass the class of the partitioner to construct @param numPartitions the desired number of partitions (this is just a loose hint not a strict number) @param sizeFunction a function that calculates the size of each feature for load balancing. Only needed if the partition criterion is specified through partition size [[Size]] @return a constructed spatial partitioner

### Goal
Construct a `SpatialPartitioner` (for example `RSGrovePartitioner` or `GridPartitioner`) from an input `SpatialRDD` so vector data can be spatially partitioned for scalable Spark geospatial processing.

### Parameters
- `features` (`SpatialRDD`): input spatial features used to initialize/build the partitioner.
- `partitionerClass` (`Class[_ <: SpatialPartitioner],
                        numPartitions: NumPartitions,
                        sizeFunction: IFeature=>Int`): the spatial partitioner class to instantiate (e.g., `classOf[RSGrovePartitioner]`, `classOf[GridPartitioner]`), together with partition-count criterion via `NumPartitions(...)` and optional per-feature sizing function for size-based balancing.
- `opts` (`BeastOptions`): Beast configuration/options passed to partitioner construction (e.g., options such as `"disjoint" -> true` are shown in project usage).

### Input
Caller must provide:
- A valid `SpatialRDD` (or `JavaSpatialRDD` in the overload).
- A partitioner class that extends `SpatialPartitioner`.
- A partition target/criterion:
  - Scala overload: `numPartitions: NumPartitions` (source doc says this is a loose hint, not strict).
  - Java overload: `pcriterion: String` and `pvalue: Long`.
- A size function `IFeature => Int` when partitioning criterion is by size (`Size`), per source doc.

Preconditions/compatibility notes from project context:
- If using disjoint partitioning (`"disjoint" -> true` in options), only partitioners that support disjoint partitions should be used; otherwise error.
- Disjoint partitioning may replicate features; downstream duplicate handling may be needed unless using Beast built-in operators that handle it.

### Output
Returns `SpatialPartitioner` — a constructed/initialized partitioner instance derived from the input features and requested partitioning setup, suitable for use in calls such as `features.spatialPartition(partitioner)`.

### Valid Call Patterns
```scala
val partitioner = IndexHelper.createPartitioner(dataset, classOf[GridPartitioner],
  NumPartitions(IndexHelper.Size, 1024 * 1024), { f: IFeature => 1024 }, new BeastOptions())

val partitioner2 = IndexHelper.createPartitioner(dataset, classOf[RSGrovePartitioner],
  NumPartitions(IndexHelper.Size, 1024 * 1024), { f: IFeature => 1024 }, new BeastOptions())
```

```scala
import edu.ucr.cs.bdlab.beast.indexing.IndexHelper.{Fixed, NumPartitions}
import edu.ucr.cs.bdlab.beast.indexing.{IndexHelper, RSGrovePartitioner}
val partitioner = IndexHelper.createPartitioner(features, classOf[RSGrovePartitioner],
  NumPartitions(Fixed, features.getNumPartitions), _ => 1, "disjoint" -> true)
val partitionedFeatures = features.spatialPartition(partitioner)
```

### LLM Instruction Prompt
- Use the exact receiver form `IndexHelper.createPartitioner(...)` as shown.
- Pass a `SpatialRDD` as first argument and a concrete `Class[_ <: SpatialPartitioner]` as second argument.
- When using size-based partitioning (`NumPartitions(IndexHelper.Size, ...)`), provide a meaningful `IFeature => Int` size function.
- Treat requested partition count as a hint, not an exact guarantee.
- If enabling disjoint behavior through options, ensure chosen partitioner supports it.
- Do not invent additional parameters or alternate signatures beyond the two listed overloads.

### Prompt Snippet
```text
Create a spatial partitioner with IndexHelper.createPartitioner(features, classOf[RSGrovePartitioner], NumPartitions(Fixed, features.getNumPartitions), _ => 1, opts). If using size criterion, set NumPartitions(IndexHelper.Size, targetSize) and provide sizeFunction: IFeature => Int.
```

### Common Failure Modes
- Using a class that is not a `SpatialPartitioner` subtype for `partitionerClass`.
- Expecting exact partition count; API describes it as a loose hint.
- Using `Size` criterion without a proper size function, causing poor load balancing.
- Setting disjoint option with a partitioner that does not support disjoint partitioning.
- Not handling duplicated features introduced by disjoint partitioning in custom downstream logic.

### Fix Code Hint
```scala
import edu.ucr.cs.bdlab.beast.indexing.IndexHelper
import edu.ucr.cs.bdlab.beast.indexing.IndexHelper.NumPartitions
import edu.ucr.cs.bdlab.beast.indexing.RSGrovePartitioner
import edu.ucr.cs.bdlab.beast.common.BeastOptions
import edu.ucr.cs.bdlab.beast.geolite.IFeature

val opts = new BeastOptions()
val partitioner = IndexHelper.createPartitioner(
  features,
  classOf[RSGrovePartitioner],
  NumPartitions(IndexHelper.Size, 1024 * 1024),
  { f: IFeature => f.getStorageSize },
  opts
)
val partitioned = features.spatialPartition(partitioner)
```

## API Test: `createPartitions`

### Signature
```scala
def createPartitions(path: String, opts: BeastOptions, conf: Configuration): Array[FilePartition]
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/SpatialFileRDD.scala:318_

_Source doc:_ Create all partitions in this RDD for the given input file @return

### Goal
Create the `FilePartition` array that SpatialFileRDD will read from one or more spatial input paths, based on the provided Beast read options and Hadoop configuration.

### Parameters
- `path` (`String`): Input path string for spatial data files/directories; tests show a single path and a comma-separated multi-path form (e.g., `input1.getPath+","+input2.getPath`).
- `opts` (`BeastOptions`): Beast read options used to control input interpretation (tests show setting input format, e.g., `"iformat" -> "shapefile"` or `SpatialFileRDD.InputFormat -> "geojson"`).
- `conf` (`Configuration`): Hadoop `Configuration` used to access the underlying filesystem/environment (tests use `sparkContext.hadoopConfiguration`).

### Input
Caller provides:
- A valid spatial input path string (`path`) pointing to supported Beast spatial inputs (project docs include Shapefile, GeoJSON, CSV/WKT, etc.; tested here with Shapefile and GeoJSON).
- Reader options in `BeastOptions` (`opts`), especially input format when needed.
- A live Hadoop/Spark filesystem configuration (`conf`).

Preconditions and compatibility notes:
- `createPartitions` is for **spatial/vector file partitioning** (`SpatialFileRDD`), not RDPro raster tile operations.
- If format is ambiguous, set `iformat` in `opts` to avoid reader selection issues.
- For downstream reading, the selected feature reader class should be compatible with the path/options pair (as shown in tests via `getFeatureReaderClass` + `readPartition`).

### Output
Returns `Array[FilePartition]` — each element describes one partition of the input for `SpatialFileRDD` reading.  
In tests, multi-input path strings produce multiple partitions (e.g., two input paths -> `partitions.length == 2`).

### Valid Call Patterns
```scala
val partitions = SpatialFileRDD.createPartitions(input1.getPath+","+input2.getPath,
  "iformat"->"shapefile", sparkContext.hadoopConfiguration)
```

```scala
val partitions = SpatialFileRDD.createPartitions(inputFile.getPath, opts, sparkContext.hadoopConfiguration)
```

### LLM Instruction Prompt
- Use the receiver exactly as `SpatialFileRDD.createPartitions(...)`.
- Pass arguments in this exact order: `(path, opts, conf)`.
- Build `opts` as `BeastOptions` (examples show `"iformat" -> "shapefile"` and `SpatialFileRDD.InputFormat -> "geojson"` forms).
- Use `sparkContext.hadoopConfiguration` (or equivalent Hadoop `Configuration`) for `conf`.
- Do not invent extra parameters or overloads.

### Prompt Snippet
```text
Create partitions for spatial input with SpatialFileRDD.createPartitions(path, opts, sparkContext.hadoopConfiguration). 
If input format is not obvious, set opts with iformat (e.g., shapefile or geojson). 
Then iterate returned Array[FilePartition] with SpatialFileRDD.readPartition(...)
```

### Common Failure Modes
- Calling `createPartitions` without the `SpatialFileRDD` qualifier (may not compile in user code context).
- Passing a malformed `path` string (bad path or incorrect comma-separated composition for multiple inputs).
- Omitting/incorrect `iformat` in `opts` when auto-detection is insufficient.
- Using a missing/incorrect Hadoop `Configuration` (filesystem access failures).
- Mixing this API up with RDPro raster loading APIs (`sc.geoTiff`, `sc.hdfFile`), which are separate workflows.

### Fix Code Hint
```scala
val opts: BeastOptions = SpatialFileRDD.InputFormat -> "geojson"
val partitions = SpatialFileRDD.createPartitions(inputFile.getPath, opts, sparkContext.hadoopConfiguration)

// Optional downstream read pattern from tests
val featureReaderClass = SpatialFileRDD.getFeatureReaderClass(inputFile.getPath, opts)
for (partition <- partitions) {
  val features = SpatialFileRDD.readPartition(partition, featureReaderClass, true, opts)
  // process features
}
```

## API Test: `createRingsForOccupiedPixels`

### Signature
```scala
private[davinci] def createRingsForOccupiedPixels: Array[LinearRing]
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/VectorCanvas.scala:671_

_Source doc:_ Creates one linear ring for each contiguous part of occupied pixels. A pixel is connected to the four pixels to its west, east, north, and south. The linear ring is returned in image space based on the pixel location. Think of the corners of pixels as points in space that are connected with orthogonal lines to form the linear rings. @return

### Goal
Create one `LinearRing` per 4-neighbor connected occupied-pixel region on a `VectorCanvas`, with ring coordinates expressed in image (pixel-corner) space.

### Parameters
_None._

### Input
The method takes no explicit parameters, but it depends on the current internal occupied-pixel state of a `VectorCanvas` instance.

Preconditions from available evidence:

- Call it on a `VectorCanvas` receiver (as in tests: `canvas.createRingsForOccupiedPixels`).
- Occupancy must already be produced/populated on that canvas (e.g., by adding/rasterizing geometries before ring extraction).
- Connectivity used is **4-connected** (west/east/north/south), not diagonal connectivity.
- Output coordinates are in **image space** (pixel-location/corner-based), not stated as geographic CRS coordinates.

No file-format input is involved directly in this API call.

### Output
Returns `Array[LinearRing]` — one ring for each contiguous occupied-pixel component in the canvas, where each ring is an orthogonal boundary built from pixel-corner points in image space.

### Valid Call Patterns
```scala
val rings = canvas.createRingsForOccupiedPixels
```

```scala
val ring = canvas.createRingsForOccupiedPixels.head
```

### LLM Instruction Prompt
- Use the instance form exactly: `canvas.createRingsForOccupiedPixels` (no arguments).
- Ensure occupancy is prepared on the same `VectorCanvas` before calling.
- Treat results as image-space `LinearRing` boundaries of 4-connected occupied regions.
- Do not invent parameters, overloads, or alternate return types.

### Prompt Snippet
```text
Given a VectorCanvas named canvas with occupied pixels already rasterized, call:
`val rings = canvas.createRingsForOccupiedPixels`
This returns `Array[LinearRing]`, one ring per 4-neighbor connected occupied component in image space.
```

### Common Failure Modes
- Calling it on the wrong receiver/type (it is used as a `VectorCanvas` instance method).
- Expecting diagonal-connected components to merge; only west/east/north/south connectivity is documented.
- Interpreting ring coordinates as world/CRS coordinates instead of image-space pixel-corner coordinates.
- Calling before occupancy is populated, leading to empty or unintended ring results.

### Fix Code Hint
```scala
val canvas = new VectorCanvas(new Envelope(0, 3, 0, 3), 3, 3, 0, 5)
val factory = GeometryReader.DefaultGeometryFactory
canvas.addGeometry(factory.createPoint(new CoordinateXY(0, 0)), null)
canvas.addGeometry(factory.createPoint(new CoordinateXY(0, 1)), null)
canvas.addGeometry(factory.createPoint(new CoordinateXY(1, 0)), null)
canvas.addGeometry(factory.createPoint(new CoordinateXY(1, 1)), null)

val rings = canvas.createRingsForOccupiedPixels
```

## API Test: `createSummaryAccumulator`
_Grounding: doc-repaired from source (docfix)._

### Goal
Create and register a `SummaryAccumulator` on a Spark `SparkContext` to aggregate `IFeature` summaries during RDD execution.

### Valid Call Patterns|Valid Access Patterns
```scala
import org.apache.spark.SparkContext
import edu.ucr.cs.bdlab.beast.synopses.{Summary, SummaryAccumulator}
import edu.ucr.cs.bdlab.beast.geolite.IFeature

// sc must be org.apache.spark.SparkContext (not SparkSession)
val acc: SummaryAccumulator = Summary.createSummaryAccumulator(sc)

// or overload with exact function type: IFeature => Int
val acc2: SummaryAccumulator =
  Summary.createSummaryAccumulator(sc, (f: IFeature) => f.getStorageSize)

val counted = featuresRDD.map { f: IFeature =>
  acc.add(f)
  f
}
val n = counted.count()   // action required to materialize accumulator updates
val summary = acc.value
```

### LLM Instruction Prompt
- Call this API on `Summary` as receiver: `Summary.createSummaryAccumulator(...)`.
- Do **not** call `new Summary().createSummaryAccumulator(...)` (that method is not on instances).
- First argument must be `org.apache.spark.SparkContext` (`sc`), not `SparkSession`.
- Overload 2 requires exactly `sizeFunction: edu.ucr.cs.bdlab.beast.geolite.IFeature => Int`.
- Accumulator updates happen during Spark execution; run an action (`count`, etc.) before reading `.value`.

### Prompt Snippet
```text
Use:
val acc = Summary.createSummaryAccumulator(sc)

where sc: org.apache.spark.SparkContext.
If custom sizing is needed:
Summary.createSummaryAccumulator(sc, (f: IFeature) => IntValue)

Add via acc.add(f) inside an RDD transformation, trigger an action, then read acc.value.
```

### Common Failure Modes
- **Compile-time failure from wrong receiver:** using `new Summary().createSummaryAccumulator(...)` or any `summaryInstance.createSummaryAccumulator(...)`.
- Passing `SparkSession` where `SparkContext` is required.
- Using wrong type for overload 2 (must be `IFeature => Int`).
- Reading `acc.value` before an action executes (no updates materialized).

### Fix Code Hint
```scala
// Wrong (receiver error):
val s = new Summary()
val acc = s.createSummaryAccumulator(sc)

// Correct:
val acc = Summary.createSummaryAccumulator(sc)
```

## API Test: `createTileIDFilter`

### Signature
```scala
def createTileIDFilter(rect: Rectangle2D): PathFilter
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/HDF4Reader.scala:270_

_Source doc:_ Create a path filter that selects only the tiles that match the given rectangle in the Sinusoidal space. @param rect the extents of the range to compute the filter for in the Sinusoidal space @return a Path filter that will match the tiles based on the file name using the <tt>hxxvyy</tt> part

### Goal
Create a Hadoop `PathFilter` that keeps only HDF tile files whose `hxxvyy` tile ID intersects a requested rectangle in Sinusoidal space.

### Parameters
- `rect` (`Rectangle2D`): Rectangle extents for the selection window **in Sinusoidal space** (as documented), used to compute which `hxxvyy` tiles should be accepted.

### Input
- A `Rectangle2D` instance representing the target range in Sinusoidal coordinates.
- The returned filter is intended for paths whose filenames include tile IDs in the documented `hxxvyy` form (example from tests: `tile-h03v03.hdf`).
- Precondition: coordinates must already be in the Sinusoidal space expected by this API (the method does not document reprojection/conversion).

### Output
Returns `PathFilter` — a Hadoop path filter that accepts/rejects file paths by parsing the filename tile token (`hxxvyy`) and matching it against the tile set implied by `rect`.

### Valid Call Patterns
```scala
val tileIDFilter = HDF4Reader.createTileIDFilter(new Rectangle2D.Double(Math.toRadians(-145.0) * HDF4Reader.Scale,
  Math.toRadians(5.0) * HDF4Reader.Scale, Math.toRadians(29.0) * HDF4Reader.Scale, Math.toRadians(49.0) * HDF4Reader.Scale))
assert(tileIDFilter.accept(new Path("tile-h03v03.hdf")))
assert(tileIDFilter.accept(new Path("tile-h06v07.hdf")))
assert(!tileIDFilter.accept(new Path("tile-h02v09.hdf")))
assert(!tileIDFilter.accept(new Path("tile-h07v06.hdf")))
```

### LLM Instruction Prompt
- Call the method with the exact receiver form verified by tests: `HDF4Reader.createTileIDFilter(rect)`.
- Pass exactly one argument of type `Rectangle2D`.
- Provide rectangle extents in Sinusoidal space, not lat/lon degrees unless already converted.
- Use the returned object as a Hadoop `PathFilter` and call `accept(Path)` on candidate files.
- Expect matching based on filename `hxxvyy` token.

### Prompt Snippet
```text
Create a Sinusoidal Rectangle2D, then call HDF4Reader.createTileIDFilter(rect). Use the returned PathFilter to test HDF file paths whose names contain an hxxvyy tile ID (e.g., tile-h03v03.hdf). Do not pass extra parameters.
```

### Common Failure Modes
- Passing a rectangle in the wrong coordinate space (e.g., unconverted geographic degrees) causes wrong tile selection.
- Using filenames that do not contain the expected `hxxvyy` pattern prevents intended matching.
- Calling a different receiver shape (e.g., bare `createTileIDFilter(...)`) may not compile in user code.

### Fix Code Hint
```scala
val rect = new Rectangle2D.Double(
  Math.toRadians(-145.0) * HDF4Reader.Scale,
  Math.toRadians(5.0) * HDF4Reader.Scale,
  Math.toRadians(29.0) * HDF4Reader.Scale,
  Math.toRadians(49.0) * HDF4Reader.Scale
)
val tileIDFilter: PathFilter = HDF4Reader.createTileIDFilter(rect)
```

## API Test: `crsToSRID`

### Signature
```scala
def crsToSRID(crs: CoordinateReferenceSystem) : Int
```
_Source: beast/cg/src/main/scala/org/apache/spark/beast/CRSServer.scala:270_

_Source doc:_ Get an integer SRID that corresponds to the given CRS according to the following logic. 1. If crs is null, return 0 2. Search the local cache as the fastest method of known CRS. 3. If not found in cache, look up the the EPSG database to find an SRID, cache, and return it. 4a. If the server is running, contact the server to get the SRID 4b. If the server is not running, assign a custom negative SRID and cache it @param crs the CRS to find an SRID for @return a unique SRID that identifies the given CRS

### Goal
Convert a CRS object into a unique integer SRID for use in Beast/RDPro CRS-aware raster/vector processing pipelines.

### Parameters
- `crs` (`CoordinateReferenceSystem`): The CRS instance to resolve to an SRID (can be a standard EPSG CRS or a non-standard/custom CRS; if `null`, result is `0`).

### Input
Caller must provide a `CoordinateReferenceSystem` object (not a file path or raster directly).  
Preconditions and behavior rules from the API doc:

- If `crs == null`, the function returns `0`.
- The method first checks a local CRS→SRID cache.
- If not cached, it tries EPSG lookup.
- If still unresolved:
  - with CRS server running: it contacts the server to obtain SRID.
  - with CRS server not running: it assigns a custom **negative** SRID and caches it.

No raster format/type-selection rule applies directly to this function.

### Output
Returns `Int` — a unique SRID identifier for the input CRS:
- `0` for `null` CRS,
- typically positive EPSG code for standard CRS (e.g., 4326, 3857),
- custom negative SRID for non-standard CRS when needed.

### Valid Call Patterns
```scala
val mercator = CRS.decode("EPSG:3857")
val sridMercator = CRSServer.crsToSRID(mercator)

val wgs84 = CRS.decode("EPSG:4326")
val sridWGS84 = CRSServer.crsToSRID(wgs84)
```

```scala
val sinusoidal = new DefaultProjectedCRS("Sinusoidal", new DefaultGeographicCRS(new DefaultGeodeticDatum("World", DefaultEllipsoid.WGS84, DefaultPrimeMeridian.GREENWICH), DefaultEllipsoidalCS.GEODETIC_2D),
  new DefaultMathTransformFactory().createFromWKT("PARAM_MT[\"Sinusoidal\", \n  PARAMETER[\"semi_major\", 6371007.181], \n  PARAMETER[\"semi_minor\", 6371007.181], \n  PARAMETER[\"central_meridian\", 0.0], \n  PARAMETER[\"false_easting\", 0.0], \n  PARAMETER[\"false_northing\", 0.0]]"), DefaultCartesianCS.PROJECTED)
val sridSinusoidal = CRSServer.crsToSRID(sinusoidal)
```

### LLM Instruction Prompt
- Use the receiver exactly as `CRSServer.crsToSRID(crs)`.
- Pass a `CoordinateReferenceSystem` object only.
- Do not pass file paths, EPSG strings, or integers directly to this function.
- Expect `0` for `null`.
- For standard CRS, expect EPSG-like positive SRIDs when resolvable.
- For non-standard CRS, allow negative SRID assignment (especially when server is not running).

### Prompt Snippet
```text
Given a CoordinateReferenceSystem object `crs`, call `CRSServer.crsToSRID(crs)` to get its SRID.
If `crs` is null, expect 0.
If CRS is standard (e.g., EPSG:4326), expect a positive EPSG SRID when available.
If CRS is custom/non-EPSG, the returned SRID may be negative.
```

### Common Failure Modes
- Passing the wrong input type (e.g., `"EPSG:4326"` string instead of a `CoordinateReferenceSystem` object).
- Assuming non-standard CRS must always map to a positive EPSG SRID.
- Ignoring the documented `null` behavior (`0`).
- Calling as bare `crsToSRID(...)` without `CRSServer` receiver (call form mismatch with verified usage).

### Fix Code Hint
```scala
// Correct: create/obtain a CoordinateReferenceSystem first, then call through CRSServer
val crs: CoordinateReferenceSystem = CRS.decode("EPSG:4326")
val srid: Int = CRSServer.crsToSRID(crs)
```

## API Test: `decodeSpatialParquet`

### Signature
```scala
def decodeSpatialParquet(dataframe: DataFrame, geomColumnName: String): DataFrame
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/SpatialParquetSource.scala:69_

_Source doc:_ Decodes a [[DataFrame]] that was encoded using the SpatialParquet format @param dataframe @param geomColumnName @return

### Goal
Decode a Spark `DataFrame` that is already SpatialParquet-encoded back into a geometry-usable spatial `DataFrame` for downstream Beast/RDPro geospatial analytics.

### Parameters
- `dataframe` (`DataFrame`): Input Spark DataFrame that was previously encoded using SpatialParquet.
- `geomColumnName` (`String`): Name of the geometry column to decode (for example, `"geometry"` in the passing test).

### Input
A Spark SQL `DataFrame` in SpatialParquet-encoded form, plus the geometry column name string that exists in that DataFrame.

Preconditions (from validated usage):
- The DataFrame should come from `SpatialParquetSource.encodeSpatialParquet(dataframe)` before decode.
- `geomColumnName` must match the encoded geometry column name used in the DataFrame schema (test uses `"geometry"`).
- This API operates on DataFrames already loaded in Spark; no direct file path is passed to this function.

### Output
Returns `DataFrame` — a decoded spatial DataFrame corresponding to the original pre-encoded rows (the test verifies row-level equality after encode → decode).

### Valid Call Patterns
```scala
val input = locateResource("/allfeatures.geojson")
val dataframe = sparkSession.read.format("geojson").load(input.getPath)
val encodedDataFrame = SpatialParquetSource.encodeSpatialParquet(dataframe)
val decodedDataFrame = SpatialParquetSource.decodeSpatialParquet(encodedDataFrame, "geometry")
```

### LLM Instruction Prompt
- Call the API with this exact receiver/qualifier form: `SpatialParquetSource.decodeSpatialParquet(dataframe, geomColumnName)`.
- Only pass a `DataFrame` that is SpatialParquet-encoded (typically produced by `SpatialParquetSource.encodeSpatialParquet`).
- Use the exact geometry column name present in the DataFrame schema (for tested usage: `"geometry"`).
- Do not invent extra parameters or overloads; this function has exactly two parameters.

### Prompt Snippet
```text
Given an encoded Spark DataFrame `encodedDataFrame` and geometry column `"geometry"`, decode it using:
SpatialParquetSource.decodeSpatialParquet(encodedDataFrame, "geometry")
```

### Common Failure Modes
- Passing a regular (non-SpatialParquet-encoded) DataFrame and expecting decode semantics to work.
- Using a `geomColumnName` that does not exist in the DataFrame schema.
- Calling with wrong receiver/call shape (e.g., unqualified bare call) when `SpatialParquetSource` is not in scope.

### Fix Code Hint
```scala
val encodedDataFrame = SpatialParquetSource.encodeSpatialParquet(dataframe)
val decodedDataFrame = SpatialParquetSource.decodeSpatialParquet(encodedDataFrame, "geometry")
```

## API Test: `decompress`

### Signature
```scala
protected def decompress: Unit
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/MemoryTile.scala:231_

### Goal
Decompress a `MemoryTile`’s internally compressed pixel storage so pixel reads/writes can proceed on the in-memory tile representation.

### Parameters
_None._

### Input
Caller must have a `MemoryTile` instance (e.g., `tile`) and invoke the method on that receiver.

Preconditions grounded by available usage/context:
- Call form is instance-style on `MemoryTile` (same style as tested sibling `compress`: `tile.compress`).
- This is an internal tile-level API (`protected`), not a public Spark/RDPro raster pipeline entrypoint.
- No file path, raster format, or Spark I/O input is passed directly to this method.

### Output
Returns `Unit` — it produces no direct value; it mutates/updates internal tile state (decompressed in-memory pixel data).

### Valid Call Patterns
```scala
// Inferred from signature + tested sibling call style on MemoryTile (`tile.compress`)
tile.decompress
```

### LLM Instruction Prompt
- Use instance receiver form on a `MemoryTile` object: `value.decompress`.
- Do not add parameters (method takes none).
- Do not present this as a public top-level RDPro API; it is `protected` and typically used within class/subclass scope.
- If you need a publicly demonstrated pattern, only sibling `tile.compress` is directly tested; `decompress` call form here is inferred from signature.

### Prompt Snippet
```text
Given a MemoryTile instance `tile`, call decompression with no arguments using instance syntax:

tile.decompress

Do not pass parameters and do not call it as a static/object method.
```

### Common Failure Modes
- Calling with arguments, e.g. `tile.decompress(...)` (invalid; no params).
- Calling as a static/object method (no such API fact provided).
- Trying to invoke from unrelated code where `protected` visibility is not accessible.

### Fix Code Hint
```scala
// Correct shape: no args, instance receiver
tile.decompress
```

## API Test: `decompressDatasetFiles`

### Signature
```scala
private[dataExplorer] def decompressDatasetFiles(): Unit
```
_Source: beast/dataExplorer/src/main/scala/edu/ucr/cs/bdlab/beast/dataExplorer/DatasetProcessor.scala:195_

_Source doc:_ Decompresses dataset files that are stored locally. Specifically, it decompress any ZIP files found in the dataset's path. It deletes those ZIP files and finally updates the dataset's status in the database after decompression.

### Goal
Decompress locally stored dataset ZIP files inside a dataset’s directory, remove the ZIP archives, and update the dataset status in the backing database as part of the Data Explorer ingestion flow.

### Parameters
_None._

### Input
A `DatasetProcessor` instance that is already initialized with:
- a valid dataset entry in the database, and
- a local dataset path containing downloaded files.

From the test-backed usage pattern, this method is called after `copyDataToLocal()`, so the dataset’s local `download` directory already exists and contains a ZIP file.

File format scope for this method (per source doc): ZIP archives found in the dataset path.

Preconditions from the validated call flow:
- JDBC connection is active and DB schema exists (`DatasetProcessor.createDB(...)` is called in test setup).
- Dataset record exists in `datasets` table.
- Local filesystem dataset directory has been created/populated (e.g., via `datasetProcessor.copyDataToLocal()`).

### Output
Returns `Unit` — no Scala value is returned.  
Effect: performs side effects (decompression of ZIP files, deletion of those ZIP files, and dataset-status update in DB).

### Valid Call Patterns
```scala
datasetProcessor.decompressDatasetFiles()
```

### LLM Instruction Prompt
- Call this method as an instance method on an existing `DatasetProcessor`: `datasetProcessor.decompressDatasetFiles()`.
- Do not pass arguments (the signature has no parameters).
- Use it in the dataset-ingestion sequence after local copy/download is complete.
- Do not expect a return value; verify results via filesystem/DB state instead.

### Prompt Snippet
```text
Given an initialized DatasetProcessor named datasetProcessor, and after copying data locally, run:
datasetProcessor.decompressDatasetFiles()
This method takes no arguments and returns Unit; it performs side effects (unzip local dataset ZIPs, delete ZIP files, update DB status).
```

### Common Failure Modes
- Calling it before local data is copied/downloaded, so no ZIP files are available in the dataset path.
- Calling it without a properly initialized DB/dataset row, so status update cannot be completed.
- Treating it as a public general API from arbitrary packages: it is `private[dataExplorer]` and intended for Data Explorer–scoped code.

### Fix Code Hint
```scala
// Ensure DB and dataset are initialized, then copy local data first
datasetProcessor.copyDataToLocal()

// Then decompress local ZIP dataset files
datasetProcessor.decompressDatasetFiles()
```

## API Test: `diagonal`

### Signature
```scala
def diagonal(cardinality: Long, percentage: Double = 0.5, buffer: Double = 0.2): JavaSpatialRDD
def diagonal(cardinality: Long, percentage: Double = 0.5, buffer: Double = 0.2): SpatialRDD
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/generator/JavaSpatialGeneratorBuilder.scala:106  (+1 more definition site/overload)_

_Source doc:_ Generate diagonally distributed data @param cardinality the number of records to generate @param percentage the percentage of records exactly on the diagonal line @param buffer the buffer around the diagonal line in which records can be generated @return the RDD that contains the generated data

### Goal
Generate synthetic spatial records with a diagonal distribution pattern for Spark-scale geospatial testing and analytics workflows.

### Parameters
- `cardinality` (`Long`): the number of records to generate.
- `percentage` (`Double`), default `0.5`: the percentage of records generated exactly on the diagonal line.
- `buffer` (`Double`), default `0.2`: the buffer around the diagonal line within which records can be generated.

### Input
No raster/vector file input is required.  
You call this on a spatial data generator builder receiver (as documented), typically from a Spark context (`sc.generateSpatialData`), with numeric generation controls:

- `cardinality`: required record count.
- `percentage` and `buffer`: optional controls for how tightly data follows a diagonal pattern.

From the provided sources, no additional hard validation limits (e.g., numeric ranges) are explicitly documented for `percentage`/`buffer`; only their meanings are documented.

### Output
Returns `JavaSpatialRDD` (Scala overload returns `SpatialRDD`) containing the generated synthetic spatial data records in an RDD form suitable for downstream Beast/Spark spatial operations.

### Valid Call Patterns
```scala
sc.generateSpatialData
  .diagonal(1000, percentage = 0.3, buffer = 0.2)
  .plotImage(300, 300, "diagonal.png",
    opts = Seq(GeometricPlotter.PointSize -> 0))
```

### LLM Instruction Prompt
- Call `diagonal` as an instance method on the generator receiver, preserving the documented receiver form: `sc.generateSpatialData.diagonal(...)`.
- Use argument order and names exactly as documented: `(cardinality, percentage, buffer)`.
- Do not invent extra parameters or alternate return types.
- If you need defaults, omit `percentage` and/or `buffer` rather than fabricating values.
- Treat output as a spatial RDD for downstream operations (e.g., plotting or spatial analytics).

### Prompt Snippet
```text
Use RDPro/Beast Scala API to generate synthetic diagonal spatial data from the documented receiver:
sc.generateSpatialData.diagonal(cardinality, percentage, buffer).
Do not add extra arguments. Then run downstream operations on the returned SpatialRDD/JavaSpatialRDD.
```

### Common Failure Modes
- Calling `diagonal(...)` as a bare function without a generator receiver, which typically will not compile.
- Using a non-`Long` value for `cardinality` in strict typed Scala code.
- Assuming undocumented constraints or behavior (range checks, geometry subtype guarantees) that are not specified in the provided API facts.

### Fix Code Hint
```scala
val diagonalData: SpatialRDD =
  sc.generateSpatialData.diagonal(1000L, percentage = 0.3, buffer = 0.2)
```

## API Test: `distribution`

### Signature
```scala
def distribution(distribution: DistributionType): JavaSpatialGeneratorBuilder
def distribution(distribution: DistributionType): SpatialGeneratorBuilder
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/generator/JavaSpatialGeneratorBuilder.scala:55  (+1 more definition site/overload)_

_Source doc:_ Set the distribution of the generated data @param distribution the distributed of the generated data as one of {[[UniformDistribution]], [[DiagonalDistribution]], [[GaussianDistribution]], [[BitDistribution]], [[SierpinskiDistribution]], [[ParcelDistribution]]} @return

### Goal
Selects the spatial distribution model used by Beast/RDPro synthetic spatial data generation before calling `generate(...)`.

### Parameters
- `distribution` (`DistributionType`): the generator distribution to use, documented as one of `UniformDistribution`, `DiagonalDistribution`, `GaussianDistribution`, `BitDistribution`, `SierpinskiDistribution`, or `ParcelDistribution`.

### Input
- Receiver must be a spatial generator builder (as shown in project usage: `sc.generateSpatialData`).
- No raster file input is required by this method itself; it configures synthetic feature generation.
- Preconditions:
  - Pass a valid `DistributionType` value (from the documented set above).
  - Use this in a builder chain, typically followed by `.config(...)` and `.generate(cardinality=...)` (or sibling convenience calls like `.uniform(...)` shown in tests).

### Output
Returns `JavaSpatialGeneratorBuilder` — a builder object representing the same generator pipeline with the distribution setting applied, so you can continue chaining configuration and generation calls.

### Valid Call Patterns
```scala
import edu.ucr.cs.bdlab.beast._
import edu.ucr.cs.bdlab.beast.generator._

val randomBoxes: RDD[IFeature] = sc.generateSpatialData
  .distribution(GaussianDistribution)
  .config(UniformDistribution.GeometryType, "box")
  .config(UniformDistribution.MaxSize, "0.01,0.01")
  .generate(cardinality=10000000)

val randomPolygons: RDD[IFeature] = sc.generateSpatialData
  .distribution(BitDistribution)
  .config(UniformDistribution.GeometryType, "polygons")
  .config(UniformDistribution.NumSegments, "20")
  .generate(cardinality=10000000)
```

### LLM Instruction Prompt
- Call it as an instance method on a builder receiver exactly like `sc.generateSpatialData.distribution(...)`.
- Provide only a documented `DistributionType` constant.
- Keep chaining on the returned builder (`config`, then `generate`), do not treat `distribution(...)` as terminal output.

### Prompt Snippet
```text
Use Beast spatial data generator builder style:
sc.generateSpatialData
  .distribution(GaussianDistribution)
  .config(...)
  .generate(cardinality=...)
Only pass a documented DistributionType.
```

### Common Failure Modes
- Passing something that is not a `DistributionType` to `distribution(...)`.
- Calling `distribution(...)` as a standalone function without a builder receiver.
- Expecting `distribution(...)` to return generated data directly; it returns a builder, so generation still requires a later call such as `generate(...)`.

### Fix Code Hint
```scala
import edu.ucr.cs.bdlab.beast._
import edu.ucr.cs.bdlab.beast.generator._

val generated: RDD[IFeature] = sc.generateSpatialData
  .distribution(UniformDistribution)
  .generate(cardinality=1000)
```

## API Test: `divideScene`

### Signature
```scala
def divideScene[T: ClassTag](raster: RasterRDD[T], targetMetadata: RasterMetadata, numTilesX: Int, numTilesY: Int): RasterRDD[T]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsFocal.scala:625_

_Source doc:_ Divides an existing RDD into a new RDD such that every group of tiles is brought together into one Metadata. This is helpful when writing the resulting RDD to files because each group of tiles will be written to a separate file. @param raster the input raster to repartition @param targetMetadata the metadata of the target (output) raster @param numTilesX number of tiles to combine together into one metadata @param numTilesY number of tiles to combine together into one metadata @tparam T @return

### Goal
Repartition a raster scene into grouped output tile metadata so tiles are reorganized for downstream distributed writing (for example, controlling how tiles are grouped into output GeoTIFF files).

### Parameters
- `raster` (`RasterRDD[T]`): the input raster RDD to repartition/divide.
- `targetMetadata` (`RasterMetadata`): metadata describing the target output raster layout used for the scene division.
- `numTilesX` (`Int`): number of tiles to combine together along the X direction into one metadata group.
- `numTilesY` (`Int`): number of tiles to combine together along the Y direction into one metadata group.

### Input
You must provide an in-memory raster as `RasterRDD[T]` plus a target `RasterMetadata` and grouping sizes (`numTilesX`, `numTilesY`).

Preconditions and compatibility guidance from project context:
- Use the correct pixel type `T` when creating/loading rasters (typed load rule is critical in RDPro, e.g., `sc.geoTiff[Int]`, `sc.geoTiff[Float]`, etc.).
- `targetMetadata` should represent the intended output raster grid/layout for the divided scene.
- If your workflow mixes rasters with different layout/CRS/resolution, first make them compatible using reshape/reproject operations before downstream combine/write steps.
- No file path is passed to `divideScene`; file formats (GeoTIFF/HDF input, GeoTIFF output) apply to load/save operations around this API, not to this call itself.

### Output
Returns `RasterRDD[T]` — a new raster RDD with the same pixel value type, but reorganized according to `targetMetadata` and the tile-grouping factors (`numTilesX`, `numTilesY`) so grouped tiles can be written separately.

### Valid Call Patterns
```scala
val outputRaster = RasterOperationsFocal.divideScene(raster, targetMetadata, 2, 2)
```

### LLM Instruction Prompt
- Call the method with this exact receiver form: `RasterOperationsFocal.divideScene(raster, targetMetadata, numTilesX, numTilesY)`.
- Do not invent extra arguments or overloads (none are documented).
- Keep `raster` as `RasterRDD[T]` and keep `T` consistent with upstream typed raster loading/creation.
- Provide a valid `RasterMetadata` for the target layout before calling.
- Use positive integer grouping factors for `numTilesX` and `numTilesY`.

### Prompt Snippet
```text
Given a RasterRDD[T] named raster and a RasterMetadata named targetMetadata, divide the scene using:
RasterOperationsFocal.divideScene(raster, targetMetadata, numTilesX, numTilesY).
Keep T unchanged from the input raster pixel type, and do not add any extra parameters.
```

### Common Failure Modes
- Using the wrong pixel type upstream (for example, loading GeoTIFF with mismatched `T`) and then passing that raster through this pipeline.
- Passing a `targetMetadata` that does not reflect the intended output grid/layout.
- Providing invalid grouping factors (e.g., non-positive `numTilesX`/`numTilesY`).
- Assuming this API reads/writes files directly; it only transforms raster partition/layout in-memory.

### Fix Code Hint
```scala
// Ensure raster is correctly typed and target metadata is explicitly defined first
val outputRaster: RasterRDD[Int] =
  RasterOperationsFocal.divideScene(raster, targetMetadata, 2, 2)

// Then write with RDPro writer API if needed
// outputRaster.saveAsGeoTiff("output_path")
```

## API Test: `encodeGeoParquet`

### Signature
```scala
def encodeGeoParquet(dataframe: DataFrame): DataFrame
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/SpatialParquetSource.scala:99_

_Source doc:_ Encode the given DataFrame into GeoParquet format by replacing the geometry column with two new columns, MBR and the WKB representation of the geometry. @param dataframe @return

### Goal
Encode a spatial Spark `DataFrame` into a GeoParquet-style tabular representation by replacing geometry with MBR columns plus WKB geometry bytes.

### Parameters
- `dataframe` (`DataFrame`): Input Spark SQL DataFrame that contains a geometry column to be encoded.

### Input
A Spark `DataFrame` containing spatial features (e.g., loaded from GeoJSON in Beast/Spark), with a geometry column present for encoding.

Preconditions from verified usage:
- The call form is a static/object call on `SpatialParquetSource`.
- The input must be a spatial DataFrame with geometry data; otherwise geometry encoding is not meaningful.
- In tested decode flow, geometry-related MBR columns are named with a geometry-prefix pattern such as `geometry_minx`, `geometry_miny`, `geometry_maxx`, `geometry_maxy`.

### Output
Returns `DataFrame` — an encoded DataFrame where geometry is represented in GeoParquet-compatible form using MBR columns and WKB representation (per source doc), suitable for later decoding (e.g., with `decodeGeoParquet`).

### Valid Call Patterns
```scala
val input = locateResource("/allfeatures.geojson")
val dataframe = sparkSession.read.format("geojson").load(input.getPath)
val encodedDataFrame = SpatialParquetSource.encodeGeoParquet(dataframe)
```

### LLM Instruction Prompt
- Use the exact receiver/qualifier: `SpatialParquetSource.encodeGeoParquet(dataframe)`.
- Pass exactly one argument of type `DataFrame`.
- Do not invent extra parameters (e.g., geometry column name); this method accepts only `dataframe`.
- Use this method when converting spatial DataFrames to encoded geometry form (MBR + WKB), and pair with `decodeGeoParquet` when round-tripping.

### Prompt Snippet
```text
Given a Spark DataFrame with geometries, call SpatialParquetSource.encodeGeoParquet(dataframe) to encode geometry into GeoParquet-style columns (MBR + WKB). Do not add any extra arguments.
```

### Common Failure Modes
- Calling with a non-spatial DataFrame that lacks geometry content expected by the encoder.
- Using an incorrect call shape (e.g., bare `encodeGeoParquet(...)` without `SpatialParquetSource` qualifier in this context).
- Assuming this API takes a geometry-column-name argument (it does not, based on the signature).

### Fix Code Hint
```scala
// Ensure you start from a spatial DataFrame
val dataframe = sparkSession.read.format("geojson").load(inputPath)

// Correct call shape (authoritative from tests)
val encodedDataFrame = SpatialParquetSource.encodeGeoParquet(dataframe)
```

## API Test: `encodeGeometry`

### Signature
```scala
private def encodeGeometry(geometry: Geometry, featureBuilder: Feature.Builder): Unit
private def encodeGeometry(geometry: LiteGeometry, featureBuilder: Feature.Builder): Unit
def encodeGeometry(geometry: Geometry): Seq[InternalRow]
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/VectorLayerBuilder.scala:194  (+2 more definition site/overload)_

_Source doc:_ Encodes a geometry into the given feature @param geometry the geometry to encode @param featureBuilder the feature builder to encode to

### Goal
Encode a JTS geometry into Beast’s internal row-based geometry representation for downstream Spark/SpatialParquet processing.

### Parameters
- `geometry` (`Geometry`): The input JTS geometry to encode (e.g., point or linestring as shown by tests).
- `featureBuilder` (`Feature.Builder`): A mutable builder that receives the encoded geometry fields (used by the private overloads).

### Input
Caller must provide a valid geometry object.  
From verified tests, `SpatialParquetHelper.encodeGeometry(geometry: Geometry)` accepts JTS geometries and returns encoded rows for:
- `Point`
- `LineString`

No file-format input is required by this function directly.  
Preconditions explicitly documented for raster APIs (typed `geoTiff[T]`, raster metadata alignment, etc.) do **not** apply to this geometry encoder.

### Output
Returns `Unit` — the private overload writes encoded geometry into the provided `Feature.Builder` (side-effect only, no standalone return value).

### Valid Call Patterns
```scala
val point = geometryFactory.createPoint(new Coordinate(5.5, 3.4))
val encoded: Seq[InternalRow] = SpatialParquetHelper.encodeGeometry(point)

val linestring = geometryFactory.createLineString(createCS(5.5, 3.4, 10.2, 5.1, 1.2, 2.1))
val encoded2: Seq[InternalRow] = SpatialParquetHelper.encodeGeometry(linestring)
```

### LLM Instruction Prompt
- Use the tested public call shape exactly: `SpatialParquetHelper.encodeGeometry(geometry)`.
- Pass a JTS `Geometry` instance.
- Do not call the private overloads unless you are inside the defining class/object scope.
- Do not invent extra parameters or return types.

### Prompt Snippet
```text
Given a JTS Geometry, call SpatialParquetHelper.encodeGeometry(geometry) and handle the Seq[InternalRow] result. Do not add any extra arguments.
```

### Common Failure Modes
- Calling a private overload from outside its declaring scope:
  - `encodeGeometry(geometry, featureBuilder)` is private and not generally accessible.
- Using an unqualified or wrong receiver:
  - Verified receiver is `SpatialParquetHelper.encodeGeometry(...)`.
- Assuming unsupported return type:
  - Public tested overload returns `Seq[InternalRow]`; private overloads return `Unit`.

### Fix Code Hint
```scala
// ✅ Public, tested usage
val geom: Geometry = geometryFactory.createPoint(new Coordinate(5.5, 3.4))
val rows: Seq[InternalRow] = SpatialParquetHelper.encodeGeometry(geom)

// ⛔ Avoid from external code (private):
// encodeGeometry(geom, featureBuilder)
```

## API Test: `encodeSpatialParquet`

### Signature
```scala
def encodeSpatialParquet(dataframe: DataFrame): DataFrame
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/SpatialParquetSource.scala:81_

_Source doc:_ Parses an existing DataFrame according to the given options that determine the format of the spatial attributes. @param dataframe an existing dataframe @return a dataframe that parses and replaces the spatial attributes with a geometry column

### Goal
Convert an existing Spark `DataFrame` with spatial attributes into a spatial-parquet-encoded form where spatial attributes are parsed and represented as a geometry column.

### Parameters
- `dataframe` (`DataFrame`): an existing Spark DataFrame to be parsed for spatial attributes and transformed into encoded spatial parquet representation.

### Input
A Spark SQL `DataFrame` that already exists in memory (for example, loaded from GeoJSON as shown in tests).  
Known validated call flow from tests:

- Read spatial data into a `DataFrame`
- Call `SpatialParquetSource.encodeSpatialParquet(dataframe)`

Preconditions from available facts:

- The input must be a valid Spark `DataFrame`.
- Spatial attributes must be in a form that `encodeSpatialParquet` can parse according to configured options (exact option names/values are not documented in the provided facts).
- No additional parameters are accepted by this function (only `dataframe`).

### Output
Returns `DataFrame` — a transformed DataFrame where spatial attributes are parsed/encoded for Spatial Parquet use, with spatial attributes replaced by a geometry column (per source doc wording).

### Valid Call Patterns
```scala
val input = locateResource("/allfeatures.geojson")
val dataframe = sparkSession.read.format("geojson").load(input.getPath)
val encodedDataFrame = SpatialParquetSource.encodeSpatialParquet(dataframe)
```

### LLM Instruction Prompt
- Call this API with exactly one argument: a Spark `DataFrame`.
- Preserve receiver/qualifier exactly as validated: `SpatialParquetSource.encodeSpatialParquet(dataframe)`.
- Do not invent extra parameters (e.g., geometry column name, CRS, options map) for this method.
- If decode/round-trip is needed, use `SpatialParquetSource.decodeSpatialParquet(encodedDataFrame, "geometry")` separately (as shown in tests), not as extra args here.

### Prompt Snippet
```text
Given an existing Spark DataFrame that contains spatial attributes, call
SpatialParquetSource.encodeSpatialParquet(dataframe)
to parse/encode spatial attributes into geometry-column-based spatial parquet form.
Pass only the DataFrame argument.
```

### Common Failure Modes
- Passing anything other than a Spark `DataFrame` (type mismatch).
- Assuming this function accepts additional options/column-name arguments (it does not in the provided signature).
- Providing a DataFrame whose spatial attributes are not parseable under current spatial parsing options (exact option configuration is not documented in provided facts).

### Fix Code Hint
```scala
// Ensure you start from an existing DataFrame, then call encode with one argument
val dataframe = sparkSession.read.format("geojson").load(inputPath)
val encodedDataFrame = SpatialParquetSource.encodeSpatialParquet(dataframe)
```

## API Test: `end`

### Signature
```scala
def end: Long
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/SpatialFilePartition2.scala:26_

### Goal
Return the partition’s end position as a `Long` value (inferred from the signature; no RDPro README/test usage is provided for this method).

### Parameters
_None._

### Input
`end` takes no arguments and is called on an existing object instance that defines this method (likely a spatial file partition object, based on source path/class name).  
No file format input is passed directly to this call.

Preconditions from available docs for raster/vector compatibility (CRS/resolution/tile-size alignment, typed `geoTiff[T]` loading, etc.) are **not specifically documented for this method**.

### Output
Returns `Long` — a numeric end value from the receiver object, represented as a Scala `Long`.

### Valid Call Patterns
```scala
value.end
```
(Inferred from the signature `def end: Long`; no verified test-suite or README call example exists for this API.)

### LLM Instruction Prompt
- Call it as a parameterless member access on an instance (`value.end`), not as a standalone function.
- Do not add arguments.
- Do not assume units/semantics beyond “end value” unless additional type/context is available in user code.

### Prompt Snippet
```text
Given an instance `value` that has method `def end: Long`, read its end position using `value.end` and store/print the returned Long.
```

### Common Failure Modes
- Calling `end` without a receiver in scope (e.g., `end`) when no such symbol exists.
- Calling `end` on a type that does not define this method.
- Assuming undocumented semantics (e.g., byte offset vs index vs inclusive/exclusive boundary) without checking surrounding API/type docs.

### Fix Code Hint
```scala
// Ensure you have an instance that defines `def end: Long`
val e: Long = value.end
println(e)
```

## API Test: `envelope`

### Signature
```scala
def envelope: java.awt.Rectangle
override def envelope: java.awt.Rectangle
def envelope: Envelope
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/LiteGeometry.scala:24  (+4 more definition site/overload)_

### Goal
Return the bounding envelope (spatial extent) of the current geometry/raster-related object in model space.

### Parameters
_None._

### Input
Call `envelope` on an existing object instance that defines this method (no direct file-format argument is passed to `envelope` itself).

From the provided sources, a verified call form is:
- `Reprojector.reprojectEnvelopeInPlace(envelope, 4326, 3857)` where `envelope` is an array of four coordinates (`Array(-180.0, 0, 0, 90)`), showing envelope values are used as spatial bounds and may be transformed/restricted to valid CRS extents.

Related project preconditions that matter when envelope values are used in raster workflows:
- If combining rasters (e.g., overlay/join-like operations), metadata compatibility is required (resolution, CRS, tile size). If not compatible, reshape/reproject first.
- CRS consistency is critical before interpreting/combining envelope extents.

### Output
Returns `java.awt.Rectangle` — a rectangular bounding box of the object extent.  
Also documented with `def envelope: Envelope`, i.e., an envelope/bounds object representing raster-data boundaries in model space.

### Valid Call Patterns
```scala
val envelope = Array(-180.0, 0, 0, 90)
Reprojector.reprojectEnvelopeInPlace(envelope, 4326, 3857)
```

### LLM Instruction Prompt
- Use `envelope` as a zero-argument member (`obj.envelope`), not a free function with arguments.
- Do not invent parameters for `envelope`; API facts list none.
- Treat output as a bounds object (`java.awt.Rectangle` or `Envelope` depending on implementing type).
- Before using envelope values across datasets, ensure CRS/metadata compatibility (reshape/reproject when needed).

### Prompt Snippet
```text
Get bounds by calling the instance member with no arguments: `value.envelope`.
Do not pass parameters. Use the returned rectangle/envelope as model-space extent.
If mixing datasets, align CRS/resolution/tile metadata first (reproject/reshape).
```

### Common Failure Modes
- Calling `envelope(...)` with arguments (invalid; method takes no parameters).
- Assuming a single concrete return class everywhere; documented overloads include both `java.awt.Rectangle` and `Envelope`.
- Using envelope extents across mismatched CRS/metadata without prior alignment, causing incorrect spatial results.

### Fix Code Hint
```scala
// Correct: zero-argument instance-style usage pattern
// (replace `value` with the concrete object that provides `envelope`)
val bounds = value.envelope

// If you need CRS-aligned numeric bounds, reproject envelope coordinates explicitly
val envelope = Array(-180.0, 0, 0, 90)
Reprojector.reprojectEnvelopeInPlace(envelope, 4326, 3857)
```

## API Test: `eulerHistogramCount`

### Signature
```scala
def eulerHistogramCount(histogramSize: Array[Int], prefixSum: Boolean = false): AbstractHistogram
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/CGOperationsMixin.scala:98_

_Source doc:_ Computes an Euler histogram that works better for geometries with extents, i.e., envelopes, which calculates the number of records in each cell @param histogramSize the size of the histogram as the number of partitions along each dimension @param prefixSum     compute the prefix sum on the result to speed up range tests @return the created histogram

### Goal
Compute an Euler count histogram over spatial geometries (especially extent/envelope-like geometries) to estimate how many records fall in each grid cell, with an optional prefix-sum form for faster range tests.

### Parameters
- `histogramSize` (`Array[Int]`): the histogram grid size as partition counts along each dimension (for example, 2D grids such as `Array(100, 100)`).
- `prefixSum` (`Boolean`), default `false`: if `true`, computes a prefix-sum histogram to speed up range tests; if `false`, returns the direct Euler count histogram.

### Input
Call this on a spatial dataset receiver (as shown in project usage: `polygons.eulerHistogramCount(...)`) that already exists in memory as an RDD-like Beast spatial collection.

Preconditions from available docs:
- The call form is instance-style on the dataset (`value.eulerHistogramCount(...)`), not a standalone function call.
- `histogramSize` must match the dimensionality of the spatial data (the API describes “along each dimension”).
- No file format is passed directly to this method; loading/parsing data (e.g., shapefile/GeoJSON/CSV-WKT) is done beforehand using Beast I/O APIs.

### Output
Returns `AbstractHistogram`, an in-memory histogram object representing Euler-based per-cell record counts over the specified grid; when `prefixSum = true`, it represents the prefix-summed version intended to accelerate range tests.

### Valid Call Patterns
```scala
val eulerCountHistogram = polygons.eulerHistogramCount(Array(100, 100))
```

### LLM Instruction Prompt
- Use the instance receiver form exactly (`value.eulerHistogramCount(...)`), consistent with documented usage.
- Pass `histogramSize` as `Array[Int]` with one entry per dimension.
- Only pass `prefixSum` as a Boolean when needed; otherwise rely on the default `false`.
- Do not invent extra parameters, overloads, or return types.

### Prompt Snippet
```text
Given a spatial dataset `polygons`, compute an Euler count histogram on a 2D 100x100 grid using:
`polygons.eulerHistogramCount(Array(100, 100))`.
If I need faster range tests, call:
`polygons.eulerHistogramCount(Array(100, 100), prefixSum = true)`.
```

### Common Failure Modes
- Calling it as a top-level function (`eulerHistogramCount(...)`) instead of on a spatial dataset receiver.
- Passing a non-`Array[Int]` histogram size.
- Using a `histogramSize` that does not align with dataset dimensionality.
- Expecting file output directly from this API (it returns `AbstractHistogram` in memory).

### Fix Code Hint
```scala
// Correct: instance-style call on an existing spatial dataset
val eulerCountHistogram = polygons.eulerHistogramCount(Array(100, 100))

// Optional prefix-sum variant for faster range tests
val eulerCountPrefix = polygons.eulerHistogramCount(Array(100, 100), prefixSum = true)
```

## API Test: `eulerHistogramSize`

### Signature
```scala
def eulerHistogramSize(histogramSize: Array[Int], prefixSum: Boolean = false, sizeFunction: IFeature => Int = _.getStorageSize): AbstractHistogram
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/CGOperationsMixin.scala:109_

_Source doc:_ Computes an Euler histogram that works better for geometries with extents, i.e., envelopes, which calculates the total size of features in each cell @param histogramSize the size of the histogram as the number of partitions along each dimension @param prefixSum     compute the prefix sum on the result to speed up range tests @return the created histogram

### Goal
Compute an Euler histogram over spatial features where each cell stores accumulated feature **size** (not just count), which is useful for extent-based geometries such as envelopes.

### Parameters
- `histogramSize` (`Array[Int]`): Number of histogram partitions along each dimension (grid shape).
- `prefixSum` (`Boolean`), default `false`: If `true`, computes a prefix-sum version of the histogram to speed up range tests.
- `sizeFunction` (`IFeature => Int`), default `_.getStorageSize`: Function used to compute each feature’s contribution to cell totals.

### Input
Call this on a spatial feature dataset receiver (per documented usage: `polygons.eulerHistogramSize(...)`), where elements are `IFeature`-compatible.  
No file-format-specific requirement is defined by this method itself; input format handling happens when loading the dataset (e.g., shapefile/GeoJSON/CSV-WKT via Beast APIs).  
Preconditions on CRS/resolution alignment are **not specified** for this API in the provided facts.

### Output
Returns `AbstractHistogram` — an in-memory histogram object representing per-cell aggregated feature size (optionally in prefix-sum form when `prefixSum = true`).

### Valid Call Patterns
```scala
val eulerCountHistogram = polygons.eulerHistogramCount(Array(100, 100))
val eulerSizeHistogram = polygons.eulerHistogramSize(Array(100, 100))
```

### LLM Instruction Prompt
- Use the instance-style receiver form shown in docs: `value.eulerHistogramSize(...)`.
- Pass `histogramSize` as `Array[Int]`.
- Only use optional args from the signature: `prefixSum` and `sizeFunction`.
- Do not invent extra parameters or alternate return types.

### Prompt Snippet
```text
Given a spatial feature dataset (e.g., polygons), call:
polygons.eulerHistogramSize(Array(100, 100))
Optionally set prefixSum=true for range-test optimization, and optionally pass sizeFunction: IFeature => Int.
```

### Common Failure Modes
- Passing a non-`Array[Int]` grid size.
- Calling as a bare function (`eulerHistogramSize(...)`) instead of on a dataset receiver (`polygons.eulerHistogramSize(...)`).
- Supplying a `sizeFunction` with the wrong type (must be `IFeature => Int`).

### Fix Code Hint
```scala
val eulerSizeHistogram: AbstractHistogram =
  polygons.eulerHistogramSize(
    histogramSize = Array(100, 100),
    prefixSum = false,
    sizeFunction = _.getStorageSize
  )
```

## API Test: `explode`

### Signature
```scala
def explode: RasterRDD[T]
def explode[T](inputRaster: RasterRDD[T]): RasterRDD[T]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsLocal.scala:76  (+1 more definition site/overload)_

_Source doc:_ Returns a new RasterRDD where each tile is in its own raster. @param inputRaster the raster data to explore @tparam T @return a new raster RDD with the same number of tiles but each tile is in a separate raster

### Goal
Split a `RasterRDD[T]` so each tile becomes its own raster metadata context, which is useful before downstream tile-wise raster processing.

### Parameters
- `inputRaster` (`RasterRDD[T]`): the input raster dataset to explode; it contains tiles that may currently share the same raster metadata.

### Input
`explode` takes an in-memory `RasterRDD[T]` (for example, loaded from GeoTIFF/HDF through RDPro, or produced by another raster operation).  
Preconditions and compatibility rules to keep this valid in RDPro pipelines:

- `T` must match the raster pixel type used earlier in the pipeline (for example, the documented typed-load rule for `sc.geoTiff[T]` still applies at load time).
- Input must already be a valid `RasterRDD[T]`; `explode` does not load files directly.
- No additional CRS/resolution alignment requirement is documented specifically for `explode`; those compatibility requirements are documented for operations like `overlay`/reshape, not this one.

### Output
Returns `RasterRDD[T]` — a new raster RDD with the same tiles, but arranged so each tile is in a separate raster (per source doc: same number of tiles, each tile in its own raster).

### Valid Call Patterns
```scala
val outputRaster = RasterOperationsLocal.explode(raster)
```

### LLM Instruction Prompt
- Use the tested call form exactly: `RasterOperationsLocal.explode(raster)`.
- Pass a `RasterRDD[T]` value only; do not pass paths/format options to `explode`.
- Preserve pixel type `T` from upstream load/transform steps.
- If starting from files, first load to `RasterRDD[T]` using a typed loader, then call `explode`.

### Prompt Snippet
```text
Given a RasterRDD[T] named raster, call:
val outputRaster = RasterOperationsLocal.explode(raster)
Do not pass file paths to explode; load first, then explode.
Keep T consistent with the raster’s real pixel type.
```

### Common Failure Modes
- Calling `explode` on a file path/string instead of a `RasterRDD[T]`.
- Using an inconsistent pixel type earlier (for example, wrong `sc.geoTiff[T]` type), which breaks upstream and leaves no valid `RasterRDD[T]` to explode.
- Assuming `explode` performs reprojection/resampling/alignment; it does not document those behaviors.

### Fix Code Hint
```scala
import edu.ucr.cs.bdlab.beast._

val raster: RasterRDD[Int] = sc.geoTiff[Int]("glc2000_v1_1.tif")
val outputRaster: RasterRDD[Int] = RasterOperationsLocal.explode(raster)
```

## API Test: `extents`

### Signature
```scala
def extents: Geometry
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/RasterMetadata.scala:181  (+1 more definition site/overload)_

_Source doc:_ The extents of the RasterMetadata in model space as a rectangular polygon @return

### Goal
Get the raster tile/metadata boundary in model (map) coordinates as a rectangular polygon `Geometry`.

### Parameters
_None._

### Input
Call this on an existing raster metadata/tile context object that provides `extents` (in practice, the same receiver style as other `RasterMetadata` methods like `metadata.gridToModel(...)` and `metadata.modelToGrid(...)` in tests).  
No file path or format is passed directly to `extents`; the raster must already be loaded/read so metadata exists.

### Output
Returns `Geometry` — a polygon (rectangle) representing the boundaries of this tile in model space.

### Valid Call Patterns
```scala
// Inferred from signature; receiver style grounded by tested sibling RasterMetadata calls
val boundary: Geometry = metadata.extents
```

### LLM Instruction Prompt
- Use it as a zero-argument member access on a raster metadata/tile receiver (`value.extents`), not a standalone function call.
- Do not add parameters; signature is exactly `def extents: Geometry`.
- Treat the result as model-space boundary geometry (rectangle), not pixel indices.
- If metadata is not yet available, first load/read raster data and obtain metadata from that object.

### Prompt Snippet
```text
Given a RasterMetadata-like object `metadata`, get its model-space boundary polygon with:
`val g: Geometry = metadata.extents`
Do not pass arguments to `extents`.
```

### Common Failure Modes
- Calling `extents()` with parentheses/arguments not defined by this API.
- Calling `extents` without a valid receiver object that has raster metadata.
- Misinterpreting output as grid/pixel-space extent instead of model-space geometry.

### Fix Code Hint
```scala
// Ensure you have metadata first, then call extents with no arguments
val outPoint = new java.awt.geom.Point2D.Double
metadata.gridToModel(0, 0, outPoint)   // sibling verified call style
val boundary: Geometry = metadata.extents
```

## API Test: `extractTables`

### Signature
```scala
def extractTables(sql: String): Set[String]
```
_Source: beast/dataExplorer/src/main/scala/edu/ucr/cs/bdlab/beast/dataExplorer/SQLQueryHelper.scala:22_

_Source doc:_ Checks if an SQL query is syntactically correct and extracts table names from it. @param sql The SQL query string to be analyzed. @return Either an error message as a string if the query is incorrect, or a set of table names if the query is correct.

### Goal
Validate an SQL query string and return the set of table names referenced in that query.

### Parameters
- `sql` (`String`): The SQL query text to parse and analyze for referenced table names.

### Input
A single SQL query provided as a `String`.

Preconditions:
- The SQL must be syntactically valid; otherwise parsing fails.
- No file inputs, raster inputs, vector inputs, CRS settings, or Spark raster type-selection rules apply to this function based on the provided sources.

### Output
Returns `Set[String]` — the extracted table names from a syntactically valid SQL query.

### Valid Call Patterns
```scala
val validSQL = "SELECT * FROM users"
SQLQueryHelper.extractTables(validSQL)
```

```scala
val invalidSQL = "SELEC * FROM users"
intercept[SqlParseException] {
  SQLQueryHelper.extractTables(invalidSQL)
}
```

### LLM Instruction Prompt
- Call this API with the exact receiver form used in tests: `SQLQueryHelper.extractTables(sql)`.
- Pass one argument only: a SQL string.
- Expect a `Set[String]` for valid SQL.
- Handle parse errors for invalid SQL (tests show `SqlParseException` is thrown).

### Prompt Snippet
```text
Use SQLQueryHelper.extractTables(sqlString) to parse a SQL query and extract table names.
If the SQL is invalid, handle SqlParseException.
```

### Common Failure Modes
- Invalid SQL syntax (example: `"SELEC * FROM users"`) causes a parse exception (`SqlParseException` in tests).
- Assuming it returns an error string on invalid SQL: test behavior indicates exception-based failure instead.

### Fix Code Hint
```scala
val sql = "SELECT * FROM users"
val tables: Set[String] = SQLQueryHelper.extractTables(sql)

// Defensive handling for invalid SQL input
try {
  SQLQueryHelper.extractTables("SELEC * FROM users")
} catch {
  case e: SqlParseException =>
    // fix SQL syntax before retrying
}
```

## API Test: `filterPixels`

### Signature
```scala
def filterPixels(f: T => Boolean)
def filterPixels[T: ClassTag](inputRaster: RasterRDD[T], filter: T => Boolean): RasterRDD[T]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsLocal.scala:48  (+1 more definition site/overload)_

_Source doc:_ Retains only the pixels that pass the user-defined filter and clears all other pixels (set to empty) @param inputRaster the input raster @param filter the filter function that tells which pixel values to keep in the output @tparam T the thpe of the pixels in the input @return a new raster where only pixels that pass the test are retained

### Goal
Keep only raster pixels that satisfy a user-defined predicate (e.g., threshold or class-range mask) and set all other pixels to empty for downstream RDPro/Raptor analysis.

### Parameters
- `inputRaster` (`RasterRDD[T]`): Input raster tiles/pixels to filter.
- `filter` (`T => Boolean`): Predicate function applied per pixel value; pixels returning `true` are retained, others are cleared (empty).

### Input
`filterPixels` operates on an already loaded `RasterRDD[T]` (commonly from `sc.geoTiff[T](...)` or `sc.hdfFile(...)` in RDPro workflows).  
Preconditions and compatibility rules to respect:

- Choose the raster type parameter `T` to match the real pixel type at load time (e.g., `Int`, `Float`, `Array[Int]`, `Array[Float]` as documented for `sc.geoTiff[T]`).
- The predicate must be compatible with the pixel type `T` (e.g., numeric comparisons for numeric `T`).
- This operation filters pixel values; it does not align CRS/resolution/tile grids across datasets. If later steps require compatibility across rasters, use reshape/reproject operations first (per project rules).

### Output
Returns `RasterRDD[T]` — a new raster of the same pixel type where only pixels passing `filter` remain defined; all failing pixels are set to empty.

### Valid Call Patterns
```scala
val temperatureK: RasterRDD[Float] =
  sc.hdfFile("MOD11A1.A2022173.h08v05.006.2022174092443.hdf", "LST_Day_1km")
temperatureK.filterPixels(_>300).saveAsGeoTiff("temperature_high")
```

```scala
val raster: RasterRDD[Int] = sc.geoTiff[Int]("glc2000_v1_1.tif")
val trees = raster.filterPixels(lc => lc >=1 && lc <= 10)
val countries = sc.shapefile("ne_10m_admin_0_countries.zip")
val result = RaptorJoin.raptorJoinFeature(trees, countries, Seq())
  .map(x => x.feature.getAs[String]("NAME")).countByValue().toMap
println(result)
```

```scala
val outputRaster: RDD[ITile[Short]] = RasterOperationsLocal.filterPixels(inputRaster, (x: Short) => x < 50)
```

### LLM Instruction Prompt
- Use a real receiver form shown in project usage/tests: `raster.filterPixels(...)`, `temperatureK.filterPixels(...)`, or `RasterOperationsLocal.filterPixels(inputRaster, ...)`.
- Keep `T` consistent with the loaded raster pixel type.
- Provide a pure predicate `T => Boolean`; do not add undocumented parameters.
- Treat non-matching pixels as emptied (not “deleted rows” or “set to zero” unless zero is explicitly the empty representation, which is not specified here).

### Prompt Snippet
```text
Load raster with the correct pixel type, then call value.filterPixels(predicate) to retain only desired pixel values and clear others to empty. Keep the same RasterRDD[T] type in output.
```

### Common Failure Modes
- Loading GeoTIFF with the wrong `T` (violates typed-load rule), then writing a predicate for a different type.
- Assuming filtered-out pixels are set to a numeric constant; docs state they are set to empty.
- Using call shapes not present in docs/tests (e.g., bare `filterPixels(...)` without receiver in contexts where no implicit extension is in scope).
- Forgetting to reshape/reproject before later multi-raster operations that require matching metadata (a downstream compatibility issue).

### Fix Code Hint
```scala
import edu.ucr.cs.bdlab.beast._

val raster: RasterRDD[Int] = sc.geoTiff[Int]("glc2000_v1_1.tif")
val filtered: RasterRDD[Int] = raster.filterPixels(v => v >= 1 && v <= 10)
filtered.saveAsGeoTiff("glc_filtered")
```

## API Test: `findIntersections`

### Signature
```scala
private[davinci] def findIntersections(_x1: Double, _y1: Double, _x2: Double, _y2: Double, intersections: mutable.ArrayBuffer[(Int, Int)]): Unit
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/VectorCanvas.scala:313_

_Source doc:_ Find all intersections between the given line segment and the horizontal scan line centers @param x1 @param y1 @param x2 @param y2 @param intersections all computed intersections will be appended to this list

### Goal
Compute and append all scanline-center intersections between a given 2D line segment and the canvas scan lines, for internal rasterization/visualization logic in `davinci`.

### Parameters
- `_x1` (`Double`): X coordinate of the first endpoint of the input line segment.
- `_y1` (`Double`): Y coordinate of the first endpoint of the input line segment.
- `_x2` (`Double`): X coordinate of the second endpoint of the input line segment.
- `_y2` (`Double`): Y coordinate of the second endpoint of the input line segment.
- `intersections` (`mutable.ArrayBuffer[(Int, Int)]`): Mutable output buffer that receives all computed intersections as `(Int, Int)` pairs; new results are appended to existing contents.

### Input
This method takes in-memory numeric coordinates (no file input/output formats are involved).

Preconditions from the available facts:
- Call it on a `VectorCanvas` instance (as shown in test usage).
- Provide a mutable `ArrayBuffer[(Int, Int)]` to collect results.
- The method is `private[davinci]`, so it is intended for internal/package-scoped use within `edu.ucr.cs.bdlab.davinci`.

No additional CRS, metadata, or type-parameter selection rules are documented for this API.

### Output
Returns `Unit` — results are produced by side effect: computed intersection pairs are appended into the provided `intersections` buffer.

### Valid Call Patterns
```scala
val canvas = new VectorCanvas(new Envelope(0, 5, 0, 5),
  5, 5, 0, 5)
val intersections = new mutable.ArrayBuffer[(Int, Int)]()
canvas.findIntersections(0, 0, 3, 4, intersections)
```

### LLM Instruction Prompt
- Use the instance call form exactly as verified by tests: `canvas.findIntersections(x1, y1, x2, y2, intersections)`.
- Pass four numeric coordinates and one `mutable.ArrayBuffer[(Int, Int)]`.
- Do not expect a returned collection; read results from the same buffer argument after the call.
- Do not invent overloads or alternate parameter orders.

### Prompt Snippet
```text
Given an existing VectorCanvas `canvas`, create `val intersections = new mutable.ArrayBuffer[(Int, Int)]()`, call `canvas.findIntersections(x1, y1, x2, y2, intersections)`, then use `intersections` as the output (the method returns Unit).
```

### Common Failure Modes
- Calling it as a standalone function (`findIntersections(...)`) instead of on a `VectorCanvas` instance.
- Passing an immutable collection or wrong element type instead of `mutable.ArrayBuffer[(Int, Int)]`.
- Assuming the method returns intersections directly; it returns `Unit`.
- Accessing from outside allowed scope despite `private[davinci]`.

### Fix Code Hint
```scala
val canvas = new VectorCanvas(new Envelope(0, 5, 0, 5), 5, 5, 0, 5)
val intersections = new mutable.ArrayBuffer[(Int, Int)]()

// Correct: instance method, correct argument order/types, side-effect output
canvas.findIntersections(0.0, 0.0, 3.0, 4.0, intersections)

// intersections now contains the computed (Int, Int) pairs
```

## API Test: `findTransformationInfo`

### Signature
```scala
def findTransformationInfo(sourceCRS: CoordinateReferenceSystem, targetCRS: CoordinateReferenceSystem): TransformationInfo
def findTransformationInfo(sourceSRID: Int, targetSRID: Int): TransformationInfo
def findTransformationInfo(sourceSRID: Int, targetCRS: CoordinateReferenceSystem): TransformationInfo
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/Reprojector.scala:146  (+2 more definition site/overload)_

_Source doc:_ Creates or retrieves a cached math transform to transform between the given two CRS @param sourceCRS source coordinate reference system @param targetCRS target coordinate reference system @return the math transformation that transforms from source to destination

### Goal
Create (or reuse from cache) CRS transformation metadata (`TransformationInfo`) that converts coordinates/geometries from a source CRS to a target CRS in RDPro/Beast reprojection workflows.

### Parameters
- `sourceCRS` (`CoordinateReferenceSystem`): the input/source coordinate reference system of the geometry/raster coordinates you currently have.
- `targetCRS` (`CoordinateReferenceSystem`): the destination coordinate reference system you want to transform coordinates into.

### Input
You must provide valid CRS definitions as either:
- two CRS objects (`sourceCRS`, `targetCRS`), or
- SRID integers (`sourceSRID`, `targetSRID`), or
- one SRID and one CRS object (`sourceSRID`, `targetCRS`).

Preconditions from observed usage:
- CRS/SRID values must be valid and transformable.
- Argument order matters: source first, target second.
- This API is CRS-transform setup only; it does not read GeoTIFF/HDF/CSV files directly.

### Output
Returns `TransformationInfo` — a transformation descriptor (including math transform details) used by Beast/Reprojector to map coordinates from source CRS to destination CRS. It is suitable for downstream calls such as geometry reprojection.

### Valid Call Patterns
```scala
val transform: TransformationInfo = Reprojector.findTransformationInfo(4326, targetCRS)

val transformInfo = Reprojector.findTransformationInfo(26911, 4326)
val point = new GeometryFactory().createPoint(new Coordinate(700000,3500000))
val convertedPoint = Reprojector.reprojectGeometry(point, transformInfo)
```

### LLM Instruction Prompt
- Use `Reprojector.findTransformationInfo(...)` with the receiver exactly as shown.
- Keep source CRS/SRID as the first argument and target CRS/SRID as the second.
- Prefer overloads demonstrated in tests when possible (`Int, Int` and `Int, CoordinateReferenceSystem`).
- Do not invent extra parameters, options, or return types.

### Prompt Snippet
```text
Create a CRS transform info object using Reprojector.findTransformationInfo(source, target), with source first and target second. Use either (sourceSRID: Int, targetSRID: Int) or (sourceSRID: Int, targetCRS: CoordinateReferenceSystem) as shown in Beast tests, then pass the returned TransformationInfo to Reprojector.reprojectGeometry.
```

### Common Failure Modes
- Reversing source and target CRS/SRID, producing incorrect coordinate results.
- Passing invalid/unknown SRID values.
- Assuming this call reprojects data by itself; it only returns `TransformationInfo`.
- Using a different/unqualified call shape instead of `Reprojector.findTransformationInfo(...)` in Scala codebases where that qualifier is required.

### Fix Code Hint
```scala
// Correct: source first, target second, qualified receiver
val transformInfo = Reprojector.findTransformationInfo(26911, 4326)

val point = new GeometryFactory().createPoint(new Coordinate(700000, 3500000))
val convertedPoint = Reprojector.reprojectGeometry(point, transformInfo)
```

## API Test: `flatten`

### Signature
```scala
def flatten[T](raster: RasterRDD[T]): RDD[(Int, Int, RasterMetadata, T)]
def flatten: RDD[(Int, Int, RasterMetadata, T)]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsGlobal.scala:69  (+1 more definition site/overload)_

_Source doc:_ Extract all pixel values into an RDD @param raster the raster to extract its pixels @tparam T the type of pixel values @return an RDD that contains all pixel locations and values

### Goal
Convert a distributed raster (`RasterRDD[T]`) into a regular Spark RDD of per-pixel records `(x, y, metadata, value)` for downstream Spark transformations/aggregations.

### Parameters
- `raster` (`RasterRDD[T]`): the raster dataset whose pixels should be extracted as individual rows.

### Input
`flatten` expects a `RasterRDD[T]` that is already loaded or produced by earlier RDPro steps (for example from `sc.geoTiff[T](...)`, `sc.hdfFile(...)`, `mapPixels`, `slidingWindow`, etc.).

Preconditions and compatibility notes from project context:
- Use the correct pixel type when creating the raster (critical rule): for GeoTIFF loading, `sc.geoTiff[T]` type parameter must match the real pixel type.
- `flatten` itself does not perform CRS/resolution/tile-size harmonization; if your raster came from multi-raster operations (like `overlay`), those inputs must have been made compatible beforehand (e.g., reshape/reproject/rescale as needed).
- Input raster formats in RDPro workflows are GeoTIFF/HDF, but `flatten` operates on the in-memory `RasterRDD[T]`, not directly on file paths.

### Output
Returns `RDD[(Int, Int, RasterMetadata, T)]` — each output row contains:
1. pixel x index (`Int`)
2. pixel y index (`Int`)
3. raster metadata (`RasterMetadata`) associated with that pixel context
4. pixel value (`T`)

This is a plain Spark `RDD`, so you can use standard RDD operations (`map`, `filter`, `collectAsMap`, aggregations, joins, etc.).

### Valid Call Patterns
```scala
val finalPixels: Map[(Int, Int), Double] = RasterOperationsGlobal.flatten(smoothedRaster)
  .map(x => ((x._1, x._2), x._4))
  .collectAsMap()
  .toMap
```

### LLM Instruction Prompt
- Call form must preserve the tested receiver exactly: `RasterOperationsGlobal.flatten(smoothedRaster)`.
- Pass a `RasterRDD[T]` argument.
- Keep the tuple field order exactly as returned: `(Int, Int, RasterMetadata, T)`.
- Do not invent extra arguments/options.
- Ensure upstream raster typing is correct (`sc.geoTiff[T]` must match actual raster pixel type).

### Prompt Snippet
```text
Use RasterOperationsGlobal.flatten(rasterRDD) to extract per-pixel rows.
Input must be RasterRDD[T]. The output schema is exactly:
(Int x, Int y, RasterMetadata metadata, T value).
If raster was loaded from GeoTIFF, ensure T matches the real pixel type.
Do not add any extra parameters.
```

### Common Failure Modes
- Using the wrong generic pixel type upstream (e.g., incorrect `sc.geoTiff[T]`) leading to type/runtime issues before flatten.
- Assuming a different tuple layout/order than `(x, y, metadata, value)` and reading wrong fields.
- Calling a bare `flatten(...)` or changing receiver shape; tested portable form here is `RasterOperationsGlobal.flatten(...)`.
- Expecting `flatten` to align/reproject rasters; compatibility must be handled before producing the input `RasterRDD`.

### Fix Code Hint
```scala
import edu.ucr.cs.bdlab.beast._

// Ensure raster is correctly typed at load time
val raster: RasterRDD[Int] = sc.geoTiff[Int]("glc2000_v1_1.tif")

// Correct tested call shape
val pixels: RDD[(Int, Int, RasterMetadata, Int)] =
  RasterOperationsGlobal.flatten(raster)

// Use tuple fields in the documented order
val xyToValue: RDD[((Int, Int), Int)] = pixels.map(p => ((p._1, p._2), p._4))
```

## API Test: `gaussian`

### Signature
```scala
def gaussian(cardinality: Long): JavaSpatialRDD
def gaussian(cardinality: Long): SpatialRDD
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/generator/JavaSpatialGeneratorBuilder.scala:117  (+1 more definition site/overload)_

_Source doc:_ Generate Gaussian distributed data @param cardinality the number of records to generate @return the RDD that contains the generated data

### Goal
Generate a Spark spatial RDD of synthetic geometries/records following a Gaussian distribution, typically for spatial workload testing or demo visualization.

### Parameters
- `cardinality` (`Long`): the number of records to generate.

### Input
`gaussian` does not read raster/vector files directly; it is called on a spatial generator builder receiver.  
From documented usage, call it as an instance method on `sc.generateSpatialData`:

- Receiver must be a spatial generator builder (as in `sc.generateSpatialData`).
- `cardinality` should be a valid `Long` count of desired generated records.

No additional file-format preconditions are documented for this method.

### Output
Returns `JavaSpatialRDD` (or `SpatialRDD` in Scala overload): an RDD containing the generated Gaussian-distributed spatial data records.

### Valid Call Patterns
```scala
sc.generateSpatialData
  .gaussian(1000)
  .plotImage(300, 300, "gaussian.png",
     opts = Seq(GeometricPlotter.PointSize -> 0))
```

### LLM Instruction Prompt
- Call `gaussian` as an instance method on the generator receiver (documented form: `sc.generateSpatialData.gaussian(...)`), not as a standalone function.
- Pass exactly one argument: `cardinality: Long`.
- Treat the result as a spatial RDD for downstream Spark/Beast operations (e.g., plotting).
- Do not invent extra parameters (mean, stddev, bounds, seed) for `gaussian`; those are not in this API signature.

### Prompt Snippet
```text
Use Beast’s generator receiver form:
sc.generateSpatialData.gaussian(cardinality)

`cardinality` is the number of records to generate (Long). Do not add extra gaussian parameters.
```

### Common Failure Modes
- Calling `gaussian(...)` without a generator receiver, which usually will not compile.
- Passing a non-`Long` count in strict typed contexts.
- Assuming undocumented parameters (e.g., variance/seed) exist on `gaussian` itself.

### Fix Code Hint
```scala
val generated: SpatialRDD =
  sc.generateSpatialData
    .gaussian(1000L)
```

## API Test: `generate`

### Signature
```scala
def generate(cardinality: Long): JavaSpatialRDD
def generate(cardinality: Long): SpatialRDD
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/generator/JavaSpatialGeneratorBuilder.scala:87  (+1 more definition site/overload)_

_Source doc:_ Generate the data as an RDD. @param cardinality the number of records to generate @return the RDD that contains the generated data

### Goal
Generate synthetic spatial features as a distributed Spark RDD with exactly the requested number of records.

### Parameters
- `cardinality` (`Long`): the number of records to generate.

### Input
`generate` does not read files directly; it generates data based on the generator builder state configured before the call (for example, via `distribution(...)` and `config(...)` in the same chain).

Preconditions from documented usage:
- Call it on a configured generator receiver (for example, `sc.generateSpatialData ... .generate(...)`).
- `cardinality` should be a valid positive record count for your Spark workload size.

### Output
Returns `JavaSpatialRDD` — an RDD containing the generated spatial records (features).  
(Scala usage in README also shows assignment to `RDD[IFeature]` for generated outputs.)

### Valid Call Patterns
```scala
import edu.ucr.cs.bdlab.beast._
import edu.ucr.cs.bdlab.beast.generator._

val randomPoints: RDD[IFeature] = sc.generateSpatialData.uniform(1000000000)

val randomBoxes: RDD[IFeature] = sc.generateSpatialData
  .distribution(GaussianDistribution)
  .config(UniformDistribution.GeometryType, "box")
  .config(UniformDistribution.MaxSize, "0.01,0.01")
  .generate(cardinality=10000000)

val randomPolygons: RDD[IFeature] = sc.generateSpatialData
  .distribution(BitDistribution)
  .config(UniformDistribution.GeometryType, "polygons")
  .config(UniformDistribution.NumSegments, "20")
  .generate(cardinality=10000000)
```

### LLM Instruction Prompt
- Use the receiver-qualified form exactly (`sc.generateSpatialData ... .generate(cardinality=...)`), not a bare `generate(...)`.
- Pass `cardinality` as `Long` record count.
- Configure distribution/geometry options before calling `generate` when non-default behavior is needed.
- Do not invent extra parameters on `generate`; it only accepts `cardinality`.

### Prompt Snippet
```text
Generate synthetic spatial features with Beast by chaining from `sc.generateSpatialData`, optionally setting `.distribution(...)` and `.config(...)`, then call `.generate(cardinality=...)` with a Long count. Keep the receiver-qualified call form and do not add extra generate parameters.
```

### Common Failure Modes
- Calling `generate(...)` without the generator receiver chain (will not match the documented call style).
- Passing an invalid/non-positive cardinality for intended workload.
- Expecting file input/output behavior from `generate` itself (it produces an in-memory/distributed RDD).

### Fix Code Hint
```scala
import edu.ucr.cs.bdlab.beast._
import edu.ucr.cs.bdlab.beast.generator._

val randomBoxes: RDD[IFeature] = sc.generateSpatialData
  .distribution(GaussianDistribution)
  .config(UniformDistribution.GeometryType, "box")
  .config(UniformDistribution.MaxSize, "0.01,0.01")
  .generate(cardinality=10000000)
```

## API Test: `generateSpatialData`

### Signature
```scala
def generateSpatialData(distribution: DistributionType, cardinality: Long, numPartitions: Int = 0, opts: BeastOptions = new BeastOptions) : SpatialRDD
def generateSpatialData: SpatialGeneratorBuilder
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/ReadWriteMixin.scala:139  (+1 more definition site/overload)_

_Source doc:_ Return a [[SpatialRDD]] of randomly generated geometries according to the given options. @param distribution the type of distribution {[[UniformDistribution]], [[DiagonalDistribution]], [[GaussianDistribution]], [[SierpinskiDistribution]], [[BitDistribution]], [[ParcelDistribution]]} @param cardinality the number of geometries to generate @param opts additional options depending on the type of generator @return an RDD with the generated geometries

### Goal
Generate synthetic spatial vector data (random geometries) as a `SpatialRDD` for testing/benchmarking spatial analytics pipelines.

### Parameters
- `distribution` (`DistributionType`): distribution family used to generate geometries; documented values are `UniformDistribution`, `DiagonalDistribution`, `GaussianDistribution`, `SierpinskiDistribution`, `BitDistribution`, and `ParcelDistribution`.
- `cardinality` (`Long`): number of geometries to generate.
- `numPartitions` (`Int`), default `0`: number of Spark partitions for the generated RDD; default is `0` (library default behavior).
- `opts` (`BeastOptions`), default `new BeastOptions`: generator-specific options (for example, tests pass `seed`, `UniformDistribution.MaxSize`, and `"geometry"` through options).

### Input
No input files are required.  
Caller must provide:
- a valid `DistributionType`,
- a `cardinality`,
- optional partition count and generator options (`BeastOptions`).

Preconditions/compatibility:
- `opts` keys/values are distribution-dependent (only partially shown in provided sources).
- Real tested call form uses the Spark context receiver exactly as `sparkContext.generateSpatialData(...)`.

### Output
Returns `SpatialRDD` — an RDD of randomly generated spatial features/geometries suitable for downstream Beast spatial operations (e.g., map, join, partitioning).

### Valid Call Patterns
```scala
val firstDataset: SpatialRDD = sparkContext.generateSpatialData(distribution, 100,
  opts = Seq("seed" -> i, UniformDistribution.MaxSize -> "0.1,0.1", "geometry" -> "box"))
  .map(snapRecords)
  .zipWithUniqueId()
  .map(addRecordID)

val secondDataset: SpatialRDD = sparkContext.generateSpatialData(UniformDistribution, 100,
  opts = Seq("seed" -> (i + 1), UniformDistribution.MaxSize -> "0.1,0.1", "geometry" -> "box"))
```

### LLM Instruction Prompt
- Use the receiver-qualified call form `sparkContext.generateSpatialData(...)` (as validated in tests).
- Only use documented distribution types.
- Pass `cardinality` as `Long`-compatible numeric value.
- Treat `opts` as generator-specific; only include keys you actually know (e.g., `seed`, `UniformDistribution.MaxSize`, `"geometry"` from tests).
- Do not invent file paths or raster I/O around this API; it generates vector-like synthetic spatial features in-memory.

### Prompt Snippet
```text
Generate synthetic test features with Spark using:
sparkContext.generateSpatialData(distribution, cardinality, numPartitions = 0, opts = ...)
Use one documented distribution type (e.g., UniformDistribution), set cardinality explicitly, and keep options distribution-specific (e.g., seed, max size, geometry shape) only when known.
```

### Common Failure Modes
- Calling `generateSpatialData(...)` without the proper receiver (e.g., bare call), which may not compile in user code.
- Passing an unsupported/unknown distribution constant.
- Supplying invalid or mismatched option keys in `opts` for the chosen distribution.
- Assuming this API reads GeoTIFF/HDF or writes GeoTIFF/CSV; it does neither by itself.

### Fix Code Hint
```scala
val synthetic: SpatialRDD =
  sparkContext.generateSpatialData(
    UniformDistribution,
    100,
    opts = Seq(
      "seed" -> 1,
      UniformDistribution.MaxSize -> "0.1,0.1",
      "geometry" -> "box"
    )
  )
```

## API Test: `geoTiff`

### Signature
```scala
def geoTiff[T](path: String, iLayer: Int = 0, opts: BeastOptions = new BeastOptions): RDD[ITile[T]]
def geoTiff[T](filename: String, layer: Int, opts: BeastOptions): JavaRasterRDD[T]
def geoTiff[T](filename: String, layer: Int): JavaRasterRDD[T]
def geoTiff[T](filename: String): JavaRasterRDD[T]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RaptorMixin.scala:40  (+3 more definition site/overload)_

_Source doc:_ Loads a GeoTIFF file as an RDD of tiles @param path the path of the file @param iLayer the index of the band to load (0 by default) @param opts additional options for loading the file @return a [[RasterRDD]] that represents all tiles in the file

### Goal
Load a GeoTIFF raster band into RDPro/Beast as a distributed tiled raster (`RDD[ITile[T]]`) for Spark-based raster analytics.

### Parameters
- `path` (`String`): Path to the input GeoTIFF file to load.
- `iLayer` (`Int`), default `0`: Zero-based band index to load from the GeoTIFF.
- `opts` (`BeastOptions`), default `new BeastOptions`: Additional Beast loading options.

### Input
A GeoTIFF path (`String`) accessible to the Spark job, plus a valid band index (`iLayer`).

Preconditions and compatibility/type rules:
- Use `sc.geoTiff[T](...)` with a `T` that matches the real pixel type in the file.
- Documented type-selection examples include:
  - `sc.geoTiff[Int](...)`
  - `sc.geoTiff[Float](...)`
  - `sc.geoTiff[Array[Int]](...)`
  - `sc.geoTiff[Array[Float]](...)`
- If unsure of loaded type in a workflow, the documented inspection pattern is `println(raster.first.pixelType)`.
- For multi-raster operations later (for example `overlay`), metadata must match (resolution, CRS, tile size); otherwise reshape/reproject first.

### Output
Returns `RDD[ITile[T]]` — a distributed collection of raster tiles representing the loaded GeoTIFF band (`iLayer`) in Spark.

### Valid Call Patterns
```scala
val raster: RDD[ITile] = sc.geoTiff("treecover")
val vector: RDD[IFeature] = sc.shapefile("us_states")
val join: RDD[(IFeature, Int, Int, Float)] = raster.raptorJoin[Float](vector)

val treecover: RDD[ITile[Float]] = sc.geoTiff("treecover")
val countries: RDD[IFeature] = sc.shapefile("ne_10m_admin_0_countries.zip")
```

### LLM Instruction Prompt
- Always call this as `sc.geoTiff[T](...)` (receiver form).
- Keep argument order exactly: `(path, iLayer, opts)` when provided.
- Use `iLayer = 0` as default unless a different band is explicitly needed.
- Choose `T` to match the GeoTIFF pixel type; do not guess incompatible types.
- Do not invent extra parameters or alternate call shapes.

### Prompt Snippet
```text
Load a GeoTIFF into Spark tiles using sc.geoTiff[T](path, iLayer, opts). Keep receiver and argument order exactly. Use iLayer=0 unless another band is required. Pick T to match the raster pixel type (e.g., Int, Float, Array[Int], Array[Float]). Return/store as RDD[ITile[T]].
```

### Common Failure Modes
- **Wrong type parameter `T`** for the actual GeoTIFF pixel type, causing downstream type/pixel handling issues.
- **Invalid band index** in `iLayer` (e.g., requesting a non-existent band).
- **Using a non-GeoTIFF input** with `geoTiff` (RDPro documents this method for GeoTIFF loading).
- **Later raster alignment errors** when combining this output with another raster that has different CRS/resolution/tile size (fix with reshape/reproject before join/overlay).

### Fix Code Hint
```scala
import edu.ucr.cs.bdlab.beast._

val raster: RasterRDD[Int] = sc.geoTiff[Int]("glc2000_v1_1.tif")
println(raster.first.pixelType) // verify loaded pixel type in workflow
```

## API Test: `geojsonFile`

### Signature
```scala
def geojsonFile(filename: String) : SpatialRDD
def geojsonFile(filename: String) : JavaSpatialRDD
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/ReadWriteMixin.scala:84  (+1 more definition site/overload)_

_Source doc:_ Reads data from a Shapefile @param filename the name of the GeoJSON file or a directory that contains GeoJSON file @return an RDD of features

### Goal
Load GeoJSON vector data into Beast as a distributed spatial RDD of features for downstream Spark spatial analytics (e.g., partitioning, range query, joins).

### Parameters
- `filename` (`String`): Path to a GeoJSON file, or a directory containing GeoJSON file(s).

### Input
`geojsonFile` expects vector input in GeoJSON form, provided as a `String` path (`filename`) to either:
- one GeoJSON file, or
- a directory that contains GeoJSON file(s).

From project context, Beast documents GeoJSON support (including FeatureCollection and one-feature-per-line variants), and this method is the GeoJSON reader entry point.  
No extra method-level preconditions are documented for `geojsonFile` beyond providing a valid path to readable GeoJSON content.

### Output
Returns `SpatialRDD` — an RDD of spatial features (`IFeature` records) loaded from the GeoJSON source, ready for Beast/Spark spatial operations.

### Valid Call Patterns
```scala
// Scala
val records = sparkContext.geojsonFile("input.json")
```

```scala
// Load points in GeoJSON format.
// Download from https://star.cs.ucr.edu/dynamic/download.cgi/Tweets/data_index.geojson.gz?mbr=-117.8538,33.2563,-116.8142,34.4099
val points = sc.geojsonFile("Tweets.geojson.gz")
```

```java
// Java
JavaRDD<IFeature> records = spatialSparkContext.geojsonFile("input.json");
```

### LLM Instruction Prompt
- Call this API as an instance method on the Spark spatial context (e.g., `sparkContext.geojsonFile(...)` or `sc.geojsonFile(...)`), not as a bare function.
- Pass exactly one argument: `filename: String`.
- Use it only for GeoJSON inputs (file or directory containing GeoJSON files).
- Expect a feature RDD (`SpatialRDD` in Scala; Java overload returns `JavaSpatialRDD`) and then apply spatial ops on that result.

### Prompt Snippet
```text
Use `sc.geojsonFile(path)` to read GeoJSON vector data into a `SpatialRDD`.
`path` must be a String pointing to a GeoJSON file or a directory containing GeoJSON file(s).
Do not add extra parameters.
```

### Common Failure Modes
- Calling `geojsonFile(...)` without a receiver (e.g., not using `sc.` / `sparkContext.`), which typically does not compile.
- Passing a path that is not GeoJSON content.
- Passing an invalid/non-existent/unreadable path.
- Confusing overload return types in mixed Scala/Java code (`SpatialRDD` vs `JavaSpatialRDD`).

### Fix Code Hint
```scala
import edu.ucr.cs.bdlab.beast._

val records: SpatialRDD = sparkContext.geojsonFile(inputPath)
// where inputPath is a String path to a GeoJSON file or directory
```

## API Test: `geometryType`

### Signature
```scala
def geometryType: GeometryType
def geometryType: DataType
def geometryType: String
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/SpatialPartition.scala:60  (+2 more definition site/overload)_

_Source doc:_ The most inclusive geometry type for this partition. This can be interpreted as below. - Empty: All geometries are empty - Point: Contains at least one point and zero or more empty geometries - LineString: Contains at least one linestring and zero or more empty geometries - Polygon: Contains at least one polygon and zero or more empty geometries - MultiPoint: Contains at least one multipoint, and zero or more point or empty geometry. - MultiLineString: Contains at least one MultiLineString, and zero or more linestrings and empty geometries. - MultiPolygon: Contains at least one MultiPolygon, and zero or more poylgons and empty geometries. - GeometryCollection: Everything else, i.e., none of the above.

### Goal
Return the most inclusive geometry category present in a `SpatialPartition`, which is useful for understanding mixed vector contents before downstream spatial processing.

### Parameters
_None._

### Input
Call this on an existing `SpatialPartition` value (instance method, no arguments).  
No direct file format is passed to `geometryType`; the partition is typically produced by Beast vector loading/processing workflows.

Preconditions:
- Receiver must be a valid `SpatialPartition` object.
- This API itself has no raster type-parameter selection requirements and no extra compatibility arguments.

### Output
Returns `GeometryType` — the partition-level inclusive geometry classification described by the source doc (`Empty`, `Point`, `LineString`, `Polygon`, `MultiPoint`, `MultiLineString`, `MultiPolygon`, or `GeometryCollection` as catch-all).

### Valid Call Patterns
```scala
// Inferred from signature and sibling SpatialPartition call style in tests
val gt = summary.geometryType
```

### LLM Instruction Prompt
- Use it as a zero-argument instance member on a `SpatialPartition`-like value: `value.geometryType`.
- Do not add parameters.
- Do not assume which overload (`GeometryType` / `DataType` / `String`) is selected unless the expected type context is explicit.
- If receiver type is unknown, ask for/establish a `SpatialPartition` value first.

### Prompt Snippet
```text
Given a SpatialPartition value named `summary`, call `summary.geometryType` (no args) to get the partition’s most inclusive geometry type.
```

### Common Failure Modes
- Calling as a free function (`geometryType`) instead of on an instance.
- Adding nonexistent arguments (e.g., `geometryType(...)`).
- Assuming a specific return type overload without type context.
- Calling it on non-`SpatialPartition` objects.

### Fix Code Hint
```scala
// Correct shape: instance call, no arguments
val gt = summary.geometryType
```

## API Test: `getAttributeName`

### Signature
```scala
def getAttributeName(i: Int): String
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/IFeature.scala:92_

_Source doc:_ If names are associated with attributes, this function returns the name of the attribute at the given position (0-based). @param i the index of the attribute to return its name @return the name of the given attribute index or `null` if it does not exist

### Goal
Return the schema/attribute column name at a given 0-based position from a Beast `IFeature` (for example, a feature read from tabular/vector input in Spark).

### Parameters
- `i` (`Int`): 0-based attribute index whose name should be returned.

### Input
A valid feature object that supports `getAttributeName` (as shown in tests: `feature` returned from `readWKTFile(...).first()`), and an integer index `i` for an attribute position.  
Preconditions:
- Indexing is **0-based**.
- Attribute names must be associated with the feature schema; otherwise result can be `null`.
- If `i` is out of range, result is `null` (per source doc), not a guaranteed exception.

### Output
Returns `String` — the attribute name at index `i`, or `null` if that attribute name does not exist.

### Valid Call Patterns
```scala
val inputPath = makeFileCopy("/test.partitions")
val data = sparkContext.readWKTFile(inputPath.getPath, "Geometry", '\t', true)
val feature = data.first()
assert(feature.getAttributeName(0) == "ID")
assert(feature.getAttributeName(1) == "File Name")
```

### LLM Instruction Prompt
- Call it as an instance method on a feature object: `feature.getAttributeName(i)`.
- Use **0-based** indexes.
- Do not assume non-null return; handle possible `null`.
- Do not invent overloads or extra parameters.

### Prompt Snippet
```text
Given an IFeature value named feature, read attribute names by 0-based index using:
feature.getAttributeName(i)
Treat the return as nullable String (`null` if missing/out of range or unnamed).
```

### Common Failure Modes
- Using 1-based indexing (off-by-one errors).
- Assuming missing attributes throw instead of returning `null`.
- Calling `getAttributeName` on a value that is not an `IFeature`-like object.

### Fix Code Hint
```scala
val name0: String = feature.getAttributeName(0)
if (name0 == null) {
  // handle missing/unnamed attribute index
}
```

## API Test: `getBoolean`

### Signature
```scala
def getBoolean(key: String, defaultValue: Boolean): Boolean
```
_Source: beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/common/BeastOptions.scala:133_

_Source doc:_ Get value as boolean @param key @param defaultValue @return

### Goal
Retrieve a boolean option value (typically parsed from Beast/RDPro-style command-line options) by key, with a fallback default when the key is not set.

### Parameters
- `key` (`String`): The option name to read (for example, `"option2"`, `"option-3"`, `"option-4"` in tested usage).
- `defaultValue` (`Boolean`): The boolean value to return if `key` is not present in the options.

### Input
A parsed options container (receiver shown as `parsed.options` in tests) that stores key/value options from command-line-style arguments.

Preconditions from verified usage:
- Call this on an options object, e.g., `parsed.options.getBoolean(...)` (not as a bare function call).
- `key` should match the stored option name exactly, including dashes when present (e.g., `"option-3"`).
- This API is about option lookup; it does not take raster/vector files directly.

### Output
Returns `Boolean` — the resolved boolean value for `key`; if missing, returns `defaultValue`.

### Valid Call Patterns
```scala
val parsed = OperationHelper.parseCommandLineArguments("test", "path1",
  "option1:value1", "-option2", "-no-option3", "path2", "option4[0]:1", "-option4[1]")

parsed.options.getBoolean("option2", defaultValue = false)
parsed.options.getBoolean("option3", defaultValue = true)
```

```scala
val parsed = OperationHelper.parseCommandLineArguments("test", "path1",
  "option1:value1", "-no-option-3", "-option-4", "file-name:abc")

parsed.options.getBoolean("option-3", true)
parsed.options.getBoolean("option-4", false)
```

### LLM Instruction Prompt
- Use the instance call form exactly as verified: `parsed.options.getBoolean(key, defaultValue)`.
- Provide a concrete `String` key and a concrete `Boolean` default.
- Keep key spelling exact (including `-` characters).
- Do not invent overloads or omit the receiver.

### Prompt Snippet
```text
Given a parsed Beast options object `parsed`, read a boolean flag with:
`parsed.options.getBoolean("option-name", defaultValue = false)`.
Use the exact key string (including dashes), and always pass the fallback boolean.
```

### Common Failure Modes
- Calling `getBoolean(...)` without an options receiver (won’t match verified usage form).
- Using the wrong key spelling (e.g., dropping dashes: `"option3"` vs `"option-3"` when only one exists).
- Assuming missing keys throw an error; this method uses `defaultValue` fallback.

### Fix Code Hint
```scala
val enabled: Boolean = parsed.options.getBoolean("option-4", defaultValue = false)
val disabledByNoFlag: Boolean = parsed.options.getBoolean("option-3", defaultValue = true)
```

## API Test: `getFeatureReaderClass`

### Signature
```scala
def getFeatureReaderClass(path: String, opts: BeastOptions): Class[_ <: FeatureReader]
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/SpatialFileRDD.scala:398_

_Source doc:_ The class of the feature reader to use with this RDD. All partitions use the same feature reader.

### Goal
Select the `FeatureReader` implementation class Beast will use to read a spatial input path as a distributed feature RDD (with one reader class shared by all partitions).

### Parameters
- `path` (`String`): Input spatial dataset path to inspect/use for reader selection (e.g., a GeoJSON file path in the tested usage).
- `opts` (`BeastOptions`): Reader/input options that control format handling (in tested usage, includes `SpatialFileRDD.InputFormat -> "geojson"`).

### Input
A spatial input path plus Beast I/O options must be provided.

Grounded formats from project context include Shapefile, GeoJSON, CSV/WKT-style text inputs, GPX, etc., and Beast can often auto-detect by extension; however, this API’s tested call explicitly sets format via options:
- `val opts: BeastOptions = SpatialFileRDD.InputFormat -> "geojson"`

Preconditions for correct use:
- `path` should point to readable input in a supported spatial format.
- `opts` should be consistent with the actual data format if explicitly set (e.g., don’t force `"geojson"` for a non-GeoJSON file).
- This method only chooses the reader class; partitioning/reading are done by other calls (`createPartitions`, `readPartition`).

### Output
Returns `Class[_ <: FeatureReader]` — the Scala/Java class object for the feature reader Beast selected for this input. This class is then passed to partition-reading logic, and all partitions use this same reader class.

### Valid Call Patterns
```scala
val inputFile = makeFileCopy("/allfeatures.geojson")
val opts: BeastOptions = SpatialFileRDD.InputFormat -> "geojson"
val featureReaderClass = SpatialFileRDD.getFeatureReaderClass(inputFile.getPath, opts)
val partitions = SpatialFileRDD.createPartitions(inputFile.getPath, opts, sparkContext.hadoopConfiguration)
var featureCount: Int = 0
for (partition <- partitions) {
  val features = SpatialFileRDD.readPartition(partition, featureReaderClass, true, opts)
  featureCount += features.length
}
```

### LLM Instruction Prompt
- Use the receiver exactly as verified: `SpatialFileRDD.getFeatureReaderClass(path, opts)`.
- Always pass both required arguments in order: `(path: String, opts: BeastOptions)`.
- Ensure `opts` matches the true input format when explicitly specified (e.g., `SpatialFileRDD.InputFormat -> "geojson"`).
- Use the returned class as input to downstream partition reads (e.g., `readPartition`), not as loaded features itself.
- Do not invent overloads, extra parameters, or different return types.

### Prompt Snippet
```text
Given a spatial input path and BeastOptions, call SpatialFileRDD.getFeatureReaderClass(path, opts) to obtain Class[_ <: FeatureReader]. Keep the exact argument order and pass format options consistent with the file (e.g., SpatialFileRDD.InputFormat -> "geojson"). Then reuse that class when calling SpatialFileRDD.readPartition for all partitions.
```

### Common Failure Modes
- Passing a path that does not exist or is unreadable.
- Supplying `opts` with a forced input format that conflicts with the actual file content/extension.
- Treating the returned `Class[_ <: FeatureReader]` as if it were already-read features.
- Using a different/unverified call shape (e.g., missing receiver or wrong argument order).

### Fix Code Hint
```scala
val opts: BeastOptions = SpatialFileRDD.InputFormat -> "geojson"
val featureReaderClass =
  SpatialFileRDD.getFeatureReaderClass(inputFile.getPath, opts)

// Use the selected class for partition reads
val partitions =
  SpatialFileRDD.createPartitions(inputFile.getPath, opts, sparkContext.hadoopConfiguration)
val allFeatures = partitions.flatMap { p =>
  SpatialFileRDD.readPartition(p, featureReaderClass, true, opts)
}
```

## API Test: `getGeometry`

### Signature
```scala
def getGeometry: Geometry
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/IFeature.scala:69_

_Source doc:_ The geometry contained in the feature. @return the geometry in this attribute

### Goal
Return the geometry stored in an `IFeature`, so you can run geometry-based logic (for example, spatial processing in Beast/Spark pipelines).

### Parameters
_None._

### Input
Call this on an existing feature instance (e.g., `f: IFeature` from a `SpatialRDD` record).  
No file path or format is passed directly to this method; input formats (Shapefile/GeoJSON/CSV-WKT/etc.) are handled earlier when loading features.

Preconditions from observed usage:
- The receiver must be a feature object that supports `getGeometry` (as used in tests: `f.getGeometry`).
- In test usage, callers may cast the returned value to a concrete geometry type when needed (e.g., `EnvelopeND`), so your data must actually contain a compatible geometry before casting.

### Output
Returns `Geometry` — the geometry contained in that feature attribute (the feature’s spatial shape object).

### Valid Call Patterns
```scala
val envelope = f.getGeometry.asInstanceOf[EnvelopeND]
```

### LLM Instruction Prompt
- Use instance-call form on a feature object exactly as `f.getGeometry`.
- Do not add arguments; this method takes none.
- Treat the return type as `Geometry`; only cast (`asInstanceOf[...]`) if downstream logic requires a specific subtype and your data is known to match.
- If geometry subtype is unknown, keep it as `Geometry` instead of guessing.

### Prompt Snippet
```text
Given an `IFeature` value `f`, call `f.getGeometry` (no arguments) to retrieve its geometry.
If you need envelope-specific methods, cast only when valid, e.g.:
`val envelope = f.getGeometry.asInstanceOf[EnvelopeND]`.
```

### Common Failure Modes
- Calling `getGeometry` on something that is not a feature instance.
- Assuming a specific subtype without validation, then casting incorrectly (runtime cast failure).
- Treating `getGeometry` as a static/object method or adding parameters.

### Fix Code Hint
```scala
val geom: Geometry = f.getGeometry
// Only if your pipeline guarantees envelope geometries:
val envelope = f.getGeometry.asInstanceOf[EnvelopeND]
```

## API Test: `getInt`

### Signature
```scala
override def getInt(i: Int): Int
def getInt(key: String, defaultValue: Int): Int
```
_Source: beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/common/BeastOptions.scala:98  (+1 more definition site/overload)_

_Source doc:_ Get a value of a key as integer @param key @param defaultValue @return

### Goal
Retrieve an integer configuration value from options by key, falling back to a caller-provided default when needed.

### Parameters
- `key` (`String`): The option key/name to look up.
- `defaultValue` (`Int`): The integer value to return if the key is not set (or not resolved to a usable value; exact parsing behavior is not further documented in the provided sources).

### Input
A `String` key and an `Int` default value, called on an object that defines `getInt(key: String, defaultValue: Int): Int` (from `BeastOptions` per the provided API facts).

Preconditions:
- The receiver must be the options-like object exposing this method.
- No raster/vector file-format input is required for this method itself.
- The provided context does not document additional constraints (e.g., exact parse-error behavior for malformed integer strings), so that behavior is unknown here.

### Output
Returns `Int` — the resolved integer value for `key`, or `defaultValue` if no configured value is used.

### Valid Call Patterns
```scala
// Inferred from the signature/API facts (no BeastOptions.getInt(key, defaultValue)
// call form was provided in README or tests):
val value: Int = options.getInt("some.key", 10)

// Authoritative overload call form from tests (different receiver/type and overload):
val t: Int = firstGeom.getInt(0)
```

### LLM Instruction Prompt
- Use the instance method form with an explicit receiver (e.g., `options.getInt("key", defaultValue)`), not a bare `getInt(...)`.
- Pass exactly two arguments for this overload: `(String, Int)`.
- Keep default values as integer literals/variables (`Int`), not floating-point/string.
- Do not invent extra parameters, named options, or alternative return types.

### Prompt Snippet
```text
Given an options object, read an integer setting with fallback:
val partitions: Int = options.getInt("spark.sql.shuffle.partitions", 200)
Use exactly (key: String, defaultValue: Int).
```

### Common Failure Modes
- Calling the wrong overload (`getInt(i: Int)`) when you intend key-based lookup.
- Using a receiver that does not implement `getInt(key: String, defaultValue: Int): Int`.
- Passing wrong argument types (e.g., non-`String` key or non-`Int` default).
- Assuming undocumented behavior for malformed stored values; this is not specified in the provided facts.

### Fix Code Hint
```scala
// Correct: key-based integer lookup with explicit receiver
val retries: Int = options.getInt("job.maxRetries", 3)

// If you accidentally used index-based overload on another type, switch to key-based:
val configured: Int = options.getInt("my.int.key", 0)
```

## API Test: `getLong`

### Signature
```scala
def getLong(key: String, defaultValue: Long): Long
```
_Source: beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/common/BeastOptions.scala:114_

_Source doc:_ Get a key value as long @param key @param defaultValue @return

### Goal
Retrieve an option/configuration value by key as a `Long`, falling back to a caller-provided default when needed.

### Parameters
- `key` (`String`): The option name to look up.
- `defaultValue` (`Long`): The fallback value to return if the key is not available as a `Long`.

### Input
A `String` key and a `Long` default value are required.  
No raster/vector file format input is used directly by this function.  
Precondition: you must call it on an object/value that provides `getLong(key, defaultValue)` (the exact receiver is not shown in provided tests/README examples for this API).

### Output
Returns `Long` — the resolved long integer value for `key`, or `defaultValue` if no usable value is found.

### Valid Call Patterns
```scala
// Inferred from signature (no verbatim README/test call for getLong was provided)
value.getLong("some.key", 0L)
```

### LLM Instruction Prompt
- Use exactly two arguments in this order: `(key: String, defaultValue: Long)`.
- Keep the receiver form as an instance call (e.g., `value.getLong(...)`) for portability.
- Do not invent extra parameters, overloads, or type arguments.
- If no concrete receiver is known in context, state that the call form is inferred from signature.

### Prompt Snippet
```text
Call getLong as an instance method with:
- key: String
- defaultValue: Long
Example (inferred): value.getLong("some.key", 0L)
Do not add extra arguments or overloads.
```

### Common Failure Modes
- Calling `getLong` without a receiver in Scala code where no such function is in scope.
- Passing arguments in the wrong order.
- Using a non-`Long` default literal (e.g., `0` instead of `0L`) where strict typing matters.
- Assuming this API reads raster files or applies RDPro raster compatibility/type-selection rules (it is a config lookup method, not a raster operation).

### Fix Code Hint
```scala
// Ensure you call on a valid receiver and provide a Long literal default
val v: Long = value.getLong("my.option.key", 0L)
```

## API Test: `getName`

### Signature
```scala
def getName(i: Int): String
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/IFeature.scala:83_

_Source doc:_ Return the name of the given attribute. @param i the index of the attribute in the range [0, length[ @return the type of the attribute or null if unknown

### Goal
Return the attribute name at a given column/index position from a feature schema-like attribute list.

### Parameters
- `i` (`Int`): the index of the attribute, expected to be in the range `[0, length[`.

### Input
A feature-like object that exposes `getName(i: Int): String` (as documented in `IFeature.scala`), and a valid attribute index.  
Precondition from source doc: `i` should be within `[0, length[`.  
No raster format/type-selection rules are specified for this API.

### Output
Returns `String` — the name of the attribute at index `i`; if unknown, may return `null` (per source doc).

### Valid Call Patterns
```scala
// Inferred from signature/source doc (no verbatim README example for this API)
val attributeName: String = feature.getName(i)
```

### LLM Instruction Prompt
- Call as an instance method on the target feature object: `feature.getName(i)`.
- Ensure `i` is an integer index in `[0, length[`.
- Handle possible `null` return when attribute name is unknown.
- Do not invent overloads or extra parameters.

### Prompt Snippet
```text
Given an IFeature-like value `feature`, call `feature.getName(i)` with an Int index i in [0, length[ and treat the result as a String that can be null if unknown.
```

### Common Failure Modes
- Passing an out-of-range index (`i < 0` or `i >= length`), violating the documented index precondition.
- Assuming the return is always non-null; source doc explicitly allows `null if unknown`.
- Calling `getName` as a standalone function instead of on a receiver object.

### Fix Code Hint
```scala
val i: Int = 0 // choose an index in [0, length[
val nameOrNull: String = feature.getName(i)
if (nameOrNull == null) {
  // handle unknown attribute name
}
```

## API Test: `getOperationParams`

### Signature
```scala
def getOperationParams(operation: Operation, opts: BeastOptions): Array[OperationParamInfo]
```
_Source: beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/util/OperationHelper.scala:209_

_Source doc:_ Returns all parameters that are allowed for the given operation. Operation parameters are all parameters annotated with [[OperationParam]] that appear in one of the following: - In the class associated with the given operation - In any additional classes defined in the [[OperationMetadata]] annotation on the class - In any classes that are added through the method [[IConfigurable]].addDependentClasses @param operation the operation in question @param opts any additional user options. This is used to add dependent classes if they depend on some user choice. For example, if the user selects a specific indexer, it can be used to add that specific indexer as a dependent class @return an array of parameters that are allowed

### Goal
Return the full set of allowed operation parameters (as `OperationParamInfo`) for a specific Beast operation, including parameters contributed by metadata/dependent classes.

### Parameters
- `operation` (`Operation`): the operation to inspect (i.e., the operation whose allowed `@OperationParam` definitions should be collected).
- `opts` (`BeastOptions`): optional user options used while resolving dependent classes (via `IConfigurable.addDependentClasses`), which can affect which parameters are included.

### Input
This method does **not** read raster/vector files directly.  
Caller must provide:

- A valid `Operation` instance (commonly obtained from an operation registry, e.g., `OperationHelper.operations("...")` in tests).
- A `BeastOptions` instance, or `null` (as shown in tests), when no extra option-driven dependent-class resolution is needed.

Preconditions from the API/source doc:

- Parameters are discovered from:
  1. the operation class,
  2. additional classes listed in `OperationMetadata`,
  3. classes added through `IConfigurable.addDependentClasses` (possibly influenced by `opts`).

### Output
Returns `Array[OperationParamInfo]` — an array describing the parameters allowed for the given operation after collecting all applicable `@OperationParam` annotations from the operation and its related/dependent classes.

### Valid Call Patterns
```scala
val params = OperationHelper.getOperationParams(OperationHelper.operations("test"), null)
```

```scala
val paramssub = OperationHelper.getOperationParams(OperationHelper.operations("subtest1"), null)
```

### LLM Instruction Prompt
- Call using the tested static receiver form: `OperationHelper.getOperationParams(operation, opts)`.
- Pass an `Operation` object as first argument; do not pass a string directly.
- Use `opts` to influence dependent-class parameter discovery when needed; `null` is valid per tests.
- Do not invent extra parameters or overloads; this API takes exactly two arguments.

### Prompt Snippet
```text
Get allowed params for an existing Operation object using:
OperationHelper.getOperationParams(operationObj, opts)
If no extra option-driven dependency resolution is needed, use null for opts.
```

### Common Failure Modes
- Passing an operation name/string directly instead of an `Operation` instance.
- Assuming file-format or raster-type preconditions apply here (they do not; this is operation-metadata introspection).
- Expecting only parameters from the main operation class and forgetting dependent classes can add more.
- Omitting `opts`-driven behavior when dependent classes are selected by user options.

### Fix Code Hint
```scala
// Resolve/create an Operation first, then query params
val op: Operation = OperationHelper.operations("test")
val params: Array[OperationParamInfo] =
  OperationHelper.getOperationParams(op, null)
```

## API Test: `getPartition`

### Signature
```scala
override def getPartition(tile: Any): Int
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterPartitioner.scala:43_

_Source doc:_ Returns the partition of the given tileID @param tile the tile ID in the input RasterMetadata to return its partition @return the partition ID associated with the given tile

### Goal
Return the partition ID for a raster tile ID, using the `RasterPartitioner`’s configured raster metadata and partitioning layout.

### Parameters
- `tile` (`Any`): The tile ID to look up (as documented: “the tile ID in the input RasterMetadata”); in the passing test usage, this is provided as an integer tile ID (e.g., `0`, `11`, `99`).

### Input
A previously constructed `RasterPartitioner` instance with valid `RasterMetadata` and partitioning configuration, plus a tile ID argument passed to `getPartition`.

Preconditions from observed usage:
- The tile value should correspond to a tile ID in the partitioner’s input raster metadata space.
- Call shape should be instance-based: `partitioner.getPartition(tileId)`.

No file format input is required by this method itself.

### Output
Returns `Int` — the partition ID associated with the given tile ID.

### Valid Call Patterns
```scala
val rasterMetadata = new RasterMetadata(0, 0, 1000, 1000,
  100, 100, 4326, new AffineTransform())
val partitioner = new RasterPartitioner(rasterMetadata, 25)
assertResult(0)(partitioner.getPartition(0))
assertResult(0)(partitioner.getPartition(11))
assertResult(24)(partitioner.getPartition(99))
```

### LLM Instruction Prompt
- Use the instance call form exactly: `partitioner.getPartition(tileId)`.
- Provide tile IDs that are valid for the `RasterMetadata` used to build the same `RasterPartitioner`.
- Do not invent extra parameters; `getPartition` accepts exactly one argument (`tile: Any`) and returns `Int`.

### Prompt Snippet
```text
Given an existing RasterPartitioner named `partitioner`, call `partitioner.getPartition(tileId)` with a tile ID from that partitioner’s RasterMetadata tile space, and use the returned Int as the partition ID.
```

### Common Failure Modes
- Calling `getPartition` without a properly initialized `RasterPartitioner`.
- Passing a value for `tile` that is not a tile ID from the partitioner’s input raster metadata.
- Using a different call shape (e.g., bare `getPartition(...)`) instead of `partitioner.getPartition(...)`.

### Fix Code Hint
```scala
val rasterMetadata = new RasterMetadata(0, 0, 1000, 1000,
  100, 100, 4326, new AffineTransform())
val partitioner = new RasterPartitioner(rasterMetadata, 25)

val tileId = 11
val partitionId: Int = partitioner.getPartition(tileId)
println(partitionId)
```

## API Test: `getPointValue`

### Signature
```scala
def getPointValue(x: Double, y: Double): T
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/ITile.scala:93_

_Source doc:_ Return the value of the pixel that contains the given point at model (world) coordinates. @param x the x-coordinate of the point, e.g., longitude @param y the y-coordinate of the point, e.g., latitude @return the value of all components of the given pixel

### Goal
Read the pixel value from a raster tile at a given world-coordinate point (for example longitude/latitude) in RDPro/Beast raster workflows.

### Parameters
- `x` (`Double`): X coordinate in model/world space (e.g., longitude) used to locate the containing pixel.
- `y` (`Double`): Y coordinate in model/world space (e.g., latitude) used to locate the containing pixel.

### Input
A tile instance (`ITile[T]` implementation) that has already been read/loaded from a raster source (e.g., GeoTIFF via `GeoTiffReader` in the tested usage), plus world coordinates `(x, y)` that fall in that tile’s spatial extent.

Preconditions and compatibility notes:
- Coordinates are **model/world coordinates**, not pixel row/column indices.
- The tile should be chosen for the point first (tested pattern uses `reader.metadata.getTileIDAtPoint(...)` then `reader.readTile(...)`).
- Generic pixel type `T` must match the raster data type used when reading (e.g., `Int` for integer single-band, `Array[Float]` for multi-band float), consistent with Beast typed raster rules.

### Output
Returns `T` — the value of the pixel that contains `(x, y)`.  
For single-band rasters this is typically a scalar (e.g., `Int`); for multi-band rasters this is the per-band component array (e.g., `Array[Float]`).

### Valid Call Patterns
```scala
val tile1 = reader.readTile(reader.metadata.getTileIDAtPoint(23.224, 32.415))
val v1: Int = tile1.getPointValue(23.224, 32.415)

val tile2 = reader.readTile(reader.metadata.getTileIDAtPoint(31.277, 26.954))
val v2: Array[Float] = tile2.getPointValue(31.277, 26.954)
```

### LLM Instruction Prompt
- Call as an instance method on a tile object: `tile.getPointValue(x, y)`.
- Pass exactly two `Double` world coordinates.
- Ensure the tile is read from the tile ID containing the same point before calling.
- Keep the pixel type `T` consistent with the reader/load type (do not mix `Int` vs `Array[Float]`).

### Prompt Snippet
```text
Given an already loaded tile (ITile[T]) and a world-coordinate point (x, y), call:
tile.getPointValue(x, y)
Use Double coordinates (model/world space), not pixel indices. Ensure T matches raster pixel type.
```

### Common Failure Modes
- Using pixel indices `(col,row)` instead of world coordinates `(x,y)`.
- Calling `getPointValue` on a tile that does not spatially contain the point.
- Type mismatch between reader/load type and expected return type (`Int` vs `Array[Float]`).
- Trying to call `getPointValue` before reading/initializing raster/tile data.

### Fix Code Hint
```scala
val tile = reader.readTile(reader.metadata.getTileIDAtPoint(x, y))
val value = tile.getPointValue(x, y) // x,y are world/model coordinates as Double
```

## API Test: `getStorageSize`

### Signature
```scala
def getStorageSize: Int
def getStorageSize(value: Any, dataType: DataType): Int
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/IFeature.scala:112  (+1 more definition site/overload)_

### Goal
Estimate storage size in bytes for feature content (including geometry and attributes), or for a given typed value.

### Parameters
- `value` (`Any`): The value whose storage size is to be estimated in the `(value, dataType)` overload.
- `dataType` (`DataType`): The Spark SQL `DataType` describing how `value` should be interpreted for size estimation.

### Input
This API is in-memory (not file-format based).  
You call it either:

1. As an instance method on a feature-like object (`feature.getStorageSize`) to estimate total feature storage size including geometry and features, or  
2. Via the overload `getStorageSize(value, dataType)` when you already have a value and its Spark SQL type.

Preconditions from available evidence:
- `value` and `dataType` should correspond to each other in the two-argument overload.
- Null/empty attribute content should be handled without throwing (validated by tests with null values and empty maps).
- No additional raster compatibility/type-selection rules are documented for this specific API.

### Output
Returns `Int` — storage size estimate in bytes.

### Valid Call Patterns
```scala
// from tests (authoritative, compiled)
val feature = Feature.create(Row.apply(123.25, "name",
  new PointND(GeometryReader.DefaultGeometryFactory, 2, 0.0, 1.0), "name2", null), null)
assert(feature.getStorageSize > 0)

val feature2 = Feature.create(new PointND(GeometryReader.DefaultGeometryFactory, 2, 0.0, 1.0),
  Array("id", "name", "tags"), null,
  Array(33, "test", Map()))
assert(feature2.getStorageSize > 10)
```

### LLM Instruction Prompt
- Prefer the tested instance call form `feature.getStorageSize` when you have a `Feature`/`IFeature`.
- Use `getStorageSize(value, dataType)` only when both the value and its Spark SQL `DataType` are explicitly available.
- Do not invent extra parameters or alternative return types.
- Treat the result as an estimate in bytes (`Int`), not an exact serialized byte count guarantee.

### Prompt Snippet
```text
Given an existing Feature/IFeature object, call `feature.getStorageSize` and use the returned Int as estimated bytes.
If using the overload, pass exactly `(value: Any, dataType: DataType)` with matching type semantics.
```

### Common Failure Modes
- Calling a non-existent variant (extra args, different types, or different return type assumptions).
- Passing a `value` and mismatched `dataType` in the two-argument overload.
- Assuming this method reads GeoTIFF/HDF/CSV directly; it operates on in-memory values/features.
- Treating the estimate as exact persisted file size.

### Fix Code Hint
```scala
// Preferred, tested call shape
val sizeBytes: Int = feature.getStorageSize

// Overload usage (signature-grounded; no tested receiver form provided here)
val estimated: Int = getStorageSize(value, dataType)
```

## API Test: `getTileIDAtPixel`

### Signature
```scala
def getTileIDAtPixel(iPixel: Int, jPixel: Int): Int
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/RasterMetadata.scala:69_

_Source doc:_ Computes the ID of the tile that contains the given pixel. Tiles are numbered in row-wise ordering. @param iPixel the position of the column of the pixel @param jPixel the position of the row of the pixel @return a unique identifier for the tile that contains this pixel location

### Goal
Given a pixel location in raster grid coordinates (column, row), return the unique row-wise tile ID of the tile that contains that pixel.

### Parameters
- `iPixel` (`Int`): Pixel column index (x/grid column position) in the raster.
- `jPixel` (`Int`): Pixel row index (y/grid row position) in the raster.

### Input
Call this on a `RasterMetadata` instance (as shown in tests: `reader.metadata` or `t.rasterMetadata`) that is already initialized from raster input (e.g., GeoTIFF via RDPro/Beast readers).  
Preconditions from observed usage:
- The pixel coordinates should be grid coordinates in the raster’s pixel space (not model/world coordinates).
- Use integer pixel indices.
- The call form is instance-based: `value.getTileIDAtPixel(iPixel, jPixel)`.

### Output
Returns `Int` — a unique tile identifier for the tile containing `(iPixel, jPixel)`, using row-wise tile numbering.

### Valid Call Patterns
```scala
val tileID = reader.metadata.getTileIDAtPixel(37, 24)

fileTileRDD.filter(t => t.rasterMetadata.getTileIDAtPixel(0, 0) == t.tileID)
```

### LLM Instruction Prompt
- Call this as an instance method on raster metadata (`reader.metadata` / `t.rasterMetadata`), not as a standalone function.
- Pass pixel-space indices in `(column, row)` order.
- Do not pass model/CRS coordinates directly; convert to grid indices first if needed.
- Treat the return value as a tile ID integer (row-wise numbering), suitable for comparison with tile IDs.

### Prompt Snippet
```text
Given a RasterMetadata instance `md`, compute the tile ID containing pixel column `i` and row `j` by calling:
`md.getTileIDAtPixel(i, j)`.
Use pixel grid coordinates (column, row), not model coordinates.
```

### Common Failure Modes
- Swapping argument meaning/order (passing row as `iPixel` and column as `jPixel`).
- Passing model coordinates (e.g., lon/lat) instead of raster grid pixel indices.
- Calling without a metadata receiver (e.g., bare `getTileIDAtPixel(...)`), which does not match verified usage.
- Comparing against unrelated IDs instead of the tile’s `tileID` field when filtering/joining tiles.

### Fix Code Hint
```scala
// If you start from model/world coordinates, convert first, then call getTileIDAtPixel
val outPoint = new java.awt.geom.Point2D.Double
reader.metadata.modelToGrid(-0.06, 49.28, outPoint)
val iPixel = outPoint.getX.toInt
val jPixel = outPoint.getY.toInt

val tileID = reader.metadata.getTileIDAtPixel(iPixel, jPixel)
```

## API Test: `getTileIDAtPoint`

### Signature
```scala
def getTileIDAtPoint(x: Double, y: Double): Int
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/RasterMetadata.scala:81_

_Source doc:_ Returns the ID of the tile that contains the given point location in model (world) space @param x the x-coordinate of the point, e.g., longitude @param y the y-coordinate of the point, e.g., latitude @return the ID of the tile that contains this pixel or -1 if the point is outside the input space

### Goal
Find which raster tile contains a world/model-space point (for example longitude/latitude) so you can read or process the correct tile.

### Parameters
- `x` (`Double`): x-coordinate of the query point in model/world space (e.g., longitude).
- `y` (`Double`): y-coordinate of the query point in model/world space (e.g., latitude).

### Input
A `RasterMetadata` instance (e.g., `reader.metadata`) must already be initialized from a raster dataset (such as GeoTIFF read through `GeoTiffReader` in the test examples).  
The `(x, y)` coordinates must be in the same model/world coordinate space as that metadata.  
If the point is outside the raster input space, the method returns `-1`.

### Output
Returns `Int` — the tile ID that contains the given point; returns `-1` when the point is outside the input raster space.

### Valid Call Patterns
```scala
val tile1 = reader.readTile(reader.metadata.getTileIDAtPoint(23.224, 32.415))
val tile2 = reader.readTile(reader.metadata.getTileIDAtPoint(33.694, 14.761))
val tile1Banded = reader.readTile(reader.metadata.getTileIDAtPoint(31.277, 26.954))
```

### LLM Instruction Prompt
- Call this as an instance method on raster metadata using the verified receiver form: `reader.metadata.getTileIDAtPoint(x, y)`.
- Pass `x` and `y` as `Double` in model/world space.
- Check for `-1` before calling `readTile`, because `-1` means outside raster extent.
- Do not invent extra parameters or overloads.

### Prompt Snippet
```text
Given an initialized GeoTiffReader, use reader.metadata.getTileIDAtPoint(x, y) to locate the tile containing a world-space point. If the returned tile ID is -1, treat it as out of bounds and do not call readTile on it.
```

### Common Failure Modes
- Passing coordinates in a different CRS/space than the raster metadata uses, causing wrong tile IDs or `-1`.
- Calling `readTile` directly with the result without handling `-1` (out-of-bounds case).
- Attempting a different call shape (e.g., bare `getTileIDAtPoint(...)`) instead of calling through a metadata instance.

### Fix Code Hint
```scala
val tileID = reader.metadata.getTileIDAtPoint(x, y)
if (tileID != -1) {
  val tile = reader.readTile(tileID)
  // use tile.getPointValue(x, y)
} else {
  // point is outside input space
}
```

## API Test: `getTitle`

### Signature
```scala
private[davinci] def getTitle(feature: IFeature): String
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/SVGPlotter.scala:76_

_Source doc:_ Extract the title of the given feature by interpolating the [[svgTitle]] with feature attributes @param feature the feature to extract the elements from @return the string that interpolates the given string with the feature

### Goal
Generate a feature title string for visualization by interpolating the plotter’s `svgTitle` template with values from an `IFeature`.

### Parameters
- `feature` (`IFeature`): the input feature whose attribute names/positions are used to resolve placeholders in `svgTitle`.

### Input
- A valid `IFeature` instance.
- The call is instance-based on an `SVGPlotter` receiver (`plotter.getTitle(feature)` as shown in tests).
- `svgTitle` is expected to be configured on the plotter before calling:
  - Plain text title (no placeholders), e.g. `"simple"`.
  - Attribute-name placeholders, e.g. `"record #${id}"`, including names with hyphens like `"${name-full}"`.
  - Attribute-index placeholders, e.g. `"${#0}"`, `"${#1}"`.
- No file-format input is involved for this method directly (it operates on in-memory `IFeature`).

### Output
Returns `String` — the interpolated title text derived from `svgTitle` and the provided feature’s attributes.

### Valid Call Patterns
```scala
val plotter = new SVGPlotter
plotter.svgTitle = "simple"
plotter.getTitle(Feature.create(EmptyGeometry.instance, null, null, Array()))

plotter.svgTitle = "record #${id}"
plotter.getTitle(Feature.create(EmptyGeometry.instance, Array("id"), null, Array(15)))

plotter.svgTitle = "the ${name-full}"
plotter.getTitle(Feature.create(EmptyGeometry.instance, Array("name-full"), null, Array("Santo")))

plotter.svgTitle = "record #${#0}"
plotter.getTitle(Feature.create(EmptyGeometry.instance, Array("id"), null, Array(15)))

plotter.svgTitle = "the ${#1}"
plotter.getTitle(Feature.create(EmptyGeometry.instance, Array("id", "name-full"), null, Array(5, "Santo")))
```

### LLM Instruction Prompt
- Call this method as an instance method on `SVGPlotter`: `plotter.getTitle(feature)`.
- Ensure `plotter.svgTitle` is set before calling; `getTitle` interpolates that template.
- Provide an `IFeature` whose schema/values match placeholders used in `svgTitle` (by name like `${id}` or by index like `${#0}`).
- Do not invent extra parameters or alternate signatures.

### Prompt Snippet
```text
Given an existing SVGPlotter `plotter` and an `IFeature` `feature`, set `plotter.svgTitle` to the desired template, then call `plotter.getTitle(feature)`. Use `${attrName}` for named attributes or `${#index}` for positional attributes.
```

### Common Failure Modes
- Calling without setting `svgTitle` to the intended template first, producing unexpected title text.
- Using placeholder names not present in the feature attributes (e.g., `${id}` when `id` is not in the feature schema).
- Using positional placeholders with the wrong index (e.g., `${#1}` when only one attribute exists).
- Attempting to call `getTitle` as a top-level/static function instead of on an `SVGPlotter` instance.

### Fix Code Hint
```scala
val plotter = new SVGPlotter
plotter.svgTitle = "record #${id}" // or "record #${#0}"
val feature = Feature.create(EmptyGeometry.instance, Array("id"), null, Array(15))
val title: String = plotter.getTitle(feature)
println(title) // record #15
```

## API Test: `getValue`

### Signature
```scala
def getValue(in: FSDataInputStream, offset: Long, key: Long): (Long, Int)
def getValue(fileSystem: FileSystem, path: Path, key: Long): (Long, Int)
def getValue(i: Int, j: Int, position: Int): T
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/DiskTileHashtable.scala:91  (+2 more definition site/overload)_

_Source doc:_ Return the value that corresponds to the given key or null if the value is not found. @param in the hashtable file @param offset the offset of the hashtable in the file @param key the key to search for @return the value of the key if found, or `null` if the key is not found.

### Goal
Look up the value associated with a `Long` key from a hashtable stored on disk (or via overloads from a file path / grid position), for internal Beast/RDPro/DaVinci indexed data access.

### Parameters
- `in` (`FSDataInputStream`): Input stream for the hashtable file content.
- `offset` (`Long`): Byte offset of the hashtable inside the file/stream.
- `key` (`Long`): Key to search for in that hashtable.

### Input
- For this overload, caller must provide:
  - an open `FSDataInputStream` pointing to the hashtable file,
  - a valid hashtable `offset` within that stream,
  - the `Long` key to query.
- Source doc explicitly says lookup is against a “hashtable file” and can return not found.
- No additional RDPro raster compatibility/type-selection preconditions are documented for this method in the provided sources.

### Output
Returns `(Long, Int)` — a tuple value associated with the requested key when found.  
Per source doc, if key is not found, return is “null”. (This is documented behavior; exact null-handling details for Scala tuple type are not further specified in provided sources.)

### Valid Call Patterns
```scala
// Inferred from the authoritative signature (no direct test/README call for this overload was provided)
val v: (Long, Int) = getValue(in, offset, key)
```

### LLM Instruction Prompt
- Use exactly one of the documented overloads; do not invent arguments.
- For this overload, pass `(FSDataInputStream, Long, Long)` in that order.
- Treat lookup as nullable/not-found per source doc.
- Do not confuse this API with histogram `histogram.getValue(...)` examples; those are different receivers/signatures.

### Prompt Snippet
```text
Call getValue only with documented overloads. For hashtable-file lookup use:
getValue(in: FSDataInputStream, offset: Long, key: Long): (Long, Int)
Use a valid hashtable offset. Handle not-found as documented (null).
Do not replace this with histogram.getValue(...) calls.
```

### Common Failure Modes
- Passing wrong argument types/order (e.g., not `FSDataInputStream, Long, Long`).
- Using an invalid `offset` that does not point to a hashtable location.
- Assuming key always exists and not handling the documented “null if not found”.
- Mixing up overloads (`FileSystem, Path, Long` vs stream-based overload).

### Fix Code Hint
```scala
// Choose the stream overload with exact parameter order/types
val result: (Long, Int) = getValue(in, offset, key)

// If you have filesystem + path, use the matching overload instead
val result2: (Long, Int) = getValue(fileSystem, path, key)
```

## API Test: `gridToModel`

### Signature
```scala
def gridToModel(i: Double, j: Double, outPoint: Point2D.Double): Unit
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/RasterMetadata.scala:150_

_Source doc:_ Converts a point location from the grid (pixel) space to the model (world) space @param i the position of the column @param j the position of the row @param outPoint the output point that contains the model coordinates

### Goal
Convert raster grid coordinates (column/row in pixel space) into model/world coordinates using a `RasterMetadata` transform.

### Parameters
- `i` (`Double`): Column position in grid (pixel) space.
- `j` (`Double`): Row position in grid (pixel) space.
- `outPoint` (`Point2D.Double`): Mutable output point that will be populated with the converted model/world `x` and `y`.

### Input
A caller must provide:
- A valid `RasterMetadata` instance (for example `metadata` or `reader.metadata`) that defines the grid↔model transform.
- Numeric grid coordinates `i` and `j` as `Double`.
- A pre-allocated `Point2D.Double` instance to receive output coordinates.

Preconditions/compatibility notes from available context:
- This is a coordinate transform utility on raster metadata; it does not load files by itself.
- The method call form is instance-based (`value.gridToModel(...)`) as shown in tests.
- No additional API-level bounds checks or CRS-mixing behavior are documented here; if you need inverse checks, pair with `modelToGrid` on the same metadata (as in tests).

### Output
Returns `Unit` — the result is written into `outPoint` (its `x`/`y` are mutated to model/world coordinates).

### Valid Call Patterns
```scala
val point1 = new Point2D.Double()
metadata.gridToModel(100, 200, point1)

val outPoint = new Point2D.Double
reader.metadata.gridToModel(0, 0, outPoint)
reader.metadata.gridToModel(reader.metadata.rasterWidth, reader.metadata.rasterHeight, outPoint)
```

### LLM Instruction Prompt
- Always call it as an instance method on `RasterMetadata` (`metadata.gridToModel(...)` or `reader.metadata.gridToModel(...)`), not as a standalone function.
- Pass arguments in exact order: `(i, j, outPoint)`.
- Allocate `outPoint` before the call and read results from that same object after the call.
- Use `Double` numeric inputs for `i` and `j`.

### Prompt Snippet
```text
Given a RasterMetadata instance named metadata, convert grid pixel coordinates to world coordinates by:
1) creating a Point2D.Double output object,
2) calling metadata.gridToModel(i, j, outPoint),
3) reading outPoint.x and outPoint.y.
Use the exact argument order (i, j, outPoint).
```

### Common Failure Modes
- Calling `gridToModel` without a `RasterMetadata` receiver (won’t match tested call shape).
- Swapping `i`/`j` (column/row) and getting wrong coordinates.
- Expecting a return value instead of reading the mutated `outPoint`.
- Passing a null/uninitialized `outPoint`.

### Fix Code Hint
```scala
val outPoint = new Point2D.Double()
reader.metadata.gridToModel(37.0, 24.0, outPoint)
println(s"Model coordinates: ${outPoint.x}, ${outPoint.y}")
```

## API Test: `hdfFile`

### Signature
```scala
def hdfFile(path: String, layer: String, opts: BeastOptions = new BeastOptions()): RDD[ITile[Float]]
def hdfFile(filename: String, layer: String): JavaRasterRDD[Float]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RaptorMixin.scala:46  (+1 more definition site/overload)_

### Goal
Load raster tiles from an HDF file (or directory of HDF files) for a specific named layer into RDPro/Beast as a distributed float raster RDD.

### Parameters
- `path` (`String`): Path to the input HDF file or directory of HDF files to read.
- `layer` (`String`): Layer name inside the HDF input to load (for example, `"LST_Day_1km"` in the README example).
- `opts` (`BeastOptions`), default `new BeastOptions()`: Beast read options used while loading; exact option keys/semantics are not specified in the provided facts.

### Input
- **Format**: HDF raster input (single file or directory), as documented by the source doc.
- **Required**: A valid `layer` name that exists in the HDF input.
- **Receiver/call style**: Use the Spark context mixin form shown in project docs: `sc.hdfFile(...)`.
- **Type rule**: `hdfFile` returns float tiles (`RDD[ITile[Float]]` / `RasterRDD[Float]` alias in examples), so downstream code should treat pixels as `Float`.
- **Downstream compatibility**: If you later combine this raster with others (e.g., overlay/reshape workflows), metadata compatibility (resolution/CRS/tile size) may need reshape/reproject first per project rules.

### Output
Returns `RDD[ITile[Float]]` — a distributed raster tile collection containing all tiles read from the requested HDF layer across the given input file(s). In README usage this is assigned via alias as `RasterRDD[Float]`.

### Valid Call Patterns
```scala
val temperatureK: RasterRDD[Float] =
  sc.hdfFile("MOD11A1.A2022173.h08v05.006.2022174092443.hdf", "LST_Day_1km")
val temperatureF: RasterRDD[Float] = temperatureK.mapPixels(k => (k-273.15f) * 9 / 5 + 32)
temperatureF.saveAsGeoTiff("temperature_f")
```

### LLM Instruction Prompt
- Call `hdfFile` with receiver `sc` exactly as `sc.hdfFile(path, layer)` (or with `opts` as third argument when needed).
- Pass a real HDF path/directory string and a real HDF layer name string; do not invent extra parameters.
- Treat the result as float raster tiles (`RDD[ITile[Float]]` / `RasterRDD[Float]` alias).
- If subsequent operations require aligned metadata, add reshape/reproject steps before joins/overlays.

### Prompt Snippet
```text
Use `sc.hdfFile(path, layer)` to load an HDF raster layer as float tiles. 
Inputs: HDF file or directory path, and an existing layer name (e.g., "LST_Day_1km"). 
Return type is `RDD[ITile[Float]]` (often used as `RasterRDD[Float]` alias). 
Do not add unsupported arguments; optional third arg is `BeastOptions`.
```

### Common Failure Modes
- Using a wrong/nonexistent `layer` name for the HDF file.
- Passing a path that is not an HDF file/directory.
- Assuming integer pixel type after load; this API returns float tiles.
- Calling a bare `hdfFile(...)` without the `sc.` receiver in Scala examples that rely on Spark context mixins.

### Fix Code Hint
```scala
import edu.ucr.cs.bdlab.beast._

val temperatureK: RasterRDD[Float] =
  sc.hdfFile("MOD11A1.A2022173.h08v05.006.2022174092443.hdf", "LST_Day_1km")

val temperatureF: RasterRDD[Float] =
  temperatureK.mapPixels(k => (k - 273.15f) * 9 / 5 + 32)

temperatureF.saveAsGeoTiff("temperature_f")
```

## API Test: `id`

### Signature
```scala
def id: Int
```
_Source: beast/dataExplorer/src/main/scala/edu/ucr/cs/bdlab/beast/dataExplorer/DatasetProcessor.scala:58_

### Goal
Returns the integer identifier of the current `DatasetProcessor` instance.

### Parameters
_None._

### Input
No arguments are provided to this method.

Preconditions from the provided facts:
- The method must be called on an instance/value that defines `id` (no verified README/test call site for this exact method was provided).
- No raster/vector file input is required for this call itself.

### Output
Returns `Int` — the ID value associated with the object instance on which `id` is called.

### Valid Call Patterns
```scala
// Inferred from signature only (no verbatim README/test call for `id` was provided)
val datasetId: Int = value.id
```

### LLM Instruction Prompt
- Call `id` as a parameterless member access (`value.id`), not as `id()` unless the concrete type explicitly requires parentheses.
- Do not add arguments; signature is exactly `def id: Int`.
- Ensure the receiver object actually has this method in scope.
- Treat this as a metadata/accessor call; it does not load GeoTIFF/HDF or perform raster transforms by itself.

### Prompt Snippet
```text
Get the processor identifier as an Int by calling `value.id` on the existing DatasetProcessor-like instance. Do not pass any parameters.
```

### Common Failure Modes
- Calling `id` on the wrong receiver type (compile error: member `id` not found).
- Writing `id(...)` with arguments (compile error due to no-arg signature).
- Assuming this method performs RDPro raster I/O or Spark actions; provided facts only define it as returning an `Int`.

### Fix Code Hint
```scala
// Ensure you have the correct receiver instance, then read the property-like method
val datasetId: Int = value.id
```

## API Test: `image`

### Signature
```scala
private def image(): Unit
```
_Source: beast/satex/src/main/scala/edu/ucr/cs/bdlab/beast/satex/ImageIterator.scala:58_

### Goal
Provides an internal, zero-argument method named `image` in `ImageIterator` that performs side-effectful work and does not return a value.

### Parameters
_None._

### Input
Because this method is `private` and has no public doc/test/readme usage here, the required runtime input is **not documented** in the provided sources.  
No file-format-specific contract (GeoTIFF/HDF/etc.) is stated for this method itself.

### Output
Returns `Unit` — it does not produce a direct Scala value; any effect is internal side effects in its owning class context (not specified in the provided docs).

### Valid Call Patterns
```scala
// Inferred from signature only (not verified by tests or README examples):
image()
```

### LLM Instruction Prompt
- Treat `image` as an internal/private method; do not use it as a public RDPro API in user pipelines.
- Do not invent arguments, overloads, or return data.
- If generating runnable user code, prefer documented public raster APIs (`sc.geoTiff[T]`, `mapPixels`, `overlay`, `reshapeNN`, `saveAsGeoTiff`) instead of this private method.
- If access context is missing, state that `private def image(): Unit` is not callable from outside its defining class/object.

### Prompt Snippet
```text
Use `image()` only when you are inside the defining scope of `ImageIterator`; it takes no parameters and returns Unit. Do not add arguments or expect a return value.
```

### Common Failure Modes
- Calling `image()` from outside `ImageIterator` (or its allowed private scope), causing an access error due to `private`.
- Assuming it returns raster data or metadata; return type is strictly `Unit`.
- Inventing a receiver/arguments such as `obj.image(path)`; no parameters are defined.

### Fix Code Hint
```scala
// If you are outside the private scope, switch to public RDPro APIs instead:
import edu.ucr.cs.bdlab.beast._

val raster: RasterRDD[Int] = sc.geoTiff[Int]("glc2000_v1_1.tif")
raster.saveAsGeoTiff("output")
```

## API Test: `initialized`

### Signature
```scala
def initialized: Boolean
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/shapefilev2/ShapefileReader.scala:48_

_Source doc:_ A flag that is raised after the file has been initialized

### Goal
Check whether a shapefile reader instance has already completed its file initialization step before you proceed with shapefile-dependent processing.

### Parameters
_None._

### Input
This method takes no arguments, but it must be called on an existing object instance that defines `initialized` (from the shapefile reader context in `shapefilev2`).

Preconditions from the provided facts:
- No explicit parameter/data-format precondition is documented for this method itself.
- Since it is a file-initialization flag, it is meaningful only in a workflow where a file-backed reader lifecycle exists (e.g., shapefile reader setup/open/init flow).

### Output
Returns `Boolean` — `true` means the file has been initialized; `false` means it has not been initialized yet.

### Valid Call Patterns
```scala
// Inferred from signature (no test-suite or README call example was provided)
val isReady: Boolean = value.initialized
```

### LLM Instruction Prompt
- Call it as a zero-argument property-style method: `value.initialized`.
- Do not add arguments (signature is `def initialized: Boolean`).
- Do not invent alternate overloads or static/object call forms.
- Treat the result strictly as an initialization-state flag.

### Prompt Snippet
```text
Given a shapefile-reader instance `value`, check initialization state with:
`val isReady: Boolean = value.initialized`
If false, run the reader’s initialization/open step before file-dependent operations.
```

### Common Failure Modes
- Calling `initialized` on the wrong receiver type (an object that does not define this method).
- Assuming `initialized == true` implies anything beyond “file has been initialized” (no stronger guarantees are documented).
- Passing arguments to `initialized` (none are accepted).

### Fix Code Hint
```scala
// Correct: zero-arg flag check on a valid receiver
val isReady: Boolean = value.initialized
if (!isReady) {
  // invoke the reader's documented initialization/open routine (API not provided here)
}
```

## API Test: `isCW`

### Signature
```scala
def isCW: Boolean
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/LiteGeometry.scala:97_

_Source doc:_ Checks whether this list of points form a closed ring stored in CW order @return `true` if the points form a ring and the ring is stored in clock-wise order

### Goal
Determine whether a ring geometry (point list) is both closed and stored in clockwise (CW) order, which is used in Beast/RDPro geometry handling (for example, polygon shell orientation checks).

### Parameters
_None._

### Input
Call this on a geometry/ring object that exposes `isCW` (as shown in tests: a `LitePolygon` part, e.g., `simplifiedPolygon.asInstanceOf[LitePolygon].parts(0)`).

Preconditions from the API/source doc:
- The underlying point list must represent a **ring candidate**.
- `isCW` only returns `true` when the points both:
  1. form a **closed ring**, and
  2. are ordered **clockwise**.

No file format input is involved directly for this method; it is an in-memory geometry check.

### Output
Returns `Boolean` — `true` means the points form a closed ring and that ring is in clockwise order; `false` means either it is not a closed ring, not clockwise, or both.

### Valid Call Patterns
```scala
assert(simplifiedPolygon.asInstanceOf[LitePolygon].parts(0).isCW, "Outer ring was not in CW order")
```

### LLM Instruction Prompt
- Use the instance call form shown in tests: `value.isCW`.
- Do not pass arguments (`isCW` has no parameters).
- Use it on ring-like geometry data (e.g., polygon part/ring), not on raster objects.
- Interpret `true` strictly as “closed ring + clockwise order,” per source doc.

### Prompt Snippet
```text
Given a simplified polygon in Beast visualization types, check clockwise orientation of the outer ring using the tested call form:
simplifiedPolygon.asInstanceOf[LitePolygon].parts(0).isCW
Treat true as: the points form a closed ring and are in CW order.
```

### Common Failure Modes
- Calling `isCW` on the wrong type (e.g., non-ring/non-lite-geometry object), which will fail before orientation logic is applied.
- Assuming `true` means only clockwise ordering; per API doc it also requires a **closed ring**.
- Using a geometry result that is not a polygon ring (test context shows simplification can produce `LiteLineString` for very small polygons), so ring checks are not applicable.

### Fix Code Hint
```scala
val simplifiedPolygon = interTile.simplifyGeometry(polygon)
if (simplifiedPolygon.isInstanceOf[LitePolygon]) {
  val outerRingIsCW = simplifiedPolygon.asInstanceOf[LitePolygon].parts(0).isCW
  println(outerRingIsCW)
}
```

## API Test: `isDefined`

### Signature
```scala
@inline def isDefined(i: Int, j: Int): Boolean
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/ITile.scala:126_

_Source doc:_ Checks if the given pixel is defined (not empty) @param i the index of the column @param j the index of the row @return `true` if pixel has a valid value or `false` if it does not.

### Goal
Check whether a specific raster pixel location in a tile has a valid (non-empty) value before using it in raster analytics.

### Parameters
- `i` (`Int`): Column index of the pixel to test.
- `j` (`Int`): Row index of the pixel to test.

### Input
Call this on an `ITile` instance (or compatible tile object that provides this method), with pixel indices `(i, j)` for the target cell.

Preconditions from available docs/context:
- The method is pixel-level and assumes you are working with raster tile data already loaded/produced in RDPro workflows (e.g., from GeoTIFF/HDF pipelines).
- `i` and `j` should refer to a valid pixel position in that tile’s grid. (Exact out-of-range behavior is not documented in the provided sources.)

### Output
Returns `Boolean` — `true` means the pixel at `(i, j)` is defined (has a valid value), and `false` means it is empty / not defined.

### Valid Call Patterns
```scala
val isSet: Boolean = tile.isDefined(i, j) // inferred from signature; no verbatim README/test call for this overload was provided
```

### LLM Instruction Prompt
- Use instance-method form on a tile-like receiver: `value.isDefined(i, j)`.
- Pass exactly two `Int` arguments in order: column index first, row index second.
- Do not invent extra parameters (e.g., band index, nodata value, CRS, metadata).
- Treat this as a per-pixel validity check only; it does not load data, reproject, reshape, or aggregate.

### Prompt Snippet
```text
Given an existing raster tile object `tile`, check pixel validity with:
`tile.isDefined(i, j)`.
Use `i` as column index and `j` as row index, both Int.
```

### Common Failure Modes
- Calling `isDefined` as a standalone/global function instead of on a tile instance.
- Swapping index meaning/order (`j, i` instead of `i, j`).
- Assuming it performs raster compatibility fixes (CRS/resolution/tile-size alignment). Those are separate reshape/reproject steps in RDPro.
- Using indices that do not correspond to the tile extent (bounds behavior is not specified in provided docs).

### Fix Code Hint
```scala
// Correct call shape: instance method on a tile object
val defined: Boolean = tile.isDefined(i, j)
if (defined) {
  // safe to read/use this pixel in your logic
}
```

## API Test: `isEmptyAt`

### Signature
```scala
def isEmptyAt(x: Double, y: Double): Boolean
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/ITile.scala:114_

_Source doc:_ Check if the pixel that contains the given location is empty @param x the x-coordinate of the point, e.g., longitude @param y the y-coordinate of the point, e.g., latitude @return `true` if the pixel at the location is empty, i.e., contains no data

### Goal
Check whether the raster pixel covering a given map location `(x, y)` is no-data/empty in an RDPro/Beast tile.

### Parameters
- `x` (`Double`): X coordinate of the query point (for example, longitude), in the same coordinate space used by the tile metadata.
- `y` (`Double`): Y coordinate of the query point (for example, latitude), in the same coordinate space used by the tile metadata.

### Input
A raster tile object that implements this method (as used in tests: `tile1.isEmptyAt(...)`), plus numeric coordinates as `Double`.

Preconditions from observed usage:
- The tile must already be read/loaded from raster data (e.g., via `GeoTiffReader.readTile(...)`).
- Coordinates should be meaningful for that tile’s georeferencing (same CRS/space as the tile metadata); otherwise the result may not represent the intended location.
- No file format is passed directly to `isEmptyAt`; format handling (GeoTIFF/HDF, etc.) happens earlier when reading raster data.

### Output
Returns `Boolean` — `true` means the pixel containing `(x, y)` is empty (contains no data), and `false` means it is not empty.

### Valid Call Patterns
```scala
val rasterPath = locateResource("/rasters/glc2000_small.tif")
val fileSystem = new Path(rasterPath.getPath).getFileSystem(new Configuration())
val reader = new GeoTiffReader[Int]
try {
  reader.initialize(fileSystem, rasterPath.getPath, "0", "fillvalue" -> 8)
  val tile1 = reader.readTile(reader.metadata.getTileIDAtPoint(23.224, 32.415))
  assert(tile1.isEmptyAt(23.224, 32.415))
} finally {
  reader.close()
}
```

### LLM Instruction Prompt
- Call this as an instance method on a tile object: `tile.isEmptyAt(x, y)`.
- Pass both coordinates as `Double`.
- Use coordinates in the tile’s coordinate reference space.
- Do not invent extra parameters (there are only `x` and `y`).
- Load/read raster data first; `isEmptyAt` is a per-tile query, not a file-loading API.

### Prompt Snippet
```text
Given a loaded raster tile (e.g., tile1 from GeoTiffReader.readTile), call:
tile1.isEmptyAt(x, y)
where x and y are Double coordinates in the tile’s coordinate system. 
Interpret true as no-data/empty pixel at that location.
```

### Common Failure Modes
- Calling `isEmptyAt` without a tile instance (it is not shown as a static/global function).
- Passing coordinates in a different CRS/space than the tile uses.
- Expecting this method to load files or perform reprojection/alignment automatically (it does neither).
- Using non-`Double` coordinate literals in strict contexts without conversion.

### Fix Code Hint
```scala
// Ensure you already have a tile, then query emptiness at map coordinates
val tile1 = reader.readTile(reader.metadata.getTileIDAtPoint(23.224, 32.415))
val isNoData: Boolean = tile1.isEmptyAt(23.224, 32.415)
```

## API Test: `isSpatiallyPartitioned`

### Signature
```scala
def isSpatiallyPartitioned: Boolean
def isSpatiallyPartitioned(rdd: JavaSpatialRDD): Boolean
```
_Source: beast/beast-spark/src/main/scala/edu/ucr/cs/bdlab/beast/JavaSpatialRDDHelper.scala:45  (+1 more definition site/overload)_

_Source doc:_ Tells whether a SpatialRDD is partitioned using any spatial partitioner or not @return {@code true} if the RDD is partitioned using any spatial partitioner

### Goal
Checks whether a spatial RDD in Beast/RDPro is currently partitioned by any spatial partitioner.

### Parameters
- `rdd` (`JavaSpatialRDD`): The `JavaSpatialRDD` instance to test for presence of a spatial partitioner (overload form).

### Input
A `JavaSpatialRDD` must be available (for the overload that takes `rdd`).  
No file-path or raster format input is consumed by this function directly; it inspects partitioning state on an already-created spatial RDD object.

Preconditions from project usage context:
- If you need this to return `true`, the dataset must have been spatially partitioned earlier (for example via documented partitioning workflows such as `spatialPartition(...)` / indexing workflows).
- This API does not apply partitioning; it only reports existing partitioning state.

### Output
Returns `Boolean` — `true` means the spatial RDD is partitioned using some spatial partitioner; `false` means it is not spatially partitioned.

### Valid Call Patterns
```scala
// Inferred from the API signature (no verbatim README/test call for this API was provided)
val partitioned: Boolean = rdd.isSpatiallyPartitioned
```

```scala
// Inferred from the API signature overload (no verbatim README/test call for this API was provided)
val partitioned: Boolean = isSpatiallyPartitioned(rdd)
```

### LLM Instruction Prompt
- Call this API only to **check** partitioning status; do not describe it as performing partitioning.
- Use it on an existing `JavaSpatialRDD`.
- If code needs spatial partitioning before join/query performance optimizations, call partitioning APIs first, then re-check with `isSpatiallyPartitioned`.
- Do not invent extra parameters or return fields; output is only `Boolean`.

### Prompt Snippet
```text
Given an existing JavaSpatialRDD named rdd, check whether it already has a spatial partitioner:
`val partitioned: Boolean = rdd.isSpatiallyPartitioned`
If false and downstream logic requires partitioning, apply a spatial partitioning step separately, then check again.
```

### Common Failure Modes
- Assuming this method partitions data. It does not; it only reports status.
- Calling it before constructing/loading a spatial RDD object.
- Expecting details such as partitioner type/name; this API returns only `Boolean`.

### Fix Code Hint
```scala
// Inferred usage: check first
val partitioned: Boolean = rdd.isSpatiallyPartitioned

// If false, run your project’s spatial partitioning step (separate API), then re-check:
val partitionedAfter: Boolean = rdd.isSpatiallyPartitioned
```

## API Test: `lastNFiles`

### Signature
```scala
def lastNFiles(fs: FileSystem, path: Path, n: Int): Array[(String, Long, Long)]
```
_Source: beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/util/ZipUtil.scala:48_

_Source doc:_ Returns information about the last n files in the archive. **Compatibility Note**: This method is not guaranteed to return the correct answer. For efficiency, it tries to locate the directory entries from the end using the ZIP signature. In rare cases, it might retrieve false information since the signature might appear out of coincidence. To be accurate, this method has to read all ZIP entries until it finds the last ones because directory entries are variable size in ZIP. @param fs the file system that contains the ZIP archive @param path the path to the ZIP file @param n the number of entries to retrieve from the end @return file names, offsets, and lengths for the last n entries if the ZIP file contains at least n entries. Otherwise, it returns all entries in the file.

### Goal
Retrieve metadata for the last `n` entries in a ZIP archive (name, byte offset, and byte length) from a Hadoop `FileSystem` path.

### Parameters
- `fs` (`FileSystem`): Hadoop file system that contains the ZIP archive (e.g., local FS in tests).
- `path` (`Path`): Path to the ZIP file in that file system.
- `n` (`Int`): Number of entries to retrieve from the end of the archive.

### Input
The caller must provide:
- A valid `FileSystem`.
- A `Path` pointing to a ZIP archive.
- An integer `n` indicating how many trailing entries are requested.

Preconditions / compatibility notes:
- The method is designed for ZIP archives (tests cover regular ZIP and ZIP64 archives).
- If the ZIP has fewer than `n` entries, all entries are returned.
- **Important compatibility caveat from source doc:** this method is optimized and may return incorrect results in rare cases because it searches for ZIP signatures from the end; signatures can appear coincidentally in data. A fully accurate approach would require reading all ZIP entries.

### Output
Returns `Array[(String, Long, Long)]` where each tuple is:
1. file name (`String`)
2. file content offset in the ZIP (`Long`)
3. file content length in bytes (`Long`)

The array contains up to the last `n` entries (or all entries if fewer than `n` exist).

### Valid Call Patterns
```scala
val lastFile: Array[(String, Long, Long)] = ZipUtil.lastNFiles(fileSystem, file1, 1)

val lastFiles: Array[(String, Long, Long)] = ZipUtil.lastNFiles(fileSystem, file1, 2)
```

### LLM Instruction Prompt
- Use the exact receiver and argument order shown in tested code: `ZipUtil.lastNFiles(fileSystem, filePath, n)`.
- Pass a Hadoop `FileSystem` and `Path` to a ZIP file.
- Treat returned tuples as `(name, offset, length)`.
- Warn users that results are not strictly guaranteed correct in rare signature-collision cases.

### Prompt Snippet
```text
Use ZipUtil.lastNFiles(fs, path, n) to read the last ZIP entries metadata. Inputs must be a Hadoop FileSystem and Path to a ZIP (ZIP64 is also covered by tests). Interpret each result tuple as (fileName, offset, length). Note: method is optimized and may be inaccurate in rare cases due to ZIP-signature coincidence.
```

### Common Failure Modes
- Passing a non-ZIP file path: method behavior is not documented for other formats.
- Assuming strict correctness in all cases: source doc explicitly says rare false matches can occur.
- Misreading tuple fields (e.g., treating `_2` as length instead of offset).
- Requesting `n` larger than archive entries and expecting exactly `n` results (it returns all available entries).

### Fix Code Hint
```scala
val entries: Array[(String, Long, Long)] = ZipUtil.lastNFiles(fileSystem, zipPath, 2)

val in = fileSystem.open(zipPath)
try {
  val (name, offset, length) = entries(0)
  in.seek(offset)
  val bytes = new Array[Byte](length.toInt)
  in.readFully(bytes)
  // bytes now contains the entry payload for `name`
} finally {
  in.close()
}
```

## API Test: `listFilesInZip`

### Signature
```scala
def listFilesInZip(fileSystem: fs.FileSystem, zipFilePath: Path): Array[(String, Long, Long)]
```
_Source: beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/util/ZipUtil.scala:478_

_Source doc:_ List all files contained in the given ZIP file @param fileSystem the file system that contains the zip file @param zipFilePath the ZIP file to return its contents @return

### Goal
List all file entries inside a ZIP archive (including ZIP64 archives) and return each entry’s name plus byte location/size metadata for random-access reading.

### Parameters
- `fileSystem` (`fs.FileSystem`): Hadoop-compatible file system instance that can open/read the ZIP file (for example, local FS from `FileSystem.getLocal(new Configuration())`).
- `zipFilePath` (`Path`): Path to the ZIP file whose internal file entries should be listed.

### Input
A valid ZIP file reachable through the provided `fileSystem` at `zipFilePath`.  
From tests, this works for regular ZIP and ZIP64.  
Preconditions:
- `fileSystem` and `zipFilePath` must refer to the same storage backend/context.
- The path must exist and be readable.
- The file must be a ZIP archive parseable by RDPro/Beast ZIP utilities.

### Output
Returns `Array[(String, Long, Long)]` where each tuple represents one ZIP entry:
1. `String`: entry/file name inside the ZIP (e.g., `"README.bin"`),
2. `Long`: byte offset usable with `FSDataInputStream.seek(...)` on the ZIP file,
3. `Long`: entry byte length.

### Valid Call Patterns
```scala
val fileSystem = FileSystem.getLocal(new Configuration())
val contents = ZipUtil.listFilesInZip(fileSystem, new Path(file1.getPath))
```

```scala
val files = ZipUtil.listFilesInZip(fileSystem, file1)
```

### LLM Instruction Prompt
- Use the exact static call form `ZipUtil.listFilesInZip(fileSystem, zipFilePath)`.
- Pass a Hadoop `fs.FileSystem` and a Hadoop `Path`; do not pass plain strings directly.
- Ensure the ZIP path is accessible by that exact filesystem instance.
- Treat returned tuples as `(entryName, offset, length)`.

### Prompt Snippet
```text
Use ZipUtil.listFilesInZip(fileSystem, zipFilePath) to enumerate ZIP contents.
`fileSystem` must be an fs.FileSystem that can open `zipFilePath` (Path).
Interpret each returned tuple as (name, byteOffset, byteLength).
```

### Common Failure Modes
- Passing a path that does not exist or is unreadable on the provided filesystem.
- Filesystem/path mismatch (e.g., local `FileSystem` with a non-local path context).
- Assuming the return type is only names; it also includes offset and size.
- Passing a non-ZIP file and expecting valid ZIP entry metadata.

### Fix Code Hint
```scala
import org.apache.hadoop.conf.Configuration
import org.apache.hadoop.fs.{FileSystem, Path}
import edu.ucr.cs.bdlab.beast.util.ZipUtil

val fileSystem = FileSystem.getLocal(new Configuration())
val zipPath = new Path("/path/to/archive.zip") // must exist on this fileSystem
val entries: Array[(String, Long, Long)] = ZipUtil.listFilesInZip(fileSystem, zipPath)

// Example: random-access read of first entry bytes
val in = fileSystem.open(zipPath)
in.seek(entries(0)._2)
val data = new Array[Byte](entries(0)._3.toInt)
in.readFully(data)
in.close()
```

## API Test: `locateResource`

### Signature
```scala
def locateResource(srcPath: String): File
```
_Source: beast/commontest/src/main/scala/org/apache/spark/test/ScalaSparkTest.scala:293_

_Source doc:_ Returns the relative or full path to the given resource @param srcPath a path to a resource that starts with "/" @return the path of the file of the given resource

### Goal
Resolve a test/resource path string into a `File` path that can be passed to Beast/RDPro operations that expect filesystem input paths.

### Parameters
- `srcPath` (`String`): Path to the resource to locate; source doc states this path starts with `"/"`.

### Input
A resource path string (not raster pixels or vector features), typically used in tests to locate bundled input files before passing `file.getPath` into downstream APIs (for example, `GeometricSummary.run`).

Preconditions from provided sources:
- `srcPath` should start with `"/"` (from the source doc).
- The resource must exist and be locatable in the runtime test/classpath environment (exact lookup behavior beyond source doc is not specified here).

### Output
Returns `File` — the located file path for the requested resource (relative or full path per source doc), suitable for calls that require a filesystem path string via `getPath`.

### Valid Call Patterns
```scala
val inputfile = locateResource("/test.partitions")
val opts = new BeastOptions().set("iformat", "wkt(Geometry)")
  .set("skipheader", true)
  .set("separator", "\t")
val summary = GeometricSummary.run(opts, Array(inputfile.getPath), null, sparkContext).asInstanceOf[Summary]
```

### LLM Instruction Prompt
- Call exactly `locateResource(srcPath: String)` and pass one string argument.
- Use a resource-style path that starts with `/` (per source doc).
- Use the returned `File` as a path holder (e.g., `inputfile.getPath`) for downstream Beast APIs.
- Do not invent extra parameters, overloads, or return types.

### Prompt Snippet
```text
Use locateResource with a single String resource path that starts with "/".
Store the returned File, then pass file.getPath into APIs that require input paths.
Example form: val inputfile = locateResource("/test.partitions")
```

### Common Failure Modes
- Passing a path that does not start with `/` (violates documented parameter expectation).
- Supplying a resource name that is not available in the runtime resource/classpath environment.
- Treating the return as `String` directly instead of `File` (use `.getPath` when a string path is required).
- Attempting to call nonexistent overloads or additional arguments.

### Fix Code Hint
```scala
val inputfile = locateResource("/test.partitions")
val inputPath: String = inputfile.getPath
```

## API Test: `makeBoxes`

### Signature
```scala
def makeBoxes(maxSize: Int*): JavaSpatialGeneratorBuilder
def makeBoxes(maxSize: Double*): SpatialGeneratorBuilder
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/generator/JavaSpatialGeneratorBuilder.scala:76  (+1 more definition site/overload)_

_Source doc:_ Generate boxes around each generated point @param maxSize the maximum size for each side length of the generated box @return

### Goal
Configure the spatial data generator to emit **box geometries** around generated points, with each side length bounded by `maxSize` as a fraction of the dataset bounding box.

### Parameters
- `maxSize` (`Int*`): Variadic maximum side length(s) for generated boxes; values are interpreted as fractions in `[0, 1]` of the dataset bounding box per source docs, and values above `1.0` are invalid.

### Input
Call this on a spatial generator builder (as shown via `sparkContext.generateSpatialData` / `sc.generateSpatialData`) before a generator terminal call such as `.uniform(...)`.

Preconditions from docs/context:
- `maxSize` should be in `[0, 1]` according to source docs.
- Any `maxSize` value `> 1.0` is invalid.
- This API is for generated geometries (not raster file I/O); no raster/vector file format input is required at this step.

### Output
Returns `JavaSpatialGeneratorBuilder` — a configured generator-builder object (builder state), ready for additional chained configuration and a generation call (for example, `.uniform(...)`) to produce spatial data.

### Valid Call Patterns
```scala
sparkContext.generateSpatialData
      .makeBoxes(0.3, 0.4)
      .uniform(1000000)

sc.generateSpatialData
  .makeBoxes(0.1, 0.2)
  .uniform(100)
  .plotImage(300, 300, "uniform.png")
```

### LLM Instruction Prompt
- Use the instance call form exactly as documented: `value.makeBoxes(...)` on a generator builder (`sparkContext.generateSpatialData` or `sc.generateSpatialData`).
- Keep `maxSize` values within `[0, 1]`; never emit values above `1.0`.
- Chain to a generation method like `.uniform(n)`; `makeBoxes` alone only configures the builder.
- Do not invent extra parameters.

### Prompt Snippet
```text
Use `sc.generateSpatialData.makeBoxes(...)` to generate box geometries. Pass one or more max side sizes as fractions of the dataset MBR in [0,1], then call `.uniform(count)`. Do not use values > 1.0.
```

### Common Failure Modes
- Passing `maxSize` values greater than `1.0` (explicitly invalid by source docs).
- Calling `makeBoxes` as a standalone function instead of on a builder instance (`value.makeBoxes(...)`).
- Expecting output geometries without a terminal generation call (e.g., forgetting `.uniform(...)`).

### Fix Code Hint
```scala
val generated = sc.generateSpatialData
  .makeBoxes(0.1, 0.2)   // keep all values <= 1.0
  .uniform(100)
```

## API Test: `mapPixels`

### Signature
```scala
def mapPixels[U: ClassTag](f: T => U)
def mapPixels[T: ClassTag, U: ClassTag](inputRaster: RasterRDD[T], f: T => U): RasterRDD[U]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsLocal.scala:38  (+1 more definition site/overload)_

_Source doc:_ Apply a user-defined function for each pixel in the input raster to produce the output raster @param inputRaster the input raster RDD @param f the function to apply on each input pixel value to produce the output pixel value @tparam T the type of pixels in the input @tparam U the type of pixels in the output @return the resulting RDD

### Goal
Apply per-pixel band math/value transformation on a raster (e.g., unit conversion or thresholding) and return a new raster with transformed pixel type/value.

### Parameters
- `inputRaster` (`RasterRDD[T]`): the input raster RDD whose pixel values are read as type `T`.
- `f` (`T => U`): user function applied to each input pixel value to produce one output pixel value of type `U`.

### Input
A `RasterRDD[T]` already loaded in RDPro (commonly from GeoTIFF via `sc.geoTiff[T]` or HDF via `sc.hdfFile(...)` in project examples), plus a pure pixel-mapping function `T => U`.

Preconditions/type rules to keep calls valid:
- `T` must match the raster’s real runtime pixel type when loading typed rasters (e.g., `sc.geoTiff[Int]`, `sc.geoTiff[Float]`, `sc.geoTiff[Array[Int]]`, `sc.geoTiff[Array[Float]]`).
- Choose `U` to match your intended output pixel values (e.g., `Float => Float` for temperature conversion, `Short => Int` for thresholding with widening).
- Call shape should use the real receiver form shown in project usage (`value.mapPixels(...)`), which is documented and portable.

### Output
Returns `RasterRDD[U]` — a raster RDD with the same raster structure/coverage as input, but with each defined pixel value transformed by `f` into type `U`.

### Valid Call Patterns
```scala
val temperatureK: RasterRDD[Float] =
  sc.hdfFile("MOD11A1.A2022173.h08v05.006.2022174092443.hdf", "LST_Day_1km")
val temperatureF: RasterRDD[Float] = temperatureK.mapPixels(k => (k-273.15f) * 9 / 5 + 32)
temperatureF.saveAsGeoTiff("temperature_f")
```

```scala
val outputRaster: RDD[ITile[Int]] = RasterOperationsLocal.mapPixels(inputRaster, (x: Short) => Math.max(x, 50))
```

### LLM Instruction Prompt
- Use the receiver form `raster.mapPixels(f)` when you already have a `RasterRDD[T]`.
- Ensure typed raster loading uses the correct `T` for source pixels before mapping.
- Make `f` a single-pixel transform `T => U`; do not pass multi-argument or neighborhood functions.
- If changing numeric range/type, set `U` explicitly via assignment type context (e.g., `RasterRDD[Int]`).
- Save raster outputs with GeoTIFF APIs when persistence is required.

### Prompt Snippet
```text
Given a RasterRDD[T], call mapPixels as raster.mapPixels(pixel => ...). 
Keep the lambda type-compatible with T => U, and ensure T matches the source raster load type (e.g., geoTiff[Int], geoTiff[Float], hdfFile layer type). 
Return/use RasterRDD[U], and save with saveAsGeoTiff(...) if output is needed on disk.
```

### Common Failure Modes
- Loading raster with wrong type parameter (`sc.geoTiff[T]`) so `mapPixels` lambda type does not match actual pixels.
- Using a lambda that is not `T => U` (wrong input type or returns unexpected type).
- Assuming `mapPixels` performs reprojection/resampling/alignment; it only transforms pixel values.
- Trying to write non-GeoTIFF output from raster pipeline when task expects GeoTIFF.

### Fix Code Hint
```scala
import edu.ucr.cs.bdlab.beast._

val input: RasterRDD[Float] =
  sc.hdfFile("MOD11A1.A2022173.h08v05.006.2022174092443.hdf", "LST_Day_1km")

val output: RasterRDD[Float] =
  input.mapPixels(k => (k - 273.15f) * 9 / 5 + 32)

output.saveAsGeoTiff("temperature_f")
```

## API Test: `mbr`

### Signature
```scala
def mbr : EnvelopeNDLite
def mbr: EnvelopeNDLite
def mbr(mbr: EnvelopeNDLite): SpatialGeneratorBuilder
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/generator/SpatialGeneratorBuilder.scala:97  (+2 more definition site/overload)_

_Source doc:_ Generates data in the given bounding box @param mbr the bounding box of the generated data @return

### Goal
Set the spatial bounding box used by the spatial data generator so generated geometries are constrained to a specified MBR.

### Parameters
- `mbr` (`EnvelopeNDLite`): The target bounding box (minimum bounding rectangle / envelope) within which generated data should be created.

### Input
This call does not read raster/vector files directly; it configures a `SpatialGeneratorBuilder` pipeline.  
Preconditions:
- You must provide a valid `EnvelopeNDLite` instance.
- `mbr(...)` is used as part of a generator chain (for example before `.uniform(...)`), on a real builder receiver.

### Output
Returns `SpatialGeneratorBuilder` — the same generator builder configured with the given bounding box, so you can continue chaining generator configuration and generation calls (for example distribution settings and `.uniform(...)`).

### Valid Call Patterns
```scala
val desiredMBR = new EnvelopeNDLite(2, 2, 3, 9, 8)
val randomPoints: SpatialRDD = new SpatialGeneratorBuilder(sparkContext).mbr(desiredMBR)
  .config(UniformDistribution.MaxSize, "0.2,0.1")
  .config(UniformDistribution.NumSegments, 10)
  .config(UniformDistribution.GeometryType, "box")
  .config(SpatialGenerator.Seed, 1794)
  .uniform(10)
```

```scala
println(sparkContext.generateSpatialData
  .mbr(new EnvelopeNDLite(2, 1.0, 0.0, 4.0, 8.0))
  .uniform(1000)
  .summary)
```

### LLM Instruction Prompt
- Call `mbr` as an instance method on a real generator builder receiver (for example `new SpatialGeneratorBuilder(sparkContext)` or `sparkContext.generateSpatialData`).
- Pass exactly one argument of type `EnvelopeNDLite`.
- Do not invent extra parameters.
- If generation is intended, continue the chain with a generator method such as `.uniform(...)`.

### Prompt Snippet
```text
Create a spatial generator pipeline in Scala using Beast, set the generation bounding box with `.mbr(new EnvelopeNDLite(...))`, then generate data with `.uniform(...)`. Use a real builder receiver exactly as in Beast examples.
```

### Common Failure Modes
- Calling `mbr(...)` without a builder receiver (bare call), which typically will not compile.
- Passing a type other than `EnvelopeNDLite`.
- Expecting `mbr(...)` alone to generate output; it only configures the builder.

### Fix Code Hint
```scala
val builder = new SpatialGeneratorBuilder(sparkContext)
val configured = builder.mbr(new EnvelopeNDLite(2, 2, 3, 9, 8))
val generated = configured.uniform(1000)
```

## API Test: `mergeWith`

### Signature
```scala
def mergeWith(another: VectorCanvas): VectorCanvas
def mergeWith(another: MemoryTileWindow[T]): Unit
def mergeWith(opts: BeastOptions): BeastOptions
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/VectorCanvas.scala:440  (+2 more definition site/overload)_

_Source doc:_ Merges this canvas with another vector canvas and returns this canvas after the merge. @param another the other canvas to merge with @return this canvas after the merge so that you can chain a number of mergeWidth operations.

### Goal
Merge one in-memory tile/window/canvas state into another by taking defined content from `another` and applying it to the receiver object.

### Parameters
- `another` (`VectorCanvas`): the other canvas instance whose geometries/content are merged into the current canvas.

### Input
`mergeWith` is overloaded; this entry includes `VectorCanvas`, `MemoryTileWindow[T]`, and `BeastOptions` forms.

For the raster-memory-window form (authoritative API facts):
- Receiver must be a `MemoryTileWindow[T]`.
- Argument must be another `MemoryTileWindow[T]`.
- Behavior from source doc: defined values in the other window are merged into this one.

For the tested vector-canvas form:
- Receiver and argument are both `VectorCanvas`.
- Real test usage constructs both canvases with matching extents/dimensions before merge (same envelope/width/height shown in tests), then calls `canvas1.mergeWith(canvas2)`.

No file formats are involved directly in this API call (it is in-memory object merge).

### Output
Returns `VectorCanvas` — the same canvas instance after merge (per source doc text for this overload), enabling chaining.

For the `MemoryTileWindow[T]` overload, return type is `Unit` (in-place merge side effect only).

### Valid Call Patterns
```scala
canvas1.mergeWith(canvas2)
```

### LLM Instruction Prompt
- Use instance-call form exactly: `value.mergeWith(...)`.
- Pick the overload by receiver type:
  - `VectorCanvas.mergeWith(VectorCanvas): VectorCanvas`
  - `MemoryTileWindow[T].mergeWith(MemoryTileWindow[T]): Unit`
  - `BeastOptions.mergeWith(BeastOptions): BeastOptions`
- Do not invent extra parameters.
- For `MemoryTileWindow[T]`, treat merge as in-place because return type is `Unit`.

### Prompt Snippet
```text
Given two compatible in-memory objects of the same mergeWith overload, call receiver.mergeWith(argument) using exactly one argument. For MemoryTileWindow[T], do not assign return value (Unit); for VectorCanvas/BeastOptions, you may use the returned object for chaining.
```

### Common Failure Modes
- Calling the wrong overload type (e.g., passing `BeastOptions` to a `VectorCanvas` receiver).
- Assuming `MemoryTileWindow[T].mergeWith(...)` returns a merged object; it returns `Unit`.
- Using a bare `mergeWith(...)` without a receiver (usually will not compile).

### Fix Code Hint
```scala
// VectorCanvas overload (tested call form)
canvas1.mergeWith(canvas2)

// MemoryTileWindow overload (API-fact signature; in-place, returns Unit)
window1.mergeWith(window2)
```

## API Test: `mergeZip`

### Signature
```scala
def mergeZip(fileSystem: fs.FileSystem, mergedFile: Path, @varargs zipFiles: Path*): Unit
```
_Source: beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/util/ZipUtil.scala:425_

_Source doc:_ Merges multiple ZIP files into one and deletes the input files. @param mergedFile the output file that contains the merged ZIP files @param zipFiles the input files to be merged

### Goal
Merge multiple ZIP files into one ZIP output file, then delete the input ZIP files.

### Parameters
- `fileSystem` (`fs.FileSystem`): Hadoop-compatible filesystem handle used to read input ZIP files, write the merged ZIP, and delete input files.
- `mergedFile` (`Path`): Output ZIP file path to create; this ZIP will contain merged entries from all inputs.
- `@varargs zipFiles` (`Path*`): One or more input ZIP file paths to merge.

### Input
Caller must provide:
- A valid `fs.FileSystem` instance for the target storage backend (e.g., local FS/HDFS as configured).
- `Path` values for ZIP files (`zipFiles`) that exist and are readable.
- An output `Path` (`mergedFile`) where the merged ZIP can be written.

Preconditions from the API/test behavior:
- Inputs are ZIP files.
- The method deletes input files after merge (as documented and verified by test).
- No additional compatibility/type-parameter rules are documented for this API.

### Output
Returns `Unit` — side-effect only:
- Creates `mergedFile` as a merged ZIP archive.
- Deletes the input files passed in `zipFiles`.

### Valid Call Patterns
```scala
ZipUtil.mergeZip(fileSystem, mergedFile, file1, file2)
```

### LLM Instruction Prompt
- Use the object-qualified call form exactly: `ZipUtil.mergeZip(fileSystem, mergedFile, ...)`.
- Pass a `fs.FileSystem`, one output `Path`, and varargs input `Path`s in that order.
- Provide ZIP input paths only.
- Do not expect a return value; verify by checking filesystem state (output exists, inputs removed) if needed.

### Prompt Snippet
```text
Merge ZIP files with:
ZipUtil.mergeZip(fileSystem, mergedFile, zip1, zip2, ...)
Where `fileSystem` is fs.FileSystem, `mergedFile` is the output Path, and remaining args are input ZIP Paths. This call returns Unit and deletes input ZIP files after merging.
```

### Common Failure Modes
- Passing non-ZIP files in `zipFiles` (merge expects ZIP inputs).
- Using a `fileSystem` that cannot access the provided paths.
- Assuming input ZIP files remain after merge (they are deleted).
- Assuming a non-`Unit` return payload.

### Fix Code Hint
```scala
val fileSystem = FileSystem.getLocal(new Configuration())
val mergedFile = new Path(scratchPath, "merged.zip")
ZipUtil.mergeZip(fileSystem, mergedFile, file1, file2)
// Optional checks:
// fileSystem.exists(mergedFile) should be true
// fileSystem.exists(file1) / fileSystem.exists(file2) should be false
```

## API Test: `metadata`

### Signature
```scala
override def metadata: RasterMetadata
def metadata: RasterMetadata
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/GeoTiffReader.scala:165  (+2 more definition site/overload)_

### Goal
Return the raster file’s metadata (dimensions/georeferencing/tile layout) from an initialized raster reader so you can do coordinate/pixel/tile-aware raster processing correctly.

### Parameters
_None._

### Input
`metadata` takes no arguments, but it is called on a reader instance that has already been initialized on a raster input (e.g., GeoTIFF in the test usage).  
From the validated call patterns, precondition is: initialize the `GeoTiffReader[...]` first, then access `reader.metadata`.

### Output
Returns `RasterMetadata` — metadata of the raster file, used to access properties and transforms such as raster width/height, pixel scale, grid-to-model and model-to-grid conversions, and tile lookup helpers (as shown in tests).

### Valid Call Patterns
```scala
val reader = new GeoTiffReader[Array[Int]]
reader.initialize(fileSystem, rasterPath.toString, "0", new BeastOptions())
assert(reader.metadata.rasterWidth == 99)
assert(reader.metadata.rasterHeight == 72)
assert(reader.metadata.getPixelScaleX == 0.17578125)

val outPoint = new Point2D.Double
reader.metadata.gridToModel(0, 0, outPoint)
reader.metadata.modelToGrid(-0.06, 49.28, outPoint)
val tileID = reader.metadata.getTileIDAtPixel(37, 24)
```

```scala
val reader = new GeoTiffReader[Int]
reader.initialize(fileSystem, rasterPath.toString, "0", new BeastOptions)
assert(256 == reader.metadata.rasterWidth)
assert(128 == reader.metadata.rasterHeight)
val tile = reader.readTile(reader.metadata.getTileIDAtPoint(23.224, 32.415))
```

### LLM Instruction Prompt
- Call `metadata` as a zero-argument member access on an initialized reader instance: `reader.metadata`.
- Do not invent parameters; `metadata` has none.
- Use the returned `RasterMetadata` for coordinate transforms and tile/pixel addressing before downstream raster operations.
- Keep the receiver form exactly (`reader.metadata`) as in validated tests.

### Prompt Snippet
```text
After initializing GeoTiffReader, access `reader.metadata` (no args) to get RasterMetadata, then use it for rasterWidth/rasterHeight, gridToModel/modelToGrid, and tile-ID lookup.
```

### Common Failure Modes
- Calling `metadata` before `reader.initialize(...)` (reader not ready).
- Treating `metadata` like a method with parameters (it has none).
- Using wrong pixel type when creating `GeoTiffReader[T]` for the source raster data (type mismatch issues elsewhere in the pipeline).

### Fix Code Hint
```scala
val reader = new GeoTiffReader[Int]
try {
  reader.initialize(fileSystem, rasterPath.toString, "0", new BeastOptions)
  val md: RasterMetadata = reader.metadata
  println(md.rasterWidth -> md.rasterHeight)
} finally {
  reader.close()
}
```

## API Test: `modelToGrid`

### Signature
```scala
def modelToGrid(x: Double, y: Double, outPoint: Point2D.Double): Unit
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/RasterMetadata.scala:161_

_Source doc:_ Converts a point location from model (world) space to grid (pixel) space @param x the x-coordinate in the model space (e.g., longitude) @param y the y-coordinate in the model space (e.g., latitude) @param outPoint the output point that contains the grid coordinates

### Goal
Convert a world/model coordinate (for example longitude/latitude or projected coordinates) into raster grid (pixel) coordinates using a raster’s metadata transform.

### Parameters
- `x` (`Double`): X coordinate in model/world space (e.g., longitude or projected X), in the same CRS/units as the raster metadata.
- `y` (`Double`): Y coordinate in model/world space (e.g., latitude or projected Y), in the same CRS/units as the raster metadata.
- `outPoint` (`Point2D.Double`): Mutable output object that will be filled with the computed grid/pixel coordinates (`outPoint.x`, `outPoint.y`).

### Input
You call this on a `RasterMetadata` instance (as shown in tests: `reader.metadata.modelToGrid(...)`), so required input is:

- A valid raster metadata transform already initialized from a raster reader (e.g., GeoTIFF/HDF readers in RDPro/Raptor internals).
- Model-space coordinates `x`, `y` that are expressed in the raster’s model CRS/units.
- A non-null `Point2D.Double` instance to receive output.

Preconditions:
- Coordinate system compatibility is required: if `x`,`y` are in a different CRS than the raster metadata, results will be incorrect (no implicit reprojection is documented here).
- `outPoint` must be allocated by caller before invocation.

### Output
Returns `Unit` — the method writes the computed grid coordinates into `outPoint` in-place.

### Valid Call Patterns
```scala
val outPoint = new Point2D.Double
reader.metadata.modelToGrid(-6.679688, 53.613281, outPoint)
```

```scala
val pt = new Point2D.Double
reader.metadata.modelToGrid(Math.toRadians(-110.0) * HDF4Reader.Scale, Math.toRadians(30.0) * HDF4Reader.Scale, pt)
```

### LLM Instruction Prompt
- Call this as an instance method on raster metadata: `reader.metadata.modelToGrid(x, y, outPoint)`.
- Always create and pass a mutable `Point2D.Double` output object.
- Ensure `x` and `y` are in the same model CRS/units as `reader.metadata`.
- Do not expect a return value; read results from `outPoint.x` and `outPoint.y`.

### Prompt Snippet
```text
Given an initialized raster reader, allocate Point2D.Double and call:
reader.metadata.modelToGrid(xModel, yModel, outPoint)
Then use outPoint.x/outPoint.y as pixel coordinates. Keep CRS/units consistent with metadata.
```

### Common Failure Modes
- Passing coordinates in a different CRS/units than raster metadata, producing wrong pixel locations.
- Forgetting to initialize `outPoint` (`null`), causing runtime failure.
- Assuming the method returns coordinates directly (it returns `Unit`).
- Calling `modelToGrid` without a metadata receiver (bare call), which will not match documented usage.

### Fix Code Hint
```scala
val pt = new Point2D.Double
// x/y must be in the raster metadata model space
reader.metadata.modelToGrid(x, y, pt)
val pixelX = pt.x
val pixelY = pt.y
```

## API Test: `name`

### Signature
```scala
override def name(): String
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/SpatialFileSource.scala:93_

### Goal
Returns the operation/source name as a `String` for this `SpatialFileSource` implementation.

### Parameters
_None._

### Input
No arguments are passed to this method.  
The call form is **inferred from the signature** (no README or test snippet in the provided material calls this specific API).

### Output
Returns `String` — the name identifier of the implementing object/class, as plain text.

### Valid Call Patterns
```scala
value.name()
```

### LLM Instruction Prompt
- Call `name` as a zero-argument instance method.
- Do not add parameters.
- Expect a `String` result only.
- Since no verified README/test call exists for this API, treat `value.name()` as inferred from the signature.

### Prompt Snippet
```text
Call `name` on an existing SpatialFileSource-like instance with no arguments, and use the returned String as the source/operation name.
```

### Common Failure Modes
- Calling `name` as a static/object method when you only have an instance method (`override def`).
- Adding nonexistent arguments (signature is strictly `name(): String`).
- Assuming the returned string is a file path, CRS, or format descriptor (not documented in provided facts).

### Fix Code Hint
```scala
// Ensure `value` is an instance of a class that defines `override def name(): String`
val n: String = value.name()
println(n)
```

## API Test: `normal`

### Signature
```scala
def normal(mu: Double, sigma: Double): Double
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/generator/SpatialGenerator.scala:40_

_Source doc:_ Generate a random number in the range (-inf, +inf) from a normal distribution

### Goal
Generate one random scalar from a normal (Gaussian) distribution, typically for synthetic-data or stochastic pipeline steps.

### Parameters
- `mu` (`Double`): Mean of the normal distribution (center value).
- `sigma` (`Double`): Standard deviation of the normal distribution (spread).

### Input
Two scalar `Double` values (`mu`, `sigma`) are required; no raster/vector file input is involved in this call.  
Preconditions are not explicitly documented beyond the signature/source doc.

### Output
Returns `Double` — one sampled random value drawn from a normal distribution with the provided `mu` and `sigma`, in the range `(-inf, +inf)`.

### Valid Call Patterns
```scala
// Inferred from signature only (no test-suite or README call form provided)
normal(0.0, 1.0)
```

### LLM Instruction Prompt
- Use exactly two `Double` arguments in order: `(mu, sigma)`.
- Do not add extra parameters or named options.
- Since no authoritative receiver/qualifier form is documented in tests/README, treat this call shape as inferred from the signature.
- Keep this API separate from RDPro raster I/O operations; it does not read/write GeoTIFF/HDF/CSV directly.

### Prompt Snippet
```text
Call `normal` with two Double values: mean first, standard deviation second.
Example (inferred): normal(0.0, 1.0)
```

### Common Failure Modes
- Passing non-`Double` arguments (or wrong argument count).
- Assuming this function loads/processes raster tiles; it only returns one numeric random sample.
- Assuming documented behavior for invalid `sigma` values; constraints are not specified in the provided API facts.

### Fix Code Hint
```scala
val mu: Double = 10.0
val sigma: Double = 2.5
val x: Double = normal(mu, sigma)
```

## API Test: `numFeatures`

### Signature
```scala
def numFeatures: Long
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/SpatialPartition.scala:32_

_Source doc:_ Total number of features (records) in this partition

### Goal
Return the total count of feature records represented by the current partition/summary object in a Beast Spark workflow.

### Parameters
_None._

### Input
`numFeatures` takes no arguments and is called on an existing value that exposes this method (as shown in tests: `summary.numFeatures` where `summary` is a `Summary` returned by `GeometricSummary.run(...)`).

Data/file format handling happens before this call (for example, `iformat`, separators, header options), and `numFeatures` just reads the computed count from that result object.

### Output
Returns `Long` — the total number of features (records) in the associated partition/summary result, as a scalar integer count.

### Valid Call Patterns
```scala
val summary = GeometricSummary.run(opts, Array(inputfile.getPath), null, sparkContext).asInstanceOf[Summary]
assert(summary.numFeatures == 44)
```

### LLM Instruction Prompt
- Call `numFeatures` as a zero-argument property-style method on a valid receiver (for example, `summary.numFeatures`).
- Do not add parameters; signature is exactly `def numFeatures: Long`.
- Ensure the receiver is produced by a prior Beast operation (e.g., `GeometricSummary.run(...).asInstanceOf[Summary]`) before calling.
- Use the returned `Long` as a record count.

### Prompt Snippet
```text
After computing a Beast summary object, read feature count with `summary.numFeatures` (no arguments). Treat the result as a Long total record count.
```

### Common Failure Modes
- Calling `numFeatures` on the wrong type (receiver does not define `numFeatures`).
- Trying to pass arguments (none are accepted).
- Calling before computing/obtaining a summary/partition object.

### Fix Code Hint
```scala
val summary = GeometricSummary.run(opts, Array(inputfile.getPath), null, sparkContext).asInstanceOf[Summary]
val n: Long = summary.numFeatures
println(n)
```

## API Test: `numFields`

### Signature
```scala
def numFields: Int
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/shapefilev2/DBFWriter.scala:42_

_Source doc:_ Number of attributes in the file

### Goal
Return how many attributes (columns/fields) are present in the current record schema being read (for example, a GPX record in Beast I/O tests).

### Parameters
_None._

### Input
Call this on a record-like value that exposes `numFields` (authoritatively shown as `r.numFields` in tests while iterating a `GPXReader2`).  
From the provided sources, this is used with GPX input records; no additional arguments are required.

Preconditions from available facts:
- The receiver object must be a valid row/record instance from the reader iteration (e.g., `for (r <- gpxReader)`).
- This API has no type parameter and no file-path argument.

### Output
Returns `Int` — the number of attributes/fields in the record (schema width), e.g., `8` in the provided GPX test.

### Valid Call Patterns
```scala
assertResult(8)(r.numFields)
```

### LLM Instruction Prompt
- Call this as an instance member exactly in the form `r.numFields` (no parentheses needed).
- Do not add arguments; the method takes none.
- Use it on an existing record object from a Beast reader iteration (as in GPXReader2 tests).
- Treat the result as schema field count, not row count.

### Prompt Snippet
```text
Given a Beast record `r` from reader iteration, get its attribute count with `r.numFields` and compare it to the expected schema width.
```

### Common Failure Modes
- Calling `numFields` as a standalone function instead of on a record instance.
- Expecting it to return number of records in a file (it returns number of fields in one record/schema).
- Trying to pass parameters to `numFields` (it accepts none).

### Fix Code Hint
```scala
for (r <- gpxReader) {
  val n: Int = r.numFields
  // use n as the number of attributes in this record/schema
}
```

## API Test: `numNonEmptyGeometries`

### Signature
```scala
def numNonEmptyGeometries: Long
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/SpatialPartition.scala:35_

_Source doc:_ Number of non-empty geometries in this partition

### Goal
Return how many geometries in a `SpatialPartition` are non-empty, which is useful for partition-level geometric summary checks in Beast vector workflows.

### Parameters
_None._

### Input
A `SpatialPartition` receiver value (instance method call), e.g., a partition-level summary object produced by Beast operations.

Preconditions from available facts:
- The call form is instance-based (same style as sibling methods on the same class/object usage: `summary.numFeatures`).
- No file format is passed directly to this method.
- No additional compatibility/type-parameter rules are documented specifically for this method.

### Output
Returns `Long` — the count of non-empty geometries in the target partition (a scalar numeric summary value).

### Valid Call Patterns
```scala
// Inferred from signature and sibling instance-call style (no direct test/readme example for this exact method)
val nonEmptyCount: Long = spatialPartition.numNonEmptyGeometries
```

### LLM Instruction Prompt
- Call this as a zero-argument instance method on a `SpatialPartition` value.
- Do not add parameters (signature is exactly `def numNonEmptyGeometries: Long`).
- Treat the result as a partition summary count (`Long`), not as raster pixels/tiles or file output.
- If your variable is not a `SpatialPartition`, convert or obtain the correct object before calling.

### Prompt Snippet
```text
Given a SpatialPartition value `spatialPartition`, compute the number of non-empty geometries using the zero-arg instance method and store it as Long:
`val nonEmptyCount: Long = spatialPartition.numNonEmptyGeometries`
Do not pass any arguments.
```

### Common Failure Modes
- Calling it like a static/object method (no evidence for `SpatialPartition.numNonEmptyGeometries`).
- Supplying arguments, e.g., `numNonEmptyGeometries(...)` (invalid; takes none).
- Calling on the wrong receiver type (anything other than `SpatialPartition`).

### Fix Code Hint
```scala
// Correct: instance receiver, no arguments
val nonEmptyCount: Long = spatialPartition.numNonEmptyGeometries
```

## API Test: `numPartitions`

### Signature
```scala
def numPartitions(num: Int): JavaSpatialGeneratorBuilder
def numPartitions(num: Int): SpatialGeneratorBuilder
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/generator/JavaSpatialGeneratorBuilder.scala:66  (+1 more definition site/overload)_

_Source doc:_ Set the number of partitions in the output. If not set or set to zero, one partition will be generated for each one million records @param num the number of partitions in the generated RDD @return

### Goal
Set how many Spark partitions the generated spatial output RDD should have when building synthetic/random spatial data.

### Parameters
- `num` (`Int`): The requested number of partitions in the generated RDD; if not set or set to `0`, default behavior is one partition per one million records.

### Input
A `SpatialGeneratorBuilder` / `JavaSpatialGeneratorBuilder` instance (i.e., this is a builder method in a generator pipeline), plus an integer partition count.

Preconditions and compatibility notes from the available docs:
- `numPartitions` controls partition count for generated output RDDs; it does **not** load raster/vector files directly.
- If you pass `0` (or leave it unset), partitioning falls back to the documented default (1 partition per 1,000,000 records).
- No file-format-specific input is required by this method itself.

### Output
Returns `JavaSpatialGeneratorBuilder` — the same builder type (Java API overload) with partition-count configuration applied, so you can continue chaining generator settings before materializing the RDD.

### Valid Call Patterns
```scala
// Inferred from the signature (no direct README/test call to this exact method was provided)
val configured = generatorBuilder.numPartitions(16)
```

### LLM Instruction Prompt
- Call this as an instance method on an existing generator builder object: `value.numPartitions(num)`.
- Pass an `Int`.
- Use `0` only when you intentionally want default auto-partitioning (1 partition per 1M records).
- Do not invent extra parameters.

### Prompt Snippet
```text
Given a SpatialGeneratorBuilder (or JavaSpatialGeneratorBuilder), set explicit output partitioning with:
builder.numPartitions(desiredPartitionsInt)

If desiredPartitionsInt is 0, default partitioning is used (1 partition per 1,000,000 records).
```

### Common Failure Modes
- Calling `numPartitions` as a standalone function instead of on a builder instance.
- Passing a non-`Int` value.
- Assuming `0` means “no partitions”; per source doc, it triggers default automatic partitioning.

### Fix Code Hint
```scala
// Ensure you call on a builder instance and pass an Int
val configured = generatorBuilder.numPartitions(8)

// Or intentionally use default auto partitioning
val configuredDefault = generatorBuilder.numPartitions(0)
```

## API Test: `numPoints`

### Signature
```scala
def numPoints: Int
override def numPoints: Int
def numPoints: Long
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/LiteGeometry.scala:22  (+4 more definition site/overload)_

### Goal
Return the total number of points across a geometry object (used in Beast/RDPro geometry simplification and vector-tile workflows).

### Parameters
_None._

### Input
Call this on an existing geometry-like object instance that exposes `numPoints` (as shown in tests: `simplifiedLine.numPoints`, `simplifiedRing.numPoints`).

- No file path or raster input is passed directly to `numPoints`.
- Preconditions from observed usage:
  - The receiver must be non-null (tests also show cases where simplification can return `null`; calling `numPoints` then would fail).
  - The method is parameterless; point counting is based on the receiver’s current in-memory geometry content.
- Return type differs by definition site (`Int` and `Long` are both documented); use the concrete type from your receiver at compile time.

### Output
Returns `Int` — the count of points in the receiver geometry (an in-memory numeric scalar, not a file/collection output).

### Valid Call Patterns
```scala
assertResult(4)(simplifiedLine.numPoints)
assertResult(3)(simplifiedLine.numPoints)
assertResult(4)(simplifiedRing.numPoints)
```

### LLM Instruction Prompt
- Use instance-call form exactly as verified in tests: `value.numPoints`.
- Do not add arguments (the method takes none).
- Ensure the receiver is not `null` before calling.
- Do not assume a single universal return width; some overload/definitions are `Int`, and authoritative API facts also list `Long`.

### Prompt Snippet
```text
Given a non-null simplified geometry object (e.g., simplifiedLine or simplifiedRing),
call numPoints exactly as `receiver.numPoints` with no arguments, and treat the result
as the total point count for that geometry.
```

### Common Failure Modes
- Calling `numPoints` on `null` (e.g., simplification returned `null` for fully excluded geometry) causes runtime failure.
- Calling as a standalone function (`numPoints`) instead of on an instance (`receiver.numPoints`) does not match verified usage.
- Assuming the wrong numeric type (`Int` vs `Long`) can cause type mismatch in strict typed code.

### Fix Code Hint
```scala
val simplifiedLine = interTile.simplifyGeometry(line)
if (simplifiedLine != null) {
  val n = simplifiedLine.numPoints
  println(n)
}
```

## API Test: `numTiles`

### Signature
```scala
def numTiles: Int
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/RasterMetadata.scala:61_

_Source doc:_ Total number of tiles in the raster layer

### Goal
Return the total number of raster tiles represented by a `RasterMetadata` instance, which is useful for planning distributed raster processing work in RDPro/Beast.

### Parameters
_None._

### Input
Call this on an existing `RasterMetadata` object (as shown in tests: `reader.metadata.numTiles`) after metadata has been successfully initialized/read from a raster source (e.g., HDF via `HDF4Reader.initialize(...)` in the provided test).

File-format support is not defined by `numTiles` itself; it depends on how the metadata object was produced by upstream readers/workflows.

### Output
Returns `Int` — the total tile count in the raster layer as a scalar integer value.

### Valid Call Patterns
```scala
assertResult(1)(reader.metadata.numTiles)
```

### LLM Instruction Prompt
- Use the instance receiver form exactly as grounded: `reader.metadata.numTiles`.
- Do not pass arguments (`numTiles` has no parameters).
- Ensure metadata is initialized before access (e.g., after reader initialization in a valid raster-reading workflow).
- Do not invent overloads or alternative return types; output is `Int`.

### Prompt Snippet
```text
Given an initialized raster reader, read tile-count metadata using the instance property call `reader.metadata.numTiles` (no arguments) and treat the result as `Int`.
```

### Common Failure Modes
- Accessing `numTiles` before reader/metadata initialization, leading to runtime errors from upstream objects.
- Calling it like a method with arguments (e.g., `numTiles(...)`) even though signature is parameterless.
- Assuming `numTiles` reads files by itself; it only reports from already-available metadata.

### Fix Code Hint
```scala
val reader = new HDF4Reader
try {
  reader.initialize(fileSystem, hdfFile.toString, "water_mask", new BeastOptions())
  val totalTiles: Int = reader.metadata.numTiles
  println(totalTiles)
} finally {
  reader.close()
}
```

## API Test: `overlay`

### Signature
```scala
def overlay[V](rasters: RasterRDD[T]*)
def overlay[T: ClassTag, V](@varargs inputs: RDD[ITile[T]]*)
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RaptorMixin.scala:96  (+1 more definition site/overload)_

_Source doc:_ Overlays this raster RDD on top other ones @param rasters the other rasters to stack this raster on @return a new RasterRDD which contains the stack of this raster on top of the given ones

### Goal
Stack this raster with one or more other rasters so each defined pixel carries values from all overlaid inputs (band-like array output per pixel).

### Parameters
- `rasters` (`RasterRDD[T]*`): One or more other raster RDDs to overlay with the receiver raster (`this`), in the given order.

### Input
Caller provides `RasterRDD[T]` inputs (or `RDD[ITile[T]]` for the overload), typically loaded from RDPro-supported raster sources such as GeoTIFF/HDF beforehand.

Preconditions (critical):
- All rasters must be metadata-compatible (same resolution, CRS, and tile size).
- If not compatible, first align them using reshape/reprojection operations (for example `reshapeNN` / other reshape ops per workflow).
- When loading GeoTIFF, use the correct typed loader `sc.geoTiff[T]` that matches the real pixel type.

### Output
Returns `unspecified` — a new overlaid raster RDD representing the stacked inputs; documented usage shows `RasterRDD[Array[Int]]` for `Int` inputs, and tests show `RasterRDD[Array[Short]]` for `Short` tile inputs.

### Valid Call Patterns
```scala
val raster1: RasterRDD[Int] = sc.geoTiff[Int]("glc2000_v1_1.tif")
val raster2: RasterRDD[Int] = sc.geoTiff[Int]("vegetation")
val stacked: RasterRDD[Array[Int]] = raster1.overlay(raster2)
```

```scala
val raster3: RasterRDD[Array[Short]] = RasterOperationsLocal.overlay(raster1, raster2)
```

### LLM Instruction Prompt
- Use the instance call form when working from `RasterRDD` values: `rasterA.overlay(rasterB, ...)`.
- Only pass raster inputs of compatible metadata (resolution/CRS/tile size); otherwise reshape/reproject first.
- Ensure typed raster loading matches true pixel type (e.g., `sc.geoTiff[Int]`, `sc.geoTiff[Float]`, etc.) before calling overlay.
- Do not invent extra parameters; `overlay` takes only varargs raster inputs.

### Prompt Snippet
```text
Given compatible RasterRDDs with matching resolution, CRS, and tile size, call overlay in instance form:
val stacked = raster1.overlay(raster2)
If metadata differs, first reshape/reproject to align them, then overlay.
Use typed loaders that match actual pixel type.
```

### Common Failure Modes
- Metadata mismatch across inputs (different CRS/resolution/tile size) causing invalid overlay semantics or runtime issues.
- Wrong pixel type at load time (`sc.geoTiff[T]` not matching actual raster type), which can break downstream typing.
- Using a non-receiver/bare call shape not shown in project usage.

### Fix Code Hint
```scala
val raster: RasterRDD[Int] = sc.geoTiff[Int]("glc2000_v1_1.tif")
val reshaped = RasterOperationsFocal.reshapeNN(raster,
  RasterMetadata.create(-124, 42, -114, 32, 4326, 1000, 1000, 100, 100))
reshaped.saveAsGeoTiff("glc_ca")
```

## API Test: `parcel`

### Signature
```scala
def parcel(cardinality: Long, dither: Double = 0.2, splitRange: Double = 0.2): JavaSpatialRDD
def parcel(cardinality: Long, dither: Double = 0.2, splitRange: Double = 0.2): SpatialRDD
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/generator/JavaSpatialGeneratorBuilder.scala:153  (+1 more definition site/overload)_

_Source doc:_ Generates boxes from the parcel distribution @param cardinality the number of records to generate @param dither the amount of randomization to add to each generated box @param splitRange the range of splitting each box @return the RDD that contains the generated data

### Goal
Generate a distributed synthetic **box (parcel-like) spatial dataset** as an RDD for Spark-based geospatial workloads.

### Parameters
- `cardinality` (`Long`): the number of records (generated boxes) to produce.
- `dither` (`Double`), default `0.2`: the amount of randomization added to each generated box.
- `splitRange` (`Double`), default `0.2`: the range used when splitting each generated box.

### Input
`parcel` is called on a spatial generator builder receiver (as shown below: `sc.generateSpatialData.parcel(...)`).  
It does **not** take file inputs directly (no GeoTIFF/CSV/Shapefile path parameters in this API).

Preconditions from the available facts:
- Use the instance call form on the generator receiver exactly as documented (`value.parcel(...)`).
- `cardinality` should be a valid requested record count (the API defines it as “number of records to generate”).
- No additional constraints for `dither`/`splitRange` ranges are explicitly documented in the provided sources.

### Output
Returns `JavaSpatialRDD` / `SpatialRDD` (depending on overload): an RDD containing the generated parcel-distribution box geometries.

### Valid Call Patterns
```scala
val parcels: SpatialRDD = sc.generateSpatialData
      .parcel(1000000, dither = 0.1, splitRange = 0.4)

sc.generateSpatialData
  .parcel(100, dither = 0.2, splitRange = 0.3)
  .plotImage(300, 300, "parcel.png")
```

### LLM Instruction Prompt
- Call `parcel` as an instance method on the generator receiver (`sc.generateSpatialData.parcel(...)`), not as a bare function.
- Keep argument order and names consistent with the signature: `cardinality`, `dither`, `splitRange`.
- Do not invent extra parameters, file paths, or return types.
- If Java interop is needed, use the documented `JavaSpatialRDD` overload; otherwise Scala code can use `SpatialRDD`.

### Prompt Snippet
```text
Use RDPro/Beast spatial data generator in Scala with the receiver form:
sc.generateSpatialData.parcel(cardinality, dither = ..., splitRange = ...)
Generate parcel-like boxes as SpatialRDD, without adding any undocumented arguments.
```

### Common Failure Modes
- Calling `parcel(...)` without a receiver (usually will not compile in user code).
- Assuming this API reads external files; it generates synthetic spatial data and accepts only the listed numeric parameters.
- Adding undocumented options (e.g., seed/path/schema args) not present in the signature.

### Fix Code Hint
```scala
val parcels: SpatialRDD = sc.generateSpatialData
  .parcel(1000000L, dither = 0.1, splitRange = 0.4)
```

## API Test: `part`

### Signature
```scala
def part(i: Int): LiteList
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/LiteGeometry.scala:146_

### Goal
Return a geometry part (as a `LiteList`) at a given index from a `LiteGeometry` value.

### Parameters
- `i` (`Int`): Zero-based part index to retrieve from the geometry.

### Input
Call this on a `LiteGeometry` instance (instance-style call inferred from sibling methods like `simplifiedLine.numPoints`).

Preconditions:
- `i` should refer to an existing part index for that geometry.
- This method is geometry-internal; no raster file format input (GeoTIFF/HDF) is involved directly in this call.

### Output
Returns `LiteList` — the selected geometry part at index `i`, represented in Beast’s lightweight internal list structure.

### Valid Call Patterns
```scala
// Inferred from signature and sibling instance-call style (no direct test/readme example for `part`)
val p: LiteList = liteGeometry.part(0)
```

### LLM Instruction Prompt
- Use instance form: `value.part(i)` (not bare `part(i)`).
- Pass an `Int` index only.
- Do not invent overloads or extra parameters.
- If part count/bounds are unknown, validate index before calling.

### Prompt Snippet
```text
Given a LiteGeometry value `g`, get the first part with `g.part(0)`.
Use an Int index, and ensure the index is within available parts.
```

### Common Failure Modes
- Using a non-instance call (e.g., `part(0)`) that will not compile.
- Passing a non-`Int` argument.
- Using an out-of-range index for the geometry’s parts (behavior not documented here; may fail at runtime).

### Fix Code Hint
```scala
// Correct: call on a LiteGeometry instance with Int index
val idx: Int = 0
val part0: LiteList = liteGeometry.part(idx)
```

## API Test: `partitionBy`

### Signature
```scala
def partitionBy(spatialPartitioner: SpatialPartitioner): PartitionedSpatialRDD
def partitionBy(partitionerKlass: Class[_ <: SpatialPartitioner], numPartitions: Int = rdd.getNumPartitions, opts: BeastOptions = new BeastOptions()): PartitionedSpatialRDD
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/indexing/IndexMixin.scala:35  (+1 more definition site/overload)_

### Goal
`partitionBy` repartitions a spatial dataset into spatially organized Spark partitions using a `SpatialPartitioner`, so downstream spatial operations and indexing can run efficiently at scale.

### Parameters
- `spatialPartitioner` (`SpatialPartitioner`): a concrete spatial partitioning strategy instance that defines how features are assigned to partitions.

### Input
A spatial RDD-like dataset (as shown in project usage on shapefile-loaded data) must be the receiver of this call, and you must provide either:

1. a `SpatialPartitioner` instance, or  
2. a partitioner class (`Class[_ <: SpatialPartitioner]`) with optional `numPartitions` and `BeastOptions`.

Grounded call forms shown in docs/tests use vector data loaded through Beast/Spark APIs (e.g., `sparkContext.shapefile(...)`, `sparkContext.readCSVPoint(...)`) and then partitioned (`spatialPartition` sibling in tests; `partitionBy` in README).

Preconditions/compatibility notes from project context:
- Use a partitioner compatible with your workflow (e.g., `RSGrovePartitioner` is the recommended one in project docs).
- If you need **disjoint** behavior, only partitioners that support disjoint partitioning can be used; otherwise Beast reports an error (this rule is documented for indexing partitioners and applies to partitioner capability selection).
- Partitioning quality and partition count affect downstream joins/range queries performance.

### Output
Returns `PartitionedSpatialRDD` — a spatially partitioned RDD with partition metadata/partitioner defined, intended for efficient spatial filtering, joins, and index-oriented workflows.

### Valid Call Patterns
```scala
// Index the datasets
sparkContext.shapefile("ne_10m_admin_1_states_provinces.zip")
    .partitionBy(classOf[RSGrovePartitioner])
    .saveAsIndex("provinces_index", "rtree")
```

```scala
val testFile = makeFileCopy("/test111.points")
val data: SpatialRDD = sparkContext.readCSVPoint(testFile.getPath)
val mbr = data.summary
val gridPartitioner = new GridPartitioner(mbr, Array(2, 2))
val partitionedData = data.spatialPartition(gridPartitioner)
```

### LLM Instruction Prompt
- Call `partitionBy` as an instance method on a spatial dataset receiver (e.g., `sparkContext.shapefile(...).partitionBy(...)`), not as a standalone function.
- Prefer documented class-based usage when matching README examples: `.partitionBy(classOf[RSGrovePartitioner])`.
- If using the instance overload, pass a valid `SpatialPartitioner` object.
- Do not invent extra arguments or overloads beyond the two listed signatures.
- Keep follow-up pipeline steps consistent with partitioned output (e.g., `saveAsIndex`, spatial query/join operations).

### Prompt Snippet
```text
Load a spatial dataset, then call partitionBy on that dataset using either:
- classOf[RSGrovePartitioner], or
- a concrete SpatialPartitioner instance.
Do not call partitionBy as a top-level function.
Use only the documented signatures and then continue with index/query workflow.
```

### Common Failure Modes
- Calling `partitionBy` without a spatial receiver (non-compiling shape).
- Passing a class/instance that is not a `SpatialPartitioner`.
- Assuming unsupported partitioner capabilities (e.g., disjoint mode where not supported).
- Using poor partition count/options for data scale, causing skew or weak spatial-query performance.
- Confusing `partitionBy` with sibling `spatialPartition`; both are partitioning APIs on similar receivers, but use the documented signature you intend.

### Fix Code Hint
```scala
import edu.ucr.cs.bdlab.beast._

// Class-based overload (documented in README)
val partitioned =
  sparkContext.shapefile("ne_10m_admin_1_states_provinces.zip")
    .partitionBy(classOf[RSGrovePartitioner])

// Instance-based overload (signature-authoritative)
val data: SpatialRDD = sparkContext.readCSVPoint("input.points")
val mbr = data.summary
val grid = new GridPartitioner(mbr, Array(2, 2))
val partitioned2 = data.partitionBy(grid)
```

## API Test: `partitionFeatures`

### Signature
```scala
def partitionFeatures(features: SpatialRDD, spatialPartitioner: SpatialPartitioner): PartitionedSpatialRDD
def partitionFeatures(features: JavaSpatialRDD, partitioner: SpatialPartitioner): JavaPairRDD[Integer, IFeature]
def partitionFeatures(features: SpatialRDD, partitionerClass: Class[_ <: SpatialPartitioner], sizeFunction: IFeature=>Int, opts: BeastOptions): PartitionedSpatialRDD
def partitionFeatures(features: JavaSpatialRDD, partitionerClass: Class[_ <: SpatialPartitioner], sizeFunction: org.apache.spark.api.java.function.Function[IFeature, Int], opts: BeastOptions) : JavaPartitionedSpatialRDD
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/indexing/IndexHelper.scala:413  (+3 more definition site/overload)_

### Goal
Partition a spatial feature RDD into spatial partitions using a provided/initialized `SpatialPartitioner` (or partitioner class + options), producing partition-assigned features for scalable spatial indexing and downstream spatial analytics.

### Parameters
- `features` (`SpatialRDD`): The input distributed spatial features (`IFeature`) to be assigned into spatial partitions.
- `partitionerClass` (`Class[_ <: SpatialPartitioner],
                        sizeFunction: IFeature=>Int`): The partitioner implementation to construct (for overloads that build a partitioner) and a per-feature size function used during partitioning.
- `opts` (`BeastOptions`): Partitioner/configuration options used when creating and applying the partitioner.

### Input
- Input is an in-memory Spark spatial RDD (`SpatialRDD` / `JavaSpatialRDD`) of `IFeature`.
- This API itself does **not** read files directly; load data first (e.g., shapefile/GeoJSON/CSV-WKT via Beast loaders), then pass the resulting `SpatialRDD`.
- You must provide either:
  - an already initialized `SpatialPartitioner` (2-arg overload), or
  - a `partitionerClass` + `sizeFunction` + `BeastOptions` (4-arg overload).
- Source doc notes this method is **deprecated** in favor of `partitionFeatures2`.

### Output
Returns `PartitionedSpatialRDD` — an RDD of partition-assigned features (source doc: “an RDD of (partition number, IFeature)”), with partitioning metadata suitable for indexed storage and efficient spatial processing.

### Valid Call Patterns
```scala
val partitionedFeatures =
  IndexHelper.partitionFeatures(features, new GridPartitioner(Summary.computeForFeatures(features), 1))
```

```scala
val partitionedFeatures: JavaPartitionedSpatialRDD =
  IndexHelper.partitionFeatures(JavaRDD.fromRDD(features), classOf[RSGrovePartitioner],
  new org.apache.spark.api.java.function.Function[IFeature, Int]() {
    override def call(v1: IFeature): Int = 1
  } , new BeastOptions())
```

### LLM Instruction Prompt
- Use the exact receiver/qualifier form shown in tested usage: `IndexHelper.partitionFeatures(...)`.
- Do not invent arguments; match one of the documented overloads exactly.
- If using the class-based overload, always provide both `sizeFunction` and `BeastOptions`.
- Prefer migration to `partitionFeatures2` when writing new code, since this API is deprecated.
- Keep Scala and Java call shapes separate (`SpatialRDD` vs `JavaSpatialRDD` overloads).

### Prompt Snippet
```text
Partition this existing SpatialRDD using IndexHelper.partitionFeatures. 
If I already have a SpatialPartitioner instance, call:
IndexHelper.partitionFeatures(features, spatialPartitioner).
If not, call the class-based overload with:
(partitionerClass, sizeFunction, new BeastOptions()).
Do not invent extra parameters, and keep the exact overload argument order.
```

### Common Failure Modes
- Calling with wrong overload shape (e.g., missing `sizeFunction`/`opts` when using `partitionerClass`).
- Passing non-spatial data instead of `SpatialRDD`/`JavaSpatialRDD`.
- Mixing Scala and Java function types for `sizeFunction`.
- Assuming this method reads files directly (it does not).
- Ignoring deprecation (`partitionFeatures2` is the recommended replacement).

### Fix Code Hint
```scala
// Scala SpatialRDD + initialized partitioner
val partitioned: PartitionedSpatialRDD =
  IndexHelper.partitionFeatures(features, new GridPartitioner(Summary.computeForFeatures(features), 1))

// JavaSpatialRDD + class-based overload
val partitionedJava: JavaPartitionedSpatialRDD =
  IndexHelper.partitionFeatures(
    JavaRDD.fromRDD(features),
    classOf[RSGrovePartitioner],
    new org.apache.spark.api.java.function.Function[IFeature, Int]() {
      override def call(v1: IFeature): Int = 1
    },
    new BeastOptions()
  )
```

## API Test: `partitionFeatures2`

### Signature
```scala
def partitionFeatures2(features: SpatialRDD, spatialPartitioner: SpatialPartitioner): SpatialRDD
def partitionFeatures2(features: JavaSpatialRDD, partitioner: SpatialPartitioner): JavaSpatialRDD
def partitionFeatures2(features: SpatialRDD, partitionerClass: Class[_ <: SpatialPartitioner], sizeFunction: IFeature=>Int, opts: BeastOptions): SpatialRDD
def partitionFeatures2(features: JavaSpatialRDD, partitionerClass: Class[_ <: SpatialPartitioner], sizeFunction: org.apache.spark.api.java.function.Function[IFeature, Int], opts: BeastOptions) : JavaSpatialRDD
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/indexing/IndexHelper.scala:429  (+3 more definition site/overload)_

_Source doc:_ Partitions the given features using a partitioner of the given type. This method first initializes the partitioner and then uses this initialized partitioner to partition the data. @param features the set of features to spatially partition @param partitionerClass the type of the spatial partition @param sizeFunction the function used to computed the size @param opts additional options @return the same set of input features after they are partitioned.

### Goal
Spatially repartition a vector `SpatialRDD` using a Beast `SpatialPartitioner` so downstream distributed spatial operations (indexing, joins, queries) run on partitioned data.

### Parameters
- `features` (`SpatialRDD`): The input spatial features (`RDD[IFeature]`) to partition.
- `partitionerClass` (`Class[_ <: SpatialPartitioner],
                        sizeFunction: IFeature=>Int`): In this overload, provide the `SpatialPartitioner` class to initialize, plus a feature-size function used during partitioner initialization.
- `opts` (`BeastOptions`): Additional options used while initializing/configuring partitioning behavior.

### Input
A valid Beast `SpatialRDD` as input (vector features).  
No file path is passed directly to this function; load/create the `SpatialRDD` first (e.g., shapefile/GeoJSON readers or generated features), then call `IndexHelper.partitionFeatures2(...)`.

Preconditions and compatibility notes from project context/tests:
- Use a valid `SpatialPartitioner` (e.g., `GridPartitioner` in tests; `RSGrovePartitioner` is recommended generally in Beast docs).
- If working with replicated/disjoint partitioned data, duplicate handling may be needed in later steps (tests use `IndexHelper.runDuplicateAvoidance(...)`).
- For `-disjoint`-style behavior (context rule), only partitioners that support disjoint partitions can be used.

### Output
Returns `SpatialRDD` — the same logical input features after spatial partitioning is applied, with Spark partitioner metadata set to a `SpatialPartitioner`.

### Valid Call Patterns
```scala
val partitioned1 = IndexHelper.partitionFeatures2(dataset, new GridPartitioner(unitsquare, Array(3, 3)))
val partitioned2 = IndexHelper.partitionFeatures2(partitioned1, new GridPartitioner(unitsquare, Array(5, 5)))
```

```scala
val partitionedFeatures: RDD[IFeature] = IndexHelper.partitionFeatures2(features,
  new GridPartitioner(new EnvelopeNDLite(2, 0.0, 0.0, 4.0, 4.0), Array(2, 2)))
```

### LLM Instruction Prompt
- Use the receiver exactly as `IndexHelper.partitionFeatures2(...)` (verified by tests).
- Prefer the tested overload with an initialized `SpatialPartitioner` instance when possible.
- Pass a `SpatialRDD`/`RDD[IFeature]` as the first argument.
- Do not invent options/arguments not present in the signature.
- If disjoint replication is involved, include a duplicate-avoidance step in downstream logic.

### Prompt Snippet
```text
Given an existing SpatialRDD named `features`, repartition it with Beast using:
`IndexHelper.partitionFeatures2(features, new GridPartitioner(...))`.
Return the partitioned SpatialRDD and preserve this exact call shape.
```

### Common Failure Modes
- Passing a non-spatial RDD instead of `SpatialRDD`/`RDD[IFeature]`.
- Using the wrong overload argument shape (e.g., mixing `partitionerClass` form with instantiated partitioner form).
- Using a partitioner/configuration incompatible with requested disjoint behavior (context rule: unsupported disjoint partitioning errors).
- Assuming repartitioning removes duplicates automatically in replicated scenarios; tests explicitly run duplicate avoidance when needed.

### Fix Code Hint
```scala
val partitioned: RDD[IFeature] =
  IndexHelper.partitionFeatures2(features,
    new GridPartitioner(new EnvelopeNDLite(2, 0.0, 0.0, 4.0, 4.0), Array(2, 2)))

// Optional downstream safety for replicated/disjoint cases:
val deduped = IndexHelper.runDuplicateAvoidance(partitioned)
```

## API Test: `path`

### Signature
```scala
override def path(): String
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/kmlv2/KMLFormat.scala:49  (+2 more definition site/overload)_

### Goal
Return the path string associated with the current Beast/RDPro file-partition/format object instance.

### Parameters
_None._

### Input
Call this on an existing instance that defines `override def path(): String` (for example, objects in Beast I/O internals such as file partitions/formats).  
No arguments are provided.

From the provided test context, a related concrete usage is reading a partition path via:
- `features.partitions(0).asInstanceOf[FilePartition].path`

No additional file-format-specific preconditions are documented for this zero-argument method itself.

### Output
Returns `String` — the path value stored by that object (for example, a filesystem path such as a `.shp` file path in a `FilePartition`).

### Valid Call Patterns
```scala
// Inferred from signature (no direct README/path() example provided)
val p: String = value.path()

// Real test-suite form for this API family (field-style access on FilePartition)
val partitionPath: String = features.partitions(0).asInstanceOf[FilePartition].path
```

### LLM Instruction Prompt
- Call `path` only on an object instance that actually provides this member.
- Use zero arguments exactly: `value.path()`.
- Do not invent parameters or alternate return types.
- If your object is a `FilePartition`, the tested codebase also uses field-style `.path`.

### Prompt Snippet
```text
Given an existing Beast I/O object instance `value` that defines `path`, get its path string with:
`val p: String = value.path()`
Use no arguments, and do not invent overload parameters.
```

### Common Failure Modes
- Calling `path()` on a value whose static type does not define `path`.
- Assuming `path` mutates data; it is a getter-style accessor returning a `String`.
- Confusing method-style `path()` with field-style `path` used by some classes (e.g., `FilePartition` in tests).

### Fix Code Hint
```scala
// Ensure the receiver type supports path
val fp = features.partitions(0).asInstanceOf[FilePartition]
val p: String = fp.path   // tested form in suite

// If using a method-bearing receiver from another implementation:
val p2: String = value.path()
```

## API Test: `pixelLocations`

### Signature
```scala
def pixelLocations: Iterator[(Int, Int)]
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/ITile.scala:81_

_Source doc:_ An iterator that goes over all pixels in this tile @return an iterator that goes over all pixels (whether empty or not) in this tile

### Goal
Iterate through every pixel coordinate in an RDPro tile (`ITile`), including empty/no-data positions, so you can run per-pixel checks or aggregations.

### Parameters
_None._

### Input
You must already have a tile object that exposes `pixelLocations` (for example, `tile` read from a `GeoTiffReader` or from a raster RDD iteration).

From verified test usage:
- `tile` comes from `reader.readTile(tileID)` in GeoTIFF reader tests.
- `tile` can also come from iterating a `RasterFileRDD`/`RDD[ITile[Int]]`.

Preconditions:
- The tile must be successfully read/constructed before calling `tile.pixelLocations`.
- `pixelLocations` itself has no arguments and no file-format argument; file formats (GeoTIFF/HDF) are handled earlier at raster load/read stage.

### Output
Returns `Iterator[(Int, Int)]` — an iterator of pixel index pairs `(x, y)` that covers all pixel positions in the tile, whether defined or empty.

### Valid Call Patterns
```scala
for ((x, y) <- tile.pixelLocations)
  tile.isDefined(x, y)
```

```scala
for ((x,y) <- tile.pixelLocations; if tile.isDefined(x, y))
  numNonEmptyPixels += 1
```

### LLM Instruction Prompt
- Call this as an instance method on a tile value: `tile.pixelLocations`.
- Do not add parameters; signature is parameterless.
- Treat returned tuples as pixel indices `(x, y)`.
- If you need only non-empty pixels, filter with `tile.isDefined(x, y)` during iteration.
- Do not claim it skips empty pixels; source doc explicitly says it includes all pixels.

### Prompt Snippet
```text
Given an ITile value named tile, iterate all pixel coordinates with:
for ((x, y) <- tile.pixelLocations) { ... }
If processing only valid pixels, add:
if tile.isDefined(x, y)
Do not pass arguments to pixelLocations.
```

### Common Failure Modes
- Calling `pixelLocations` as a static/bare function instead of on a tile instance (`tile.pixelLocations`).
- Assuming iterator includes only defined pixels; it includes empty and non-empty pixels.
- Using `x, y` as world coordinates (lon/lat); they are tile pixel indices.
- Calling on an uninitialized or unavailable tile reference (read/load step failed earlier).

### Fix Code Hint
```scala
val tile = reader.readTile(tileID)   // ensure tile exists first
for ((x, y) <- tile.pixelLocations; if tile.isDefined(x, y)) {
  // safe per-pixel logic on defined cells
}
```

## API Test: `pixelType`

### Signature
```scala
def pixelType: DataType
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/ITile.scala:138_

_Source doc:_ Returns the type of the pixel as an SQL data type @return the type of the pixel values

### Goal
Return the Spark SQL `DataType` of pixel values stored in a raster tile, so you can verify pixel schema (for example, `FloatType` vs integer/array types) in RDPro raster workflows.

### Parameters
_None._

### Input
Call this method on an existing tile object (for example, `readRaster.first()` in an `RDD[ITile[T]]` workflow).

Relevant compatibility/type rules from project context:
- `pixelType` is an inspection method; it does not load or convert data itself.
- The raster must already be loaded with the correct typed loader (`sc.geoTiff[T]`) for downstream correctness. Documented mapping includes `IntegerType`, `FloatType`, `ArrayType(IntegerType,true)`, and `ArrayType(FloatType,true)`.

### Output
Returns `DataType` — the Spark SQL data type describing the tile’s pixel values (e.g., `FloatType` in the provided passing test).

### Valid Call Patterns
```scala
val readRaster = new RasterFileRDD(sparkContext, outputFile.getPath, new BeastOptions())
assertResult(FloatType)(readRaster.first().pixelType)
```

### LLM Instruction Prompt
- Call `pixelType` as a zero-argument instance member on a tile object (e.g., `someTile.pixelType`).
- Do not add arguments; signature is exactly `def pixelType: DataType`.
- Use it for type inspection/validation, especially to confirm pixel type assumptions before pixel math or writer configuration.
- If type mismatches are suspected, fix the raster load type (`sc.geoTiff[T]`) upstream rather than trying to pass options to `pixelType`.

### Prompt Snippet
```text
Inspect the raster tile pixel SQL type by calling `tile.pixelType` (no arguments). Compare the returned `DataType` (e.g., FloatType) to the expected type and correct the upstream typed load (`sc.geoTiff[T]`) if mismatched.
```

### Common Failure Modes
- Calling it like a function with parameters (e.g., `pixelType(...)`) — invalid; it takes no parameters.
- Calling it on the wrong receiver (e.g., on an RDD without extracting a tile first).
- Assuming `pixelType` converts types; it only reports type.
- Upstream typed load mismatch (`sc.geoTiff[T]` not matching actual pixel type), leading to incorrect assumptions in later operations.

### Fix Code Hint
```scala
// Get one tile, then inspect its pixel type (no args)
val tile = readRaster.first()
val dt: DataType = tile.pixelType
println(dt)
```

## API Test: `pixels`

### Signature
```scala
def pixels: Iterator[(Int, Int, T)]
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/ITile.scala:84_

### Goal
Iterate over all pixels in an `ITile`, returning each pixel as its tile coordinates plus typed pixel value for downstream raster analysis (e.g., filtering, aggregation, export-ready transformation).

### Parameters
_None._

### Input
- Receiver: an existing tile object (`ITile[T]`) in memory.
- `pixels` itself does **not** load files; raster file formats (GeoTIFF/HDF) are handled earlier by RDPro readers/loaders (for example via `sc.geoTiff[T]` / `sc.hdfFile(...)` workflows).
- Type rule: the tile’s `T` must already match the raster pixel type selected at load time (project rule: typed raster loading must match actual pixel type).
- No additional arguments or options are accepted.

### Output
Returns `Iterator[(Int, Int, T)]` — each element is one pixel as:
1. `Int`: pixel x/index within the tile,
2. `Int`: pixel y/index within the tile,
3. `T`: pixel value (typed to the tile pixel type).

### Valid Call Patterns
```scala
// Inferred from signature/API facts (no direct test or README verbatim call for `pixels`)
val px: Iterator[(Int, Int, T)] = tile.pixels
```

### LLM Instruction Prompt
- Call as an instance member on a tile value: `tile.pixels`.
- Do not add parameters (method has none).
- Preserve generic pixel type `T` from the tile; do not cast unless required by surrounding logic.
- If starting from files, load raster first with correct typed API (`sc.geoTiff[T]`) before reaching tile-level iteration.

### Prompt Snippet
```text
Given an ITile[T] value named `tile`, iterate its pixels using `tile.pixels` (no arguments) and consume the returned Iterator[(Int, Int, T)].
```

### Common Failure Modes
- Calling `pixels(...)` with arguments (signature has none).
- Calling `pixels` without a tile receiver in scope.
- Pixel type mismatch introduced earlier during raster load (e.g., wrong `sc.geoTiff[T]` type), which can break downstream typed logic.
- Assuming `pixels` performs file I/O; it only iterates an already-available tile.

### Fix Code Hint
```scala
// Ensure you already have an ITile[T] named `tile`
val it: Iterator[(Int, Int, T)] = tile.pixels

// Example consumption
it.foreach { case (x, y, v) =>
  // process per-pixel value v at tile coordinate (x, y)
}
```

## API Test: `plot`

### Signature
```scala
override def plot(layer: Canvas, feature: IFeature): Boolean
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/SVGPlotter.scala:62_

### Goal
Draw a single vector `IFeature` onto a visualization `Canvas` and report whether plotting succeeded.

### Parameters
- `layer` (`Canvas`): Target drawing surface (tile/image canvas) that receives the rendered feature.
- `feature` (`IFeature`): Input spatial feature to render (geometry + optional attributes).

### Input
Caller must provide:
- An initialized plotter instance (same style as tested sibling calls on plotter objects).
- A valid `Canvas` instance to draw into.
- A valid `IFeature` instance.

Grounded preconditions:
- No direct test/readme example exists for `plot`; call shape below is inferred from the method signature and sibling instance-method usage (`plotter.setup(...)`, `plotter.getTitle(...)`).
- Project-wide raster compatibility/type-selection rules (`sc.geoTiff[T]`, overlay metadata matching, reshape rules) do **not** directly apply to this vector plotting method.

### Output
Returns `Boolean` — indicates whether the feature was plotted onto the given canvas (`true`/`false` success status; exact failure semantics are not documented here).

### Valid Call Patterns
```scala
// Inferred from signature + sibling instance-method style (not directly shown in tests/readme for plot)
val plotter = new SVGPlotter
plotter.setup(new BeastOptions())
val ok: Boolean = plotter.plot(layer, feature)
```

### LLM Instruction Prompt
- Use instance-method form on a plotter object: `plotter.plot(layer, feature)`.
- Pass arguments in exact order: `(Canvas, IFeature)`.
- Do not invent overloads, extra options, or different return types.
- If `layer`/`feature` construction details are unknown in context, state that explicitly.

### Prompt Snippet
```text
Create and configure a plotter instance, then call:
plotter.plot(layer, feature)
where layer: Canvas and feature: IFeature.
Do not add extra parameters or overloads.
```

### Common Failure Modes
- Calling `plot` as a static/global function instead of on a plotter instance.
- Reversing argument order (`feature, layer`) instead of `(layer, feature)`.
- Passing types other than `Canvas` and `IFeature`.
- Assuming documented behavior beyond boolean success/failure (not specified in provided sources).

### Fix Code Hint
```scala
val plotter = new SVGPlotter
plotter.setup(new BeastOptions())
val plotted: Boolean = plotter.plot(layer, feature)
```

## API Test: `plotAllTiles`

### Signature
```scala
def plotAllTiles(features: SpatialDataTypes.JavaSpatialRDD, minLevel: Int, maxLevel: Int, resolution: Int, buffer: Int, opts: BeastOptions): JavaPairRDD[java.lang.Long, IntermediateVectorTile]
def plotAllTiles(features: SpatialDataTypes.SpatialRDD, levels: Range, resolution: Int, buffer: Int = 0, opts: BeastOptions = new BeastOptions()): RDD[(Long, IntermediateVectorTile)]
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/MVTDataVisualizer.scala:170  (+1 more definition site/overload)_

_Source doc:_ Plots all tiles in a range of Zoom levels according to the provided specifications and configuration @param features   the set of features to visualize @param minLevel   the minimum level to visualize (inclusive) @param maxLevel   the maximum level to visualize (inclusive) @param resolution the resolution of each tile @param buffer     the buffer around each tile to consider when visualizing @param opts       additional options for generating the tiles @return an RDD that contains all the generated tiles along with their IDs.

### Goal
Generate multi-zoom vector tiles (MVT intermediates) from a distributed feature dataset for a given zoom-level range, tile resolution, and rendering options.

### Parameters
- `features` (`SpatialDataTypes.JavaSpatialRDD`): the input distributed spatial features to visualize as tiles.
- `minLevel` (`Int`): minimum zoom level to generate (inclusive).
- `maxLevel` (`Int`): maximum zoom level to generate (inclusive).
- `resolution` (`Int`): tile resolution used when generating each tile (for example, README usage shows `256`).
- `buffer` (`Int`): tile buffer size used when plotting features near tile boundaries.
- `opts` (`BeastOptions`): additional tile-generation options (README examples include `threshold` in options).

### Input
- A Spark spatial RDD of vector features (`SpatialRDD` / `JavaSpatialRDD`), typically loaded from Beast-supported vector inputs (e.g., shapefile via `sparkContext.shapefile(...)`, or indexed input via `sparkContext.spatialFile(...)` in documented usage).
- Zoom levels must be provided either as:
  - `minLevel` + `maxLevel` (Java overload), or
  - `levels: Range` (Scala overload).
- Preconditions/compatibility guidance from project docs:
  - For efficient multilevel visualization workflows, docs indicate using server-backed mode (`beast server`) versus portable mode (`threshold:0`).
  - README examples show using spatial indexing (`RSGrovePartitioner` + `saveAsIndex`) before plotting for scalable visualization pipelines.

### Output
Returns `JavaPairRDD[java.lang.Long, IntermediateVectorTile]` — an RDD of `(tileId, tileData)` pairs where:
- key `Long` is the encoded tile ID,
- value `IntermediateVectorTile` is the generated intermediate MVT tile content for that tile.

### Valid Call Patterns
```scala
val opts: BeastOptions = "threshold" -> 0
val features = sparkContext.shapefile("ne_10m_admin_1_states_provinces.zip")
val tiles = MVTDataVisualizer.plotAllTiles(features, levels=0 to 6, resolution=256, buffer=5, opts)
MVTDataVisualizer.saveTilesCompact(tiles, "provinces_mvt.zip", opts)

// Index the datasets
sparkContext.shapefile("ne_10m_admin_1_states_provinces.zip")
    .partitionBy(classOf[RSGrovePartitioner])
    .saveAsIndex("provinces_index", "rtree")
// Build the multilevel visualization
val tiles = MVTDataVisualizer.plotAllTiles(sparkContext.spatialFile("provinces_index"),
    levels=0 to 19, resolution=256, buffer=5, "threshold" -> "1m")
// Save the tiles
MVTDataVisualizer.saveTilesCompact(tiles, "provinces_mvt.zip", opts)
// Start the server
new BeastServer().run(new BeastOptions(), null, null, sparkContext)
```

### LLM Instruction Prompt
- Call using the real receiver form `MVTDataVisualizer.plotAllTiles(...)` as shown in project examples.
- Do not invent parameters; use only `features`, zoom range (`levels` or `minLevel`/`maxLevel`), `resolution`, `buffer`, and `opts`.
- Keep zoom bounds inclusive semantics (`minLevel` and `maxLevel` are inclusive).
- Use a `SpatialRDD`/`JavaSpatialRDD` input (e.g., from `shapefile` or `spatialFile`), not raster RDDs.
- If generating portable all-tiles output, use options consistent with docs (e.g., `threshold:0`).

### Prompt Snippet
```text
Use MVTDataVisualizer.plotAllTiles with a SpatialRDD of vector features, an inclusive zoom range, tile resolution, buffer, and BeastOptions. Keep the exact call shape from README examples (receiver-qualified call), and do not add undocumented arguments.
```

### Common Failure Modes
- Passing non-spatial input (e.g., raster RDD) instead of `SpatialRDD`/`JavaSpatialRDD`.
- Using an invalid zoom configuration (e.g., reversed bounds when using `minLevel`/`maxLevel`).
- Assuming this API writes files directly; it returns tiles as an RDD and should be followed by a save step (e.g., `saveTilesCompact` in README examples).
- Confusing efficient vs portable visualization modes; docs indicate `threshold:0` for portable all-tiles behavior.

### Fix Code Hint
```scala
val opts: BeastOptions = "threshold" -> 0
val features = sparkContext.shapefile("ne_10m_admin_1_states_provinces.zip")
val tiles = MVTDataVisualizer.plotAllTiles(features, levels = 0 to 6, resolution = 256, buffer = 5, opts)
MVTDataVisualizer.saveTilesCompact(tiles, "provinces_mvt.zip", opts)
```

## API Test: `plotFeatures`

### Signature
```scala
def plotFeatures(features: SpatialDataTypes.SpatialRDD, imageWidth: Int, imageHeight: Int, imagePath: String, plotterClass: Class[_ <: Plotter] = classOf[GeometricPlotter], canvasMBR: EnvelopeNDLite = null, opts: BeastOptions = new BeastOptions()): Unit
def plotFeatures(features: JavaSpatialRDD, minLevel: Int, maxLevel: Int, plotterClass: Class[_ <: Plotter], inputPath: String, outputPath: String, opts: BeastOptions): Unit
def plotFeatures(features: SpatialRDD, levels: Range, plotterClass: Class[_ <: Plotter], inputPath: String, outputPath: String, opts: BeastOptions): Unit
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/SingleLevelPlot.scala:58  (+2 more definition site/overload)_

_Source doc:_ Plots a set of features to a single image. By default, the aspect ratio of the input is maintained and the given dimensions are treated as upper bounds for image width and height, i.e., the produced image might have smaller dimensions. Also, by default, the extents of the canvas will be equal to the input data. This means that the plotted image will occupy the largest portion of the image. If you wish to visualize only a subset of the data or visualize the data on a small portion of the image, you can specify the [[canvasMBR]] parameter. @param features the set of features to plot @param imageWidth the width of the image in pixels @param imageHeight the height of the image in pixels. @param imagePath the path to which the image will be written @param plotterClass the class of the plotter to use for producing the image @param canvasMBR (Optional) the extents of the data (minimum bounding rectangle) @param opts (Optional) additional options to use with the plotter, e.g., colors

### Goal
Render a distributed set of spatial features (vector geometries) into an image output, with controllable image bounds and plot styling options.

### Parameters
- `features` (`SpatialDataTypes.SpatialRDD`): The spatial feature dataset to visualize (distributed spatial RDD).
- `imageWidth` (`Int`): Target image width in pixels (used as an upper bound when aspect ratio is preserved).
- `imageHeight` (`Int`): Target image height in pixels (used as an upper bound when aspect ratio is preserved).
- `imagePath` (`String`): Destination path where the generated image is written.
- `plotterClass` (`Class[_ <: Plotter]`), default `classOf[GeometricPlotter], canvasMBR: EnvelopeNDLite = null,
                   opts: BeastOptions = new BeastOptions()`: Plotter implementation class used to draw features; default is `GeometricPlotter`. The same signature also supports optional `canvasMBR` (canvas extent) and `opts` (plotter options such as colors).

### Input
Caller must provide:
- A valid spatial RDD (`features`) containing geometries/features to draw.
- Positive pixel dimensions (`imageWidth`, `imageHeight`) for the requested image size.
- A writable output path (`imagePath`).
- Optionally:
  - `canvasMBR` to force plotting into a specific extent (useful for subset/zoomed rendering),
  - `opts: BeastOptions` for style/configuration (e.g., color-related options mentioned in source doc),
  - a different `plotterClass` implementing `Plotter`.

Behavioral preconditions from source doc:
- By default, aspect ratio is preserved, so output dimensions may be smaller than requested bounds.
- By default, canvas extent is inferred from input data extent unless `canvasMBR` is supplied.

### Output
Returns `Unit` — the effect is writing an image to `imagePath` (single-image overload) or writing multilevel plot output to `outputPath` (other overloads).

### Valid Call Patterns
```scala
JavaRDD<IFeature> counties = SpatialReader.readInput(sparkContext, new BeastOptions(), "tl_2018_us_county.zip", "shapefile");
MultilevelPlot.plotFeatures(counties, 0, 9, GeometricPlotter.class, 
          null, "counties_multilevel_portable.zip", 
          new BeastOptions().set("stroke", "blue").set("fill", "#9999E6").setLong("threshold", 0));
```

### LLM Instruction Prompt
- Use `plotFeatures` when you need visualization output from vector features.
- Keep receiver/qualifier exactly as in known working/project usage (e.g., `MultilevelPlot.plotFeatures(...)` for the documented overload).
- For single-image usage, follow the provided signature exactly and pass all required arguments.
- Do not invent extra parameters or option keys beyond documented `BeastOptions` usage.
- If you need custom extent, pass `canvasMBR`; otherwise leave it default (`null`) to use data extent.

### Prompt Snippet
```text
Plot this SpatialRDD to an image using plotFeatures with explicit width/height/path, keep aspect-ratio behavior in mind, and only use documented arguments (features, imageWidth, imageHeight, imagePath, optional plotterClass/canvasMBR/opts).
```

### Common Failure Modes
- Passing an invalid/non-spatial RDD instead of `SpatialDataTypes.SpatialRDD`/`SpatialRDD`/`JavaSpatialRDD` required by the chosen overload.
- Assuming exact output pixel size: source doc states width/height are upper bounds when aspect ratio is preserved.
- Forgetting that default canvas extent is input extent; this can hide intended zoom/subset unless `canvasMBR` is set.
- Writing to an unwritable or incorrect output path.
- Mixing overload arguments/order (single-image overload vs multilevel overloads).

### Fix Code Hint
```scala
// Single-image overload (from signature)
SingleLevelPlot.plotFeatures(
  features = featuresRDD,
  imageWidth = 1024,
  imageHeight = 768,
  imagePath = outputImagePath,
  plotterClass = classOf[GeometricPlotter],
  canvasMBR = null,
  opts = new BeastOptions()
)

// Multilevel overload (documented README usage)
MultilevelPlot.plotFeatures(counties, 0, 9, GeometricPlotter.class,
  null, "counties_multilevel_portable.zip",
  new BeastOptions().set("stroke", "blue").set("fill", "#9999E6").setLong("threshold", 0))
```

## API Test: `plotImage`

### Signature
```scala
def plotImage(imageWidth: Int, imageHeight: Int, imagePath: String, plotterClass: Class[_ <: Plotter] = classOf[GeometricPlotter], opts: BeastOptions = new BeastOptions()): Unit
def plotImage(rdd: JavaSpatialRDD, imageWidth: Int, imageHeight: Int, imagePath: String, plotterClass: Class[_ <: Plotter], opts: BeastOptions): Unit
def plotImage(rdd: JavaSpatialRDD, imageWidth: Int, imageHeight: Int, imagePath: String, opts: BeastOptions): Unit
def plotImage(rdd: JavaSpatialRDD, imageWidth: Int, imageHeight: Int, imagePath: String): Unit
```
_Source: beast/beast-spark/src/main/scala/edu/ucr/cs/bdlab/beast/JavaSpatialRDDHelper.scala:239  (+3 more definition site/overload)_

_Source doc:_ Plots the features to an image using the given plotter @param imageWidth the width of the image in pixels @param imageHeight the height of the image in pixels @param imagePath the path to write the generated image @param plotterClass the plotter class @param opts additional user options

### Goal
Render spatial **features** (vector data in a spatial RDD) into a raster image file of a given pixel width/height.

### Parameters
- `rdd` (`JavaSpatialRDD`): the spatial feature dataset to draw (used in Java overloads).
- `imageWidth` (`Int`): output image width in pixels.
- `imageHeight` (`Int`): output image height in pixels.
- `imagePath` (`String`): destination path where the generated image is written.
- `plotterClass` (`Class[_ <: Plotter], opts: BeastOptions`): plotter implementation class used for drawing; additional user options are passed through `BeastOptions`.

### Input
- A spatial feature RDD (Scala call form from README uses receiver syntax, e.g., `buildings.plotImage(...)`; Java overloads pass `rdd` explicitly).
- Pixel dimensions (`imageWidth`, `imageHeight`) must be provided as `Int`.
- An output path string for the image.
- Optional plotting customization via `plotterClass` and `opts`.
- From project docs, this operation is part of visualization workflow that produces PNG for single-image plotting (`splot` / `plotImage`).

### Output
Returns `Unit` — the method writes the rendered image to `imagePath` (side effect), rather than returning an in-memory image object.

### Valid Call Patterns
```scala
val buildings = sc.shapefile("MSBuildings_data_index.zip")
println(buildings.summary)
buildings.saveAsGeoJSON("MSBuildings.geojson")
buildings.plotImage(1000, 1000, "MSBuildings.png")

sc.generateSpatialData
  .makeBoxes(0.1, 0.2)
  .uniform(100)
  .plotImage(300, 300, "uniform.png")
```

### LLM Instruction Prompt
- Use receiver-style invocation exactly as documented (e.g., `value.plotImage(...)`) when working in Scala Beast APIs.
- Keep argument order exactly: `(imageWidth, imageHeight, imagePath[, plotterClass, opts])`.
- Do not invent extra parameters or return values.
- Treat this as a feature-plotting API (vector visualization), not RDPro raster pixel math.
- Ensure the output artifact is an image file path (README examples use `.png`).

### Prompt Snippet
```text
Given a SpatialRDD-like value `features`, call:
features.plotImage(widthPx, heightPx, outputImagePath)

Use Int pixel dimensions and a String output path.
If needed, use the overload with plotterClass and BeastOptions.
Do not change argument order and do not expect a return value.
```

### Common Failure Modes
- Calling it as a bare function (`plotImage(...)`) instead of on a receiver in Scala contexts where extension/helper methods are expected.
- Swapping `imageWidth` and `imageHeight` or passing non-`Int` values.
- Passing an invalid/unwritable `imagePath`, causing write failure.
- Assuming it returns image bytes/data; it returns `Unit` and writes to storage.

### Fix Code Hint
```scala
// Correct receiver-style call and argument order
val features = sc.shapefile("MSBuildings_data_index.zip")
features.plotImage(1000, 1000, "MSBuildings.png")
```

## API Test: `plotPyramid`

### Signature
```scala
def plotPyramid(outPath: String, numLevels: Int, plotterClass: Class[_ <: Plotter] = classOf[GeometricPlotter], opts: BeastOptions = new BeastOptions()): Unit
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/VisualizationMixin.scala:53_

_Source doc:_ Plots the dataset as multilevel tiled image and write the output to the given path. @param outPath the output path to write the image tiles to. @param numLevels the number of levels to create @param plotterClass the plotter class to use for plotting @param opts additional options for the plotter

### Goal
Create a multilevel tiled visualization pyramid from a spatial dataset and write it to an output path for map-style browsing.

### Parameters
- `outPath` (`String`): Output path where generated image pyramid tiles are written (for example, a `.zip` path in documented usage).
- `numLevels` (`Int`): Number of pyramid levels to generate.
- `plotterClass` (`Class[_ <: Plotter]`), default `classOf[GeometricPlotter],
                    opts: BeastOptions = new BeastOptions()`: Plotter implementation class used to render features into tiles.

### Input
A spatial dataset loaded as a Beast spatial RDD (as shown with `sparkContext.spatialFile(...)` or `sparkContext.shapefile(...)`), then calling the instance method `.plotPyramid(...)`.

Documented inputs/formats in examples are shapefile-derived datasets and indexed spatial files.  
`opts` is used for visualization options (examples include `"mercator"`, `"stroke"`, `"threshold"`).  
Compatibility/preconditions from project docs:
- Efficient multilevel visualization is associated with running `beast server`.
- Portable/all-tiles mode is achieved with `threshold:0`.

### Output
Returns `Unit` — the method performs side effects by writing multilevel tiled image output to `outPath` (documented project outputs for this workflow are pyramid zip archives).

### Valid Call Patterns
```scala
// Index the datasets
sparkContext.shapefile("tl_2018_us_county.zip")
  .spatialPartition(classOf[RSGrovePartitioner])
  .writeSpatialFile("counties_index", "rtree")
// Build the multilevel visualization
sparkContext.spatialFile("counties_index")
  .plotPyramid("counties_multilevel.zip", 20,
    opts = Seq("mercator" -> true, "stroke" -> "blue", "threshold" -> "1m"))
// Start the server
new BeastServer().run(new BeastOptions(), null, null, sparkContext)

sparkContext.shapefile("tl_2018_us_county.zip")
  .plotPyramid("counties_multilevel_portable.zip", 10,
    opts = Seq("mercator" -> true, "stroke" -> "blue", "threshold" -> 0))
```

### LLM Instruction Prompt
- Call `plotPyramid` as an instance method on a loaded spatial dataset (`value.plotPyramid(...)`), not as a bare function.
- Keep argument order: `outPath`, `numLevels`, optional `plotterClass`, optional `opts`.
- Use only provided paths/variables; do not invent file paths.
- For portable output, set threshold to `0` in `opts`; for efficient/server-backed usage, use nonzero threshold and run Beast server separately.
- Do not assume undocumented option keys or plotter classes beyond what is shown.

### Prompt Snippet
```text
Given a Beast spatial dataset value, call:
value.plotPyramid(outPath, numLevels, opts = ...)
Use the provided output path and level count exactly.
If portable tiles are required, set ("threshold" -> 0).
If efficient multilevel mode is required, keep threshold nonzero and run BeastServer separately.
```

### Common Failure Modes
- Calling `plotPyramid` without a spatial dataset receiver (won’t match documented call shape).
- Expecting a return value (it returns `Unit`; artifacts are written to disk).
- Misconfiguring visualization mode:
  - expecting portable all-tiles output without `threshold:0`
  - expecting efficient serving behavior without running Beast server.
- Using unprovided/imaginary paths instead of the task’s given `outPath`.

### Fix Code Hint
```scala
val indexed = sparkContext.spatialFile("counties_index")
indexed.plotPyramid(
  "counties_multilevel.zip",
  20,
  opts = Seq("mercator" -> true, "stroke" -> "blue", "threshold" -> "1m")
)

// Portable variant
sparkContext.shapefile("tl_2018_us_county.zip")
  .plotPyramid(
    "counties_multilevel_portable.zip",
    10,
    opts = Seq("mercator" -> true, "stroke" -> "blue", "threshold" -> 0)
  )
```

## API Test: `plotSingleTileParallel`

### Signature
```scala
def plotSingleTileParallel(features: SpatialDataTypes.SpatialRDD, resolution: Int, tileID: Long, buffer: Int = 0, opts: BeastOptions = new BeastOptions()): VectorTile.Tile
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/MVTDataVisualizer.scala:98_

_Source doc:_ Plots the given set of features as a vector tile according to Mapbox specifications using a Spark job. @param features the set of features to plot @param resolution the resolution of the image in pixels @param tileID the ID of the tile to plot @param buffer additional pixels around the tile to plot from all directions (default is zero) @param opts additional options to customize the plotting @return a vector tile that contains all the given features

### Goal
Generate one Mapbox-compatible vector tile from a Spark spatial RDD for a specific tile ID, at a requested pixel resolution, using a Spark job.

### Parameters
- `features` (`SpatialDataTypes.SpatialRDD`): the spatial features to encode into the vector tile (e.g., an `RDD[IFeature]` as used in tests).
- `resolution` (`Int`): tile resolution in pixels.
- `tileID` (`Long`): encoded ID of the target tile to generate.
- `buffer` (`Int`), default `0`: extra pixels around tile boundaries to include from all directions.
- `opts` (`BeastOptions`), default `new BeastOptions()`: additional plotting/customization options.

### Input
- A Spark spatial RDD (`SpatialDataTypes.SpatialRDD`) containing vector features.
- A valid encoded tile identifier (`Long`) for the tile to render (tests use `TileIndex.encode(...)` to produce it).
- Integer resolution and optional buffer.
- Optional `BeastOptions`.

Supported vector input formats in the wider Beast workflow include Shapefile/GeoJSON/CSV-WKT/etc., but this function itself takes an already-loaded `SpatialRDD` (not a file path).

### Output
Returns `VectorTile.Tile` — an in-memory Mapbox Vector Tile object containing plotted features for the requested tile.

### Valid Call Patterns
```scala
val tile = MVTDataVisualizer.plotSingleTileParallel(features, 128, TileIndex.encode(0, 0, 0), 0)
```

```scala
val tile = MVTDataVisualizer.plotSingleTileParallel(features, 100, TileIndex.encode(0, 0, 0), 0)
```

### LLM Instruction Prompt
- Call it with receiver `MVTDataVisualizer` and argument order exactly as in the signature/tests.
- Pass a `SpatialDataTypes.SpatialRDD` (tests show `RDD[IFeature]`) as `features`.
- Provide `tileID` as `Long` (tests use `TileIndex.encode(...)`).
- Use integer `resolution`; keep `buffer` explicit or rely on default.
- Do not invent extra parameters or different return types.

### Prompt Snippet
```text
Use MVTDataVisualizer.plotSingleTileParallel(features, resolution, tileID, buffer[, opts]) to build one Mapbox vector tile from a SpatialRDD. Compute tileID with TileIndex.encode(z, x, y) when needed, keep argument order unchanged, and expect VectorTile.Tile as the return value.
```

### Common Failure Modes
- Passing a non-spatial RDD or wrong feature type instead of `SpatialDataTypes.SpatialRDD`.
- Passing arguments in the wrong order (e.g., swapping `resolution` and `tileID`).
- Supplying a non-`Long` tile ID value.
- Assuming this API reads files directly; it expects already-loaded features.
- Expecting raster output (GeoTIFF/PNG) instead of `VectorTile.Tile`.

### Fix Code Hint
```scala
import edu.ucr.cs.bdlab.beast._
import edu.ucr.cs.bdlab.davinci.MVTDataVisualizer

val tile: VectorTile.Tile =
  MVTDataVisualizer.plotSingleTileParallel(
    features,                  // SpatialDataTypes.SpatialRDD
    128,                       // resolution
    TileIndex.encode(0, 0, 0), // tileID: Long
    0                          // buffer
  )
```

## API Test: `pointSample`

### Signature
```scala
def pointSample(features: SpatialRDD, sampleSize: Int, sampleRatio: Double, seed: Long = System.currentTimeMillis()): Array[Array[Double]]
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/synopses/PointSampler.scala:47_

_Source doc:_ Reads a point sample from the given spatial RDD. It returns a two dimensional array where the first index is the dimension and the second index is the point. This method runs an action on the given RDD. The method takes both a sample size and sample ratio and it returns whichever is smaller. In other words, it tries to read the given sample ratio and if the result is bigger than the sample size, it truncates it to the sample size. This ensures that the final result will fit in memory regardless of the input size. @param features the input features to sample @param sampleSize number of sample points to read @param sampleRatio the ratio of the points to read @return a two-dimensional array of sample points

### Goal
Sample point coordinates from a distributed spatial RDD in Spark, with an explicit cap (`sampleSize`) and ratio (`sampleRatio`) to keep the collected sample memory-bounded.

### Parameters
- `features` (`SpatialRDD`): the input spatial RDD to sample from (point features are the intended input per method purpose and tests).
- `sampleSize` (`Int`): maximum number of sample points to return.
- `sampleRatio` (`Double`): fraction of input points to try sampling before truncation by `sampleSize`.
- `seed` (`Long`), default `System.currentTimeMillis()`: random seed used for sampling reproducibility.

### Input
`pointSample` operates on a Spark `SpatialRDD` already loaded/prepared by your pipeline (no file path is passed directly to this method).  
Preconditions from the provided docs/tests:

- This is an **action** on the RDD (it triggers execution).
- Intended for sampling **points** from spatial features.
- The method uses both `sampleRatio` and `sampleSize`, and returns the smaller effective result.
- Tests show it handles:
  - empty partitions, and
  - rows with null geometries
  without failing.

No additional format/CRS/type-precondition is documented for this specific API.

### Output
Returns `Array[Array[Double]]` — a 2D numeric array of sampled point coordinates where:

- first index = **dimension**
- second index = **point**

So for 2D points, the outer length is expected to be 2 (as validated in tests), and each inner array contains sampled values for that dimension across sampled points.

### Valid Call Patterns
```scala
val sample = PointSampler.pointSample(features, 1, 1.0)
```

```scala
val sample = PointSampler.pointSample(features, 1, 1.0, 12345L)
```

### LLM Instruction Prompt
- Use the tested call form with explicit qualifier: `PointSampler.pointSample(features, sampleSize, sampleRatio[, seed])`.
- Pass an existing `SpatialRDD` variable; do not invent file paths in this call.
- Remember this is an action and returns an in-memory `Array[Array[Double]]`.
- Respect the size/ratio semantics: effective sample count is bounded by the smaller of ratio-based sample and `sampleSize`.
- If deterministic results are needed, provide `seed` explicitly.

### Prompt Snippet
```text
Given a SpatialRDD variable `features`, call:
PointSampler.pointSample(features, sampleSize, sampleRatio, seed)

Use this when you need an in-memory point sample for downstream stats/indexing.
Keep sampleSize conservative to fit driver memory.
```

### Common Failure Modes
- Assuming it is a lazy transformation; it is an **action** and will execute immediately.
- Setting very large `sampleSize` and expecting no driver-memory impact (result is collected as arrays).
- Expecting sampled count to always equal `sampleRatio * N`; method truncates to `sampleSize` when needed.
- Calling with non-reproducible behavior unintentionally (default seed is current time).

### Fix Code Hint
```scala
// Reproducible, bounded sample
val sampleSize = 10000
val sampleRatio = 0.01
val seed = 42L
val sample: Array[Array[Double]] =
  PointSampler.pointSample(features, sampleSize, sampleRatio, seed)
```

## API Test: `printOperationUsage`

### Signature
```scala
def printOperationUsage(operation: Operation, options: BeastOptions, out: PrintStream): Unit
```
_Source: beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/util/OperationHelper.scala:334_

_Source doc:_ Prints the usage of a specific operation. @param operation the operation to print the usage to @param out the print stream to write to

### Goal
Print the usage/help text for one specific Beast operation to a provided output stream (for example, CLI-style usage text written to a `PrintStream`).

### Parameters
- `operation` (`Operation`): The operation whose usage should be printed (in tests, retrieved from `OperationHelper.operations("subtest1")`).
- `options` (`BeastOptions`): Options context passed to the usage printer; test coverage shows `null` is accepted in at least one call path.
- `out` (`PrintStream`): Destination stream to receive the usage text (for example, a `PrintStream` backed by `ByteArrayOutputStream`).

### Input
This function does not consume raster/vector files directly.  
Caller must provide:
1. A valid `Operation` object.
2. A `PrintStream` to write into.
3. A `BeastOptions` instance if available (or `null`, as shown in tests).

No RDPro raster type-parameter selection or raster compatibility preconditions apply to this API directly.

### Output
Returns `Unit` — the effect is side-effect output: usage text is written to `out` (plain text help/usage content for the given operation).

### Valid Call Patterns
```scala
val baos2 = new ByteArrayOutputStream()
val printer2: PrintStream = new PrintStream(baos2)
OperationHelper.printOperationUsage(OperationHelper.operations("subtest1"), null, printer2)
printer2.close()
val str2 = new String(baos2.toByteArray)
assert(str2.contains("sparam2"))
```

### LLM Instruction Prompt
- Call using the tested receiver and argument order: `OperationHelper.printOperationUsage(operation, options, out)`.
- Provide a real `Operation` object (for example from `OperationHelper.operations(...)`).
- Provide a writable `PrintStream`.
- Do not expect a return value; inspect captured stream content if needed.
- Do not invent extra parameters or overloads.

### Prompt Snippet
```text
Use OperationHelper.printOperationUsage(operation, options, out) with exactly three arguments.
Create a PrintStream (optionally backed by ByteArrayOutputStream) to capture the help text.
Pass an existing Operation instance (e.g., OperationHelper.operations("subtest1")).
Treat the method as side-effecting (returns Unit).
```

### Common Failure Modes
- Passing an invalid/missing operation key when fetching from `OperationHelper.operations(...)` before calling.
- Passing a closed or unwritable `PrintStream`, resulting in missing output.
- Expecting a returned string instead of reading from the provided stream.
- Assuming `options` must always be non-null; test usage demonstrates a `null` call path.

### Fix Code Hint
```scala
val baos = new java.io.ByteArrayOutputStream()
val out = new java.io.PrintStream(baos)

val op = OperationHelper.operations("subtest1")
OperationHelper.printOperationUsage(op, null, out)

out.flush()
out.close()
val usageText = new String(baos.toByteArray)
// e.g., assert(usageText.contains("sparam2"))
```

## API Test: `process`

### Signature
```scala
private def process(inputMBR: Rectangle, filePath: String): Option[String]
private def process(filePath: String, pointX: Double, pointY: Double): Option[(String, Int)]
```
_Source: beast/dynoviz/src/main/scala/edu/ucr/cs/bdlab/dynoviz/raptorhunt/GetPointValue.scala:134  (+1 more definition site/overload)_

### Goal
Resolve a point query against a raster-related input at `filePath`, returning an optional result as `(String, Int)` when a value is found.

### Parameters
- `filePath` (`String`): Path to the input dataset/resource to query.
- `pointX` (`Double`): X coordinate of the query point.
- `pointY` (`Double`): Y coordinate of the query point.

### Input
A caller must provide:
- A valid `filePath` string pointing to readable input data.
- Numeric point coordinates (`pointX`, `pointY`) in the coordinate space expected by that input.

Preconditions and compatibility notes:
- This method is `private`, so it is only callable inside its defining scope/class.
- No test-suite call and no README call are provided for this API; call form below is inferred from the signature only.
- The provided project context does not document exact accepted format(s) for this specific method, nor CRS/nodata behavior for this method; these are unknown from the given facts.

### Output
Returns `Option[(String, Int)]` — `Some((..., ...))` when the query succeeds with a `(String, Int)` payload, or `None` when no result is produced.  
The semantic meaning of the `String` and `Int` fields is not documented in the provided sources.

### Valid Call Patterns
```scala
// Inferred from signature only (no test/README verbatim usage available)
value.process(filePath, pointX, pointY)
```

### LLM Instruction Prompt
- Use exactly three arguments in order: `(filePath: String, pointX: Double, pointY: Double)`.
- Preserve an explicit receiver (for example, `value.process(...)`), since no bare-call usage is documented.
- Handle the return as `Option[(String, Int)]` and branch for `None`.
- Do not assume undocumented semantics for tuple fields.

### Prompt Snippet
```text
Call `value.process(filePath, pointX, pointY)` with a valid path string and Double coordinates, then pattern-match on Option[(String, Int)].
```

### Common Failure Modes
- Calling it as a public API from outside its class/object (`private def` visibility).
- Passing arguments in wrong order or wrong types.
- Assuming a result always exists and using `.get` on `None`.
- Assuming undocumented meaning of returned tuple components.

### Fix Code Hint
```scala
value.process(filePath, pointX, pointY) match {
  case Some((s, i)) =>
    // use s and i only after checking Some
    println(s"result=($s,$i)")
  case None =>
    println("No result for this point/path")
}
```

## API Test: `putStoredFile`

### Signature
```scala
def putStoredFile(zip: ZipOutputStream, filename: String, data: Array[Byte]): Unit
def putStoredFile(zip: org.apache.commons.compress.archivers.zip.ZipArchiveOutputStream, filename: String, data: Array[Byte]): Unit
```
_Source: beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/util/ZipUtil.scala:584  (+1 more definition site/overload)_

_Source doc:_ Add a file to the given ZIP file using [[ZipEntry.STORED]] method, i.e., no compression. @param zip the ZIP file to write the entry to @param filename the name of the entry in the ZIP file @param data the binary data of the file

### Goal
Add one binary file entry into an open ZIP stream using the STORED (no-compression) method.

### Parameters
- `zip` (`ZipOutputStream`): An open ZIP output stream to which the new entry will be written.
- `filename` (`String`): The entry name to store inside the ZIP archive (for example, `"README.bin"`).
- `data` (`Array[Byte]`): Raw bytes to write as the entry content.

### Input
You must provide:
- a writable, open ZIP stream (`java.util.zip.ZipOutputStream` for this signature, or the documented overload with `org.apache.commons.compress.archivers.zip.ZipArchiveOutputStream`),
- an entry name as a string,
- and the full entry payload as bytes.

Preconditions from usage:
- Call this while the ZIP stream is still open; close the ZIP after adding entries.
- This API stores entries with `ZipEntry.STORED` (no compression), per source doc.
- No raster/vector type-selection rules are documented for this utility method.

### Output
Returns `Unit` — it does not return a value; its effect is writing a new stored ZIP entry into the provided stream.

### Valid Call Patterns
```scala
val file1 = new File(scratchDir, "test1.zip")
val zip1 = new ZipOutputStream(new FileOutputStream(file1))
ZipUtil.putStoredFile(zip1, "README.bin", Array[Byte](1, 2, 3, 4, 5, 6))
ZipUtil.putStoredFile(zip1, "data.bin", Array[Byte](1, 2, 3))
zip1.close()
```

```scala
val file1 = new Path(scratchPath, "test1.zip")
val zip1 = new ZipOutputStream(fileSystem.create(file1))
ZipUtil.putStoredFile(zip1, "README.bin", Array[Byte](1, 2, 3, 4, 5, 6))
ZipUtil.putStoredFile(zip1, "data.bin", Array[Byte](1, 2, 3))
zip1.close()
```

### LLM Instruction Prompt
- Use the exact receiver form `ZipUtil.putStoredFile(zip, filename, data)` as shown in passing tests.
- Ensure `zip` is an already-created `ZipOutputStream` (or use the documented overload type when applicable).
- Pass `data` as `Array[Byte]` only.
- Keep argument order exactly: `(zip, filename, data)`.
- Close the ZIP stream after writing all entries.

### Prompt Snippet
```text
Given an open ZipOutputStream named zip1, write binary entries with:
ZipUtil.putStoredFile(zip1, "README.bin", Array[Byte](1,2,3,4,5,6))
Then close zip1. Do not change argument order or receiver.
```

### Common Failure Modes
- Passing a closed ZIP stream: write fails at runtime.
- Passing the wrong stream type for this signature (use the overload if using `ZipArchiveOutputStream`).
- Wrong argument order (e.g., filename/data swapped) causing compile errors.
- Using non-byte payload types instead of `Array[Byte]`.

### Fix Code Hint
```scala
val zip = new ZipOutputStream(new FileOutputStream(outputZipPath))
try {
  ZipUtil.putStoredFile(zip, "part-000.bin", bytes0)
  ZipUtil.putStoredFile(zip, "part-001.bin", bytes1)
} finally {
  zip.close()
}
```

## API Test: `rangeQuery`

### Signature
```scala
def rangeQuery(range: Geometry, mbrCount: LongAccumulator = null): SpatialRDD
def rangeQuery(range: Geometry, mbrCount: LongAccumulator = null): PartitionedSpatialRDD
def rangeQuery(rdd: JavaSpatialRDD, range: Geometry): JavaSpatialRDD
def rangeQuery(rdd: JavaSpatialRDD, range: Geometry, mbrCount: LongAccumulator): JavaSpatialRDD
def rangeQuery(partitionedRDD: JavaPartitionedSpatialRDD, range: Geometry): JavaPartitionedSpatialRDD
```
_Source: beast/beast-spark/src/main/scala/edu/ucr/cs/bdlab/beast/JavaSpatialRDDHelper.scala:131  (+4 more definition site/overload)_

_Source doc:_ Performs a range query while counting the number of MBR tests for profiling the performance. @param rdd the RDD that contains the spatial features @param range the query range @param mbrCount (out) an accumulator that counts the number of MBR tests @return a filtered RDD with the features that intersect the given query range

### Goal
Filter a spatial feature RDD to only features that intersect a given query geometry (range), optionally collecting MBR-test counts for profiling.

### Parameters
- `rdd` (`JavaSpatialRDD`): The input spatial RDD to query (Java overloads); it contains spatial features to be filtered by intersection with `range`.
- `range` (`Geometry`): The spatial query window/geometry to search within; features intersecting this geometry are returned.
- `mbrCount` (`LongAccumulator`): Optional Spark accumulator (default `null`) used to count MBR tests for performance profiling.

### Input
A spatial dataset already loaded as a Beast spatial RDD (Scala `SpatialRDD` / `PartitionedSpatialRDD`, or Java `JavaSpatialRDD` / `JavaPartitionedSpatialRDD`) and a JTS `Geometry` query range.

Preconditions and compatibility notes from project context/tests:
- Use the instance call form on an RDD value (e.g., `partitionedData.rangeQuery(...)`), as shown in tested and README usage.
- Range queries are commonly run after spatial partitioning (`spatialPartition(...)`) for efficiency; tests show partition pruning behavior on partitioned inputs.
- The query geometry can be created with JTS geometry factories/envelopes (including `EnvelopeND` / envelope-based geometry).
- Tests demonstrate querying partitioned data with a geometry created under a different CRS setup and still producing results; however, full CRS default/behavior across APIs is not fully documented in the provided context.

### Output
Returns `JavaSpatialRDD` — a filtered spatial RDD containing only features that intersect the input `range` geometry (or the corresponding Scala spatial RDD type for Scala overloads). The output remains an in-memory distributed spatial RDD, not a file format by itself.

### Valid Call Patterns
```scala
partitionedFeatures.rangeQuery(range)

val range = new EnvelopeNDLite(2, -117.337182, 33.622048, -117.241395, 33.72865)
val matchedPolygons: RDD[IFeature] = polygons.rangeQuery(range)
val matchedPoints: RDD[IFeature] = points.rangeQuery(range)

// from tests
val filteredData = partitionedData.rangeQuery(
  new EnvelopeND(new GeometryFactory, 2, -100, 30, -90, 40))
```

### LLM Instruction Prompt
- Call `rangeQuery` as an instance method on an existing spatial RDD value (`value.rangeQuery(...)`), not as a bare function.
- Pass a `Geometry` as `range`; do not invent other parameter types.
- Only pass `mbrCount` when you already have a `LongAccumulator`; otherwise omit it and use default `null`.
- Prefer querying partitioned data (`spatialPartition(...)`) when scalable performance/partition pruning is needed.

### Prompt Snippet
```text
Given a SpatialRDD (or partitioned SpatialRDD) named `data` and a JTS Geometry named `range`,
call:
`val filtered = data.rangeQuery(range)`
Optionally, if profiling MBR tests with an existing LongAccumulator `acc`:
`val filtered = data.rangeQuery(range, acc)`
Do not change argument order.
```

### Common Failure Modes
- Calling `rangeQuery(...)` without an RDD receiver (won’t match the common extension-style usage).
- Passing a non-`Geometry` object as `range`.
- Expecting file output directly; `rangeQuery` returns an RDD, so you must save it separately if needed.
- Skipping partitioning on large datasets and then seeing poor performance (functionally valid, less efficient).

### Fix Code Hint
```scala
// Prepare/query as instance call on a spatial RDD
val data: SpatialRDD = sparkContext.readCSVPoint(inputPath)

// Optional but recommended for scalable query performance
val mbr = data.summary
val gridPartitioner = new GridPartitioner(mbr, Array(2, 2))
val partitionedData = data.spatialPartition(gridPartitioner)

// Geometry range (tested call shape)
val filteredData = partitionedData.rangeQuery(
  new EnvelopeND(new GeometryFactory, 2, -100, 30, -90, 40)
)

// Optional profiling accumulator (only if already created)
// val filteredData2 = partitionedData.rangeQuery(rangeGeometry, mbrCount)
```

## API Test: `raptorJoin`

### Signature
```scala
def raptorJoin(features: SpatialRDD, opts: BeastOptions = new BeastOptions)
def raptorJoin[T](vectors: JavaSpatialRDD, rasters: JavaRasterRDD[T], opts: BeastOptions): JavaRDD[RaptorJoinFeature[T]]
```
_Source: beast/beast-spark/src/main/scala/edu/ucr/cs/bdlab/beast/JavaSpatialRDDHelper.scala:269  (+1 more definition site/overload)_

_Source doc:_ Performs a raster X vector join (Raptor join) between the two given RDDs. @param vectors the set of vector features @param rasters the set of raster tiles @param opts additional options for the algorithm @return the intersection between the feature vectors and all raster pixels.

### Goal
Run a distributed raster–vector overlap join (Raptor) to return all feature/pixel intersections, enabling zonal-style analysis such as per-polygon raster aggregation.

### Parameters
- `vectors` (`JavaSpatialRDD`): the vector features to join against raster pixels (points/lines/polygons are supported by Raptor semantics in project docs).
- `rasters` (`JavaRasterRDD[T]`): the raster tiles to be joined; `T` is the raster pixel value type.
- `opts` (`BeastOptions`): additional algorithm/configuration options for the join.

### Input
Caller must provide:
- A vector RDD (`SpatialRDD` / `JavaSpatialRDD`) and a raster RDD (`RasterRDD` / `JavaRasterRDD[T]`).
- Raster data typically loaded from RDPro-supported formats (GeoTIFF or HDF), and vector data from Beast-supported spatial formats (e.g., Shapefile/GeoJSON), before calling `raptorJoin`.

Preconditions and compatibility rules to enforce:
- **Type compatibility rule:** the join result type parameter `T` should be compatible with the raster pixel type (as stated in the API source doc).
- **Typed raster loading rule:** when loading GeoTIFF, use matching typed load (`sc.geoTiff[Int]`, `sc.geoTiff[Float]`, etc.) so downstream `raptorJoin` type `T` is correct.
- CRS/nodata/default mixed-dataset behavior is **not clearly documented** in the provided sources; do not assume automatic harmonization.

### Output
Returns `JavaRDD[RaptorJoinFeature[T]]` — each record represents an overlap/intersection between an input vector feature and raster pixels, carrying pixel value(s) of type `T` for downstream filtering/aggregation.

### Valid Call Patterns
```scala
val raster: RDD[ITile] = sc.geoTiff("treecover")
val vector: RDD[IFeature] = sc.shapefile("us_states")
val join: RDD[(IFeature, Int, Int, Float)] = raster.raptorJoin[Float](vector)

val join: RDD[RaptorJoinFeature[Float]] = treecover.raptorJoin(countries)
  .filter(v => v.m >= 0 && v.m <= 100.0)
```

### LLM Instruction Prompt
- Use the instance/implicit call form exactly as documented: `raster.raptorJoin[...] (vector)` (or with optional options where available), not a bare `raptorJoin(...)`.
- Ensure generic/result pixel type is compatible with the raster’s real pixel type.
- Prepare inputs first (load raster/vector into RDDs); do not pass file paths directly to `raptorJoin`.
- If CRS or nodata handling is required, state that behavior is undocumented here and must be verified before assuming defaults.

### Prompt Snippet
```text
Given a raster RDD and a vector SpatialRDD, call `value.raptorJoin(...)` in RDPro/Beast style, keeping pixel type `T` compatible with raster pixel type. Return/consume overlap records for filtering or zonal-style aggregation. Do not assume undocumented CRS/nodata auto-handling.
```

### Common Failure Modes
- Pixel type mismatch (e.g., forcing `Float` join type when raster is loaded as integer type).
- Calling shape does not match real API usage (e.g., bare `raptorJoin(...)` instead of `value.raptorJoin(...)`).
- Passing raw paths instead of loaded `SpatialRDD`/`RasterRDD`.
- Assuming undocumented behavior for CRS reconciliation or nodata semantics.

### Fix Code Hint
```scala
import edu.ucr.cs.bdlab.beast._

val treecover = sc.geoTiff[Float]("treecover")
val countries = sc.shapefile("us_states")

val join: RDD[RaptorJoinFeature[Float]] =
  treecover.raptorJoin(countries, new BeastOptions())
    .filter(v => v.m >= 0 && v.m <= 100.0)
```

## API Test: `raptorJoinFeature`

### Signature
```scala
def raptorJoinFeature[T](raster: RasterRDD[T], features: RDD[IFeature], opts: BeastOptions = new BeastOptions(), numTiles: LongAccumulator = null): RDD[RaptorJoinFeature[T]]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RaptorJoin.scala:73_

_Source doc:_ Performs a raptor join between a raster RDD and a set of features. The output contains information about all pixels that match with the set of features. @param raster the raster RDD that contains all the tiles to test @param features the set of features to join with the raster data @param opts additional options for the query processor @param numTiles an optional accumulator to count the number of tiles accesses during the query processing. @tparam T the type of the pixel values @return the set of overlaps between pixels and features

### Goal
Run a distributed raster–vector join that finds all raster pixels overlapping the input features and returns overlap records as `RaptorJoinFeature[T]`.

### Parameters
- `raster` (`RasterRDD[T]`): The raster tiles to be tested in the join (pixel type is `T`).
- `features` (`RDD[IFeature]`): The vector features to join against the raster pixels.
- `opts` (`BeastOptions`), default `new BeastOptions()`: Additional query-processor options.
- `numTiles` (`LongAccumulator`), default `null`: Optional Spark accumulator to count tile accesses during query processing.

### Input
Caller provides:
- A `RasterRDD[T]` (commonly loaded from GeoTIFF or HDF in RDPro workflows).
- An `RDD[IFeature]` (commonly loaded from shapefile/GeoJSON in Beast workflows).

Preconditions and compatibility rules to make calls correct:
- **Typed raster loading rule:** choose `T` to match the real pixel type when creating the raster (e.g., `sc.geoTiff[Int]`, `sc.geoTiff[Float]`, `sc.geoTiff[Array[Int]]`, `sc.geoTiff[Array[Float]]`).
- If you created derived rasters before joining (e.g., overlay/reshape pipeline), ensure upstream raster compatibility constraints are already satisfied (for example, overlay requires same metadata; otherwise reshape first).
- `numTiles` is optional; pass `null` if you do not need tile-access counting.

### Output
Returns `RDD[RaptorJoinFeature[T]]`, i.e., distributed overlap records between raster pixels and input features, with pixel values typed as `T`.  
The exact field schema/details of `RaptorJoinFeature[T]` are not specified in the provided facts beyond containing pixel-feature match information.

### Valid Call Patterns
```scala
val raster: RasterRDD[Int] = sc.geoTiff[Int]("glc2000_v1_1.tif")
val trees = raster.filterPixels(lc => lc >=1 && lc <= 10)
val countries = sc.shapefile("ne_10m_admin_0_countries.zip")
val result = RaptorJoin.raptorJoinFeature(trees, countries, Seq())
  .map(x => x.feature.getAs[String]("NAME")).countByValue().toMap
println(result)
```

### LLM Instruction Prompt
- Use receiver form exactly as documented: `RaptorJoin.raptorJoinFeature(...)`.
- Keep argument order exactly: `(raster, features, opts, numTiles?)`.
- Ensure `raster` is a `RasterRDD[T]` with correctly matched pixel type `T`.
- Ensure `features` is `RDD[IFeature]` (not `(Long, IFeature)`; that shape is for sibling APIs).
- Do not assume undocumented fields of `RaptorJoinFeature[T]`; only use fields shown in available examples.

### Prompt Snippet
```text
Use RaptorJoin.raptorJoinFeature(raster, features, opts, numTiles) to compute raster–vector overlaps.
`raster` must be RasterRDD[T] with correct GeoTIFF/HDF pixel type binding; `features` must be RDD[IFeature].
If no custom options are needed, pass new BeastOptions() (or rely on default where allowed).
If tile-access metrics are needed, pass a LongAccumulator; otherwise use default null.
Treat the result as RDD[RaptorJoinFeature[T]] and only access fields proven in examples.
```

### Common Failure Modes
- Loading raster with wrong generic type (`sc.geoTiff[T]` mismatch), causing type/runtime issues downstream.
- Passing the wrong vector RDD shape (e.g., `RDD[(Long, IFeature)]` from sibling join APIs) instead of `RDD[IFeature]`.
- Using undocumented assumptions about `RaptorJoinFeature[T]` structure.
- Supplying incompatible intermediate rasters from prior steps that violated known preprocessing constraints (e.g., overlay without metadata alignment before reshape).

### Fix Code Hint
```scala
import edu.ucr.cs.bdlab.beast._
import org.apache.spark.util.LongAccumulator

val raster: RasterRDD[Int] = sc.geoTiff[Int]("glc2000_v1_1.tif") // match real pixel type
val features: RDD[IFeature] = sc.shapefile("ne_10m_admin_0_countries.zip")

val tileCounter: LongAccumulator = sc.longAccumulator("tiles_accessed")
val joined: RDD[RaptorJoinFeature[Int]] =
  RaptorJoin.raptorJoinFeature(raster, features, new BeastOptions(), tileCounter)
```

## API Test: `raptorJoinIDFull`

### Signature
```scala
def raptorJoinIDFull[T](raster: RDD[ITile[T]], vector: RDD[(Long, IFeature)], opts: BeastOptions, numTiles: LongAccumulator = null, numRanges: LongAccumulator = null) : RDD[RaptorJoinResult[T]]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RaptorJoin.scala:180_

_Source doc:_ A Raptor join implementation that returns all the matches between features and pixels along with the raster metadata that puts the pixel in context. @param raster the RDD that contains the raster tiles @param vector the RDD that contains the vector features and their unique IDs @param opts additional options for the query processor @tparam T the type of the pixel values @return RDD that contains all overlaps between pixels and geometries

### Goal
Run a full raster-vector Raptor join that returns every overlapping pixel/feature match, including pixel value type `T` and contextual raster metadata.

### Parameters
- `raster` (`RDD[ITile[T]]`): Raster tiles to join (e.g., `RasterFileRDD[T]`), where `T` is the raster pixel type.
- `vector` (`RDD[(Long, IFeature)]`): Vector features paired with unique IDs (`Long`) used in the join.
- `opts` (`BeastOptions`): Additional options for the query processor.
- `numTiles` (`LongAccumulator`), default `null`: Optional accumulator for counting processed tiles.
- `numRanges` (`LongAccumulator`), default `null`: Optional accumulator for counting ranges.

### Input
You must provide:
- A raster as `RDD[ITile[T]]` (RDPro/Beast raster tiles).
- A vector RDD in exactly this shape: `RDD[(Long, IFeature)]` (ID + geometry feature).
- A `BeastOptions` instance.

Documented raster format support in RDPro is GeoTIFF and HDF at load time; this API itself operates on already-loaded RDD tiles.  
Type selection rule still applies upstream when loading GeoTIFF: choose `sc.geoTiff[T]` with `T` matching the real pixel type (e.g., `Int`, `Float`, `Array[Int]`, `Array[Float]`).

### Output
Returns `RDD[RaptorJoinResult[T]]` — all overlaps between vector geometries and raster pixels, including pixel matches and raster context metadata (per source doc).

### Valid Call Patterns
```scala
val values: RDD[RaptorJoinResult[Int]] = RaptorJoin.raptorJoinIDFull(raster, vector, new BeastOptions())
```

```scala
val values: RDD[RaptorJoinResult[Array[Int]]] = RaptorJoin.raptorJoinIDFull(raster, vector, new BeastOptions())
```

### LLM Instruction Prompt
- Use the exact receiver and argument order: `RaptorJoin.raptorJoinIDFull(raster, vector, opts, ...)`.
- Ensure `vector` is `RDD[(Long, IFeature)]`; do not pass plain `RDD[IFeature]`.
- Keep `T` consistent with raster pixel type (including multiband array pixel types).
- Use `new BeastOptions()` if no custom options are required.
- `numTiles` and `numRanges` are optional; omit them unless accumulators are explicitly needed.

### Prompt Snippet
```text
Given a raster RDD[ITile[T]] and vector RDD[(Long, IFeature)], call:
RaptorJoin.raptorJoinIDFull(raster, vector, new BeastOptions())
Keep T matched to raster pixel type (e.g., Int, Float, Array[Int], Array[Float]).
```

### Common Failure Modes
- Passing `vector` without IDs (wrong type): must be `RDD[(Long, IFeature)]`.
- Pixel type mismatch from upstream load (e.g., loading multiband raster as scalar `Int`): choose correct `T`.
- Assuming this returns aggregated zonal stats: it returns full overlap matches, not pre-aggregated summaries.
- Using incompatible/incorrectly prepared raster input type (must be `RDD[ITile[T]]`).

### Fix Code Hint
```scala
// Build vector with explicit IDs
val vector: RDD[(Long, IFeature)] =
  sparkContext.parallelize(Seq((1L, Feature.create(null, testPoly))))

// Keep raster type aligned with actual pixel type
val raster: RasterFileRDD[Array[Int]] =
  new RasterFileRDD[Array[Int]](sparkContext, rasterFile, IRasterReader.OverrideSRID -> 4326)

// Correct call form
val values: RDD[RaptorJoinResult[Array[Int]]] =
  RaptorJoin.raptorJoinIDFull(raster, vector, new BeastOptions())
```

## API Test: `rasterHeight`

### Signature
```scala
def rasterHeight: Int
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/RasterMetadata.scala:52_

_Source doc:_ Total number of rows (scanlines) in the raster layer

### Goal
Get the raster grid height (row count / scanlines) from a raster layer’s metadata so downstream raster processing can reason about grid dimensions.

### Parameters
_None._

### Input
Call this on an existing raster metadata object (e.g., `reader.metadata`) that has already been initialized from a raster source.  
From project context, RDPro raster sources are GeoTIFF and HDF, and metadata becomes available after successful raster reader initialization/loading.

Preconditions:
- The raster reader/metadata must be initialized before access.
- This method reports metadata only; it does not perform reprojection/reshape/alignment. If datasets must match dimensions/CRS/tile layout for other operations (e.g., overlay), prepare them with reshape/reproject operations first.

### Output
Returns `Int` — the total number of raster rows (scanlines) in the raster layer grid.

### Valid Call Patterns
```scala
assert(reader.metadata.rasterHeight == 72)
assert(128 == reader.metadata.rasterHeight)
reader.metadata.gridToModel(reader.metadata.rasterWidth, reader.metadata.rasterHeight, outPoint)
```

### LLM Instruction Prompt
- Use the instance receiver form shown in tests: `reader.metadata.rasterHeight`.
- Do not add arguments (the method is parameterless).
- Ensure metadata exists (reader initialized) before calling.
- Treat return as grid row count (`Int`), not geographic units.

### Prompt Snippet
```text
After initializing GeoTiffReader, read raster row count from metadata using `reader.metadata.rasterHeight` (no arguments). Use it as an Int grid dimension (scanlines), e.g., in assertions or grid/model coordinate transforms.
```

### Common Failure Modes
- Calling before reader initialization, so metadata is unavailable.
- Misinterpreting `rasterHeight` as map-space height instead of pixel-row count.
- Confusing it with tile height; this is full raster grid height.

### Fix Code Hint
```scala
val reader = new GeoTiffReader[Int]
try {
  reader.initialize(fileSystem, rasterPath.toString, "0", new BeastOptions)
  val rows: Int = reader.metadata.rasterHeight
  println(rows)
} finally {
  reader.close()
}
```

## API Test: `rasterWidth`

### Signature
```scala
def rasterWidth: Int
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/RasterMetadata.scala:49_

_Source doc:_ Total number of columns in the raster layer

### Goal
Get the raster layer width (number of pixel columns) from `RasterMetadata` so downstream raster logic (tile lookup, grid/model transforms, bounds checks) uses correct grid dimensions.

### Parameters
_None._

### Input
A `RasterMetadata` instance is required as the receiver (as shown in tests via `reader.metadata.rasterWidth`).

Grounded usage context:
- Metadata is obtained after initializing a raster reader, e.g., GeoTIFF reader in tests.
- RDPro/Beast raster workflows commonly load GeoTIFF/HDF, but `rasterWidth` itself operates on metadata already in memory (not directly on file paths).

Preconditions:
- The reader/metadata object must be initialized/available before access.
- No additional arguments are accepted.

### Output
Returns `Int` — the total number of columns (pixel width in grid space) in the raster layer.

### Valid Call Patterns
```scala
assert(reader.metadata.rasterWidth == 99)
assert(256 == reader.metadata.rasterWidth)
reader.metadata.gridToModel(reader.metadata.rasterWidth, reader.metadata.rasterHeight, outPoint)
```

### LLM Instruction Prompt
- Call `rasterWidth` as a zero-argument member on a `RasterMetadata` receiver.
- Use the verified receiver form `reader.metadata.rasterWidth` when documenting or generating code.
- Do not add parameters (signature is exactly `def rasterWidth: Int`).
- Ensure metadata is initialized first (e.g., after `reader.initialize(...)`).

### Prompt Snippet
```text
Use `rasterWidth` only as `metadata.rasterWidth` (no parentheses/arguments). It returns an Int equal to total raster columns. Require initialized metadata (e.g., `reader.metadata.rasterWidth` after reader initialization).
```

### Common Failure Modes
- Calling `rasterWidth` on the wrong object (e.g., on `reader` instead of `reader.metadata`).
- Treating it like a method with parameters.
- Accessing metadata before reader initialization, so metadata is unavailable/invalid for use.

### Fix Code Hint
```scala
val reader = new GeoTiffReader[Int]
reader.initialize(fileSystem, rasterPath.toString, "0", new BeastOptions)
val width: Int = reader.metadata.rasterWidth
```

## API Test: `rasterizeGeometry`

### Signature
```scala
private[davinci] def rasterizeGeometry(geometry: Geometry): Boolean
private def rasterizeGeometry(geometry: LiteGeometry): Unit
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/VectorCanvas.scala:220  (+1 more definition site/overload)_

_Source doc:_ Plot the given geometry to the blocked pixels @param geometry the geometry to plot. The goemetry should already by in the image space. @return `true` if the pixels changed as a result of this step. Not 100% accurate, through

### Goal
Rasterize a JTS geometry onto a `VectorCanvas` occupancy mask (blocked pixels) in image space, and report whether pixels changed.

### Parameters
- `geometry` (`Geometry`): Geometry to plot onto the canvas blocked-pixel grid; expected to already be in the canvas/image coordinate space.

### Input
Caller provides:
- A `VectorCanvas` receiver instance.
- A JTS `Geometry` argument (including geometry collections, envelopes wrapped as geometry types such as `EnvelopeND` in tests).

Preconditions from source doc/tests:
- The geometry **should already be in image space** before calling.
- This is an internal visualization API (`private[davinci]`), not a public file-loading API; no file format is consumed directly by this method.
- There is an overload for `LiteGeometry`, but call shapes shown in tests use the `Geometry` form on a `VectorCanvas` instance.

### Output
Returns `Boolean` — `true` if blocked/occupied pixels changed as a result of rasterizing this geometry; source doc notes this change signal is “not 100% accurate”.

### Valid Call Patterns
```scala
val canvas = new VectorCanvas(new Envelope(0, 256, 0, 256),
  256, 256, 0, 1)
val factory = GeometryReader.DefaultGeometryFactory
canvas.rasterizeGeometry(factory.createGeometryCollection(Array(factory.createLineString(),
  factory.createPoint(new CoordinateXY(0, 0)))))
```

```scala
val canvas = new VectorCanvas(new Envelope(0, 3, 0, 3),
  3, 3, 0, 2)
val factory = GeometryReader.DefaultGeometryFactory
canvas.rasterizeGeometry(new EnvelopeND(factory, 2, -2, -2, 1, 1))
```

### LLM Instruction Prompt
- Call it as an instance method on `VectorCanvas`: `canvas.rasterizeGeometry(...)`.
- Pass a `Geometry` that is already transformed to image/canvas space.
- Do not invent extra parameters (no CRS arg, no options map, no Spark context).
- Treat the boolean return as a best-effort “pixels changed” flag, not an exact guarantee.
- If working with other geometry representations, convert to supported geometry type before calling.

### Prompt Snippet
```text
Given an existing VectorCanvas named `canvas` and a JTS Geometry already in image space,
call:
`val changed: Boolean = canvas.rasterizeGeometry(geometry)`
Use the Boolean only as an approximate indicator that occupied pixels changed.
Do not add any extra arguments.
```

### Common Failure Modes
- Passing geometries in world CRS/map coordinates instead of image space, causing incorrect rasterization footprint.
- Assuming return value is perfectly accurate for change detection, despite source doc warning.
- Trying to call as a top-level/static function instead of instance call on `VectorCanvas`.
- Attempting to use undocumented extra options/arguments.

### Fix Code Hint
```scala
// Ensure geometry is prepared in image space before rasterization,
// then call as an instance method on VectorCanvas.
val changed: Boolean = canvas.rasterizeGeometry(geometry)
if (changed) {
  // proceed with downstream logic that depends on occupied pixels update
}
```

## API Test: `rasterizePixels`

### Signature
```scala
def rasterizePixels[T: ClassTag](pixels: RDD[(Int, Int, T)], metadata: RasterMetadata, rasterFeature: RasterFeature): RasterRDD[T]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsGlobal.scala:35  (+1 more definition site/overload)_

_Source doc:_ Create a raster from a set of pixel values @param pixels the list of pixel locations and values @param metadata the raster metadata that defines the geography of the pixels @return a raster that contains all the pixels

### Goal
Create a distributed raster (`RasterRDD[T]`) from explicit pixel coordinates and values, using provided raster metadata and feature attributes.

### Parameters
- `pixels` (`RDD[(Int, Int, T)]`): An RDD of pixel records, each as `(x, y, value)` where the first two `Int`s are pixel coordinates and `T` is the pixel value.
- `metadata` (`RasterMetadata`): Raster grid/georeferencing definition used to interpret the pixel coordinates (extent, dimensions, tiling, CRS/SRID, transform).
- `rasterFeature` (`RasterFeature`): Raster-level feature metadata attached to the raster (tests use `RasterFeature.create(Array("fileName"), Array("testFile.tif"))`).

### Input
- In-memory Spark input (not file-based): you must provide an `RDD[(Int, Int, T)]`.
- `metadata` must be prepared before the call and must describe the target raster layout.
- `T` is generic and must be consistent with pixel values in `pixels` (e.g., test usage uses `Float` values and gets float tiles).
- Call form must follow real project usage. Verified test usage calls:
  `RasterOperationsGlobal.rasterizePixels(pixels, metadata, rasterFeature)`.
- README also shows an instance-style `sc.rasterizePixels(pixels, metadata)` call, but that form does not include `rasterFeature` and is a different overload/wrapper shape than the signature listed here.

### Output
Returns `RasterRDD[T]` — a distributed raster containing the provided pixels, organized as raster tiles according to `metadata`, with pixel type `T`.

### Valid Call Patterns
```scala
val metadata = new RasterMetadata(0, 0, 360, 180, 90, 90, 4326,
  new AffineTransform(1, 0, 0, -1, -180, 90))
val pixels = sparkContext.parallelize(Seq(
  (0, 0, 100f),
  (180, 0, 200f),
  (100, 50, 300f),
))
val rasterRDD: RDD[ITile[Float]] =
  RasterOperationsGlobal.rasterizePixels(
    pixels,
    metadata,
    RasterFeature.create(Array("fileName"), Array("testFile.tif"))
  )
```

### LLM Instruction Prompt
- Use the exact 3-argument form from the signature when targeting this API: `(pixels, metadata, rasterFeature)`.
- Keep receiver/qualifier exactly as in verified usage when possible: `RasterOperationsGlobal.rasterizePixels(...)`.
- Ensure `pixels` is an `RDD[(Int, Int, T)]` and `T` matches the actual value type in tuples.
- Do not invent missing arguments or alternative parameter types.
- If using an instance helper like `sc.rasterizePixels(...)`, treat it as a separate call shape and do not assume it has the same parameter list unless explicitly documented.

### Prompt Snippet
```text
Create RasterMetadata first, then build an RDD of (xPixel: Int, yPixel: Int, value: T), and call RasterOperationsGlobal.rasterizePixels(pixels, metadata, rasterFeature). Keep T consistent with pixel values (e.g., Float values => T = Float).
```

### Common Failure Modes
- Passing tuples in the wrong shape/type (anything other than `(Int, Int, T)`).
- Type mismatch between tuple values and `T` (e.g., mixing `Int` and `Float` unexpectedly).
- Omitting `rasterFeature` when calling the 3-argument global method.
- Using a different receiver/call shape than the one available in scope (e.g., calling bare `rasterizePixels(...)` without qualifier/import support).

### Fix Code Hint
```scala
val pixels: RDD[(Int, Int, Float)] = sparkContext.parallelize(Seq(
  (0, 0, 100f),
  (99, 94, 300f)
))

val metadata = new RasterMetadata(0, 0, 100, 95, 30, 30, 4326, new AffineTransform())

val raster: RasterRDD[Float] =
  RasterOperationsGlobal.rasterizePixels(
    pixels,
    metadata,
    RasterFeature.create(Array("fileName"), Array("testFile.tif"))
  )
```

## API Test: `rasterizePoints`

### Signature
```scala
def rasterizePoints[T: ClassTag](points: RDD[(Double, Double, T)], metadata: RasterMetadata, rasterFeature: RasterFeature): RasterRDD[T]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsGlobal.scala:55  (+1 more definition site/overload)_

_Source doc:_ Creates a raster from a list of point locations and values. @param points point locations and raster values @param metadata the metadata that describes the raster location @tparam T the type of raster values @return a raster that contains the given point locations

### Goal
Create a distributed raster (`RasterRDD[T]`) from point coordinates plus per-point values, using provided raster metadata to define the raster’s spatial extent/grid.

### Parameters
- `points` (`RDD[(Double, Double, T)]`): Point records as `(x, y, value)` where `x`/`y` are point coordinates and `value` is the raster value to burn at that location.
- `metadata` (`RasterMetadata`): Raster grid/georeferencing description used to place points into raster cells/tiles.
- `rasterFeature` (`RasterFeature`): Raster feature argument required by this overload; documented behavior/details are not specified in the provided source doc.

### Input
- You must provide an in-memory Spark `RDD[(Double, Double, T)]` of points and values (not a file path argument to this method).
- You must provide a `RasterMetadata` compatible with your intended output raster extent/resolution/tiling.
- Type parameter `T` must match your point value type (e.g., `Int` in the tested usage).
- Verified call form from tests uses:
  - `RasterOperationsGlobal.rasterizePoints(points, metadata, null)`
- Project README also shows an extension-style form:
  - `sc.rasterizePoints(pixels, metadata)`  
  This call shape differs and does not show the `rasterFeature` argument; use the overload actually available in your build.
- If you later combine this raster with others (e.g., overlay/reshape workflows), follow RDPro compatibility rules: metadata (CRS/resolution/tile layout) must be aligned before operations that require matching metadata.

### Output
Returns `RasterRDD[T]` — a distributed raster containing the given point locations with values of type `T`, laid out according to the supplied `RasterMetadata`.

### Valid Call Patterns
```scala
val metadata = RasterMetadata.create(0, 0, 6, 4, 4326, 60, 40, 60, 40)
val pixels = sparkContext.parallelize(Seq(
  (2.20, 1.7, 100),
  (2.7, 2.0, 50),
  (5.3, 2.2, 25),
))
val raster: RasterRDD[Int] = RasterOperationsGlobal.rasterizePoints(pixels, metadata, null)
```

```scala
val metadata = RasterMetadata.create(x1 = -50, y1 = 40, x2 = -60, y2 = 30, srid = 4326,
  rasterWidth = 10, rasterHeight = 10, tileWidth = 10, tileHeight = 10)
val pixels = sc.parallelize(Seq(
  (-51.3, 30.4, 100),
  (-55.2, 34.5, 200),
  (-56.4, 39.2, 300)
))
val raster = sc.rasterizePoints(pixels, metadata)
```

### LLM Instruction Prompt
- Use the exact available overload in the target codebase.
- Prefer the test-verified static call form when unsure: `RasterOperationsGlobal.rasterizePoints(points, metadata, rasterFeature)`.
- Keep tuple order exactly `(Double, Double, T)` = `(x, y, value)`.
- Ensure `T` is consistent between `points` values and the declared/expected `RasterRDD[T]`.
- Do not invent extra arguments, options, or file-based inputs for this method.

### Prompt Snippet
```text
Create an RDD[(Double, Double, T)] of (x, y, value), build RasterMetadata for the target grid, then call RasterOperationsGlobal.rasterizePoints(points, metadata, rasterFeature). Keep tuple order as (x, y, value) and keep T consistent (e.g., Int -> RasterRDD[Int]).
```

### Common Failure Modes
- Calling a non-existent overload for your installed version (README-style 2-arg form vs 3-arg signature form).
- Wrong tuple order in `points` (e.g., `(value, x, y)`), causing incorrect rasterization.
- Type mismatch for `T` (e.g., `RDD[(Double, Double, Int)]` but expecting `RasterRDD[Float]`).
- Supplying metadata that does not represent the intended output raster footprint/grid, leading to misplaced or missing burned points.
- Passing incompatible rasters downstream without metadata alignment (for operations that require same metadata).

### Fix Code Hint
```scala
import edu.ucr.cs.bdlab.beast._
import org.apache.spark.rdd.RDD

val points: RDD[(Double, Double, Int)] = sparkContext.parallelize(Seq(
  (2.20, 1.7, 100),
  (2.7, 2.0, 50),
  (5.3, 2.2, 25)
))

val metadata = RasterMetadata.create(0, 0, 6, 4, 4326, 60, 40, 60, 40)

// Use the signature-backed form when available in your build:
val raster: RasterRDD[Int] = RasterOperationsGlobal.rasterizePoints(points, metadata, null)
```

## API Test: `readCSVPoint`

### Signature
```scala
def readCSVPoint(filename: String, xColumn: Any = 0, yColumn: Any = 1, delimiter: Char = ',', skipHeader: Boolean = false): SpatialRDD
def readCSVPoint(filename: String, xColumn: String, yColumn: String, delimiter: Char, skipHeader: Boolean): JavaSpatialRDD
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/ReadWriteMixin.scala:97  (+1 more definition site/overload)_

_Source doc:_ Reads points from a CSV file given the names of the columns that contain the x and y coordinates @param filename the name of the file or directory that contains the data @param xColumn the name of the column that contains the x coordinate @param yColumn the name of the column that contains the y coordinate @param delimiter the field delimiter, comma by default @param skipHeader whether to skip the header line or not. If either xColumn or yColumn is String, this option will be ignored a header line will be assumed. Otherwise, it is false by default @return the set of records in the file

### Goal
Load point geometries from a CSV-like text file (or directory) into a distributed `SpatialRDD` by specifying which columns contain X/Y coordinates.

### Parameters
- `filename` (`String`): Path to the input file or directory that contains the point records.
- `xColumn` (`Any`), default `0`: Column selector for X coordinates (documented as column name; default positional index is `0`).
- `yColumn` (`Any`), default `1`: Column selector for Y coordinates (documented as column name; default positional index is `1`).
- `delimiter` (`Char`), default `'`: Field separator character between columns (source doc says comma by default in behavior/signature).
- `'`: No standalone meaning is documented; this appears in the provided parameter list artifact, not as a real API argument.
- `skipHeader` (`Boolean`), default `false`: Whether to skip the first line. If either `xColumn` or `yColumn` is a `String`, this flag is ignored and a header is assumed.

### Input
A delimited text dataset containing point coordinates, provided via `filename` as a file or directory.  
From project docs, CSV inputs are supported (including compressed `.gz` / `.bz2` in general CSV support).  
Preconditions:
- The selected `xColumn` and `yColumn` must exist and represent coordinate values.
- If you pass column names (`String`) for `xColumn`/`yColumn`, header handling is automatic (header assumed; `skipHeader` ignored).
- Delimiter must match the actual file layout.

### Output
Returns `SpatialRDD` — the distributed set of parsed spatial records (points) read from the input file(s), ready for Beast spatial operations (e.g., partitioning, range query, joins).

### Valid Call Patterns
```scala
val data: SpatialRDD = sparkContext.readCSVPoint(testFile.getPath)
```

### LLM Instruction Prompt
- Use the receiver form exactly as validated in tests: `sparkContext.readCSVPoint(...)`.
- Do not invent extra parameters; only use `filename`, `xColumn`, `yColumn`, `delimiter`, `skipHeader`.
- When using string column names, do not rely on `skipHeader` to change behavior (it is ignored per source doc).
- Keep return-type expectations consistent: Scala signature returns `SpatialRDD`; documented overload returns `JavaSpatialRDD`.

### Prompt Snippet
```text
Read points from a CSV into Beast using:
sparkContext.readCSVPoint(filename, xColumn, yColumn, delimiter, skipHeader)

Rules:
- filename is required and points to file or directory.
- xColumn/yColumn identify coordinate columns (index defaults 0/1).
- delimiter must match file format.
- If xColumn or yColumn is String, header is assumed and skipHeader is ignored.
- Do not add undocumented arguments.
```

### Common Failure Modes
- Wrong delimiter causes incorrect column parsing.
- `xColumn`/`yColumn` points to missing or non-coordinate columns.
- Expecting `skipHeader=true` to matter while using string column names (it is ignored).
- Calling a different receiver form than the tested one may fail in user code setup (portable form shown is `sparkContext.readCSVPoint(...)`).

### Fix Code Hint
```scala
val data: SpatialRDD =
  sparkContext.readCSVPoint(
    filename = testFile.getPath,
    xColumn = 0,
    yColumn = 1,
    delimiter = ',',
    skipHeader = false
  )
```

## API Test: `readConfigurationXML`

### Signature
```scala
def readConfigurationXML(filename: String): java.util.Map[String, java.util.List[String]]
```
_Source: beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/util/OperationHelper.scala:60_

_Source doc:_ Read all XML configuration files of the given name in the class path and merge them into one object. This method internally caches the configuration so it does not have to be loaded multiple times. The XML is organized in three levels. The first level is the root element and it is always &lt;beast&gt;. The second level is a name of a collection, e.g., &lt;Indexers&gt;. Finally, the third level contains the contents of the collection in their text part. @param filename A path to an XML file that contains the configuration. @return the beast configuration as a map from each key to all values under this key.

### Goal
Load and merge Beast XML configuration entries (from classpath resources with the same name) into a single cached key→list-of-values map.

### Parameters
- `filename` (`String`): Path/name of the XML configuration file to look up in the class path (e.g., `"test-beast.xml"` in the test).

### Input
`readConfigurationXML` expects an XML configuration file name/path that is resolvable from the class path.

Documented XML structure precondition:
1. Root element must be `<beast>`.
2. Second level contains collection names (for example `<Indexers>` or `<Operations>`).
3. Third level elements carry the collection values in their text content.

It reads **all XML configuration files of the given name in the class path** and merges them. It also caches loaded configuration internally.

### Output
Returns `java.util.Map[String, java.util.List[String]]` — a merged Beast configuration where:
- each map key is a second-level collection name (such as `"Operations"` / `"Indexers"`),
- each map value is the list of text values collected under that collection across matching classpath XML files.

### Valid Call Patterns
```scala
val conf: util.Map[String, util.List[String]] = OperationHelper.readConfigurationXML("test-beast.xml")
assert(4 == conf.get("Operations").size)
assert(1 == conf.get("Indexers").size)
assert("Op1" == conf.get("Operations").get(0))
```

### LLM Instruction Prompt
- Use the static receiver exactly as validated in tests: `OperationHelper.readConfigurationXML("...")`.
- Pass exactly one argument of type `String`.
- Provide a classpath-visible XML file name/path.
- Expect a Java map of string keys to Java lists of strings; do not assume Scala collections unless explicitly converted.
- Do not invent additional options, overloads, or schema fields beyond the documented 3-level XML organization.

### Prompt Snippet
```text
Call OperationHelper.readConfigurationXML(filename) with a classpath XML name (String). The XML must use <beast> as root, second-level collection tags (e.g., <Operations>), and third-level text entries. Treat the result as java.util.Map[String, java.util.List[String]].
```

### Common Failure Modes
- File not found on classpath: passing a filename that is not available as a classpath resource.
- Invalid XML layout: root not `<beast>` or unexpected nesting that does not match the documented three-level structure.
- Type mismatch in usage: treating returned Java collections as Scala collections without conversion.
- Expecting re-read side effects immediately after changing XML at runtime: method is documented to cache configuration internally.

### Fix Code Hint
```scala
import java.util
import edu.ucr.cs.bdlab.beast.util.OperationHelper

val conf: util.Map[String, util.List[String]] =
  OperationHelper.readConfigurationXML("test-beast.xml")

val operations: util.List[String] = conf.get("Operations")
if (operations != null) {
  println(s"Operations count = ${operations.size}")
}
```

## API Test: `readFile`

### Signature
```scala
def readFile(filename: String): Array[String]
```
_Source: beast/commontest/src/main/scala/org/apache/spark/test/ScalaSparkTest.scala:170_

_Source doc:_ Read a text file as a single big string. @param filename the name (or path) of the file @return the contents of the file as one big String.

### Goal
Read a text file from a given path/name so test or pipeline code can inspect its textual contents line-by-line (or concatenate all lines into one string).

### Parameters
- `filename` (`String`): the file name or full path to the text file to read.

### Input
`readFile` expects a readable text file path as a `String`.

Preconditions from observed usage:
- The file must already exist (e.g., after a writer has `close()`d).
- The path must be accessible from the current runtime environment.
- This API is used on text outputs (e.g., JSON/KML text written by Beast writers in tests).

### Output
Returns `Array[String]` — the file contents split into lines, where each array element is one line of text.  
In practice (from tests), callers may:
- check line count/content directly, or
- combine all lines with `.mkString("")` to validate full-document text.

### Valid Call Patterns
```scala
val content: Array[String] = readFile(jsonPath.toString)
```

```scala
val content = readFile(kmlPath.toString).mkString("")
```

### LLM Instruction Prompt
- Call shape must be exactly `readFile(pathString)` (as validated by test usage).
- Pass a `String` filename/path only.
- Use this for text files whose contents you want as lines (`Array[String]`).
- If whole-file text is needed, join result lines (e.g., `.mkString("")`).

### Prompt Snippet
```text
After writing and closing the output file, call readFile(outputPath.toString) to read it.
Treat the result as Array[String] (one entry per line), or use .mkString("") for a single string.
```

### Common Failure Modes
- Passing a non-existent path.
- Calling before the writer is closed, so content is incomplete/not flushed.
- Assuming return type is `String` directly (it is `Array[String]`).
- Using non-text/binary files where line-based text checks are not meaningful.

### Fix Code Hint
```scala
// Ensure writer is closed first, then read
writer.close()

val lines: Array[String] = readFile(outputPath.toString)
// If you need one string:
val text: String = lines.mkString("")
```

## API Test: `readInput`

### Signature
```scala
def readInput(sc: JavaSparkContext, opts: BeastOptions, filename: String, iFormat: String): JavaSpatialRDD
def readInput(sc: SparkContext, opts: BeastOptions, filename: String, iFormat: String) : SpatialRDD
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/SpatialReader.scala:205  (+1 more definition site/overload)_

_Source doc:_ Java shortcut

### Goal
Load a spatial input file (for example shapefile or GeoJSON) into a Spark spatial RDD using an explicit input format string.

### Parameters
- `sc` (`JavaSparkContext`): Spark context used to read distributed input data (Java API overload).
- `opts` (`BeastOptions`): Reader options container passed to Beast I/O.
- `filename` (`String`): Path to the input spatial file/dataset to read.
- `iFormat` (`String`): Input format identifier (for example `"shapefile"` or `"geojson"` in provided usage).

### Input
Caller must provide:
- A valid Spark context (`JavaSparkContext` or `SparkContext`, depending on overload).
- A `BeastOptions` instance.
- A path string to accessible input data.
- An explicit format string matching the actual data format.

Documented vector formats in project context include Shapefile and GeoJSON (and others), and real `readInput` examples here use:
- `"shapefile"` for zipped shapefile input
- `"geojson"` for GeoJSON input

Precondition for correctness: `iFormat` must match the actual file format; otherwise parsing can fail or produce incorrect reads.

### Output
Returns `JavaSpatialRDD` — a distributed spatial RDD containing the loaded spatial features, suitable for downstream spatial operations (e.g., spatial join, summary, reprojection workflows shown in tests/examples).

### Valid Call Patterns
```scala
val polygons: RDD[IFeature] = SpatialReader.readInput(sparkContext,new BeastOptions(), vectorFile.getPath, "shapefile")
```

```Scala
JavaRDD<IFeature> polygons = SpatialReader.readInput(sparkContext, new BeastOptions(), "tl_2018_us_state.zip", "shapefile");

// Load points in GeoJSON format.
// Download from https://star.cs.ucr.edu/dynamic/download.cgi/Tweets/data_index.geojson.gz?mbr=-117.8538,33.2563,-116.8142,34.4099
JavaRDD<IFeature> points = SpatialReader.readInput(sparkContext, new BeastOptions(), "Tweets.geojson.gz", "geojson");
```

### LLM Instruction Prompt
- Use the exact receiver form `SpatialReader.readInput(...)`.
- Keep argument order exactly: `(sc, opts, filename, iFormat)`.
- Pass a real format string consistent with the file content (e.g., `"shapefile"` / `"geojson"` from verified examples).
- Do not invent extra parameters; all configuration goes through `BeastOptions`.
- Choose overload by context type (`JavaSparkContext`→`JavaSpatialRDD`, `SparkContext`→`SpatialRDD`).

### Prompt Snippet
```text
Use SpatialReader.readInput(sc, new BeastOptions(), inputPath, inputFormat) with inputFormat matching the actual dataset (e.g., "shapefile" or "geojson"). Keep the 4-argument order exactly and use the overload matching JavaSparkContext vs SparkContext.
```

### Common Failure Modes
- Using a wrong `iFormat` for the file (e.g., passing `"geojson"` for a shapefile zip).
- Passing an invalid/inaccessible `filename` path in the Spark runtime environment.
- Mixing overload/context types (expecting Java return type while calling SparkContext overload, or vice versa).
- Assuming raster loading through this method; in project docs, raster loading is done with RDPro raster APIs (`geoTiff`, `hdfFile`), not this vector reader shortcut.

### Fix Code Hint
```scala
// Scala SparkContext overload
val features: SpatialRDD =
  SpatialReader.readInput(sparkContext, new BeastOptions(), vectorFile.getPath, "shapefile")

// Java-style usage pattern (as documented)
JavaRDD<IFeature> polygons =
  SpatialReader.readInput(sparkContext, new BeastOptions(), "tl_2018_us_state.zip", "shapefile")
```

## API Test: `readLocal`

### Signature
```scala
def readLocal(path: String, iformat: String, opts: BeastOptions, conf: Configuration): Iterator[IFeature]
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/SpatialFileRDD.scala:492_

_Source doc:_ Reads the given path locally without creating any RDDs. Useful for reading a small file when SparkContext is not accessible, e.g., inside a mapPartition function. @param path path to a single file or a directory @param iformat the format of the data @param opts additional options for reading the file @return an iterator to features in the given path

### Goal
Read a small spatial file (or directory of files) as local `IFeature` records without creating an RDD, especially in contexts where `SparkContext` is unavailable.

### Parameters
- `path` (`String`): Path to input data; can be a single file or a directory.
- `iformat` (`String`): Input format string used by Beast to parse the data (for example, the test uses `"wkt(1)"`).
- `opts` (`BeastOptions`): Additional reader options (for example, CSV/WKT reader options such as skipping header or field separator).
- `conf` (`Configuration`): Hadoop `Configuration` used for filesystem access and reader setup.

### Input
A local-readable path to vector/spatial input data plus a matching `iformat` and parsing options.

Known valid pattern from tests:
- Directory input containing multiple files.
- `iformat = "wkt(1)"`.
- Options passed for CSV/WKT parsing (e.g., skip header, tab separator).

Preconditions:
- `iformat` and `opts` must be compatible with the actual file content, otherwise parsing can fail or produce wrong features.
- This API is for local iteration (no RDD creation); use it for small inputs or contexts like inside partition-level logic where creating/accessing Spark RDDs is not desired.

### Output
Returns `Iterator[IFeature]` — an iterator of parsed spatial features from the given file or directory path.

### Valid Call Patterns
```scala
val features = SpatialFileRDD.readLocal(input.getPath, "wkt(1)",
  Seq(CSVFeatureReader.SkipHeader -> true, CSVFeatureReader.FieldSeparator -> '\t'), sparkContext.hadoopConfiguration)
```

### LLM Instruction Prompt
- Use the receiver exactly as `SpatialFileRDD.readLocal(...)` (verified test call form).
- Pass all four arguments in order: `path`, `iformat`, `opts`, `conf`.
- Ensure `iformat` and `opts` match the real input encoding/schema.
- Do not invent overloads or omit `conf`; this API has no listed overloads.

### Prompt Snippet
```text
Use SpatialFileRDD.readLocal(path, iformat, opts, conf) to read a small spatial file/directory locally into Iterator[IFeature] without creating an RDD. Keep argument order exact and make iformat/options consistent with the input encoding (e.g., "wkt(1)" with CSVFeatureReader options).
```

### Common Failure Modes
- Using an `iformat` that does not match the actual input files.
- Missing/misconfigured parser options in `opts` (e.g., wrong delimiter, header handling).
- Passing an invalid or inaccessible `path`.
- Assuming this creates an RDD; it returns a local `Iterator[IFeature]` only.

### Fix Code Hint
```scala
val features: Iterator[IFeature] =
  SpatialFileRDD.readLocal(
    input.getPath,
    "wkt(1)",
    Seq(
      CSVFeatureReader.SkipHeader -> true,
      CSVFeatureReader.FieldSeparator -> '\t'
    ),
    sparkContext.hadoopConfiguration
  )
```

## API Test: `readPartition`

### Signature
```scala
def readPartition(partition: FilePartition, featureReaderClass: Class[_ <: FeatureReader], applyDuplicateAvoidance: Boolean, opts: BeastOptions): Iterator[IFeature]
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/SpatialFileRDD.scala:441_

_Source doc:_ Reads the given partition @param partition the partition to read @param featureReaderClass the class of the feature reader @param opts the user options @return an iterator to the features

### Goal
Read one `FilePartition` of a spatial input file using the selected `FeatureReader` class and return its features as an iterator.

### Parameters
- `partition` (`FilePartition`): A partition object produced for an input path (e.g., from `SpatialFileRDD.createPartitions`) that identifies the specific split/chunk to read.
- `featureReaderClass` (`Class[_ <: FeatureReader],
                    applyDuplicateAvoidance: Boolean, opts: BeastOptions`): The `FeatureReader` implementation class used to parse records in this partition (typically obtained from `SpatialFileRDD.getFeatureReaderClass(...)`).

### Input
Caller must provide:
- A valid `FilePartition` for the target input.
- A compatible `FeatureReader` class for that input format.
- `BeastOptions` containing relevant read options (in tested usage, `SpatialFileRDD.InputFormat -> "geojson"`).

Supported vector input families in Beast context include formats such as GeoJSON, Shapefile, CSV/WKT-style, etc., but this function’s exact behavior depends on the passed `featureReaderClass` and `opts`.

Precondition from real usage:
- Build `featureReaderClass` and `partitions` from the same input path/options combination before calling `readPartition`, so reader/partition stay consistent.

### Output
Returns `Iterator[IFeature]` — an iterator over spatial features decoded from the given partition.

### Valid Call Patterns
```scala
val inputFile = makeFileCopy("/allfeatures.geojson")
val opts: BeastOptions = SpatialFileRDD.InputFormat -> "geojson"
val featureReaderClass = SpatialFileRDD.getFeatureReaderClass(inputFile.getPath, opts)
val partitions = SpatialFileRDD.createPartitions(inputFile.getPath, opts, sparkContext.hadoopConfiguration)

for (partition <- partitions) {
  val features = SpatialFileRDD.readPartition(partition, featureReaderClass, true, opts)
  // consume features
}
```

### LLM Instruction Prompt
- Use the receiver exactly as `SpatialFileRDD.readPartition(partition, featureReaderClass, trueOrFalse, opts)`.
- Derive `featureReaderClass` via `SpatialFileRDD.getFeatureReaderClass(inputPath, opts)`.
- Derive `partition` values via `SpatialFileRDD.createPartitions(inputPath, opts, hadoopConf)`.
- Keep options consistent across `getFeatureReaderClass`, `createPartitions`, and `readPartition`.
- Do not invent extra parameters or overloads.

### Prompt Snippet
```text
Given an input path and BeastOptions, first call SpatialFileRDD.getFeatureReaderClass(path, opts), then SpatialFileRDD.createPartitions(path, opts, sparkContext.hadoopConfiguration). For each partition, call SpatialFileRDD.readPartition(partition, featureReaderClass, true, opts) and consume the returned Iterator[IFeature].
```

### Common Failure Modes
- Passing a `featureReaderClass` that does not match the actual input format/options.
- Building partitions from one path/options set and reading with a different reader/options set.
- Assuming `readPartition` is a standalone bare function call (use `SpatialFileRDD.readPartition(...)` as shown).
- Providing incomplete read options (e.g., missing/incorrect input format hint when auto-detection is not sufficient).

### Fix Code Hint
```scala
val opts: BeastOptions = SpatialFileRDD.InputFormat -> "geojson"
val featureReaderClass = SpatialFileRDD.getFeatureReaderClass(inputPath, opts)
val partitions = SpatialFileRDD.createPartitions(inputPath, opts, sparkContext.hadoopConfiguration)

val allFeatures =
  partitions.iterator.flatMap { p =>
    SpatialFileRDD.readPartition(p, featureReaderClass, true, opts)
  }
```

## API Test: `readTextResource`

### Signature
```scala
def readTextResource(resourcePath: String, maxLines: Int): Array[String]
def readTextResource(resourcePath: String): Array[String]
```
_Source: beast/commontest/src/main/scala/org/apache/spark/test/ScalaSparkTest.scala:153  (+1 more definition site/overload)_

_Source doc:_ Read the first n lines from the given resource and return those lines as an array of Strings. If the given upper bound is bigger than the input file, the entire input file is loaded and returned. Therefore, the returned array might be smaller than the given upper bound if the file is smaller. @param resourcePath the path to the resource to read @param maxLines     the upper bound of the number of lines to read @return an array of strings containing the lines read from the input file

### Goal
Read text lines from a classpath/resource file (optionally capped by a maximum number of lines) and return them as Scala strings.

### Parameters
- `resourcePath` (`String`): Path to the resource to read (as used in project tests, e.g., `"/test.wkt"`).
- `maxLines` (`Int`): Upper bound on number of lines to read.

### Input
A readable text resource identified by `resourcePath`.  
Preconditions from the source doc:
- The function reads lines from a resource text file.
- If `maxLines` is larger than the file length, the function returns all available lines (so result size may be `< maxLines`).

No raster/vector format constraints are documented for this API; it is a general text-resource utility.

### Output
Returns `Array[String]` — the lines read from the resource, in order, up to `maxLines` (or fewer if the resource has fewer lines).

### Valid Call Patterns
```scala
val wkt: String = readTextResource("/test.wkt")(0)
```

### LLM Instruction Prompt
- Use the tested call form exactly when grounding examples: `readTextResource("/...")(0)` is validated by the test suite.
- Pass a valid resource path string.
- Do not assume the returned array has a specific length; check length before indexing unless test data guarantees at least one line.
- If you need explicit line-limit behavior, use the two-argument signature with `maxLines`.

### Prompt Snippet
```text
Read at most N lines from a text resource and return Array[String]. Use readTextResource(resourcePath, maxLines) when you need an explicit cap; otherwise readTextResource(resourcePath). Always handle the case where returned length is smaller than requested.
```

### Common Failure Modes
- Indexing without checking size (e.g., `(0)`) when resource may be empty.
- Passing an incorrect/nonexistent `resourcePath`.
- Assuming the function always returns exactly `maxLines` lines.

### Fix Code Hint
```scala
val lines: Array[String] = readTextResource("/test.wkt", 1)
require(lines.nonEmpty, "Resource is empty or not found: /test.wkt")
val wkt: String = lines(0)
```

## API Test: `readTile`

### Signature
```scala
override def readTile(tileID: Int): ITile[T]
def readTile(tileID: Int): ITile[T]
override def readTile(tileID: Int): ITile[Float]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/GeoTiffReader.scala:167  (+2 more definition site/overload)_

### Goal
Read one raster tile by tile ID from an initialized raster reader (e.g., GeoTIFF reader) for use in pixel access and raster analysis workflows.

### Parameters
- `tileID` (`Int`): The ID of the tile to read (typically obtained from reader metadata, e.g., from pixel or point-to-tile lookup methods).

### Input
A raster reader instance must already be initialized on raster input (project context documents GeoTIFF/HDF support in RDPro; test-backed usage here is `GeoTiffReader`).  
Preconditions from observed usage and API/source doc:
- Call on an initialized reader (`reader.initialize(...)` is done first in tests).
- Provide a valid tile ID for that raster; test usage derives it from metadata (`getTileIDAtPixel`, `getTileIDAtPoint`).
- The interface requires accessors to support multiple concurrent `readTile` calls.
- Returned tile may or may not remain usable after reader close; both behaviors are allowed by the interface, so do not rely on post-close validity unless implementation-specific behavior is known.

### Output
Returns `ITile[T]` — an object containing tile information and pixel values for the requested tile, parameterized by the reader pixel type `T` (or `Float` in the float overload).

### Valid Call Patterns
```scala
val tileID = reader.metadata.getTileIDAtPixel(37, 24)
val tile = reader.readTile(tileID)
```

```scala
val tile1 = reader.readTile(reader.metadata.getTileIDAtPoint(23.224, 32.415))
val tile2 = reader.readTile(reader.metadata.getTileIDAtPoint(33.694, 14.761))
```

### LLM Instruction Prompt
- Use the instance call form exactly: `reader.readTile(tileID)`.
- Derive `tileID` from the same reader’s metadata (e.g., point/pixel lookup) rather than inventing IDs.
- Ensure reader initialization happens before calling `readTile`.
- Keep the reader’s type parameter consistent with raster pixel type (e.g., `GeoTiffReader[Int]`, `GeoTiffReader[Array[Int]]`, `GeoTiffReader[Float]`).
- Do not assume the returned tile is valid after `reader.close()` unless explicitly guaranteed by that implementation.

### Prompt Snippet
```text
Initialize a GeoTiffReader[T], compute tileID from reader.metadata (getTileIDAtPixel or getTileIDAtPoint), then call reader.readTile(tileID). Keep T matched to actual raster pixel type and access tile values before closing the reader.
```

### Common Failure Modes
- Calling `readTile` before initializing the reader.
- Passing a tile ID not belonging to the current raster/metadata.
- Mismatching generic pixel type `T` with actual raster pixel encoding.
- Assuming tile lifetime after `reader.close()` (not guaranteed by interface; implementation-dependent).

### Fix Code Hint
```scala
val reader = new GeoTiffReader[Int]
try {
  reader.initialize(fileSystem, rasterPath.toString, "0", new BeastOptions)
  val tileID = reader.metadata.getTileIDAtPoint(23.224, 32.415)
  val tile = reader.readTile(tileID)
  val v = tile.getPointValue(23.224, 32.415)
} finally {
  reader.close()
}
```

## API Test: `readWKTFile`

### Signature
```scala
def readWKTFile(filename: String, wktColumn: Any, delimiter: Char = '\t', skipHeader: Boolean = false): SpatialRDD
def readWKTFile(filename: String, wktColumn: String, delimiter: Char, skipHeader: Boolean): JavaSpatialRDD
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/ReadWriteMixin.scala:118  (+1 more definition site/overload)_

_Source doc:_ Read a CSV file with WKT-encoded geometry @param filename the name of the file or directory fo the input @param wktColumn the column that includes the WKT-encoded geometry, either an Integer for the index of the attribute or String for its name @param delimiter the field delimiter, tab by default @param skipHeader whether to skip the header line or not, if wktColumn is a string, this has to be true, if wktColumn is an Integer, this is false by default but can be overloaded @return the set of features in the input file

### Goal
Load a text-delimited CSV-like dataset that contains WKT geometry into a distributed `SpatialRDD` for downstream Spark spatial operations (e.g., range query, spatial join, indexing).

### Parameters
- `filename` (`String`): Path to the input file or directory to read.
- `wktColumn` (`Any`): Identifies which column contains WKT geometry; either an integer column index or a string column name.
- `delimiter` (`Char`), default `'\t'`: Field separator used in the input text file (tab by default).
- `skipHeader` (`Boolean`), default `false`: Whether to skip the first line as a header. If `wktColumn` is a string (column name), this must be `true`. If `wktColumn` is an integer index, default is `false` but can be set as needed.

### Input
A CSV/text-delimited input (file or directory) with one column containing WKT-encoded geometry.

Preconditions from the API doc:
- The file must contain valid WKT in the specified column.
- If `wktColumn` is provided as a **column name** (`String`), `skipHeader` must be `true` so the header can be used.
- If `wktColumn` is provided as a **column index** (`Integer`), `skipHeader` defaults to `false` (can be overridden).

### Output
Returns `SpatialRDD` — the distributed set of spatial features parsed from the input rows, with geometry read from the specified WKT column.

### Valid Call Patterns
```scala
val data: RDD[IFeature] = sparkContext.readWKTFile(testFile.getPath, 0)
```

### LLM Instruction Prompt
- Use the receiver form `sparkContext.readWKTFile(...)` as shown in tested code.
- Pass a real input path as `filename`.
- Set `wktColumn` to either:
  - integer index (e.g., `0`), or
  - string column name (and then set `skipHeader = true`).
- Keep `delimiter` aligned with the actual file format (default is tab).
- Do not invent extra parameters or alternate signatures.

### Prompt Snippet
```text
Read a WKT text file into Spark using:
sparkContext.readWKTFile(filename, wktColumn, delimiter, skipHeader)

Rules:
- wktColumn can be Int index or String column name.
- If wktColumn is String, skipHeader must be true.
- delimiter defaults to '\t' unless the file uses another separator.
```

### Common Failure Modes
- Using a string `wktColumn` with `skipHeader = false`, which violates documented behavior.
- Wrong `delimiter` for the actual file, causing incorrect column parsing.
- Pointing `wktColumn` to a non-WKT field, causing geometry parse issues.
- Supplying an invalid/nonexistent `filename`.

### Fix Code Hint
```scala
// Index-based WKT column (tested form)
val data: RDD[IFeature] = sparkContext.readWKTFile(inputPath, 0)

// Name-based WKT column requires header skipping
val dataByName: SpatialRDD = sparkContext.readWKTFile(inputPath, "wkt", ',', true)
```

## API Test: `reproject`

### Signature
```scala
def reproject(targetSRID: Int)
def reproject(targetCRS: CoordinateReferenceSystem, unifiedRaster: Boolean = false, interpolationMethod: InterpolationMethod.InterpolationMethod = InterpolationMethod.NearestNeighbor)
def reproject[T: ClassTag](raster: RasterRDD[T], targetCRS: CoordinateReferenceSystem, unifiedRaster: Boolean = false, interpolationMethod: InterpolationMethod.InterpolationMethod = InterpolationMethod.NearestNeighbor): RasterRDD[T]
def reproject(sourceCRS: CoordinateReferenceSystem, targetCRS: CoordinateReferenceSystem): SpatialRDD
protected def reproject(sourceSRID: Int, targetSRID: Int): SpatialRDD
def reproject(targetCRS: CoordinateReferenceSystem): SpatialRDD
def reproject(targetSRID: Int): SpatialRDD
def reproject(targetCRS: CoordinateReferenceSystem): RasterMetadata
def reproject(metadata: Array[RasterMetadata], targetCRS: CoordinateReferenceSystem): RasterMetadata
def reproject(rdd: JavaSpatialRDD, targetCRS: CoordinateReferenceSystem): JavaSpatialRDD
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsFocal.scala:517  (+9 more definition site/overload)_

_Source doc:_ Reproject a raster to a target coordinate reference system. This method uses the same resolution (number of pixels) of the first tile in the source raster. You can use the other [[reshapeAverage()]] method that takes [[RasterMetadata]] to change all the information. @param raster the raster layer to reproject @param targetCRS the target coordinate reference system @param unifiedRaster if set to true, all output tiles will belong to a single RasterMetadata @param interpolationMethod how to handle a target pixel that overlaps multiple source pixels @tparam T the type of the pixels @return

### Goal
Reproject a `RasterRDD[T]` from its current CRS into a target CRS for distributed raster analytics, while preserving pixel type `T` and using a chosen interpolation rule.

### Parameters
- `raster` (`RasterRDD[T]`): The input raster layer to reproject.
- `targetCRS` (`CoordinateReferenceSystem`): The destination coordinate reference system (for example, via `CRS.decode("EPSG:4326")`).
- `unifiedRaster` (`Boolean`), default `false`: If `true`, output tiles belong to a single `RasterMetadata`; if `false`, they are not forced into one unified metadata.
- `interpolationMethod` (`InterpolationMethod.InterpolationMethod`), default `InterpolationMethod.NearestNeighbor`: How to compute target pixels that overlap multiple source pixels (e.g., nearest-neighbor vs averaging, depending on enum value used).

### Input
- A raster already loaded as `RasterRDD[T]` (commonly from GeoTIFF or HDF in RDPro workflows).
- A valid `CoordinateReferenceSystem` target.
- **Type-selection rule:** when loading with `sc.geoTiff[T]`, `T` must match the actual raster pixel type (documented as critical in project docs).
- Reprojection here keeps the same resolution **as the first source tile** (per source doc).  
  If you need to change full output grid/metadata intentionally, use reshape APIs (source doc points to `reshapeAverage(...)` with `RasterMetadata`).

### Output
Returns `RasterRDD[T]` — a raster dataset geometrically transformed into `targetCRS`, with pixel values produced according to `interpolationMethod`, retaining pixel type `T`.

### Valid Call Patterns
```scala
val temperature: RasterRDD[Float] = 
  sc.hdfFile("MOD11A1.A2022173.h08v05.006.2022174092443.hdf", "LST_Day_1km")
temperature.reproject(4326)

val temperature: RasterRDD[Float] =
  sc.hdfFile("MOD11A1.A2022173.h08v05.006.2022174092443.hdf", "LST_Day_1km")
val rescaled = temperature.rescale(360, 180, RasterOperationsFocal.InterpolationMethod.Average)
temperature.reproject(CRS.decode("EPSG:4326"), RasterOperationsFocal.InterpolationMethod.Average)
```

### LLM Instruction Prompt
- Use the instance style `value.reproject(...)` as shown.
- Prefer passing a `CoordinateReferenceSystem` (`CRS.decode(...)`) when targeting a CRS object.
- Only use listed parameters: `targetCRS`, optional `unifiedRaster`, optional `interpolationMethod`.
- Keep raster type consistent end-to-end (`RasterRDD[T]` in, `RasterRDD[T]` out).
- Do not invent extra options (nodata overrides, custom output grid, etc. are not in this signature).

### Prompt Snippet
```text
Given a RasterRDD[T] named raster, reproject it with:
raster.reproject(CRS.decode("EPSG:4326"), unifiedRaster = false, interpolationMethod = InterpolationMethod.NearestNeighbor)
Use only this API shape and preserve type T.
```

### Common Failure Modes
- Loading raster with wrong `T` (e.g., `sc.geoTiff[Int]` for float pixels), causing downstream type/runtime issues.
- Using the wrong overload family (vector/`SpatialRDD` reproject) instead of raster `RasterRDD[T]` flow.
- Expecting this call to redefine arbitrary output grid/metadata; by doc it uses resolution based on the first source tile.
- Choosing interpolation inconsistent with data semantics (e.g., nearest-neighbor is usually preferred for categorical rasters; averaging is for continuous rasters per reshape guidance).

### Fix Code Hint
```scala
import edu.ucr.cs.bdlab.beast._
import org.geotools.referencing.CRS

val raster: RasterRDD[Float] =
  sc.hdfFile("MOD11A1.A2022173.h08v05.006.2022174092443.hdf", "LST_Day_1km")

val reprojected: RasterRDD[Float] =
  raster.reproject(
    CRS.decode("EPSG:4326"),
    unifiedRaster = false,
    interpolationMethod = RasterOperationsFocal.InterpolationMethod.NearestNeighbor
  )
```

## API Test: `reprojectEnvelope`

### Signature
```scala
def reprojectEnvelope(envelope: Envelope, sourceSRID: Int, targetSRID: Int): Envelope
def reprojectEnvelope(envelope: Envelope, sourceCRS: CoordinateReferenceSystem, targetCRS: CoordinateReferenceSystem): Envelope
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/Reprojector.scala:427  (+1 more definition site/overload)_

_Source doc:_ Reprojects an envelope from one SRID to another SRID @param envelope the envelope to reproject with dimensions in source SRID @param sourceSRID the SRID of the given envelope @param targetSRID the desired SRID of the reprojected envelope @return the envelope after being reprojected to target SRID

### Goal
Reproject a bounding box (`Envelope`) from one coordinate reference system to another so downstream raster/vector operations use a consistent CRS extent.

### Parameters
- `envelope` (`Envelope`): The input bounding box to transform; its coordinates are interpreted in the source CRS/SRID.
- `sourceSRID` (`Int`): EPSG SRID of the input `envelope`.
- `targetSRID` (`Int`): EPSG SRID to transform the `envelope` into.

### Input
A caller must provide:
- A valid `Envelope` instance.
- A valid source CRS and target CRS, either as:
  - SRIDs (`sourceSRID`, `targetSRID`), or
  - `CoordinateReferenceSystem` objects (overload).

Preconditions:
- The envelope coordinates must actually be in the declared source CRS.
- Source and target CRS/SRID must be resolvable/valid in the runtime CRS libraries.
- No file-format input is required by this function itself (it is an in-memory geometry operation).

### Output
Returns `Envelope` — the input extent transformed into the target CRS coordinate space.

### Valid Call Patterns
```scala
// Inferred from the API signature (no direct reprojectEnvelope call form shown in provided tests/readme)
val out: Envelope = Reprojector.reprojectEnvelope(envelope, sourceSRID, targetSRID)

// Overload with CRS objects
val out2: Envelope = Reprojector.reprojectEnvelope(envelope, sourceCRS, targetCRS)
```

### LLM Instruction Prompt
- Use `Reprojector.reprojectEnvelope(...)` with argument order exactly matching the signature.
- Do not invent extra parameters (e.g., axis-order flags, tolerance, nodata options).
- Prefer the SRID overload when SRIDs are known; use CRS overload when CRS objects are already available.
- Ensure the envelope CRS declaration is correct before reprojection; wrong source CRS yields wrong extents.

### Prompt Snippet
```text
Given an existing Envelope `env` in EPSG:4326, reproject it to EPSG:3857 using:
Reprojector.reprojectEnvelope(env, 4326, 3857)
Return the resulting Envelope.
```

### Common Failure Modes
- Passing coordinates in one CRS while declaring a different `sourceSRID`/`sourceCRS` (produces incorrect bounds).
- Using invalid or unsupported SRID values.
- Mixing up source and target argument order.
- Assuming this function reads/writes raster files; it only transforms an in-memory envelope.

### Fix Code Hint
```scala
// Correct source/target order and explicit SRIDs
val srcSRID = 4326
val dstSRID = 3857
val projected: Envelope = Reprojector.reprojectEnvelope(envelope, srcSRID, dstSRID)
```

## API Test: `reprojectEnvelopeInPlace`

### Signature
```scala
def reprojectEnvelopeInPlace(envelope: Array[Double], sourceSRID: Int, targetSRID: Int): Unit
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/Reprojector.scala:465_

_Source doc:_ Reproject an envelope (orthogonal rectangle) to the target CRS in-place @param envelope the input envelope to convert in the form (x1, y1, x2, y2) @param sourceSRID the source coordinate reference system (CRS) @param targetSRID the target coordinate reference system (CRS) @return the converted envelope

### Goal
Reproject a bounding box (envelope) from one CRS/SRID to another by mutating the same `Array[Double]` in place.

### Parameters
- `envelope` (`Array[Double]`): Input/output envelope in the form `(x1, y1, x2, y2)`; this same array is overwritten with converted coordinates.
- `sourceSRID` (`Int`): SRID of the input envelope coordinates.
- `targetSRID` (`Int`): SRID to convert the envelope into.

### Input
A caller-provided numeric envelope array and two CRS identifiers:
- `envelope` must represent an orthogonal rectangle as four doubles in `(x1, y1, x2, y2)` order.
- `sourceSRID` and `targetSRID` must identify the source and target CRS used for reprojection.

No file format input is used by this method directly (it operates on in-memory coordinates only).

### Output
Returns `Unit` — there is no returned object.  
The converted envelope is written back into the provided `envelope: Array[Double]`.

### Valid Call Patterns
```scala
val envelope = Array(-180.0, 0, 0, 90)
Reprojector.reprojectEnvelopeInPlace(envelope, 4326, 3857)
```

### LLM Instruction Prompt
- Use the receiver and argument order exactly as validated in tests: `Reprojector.reprojectEnvelopeInPlace(envelope, sourceSRID, targetSRID)`.
- Pass an `Array[Double]` with exactly envelope-style coordinates `(x1, y1, x2, y2)`.
- Do not expect a return value; read results from the same mutated array.
- Use valid CRS SRIDs consistent with the input coordinate values.

### Prompt Snippet
```text
Given an envelope as Array[Double](x1, y1, x2, y2), call Reprojector.reprojectEnvelopeInPlace(envelope, sourceSRID, targetSRID). This method returns Unit and updates the same envelope array in place with reprojected coordinates.
```

### Common Failure Modes
- Passing coordinates not in `(x1, y1, x2, y2)` envelope form.
- Treating this API as returning a new envelope (it returns `Unit`).
- Using the wrong SRID pair for the provided coordinate values, causing incorrect extents.
- Passing a non-`Array[Double]` envelope.

### Fix Code Hint
```scala
val envelope: Array[Double] = Array(-180.0, 0.0, 0.0, 90.0) // (x1, y1, x2, y2)
Reprojector.reprojectEnvelopeInPlace(envelope, 4326, 3857)
// Read converted values from `envelope` after the call
println(envelope.mkString(", "))
```

## API Test: `reprojectGeometry`

### Signature
```scala
def reprojectGeometry(geometry: Geometry, sourceCRS: CoordinateReferenceSystem, targetCRS: CoordinateReferenceSystem): Geometry
def reprojectGeometry(geometry: Geometry, targetCRS: CoordinateReferenceSystem): Geometry
def reprojectGeometry(geometry: Geometry, targetSRID: Int): Geometry
def reprojectGeometry(geometry: Geometry, transform: TransformationInfo): Geometry
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/Reprojector.scala:274  (+3 more definition site/overload)_

_Source doc:_ Reprojects the given geometry from source to target CRS. This method ignores the SRID of the geometry and assumes it to be in the source CRS. @param geometry the geometry to transform @param sourceCRS source coordinate reference system @param targetCRS target coordinate reference system @return a new geometry that is transformed

### Goal
Reproject a vector `Geometry` from one CRS to another so it can be spatially aligned with other datasets (e.g., rasters/vectors in RDPro/Beast workflows).

### Parameters
- `geometry` (`Geometry`): The input geometry to transform (e.g., point, linestring, envelope-like geometry types used in Beast/JTS).
- `sourceCRS` (`CoordinateReferenceSystem`): The CRS that the input coordinates are currently in.
- `targetCRS` (`CoordinateReferenceSystem`): The CRS to transform the geometry into.

### Input
Caller must provide:
- A valid in-memory `Geometry` object.
- Valid `CoordinateReferenceSystem` objects for source and target.

Preconditions and compatibility notes:
- The method **ignores geometry SRID** and assumes coordinates are in `sourceCRS` (per source doc).  
- Therefore, `sourceCRS` must match the actual coordinate values of `geometry`; do not rely on `geometry.getSRID`.
- No file-format input is used directly by this function (it operates on geometry objects, not GeoTIFF/CSV/etc.).

### Output
Returns `Geometry` — a **new transformed geometry** in the target CRS coordinate space.

### Valid Call Patterns
```scala
Reprojector.CachedTransformationInfo.clear()
val point: Geometry = new GeometryFactory().createPoint(new Coordinate(1, 1))
point.setSRID(4326)
val transform: Geometry = Reprojector.reprojectGeometry(point, CRS.decode("EPSG:3857", true))

val sourceCRS: CoordinateReferenceSystem = factory.createCoordinateReferenceSystem("EPSG:4326")
val targetCRS: CoordinateReferenceSystem = CRS.decode("EPSG:3857", true)
val jtsPoint = new GeometryFactory().createPoint(new Coordinate(-100, 20))
val out: Geometry = Reprojector.reprojectGeometry(jtsPoint, sourceCRS, targetCRS)
```

### LLM Instruction Prompt
- Use the call form exactly as `Reprojector.reprojectGeometry(...)` (as validated in tests).
- Prefer the 3-argument overload when source CRS is known explicitly.
- Do not assume SRID is used; pass the correct `sourceCRS` for the geometry coordinates.
- Treat result as a new geometry object (do not assume in-place mutation).

### Prompt Snippet
```text
Reproject this JTS/Beast geometry with Reprojector.reprojectGeometry(geometry, sourceCRS, targetCRS). 
Do not rely on geometry SRID for source CRS inference because this API ignores SRID for the 3-arg form.
```

### Common Failure Modes
- Passing the wrong `sourceCRS` (coordinates interpreted incorrectly, wrong location after transform).
- Assuming `geometry.setSRID(...)` is sufficient for the 3-arg overload.
- Assuming the function mutates input geometry; tests show transformed geometry is a different object.

### Fix Code Hint
```scala
val sourceCRS = CRS.decode("EPSG:4326", true)   // match actual input coordinate values
val targetCRS = CRS.decode("EPSG:3857", true)
val transformed = Reprojector.reprojectGeometry(inputGeometry, sourceCRS, targetCRS)
```

## API Test: `reprojectRDD`

### Signature
```scala
def reprojectRDD(sourceRDD: SpatialRDD, targetCRS: CoordinateReferenceSystem): SpatialRDD
def reprojectRDD(sourceRDD: SpatialRDD, targetSRID: Int): SpatialRDD
def reprojectRDD(sourceRDD: SpatialRDD, transform: TransformationInfo): SpatialRDD
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/Reprojector.scala:235  (+2 more definition site/overload)_

_Source doc:_ Reproject the given RDD to the target CRS. The source CRS is retrieved from the first element of the source RDD. @param sourceRDD the RDD to transform @param targetCRS the target Coordinate Reference System @return the transformed RDD

### Goal
Reproject a spatial feature RDD from its current CRS into a target CRS so downstream raster/vector analytics (for example zonal statistics) run in a consistent coordinate system.

### Parameters
- `sourceRDD` (`SpatialRDD`): The input spatial RDD to transform; its source CRS is inferred from the first element.
- `targetCRS` (`CoordinateReferenceSystem`): The destination coordinate reference system to project all geometries into.

### Input
`reprojectRDD` operates on an in-memory `SpatialRDD` (for example, polygons loaded from a shapefile into an `RDD[IFeature]`/`SpatialRDD` pipeline).  
From the source doc, a key precondition is that the input RDD has a valid source CRS retrievable from its first element; this is what the reprojection is based on.

In typical Beast/RDPro workflows, you prepare `sourceRDD` by reading vector input (such as shapefile/GeoJSON) before calling reprojection. If you later combine with raster workflows (join/zonal), align CRS first to avoid mismatches.

### Output
Returns `SpatialRDD` — a transformed spatial RDD containing the same features reprojected into the requested target CRS.

### Valid Call Patterns
```scala
val projectedPolygons: RDD[IFeature] = Reprojector.reprojectRDD(polygons, CRSServer.sridToCRS(3857))
```

### LLM Instruction Prompt
- Use the tested static call form exactly: `Reprojector.reprojectRDD(sourceRDD, targetCRS)`.
- Ensure `sourceRDD` is a `SpatialRDD`.
- Pass a real `CoordinateReferenceSystem` object for this overload (for example via `CRSServer.sridToCRS(...)` as shown).
- Do not invent extra parameters.
- If you need a different overload, use exactly one of the documented alternatives: `(sourceRDD, targetSRID: Int)` or `(sourceRDD, transform: TransformationInfo)`.

### Prompt Snippet
```text
Given a SpatialRDD named polygons, reproject it to EPSG:3857 using the CoordinateReferenceSystem overload:
val projectedPolygons = Reprojector.reprojectRDD(polygons, CRSServer.sridToCRS(3857))
Keep the receiver as Reprojector and do not add extra arguments.
```

### Common Failure Modes
- Calling with a bare `reprojectRDD(...)` instead of the tested receiver `Reprojector.reprojectRDD(...)`.
- Passing the wrong second-argument type for this overload (must be `CoordinateReferenceSystem`).
- Source features missing/invalid CRS metadata; reprojection depends on source CRS retrieved from the first element.
- Running downstream raster-vector analytics without CRS alignment (results can be incorrect or empty due to spatial mismatch).

### Fix Code Hint
```scala
// Correct: explicit receiver + CRS object
val projectedPolygons: RDD[IFeature] =
  Reprojector.reprojectRDD(polygons, CRSServer.sridToCRS(3857))

// Alternative documented overload if you already have SRID as Int:
// val projectedPolygons = Reprojector.reprojectRDD(polygons, 3857)
```

## API Test: `rescale`

### Signature
```scala
def rescale(rasterWidth: Int, rasterHeight: Int, unifiedRaster: Boolean = false, interpolationMethod: InterpolationMethod.InterpolationMethod = InterpolationMethod.NearestNeighbor)
def rescale[T: ClassTag](raster: RasterRDD[T], rasterWidth: Int, rasterHeight: Int, unifiedRaster: Boolean = false, interpolationMethod: InterpolationMethod.InterpolationMethod = InterpolationMethod.NearestNeighbor): RasterRDD[T]
def rescale(newRasterWidth: Int, newRasterHeight: Int): RasterMetadata
def rescale(metadata: Array[RasterMetadata], rasterWidth: Int, rasterHeight: Int): RasterMetadata
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsFocal.scala:542  (+3 more definition site/overload)_

_Source doc:_ Changes the resolution of the raster to the desired resolution without changing tile size or CRS. @param raster the raster to rescale @param rasterWidth the new raster width in terms of pixels @param rasterHeight the new height of the raster layer in terms of pixels @param unifiedRaster if set to true, all output tiles will belong to a single RasterMetadata @param interpolationMethod how to handle a target pixel that overlaps multiple source pixels @return a new raster RDD with the desired width and height

### Goal
Resize a raster layer to a target pixel width/height (resolution change) while keeping CRS and tile size unchanged, for workflows like downsampling large GeoTIFF/HDF products before analysis or export.

### Parameters
- `raster` (`RasterRDD[T]`): Input distributed raster to rescale.
- `rasterWidth` (`Int`): Target raster width in pixels.
- `rasterHeight` (`Int`): Target raster height in pixels.
- `unifiedRaster` (`Boolean`), default `false`: If `true`, output tiles belong to a single `RasterMetadata`.
- `interpolationMethod` (`InterpolationMethod.InterpolationMethod`), default `InterpolationMethod.NearestNeighbor`: Method used when a target pixel overlaps multiple source pixels (e.g., nearest-neighbor vs average-based behavior).

### Input
A `RasterRDD[T]` loaded in RDPro (commonly from GeoTIFF or HDF in documented workflows), plus target output pixel dimensions.

Preconditions / compatibility rules to enforce:
- Use a typed raster load that matches the real pixel type (e.g., `sc.geoTiff[Int]`, `sc.geoTiff[Float]`, `sc.geoTiff[Array[Int]]`, `sc.geoTiff[Array[Float]]`).
- `rescale` changes resolution only; it does **not** change CRS or tile size.
- Choose interpolation according to data semantics: nearest-neighbor is safe for categorical rasters; averaging-style interpolation is typically for continuous numeric rasters.

### Output
Returns `RasterRDD[T]` — a new raster RDD with the requested width/height in pixels, preserving CRS and tile-size behavior from the source (unless only metadata grouping is changed via `unifiedRaster`).

### Valid Call Patterns
```scala
val raster: RasterRDD[Int] = sc.geoTiff[Int]("glc2000_v1_1.tif")
val rescaled = raster.rescale(360, 180)
rescaled.saveAsGeoTiff("glc_small", GeoTiffWriter.WriteMode -> "compatibility")

val temperature: RasterRDD[Float] =
  sc.hdfFile("MOD11A1.A2022173.h08v05.006.2022174092443.hdf", "LST_Day_1km")
val rescaled = temperature.rescale(360, 180, RasterOperationsFocal.InterpolationMethod.Average)
temperature.reproject(CRS.decode("EPSG:4326"), RasterOperationsFocal.InterpolationMethod.Average)
```

### LLM Instruction Prompt
- Always call `rescale` as an instance method on a raster value (e.g., `raster.rescale(...)`).
- Keep argument order exactly as API-defined: width, height, optional `unifiedRaster`, optional interpolation.
- Do not claim CRS conversion from `rescale`; use `reproject` for CRS changes.
- Ensure `sc.geoTiff[T]` / `sc.hdfFile` typing matches actual pixel type before rescaling.
- Prefer nearest-neighbor for categorical classes; use average interpolation only for continuous numeric data.

### Prompt Snippet
```text
Given a RasterRDD[T], call value.rescale(targetWidth, targetHeight, unifiedRaster?, interpolationMethod?).
Do not use rescale for CRS conversion. Keep pixel type T consistent with the source raster load.
For categorical land-cover rasters, use default nearest-neighbor; for continuous measurements, pass Average if needed.
```

### Common Failure Modes
- Loading raster with wrong type parameter (e.g., `sc.geoTiff[Int]` for float pixels), causing downstream type/logic errors.
- Expecting `rescale` to reproject CRS; it will not.
- Using averaging interpolation on categorical rasters (class IDs become semantically invalid).
- Passing the 3rd positional argument as interpolation when method expects `unifiedRaster` first in the 4-arg form.

### Fix Code Hint
```scala
import edu.ucr.cs.bdlab.beast._

val lc: RasterRDD[Int] = sc.geoTiff[Int]("glc2000_v1_1.tif")
// Categorical raster -> nearest-neighbor default
val lcSmall: RasterRDD[Int] = lc.rescale(360, 180)

val temp: RasterRDD[Float] =
  sc.hdfFile("MOD11A1.A2022173.h08v05.006.2022174092443.hdf", "LST_Day_1km")
// Continuous raster -> explicit average interpolation
val tempSmall: RasterRDD[Float] =
  temp.rescale(360, 180, false, RasterOperationsFocal.InterpolationMethod.Average)
```

## API Test: `reshapeAverage`

### Signature
```scala
def reshapeAverage[T: ClassTag](raster: RasterRDD[T], targetMetadataConv: RasterMetadata => RasterMetadata, _numPartitions: Int = 0): RasterRDD[T]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsFocal.scala:58_

_Source doc:_ Converts the metadata of the input raster to the target metadata. This might involve any combination of the following: - reproject: Change the coordinate reference system (CRS) - regrid: Change the tiling of the raster - rescale: Change the resolution, i.e., number of pixels, in the raster - subset: Retrieve a subset of the data, even though, it would be an inefficient way to do just the subsetting Note: This is a low-level method that is normally not called directly by users. Instead, we provide higher-level easier to use functions for real use cases that all call this low-level function. Note: This method uses the average method to determine the final value of each pixel. If one pixel in the answer overlaps multiple pixels in the source, their average is computed. This method should only be used when pixels represent continuous values, e.g., red, infrared, temperature, or vegetation. If the pixels represent categorical values, e.g., land type, then the nearest neighbor method [[reshapeNN]] should be used instead. @param raster the input raster that should be reshaped @param targetMetadataConv a function that returns the desired metadata for source metadata @param _numPartitions the number of partitions of the produces RDD. If not set, it will be the same as the input @return the new raster with the target metadata

### Goal
Reshape a raster to new metadata (CRS/grid/resolution/extent) using **average resampling** so overlapping source pixels are averaged into each output pixel.

### Parameters
- `raster` (`RasterRDD[T]`): Input raster RDD to reshape.
- `targetMetadataConv` (`RasterMetadata => RasterMetadata,
                                  _numPartitions: Int`), default `0`: Function that maps source metadata to the desired target metadata; `_numPartitions` controls output partition count (default `0` means keep input partitioning behavior per source doc).

### Input
- A `RasterRDD[T]` (e.g., GeoTIFF/HDF loaded into RDPro types).
- A metadata conversion function `RasterMetadata => RasterMetadata` that defines target CRS/grid/resolution/extent.
- **Precondition:** use this method for **continuous numeric rasters** (e.g., temperature, reflectance, vegetation indices), because values are aggregated by averaging overlaps.
- **Compatibility/type rule:** choose raster load type to match real pixel type (e.g., `sc.geoTiff[Int]`, `sc.geoTiff[Float]`, `sc.geoTiff[Array[Int]]`, `sc.geoTiff[Array[Float]]`) before reshape; mismatched load type is a separate upstream failure mode.
- For categorical rasters (e.g., land cover classes), use `reshapeNN` instead of `reshapeAverage`.

### Output
Returns `RasterRDD[T]` — a new raster with target metadata applied (potentially reprojected/regridded/rescaled/subset), with pixel values computed via average where output pixels overlap multiple input pixels.

### Valid Call Patterns
```scala
val outputRaster = RasterOperationsFocal.reshapeAverage(inputRaster, _=>targetMetadata)
```

### LLM Instruction Prompt
- Call with receiver/qualifier exactly as verified: `RasterOperationsFocal.reshapeAverage(inputRaster, _=>targetMetadata)`.
- Provide a `targetMetadataConv` function, not raw metadata.
- Use only for continuous-value rasters; for categorical labels, switch to `reshapeNN`.
- Keep generic type `T` consistent with the raster’s actual pixel type selected at load time.

### Prompt Snippet
```text
Use RasterOperationsFocal.reshapeAverage(inputRaster, _ => targetMetadata) to reshape a continuous raster by averaging overlaps. Do not use it for categorical classes; use reshapeNN there. Ensure RasterRDD[T] pixel type matches the source raster type.
```

### Common Failure Modes
- Using `reshapeAverage` on categorical data (land-cover classes) causes invalid mixed class values.
- Passing metadata directly instead of a function (`RasterMetadata => RasterMetadata`) does not match the API shape.
- Loading raster with wrong type parameter (`sc.geoTiff[T]` mismatch) leads to incorrect/failed downstream processing.
- Expecting this low-level function to be the primary user API; source docs state it is low-level and usually wrapped by higher-level ops.

### Fix Code Hint
```scala
// Correct call shape (from tests)
val targetMetadata = sourceMetadata.rescale(10, 10)
val outputRaster = RasterOperationsFocal.reshapeAverage(inputRaster, _=>targetMetadata)

// If raster is categorical, use nearest-neighbor instead
// val outputRaster = RasterOperationsFocal.reshapeNN(inputRaster, _=>targetMetadata)
```

## API Test: `reshapeNN`

### Signature
```scala
def reshapeNN[T: ClassTag](raster: RasterRDD[T], targetMetadataConv: RasterMetadata => RasterMetadata, numPartitions: Int = 0): RasterRDD[T]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsFocal.scala:408_

_Source doc:_ Converts the metadata of the input raster to the target metadata. This might involve any combination of the following: - reproject: Change the coordinate reference system (CRS) - regrid: Change the tiling of the raster - rescale: Change the resolution, i.e., number of pixels, in the raster - subset: Retrieve a subset of the data, even though, it would be an inefficient way to do just the subsetting Note: This is a low-level method that is normally not called directly by users. Instead, we provide higher-level easier to use functions for real use cases that all call this low-level function. Note: This method uses the nearest neighbor method to match source to target pixels. Each target pixel gets its value from the nearest source pixel. If that source pixel is empty or outside the range of the source raster, the target pixel will be empty. @param raster the input raster that should be reshaped @param targetMetadataConv a function that converts a source RasterMetadata to target RasterMetadata @param numPartitions the number of partitions in the output RDD. If not set, the input numPartitions is used @return the new raster with the target metadata

### Goal
Reshape a distributed raster to new target metadata (CRS/grid/resolution/extent/tiling) using nearest-neighbor pixel assignment.

### Parameters
- `raster` (`RasterRDD[T]`): Input raster to reshape.
- `targetMetadataConv` (`RasterMetadata => RasterMetadata,
                             numPartitions: Int`), default `0`: A metadata-conversion function from source `RasterMetadata` to target `RasterMetadata`; `numPartitions` controls output partition count (0 means use input partition count).

### Input
- A `RasterRDD[T]` already loaded in RDPro (for example from GeoTIFF/HDF workflows).
- A target metadata conversion function that returns the desired output `RasterMetadata`.
- Type parameter `T` must match the runtime pixel type when loading rasters (e.g., `sc.geoTiff[Int]`, `sc.geoTiff[Float]`, `sc.geoTiff[Array[Int]]`, `sc.geoTiff[Array[Float]]`).
- This is a low-level reshape primitive; it can perform reproject/regrid/rescale/subset in one step.
- Nearest-neighbor behavior: each target pixel is copied from nearest source pixel; if nearest source is empty or outside source raster range, target pixel is empty.

### Output
Returns `RasterRDD[T]` — a new raster RDD with target metadata and nearest-neighbor sampled pixel values.

### Valid Call Patterns
```scala
val raster: RasterRDD[Int] = sc.geoTiff[Int]("glc2000_v1_1.tif")
val reshaped = RasterOperationsFocal.reshapeNN(raster,
  RasterMetadata.create(-124, 42, -114, 32, 4326, 1000, 1000, 100, 100))
reshaped.saveAsGeoTiff("glc_ca")
```

### LLM Instruction Prompt
- Use receiver form exactly as documented: `RasterOperationsFocal.reshapeNN(raster, ...)`.
- Pass a `RasterRDD[T]` and a metadata conversion argument in the second position.
- Keep pixel type consistent with source raster load type.
- Use `reshapeNN` for categorical/general nearest-neighbor reshaping; do not switch to averaging semantics.
- Do not invent extra parameters or alternate signatures.

### Prompt Snippet
```text
Given a RasterRDD[T], call RasterOperationsFocal.reshapeNN(raster, targetMetadataConv, numPartitions).
Use nearest-neighbor semantics and keep T consistent with the raster’s actual pixel type.
If numPartitions is omitted, output partitions default to input partition count.
```

### Common Failure Modes
- Loading raster with wrong type parameter `T` (pixel type mismatch).
- Passing a non-conversion second argument shape (must match metadata conversion usage expected by API/signature).
- Expecting interpolation/averaging behavior from `reshapeNN` (it is nearest neighbor only).
- Assuming out-of-range or empty source pixels will be filled; they remain empty in output.

### Fix Code Hint
```scala
import edu.ucr.cs.bdlab.beast._

val raster: RasterRDD[Int] = sc.geoTiff[Int]("glc2000_v1_1.tif")

val reshaped: RasterRDD[Int] = RasterOperationsFocal.reshapeNN(
  raster,
  RasterMetadata.create(-124, 42, -114, 32, 4326, 1000, 1000, 100, 100)
  // optional third arg: numPartitions
)

reshaped.saveAsGeoTiff("glc_ca")
```

## API Test: `retainIndex`

### Signature
```scala
def retainIndex(index: Int): BeastOptions
```
_Source: beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/common/BeastOptions.scala:168_

_Source doc:_ Keep only the parameters that do not have an index or the ones with the given index. In other words, remove any indexed parameter that have a different index than the one given. The index of the parameter is a suffix between square brackets, e.g., param[1] @param index the index to retain @return a new options with the given index retained

### Goal
Filter a `BeastOptions` object so it keeps unindexed parameters plus only parameters whose bracket index matches the requested `index`, while dropping differently indexed entries.

### Parameters
- `index` (`Int`): the bracket index to retain (for keys shaped like `param[index]`).

### Input
A `BeastOptions` instance containing option keys, where some keys may be indexed using a square-bracket suffix such as `key1[1]` and others may be unindexed such as `key3`.

Preconditions:
- Call form is instance-based (`opts.retainIndex(...)`) as verified by test usage.
- Indexed keys are expected in the documented suffix format `name[number]` for this filtering behavior to apply.
- No raster/vector file-format input is involved for this method.

### Output
Returns `BeastOptions` — a new options object that:
- keeps all unindexed keys,
- keeps keys with the requested bracket index,
- removes keys with other bracket indices,
- and exposes retained indexed values under unindexed key names (as shown by `opts1("key1") == "val1"` in tests).

### Valid Call Patterns
```scala
val opts = new BeastOptions().set("key1[1]", "val1")
  .set("key1[2]", "val2")
  .set("key3", "val3")
  .set("key4[2]", "val4")
assert(opts("key1[1]") == "val1")
val opts1 = opts.retainIndex(1)
assert(opts1("key1") == "val1")
assert(!opts1.contains("key4"))
assert(opts1("key3") == "val3")
val opts2 = opts.retainIndex(2)
assert(opts2("key1") == "val2")
assert(opts2("key3") == "val3")
assert(opts2("key4") == "val4")
```

### LLM Instruction Prompt
- Call `retainIndex` as an instance method on an existing `BeastOptions` value: `opts.retainIndex(i)`.
- Pass a single `Int` argument.
- Use indexed option keys in `name[index]` form when preparing options to be filtered.
- Do not invent overloads or extra parameters.

### Prompt Snippet
```text
Given a BeastOptions value `opts`, keep only index 2 settings plus unindexed settings by calling:
`val filtered = opts.retainIndex(2)`.
Assume indexed keys use the `param[2]` suffix format.
```

### Common Failure Modes
- Calling it as a static/global function (e.g., `retainIndex(1)`) instead of on a `BeastOptions` instance.
- Expecting keys with non-matching indices (e.g., `[1]` when retaining `2`) to remain.
- Expecting only indexed keys to remain; unindexed keys are also retained by design.
- Using inconsistent key naming instead of documented bracket suffixes, which can prevent intended index-based filtering.

### Fix Code Hint
```scala
val opts = new BeastOptions()
  .set("input[1]", "a.tif")
  .set("input[2]", "b.tif")
  .set("format", "geotiff")

val keep2: BeastOptions = opts.retainIndex(2)
// keep2 should retain "format" and index-2 values, and drop index-1 values
```

## API Test: `retile`

### Signature
```scala
def retile(tileWidth: Int, tileHeight: Int)
def retile[T: ClassTag](raster: RasterRDD[T], tileWidth: Int, tileHeight: Int): RasterRDD[T]
def retile(newTileWidth: Int, newTileHeight: Int): RasterMetadata
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsFocal.scala:566  (+2 more definition site/overload)_

_Source doc:_ Regrids the given raster to the target tile width and height @param raster the raster to regrid @param tileWidth the new tile width in pixels @param tileHeight the new tile height in pixels @tparam T the type of the pixel values in the raster @return a new raster with the given tile width and height

### Goal
Regrid a `RasterRDD[T]` into a new tile layout by setting tile width/height in pixels, while keeping the same pixel value type `T`.

### Parameters
- `raster` (`RasterRDD[T]`): input distributed raster to retile.
- `tileWidth` (`Int`): target tile width in pixels.
- `tileHeight` (`Int`): target tile height in pixels.

### Input
A `RasterRDD[T]` (commonly loaded from GeoTIFF or HDF in RDPro workflows) and integer target tile dimensions.  
Preconditions and compatibility/type rules to keep calls correct:

- Use a correctly typed raster load before calling (`sc.geoTiff[T]` type must match the real pixel type).
- `tileWidth` and `tileHeight` are pixel counts for the new tile grid.
- If this is part of a multi-raster pipeline (for example before `overlay`), ensure downstream metadata compatibility requirements are met (same resolution/CRS/tile size across rasters), potentially by reshape/reproject operations before combining datasets.

### Output
Returns `RasterRDD[T]` — a new raster dataset containing the same pixel type `T`, but regridded to the requested tile width and tile height.

### Valid Call Patterns
```scala
val raster: RasterRDD[Int] = sc.geoTiff[Int]("glc2000_v1_1.tif")
val retiled = raster.retile(64, 64)
retiled.saveAsGeoTiff("glc_retiled")

val raster: RasterRDD[Int] = sc.geoTiff[Int]("glc2000_v1_1.tif")
val retiled = raster.retile(64, 64).explode
retiled.saveAsGeoTiff("glc_retiled", GeoTiffWriter.WriteMode -> "distributed")

val retiled: RasterRDD[Int] = RasterOperationsFocal.retile(raster, 20, 20)
```

### LLM Instruction Prompt
- Call `retile` using a real supported receiver form: `raster.retile(tileWidth, tileHeight)` or `RasterOperationsFocal.retile(raster, tileWidth, tileHeight)`.
- Keep argument order exactly `(raster, tileWidth, tileHeight)` for the static form.
- Ensure raster type parameter `T` is already correct at load time (`sc.geoTiff[T]` matched to actual pixel type).
- Do not invent extra parameters (no CRS/resampling/compression args on `retile` itself).
- If the result is used with operations that require matching metadata (e.g., overlay), align datasets as needed in preceding steps.

### Prompt Snippet
```text
Retile this RasterRDD to a new tile grid using raster.retile(tileWidth, tileHeight), keeping the same pixel type T. 
Use only the provided RasterRDD and integer tile sizes; do not add extra retile arguments.
If this raster will be combined with other rasters later, ensure metadata compatibility in the pipeline.
```

### Common Failure Modes
- Loading raster with wrong `T` (e.g., `sc.geoTiff[Int]` for non-integer pixel data), causing type/runtime issues earlier in pipeline.
- Using unsupported/invented call shapes or extra arguments not in the API.
- Retiling one raster but not other rasters before metadata-sensitive combination steps (such as overlay), causing compatibility errors downstream.
- Confusing `retile` overloads: one overload returns `RasterRDD[T]` (raster retile), another listed overload returns `RasterMetadata`.

### Fix Code Hint
```scala
import edu.ucr.cs.bdlab.beast._

val raster: RasterRDD[Int] = sc.geoTiff[Int]("glc2000_v1_1.tif")
val retiled: RasterRDD[Int] = raster.retile(64, 64)
retiled.saveAsGeoTiff("glc_retiled")
```

## API Test: `run`

### Signature
```scala
override def run(opts: BeastOptions, inputs: Array[String], outputs: Array[String], sc: SparkContext): Any
override def run(opts: BeastOptions, inputs: Array[String], outputs: Array[String], sc: SparkContext): Unit
def run(source: String, tileDir: String, indexFile:FileStatus, z: Int, currX: Int, currY: Int, sc: SparkContext): (BufferedImage,Int)
def run(inputs: Array[String], sc: SparkContext): String
def run(inputs: Array[String], sc: SparkContext): Array[Int]
def run(opts: BeastOptions, inputs: Array[String], sc: SparkContext): String
def run(inputs: Array[String], sc: SparkContext): BufferedImage
def run(): Unit
def run(opts: BeastOptions, inputs: Array[String], outputs: Array[String], sc: JavaSparkContext): Any
def run(opts: BeastOptions, inputs: Array[String], outputs: Array[String], sc: SparkContext): Any
def run(opts: BeastOptions, inputs: Array[String], outputs: Array[String], ss: SparkSession): Any
```
_Source: beast/dynoviz/src/main/scala/edu/ucr/cs/bdlab/dynoviz/NPYTileGeneratorOnthefly.scala:29  (+28 more definition site/overload)_

### Goal
Run a Beast operation’s main execution entry point using user options, input/output paths, and a Spark context, returning an operation-specific result.

### Parameters
- `source` (`String`): Unknown from the provided authoritative API facts for the documented `run`; this name belongs to a different overload listed in the signature block.
- `tileDir` (`String`): Unknown from the provided authoritative API facts for the documented `run`; this name belongs to a different overload listed in the signature block.
- `indexFile` (`FileStatus`): Unknown from the provided authoritative API facts for the documented `run`; this name belongs to a different overload listed in the signature block.
- `z` (`Int`): Unknown from the provided authoritative API facts for the documented `run`; this name belongs to a different overload listed in the signature block.
- `currX` (`Int`): Unknown from the provided authoritative API facts for the documented `run`; this name belongs to a different overload listed in the signature block.
- `currY` (`Int`): Unknown from the provided authoritative API facts for the documented `run`; this name belongs to a different overload listed in the signature block.
- `sc` (`SparkContext`): The Spark context used to execute the operation.

### Input
For the authoritative method:

`override def run(opts: BeastOptions, inputs: Array[String], outputs: Array[String], sc: SparkContext): Any`

the caller must provide:
- `opts`: command-style Beast options that configure the operation.
- `inputs`: input path array (operation-specific interpretation).
- `outputs`: output path array (operation-specific interpretation; may be `null` in real passing tests for some operations).
- `sc`: active Spark context.

Documented Beast/RDPro ecosystem input formats include:
- Raster: GeoTIFF and HDF (for raster workflows).
- Vector: shapefile/GeoJSON/CSV-WKT and others (for vector workflows).

Preconditions are operation-specific. From provided tested usage, `run` may still return in-memory results even when output format settings are invalid, depending on operation behavior.

### Output
Returns `(BufferedImage,Int)` — this return applies to a different overload (`run(source, tileDir, indexFile, z, currX, currY, sc)`) shown in the signature list, not to the authoritative API fact.  
For the authoritative method, return type is `Any`, documented as an optional operation result.

### Valid Call Patterns
```scala
val summary = GeometricSummary.run(opts, Array(inputfile.getPath), null, sparkContext).asInstanceOf[Summary]
```

```scala
new BeastServer().run(new BeastOptions(), null, null, sparkContext)
```

### LLM Instruction Prompt
- Call the 4-argument SparkContext form exactly as `value.run(opts, inputs, outputs, sc)` (or `Object.run(...)` when documented that way).
- Do not invent additional parameters or change argument order.
- Treat result as operation-specific `Any`; cast only when the concrete operation is known (e.g., `Summary`).
- `inputs`/`outputs` may be `null` for operations that accept it (as shown in real usage), but prefer explicit arrays when required by the chosen operation.

### Prompt Snippet
```text
Use the Beast operation entry point with this exact call shape:
<receiver>.run(opts: BeastOptions, inputs: Array[String], outputs: Array[String], sc: SparkContext)

Do not change parameter order. Do not add parameters. The return type is Any and depends on the concrete operation.
```

### Common Failure Modes
- Using a bare `run(...)` without receiver when only `Object.run(...)` or `instance.run(...)` is available.
- Assuming a fixed return type for all operations; `run` returns `Any`.
- Passing incompatible or missing `opts` keys for the selected operation.
- Providing wrong input format/options pair (e.g., mismatched `iformat` vs actual data layout).
- Confusing overloads: the `(BufferedImage, Int)` return is not from the authoritative `opts/inputs/outputs/sc` signature.

### Fix Code Hint
```scala
val opts = new BeastOptions()
  .set("iformat", "wkt(Geometry)")
  .set("skipheader", true)
  .set("separator", "\t")

val result: Any = GeometricSummary.run(opts, Array(inputfile.getPath), null, sparkContext)
// If you know the operation result type:
val summary = result.asInstanceOf[Summary]
```

## API Test: `runDuplicateAvoidance`

### Signature
```scala
private[beast] def runDuplicateAvoidance(features: SpatialRDD): SpatialRDD
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/indexing/IndexHelper.scala:354_

_Source doc:_ Run the duplicate avoidance technique on the given set of features if it is spatially partitioned using a disjoint partitioner. Otherwise, the input set is returned as-is. @param features the set of features to remove the duplicates from. @return a set of features with all duplicates removed.

### Goal
Remove replicated features introduced by disjoint spatial partitioning (when applicable), while leaving non-disjoint inputs unchanged.

### Parameters
- `features` (`SpatialRDD`): the input spatial feature dataset to de-duplicate if it has been partitioned with a disjoint partitioner.

### Input
A `SpatialRDD` in memory (not a file path argument to this function).  
Preconditions and compatibility rules from project context:

- Duplicate-avoidance is relevant when data was spatially partitioned with **disjoint** partitions, which may replicate features across partitions.
- If the input is **not** spatially partitioned using a disjoint partitioner, this method returns the input as-is (per source doc).
- This is an internal Beast API (`private[beast]`), so direct use is intended from Beast package scope.

### Output
Returns `SpatialRDD` — a spatial feature RDD with duplicates removed when duplicate-avoidance conditions apply; otherwise effectively the same feature set as input.

### Valid Call Patterns
```scala
assert(IndexHelper.runDuplicateAvoidance(partitioned1).count() == 10000)
assert(IndexHelper.runDuplicateAvoidance(partitioned2).count() == 10000)
```

### LLM Instruction Prompt
- Use the receiver-qualified call form exactly as validated in tests: `IndexHelper.runDuplicateAvoidance(features)`.
- Pass exactly one argument of type `SpatialRDD`.
- Do not add extra parameters/options.
- Only claim deduplication behavior stated in source doc: runs for disjoint-partitioned input; otherwise returns input as-is.
- Do not invent file I/O for this function (it operates on an existing `SpatialRDD`).

### Prompt Snippet
```text
Given a SpatialRDD named partitionedFeatures, call IndexHelper.runDuplicateAvoidance(partitionedFeatures) and use the returned SpatialRDD for downstream count/join/query. Assume duplicate removal is applied only when the input uses disjoint spatial partitioning; otherwise treat output as unchanged from input.
```

### Common Failure Modes
- Calling it as a bare `runDuplicateAvoidance(...)` without `IndexHelper` qualifier (call shape not grounded in provided examples).
- Expecting duplicate removal on any partitioning strategy; per source doc, behavior is conditional on disjoint partitioning.
- Trying to pass file paths or non-`SpatialRDD` objects.

### Fix Code Hint
```scala
val deduped: SpatialRDD = IndexHelper.runDuplicateAvoidance(partitionedFeatures)
```

## API Test: `saveAsCSVPoints`

### Signature
```scala
def saveAsCSVPoints(filename: String, xColumn: Int = 0, yColumn: Int = 1, delimiter: Char = ',', header: Boolean = true): Unit
def saveAsCSVPoints(rdd: JavaSpatialRDD, filename: String, xColumn: Int, yColumn: Int, delimiter: Char, header: Boolean): Unit
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/ReadWriteMixin.scala:212  (+1 more definition site/overload)_

_Source doc:_ Save features to a CSV or text-delimited file. This method should be used only for point features. @param filename the name of the output file @param xColumn the index of the column that contains the x-coordinate in the output file @param yColumn the index of the column that contains the y-coordinate in the output file @param delimiter the delimiter in the output file, comma by default @param header whether to write a header line, true by default

### Goal
Write a point-feature `SpatialRDD`/`JavaSpatialRDD` to a CSV (or other text-delimited) output file with configurable X/Y column positions, delimiter, and optional header.

### Parameters
- `filename` (`String`): Output file name/path to write the CSV or text-delimited result to.
- `xColumn` (`Int`), default `0`: Zero-based output column index that should contain the x-coordinate.
- `yColumn` (`Int`), default `1`: Zero-based output column index that should contain the y-coordinate.
- `delimiter` (`Char`), default `'`: Delimiter character used between output columns (source doc states comma is the default delimiter).
- `'`: This appears to be a parsing artifact in the provided API facts (not an actual standalone parameter in the Scala signature).
- `header` (`Boolean`), default `true`: Whether to write a header line.

### Input
A point-feature dataset (per source doc: “should be used only for point features”) on a receiver that supports `saveAsCSVPoints`, e.g., `records.saveAsCSVPoints(...)`, or the Java overload with `JavaSpatialRDD`.  
Supported output encoding is CSV or text-delimited text.  
No additional CRS/type-conversion rules are documented for this method in the provided sources.

### Output
Returns `Unit` — side effect only: writes a CSV/text-delimited file at `filename`; no in-memory return value.

### Valid Call Patterns
```scala
// Scala
records.saveAsCSVPoints("output.csv", 1, 2, ',', true)

// Java
JavaSpatialRDDHelper.saveAsCSVPoints(records, "output.csv", 1, 2, ',', true);
```

### LLM Instruction Prompt
- Use this method only for point features.
- Preserve receiver form exactly as documented (`records.saveAsCSVPoints(...)` in Scala, helper static call in Java).
- Pass delimiter as a `Char` (e.g., `','`), not a `String`.
- Do not invent extra parameters or return handling; it returns `Unit`.

### Prompt Snippet
```text
Given a point-feature SpatialRDD named records, write it as CSV using:
records.saveAsCSVPoints("output.csv", 1, 2, ',', true)
Use xColumn/yColumn as zero-based output column positions, delimiter as Char, and optional header flag.
```

### Common Failure Modes
- Calling on non-point features (violates documented precondition).
- Passing delimiter as string literal (`","`) instead of char (`','`).
- Assuming a returned dataset/value; this API writes output and returns `Unit`.
- Misinterpreting `xColumn`/`yColumn` as input-schema positions instead of output column indices.

### Fix Code Hint
```scala
// Ensure records contains point features, then write with char delimiter and explicit columns
records.saveAsCSVPoints("output.csv", 1, 2, ',', true)
```

## API Test: `saveAsGeoJSON`

### Signature
```scala
def saveAsGeoJSON(filename: String, opts: BeastOptions = new BeastOptions()): Unit
def saveAsGeoJSON(rdd: JavaSpatialRDD, filename: String): Unit
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/ReadWriteMixin.scala:201  (+1 more definition site/overload)_

_Source doc:_ Save features in GeoJSON format @param filename the output filename

### Goal
Write a spatial feature dataset (vector records) to disk in GeoJSON format for downstream geospatial analysis and exchange.

### Parameters
- `filename` (`String`): Output file path/name for the GeoJSON to write (for example, `"output.geojson"`).
- `opts` (`BeastOptions`), default `new BeastOptions()`: Writer options container; if omitted, default options are used.

### Input
A spatial/vector dataset (the receiver in Scala instance style, or a `JavaSpatialRDD` in the Java overload) must already exist in your Spark pipeline.  
Documented vector I/O context includes GeoJSON as an output format.  
No additional `saveAsGeoJSON`-specific preconditions are explicitly documented in the provided sources.

### Output
Returns `Unit` — the method performs a side effect by writing the input features to the specified GeoJSON output location.

### Valid Call Patterns
```scala
// Scala
records.saveAsGeoJSON("output.geojson")

// Java
JavaSpatialRDDHelper.saveAsGeoJSON(records, "output.geojson")
```

### LLM Instruction Prompt
- Use the instance-style Scala call exactly as documented: `records.saveAsGeoJSON("...")`.
- Provide a concrete output filename string.
- Only pass `opts` when you explicitly need non-default `BeastOptions`.
- Do not invent extra parameters or return values; this API returns `Unit`.

### Prompt Snippet
```text
Given a SpatialRDD named `records`, write it as GeoJSON using:
records.saveAsGeoJSON("output.geojson")
If custom write settings are needed, use the overload with opts:
records.saveAsGeoJSON("output.geojson", opts)
```

### Common Failure Modes
- Calling it as a bare function (`saveAsGeoJSON(...)`) without a receiver in Scala; documented usage is receiver-based (`records.saveAsGeoJSON(...)`).
- Expecting a returned dataset/value; this method returns `Unit` and writes output as a side effect.
- Passing a non-string or empty/invalid output path in `filename`.

### Fix Code Hint
```scala
// Correct Scala receiver-style usage
records.saveAsGeoJSON("output.geojson")

// With explicit options object
val opts = new BeastOptions()
records.saveAsGeoJSON("output.geojson", opts)
```

## API Test: `saveAsGeoTiff`

### Signature
```scala
def saveAsGeoTiff(path: String, opts: BeastOptions = new BeastOptions): Unit
def saveAsGeoTiff[T](rasterRDD: RDD[ITile[T]], outPath: String, opts: BeastOptions): Unit
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/GeoTiffWriter.scala:476  (+1 more definition site/overload)_

### Goal
Save an RDPro raster (`RasterRDD` / `RDD[ITile[T]]`) to GeoTIFF output at a target path, with optional writer settings in `BeastOptions`.

### Parameters
- `rasterRDD` (`RDD[ITile[T]]`): The raster tiles to write (static overload); in instance-style usage, this is the receiver raster (for example, `temperatureF.saveAsGeoTiff(...)`).
- `outPath` (`String`): Destination path to write GeoTIFF output files to.
- `opts` (`BeastOptions`): Additional GeoTIFF writer options (for example, options used by `GeoTiffWriter` such as bits-per-sample / BigTIFF in project tests).

### Input
A raster dataset already loaded/produced in RDPro (commonly from GeoTIFF/HDF workflows) as `RasterRDD[T]` / `RDD[ITile[T]]`, plus an output path string and optional `BeastOptions`.

Preconditions and compatibility rules to keep calls correct in pipelines:
- Use typed raster loading correctly upstream (`sc.geoTiff[T]` must match the real pixel type).
- If the raster was created from multi-raster operations (for example overlay/reshape workflows), ensure upstream compatibility constraints were satisfied before writing (e.g., overlay requires same metadata unless reshaped first).
- Bit compaction applies to integer pixels; float pixels remain 32-bit.

### Output
Returns `Unit` — the method performs a write side effect, producing GeoTIFF output at the specified path.

### Valid Call Patterns
```scala
val temperatureK: RasterRDD[Float] =
  sc.hdfFile("MOD11A1.A2022173.h08v05.006.2022174092443.hdf", "LST_Day_1km")
val temperatureF: RasterRDD[Float] = temperatureK.mapPixels(k => (k-273.15f) * 9 / 5 + 32)
temperatureF.saveAsGeoTiff("temperature_f")

val temperatureK: RasterRDD[Float] =
  sc.hdfFile("MOD11A1.A2022173.h08v05.006.2022174092443.hdf", "LST_Day_1km")
temperatureK.filterPixels(_>300).saveAsGeoTiff("temperature_high")

GeoTiffWriter.saveAsGeoTiff(rasterRDD, outputFile.getPath, GeoTiffWriter.BitsPerSample -> 8)

GeoTiffWriter.saveAsGeoTiff(rasterRDD, outputFile.getPath,
  Seq(GeoTiffWriter.BitsPerSample -> 8, GeoTiffWriter.BigTiff -> "yes"))
```

### LLM Instruction Prompt
- Call `saveAsGeoTiff` using a real receiver/qualifier form shown in project usage (`value.saveAsGeoTiff(...)` or `GeoTiffWriter.saveAsGeoTiff(...)`).
- Do not invent extra parameters beyond `path/outPath` and `opts`.
- Provide `BeastOptions`/writer options only when needed; otherwise rely on default options.
- Ensure upstream raster typing/preparation is valid before saving.

### Prompt Snippet
```text
Given a RasterRDD produced in RDPro, write it as GeoTIFF using either:
1) instance form: raster.saveAsGeoTiff(outputPath)
2) static form: GeoTiffWriter.saveAsGeoTiff(rasterRDD, outputPath, opts)

Do not add unsupported arguments. Keep typed raster loading and upstream compatibility rules valid.
```

### Common Failure Modes
- Pixel type mismatch earlier in pipeline (wrong `sc.geoTiff[T]`) leading to invalid downstream processing before save.
- Using integer-only bit-compaction expectations with float rasters.
- Attempting to save a raster produced from incompatible inputs that were not aligned/reshaped first.
- Passing an invalid/unwritable output path.

### Fix Code Hint
```scala
import edu.ucr.cs.bdlab.beast._

val raster: RasterRDD[Float] =
  sc.hdfFile("MOD11A1.A2022173.h08v05.006.2022174092443.hdf", "LST_Day_1km")

// Keep processing type-safe, then save
val out: RasterRDD[Float] = raster.mapPixels(k => (k - 273.15f) * 9 / 5 + 32)
out.saveAsGeoTiff("temperature_f")
```

## API Test: `saveAsIndex`

### Signature
```scala
def saveAsIndex(indexPath: String, oformat: String = "rtree"): Unit
def saveAsIndex(partitionedRDD: JavaPartitionedSpatialRDD, indexPath: String): Unit
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/indexing/IndexMixin.scala:92  (+1 more definition site/overload)_

### Goal
Write a **spatially partitioned** dataset to an index directory as partition files plus a `_master` metadata file, typically for faster downstream spatial access.

### Parameters
- `indexPath` (`String`): Output path where the indexed partition files and `_master` file are written.
- `oformat` (`String`), default `"rtree"`: Output index/file format name; documented default is `"rtree"`.

### Input
A spatial RDD that has already been spatially partitioned (e.g., via `spatialPartition(...)` / `partitionBy(...)`), then saved with this API.

Preconditions from project context:
- The operation is for **spatially partitioned** data (source doc explicitly says “Writes a spatially partitioned RDD…”).
- If you need disjoint partitioning behavior, that must be configured at partitioning time with a partitioner that supports it; otherwise partitioning can fail before `saveAsIndex`.
- `indexPath` must be a writable filesystem path visible to Spark (local/HDFS depending cluster config).

### Output
Returns `Unit` — side effect only.  
On storage, it produces:
- one file per partition, and
- a `_master` file with partition metadata.

### Valid Call Patterns
```scala
// Index the datasets
sparkContext.shapefile("ne_10m_admin_1_states_provinces.zip")
    .partitionBy(classOf[RSGrovePartitioner])
    .saveAsIndex("provinces_index", "rtree")
```

### LLM Instruction Prompt
- Call `saveAsIndex` as an instance method on a partitioned spatial dataset (`value.saveAsIndex(...)`).
- Keep argument order exactly: `indexPath` first, then optional `oformat`.
- Prefer explicit `"rtree"` when matching documented examples; otherwise omit to use default.
- Do not invent extra options/parameters.
- Ensure data is partitioned before calling; if not, partition first.

### Prompt Snippet
```text
Partition the spatial dataset first, then call:
partitioned.saveAsIndex(indexPath, "rtree")
Use only the documented parameters (indexPath, optional oformat).
```

### Common Failure Modes
- Calling `saveAsIndex` on non-partitioned data (violates documented expectation of spatially partitioned input).
- Invalid or non-writable `indexPath`.
- Assuming unsupported index format strings in `oformat` (only default `"rtree"` is explicitly documented here).
- Earlier partitioning step misconfigured (e.g., disjoint option with unsupported partitioner), so no valid partitioned RDD is produced for saving.

### Fix Code Hint
```scala
import edu.ucr.cs.bdlab.beast._

val partitioned =
  sparkContext.shapefile("ne_10m_admin_1_states_provinces.zip")
    .partitionBy(classOf[RSGrovePartitioner])

partitioned.saveAsIndex("provinces_index", "rtree")
// or rely on default format:
// partitioned.saveAsIndex("provinces_index")
```

## API Test: `saveAsKML`

### Signature
```scala
def saveAsKML(filename: String): Unit
def saveAsKML(rdd: JavaSpatialRDD, filename: String): Unit
```
_Source: beast/beast-spark/src/main/scala/edu/ucr/cs/bdlab/beast/JavaSpatialRDDHelper.scala:86  (+1 more definition site/overload)_

_Source doc:_ Save features in KML format @param filename the name of the output file

### Goal
Save a spatial feature dataset (vector records) to a KML file for downstream geospatial use and visualization.

### Parameters
- `rdd` (`JavaSpatialRDD`): The Java spatial RDD to write (used in the Java helper overload).
- `filename` (`String`): The output KML file name/path.

### Input
A populated spatial/vector dataset is required as the receiver (`records.saveAsKML(...)`) or as `rdd` in the Java helper overload.  
KML/KMZ is documented as **output-only** in this project context.  
No additional compatibility/type-parameter rules are documented specifically for `saveAsKML`.

### Output
Returns `Unit` — the method performs a side effect by writing the features to KML at `filename`; no value is returned.

### Valid Call Patterns
```scala
// Scala
records.saveAsKML("output.kml")

// Java
JavaSpatialRDDHelper.saveAsKML(records, "output.kml")
```

### LLM Instruction Prompt
- Use the instance form exactly as documented for Scala: `records.saveAsKML("...")`.
- Use the helper overload exactly as documented for Java: `JavaSpatialRDDHelper.saveAsKML(records, "...")`.
- Pass exactly one filename string in Scala, or `(JavaSpatialRDD, filename)` in Java.
- Do not invent extra options/parameters (none are documented for this API).

### Prompt Snippet
```text
Given a SpatialRDD `records`, write it to KML using:
records.saveAsKML("output.kml")

For JavaSpatialRDD, use:
JavaSpatialRDDHelper.saveAsKML(records, "output.kml")
```

### Common Failure Modes
- Calling a non-existent shape such as bare `saveAsKML("output.kml")` without a receiver.
- Passing arguments in the wrong order in Java helper calls.
- Assuming extra writer options exist for KML output on this method (not documented here).

### Fix Code Hint
```scala
// Scala: call on the dataset object
records.saveAsKML("output.kml")

// Java helper overload: pass (rdd, filename)
JavaSpatialRDDHelper.saveAsKML(records, "output.kml")
```

## API Test: `saveAsShapefile`

### Signature
```scala
def saveAsShapefile(filename: String, opts: BeastOptions = new BeastOptions()): Unit
def saveAsShapefile(rdd: JavaSpatialRDD, filename: String): Unit
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/ReadWriteMixin.scala:194  (+1 more definition site/overload)_

_Source doc:_ Save features as a shapefile @param filename the output filename

### Goal
Write a spatial feature dataset (vector records) from Beast/RDPro Spark workflows to Shapefile output.

### Parameters
- `filename` (`String`): Output filename/path for the shapefile to write (for example, `"output.shp"` in the project README usage).
- `opts` (`BeastOptions`), default `new BeastOptions()`: Optional Beast write options; if not provided, defaults are used.

### Input
A spatial/vector RDD-like dataset (features) as the receiver for the Scala instance form, or a `JavaSpatialRDD` for the Java helper overload.

Supported/project-documented vector I/O context includes Shapefile output.  
No additional `saveAsShapefile`-specific preconditions are documented in the provided sources.

### Output
Returns `Unit` — the method performs side-effecting write of the input features as a Shapefile at `filename`; no Scala return value is produced.

### Valid Call Patterns
```scala
// Scala
records.saveAsShapefile("output.shp")

// Java
JavaSpatialRDDHelper.saveAsShapefile(records, "output.shp");
```

### LLM Instruction Prompt
- Use the instance call form exactly as documented when writing Scala: `value.saveAsShapefile("...")`.
- Pass a `String` output filename.
- Only pass `opts` when you explicitly need non-default `BeastOptions`; otherwise rely on `new BeastOptions()`.
- Do not invent extra parameters or a different argument order.

### Prompt Snippet
```text
Given a SpatialRDD-like value `records`, write it as a shapefile using:
records.saveAsShapefile(outputPath)
where `outputPath` is a String such as "output.shp".
If options are needed, use the overload with `opts: BeastOptions`.
```

### Common Failure Modes
- Calling with a non-string output argument (must be `filename: String`).
- Using a nonexistent call shape (for example, adding unsupported parameters).
- In Scala, dropping the receiver and calling a bare `saveAsShapefile(...)` in contexts where the implicit mixin/extension is not in scope.

### Fix Code Hint
```scala
import edu.ucr.cs.bdlab.beast._

// Correct Scala call shape from project README
records.saveAsShapefile("output.shp")

// Optional explicit options form (same signature)
records.saveAsShapefile("output.shp", new BeastOptions())
```

## API Test: `saveAsWKTFile`

### Signature
```scala
def saveAsWKTFile(filename: String, wktColumn: Int, delimiter: Char = '\t', header: Boolean = true): Unit
def saveAsWKTFile(rdd: JavaSpatialRDD, filename: String, wktColumn: Int, delimiter: Char, header: Boolean): Unit
```
_Source: beast/beast-spark/src/main/scala/edu/ucr/cs/bdlab/beast/JavaSpatialRDDHelper.scala:79  (+1 more definition site/overload)_

_Source doc:_ Save features to a CSV file where the geometry is encoded in WKT format @param filename the name of the output file @param wktColumn the index of the column that contains the WKT attribute @param delimiter the delimiter between attributes, tab by default @param header whether to write a header line or not, true by default

### Goal
Write a spatial feature dataset to a delimited text (CSV-like) file where geometry is stored as WKT in a specified column.

### Parameters
- `rdd` (`JavaSpatialRDD`): The Java spatial RDD to write (Java overload).
- `filename` (`String`): Output file name/path to write.
- `wktColumn` (`Int`): Zero-based index of the column that contains (or will contain) the WKT geometry attribute.
- `delimiter` (`Char`): Field separator character between attributes (default is tab `'\t'`).
- `header` (`Boolean`): Whether to write a header line (default `true`).

### Input
A spatial feature RDD (Scala call style shown as instance method in README, and Java overload with `JavaSpatialRDD`) plus:
- an output destination `filename`,
- a valid geometry column index `wktColumn`,
- optional delimiter and header choice.

Format intent is a delimited text file with WKT geometry encoding.  
No additional preconditions are explicitly documented for this method in the provided sources.

### Output
Returns `Unit` — it performs a write side effect: creates/writes a delimited output file where geometry is encoded as WKT.

### Valid Call Patterns
```scala
// Scala
records.saveAsWKTFile("output.csv", 0, '\t', false)

// Java
JavaSpatialRDDHelper.saveAsWKTFile(records, "output.csv", 0, '\t', false)
```

### LLM Instruction Prompt
- Use one of the documented call shapes exactly (Scala instance call or Java helper static call).
- Keep argument order exactly: `filename, wktColumn, delimiter, header` (or `rdd, filename, wktColumn, delimiter, header` for Java helper).
- Pass `delimiter` as `Char` (e.g., `'\t'`), not `String`.
- Ensure `wktColumn` is an `Int` column index.

### Prompt Snippet
```text
Given a SpatialRDD-like value `records`, write it as WKT text using:
records.saveAsWKTFile("output.csv", 0, '\t', false)

If using Java API, call:
JavaSpatialRDDHelper.saveAsWKTFile(records, "output.csv", 0, '\t', false)
```

### Common Failure Modes
- Passing delimiter as string (`"\t"`) instead of char (`'\t'`).
- Wrong argument order (e.g., swapping `wktColumn` and `filename`).
- Invalid `wktColumn` index for the output schema.
- Using a non-matching receiver form (e.g., bare `saveAsWKTFile(...)` without instance/helper).

### Fix Code Hint
```scala
// Correct Scala instance call shape
records.saveAsWKTFile("output.csv", 0, '\t', false)

// Correct Java helper call shape
JavaSpatialRDDHelper.saveAsWKTFile(records, "output.csv", 0, '\t', false)
```

## API Test: `saveFeatures`

### Signature
```scala
def saveFeatures(features: SpatialRDD, oFormat: String, outPath: String, opts: BeastOptions): Unit
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/SpatialWriter.scala:123_

_Source doc:_ Saves the given set of features to the output using the provided output format. @param features the set of features to store to the output @param oFormat the output format to use for writing @param outPath the path to write the output to @param opts user options to configure the writer

### Goal
Write a distributed vector feature dataset (`SpatialRDD`) from Spark to disk using a chosen Beast output format and writer options.

### Parameters
- `features` (`SpatialRDD`): The set of spatial features to write (in tests, passed as `RDD[IFeature]`).
- `oFormat` (`String`): Output writer format name (e.g., `"geojson"` or `"shapefile"` as shown in tests).
- `outPath` (`String`): Destination path where output files are written.
- `opts` (`BeastOptions`): Writer configuration options object.

### Input
Caller must provide:
- A valid spatial feature RDD (`SpatialRDD`).
- A supported output format string for Beast spatial writing (tests confirm `"geojson"` and `"shapefile"`).
- An output path.
- A `BeastOptions` instance.

Observed format behavior from tests:
- GeoJSON call with `.bz2` path produced compressed output files ending with `.bz2`.
- Shapefile call produced shapefile sidecar set (`.shp`, `.shx`, `.dbf`).

No additional preconditions are explicitly documented for this method in the provided sources.

### Output
Returns `Unit` — no Scala return value; the effect is materialized files written to `outPath` in the requested spatial output format.

### Valid Call Patterns
```scala
SpatialWriter.saveFeatures(features, "geojson", outputPath.getPath, new BeastOptions())
SpatialWriter.saveFeatures(features, "shapefile", outputPath.getPath, new BeastOptions())
```

### LLM Instruction Prompt
- Use the exact static call receiver form validated by tests: `SpatialWriter.saveFeatures(...)`.
- Keep argument order exactly: `(features, oFormat, outPath, opts)`.
- Pass a spatial feature RDD as `features` (tests use `RDD[IFeature]`).
- Use a real Beast vector output format string; `"geojson"` and `"shapefile"` are verified by tests.
- Provide `new BeastOptions()` (or an existing `BeastOptions`) for `opts`.
- Do not invent extra parameters or return values.

### Prompt Snippet
```text
Save this SpatialRDD to disk with Beast using:
SpatialWriter.saveFeatures(features, "<format>", outPath, new BeastOptions())
Use a supported format such as "geojson" or "shapefile", and keep the argument order unchanged.
```

### Common Failure Modes
- Passing an unsupported or misspelled `oFormat` string.
- Using a non-spatial/non-feature RDD instead of `SpatialRDD`.
- Supplying an invalid or inaccessible `outPath`.
- Expecting a returned dataset/value (method returns `Unit`; output is on disk).

### Fix Code Hint
```scala
import edu.ucr.cs.bdlab.beast.common.BeastOptions
import edu.ucr.cs.bdlab.beast.io.SpatialWriter

// features: SpatialRDD (tests use RDD[IFeature])
SpatialWriter.saveFeatures(features, "geojson", outPath, new BeastOptions())
// or
SpatialWriter.saveFeatures(features, "shapefile", outPath, new BeastOptions())
```

## API Test: `saveIndex2`

### Signature
```scala
def saveIndex2(partitionFeatures: SpatialRDD, path: String, opts: BeastOptions): Unit
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/indexing/IndexHelper.scala:541_

_Source doc:_ Saves a partitioned RDD to disk. Each partition is stored to a separate file and an additional master file that stores the partition information. @param partitionFeatures a set of partitioned features @param path the path to store the files @param opts additional options for storing the data

### Goal
Persist an already **spatially partitioned** feature RDD as an on-disk spatial index layout (one file per partition plus a master partition-info file) for scalable geospatial workflows.

### Parameters
- `partitionFeatures` (`SpatialRDD`): A set of **partitioned** spatial features to write; expected to carry a spatial partitioner (as in the tested flow using `IndexHelper.partitionFeatures2`).
- `path` (`String`): Output directory/path where index files are written.
- `opts` (`BeastOptions`): Additional write options controlling output behavior/format (e.g., test uses `"oformat" -> "wkt(0)"`).

### Input
- Input is a `SpatialRDD` (partitioned spatial features), not raw raster tiles.
- Preconditions:
  - The RDD should already be spatially partitioned (test asserts partitioner is defined and is a `SpatialPartitioner` before saving).
  - Provide a writable output path.
  - Provide valid `BeastOptions` for the target output encoding.
- Data format written depends on `opts` (authoritative example uses WKT output option via `oformat`).

### Output
Returns `Unit` — side-effect is writing index artifacts to `path`: per-partition files plus a master file containing partition metadata.

### Valid Call Patterns
```scala
IndexHelper.saveIndex2(partitionedFeatures, outPath.getPath, "oformat" -> "wkt(0)")
```

### LLM Instruction Prompt
- Only call this after creating a **spatially partitioned** `SpatialRDD`.
- Preserve receiver and argument order exactly: `IndexHelper.saveIndex2(partitionedFeatures, path, opts)`.
- Pass a real output path string and a `BeastOptions` value (the tuple form shown in tests is a valid call form in this codebase).
- Do not use this API for raster `RasterRDD` output; this is for partitioned feature/index persistence.

### Prompt Snippet
```text
Given a SpatialRDD that is already partitioned with a SpatialPartitioner, write it as an index using:
IndexHelper.saveIndex2(partitionedFeatures, outputPath, "oformat" -> "wkt(0)")
Ensure outputPath is writable.
```

### Common Failure Modes
- Calling `saveIndex2` on an unpartitioned feature RDD (missing spatial partitioner), leading to incorrect/failed index write workflow.
- Passing invalid or unsupported writer options in `opts`.
- Output path not writable or conflicting with existing filesystem state.

### Fix Code Hint
```scala
val partitionedFeatures: RDD[IFeature] = IndexHelper.partitionFeatures2(
  features,
  new GridPartitioner(new EnvelopeNDLite(2, 0.0, 0.0, 4.0, 4.0), Array(2, 2))
)

IndexHelper.saveIndex2(partitionedFeatures, outPath.getPath, "oformat" -> "wkt(0)")
```

## API Test: `saveTiles`

### Signature
```scala
def saveTiles(tiles: JavaPairRDD[java.lang.Long, IntermediateVectorTile], outPath: String, opts: BeastOptions): Unit
def saveTiles(tiles: RDD[(Long, IntermediateVectorTile)], outPath: String, opts: BeastOptions): Unit
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/MVTDataVisualizer.scala:453  (+1 more definition site/overload)_

_Source doc:_ Save an RDD of tiles to the given output @param tiles   the set of tiles to save @param outPath the path to save the tiles to

### Goal
Save a distributed set of intermediate vector tiles (MVT tile payloads keyed by tile ID) from Spark to the specified output path.

### Parameters
- `tiles` (`JavaPairRDD[java.lang.Long, IntermediateVectorTile]`): The tile dataset to write, where each record is a tile ID key and its corresponding `IntermediateVectorTile` value.
- `outPath` (`String`): Destination path where tiles are written.
- `opts` (`BeastOptions`): Beast writer/options container used by the save operation.

### Input
- You must provide tile data already prepared as either:
  - `JavaPairRDD[java.lang.Long, IntermediateVectorTile]`, or
  - `RDD[(Long, IntermediateVectorTile)]` (overload).
- `outPath` must be a writable path in the filesystem configured for your Spark job (local/HDFS/etc. depends on runtime environment; exact scheme rules are not documented here).
- `opts` must be a valid `BeastOptions` instance.
- No direct test or README example is provided for `saveTiles`; call shape below is inferred from the signature and sibling `MVTDataVisualizer` static-style usage.

### Output
Returns `Unit` — no Scala value is returned; the effect is writing the tiles to `outPath`.

### Valid Call Patterns
```scala
// Inferred from signature (no direct saveTiles test/readme example provided)
MVTDataVisualizer.saveTiles(tilesRDD, outPath, opts)

// Overload for Scala RDD[(Long, IntermediateVectorTile)]
MVTDataVisualizer.saveTiles(scalaTilesRDD, outPath, opts)
```

### LLM Instruction Prompt
- Use `MVTDataVisualizer.saveTiles(...)` with exactly three arguments in this order: `(tiles, outPath, opts)`.
- Pass either supported `tiles` type only: `JavaPairRDD[java.lang.Long, IntermediateVectorTile]` or `RDD[(Long, IntermediateVectorTile)]`.
- Do not invent extra parameters, return values, or option keys for this method.
- Treat this as a write side-effect API (`Unit`), not a transformation returning an RDD.

### Prompt Snippet
```text
Save generated intermediate vector tiles by calling:
MVTDataVisualizer.saveTiles(tiles, outPath, opts)
where tiles is either JavaPairRDD[java.lang.Long, IntermediateVectorTile] or RDD[(Long, IntermediateVectorTile)].
Do not add extra arguments.
```

### Common Failure Modes
- Passing the wrong tile RDD element type (anything other than `(Long, IntermediateVectorTile)` / Java equivalent).
- Assuming `saveTiles` returns saved data (it returns `Unit`).
- Using a non-writable or invalid `outPath` for the active Spark filesystem.
- Omitting `opts` or passing an invalid/non-`BeastOptions` object.

### Fix Code Hint
```scala
import edu.ucr.cs.bdlab.davinci.MVTDataVisualizer
// ensure tilesRDD has type RDD[(Long, IntermediateVectorTile)] (or JavaPairRDD[java.lang.Long, IntermediateVectorTile])
MVTDataVisualizer.saveTiles(tilesRDD, outPath, opts)
```

## API Test: `saveTilesCompact`

### Signature
```scala
def saveTilesCompact(tiles: JavaPairRDD[java.lang.Long, IntermediateVectorTile], outPath: String, _opts: BeastOptions): Unit
def saveTilesCompact(tiles: RDD[(Long, IntermediateVectorTile)], outPath: String, _opts: BeastOptions): Unit
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/MVTDataVisualizer.scala:495  (+1 more definition site/overload)_

_Source doc:_ A wrapper around [[saveTilesCompact()]]. Saves all the given tiles to a ZIP file. @param tiles   the set of tiles ot visualize @param outPath the path of the output ZIP file @param _opts   additional options that were used for visualization.

### Goal
Save a distributed set of pre-rendered vector tiles (`IntermediateVectorTile`) into one compact ZIP archive for multilevel MVT visualization output.

### Parameters
- `tiles` (`JavaPairRDD[java.lang.Long, IntermediateVectorTile]`): the tile dataset to write, keyed by tile ID (`Long`) and containing `IntermediateVectorTile` values (or the Scala overload `RDD[(Long, IntermediateVectorTile)]`).
- `outPath` (`String`): destination path of the output ZIP file.
- `_opts` (`BeastOptions`): visualization options associated with tile generation/saving (the docs describe these as additional options used for visualization).

### Input
Caller must provide:
- A tiles RDD produced in the expected tile form, e.g., from `MVTDataVisualizer.plotAllTiles(...)` as shown in project docs.
- A valid output ZIP path string.
- A `BeastOptions` instance.

Documented compatibility/precondition context:
- For **portable visualization archives**, examples use `threshold -> 0` in options.
- Efficient/server-backed visualization is a separate mode in Beast docs; `saveTilesCompact` is specifically documented as writing ZIP output.

### Output
Returns `Unit` — this method writes side effects: a ZIP file at `outPath` containing all provided tiles in compact form.

### Valid Call Patterns
```scala
val opts: BeastOptions = "threshold" -> 0
val features = sparkContext.shapefile("ne_10m_admin_1_states_provinces.zip")
val tiles = MVTDataVisualizer.plotAllTiles(features, levels=0 to 6, resolution=256, buffer=5, opts)
MVTDataVisualizer.saveTilesCompact(tiles, "provinces_mvt.zip", opts)

// Index the datasets
sparkContext.shapefile("ne_10m_admin_1_states_provinces.zip")
    .partitionBy(classOf[RSGrovePartitioner])
    .saveAsIndex("provinces_index", "rtree")
// Build the multilevel visualization
val tiles = MVTDataVisualizer.plotAllTiles(sparkContext.spatialFile("provinces_index"),
    levels=0 to 19, resolution=256, buffer=5, "threshold" -> "1m")
// Save the tiles
MVTDataVisualizer.saveTilesCompact(tiles, "provinces_mvt.zip", opts)
// Start the server
new BeastServer().run(new BeastOptions(), null, null, sparkContext)
```

### LLM Instruction Prompt
- Use receiver form exactly as documented: `MVTDataVisualizer.saveTilesCompact(tiles, outPath, opts)`.
- Pass exactly 3 arguments in this order: tiles RDD/pair RDD, output path string, `BeastOptions`.
- Do not invent extra parameters (compression flags, overwrite flags, etc.) for this API.
- Ensure `tiles` is already computed as `(Long, IntermediateVectorTile)` pairs (typically from `plotAllTiles`).

### Prompt Snippet
```text
Generate MVT tiles first (e.g., with MVTDataVisualizer.plotAllTiles), then call:
MVTDataVisualizer.saveTilesCompact(tiles, "output.zip", opts)
Use a BeastOptions object for visualization options; for portable all-tiles output, use threshold -> 0 as in docs.
```

### Common Failure Modes
- Passing the wrong `tiles` type (not keyed by `Long` with `IntermediateVectorTile` values).
- Calling with arguments in wrong order.
- Supplying non-`BeastOptions` as `_opts`.
- Expecting a return value; method returns `Unit` and writes files as side effect.
- Using server-oriented visualization expectations while writing portable ZIP tiles (mode mismatch in workflow).

### Fix Code Hint
```scala
val opts: BeastOptions = "threshold" -> 0
val features = sparkContext.shapefile("ne_10m_admin_1_states_provinces.zip")
val tiles = MVTDataVisualizer.plotAllTiles(features, levels=0 to 6, resolution=256, buffer=5, opts)
MVTDataVisualizer.saveTilesCompact(tiles, "provinces_mvt.zip", opts)
```

## API Test: `seek`

### Signature
```scala
override def seek(pos: Long): Unit
private def seek(pos: Long, newSource: Boolean): Boolean
```
_Source: beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/util/BufferedFSDataInputStream.scala:37  (+1 more definition site/overload)_

### Goal
Move a `BufferedFSDataInputStream` to a target byte position, reusing the current buffer when possible and reloading from the underlying stream when needed.

### Parameters
- `pos` (`Long`): The target byte offset to seek to in the input stream.
- `newSource` (`Boolean`): Internal flag indicating whether seeking should treat the source as changed/new while repositioning (private overload behavior control).

### Input
A readable underlying Hadoop FS input stream wrapped by `BufferedFSDataInputStream`, with a valid target byte position (`pos`) within the stream/file range expected by the caller.  
From tests, call pattern is on stream instances like `fsStream.seek(pos)` and `bufStream.seek(pos)`; `newSource` is private/internal and not called directly from user code.

### Output
Returns `Boolean` — for the private overload, indicates whether the seek operation was handled successfully (including buffer-aware seek and possible disk seek + buffer reload as described in source doc).

### Valid Call Patterns
```scala
val seekPos = if (fileLength - fsStream.getPos < 16 || random.nextBoolean()) {
  val pos = random.nextLong().abs % (fileLength - 16)
  fsStream.seek(pos)
  bufStream.seek(pos)
} else {
  fsStream.getPos
}
```

### LLM Instruction Prompt
- Use instance-style calls exactly as in tested code: `bufStream.seek(pos)` (and `fsStream.seek(pos)` for baseline stream).
- Do **not** call `seek(pos, newSource)` directly; it is private.
- Provide `pos` as a `Long` byte offset computed from current file-length bounds to avoid invalid seeks.

### Prompt Snippet
```text
Given a BufferedFSDataInputStream named bufStream, seek using bufStream.seek(pos) where pos is a Long byte offset within file bounds. Do not call the private overload seek(pos, newSource).
```

### Common Failure Modes
- Calling the private overload `seek(pos, newSource)` from external code (not accessible).
- Passing an invalid/out-of-range `pos` (can cause seek/read errors in subsequent operations).
- Mixing position logic between wrapped and unwrapped streams without re-checking `getPos`, causing assertion mismatches in validation code.

### Fix Code Hint
```scala
val pos: Long = random.nextLong().abs % (fileLength - 16)
fsStream.seek(pos)
bufStream.seek(pos)
assertResult(fsStream.getPos)(bufStream.getPos)
```

## API Test: `selectFiles`

### Signature
```scala
def selectFiles(fileSystem: FileSystem, dir: String, range: Geometry): Array[String]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterFileRDD.scala:233_

_Source doc:_ Selects all the raster files that could potentially overlap the given query range from a directory of files. If that directory contains an index file, i.e., "_index.csv", then this index is used to prune files that are not relevant. If no index file is there, then all files are returned. @param fileSystem the file system at which the raster files exist @param dir the directory that contains the raster files @param range the query range to limit the files @return the list of files that potentially overlap the given query range

### Goal
Select candidate raster files in a directory that may overlap a query geometry, using `_index.csv` for pruning when available.

### Parameters
- `fileSystem` (`FileSystem`): Hadoop `FileSystem` instance pointing to where the raster directory exists (e.g., obtained from Spark Hadoop configuration).
- `dir` (`String`): Path to the directory that contains raster files (and optionally `_index.csv`).
- `range` (`Geometry`): Query geometry used to limit candidate files to those that potentially overlap it.

### Input
A raster-files directory path and a query `Geometry` must be provided.  
Behavior depends on index availability in that directory:

- If `dir/_index.csv` exists, it is used to prune non-relevant files.
- If no `_index.csv` exists, all files in the directory are returned.

Practical precondition from tested usage: `fileSystem` should match the filesystem backing `dir` (created via `FileSystem.get(sparkContext.hadoopConfiguration)` in Spark workflows).

### Output
Returns `Array[String]` — a list of file paths (as strings) for raster files that **potentially** overlap the given `range` (candidate set, not guaranteed exact intersection).

### Valid Call Patterns
```scala
val matchingFiles = RasterFileRDD.selectFiles(FileSystem.get(sparkContext.hadoopConfiguration), dir.toString,
  geometryFactory.toGeometry(new Envelope(-100, -99, 27, 28)))
```

### LLM Instruction Prompt
- Use the exact receiver form `RasterFileRDD.selectFiles(...)`.
- Pass arguments in this exact order: `(fileSystem, dir, range)`.
- Provide `range` as a JTS `Geometry` (e.g., from `GeometryFactory.toGeometry(new Envelope(...))`).
- Do not invent extra options/parameters (no filters, no format flags).
- If `_index.csv` is missing, expect broad results (all files), not an error.

### Prompt Snippet
```text
Use RasterFileRDD.selectFiles(FileSystem.get(sparkContext.hadoopConfiguration), dirPath, queryGeometry).
queryGeometry must be a JTS Geometry. The method returns Array[String] candidate raster file paths.
If dirPath contains _index.csv, file pruning is applied; otherwise all files are returned.
```

### Common Failure Modes
- Passing a non-`Geometry` object for `range`.
- Using a `FileSystem` that does not correspond to `dir`’s actual storage backend.
- Assuming output contains only exact overlaps; API guarantees only “potentially overlap”.
- Expecting pruning without creating `_index.csv` first.

### Fix Code Hint
```scala
// Optional: build index first to enable pruning
RasterFileRDD.buildIndex(sparkContext, dir.toString, new File(dir, "_index.csv").toString)

val fs = FileSystem.get(sparkContext.hadoopConfiguration)
val geometryFactory = new GeometryFactory(new PrecisionModel(PrecisionModel.FLOATING_SINGLE), 4326)
val queryRange = geometryFactory.toGeometry(new Envelope(-100, -99, 27, 28))

val matchingFiles: Array[String] = RasterFileRDD.selectFiles(fs, dir.toString, queryRange)
```

## API Test: `set`

### Signature
```scala
def set(key: String, value: Any): BeastOptions
```
_Source: beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/common/BeastOptions.scala:83_

_Source doc:_ Set a key to any value by conerting it to string @param key key name @param value value @return

### Goal
Set one configuration option in a `BeastOptions` object (key + value), where the value is converted to string for Beast/RDPro/Spark operation options.

### Parameters
- `key` (`String`): Option name to set (for example, format/reader/plot options such as `"iformat"`, `"skipheader"`, `"separator"`, `"stroke"`, `"fill"`, `"oformat"`).
- `value` (`Any`): Option value for that key; this method accepts any Scala/Java value type and stores it by converting it to string.

### Input
A mutable call context with an existing `BeastOptions` instance (typically `new BeastOptions()`), plus:
- a non-empty option key string,
- a value object compatible with string conversion.

`set` itself is not tied to raster/vector file formats directly; it configures downstream Beast operations (e.g., readers, summaries, plotting).  
Project compatibility/precondition notes from broader workflows still apply to the operation that consumes these options (e.g., typed `sc.geoTiff[T]` matching pixel type, raster metadata alignment for overlay), but those are enforced by those APIs, not by `set`.

### Output
Returns `BeastOptions` — the updated options object, enabling fluent chaining of multiple `.set(...)` calls.

### Valid Call Patterns
```scala
val opts = new BeastOptions().set("iformat", "wkt(Geometry)")
  .set("skipheader", true)
  .set("separator", "\t")
```

```scala
val opts = new BeastOptions().set("iformat", "wkt(Geometry)")
    .set("skipheader", true)
    .set("separator", "\t")
    .set("oformat", "invalid")
```

```scala
new BeastOptions().set("stroke", "blue").set("fill", "#9999e6")
```

### LLM Instruction Prompt
- Call as an instance method on `BeastOptions` (e.g., `new BeastOptions().set(...)`), not as a standalone function.
- Pass exactly two arguments in order: `(key: String, value: Any)`.
- Use real option keys expected by the downstream Beast API being called.
- Chain `.set(...)` calls when multiple options are needed.
- Do not invent extra parameters or alternate signatures for `set`.

### Prompt Snippet
```text
Create a Beast options object with fluent chaining:
new BeastOptions()
  .set("iformat", "wkt(Geometry)")
  .set("skipheader", true)
  .set("separator", "\t")
Use set(key: String, value: Any) exactly.
```

### Common Failure Modes
- Calling `set(...)` without a `BeastOptions` receiver (won’t match intended call form in examples/tests).
- Misspelled option key names (option silently not applied or ignored by downstream operation).
- Assuming `set` validates semantic correctness of options; it only stores key/value (as string), while errors may appear later in the consuming API.
- Using options inconsistent with the downstream workflow (e.g., wrong `iformat` for input data).

### Fix Code Hint
```scala
val opts = new BeastOptions()
  .set("iformat", "wkt(Geometry)")
  .set("skipheader", true)
  .set("separator", "\t")
```

## API Test: `setBoolean`

### Signature
```scala
def setBoolean(key: String, value: Boolean): BeastOptions
```
_Source: beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/common/BeastOptions.scala:141_

_Source doc:_ Set key to a boolean value @param key @param value @return

### Goal
Set a boolean configuration option in a `BeastOptions` object used by Beast/RDPro/Spark workflows.

### Parameters
- `key` (`String`): Configuration option name to set (for example, a Hadoop/Beast option key such as `"fs.file.impl.disable.cache"` as shown in tests).
- `value` (`Boolean`): Boolean value to assign to `key` (`true` or `false`).

### Input
A valid options/configuration context where boolean flags are expected, specifically:
- a string key (`key`)
- a boolean value (`value`)

Grounded call form is shown in tests on Hadoop configuration (`conf.setBoolean(...)`).  
No additional file-format inputs are required by `setBoolean` itself.

### Output
Returns `BeastOptions` — the updated options object after assigning `key` to the provided boolean value, enabling chained option-setting patterns.

### Valid Call Patterns
```scala
conf.setBoolean("fs.file.impl.disable.cache", true)
```

### LLM Instruction Prompt
- Use the instance-method form with an options/config receiver (do not emit bare `setBoolean(...)`).
- Pass exactly two arguments in order: `(key: String, value: Boolean)`.
- Use boolean literals `true`/`false` for the second argument.
- Do not invent extra parameters.

### Prompt Snippet
```text
Given a Beast/Hadoop-style configuration object, set a boolean flag using:
receiver.setBoolean("some.key", trueOrFalse)
Example grounded in tests: conf.setBoolean("fs.file.impl.disable.cache", true)
```

### Common Failure Modes
- Calling without a receiver (e.g., `setBoolean("k", true)`) in contexts where only instance methods exist.
- Passing non-boolean values for `value` (e.g., `"true"` string instead of `true`).
- Using an incorrect/misspelled key string, which sets the wrong option.

### Fix Code Hint
```scala
// Correct: instance receiver + (String, Boolean)
conf.setBoolean("fs.file.impl.disable.cache", true)
```

## API Test: `setLong`

### Signature
```scala
def setLong(key: String, value: Long): BeastOptions
```
_Source: beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/common/BeastOptions.scala:122_

_Source doc:_ Set a key to a long value @param key @param value @return

### Goal
Set a configuration option in a `BeastOptions` object using a 64-bit integer (`Long`) value so Beast/RDPro operations read that option as a numeric setting.

### Parameters
- `key` (`String`): Configuration option name to set (for example, an option like `"threshold"` in plotting options, or constants such as `SpatialFilePartitioner.MaxSplitSize` / `SpatialFileRDD.MaxSplitSize` in Hadoop/Spark configuration usage shown by tests).
- `value` (`Long`): 64-bit integer value to assign to `key` (for example `0` or `1024`).

### Input
A valid `String` key and a `Long` value, called on a `BeastOptions` instance (or on Hadoop configuration via its own `setLong` API, as shown in tests).  
No raster file format is directly consumed by `setLong` itself; it only prepares numeric options consumed by downstream Beast/Spark operations.

### Output
Returns `BeastOptions` — the updated options object after setting the given key to the given long value, enabling fluent chaining of additional option setters.

### Valid Call Patterns
```scala
new BeastOptions().set("stroke", "blue").set("fill", "#9999E6").setLong("threshold", 0)
```

```scala
conf.setLong(SpatialFilePartitioner.MaxSplitSize, 500)
```

```scala
sparkContext.hadoopConfiguration.setLong(SpatialFileRDD.MaxSplitSize, 1024)
```

### LLM Instruction Prompt
- Call `setLong` on an existing receiver exactly (for Beast options: `new BeastOptions().setLong(...)`; for Hadoop config: `conf.setLong(...)`).
- Pass exactly two arguments in order: `(key: String, value: Long)`.
- Use this method only for integer-like numeric options that should be stored as `Long`.
- Do not invent extra parameters, overloads, or alternate return types.

### Prompt Snippet
```text
Create a BeastOptions object and set a long-valued option using:
new BeastOptions().setLong("threshold", 0)
Keep argument order as (key, value), with key as String and value as Long.
```

### Common Failure Modes
- Using a non-`Long` numeric literal where strict typing is required.
- Calling `setLong` without a receiver (bare `setLong(...)`), which may not compile.
- Passing an option key that downstream code does not recognize (the setter succeeds, but the option may have no effect).

### Fix Code Hint
```scala
val opts = new BeastOptions()
  .set("stroke", "blue")
  .set("fill", "#9999E6")
  .setLong("threshold", 0L)
```

## API Test: `setPixelValue`

### Signature
```scala
def setPixelValue(i: Int, j:Int, value: T): Unit
def setPixelValue(i: Int, j: Int, value: T): Unit
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/MemoryTile.scala:147  (+1 more definition site/overload)_

_Source doc:_ Sets the value of the given pixel @param i the column position of the pixel @param j the row position of the pixel @param value the value to set at the given pixel

### Goal
Set (write) a pixel value at a specific column/row location inside a raster tile (e.g., a `MemoryTile`) used in RDPro/Raptor raster processing.

### Parameters
- `i` (`Int`): Column position (x index) of the target pixel.
- `j` (`Int`): Row position (y index) of the target pixel.
- `value` (`T`): Pixel value to write at `(i, j)`; must match the tile’s pixel type `T` (e.g., `Float`, `Array[Float]` in the test-suite examples).

### Input
Call this on a tile instance that provides `setPixelValue` (authoritative examples use `MemoryTile[T]` receivers such as `tile1` / `tile2`).

Preconditions from verified usage and project type rules:
- `i` and `j` are pixel indices in the tile/grid coordinate space (source doc: column/row position).
- `value` type must be compatible with the tile generic type `T` (e.g., `MemoryTile[Float]` gets `Float`; `MemoryTile[Array[Float]]` gets `Array[Float]`).
- For multi-band tiles represented as arrays (e.g., `Array[Float]`), provide the expected band structure consistently per pixel. Exact band-count validation behavior is not documented here.

No file format input is required by this method itself; it mutates in-memory tile content.

### Output
Returns `Unit` — no value is returned; the effect is an in-place update of the tile pixel at `(i, j)`.

### Valid Call Patterns
```scala
val tile1 = new MemoryTile[Float](0, metadata, RasterFeature.create(Array("fileName"), Array("testFile.tif")))
tile1.setPixelValue(0, 0, 0.5f)
tile1.setPixelValue(9, 9, 4.00f)

val tile2 = new MemoryTile[Array[Float]](1, metadata, RasterFeature.create(Array("fileName"),Array("testFile.tif")))
tile2.setPixelValue(10, 0, Array(5.0f, 10.0f))
tile2.setPixelValue(10, 9, Array(5.0f, 20.0f))
```

### LLM Instruction Prompt
- Use instance-call form exactly: `tile.setPixelValue(i, j, value)`.
- Keep argument order exactly `(i, j, value)` where `i` is column and `j` is row.
- Ensure `value` matches the tile’s generic pixel type `T`; do not mix scalar and array pixel types.
- Do not invent extra parameters or return handling; this method returns `Unit`.

### Prompt Snippet
```text
Given a tile object (e.g., MemoryTile[T]), write pixel values using:
tile.setPixelValue(i, j, value)
where i=column index, j=row index, and value has type T.
Use exact argument order and do not expect a return value.
```

### Common Failure Modes
- Swapping row/column semantics (`i` vs `j`), causing writes to wrong pixel locations.
- Passing a value with the wrong type for `T` (e.g., `Float` into `MemoryTile[Array[Float]]`).
- Assuming the method returns a modified tile; it returns `Unit` and mutates in place.
- Using a non-instance/bare call shape (`setPixelValue(...)`) instead of `tile.setPixelValue(...)`.

### Fix Code Hint
```scala
// Correct: receiver is the tile instance, argument order is (column, row, value)
val tile = new MemoryTile[Float](0, metadata, RasterFeature.create(Array("fileName"), Array("testFile.tif")))
tile.setPixelValue(1, 0, 0.25f)

// Multi-band example: value type matches T = Array[Float]
val mbTile = new MemoryTile[Array[Float]](1, metadata, RasterFeature.create(Array("fileName"), Array("testFile.tif")))
mbTile.setPixelValue(1, 0, Array(0.25f, 0.4f))
```

## API Test: `setup`

### Signature
```scala
override def setup(opts: BeastOptions): Unit
override def setup(ss: SparkSession, opts: BeastOptions): Unit
override def setup(sc: SparkContext, opts: BeastOptions): Unit
```
_Source: beast/dataExplorer/src/main/scala/edu/ucr/cs/bdlab/beast/dataExplorer/DataExplorerServer.scala:91  (+2 more definition site/overload)_

### Goal
Initialize a Beast server/handler component with Spark runtime context and Beast configuration options before serving geospatial (including RDPro/Raptor-related) operations.

### Parameters
- `ss` (`SparkSession`): Spark SQL/session entry point used by the `setup(ss, opts)` overload.
- `opts` (`BeastOptions`): Beast configuration/options object used to configure initialization.
- `sc` (`SparkContext`): Spark core context used by the `setup(sc, opts)` overload.

### Input
Caller must provide a valid `BeastOptions` instance, and for context-based overloads also provide a live Spark runtime object (`SparkContext` or `SparkSession`) matching the selected overload.

From documented usage, this is typically called in server/web-handler initialization code and may delegate to `super.setup(...)` first.

No raster file-format input is passed directly to `setup`; raster/vector format constraints (GeoTIFF/HDF/etc.) apply to later processing APIs, not this method call itself.

### Output
Returns `Unit` — it performs initialization side effects (e.g., storing context/config in the handler/server) and does not return a data object.

### Valid Call Patterns
```scala
plotter.setup(new BeastOptions())
```

```scala
override def setup(sc: SparkContext, opts: BeastOptions): Unit = {
  super.setup(sc, opts)
  this.sc = sc
  // Additional initialization steps
}
```

### LLM Instruction Prompt
- Call `setup` as an instance method (`value.setup(...)`), not as a bare function.
- Match one of the documented overloads exactly:
  - `setup(opts: BeastOptions)`
  - `setup(ss: SparkSession, opts: BeastOptions)`
  - `setup(sc: SparkContext, opts: BeastOptions)`
- Do not invent extra arguments or return handling (`setup` returns `Unit`).
- In subclass overrides, preserve the documented pattern of calling `super.setup(sc, opts)` when extending base initialization.

### Prompt Snippet
```text
Initialize the handler before running requests by calling setup on the instance.
Use an existing BeastOptions object and, if needed, a SparkContext or SparkSession
matching one of the overloads. Do not expect a return value.
```

### Common Failure Modes
- Calling `setup` without an instance receiver (bare `setup(...)`) in code where no such function is in scope.
- Passing wrong argument shape/order (e.g., swapping `opts` and Spark context/session).
- Expecting a return object from `setup` instead of treating it as side-effect initialization.
- In subclass code, skipping `super.setup(sc, opts)` and then missing base-class initialization.

### Fix Code Hint
```scala
import edu.ucr.cs.bdlab.beast.common.BeastOptions
import org.apache.spark.SparkContext

class CustomServer extends AbstractWebHandler {
  var sc: SparkContext = _

  override def setup(sc: SparkContext, opts: BeastOptions): Unit = {
    super.setup(sc, opts)
    this.sc = sc
  }
}
```

## API Test: `shapefile`

### Signature
```scala
def shapefile(filename: String) : SpatialRDD
def shapefile(filename: String) : JavaSpatialRDD
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/ReadWriteMixin.scala:76  (+1 more definition site/overload)_

_Source doc:_ Reads features from an Esri Shapefile(c) @param filename the name of the .shp file, a compressed ZIP file that contains shapefiles, or a directory that contains shapefiles or ZIP files. @return an RDD of features

### Goal
Load vector features from Esri Shapefile input into Beast/Spark as a distributed `SpatialRDD` for downstream spatial analytics (e.g., summary, partitioning, join, export).

### Parameters
- `filename` (`String`): Path/name of the input shapefile source: a `.shp` file, a compressed `.zip` containing shapefiles, or a directory containing shapefiles or ZIP files.

### Input
`shapefile` expects Esri Shapefile-based vector input provided via `filename` as one of:
- a `.shp` file,
- a `.zip` file that contains shapefile content,
- or a directory containing shapefiles or ZIP files.

Preconditions from the provided API facts/context:
- The receiver call form should be a Spark context extension style (e.g., `sparkContext.shapefile(...)` / `sc.shapefile(...)`) as shown in project examples.
- No additional typed parameter is used here (unlike `geoTiff[T]`); this API is not generic in pixel type.

### Output
Returns `SpatialRDD` — an RDD of spatial features read from the shapefile input, suitable for Beast vector operations (e.g., `summary`, `spatialPartition`, `rangeQuery`, `saveAsGeoJSON`, plotting).

### Valid Call Patterns
```scala
// Scala
val records = sparkContext.shapefile("input.zip")
// Or
val records = sparkContext.shapefile("input.shp")

val buildings = sc.shapefile("MSBuildings_data_index.zip")
println(buildings.summary)
buildings.saveAsGeoJSON("MSBuildings.geojson")
buildings.plotImage(1000, 1000, "MSBuildings.png")
```

### LLM Instruction Prompt
- Use the receiver-qualified form exactly as documented: `sparkContext.shapefile(...)` or `sc.shapefile(...)`.
- Pass exactly one argument: `filename: String`.
- Only supply supported inputs: `.shp`, `.zip` containing shapefiles, or a directory containing shapefiles/ZIPs.
- Do not invent extra options/parameters for this method.
- Treat output as `SpatialRDD` (or `JavaSpatialRDD` for the overload), i.e., an RDD of features.

### Prompt Snippet
```text
Load shapefile features with `sc.shapefile(filename)` (single String argument only). 
Use a path to `.shp`, `.zip` (containing shapefile), or a directory of shapefiles/ZIPs. 
Store the result as `SpatialRDD` and then run vector ops such as `summary`, `spatialPartition`, `rangeQuery`, or `saveAsGeoJSON`.
```

### Common Failure Modes
- Passing an unsupported input path/type (not a `.shp`, shapefile ZIP, or directory containing them).
- Calling `shapefile(...)` without a Spark context receiver (bare call usually will not compile in normal usage).
- Assuming raster-style typed loading (`[T]`) applies here; it does not for `shapefile`.

### Fix Code Hint
```scala
import edu.ucr.cs.bdlab.beast._

val features: SpatialRDD = sparkContext.shapefile("input.zip")
// or
val features2: SpatialRDD = sc.shapefile("input.shp")

println(features.summary)
```

## API Test: `sierpinski`

### Signature
```scala
def sierpinski(cardinality: Long): JavaSpatialRDD
def sierpinski(cardinality: Long): SpatialRDD
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/generator/JavaSpatialGeneratorBuilder.scala:127  (+1 more definition site/overload)_

_Source doc:_ Generate data from the Sierpinski distribution @param cardinality the number of records to generate @return the RDD that contains the generated data

### Goal
Generate a distributed spatial dataset following a Sierpinski distribution, with a caller-specified number of generated records.

### Parameters
- `cardinality` (`Long`): the number of records to generate.

### Input
This method does not take file-based raster/vector input formats directly.  
You provide only:
- a `Long` cardinality value, and
- a valid generator receiver (as shown below) in a Spark/Beast context.

Preconditions from the available sources:
- Call it as an instance method on a spatial generator builder receiver (`sc.generateSpatialData` in the README example).
- Use a `Long` argument for record count.

### Output
Returns `JavaSpatialRDD` — an RDD-backed generated spatial dataset containing records sampled from the Sierpinski distribution.  
(Scala overload returns `SpatialRDD` with the same documented meaning: “the RDD that contains the generated data”.)

### Valid Call Patterns
```scala
sc.generateSpatialData
  .sierpinski(1000)
  .plotImage(300, 300, "sierpinski.png",
    opts = Seq(GeometricPlotter.PointSize -> 0))
```

### LLM Instruction Prompt
- Call `sierpinski` as an instance method on the documented generator receiver form: `sc.generateSpatialData.sierpinski(...)`.
- Pass exactly one argument: `cardinality: Long`.
- Do not add extra parameters or options to `sierpinski`.
- Treat the result as a spatial RDD (Scala: `SpatialRDD`, Java overload: `JavaSpatialRDD`).

### Prompt Snippet
```text
Use Beast’s generator receiver form and call:
sc.generateSpatialData.sierpinski(<cardinalityLong>)
where <cardinalityLong> is the number of records to generate.
Do not invent extra arguments.
```

### Common Failure Modes
- Calling `sierpinski` without a generator receiver (e.g., bare `sierpinski(...)`) so the code does not resolve.
- Passing a non-`Long` cardinality type.
- Assuming file input/output parameters exist on `sierpinski` itself (they are not part of this API).

### Fix Code Hint
```scala
// Correct receiver + single Long argument
val sierpinskiRDD: SpatialRDD =
  sc.generateSpatialData.sierpinski(1000L)
```

## API Test: `simplifyGeometry`

### Signature
```scala
private[davinci] def simplifyGeometry(geometry: Geometry): LiteGeometry
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/IntermediateVectorTile.scala:207_

_Source doc:_ Takes a geometry that is already projected to the image space of this tile and returns a simplified lite geometry that satisfies the following: - If the geometry does not overlap with the tile boundaries, null is returned - Coordinates are snapped to the nearest integer - Parts of the geometry that are outside the tile boundaries can be simplified without affecting the portion that is within the tile boundaries. - If there are consecutive coordinates that snap to the same pixel, only one can be kept @param geometry the input geometry @return the simplified geometry or null if empty

### Goal
Simplify a tile-space JTS geometry into RDPro/DaVinci `LiteGeometry` form for tile rendering/processing, with clipping-aware simplification and pixel snapping.

### Parameters
- `geometry` (`Geometry`): the input JTS geometry to simplify, expected to already be projected into the image space of the current tile.

### Input
The caller provides:
- A `Geometry` object (JTS type).
- The call is made on an `IntermediateVectorTile` instance (per test usage).

Preconditions (from source doc + tests):
- Geometry must already be in this tile’s image coordinate space.
- If geometry does not overlap tile boundaries/extent, result is `null`.
- Coordinates are snapped to nearest integer pixel.
- Consecutive coordinates snapping to the same pixel may be collapsed.
- Portions outside tile boundaries may be simplified as long as in-tile portion is preserved.

### Output
Returns `LiteGeometry` — a simplified lightweight geometry representation (e.g., `LitePoint`, `LiteLineString` in tests) aligned to tile pixel coordinates; returns `null` if simplified result is empty/non-overlapping tile.

### Valid Call Patterns
```scala
val interTile = new IntermediateVectorTile(10, 0)
val point = GeometryReader.DefaultGeometryFactory.createPoint(new Coordinate(5, 5))
val simplifiedPoint = interTile.simplifyGeometry(point)
```

```scala
val interTile = new IntermediateVectorTile(10, 0)
val line = GeometryReader.DefaultGeometryFactory.createLineString(Array(
  new Coordinate(5, 5), new Coordinate(-5, 5), new Coordinate(-5, 6), new Coordinate(-5, 7),
  new Coordinate(-5, 15), new Coordinate(5, 8),
))
val simplifiedLine = interTile.simplifyGeometry(line)
```

### LLM Instruction Prompt
- Call using the instance form shown in tests: `interTile.simplifyGeometry(geometry)`.
- Pass a `Geometry` already projected to the tile image space.
- Handle possible `null` return (non-overlap/empty after simplification).
- Do not invent extra parameters or overloads; only one parameter is supported.

### Prompt Snippet
```text
Given an existing IntermediateVectorTile `interTile` and a JTS `Geometry` already in tile image space, call:
`val simplified = interTile.simplifyGeometry(geometry)`
Then check for null before using/casting the returned LiteGeometry.
```

### Common Failure Modes
- Passing geometry not projected to tile image space, causing incorrect simplification.
- Assuming output is never `null`; tests show `null` for out-of-tile geometries.
- Expecting original floating coordinates to be preserved (they are snapped to integer pixels).
- Assuming every input vertex is retained; consecutive snapped duplicates may be removed.

### Fix Code Hint
```scala
val interTile = new IntermediateVectorTile(10, 0)
val geometry: Geometry = GeometryReader.DefaultGeometryFactory.createLineString(Array(
  new Coordinate(5, 5), new Coordinate(-5, 5), new Coordinate(-5, 6)
))

val simplified: LiteGeometry = interTile.simplifyGeometry(geometry)
if (simplified != null) {
  // safe to use simplified geometry
} else {
  // no overlap / empty after simplification
}
```

## API Test: `size`

### Signature
```scala
def size: Long
override def size: Long
override def size: Int
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/SpatialPartition.scala:41  (+2 more definition site/overload)_

_Source doc:_ Size in bytes

### Goal
Return the size of the target object in bytes, as used by Beast internal spatial/raster processing components.

### Parameters
_None._

### Input
A receiver object that defines `size` (for example, the test-proven receivers `results` and `joinResults`).

No file path or format is passed directly to this method.

Preconditions:
- `size` is parameterless; call it only on an instance that already exists.
- The exact semantic unit is bytes per the source doc (“Size in bytes”), but one shown overload is `Int`; use the declared type on the concrete receiver.

### Output
Returns `Long` — the size value (documented as size in bytes).  
In some concrete implementations, an `Int` overload exists, so the static type may be `Int` depending on receiver type.

### Valid Call Patterns
```scala
assertResult(1)(results.size)
assert(joinResults.size == 4)
```

### LLM Instruction Prompt
- Use instance form `value.size` (no arguments).
- Do not invent arguments (no `size(...)` with params).
- Preserve receiver-qualified call shape from real usage (e.g., `results.size`, `joinResults.size`).
- Treat result as numeric size; when needed, widen `Int` to `Long` safely rather than assuming only one overload exists.

### Prompt Snippet
```text
Call `size` as a parameterless instance member on an existing object (e.g., `results.size`).
Do not pass any arguments.
Interpret the returned number as size in bytes per source doc; handle either Int or Long based on receiver type.
```

### Common Failure Modes
- Calling `size()` with arguments or using a nonexistent static form.
- Assuming every receiver returns `Long`; some implementations expose `Int`.
- Calling `size` before the receiver is created/populated.

### Fix Code Hint
```scala
val n: Long = results.size.toLong
if (joinResults.size > 0) {
  // proceed
}
```

## API Test: `skipDuplicateAvoidance`

### Signature
```scala
private[beast] def skipDuplicateAvoidance(rdd: RDD[_]): Unit
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/SpatialFileRDD.scala:535_

_Source doc:_ If the given RDD is based on a SpatialFileRDD, it causes it to skip duplicate avoidance. @param rdd the rdd to skip duplicate avoidance for

### Goal
Disable duplicate-avoidance behavior for an RDD that is backed by `SpatialFileRDD`, so repeated records are preserved during reading.

### Parameters
- `rdd` (`RDD[_]`): The target Spark RDD to mark for skipping duplicate avoidance; this is intended for RDDs based on `SpatialFileRDD`.

### Input
A Spark `RDD[_]`, specifically expected to be based on `SpatialFileRDD` for the documented effect to apply.  
From the verified test usage, this is used on data read via `SpatialFileRDD` (example input format in test: `"envelopek(2)"` with CSV field separator option).  
No additional file-format constraints are defined by this method itself beyond the upstream `SpatialFileRDD` read configuration.

### Output
Returns `Unit` — it performs a side effect (configuring behavior on the passed RDD) and does not return a data value.

### Valid Call Patterns
```scala
val features = new SpatialFileRDD(sparkContext, indexPath.getPath,
  Seq(SpatialFileRDD.InputFormat -> "envelopek(2)", CSVFeatureReader.FieldSeparator -> ','))
SpatialFileRDD.skipDuplicateAvoidance(features)
```

### LLM Instruction Prompt
- Call with the exact qualified receiver form verified by tests: `SpatialFileRDD.skipDuplicateAvoidance(features)`.
- Pass an `RDD[_]` that is based on `SpatialFileRDD`; otherwise, the documented effect (“skip duplicate avoidance”) is not guaranteed.
- Do not invent return handling; this method returns `Unit` and is used for side effects.
- Keep this call before actions (e.g., `count`) that should observe duplicates.

### Prompt Snippet
```text
Given an RDD created from SpatialFileRDD, call:
SpatialFileRDD.skipDuplicateAvoidance(rdd)
Then run the action (such as count) that should keep repeated records. Do not assign a return value; it returns Unit.
```

### Common Failure Modes
- Calling it on an RDD not based on `SpatialFileRDD` and expecting duplicate-avoidance behavior to change.
- Expecting a transformed/new RDD as output (it returns `Unit`).
- Invoking it after already materializing results where duplicate handling has already taken effect.

### Fix Code Hint
```scala
val features = new SpatialFileRDD(sparkContext, indexPath.getPath,
  Seq(SpatialFileRDD.InputFormat -> "envelopek(2)", CSVFeatureReader.FieldSeparator -> ','))

// Apply before action
SpatialFileRDD.skipDuplicateAvoidance(features)

val n = features.count()
println(n)
```

## API Test: `slidingWindow`

### Signature
```scala
def slidingWindow[T: ClassTag, U: ClassTag](raster: RasterRDD[T], w: Int, f: (Array[T], Array[Boolean]) => U): RasterRDD[U]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsFocal.scala:711_

_Source doc:_ Performs a sliding window calculation for a window of size (2w + 1) &times; (2w + 1) given an integer value w. The user-defined window calculation function takes all values in the window ordered in row-major order. Additionally, a Boolean array of the same size is passed to indicate which values are defined and which are not. The Boolean array is useful for two scenarios. 1. When the window is near the edge of the raster, there must be some undefined values outside the raster. 2. Some pixel values in raster might be undefined, e.g., due to cloud coverage. *Note*: This function will only work correctly if all input tiles have the same raster metadata. @param raster the input raster to process @param w the radius of the square window. The window size will be (2w + 1) &times; (2w + 1) @param f the function to perform the calculation. @tparam T the type of values in the input raster @tparam U the type of output values (the result of the user-defined function). @return a new raster with the same dimensions as the input after applying the window function.

### Goal
Apply a focal (moving-window) computation over a `RasterRDD`, producing one output pixel per input pixel using a user function over each local neighborhood.

### Parameters
- `raster` (`RasterRDD[T]`): Input raster dataset to process (typed pixel values).
- `w` (`Int`): Radius of the square window; effective window size is `(2w + 1) × (2w + 1)`.
- `f` (`(Array[T], Array[Boolean]) => U`): User-defined window function; receives window pixel values in row-major order plus a same-length `Boolean` mask indicating which entries are defined.

### Input
- A `RasterRDD[T]` (commonly loaded from GeoTIFF/HDF in RDPro workflows) with a correct type parameter `T` for underlying pixel type.
- Precondition from API doc: this works correctly only if all input tiles have the same raster metadata.
- Your function `f` must handle undefined entries using the `defined` Boolean array (undefined can occur at raster edges or from undefined source pixels, e.g., cloud-masked areas).

### Output
Returns `RasterRDD[U]` — a new raster with the same dimensions as the input raster, where each pixel is replaced by the result of applying `f` to its local window.

### Valid Call Patterns
```scala
val smoothedRaster: RasterRDD[Double] = RasterOperationsFocal.slidingWindow(raster, 1, (values: Array[Int], defined) => {
  var sum: Int = 0
  var count: Int = 0
  for (i <- values.indices; if defined(i)) {
    sum += values(i)
    count += 1
  }
  sum.toDouble / count
})
```

### LLM Instruction Prompt
- Use the call form `RasterOperationsFocal.slidingWindow(raster, w, f)` (verified from test suite).
- Keep argument order exactly: `(raster, w, f)`.
- Ensure `f` consumes both arrays and checks `defined(i)` before using `values(i)`.
- Do not assume all window cells are valid at edges or for undefined pixels.
- Ensure raster tiles are metadata-compatible before calling.

### Prompt Snippet
```text
Use RasterOperationsFocal.slidingWindow(raster, w, f) to run a focal operation.
Set window radius w so size = (2w+1)x(2w+1).
In f: values are row-major; defined marks valid entries.
Always guard calculations with defined(i), and return one U per center pixel.
Require consistent raster metadata across all input tiles.
```

### Common Failure Modes
- Ignoring `defined` and aggregating all `values`, causing wrong results near raster borders or where source pixels are undefined.
- Using a `RasterRDD` whose tiles do not share the same raster metadata (documented correctness precondition).
- Choosing an input type `T` that does not match actual raster pixel type at load time (typed loading must match data type in RDPro workflows).

### Fix Code Hint
```scala
val out: RasterRDD[Double] = RasterOperationsFocal.slidingWindow(raster, 1, (values: Array[Int], defined: Array[Boolean]) => {
  var sum = 0.0
  var count = 0
  var i = 0
  while (i < values.length) {
    if (defined(i)) {
      sum += values(i)
      count += 1
    }
    i += 1
  }
  if (count == 0) Double.NaN else sum / count
})
```

## API Test: `sparkContext`

### Signature
```scala
def sparkContext: SparkContext
```
_Source: beast/commontest/src/main/scala/org/apache/spark/test/ScalaSparkTest.scala:38_

### Goal
Provide the active Spark execution context (`SparkContext`) used to run Beast/RDPro distributed operations.

### Parameters
_None._

### Input
This method takes no parameters and does not read raster/vector files directly.  
Precondition: it must be called from a scope/object where `sparkContext` is defined (as in the Scala test style shown), and Spark must be initialized by that test/application harness.

### Output
Returns `SparkContext` — the live Apache Spark driver-side context object used to submit distributed jobs (RDD operations, Beast operations such as summaries, raster/vector processing, etc.).

### Valid Call Patterns
```scala
val summary = GeometricSummary.run(opts, Array(inputfile.getPath), null, sparkContext).asInstanceOf[Summary]
```

### LLM Instruction Prompt
- Use `sparkContext` exactly as a zero-argument value (`sparkContext`), not as a function call with arguments.
- Preserve receiver/usage style from verified test code; pass it where an API expects a `SparkContext`.
- Do not invent parameters, overloads, or alternate call shapes for this API.

### Prompt Snippet
```text
Use the existing Spark test/application context and pass `sparkContext` directly to APIs that require a `SparkContext` (example: `..., sparkContext)`), with no arguments.
```

### Common Failure Modes
- Calling it like a method with arguments (e.g., `sparkContext(...)`) instead of using it as `sparkContext`.
- Trying to use it outside the class/trait/scope that defines it.
- Assuming it creates a new Spark context; it returns the existing one.

### Fix Code Hint
```scala
val summary = GeometricSummary.run(opts, Array(inputfile.getPath), null, sparkContext).asInstanceOf[Summary]
```

## API Test: `sparkSession`

### Signature
```scala
override def sparkSession: SparkSession
def sparkSession: SparkSession
```
_Source: beast/spatialtest/src/main/scala/edu/ucr/cs/bdlab/test/BeastSpatialTest.scala:27  (+1 more definition site/overload)_

### Goal
Return the active Spark SQL session object used by Beast/RDPro code, so raster/vector workflows run on the current Spark runtime.

### Parameters
_None._

### Input
This method takes no arguments and does not directly consume raster/vector files.  
Precondition: it must be called on an object/context that defines this method (the exact receiver form is not documented in the provided README/tests for this API).

### Output
Returns `SparkSession` — the Spark session handle (Spark SQL entry point) associated with the current Beast/RDPro execution context.

### Valid Call Patterns
```scala
// Inferred from signature only (no verbatim README/test call form was provided)
val session: SparkSession = sparkSession
```

### LLM Instruction Prompt
- Use `sparkSession` as a zero-argument accessor returning `SparkSession`.
- Do not add arguments or type parameters.
- Because no authoritative call-site receiver is provided, treat the exact qualifier/receiver as context-dependent.
- If generating runnable code, ensure `SparkSession` is in scope and call this only from a type that actually exposes `sparkSession`.

### Prompt Snippet
```text
Get the current SparkSession via `sparkSession` (no arguments). Do not pass parameters. Use the receiver available in the current Beast/RDPro context.
```

### Common Failure Modes
- Calling `sparkSession(...)` with arguments (invalid; method has no params).
- Calling `sparkSession` from a scope/object that does not define it.
- Assuming a specific Beast receiver form from docs: no verbatim receiver call shape was provided for this API.

### Fix Code Hint
```scala
// Correct shape: zero-argument accessor
val session: SparkSession = sparkSession
```

## API Test: `spatialFile`

### Signature
```scala
def spatialFile(filename: String, format: String = null, opts: BeastOptions = new BeastOptions): SpatialRDD
def spatialFile(filename: String, opts: BeastOptions): SpatialRDD
def spatialFile(filename: String, iformat: String, opts: BeastOptions): JavaSpatialRDD
def spatialFile(filename: String, iformat: String): JavaSpatialRDD
def spatialFile(filename: String, opts: BeastOptions): JavaSpatialRDD
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/ReadWriteMixin.scala:46  (+4 more definition site/overload)_

_Source doc:_ Reads the given file according to the given spatial format. If spatial format is not given, it auto-detects the input based on the extension and then file contents (for CSV files only) @param filename the name of the file or directory of files @return the [[SpatialRDD]] that contains the records

### Goal
Load vector spatial records from a file (or directory of files) into a Spark `SpatialRDD`, with either explicit format selection or automatic format detection.

### Parameters
- `filename` (`String`): Path to the input file, or a directory containing input files to read as spatial data.
- `format` (`String`), default `null`: Input spatial format identifier; if `null`, Beast auto-detects from file extension, and for CSV specifically can further infer from file contents.
- `opts` (`BeastOptions`), default `new BeastOptions`: Reader options (for example, delimiter-related options in CSV-like inputs, as shown in project examples).

### Input
`spatialFile` expects vector spatial input supported by Beast I/O. From the provided docs/context, this includes formats such as Shapefile, GeoJSON, GPX, and text-delimited encodings (e.g., WKT/envelope forms) when the corresponding format string is provided.

Preconditions and compatibility notes:
- `filename` must point to existing readable input (file or directory).
- If you omit `format`, detection relies on extension (plus CSV content inference only).
- If extension/content is ambiguous, pass an explicit `format`.
- For indexed/partitioned datasets written with Beast, use a matching declared format when reloading (as shown in tests with `"wkt"` and `"envelope"`).

### Output
Returns `SpatialRDD` — a distributed RDD of spatial feature records loaded from the input path(s), ready for downstream operations such as `spatialJoin`, partitioning, filtering, and writing.

### Valid Call Patterns
```scala
val parks = sparkContext.spatialFile(parksFile.getPath, "wkt")
val lakes = sparkContext.spatialFile(lakesFile, "wkt")

val r1Disk: SpatialRDD = sparkContext.spatialFile(index1Path, "envelope")
val r2Disk: SpatialRDD = sparkContext.spatialFile(index2Path, "envelope")

val records = sparkContext.spatialFile("input.gpx", "gpx")
```

### LLM Instruction Prompt
- Use receiver-qualified calls exactly like `sparkContext.spatialFile(...)`.
- Prefer explicit `format` when format inference may be ambiguous.
- Pass only the documented arguments: `filename`, optional `format`, optional `opts`.
- Do not invent extra parameters or alternate signatures.
- If options are needed, put them in `BeastOptions`; otherwise rely on defaults.

### Prompt Snippet
```text
Load the vector dataset with sparkContext.spatialFile(path, format). 
If format is unknown but extension is reliable, omit format and rely on auto-detection; 
if CSV or ambiguous input, provide explicit format and BeastOptions.
```

### Common Failure Modes
- Wrong or missing `format` for ambiguous input, causing parse/read failure.
- Invalid `filename` path (nonexistent file/directory or inaccessible location).
- Supplying options outside `BeastOptions` instead of via `opts`.
- Using a call shape not present in API/tests (e.g., bare `spatialFile(...)` without `sparkContext` receiver in Scala code context).

### Fix Code Hint
```scala
import edu.ucr.cs.bdlab.beast._
import edu.ucr.cs.bdlab.beast.common.BeastOptions

// Prefer explicit format when known
val features: SpatialRDD = sparkContext.spatialFile(inputPath, "envelope")

// If reader options are needed, pass BeastOptions
val opts = new BeastOptions("separator:,")
val rects = sparkContext.spatialFile("rects.csv", "envelope(0,1,2,3)", opts)
```

## API Test: `spatialJoin`

### Signature
```scala
def spatialJoin(rdd2: SpatialRDD, joinPredicate: ESJPredicate = ESJPredicate.Intersects, method: ESJDistributedAlgorithm = null, mbrCount: LongAccumulator = null, opts: BeastOptions = new BeastOptions()): RDD[(IFeature, IFeature)]
def spatialJoin(partitionedRDD2: PartitionedSpatialRDD, joinPredicate: ESJPredicate = ESJPredicate.Intersects, mbrCount: LongAccumulator = null): RDD[(IFeature, IFeature)]
def spatialJoin(rdd1: JavaSpatialRDD, rdd2: JavaSpatialRDD, predicate: SpatialJoinAlgorithms.ESJPredicate, algorithm: SpatialJoinAlgorithms.ESJDistributedAlgorithm): JavaPairRDD[IFeature, IFeature]
def spatialJoin(rdd1: JavaSpatialRDD, rdd2: JavaSpatialRDD): JavaPairRDD[IFeature, IFeature]
def spatialJoin(r1: SpatialRDD, r2: SpatialRDD, joinPredicate: ESJPredicate = ESJPredicate.Intersects, joinMethod: ESJDistributedAlgorithm = null, mbrCount: LongAccumulator = null, opts: BeastOptions = new BeastOptions()): RDD[(IFeature, IFeature)]
def spatialJoin(r1: JavaSpatialRDD, r2: JavaSpatialRDD, joinPredicate: ESJPredicate, joinMethod: ESJDistributedAlgorithm, mbrCount: LongAccumulator, opts: BeastOptions): JavaPairRDD[IFeature, IFeature]
```
_Source: beast/beast-spark/src/main/scala/edu/ucr/cs/bdlab/beast/operations/SpatialJoin.scala:146  (+5 more definition site/overload)_

_Source doc:_ The main entry point for spatial join operations. Performs a spatial join between the given two inputs and returns an RDD of pairs of matching features. This method is a transformation. However, if the [[ESJDistributedAlgorithm.PBSM]] is used, the MBR of the two inputs has to be calculated first which runs a reduce action on each dataset even if the output of the spatial join is not used. You can specify a specific spatial join method through the [[joinMethod]] parameter. If not specified, an algorithm will be picked automatically based on the following rules. - If both datasets are spatially partitioned, the distributed join [[ESJDistributedAlgorithm.DJ]] algorithm is used. - If the product of the number of partitions of both datasets is less than [[SparkContext.defaultParallelism]], then the block nested loop join is used [[ESJDistributedAlgorithm.BNLJ]] - If at least one dataset is partition, then the repartition join is used [[ESJDistributedAlgorithm.REPJ]] - If none of the above, then the partition based spatial merge join is used [[ESJDistributedAlgorithm.PBSM]] @param r1 the first (left) dataset @param r2 the second (right) dataset @param joinPredicate the join predicate. The default is [[ESJPredicate.Intersects]] which finds all non-disjoint features @param joinMethod the join algorithm. If not specified the algorithm automatically chooses an algorithm based on the heuristic described above. @param mbrCount an (optional) accumulator to count the number of MBR tests during the algorithm. @return an RDD that contains pairs of matching features.

### Goal
Run a distributed vector spatial join between two `SpatialRDD` datasets and return all feature pairs that satisfy a spatial predicate (default: intersects).

### Parameters
- `r1` (`SpatialRDD`): the first (left) spatial dataset to join.
- `r2` (`SpatialRDD`): the second (right) spatial dataset to join.
- `joinPredicate` (`ESJPredicate`), default `ESJPredicate.Intersects`: spatial relation used to match features (default finds non-disjoint pairs).
- `joinMethod` (`ESJDistributedAlgorithm`), default `null`: distributed join algorithm; if `null`, Beast auto-selects using documented heuristics (DJ/BNLJ/REPJ/PBSM).
- `mbrCount` (`LongAccumulator`), default `null`: optional accumulator counting MBR tests during join processing.
- `opts` (`BeastOptions`), default `new BeastOptions()`: optional Beast configuration options passed to the join.

### Input
Two vector `SpatialRDD` inputs (or partitioned variants via overloads), typically loaded from Beast-supported vector sources (e.g., WKT/GeoJSON/Shapefile via corresponding readers).

Preconditions / compatibility notes:
- Inputs must be valid `SpatialRDD`/`PartitionedSpatialRDD` values.
- If using the partitioned overload (`partitioned1.spatialJoin(partitioned2, ...)`), both sides should be partitioned datasets.
- If `joinMethod` is `ESJDistributedAlgorithm.PBSM`, Beast computes MBRs first, which triggers reduce actions on both inputs even if the final join RDD is not later consumed.
- If `joinMethod` is not specified (`null`), algorithm selection follows documented rules:
  - both datasets spatially partitioned → `DJ`
  - partition-count product < `SparkContext.defaultParallelism` → `BNLJ`
  - at least one dataset partitioned → `REPJ`
  - otherwise → `PBSM`

### Output
Returns `RDD[(IFeature, IFeature)]` — each record is a matched pair `(leftFeature, rightFeature)` where the two geometries satisfy `joinPredicate`.

### Valid Call Patterns
```scala
val joinResults = dataset1.spatialJoin(dataset2, ESJPredicate.Intersects, ESJDistributedAlgorithm.DJ)

val joinResults = partitioned1.spatialJoin(partitioned2, ESJPredicate.Intersects)

partitionedFeatures1.spatialJoin(partitionedFeatures2)

val sjResults: RDD[(IFeature, IFeature)] =
      matchedPolygons.spatialJoin(matchedPoints, ESJPredicate.Contains, ESJDistributedAlgorithm.PBSM)
```

### LLM Instruction Prompt
- Use the instance call form `value.spatialJoin(...)` exactly as shown in tested/readme examples.
- Pass only documented parameters (`r2`, `joinPredicate`, `method/joinMethod`, `mbrCount`, `opts`) for Scala overloads.
- Do not invent extra arguments, return types, or option keys.
- If forcing `PBSM`, mention it can trigger MBR reduce actions eagerly.
- For partitioned workflows, prefer the partitioned overload on `PartitionedSpatialRDD`.

### Prompt Snippet
```text
Given two SpatialRDDs, call spatial join as:
left.spatialJoin(right, ESJPredicate.Intersects, ESJDistributedAlgorithm.DJ)
or, for partitioned inputs:
partitionedLeft.spatialJoin(partitionedRight, ESJPredicate.Intersects)

Return type is RDD[(IFeature, IFeature)].
Do not add undocumented parameters.
```

### Common Failure Modes
- Calling a nonexistent shape (e.g., bare `spatialJoin(...)` without receiver in Scala implicit context).
- Expecting pure laziness with `ESJDistributedAlgorithm.PBSM`; MBR computation may run reduce actions immediately.
- Assuming algorithm selection without understanding partitioning state; auto-selection may choose different algorithms than expected.
- Mixing Java and Scala overload expectations (`JavaPairRDD` vs `RDD[(IFeature, IFeature)]`).

### Fix Code Hint
```scala
// Non-partitioned / explicit algorithm
val joinResults: RDD[(IFeature, IFeature)] =
  dataset1.spatialJoin(dataset2, ESJPredicate.Intersects, ESJDistributedAlgorithm.DJ)

// Partitioned overload
val joinResults2: RDD[(IFeature, IFeature)] =
  partitioned1.spatialJoin(partitioned2, ESJPredicate.Intersects)
```

## API Test: `spatialJoinBNLJ`

### Signature
```scala
def spatialJoinBNLJ(r1: SpatialRDD, r2: SpatialRDD, joinPredicate: ESJPredicate, numMBRTests: LongAccumulator = null) : RDD[(IFeature, IFeature)]
def spatialJoinBNLJ(r1: JavaSpatialRDD, r2: JavaSpatialRDD, joinPredicate: ESJPredicate, numMBRTests: LongAccumulator): JavaPairRDD[IFeature, IFeature]
def spatialJoinBNLJ(r1: JavaSpatialRDD, r2: JavaSpatialRDD, joinPredicate: ESJPredicate): JavaPairRDD[IFeature, IFeature]
```
_Source: beast/beast-spark/src/main/scala/edu/ucr/cs/bdlab/beast/operations/SpatialJoin.scala:418  (+2 more definition site/overload)_

_Source doc:_ Runs a spatial join between the two given RDDs using the block-nested-loop join algorithm. @param r1            the first set of features @param r2            the second set of features @param joinPredicate the predicate that joins a feature from r1 with a feature in r2 @return

### Goal
Run a spatial join between two feature RDDs using the block-nested-loop join (BNLJ) algorithm, returning all feature pairs that satisfy the requested spatial predicate.

### Parameters
- `r1` (`SpatialRDD`): the first input set of spatial features (`IFeature` records) to be joined.
- `r2` (`SpatialRDD`): the second input set of spatial features (`IFeature` records) to be joined against `r1`.
- `joinPredicate` (`ESJPredicate`): the spatial predicate used to decide whether one feature from `r1` joins with one feature from `r2` (example from tests: `ESJPredicate.MBRIntersects`).
- `numMBRTests` (`LongAccumulator`), default `null`: optional Spark accumulator for counting MBR tests during join processing; may be left as `null`.

### Input
`spatialJoinBNLJ` expects two already-created `SpatialRDD` inputs (Scala API) or `JavaSpatialRDD` inputs (Java API).  
It does **not** load files directly; load data first (e.g., shapefile/GeoJSON/etc.) and then pass the resulting spatial RDDs.

Preconditions/compatibility notes from available docs:
- Inputs must be feature RDDs (`IFeature`-based spatial data), not raster tiles.
- You must choose a valid `ESJPredicate` for the intended join semantics.
- If you need better scalability for large production joins, project docs recommend spatial partitioning/indexing workflows (e.g., `spatialPartition(...)`) and other distributed algorithms; this API specifically runs **BNLJ**.

### Output
Returns `RDD[(IFeature, IFeature)]` — each output record is one matched pair:
- first element: a feature from `r1`
- second element: a feature from `r2`
that satisfies `joinPredicate`.

### Valid Call Patterns
```scala
val results = SpatialJoin.spatialJoinBNLJ(r1, r2, joinPredicate = ESJPredicate.MBRIntersects)
```

### LLM Instruction Prompt
- Use the static/object call form exactly as validated in tests: `SpatialJoin.spatialJoinBNLJ(...)`.
- Pass two `SpatialRDD` inputs and one `ESJPredicate`; optionally pass `numMBRTests`.
- Do not replace this with `spatialJoin(...)` or another algorithm unless explicitly requested.
- Do not pass raster types (`RasterRDD`, `ITile`) to this API.

### Prompt Snippet
```text
Given two SpatialRDD variables r1 and r2, call:
SpatialJoin.spatialJoinBNLJ(r1, r2, joinPredicate = ESJPredicate.MBRIntersects)
Optionally include a LongAccumulator as the 4th argument for numMBRTests.
Return or further process the resulting RDD[(IFeature, IFeature)].
```

### Common Failure Modes
- Passing non-spatial-feature RDDs (for example raster data) instead of `SpatialRDD`.
- Using an invalid or unintended join predicate for the analysis goal.
- Expecting this API to read files directly; loading/parsing must happen before the call.
- Using a different receiver/call shape than the tested one in this context.

### Fix Code Hint
```scala
// Ensure both inputs are SpatialRDD, then call the tested form
val r1: SpatialRDD = /* preloaded feature RDD */
val r2: SpatialRDD = /* preloaded feature RDD */

val results: RDD[(IFeature, IFeature)] =
  SpatialJoin.spatialJoinBNLJ(r1, r2, joinPredicate = ESJPredicate.MBRIntersects)
```

## API Test: `spatialJoinDJ`

### Signature
```scala
def spatialJoinDJ(r1: SpatialRDD, r2: SpatialRDD, joinPredicate: ESJPredicate, numMBRTests: LongAccumulator = null): RDD[(IFeature, IFeature)]
```
_Source: beast/beast-spark/src/main/scala/edu/ucr/cs/bdlab/beast/operations/SpatialJoin.scala:461_

_Source doc:_ Distributed join algorithm between spatially partitioned RDDs @param r1            the first set of features @param r2            the second set of features @param joinPredicate the predicate that joins a feature from r1 with a feature in r2 @param numMBRTests   a counter that will contain the number of MBR tests @return a pair RDD for joined features

### Goal
Run a distributed spatial join (DJ algorithm) between two `SpatialRDD`s and return all feature pairs that satisfy a given spatial predicate.

### Parameters
- `r1` (`SpatialRDD`): the first input feature dataset to join.
- `r2` (`SpatialRDD`): the second input feature dataset to join.
- `joinPredicate` (`ESJPredicate`): spatial relation used to match one feature from `r1` with one feature from `r2` (for example, predicates used in Beast spatial join workflows such as `Contains`).
- `numMBRTests` (`LongAccumulator`), default `null`: optional Spark accumulator to count MBR (minimum bounding rectangle) tests performed during join processing.

### Input
`spatialJoinDJ` expects two in-memory/vector `SpatialRDD` inputs (not file paths).  
You typically create them first using Beast readers such as `sc.shapefile(...)`, `sc.geojsonFile(...)`, or other vector loaders.

Preconditions and compatibility notes from project context:
- This method is documented as a **distributed join algorithm between spatially partitioned RDDs**; callers should provide `SpatialRDD`s prepared for distributed join workflows.
- If your pipeline includes partitioning/indexing, Beast recommends `RSGrovePartitioner` for spatial workloads.
- Input formats (Shapefile/GeoJSON/CSV-WKT/etc.) are handled at load time; this API itself only accepts `SpatialRDD`.

### Output
Returns `RDD[(IFeature, IFeature)]`, where each tuple is one matched pair:
- first element: a feature from `r1`
- second element: a feature from `r2`
and the pair satisfies `joinPredicate`.

### Valid Call Patterns
```scala
// Inferred from the API signature (no verbatim spatialJoinDJ call example provided in README/test snippet)
val sjResults: RDD[(IFeature, IFeature)] =
  SpatialJoin.spatialJoinDJ(r1, r2, joinPredicate)
```

### LLM Instruction Prompt
- Use `SpatialRDD` variables as inputs; do not pass file paths directly to `spatialJoinDJ`.
- Provide a valid `ESJPredicate` value explicitly.
- Use the 3-argument call unless you intentionally track MBR tests; pass a `LongAccumulator` only when needed.
- Keep argument order exactly: `(r1, r2, joinPredicate, numMBRTests)`.

### Prompt Snippet
```text
Given two existing SpatialRDD variables r1 and r2, call SpatialJoin.spatialJoinDJ(r1, r2, <ESJPredicate>) and store the result as RDD[(IFeature, IFeature)]. Do not invent extra parameters. If MBR test counting is needed, pass a LongAccumulator as the 4th argument; otherwise omit it.
```

### Common Failure Modes
- Passing paths/strings instead of `SpatialRDD` objects.
- Swapping argument order (e.g., putting predicate in the wrong position).
- Using an invalid or missing `ESJPredicate`.
- Expecting this API to load data; loading must happen beforehand via Beast input APIs.
- Assuming output is aggregated stats; output is raw matched feature pairs.

### Fix Code Hint
```scala
import edu.ucr.cs.bdlab.beast._
import org.apache.spark.rdd.RDD

val r1: SpatialRDD = sc.shapefile("left.zip")
val r2: SpatialRDD = sc.geojsonFile("right.geojson.gz")

val sj: RDD[(IFeature, IFeature)] =
  SpatialJoin.spatialJoinDJ(r1, r2, ESJPredicate.Contains)
```

## API Test: `spatialJoinIntersectsPlaneSweepFeatures`

### Signature
```scala
private[beast] def spatialJoinIntersectsPlaneSweepFeatures[T1 <: IFeature, T2 <: IFeature] (r: Array[T1], s: Array[T2], dupAvoidanceMBR: EnvelopeNDLite, joinPredicate: ESJPredicate, numMBRTests: LongAccumulator): TraversableOnce[(IFeature, IFeature)]
```
_Source: beast/beast-spark/src/main/scala/edu/ucr/cs/bdlab/beast/operations/SpatialJoin.scala:244_

_Source doc:_ Runs a plane-sweep algorithm between the given two arrays of input features and returns an iterator of pairs of features. @param r the first set of features @param s the second set of features @param dupAvoidanceMBR the duplicate avoidance MBR to run the reference point technique. @param joinPredicate the join predicate to match features @param numMBRTests an (optional) accumulator to count the number of MBR tests @tparam T1 the type of the first dataset @tparam T2 the type of the second dataset @return an iterator over pairs of features

### Goal
Run an in-memory plane-sweep spatial join between two feature arrays and return matched feature pairs under a specified spatial predicate, with optional duplicate-avoidance and MBR-test counting.

### Parameters
- `r` (`Array[T1]`): The first input feature set (left side of the join), where `T1` is a subtype of `IFeature`.
- `s` (`Array[T2]`): The second input feature set (right side of the join), where `T2` is a subtype of `IFeature`.
- `dupAvoidanceMBR` (`EnvelopeNDLite`): Duplicate-avoidance MBR used by the reference-point technique during join matching.
- `joinPredicate` (`ESJPredicate`): Spatial predicate used to decide whether a pair matches (for example, test code uses `ESJPredicate.Intersects`).
- `numMBRTests` (`LongAccumulator`): Optional accumulator to count how many MBR tests are performed; test usage shows `null` is accepted.

### Input
This method takes **in-memory feature arrays**, not file paths. You must provide:

- `Array[T1]` and `Array[T2]` where each element is an `IFeature` subtype.
- A valid `EnvelopeNDLite` for duplicate avoidance.
- A join predicate (`ESJPredicate`).
- A `LongAccumulator` or `null` (optional, per source doc and test usage).

Preconditions/compatibility notes from available context:

- This is a `private[beast]` API, so it is intended for internal/package-level use.
- The method is part of vector spatial join processing (not RDPro raster load/save APIs).
- Inputs must already be prepared as feature objects in memory (for example via prior parsing/loading steps in your pipeline).

### Output
Returns `TraversableOnce[(IFeature, IFeature)]` — an iterable-once collection of matched `(leftFeature, rightFeature)` pairs that satisfy `joinPredicate` under the plane-sweep join logic (with duplicate-avoidance behavior controlled by `dupAvoidanceMBR`).

### Valid Call Patterns
```scala
val results = SpatialJoin.spatialJoinIntersectsPlaneSweepFeatures(r.toArray, s.toArray,
  new EnvelopeNDLite(2, 2.0, 0.0, 5.0, 3.0), ESJPredicate.Intersects, null)
```

### LLM Instruction Prompt
- Use the call receiver exactly as validated in tests: `SpatialJoin.spatialJoinIntersectsPlaneSweepFeatures(...)`.
- Pass arguments in this exact order: `r, s, dupAvoidanceMBR, joinPredicate, numMBRTests`.
- Provide arrays of `IFeature` subtypes for `r` and `s`; do not pass RDDs or file paths.
- Use an `EnvelopeNDLite` for `dupAvoidanceMBR`; do not substitute other envelope types.
- `numMBRTests` is optional and can be `null` (as shown by passing test).
- Do not invent extra parameters or alternate overloads (none documented).

### Prompt Snippet
```text
Call SpatialJoin.spatialJoinIntersectsPlaneSweepFeatures with:
1) r: Array[T1 <: IFeature]
2) s: Array[T2 <: IFeature]
3) dupAvoidanceMBR: EnvelopeNDLite
4) joinPredicate: ESJPredicate
5) numMBRTests: LongAccumulator (or null if not used)

Keep receiver and argument order exactly:
SpatialJoin.spatialJoinIntersectsPlaneSweepFeatures(r, s, dupAvoidanceMBR, joinPredicate, numMBRTests)
```

### Common Failure Modes
- Calling it as a public API from outside Beast package scope (`private[beast]` visibility).
- Passing non-array inputs (e.g., `RDD[IFeature]`, `List` without `.toArray`, or file path strings).
- Using the wrong envelope type for duplicate avoidance (must be `EnvelopeNDLite`).
- Reordering arguments (especially mixing `joinPredicate` and `numMBRTests`).
- Assuming `numMBRTests` is mandatory when test usage shows `null` is valid.

### Fix Code Hint
```scala
val results = SpatialJoin.spatialJoinIntersectsPlaneSweepFeatures(
  r.toArray,
  s.toArray,
  new EnvelopeNDLite(2, 2.0, 0.0, 5.0, 3.0),
  ESJPredicate.Intersects,
  null
)
```

## API Test: `spatialJoinPBSM`

### Signature
```scala
def spatialJoinPBSM(r1: SpatialRDD, r2: SpatialRDD, joinPredicate: ESJPredicate, numMBRTests: LongAccumulator = null, opts: BeastOptions = new BeastOptions()): RDD[(IFeature, IFeature)]
def spatialJoinPBSM(r1: JavaSpatialRDD, r2: JavaSpatialRDD, joinPredicate: ESJPredicate, numMBRTests: LongAccumulator): JavaPairRDD[IFeature, IFeature]
def spatialJoinPBSM(r1: JavaSpatialRDD, r2: JavaSpatialRDD, joinPredicate: ESJPredicate) : JavaPairRDD[IFeature, IFeature]
```
_Source: beast/beast-spark/src/main/scala/edu/ucr/cs/bdlab/beast/operations/SpatialJoin.scala:297  (+2 more definition site/overload)_

_Source doc:_ Performs a partition-based spatial-merge (PBSM) join as explained in the following paper. Jignesh M. Patel, David J. DeWitt: Partition Based Spatial-Merge Join. SIGMOD Conference 1996: 259-270 https://doi.org/10.1145/233269.233338 @param r1            the first dataset @param r2            the second dataset @param joinPredicate the join predicate @param numMBRTests   (output) the number of MBR tests done during the algorithm @param opts          Additional options for the PBSM algorithm @return a pair RDD for joined features

### Goal
Run a distributed partition-based spatial join (PBSM) between two vector `SpatialRDD`s and return matching feature pairs under a chosen spatial predicate.

### Parameters
- `r1` (`SpatialRDD`): the first input spatial dataset (features to be joined).
- `r2` (`SpatialRDD`): the second input spatial dataset (features to be joined against `r1`).
- `joinPredicate` (`ESJPredicate`): spatial join condition used to decide whether a feature from `r1` matches a feature from `r2` (e.g., tests use `ESJPredicate.MBRIntersects`).
- `numMBRTests` (`LongAccumulator`), default `null`: optional output accumulator to collect the number of MBR tests performed by the algorithm.
- `opts` (`BeastOptions`), default `new BeastOptions()`: additional PBSM options.

### Input
`spatialJoinPBSM` operates on already-loaded vector `SpatialRDD` inputs (not raster inputs).  
Typical vector sources in Beast include Shapefile/GeoJSON/CSV-WKT/etc., but this function itself receives `SpatialRDD` objects.

Preconditions/compatibility guidance from project context:
- Inputs must be valid spatial feature datasets (`SpatialRDD`) suitable for spatial join.
- If you need faster large-scale joins, Beast documentation recommends spatial partitioning/index workflows (e.g., `RSGrovePartitioner`) before running join operations.
- This API is for vector join logic; raster compatibility/type-selection rules (`sc.geoTiff[T]`, reshape rules, etc.) do **not** apply directly to this function.

### Output
Returns `RDD[(IFeature, IFeature)]` — each record is a matched pair:
- first element: one `IFeature` from `r1`
- second element: one `IFeature` from `r2`
that satisfies `joinPredicate` under PBSM.

### Valid Call Patterns
```scala
val result = SpatialJoin.spatialJoinPBSM(dataset1, dataset2, ESJPredicate.MBRIntersects)
```

```scala
val result = SpatialJoin.spatialJoinPBSM(dataset1, dataset2, ESJPredicate.MBRIntersects)
assertResult(0)(result.getNumPartitions)
assertResult(true)(result.isEmpty())
```

### LLM Instruction Prompt
- Use the tested call form with qualifier: `SpatialJoin.spatialJoinPBSM(r1, r2, predicate, ...)`.
- Pass `SpatialRDD` inputs only.
- Provide a valid `ESJPredicate` explicitly.
- Use `numMBRTests` only if you need MBR-test counting; otherwise rely on default `null`.
- Use `opts` only when you have concrete PBSM options to set; otherwise keep default `new BeastOptions()`.

### Prompt Snippet
```text
Given two SpatialRDD variables r1 and r2, call:
SpatialJoin.spatialJoinPBSM(r1, r2, ESJPredicate.MBRIntersects)
Optionally pass a LongAccumulator as numMBRTests and BeastOptions as opts.
Return type is RDD[(IFeature, IFeature)].
```

### Common Failure Modes
- Passing non-`SpatialRDD` inputs (e.g., raster `RasterRDD`) to `spatialJoinPBSM`.
- Using an invalid or omitted join predicate.
- Expecting non-empty output for disjoint datasets; tested behavior shows empty results are valid.
- Assuming a different receiver/call shape; use the object-qualified form shown in tests: `SpatialJoin.spatialJoinPBSM(...)`.

### Fix Code Hint
```scala
import edu.ucr.cs.bdlab.beast._
import edu.ucr.cs.bdlab.beast.operations.SpatialJoin

val result: RDD[(IFeature, IFeature)] =
  SpatialJoin.spatialJoinPBSM(dataset1, dataset2, ESJPredicate.MBRIntersects)

// Optional: with accumulator/options if needed
// val acc = sparkContext.longAccumulator("numMBRTests")
// val result2 = SpatialJoin.spatialJoinPBSM(dataset1, dataset2, ESJPredicate.MBRIntersects, acc, new BeastOptions())
```

## API Test: `spatialJoinRepJ`

### Signature
```scala
def spatialJoinRepJ(r1: SpatialRDD, r2: SpatialRDD, joinPredicate: ESJPredicate, numMBRTests: LongAccumulator = null): RDD[(IFeature, IFeature)]
```
_Source: beast/beast-spark/src/main/scala/edu/ucr/cs/bdlab/beast/operations/SpatialJoin.scala:488_

_Source doc:_ Repartition join algorithm between two datasets: r1 is spatially disjoint partitioned and r2 is not @param r1 the first dataset @param r2 the second dataset @param joinPredicate the join predicate @param numMBRTests an optional accumulator that counts the number of MBR tests @return an RDD of pairs of matching features

### Goal
Run a distributed spatial join using the REPJ algorithm where `r1` is already spatially disjoint-partitioned and `r2` is not, returning matching feature pairs under a given spatial predicate.

### Parameters
- `r1` (`SpatialRDD`): The first spatial dataset; per the source doc, this dataset is expected to be spatially disjoint partitioned.
- `r2` (`SpatialRDD`): The second spatial dataset; per the source doc, this dataset is not spatially disjoint partitioned.
- `joinPredicate` (`ESJPredicate`): Spatial relationship used to test matches (for example, predicates from `ESJPredicate` such as `Contains` shown elsewhere in Beast docs).
- `numMBRTests` (`LongAccumulator`), default `null`: Optional Spark accumulator to count the number of MBR (minimum bounding rectangle) tests performed.

### Input
- Two in-memory vector `SpatialRDD` inputs (`r1`, `r2`) containing `IFeature` geometries.
- Typical Beast vector sources include Shapefile/GeoJSON/CSV-WKT/etc., loaded first into `SpatialRDD` via Beast I/O APIs.
- **Precondition from source doc:** `r1` should be spatially disjoint partitioned, while `r2` is not.
- If you need disjoint partitioning, Beast context notes that this depends on partitioner support (`-disjoint` is only valid for partitioners that support disjoint partitions).

### Output
Returns `RDD[(IFeature, IFeature)]` — each record is a pair of matching features `(featureFromR1, featureFromR2)` that satisfy `joinPredicate`.

### Valid Call Patterns
```scala
// Inferred from the function signature (no verbatim spatialJoinRepJ call was provided in README/test snippet)
val results: RDD[(IFeature, IFeature)] =
  spatialJoinRepJ(r1, r2, joinPredicate)

val resultsWithAcc: RDD[(IFeature, IFeature)] =
  spatialJoinRepJ(r1, r2, joinPredicate, numMBRTests)
```

### LLM Instruction Prompt
- Use exactly four parameters in this order: `(r1, r2, joinPredicate, numMBRTests?)`.
- Pass `SpatialRDD` for `r1` and `r2`; do not pass raster types (`RasterRDD`, `ITile`).
- Ensure `r1` is the disjoint-partitioned dataset and `r2` is the non-disjoint one, matching REPJ expectations from source doc.
- Use a valid `ESJPredicate` value.
- Only pass a `LongAccumulator` as the optional fourth argument; otherwise omit it and use default `null`.

### Prompt Snippet
```text
Given two SpatialRDD datasets, call spatialJoinRepJ(r1, r2, joinPredicate, numMBRTests?) to run REPJ.
Precondition: r1 is spatially disjoint partitioned; r2 is not.
Return type must be RDD[(IFeature, IFeature)].
Do not use raster inputs or add extra parameters.
```

### Common Failure Modes
- Passing inputs in the wrong role (non-disjoint dataset as `r1`), violating REPJ precondition from source doc.
- Supplying wrong data types (e.g., raster RDDs instead of `SpatialRDD`).
- Using an invalid or missing `ESJPredicate`.
- Passing a non-`LongAccumulator` value as `numMBRTests`.
- Attempting disjoint partitioning with an unsupported partitioner (per Beast partitioning constraints).

### Fix Code Hint
```scala
import edu.ucr.cs.bdlab.beast._
import org.apache.spark.rdd.RDD
import org.apache.spark.util.LongAccumulator

// r1: SpatialRDD (disjoint partitioned), r2: SpatialRDD (not disjoint), predicate: ESJPredicate
val out: RDD[(IFeature, IFeature)] =
  spatialJoinRepJ(r1, r2, joinPredicate)

// Optional MBR test counting
val mbrTests: LongAccumulator = spark.sparkContext.longAccumulator("mbr-tests")
val out2: RDD[(IFeature, IFeature)] =
  spatialJoinRepJ(r1, r2, joinPredicate, mbrTests)
```

## API Test: `spatialPartition`

### Signature
```scala
def spatialPartition(spatialPartitioner: SpatialPartitioner): SpatialRDD
def spatialPartition(partitionerKlass: Class[_ <: SpatialPartitioner], numPartitions: Int = rdd.getNumPartitions, opts: BeastOptions = new BeastOptions()): SpatialRDD
def spatialPartition(rdd: JavaSpatialRDD, spatialPartitioner: SpatialPartitioner): JavaPartitionedSpatialRDD
def spatialPartition(rdd: JavaSpatialRDD, partitionerClass: Class[_ <: SpatialPartitioner], numPartitions: Int): JavaPartitionedSpatialRDD
def spatialPartition(rdd: JavaSpatialRDD, partitionerClass: Class[_ <: SpatialPartitioner], numPartitions: Int, opts: BeastOptions): JavaPartitionedSpatialRDD
def spatialPartition(rdd: JavaSpatialRDD, partitionerClass: Class[_ <: SpatialPartitioner]): JavaPartitionedSpatialRDD
```
_Source: beast/beast-spark/src/main/scala/edu/ucr/cs/bdlab/beast/JavaSpatialRDDHelper.scala:179  (+5 more definition site/overload)_

_Source doc:_ Partition a set of features according to a created spatial partitioner @param spatialPartitioner the partitioner for the data @return partitioned records

### Goal
Partition a spatial feature RDD into spatially organized Spark partitions using an initialized `SpatialPartitioner` (or partitioner class overload), so downstream spatial operations (for example `rangeQuery`/`spatialJoin`) run more efficiently.

### Parameters
- `rdd` (`JavaSpatialRDD`): the Java spatial RDD to partition (used in Java helper overloads).
- `spatialPartitioner` (`SpatialPartitioner`): an initialized spatial partitioner that defines how features are assigned to partitions.

### Input
A spatial feature dataset already loaded as `SpatialRDD` (Scala) or `JavaSpatialRDD` (Java helper overloads), e.g., from Beast vector readers such as `readCSVPoint`, `shapefile`, or `geojsonFile`.

Preconditions and compatibility notes from project docs/context:
- For this overload, the partitioner must be **already initialized/created**.
- If using disjoint partitioning (`"disjoint" -> true`) through partitioner creation, only use partitioners that support disjoint partitions; otherwise an error is expected.
- Disjoint partitioning may replicate features across partitions; duplicate handling may be needed unless using Beast built-ins like `rangeQuery`/`spatialJoin`.

### Output
Returns `JavaPartitionedSpatialRDD` (Java helper overloads) / `SpatialRDD` (Scala overloads): the same input feature records after spatial partitioning, now carrying partitioner metadata and organized into spatial partitions.

### Valid Call Patterns
```scala
val testFile = makeFileCopy("/test111.points")
val data: SpatialRDD = sparkContext.readCSVPoint(testFile.getPath)
val mbr = data.summary
val gridPartitioner = new GridPartitioner(mbr, Array(2, 2))
val partitionedData = data.spatialPartition(gridPartitioner)
```

```scala
val partitionedFeatures: RDD[IFeature] = features.spatialPartition(classOf[RSGrovePartitioner])
```

```scala
import edu.ucr.cs.bdlab.beast.indexing.IndexHelper.{Fixed, NumPartitions}
import edu.ucr.cs.bdlab.beast.indexing.{IndexHelper, RSGrovePartitioner}
val partitioner = IndexHelper.createPartitioner(features, classOf[RSGrovePartitioner],
  NumPartitions(Fixed, features.getNumPartitions), _ => 1, "disjoint" -> true)
val partitionedFeatures = features.spatialPartition(partitioner)
```

### LLM Instruction Prompt
- Call the method as an instance method on an existing spatial RDD: `value.spatialPartition(...)`.
- Prefer verified call forms from tests/README (`data.spatialPartition(gridPartitioner)`, `features.spatialPartition(classOf[RSGrovePartitioner])`).
- Provide an initialized `SpatialPartitioner` when using `spatialPartition(spatialPartitioner: SpatialPartitioner)`.
- Do not invent unsupported arguments or options.
- If suggesting disjoint partitioning, explicitly warn about possible feature replication and partitioner support requirements.

### Prompt Snippet
```text
Given a SpatialRDD named `data`, first build or obtain an initialized SpatialPartitioner, then call:
`val partitioned = data.spatialPartition(partitioner)`.
Use documented forms only (e.g., GridPartitioner or classOf[RSGrovePartitioner]); do not add extra parameters.
```

### Common Failure Modes
- Passing an uninitialized partitioner object to `data.spatialPartition(spatialPartitioner)`.
- Using disjoint partitioning settings with a partitioner that does not support disjoint partitions.
- Assuming no duplicates after disjoint partitioning; replicated features can appear across partitions.
- Calling a nonexistent bare function form (`spatialPartition(...)`) instead of instance form (`data.spatialPartition(...)`) in Scala code.

### Fix Code Hint
```scala
val data: SpatialRDD = sparkContext.readCSVPoint(testFile.getPath)
val mbr = data.summary
val gridPartitioner = new GridPartitioner(mbr, Array(2, 2))
val partitionedData = data.spatialPartition(gridPartitioner)

// Optional downstream check (as used in tests)
assertResult(true)(partitionedData.partitioner.isDefined)
```

## API Test: `splitGeometryAcrossDateLine`

### Signature
```scala
def splitGeometryAcrossDateLine(geometry: Geometry): Geometry
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/GeometryQuadSplitter.scala:122_

_Source doc:_ Splits the given geometry across the dateline (-180 or +180 meridian) to avoid errors. 1. This function assumes that the input consists of a polygon with a single ring (outer shell). 1. We assume that the width cannot be greater than 180 degrees. 1. If the geometry width is greater than 180, we assume that it crosses the dateline. 1. To fix the geometry, we rotate all negative longitudes by adding 360. 1. After that, we split the geometry by intersecting it with the western hemisphere once and with the easter hemisphere once. @param geometry the input geometry to detect and split @return Either the same geometry if it does not cross the dateline, or the same one split into two if it crosses the dateline.

### Goal
Split a polygon geometry that crosses the ±180° dateline into valid hemisphere-local pieces to avoid downstream geometric/topological errors.

### Parameters
- `geometry` (`Geometry`): Input geometry to inspect for dateline crossing and split if needed.

### Input
- In-memory JTS `Geometry` (not a file path argument).
- Documented preconditions from source doc:
  - Assumes a **polygon with a single ring (outer shell)**.
  - Assumes polygon width should not exceed **180 degrees** unless interpreted as dateline crossing.
  - If width > 180°, the method treats it as crossing the dateline and applies longitude rotation (+360 for negative longitudes) before splitting against hemispheres.
- No additional CRS conversion behavior is documented for this method; use geometries already in a longitude/latitude frame consistent with dateline logic.

### Output
Returns `Geometry` — either:
- the same geometry (if it does not cross the dateline), or
- a split geometry composed of two parts (west/east side) when dateline crossing is detected.

### Valid Call Patterns
```scala
val geometry = GeometryReader.DefaultGeometryFactory.createPolygon(
  Array(new Coordinate(170, 50), new Coordinate(-170, 60), new Coordinate(-170, 50), new Coordinate(170, 50))
)
val split = GeometryQuadSplitter.splitGeometryAcrossDateLine(geometry)
assertResult(2)(split.getNumGeometries)
assertResult(9)(split.getNumPoints)
```

### LLM Instruction Prompt
- Call with the static/object receiver exactly as validated in tests: `GeometryQuadSplitter.splitGeometryAcrossDateLine(geometry)`.
- Provide a `Geometry` argument only; do not add extra parameters.
- Use this API for dateline handling of polygon-like input before operations that are sensitive to wraparound.
- Respect documented assumptions (single-ring polygon, width-based crossing logic); if data violates assumptions, state that behavior is not guaranteed by docs.

### Prompt Snippet
```text
Given a JTS Geometry polygon that may cross ±180°, call GeometryQuadSplitter.splitGeometryAcrossDateLine(geometry) and use the returned Geometry (unchanged or split) for subsequent processing. Do not pass file paths or additional arguments.
```

### Common Failure Modes
- Passing geometries that do not meet the documented assumption (not a single-ring polygon outer shell); result is not specified by provided docs.
- Using coordinates not compatible with dateline longitude semantics (the function logic is explicitly based on -180/+180 and longitude rotation).
- Assuming it always returns two geometries; it may return the original geometry unchanged when no crossing is detected.

### Fix Code Hint
```scala
// Ensure you pass a Geometry and call the tested receiver form
val split: Geometry = GeometryQuadSplitter.splitGeometryAcrossDateLine(geometry)

// Optional sanity check in your pipeline:
if (split.getNumGeometries > 1) {
  // geometry was split across dateline
}
```

## API Test: `sridToCRS`

### Signature
```scala
def sridToCRS(srid: Int): CoordinateReferenceSystem
```
_Source: beast/cg/src/main/scala/org/apache/spark/beast/CRSServer.scala:352_

_Source doc:_ Convert the given SRID to CRS according to the following logic. 1. If the SRID is zero, it indicates an invalid SRID and `null` is returned. 2. It searches the local cache and retrieves the SRID. 3a. If SRID is positive, use it as an EPSG, retrieve the CRS, cache and return it. 3b. If SRID is negative, contact the server, retrieve the CRS, cache and return it. @param srid the SRID that needs to be converted to a CRS @return the converted CRS.

### Goal
Convert an SRID integer into a GeoTools `CoordinateReferenceSystem` for CRS-aware geospatial processing in Beast/RDPro pipelines.

### Parameters
- `srid` (`Int`): The SRID to convert to a CRS; `0` is invalid (returns `null`), positive values are treated as EPSG codes, and negative values are looked up via the CRS server.

### Input
A single integer SRID value (no file input). Preconditions from documented behavior/tests:
- `srid == 0` is invalid and returns `null`.
- `srid > 0` is interpreted as an EPSG code.
- `srid < 0` requires server-based retrieval path (“contact the server”); in tests, this is used with `CRSServer.startServer(sparkContext)` before lookup.

### Output
Returns `CoordinateReferenceSystem` — the decoded CRS object corresponding to the input SRID (cached after retrieval), or `null` when `srid` is `0`.

### Valid Call Patterns
```scala
CRSServer.startServer(sparkContext)
try {
  val mercator = CRS.decode("EPSG:3857")
  val sridMercator = CRSServer.crsToSRID(mercator)
  val wgs84 = CRS.decode("EPSG:4326")
  val sridWGS84 = CRSServer.crsToSRID(wgs84)
  // Now retrieve them back
  assert(CRS.lookupEpsgCode(CRSServer.sridToCRS(sridMercator), false) == 3857)
  assert(CRS.lookupEpsgCode(CRSServer.sridToCRS(sridWGS84), false) == 4326)
} finally {
  CRSServer.stopServer(true)
}
```

```scala
CRSServer.startServer(sparkContext)
val port = sparkContext.getLocalProperty(CRSServer.CRSServerPort)
try {
  val sinusoidal = new DefaultProjectedCRS("Sinusoidal", new DefaultGeographicCRS(new DefaultGeodeticDatum("World", DefaultEllipsoid.WGS84, DefaultPrimeMeridian.GREENWICH), DefaultEllipsoidalCS.GEODETIC_2D), //sinus.getConversionFromBase.getMathTransform,
    new DefaultMathTransformFactory().createFromWKT("PARAM_MT[\"Sinusoidal\", \n  PARAMETER[\"semi_major\", 6371007.181], \n  PARAMETER[\"semi_minor\", 6371007.181], \n  PARAMETER[\"central_meridian\", 0.0], \n  PARAMETER[\"false_easting\", 0.0], \n  PARAMETER[\"false_northing\", 0.0]]"), DefaultCartesianCS.PROJECTED)
  // Create a new SRID
  val sridSinusoidal = CRSServer.crsToSRID(sinusoidal)
  assert(sridSinusoidal < 0)
  // Now retrieve it back
  assert(CRSServer.sridToCRS(sridSinusoidal).toWKT == sinusoidal.toWKT())
  // Retrieve through the HTTP API
  val url = new URL(s"http://localhost:$port/crs/$sridSinusoidal")
  val content = new ObjectInputStream(url.openStream())
  val crs = content.readObject().asInstanceOf[CoordinateReferenceSystem]
  assertResult("Sinusoidal")(crs.getName.toString)
} finally {
  CRSServer.stopServer(true)
}
```

### LLM Instruction Prompt
- Call exactly as `CRSServer.sridToCRS(srid)`.
- Pass an `Int` SRID only.
- Handle `srid == 0` as invalid (`null` result possible).
- For negative SRIDs (non-EPSG), ensure CRS server path is available (per tests, start server first).
- Do not invent overloads or extra parameters.

### Prompt Snippet
```text
Use `CRSServer.sridToCRS(sridInt)` to convert SRID to CRS.
Interpret SRID rules exactly: 0 -> null, positive -> EPSG lookup, negative -> server lookup.
If using negative SRIDs, start CRSServer before calling and stop it afterward.
```

### Common Failure Modes
- Passing `0` and then dereferencing the result without null-check (`null` is expected).
- Using a negative SRID without CRS server availability, causing retrieval failure.
- Assuming all SRIDs are EPSG codes; negative SRIDs are explicitly non-EPSG/server-backed.

### Fix Code Hint
```scala
CRSServer.startServer(sparkContext)
try {
  val crs = CRSServer.sridToCRS(srid)
  require(crs != null, s"Invalid SRID: $srid")
  // use crs safely
} finally {
  CRSServer.stopServer(true)
}
```

## API Test: `startServer`

### Signature
```scala
def startServer(defaultPort: Int = DefaultPort): Int
def startServer(sc: SparkContext): Boolean
def startServer(jsc: JavaSparkContext): Boolean
```
_Source: beast/cg/src/main/scala/org/apache/spark/beast/CRSServer.scala:91  (+2 more definition site/overload)_

_Source doc:_ Starts the server and returns the port on which it is listening @return the port on which the server is started

### Goal
Start the Beast `CRSServer` so CRS/SRID mappings can be served during Spark geospatial workflows, and obtain the listening port (for the `defaultPort` overload) or a success flag (for Spark-context overloads).

### Parameters
- `defaultPort` (`Int`), default `DefaultPort`: Preferred port to start the CRS server on.

### Input
No raster/vector file input is required for this call itself.  
Preconditions from validated usage:
- Call it on `CRSServer` (as shown in tests): `CRSServer.startServer(...)`.
- If you use Spark-based overloads, you must provide a valid `SparkContext` or `JavaSparkContext`.
- In test usage, server lifecycle is managed with `try/finally` and `CRSServer.stopServer(true)` after startup.

### Output
Returns `Int` — the port number on which the server is listening (for `startServer(defaultPort: Int = DefaultPort)`).

### Valid Call Patterns
```scala
CRSServer.startServer(sparkContext)
```

### LLM Instruction Prompt
- Use the exact receiver `CRSServer` and argument order shown in compiled tests.
- Choose overload by provided argument type:
  - `SparkContext` -> `Boolean` overload
  - `JavaSparkContext` -> `Boolean` overload
  - `Int` or no argument -> `Int` overload with `defaultPort`
- Do not invent extra parameters.
- After starting in long-running/test code, stop with `CRSServer.stopServer(true)` in `finally`.

### Prompt Snippet
```text
Start the CRS server using the existing SparkContext with:
CRSServer.startServer(sparkContext)
Do not change receiver or argument order. If you need the listening port, call the Int overload:
CRSServer.startServer()
```

### Common Failure Modes
- Calling `startServer` without the `CRSServer` qualifier (may not compile in user code).
- Passing the wrong argument type to an overload (e.g., expecting an `Int` return from `startServer(sparkContext)` which returns `Boolean`).
- Starting the server and not stopping it, causing resource/port issues in repeated runs.

### Fix Code Hint
```scala
CRSServer.startServer(sparkContext)
try {
  // CRS/SRID operations
} finally {
  CRSServer.stopServer(true)
}
```

## API Test: `sumSideLength`

### Signature
```scala
def sumSideLength: Array[Double]
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/SpatialPartition.scala:47_

_Source doc:_ The sum of side length along each dimension. Combined with numNonEmptyGeometries, it can be used to compute average side length per dimension.

### Goal
Compute, for a spatial partition summary, the total side-length accumulated per coordinate dimension (e.g., X, Y).

### Parameters
_None._

### Input
Call this on an existing `SpatialPartition`/summary value (instance method, no arguments).  
There is no direct test or README example for `sumSideLength`; call form below is inferred from the signature and sibling instance-style usage (`summary.numFeatures`, `results.size`).

No file format is passed directly to this method; any upstream loading/format handling (e.g., WKT/GeoJSON/Shapefile/GeoTIFF workflows) happens before obtaining the summary object.

### Output
Returns `Array[Double]` — one entry per dimension, where each entry is the sum of side lengths along that dimension across non-empty geometries/partitions represented by the receiver.

### Valid Call Patterns
```scala
// Inferred from signature + sibling instance-call style in tests
val sideSums: Array[Double] = summary.sumSideLength
```

### LLM Instruction Prompt
- Use instance-call form on an existing summary/spatial-partition object: `value.sumSideLength`.
- Do not add parameters; this method takes none.
- Treat result as per-dimension totals (`Array[Double]`), not a scalar.
- If average side length is needed, combine with `numNonEmptyGeometries` as documented.

### Prompt Snippet
```text
Given a SpatialPartition-like summary object `summary`, call `summary.sumSideLength` (no args) and store the `Array[Double]` result. If needed, compute per-dimension averages by dividing each element by `summary.numNonEmptyGeometries`.
```

### Common Failure Modes
- Calling it like a static/global function (`sumSideLength(...)`) instead of on an instance.
- Passing arguments even though the signature is parameterless.
- Misinterpreting the output as a single number rather than one value per dimension.
- Assuming this method itself loads data/files; it only reads already-computed summary state.

### Fix Code Hint
```scala
// Correct: call on an existing summary instance
val sideSums: Array[Double] = summary.sumSideLength

// Optional documented usage pattern: average side length per dimension
val n = summary.numNonEmptyGeometries
val avg: Array[Double] =
  if (n == 0) sideSums.map(_ => 0.0) else sideSums.map(_ / n)
```

## API Test: `summarizeData`

### Signature
```scala
private[dataExplorer] def summarizeData(): Unit
```
_Source: beast/dataExplorer/src/main/scala/edu/ucr/cs/bdlab/beast/dataExplorer/DatasetProcessor.scala:219_

_Source doc:_ Summarize the dataset and set the corresponding attributes in the dataset.

### Goal
Summarize a dataset inside the Data Explorer processing flow and write the computed summary attributes back to that dataset record/state.

### Parameters
_None._

### Input
- Receiver: an existing `DatasetProcessor` instance.
- The method takes no explicit arguments; it operates on dataset state already associated with that `DatasetProcessor`.
- Visibility constraint: `private[dataExplorer]`, so it is callable only from within the `dataExplorer` package scope.
- Preconditions from available evidence:
  - A dataset should already be created/loaded in the processor workflow before summarization (inferred from the method purpose and test flow around `DatasetProcessor` lifecycle).
- File-format-specific requirements for this method are **not explicitly documented** in the provided sources.

### Output
Returns `Unit` — no direct return value; the effect is side-effect-based (it updates/sets corresponding dataset attributes as part of internal dataset metadata/state).

### Valid Call Patterns
```scala
// Inferred from signature (no direct summarizeData invocation was provided in tests/README)
datasetProcessor.summarizeData()
```

### LLM Instruction Prompt
- Use only the zero-argument instance call form on a `DatasetProcessor`: `datasetProcessor.summarizeData()`.
- Do not add parameters; the API defines none.
- Do not treat it as a public API outside `dataExplorer`; respect `private[dataExplorer]` visibility.
- Expect side effects (dataset attributes updated), not a returned summary object/value.

### Prompt Snippet
```text
Call summarizeData as a zero-argument method on an existing DatasetProcessor instance inside dataExplorer package scope:

datasetProcessor.summarizeData()

Do not pass any arguments and do not assign a return value (it returns Unit and updates dataset attributes by side effect).
```

### Common Failure Modes
- Calling it with arguments (compile error): signature is `summarizeData(): Unit`.
- Calling it as a static/object method instead of on a `DatasetProcessor` instance.
- Calling it from code that cannot access `private[dataExplorer]` members (visibility error).
- Expecting a returned summary structure instead of side-effect updates.

### Fix Code Hint
```scala
// Ensure you have a DatasetProcessor instance already created in the workflow
val datasetProcessor = new DatasetProcessor(
  "cities",
  dbConnection,
  datasetsPath.getPath,
  FileSystem.getLocal(sparkContext.hadoopConfiguration),
  sparkSession
)

// Correct call shape (no args, instance method)
datasetProcessor.summarizeData()
```

## API Test: `summary`

### Signature
```scala
def summary: Summary
def summary(rdd: JavaSpatialRDD): Summary
```
_Source: beast/beast-spark/src/main/scala/edu/ucr/cs/bdlab/beast/JavaSpatialRDDHelper.scala:171  (+2 more definition site/overload)_

_Source doc:_ Compute the geometric summary of the given RDD @param rdd the spatial RDD to compute its summary @return the summary of the given RDD

### Goal
Compute a geometric summary for a spatial feature dataset (record count, geometry characteristics, and size-related stats) so it can be used in downstream spatial processing (for example, partitioner setup).

### Parameters
- `rdd` (`JavaSpatialRDD`): the Java spatial RDD whose geometric summary is computed (Java overload).

### Input
A spatial RDD of features is required.

- Scala instance form (from tests/README): call on an existing spatial RDD value (for example from `readCSVPoint` or `shapefile`).
- Java helper form (from README): pass a `JavaSpatialRDD` to `summary(rdd)`.

Documented vector sources in Beast include shapefile/GeoJSON/CSV-WKT/etc., but `summary` itself operates on an already-loaded spatial RDD rather than directly on file paths.

Preconditions:
- The receiver/argument must be a spatial RDD type compatible with `summary` (e.g., `SpatialRDD` in Scala usage, `JavaSpatialRDD` in Java usage).

### Output
Returns `Summary` — a computed geometric summary that includes (per authoritative API doc): size in bytes, number of records, number of points, number of non-empty geometries, average side length (width and height), and geometry type.

### Valid Call Patterns
```scala
val data: SpatialRDD = sparkContext.readCSVPoint(testFile.getPath)
val mbr = data.summary
```

```Scala
import edu.ucr.cs.bdlab.beast._
val rdd = sparkContext.shapefile("input.zip")
rdd.summary()
```

```Scala
JavaRDD<IFeature> polygons = SpatialReader.readInput(sparkContext, new BeastOptions(), "input.zip", "shapefile");
Summary summary = JavaSpatialRDDHelper.summary(rdd);
```

### LLM Instruction Prompt
- Use the instance form exactly as shown when you already have a Scala spatial RDD: `value.summary` (or `value.summary()` as documented in README).
- For Java usage, call `JavaSpatialRDDHelper.summary(rdd)` with a `JavaSpatialRDD`.
- Do not invent arguments for the Scala no-arg form.
- Do not call `summary` on raster RDDs; this API is for spatial feature RDD summaries.

### Prompt Snippet
```text
Given an existing SpatialRDD value named data, compute its geometric summary using the instance call form:

val mbr = data.summary

If using JavaSpatialRDD, call:
Summary s = JavaSpatialRDDHelper.summary(rdd);
```

### Common Failure Modes
- Calling `summary` on a non-spatial dataset type (e.g., raster RDD) instead of a feature RDD.
- Using an unverified call shape (e.g., adding parameters to Scala `summary`) that is not in the API/tested examples.
- In Java, passing a value that is not the expected `JavaSpatialRDD` to the helper overload.

### Fix Code Hint
```scala
import edu.ucr.cs.bdlab.beast._

val data: SpatialRDD = sparkContext.readCSVPoint(testFile.getPath)
val mbr = data.summary
val gridPartitioner = new GridPartitioner(mbr, Array(2, 2))
val partitionedData = data.spatialPartition(gridPartitioner)
```

## API Test: `tileIDs`

### Signature
```scala
def tileIDs: Iterator[Int]
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/RasterMetadata.scala:91_

_Source doc:_ An iterators that goes over all tile IDs @return an iterator that iterates over all tile IDs in this raster

### Goal
Iterate over all tile IDs defined by a raster’s metadata so you can read/process tiles one-by-one in distributed raster workflows.

### Parameters
_None._

### Input
A `RasterMetadata` receiver instance (as used in tests: `reader.metadata`) must already exist.

From the verified usage, this metadata is available after initializing a `GeoTiffReader` on a GeoTIFF input:

- initialize reader with filesystem/path/layer/options
- then call `reader.metadata.tileIDs`

No additional parameters are required by `tileIDs` itself.

### Output
Returns `Iterator[Int]` — an iterator of integer tile IDs for the raster described by that metadata. Each element is one tile identifier that can be passed to tile-reading logic (e.g., `reader.readTile(tileID)` in the test).

### Valid Call Patterns
```scala
val rasterPath = new Path(locateResource("/rasters/FRClouds.tif").getPath)
val fileSystem = rasterPath.getFileSystem(new Configuration())
val reader = new GeoTiffReader
try {
  reader.initialize(fileSystem, rasterPath.toString, "0", new BeastOptions())
  for (tileID <- reader.metadata.tileIDs) {
    val tile = reader.readTile(tileID)
    for ((x, y) <- tile.pixelLocations)
      tile.isDefined(x, y)
  }

} finally {
  reader.close()
}
```

### LLM Instruction Prompt
- Call this as a parameterless member on a `RasterMetadata` instance: `value.tileIDs`.
- Preserve receiver form from verified usage (`reader.metadata.tileIDs`), do not rewrite as a standalone function.
- Do not add arguments; signature has none.
- Treat output as `Iterator[Int]` of tile identifiers, typically consumed in a loop.

### Prompt Snippet
```text
Given a GeoTiffReader already initialized, iterate tiles using:
for (tileID <- reader.metadata.tileIDs) { ... }
Do not pass any arguments to tileIDs.
```

### Common Failure Modes
- Calling `tileIDs` on the wrong receiver (e.g., not a `RasterMetadata` object).
- Trying to pass arguments to `tileIDs` (it takes none).
- Using `reader.metadata.tileIDs` before reader initialization, so metadata is not ready.
- Assuming it returns tile data; it only returns IDs (`Int`), so you still need `readTile(tileID)`.

### Fix Code Hint
```scala
reader.initialize(fileSystem, rasterPath.toString, "0", new BeastOptions())
for (tileID <- reader.metadata.tileIDs) {
  val tile = reader.readTile(tileID)
  // process tile
}
```

## API Test: `transform`

### Signature
```scala
override def transform(ptSrc: DirectPosition, ptDst: DirectPosition): DirectPosition
override def transform(srcPts: Array[Double], srcOff: Int, dstPts: Array[Double], dstOff: Int, numPts: Int): Unit
override def transform(srcPts: Array[Float], srcOff: Int, dstPts: Array[Float], dstOff: Int, numPts: Int): Unit
override def transform(srcPts: Array[Float], srcOff: Int, dstPts: Array[Double], dstOff: Int, numPts: Int): Unit
override def transform(srcPts: Array[Double], srcOff: Int, dstPts: Array[Float], dstOff: Int, numPts: Int): Unit
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/SnapTransform.scala:46  (+4 more definition site/overload)_

### Goal
Apply a coordinate transform to one or more point coordinates (in-place or into another array) as used in RDPro/Beast raster metadata reprojection/rescaling workflows.

### Parameters
- `srcPts` (`Array[Double]`): Source coordinate array containing point ordinates to transform.
- `srcOff` (`Int`): Start offset in `srcPts` where the first source point ordinates begin.
- `dstPts` (`Array[Double]`): Destination coordinate array where transformed ordinates are written.
- `dstOff` (`Int`): Start offset in `dstPts` where the first transformed point ordinates will be written.
- `numPts` (`Int`): Number of points to transform.

### Input
Caller must provide numeric coordinate arrays and valid offsets/count for the selected overload.  
From tested usage in Beast, the call is made on a transform instance (e.g., `metadata2.g2m.transform(...)`) after raster metadata operations such as `rescale`/`reproject`.

Preconditions visible from project context/tests:
- The receiver transform object must already be constructed/available (e.g., `g2m` from `RasterMetadata`).
- Offsets and point count must be consistent with source/destination array sizes.
- If performing CRS alignment in broader workflows, ensure datasets are reshaped/reprojected beforehand when metadata/CRS/resolution differ (per RDPro compatibility rules).

### Output
Returns `Unit` — transformed coordinates are written into `dstPts` (or same array when source and destination are the same array), not returned as a separate value.

### Valid Call Patterns
```scala
val point = Array[Double](0, 0)
metadata2.g2m.transform(point, 0, point, 0, 1)
```

```scala
val point1 = new Point2D.Double(0, 0)
metadata2.g2m.transform(point1, point1)
```

### LLM Instruction Prompt
- Call `transform` as an instance method on an existing transform object (verified form: `metadata2.g2m.transform(...)`).
- Use one of the documented overloads only.
- For the array overload, pass arrays plus `srcOff`, `dstOff`, and `numPts`; do not invent extra parameters.
- Remember it returns `Unit`; read results from destination arguments.
- In raster pipelines, handle CRS/resolution/tile compatibility using reshape/reproject operations before downstream overlay/join operations.

### Prompt Snippet
```text
Use metadata2.g2m.transform(point, 0, point, 0, 1) to transform one point in-place.
`point` is Array[Double], offsets are 0, and numPts is 1. The method returns Unit and mutates destination coordinates.
```

### Common Failure Modes
- Using a bare `transform(...)` call without a receiver object; this usually will not compile.
- Expecting a returned coordinate array/value from the `Array[Double]` overload; output is written into `dstPts`.
- Passing invalid offsets or `numPts` relative to array lengths.
- Mixing incompatible raster datasets later in pipeline (different CRS/resolution/tile size) without prior reshape/reproject, causing downstream operation issues.

### Fix Code Hint
```scala
// Correct instance call form and in-place write
val point = Array[Double](0, 0)
metadata2.g2m.transform(point, 0, point, 0, 1)
println(point.mkString(","))
```

## API Test: `trimLineSegment`

### Signature
```scala
private[davinci] def trimLineSegment(x1: Double, y1: Double, x2: Double, y2: Double): (Double, Double, Double, Double)
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/IntermediateVectorTile.scala:146_

_Source doc:_ Trim a line segment with the boundaries of this tile, i.e., the box (-buffer, -buffer, resolution + buffer, resolution + buffer) @param x1 the x-coordinate of the first point @param y1 the y-coordinate of the first point @param x2 the x-coordinate of the second point @param y2 the y-coordinate of the second point @return the given line segment trimmed to the tile boundaries or null if the line segment is completely outside

### Goal
Clip a 2D line segment to the current `IntermediateVectorTile` bounds (`-buffer` to `resolution + buffer`) so only the in-tile portion is kept.

### Parameters
- `x1` (`Double`): x-coordinate of the first endpoint of the input segment, in the tile’s coordinate space.
- `y1` (`Double`): y-coordinate of the first endpoint of the input segment, in the tile’s coordinate space.
- `x2` (`Double`): x-coordinate of the second endpoint of the input segment, in the tile’s coordinate space.
- `y2` (`Double`): y-coordinate of the second endpoint of the input segment, in the tile’s coordinate space.

### Input
A caller must provide four `Double` coordinates representing one line segment endpoint pair.  
This is an internal visualization/tile operation (`private[davinci]`) and is called on an `IntermediateVectorTile` instance, as in the test suite.

Preconditions:
- Coordinates must be in the same coordinate system used by that tile.
- The clipping region is defined by the tile instance: `(-buffer, -buffer, resolution + buffer, resolution + buffer)`.

No file formats are involved for this method directly.

### Output
Returns `(Double, Double, Double, Double)` — the trimmed segment endpoints `(x1', y1', x2', y2')` after clipping to tile boundaries.  
Per source doc and tests, it can return `null` when the segment is completely outside the tile clipping box.

### Valid Call Patterns
```scala
val tile = new IntermediateVectorTile(10, 2)
assertResult((1, 2, 3, 4))(tile.trimLineSegment(1, 2, 3, 4))
assertResult(null)(tile.trimLineSegment(-4, 2, -3, 5))
assertResult((-2, 3, 2, 5))(tile.trimLineSegment(-4, 2, 2, 5))
assertResult((6, 8, 4, 12))(tile.trimLineSegment(6, 8, 3, 14))
```

### LLM Instruction Prompt
- Call it as an instance method on an `IntermediateVectorTile`: `tile.trimLineSegment(x1, y1, x2, y2)`.
- Pass exactly 4 arguments, all `Double`-compatible numeric values.
- Handle `null` return (segment fully outside).
- Do not invent extra parameters (no CRS, no metadata, no options map).

### Prompt Snippet
```text
Given an IntermediateVectorTile instance `tile`, clip one segment with:
`tile.trimLineSegment(x1, y1, x2, y2)`.
Inputs are tile-space endpoint coordinates. The return is either a tuple
(x1', y1', x2', y2') for the clipped segment or null if fully outside.
```

### Common Failure Modes
- Calling without a receiver (e.g., bare `trimLineSegment(...)`) instead of `tile.trimLineSegment(...)`.
- Assuming it always returns a tuple; it may return `null` for fully outside segments.
- Passing coordinates in a different coordinate space than the tile’s internal one, leading to incorrect clipping.

### Fix Code Hint
```scala
val tile = new IntermediateVectorTile(10, 2)
val clipped = tile.trimLineSegment(x1, y1, x2, y2)
if (clipped != null) {
  val (cx1, cy1, cx2, cy2) = clipped
  // use clipped segment
} else {
  // segment is completely outside tile bounds
}
```

## API Test: `uniform`

### Signature
```scala
def uniform(cardinality: Long): JavaSpatialRDD
def uniform(cardinality: Long): SpatialRDD
def uniform(a: Double, b: Double): Double
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/generator/SpatialGenerator.scala:37  (+2 more definition site/overload)_

_Source doc:_ Generate a random value in the range [a, b) from a uniform distribution

### Goal
Generate one random numeric sample from a uniform distribution over a half-open interval `[a, b)`.

### Parameters
- `a` (`Double`): Lower bound of the random range (inclusive).
- `b` (`Double`): Upper bound of the random range (exclusive).

### Input
Two scalar `Double` bounds are required; no raster/vector file input is involved for this overload.  
Preconditions are not explicitly documented beyond the source doc range contract `[a, b)`.

### Output
Returns `Double` — one random value sampled uniformly from the interval `[a, b)`.

### Valid Call Patterns
```scala
import edu.ucr.cs.bdlab.beast._
import edu.ucr.cs.bdlab.beast.generator._

val randomPoints: RDD[IFeature] = sc.generateSpatialData.uniform(1000000000)

import edu.ucr.cs.bdlab.beast._
val randomData: SpatialRDD = sc.generateSpatialData.uniform(1000000000)
```

### LLM Instruction Prompt
- Use `uniform(a: Double, b: Double)` only when you need a single random `Double` in `[a, b)`.
- Do not replace this with `uniform(cardinality: Long)`, which is a different overload returning spatial RDDs.
- Keep receiver-qualified calls (e.g., `value.uniform(...)`) when using generator APIs; do not emit bare `uniform(...)` unless a receiver is in scope.
- Do not invent extra parameters, seeds, or distribution options for this method.

### Prompt Snippet
```text
Use `uniform(a: Double, b: Double)` to draw one random Double in [a, b). 
If generating synthetic spatial features, use the documented receiver form 
`sc.generateSpatialData.uniform(cardinality)` instead of the Double-returning overload.
```

### Common Failure Modes
- Calling the wrong overload (`uniform(cardinality: Long)`) when a scalar random `Double` is needed.
- Assuming this overload reads raster/vector inputs; it does not.
- Emitting unqualified `uniform(...)` with no valid receiver/import context.

### Fix Code Hint
```scala
// Scalar random sample in [a, b)
val x: Double = uniform(0.0, 1.0)

// Spatial data generation overload (different return type)
import edu.ucr.cs.bdlab.beast._
val randomData: SpatialRDD = sc.generateSpatialData.uniform(1000000000)
```

## API Test: `uniformHistogramCount`

### Signature
```scala
def uniformHistogramCount(histogramSize: Array[Int], prefixSum: Boolean = false): AbstractHistogram
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/CGOperationsMixin.scala:67_

_Source doc:_ Computes a uniform histogram with the given size that counts number of features in each cell @param histogramSize the size of the histogram as the number of partitions along each dimension @param prefixSum     compute the prefix sum on the result to speed up range tests @return the created histogram

### Goal
Compute a uniform grid histogram over spatial features, where each grid cell stores the count of features, with optional prefix-sum acceleration for fast range-count queries.

### Parameters
- `histogramSize` (`Array[Int]`): the histogram grid size as the number of partitions along each dimension (for example, `Array(100, 100)` in 2D).
- `prefixSum` (`Boolean`), default `false`: whether to convert the histogram to prefix-sum form to speed up range tests (e.g., range count lookups in constant time).

### Input
Call this on a spatial feature dataset receiver (as shown: `features.uniformHistogramCount(...)`, `polygons.uniformHistogramCount(...)`), i.e., an object that has `CGOperationsMixin` methods available.

Preconditions and compatibility notes from available docs:
- The `histogramSize` dimensionality should match the dataset dimensionality used for the histogram (examples are 2D: `Array(100, 100)`).
- No raster pixel type-selection rule applies to this method directly (that rule is for typed raster loads such as `sc.geoTiff[T]`).
- If you need fast range tests on the resulting histogram, set `prefixSum = true` at creation time.

### Output
Returns `AbstractHistogram` — an in-memory histogram object representing feature counts per uniform grid cell.  
If created with `prefixSum = true`, it is prepared for faster range queries such as:
`histogram.getValue(Array(4, 3), Array(10, 10))`.

### Valid Call Patterns
```scala
val countHistogram = features.uniformHistogramCount(Array(100, 100))
val sizeHistogram = features.uniformHistogramSize(Array(100, 100))

val histogram = polygons.uniformHistogramCount(Array(100, 100), prefixSum = true)
// The following function will run in constant time regardless of the size of the range
histogram.getValue(Array(4, 3), Array(10, 10))
```

### LLM Instruction Prompt
- Use the instance call form exactly: `value.uniformHistogramCount(...)` (not a bare/global call).
- Pass `histogramSize` as `Array[Int]` in the same argument position/order as the signature.
- Use `prefixSum = true` only when range-test performance is needed; otherwise rely on default `false`.
- Do not invent extra parameters, overloads, or return types.
- Keep the receiver as an existing spatial feature collection variable (e.g., `features`, `polygons`).

### Prompt Snippet
```text
Given a spatial feature dataset variable (for example `features`), compute a count histogram with:
`features.uniformHistogramCount(Array(100, 100))`.
If fast range-count queries are needed, use:
`features.uniformHistogramCount(Array(100, 100), prefixSum = true)`.
Do not add any extra arguments or change the return type (`AbstractHistogram`).
```

### Common Failure Modes
- Passing a non-`Array[Int]` histogram size (wrong type/shape).
- Using a bare `uniformHistogramCount(...)` call without a valid receiver that provides `CGOperationsMixin`.
- Using histogram bounds/ranges later with dimensionality inconsistent with the histogram configuration.
- Expecting file output: this API returns an in-memory `AbstractHistogram`; saving/export is separate.

### Fix Code Hint
```scala
// Correct receiver-based call with required argument type
val histogram = polygons.uniformHistogramCount(Array(100, 100), prefixSum = true)

// Example range query on prefix-sum histogram
val count = histogram.getValue(Array(4, 3), Array(10, 10))
```

## API Test: `uniformHistogramSize`

### Signature
```scala
def uniformHistogramSize(histogramSize: Array[Int], prefixSum: Boolean = false, sizeFunction: IFeature => Int = _.getStorageSize): AbstractHistogram
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/CGOperationsMixin.scala:78_

_Source doc:_ Computes a uniform histogram with the given size that calculates the size of the data in each cell @param histogramSize the size of the histogram as the number of partitions along each dimension @param prefixSum     compute the prefix sum on the result to speed up range tests @param sizeFunction  an optional function that computes the size of a feature. @return the created histogram

### Goal
Compute a uniform grid histogram over spatial features where each cell stores accumulated feature **size** (not just count), optionally as a prefix-sum histogram for faster range tests.

### Parameters
- `histogramSize` (`Array[Int]`): the histogram grid shape, i.e., number of partitions (cells) along each dimension.
- `prefixSum` (`Boolean`), default `false`: if `true`, computes prefix sums on the histogram result to speed up range tests.
- `sizeFunction` (`IFeature => Int`), default `_.getStorageSize`: function used to compute each feature’s size contribution to histogram cells.

### Input
Call this on a feature collection/RDD receiver that supports `CGOperationsMixin` methods (as shown by `features.uniformHistogramSize(...)` usage).  
The method itself does not take file paths or formats directly; loading data (e.g., shapefile/GeoJSON/CSV-WKT) happens before this call using Beast I/O APIs.

Preconditions from the API facts:
- `histogramSize` must be provided and should match the dimensionality of your data space (number of partitions per dimension).
- `sizeFunction` must be a valid `IFeature => Int`.

### Output
Returns `AbstractHistogram` — a histogram object representing the accumulated **feature size per uniform grid cell**; if `prefixSum = true`, it stores the prefix-summed form for faster range testing.

### Valid Call Patterns
```scala
val countHistogram = features.uniformHistogramCount(Array(100, 100))
val sizeHistogram = features.uniformHistogramSize(Array(100, 100))

val sizeHistogram = features.uniformHistogramSize(Array(100, 100),
    sizeFunction = new FeatureWriterSizeFunction("iformat" -> "geojson"))
```

### LLM Instruction Prompt
- Use the instance call form exactly as documented: `features.uniformHistogramSize(...)`.
- Pass `histogramSize` as `Array[Int]`.
- Only use supported optional arguments: `prefixSum` and `sizeFunction`.
- Do not invent extra parameters, return types, or alternate call receivers.
- If customizing feature-size logic, provide a function of type `IFeature => Int`.

### Prompt Snippet
```text
Given a feature dataset `features`, compute a size-based uniform histogram using:
`features.uniformHistogramSize(Array(nx, ny), prefixSum = false)`.
Optionally pass `sizeFunction: IFeature => Int` (for example, FeatureWriterSizeFunction with iformat options).
Do not add unsupported arguments.
```

### Common Failure Modes
- Passing a non-`Array[Int]` value for `histogramSize`.
- Using an invalid `sizeFunction` type (must be `IFeature => Int`).
- Calling as a standalone function (`uniformHistogramSize(...)`) instead of on the dataset receiver (`features.uniformHistogramSize(...)`), which may not compile in user code.

### Fix Code Hint
```scala
// Correct receiver + argument types
val sizeHistogram: AbstractHistogram =
  features.uniformHistogramSize(Array(100, 100), prefixSum = true)

// Custom size function form from docs
val sizeHistogram2: AbstractHistogram =
  features.uniformHistogramSize(
    Array(100, 100),
    sizeFunction = new FeatureWriterSizeFunction("iformat" -> "geojson")
  )
```

## API Test: `using`

### Signature
```scala
def using[A <: AutoCloseable, B](resource: A)
```
_Source: beast/dataExplorer/src/main/scala/edu/ucr/cs/bdlab/beast/dataExplorer/DatasetProcessor.scala:606  (+1 more definition site/overload)_

### Goal
Safely run a block of code with an `AutoCloseable` resource (such as JDBC connections/statements/result sets) in Beast/RDPro workflows, ensuring the resource is scoped and then closed.

### Parameters
- `resource` (`A`): The open `AutoCloseable` instance to use inside the block (for example, `DriverManager.getConnection(...)`, `dbConnection.prepareStatement(...)`, `dbConnection.createStatement()`, or `statement.executeQuery(...)` as shown in tests).

### Input
A valid, already-created object of type `A <: AutoCloseable`, plus a function block (second parameter list, shown in tested usage) that receives that resource and performs work.

Preconditions from verified usage:
- The passed object must implement `AutoCloseable`.
- Resource creation must succeed before calling `using` (e.g., JDBC driver loaded, connection string valid).
- The tested/authoritative call form is a top-level `using(resource) { ... }` shape.

### Output
Returns `unspecified` — the provided API facts do not declare a concrete return type in this entry. From the generic signature, the helper is parameterized by `B`, so the block computes a value of that type, but exact documented return semantics are not specified in the provided source facts.

### Valid Call Patterns
```scala
using(DriverManager.getConnection(s"jdbc:h2:${datasetsPath}/beast", "sa", "")) {dbConnection =>
  DatasetProcessor.createDB(dbConnection)
  val insertSQL: String = "INSERT INTO datasets(name, dir_name, source_uri, source_format, status) VALUES (?, ?, ?, ?, ?)"
  using(dbConnection.prepareStatement(insertSQL)) { insertStatement =>
    insertStatement.setString(1, "cities")
    insertStatement.setString(2, "cities")
    insertStatement.setString(3, testData.getPath)
    insertStatement.setString(4, "shapefile")
    insertStatement.setString(5, "created")
    insertStatement.executeUpdate()
  }
}
```

```scala
using(dbConnection.createStatement()) { statement =>
  using(statement.executeQuery("SELECT * FROM datasets WHERE name='cities'")) { data =>
    assert(data.next())
    val status = data.getString("status")
    assertResult("ready")(status)
  }
}
```

### LLM Instruction Prompt
- Call it in the tested form: `using(resource) { r => ... }`.
- Pass only objects that are `AutoCloseable`.
- Nest `using` for dependent resources (connection → statement → result set).
- Do not invent alternate receiver forms unless present in project code.
- Ensure resource construction is done before `using(...)`.

### Prompt Snippet
```text
Use `using(resource) { r => ... }` with an `AutoCloseable` resource (e.g., JDBC Connection/PreparedStatement/ResultSet), and nest `using` blocks for child resources. Follow the exact tested call shape.
```

### Common Failure Modes
- Passing a non-`AutoCloseable` object as `resource` (type bound violation).
- Omitting the function block after `using(resource)`.
- Using an invalid/uninitialized JDBC resource (e.g., driver not loaded, bad URL) before entering `using`.
- Inventing undocumented call shapes (e.g., different receiver/qualifier form not shown in tests).

### Fix Code Hint
```scala
Class.forName("org.h2.Driver")

using(DriverManager.getConnection(s"jdbc:h2:${datasetsPath}/beast", "sa", "")) { dbConnection =>
  val insertSQL = "INSERT INTO datasets(name, dir_name, source_uri, source_format, status) VALUES (?, ?, ?, ?, ?)"
  using(dbConnection.prepareStatement(insertSQL)) { insertStatement =>
    insertStatement.setString(1, "cities")
    insertStatement.setString(2, "cities")
    insertStatement.setString(3, testData.getPath)
    insertStatement.setString(4, "shapefile")
    insertStatement.setString(5, "created")
    insertStatement.executeUpdate()
  }
}
```

## API Test: `value`

### Signature
```scala
override def value: Summary
override def value: Array[PointND]
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/synopses/SummaryAccumulator.scala:68  (+1 more definition site/overload)_

### Goal
Return the current accumulated result from an internal Beast/RDPro accumulator, either as a `Summary` or as an `Array[PointND]` depending on the concrete implementation.

### Parameters
_None._

### Input
This method takes no explicit arguments.  
The effective input is the accumulator’s internal state, which must have been populated earlier by the owning workflow.

From the provided sources, there is no documented README or test-suite call site for `value`, so concrete receiver type and lifecycle preconditions are not explicitly documented here.

### Output
Returns `Summary` — in the `Summary` overload, this is the current aggregate synopsis object held by the accumulator.  
In the other overload, returns `Array[PointND]` — the current accumulated points as an array.

### Valid Call Patterns
```scala
// Inferred from signature only (no verbatim README/test call form available):
acc.value
```

### LLM Instruction Prompt
- Call `value` as a zero-argument member access on an existing accumulator instance (`receiver.value`).
- Do not add arguments.
- Do not assume which overload (`Summary` vs `Array[PointND]`) is returned; use the static type of the receiver to disambiguate.
- If receiver type is unknown, ask for it before generating downstream code that depends on the returned type.

### Prompt Snippet
```text
Use `value` only as `receiver.value` (no parameters). Determine the return type from the receiver’s concrete type: it is either `Summary` or `Array[PointND]`. If that type is not known, request it instead of guessing.
```

### Common Failure Modes
- Assuming `value(...)` takes parameters.
- Assuming the return type is always `Summary` (or always `Array[PointND]`) without checking receiver type.
- Calling `value` before any accumulation step and expecting meaningful populated results (behavior not specified in provided docs).

### Fix Code Hint
```scala
// Ensure the receiver type is known, then call zero-arg accessor style.
val out = acc.value
```

## API Test: `visualize`

### Signature
```scala
private[dataExplorer] def visualize(): Unit
```
_Source: beast/dataExplorer/src/main/scala/edu/ucr/cs/bdlab/beast/dataExplorer/DatasetProcessor.scala:357_

_Source doc:_ Build the visualization index for this dataset

### Goal
Build the dataset’s visualization index in Beast’s data-explorer workflow so the dataset can be served/viewed through Beast visualization pipelines.

### Parameters
_None._

### Input
`visualize` takes no explicit parameters; it operates on the current `DatasetProcessor` instance state.

From the provided facts, the caller must ensure:

- A valid `DatasetProcessor` object already exists (as shown in tests).
- Dataset metadata/storage is already prepared in the processor workflow (the method is part of step-by-step dataset processing).
- Because this is a visualization-index build step, the dataset should already be available locally/processed before visualization is attempted (the test shows prior steps like `copyDataToLocal()` and `decompressDatasetFiles()` in the same workflow).
- No file-format-specific arguments are passed to this method directly (format handling is upstream in dataset ingestion/processing).

Unknown from provided sources:
- Exact accepted source formats at this specific method boundary.
- Whether it builds PNG tiles, pyramid zip, MVT, or internal index artifacts specifically.
- Whether Beast server must be running for this method itself (server requirement is documented for efficient visualization consumption, not explicitly for this call).

### Output
Returns `Unit` — it produces side effects (building visualization index artifacts for the dataset) and does not return a value.

### Valid Call Patterns
```scala
// Inferred from signature and verified receiver style from test setup (instance method call form)
datasetProcessor.visualize()
```

### LLM Instruction Prompt
- Call this only as an instance method on an existing `DatasetProcessor` (e.g., `datasetProcessor.visualize()`).
- Do not add arguments; signature is exactly `visualize(): Unit`.
- Place it after dataset preparation steps in the processing pipeline.
- Do not assume a returned object/path; it returns `Unit` and writes artifacts via side effects.
- If workflow needs portable vs server-backed visualization behavior, configure that in the relevant visualization tooling/steps; `visualize()` itself exposes no options in this signature.

### Prompt Snippet
```text
Given an existing DatasetProcessor instance named datasetProcessor that has already prepared dataset files, call:
datasetProcessor.visualize()
Do not pass any arguments and do not assign a return value (method returns Unit).
```

### Common Failure Modes
- Calling `visualize` before dataset preparation steps complete (missing local/decompressed/processed inputs in the dataset workflow).
- Attempting to pass parameters (none are supported).
- Expecting a return value containing visualization output location/metadata (it returns `Unit`).
- Trying to call it from outside accessible scope without proper package visibility handling (`private[dataExplorer]`).

### Fix Code Hint
```scala
// Ensure processor is created and prep steps are done first, then call visualize with no args
datasetProcessor.copyDataToLocal()
datasetProcessor.decompressDatasetFiles()
datasetProcessor.visualize()
```

## API Test: `writeSpatialFile`

### Signature
```scala
def writeSpatialFile(filename: String, oformat: String, opts: BeastOptions = new BeastOptions): Unit
def writeSpatialFile(rdd: JavaSpatialRDD, filename: String, oformat: String, opts: BeastOptions): Unit
def writeSpatialFile(rdd: JavaSpatialRDD, filename: String, oformat: String): Unit
```
_Source: beast/beast-spark/src/main/scala/edu/ucr/cs/bdlab/beast/JavaSpatialRDDHelper.scala:94  (+2 more definition site/overload)_

_Source doc:_ Write this RDD as a spatial file with the given format and additional options @param filename the output file name @param oformat the output file format (short name) @param opts additional user options

### Goal
Write a spatial RDD to disk in a specified spatial output format (by short format name), with optional writer options.

### Parameters
- `rdd` (`JavaSpatialRDD`): The Java spatial RDD to write (used in the static/helper overloads).
- `filename` (`String`): Output file path/name to write.
- `oformat` (`String`): Output format short name (for example, `"envelope"` as shown in project usage).
- `opts` (`BeastOptions`): Additional write options.

### Input
A spatial RDD (Scala `SpatialRDD` in instance form, or `JavaSpatialRDD` in helper form), plus:
- an output target path (`filename`),
- an output format short name (`oformat`),
- optional `BeastOptions`.

Documented/project-grounded spatial format ecosystem includes outputs such as CSV point/WKT/envelope, Shapefile, zipshapefile, GeoJSON, KML, KMZ, while concrete `writeSpatialFile` examples here use `"envelope"`.

No extra compatibility/type-parameter precondition is documented specifically for `writeSpatialFile` beyond providing a valid spatial RDD and a supported output format short name.

### Output
Returns `Unit` — the method performs side effects by writing files to the given output location in the requested spatial format; no in-memory value is returned.

### Valid Call Patterns
```scala
sparkContext.parallelize(r1).asInstanceOf[SpatialRDD].spatialPartition(grid).writeSpatialFile(index1Path, "envelope")
```

```scala
records.writeSpatialFile("output.csv", "envelope", "oseparator" -> ",")
```

```scala
JavaSpatialRDDHelper.writeSpatialFile(records, "output.csv", "envelope", new BeastOptions("oseparator:,");
```

### LLM Instruction Prompt
- Use an existing `SpatialRDD`/`JavaSpatialRDD` receiver; do not emit a bare `writeSpatialFile(...)` call.
- Keep argument order exactly as documented: `(filename, oformat, opts)` for instance form, or `(rdd, filename, oformat, opts)` for helper form.
- Pass `oformat` as a short format name string (e.g., `"envelope"` in verified examples).
- Use `BeastOptions` for extra options when needed; otherwise use overload/default without extra options.
- Do not invent undocumented parameters or return handling (method returns `Unit`).

### Prompt Snippet
```text
Write the indexed SpatialRDD to disk using the instance form:
spatialRdd.writeSpatialFile(outputPath, "envelope")
If delimiter/options are needed, pass BeastOptions (or the documented tuple-style options form shown in README examples).
```

### Common Failure Modes
- Calling `writeSpatialFile` without a spatial RDD receiver (won’t match instance/helper API shape).
- Wrong argument order (e.g., swapping `filename` and `oformat`).
- Unsupported or misspelled `oformat` short name.
- Supplying non-`BeastOptions` in helper overloads that require `BeastOptions`.

### Fix Code Hint
```scala
// Instance form (Scala SpatialRDD)
val indexPath = new File(scratchDir, "dataset1_index").getPath
sparkContext.parallelize(r1)
  .asInstanceOf[SpatialRDD]
  .spatialPartition(grid)
  .writeSpatialFile(indexPath, "envelope")

// Helper form (JavaSpatialRDD)
JavaSpatialRDDHelper.writeSpatialFile(records, "output.csv", "envelope", new BeastOptions("oseparator:,"))
```

## API Test: `x1`

### Signature
```scala
def x1: Int
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/SlidingWindowTile.scala:14_

### Goal
Return the tile/window minimum X grid coordinate (`x1`) used as a raster index boundary in RDPro/Raptor tile processing.

### Parameters
_None._

### Input
`x1` is a parameterless accessor, so the caller provides no direct arguments.  
Precondition: you must call it on a valid tile/window instance that defines spatial index bounds (as seen in tile iteration patterns like `tile.x1 to tile.x2` in tests).  
No file format is passed directly to `x1`; any raster loading/type-selection rules (e.g., `sc.geoTiff[T]`) apply earlier when creating raster/tile objects, not to this accessor itself.

### Output
Returns `Int` — the lower (start) X index of the tile/window extent in raster grid coordinates.

### Valid Call Patterns
```scala
tile.x1
```
*(Inferred from signature and grounded by test usage patterns that iterate with `tile.x1 to tile.x2`; no direct `x1` call snippet was provided.)*

### LLM Instruction Prompt
- Call `x1` only as a member accessor on a tile/window object (e.g., `tile.x1`), not as a standalone function.
- Do not add arguments; the API takes none.
- Use it with matching bound accessors (typically together with `x2`, `y1`, `y2`) when iterating raster cells.

### Prompt Snippet
```text
Given an existing raster tile object, read its left boundary grid index using `tile.x1` (no arguments), then use it in loops like `for (x <- tile.x1 to tile.x2)`.
```

### Common Failure Modes
- Calling `x1` as a free function (`x1`) instead of on an instance (`tile.x1`), which will not resolve in Scala.
- Assuming `x1` is a world-coordinate longitude; it is an integer grid index boundary.
- Using `x1` before obtaining a valid tile/window object from upstream raster operations.

### Fix Code Hint
```scala
// Correct: call on an existing tile instance
val startX: Int = tile.x1

// Typical usage with other bounds
for (y <- tile.y1 to tile.y2; x <- tile.x1 to tile.x2) {
  if (tile.isDefined(x, y)) {
    // process pixel
  }
}
```

## API Test: `x2`

### Signature
```scala
def x2: Int
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/SlidingWindowTile.scala:16_

### Goal
Return the tile/window’s `x2` boundary coordinate as an integer in RDPro/Beast raster tile processing.

### Parameters
_None._

### Input
Call this on an existing tile/window object that defines spatial index bounds (for example, tile-like objects used in Raptor/RDPro tests iterate from `x1` to `x2` and `y1` to `y2`).  
No file path or format is passed directly to `x2`.

Preconditions:
- The receiver object must be a valid instance that has this method/property available.
- Boundary compatibility rules for raster operations (same metadata/resolution/CRS/tile size) are relevant to operations like `overlay`/`reshape`, but are **not directly validated by `x2`** itself.

### Output
Returns `Int` — the `x2` boundary value (the second/end x-index bound) of the receiver tile/window.

### Valid Call Patterns
```scala
tile.x2
```
```scala
tile.setPixelValue(tile.x2, tile.y2, Array[Byte](10, 20, 30))
```

### LLM Instruction Prompt
- Use `x2` as a zero-argument member access on a tile/window receiver (e.g., `tile.x2`), not as a function with parameters.
- Do not invent arguments or alternate overloads (none are documented).
- Ensure the receiver is a tile/window object from RDPro/Raptor context.

### Prompt Snippet
```text
Given a valid RDPro/Raptor tile object `tile`, read its ending x-bound with `tile.x2` (no parentheses or arguments), and use that Int for boundary-aware pixel logic.
```

### Common Failure Modes
- Calling `x2` on the wrong receiver type (object does not define `x2`).
- Inventing a parameterized form like `x2(...)` even though signature is `def x2: Int`.
- Assuming `x2` performs reprojection/reshaping/metadata alignment (it does not; it only returns a bound value).

### Fix Code Hint
```scala
// Correct: access as a no-arg member on a valid tile/window receiver
val endX: Int = tile.x2
```

## API Test: `y1`

### Signature
```scala
def y1: Int
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/SlidingWindowTile.scala:15_

### Goal
Return the starting **Y pixel index** (top/bottom bound endpoint in tile index space, depending on tile convention) for an RDPro/Beast tile, used to iterate pixels safely over tile bounds.

### Parameters
_None._

### Input
Call this on a tile instance (as shown in tests: `tile` or `originalTile`) that implements the tile boundary API (`y1`, `y2`, `x1`, `x2`) such as `MemoryTile` / `ITile`.

- No file path or format is passed directly to `y1`.
- In practice, the tile is created from raster metadata (e.g., `RasterMetadata`) and then used in per-pixel loops.
- Preconditions from usage pattern:
  - Use `y1` together with `y2` (and usually `x1`/`x2`) for bounded iteration.
  - If counting/reading actual stored pixels, guard with `isDefined(x, y)` before `getPixelValue(x, y)`.

### Output
Returns `Int` — the tile’s first Y index in pixel coordinates (integer grid index) for iteration bounds.

### Valid Call Patterns
```scala
for (y <- tile.y1 to tile.y2; x <- tile.x1 to tile.x2; if tile.isDefined(x, y))
  pixelCount += 1
```

```scala
for (j <- originalTile.y1 to originalTile.y2; i <- originalTile.x1 to originalTile.x2) {
  assertResult(originalTile.isDefined(i, j), s"Error in defined pixel ($i, $j)")(readTile.isDefined(i, j))
  if (originalTile.isDefined(i, j)) {
    assertResult(originalTile.getPixelValue(i, j), s"Error in pixel value ($i, $j)")(readTile.getPixelValue(i, j))
  }
}
```

### LLM Instruction Prompt
- Call as an instance property with no arguments: `value.y1`.
- Do not invent parameters or alternate overloads.
- Use it as a loop bound with `to value.y2` for full Y-range traversal.
- When reading pixel values, include `isDefined` checks to avoid undefined-pixel access.

### Prompt Snippet
```text
Iterate over tile pixels using tile.y1 to tile.y2 and tile.x1 to tile.x2; check tile.isDefined(x, y) before tile.getPixelValue(x, y).
```

### Common Failure Modes
- Calling `y1(...)` with arguments (invalid; method takes none).
- Using `y1` as a global/static function instead of `tile.y1`.
- Iterating only from `0` instead of tile bounds, which can be wrong for some tile layouts.
- Accessing `getPixelValue` without `isDefined` guard when undefined pixels may exist.

### Fix Code Hint
```scala
var pixelCount = 0
for (y <- tile.y1 to tile.y2; x <- tile.x1 to tile.x2) {
  if (tile.isDefined(x, y)) {
    // safe to read/use pixel
    // val v = tile.getPixelValue(x, y)
    pixelCount += 1
  }
}
```

## API Test: `y2`

### Signature
```scala
def y2: Int
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/SlidingWindowTile.scala:17_

### Goal
Return the tile’s ending Y coordinate (inclusive) so raster code can iterate over the tile’s valid row range.

### Parameters
_None._

### Input
Call `y2` on a tile-like raster object that exposes tile bounds (as shown in tests with `MemoryTile`), e.g., `tile.y2`.

Preconditions from validated usage:
- The receiver must be an initialized tile instance (e.g., `MemoryTile[Int]`, `MemoryTile[Array[Byte]]` in tests).
- `y2` is used together with `y1`/`x1`/`x2` for bounded pixel iteration:
  - `for (y <- tile.y1 to tile.y2; x <- tile.x1 to tile.x2; if tile.isDefined(x, y)) ...`

No file-format input is required by `y2` itself.

### Output
Returns `Int` — the maximum Y index of the tile extent, used as the inclusive upper bound for row iteration.

### Valid Call Patterns
```scala
for (y <- tile.y1 to tile.y2; x <- tile.x1 to tile.x2; if tile.isDefined(x, y))
  pixelCount += 1
```

```scala
tile.setPixelValue(tile.x2, tile.y2, Array[Byte](10, 20, 30))
```

### LLM Instruction Prompt
- Call as a property on a tile instance: `tile.y2` (no arguments).
- Use it as an inclusive bound (`to`, not `until`) when reproducing tested iteration patterns.
- Do not invent overloads or parameters; API facts define `def y2: Int`.
- Ensure receiver is a valid tile object (as in `MemoryTile` test usage).

### Prompt Snippet
```text
Given a tile instance, read its inclusive bottom row index with `tile.y2` and pair it with `tile.y1`/`tile.x1`/`tile.x2` for bounded pixel traversal.
```

### Common Failure Modes
- Calling `y2` like a method with arguments (e.g., `tile.y2(...)`) — invalid; it has no parameters.
- Using `until tile.y2` and unintentionally skipping the last row.
- Calling on a non-tile receiver that does not define `y2`.

### Fix Code Hint
```scala
var pixelCount = 0
for (y <- tile.y1 to tile.y2; x <- tile.x1 to tile.x2; if tile.isDefined(x, y))
  pixelCount += 1
```

## API Test: `zigzagDecode`

### Signature
```scala
def zigzagDecode(x: Int): Int
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/VectorLayerBuilder.scala:150_

_Source doc:_ Decodes a value from Zigzag encoding

### Goal
Decode a Zigzag-encoded integer (as used in vector-tile geometry command streams) back to its signed integer value.

### Parameters
- `x` (`Int`): A Zigzag-encoded integer value to decode.

### Input
`zigzagDecode` takes a single in-memory `Int`; it does not read raster/vector files directly.

Preconditions from available usage:
- Pass an integer that is actually Zigzag-encoded (e.g., geometry entries read from a vector tile feature geometry stream in Davinci tests).
- Call form verified by tests uses the object receiver `VectorLayerBuilder.zigzagDecode(...)`.

### Output
Returns `Int` — the decoded signed integer represented by the Zigzag-encoded input value.

### Valid Call Patterns
```scala
val x = VectorLayerBuilder.zigzagDecode(feature.getGeometry(1))
val y = VectorLayerBuilder.zigzagDecode(feature.getGeometry(2))
```

### LLM Instruction Prompt
- Use the exact receiver form `VectorLayerBuilder.zigzagDecode(...)` as shown in compiled tests.
- Provide exactly one `Int` argument.
- Only use this function to decode values that were Zigzag-encoded; it is not a generic coordinate transform.
- Do not invent overloads or extra parameters.

### Prompt Snippet
```text
Given a vector-tile feature geometry integer, decode it with:
VectorLayerBuilder.zigzagDecode(encodedValue)
where encodedValue is an Int from feature.getGeometry(i).
```

### Common Failure Modes
- Passing a value that is not Zigzag-encoded, which yields meaningless decoded results.
- Using an unqualified call (e.g., `zigzagDecode(...)`) without the proper receiver/import in scope.
- Assuming this function reads files or performs full geometry decoding; it only decodes one integer.

### Fix Code Hint
```scala
val encoded: Int = feature.getGeometry(1)
val decoded: Int = VectorLayerBuilder.zigzagDecode(encoded)
```

## API Test: `zonalStats2`

### Signature
```scala
def zonalStats2[T](zones: RDD[IFeature], raster: RDD[ITile[T]], collectorClass: Class[_ <: Collector], opts: BeastOptions, numTiles: LongAccumulator = null)
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/ZonalStatistics.scala:128_

_Source doc:_ Computes zonal statistics between a set of zones (polygons) and a raster file given by its path and a layer in that file. The result is an RDD of pairs of a feature and a collector value @param zones a set of polygons that represent the regions or zones @param raster the RDD of tiles @param collectorClass the class that collects the pixel values to compute the statistics @param opts additional user-defined options @param numTiles an optional accumulator to collect the total number of processed tiles @return a set of (Feature, Statistics)

### Goal
Compute distributed zonal statistics by aggregating raster tile pixel values per polygon zone using a user-selected `Collector` implementation.

### Parameters
- `zones` (`RDD[IFeature]`): Polygon features representing zones/regions to aggregate over.
- `raster` (`RDD[ITile[T]]`): Raster tiles as an RDD; pixel type `T` must match the actual raster pixel type used when loading.
- `collectorClass` (`Class[_ <: Collector],
                  opts: BeastOptions, numTiles: LongAccumulator`), default `null`: `collectorClass` is the collector implementation class (for example `classOf[Statistics]`) that defines how pixel values are accumulated; `opts` provides runtime options; `numTiles` is optional and can be `null` to skip tile-count accumulation.

### Input
- `zones`: an `RDD[IFeature]` of polygons (tests use shapefile-derived features).
- `raster`: an `RDD[ITile[T]]` (tests use `new RasterFileRDD[Int](...)` from a GeoTIFF).
- Formats in project context: RDPro raster inputs include GeoTIFF/HDF; vector inputs include shapefile and others.
- Preconditions/rules:
  - Use a raster pixel type `T` that matches real raster data type (critical typed-load rule in project docs).
  - Zones and raster should be in compatible CRS; tests explicitly reproject polygons (`Reprojector.reprojectRDD`) before calling and still use the same call form.
  - `collectorClass` must be a subtype of `Collector`.

### Output
Returns `unspecified` — per source doc and passing tests, the returned value is an RDD of pairs `(IFeature, Collector)` (e.g., feature with its `Statistics` collector result), which you can map/collect/sort for downstream analysis.

### Valid Call Patterns
```scala
val zsResults: Array[Collector] =
  ZonalStatistics.zonalStats2(polygons, raster, classOf[Statistics], new BeastOptions())
    .map(fc => (fc._1.getAs[Int]("index"), fc._2))
    .collect
    .sortBy(_._1)
    .map(_._2)
```

```scala
val zsResults: Array[Collector] =
  ZonalStatistics.zonalStats2(projectedPolygons, raster, classOf[Statistics], new BeastOptions())
    .map(fc => (fc._1.getAs[Int]("index"), fc._2))
    .collect
    .sortBy(_._1)
    .map(_._2)
```

### LLM Instruction Prompt
- Call exactly as `ZonalStatistics.zonalStats2(zones, raster, collectorClass, opts)` (or with optional `numTiles` as 5th arg).
- Pass `zones` as `RDD[IFeature]` polygon zones.
- Pass `raster` as `RDD[ITile[T]]` with correct pixel type `T`.
- Pass a valid collector class subtype, e.g., `classOf[Statistics]`.
- Ensure CRS compatibility between zones and raster (reproject zones first when needed).

### Prompt Snippet
```text
Use ZonalStatistics.zonalStats2(zonesRDD, rasterTilesRDD, classOf[Statistics], new BeastOptions()).
`zonesRDD` must be RDD[IFeature] polygons, `rasterTilesRDD` must be RDD[ITile[T]] with correct T for the raster pixel type.
If CRS differs, reproject zones before zonalStats2.
The result is an RDD of (feature, collector); map/cast collector to read stats.
```

### Common Failure Modes
- Pixel type mismatch in `RDD[ITile[T]]` (wrong `T`) causing incorrect behavior or failures.
- Passing non-polygon or invalid zone features.
- CRS mismatch between zones and raster leading to wrong/empty zonal intersections; fix by reprojection.
- Passing a class that is not a `Collector` subtype for `collectorClass`.

### Fix Code Hint
```scala
// Ensure CRS compatibility (example from tests)
val projectedPolygons: RDD[IFeature] =
  Reprojector.reprojectRDD(polygons, CRSServer.sridToCRS(3857))

// Ensure typed raster tiles (example type Int from tests)
val raster: RDD[ITile[Int]] =
  new RasterFileRDD[Int](sparkContext, rasterPath, new BeastOptions())

val results =
  ZonalStatistics.zonalStats2(projectedPolygons, raster, classOf[Statistics], new BeastOptions())
```

## API Test: `zonalStatsLocal`

### Signature
```scala
def zonalStatsLocal[T](geometries: Array[Geometry], raster: IRasterReader[T], collectorClass: Class[_ <: Collector]) : Array[Collector]
def zonalStatsLocal[T](zones: Array[IFeature], raster: IRasterReader[T], collectorClass: Class[_ <: Collector]) : Array[Collector]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/ZonalStatistics.scala:162  (+1 more definition site/overload)_

_Source doc:_ Run zonal statistics locally in one thread. This is useful when the array of geometries is small and the overhead of partitioning could be high. @param zones the array of features that describe the zones. @param raster the raster reader that points to the raster file being aggregated @param collectorClass the class that computes the statistics @return an array of collectors that is equal in length to the input array of features with the result for each. Features that do not overlap any pixels will have null.

### Goal
Compute zonal statistics for a small in-memory set of zones against a raster using a single-thread local execution path.

### Parameters
- `geometries` (`Array[Geometry]`): Zone geometries to aggregate raster pixels over (for the `Geometry` overload).
- `raster` (`IRasterReader[T]`): An initialized raster reader pointing to the raster to aggregate.
- `collectorClass` (`Class[_ <: Collector]`): Collector implementation class that defines which statistics are computed (for example, `classOf[Statistics]` in tests).

### Input
Provide:
- An array of zones (`Array[Geometry]` or `Array[IFeature]` depending on overload).
- An `IRasterReader[T]` that is already initialized and readable.
- A collector class extending `Collector`.

Preconditions and compatibility notes from project context:
- This method is intended for **small arrays of zones** (local, one-thread execution).
- If your raster source is GeoTIFF loaded elsewhere in RDPro, keep type selection consistent with pixel type (`Int`, `Float`, `Array[Int]`, `Array[Float]`) when constructing/using raster readers in your pipeline.
- The method returns per-zone results aligned with input order; non-overlapping zones produce `null`.

### Output
Returns `Array[Collector]`:
- Length matches the input zones length.
- Each position contains that zone’s aggregation result as a `Collector`.
- Zones that do not overlap raster pixels have `null` in their corresponding position.

### Valid Call Patterns
```scala
val zsResults: Array[Collector] = ZonalStatistics.zonalStatsLocal(features, rasterReader, classOf[Statistics])
  .filter(_ != null)
```

### LLM Instruction Prompt
- Use the receiver exactly as `ZonalStatistics.zonalStatsLocal(...)` when following the verified test call form.
- Pass arguments in this order: `(zones/geometries array, raster reader, collector class)`.
- Ensure `raster` is an `IRasterReader[T]` (initialized before call).
- Handle possible `null` entries in returned `Array[Collector]` for non-overlapping zones.
- Do not invent extra parameters (no Spark partition args, no output path, no options map).

### Prompt Snippet
```text
Call ZonalStatistics.zonalStatsLocal with exactly three arguments:
1) Array[IFeature] or Array[Geometry] zones,
2) initialized IRasterReader[T],
3) Class[_ <: Collector] (e.g., classOf[Statistics]).
Then filter null collectors because zones with no overlapping pixels return null.
```

### Common Failure Modes
- Passing a non-initialized `IRasterReader[T]`.
- Using a collector class that is not a subtype of `Collector`.
- Assuming all returned entries are non-null (non-overlapping zones return `null`).
- Using this local API for very large zone arrays where distributed partitioned workflows are more appropriate.

### Fix Code Hint
```scala
val zsResults: Array[Collector] =
  ZonalStatistics.zonalStatsLocal(features, rasterReader, classOf[Statistics])

val nonNull: Array[Collector] = zsResults.filter(_ != null)
```

