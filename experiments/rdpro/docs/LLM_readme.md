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

### Signature
```scala
def createSummaryAccumulator(sc: SparkContext) : SummaryAccumulator
def createSummaryAccumulator(sc: SparkContext, sizeFunction: IFeature => Int) : SummaryAccumulator
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/synopses/Summary.scala:422  (+1 more definition site/overload)_

_Source doc:_ Create a summary accumulator that uses the method [[IFeature#getStorageSize]] to accumulate the sizes of the features. @param sc the spark context to register the accumulator to @return the initialized and registered accumulator

### Goal
Create and register a Spark-side `SummaryAccumulator` to aggregate feature summary information (including feature sizes) while processing spatial/vector features in distributed Beast/RDPro workflows.

### Parameters
- `sc` (`SparkContext`): Spark context where the accumulator is initialized and registered.
- `sizeFunction` (`IFeature => Int`): Function that returns an `Int` size for each `IFeature` to be accumulated (source doc notes storage-size accumulation via `IFeature#getStorageSize` behavior).

### Input
A valid Spark `SparkContext` and, for the 2-argument overload, a per-feature size function of type `IFeature => Int`.  
This API itself does not read files directly; you typically apply the accumulator while mapping over loaded features (for example, from `sc.shapefile(...)` as shown in README usage).  
Precondition: you must trigger an action after adding features to the accumulator; otherwise, no distributed computation runs and accumulator values will not be updated.

### Output
Returns `SummaryAccumulator` — an initialized, Spark-registered accumulator object whose `.value` provides the aggregated summary after actions execute.

### Valid Call Patterns
```scala
var features = sparkContext.shapefile("input.zip")
val accumulator = Summary.createSummaryAccumulator(sparkContext)
features = polygons.map(f=> {accumulator.add(f); f})
// ... run an action on features
val summary = accumulator.value
```

### LLM Instruction Prompt
- Use receiver/qualifier exactly as documented: `Summary.createSummaryAccumulator(sparkContext)`.
- Pass a real `SparkContext`; do not substitute `SparkSession` directly.
- If using the 2-argument overload, provide exactly `IFeature => Int` for `sizeFunction`.
- Add features with `accumulator.add(f)` inside a transformation, then run an action before reading `accumulator.value`.
- Do not invent extra parameters, options, or return types.

### Prompt Snippet
```text
Create a SummaryAccumulator with Summary.createSummaryAccumulator(sparkContext), add each IFeature via accumulator.add(f) in an RDD transformation, run an action, then read accumulator.value. If custom sizing is needed, call the overload that takes sizeFunction: IFeature => Int.
```

### Common Failure Modes
- Reading `accumulator.value` before any Spark action runs (value remains unmaterialized/unchanged).
- Passing the wrong context object type (must be `SparkContext`).
- Using an invalid size function type for the overload (must be `IFeature => Int`).
- Calling form that drops the documented receiver (can fail depending on imports/scope).

### Fix Code Hint
```scala
val acc = Summary.createSummaryAccumulator(sparkContext)
val counted = features.map(f => { acc.add(f); f })
counted.count()   // trigger action
val summary = acc.value
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

