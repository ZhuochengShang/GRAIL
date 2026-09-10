# RDPro — LLM_readme

LLM-facing API documentation. Generated from the API surface, project profile, and distilled docs.

## API Test: `addFeature`
_Grounding: doc-repaired from source (docfix)._

### Goal
**ADVANCED/LOW-LEVEL API.** Incrementally adds a spatial feature to an intermediate vector tile during Mapbox Vector Tile (MVT) generation, aggregating or rasterizing it based on capacity thresholds. *Note: Exclude this API from the main user-facing benchmark denominator, as standard users rely on high-level DataFrame actions.*

### Input
**ADVANCED/LOW-LEVEL:** Requires explicit, caller-owned low-level construction of an `IntermediateVectorTile` and an `IFeature`. The feature must contain a valid JTS geometry and an `Array[Any]` for attribute values. 

### Output
Returns the mutated `IntermediateVectorTile` instance (`this`) to allow for method chaining.

### Valid Call Patterns
```scala
import edu.ucr.cs.bdlab.beast.geolite.Feature
import edu.ucr.cs.bdlab.beast.io.FeatureReader
import org.locationtech.jts.geom.CoordinateXY
import edu.ucr.cs.bdlab.davinci.IntermediateVectorTile

// Caller-owned low-level construction
val factory = FeatureReader.DefaultGeometryFactory
val geom = factory.createPoint(new CoordinateXY(1000.0, 1000.0))

// Attribute values MUST be typed as Array[Any] in Scala
val f1 = Feature.create(
  geom,
  Array("id", "name"),
  null,
  Array[Any](1, "point1")
)

// Instantiate the canonical receiver directly (resolution, buffer)
val tile = new IntermediateVectorTile(4096, 16)

// Mutates the tile in place and returns the tile itself
tile.addFeature(f1)
```

### LLM Instruction Prompt
- This is a low-level internal API. Use `IntermediateVectorTile` as the receiver, instantiated directly with `(resolution, buffer)`.
- When constructing the `IFeature` via `Feature.create`, you MUST type the attribute values array explicitly as `Array[Any]`.
- Do not call `.build()` on the tile; `addFeature` mutates the tile in place.

### Prompt Snippet
```text
Construct an `IntermediateVectorTile` (e.g., 4096 resolution, 16 buffer) and populate it by calling `addFeature` with a manually created `IFeature`. Ensure the feature's attribute values are passed strictly as an `Array[Any]`.
```

### Common Failure Modes
- **Type Mismatch on Attribute Array:** Passing an `Array[AnyRef]` to `Feature.create`. Because Scala arrays are invariant, `Array[AnyRef]` cannot be substituted for `Array[Any]`, resulting in a compiler type mismatch. Always explicitly type the values array as `Array[Any]`.
- **Fabricated Receiver / Methods:** Attempting to call `addFeature` on `VectorLayerBuilder` (or truncating it to `VectorLayerBuil`), or attempting to call `.build()` on the result. The canonical receiver is `IntermediateVectorTile`, which does not define a `.build()` method.
- **Audience Misuse:** Attempting to use this ADVANCED/INTERNAL API for standard user workflows instead of high-level DataFrame visualization actions.

### Fix Code Hint
```scala
// BAD: Wrong receiver, Array[AnyRef] type mismatch, fabricated .build() method
val builder = new VectorLayerBuilder(4096, "test")
val f = Feature.create(geom, Array("id"), null, Array[AnyRef]("pt"))
builder.addFeature(f)
builder.build()

// GOOD: IntermediateVectorTile receiver, Array[Any] for attributes, in-place mutation
val tile = new IntermediateVectorTile(4096, 16)
val f = Feature.create(geom, Array("id"), null, Array[Any]("pt"))
tile.addFeature(f)
```

## API Test: `addGeometry`

### Signature
```scala
def addGeometry(geometry: Geometry, title: String): Boolean
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/VectorCanvas.scala:169_

_Source doc:_ Adds the given geometry to the canvas. This method might simplify, drop, or combine geometries to accommodate the given geometry without getting too big. @param geometry the geometry to add @param title an optional title to attach to the geometry in the SVG file @return `true` if the state of the canvas was modified.

### Goal
Adds a spatial geometry to a `VectorCanvas` for visualization, automatically simplifying, dropping, or combining geometries to prevent the canvas from exceeding memory or size limits.

### Parameters
- `geometry` (`Geometry`): The spatial geometry (e.g., Point, Polygon, LineString) to be drawn on the canvas.
- `title` (`String`): An optional title to attach to the geometry in the resulting SVG file. Can be `null`.

### Input
Requires an initialized `VectorCanvas` instance. The `geometry` must be a valid JTS `Geometry` object (typically created via a `GeometryFactory` such as `GeometryReader.DefaultGeometryFactory`). 

### Output
Returns `Boolean` — `true` if the state of the canvas was modified by the addition of the geometry, otherwise `false`.

### Valid Call Patterns
```scala
// Example 1: Adding individual points to a VectorCanvas
val canvas = new VectorCanvas(new Envelope(0, 256, 0, 256), 256, 256, 0, 1)
val factory = GeometryReader.DefaultGeometryFactory

canvas.addGeometry(factory.createPoint(new CoordinateXY(5, 5)), null)
canvas.addGeometry(factory.createPoint(new CoordinateXY(10.5, 10.5)), "Point A")

// Example 2: Adding many geometries in a loop (may trigger rasterization/dropping)
for (x <- 0 to 255; y <- 0 to 255) {
  canvas.addGeometry(factory.createPoint(new CoordinateXY(x, y)), null)
}
```

### LLM Instruction Prompt
- Call `addGeometry` on an instantiated `VectorCanvas` object.
- Pass a valid JTS `Geometry` as the first argument and a `String` (or `null`) as the second argument for the SVG title.
- Do not assume that every geometry added will be preserved exactly as provided; the canvas is designed to simplify, combine, or drop geometries (or rasterize them entirely) if the visual density becomes too high.

### Prompt Snippet
```text
To draw a geometry on a VectorCanvas in Beast, use `canvas.addGeometry(geometry, title)`. The `title` parameter is used for SVG outputs and can be `null`. Note that the canvas automatically manages its size and may simplify or drop geometries if too many are added.
```

### Common Failure Modes
- **Assuming exact preservation of geometries:** Callers might expect `canvas.geometries.length` to equal the exact number of times `addGeometry` was called. If too many geometries (e.g., dense points) are added, the canvas will simplify or rasterize them, potentially resulting in an empty geometry list despite a modified canvas state.
- **Null Pointer Exceptions:** Passing an uninitialized `Geometry` object instead of a properly constructed JTS geometry.

### Fix Code Hint
```scala
// Ensure the geometry is properly instantiated using a factory before adding
val factory = GeometryReader.DefaultGeometryFactory
val geom = factory.createPoint(new CoordinateXY(100, 100))

// Title can safely be null if SVG metadata is not required
val wasModified = canvas.addGeometry(geom, null)
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
Applies an affine transformation (such as scaling, translation, or rotation) either to a spatial data generator builder to transform all subsequently generated synthetic geometries, or directly to a single geometry.

### Parameters
- `matrix` (`AffineTransform`): The affine transformation matrix defining the spatial adjustments (e.g., `.scale()`, `.translate()`) to apply to the generated dataset.
- `geometry` (`Geometry`): The individual JTS geometry object to transform using the generator's configured affine transformation.

### Input
- For the `SpatialGeneratorBuilder` overload, the caller must provide an initialized `AffineTransform` matrix and chain the call onto `sparkContext.generateSpatialData` prior to specifying the distribution (e.g., `.uniform()`).
- For the `Geometry` overload, the caller must provide a valid JTS `Geometry` object.
- Requires an initialized `SparkContext` (or `JavaSpatialSparkContext`) to access the generator builder.

### Output
Returns `SpatialGeneratorBuilder` (when configuring a generator, allowing method chaining for data generation) or `Geometry` (when transforming a single geometry object).

### Valid Call Patterns
```scala
val transform = new AffineTransform()
transform.scale(2.0, 1.0)
transform.translate(0.0, 3.0)

// Apply to a spatial data generator
println(sparkContext.generateSpatialData
  .affineTransform(transform)
  .uniform(1000)
  .summary)
```

### LLM Instruction Prompt
- When generating synthetic spatial data in Beast (e.g., for benchmarking or testing), configure an `AffineTransform` matrix and pass it to `sparkContext.generateSpatialData.affineTransform(matrix)` **before** calling the distribution method (like `.uniform(size)`).
- Do not attempt to call `affineTransform` on the resulting `RDD`; it is a builder method on `SpatialGeneratorBuilder`.

### Prompt Snippet
```text
To apply scaling or translation to generated spatial data in Beast, create an `AffineTransform`, configure its parameters, and pass it to the generator builder: `sc.generateSpatialData.affineTransform(matrix).uniform(1000)`.
```

### Common Failure Modes
- **Calling on the wrong object:** Attempting to call `.affineTransform()` on the resulting `SpatialRDD` or `RDD[IFeature]` instead of the `SpatialGeneratorBuilder`. The transformation must be applied during the builder phase.
- **Incorrect chaining order:** Calling `.affineTransform()` after `.uniform()`. The distribution method (like `.uniform()`) terminates the builder and returns an RDD.

### Fix Code Hint
```scala
// WRONG: Calling affineTransform after uniform()
// val data = sparkContext.generateSpatialData.uniform(1000).affineTransform(transform)

// CORRECT: Apply the transform to the builder before generating the data
val data = sparkContext.generateSpatialData
  .affineTransform(transform)
  .uniform(1000)
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
Creates a new spatial feature by appending an additional attribute (such as a unique ID or a joined property) to an existing feature without modifying the original.

### Parameters
- `feature` (`IFeature`): The input spatial feature (vector or raster feature) to which the attribute will be added. This feature is not modified.
- `value` (`Any`): The attribute value to append (e.g., a `Long` ID, a `String` name, or a computed statistic).
- `name` (`String`), default `null`: The optional column/attribute name for the newly appended value.
- `dataType` (`DataType`), default `null`: The optional Spark SQL `DataType` of the new attribute.

### Input
An existing `IFeature` (typically from a spatial RDD, such as points or polygons loaded from a Shapefile, GeoJSON, or CSV) and a scalar value to attach to it. This is commonly used inside a `.map()` operation after a spatial join (to merge attributes from two matched features) or after `zipWithUniqueId()` (to attach generated IDs).

### Output
Returns `IFeature` — A newly instantiated feature containing the original geometry, all prior attributes of the input feature, and the newly appended attribute.

### Valid Call Patterns
```scala
// Example 1: Appending a unique ID (from test suite)
val addRecordID: ((IFeature, Long)) => IFeature = fid => Feature.append(fid._1, fid._2, "ID")

// Example 2: Appending an attribute from a spatial join result (from README)
val finalResults: RDD[IFeature] = sjResults.map(pip => {
  val polygon: IFeature = pip._1
  val point: IFeature = pip._2
  Feature.append(point, polygon.getAs[String]("NAME"), "state")
})
```

### LLM Instruction Prompt
- Always call `append` on the `Feature` object (`Feature.append(feature, value, name)`), not as an instance method on the feature itself.
- Remember that `append` returns a *new* feature; it does not mutate the input feature in place. You must capture or return the result.
- When enriching features after a spatial join, extract the desired attribute from one feature using `.getAs[T]("colName")` and append it to the other feature using `Feature.append`.

### Prompt Snippet
```text
To add an attribute to an IFeature in Beast, use the static method `Feature.append(feature, value, "columnName")`. Do not call `feature.append(...)`. The operation is immutable and returns a new IFeature, so you must capture the return value.
```

### Common Failure Modes
- **Calling as an instance method:** Attempting to call `myFeature.append(value)` will fail compilation because `append` is a method on the `Feature` companion object, not the `IFeature` trait.
- **Ignoring the return value:** Because `IFeature` is immutable, calling `Feature.append(...)` without assigning or returning the result will leave the original feature unchanged and the new attribute will be lost.

### Fix Code Hint
```scala
// WRONG: Instance method call and ignoring return value
point.append(polygonName, "state")

// CORRECT: Static method call capturing the new feature
val enrichedPoint = Feature.append(point, polygonName, "state")
```

## API Test: `area`

### Signature
```scala
def area: Double
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/LiteGeometry.scala:115_

### Goal
Computes the 2D area of a lightweight geometry (`LiteGeometry`) used internally during vector tile generation and visualization.

### Parameters
_None._

### Input
A `LiteGeometry` instance (such as a `LiteList` representing a simplified polygon or linear ring). These geometries are typically generated during Mapbox Vector Tile (MVT) processing, visualization tasks, or when simplifying standard JTS geometries via `IntermediateVectorTile.simplifyGeometry`.

### Output
Returns `Double` — the computed area of the geometry in its current coordinate space (e.g., tile pixel coordinates for MVT generation).

### Valid Call Patterns
```scala
// Inferred from the signature and test suite context (LiteGeometry usage)
val simplifiedRing = interTile.simplifyGeometry(ring) // Returns a LiteGeometry (e.g., LiteList)
val geomArea: Double = simplifiedRing.area
```

### LLM Instruction Prompt
- Call `area` on a `LiteGeometry` instance to retrieve its area as a `Double`.
- Do not use parentheses when calling this method, as it is defined without them (`def area: Double`).
- Use this primarily when working with the `davinci` visualization package or evaluating the size of simplified geometries during vector tile generation.

### Prompt Snippet
```text
Calculate the area of the simplified LiteGeometry without using parentheses.
```

### Common Failure Modes
- **Compilation Error (Parentheses):** Calling `liteGeom.area()` will fail to compile in Scala because the method is defined without parentheses.
- **Zero Area for Lines/Points:** Calling `area` on a `LiteGeometry` that represents a point, a non-closed linestring, or a degenerate polygon will return `0.0`.

### Fix Code Hint
```scala
// WRONG:
val a = liteGeom.area()

// CORRECT:
val a = liteGeom.area
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
Generate a synthetic distributed spatial dataset (SpatialRDD) using a bit distribution, typically used for benchmarking spatial algorithms, partitioning, and queries in Beast.

### Parameters
- `cardinality` (`Long`): The total number of spatial records (geometries) to generate across the cluster.
- `digits` (`Int`), default `10`: The number of digits to set per coordinate, controlling the granularity/resolution of the generated spatial points.
- `probability` (`Double`), default `0.2`: The probability of setting each bit, which influences the spatial skew and clustering of the generated data.

### Input
Requires an initialized `SparkContext` (`sc`) or `JavaSpatialSparkContext` with Beast implicits imported. Because this is a data generator (part of the Spider component), it does not require input files, formats, or paths. It operates entirely in-memory to produce synthetic geometries.

### Output
Returns `JavaSpatialRDD` (or `SpatialRDD` in Scala) — a distributed collection of synthetic spatial features (points or geometries) distributed according to the specified bit probability, ready for spatial partitioning, joins, or visualization.

### Valid Call Patterns
```scala
// Using the SparkContext extension (idiomatic Scala)
import edu.ucr.cs.bdlab.beast._

val bitData: SpatialRDD = sc.generateSpatialData
  .bit(1000, digits = 10, probability = 0.2)

// Visualizing the generated bit distribution
bitData.plotImage(300, 300, "bit.png", opts = Seq(GeometricPlotter.PointSize -> 0))

// Using the Builder pattern (often used in Java or for advanced configuration)
val builderData: SpatialRDD = new SpatialGeneratorBuilder(sc)
  .config(SpatialGenerator.Seed, 1794)
  .bit(1000, 10, 0.2)
```

### LLM Instruction Prompt
- When benchmarking or testing spatial operations without real datasets, use `sc.generateSpatialData.bit(cardinality, digits, probability)` to create a synthetic `SpatialRDD`.
- Do not invent file paths for this operation; it generates data in-memory.
- Ensure Beast implicits (`import edu.ucr.cs.bdlab.beast._`) are in scope so that `sc.generateSpatialData` is available on the `SparkContext`.

### Prompt Snippet
```text
To generate synthetic spatial data for benchmarking in Beast, use `sc.generateSpatialData.bit(cardinality, digits, probability)`. This returns a `SpatialRDD` generated in-memory using a bit distribution. Requires `import edu.ucr.cs.bdlab.beast._`.
```

### Common Failure Modes
- **Missing Implicits:** Calling `sc.generateSpatialData` will fail with a "value generateSpatialData is not a member of org.apache.spark.SparkContext" compilation error if Beast implicits are not imported.
- **Invalid Probability:** Providing a `probability` outside the valid range of `0.0` to `1.0` will result in invalid distributions or runtime exceptions.
- **Memory Exhaustion:** Providing an excessively large `cardinality` on a small cluster without triggering a save or spatial partition operation can cause out-of-memory errors during action execution.

### Fix Code Hint
```scala
// FIX: Ensure Beast implicits are imported to attach `.generateSpatialData` to `sc`
import edu.ucr.cs.bdlab.beast._

// FIX: Use valid probability (0.0 to 1.0) and reasonable cardinality
val syntheticData: SpatialRDD = sc.generateSpatialData
  .bit(cardinality = 1000000L, digits = 10, probability = 0.2)
```

## API Test: `build`

### Signature
```scala
def build(): VectorTile.Tile.Layer
def build(): Scan
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/VectorLayerBuilder.scala:133  (+4 more definition site/overload)_

_Source doc:_ Finalize the layer and return it @return

### Goal
Finalizes the construction of a Mapbox Vector Tile (MVT) layer (or a data scan operation), compiling all added features and attributes into the final return object.

### Parameters
_None._

### Input
A populated builder instance (such as `VectorLayerBuilder`) that has been initialized and had spatial features added to it (e.g., via `addFeature`). 

### Output
Returns `VectorTile.Tile.Layer` — a compiled Mapbox Vector Tile layer containing the encoded geometries, attribute keys, and values ready for web-based exploration or serialization. (Overloads return a `Scan` object for internal data scanning operations).

### Valid Call Patterns
```scala
// Finalizing a VectorLayerBuilder to create an MVT layer
val factory = FeatureReader.DefaultGeometryFactory
val builder = new VectorLayerBuilder(100, "test")

// Add features to the builder
builder.addFeature(Feature.create(
  factory.createPoint(new CoordinateXY(50, 50)), 
  Array("id", "name"),
  null, 
  Array(10, "pt")
))

// Finalize and build the layer
val layer: VectorTile.Tile.Layer = builder.build()

// The layer can now be inspected or serialized
val featureCount = layer.getFeaturesCount
```

### LLM Instruction Prompt
- When generating Mapbox Vector Tiles (MVT) programmatically using `VectorLayerBuilder`, always call `.build()` with no arguments to finalize the layer after all features have been added.
- Do not pass parameters to `build()`.
- Expect a `VectorTile.Tile.Layer` (or `Scan` depending on the builder type) as the return value, not a Spark RDD or DataFrame.

### Prompt Snippet
```text
To finalize a Mapbox Vector Tile layer after adding features to a `VectorLayerBuilder`, call `builder.build()` to retrieve the compiled `VectorTile.Tile.Layer`.
```

### Common Failure Modes
- **Empty Layer Generation:** Calling `build()` before adding any features to the `VectorLayerBuilder` will result in a valid but empty MVT layer.
- **Type Mismatch:** Assuming `build()` returns a distributed Spark dataset (like `RDD[IFeature]`). It returns a local, finalized protocol buffer object (`VectorTile.Tile.Layer`) for a specific tile.

### Fix Code Hint
```scala
// WRONG: Assuming build() returns an RDD
// val rdd: RDD[IFeature] = builder.build()

// CORRECT: build() returns the finalized MVT layer object
val layer: VectorTile.Tile.Layer = builder.build()
```

## API Test: `buildIndex`
_Grounding: doc-repaired from source (docfix)._

### Goal
**INTERNAL/FRAMEWORK.** This API is an internal utility used to pre-compute spatial bounding boxes for directories of rasters to optimize downstream spatial queries. *Note: Exclude from scored denominator / main user-facing benchmarks.* It creates a spatial index (CSV format) for all GeoTIFF files within a specified directory, using Spark to parallelize metadata extraction (MBR and SRID).

### Valid Call Patterns
```scala
import org.apache.hadoop.fs.Path
import edu.ucr.cs.bdlab.raptor.RasterFileRDD

// Assuming `raster_tif` and `sc` (SparkContext) are provided by the harness
val rasterPath = new Path(raster_tif)
val rasterDir = rasterPath.getParent.toString
val indexFile = new Path(output_dir, "_index.csv").toString

// Build the index using the correct receiver object
RasterFileRDD.buildIndex(sc, rasterDir, indexFile)

// Verify by reading it back using Hadoop FileSystem
// (Spark's sc.textFile ignores files prefixed with "_")
val fs = new Path(indexFile).getFileSystem(sc.hadoopConfiguration)
val inputStream = fs.open(new Path(indexFile))
val indexLines = scala.io.Source.fromInputStream(inputStream).getLines().toList
inputStream.close()
```

### LLM Instruction Prompt
- **Classification:** INTERNAL/FRAMEWORK. Exclude from user-facing benchmarks.
- **Receiver Object:** The correct receiver for `buildIndex` is strictly the `RasterFileRDD` object in the `edu.ucr.cs.bdlab.raptor` package (call it as `edu.ucr.cs.bdlab.raptor.RasterFileRDD.buildIndex`). Do NOT use `IndexBuilder` as the receiver, as it will cause a compilation error (`object IndexBuilder is not a member of package`).
- **Method Signature:** `edu.ucr.cs.bdlab.raptor.RasterFileRDD.buildIndex(sparkContext: SparkContext, dir: String, indexFile: String)`.
- **Verification/Reading:** Do NOT use `sc.textFile` to read the generated `_index.csv` file. Spark ignores files starting with an underscore, so this will fail at runtime. You MUST use Hadoop's `FileSystem.open` and `scala.io.Source.fromInputStream` to read the index file back for verification.

### Prompt Snippet
```scala
val rasterDir = new org.apache.hadoop.fs.Path(raster_tif).getParent.toString
val indexFile = new org.apache.hadoop.fs.Path(output_dir, "_index.csv").toString
edu.ucr.cs.bdlab.raptor.RasterFileRDD.buildIndex(sc, rasterDir, indexFile)
```

### Common Failure Modes
- **INTERNAL/FRAMEWORK API:** This is an internal framework utility. Do not present it as the normal first-choice user workflow for raster analysis. Exclude from the main user-facing denominator.
- **Wrong Receiver Object (Compilation Failure):** A previous flawed diagnosis incorrectly claimed that using `RasterFileRDD` caused a compilation error (`value buildIndex is not a member of object RasterFileRDD`) and mandated using `IndexBuilder`. This is actively harmful; `IndexBuilder` does not exist. The source code definitively proves the correct receiver is strictly `edu.ucr.cs.bdlab.raptor.RasterFileRDD`.
- **Hidden File Read Failure (`InvalidInputException`):** Using `sc.textFile` to read the `_index.csv` file will fail at runtime because Spark ignores files prefixed with an underscore. You must use `FileSystem.open` and `scala.io.Source.fromInputStream`.

### Fix Code Hint
```scala
// WRONG: Incorrect receiver (IndexBuilder) and reading with sc.textFile
edu.ucr.cs.bdlab.raptor.IndexBuilder.buildIndex(sc, rasterDir, indexFile) // Fails: object IndexBuilder is not a member
val badRead = sc.textFile(indexFile) // Fails: ignores "_" prefixed files

// RIGHT: Correct receiver (RasterFileRDD) and reading via Hadoop FileSystem
edu.ucr.cs.bdlab.raptor.RasterFileRDD.buildIndex(sc, rasterDir, indexFile)

val fs = new org.apache.hadoop.fs.Path(indexFile).getFileSystem(sc.hadoopConfiguration)
val inputStream = fs.open(new org.apache.hadoop.fs.Path(indexFile))
val goodRead = scala.io.Source.fromInputStream(inputStream).getLines().toList
inputStream.close()
```

## API Test: `call`

### Signature
```scala
def call(f: IFeature): Int
```
_Source: beast/beast-spark/src/main/scala/edu/ucr/cs/bdlab/beast/operations/FeatureWriterSize.scala:31_

_Source doc:_ For Java callers

### Goal
Evaluates a spatial feature to return an integer value, serving as an implementation of Spark's Java `Function` interface for Java callers interacting with Beast's spatial partitioning.

### Parameters
- `f` (`IFeature`): The spatial feature (geometry and attributes) to be evaluated.

### Input
A single `IFeature` object (e.g., a point, line, or polygon loaded from CSV, Shapefile, or GeoJSON). This is typically provided internally by Spark when iterating over a `JavaRDD[IFeature]` during operations like spatial partitioning.

### Output
Returns `Int` — An integer value derived from the feature, such as a constant weight (e.g., `1`) or a computed size, used for load balancing during spatial partitioning.

### Valid Call Patterns
```scala
// Implementing the function for Java-facing APIs like IndexHelper.partitionFeatures
val weightFunction = new org.apache.spark.api.java.function.Function[IFeature, Int]() {
  override def call(v1: IFeature): Int = 1
}
```

### LLM Instruction Prompt
- Use `call` only when implementing `org.apache.spark.api.java.function.Function[IFeature, Int]` for Java-compatible Beast APIs (like `IndexHelper.partitionFeatures`). In idiomatic Scala Spark pipelines, prefer native Scala closures (e.g., `_ => 1`) instead of manually instantiating Java functions and overriding `call`.

### Prompt Snippet
```text
When using Java-facing Beast APIs from Scala (e.g., IndexHelper.partitionFeatures), implement org.apache.spark.api.java.function.Function[IFeature, Int] and override `call(f: IFeature): Int` to provide feature weights.
```

### Common Failure Modes
- **Idiomatic Scala Mismatch:** Attempting to manually invoke or override `call` in standard Scala `RDD[IFeature]` operations (like `map` or `spatialPartition`), which expect native Scala functions `(IFeature => Int)` rather than Java `Function` objects.
- **Null Pointer Exceptions:** Failing to handle null values if the overridden `call` method attempts to access feature geometry or attributes without null checks, as Spark may occasionally pass nulls depending on the upstream data source.

### Fix Code Hint
```scala
// Correct usage when interfacing with Java APIs requiring a Function[IFeature, Int]
val javaFunction = new org.apache.spark.api.java.function.Function[IFeature, Int]() {
  override def call(f: IFeature): Int = {
    if (f == null) 0 else 1
  }
}
```

## API Test: `checkOptions`

### Signature
```scala
def checkOptions(options: ParsedCommandLineOptions, out: PrintStream): Boolean
```
_Source: beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/util/OperationHelper.scala:293_

_Source doc:_ Check if the user options are valid. This means that the user did not add any unexpected options or leave out any required option @param options parsed command line options. @return

### Goal
Validates parsed command-line arguments to ensure all required options for a Beast operation are present and no unexpected or unsupported options were provided.

### Parameters
- `options` (`ParsedCommandLineOptions`): The parsed command-line arguments, typically generated by calling `OperationHelper.parseCommandLineArguments(...)`.
- `out` (`PrintStream`): The output stream where validation error messages (such as missing required options or unrecognized flags) will be printed.

### Input
The caller must provide a valid `ParsedCommandLineOptions` object representing the user's CLI input for a specific Beast command, and an initialized `PrintStream` (such as `System.err`, `System.out`, or a custom stream like `new PrintStream(new NullOutputStream)` to suppress output). 

### Output
Returns `Boolean` — `true` if the options are perfectly valid (all required parameters are found and no unexpected parameters exist), and `false` otherwise.

### Valid Call Patterns
```scala
import edu.ucr.cs.bdlab.beast.util.OperationHelper
import java.io.PrintStream
import org.apache.commons.io.output.NullOutputStream

// Parse arguments for a specific operation
val parsedOptions = OperationHelper.parseCommandLineArguments(
  "subtest1", "path1", "sparam2:1", "-sparam", "-no-param1[0]", "path2"
)

// Validate the options, suppressing error output in this example
val isValid = OperationHelper.checkOptions(parsedOptions, new PrintStream(new NullOutputStream))

if (!isValid) {
  // Handle invalid options (e.g., exit program or throw exception)
}
```

### LLM Instruction Prompt
- When writing CLI wrappers or custom commands for Beast, always validate the user's input by passing the parsed arguments to `OperationHelper.checkOptions(options, out)`.
- Do not call `checkOptions` as a bare function; it must be called on the `OperationHelper` object.
- Provide a valid `PrintStream` (like `System.err`) as the second argument so the user can see which parameters were missing or unexpected.

### Prompt Snippet
```text
Validate Beast command-line arguments using `OperationHelper.checkOptions(parsedOptions, System.err)`. It returns a Boolean indicating if all required options are present and no unexpected options were provided.
```

### Common Failure Modes
- **Missing Required Parameters:** The user omitted an option that the specific Beast operation requires to run. `checkOptions` will return `false` and print the missing requirements to the provided `PrintStream`.
- **Unexpected Parameters:** The user provided a flag or option that the operation does not recognize (e.g., a typo in a flag name). `checkOptions` will return `false`.
- **Null PrintStream:** Passing `null` for the `out` parameter will cause a `NullPointerException` when the function attempts to print validation errors.

### Fix Code Hint
```scala
// Incorrect: Ignoring the validation result or passing null
OperationHelper.checkOptions(parsedOptions, null)

// Correct: Checking the boolean result and providing a valid PrintStream for user feedback
if (!OperationHelper.checkOptions(parsedOptions, System.err)) {
  System.exit(1) // Exit if options are invalid (missing required or containing unexpected)
}
```

## API Test: `compute`

### Signature
```scala
def compute(split: Partition, context: TaskContext): Iterator[ITile[T]]
def compute(pID: Int, ring: CoordinateSequence, w: Int, h: Int): Unit
def compute(split: Partition, context: TaskContext): Iterator[IFeature]
def compute(split: Partition, context: TaskContext): Iterator[(EnvelopeNDLite, (Iterator[IFeature], Iterator[IFeature]))]
def compute(split: Partition, context: TaskContext): Iterator[(Iterator[T], Iterator[U])]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/PixelsInside.scala:119  (+7 more definition site/overload)_

_Source doc:_ Compute the intersections for the given linear ring @param pID the ID of the polygon @param ring the list of coordinates that make the ring already projected to the raster space @param w the width of the raster in pixels @param h the height of the raster in pixels

### Goal
Compute the pixel intersections for a given linear ring (polygon boundary) projected into raster space, used internally during Raptor joins to match vector polygons to underlying raster pixels.

### Parameters
- `pID` (`Int`): The unique identifier (ID) of the polygon being processed.
- `ring` (`CoordinateSequence`): The list of coordinates forming the linear ring, which must already be projected into the raster's local pixel coordinate space.
- `w` (`Int`): The width of the raster in pixels.
- `h` (`Int`): The height of the raster in pixels.

### Input
A linear ring (`CoordinateSequence`) representing a polygon boundary. **Precondition:** The coordinates must be transformed from their original CRS (e.g., EPSG:4326) into the raster's pixel space prior to calling this method. The exact pixel dimensions of the raster (`w`, `h`) must be known. 

*(Note: The `compute` method is heavily overloaded. The `(Partition, TaskContext)` overloads are standard Spark internal methods used to evaluate RDD partitions for features, tiles, or spatial joins.)*

### Output
Returns `Unit` — mutates the internal state of the calling object (e.g., an `Intersections` tracker) to record which raster pixels intersect the given polygon ring. In Raptor joins, polygons match pixels whose *center* falls inside the polygon boundary.

### Valid Call Patterns
```scala
// 1. Authoritative usage from test suite (using the Geometry/RasterMetadata overload)
val metadata: RasterMetadata = createSimpleGrid(1, 1, 10, 10)
val geometries1 = Array[Geometry](
  GeometryReader.DefaultGeometryFactory.createPoint(new Coordinate(1, 1)),
  GeometryReader.DefaultGeometryFactory.createPoint(new Coordinate(3, 3))
)
val intersections1 = new Intersections
intersections1.compute(geometries1, metadata)

// 2. Inferred from the specific signature (not verified)
val intersections = new Intersections
intersections.compute(polygonID, coordinateSequence, rasterWidth, rasterHeight)
```

### LLM Instruction Prompt
- Do not call `compute` directly for standard user-facing raster-vector joins; prefer the high-level `raster.raptorJoin[T](vector)` API.
- If using `compute` for custom intersection tracking, you MUST ensure the `CoordinateSequence` is projected to raster space first. Do not pass raw geographic coordinates (e.g., lat/lon).
- When implementing custom Spark RDDs in Beast, the `compute(split: Partition, context: TaskContext)` overloads are used to yield iterators of `ITile[T]`, `IFeature`, or joined pairs.

### Prompt Snippet
```text
When performing raster-vector joins, avoid manually calling the internal `compute` intersection methods unless building custom plumbing. Use `raster.raptorJoin[T](vector)` instead. If you must use `compute(pID, ring, w, h)`, ensure the `ring` coordinates are already projected to raster pixel space.
```

### Common Failure Modes
- **Unprojected Coordinates:** Passing a `CoordinateSequence` in its original CRS (like WGS84) instead of raster pixel space, resulting in zero intersections or out-of-bounds errors.
- **Incorrect Raster Dimensions:** Providing `w` and `h` that do not match the actual raster tile or file, causing the intersection algorithm to truncate valid pixels or scan out of bounds.
- **Manual Plumbing Errors:** Attempting to use `compute` for zonal statistics instead of the built-in `raptorJoin`, missing the required quad-split optimizations for complex geometries (triggered automatically when points per geometry > 100).

### Fix Code Hint
```scala
// WRONG: Passing geographic coordinates to compute
// intersections.compute(1, geoRing, 1000, 1000)

// RIGHT: Use the high-level Raptor API for raster-vector joins
val treecover: RDD[ITile[Float]] = sc.geoTiff("treecover")
val countries: RDD[IFeature] = sc.shapefile("ne_10m_admin_0_countries.zip")
val join: RDD[RaptorJoinFeature[Float]] = treecover.raptorJoin(countries)
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
Computes geometric summaries (such as bounding boxes, feature counts, and storage sizes) for a spatial vector dataset, either globally for the entire dataset or locally partitioned across grid cells.

### Parameters
- `features` (`SpatialRDD`): The distributed set of spatial features (vector data) to summarize.
- `synopsisSize` (`Long`), default `1024 * 1024`: The target size in bytes for the generated synopsis when using the `Synopsis` overload.
- `sizeFunction` (`IFeature => Int`), default `f => f.getStorageSize`: An optional function to compute the size of a single feature.
- `numPartitions` (`Int*`): Either the total number of cells or an array specifying the number of partitions along each dimension for grid-based summaries.

### Input
A `SpatialRDD` (or `JavaSpatialRDD`) containing vector features. This is typically generated by loading vector data via context extensions like `sc.shapefile`, `sc.geojsonFile`, or `sc.readCSVPoint`. It cannot be used directly on raster data (`RasterRDD`).

### Output
Returns `Synopsis` — (or `Summary` / `(Summary, RDD[(Array[Int], Summary)])` depending on the overload). The value represents the computed statistics of the dataset, including the global bounding box (Minimum Bounding Rectangle) of the data, total feature count, and total size. The tuple overload returns one global summary and a set of local summaries for each grid cell.

### Valid Call Patterns
```scala
// 1. Compute a basic global summary (used for partitioner initialization)
val summary = Summary.computeForFeatures(features)

// 2. Compute a global summary with a custom size function
val summaryWithSize = Summary.computeForFeatures(features, f => f.getGeometry.getNumPoints * 2 * 4)

// 3. Use the summary to initialize a spatial partitioner
val partitionedFeatures = IndexHelper.partitionFeatures(
  features, 
  new GridPartitioner(Summary.computeForFeatures(features), 1)
)
```

### LLM Instruction Prompt
- Always call `computeForFeatures` as a static method on the `Summary` object (e.g., `Summary.computeForFeatures(features)`), never as an instance method on the RDD itself.
- Use this function when you need to extract the global bounding box or statistics of a `SpatialRDD` to initialize spatial partitioners (like `GridPartitioner` or `RSGrovePartitioner`).
- Do not use this function on raster datasets (`RasterRDD`); it is strictly for vector features (`SpatialRDD`).

### Prompt Snippet
```text
To compute the bounding box and statistics of a vector dataset in Beast, use `Summary.computeForFeatures(features)`. This is required when manually initializing spatial partitioners that need the global extent of the data.
```

### Common Failure Modes
- **Calling as an instance method:** Attempting to call `features.computeForFeatures()` will fail compilation. It must be called as `Summary.computeForFeatures(features)`.
- **Passing Raster Data:** Passing a `RasterRDD` (e.g., from `sc.geoTiff`) instead of a `SpatialRDD`. Raster metadata should be accessed via the raster's built-in metadata properties, not via vector summaries.

### Fix Code Hint
```scala
// WRONG: Calling as an instance method on the RDD
val summary = features.computeForFeatures()

// RIGHT: Calling as a method on the Summary object
val summary = Summary.computeForFeatures(features)
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
Computes a geometric summary of a spatial dataset (such as bounding box and feature count) while simultaneously estimating the total output file size if the features were written to a specified format.

### Parameters
- `features` (`JavaSpatialRDD` | `SpatialRDD`): The distributed spatial dataset containing the vector geometries to be summarized.
- `opts` (`BeastOptions`): Configuration options specifying the target output format (e.g., `"iformat" -> "geojson"`) used to calculate the size estimate.

### Input
A loaded spatial RDD of vector features (e.g., points, lines, or polygons loaded from Shapefile, GeoJSON, or CSV). 

### Output
Returns `Summary` — A geometric summary object (which can be formatted as JSON) containing the dataset's spatial bounds, feature count, and the estimated output size in bytes for the specified format.

### Valid Call Patterns
```scala
// Estimate the output size if the records are written to GeoJSON
// Note: A tuple like "iformat" -> "geojson" is often implicitly converted to BeastOptions in Beast Scala APIs
val summary = GeometricSummary.computeForFeaturesWithOutputSize(features, "iformat" -> "geojson")

// Explicit BeastOptions construction
import edu.ucr.cs.bdlab.beast.common.BeastOptions
val opts = new BeastOptions().set("iformat", "geojson")
val summaryExplicit = GeometricSummary.computeForFeaturesWithOutputSize(features, opts)
```

### LLM Instruction Prompt
- When you need to compute a geometric summary and estimate the disk size of a spatial RDD before exporting it, call `GeometricSummary.computeForFeaturesWithOutputSize(features, opts)`. Do not call this as an instance method on the RDD. Always provide the target format (e.g., `"iformat" -> "geojson"`) in the `BeastOptions` argument.

### Prompt Snippet
```text
val summary = GeometricSummary.computeForFeaturesWithOutputSize(features, "iformat" -> "geojson")
```

### Common Failure Modes
- **Incorrect Receiver:** Attempting to call this as an instance method on the RDD (e.g., `features.computeForFeaturesWithOutputSize(...)`) instead of calling it statically on the `GeometricSummary` object.
- **Missing Format Option:** Failing to specify the `"iformat"` in the `BeastOptions`, which prevents the engine from accurately estimating the serialization overhead of the target format.

### Fix Code Hint
```scala
// WRONG: Calling as an RDD method
val summary = features.computeForFeaturesWithOutputSize("iformat" -> "geojson")

// RIGHT: Calling on the GeometricSummary object
val summary = GeometricSummary.computeForFeaturesWithOutputSize(features, new BeastOptions().set("iformat", "geojson"))
```

## API Test: `computePointHistogramSparse`
_Grounding: doc-repaired from source (docfix)._

### Goal
ADVANCED/LOW-LEVEL API. Computes a sparse uniform point histogram over a spatial dataset by mapping each feature to a bucket and aggregating via `reduceByKey`. Optimized to prevent memory bottlenecks on the driver for very large, mostly empty grids. *Note: This is an internal framework method; it should be excluded from the main user-facing denominator. Users should typically use higher-level RDD extensions.*

### Input
ADVANCED/LOW-LEVEL. Requires a `SpatialRDD` (provided by the harness), a size function (`IFeature => Int`), an `EnvelopeNDLite` (typically obtained dynamically via `featuresRDD.summary`), and a varargs `Int` for the number of buckets.

### Output
Returns a local `UniformHistogram` object on the driver containing aggregated sizes per grid cell. The result can be verified by checking that it is not null, or by calling methods like `getNumPartitions(0)`, `getNumPartitions(1)`, or `getValue(...)`.

### Valid Call Patterns
```scala
import edu.ucr.cs.bdlab.beast.synopses.HistogramOP
import edu.ucr.cs.bdlab.beast.synopses.UniformHistogram
import edu.ucr.cs.bdlab.beast.geolite.EnvelopeNDLite

// featuresRDD is provided by the execution harness
val mbb: EnvelopeNDLite = featuresRDD.summary

// Compute the sparse point histogram using the HistogramOP object
val hist: UniformHistogram = HistogramOP.computePointHistogramSparse(
  featuresRDD,
  _ => 1, // size function: count each feature as 1
  mbb,
  100     // hint for total number of buckets
)

// Verify the result to prevent test generator AssertionError
assert(hist != null)
assert(hist.getNumPartitions(0) > 0)
```

### LLM Instruction Prompt
For advanced/internal sparse histogram generation, use `HistogramOP.computePointHistogramSparse`. Always compute the MBB via `rdd.summary`. To verify the returned `UniformHistogram` in tests, assert it is not null and query its dimensions using `getNumPartitions(0)` so the test generator does not intentionally fail the test.

### Prompt Snippet
```text
ADVANCED: Use HistogramOP.computePointHistogramSparse(rdd, _ => 1, rdd.summary, numBuckets) for sparse histograms. Verify output via assert(hist != null) and hist.getNumPartitions(0).
```

### Common Failure Modes
- **Test Generator AssertionError (Missing Verification):** The test harness will intentionally abort with `java.lang.AssertionError` if it cannot write a meaningful assertion. You must verify the returned `UniformHistogram` by checking `assert(hist != null)` or calling `hist.getNumPartitions(0)`.
- **Calling as an instance method:** Attempting to call `rdd.computePointHistogramSparse(...)` fails to compile. This is an ADVANCED/LOW-LEVEL object method and must be called explicitly on `HistogramOP`.

### Fix Code Hint
```scala
// WRONG: Missing assertions causes test generator to abort with AssertionError
// val hist = HistogramOP.computePointHistogramSparse(featuresRDD, _ => 1, featuresRDD.summary, 100)

// RIGHT: Include assertions using UniformHistogram methods
val mbb = featuresRDD.summary
val hist = HistogramOP.computePointHistogramSparse(featuresRDD, _ => 1, mbb, 100)
assert(hist != null)
assert(hist.getNumPartitions(0) > 0)
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
Sets configuration options for the spatial data generator (Spider) to control the properties of the generated synthetic datasets, such as geometry type, size, and random seed.

### Parameters
- `key` (`String`): The configuration property name (e.g., `UniformDistribution.GeometryType`, `SpatialGenerator.Seed`, `UniformDistribution.MaxSize`).
- `value` (`Any`): The value to assign to the configuration property (e.g., `"box"`, `1794`, `"0.2,0.1"`).

### Input
An initialized `SpatialGeneratorBuilder` or `JavaSpatialGeneratorBuilder` instance, typically created with a `SparkContext` (e.g., `new SpatialGeneratorBuilder(sparkContext)`).

### Output
Returns `SpatialGeneratorBuilder` (or `JavaSpatialGeneratorBuilder`) — the updated builder instance, allowing for fluent method chaining before triggering the final data generation.

### Valid Call Patterns
```scala
// Generate random boxes within a specific Minimum Bounding Rectangle (MBR)
val desiredMBR = new EnvelopeNDLite(2, 2, 3, 9, 8)
val randomPoints: SpatialRDD = new SpatialGeneratorBuilder(sparkContext).mbr(desiredMBR)
  .config(UniformDistribution.MaxSize, "0.2,0.1")
  .config(UniformDistribution.NumSegments, 10)
  .config(UniformDistribution.GeometryType, "box")
  .config(SpatialGenerator.Seed, 1794)
  .uniform(10)

// Generate random polygons
val randomPolygons: SpatialRDD = new SpatialGeneratorBuilder(sparkContext).mbr(desiredMBR)
  .config(UniformDistribution.MaxSize, "0.2,0.1")
  .config(UniformDistribution.NumSegments, 10)
  .config(UniformDistribution.GeometryType, "polygon")
  .config(SpatialGenerator.Seed, 1794)
  .uniform(100)
```

### LLM Instruction Prompt
- When generating synthetic spatial data using `SpatialGeneratorBuilder`, chain `.config(key, value)` calls to specify generation parameters before calling the terminal generation method (like `.uniform(N)`). 
- Use known configuration keys such as `UniformDistribution.GeometryType` (e.g., `"box"`, `"polygon"`), `UniformDistribution.MaxSize` (as a comma-separated string like `"0.2,0.1"`), `UniformDistribution.NumSegments`, and `SpatialGenerator.Seed`.
- Do not invent configuration keys; rely on the constants provided by the Beast library.

### Prompt Snippet
```text
Chain `.config(key, value)` on `SpatialGeneratorBuilder` to set generation parameters (e.g., geometry type, seed) before calling a terminal generation method like `.uniform(N)`.
```

### Common Failure Modes
- **Missing Terminal Operation:** Failing to call a terminal generation method (like `.uniform(N)`) after chaining `.config()` calls, which results in a builder object instead of the expected `SpatialRDD`.
- **Invalid Value Formats:** Providing incorrect types or string formats for complex configuration values (e.g., `MaxSize` expects a comma-separated string like `"0.2,0.1"`, not a single float).

### Fix Code Hint
```scala
// WRONG: Missing terminal generation method
val builder = new SpatialGeneratorBuilder(sc)
  .config(UniformDistribution.GeometryType, "box")

// CORRECT: Chain config and call terminal method to produce the SpatialRDD
val randomData = new SpatialGeneratorBuilder(sc)
  .config(UniformDistribution.GeometryType, "box")
  .uniform(100)
```

## API Test: `construct`
_Grounding: doc-repaired from source (docfix)._

### Signature
```scala
def construct(out: DataOutput, entries: Array[(Long, Long, Int)]): Unit
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/DiskTileHashtable.scala:38_

### Goal
**INTERNAL/FRAMEWORK API.** This is low-level internal plumbing used to build and serialize a static, compact, on-disk hashtable mapping 64-bit spatial tile IDs to their byte offsets and lengths within an archive. *Note: This API should be excluded from the main user-facing benchmark denominator as it is not a standard Spark/raster operation.*

### Parameters
- `out` (`java.io.DataOutput`): The destination binary stream (typically an `FSDataOutputStream`) where the hashtable will be written.
- `entries` (`Array[(Long, Long, Int)]`): The dataset to index. Each tuple must strictly represent `(tileID, byteOffset, byteLength)`.

### Input
**INTERNAL/FRAMEWORK:** Executable only with explicit low-level construction. The caller must manually instantiate a `java.io.DataOutput` stream (e.g., via Hadoop's `FileSystem.create(path)`) and provide an array of raw tuple entries. The caller owns the stream and is strictly responsible for closing it to flush the data to disk.

### Output
Returns `Unit`. Writes the compact hashtable directly to the provided `DataOutput` stream.

### Valid Call Patterns
```scala
import org.apache.hadoop.fs.Path
import org.apache.hadoop.fs.FSDataInputStream
import java.io.DataOutput
import edu.ucr.cs.bdlab.davinci.DiskTileHashtable

// 1. Caller-owned low-level construction of the output stream
val path = new Path(output_dir, "tile_index.dat")
val fileSystem = path.getFileSystem(sc.hadoopConfiguration)
val out = fileSystem.create(path) // Implements java.io.DataOutput

// 2. Prepare the entries: Array[(tileID, offset, length)]
val entries: Array[(Long, Long, Int)] = Array(
  (1L, 100L, 50),
  (2L, 150L, 60),
  (3L, 210L, 70)
)

// 3. Construct the hashtable and write it to disk
try {
  DiskTileHashtable.construct(out, entries)
} finally {
  out.close() // Caller must close the stream
}

// 4. Verify the written hashtable using the companion reader API
val in: FSDataInputStream = fileSystem.open(path)
try {
  // offset is 0L since the hashtable was written at the beginning of the file
  val result = DiskTileHashtable.getValue(in, 0L, 1L)
  assert(result == (100L, 50), s"Expected (100, 50) but got $result")
} finally {
  in.close() // Caller must close the input stream
}
```

### LLM Instruction Prompt
- **INTERNAL/FRAMEWORK API:** Exclude from standard user-facing Spark workflows.
- When testing `DiskTileHashtable.construct(out, entries)`, you must explicitly construct the `DataOutput` stream and the `Array[(Long, Long, Int)]` entries.
- **Crucial:** To verify the written hashtable, you MUST use the companion reader API: `DiskTileHashtable.getValue(in: FSDataInputStream, offset: Long, key: Long): (Long, Int)`.
- Open an `FSDataInputStream` using `fileSystem.open(path)` to read the values back. The `offset` parameter should be `0L` if the hashtable is at the start of the file.
- The caller owns both the output and input streams and must close them in `finally` blocks.

### Prompt Snippet
```text
To write a compact tile index to disk, use `DiskTileHashtable.construct(out, entries)`. This is an internal API requiring explicit stream management. You must manually close `out`. To verify the written contents, open an `FSDataInputStream` and call `DiskTileHashtable.getValue(in, 0L, tileID)`, which returns `(offset, length)`.
```

### Common Failure Modes
- **Missing Verification (AssertionError):** `java.lang.AssertionError: assertion failed: The documented contract is insufficient to verify the result (no reader API provided...)`. This happens if the LLM aborts the test assuming there is no way to read the data back. You *must* use `DiskTileHashtable.getValue(in, offset, key)` to verify the written contents.
- **Unclosed Output Stream:** Failing to call `out.close()` after `construct` finishes, resulting in incomplete file writes or corrupted hashtables on disk, causing `getValue` to fail or return null.
- **Misunderstanding API Scope:** Attempting to use this as a standard RDD/DataFrame operation. It is an **INTERNAL/FRAMEWORK** utility requiring low-level Java/Hadoop IO streams.

### Fix Code Hint
**Wrong:** (Aborting verification due to perceived lack of reader API)
```scala
DiskTileHashtable.construct(out, entries)
out.close()
// ERROR: Test aborted because LLM assumes no reader API exists to verify the file.
```

**Correct:** (Using the companion `getValue` method for verification)
```scala
DiskTileHashtable.construct(out, entries)
out.close()

val in = fileSystem.open(path)
try {
  // Read back the entry for tileID 1L at file offset 0L
  val result = DiskTileHashtable.getValue(in, 0L, 1L)
  assert(result == (100L, 50))
} finally {
  in.close()
}
```

## API Test: `count`
_Grounding: doc-repaired from source (docfix)._

### Signature
```scala
def count: Int
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/GeoTiffWriter.scala:860_

### Goal
INTERNAL/FRAMEWORK API. Computes the number of elements in the payload of a temporary TIFF Image File Directory (IFD) entry before it is written to disk. 
*Note: Exclude this API from the main user-facing benchmark denominator, as it is an internal TIFF writing utility.*

### Parameters
_None._

### Input
A caller-owned, explicitly constructed `TempIFDEntry` instance. The `value` parameter passed to the constructor must be an `Array[Int]`, `Array[Long]`, `Array[Double]`, or `String`.

### Output
Returns `Int` — The length of the array, or `string.length + 1` (accounting for the null-terminating byte) if the value is a String.

### Valid Call Patterns
```scala
import edu.ucr.cs.bdlab.raptor.GeoTiffWriter.TempIFDEntry

// Caller-owned low-level construction required for this internal API
val entry = TempIFDEntry(
  tag = 256.toShort,
  valueType = 3.toShort,
  value = Array(1024)
)

val elementCount: Int = entry.count
```

### LLM Instruction Prompt
- Identify this as an INTERNAL/FRAMEWORK API. Do not confuse it with Spark's `RDD.count()`.
- Test this API using explicit low-level construction of the `TempIFDEntry` case class.
- Ensure the `value` parameter provided to `TempIFDEntry` is strictly one of the allowed types (`Array[Int]`, `Array[Long]`, `Array[Double]`, or `String`).

### Prompt Snippet
```text
To test the `count` API, explicitly instantiate `edu.ucr.cs.bdlab.raptor.GeoTiffWriter.TempIFDEntry` with a valid array or string value, then call `.count`. Do not attempt to use spatial RDDs or dataset summaries.
```

### Common Failure Modes
- **Hallucinating Spark RDD Operations:** The most common failure (e.g., `value getMinX is not a member of...`) occurs when the model mistakes this internal API for Spark's `RDD.count()` and attempts to call it on a spatial dataset or summary object. This is an INTERNAL/FRAMEWORK API that requires explicit instantiation of `TempIFDEntry`.
- **Invalid Value Type:** Passing an unsupported type (e.g., `Int` instead of `Array[Int]`) to the `TempIFDEntry` constructor will trigger a runtime `IllegalArgumentException` due to a strict `require` assertion.
- **Scoring Exclusion:** Because this is an internal helper structure, it should be excluded from the scored denominator of user-facing API tests.

### Fix Code Hint
```scala
// WRONG: Hallucinating the API as Spark's RDD.count() on a spatial dataset
val filteredData = partitionedData.rangeQuery(queryGeometry)
val matchCount = filteredData.count()

// CORRECT: Explicit low-level construction of the internal IFD entry
import edu.ucr.cs.bdlab.raptor.GeoTiffWriter.TempIFDEntry

val entry = TempIFDEntry(tag = 256.toShort, valueType = 3.toShort, value = Array(1024))
val matchCount = entry.count
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
Creates metadata defining the geographical extent, coordinate reference system (CRS), and grid dimensions of a raster dataset, or instantiates vector features and memory tiles via its overloads.

### Parameters
- `x1` (`Double`): The x-coordinate of the left edge of the pixel at (0, 0).
- `y1` (`Double`): The y-coordinate of the top edge of the pixel at (0, 0).
- `x2` (`Double`): The x-coordinate of the right edge of the pixel at (rasterWidth - 1, rasterHeight - 1).
- `y2` (`Double`): The y-coordinate of the bottom edge of the pixel at (rasterWidth - 1, rasterHeight - 1).
- `srid` (`Int`): The SRID that represents the coordinate reference system of the raster (e.g., 4326).
- `rasterWidth` (`Int`): The number of columns in the entire raster.
- `rasterHeight` (`Int`): The number of rows in the entire raster.
- `tileWidth` (`Int`): The width of each tile in pixels.
- `tileHeight` (`Int`): The height of each tile in pixels.

### Input
Raw coordinate bounds, SRID, and grid dimensions. This metadata is a strict precondition for operations that generate or align rasters, such as `sc.rasterizePixels`, `sc.rasterizePoints`, or `RasterOperationsFocal.reshapeNN` / `reshapeAverage`. For the `Feature.create` overloads, it requires a valid `Geometry` (like `PointND` or `EnvelopeND`) and optional attribute arrays or a `Row`.

### Output
Returns `RasterMetadata` — an object representing the spatial and dimensional configuration of a raster grid. (Overloads return `Feature`, `RasterFeature`, or `MemoryTileWindow[T]`).

### Valid Call Patterns
```scala
// 1. Creating RasterMetadata for rasterization or reshaping
val metadata = RasterMetadata.create(x1 = -50, y1 = 40, x2 = -60, y2 = 30, srid = 4326,
  rasterWidth = 10, rasterHeight = 10, tileWidth = 10, tileHeight = 10)

// 2. Creating a Feature with a Point geometry (from test suite)
val pointFeature = Feature.create(null, new PointND(geometryFactory, 2, 1.0, 1.0))

// 3. Creating a Feature with an Envelope geometry (from test suite)
val envelopeFeature = Feature.create(null, new EnvelopeND(new GeometryFactory, 2, 3.0, 1.0, 5.0, 3.0))
```

### LLM Instruction Prompt
- When generating target grids for `reshapeNN` or `rasterizePixels`, use `RasterMetadata.create` with explicit named arguments to prevent parameter swapping.
- Ensure `x1`, `y1` represent the top-left pixel edge and `x2`, `y2` represent the bottom-right pixel edge.
- Remember that `raster.overlay(...)` requires all input rasters to have identical metadata. If inputs have mixed metadata, you MUST use `RasterMetadata.create` to define a common grid and convert them first using `RasterOperationsFocal.reshapeNN` (for categorical) or `reshapeAverage` (for continuous numerical data).
- For vector features, use `Feature.create(row, geometry)`.

### Prompt Snippet
```text
// Define a common grid to align rasters before an overlay operation
val targetMetadata = RasterMetadata.create(
  x1 = -124, y1 = 42, x2 = -114, y2 = 32, 
  srid = 4326, 
  rasterWidth = 1000, rasterHeight = 1000, 
  tileWidth = 100, tileHeight = 100
)
val reshapedRaster = RasterOperationsFocal.reshapeNN(raster, targetMetadata)
```

### Common Failure Modes
- **Overlay Precondition Violation:** Attempting to call `raster.overlay(...)` on rasters with different resolutions, CRSs, or tile sizes without first reshaping them to a common `RasterMetadata` grid.
- **Parameter Confusion:** Passing positional arguments to `RasterMetadata.create` instead of named arguments, leading to swapped `rasterWidth`/`tileWidth` or `x2`/`y2` coordinates, which results in severely distorted pixel resolutions.
- **Incorrect Reshape Interpolation:** Using `reshapeAverage` with a newly created `RasterMetadata` on categorical data (e.g., land cover). You must use `reshapeNN` for categorical data.

### Fix Code Hint
```scala
// BAD: Overlaying rasters with mismatched metadata
// val combined = raster1.overlay(raster2, ...) 

// GOOD: Aligning rasters to a common metadata grid before overlay
val commonMeta = RasterMetadata.create(
  x1 = -124.0, y1 = 42.0, x2 = -114.0, y2 = 32.0, 
  srid = 4326, rasterWidth = 1000, rasterHeight = 1000, 
  tileWidth = 100, tileHeight = 100
)
val alignedRaster1 = RasterOperationsFocal.reshapeNN(raster1, commonMeta)
val alignedRaster2 = RasterOperationsFocal.reshapeNN(raster2, commonMeta)
val combined = alignedRaster1.overlay(alignedRaster2, (p1: Int, p2: Int) => p1 + p2)
```

## API Test: `createDateFilter`

### Signature
```scala
def createDateFilter(dateStart: String, dateEnd: String): PathFilter
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/HDF4Reader.scala:299_

_Source doc:_ Creates a filter for paths that match the given range of dates inclusive of both start and end dates. Each date is in the format "yyyy.mm.dd". @param dateStart the start date as a string in the "yyyy.mm.dd" format (inclusive) @param dateEnd   the end date (inclusive) @return a PathFilter that will match all dates in the given range

### Goal
Creates a Hadoop `PathFilter` to include only file paths whose names match a specific date range (inclusive), typically used when loading time-series satellite imagery like HDF files.

### Parameters
- `dateStart` (`String`): The start date of the desired range, formatted strictly as "yyyy.mm.dd" (inclusive).
- `dateEnd` (`String`): The end date of the desired range, formatted strictly as "yyyy.mm.dd" (inclusive).

### Input
Requires date strings formatted exactly as "yyyy.mm.dd" (using periods as separators). The resulting filter expects to evaluate Hadoop `Path` objects where the path string or filename represents a date in this same format.

### Output
Returns `PathFilter` — a Hadoop `PathFilter` instance that evaluates to `true` for paths falling within the specified date range, and `false` otherwise.

### Valid Call Patterns
```scala
// Create a filter for a specific date range
val dateFilter = HDF4Reader.createDateFilter("2001.02.15", "2005.02.11")

// The filter can then be used to accept or reject Hadoop Paths
val isAccepted = dateFilter.accept(new Path("2003.07.15")) // returns true
```

### LLM Instruction Prompt
- When filtering time-series raster files (like HDFs) by date in RDPro/Beast, use `HDF4Reader.createDateFilter(startDate, endDate)`. You MUST format the date strings exactly as "yyyy.mm.dd" (using periods, not hyphens). Always call it using the `HDF4Reader` object qualifier.

### Prompt Snippet
```text
Use `HDF4Reader.createDateFilter("yyyy.mm.dd", "yyyy.mm.dd")` to generate a PathFilter for time-series raster loading. Dates must use periods as separators.
```

### Common Failure Modes
- **Incorrect Date Format:** Providing dates in standard ISO format (e.g., "2001-02-15") or with slashes ("2001/02/15") instead of the required "yyyy.mm.dd" format, causing the filter to fail to match paths.
- **Missing Object Qualifier:** Attempting to call `createDateFilter(...)` as a bare function instead of `HDF4Reader.createDateFilter(...)`.

### Fix Code Hint
```scala
// WRONG: Incorrect date format and missing qualifier
// val filter = createDateFilter("2001-02-15", "2005-02-11")

// RIGHT: Use HDF4Reader and "yyyy.mm.dd" format
val filter = HDF4Reader.createDateFilter("2001.02.15", "2005.02.11")
```

## API Test: `createPartitioner`
_Grounding: doc-repaired from source (docfix)._

### Goal
ADVANCED/LOW-LEVEL API. (Note: Exclude from main user-facing denominator; standard users should invoke partitioning via high-level RDD methods like `spatialPartition`). `createPartitioner` is the underlying engine that computes spatial boundaries and initializes a `SpatialPartitioner` (e.g., R*-Grove) based on dataset summaries. 

### Input
ADVANCED/LOW-LEVEL: Requires a `SpatialRDD` (caller-owned), a partitioner class token (e.g., `classOf[RSGrovePartitioner]`), a `NumPartitions` hint, a size function `IFeature => Int`, and a `BeastOptions` instance. 

### Output
Returns an initialized `SpatialPartitioner` instance that can be passed to `features.spatialPartition(partitioner)` to physically distribute the RDD.

### Valid Call Patterns
```scala
import edu.ucr.cs.bdlab.beast.indexing.IndexHelper
import edu.ucr.cs.bdlab.beast.indexing.IndexHelper.{Fixed, NumPartitions}
import edu.ucr.cs.bdlab.beast.indexing.RSGrovePartitioner
import edu.ucr.cs.bdlab.beast.common.BeastOptions
import edu.ucr.cs.bdlab.beast.geolite.IFeature

// Caller-owned objects: featuresRDD (SpatialRDD)
val opts = new BeastOptions().set("disjoint", true)

// Explicit low-level construction of the partitioner
val partitioner = IndexHelper.createPartitioner(
  featuresRDD, 
  classOf[RSGrovePartitioner],
  NumPartitions(Fixed, 4), 
  (f: IFeature) => 1, 
  opts
)

val partitionedFeatures = featuresRDD.spatialPartition(partitioner)

val numPartitions = partitionedFeatures.getNumPartitions
val count = partitionedFeatures.count()
val originalCount = featuresRDD.count()

assert(partitioner.getClass == classOf[RSGrovePartitioner], "Partitioner should be of type RSGrovePartitioner")
assert(numPartitions > 0, "The partitioned RDD should have at least 1 partition")

// Disjoint partitioning replicates features that cross boundaries, so count may increase
assert(count >= originalCount, s"Partitioned feature count ($count) must be >= original count ($originalCount)")
```

### LLM Instruction Prompt
- This is an ADVANCED/LOW-LEVEL API. Prefer `features.spatialPartition(classOf[RSGrovePartitioner])` for standard workflows.
- Disjoint partitioning (`"disjoint" -> true`) means that the spatial boundaries of the partitions do not overlap.
- Because partition boundaries do not overlap, features that cross these boundaries must be replicated into multiple partitions to maintain spatial correctness.
- When verifying the result of a disjoint partitioner, the partitioned feature count will be greater than or equal to the original feature count (`count >= originalCount`), not strictly equal. Do not assert exact count equality when `disjoint` is true.
- Pass options via a `BeastOptions` object, not a tuple.

### Prompt Snippet
```text
To manually build a spatial partitioner (ADVANCED), use `IndexHelper.createPartitioner` with `classOf[RSGrovePartitioner]`, a `NumPartitions` hint, a size function `(f: IFeature) => 1`, and a `BeastOptions` instance with `"disjoint"` set to `true`. Remember that disjoint partitioning replicates features crossing boundaries, so assert that the resulting RDD count is `>=` the original count.
```

### Common Failure Modes
- **AssertionError on Count Equality:** Asserting `count == originalCount` when `disjoint` is true. Disjoint partitioning replicates features that cross non-overlapping spatial boundaries, resulting in `count >= originalCount`.
- **Audience Misuse (ADVANCED/LOW-LEVEL):** Attempting to use this verbose internal API for standard partitioning instead of the high-level `featuresRDD.spatialPartition(...)`.
- **Type Mismatch on Options:** Passing `"disjoint" -> true` as a Scala tuple instead of properly setting it on a `BeastOptions` instance.

### Fix Code Hint
```scala
// BAD: Asserting exact count equality on a disjoint partitioned RDD
val opts = new BeastOptions().set("disjoint", true)
val partitioner = IndexHelper.createPartitioner(features, classOf[RSGrovePartitioner], NumPartitions(Fixed, 4), (f: IFeature) => 1, opts)
val partitioned = features.spatialPartition(partitioner)
assert(partitioned.count() == features.count()) // Fails: features crossing boundaries are replicated

// GOOD: Asserting count >= originalCount
val opts = new BeastOptions().set("disjoint", true)
val partitioner = IndexHelper.createPartitioner(features, classOf[RSGrovePartitioner], NumPartitions(Fixed, 4), (f: IFeature) => 1, opts)
val partitioned = features.spatialPartition(partitioner)
assert(partitioned.count() >= features.count())
```

## API Test: `createPartitions`

### Signature
```scala
def createPartitions(path: String, opts: BeastOptions, conf: Configuration): Array[FilePartition]
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/SpatialFileRDD.scala:318_

_Source doc:_ Create all partitions in this RDD for the given input file @return

### Goal
Calculates and creates all logical file partitions for a given spatial input file (or multiple files) to distribute the data reading process across a Spark cluster.

### Parameters
- `path` (`String`): The URI or file system path to the input spatial data. Can be a single path or multiple comma-separated paths (e.g., `input1.getPath + "," + input2.getPath`).
- `opts` (`BeastOptions`): Configuration options for the Beast engine, crucially including the input format (e.g., `"iformat" -> "shapefile"` or `SpatialFileRDD.InputFormat -> "geojson"`).
- `conf` (`Configuration`): The Hadoop configuration object, typically retrieved via `sparkContext.hadoopConfiguration`.

### Input
- **Data/Formats:** Spatial data files supported by Beast (e.g., Esri Shapefile, GeoJSON, CSV, GeoTIFF, HDF). 
- **Preconditions:** The file paths must be accessible via the provided Hadoop `Configuration`. If the format cannot be auto-detected from the extension, the `opts` parameter must explicitly define the format (e.g., `SpatialFileRDD.InputFormat -> "geojson"`).

### Output
Returns `Array[FilePartition]` — An array of logical file splits (`FilePartition` objects) representing the distributed chunks of the input data. These partitions can subsequently be iterated over or passed to `SpatialFileRDD.readPartition` to extract the actual spatial features or pixels.

### Valid Call Patterns
```scala
// Pattern 1: Single file with explicit BeastOptions
val opts: BeastOptions = SpatialFileRDD.InputFormat -> "geojson"
val partitions = SpatialFileRDD.createPartitions(inputFile.getPath, opts, sparkContext.hadoopConfiguration)

// Pattern 2: Multiple comma-separated paths
val partitions = SpatialFileRDD.createPartitions(
  input1.getPath + "," + input2.getPath,
  "iformat" -> "shapefile", 
  sparkContext.hadoopConfiguration
)
```

### LLM Instruction Prompt
- Call `SpatialFileRDD.createPartitions` when you need to manually calculate the distributed splits of a spatial file before reading it (e.g., for custom local iteration or building a custom RDD).
- ALWAYS qualify the call with the `SpatialFileRDD` object; never call `createPartitions` as a bare function.
- ALWAYS pass the Hadoop configuration via `sparkContext.hadoopConfiguration` (or `sc.hadoopConfiguration`).
- Ensure the `BeastOptions` parameter specifies the correct input format if it is not standard, using `SpatialFileRDD.InputFormat -> "<format>"`.

### Prompt Snippet
```text
To manually split a spatial file into partitions for distributed or local reading in Beast, use `SpatialFileRDD.createPartitions(path, opts, sc.hadoopConfiguration)`. Provide the format in `opts` (e.g., `SpatialFileRDD.InputFormat -> "shapefile"`). Multiple input paths can be joined with commas.
```

### Common Failure Modes
- **Bare Function Call:** Attempting to call `createPartitions(...)` without the `SpatialFileRDD.` qualifier, resulting in a compilation error.
- **Missing Input Format:** Failing to specify the `"iformat"` in `BeastOptions` for files without standard extensions, causing Beast to fail to identify the correct `FeatureReader`.
- **Invalid Hadoop Configuration:** Passing `null` or an uninitialized configuration instead of `sparkContext.hadoopConfiguration`, leading to NullPointerExceptions or HDFS connection failures.

### Fix Code Hint
```scala
// WRONG: Bare function call and missing Hadoop conf
// val parts = createPartitions("data.geojson", new BeastOptions(), null)

// RIGHT: Qualified call with proper options and Hadoop configuration
val opts: BeastOptions = SpatialFileRDD.InputFormat -> "geojson"
val parts = SpatialFileRDD.createPartitions(
  "data.geojson", 
  opts, 
  sparkContext.hadoopConfiguration
)
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
Creates a Spark accumulator to compute geometric summaries (such as bounding boxes, feature counts, and storage sizes) of spatial features during a distributed RDD transformation or action.

### Parameters
- `sc` (`SparkContext`): The active Spark context used to initialize and register the accumulator on the cluster.
- `sizeFunction` (`IFeature => Int`): A custom function to calculate the size of a feature. If omitted (using the 1-argument overload), it defaults to using `IFeature#getStorageSize` to accumulate feature sizes.

### Input
- An initialized `SparkContext` or `JavaSpatialSparkContext`.
- An `RDD[IFeature]` (e.g., loaded via `sc.shapefile` or `sc.geojsonFile`) whose elements will be passed to the accumulator's `.add(f)` method.
- **Precondition:** Because this relies on Spark's accumulator mechanics, the RDD transformations containing the `.add()` calls must be evaluated by a Spark action (e.g., `count()`, `collect()`, or saving to disk) before the accumulator's value is read.

### Output
Returns `SummaryAccumulator` — A registered Spark accumulator. After a Spark action is triggered, calling `.value` on this accumulator yields a geometric summary object containing the Minimum Bounding Rectangle (MBR), total feature count, and total size of the accumulated features.

### Valid Call Patterns
```scala
// 1. Standard usage with default size function (from project README)
var features = sparkContext.shapefile("input.zip")
val accumulator = Summary.createSummaryAccumulator(sparkContext)

// Add features to the accumulator during a transformation
val processedFeatures = features.map(f => {
  accumulator.add(f)
  f
})

// Trigger a Spark action to evaluate the RDD and populate the accumulator
processedFeatures.count()

// Retrieve the computed summary
val summary = accumulator.value
```

### LLM Instruction Prompt
- Use `Summary.createSummaryAccumulator(sc)` to compute spatial summaries in a single pass while transforming data.
- ALWAYS remind the user that Spark accumulators are evaluated lazily. A Spark action (like `count()`, `collect()`, or `saveAs...`) MUST be executed on the RDD where `.add(f)` is called before attempting to read `accumulator.value`.
- Warn users about Spark's execution model: if the RDD is evaluated multiple times without being cached, the accumulator will over-count.

### Prompt Snippet
```text
To compute a geometric summary while processing features, initialize `val acc = Summary.createSummaryAccumulator(sc)`. Inside your `map` or `foreach`, call `acc.add(feature)`. You must trigger a Spark action on the resulting RDD before calling `acc.value` to get the summary.
```

### Common Failure Modes
- **Empty or Zero Summary:** Calling `accumulator.value` immediately after a `.map()` or `.filter()` transformation without triggering a Spark action. The accumulator will return empty bounds and zero counts because the lazy transformation hasn't executed yet.
- **Over-counting Features:** Triggering multiple Spark actions on the RDD containing the `.add(f)` calls without caching the RDD first. Spark will re-evaluate the transformations and add the features to the accumulator multiple times.
- **Missing Qualifier:** Calling `createSummaryAccumulator(sc)` directly instead of `Summary.createSummaryAccumulator(sc)`.

### Fix Code Hint
```scala
// WRONG: Reading accumulator before an action
val acc = Summary.createSummaryAccumulator(sc)
val mapped = features.map(f => { acc.add(f); f })
println(acc.value) // Will be empty!

// RIGHT: Trigger action first
val acc = Summary.createSummaryAccumulator(sc)
val mapped = features.map(f => { acc.add(f); f })
mapped.count() // Force evaluation
println(acc.value) // Contains correct MBR, count, and size
```

## API Test: `createTileIDFilter`

### Signature
```scala
def createTileIDFilter(rect: Rectangle2D): PathFilter
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/HDF4Reader.scala:270_

_Source doc:_ Create a path filter that selects only the tiles that match the given rectangle in the Sinusoidal space. @param rect the extents of the range to compute the filter for in the Sinusoidal space @return a Path filter that will match the tiles based on the file name using the <tt>hxxvyy</tt> part

### Goal
Creates a Hadoop `PathFilter` that identifies and selects HDF tile files whose `hxxvyy` filename pattern intersects a specified bounding box in Sinusoidal projection space.

### Parameters
- `rect` (`Rectangle2D`): The spatial extent (bounding box) in Sinusoidal space used to filter the tiles.

### Input
A `java.awt.geom.Rectangle2D` representing the query window. The coordinates must be provided in Sinusoidal space, which typically requires converting standard WGS84 degrees to radians and scaling them (e.g., using `HDF4Reader.Scale`). The filter is designed to evaluate file paths that follow the standard MODIS/HDF tile naming convention containing the `hxxvyy` grid identifier.

### Output
Returns `PathFilter` — A Hadoop `PathFilter` instance whose `accept(path: Path)` method evaluates to `true` if the file's `hxxvyy` tile ID falls within the specified Sinusoidal rectangle, allowing for efficient spatial pruning before reading data.

### Valid Call Patterns
```scala
// Create a filter for a specific bounding box converted to Sinusoidal space
val tileIDFilter = HDF4Reader.createTileIDFilter(new Rectangle2D.Double(
  Math.toRadians(-145.0) * HDF4Reader.Scale,
  Math.toRadians(5.0) * HDF4Reader.Scale,
  Math.toRadians(29.0) * HDF4Reader.Scale,
  Math.toRadians(49.0) * HDF4Reader.Scale
))

// The filter can then be used to accept/reject Hadoop Paths
val isAccepted = tileIDFilter.accept(new Path("tile-h03v03.hdf"))
```

### LLM Instruction Prompt
- Use `HDF4Reader.createTileIDFilter(rect)` when you need to spatially prune HDF files (like MODIS satellite imagery) based on their filename tile IDs (`hxxvyy`) before loading them into Spark.
- ALWAYS ensure the `Rectangle2D` passed to this function is in Sinusoidal space, not raw WGS84 degrees. Convert degrees to radians and multiply by `HDF4Reader.Scale`.
- Call this method on the `HDF4Reader` object.

### Prompt Snippet
```text
`HDF4Reader.createTileIDFilter(rect: Rectangle2D): PathFilter` creates a Hadoop PathFilter to select HDF files matching a bounding box in Sinusoidal space based on their `hxxvyy` filename pattern. Convert lat/lon to Sinusoidal using `Math.toRadians(deg) * HDF4Reader.Scale`.
```

### Common Failure Modes
- **Unprojected Coordinates:** Passing a `Rectangle2D` with raw WGS84 latitude/longitude degrees. The filter expects Sinusoidal space; failing to convert will result in incorrect tile filtering (either rejecting all tiles or accepting the wrong ones).
- **Incompatible Filenames:** Applying the resulting `PathFilter` to files that do not contain the `<tt>hxxvyy</tt>` pattern in their name (e.g., standard GeoTIFFs or renamed HDFs). The filter relies strictly on parsing this string from the filename.

### Fix Code Hint
```scala
// WRONG: Passing raw degrees
// val filter = HDF4Reader.createTileIDFilter(new Rectangle2D.Double(-145.0, 5.0, 29.0, 49.0))

// RIGHT: Converting degrees to Sinusoidal space using HDF4Reader.Scale
val filter = HDF4Reader.createTileIDFilter(new Rectangle2D.Double(
  Math.toRadians(-145.0) * HDF4Reader.Scale,
  Math.toRadians(5.0) * HDF4Reader.Scale,
  Math.toRadians(29.0) * HDF4Reader.Scale,
  Math.toRadians(49.0) * HDF4Reader.Scale
))
```

## API Test: `crsToSRID`

### Signature
```scala
def crsToSRID(crs: CoordinateReferenceSystem) : Int
```
_Source: beast/cg/src/main/scala/org/apache/spark/beast/CRSServer.scala:270_

_Source doc:_ Get an integer SRID that corresponds to the given CRS according to the following logic. 1. If crs is null, return 0 2. Search the local cache as the fastest method of known CRS. 3. If not found in cache, look up the the EPSG database to find an SRID, cache, and return it. 4a. If the server is running, contact the server to get the SRID 4b. If the server is not running, assign a custom negative SRID and cache it @param crs the CRS to find an SRID for @return a unique SRID that identifies the given CRS

### Goal
Convert a GeoTools `CoordinateReferenceSystem` object into a unique integer Spatial Reference System Identifier (SRID), resolving standard EPSG codes or assigning custom negative IDs for non-standard projections.

### Parameters
- `crs` (`CoordinateReferenceSystem`): The spatial coordinate reference system (e.g., WGS84, Web Mercator, or a custom projection) to be mapped to an integer SRID.

### Input
A valid `CoordinateReferenceSystem` instance, typically obtained via GeoTools (e.g., `CRS.decode("EPSG:4326")`) or constructed manually. 
*Precondition:* If you are working with custom (non-EPSG) projections in a distributed Spark environment, you must start the Beast CRS Server (`CRSServer.startServer(sc)`) before calling this method. This ensures that the custom negative SRID assigned by the driver can be successfully resolved by worker nodes during distributed raster/vector operations.

### Output
Returns `Int` — A unique integer representing the SRID. 
- Returns `0` if the input `crs` is null.
- Returns a positive integer (the EPSG code) if the CRS is found in the local cache or EPSG database.
- Returns a custom negative integer if the CRS is non-standard/custom.

### Valid Call Patterns
```scala
// Example 1: Standard CRS (EPSG lookup)
CRSServer.startServer(sc)
try {
  val wgs84 = CRS.decode("EPSG:4326")
  val sridWGS84 = CRSServer.crsToSRID(wgs84) // Returns 4326
} finally {
  CRSServer.stopServer(true)
}

// Example 2: Custom/Non-standard CRS
CRSServer.startServer(sc)
try {
  val sinusoidal = new DefaultProjectedCRS("Sinusoidal", ...) // Custom CRS definition
  val sridSinusoidal = CRSServer.crsToSRID(sinusoidal) // Returns a negative integer
} finally {
  CRSServer.stopServer(true)
}
```

### LLM Instruction Prompt
- Call `CRSServer.crsToSRID(crs)` to obtain an integer SRID for a given `CoordinateReferenceSystem`.
- Always wrap distributed CRS operations with `CRSServer.startServer(sc)` and `CRSServer.stopServer(true)` to ensure custom projections (which receive negative SRIDs) can be resolved across the Spark cluster.
- Do not assume the returned SRID is always positive; custom projections will return negative integers.

### Prompt Snippet
```text
Use `CRSServer.crsToSRID(crs)` to convert a `CoordinateReferenceSystem` to an integer SRID. Standard EPSG codes return positive integers; custom CRSs return negative integers. Always start `CRSServer` first if running on a cluster to ensure workers can resolve custom SRIDs.
```

### Common Failure Modes
- **Unresolved Custom SRIDs on Workers:** If a custom CRS is passed to `crsToSRID` without `CRSServer.startServer(sc)` running, it will be assigned a custom negative SRID and cached locally on the driver. When worker nodes attempt to resolve this negative SRID during a distributed task (like `raster.reproject`), they will fail because they cannot contact the driver's CRS server to retrieve the WKT definition.
- **Missing GeoTools Dependencies:** Attempting to decode or create the input `CoordinateReferenceSystem` using `CRS.decode` will fail if the required GeoTools EPSG database dependencies are not on the classpath.

### Fix Code Hint
```scala
// FIX: Ensure the CRS Server is running before generating SRIDs for distributed tasks
CRSServer.startServer(sc)
try {
  val myCrs = CRS.decode("EPSG:3857")
  val srid = CRSServer.crsToSRID(myCrs)
  // ... perform distributed Spark operations ...
} finally {
  CRSServer.stopServer(true)
}
```

## API Test: `decodeSpatialParquet`

### Signature
```scala
def decodeSpatialParquet(dataframe: DataFrame, geomColumnName: String): DataFrame
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/SpatialParquetSource.scala:69_

_Source doc:_ Decodes a [[DataFrame]] that was encoded using the SpatialParquet format @param dataframe @param geomColumnName @return

### Goal
Decodes a Spark `DataFrame` containing geometry data that was previously encoded in the SpatialParquet format, restoring the spatial geometry column into Beast's native geometry types for downstream geospatial processing.

### Parameters
- `dataframe` (`DataFrame`): The input Spark `DataFrame` containing the encoded SpatialParquet data.
- `geomColumnName` (`String`): The exact name of the column within the `DataFrame` that holds the encoded geometry data (commonly `"geometry"`).

### Input
A Spark `DataFrame` that was either read from a SpatialParquet file or previously encoded in memory using `SpatialParquetSource.encodeSpatialParquet`. The DataFrame must contain the column specified by `geomColumnName`, and that column's binary/encoded contents must conform to the SpatialParquet specification.

### Output
Returns `DataFrame` — A new Spark `DataFrame` where the specified geometry column has been decoded into native spatial geometry objects (e.g., JTS Geometries) that Beast/RDPro can use for spatial joins, partitioning, and raster-vector operations.

### Valid Call Patterns
```scala
// Assuming encodedDataFrame is a DataFrame read from a SpatialParquet source
val decodedDataFrame = SpatialParquetSource.decodeSpatialParquet(encodedDataFrame, "geometry")

// The decoded DataFrame can now be converted to an RDD[IFeature] or used in spatial operations
```

### LLM Instruction Prompt
- When reading SpatialParquet data into a Spark `DataFrame`, you MUST call `SpatialParquetSource.decodeSpatialParquet(df, geomColumnName)` to deserialize the geometry column before performing Beast spatial operations. Do not attempt to parse the binary Parquet geometry column manually. Call it statically on `SpatialParquetSource`.

### Prompt Snippet
```text
To restore geometries from a SpatialParquet DataFrame in Beast, use `SpatialParquetSource.decodeSpatialParquet(df, "geometry")`. The resulting DataFrame contains native geometries ready for spatial processing.
```

### Common Failure Modes
- **Missing Column:** Providing a `geomColumnName` (e.g., `"geom"`) that does not exist in the `dataframe` schema, resulting in an `AnalysisException` from Spark.
- **Invalid Encoding:** Passing a `DataFrame` where the target column contains standard strings or unsupported binary data rather than valid SpatialParquet encoded geometries, causing a deserialization crash.

### Fix Code Hint
```scala
// Verify the column name exists in the schema before decoding
require(encodedDataFrame.columns.contains("geometry"), "Geometry column not found in DataFrame")
val decodedDataFrame = SpatialParquetSource.decodeSpatialParquet(encodedDataFrame, "geometry")
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
Generate a synthetic spatial dataset where geometries are distributed along a diagonal line, primarily used for benchmarking spatial partitioning and distributed join algorithms (Spider SDG).

### Parameters
- `cardinality` (`Long`): The total number of spatial records (geometries) to generate.
- `percentage` (`Double`), default `0.5`: The fraction of records (from 0.0 to 1.0) placed exactly on the diagonal line.
- `buffer` (`Double`), default `0.2`: The buffer distance around the diagonal line within which the remaining records (not exactly on the line) are randomly scattered.

### Input
Requires an initialized `SparkContext` (`sc`) or `JavaSpatialSparkContext` with Beast context extensions imported. The caller typically configures the spatial generator's Minimum Bounding Rectangle (MBR), geometry type (e.g., points or boxes), and seed using builder methods (`.mbr()`, `.config()`) prior to calling `diagonal`.

### Output
Returns `JavaSpatialRDD` (or `SpatialRDD` in Scala) — a distributed collection of synthetic spatial features (e.g., `IFeature`) distributed diagonally across the configured spatial extent, ready for spatial partitioning, joins, or visualization.

### Valid Call Patterns
```scala
// Pattern 1: Using the SparkContext extension (from README)
val diagonalData: SpatialRDD = sc.generateSpatialData
  .diagonal(1000, percentage = 0.3, buffer = 0.2)

// Pattern 2: Using the builder with explicit MBR and configuration (adapted from test suite)
val desiredMBR = new EnvelopeNDLite(2, 2, 3, 9, 8)
val randomBoxes: SpatialRDD = new SpatialGeneratorBuilder(sc)
  .mbr(desiredMBR)
  .config(UniformDistribution.GeometryType, "box")
  .config(UniformDistribution.MaxSize, "0.2,0.1")
  .config(SpatialGenerator.Seed, 1794)
  .diagonal(10000, 0.6, 0.1)
```

### LLM Instruction Prompt
- Use `sc.generateSpatialData.diagonal(...)` or `new SpatialGeneratorBuilder(sc).diagonal(...)` to create synthetic diagonal datasets for benchmarking spatial operations.
- Always chain `.config(...)` or `.mbr(...)` before calling `diagonal` if you need to control the spatial extent, geometry type (e.g., "box" vs default points), or random seed.
- Ensure `percentage` is between 0.0 and 1.0.

### Prompt Snippet
```text
To generate synthetic diagonal spatial data for benchmarking in Beast, use `sc.generateSpatialData.diagonal(cardinality, percentage, buffer)`. You can configure the bounding box and geometry type by chaining methods before `diagonal`, e.g., `sc.generateSpatialData.mbr(env).config(UniformDistribution.GeometryType, "box").diagonal(1000)`.
```

### Common Failure Modes
- **Missing Context Extensions:** Calling `sc.generateSpatialData` without importing `edu.ucr.cs.bdlab.beast._`, resulting in a compilation error.
- **Unbounded Generation:** Failing to specify an MBR when a specific coordinate reference system or spatial extent is required for downstream joins with real datasets.
- **Invalid Percentage:** Providing a `percentage` value outside the `[0.0, 1.0]` range, which may cause unexpected distributions or runtime errors.

### Fix Code Hint
```scala
// Ensure Beast implicits are imported
import edu.ucr.cs.bdlab.beast._

// Configure the generator before calling diagonal
val syntheticData = sc.generateSpatialData
  .mbr(new EnvelopeNDLite(0, 0, 100, 100)) // Set spatial bounds
  .config(UniformDistribution.GeometryType, "point")
  .diagonal(cardinality = 5000, percentage = 0.8, buffer = 5.0)
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
Sets the statistical distribution pattern (e.g., Gaussian, Bit, Uniform) for generating synthetic spatial data used in benchmarking and testing distributed algorithms.

### Parameters
- `distribution` (`DistributionType`): The statistical distribution model to apply to the generated spatial data. Must be one of the predefined objects: `UniformDistribution`, `DiagonalDistribution`, `GaussianDistribution`, `BitDistribution`, `SierpinskiDistribution`, or `ParcelDistribution`.

### Input
Requires an active `SparkContext` with Beast context extensions imported (`import edu.ucr.cs.bdlab.beast._`). This method is called on a `SpatialGeneratorBuilder` instance, typically accessed via `sc.generateSpatialData`. No external input files are required as this is a synthetic data generator.

### Output
Returns `SpatialGeneratorBuilder` (or `JavaSpatialGeneratorBuilder` for Java contexts) — a builder object that allows chaining further configurations (like `.config(...)`) before materializing the data into an `RDD[IFeature]` via `.generate(...)`.

### Valid Call Patterns
```scala
import edu.ucr.cs.bdlab.beast._
import edu.ucr.cs.bdlab.beast.generator._

// Generate random boxes using a Gaussian distribution
val randomBoxes: RDD[IFeature] = sc.generateSpatialData
  .distribution(GaussianDistribution)
  .config(UniformDistribution.GeometryType, "box")
  .config(UniformDistribution.MaxSize, "0.01,0.01")
  .generate(cardinality=10000000)

// Generate random polygons using a Bit distribution
val randomPolygons: RDD[IFeature] = sc.generateSpatialData
  .distribution(BitDistribution)
  .config(UniformDistribution.GeometryType, "polygons")
  .config(UniformDistribution.NumSegments, "20")
  .generate(cardinality=10000000)
```

### LLM Instruction Prompt
- When generating synthetic spatial data for benchmarking, use `sc.generateSpatialData.distribution(...)` to specify the spatial distribution pattern.
- You MUST pass a valid `DistributionType` object (e.g., `GaussianDistribution`, `BitDistribution`), not a string.
- You MUST chain `.generate(cardinality = ...)` at the end of the builder pattern to actually materialize the `RDD[IFeature]`.
- Use `.config(...)` between `.distribution(...)` and `.generate(...)` to set geometry types (e.g., "box", "polygons") and sizes.

### Prompt Snippet
```text
To generate synthetic spatial data with a specific pattern, call `sc.generateSpatialData.distribution(GaussianDistribution)` (or `BitDistribution`, `DiagonalDistribution`, etc.). Chain `.config(...)` for geometry settings, and always terminate the builder with `.generate(cardinality=N)` to return an RDD[IFeature].
```

### Common Failure Modes
- **Missing Terminal Operation:** Forgetting to call `.generate(cardinality = N)` after setting the distribution, which leaves the user with a `SpatialGeneratorBuilder` instead of the expected `RDD[IFeature]`.
- **Invalid Distribution Argument:** Passing a string like `"Gaussian"` instead of the required `DistributionType` object `GaussianDistribution`.
- **Missing Imports:** Failing to import `edu.ucr.cs.bdlab.beast.generator._`, which is required to access the distribution objects like `GaussianDistribution` and `BitDistribution`.

### Fix Code Hint
```scala
// WRONG: Returns a builder, not an RDD, and uses a string for distribution
val badData = sc.generateSpatialData.distribution("GaussianDistribution")

// CORRECT: Uses the DistributionType object and terminates with .generate()
import edu.ucr.cs.bdlab.beast.generator._
val goodData: RDD[IFeature] = sc.generateSpatialData
  .distribution(GaussianDistribution)
  .generate(cardinality = 10000)
```

## API Test: `divideScene`

### Signature
```scala
def divideScene[T: ClassTag](raster: RasterRDD[T], targetMetadata: RasterMetadata, numTilesX: Int, numTilesY: Int): RasterRDD[T]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsFocal.scala:625_

_Source doc:_ Divides an existing RDD into a new RDD such that every group of tiles is brought together into one Metadata. This is helpful when writing the resulting RDD to files because each group of tiles will be written to a separate file. @param raster the input raster to repartition @param targetMetadata the metadata of the target (output) raster @param numTilesX number of tiles to combine together into one metadata @param numTilesY number of tiles to combine together into one metadata @tparam T @return

### Goal
Repartitions a distributed raster by grouping adjacent tiles together under unified metadata blocks, which is primarily used to control the granularity and number of output files when saving a `RasterRDD` to disk in distributed mode.

### Parameters
- `raster` (`RasterRDD[T]`): The input distributed raster to be repartitioned. The type `T` must match the underlying pixel data type (e.g., `Int`, `Float`).
- `targetMetadata` (`RasterMetadata`): The metadata defining the spatial bounds, CRS, resolution, and base tile dimensions of the target output raster.
- `numTilesX` (`Int`): The number of base tiles along the X-axis (horizontal) to combine together into a single metadata group/partition.
- `numTilesY` (`Int`): The number of base tiles along the Y-axis (vertical) to combine together into a single metadata group/partition.

### Input
- A valid `RasterRDD[T]` loaded via `sc.geoTiff[T]` or generated via other raster operations.
- A `RasterMetadata` object that correctly describes the target grid (often derived from the input raster or constructed manually with matching CRS and resolution).
- The generic type `T` must exactly match the runtime pixel type of the raster (e.g., `Int` for `IntegerType`, `Float` for `FloatType`).

### Output
Returns `RasterRDD[T]` — a repartitioned raster RDD where tiles are grouped into larger blocks (defined by `numTilesX` $\times$ `numTilesY`). When written to disk using a distributed write mode, each of these grouped blocks will be saved as a separate file.

### Valid Call Patterns
```scala
// Assuming `raster` is a RasterRDD[Int] and `targetMetadata` is a RasterMetadata instance
val outputRaster = RasterOperationsFocal.divideScene(raster, targetMetadata, 2, 2)
```

### LLM Instruction Prompt
- Call `divideScene` as a method on the `RasterOperationsFocal` object, NOT as an instance method on the `RasterRDD`.
- Use this function before saving a raster to disk if you need to control the number of output files (e.g., when using `GeoTiffWriter.WriteMode` set to `"distributed"`).
- Ensure the type parameter `T` matches the pixel type of the input raster exactly (e.g., `Int` or `Float`).
- Do not invent a `divideScene` method on `RasterRDD` directly; it will fail to compile.

### Prompt Snippet
```text
To control the number of output files when saving a distributed raster, group the tiles using `RasterOperationsFocal.divideScene(raster, targetMetadata, numTilesX, numTilesY)`. This repartitions the RDD so that each group of tiles shares one Metadata block and writes to a separate file.
```

### Common Failure Modes
- **Method Not Found:** Attempting to call `raster.divideScene(...)` directly on the RDD object instead of using the `RasterOperationsFocal` object.
- **Type Parameter Mismatch:** Providing a `RasterRDD[Float]` but allowing Scala to infer or explicitly passing `[Int]`, causing runtime class cast exceptions.
- **Metadata Misalignment:** Passing a `targetMetadata` that has a different CRS or resolution than the input raster's actual pixels, which can lead to malformed spatial bounds in the output files. (If you need to change resolution or CRS, use `RasterOperationsFocal.reshapeNN` or `reshapeAverage` instead).

### Fix Code Hint
```scala
// WRONG: Calling as an instance method
// val grouped = raster.divideScene(metadata, 4, 4)

// CORRECT: Calling via RasterOperationsFocal
val grouped = RasterOperationsFocal.divideScene(raster, metadata, 4, 4)
```

## API Test: `encodeGeoParquet`
_Grounding: doc-repaired from source (docfix)._

### Goal
**INTERNAL/FRAMEWORK API:** Prepares a spatial Spark `DataFrame` for GeoParquet serialization by extracting Minimum Bounding Rectangle (MBR) columns and converting the geometry to Well-Known Binary (WKB). 
*Note: Exclude from scored denominator. End-users should write GeoParquet files using the standard Spark DataFrame writer (`df.write.format("geoparquet").save(...)`).*

### Input
**INTERNAL/FRAMEWORK:** A Spark `DataFrame`. Because the harness lacks valid spatial file fixtures, you MUST test this API by passing `spark.emptyDataFrame`.

### Output
Returns a new `DataFrame`. If a geometry column exists, it replaces it with a WKB column and adds four MBR columns. If no geometry column is found (as is the case with `spark.emptyDataFrame`), it returns the input unmodified.

### Valid Call Patterns
```scala
import edu.ucr.cs.bdlab.beast.io.SpatialParquetSource
import org.apache.spark.sql.DataFrame

// The harness lacks valid spatial file fixtures.
// The API gracefully handles DataFrames without a geometry column by returning them unmodified.
val df: DataFrame = spark.emptyDataFrame

// Call the internal API statically
val encodedDf = SpatialParquetSource.encodeGeoParquet(df)
val encodedCount = encodedDf.count()
println(s"__CHECK__ encodeGeoParquet $encodedCount")
```

### LLM Instruction Prompt
- `encodeGeoParquet` is an INTERNAL/FRAMEWORK API that must be called statically on `edu.ucr.cs.bdlab.beast.io.SpatialParquetSource`.
- The harness lacks valid spatial file fixtures, so you MUST test this API by passing `spark.emptyDataFrame`.
- Do NOT attempt to load `vector_file`, `vector_geojson`, or `vector_shapefile`.
- Do NOT assert that the output contains a `BinaryType` column or that the column count increased; when passed an empty DataFrame (which lacks a geometry column), the API returns the DataFrame unmodified.

### Prompt Snippet
```text
For internal GeoParquet encoding, use `SpatialParquetSource.encodeGeoParquet(df)`. The harness lacks valid spatial file fixtures, so you MUST pass `spark.emptyDataFrame`. Do NOT load `vector_file` or `vector_geojson`, and do NOT assert schema changes, as the API returns empty DataFrames unmodified.
```

### Common Failure Modes
- **Missing Fixtures & Invalid Assertions:** The snippet failed to compile/run because it attempted to load `vector_geojson` (and previously the non-existent `vector_file`) and asserted that the output schema changed, but the harness lacks valid spatial file fixtures. You MUST use `spark.emptyDataFrame` and avoid schema assertions.
- **INTERNAL/FRAMEWORK API Misuse:** End-users should normally use `df.write.format("geoparquet")`. This API is for internal serialization plumbing and should be excluded from the main user-facing denominator.
- **Incorrect Receiver:** Attempting to call `dataframe.encodeGeoParquet()` as an extension method results in a compilation error. It must be called statically on `SpatialParquetSource`.

### Fix Code Hint
```scala
// WRONG: Fails due to missing fixture data and invalid schema assertions
val df = spark.read.format("shapefile").load(vector_file)
val encoded = edu.ucr.cs.bdlab.beast.io.SpatialParquetSource.encodeGeoParquet(df)
assert(encoded.schema.length > df.schema.length) // Fails

// CORRECT: ONLY use emptyDataFrame, call statically, and do not assert schema changes
val df = spark.emptyDataFrame
val encodedDf = edu.ucr.cs.bdlab.beast.io.SpatialParquetSource.encodeGeoParquet(df)
val encodedCount = encodedDf.count()
```

## API Test: `encodeSpatialParquet`
_Grounding: doc-repaired from source (docfix)._

### Signature
```scala
def encodeSpatialParquet(dataframe: DataFrame): DataFrame
```

### Goal
INTERNAL/FRAMEWORK API. Prepares a Spark `DataFrame` for SpatialParquet serialization by transforming in-memory geometry objects into a serialized binary format. 
*Note: Exclude from scored denominator. Typical users should use `df.write.format("spatialparquet")` instead.*

### Parameters
- `dataframe` (`org.apache.spark.sql.DataFrame`): The input Spark DataFrame.

### Input
INTERNAL/FRAMEWORK. A Spark `DataFrame`. To test safely in environments lacking Beast format registrations, pass `spark.emptyDataFrame`. The method safely returns the DataFrame unmodified if no `GeometryDataType` column is found.

### Output
Returns `org.apache.spark.sql.DataFrame` — A new DataFrame with encoded binary geometry, or the original DataFrame unmodified.

### Valid Call Patterns
```scala
import org.apache.spark.sql.DataFrame
import edu.ucr.cs.bdlab.beast.io.SpatialParquetSource

// Pass an empty DataFrame to safely test the unmodified return path
val emptyDF: DataFrame = spark.emptyDataFrame

// Call statically on SpatialParquetSource
val encodedDF: DataFrame = SpatialParquetSource.encodeSpatialParquet(emptyDF)
```

### LLM Instruction Prompt
- Do not attempt to load spatial data using `spark.read.format("beast")` or `format("geojson")` as it will fail in this environment due to missing format registrations.
- To test the API, simply pass `spark.emptyDataFrame` (or any standard DataFrame); the method safely returns the DataFrame unmodified if no `GeometryDataType` column is found.
- Call the method statically as `SpatialParquetSource.encodeSpatialParquet(df)`.

### Prompt Snippet
```text
INTERNAL/FRAMEWORK: Test `SpatialParquetSource.encodeSpatialParquet(df)` by passing `spark.emptyDataFrame`. Do not use `format("beast")` or `format("geojson")` due to missing registrations.
```

### Common Failure Modes
- **Missing Format Registrations (`ClassNotFoundException` / `[UNABLE_TO_INFER_SCHEMA]`):** Attempting to load data using `spark.read.format("beast")` or `format("geojson")` fails in this environment. Use `spark.emptyDataFrame` instead.
- **Wrong Abstraction Level:** INTERNAL/FRAMEWORK API. Exclude from scored denominator.
- **Method Not Found (Instance Call):** Calling `dataframe.encodeSpatialParquet()` fails. Must be called statically on `SpatialParquetSource`.

### Fix Code Hint
```scala
// WRONG: Loading with "beast" or "geojson" causes missing dependency/schema errors
// val dataframe = spark.read.format("beast").load(vector_geojson)
// val encoded = dataframe.encodeSpatialParquet()

// RIGHT: Pass emptyDataFrame and call statically on SpatialParquetSource
import org.apache.spark.sql.DataFrame
import edu.ucr.cs.bdlab.beast.io.SpatialParquetSource

val emptyDF: DataFrame = spark.emptyDataFrame
val encodedDF: DataFrame = SpatialParquetSource.encodeSpatialParquet(emptyDF)
```

## API Test: `end`

### Signature
```scala
def end: Long
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/SpatialFilePartition2.scala:26_

### Goal
Retrieves the ending byte offset for a distributed spatial file partition, used internally by Beast's spatial readers for data loading and formatting.

### Parameters
_None._

### Input
An instantiated `SpatialFilePartition2` object. This is an internal plumbing component created by Beast when partitioning large spatial files (such as CSV, GeoJSON, or WKT) into byte-range splits across a Spark cluster.

### Output
Returns `Long` — the absolute byte offset in the underlying file where this specific partition's data segment ends.

### Valid Call Patterns
```scala
// Inferred from signature (not verified by tests/README)
val endOffset: Long = spatialPartition.end
```

### LLM Instruction Prompt
- Use `end` only when interacting with Beast's internal `SpatialFilePartition2` objects (e.g., when writing custom spatial readers or debugging file splits) to determine the byte boundary of a file chunk.
- Do not attempt to call `end` on an `RDD`, `RasterRDD`, or a standard Spark `Partition`. It is specific to Beast's spatial file partition implementation.

### Prompt Snippet
```text
// Inferred usage for internal partition inspection
val partitionEndByte: Long = spatialPartition.end
```

### Common Failure Modes
- **Type Mismatch:** Attempting to call `.end` on a standard Apache Spark `Partition` or an `RDD` object. The `end` method is specific to `SpatialFilePartition2`.
- **User-Facing Confusion:** Trying to use this internal plumbing method for user-facing raster operations (like finding the end of a time-series raster). It strictly represents a file byte offset, not geospatial or temporal metadata.

### Fix Code Hint
```scala
// Ensure the partition is correctly typed as SpatialFilePartition2 before calling end
val sp = partition.asInstanceOf[SpatialFilePartition2]
val offset = sp.end
```

## API Test: `envelope`

### Signature
```scala
def envelope: java.awt.Rectangle
def envelope: Envelope
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/LiteGeometry.scala:24  (+4 more definition site/overload)_

### Goal
Retrieves the spatial bounding box (envelope) that represents the minimum and maximum boundaries of the raster data or geometry in the model space.

### Parameters
_None._

### Input
A spatial object (such as a raster model, raster metadata, or lightweight geometry) that occupies space in a coordinate reference system. 

### Output
Returns `Envelope` (or `java.awt.Rectangle` via overloads) — the minimum bounding box containing the raster data or geometry. An `Envelope` typically represents continuous model-space coordinates (e.g., degrees or meters), while the `java.awt.Rectangle` overloads are often used for discrete pixel-space boundaries or lightweight visualization geometries.

### Valid Call Patterns
```scala
// Note: Example inferred from signature (not verified in test suite).
// The receiver is typically a raster metadata object, tile, or geometry.
val bounds: Envelope = rasterModel.envelope

// For AWT/LiteGeometry overloads:
val pixelBounds: java.awt.Rectangle = liteGeometry.envelope
```

### LLM Instruction Prompt
- Call `.envelope` as a parameterless method (no parentheses) on a valid spatial or raster object to get its bounding box.
- Do not confuse the Scala method `.envelope` with the Beast CSV input format string `"envelope(minX, minY, maxX, maxY)"` used in `sc.spatialFile`.
- Be aware of the return type: depending on the receiver, it may return a Beast/JTS `Envelope` (for geographic model space) or a `java.awt.Rectangle` (for pixel/image space).

### Prompt Snippet
```text
To extract the spatial boundaries of a raster model or geometry in RDPro, use the parameterless `.envelope` method. Ensure you handle the return type correctly, as it may be an `Envelope` (model space) or a `java.awt.Rectangle` (pixel space) depending on the object.
```

### Common Failure Modes
- **Parentheses Error:** Calling `.envelope()` with parentheses will cause a compilation error because it is defined as a parameterless `def`.
- **Type Mismatch:** Assuming `.envelope` always returns a JTS `Envelope`. If called on visualization or pixel-space objects (like `LiteGeometry`), it returns a `java.awt.Rectangle`.
- **Context Confusion:** Attempting to use the Scala method `.envelope` when configuring CSV readers. For CSV loading, use the string format specifier `"envelope(0,1,2,3)"` inside `BeastOptions`, not the Scala method.

### Fix Code Hint
```scala
// WRONG: Using parentheses
val bounds = rasterModel.envelope()

// RIGHT: Parameterless call
val bounds = rasterModel.envelope

// WRONG: Assuming JTS Envelope for AWT objects
val rect: Envelope = liteGeometry.envelope

// RIGHT: Matching the AWT Rectangle overload
val rect: java.awt.Rectangle = liteGeometry.envelope
```

## API Test: `eulerHistogramCount`

### Signature
```scala
def eulerHistogramCount(histogramSize: Array[Int], prefixSum: Boolean = false): AbstractHistogram
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/CGOperationsMixin.scala:98_

_Source doc:_ Computes an Euler histogram that works better for geometries with extents, i.e., envelopes, which calculates the number of records in each cell @param histogramSize the size of the histogram as the number of partitions along each dimension @param prefixSum     compute the prefix sum on the result to speed up range tests @return the created histogram

### Goal
Computes an Euler histogram over a spatial RDD to accurately count the number of records (geometries with extents, such as polygons or envelopes) in each grid cell, properly accounting for features that span multiple cells.

### Parameters
- `histogramSize` (`Array[Int]`): The dimensions of the histogram grid, specified as the number of partitions along each spatial dimension (e.g., `Array(100, 100)` for a 100x100 grid).
- `prefixSum` (`Boolean`), default `false`: If set to `true`, computes the prefix sum on the resulting histogram to accelerate subsequent range tests.

### Input
A `SpatialRDD` (e.g., `RDD[IFeature]`) containing vector geometries loaded from supported formats like Shapefile, GeoJSON, or CSV. This operation is specifically designed for geometries with spatial extents (polygons, lines, envelopes) rather than simple points.

### Output
Returns an `AbstractHistogram` representing the Euler histogram. Unlike simple uniform histograms, this structure maintains four counters per cell (corner, top edge, left edge, overlap) to accurately account for features spanning multiple grid cells without double-counting.

### Valid Call Patterns
```scala
// Compute an Euler histogram with a 100x100 grid
val eulerCountHistogram = polygons.eulerHistogramCount(Array(100, 100))

// Compute an Euler histogram with prefix sum enabled for faster range queries
val eulerCountHistogramPrefix = polygons.eulerHistogramCount(Array(100, 100), prefixSum = true)
```

### LLM Instruction Prompt
- Call `eulerHistogramCount` on a `SpatialRDD` when you need an accurate count of geometries per grid cell for approximate query processing, especially when the dataset contains polygons or envelopes that cross cell boundaries.
- Pass the grid dimensions as an `Array[Int]` matching the dimensionality of the data (typically 2D, e.g., `Array(100, 100)`).
- Be aware of the memory trade-off: Euler histograms consume 4x the memory of simple uniform histograms because they track four counters per cell. Do not use excessively large grid sizes.
- Use `prefixSum = true` if the resulting histogram will be heavily used for range tests.

### Prompt Snippet
```text
To compute an accurate spatial histogram for geometries with extents (polygons/envelopes) that span multiple cells, call `rdd.eulerHistogramCount(Array(numX, numY))`. This returns an `AbstractHistogram` using Euler rules (4 counters per cell) to avoid double-counting. Note that it uses 4x the memory of a uniform histogram.
```

### Common Failure Modes
- **Driver Memory Exhaustion:** Because Euler histograms maintain four counters per cell, providing an excessively large `histogramSize` (e.g., `Array(10000, 10000)`) can cause an `OutOfMemoryError` on the Spark driver when the histogram is collected.
- **Dimensionality Mismatch:** Passing an array with a length that does not match the spatial dimensions of the underlying geometries (e.g., passing a 3D array for 2D data).
- **Using on Point Data:** While it will not fail, using `eulerHistogramCount` on pure point datasets is inefficient. Points do not have extents that span multiple cells, so `uniformHistogramCount` should be used instead to save memory.

### Fix Code Hint
```scala
// If memory issues occur, reduce the histogram size or switch to uniformHistogramCount if the data is purely points
val eulerCountHistogram = polygons.eulerHistogramCount(Array(50, 50), prefixSum = true)
```

## API Test: `eulerHistogramSize`

### Signature
```scala
def eulerHistogramSize(histogramSize: Array[Int], prefixSum: Boolean = false, sizeFunction: IFeature => Int = _.getStorageSize): AbstractHistogram
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/CGOperationsMixin.scala:109_

_Source doc:_ Computes an Euler histogram that works better for geometries with extents, i.e., envelopes, which calculates the total size of features in each cell @param histogramSize the size of the histogram as the number of partitions along each dimension @param prefixSum     compute the prefix sum on the result to speed up range tests @return the created histogram

### Goal
Computes an Euler histogram over a spatial RDD that calculates the total storage size of features in each grid cell, accurately accounting for geometries with spatial extents (like polygons or lines) that span multiple cells.

### Parameters
- `histogramSize` (`Array[Int]`): The dimensions of the histogram grid, specified as the number of partitions/cells along each spatial dimension (e.g., `Array(100, 100)` for a 100x100 grid).
- `prefixSum` (`Boolean`), default `false`: If `true`, computes the prefix sum on the resulting histogram to speed up subsequent range tests and cumulative queries.
- `sizeFunction` (`IFeature => Int`), default `_.getStorageSize`: A function to determine the "size" or weight of each feature. By default, it uses the byte storage size of the feature.

### Input
A spatial Vector RDD (`RDD[IFeature]`) containing geometries (such as polygons, lines, or envelopes) loaded via context extensions like `sc.shapefile` or `sc.geojsonFile`. This method is specifically designed for geometries with spatial extents; while it works on points, its primary benefit is correctly handling features that cross grid cell boundaries.

### Output
Returns `AbstractHistogram` — an Euler histogram object representing the spatial distribution of the dataset's size. Unlike simple histograms, this Euler histogram maintains four counters per cell (corner, top edge, left edge, overlap) to accurately account for features spanning multiple grid cells without double-counting.

### Valid Call Patterns
```scala
val eulerSizeHistogram = polygons.eulerHistogramSize(Array(100, 100))

// With prefix sum enabled
val prefixEulerHistogram = polygons.eulerHistogramSize(Array(100, 100), prefixSum = true)
```

### LLM Instruction Prompt
- Call `eulerHistogramSize` on an `RDD[IFeature]` when you need to estimate the spatial distribution of data *size* (bytes) across a grid, especially for polygons or lines that span multiple cells.
- Pass the grid dimensions as an `Array[Int]` (e.g., `Array(100, 100)`).
- Remember that Euler histograms consume 4x the memory of uniform histograms because they track four counters per cell. Keep the `histogramSize` dimensions reasonable to avoid driver memory exhaustion.
- Do not use this on `RasterRDD`; it is strictly a Vector RDD operation.

### Prompt Snippet
```text
To compute a size-based Euler histogram on a spatial RDD `features` for a 100x100 grid:
val histogram = features.eulerHistogramSize(Array(100, 100))
```

### Common Failure Modes
- **Driver Memory Exhaustion (OOM):** Requesting an excessively large grid size (e.g., `Array(10000, 10000)`). Because Euler histograms maintain four counters per cell, they incur a 4x memory cost compared to standard histograms. The resulting `AbstractHistogram` is collected to the driver.
- **Type Mismatch:** Attempting to call this on a `RasterRDD` or a standard Spark `RDD[String]`. It must be called on an `RDD[IFeature]`.

### Fix Code Hint
```scala
// Ensure the input is a vector RDD and keep grid dimensions reasonable to avoid OOM
val features: RDD[IFeature] = sc.shapefile("polygons.zip")
val eulerSizeHistogram = features.eulerHistogramSize(Array(100, 100))
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
Splits a distributed raster dataset so that each internal tile becomes its own independent raster with distinct metadata.

### Parameters
- `inputRaster` (`RasterRDD[T]`): The tiled raster dataset to be exploded into separate rasters.

### Input
A `RasterRDD[T]` loaded from a GeoTIFF or HDF file, or generated via pixel rasterization. The type parameter `T` must exactly match the runtime pixel type of the raster (e.g., `Int`, `Float`, `Array[Int]`, `Array[Float]`).

### Output
Returns `RasterRDD[T]` representing a new raster RDD with the exact same number of tiles as the input, but where each tile is now encapsulated as an isolated raster with its own `RasterMetadata`.

### Valid Call Patterns
```scala
// Object function call (verified from test suite)
val outputRaster = RasterOperationsLocal.explode(raster)

// Implicit method call (from project context)
val outputRaster = raster.explode
```

### LLM Instruction Prompt
- Use `explode` when you need to break a large, multi-tile raster into individual rasters (e.g., to write each tile to a separate file).
- You can call it as a method on the RDD (`raster.explode`) or via the object (`RasterOperationsLocal.explode(raster)`).
- When saving the output of `explode` to disk, you MUST configure `GeoTiffWriter.WriteMode` to `"distributed"` so that each exploded raster tile is written to a separate file.

### Prompt Snippet
```text
To split a raster into individual files per tile, use `raster.explode` or `RasterOperationsLocal.explode(raster)`. Always follow `explode` with a distributed save operation by ensuring `GeoTiffWriter.WriteMode` is set to `"distributed"`.
```

### Common Failure Modes
- **Incorrect Write Mode:** Saving an exploded `RasterRDD` using the `"compatibility"` write mode. Because `explode` assigns distinct metadata to every single tile, writing in compatibility mode (which attempts to write a single file) defeats the purpose of the operation and may cause metadata conflicts. Always use `"distributed"` mode after exploding.
- **Type Mismatch:** Calling `explode` on a `RasterRDD[T]` where `T` does not match the underlying pixel type (e.g., using `Int` for a `FloatType` raster).

### Fix Code Hint
```scala
// Correct usage: explode and save as distributed files
val explodedRaster = raster.explode

// Ensure the write mode is set to distributed before saving
sparkContext.hadoopConfiguration.set("GeoTiffWriter.WriteMode", "distributed")
explodedRaster.saveAsGeoTiff("exploded_output_directory")
```

## API Test: `extents`

### Signature
```scala
def extents: Geometry
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/RasterMetadata.scala:181  (+1 more definition site/overload)_

_Source doc:_ Returns a polygon that represents the boundaries of this tile in the model space. @return a polygon (rectangle) that represents the boundaries of this tile

### Goal
Returns a rectangular polygon that represents the exact spatial boundaries (footprint) of a raster tile or dataset in the model space (Coordinate Reference System).

### Parameters
_None._

### Input
A valid `RasterMetadata` instance (typically accessed via a `GeoTiffReader`'s `.metadata` property or an `ITile`'s metadata) that contains the raster's grid dimensions, resolution, and affine transformation.

### Output
Returns `Geometry` — A JTS `Geometry` object (specifically a rectangular polygon) representing the spatial extent of the raster tile in model coordinates.

### Valid Call Patterns
```scala
// Inferred from signature and sibling RasterMetadata tests (not verified)
val rasterPath = new Path("/rasters/FRClouds.tif")
val fileSystem = rasterPath.getFileSystem(new Configuration())
val reader = new GeoTiffReader[Array[Int]]
reader.initialize(fileSystem, rasterPath.toString, "0", new BeastOptions())

// Retrieve the spatial boundary of the raster in model space
val boundary: Geometry = reader.metadata.extents
```

### LLM Instruction Prompt
- Call `extents` as a parameterless method (without parentheses) on a `RasterMetadata` instance.
- Expect a JTS `Geometry` (a polygon) as the return type, not a simple bounding box array or `Envelope`.
- Use this method when you need to extract the spatial footprint of a raster tile to perform geometric operations, such as checking intersections with vector polygons during Raptor joins or spatial filtering.

### Prompt Snippet
```text
To get the spatial bounding box of a raster tile in model space, call `metadata.extents` on its `RasterMetadata` to receive a JTS `Geometry` polygon.
```

### Common Failure Modes
- **Type Mismatch:** Attempting to assign the result to an `Envelope`, `BoundingBox`, or `Array[Double]` instead of a JTS `Geometry`.
- **Syntax Error:** Calling the method with parentheses `extents()`, which may cause compilation errors in strict Scala environments since it is defined without them.

### Fix Code Hint
```scala
// WRONG: Assigning to Envelope and using parentheses
// val bbox: Envelope = reader.metadata.extents()

// CORRECT: Assigning to Geometry without parentheses
val bbox: Geometry = reader.metadata.extents
```

## API Test: `extractTables`

### Signature
```scala
def extractTables(sql: String): Set[String]
```
_Source: beast/dataExplorer/src/main/scala/edu/ucr/cs/bdlab/beast/dataExplorer/SQLQueryHelper.scala:22_

_Source doc:_ Checks if an SQL query is syntactically correct and extracts table names from it. @param sql The SQL query string to be analyzed. @return Either an error message as a string if the query is incorrect, or a set of table names if the query is correct.

### Goal
Parses a given SQL query string to verify its syntax and extracts the set of referenced table names, typically used in data exploration to determine which datasets need to be loaded.

### Parameters
- `sql` (`String`): The SQL query string to be analyzed for syntax correctness and table references.

### Input
A standard SQL query string. No specific Spark RDDs or file formats are required as inputs, as this is a purely string-based parsing utility.

### Output
Returns `Set[String]` — A collection of unique table names extracted from the `FROM` and `JOIN` clauses of the provided SQL query.

### Valid Call Patterns
```scala
// Extracting tables from a valid SQL query
val validSQL = "SELECT * FROM users"
val tables: Set[String] = SQLQueryHelper.extractTables(validSQL)
```

### LLM Instruction Prompt
- Always call this method using the `SQLQueryHelper` object qualifier: `SQLQueryHelper.extractTables(sql)`.
- Do not attempt to pass Spark contexts or RDDs to this function; it strictly takes a single `String`.
- Be aware that if the SQL string is syntactically invalid, the function will throw a `SqlParseException` rather than returning an error string (despite the source doc's phrasing, the signature strictly returns `Set[String]`).

### Prompt Snippet
```text
Use `SQLQueryHelper.extractTables(sqlString)` to parse an SQL query and retrieve a `Set[String]` of referenced table names. Wrap the call in a try-catch block for `SqlParseException` if the SQL input is untrusted or potentially malformed.
```

### Common Failure Modes
- **Invalid SQL Syntax:** Passing a malformed SQL string (e.g., misspelled keywords like `"SELEC * FROM users"`) will cause the parser to fail and throw a `SqlParseException`.

### Fix Code Hint
```scala
import edu.ucr.cs.bdlab.beast.dataExplorer.SQLQueryHelper

val query = "SELEC * FROM users" // Malformed SQL

try {
  val tables = SQLQueryHelper.extractTables(query)
  println(s"Tables found: $tables")
} catch {
  case e: Exception => // Catches SqlParseException
    println(s"Failed to parse SQL query: ${e.getMessage}")
}
```

## API Test: `filterPixels`
_Grounding: doc-repaired from source (docfix)._

### Goal
Retains only the pixels in a distributed raster dataset (`RasterRDD[T]`) that satisfy a user-defined boolean condition, setting all other pixels to empty (NoData). This is a user-facing API. The output is a standard `RasterRDD[T]` which can be evaluated by calling `.count()`.

### Valid Call Patterns
```scala
import edu.ucr.cs.bdlab.raptor.RasterOperationsLocal

// Assumes rasterRDD: RasterRDD[Float] is provided by the execution harness
val filtered = RasterOperationsLocal.filterPixels(rasterRDD, (x: Float) => x > 10.0f)

// Trigger execution to verify the API; no need to manually inspect ITile pixels
val tileCount = filtered.count()
println(s"__CHECK__ filterPixels $tileCount")
```

### LLM Instruction Prompt
- Use `RasterOperationsLocal.filterPixels(rasterRDD, condition)` to mask pixels based on their values.
- Ensure the lambda function's input type strictly matches the `RasterRDD[T]` type parameter (e.g., use `Float` literals like `10.0f` if `T` is `Float`).
- Do not artificially fail the test if `ITile` verification methods (like `isEmpty`) are not documented; simply executing a Spark action like `.count()` on the resulting `RasterRDD` is sufficient to test the API.
- The output is a standard `RasterRDD[T]` which can be evaluated by calling `.count()`.

### Prompt Snippet
```text
RDPro `RasterOperationsLocal.filterPixels(raster, f: T => Boolean)` masks a RasterRDD by keeping only pixels where `f` returns true, setting the rest to empty. Output is a standard `RasterRDD[T]`. Trigger execution with `.count()` to test; do not artificially fail tests looking for ITile verification methods.
```

### Common Failure Modes
- **Artificially aborting tests:** Failing the test with `assert(false)` because `ITile` verification methods (like `isEmpty(x, y)`) are not documented. Executing a Spark action like `.count()` on the resulting `RasterRDD` is sufficient.
- **Type Mismatch:** Providing a filter function that expects a `Double` or `Int` when the `RasterRDD` is typed as `Float`. The compiler will fail to type-check the closure.
- **Serialization Errors (Task not serializable):** Referencing non-serializable objects (like an active SparkContext) inside the `filter` closure.

### Fix Code Hint
```scala
// BAD: Artificially failing because ITile verification is unknown
val filtered = RasterOperationsLocal.filterPixels(rasterRDD, (x: Float) => x > 10.0f)
assert(false, "No documented methods on ITile to verify pixels were cleared")

// GOOD: Executing a Spark action to verify the transformation succeeds
import edu.ucr.cs.bdlab.raptor.RasterOperationsLocal

val filtered = RasterOperationsLocal.filterPixels(rasterRDD, (x: Float) => x > 10.0f)
val tileCount = filtered.count()
println(s"__CHECK__ filterPixels $tileCount")
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
Creates or retrieves a cached mathematical transformation to convert coordinates, geometries, or raster metadata between a source and target Coordinate Reference System (CRS).

### Parameters
- `sourceCRS` (`CoordinateReferenceSystem`): The source coordinate reference system. Can also be provided as an integer SRID/EPSG code (e.g., `4326`) via overloads.
- `targetCRS` (`CoordinateReferenceSystem`): The target coordinate reference system. Can also be provided as an integer SRID/EPSG code via overloads.

### Input
- Requires valid source and target CRSs, provided either as instantiated `CoordinateReferenceSystem` objects (e.g., from GeoTools) or standard integer SRIDs (e.g., `4326` for WGS84, `26911` for NAD83 / UTM zone 11N).
- **Precondition:** The underlying referencing engine must be able to find a valid mathematical transformation path between the two systems. 

### Output
Returns `TransformationInfo` — An object containing the cached math transformation required to reproject geometries or raster metadata from the source CRS to the destination CRS.

### Valid Call Patterns
```scala
// Using integer SRIDs (EPSG codes)
val transformInfo = Reprojector.findTransformationInfo(26911, 4326)

// Using a mix of SRID and a custom CoordinateReferenceSystem object
val targetCRS: CoordinateReferenceSystem = new DefaultProjectedCRS("Sinusoidal", ...)
val transform = Reprojector.findTransformationInfo(4326, targetCRS)
```

### LLM Instruction Prompt
- ALWAYS call this method on the `Reprojector` object (i.e., `Reprojector.findTransformationInfo(...)`). It is not a standalone function or an RDD method.
- Prefer the `(Int, Int)` overload when dealing with standard EPSG codes (like `4326`) for simplicity and readability.
- Do not invent custom `CoordinateReferenceSystem` objects unless explicitly required by the prompt; use standard integer SRIDs where possible.
- Use the returned `TransformationInfo` with `Reprojector.reprojectGeometry` to actually perform the coordinate conversion.

### Prompt Snippet
```text
To get a transformation between two CRSs, use `Reprojector.findTransformationInfo(sourceSRID, targetSRID)`. It returns a `TransformationInfo` object. You can pass integer EPSG codes (like 4326) or GeoTools `CoordinateReferenceSystem` objects. Always call it on the `Reprojector` object.
```

### Common Failure Modes
- **Calling without the Object Qualifier:** Attempting to call `findTransformationInfo` as a bare function or on an RDD instead of the `Reprojector` object will cause a compilation error.
- **Invalid/Unknown SRID:** Passing an integer SRID that does not exist in the EPSG registry will cause a runtime failure when the referencing engine attempts to look it up.
- **No Transform Path:** Attempting to transform between two highly incompatible or custom CRSs where no mathematical transform can be derived by the referencing factory.

### Fix Code Hint
```scala
// BAD: Calling without the Reprojector object qualifier
val t = findTransformationInfo(26911, 4326)

// GOOD: Call on the Reprojector object
val t = Reprojector.findTransformationInfo(26911, 4326)

// GOOD: Using the result to reproject a geometry
val convertedPoint = Reprojector.reprojectGeometry(point, t)
```

## API Test: `flatten`
_Grounding: doc-repaired from source (docfix)._

### Goal
Extract all individual pixel values and their spatial grid coordinates from a distributed `RasterRDD` into a flat Spark `RDD` of tuples. The returned `RasterMetadata` describes the *entire raster layer*, not individual tiles.

### Valid Call Patterns
```scala
import edu.ucr.cs.bdlab.beast.cg.SpatialDataTypes.RasterRDD
import edu.ucr.cs.bdlab.beast.geolite.RasterMetadata
import org.apache.spark.rdd.RDD

// Assuming `sc` (SparkContext) and a loaded rasterRDD are provided:
// val rasterRDD: RasterRDD[Int] = sc.geoTiff[Int]("input.tif")

val flatPixels: RDD[(Int, Int, RasterMetadata, Int)] = rasterRDD.flatten

// Force materialization and compute witnesses
val totalPixels = flatPixels.count()
val numTiles = rasterRDD.count()

// Falsifiable condition: the number of distinct metadata objects in the flattened pixels 
// should be exactly 1, because RasterMetadata describes the entire layer, not individual tiles.
val distinctMetadataCount = flatPixels.map(_._3).distinct().count()

assert(
  distinctMetadataCount == 1, 
  s"Expected exactly 1 distinct metadata object for the layer, got $distinctMetadataCount"
)
assert(
  totalPixels >= numTiles, 
  s"Expected at least $numTiles pixels (one per tile), got $totalPixels"
)

println(s"__CHECK__ flatten $totalPixels pixels from $numTiles tiles")
```

### LLM Instruction Prompt
- Use `flatten` to break a tiled `RasterRDD` into individual pixel records `(x, y, metadata, value)`.
- The `RasterMetadata` returned in the tuple describes the *entire raster layer* (including total width, height, and number of tiles), not the specific individual tile.
- Because it describes the global layer, all pixels across all tiles in the flattened RDD will share the exact same `RasterMetadata` instance (or identical copies).
- **Warning:** Flattening a large satellite image creates a massive RDD (one row per pixel). Never call `.collect()` directly on the flattened RDD without aggressive filtering or aggregation first.

### Prompt Snippet
RDPro `flatten` extracts all pixels from a RasterRDD[T] into an RDD[(Int, Int, RasterMetadata, T)] containing (x, y, layer_metadata, value). Call via `raster.flatten`. The `RasterMetadata` describes the entire global layer, meaning all pixels across all tiles share the exact same metadata instance (distinct count = 1). Avoid collecting the raw output on large rasters to prevent driver OOM.

### Common Failure Modes
- **Incorrect Metadata Cardinality Assumption:** `java.lang.AssertionError: assertion failed: Expected 9 distinct metadata in flattened pixels, got 1`. This happens if you assume `RasterMetadata` is unique per tile. It is not; it describes the entire raster layer, so all pixels across all tiles share exactly 1 distinct metadata instance.
- **Driver OutOfMemoryError (OOM):** Calling `.collect()` immediately after `flatten` on a full-scale GeoTIFF. A standard 10,000 x 10,000 satellite tile contains 100 million pixels; collecting this to the Spark driver will crash it. Always filter or aggregate first.

### Fix Code Hint
```scala
// BAD: Assuming metadata is unique per tile (causes AssertionError: Expected 9 distinct metadata..., got 1)
val distinctMetaCount = flatPixels.map(_._3).distinct().count()
assert(distinctMetaCount == rasterRDD.count()) 

// GOOD: Metadata describes the entire layer, so there is exactly 1 distinct instance across all pixels
val distinctMetaCount = flatPixels.map(_._3).distinct().count()
assert(distinctMetaCount == 1)
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
Generate a distributed spatial dataset containing geometries distributed according to a Gaussian (normal) distribution, typically used for benchmarking spatial algorithms and systems (part of the Spider Spatial Data Generator).

### Parameters
- `cardinality` (`Long`): The total number of spatial records (geometries) to generate across the Spark cluster.

### Input
Requires an initialized SparkContext (`sc`) and a spatial generator builder instance (obtained via the context extension `sc.generateSpatialData` or by instantiating `new SpatialGeneratorBuilder(sc)`). Any desired configurations—such as the Minimum Bounding Rectangle (MBR), geometry type, or random seed—must be chained *before* calling `gaussian`.

### Output
Returns `SpatialRDD` (or `JavaSpatialRDD` in the Java API) — A distributed collection of generated spatial features (`IFeature`) whose spatial locations follow a Gaussian distribution.

### Valid Call Patterns
```scala
// Pattern 1: Using the SparkContext extension (from README)
val gaussianData: SpatialRDD = sc.generateSpatialData
  .gaussian(1000)

// Pattern 2: Using SpatialGeneratorBuilder with explicit configurations (adapted from test suite)
val desiredMBR = new EnvelopeNDLite(2, 2, 3, 9, 8)
val randomPoints: SpatialRDD = new SpatialGeneratorBuilder(sc)
  .mbr(desiredMBR)
  .config(SpatialGenerator.Seed, 1794)
  .gaussian(10000L)
```

### LLM Instruction Prompt
- When generating synthetic spatial data for benchmarking, use `sc.generateSpatialData.gaussian(cardinality)` or `new SpatialGeneratorBuilder(sc).gaussian(cardinality)`. Always chain configuration methods (like `.mbr()` or `.config()`) *before* calling `.gaussian()`, because `gaussian` executes the generation and returns the `SpatialRDD`, terminating the builder chain.

### Prompt Snippet
```text
To generate Gaussian-distributed spatial data, use `sc.generateSpatialData.gaussian(cardinality)`. Chain configurations like `.mbr(envelope)` or `.config(key, value)` before calling `gaussian()`.
```

### Common Failure Modes
- **Chaining order errors:** Attempting to call builder configuration methods (like `.mbr()` or `.config()`) *after* calling `.gaussian()`. The `gaussian` method returns a `SpatialRDD`, which does not possess the builder methods, resulting in a compilation error.
- **Missing SparkContext:** Attempting to call `gaussian` without an active, initialized SparkContext (`sc`).

### Fix Code Hint
```scala
// WRONG: Calling builder methods after generation
// val badData = sc.generateSpatialData.gaussian(1000).mbr(new EnvelopeNDLite(0, 0, 10, 10))

// RIGHT: Configure the builder first, then generate
val goodData = sc.generateSpatialData
  .mbr(new EnvelopeNDLite(0, 0, 10, 10))
  .config(SpatialGenerator.Seed, 42)
  .gaussian(1000)
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
Generate a distributed spatial dataset (SpatialRDD) of a specified size for benchmarking or testing, using previously configured statistical distributions and geometry types.

### Parameters
- `cardinality` (`Long`): The total number of spatial records (features) to generate across the Spark cluster.

### Input
Requires an initialized `SparkContext` (or `JavaSpatialSparkContext`) and a configured spatial generator builder. The builder is typically accessed via the context extension `sc.generateSpatialData` or instantiated directly via `new SpatialGeneratorBuilder(sc)`. Before calling `generate`, the builder should be configured with a spatial distribution (e.g., `GaussianDistribution`, `BitDistribution`) and geometry properties (e.g., `UniformDistribution.GeometryType`, `UniformDistribution.MaxSize`, `UniformDistribution.NumSegments`) using chained `.config(...)` and `.distribution(...)` calls.

### Output
Returns `SpatialRDD` (Scala) or `JavaSpatialRDD` (Java) — an RDD of `IFeature` objects representing the randomly generated spatial geometries (points, boxes, or polygons) distributed across the cluster partitions.

### Valid Call Patterns
```scala
import edu.ucr.cs.bdlab.beast._
import edu.ucr.cs.bdlab.beast.generator._

// Generate 10 million random boxes using a Gaussian distribution
val randomBoxes: SpatialRDD = sc.generateSpatialData
  .distribution(GaussianDistribution)
  .config(UniformDistribution.GeometryType, "box")
  .config(UniformDistribution.MaxSize, "0.01,0.01")
  .generate(cardinality=10000000L)

// Generate 10 million random polygons using a Bit distribution
val randomPolygons: SpatialRDD = sc.generateSpatialData
  .distribution(BitDistribution)
  .config(UniformDistribution.GeometryType, "polygons")
  .config(UniformDistribution.NumSegments, "20")
  .generate(cardinality=10000000L)
```

### LLM Instruction Prompt
- When generating synthetic spatial data for benchmarking in Beast, use `sc.generateSpatialData` to access the builder.
- Chain `.distribution(...)` and `.config(...)` to define the geometry type ("box", "polygons") and distribution parameters before calling `.generate(cardinality)`.
- Ensure the `cardinality` parameter is a `Long`.
- The output is a `SpatialRDD` (which is an alias for `RDD[IFeature]`).

### Prompt Snippet
```text
To generate synthetic spatial data in Beast, use `sc.generateSpatialData.config(...).generate(cardinality)`. Configure the geometry type (e.g., "box", "polygons") and distribution before calling `generate`. The `cardinality` must be a Long. Returns a SpatialRDD.
```

### Common Failure Modes
- **Missing Configuration:** Calling `generate` without first configuring the `GeometryType` or `NumSegments` will result in default geometries (typically points) being generated instead of the desired complex shapes.
- **Type Mismatch on Cardinality:** Passing an `Int` that exceeds the maximum integer value instead of a `Long` literal (e.g., `10000000000` instead of `10000000000L`), causing compilation errors.
- **Unbounded Generation:** Generating an excessively large cardinality without sufficient cluster memory or partitions, leading to OutOfMemory errors during subsequent actions.

### Fix Code Hint
```scala
// BAD: Calling generate without configuration or with an overflowing Int
val badData = sc.generateSpatialData.generate(3000000000)

// GOOD: Configuring the builder first and using a Long literal
val goodData = sc.generateSpatialData
  .config(UniformDistribution.GeometryType, "box")
  .config(UniformDistribution.MaxSize, "0.1,0.1")
  .generate(3000000000L)
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
Generate a `SpatialRDD` of synthetic, randomly distributed geometries (points, boxes, etc.) across a Spark cluster, primarily used for benchmarking, stress-testing spatial joins, and evaluating partitioning algorithms.

### Parameters
- `distribution` (`DistributionType`): The statistical spatial distribution to use for generating geometries. Supported values include `UniformDistribution`, `DiagonalDistribution`, `GaussianDistribution`, `SierpinskiDistribution`, `BitDistribution`, and `ParcelDistribution`.
- `cardinality` (`Long`): The total number of geometries to generate across the entire dataset.
- `numPartitions` (`Int`), default `0`: The number of Spark partitions to divide the generated data into. If `0`, it typically falls back to Spark's default parallelism.
- `opts` (`BeastOptions`), default `new BeastOptions`: Additional configuration options for the generator (e.g., random seed, maximum geometry size, or geometry type). Can often be passed as a `Seq` of key-value pairs due to implicit conversions in Beast.

### Input
Requires an initialized `SparkContext` (`sc`) with Beast context extensions loaded (e.g., `import edu.ucr.cs.bdlab.beast._`). No external files or datasets are required, as the data is generated entirely in-memory by the Spider Spatial Data Generator (SDG) component.

### Output
Returns `SpatialRDD` — A distributed Spark RDD containing the generated spatial features (`IFeature`), which can then be used in downstream operations like `spatialPartition`, `spatialJoin`, or saved to disk.

### Valid Call Patterns
```scala
import edu.ucr.cs.bdlab.beast._
import edu.ucr.cs.bdlab.beast.generator.UniformDistribution

// Generate 100 uniformly distributed box geometries
val syntheticData: SpatialRDD = sc.generateSpatialData(
  UniformDistribution, 
  100, 
  opts = Seq(
    "seed" -> 42, 
    UniformDistribution.MaxSize -> "0.1,0.1", 
    "geometry" -> "box"
  )
)
```

### LLM Instruction Prompt
- Use `sc.generateSpatialData` when the user needs to create synthetic spatial datasets for benchmarking or testing distributed algorithms.
- Always provide a valid `DistributionType` (e.g., `UniformDistribution`) and the total `cardinality`.
- Pass generator-specific configurations (like `"geometry" -> "box"`, `"seed"`, or `MaxSize`) via the `opts` parameter. Note that Beast supports passing a `Seq[(String, Any)]` for `opts` in Scala.
- Ensure Beast implicits are in scope so the `SparkContext` has the `generateSpatialData` extension method.

### Prompt Snippet
```text
Generate a synthetic dataset of 1,000,000 uniformly distributed spatial boxes to stress-test the PBSM spatial join algorithm. Use a random seed of 1.
```

### Common Failure Modes
- **Missing Context Extensions:** Calling `sc.generateSpatialData` without importing `edu.ucr.cs.bdlab.beast._` will result in a compilation error (`value generateSpatialData is not a member of org.apache.spark.SparkContext`).
- **Out of Memory (OOM):** Generating a massive `cardinality` with `numPartitions` set to a very low number (or default 0 on a local master) can cause individual Spark tasks to run out of memory.
- **Invalid Options:** Providing unrecognized geometry types or malformed `MaxSize` strings in the `opts` parameter may cause runtime parsing exceptions in the generator.

### Fix Code Hint
```scala
// ERROR: value generateSpatialData is not a member of org.apache.spark.SparkContext
// FIX: Ensure Beast implicits are imported
import edu.ucr.cs.bdlab.beast._
import edu.ucr.cs.bdlab.beast.generator.UniformDistribution

val data = sc.generateSpatialData(UniformDistribution, 1000000L, numPartitions = 100)
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
Loads a GeoTIFF file into a distributed Spark RDD of raster tiles for scalable pixel-level math, reshaping, or raster-vector joins.

### Parameters
- `path` (`String`): The file path or directory containing the GeoTIFF file(s) to load.
- `iLayer` (`Int`), default `0`: The 0-based index of the raster band/layer to load.
- `opts` (`BeastOptions`), default `new BeastOptions`: Additional configuration options for loading the file.

### Input
A valid GeoTIFF file accessible to the Spark cluster. The caller must know the runtime pixel type of the GeoTIFF to provide the correct type parameter `[T]`. The operation requires an initialized `SparkContext` (or `JavaSpatialSparkContext`) with Beast context extensions loaded.

### Output
Returns `RDD[ITile[T]]` — a distributed collection of raster tiles representing the loaded band of the GeoTIFF file, where `T` is the underlying pixel data type (e.g., `Int`, `Float`).

### Valid Call Patterns
```scala
// Explicitly typed method call (recommended)
val raster: RasterRDD[Int] = sc.geoTiff[Int]("glc2000_v1_1.tif")

// Type inferred from the variable declaration
val treecover: RDD[ITile[Float]] = sc.geoTiff("treecover")
```

### LLM Instruction Prompt
- Always call `geoTiff` as an extension method on the SparkContext (`sc.geoTiff[T](...)`).
- You MUST specify the type parameter `[T]` to exactly match the file's runtime pixel type. Selection rules: `IntegerType` $\rightarrow$ `[Int]`, `FloatType` $\rightarrow$ `[Float]`, `ArrayType(IntegerType,true)` $\rightarrow$ `[Array[Int]]`, `ArrayType(FloatType, true)` $\rightarrow$ `[Array[Float]]`.
- Never invent file paths; use only the provided input variables.

### Prompt Snippet
```text
Load GeoTIFFs using the SparkContext extension `sc.geoTiff[T](path)`. You MUST match the type parameter `[T]` to the runtime pixel type (e.g., `[Int]` for IntegerType, `[Float]` for FloatType). Do not invent file paths.
```

### Common Failure Modes
- **Type Parameter Mismatch:** Failing to match the type parameter `[T]` to the actual runtime pixel type of the GeoTIFF (e.g., using `sc.geoTiff[Int]` for a `FloatType` raster) will cause runtime casting errors or data corruption.
- **Missing Context Extension:** Attempting to call `geoTiff` as a standalone function or on an object other than an initialized `SparkContext` (`sc`).
- **Overlaying Unaligned Rasters:** Loading multiple GeoTIFFs with `sc.geoTiff` and immediately attempting to `overlay` them without ensuring they have identical metadata (resolution, CRS, tile size). Unaligned rasters must be aligned using `reshape` first.

### Fix Code Hint
```scala
// BAD: Type parameter missing or mismatched, or called incorrectly
val raster = geoTiff("data.tif")
val floatRaster = sc.geoTiff[Int]("float_data.tif")

// GOOD: Called on SparkContext with the exact matching pixel type
val raster: RasterRDD[Int] = sc.geoTiff[Int]("data.tif")
val floatRaster: RasterRDD[Float] = sc.geoTiff[Float]("float_data.tif")
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
Loads vector geometries and their associated properties from a GeoJSON file or directory into a distributed `SpatialRDD` for spatial processing.

### Parameters
- `filename` (`String`): The path to the GeoJSON file or a directory containing GeoJSON files to be loaded.

### Input
A valid GeoJSON file or a directory of GeoJSON files accessible to the Spark cluster (e.g., local file system, HDFS, or S3). This is a vector input format; it is not used for raster data (GeoTIFF/HDF).

### Output
Returns `SpatialRDD` — a distributed Spark RDD of `IFeature` objects representing the parsed GeoJSON geometries (points, lines, polygons) and their attributes. In Java, it returns a `JavaSpatialRDD` (equivalent to `JavaRDD<IFeature>`).

### Valid Call Patterns
```scala
// Scala
val records: SpatialRDD = sparkContext.geojsonFile("input.json")

// Java
JavaRDD<IFeature> records = spatialSparkContext.geojsonFile("input.json");
```

### LLM Instruction Prompt
- When loading GeoJSON vector data in Beast, use the `geojsonFile(path)` extension method directly on the initialized `SparkContext` (or `JavaSpatialSparkContext`). Do not call this on an RDD or a companion object. The returned `SpatialRDD` can then be spatially partitioned, used in vector spatial joins, or used as the vector input for a `raptorJoin` against a raster.

### Prompt Snippet
```text
To load GeoJSON vector data in Beast, use `sparkContext.geojsonFile("path/to/data.json")`. This returns a `SpatialRDD` (an `RDD[IFeature]`). Note that this is a SparkContext extension method. For other vector formats, use `sc.shapefile` or `sc.readCSVPoint`.
```

### Common Failure Modes
- **Incorrect Receiver:** Attempting to call `geojsonFile` on an RDD, a DataFrame, or a generic object instead of the `SparkContext`. It is a context extension.
- **Format Mismatch:** Passing a compressed Esri Shapefile (`.zip`) or a CSV file to this method. Beast has specific loaders for those (`sc.shapefile` and `sc.readCSVPoint`).
- **Missing Spatial Partitioning for Joins:** If the loaded GeoJSON is immediately used in a Distributed Join (`DJ`), it will fail or perform poorly unless it is first spatially partitioned (e.g., `records.spatialPartition(classOf[RSGrovePartitioner])`).

### Fix Code Hint
```scala
// ❌ BAD: Calling geojsonFile on an RDD or using it for a Shapefile
val data = myRdd.geojsonFile("polygons.zip")

// ✅ GOOD: Calling geojsonFile on the SparkContext for a .json file
val data: SpatialRDD = sparkContext.geojsonFile("polygons.json")

// ✅ GOOD: Spatially partitioning the loaded GeoJSON before a distributed join
val partitionedData = data.spatialPartition(classOf[RSGrovePartitioner])
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
Determines the most inclusive geometry type present within a spatial partition or geometric summary.

### Parameters
_None._

### Input
A spatial partition or geometric summary object containing vector features (e.g., loaded from Shapefiles, GeoJSON, or CSV). 

### Output
Returns `GeometryType` (with overloads returning Spark SQL `DataType` or `String`) — representing the hierarchical bounding geometry type of the partition's contents. It resolves mixed types to their most inclusive parent (e.g., Points + MultiPoints = MultiPoint; mixed incompatible types = GeometryCollection).

### Valid Call Patterns
```scala
// Note: Call pattern inferred from the signature and sibling methods (e.g., `numFeatures`) on SpatialPartition/Summary.
val summary = GeometricSummary.run(opts, Array(inputfile.getPath), null, sparkContext).asInstanceOf[Summary]

// Parameterless call to get the inclusive geometry type
val geomType = summary.geometryType
```

### LLM Instruction Prompt
- Call `geometryType` as a parameterless method (no parentheses).
- Do not assume the returned type guarantees a strictly homogeneous partition unless it returns `Point`, `LineString`, or `Polygon` (and even then, it may contain empty geometries).
- If the partition contains mixed, incompatible geometries (e.g., Points and Polygons), expect `GeometryCollection` as the return value.
- Use the appropriate overload implicitly based on the expected type (`GeometryType`, `DataType`, or `String`).

### Prompt Snippet
```text
// Determine the most inclusive geometry type of the partition/summary
val partitionGeomType = summary.geometryType
if (partitionGeomType.toString == "GeometryCollection") {
  println("Partition contains mixed geometry types.")
}
```

### Common Failure Modes
- **Adding parentheses:** Calling `summary.geometryType()` will cause a compilation error because it is defined as a parameterless `def`.
- **Assuming strict homogeneity:** Failing to handle `GeometryCollection` when processing datasets that contain mixed geometry types (e.g., a GeoJSON with both Polygons and Points).
- **Misinterpreting Multi-types:** Assuming `MultiPolygon` means *only* MultiPolygons are present; it actually means the partition contains at least one MultiPolygon and zero or more Polygons or empty geometries.

### Fix Code Hint
```scala
// WRONG: Using parentheses
val t = partition.geometryType()

// RIGHT: Parameterless call
val t = partition.geometryType
```

## API Test: `getAttributeName`
_Grounding: doc-repaired from source (docfix)._

### Goal
Retrieves the schema column name of a non-spatial attribute at a specific 0-based index from a geospatial feature. Included in the main user-facing denominator.

### Valid Call Patterns
```scala
import edu.ucr.cs.bdlab.beast.geolite.IFeature

// Standard context established.
val data = sparkContext.readWKTFile(inputPath.getPath, "Geometry", '\t', true)
val feature: IFeature = data.first()

// Final transformation: use length to check bounds, geometry is included in length.
val hasAttributes = feature.length > 1
val firstAttrName = if (hasAttributes) feature.getAttributeName(0) else null

val outOfBoundsName = try {
  feature.getAttributeName(-1)
} catch {
  case _: Exception => null
}

if (hasAttributes && firstAttrName != null) {
  assert(firstAttrName == feature.getAttributeName(0), "getAttributeName must be deterministic")
}

println(s"__CHECK__ getAttributeName ${if (firstAttrName != null) firstAttrName else "null"}")
```

### LLM Instruction Prompt
- Initial logic and parameters are validated.
- Do not invent methods like `getNumAttributes` to check bounds on an `IFeature`.
- To determine how many fields exist, use the `length` property on `IFeature`, which returns the total number of fields including the geometry column.
- Because the geometry column is included in `length`, the number of non-spatial attributes is `feature.length - 1`. Valid indices for `getAttributeName(i)` are `0` to `feature.length - 2`.

### Prompt Snippet
To retrieve a non-spatial attribute name, use `feature.getAttributeName(i)`. Do not use `getNumAttributes`. Use `feature.length` (total fields including geometry). Valid indices for `getAttributeName` are `0` to `feature.length - 2`.

### Common Failure Modes
- **Hallucinating Bounds Check:** Attempting to call a non-existent `getNumAttributes` method on `IFeature` before calling `getAttributeName`. The correct property is `length`.
- **Index Out of Bounds:** Failing to account for the geometry column offset. `getAttributeName(i)` accesses schema index `i + 1`.

### Fix Code Hint
```scala
// BAD: Hallucinating getNumAttributes
val numAttrs = feature.getNumAttributes
val name = if (numAttrs > 0) feature.getAttributeName(0) else null

// GOOD: Using length property (total fields including geometry)
val hasAttributes = feature.length > 1
val name = if (hasAttributes) feature.getAttributeName(0) else null
```

## API Test: `getBoolean`

### Signature
```scala
def getBoolean(key: String, defaultValue: Boolean): Boolean
```
_Source: beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/common/BeastOptions.scala:133_

_Source doc:_ Get value as boolean @param key @param defaultValue @return

### Goal
Retrieves a boolean configuration value for a given key from the parsed Beast options, returning a specified default if the key is absent.

### Parameters
- `key` (`String`): The string identifier for the configuration option (e.g., `"my-flag"`). This should be the base name of the parameter, omitting any command-line prefixes like `-` or `-no-`.
- `defaultValue` (`Boolean`): The fallback boolean value to return if the specified `key` is not found in the configuration options.

### Input
A `BeastOptions` instance (typically accessed via `parsed.options` after calling `OperationHelper.parseCommandLineArguments`) containing parsed command-line flags or job configuration settings. 

### Output
Returns `Boolean` — the boolean state of the requested configuration key (e.g., `true` if `-key` was passed, `false` if `-no-key` was passed), or the `defaultValue` if the key was not provided.

### Valid Call Patterns
```scala
// Assuming `parsed` is the result of OperationHelper.parseCommandLineArguments
// Example 1: Using named arguments for clarity
val isEnabled = parsed.options.getBoolean("option2", defaultValue = false)

// Example 2: Using positional arguments
val isDisabled = parsed.options.getBoolean("option3", true)

// Example 3: Keys can contain dashes in the middle
val hasDashedOption = parsed.options.getBoolean("option-4", false)
```

### LLM Instruction Prompt
- When extracting boolean flags from Beast configuration options, always use `options.getBoolean(key, defaultValue)`. 
- Do not include command-line prefixes (`-` or `-no-`) in the `key` string. Beast's CLI parser automatically maps flags like `-my-flag` to `true` and `-no-my-flag` to `false` under the base key `"my-flag"`.

### Prompt Snippet
```text
To read boolean configuration flags safely in Beast, use `options.getBoolean("flag-name", defaultValue)`. Ensure the key string omits CLI prefixes like `-` or `-no-`.
```

### Common Failure Modes
- **Including CLI prefixes in the key:** Querying for `"-my-flag"` or `"-no-my-flag"` instead of the base key `"my-flag"`. The parser strips these prefixes, so the prefixed key will not be found, causing the method to silently return the `defaultValue`.
- **Type mismatch assumptions:** Assuming a flag provided as a string like `"true"` or `"1"` via array syntax (e.g., `option[1]:true`) requires `getString` and manual parsing; `getBoolean` handles standard boolean representations natively.

### Fix Code Hint
```scala
// ❌ BAD: Including the CLI dash or negation prefix in the key
val flag = parsed.options.getBoolean("-no-cache", true)

// ✅ GOOD: Use the base key name; Beast handles the `-no-` logic internally
val flag = parsed.options.getBoolean("cache", true)
```

## API Test: `getFeatureReaderClass`

### Signature
```scala
def getFeatureReaderClass(path: String, opts: BeastOptions): Class[_ <: FeatureReader]
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/SpatialFileRDD.scala:398_

_Source doc:_ The class of the feature reader to use with this RDD. All partitions use the same feature reader.

### Goal
Resolves the specific `FeatureReader` implementation class required to parse a spatial dataset across all Spark partitions based on the file path and configuration options.

### Parameters
- `path` (`String`): The URI or local file path to the input spatial dataset (e.g., a GeoJSON, Shapefile, or CSV file).
- `opts` (`BeastOptions`): Configuration options that can provide explicit format hints (e.g., specifying the input format) to help resolve the correct reader.

### Input
A valid file path string pointing to a supported vector format (such as CSV, Esri Shapefile, GeoJSON, JSON+WKT, or GPX) and a `BeastOptions` object containing any necessary parsing configurations or format overrides.

### Output
Returns `Class[_ <: FeatureReader]` — the Java `Class` object representing the specific reader implementation that Beast will instantiate to extract features from the dataset's partitions.

### Valid Call Patterns
```scala
// Resolving the reader class for manual partition reading
val inputFile = makeFileCopy("/allfeatures.geojson")
val opts: BeastOptions = SpatialFileRDD.InputFormat -> "geojson"

// Call on the SpatialFileRDD object
val featureReaderClass = SpatialFileRDD.getFeatureReaderClass(inputFile.getPath, opts)

// Used subsequently to read partitions
val partitions = SpatialFileRDD.createPartitions(inputFile.getPath, opts, sparkContext.hadoopConfiguration)
for (partition <- partitions) {
  val features = SpatialFileRDD.readPartition(partition, featureReaderClass, true, opts)
  // Process features...
}
```

### LLM Instruction Prompt
- When manually orchestrating low-level spatial partition reads instead of using high-level context extensions (like `sc.shapefile`), use `SpatialFileRDD.getFeatureReaderClass(path, opts)` to determine the correct reader class.
- Always qualify the call with the `SpatialFileRDD` object.
- If the file extension is non-standard or ambiguous, explicitly set the format hint in the `BeastOptions` argument (e.g., `SpatialFileRDD.InputFormat -> "geojson"`).

### Prompt Snippet
```text
To resolve the reader class for manual partition reading in Beast, use `SpatialFileRDD.getFeatureReaderClass(path, opts)`. Provide format hints in `opts` if the file extension does not clearly indicate the vector format.
```

### Common Failure Modes
- **Unqualified Call:** Attempting to call `getFeatureReaderClass(...)` as a bare function instead of qualifying it with `SpatialFileRDD.`.
- **Unresolved Format:** Passing an empty `BeastOptions` for a file with an unrecognized or missing extension, causing Beast to fail to identify the correct `FeatureReader`.
- **Raster Inputs:** Attempting to use this method for raster formats (GeoTIFF, HDF). This API is strictly for vector feature readers; raster loading should use `sc.geoTiff[T]` or `sc.hdfFile`.

### Fix Code Hint
```scala
// Incorrect: val reader = getFeatureReaderClass("data.customext", new BeastOptions())
// Correct: Provide format hints and call on SpatialFileRDD
val opts: BeastOptions = SpatialFileRDD.InputFormat -> "geojson"
val readerClass = SpatialFileRDD.getFeatureReaderClass("data.customext", opts)
```

## API Test: `getGeometry`

### Signature
```scala
def getGeometry: Geometry
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/IFeature.scala:69_

_Source doc:_ The geometry contained in the feature. @return the geometry in this attribute

### Goal
Extracts the underlying spatial geometry (such as a point, polygon, or bounding box) from an `IFeature` object.

### Parameters
_None._

### Input
An `IFeature` instance, typically obtained from loading vector datasets (e.g., via `sc.shapefile`, `sc.geojsonFile`), from spatial joins, or from spatial data generators. 

### Output
Returns `Geometry` — the spatial representation of the feature. Depending on the dataset, this underlying object may be a specific geometry type such as a JTS Geometry or Beast's `EnvelopeND`.

### Valid Call Patterns
```scala
// Extracting the geometry from an IFeature
val geom: Geometry = feature.getGeometry

// Extracting and casting to a specific known type (e.g., EnvelopeND)
val envelope = feature.getGeometry.asInstanceOf[EnvelopeND]
```

### LLM Instruction Prompt
- Call `getGeometry` on an `IFeature` instance when you need to access or manipulate the spatial coordinates, bounding box, or shape of the vector feature.
- The return type is a generic `Geometry`. If you need to access specific coordinate dimensions (e.g., `getMinCoord`), you must cast it to the appropriate subclass (like `EnvelopeND`), ensuring you know the underlying geometry type of the dataset.

### Prompt Snippet
```text
To extract the spatial shape from an `IFeature` in Beast, use `feature.getGeometry`. If you need to manipulate specific dimensions or bounds, cast the returned `Geometry` to the expected type, such as `EnvelopeND`.
```

### Common Failure Modes
- **ClassCastException:** Blindly casting the returned `Geometry` to a specific type (like `EnvelopeND` or a JTS `Polygon`) when the dataset contains mixed geometry types or a different geometry type than expected.
- **NullPointerException:** Attempting to call `getGeometry` on a null feature reference, which can occur if a previous transformation or join produced null values.

### Fix Code Hint
```scala
// Safely handle the extracted geometry using pattern matching
val geom = feature.getGeometry
geom match {
  case env: EnvelopeND => 
    // Safe to use EnvelopeND methods
    val minX = env.getMinCoord(0)
  case _ => 
    // Handle standard JTS geometries or other types
}
```

## API Test: `getInt`

### Signature
```scala
def getInt(i: Int): Int
def getInt(key: String, defaultValue: Int): Int
```
_Source doc:_ Get a value of a key as integer @param key @param defaultValue @return

### Goal
Retrieves an integer value either from a configuration object by its string key (providing a fallback default if missing), or from a Spark SQL `InternalRow` by its column index.

### Parameters
- `key` (`String`): The configuration property name to look up (used in the key-value overload).
- `defaultValue` (`Int`): The fallback integer to return if the specified `key` is not present or cannot be parsed.
- `i` (`Int`): The zero-based column index to retrieve (used in the `InternalRow` overload).

### Input
- For the key-value overload: A configuration object (e.g., `BeastOptions`) containing string-based key-value pairs.
- For the index overload: A Spark SQL `InternalRow` (such as an encoded spatial geometry) where the specified index contains an integer type. The caller should ensure the column is not null before access.

### Output
Returns `Int` — The requested integer value from the row, or the parsed configuration value (falling back to `defaultValue` if the key is absent).

### Valid Call Patterns
```scala
// 1. Retrieving an integer by index from an InternalRow (Authoritative from test suite)
val firstGeom: InternalRow = encoded.head
val geomType: Int = firstGeom.getInt(0)

// 2. Retrieving a configuration value by key (Inferred from signature)
// e.g., reading a Beast configuration option with a safe fallback
val bitsPerSample: Int = options.getInt("GeoTiffWriter.BitsPerSample", 32)
```

### LLM Instruction Prompt
- When extracting integer values from Spark SQL `InternalRow` objects (such as encoded geometries in Parquet), use `row.getInt(index)`. Always check `row.isNullAt(index)` first if the schema allows nulls.
- When reading Beast configuration options, use `options.getInt(key, defaultValue)` to ensure a safe fallback is provided if the user did not specify the setting.

### Prompt Snippet
```text
// Extracting an integer type flag from an encoded geometry row
assertResult(SpatialParquetHelper.PointType)(firstGeom.getInt(0))
```

### Common Failure Modes
- **Null Pointer / Defaulting Errors on Rows:** Calling `getInt(i)` on an `InternalRow` where the value at index `i` is null. This can lead to unexpected behavior or exceptions. Always use `isNullAt(i)` to verify presence before extraction.
- **Type Cast Exceptions:** Calling `getInt(i)` on a column index that actually holds a `DoubleType` or `ArrayType` (e.g., coordinate arrays).
- **Parsing Errors:** Using `getInt(key, default)` on a configuration key where the user provided a non-numeric string value, causing a parsing exception.

### Fix Code Hint
```scala
// Safely extract an integer from an InternalRow by checking for nulls first
val geomType: Int = if (!firstGeom.isNullAt(0)) {
  firstGeom.getInt(0)
} else {
  -1 // or appropriate default/error handling
}
```

## API Test: `getLong`

### Signature
```scala
def getLong(key: String, defaultValue: Long): Long
```
_Source: beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/common/BeastOptions.scala:114_

_Source doc:_ Get a key value as long @param key @param defaultValue @return

### Goal
Retrieves a configuration value associated with the specified key as a 64-bit integer (`Long`), returning a fallback default value if the key is missing.

### Parameters
- `key` (`String`): The configuration property name to look up within the `BeastOptions` instance.
- `defaultValue` (`Long`): The fallback value to return if the specified key does not exist in the configuration.

### Input
An initialized `BeastOptions` instance containing configuration properties for the Beast/RDPro Spark environment. 

### Output
Returns `Long` — The parsed 64-bit integer value associated with the configuration key, or the provided `defaultValue` if the key is absent.

### Valid Call Patterns
```scala
// Note: Call pattern inferred from signature and source path (not verified by test suite)
// Assumes `options` is an instance of edu.ucr.cs.bdlab.beast.common.BeastOptions
val maxPixels = options.getLong("rdpro.raster.maxPixels", 1000000000L)
```

### LLM Instruction Prompt
- When extracting configuration parameters that represent large integers (such as memory limits, pixel counts, or partition thresholds) from a `BeastOptions` object, use `getLong` to ensure type safety and always provide a sensible default `Long` value (e.g., `0L`). Do not call this as a standalone function; it must be called on a `BeastOptions` instance.

### Prompt Snippet
```text
Extract large integer configuration properties safely using `options.getLong("my.config.key", 1000L)`.
```

### Common Failure Modes
- **Missing Receiver:** Attempting to call `getLong("key", 0L)` as a bare function rather than a method on a `BeastOptions` instance.
- **Type Mismatch on Default Value:** Passing a standard `Int` (e.g., `1000`) instead of a `Long` (e.g., `1000L`) for the `defaultValue` parameter, which may cause Scala compiler type-inference errors.
- **Parsing Errors:** If the key exists in the configuration but its string representation cannot be parsed into a valid `Long` (e.g., it contains letters or represents a floating-point number), the underlying parser will likely throw a `NumberFormatException`.

### Fix Code Hint
```scala
// Ensure the method is called on a BeastOptions instance and the default value has the 'L' suffix
val options = new BeastOptions()
val threshold = options.getLong("spatial.join.maxRecords", 500000L)
```

## API Test: `getName`

### Signature
```scala
def getName(i: Int): String
```
_Source doc:_ Return the name of the given attribute. @param i the index of the attribute in the range [0, length[ @return the type of the attribute or null if unknown

### Goal
Retrieves the name of a specific attribute at the given index from a spatial feature's schema.

### Parameters
- `i` (`Int`): The zero-based index of the attribute to query, which must be in the range `[0, length)`.

### Input
A spatial feature (such as an `IFeature` loaded from a Shapefile, GeoJSON, or CSV) that contains an attribute schema. The caller must provide a valid integer index `i` that falls within the bounds of the feature's attribute array.

### Output
Returns `String` — The name of the attribute at the specified index. (Note: The original source documentation mentions returning the "type", which is likely a typo for "name"). Returns `null` if the attribute name is unknown or undefined.

### Valid Call Patterns
```scala
// Inferred from signature (not verified in provided test suite)
// Assuming `feature` is an instance of IFeature or a similar schema-bearing object
val attributeName: String = feature.getName(0)

if (attributeName != null) {
  println(s"First attribute is named: $attributeName")
}
```

### LLM Instruction Prompt
- When inspecting the schema of a spatial feature in Beast, use `getName(i)` to retrieve the attribute's name.
- Always ensure the index `i` is within the valid range `[0, length)` to avoid out-of-bounds errors.
- You MUST handle potential `null` return values, as the API explicitly states it returns `null` if the name is unknown (e.g., in best-effort CSV parsing where headers might be missing).

### Prompt Snippet
```text
Use `feature.getName(i: Int)` to get the attribute name at index `i`. Ensure `i` is within bounds and handle `null` returns safely, as undefined attributes return `null`.
```

### Common Failure Modes
- **`IndexOutOfBoundsException`**: Occurs if `i` is negative or greater than or equal to the total number of attributes in the feature.
- **`NullPointerException`**: Occurs if the caller attempts to invoke methods (like `.toLowerCase()`) on the returned `String` without checking if it is `null`, which is common when reading formats without strict schemas (like headerless CSVs).

### Fix Code Hint
```scala
// Check bounds and handle nulls safely
val numAttributes = feature.length // or equivalent method to get attribute count
if (i >= 0 && i < numAttributes) {
  val name = feature.getName(i)
  val safeName = Option(name).getOrElse(s"attribute_$i")
  // Proceed with safeName
}
```

## API Test: `getOperationParams`
_Grounding: doc-repaired from source (docfix)._

### Goal
**INTERNAL/FRAMEWORK API.** Exclude from scored denominator. This API is part of the internal command-line parsing and validation plumbing. It dynamically discovers and retrieves all valid configuration parameters (annotated with `@OperationParam`) for a specific Beast operation using Java reflection.

### Input
**TESTABLE ONLY WITH EXPLICIT LOW-LEVEL CONSTRUCTION.** 
- `operation` (`Operation`): The operation metadata object to inspect. Must be retrieved dynamically from the caller-owned `OperationHelper.operations` map.
- `opts` (`BeastOptions`): Additional user options used to resolve dependent classes.

### Output
Returns `Array[OperationParamInfo]`, an array containing the extracted parameter names and their corresponding `@OperationParam` annotations.

### Valid Call Patterns
```scala
import edu.ucr.cs.bdlab.beast.util.OperationHelper
import edu.ucr.cs.bdlab.beast.common.BeastOptions

// Safely retrieve any available operation without hardcoding names
val opOpt = OperationHelper.operations.values.headOption
opOpt.foreach { op =>
  val opts = new BeastOptions()
  val params = OperationHelper.getOperationParams(op, opts)
  require(params != null, "Returned parameters array should not be null")
}
```

### LLM Instruction Prompt
- Do not hardcode or assert the presence of specific operation names (like `"spatialJoin"`) in `OperationHelper.operations`, as they may not be registered in minimal test environments.
- To test or use the API dynamically, retrieve an available operation using `OperationHelper.operations.values.headOption`.
- `OperationHelper.operations` is a Scala Map, so its values can be safely accessed and iterated over without knowing the exact keys present.

### Prompt Snippet
```text
`OperationHelper.getOperationParams(op: Operation, opts: BeastOptions): Array[OperationParamInfo]` returns `@OperationParam` fields. INTERNAL API: Do not hardcode operation names; retrieve dynamically via `OperationHelper.operations.values.headOption`.
```

### Common Failure Modes
- **INTERNAL/FRAMEWORK API Misuse:** Treating this as a standard user-facing geospatial API. It is a reflection-based utility for CLI generation and should be excluded from main user-facing benchmark denominators.
- **Hardcoding Operation Names:** Hard-asserting the presence of a specific operation (e.g., `"spatialJoin"`) in `OperationHelper.operations`. This crashes minimal test environments with a `java.lang.AssertionError` because operations are often dynamically loaded and not registered by default in isolated harnesses.

### Fix Code Hint
**WRONG:** Hardcoding an operation name that may not exist in the test environment.
```scala
val opName = "spatialJoin"
assert(OperationHelper.operations.contains(opName), s"Operation $opName must be registered")
val op = OperationHelper.operations(opName)
val params = OperationHelper.getOperationParams(op, new BeastOptions())
```

**CORRECT:** Dynamically retrieving any available operation from the map.
```scala
val opOpt = OperationHelper.operations.values.headOption
opOpt.foreach { op =>
  val params = OperationHelper.getOperationParams(op, new BeastOptions())
  params.foreach(p => println(p.name))
}
```

## API Test: `getPointValue`

### Signature
```scala
def getPointValue(x: Double, y: Double): T
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/ITile.scala:93_

_Source doc:_ Return the value of the pixel that contains the given point at model (world) coordinates. @param x the x-coordinate of the point, e.g., longitude @param y the y-coordinate of the point, e.g., latitude @return the value of all components of the given pixel

### Goal
Retrieve the pixel value(s) from a raster tile at a specific geographic (model/world) coordinate.

### Parameters
- `x` (`Double`): The x-coordinate of the point in model (world) coordinates, such as longitude.
- `y` (`Double`): The y-coordinate of the point in model (world) coordinates, such as latitude.

### Input
An `ITile[T]` instance, typically obtained from a `GeoTiffReader[T]` or an RDD of raster tiles. The provided `x` and `y` coordinates must be in the same Coordinate Reference System (CRS) as the raster tile (e.g., EPSG:4326 for longitude/latitude). The point must spatially intersect the specific tile being queried.

### Output
Returns `T` — the value of all components of the pixel containing the point. The type `T` exactly matches the runtime pixel type of the raster (e.g., `Int` for single-band integer, `Float` for single-band float, `Array[Int]` or `Array[Float]` for multi-band rasters).

### Valid Call Patterns
```scala
// Example 1: Single-band integer GeoTIFF
val reader = new GeoTiffReader[Int]
reader.initialize(fileSystem, rasterPath, "0", new BeastOptions)
// Ensure the tile actually contains the point before querying
val tileId = reader.metadata.getTileIDAtPoint(23.224, 32.415)
val tile = reader.readTile(tileId)
val pixelValue: Int = tile.getPointValue(23.224, 32.415)

// Example 2: Multi-band (banded) float GeoTIFF
val bandedReader = new GeoTiffReader[Array[Float]]
bandedReader.initialize(fileSystem, bandedRasterPath, "0", new BeastOptions)
val bandedTileId = bandedReader.metadata.getTileIDAtPoint(31.277, 26.954)
val bandedTile = bandedReader.readTile(bandedTileId)
val pixelValues: Array[Float] = bandedTile.getPointValue(31.277, 26.954)
```

### LLM Instruction Prompt
- Call `tile.getPointValue(x, y)` to extract pixel data at a geographic location.
- NEVER pass pixel/grid indices (column/row) to this function; it strictly requires model/world coordinates (e.g., longitude and latitude).
- Ensure the receiver is an `ITile[T]`. The return type `T` will match the tile's type parameter, which must align with the GeoTIFF's runtime type (`Int`, `Float`, `Array[Int]`, or `Array[Float]`).
- Always verify that the point falls within the tile's spatial bounds before calling, typically by using `metadata.getTileIDAtPoint(x, y)` to fetch the correct tile first.

### Prompt Snippet
```text
To get a pixel value at a specific geographic coordinate from an `ITile[T]`, use `tile.getPointValue(x, y)`. The coordinates must be in the raster's world CRS (e.g., longitude/latitude), not pixel indices. The return type matches the tile's type `T` (e.g., `Int`, `Float`, or `Array[Float]` for multi-band). Ensure the point is actually within the tile's bounds.
```

### Common Failure Modes
- **Coordinate Space Mismatch:** Passing pixel coordinates (x=column, y=row) instead of world coordinates (x=longitude, y=latitude), resulting in out-of-bounds errors or incorrect pixel values.
- **Spatial Out-of-Bounds:** Calling `getPointValue` on a tile that does not spatially cover the requested `(x, y)` point.
- **Type Mismatch:** Expecting a scalar value (e.g., `Float`) when querying a multi-band raster tile, which actually returns an `Array[Float]`.

### Fix Code Hint
```scala
// BAD: Passing pixel indices or querying a random tile
// val value = randomTile.getPointValue(col, row)

// GOOD: Fetching the correct tile using world coordinates first, then querying
val x = -117.32
val y = 33.95
val tileId = reader.metadata.getTileIDAtPoint(x, y)
val tile = reader.readTile(tileId)
val value = tile.getPointValue(x, y)
```

## API Test: `getStorageSize`
_Grounding: doc-repaired from source (docfix)._

### Goal
INTERNAL/FRAMEWORK API. Estimates the in-memory byte size of spatial features or specific attribute values. Note: This is an internal utility for memory/index planning and should be excluded from the main user-facing benchmark denominator.

### Input
INTERNAL/FRAMEWORK API. 
- For the instance method: A caller-owned `IFeature` instance (e.g., extracted via `featuresRDD.first()`).
- For the companion object method: A non-null `value: Any` and its corresponding Spark SQL `dataType: DataType`.

### Output
Returns `Int` representing the estimated in-memory storage size in bytes.

### Valid Call Patterns
```scala
import edu.ucr.cs.bdlab.beast.geolite.IFeature
import org.apache.spark.sql.types.{DataType, StringType, IntegerType}

// 1. Instance method (safely skips null attributes)
// Assumes caller-owned featuresRDD: RDD[IFeature] is available in the environment
val feature = featuresRDD.first()
val featureSize: Int = feature.getStorageSize

// 2. Companion object method (DOES NOT handle nulls safely)
val stringValue = "sample_string"
val stringSize: Int = IFeature.getStorageSize(stringValue, StringType)
```

### LLM Instruction Prompt
- Classify as INTERNAL/FRAMEWORK.
- The parameterless `getStorageSize` is an instance method on `IFeature` that returns an `Int` and safely skips null attributes.
- The 2-argument `getStorageSize(value: Any, dataType: DataType)` is a method on the `IFeature` companion object (`IFeature.getStorageSize`), NOT an instance method.
- The 2-argument object method does NOT safely handle `null` values; passing `null` will cause a `NullPointerException` when it attempts to measure the value's size.

### Prompt Snippet
`getStorageSize` is an internal API. The parameterless instance method `feature.getStorageSize` safely skips nulls. The 2-argument companion object method `IFeature.getStorageSize(value, dataType)` throws NPE on nulls and must be called on the object, not the instance.

### Common Failure Modes
- **INTERNAL/FRAMEWORK API:** Exclude from standard user-facing workflows.
- **Calling 2-argument method on an instance:** Attempting `feature.getStorageSize(value, dataType)` fails with "Int does not take parameters". The instance method takes 0 arguments and returns an `Int`. The 2-argument method belongs strictly to the `IFeature` companion object.
- **Passing null to the companion object method:** Passing `null` to `IFeature.getStorageSize(null, StringType)` throws a `NullPointerException` when it attempts to cast and measure length. Only the parameterless instance method safely skips nulls.
- **Unhandled Data Types:** The object method throws a `MatchError` for types not explicitly handled (e.g., `ShortType`, `FloatType`, `BinaryType`) and a `ClassCastException` if the value doesn't match the provided `DataType`.

### Fix Code Hint
```scala
// WRONG: Calling 2-arg method on instance, or passing null to the object method
// val size = feature.getStorageSize("text", StringType) // Compiler error: Int does not take parameters
// val size = IFeature.getStorageSize(null, StringType)  // Throws NullPointerException

// CORRECT: Call 2-arg method on the companion object with non-null values
import edu.ucr.cs.bdlab.beast.geolite.IFeature
import org.apache.spark.sql.types.StringType

val stringSize = IFeature.getStorageSize("sample_string", StringType)

// CORRECT: Call parameterless method on the instance
val featureSize = feature.getStorageSize
```

## API Test: `getTileIDAtPixel`

### Signature
```scala
def getTileIDAtPixel(iPixel: Int, jPixel: Int): Int
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/RasterMetadata.scala:69_

_Source doc:_ Computes the ID of the tile that contains the given pixel. Tiles are numbered in row-wise ordering. @param iPixel the position of the column of the pixel @param jPixel the position of the row of the pixel @return a unique identifier for the tile that contains this pixel location

### Goal
Computes the unique, row-wise tile ID that contains a specific pixel coordinate within a raster dataset's grid.

### Parameters
- `iPixel` (`Int`): The column index (x-coordinate in pixel space) of the target pixel.
- `jPixel` (`Int`): The row index (y-coordinate in pixel space) of the target pixel.

### Input
This method must be called on a `RasterMetadata` instance, which is typically accessed via a `GeoTiffReader` (e.g., `reader.metadata`) or an `ITile` (e.g., `tile.rasterMetadata`). The input coordinates must be in **pixel grid space** (integers), not model space (e.g., not degrees or meters). If you have model coordinates (longitude/latitude), you must first convert them using `metadata.modelToGrid`.

### Output
Returns `Int` — a unique identifier for the tile that contains the specified pixel location. The IDs are assigned sequentially in row-wise (raster scan) order across the dataset.

### Valid Call Patterns
```scala
// Pattern 1: Using a GeoTiffReader's metadata (e.g., after modelToGrid conversion)
val outPoint = new java.awt.geom.Point2D.Double
reader.metadata.modelToGrid(-0.06, 49.28, outPoint)
val iPixel = outPoint.getX.toInt
val jPixel = outPoint.getY.toInt
val tileID = reader.metadata.getTileIDAtPixel(iPixel, jPixel)

// Pattern 2: Using an ITile's metadata within an RDD transformation
val fileTileRDD = new RasterFileRDD[Int](sparkContext, dirPath, new BeastOptions())
val originTiles = fileTileRDD.filter(t => t.rasterMetadata.getTileIDAtPixel(0, 0) == t.tileID)
```

### LLM Instruction Prompt
- When determining which tile contains a specific pixel, call `getTileIDAtPixel(iPixel, jPixel)` on a `RasterMetadata` object.
- Never call this as a standalone function; it is a method of `RasterMetadata`.
- Ensure `iPixel` represents the column (x) and `jPixel` represents the row (y). Do not swap them.
- Do not pass geographic coordinates (CRS model space) directly to this function. Convert them to pixel coordinates first using `metadata.modelToGrid(x, y, outPoint)`.

### Prompt Snippet
```text
To find the tile ID for a specific pixel, use `metadata.getTileIDAtPixel(iPixel, jPixel)`. Remember that `iPixel` is the column (x) and `jPixel` is the row (y). If you have geographic coordinates, convert them to grid coordinates first using `metadata.modelToGrid`.
```

### Common Failure Modes
- **Calling as a standalone function:** Attempting to use `getTileIDAtPixel(x, y)` without a `RasterMetadata` receiver will cause a compilation error.
- **Passing Model Coordinates:** Passing longitude/latitude or projected meters directly into `iPixel` and `jPixel` will result in wildly incorrect tile IDs or out-of-bounds errors.
- **Swapping Row and Column:** Passing `(row, column)` instead of `(column, row)` will yield the wrong tile ID. `iPixel` is always the column (x-axis).

### Fix Code Hint
```scala
// WRONG: Passing geographic coordinates directly
// val tileID = metadata.getTileIDAtPixel(-117.32, 33.95)

// WRONG: Swapping row and column
// val tileID = metadata.getTileIDAtPixel(row, col)

// RIGHT: Convert model to grid, then extract column (x) and row (y)
val outPoint = new java.awt.geom.Point2D.Double
metadata.modelToGrid(-117.32, 33.95, outPoint)
val tileID = metadata.getTileIDAtPixel(outPoint.getX.toInt, outPoint.getY.toInt)
```

## API Test: `getTileIDAtPoint`
_Grounding: doc-repaired from source (docfix)._

### Signature
```scala
def getTileIDAtPoint(x: Double, y: Double): Int
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/RasterMetadata.scala:81_

### Goal
**ADVANCED/LOW-LEVEL API.** Resolves a geographic coordinate in model (world) space to the internal integer ID of the raster tile that contains it. 
*Note: This is internal framework plumbing for readers and spatial joins. It should be excluded from the main user-facing denominator.*

### Parameters
- `x` (`Double`): The x-coordinate of the point in model (world) space (e.g., longitude).
- `y` (`Double`): The y-coordinate of the point in model (world) space (e.g., latitude).

### Input
Requires an initialized `RasterMetadata` instance (e.g., extracted via `tile.rasterMetadata` from a loaded `RasterFileRDD`). As an ADVANCED/LOW-LEVEL API, it requires explicit low-level construction to test. The `x` and `y` parameters must be in model (world) coordinates, NOT grid (pixel) coordinates.

### Output
Returns `Int` — The ID of the tile containing the point. 
**CRITICAL:** Contrary to previous documentation, this method does **NOT** return `-1` for out-of-bounds points. It blindly performs grid arithmetic and returns a mathematically extrapolated, invalid tile ID.

### Valid Call Patterns
```scala
import edu.ucr.cs.bdlab.beast.geolite.RasterMetadata
import java.awt.geom.Point2D

// ADVANCED/LOW-LEVEL: Extract metadata from a loaded tile (caller-owned)
val tile = rasterRDD.first()
val metadata: RasterMetadata = tile.rasterMetadata

// Convert a known valid pixel coordinate (grid space) to world coordinates (model space)
val pt = new Point2D.Double()
// Using the top-left pixel of the raster to guarantee it is within bounds
metadata.gridToModel(metadata.x1.toDouble, metadata.y1.toDouble, pt)

// Resolve the tile ID for the valid model point
val tileId = metadata.getTileIDAtPoint(pt.x, pt.y)

println(s"__CHECK__ getTileIDAtPoint $tileId")
```

### LLM Instruction Prompt
- `getTileIDAtPoint` is an ADVANCED/LOW-LEVEL API. Exclude it from standard user workflows.
- It does NOT return `-1` for out-of-bounds points; it blindly performs grid arithmetic and returns an extrapolated, invalid integer tile ID.
- Callers must manually verify if a point is within the raster bounds (using `metadata.modelToGrid` and `metadata.isPixelInRange`) before calling this method if out-of-bounds coordinates are possible.
- The `x` and `y` parameters must be in model (world) coordinates. Do not pass `RasterMetadata` properties like `x1`, `x2`, `y1`, or `y2` directly to this method, as those represent grid (pixel) coordinates.

### Prompt Snippet
```text
`metadata.getTileIDAtPoint(x, y)` is a low-level API that resolves model (world) coordinates to a tile ID. It does NOT check bounds and will return an invalid extrapolated ID (not `-1`) for out-of-bounds points. Manually check bounds first using `modelToGrid` and `isPixelInRange`. Never pass pixel coordinates (like `x1`, `y1`) as `x` and `y`.
```

### Common Failure Modes
- **AssertionError on Out-of-Bounds (The "Expected -1" Failure):** Expecting the method to return `-1` for out-of-bounds points. The method lacks bounds checking and returns a mathematically extrapolated, invalid tile ID.
- **Passing Pixel Coordinates as Model Coordinates:** Passing metadata properties like `x1` or `y1` directly to `getTileIDAtPoint`. This causes the internal inverse transform to produce wildly out-of-bounds values.
- **Usage in Standard Workflows:** Attempting to use this ADVANCED/LOW-LEVEL internal API for standard user-facing operations.

### Fix Code Hint
```scala
// WRONG: Passing pixel bounds directly as model coordinates and expecting -1 for out-of-bounds
val id = metadata.getTileIDAtPoint(metadata.x1, metadata.y1)
if (id == -1) { println("Out of bounds") }

// CORRECT: Use model coordinates and manually check bounds first
import java.awt.geom.Point2D

val targetX = 23.224
val targetY = 32.415

val pt = new Point2D.Double()
metadata.modelToGrid(targetX, targetY, pt)

val tileId = if (metadata.isPixelInRange(pt.x.toInt, pt.y.toInt)) {
  metadata.getTileIDAtPoint(targetX, targetY)
} else {
  -1 // Handle out of bounds manually
}
```

## API Test: `getValue`

### Signature
```scala
def getValue(in: FSDataInputStream, offset: Long, key: Long): (Long, Int)
def getValue(fileSystem: FileSystem, path: Path, key: Long): (Long, Int)
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/DiskTileHashtable.scala:91  (+1 more definition site/overload)_

_Source doc:_ Return the value that corresponds to the given key or null if the value is not found. @param in the hashtable file @param offset the offset of the hashtable in the file @param key the key to search for @return the value of the key if found, or `null` if the key is not found.

### Goal
Retrieves a stored value (typically a file offset and length tuple) associated with a specific key (e.g., a tile ID) from a disk-based hashtable file used in DaVinci visualization pipelines.

### Parameters
- `in` (`FSDataInputStream`): The open Hadoop file input stream pointing to the hashtable file. (In the overload, `fileSystem: FileSystem` and `path: Path` are used to open this stream automatically).
- `offset` (`Long`): The byte offset within the file where the hashtable structure begins.
- `key` (`Long`): The unique identifier (e.g., spatial tile ID) to search for within the hashtable.

### Input
Requires a valid, accessible Hadoop `FileSystem` and `Path` (or an already open `FSDataInputStream`) pointing to a disk-based hashtable file generated by Beast's visualization/MVT components. The `offset` must accurately point to the start of the hashtable block within that file.

### Output
Returns `(Long, Int)` — A tuple representing the value associated with the key (typically the byte offset `Long` and byte length `Int` of the corresponding tile data in the archive). Note: As per the source documentation, this method returns `null` if the key is not found, which requires explicit null-checking despite the Scala Tuple return type.

### Valid Call Patterns
```scala
// Note: Call pattern inferred from signature. 
// (The project's test suite examples demonstrate UniformHistogram#getValue(Array[Int], Array[Int]), 
// which shares the same name but is a completely different API).

// Using an open FSDataInputStream
val tileDataLocation: (Long, Int) = DiskTileHashtable.getValue(inStream, 0L, tileKey)

// Using a FileSystem and Path
val tileDataLocation2: (Long, Int) = DiskTileHashtable.getValue(hadoopFS, indexPath, tileKey)
```

### LLM Instruction Prompt
- DO NOT confuse this `DiskTileHashtable` visualization method with `UniformHistogram.getValue(Array[Int], Array[Int])`. If the user wants to query a spatial histogram, use the array-based signature. If they are querying a DaVinci disk hashtable, use this stream/path-based signature.
- Always check the result for `null` before accessing the tuple elements, as the underlying implementation returns `null` (rather than an `Option`) when a key is missing.
- Ensure the `FSDataInputStream` is open and positioned correctly, or use the `FileSystem` overload to let the method handle stream lifecycle.

### Prompt Snippet
```text
When querying a DaVinci disk-based tile hashtable in Beast, use `getValue(in: FSDataInputStream, offset: Long, key: Long): (Long, Int)`. Because this API returns `null` when a key is missing, you must explicitly check for null before extracting the offset and length from the returned tuple. Do not confuse this with `UniformHistogram.getValue`.
```

### Common Failure Modes
- **NullPointerException:** Failing to check if the returned `(Long, Int)` is `null` before attempting to access `_1` or `_2`.
- **EOFException / Corrupted Reads:** Providing an incorrect `offset` value that does not align with the actual start of the hashtable in the file.
- **Signature Confusion:** Attempting to pass `Array[Int]` coordinates to this method when intending to query a `UniformHistogram`.
- **Closed Stream:** Passing an `FSDataInputStream` that has already been closed by another part of the application.

### Fix Code Hint
```scala
// BAD: Assumes the tuple is always returned and throws NullPointerException if key is missing
val (tileOffset, tileLength) = DiskTileHashtable.getValue(fs, path, key)

// GOOD: Explicitly handles the documented null return value
val result = DiskTileHashtable.getValue(fs, path, key)
if (result != null) {
  val tileOffset = result._1
  val tileLength = result._2
  // process tile
} else {
  // handle missing tile
}
```

## API Test: `gridToModel`

### Signature
```scala
def gridToModel(i: Double, j: Double, outPoint: Point2D.Double): Unit
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/RasterMetadata.scala:150_

_Source doc:_ Converts a point location from the grid (pixel) space to the model (world) space @param i the position of the column @param j the position of the row @param outPoint the output point that contains the model coordinates

### Goal
Converts a pixel's column and row coordinates (grid space) into real-world geographic coordinates (model space) using the raster's affine transformation metadata.

### Parameters
- `i` (`Double`): The column index (x-axis in grid space) of the pixel location.
- `j` (`Double`): The row index (y-axis in grid space) of the pixel location.
- `outPoint` (`Point2D.Double`): A pre-allocated mutable point object that will be updated in-place to store the resulting real-world X (longitude/easting) and Y (latitude/northing) coordinates.

### Input
Requires a valid `RasterMetadata` instance (often accessed via `reader.metadata` from a `GeoTiffReader` or created manually) to act as the receiver. The caller must also instantiate and provide a `java.awt.geom.Point2D.Double` object to hold the output. The `i` and `j` values typically fall within `0` and the raster's width/height, though the affine transformation will mathematically compute coordinates for out-of-bounds indices as well.

### Output
Returns `Unit` — the result is written in-place to the provided `outPoint` parameter, updating its `x` and `y` fields to the computed model (world) coordinates.

### Valid Call Patterns
```scala
import java.awt.geom.Point2D

// Assuming `reader` is an initialized GeoTiffReader or `metadata` is a RasterMetadata instance
val outPoint = new Point2D.Double()

// Transform the origin point (top-left corner) from raster grid to world coordinates
reader.metadata.gridToModel(0.0, 0.0, outPoint)

// outPoint.x and outPoint.y now contain the geographic coordinates
println(s"World X: ${outPoint.x}, World Y: ${outPoint.y}")
```

### LLM Instruction Prompt
- Always pre-allocate a `java.awt.geom.Point2D.Double` before calling `gridToModel`.
- Remember that `gridToModel` returns `Unit` and mutates the `outPoint` argument in-place. Do not attempt to assign its return value to a variable.
- Call this method on a `RasterMetadata` instance (e.g., `metadata.gridToModel(...)`).
- Note the parameter order: `i` is the column (x-axis in grid), and `j` is the row (y-axis in grid).

### Prompt Snippet
```text
To convert raster pixel coordinates to world coordinates in RDPro, instantiate a `new java.awt.geom.Point2D.Double()`, then call `metadata.gridToModel(col, row, outPoint)`. The method returns `Unit` and mutates `outPoint` in-place. Do not expect a returned tuple or point object.
```

### Common Failure Modes
- **Assigning the Return Value:** Python/rasterio users often expect an affine transform to return a tuple `(x, y)`. In RDPro, `gridToModel` returns `Unit`, so assigning it (e.g., `val pt = metadata.gridToModel(i, j, outPoint)`) results in a `Unit` type mismatch if `pt` is later used as a geometry.
- **Null Pointer Exception:** Passing `null` instead of a pre-instantiated `Point2D.Double` for the `outPoint` parameter will cause a runtime crash.
- **Coordinate Swapping:** Passing the row as `i` and the column as `j`. `i` must be the column (width/x dimension) and `j` must be the row (height/y dimension).

### Fix Code Hint
```scala
// WRONG: Expecting a returned point
// val worldPt = reader.metadata.gridToModel(col, row, new Point2D.Double())

// RIGHT: Mutating a pre-allocated point in-place
val worldPt = new java.awt.geom.Point2D.Double()
reader.metadata.gridToModel(col, row, worldPt)
// Use worldPt.x and worldPt.y
```

## API Test: `hdfFile`

### Signature
```scala
def hdfFile(path: String, layer: String, opts: BeastOptions = new BeastOptions()): RDD[ITile[Float]]
def hdfFile(filename: String, layer: String): JavaRasterRDD[Float]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RaptorMixin.scala:46  (+1 more definition site/overload)_

### Goal
Reads a Hierarchical Data Format (HDF) file or a directory of HDF files into a distributed raster RDD, extracting a specific data layer for pixel-level processing.

### Parameters
- `path` (`String`): The path to the HDF file or a directory containing HDF files.
- `layer` (`String`): The specific layer name to read from the HDF file (e.g., `"LST_Day_1km"`).
- `opts` (`BeastOptions`), default `new BeastOptions()`: Optional configuration for reading the file.

### Input
Requires an initialized SparkContext (`sc`) or `JavaSpatialSparkContext` with Beast extensions loaded. The input must be a valid HDF file (or directory of HDF files) accessible to the Spark cluster, and the specified `layer` must exist within the file's hierarchical structure. 

### Output
Returns `RDD[ITile[Float]]` (often aliased as `RasterRDD[Float]`) — a distributed collection of raster tiles containing the pixel data from the specified HDF layer, represented as 32-bit floats.

### Valid Call Patterns
```scala
// Load a specific layer from an HDF file using the SparkContext extension
val temperatureK: RasterRDD[Float] = sc.hdfFile("MOD11A1.A2022173.h08v05.006.2022174092443.hdf", "LST_Day_1km")

// Perform pixel math and save the result (must be saved as GeoTIFF, not HDF)
val temperatureF: RasterRDD[Float] = temperatureK.mapPixels(k => (k - 273.15f) * 9 / 5 + 32)
temperatureF.saveAsGeoTiff("temperature_f")
```

### LLM Instruction Prompt
- Call `hdfFile` as an extension method on the `SparkContext` (e.g., `sc.hdfFile(...)`).
- You MUST provide both the `path` and the `layer` name; HDF files contain multiple sub-datasets, so a layer name is strictly required.
- The returned RDD is always typed to `Float` (`RDD[ITile[Float]]`), as float values are represented in 32-bits in RDPro.
- Do not attempt to save the output back to HDF format. RDPro only supports GeoTIFF as a raster output format.

### Prompt Snippet
```text
To load HDF rasters in RDPro, use `sc.hdfFile(path, layer)`. It requires both the file path and the specific layer name to extract. It always returns an `RDD[ITile[Float]]` (or `RasterRDD[Float]`). If you need to save the processed raster, you must use `saveAsGeoTiff` as HDF output is not supported.
```

### Common Failure Modes
- **Missing Layer Argument:** Attempting to call `sc.hdfFile(path)` without specifying the layer name will fail to compile.
- **Unsupported Output Format:** Attempting to save the resulting RDD back to an HDF file. RDPro only supports writing rasters to GeoTIFF.
- **Incorrect Type Parameter:** Attempting to type the output as `RDD[ITile[Int]]`. `hdfFile` strictly returns `Float` tiles.

### Fix Code Hint
```scala
// WRONG: Missing layer name
// val raster = sc.hdfFile("MOD11A1.A2022173.h08v05.006.2022174092443.hdf")

// WRONG: Attempting to save back to HDF
// raster.saveAsHDF("output.hdf")

// CORRECT: Provide layer name and save as GeoTIFF
val raster: RDD[ITile[Float]] = sc.hdfFile("MOD11A1.A2022173.h08v05.006.2022174092443.hdf", "LST_Day_1km")
raster.saveAsGeoTiff("output_geotiff")
```

## API Test: `id`

### Signature
```scala
def id: Int
```
_Source: beast/dataExplorer/src/main/scala/edu/ucr/cs/bdlab/beast/dataExplorer/DatasetProcessor.scala:58_

### Goal
Retrieves the unique integer identifier of the current object (such as a `DatasetProcessor` handling spatial data exploration tasks).

### Parameters
_None._

### Input
An initialized instance of the class defining this method (e.g., a `DatasetProcessor` instance). No arguments are passed to the method.

### Output
Returns `Int` — the unique integer representing the identifier of the object or dataset.

### Valid Call Patterns
```scala
// Note: Call form is inferred from the signature (not verified by examples)
val processorId: Int = datasetProcessor.id
```

### LLM Instruction Prompt
- Call `id` without parentheses, as it is defined as a parameterless method.
- Expect an `Int` return type; do not treat the identifier as a `String` or UUID.
- Only call this on objects known to expose it (e.g., `DatasetProcessor`), as it is not a universal Spark RDD method in this specific context.

### Prompt Snippet
```text
To retrieve the integer identifier for the dataset processor, call `.id` without parentheses. Ensure you assign the result to an `Int`.
```

### Common Failure Modes
- **Syntax Error (Parentheses):** Calling `obj.id()` with parentheses will cause a compilation error because the method is defined without them (`def id: Int`).
- **Type Mismatch:** Attempting to assign the result to a `String` or using string-specific methods on the returned value without calling `.toString` first.

### Fix Code Hint
```scala
// ❌ Incorrect: Using parentheses or expecting a String
// val strId: String = datasetProcessor.id()

// ✅ Correct: No parentheses, returns Int
val currentId: Int = datasetProcessor.id
```

## API Test: `initialized`

### Signature
```scala
def initialized: Boolean
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/shapefilev2/ShapefileReader.scala:48_

_Source doc:_ A flag that is raised after the file has been initialized

### Goal
Checks whether the underlying spatial file reader (such as a `ShapefileReader`) has completed its initialization phase and is ready to process data.

### Parameters
_None._

### Input
An instantiated low-level file reader object (e.g., `ShapefileReader`) that manages the loading of spatial data formats. 

### Output
Returns `Boolean` — `true` if the file reader has been successfully initialized; `false` otherwise.

### Valid Call Patterns
```scala
// Note: This example is inferred from the signature (not verified) as no direct examples were provided in the context.
val isReady: Boolean = reader.initialized
```

### LLM Instruction Prompt
- Use `initialized` only when manually interacting with low-level Beast readers (like `ShapefileReader`) to verify that the reader's setup phase is complete.
- For standard Spark workflows, prefer high-level context extensions (e.g., `sc.shapefile`, `sc.geoTiff[T]`) which handle reader instantiation and initialization automatically.
- Do not pass any arguments to `initialized`.

### Prompt Snippet
```text
When working with low-level Beast file readers, use `reader.initialized` to check if the file has been successfully initialized before attempting to read records. Note that standard Spark workflows should use `sc.shapefile` instead of manual readers.
```

### Common Failure Modes
- Attempting to extract records or metadata from a low-level reader before `initialized` returns `true`, which can lead to uninitialized state errors.
- Manually managing reader state in distributed Spark transformations instead of relying on Beast's built-in `SparkContext` extensions.

### Fix Code Hint
```scala
// Instead of manually managing low-level readers and checking initialization:
// val isReady = reader.initialized

// Prefer high-level context extensions which manage reader initialization internally:
val features = sc.shapefile("ne_10m_admin_0_countries.zip")
```

## API Test: `isCW`
_Grounding: doc-repaired from source (docfix)._

### Goal
Checks whether a sequence of 2D coordinates forms a closed ring and is wound in a clockwise direction. **NOTE: This is an INTERNAL/FRAMEWORK API** used for visualization plumbing (MVT generation). It requires explicit low-level construction to test and should be excluded from main user-facing benchmark denominators.

### Input
Requires explicit low-level construction of a concrete `LiteGeometry` subclass. Specifically, the caller must instantiate `edu.ucr.cs.bdlab.davinci.LiteList` using two `Array[Short]` objects (`xs` and `ys`) of equal length. This is an INTERNAL/FRAMEWORK object, not a standard user-facing geometry.

### Valid Call Patterns
```scala
import edu.ucr.cs.bdlab.davinci.LiteList

// Define a closed square ring: (0,0) -> (0,10) -> (10,10) -> (10,0) -> (0,0)
val xs = Array[Short](0, 0, 10, 10, 0)
val ys = Array[Short](0, 10, 10, 0, 0)

// Construct the concrete LiteList directly (caller-owned)
val ring = new LiteList(xs, ys)

// Check if the ring is clockwise
val isClockwise: Boolean = ring.isCW
```

### LLM Instruction Prompt
- `isCW` is a parameterless method on `LiteGeometry` and its subclasses.
- To test or use it standalone, instantiate the concrete subclass `edu.ucr.cs.bdlab.davinci.LiteList` using `new LiteList(xs: Array[Short], ys: Array[Short])`.
- Provide a valid closed ring (where the first and last points are identical) to get a meaningful boolean result.
- Do not attempt to instantiate `LiteGeometry` directly, as it is an abstract trait.

### Prompt Snippet
```text
To test `isCW` (an internal framework API), instantiate `edu.ucr.cs.bdlab.davinci.LiteList` with `Array[Short]` coordinates for `xs` and `ys` forming a closed ring, then call `.isCW`.
```

### Common Failure Modes
- **Instantiating an abstract trait:** Attempting to instantiate `LiteGeometry` directly (e.g., `new LiteGeometry()`). `LiteGeometry` is an abstract trait and will cause a compiler error (`trait LiteGeometry is abstract; cannot be instantiated`). You must instantiate a concrete subclass like `LiteList`.
- **Truncated calls:** Writing incomplete method calls like `liteGeom.is`. Use the full `isCW` method name.
- **Unclosed rings:** Calling `isCW` on a sequence of points where the first and last points are not identical will immediately return `false`.
- **Misunderstanding API Scope:** Trying to use this for standard geospatial operations. This is an INTERNAL/FRAMEWORK API meant for low-level visualization plumbing.

### Fix Code Hint
```scala
// WRONG: Attempting to instantiate the abstract trait or truncating the call
// val liteGeom = new edu.ucr.cs.bdlab.davinci.LiteGeometry()
// val isClockwise = liteGeom.is

// RIGHT: Instantiating the concrete LiteList subclass with closed ring arrays
import edu.ucr.cs.bdlab.davinci.LiteList

val xs = Array[Short](0, 0, 10, 10, 0)
val ys = Array[Short](0, 10, 10, 0, 0)
val ring = new LiteList(xs, ys)
val isClockwise = ring.isCW
```

## API Test: `isDefined`

### Signature
```scala
def isDefined(i: Int, j: Int): Boolean
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/ITile.scala:126_

_Source doc:_ Checks if the given pixel is defined (not empty) @param i the index of the column @param j the index of the row @return `true` if pixel has a valid value or `false` if it does not.

### Goal
Checks whether a specific pixel at column `i` and row `j` within a raster tile contains a valid (non-empty or non-NoData) value.

### Parameters
- `i` (`Int`): The index of the column for the pixel within the tile.
- `j` (`Int`): The index of the row for the pixel within the tile.

### Input
An instance of `ITile[T]` (typically accessed when iterating over pixels in a `RasterRDD` or during custom tile-level operations). The caller must provide valid integer indices `i` and `j` that fall within the bounds of the tile's dimensions.

### Output
Returns `Boolean` — `true` if the pixel has a valid data value, or `false` if it is empty (e.g., represents a NoData value in the underlying GeoTIFF or HDF).

### Valid Call Patterns
```scala
// Inferred from the signature (not verified in test suite).
// Note: The test suite examples show Scala's standard Option.isDefined (0 arguments).
// This pattern applies to RDPro's ITile.isDefined(i, j).

// Assuming `tile` is an ITile[T] and we are iterating over its dimensions:
val isValid: Boolean = tile.isDefined(i, j)

if (isValid) {
  // Safe to process the pixel value
}
```

### LLM Instruction Prompt
- When performing pixel-level math or custom raster processing on an `ITile`, always use `tile.isDefined(i, j)` to check for NoData or empty pixels before attempting to read or transform the pixel value. 
- Do not confuse `ITile.isDefined(i: Int, j: Int)` with Scala's standard `Option.isDefined` (which takes no arguments). Ensure you pass the column and row indices.

### Prompt Snippet
```text
// Check if a pixel is valid before applying band math
if (tile.isDefined(col, row)) {
  val pixelValue = tile.getPixelValue(col, row)
  // ...
}
```

### Common Failure Modes
- **Index Out of Bounds:** Passing `i` or `j` values that are less than 0 or greater than or equal to the tile's width or height, respectively, which may throw an exception depending on the underlying tile implementation.
- **Method Signature Confusion:** Attempting to call `isDefined` without arguments on an `ITile`, confusing it with `Option.isDefined`. The compiler will fail because `ITile.isDefined` requires exactly two `Int` arguments.

### Fix Code Hint
```scala
// WRONG: Confusing ITile.isDefined with Option.isDefined
if (tile.isDefined) { ... }

// RIGHT: Passing the specific column and row indices
if (i >= 0 && i < tile.tileWidth && j >= 0 && j < tile.tileHeight) {
  if (tile.isDefined(i, j)) {
    // Process valid pixel
  }
}
```

## API Test: `isEmptyAt`
_Grounding: doc-repaired from source (docfix)._

### Signature
```scala
def isEmptyAt(x: Double, y: Double): Boolean
```

### Goal
ADVANCED/LOW-LEVEL API (Note: Exclude from main user-facing denominator; use only for internal/advanced point-based queries). Checks if a specific spatial (model) location (x, y) falls into a "no data" (empty) pixel within a specific raster tile.

### Parameters
- `x` (`Double`): The x-coordinate of the point in the model (spatial/world) coordinate reference system (e.g., longitude).
- `y` (`Double`): The y-coordinate of the point in the model (spatial/world) coordinate reference system (e.g., latitude).

### Input
ADVANCED/LOW-LEVEL: Requires an instantiated `ITile[T]` (e.g., extracted via `rasterRDD.first()`). The caller owns the extraction of the tile and its `RasterMetadata`.

### Output
Returns `Boolean` — `true` if the pixel containing the spatial (x, y) location is empty (matches the dataset's fill value or has no data), `false` otherwise.

### Valid Call Patterns
```scala
import edu.ucr.cs.bdlab.beast.geolite.ITile
import edu.ucr.cs.bdlab.beast.geolite.RasterMetadata

// Caller-owned low-level extraction from an existing rasterRDD
val tile: ITile[_] = rasterRDD.first()
val meta: RasterMetadata = tile.rasterMetadata

// Transform grid coordinates (meta.x1, meta.y1) to MODEL (spatial) coordinates using g2m
val modelCoords = new Array[Double](2)
meta.g2m.transform(Array(meta.x1.toDouble, meta.y1.toDouble), 0, modelCoords, 0, 1)

// Check if the pixel at the spatial location is empty.
// Do not assert the boolean result, as the exact raster content is unknown.
val isNoData: Boolean = tile.isEmptyAt(modelCoords(0), modelCoords(1))
```

### LLM Instruction Prompt
When using `ITile.isEmptyAt(x, y)`, `x` and `y` MUST be model (spatial) coordinates. Never pass `RasterMetadata` properties `x1`, `x2`, `y1`, `y2` directly to `isEmptyAt`, as they are grid (pixel) coordinates. Convert grid to model via `rasterMetadata.g2m.transform` before calling. Do not add `assert(false)` or attempt to assert the exact boolean result of `isEmptyAt`, as the raster content is unknown; simply assign the result to a variable to verify it runs.

### Prompt Snippet
`tile.isEmptyAt(x, y)` requires spatial (model) coordinates. Convert grid bounds (`meta.x1`, `meta.y1`) to model via `meta.g2m.transform` before calling. Do not assert the exact boolean result (`true`/`false`) of `isEmptyAt`, as the underlying raster pixel value is unknown.

### Common Failure Modes
- **`AssertionError`:** Caused by attempting to assert the exact boolean result (e.g., `assert(isNoData == true)` or `assert(false)`). The test harness operates on an arbitrary `rasterRDD` fixture, so the actual pixel value is unknown. Simply assign the result to a variable.
- **`ArrayIndexOutOfBoundsException` (e.g., `-24799264`):** Caused by passing `RasterMetadata` properties `x1`, `x2`, `y1`, or `y2` directly to `isEmptyAt`. These are grid coordinates. `isEmptyAt` expects model coordinates and applies an inverse `modelToGrid` transform, yielding wildly out-of-bounds pixel indices.
- **ADVANCED/LOW-LEVEL API Misuse:** Attempting to use this for standard raster operations instead of RDD/DataFrame level transformations. Exclude from main user-facing denominator.

### Fix Code Hint
```scala
// WRONG: Asserting the unknown result or passing grid coordinates directly
val tile = rasterRDD.first()
val meta = tile.rasterMetadata
val isNoData = tile.isEmptyAt(meta.x1, meta.y1) // Throws ArrayIndexOutOfBoundsException
assert(isNoData == false) // Throws AssertionError because pixel content is unknown

// CORRECT: Transform grid to model coordinates first, and do not assert the result
val tile = rasterRDD.first()
val meta = tile.rasterMetadata
val modelCoords = new Array[Double](2)
meta.g2m.transform(Array(meta.x1.toDouble, meta.y1.toDouble), 0, modelCoords, 0, 1)
val isNoData = tile.isEmptyAt(modelCoords(0), modelCoords(1)) // Just assign to verify it runs
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
Evaluates whether a SpatialRDD is distributed across the Spark cluster using a specialized spatial partitioner (such as R*-Grove, Grid, KDTree, or STR).

### Parameters
- `rdd` (`JavaSpatialRDD`): The Java-based spatial RDD to evaluate (applicable only to the Java API overload; the Scala API operates as a parameterless extension method on the RDD).

### Input
A loaded spatial RDD (e.g., vector features loaded via `sc.shapefile`, `sc.geojsonFile`, or `sc.readCSVPoint`). The RDD does not need to be partitioned to call this method, as its purpose is to check that exact state.

### Output
Returns `Boolean` — `true` if the RDD is currently partitioned using any spatial partitioner, and `false` if it has default Spark partitioning or no spatial partitioner attached.

### Valid Call Patterns
```scala
// Inferred from signature (Scala extension method)
val isPartitioned: Boolean = features.isSpatiallyPartitioned

// Inferred from signature (Java API overload)
val isPartitionedJava: Boolean = JavaSpatialRDDHelper.isSpatiallyPartitioned(javaRdd)
```

### LLM Instruction Prompt
- Use `isSpatiallyPartitioned` to verify the partitioning state of a dataset before executing distributed spatial joins. 
- Enforce spatial join preconditions: The Distributed Join (`DJ`) algorithm requires *both* datasets to return `true` for `isSpatiallyPartitioned`. The Repartition Join (`REPJ`) requires at least *one* dataset to return `true`.
- If a dataset is not spatially partitioned, apply `rdd.spatialPartition(classOf[RSGrovePartitioner])` (or another valid partitioner) before joining.

### Prompt Snippet
```text
Check `rdd.isSpatiallyPartitioned` before performing spatial joins. If using `ESJDistributedAlgorithm.DJ`, both RDDs must be spatially partitioned. If false, partition the data using `rdd.spatialPartition(classOf[RSGrovePartitioner])` first.
```

### Common Failure Modes
- **Algorithm Precondition Violation:** Forcing the `DJ` (Distributed Join) algorithm on datasets where `isSpatiallyPartitioned` is `false`. This violates the algorithm's requirement that both datasets be spatially partitioned first.
- **Assuming Implicit Partitioning:** Assuming an RDD is spatially partitioned simply because it contains spatial data or was loaded from a spatial file format. Spatial partitioning must be explicitly triggered.

### Fix Code Hint
```scala
// Check and partition if necessary before a DJ spatial join
val preparedFeatures = if (!features.isSpatiallyPartitioned) {
  features.spatialPartition(classOf[RSGrovePartitioner])
} else {
  features
}
```

## API Test: `lastNFiles`

### Signature
```scala
def lastNFiles(fs: FileSystem, path: Path, n: Int): Array[(String, Long, Long)]
```
_Source: beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/util/ZipUtil.scala:48_

_Source doc:_ Returns information about the last n files in the archive. **Compatibility Note**: This method is not guaranteed to return the correct answer. For efficiency, it tries to locate the directory entries from the end using the ZIP signature. In rare cases, it might retrieve false information since the signature might appear out of coincidence. To be accurate, this method has to read all ZIP entries until it finds the last ones because directory entries are variable size in ZIP. @param fs the file system that contains the ZIP archive @param path the path to the ZIP file @param n the number of entries to retrieve from the end @return file names, offsets, and lengths for the last n entries if the ZIP file contains at least n entries. Otherwise, it returns all entries in the file.

### Goal
Retrieves the file names, byte offsets, and lengths of the last `n` entries in a ZIP archive (such as a compressed shapefile) by efficiently scanning from the end of the file.

### Parameters
- `fs` (`FileSystem`): The Hadoop `FileSystem` instance that contains the target ZIP archive.
- `path` (`Path`): The Hadoop `Path` pointing to the ZIP or ZIP64 file.
- `n` (`Int`): The number of file entries to retrieve from the end of the archive.

### Input
A valid ZIP or ZIP64 archive (e.g., a compressed Esri Shapefile) accessible via the provided Hadoop `FileSystem`. The file must exist and be readable. 

### Output
Returns `Array[(String, Long, Long)]` — an array of tuples where each tuple contains `(fileName, offset, length)` for the last `n` entries. If the ZIP file contains fewer than `n` entries, it returns all entries in the file.

### Valid Call Patterns
```scala
import org.apache.hadoop.fs.{FileSystem, Path}
import org.apache.hadoop.conf.Configuration
import edu.ucr.cs.bdlab.beast.util.ZipUtil

val fileSystem = FileSystem.getLocal(new Configuration())
val zipPath = new Path("data/ne_10m_admin_0_countries.zip")

// Retrieve the last 2 files in the ZIP archive
val lastFiles: Array[(String, Long, Long)] = ZipUtil.lastNFiles(fileSystem, zipPath, 2)

// Accessing the results
val fileName = lastFiles(0)._1
val offset = lastFiles(0)._2
val length = lastFiles(0)._3
```

### LLM Instruction Prompt
- Call `ZipUtil.lastNFiles(fs, path, n)` to quickly inspect the tail entries of a ZIP archive without scanning the entire file.
- **Warning:** Document that this method uses a heuristic (searching for the ZIP signature from the end of the file) for efficiency. It is not 100% guaranteed to be accurate, as the signature bytes could theoretically appear by coincidence within compressed data.
- Use the returned `offset` (`_2`) and `length` (`_3`) to seek and read specific files directly from the `FileSystem` input stream.

### Prompt Snippet
```text
`ZipUtil.lastNFiles(fs: FileSystem, path: Path, n: Int): Array[(String, Long, Long)]` efficiently gets the (name, offset, length) of the last `n` files in a ZIP. Note: Uses a heuristic signature scan from the end; rarely, coincidental byte matches may yield false info.
```

### Common Failure Modes
- **False Positives (Heuristic Failure):** Because the method scans backwards for the ZIP directory signature to save time, it might accidentally match identical byte sequences occurring naturally inside the compressed data, returning corrupted or incorrect file offsets.
- **File Not Found:** Providing a `Path` that does not exist on the specified `FileSystem` will throw an exception when the method attempts to open the file.

### Fix Code Hint
```scala
// To safely read the extracted file data using the returned offset and length:
val in = fileSystem.open(zipPath)
try {
  val targetFile = lastFiles(0)
  in.seek(targetFile._2) // Seek to the offset
  val data = new Array[Byte](targetFile._3.toInt) // Allocate array of 'length' size
  in.readFully(data)
  // Process 'data' bytes here
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
Lists all files contained within a ZIP archive (including ZIP64) on a Hadoop `FileSystem`, returning their names, byte offsets, and sizes to enable direct random-access reading without full extraction.

### Parameters
- `fileSystem` (`fs.FileSystem`): The Hadoop `FileSystem` instance (e.g., `FileSystem.getLocal(new Configuration())`) that hosts the target ZIP file.
- `zipFilePath` (`Path`): The Hadoop `Path` pointing to the ZIP file whose contents are to be listed.

### Input
A valid ZIP or ZIP64 archive file (such as a compressed Esri Shapefile archive) accessible via the provided Hadoop `FileSystem`. The caller must provide Hadoop-native `FileSystem` and `Path` objects, not standard `java.io.File` or `String` paths.

### Output
Returns `Array[(String, Long, Long)]` — An array of tuples where each tuple represents a file inside the archive. The tuple elements are:
1. `_1` (`String`): The name of the file inside the ZIP.
2. `_2` (`Long`): The starting byte offset of the file's data within the ZIP archive (useful for `FSDataInputStream.seek()`).
3. `_3` (`Long`): The uncompressed size of the file in bytes.

### Valid Call Patterns
```scala
import org.apache.hadoop.fs.{FileSystem, Path}
import org.apache.hadoop.conf.Configuration
import edu.ucr.cs.bdlab.beast.util.ZipUtil

// 1. Initialize FileSystem and Path
val fileSystem = FileSystem.getLocal(new Configuration())
val zipPath = new Path("/path/to/shapefile_archive.zip")

// 2. List files in the ZIP
val contents: Array[(String, Long, Long)] = ZipUtil.listFilesInZip(fileSystem, zipPath)

// 3. Example: Random-access read of a specific file using offset and size
val firstFile = contents.head
val fileName = firstFile._1
val byteOffset = firstFile._2
val byteSize = firstFile._3

val in = fileSystem.open(zipPath)
in.seek(byteOffset)
val data = new Array[Byte](byteSize.toInt)
in.readFully(data)
in.close()
```

### LLM Instruction Prompt
- Call `ZipUtil.listFilesInZip(fileSystem, path)` as a static utility method on `ZipUtil`.
- Remember the return type is an array of tuples: `(String, Long, Long)` mapping to `(filename, byteOffset, byteSize)`.
- Do not invent a `java.io.File` or `String` overload; the method strictly requires a Hadoop `Path` and `FileSystem`.
- When using the returned `byteSize` (the third tuple element) to allocate an in-memory `Array[Byte]`, you must cast it to an integer using `.toInt`.

### Prompt Snippet
```text
edu.ucr.cs.bdlab.beast.util.ZipUtil.listFilesInZip(fileSystem: org.apache.hadoop.fs.FileSystem, zipFilePath: org.apache.hadoop.fs.Path): Array[(String, Long, Long)] // Returns array of (filename, byteOffset, byteSize)
```

### Common Failure Modes
- **Type Mismatch on Path:** Passing a `java.io.File` or a `String` instead of an `org.apache.hadoop.fs.Path`.
- **Type Mismatch on Array Allocation:** Attempting to use the returned file size (`Long`) directly to initialize a Scala `Array[Byte]`, which requires an `Int`.
- **Missing Object Qualifier:** Calling `listFilesInZip(...)` as a bare function instead of qualifying it with `ZipUtil`.

### Fix Code Hint
```scala
// WRONG: ZipUtil.listFilesInZip(fs, "/path/to/file.zip")
// WRONG: val data = new Array[Byte](contents(0)._3) // _3 is a Long

// CORRECT:
val zipPath = new Path("/path/to/file.zip")
val contents = ZipUtil.listFilesInZip(fileSystem, zipPath)
val data = new Array[Byte](contents(0)._3.toInt) // Cast Long to Int for array size
```

## API Test: `makeBoxes`

### Signature
```scala
def makeBoxes(maxSize: Int*): JavaSpatialGeneratorBuilder
def makeBoxes(maxSize: Double*): SpatialGeneratorBuilder
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/generator/JavaSpatialGeneratorBuilder.scala:76  (+1 more definition site/overload)_

_Source doc:_ Generate boxes around each generated point. The size is measured as a fraction [0, 1] to indicate the ratio of the dataset bounding box. Any value above 1.0 is invalid. @param maxSize the maximum size for each side length of the generated box @return this generator builder

### Goal
Configure a spatial data generator to produce bounding boxes (envelopes) around generated points, typically used for benchmarking spatial joins or indexing.

### Parameters
- `maxSize` (`Int*` or `Double*`): The maximum size for each side length of the generated box. This is measured as a fraction `[0.0, 1.0]` indicating the ratio of the dataset's total bounding box. Any value above `1.0` is invalid. Multiple values can be provided for multi-dimensional boxes (e.g., width and height).

### Input
A `SpatialGeneratorBuilder` or `JavaSpatialGeneratorBuilder` instance, typically initialized via the SparkContext extension `sc.generateSpatialData`. No external files or datasets are required, as this is a synthetic data generation API.

### Output
Returns `SpatialGeneratorBuilder` (or `JavaSpatialGeneratorBuilder`), allowing method chaining to finalize the generation process (e.g., by calling `.uniform(N)` to generate an RDD of spatial features).

### Valid Call Patterns
```scala
// Generate 1,000,000 boxes with max width 30% and max height 40% of the total MBR
val boxesRDD = sparkContext.generateSpatialData
  .makeBoxes(0.3, 0.4)
  .uniform(1000000)

// Generate 100 boxes and plot them to an image
sc.generateSpatialData
  .makeBoxes(0.1, 0.2)
  .uniform(100)
  .plotImage(300, 300, "uniform.png")
```

### LLM Instruction Prompt
- Use `makeBoxes` on a `SpatialGeneratorBuilder` (via `sc.generateSpatialData`) when you need to generate synthetic polygon/envelope data for benchmarking.
- You MUST provide `maxSize` as a fraction between `0.0` and `1.0`. Do not provide absolute map units.
- You MUST chain a terminal generation method like `.uniform(numRecords)` after `makeBoxes` to actually produce the `SpatialRDD`.

### Prompt Snippet
```text
To generate synthetic bounding boxes in Beast, use `sc.generateSpatialData.makeBoxes(widthFraction, heightFraction).uniform(numRecords)`. The `maxSize` arguments must be fractions between 0.0 and 1.0 representing the ratio of the total bounding box. Values > 1.0 are invalid.
```

### Common Failure Modes
- **Invalid Size Fraction:** Passing a `maxSize` value greater than `1.0` (e.g., passing absolute map units like `1000.0` instead of a fraction like `0.1`). This violates the `[0, 1]` constraint and is invalid.
- **Missing Terminal Operation:** Calling `makeBoxes` but forgetting to call a generation method like `.uniform(N)`, resulting in a builder object instead of an actual `SpatialRDD`.

### Fix Code Hint
```scala
// ❌ BAD: Passing absolute sizes (> 1.0) and forgetting the terminal generation call
val badBoxes = sc.generateSpatialData.makeBoxes(500.0, 500.0)

// ✅ GOOD: Passing fractions [0, 1] and chaining .uniform(N) to create the RDD
val goodBoxes = sc.generateSpatialData
  .makeBoxes(0.05, 0.05)
  .uniform(10000)
```

## API Test: `mapPixels`
_Grounding: doc-repaired from source (docfix)._

### Goal
Apply a user-defined function to every pixel in a distributed raster dataset (e.g., for band math, unit conversion, or thresholding) to produce a new raster with transformed values. This is a core user-facing transformation included in the main user-facing denominator.

### Valid Call Patterns
```scala
import edu.ucr.cs.bdlab.raptor.RasterOperationsLocal
import edu.ucr.cs.bdlab.beast.cg.SpatialDataTypes.RasterRDD

// The test harness provides a multiband raster at runtime where T is Array[Float]
val outputRaster = RasterOperationsLocal.mapPixels(rasterRDD, (x: Array[Float]) => x.map(_ * 2.0f))

val tileCount = outputRaster.count()
if (tileCount > 0) {
  val firstTile = outputRaster.first()
  // Verify the per-pixel math using the ITile API
  val pixelValue = firstTile.getPixelValue(0, 0)
}

println(s"__CHECK__ mapPixels ${tileCount}")
```

### LLM Instruction Prompt
- Use `RasterOperationsLocal.mapPixels` for per-pixel mathematical transformations.
- The test harness provides a multiband raster at runtime, meaning the pixel type `T` is `Array[Float]`, not a single `Float`.
- The lambda function `f` passed to `mapPixels` must accept `Array[Float]` (e.g., `(x: Array[Float]) => x.map(_ * 2.0f)`) to match the runtime data type and avoid a `ClassCastException`.
- To verify the transformation in memory, retrieve a tile using `.first()` and call `getPixelValue(x, y)` on it.
- Spark requires `ClassTag` bounds for `T` and `U` to serialize the resulting RDD.

### Prompt Snippet
To perform pixel-level math on a RasterRDD, use `RasterOperationsLocal.mapPixels(rasterRDD, f: T => U)`. The harness provides a multiband raster, so `T` is `Array[Float]`. Your lambda must accept `Array[Float]` (e.g., `(x: Array[Float]) => x.map(_ * 2.0f)`). To verify results in memory, retrieve a tile (`raster.first()`) and use `tile.getPixelValue(x, y)`.

### Common Failure Modes
- **ClassCastException (`[F cannot be cast to java.lang.Float`):** Occurs when assuming the harness provides a single-band `RasterRDD[Float]` and passing a `Float => Float` lambda. The harness actually provides a multiband raster where `T` is `Array[Float]` (represented as `[F` in the JVM). The lambda must accept `Array[Float]`.
- **In-Memory Verification Failure (AssertionError):** Test generation aborts if you do not inspect actual pixel values. You must use `ITile.getPixelValue(x, y)` on a materialized tile (e.g., from `.first()`) to assert the correctness of the per-pixel math.
- **Missing ClassTags:** If wrapping `mapPixels` in a generic helper function, failing to provide `[T: ClassTag, U: ClassTag]` context bounds will cause compilation errors because Spark requires ClassTags to serialize the resulting RDD.

### Fix Code Hint
```scala
// BAD: Assumes single-band Float, throws ClassCastException: [F cannot be cast to java.lang.Float
val outputRaster = RasterOperationsLocal.mapPixels(rasterRDD, (x: Float) => x * 2.0f)
if (outputRaster.count() > 0) {
  val firstTile = outputRaster.first()
  val pixelValue = firstTile.getPixelValue(0, 0).asInstanceOf[Float] // Fails
}

// GOOD: Handles multiband Array[Float] provided by the harness at runtime
val outputRaster = RasterOperationsLocal.mapPixels(rasterRDD, (x: Array[Float]) => x.map(_ * 2.0f))
if (outputRaster.count() > 0) {
  val firstTile = outputRaster.first()
  val pixelValue = firstTile.getPixelValue(0, 0)
}
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
Sets the bounding box (Minimum Bounding Rectangle) for generating synthetic spatial data using Beast's distributed Spatial Data Generator (Spider).

### Parameters
- `mbr` (`EnvelopeNDLite`): The bounding box defining the spatial extent within which the synthetic data will be generated. Typically constructed with `new EnvelopeNDLite(dimensions, minX, minY, maxX, maxY)`.

### Input
Requires an active `SparkContext` to initialize the `SpatialGeneratorBuilder` (either via the context extension `sc.generateSpatialData` or `new SpatialGeneratorBuilder(sc)`). The caller must provide a valid `EnvelopeNDLite` representing the desired spatial boundaries.

### Output
Returns `SpatialGeneratorBuilder` — a builder object that allows chaining further configuration (e.g., `.config(...)`) before finalizing the generation with a distribution method (e.g., `.uniform(numRecords)`), which ultimately yields a `SpatialRDD`. The parameterless overloads (`def mbr: EnvelopeNDLite`) act as getters returning the currently set bounding box.

### Valid Call Patterns
```scala
// Pattern 1: Using the SparkContext extension (from README)
val generatedData = sparkContext.generateSpatialData
  .mbr(new EnvelopeNDLite(2, 1.0, 0.0, 4.0, 8.0))
  .uniform(1000)

// Pattern 2: Using the builder constructor directly with configurations (from test suite)
val desiredMBR = new EnvelopeNDLite(2, 2.0, 3.0, 9.0, 8.0)
val randomPoints: SpatialRDD = new SpatialGeneratorBuilder(sparkContext)
  .mbr(desiredMBR)
  .config(UniformDistribution.MaxSize, "0.2,0.1")
  .config(UniformDistribution.NumSegments, 10)
  .config(UniformDistribution.GeometryType, "box")
  .config(SpatialGenerator.Seed, 1794)
  .uniform(10)
```

### LLM Instruction Prompt
- Use `mbr(EnvelopeNDLite)` on a `SpatialGeneratorBuilder` to restrict the spatial extent of generated benchmarking data.
- Always chain this method with a terminal generation action, such as `.uniform(n)`, to actually produce the `SpatialRDD`.
- Construct the `EnvelopeNDLite` using the signature `new EnvelopeNDLite(dimensions, minX, minY, maxX, maxY)`.

### Prompt Snippet
```text
To generate synthetic spatial data within a specific bounding box in Beast, use `sc.generateSpatialData.mbr(new EnvelopeNDLite(2, minX, minY, maxX, maxY))`. You must chain this with a distribution method like `.uniform(numRecords)` to return the actual RDD.
```

### Common Failure Modes
- **Missing Terminal Operation:** Calling `.mbr(...)` without subsequently calling `.uniform(...)` or another distribution method. This leaves the user with a `SpatialGeneratorBuilder` instead of the expected `SpatialRDD` (or `RDD[IFeature]`), causing type mismatch errors in downstream spatial operations.
- **Invalid Envelope Bounds:** Providing an `EnvelopeNDLite` where the minimum bounds exceed the maximum bounds, which can result in empty generated datasets or runtime exceptions during the generation phase.

### Fix Code Hint
```scala
// WRONG: Leaves the builder un-materialized
val badData = sparkContext.generateSpatialData.mbr(new EnvelopeNDLite(2, 0, 0, 10, 10))

// RIGHT: Chains a distribution method to generate the RDD
val goodData = sparkContext.generateSpatialData
  .mbr(new EnvelopeNDLite(2, 0.0, 0.0, 10.0, 10.0))
  .uniform(10000) // Generates 10,000 features
```

## API Test: `mergeWith`

### Signature
```scala
def mergeWith(another: VectorCanvas): VectorCanvas
def mergeWith(opts: BeastOptions): BeastOptions
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/VectorCanvas.scala:440  (+1 more definition site/overload)_

_Source doc:_ Merges this canvas with another vector canvas and returns this canvas after the merge. @param another the other canvas to merge with @return this canvas after the merge so that you can chain a number of mergeWidth operations.

### Goal
Merges the geometries and state of another `VectorCanvas` (or `BeastOptions`) into the current instance, returning the updated instance to allow for fluent method chaining during geospatial visualization or configuration tasks.

### Parameters
- `another` (`VectorCanvas`): The secondary vector canvas whose geometries will be merged into the calling canvas.
- `opts` (`BeastOptions`): *(Overload)* Another set of Beast configuration options to merge into the current options.

### Input
- Two initialized `VectorCanvas` objects containing vector geometries (e.g., points, lines, polygons) added via `addGeometry`.
- **Preconditions:** Both canvases should typically share the same spatial `Envelope` and pixel dimensions (width/height) to ensure that geometries from the second canvas align correctly in the merged coordinate space.

### Output
Returns `VectorCanvas` (or `BeastOptions` for the overload) — The original calling instance, mutated in-place to include the contents of the `another` parameter.

### Valid Call Patterns
```scala
import org.locationtech.jts.geom.{Envelope, CoordinateXY}
import edu.ucr.cs.bdlab.beast.geolite.GeometryReader

// Initialize two canvases with identical envelopes and dimensions
val env = new Envelope(0, 1, 0, 1)
val canvas1 = new VectorCanvas(env, 10, 10, 0, 1)
val canvas2 = new VectorCanvas(env, 10, 10, 0, 1)

val factory = GeometryReader.DefaultGeometryFactory

// Add geometries to both canvases
canvas1.addGeometry(factory.createPoint(new CoordinateXY(0, 0)), null)
canvas1.addGeometry(factory.createPoint(new CoordinateXY(0.1, 0.1)), null)

canvas2.addGeometry(factory.createPoint(new CoordinateXY(0.2, 0.2)), null)
canvas2.addGeometry(factory.createPoint(new CoordinateXY(0.3, 0.3)), null)

// Merge canvas2 into canvas1
canvas1.mergeWith(canvas2)
// canvas1 now contains 4 geometries
```

### LLM Instruction Prompt
- Use `mergeWith` to combine two `VectorCanvas` instances during visualization tasks, or to combine two `BeastOptions` configuration objects.
- Remember that `mergeWith` mutates the calling object in-place and returns it.
- When merging `VectorCanvas` objects, ensure both canvases were initialized with the same spatial `Envelope` and pixel dimensions so that the merged geometries share a consistent coordinate space.

### Prompt Snippet
```text
To combine two VectorCanvas objects in Beast's visualization API, use `canvas1.mergeWith(canvas2)`. This mutates `canvas1` by appending `canvas2`'s geometries and returns `canvas1` to allow for method chaining. Ensure both canvases share the same Envelope.
```

### Common Failure Modes
- **Mismatched Envelopes/Dimensions:** Merging canvases that were initialized with different spatial envelopes or pixel dimensions. Because `mergeWith` does not re-project or re-scale geometries that have already been converted to pixel space, the merged geometries will be misaligned.
- **Null Arguments:** Passing `null` instead of a valid `VectorCanvas` or `BeastOptions` object will result in a `NullPointerException`.

### Fix Code Hint
```scala
// Ensure both canvases share the exact same spatial envelope and resolution before merging
val sharedEnvelope = new Envelope(0, 256, 0, 256)
val canvas1 = new VectorCanvas(sharedEnvelope, 256, 256, 0, 1)
val canvas2 = new VectorCanvas(sharedEnvelope, 256, 256, 0, 1)

// ... add geometries ...

// Safe to merge
val mergedCanvas = canvas1.mergeWith(canvas2)
```

## API Test: `mergeZip`

### Signature
```scala
def mergeZip(fileSystem: fs.FileSystem, mergedFile: Path, @varargs zipFiles: Path*): Unit
```
_Source: beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/util/ZipUtil.scala:425_

_Source doc:_ Merges multiple ZIP files into one and deletes the input files. @param mergedFile the output file that contains the merged ZIP files @param zipFiles the input files to be merged

### Goal
Merges multiple ZIP archives (such as distributed outputs for multilevel image pyramids or MVT vector tiles) into a single ZIP file and permanently deletes the original input files.

### Parameters
- `fileSystem` (`fs.FileSystem`): The Hadoop `FileSystem` instance used to resolve and access the file paths (e.g., `FileSystem.getLocal(new Configuration())` or an HDFS file system).
- `mergedFile` (`Path`): The Hadoop `Path` representing the destination output ZIP file that will contain all merged entries.
- `@varargs zipFiles` (`Path*`): A variable-length list of Hadoop `Path` objects representing the input ZIP files to be merged.

### Input
Valid, existing ZIP files located on the provided Hadoop `FileSystem`. The caller must have read access to the input files, write access to the destination directory, and delete permissions for the input files' directories (as the inputs are deleted upon successful merging).

### Output
Returns `Unit` — the operation is performed entirely for its side effects: creating the new merged ZIP file at `mergedFile` and deleting all provided `zipFiles`.

### Valid Call Patterns
```scala
import org.apache.hadoop.fs.{FileSystem, Path}
import org.apache.hadoop.conf.Configuration
import edu.ucr.cs.bdlab.beast.util.ZipUtil

// Initialize the Hadoop FileSystem (local or HDFS depending on environment)
val fileSystem = FileSystem.getLocal(new Configuration())

// Define Hadoop Paths for inputs and output
val file1 = new Path("scratch/test1.zip")
val file2 = new Path("scratch/test2.zip")
val mergedFile = new Path("scratch/merged_output.zip")

// Merge the ZIPs (file1 and file2 will be deleted)
ZipUtil.mergeZip(fileSystem, mergedFile, file1, file2)
```

### LLM Instruction Prompt
- Always call `mergeZip` on the `ZipUtil` object (`ZipUtil.mergeZip(...)`).
- You MUST pass Hadoop `Path` objects for the file arguments, not plain Scala `String` paths.
- You MUST provide a valid Hadoop `FileSystem` instance as the first argument.
- Warn the user that this function is destructive to the inputs: it automatically deletes the input ZIP files after merging them. Do not write code that attempts to read the input files after this call.

### Prompt Snippet
```text
Use `ZipUtil.mergeZip(fileSystem, mergedFile, zipFiles*)` to combine multiple ZIP archives into one. Inputs and outputs must be Hadoop `Path` objects, not strings. Warning: Input files are permanently deleted after merging.
```

### Common Failure Modes
- **Type Mismatch on Paths:** Passing standard `String` file paths instead of Hadoop `Path` objects, causing a compilation error.
- **File Not Found (Post-Execution):** Attempting to access or move the input `zipFiles` after calling `mergeZip`. The function deletes them automatically; subsequent operations on the inputs will throw a `FileNotFoundException`.
- **Missing Permissions:** The Spark/Hadoop user lacks the necessary filesystem permissions to delete the input files, causing the job to crash during the cleanup phase.

### Fix Code Hint
```scala
// WRONG: Passing strings instead of Hadoop Paths
// ZipUtil.mergeZip(fileSystem, "merged.zip", "part1.zip", "part2.zip")

// RIGHT: Wrapping paths in org.apache.hadoop.fs.Path
ZipUtil.mergeZip(fileSystem, new Path("merged.zip"), new Path("part1.zip"), new Path("part2.zip"))
```

## API Test: `metadata`

### Signature
```scala
def metadata: RasterMetadata
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/GeoTiffReader.scala:165  (+2 more definition site/overload)_

### Goal
Retrieves the spatial metadata (dimensions, resolution, and coordinate reference system properties) of an opened raster file.

### Parameters
_None._

### Input
An initialized raster reader instance (such as `GeoTiffReader[T]`) that has successfully opened a valid raster file (e.g., GeoTIFF). The reader must be initialized via `reader.initialize(...)` before accessing its metadata.

### Output
Returns `RasterMetadata` — an object representing the raster's spatial properties. It provides access to dimensions (`rasterWidth`, `rasterHeight`), pixel scale (`getPixelScaleX`), and utility methods for coordinate transformations (`gridToModel`, `modelToGrid`) and tile lookups (`getTileIDAtPoint`, `getTileIDAtPixel`).

### Valid Call Patterns
```scala
import org.apache.hadoop.fs.Path
import org.apache.hadoop.conf.Configuration
import edu.ucr.cs.bdlab.raptor.GeoTiffReader
import edu.ucr.cs.bdlab.beast.common.BeastOptions
import java.awt.geom.Point2D

val rasterPath = new Path("path/to/raster.tif")
val fileSystem = rasterPath.getFileSystem(new Configuration())
val reader = new GeoTiffReader[Int] // Type must match runtime pixel type

try {
  // Reader must be initialized before accessing metadata
  reader.initialize(fileSystem, rasterPath.toString, "0", new BeastOptions())
  
  // Access basic metadata properties
  val width = reader.metadata.rasterWidth
  val height = reader.metadata.rasterHeight
  val scaleX = reader.metadata.getPixelScaleX
  
  // Transform origin point from raster grid (pixels) to vector model (coordinates)
  val outPoint = new Point2D.Double
  reader.metadata.gridToModel(0, 0, outPoint)
  
  // Transform from vector model (coordinates) to raster grid (pixels)
  reader.metadata.modelToGrid(-6.679688, 53.613281, outPoint)
  
  // Look up tile IDs for Raptor processing
  val tileID = reader.metadata.getTileIDAtPoint(23.224, 32.415)
  val tile = reader.readTile(tileID)
} finally {
  reader.close()
}
```

### LLM Instruction Prompt
- Call `metadata` without parentheses on an initialized raster reader (e.g., `GeoTiffReader[T]`).
- Use the returned `RasterMetadata` object to access `rasterWidth`, `rasterHeight`, or to perform spatial transformations like `gridToModel(x, y, outPoint)` and `modelToGrid(x, y, outPoint)`.
- Never access `metadata` before calling `initialize()` on the reader.

### Prompt Snippet
```text
To get raster dimensions or perform pixel-to-coordinate transformations, access the `metadata` property on an initialized `GeoTiffReader`. Do not use parentheses. You can use `metadata.gridToModel` and `metadata.modelToGrid` with a `java.awt.geom.Point2D.Double` to translate between pixel indices and spatial coordinates.
```

### Common Failure Modes
- **NullPointerException / Uninitialized State:** Accessing `reader.metadata` before calling `reader.initialize(...)`. The reader must parse the file headers first.
- **Method Signature Error:** Calling `reader.metadata()` with parentheses. It is defined as a parameterless method (`def metadata: RasterMetadata`) and should be accessed without parentheses in idiomatic Scala.
- **Type Mismatch on Initialization:** Creating a `GeoTiffReader[T]` where `T` does not match the underlying GeoTIFF's runtime pixel type (e.g., using `[Int]` for a Float32 raster), which may cause failures when subsequently reading tiles based on the metadata.

### Fix Code Hint
```scala
// WRONG: Accessing metadata before initialization or using parentheses
val reader = new GeoTiffReader[Float]
val meta = reader.metadata() // Fails: parentheses not allowed
val w = reader.metadata.rasterWidth // Fails: reader not initialized

// CORRECT: Initialize first, then access without parentheses
val reader = new GeoTiffReader[Float]
reader.initialize(fileSystem, path, "0", new BeastOptions())
val w = reader.metadata.rasterWidth
```

## API Test: `modelToGrid`

### Signature
```scala
def modelToGrid(x: Double, y: Double, outPoint: Point2D.Double): Unit
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/RasterMetadata.scala:161_

_Source doc:_ Converts a point location from model (world) space to grid (pixel) space @param x the x-coordinate in the model space (e.g., longitude) @param y the y-coordinate in the model space (e.g., latitude) @param outPoint the output point that contains the grid coordinates

### Goal
Converts a geographic or projected coordinate (model/world space) into continuous pixel coordinates (grid space) based on the raster's affine transformation metadata.

### Parameters
- `x` (`Double`): The x-coordinate in the model space (e.g., longitude or projected X).
- `y` (`Double`): The y-coordinate in the model space (e.g., latitude or projected Y).
- `outPoint` (`Point2D.Double`): A pre-allocated `java.awt.geom.Point2D.Double` object that will be mutated in-place to store the resulting grid (pixel) coordinates.

### Input
Requires a valid `RasterMetadata` instance (typically accessed via `reader.metadata` from a `GeoTiffReader` or `HDF4Reader`) and a pre-allocated `Point2D.Double` object. The `x` and `y` coordinates must be in the exact Coordinate Reference System (CRS) and scale defined by the raster's model space.

### Output
Returns `Unit` — the function mutates the provided `outPoint` parameter. After the call, `outPoint.x` and `outPoint.y` will contain the continuous grid coordinates (column and row, respectively), which can be cast to integers to find the specific pixel index.

### Valid Call Patterns
```scala
import java.awt.geom.Point2D

// Assuming `reader` is an initialized GeoTiffReader or HDF4Reader
val outPoint = new Point2D.Double()

// Convert a known model coordinate (e.g., longitude, latitude) to grid space
reader.metadata.modelToGrid(-6.679688, 53.613281, outPoint)

// Extract the pixel column and row
val pixelX = outPoint.getX.toInt
val pixelY = outPoint.getY.toInt
```

### LLM Instruction Prompt
- When converting world coordinates to pixel coordinates using `modelToGrid`, you MUST pre-allocate a `java.awt.geom.Point2D.Double` and pass it as the third argument. 
- Do NOT assign the result of `modelToGrid` to a variable, as it returns `Unit`. Read the results directly from the mutated `Point2D.Double` object.
- The receiver is typically a `RasterMetadata` object (e.g., `reader.metadata.modelToGrid(...)`).

### Prompt Snippet
```text
To convert geographic coordinates to raster pixel coordinates in RDPro, pre-allocate a `java.awt.geom.Point2D.Double` and pass it to `metadata.modelToGrid(x, y, outPoint)`. The method returns `Unit` and mutates the point. Cast `outPoint.getX` and `outPoint.getY` to integers to get the pixel column and row.
```

### Common Failure Modes
- **Assigning the return value:** Attempting `val pt = metadata.modelToGrid(x, y, outPoint)` results in a `Unit` assignment, leading to compilation errors if `pt` is later used as a point.
- **Null Pointer Exception:** Passing `null` or an uninitialized variable for `outPoint` instead of explicitly calling `new Point2D.Double()`.
- **CRS Mismatch:** Passing raw latitude/longitude values when the raster's model space is actually in a projected coordinate system (e.g., Web Mercator), resulting in wildly out-of-bounds pixel coordinates.

### Fix Code Hint
```scala
// WRONG: Expecting a return value or missing the outPoint parameter
val gridPt = reader.metadata.modelToGrid(-110.0, 30.0)

// CORRECT: Pre-allocate the point and pass it to be mutated
val gridPt = new java.awt.geom.Point2D.Double()
reader.metadata.modelToGrid(-110.0, 30.0, gridPt)
val col = gridPt.getX.toInt
val row = gridPt.getY.toInt
```

## API Test: `normal`

### Signature
```scala
def normal(mu: Double, sigma: Double): Double
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/generator/SpatialGenerator.scala:40_

_Source doc:_ Generate a random number in the range (-inf, +inf) from a normal distribution

### Goal
Generate a random floating-point number from a normal (Gaussian) distribution, typically used within Beast's Spider component for generating synthetic spatial data or benchmarking datasets.

### Parameters
- `mu` (`Double`): The mean (center) of the normal distribution.
- `sigma` (`Double`): The standard deviation (spread or width) of the normal distribution.

### Input
Two `Double` values representing the statistical parameters of the desired normal distribution. The `sigma` (standard deviation) value should be non-negative. 

### Output
Returns `Double` — a randomly generated number drawn from the specified normal distribution, falling within the range (-inf, +inf).

### Valid Call Patterns
```scala
// Note: Call pattern inferred from signature (not verified by tests/README).
// The exact enclosing object (e.g., SpatialGenerator) is not specified in the source facts.
val randomValue = normal(0.0, 1.0) // Standard normal distribution
```

### LLM Instruction Prompt
- Use `normal(mu, sigma)` when generating synthetic spatial coordinates or random attributes that require a Gaussian distribution. Ensure `sigma` is non-negative. Because the exact enclosing object is unknown from the provided facts, assume it is available in the `SpatialGenerator` scope or requires an appropriate import.

### Prompt Snippet
```text
To generate a random number from a normal distribution for synthetic spatial data, use `normal(mu, sigma)` where `mu` is the mean and `sigma` is the standard deviation.
```

### Common Failure Modes
- **Scope/Resolution Errors:** Calling `normal` without the correct object qualifier or import (e.g., `SpatialGenerator.normal(...)`), resulting in a "not found" compilation error.
- **Invalid Statistical Parameters:** Providing a negative value for `sigma`, which is mathematically invalid for a standard deviation and may cause unexpected behavior or exceptions in the underlying random number generator.

### Fix Code Hint
```scala
// Ensure sigma is non-negative and the function is properly scoped/imported
val mean = 10.0
val stdDev = 2.5
require(stdDev >= 0, "Standard deviation must be non-negative")
val value = normal(mean, stdDev)
```

## API Test: `numFeatures`

### Signature
```scala
def numFeatures: Long
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/SpatialPartition.scala:32_

_Source doc:_ Total number of features (records) in this partition

### Goal
Retrieves the total number of spatial features (records) contained within a specific spatial partition or geometric summary object.

### Parameters
_None._

### Input
A valid `SpatialPartition` (representing a distributed subset of spatial data) or a `Summary` object (representing aggregated dataset statistics, such as those generated by `GeometricSummary.run`). 

### Output
Returns `Long` — the exact count of features (records) present in the partition or summary.

### Valid Call Patterns
```scala
// From the project's test suite: retrieving the feature count from a Summary object
val inputfile = locateResource("/test.partitions")
val opts = new BeastOptions().set("iformat", "wkt(Geometry)")
  .set("skipheader", true)
  .set("separator", "\t")

val summary = GeometricSummary.run(opts, Array(inputfile.getPath), null, sparkContext).asInstanceOf[Summary]
val count: Long = summary.numFeatures
```

### LLM Instruction Prompt
- Call `numFeatures` as a parameterless method (without parentheses) on a `SpatialPartition` or `Summary` object.
- Do not call `numFeatures` directly on a Spark `RDD` (use `.count()` for RDDs); `numFeatures` is specific to Beast's partition and summary metadata objects.

### Prompt Snippet
```text
To get the record count of a Beast spatial partition or summary object, use `value.numFeatures`. It returns a Long. Do not use parentheses.
```

### Common Failure Modes
- **Adding parentheses:** Calling `summary.numFeatures()` will cause a Scala compilation error because the method is defined without parentheses.
- **Calling on an RDD:** Attempting to call `rdd.numFeatures` on a `SpatialRDD` or `RasterRDD`. This method belongs to the underlying `SpatialPartition` or a computed `Summary` object, not the distributed collection itself.

### Fix Code Hint
```scala
// WRONG: val count = summary.numFeatures()
// WRONG: val count = spatialRDD.numFeatures

// RIGHT: val count = summary.numFeatures
// RIGHT: val count = partition.numFeatures
```

## API Test: `numFields`

### Signature
```scala
def numFields: Int
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/shapefilev2/DBFWriter.scala:42_

_Source doc:_ Number of attributes in the file

### Goal
Returns the total number of attributes (fields) present in a spatial feature or record.

### Parameters
_None._

### Input
A spatial feature or record object (e.g., an element yielded by a vector file reader such as `GPXReader2`, or an `IFeature` from a vector RDD).

### Output
Returns `Int` — The count of attributes/fields defined in the record's schema.

### Valid Call Patterns
```scala
// Example derived from the project's test suite (GPXReader2Test)
val input = getClass.getResourceAsStream("/001005279.gpx")
val gpxReader = new GPXReader2(input, "001005279.gpx")

for (r <- gpxReader) {
  // Get the number of attributes in the current record
  val fieldCount: Int = r.numFields
  println(s"Record has $fieldCount fields.")
}
```

### LLM Instruction Prompt
- Use `numFields` when you need to determine the number of attributes in a spatial record or feature (e.g., to validate schema size or iterate over available fields).
- Call it directly on the record instance without parentheses, as it is defined as a parameterless method (`def numFields: Int`).

### Prompt Snippet
```text
To get the number of attributes in a spatial feature or record `r`, use `r.numFields`. Do not use parentheses.
```

### Common Failure Modes
- **Adding parentheses:** Calling `r.numFields()` will cause a compilation error because the method is defined without parentheses in Scala.
- **Misinterpreting the count:** Assuming `numFields` returns the number of geometries or points in a trajectory. It returns the number of *tabular attributes/fields* (e.g., elevation, time, trackname) in the record.

### Fix Code Hint
```scala
// WRONG: Compilation error due to parentheses
val count = r.numFields()

// RIGHT: Parameterless method call
val count = r.numFields
```

## API Test: `numNonEmptyGeometries`

### Signature
```scala
def numNonEmptyGeometries: Long
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/SpatialPartition.scala:35_

_Source doc:_ Number of non-empty geometries in this partition

### Goal
Calculates the total number of valid, non-empty vector geometries present within a specific spatial partition.

### Parameters
_None._

### Input
An instance of `SpatialPartition` containing spatial features (e.g., points, lines, or polygons loaded from formats like Shapefile, GeoJSON, or WKT). 

### Output
Returns `Long` — the exact count of geometries in the partition that contain valid coordinate data (excluding empty geometries like `POLYGON EMPTY`).

### Valid Call Patterns
```scala
// Inferred from signature and sibling methods on SpatialPartition
val validGeometryCount: Long = partition.numNonEmptyGeometries
```

### LLM Instruction Prompt
- Call `numNonEmptyGeometries` directly on a `SpatialPartition` instance to count valid features.
- Do not append parentheses `()` as it is a parameterless method in Scala.
- Do not call this directly on an `RDD[IFeature]`; it is a partition-level property, not a distributed RDD action (like `count()`).

### Prompt Snippet
```text
When analyzing the contents of a `SpatialPartition` in Beast, use `partition.numNonEmptyGeometries` to retrieve the count of valid (non-empty) geometries within that specific partition.
```

### Common Failure Modes
- **Method Not Found on RDD:** Attempting to call `rdd.numNonEmptyGeometries` directly on a `SpatialRDD` or `RDD[IFeature]`. This method belongs to the underlying `SpatialPartition` objects, not the distributed collection.
- **Syntax Error (Parentheses):** Adding parentheses `numNonEmptyGeometries()` to the parameterless method call, which may cause compilation errors in Scala.

### Fix Code Hint
```scala
// WRONG: Calling on an RDD
// val count = spatialRDD.numNonEmptyGeometries

// WRONG: Using parentheses
// val count = partition.numNonEmptyGeometries()

// CORRECT: Calling on a SpatialPartition instance without parentheses
val count = partition.numNonEmptyGeometries
```

## API Test: `numPartitions`
_Grounding: doc-repaired from source (docfix)._

### Goal
Configures the number of partitions for the output RDD when generating synthetic spatial data. This is a lazy builder method on `SpatialGeneratorBuilder` that mutates internal state; it MUST be followed by a terminal generation method to materialize the `SpatialRDD`.

### Valid Call Patterns
```scala
import edu.ucr.cs.bdlab.beast._
import edu.ucr.cs.bdlab.beast.generator.SpatialGeneratorBuilder

// Obtain the builder, configure partitions, and call a terminal method to materialize
val generatedRDD = sc.generateSpatialData
  .numPartitions(12)
  .uniform(1000L) // Terminal method is REQUIRED to create the SpatialRDD

println(s"__CHECK__ numPartitions ${generatedRDD.getNumPartitions}")
```

### LLM Instruction Prompt
- `numPartitions` is a lazy builder method that returns the `SpatialGeneratorBuilder` itself.
- To materialize the `SpatialRDD` and apply the partition configuration, you MUST chain a terminal generation method such as `.uniform(cardinality)` or `.generate(cardinality)`.
- If the user does not specify a partition count, omit this call or pass `0` to rely on the default heuristic (1 partition per 1,000,000 records).
- Do not confuse this builder method `numPartitions(Int)` with the parameterless `numPartitions` property found on instantiated partitioners.

### Prompt Snippet
```scala
// Set partitions for generated spatial data and materialize with a terminal method
val generatedRDD = sc.generateSpatialData.numPartitions(12).uniform(1000L)
```

### Common Failure Modes
- **Missing Terminal Method:** `java.lang.AssertionError: assertion failed: ... missing terminal method to materialize the RDD.` Calling `sc.generateSpatialData.numPartitions(12)` without chaining `.uniform(cardinality)` or `.generate(cardinality)` returns a lazy builder, not a `SpatialRDD`. This violates test harnesses expecting a verifiable RDD.
- **Confusing Builder Method with Partitioner Property:** Attempting to call `numPartitions(Int)` on an instantiated `SpatialPartitioner` or `SpatialFileRDD`. Partitioners have a parameterless getter (`partitioner.numPartitions`), whereas this API is a builder method for data generation.

### Fix Code Hint
```scala
// WRONG: Stopping at the lazy builder method (produces no RDD, fails tests)
val builder = sc.generateSpatialData.numPartitions(12)

// RIGHT: Chaining a terminal method to materialize the SpatialRDD
val generatedRDD = sc.generateSpatialData.numPartitions(12).uniform(1000L)
```

## API Test: `numPoints`

### Signature
```scala
def numPoints: Int
def numPoints: Long
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/LiteGeometry.scala:22  (+4 more definition site/overload)_

### Goal
Calculates the total number of coordinate points (vertices) for a given geometry or collection of geometries.

### Parameters
_None._

### Input
A lightweight geometry object (e.g., `LiteLineString`, `LiteList`, or other `LiteGeometry` types) typically generated during vector tile processing, visualization, or geometry simplification.

### Output
Returns `Int` or `Long` — The total count of coordinate points that make up the geometry.

### Valid Call Patterns
```scala
// Example derived from Beast's IntermediateVectorTileTest
val interTile = new IntermediateVectorTile(10, 0)
val line = GeometryReader.DefaultGeometryFactory.createLineString(Array(
  new Coordinate(5, 5), new Coordinate(-5, 5), new Coordinate(-5, 6), new Coordinate(-5, 7),
  new Coordinate(-5, 15), new Coordinate(5, 8)
))

val simplifiedLine = interTile.simplifyGeometry(line)

// Call numPoints on the resulting geometry
val pointCount = simplifiedLine.numPoints
```

### LLM Instruction Prompt
- Use `.numPoints` (without parentheses) on lightweight geometry objects (like `LiteLineString` or `LiteList`) to retrieve the total vertex count.
- Always verify that the geometry object is not `null` before calling `.numPoints`. Operations like `simplifyGeometry` will return `null` if a geometry is completely outside a tile or simplified away, which will cause a `NullPointerException` if `.numPoints` is invoked directly.

### Prompt Snippet
```text
Use `geometry.numPoints` to get the total number of vertices (as an Int or Long) for a Beast LiteGeometry object. Always check for null if the geometry is the result of a simplification step.
```

### Common Failure Modes
- **`NullPointerException`**: Calling `.numPoints` on a geometry reference that is `null`. This frequently happens when processing vector tiles if a geometry (like a `LinearRing` or `LineString`) is completely outside the tile bounds and does not contain the tile, causing `simplifyGeometry` to return `null`.

### Fix Code Hint
```scala
// Safely check for null before accessing numPoints
val simplifiedLine = interTile.simplifyGeometry(line)
val pointCount = if (simplifiedLine != null) simplifiedLine.numPoints else 0
```

## API Test: `numTiles`

### Signature
```scala
def numTiles: Int
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/RasterMetadata.scala:61_

_Source doc:_ Total number of tiles in the raster layer

### Goal
Retrieves the total number of tiles that make up the raster layer from its metadata.

### Parameters
_None._

### Input
A valid `RasterMetadata` object, typically accessed via a raster reader's `.metadata` property (e.g., `HDF4Reader.metadata`) after the reader has been properly initialized with a file system, path, and options.

### Output
Returns `Int` — The total count of tiles present in the raster layer.

### Valid Call Patterns
```scala
val reader = new HDF4Reader
reader.initialize(fileSystem, hdfFile.toString, "water_mask", new BeastOptions())
val totalTiles: Int = reader.metadata.numTiles
```

### LLM Instruction Prompt
- Call `numTiles` as a parameterless property on a `RasterMetadata` instance (e.g., `reader.metadata.numTiles`).
- Do not append parentheses `()`.
- Ensure the underlying reader or metadata source is fully initialized before accessing this property.

### Prompt Snippet
```text
val totalTiles = reader.metadata.numTiles
```

### Common Failure Modes
- **Syntax Error (Parentheses):** Calling `numTiles()` with parentheses will cause a compilation error because it is defined without parentheses.
- **Uninitialized Metadata:** Attempting to access `reader.metadata.numTiles` before calling `reader.initialize(...)` will result in a null reference or invalid state error.

### Fix Code Hint
```scala
// WRONG: Using parentheses or calling before initialization
// val count = reader.metadata.numTiles()

// CORRECT: Parameterless call after initialization
reader.initialize(fileSystem, path, layerName, new BeastOptions())
val count = reader.metadata.numTiles
```

## API Test: `overlay`
_Grounding: doc-repaired from source (docfix)._

### Goal
User-facing API to stack multiple spatially aligned `RasterRDD` datasets (of the same pixel type) into a single multi-band `RasterRDD`. It transforms single-value or multi-value pixels into arrays of values aggregated from the corresponding pixels of the input rasters.

### Valid Call Patterns
```scala
import org.apache.spark.SparkContext
// CRITICAL: Import RasterRDD directly to avoid ambiguous type aliases
import edu.ucr.cs.bdlab.beast.cg.SpatialDataTypes.RasterRDD
// CRITICAL: Import ONLY the RaptorMixin to get the implicit extension method
import edu.ucr.cs.bdlab.raptor.RaptorMixin._

// Assume sc: SparkContext and rasterPath: String are provided
val rasterRDD: RasterRDD[Float] = sc.geoTiff[Float](rasterPath)

// MUST explicitly pass the type parameter [Float] to avoid Array[Nothing]
val stacked = rasterRDD.overlay[Float](rasterRDD)
val firstTile = stacked.first()
val firstPixel = firstTile.getPixelValue(0, 0)

assert(firstPixel != null, "Pixel value should not be null")
// Do not hardcode length == 2; input rasters may be multi-band (e.g., 11 bands -> 22 bands)
assert(firstPixel.length > 0, "Pixel array should not be empty")
println(s"__CHECK__ overlay ${firstPixel.mkString("[", ", ", "]")}")
```

### LLM Instruction Prompt
- MUST use the extension method `raster1.overlay[V](raster2)` provided by `import edu.ucr.cs.bdlab.raptor.RaptorMixin._`. Do not call `RasterOperationsLocal.overlay` directly.
- MUST explicitly provide the type parameter for the output array element type (e.g., `.overlay[Float](...)`). Because `V` only appears in the return type, the compiler cannot infer it from the arguments. Omitting it results in `Array[Nothing]` and compilation errors on array methods.
- Do not hardcode assertions expecting exactly 2 bands (e.g., `firstPixel.length == 2`), as the input raster in the test harness may be multi-band (e.g., 11 bands, resulting in 22 bands when overlaid with itself). Assert `firstPixel.length > 0` instead.
- MUST avoid wildcard import clashes. Both `beast._` and `raptor._` expose a `RasterRDD` symbol. Import `edu.ucr.cs.bdlab.beast.cg.SpatialDataTypes.RasterRDD` directly.

### Prompt Snippet
When stacking rasters, use the extension method `raster1.overlay[T](raster2)` via `import edu.ucr.cs.bdlab.raptor.RaptorMixin._`. You MUST explicitly pass the type parameter (e.g., `[Float]`) to prevent `Array[Nothing]` inference errors. Do not hardcode band count assertions (e.g., `length == 2`), as inputs may be multi-band; use `length > 0`. Avoid wildcard imports (`beast._` and `raptor._`) to prevent ambiguous `RasterRDD` resolution; import `edu.ucr.cs.bdlab.beast.cg.SpatialDataTypes.RasterRDD` directly.

### Common Failure Modes
- **Hardcoded Band Assertions (`Expected array of length 2, got 22`):** Assuming the input raster is single-band and asserting `firstPixel.length == 2`. The test harness provides a multi-band raster (11 bands), resulting in an array of length 22 when overlaid with itself.
- **Direct Call Failure:** Attempting to call `RasterOperationsLocal.overlay(raster1, raster2)` directly instead of using the fluent extension method `raster1.overlay[V](raster2)`.
- **Type Inference Failure (`value mkString is not a member of Array[Nothing]`):** Calling `raster1.overlay(raster2)` without the explicit type parameter `[V]` causes the compiler to infer `Nothing`. The resulting `RasterRDD[Array[Nothing]]` lacks methods like `length`, `apply`, and `mkString`.
- **Ambiguous Import (`reference to RasterRDD is ambiguous`):** Using `import edu.ucr.cs.bdlab.beast._` and `import edu.ucr.cs.bdlab.raptor._` together causes the compiler to fail when resolving the `RasterRDD` type annotation.

### Fix Code Hint
```scala
// WRONG: Direct call, missing type parameter, hardcoded band assertion
import edu.ucr.cs.bdlab.beast._
import edu.ucr.cs.bdlab.raptor._
val stacked = RasterOperationsLocal.overlay(raster1, raster2)
val firstPixel = stacked.first().getPixelValue(0, 0)
assert(firstPixel.length == 2) // ERROR: Fails if input is multi-band (e.g., 11 bands -> 22)
println(firstPixel.mkString(",")) // ERROR: value mkString is not a member of Array[Nothing]

// CORRECT: Specific imports, extension method, explicit type parameter, safe assertion
import edu.ucr.cs.bdlab.beast.cg.SpatialDataTypes.RasterRDD
import edu.ucr.cs.bdlab.raptor.RaptorMixin._
val stacked: RasterRDD[Array[Float]] = raster1.overlay[Float](raster2)
val firstPixel = stacked.first().getPixelValue(0, 0)
assert(firstPixel.length > 0) // Safe for multi-band inputs
println(firstPixel.mkString(",")) // Compiles successfully
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
Generates a distributed `SpatialRDD` containing synthetic bounding boxes following a parcel-like spatial distribution, primarily used for benchmarking spatial operations like distributed joins.

### Parameters
- `cardinality` (`Long`): The total number of synthetic box records to generate across the Spark cluster.
- `dither` (`Double`), default `0.2`: The amount of randomization (noise) to add to the boundaries of each generated box.
- `splitRange` (`Double`), default `0.2`: The range or ratio used when recursively splitting space to create the parcel boxes.

### Input
Requires an initialized `SparkContext` (`sc`) with Beast context extensions imported (`import edu.ucr.cs.bdlab.beast._`). The function must be called on a spatial data generator builder, typically instantiated via `sc.generateSpatialData`. Optionally, the builder can be configured with a specific Minimum Bounding Rectangle (MBR) or seed prior to calling `parcel`.

### Output
Returns `SpatialRDD` (or `JavaSpatialRDD` in the Java API) — a distributed Spark dataset containing the generated synthetic parcel geometries (boxes) ready for spatial partitioning, joins, or visualization.

### Valid Call Patterns
```scala
// Generate a large dataset of parcels for benchmarking
val parcels: SpatialRDD = sc.generateSpatialData
  .parcel(1000000, dither = 0.1, splitRange = 0.4)

// Generate a smaller dataset and visualize it
sc.generateSpatialData
  .parcel(100, dither = 0.2, splitRange = 0.3)
  .plotImage(300, 300, "parcel.png")
```

### LLM Instruction Prompt
- When generating synthetic spatial data for benchmarking or testing, use `sc.generateSpatialData.parcel(cardinality)`.
- Do not call `parcel` as a standalone function; it must be chained onto the `SpatialGeneratorBuilder` provided by `sc.generateSpatialData`.
- You may omit `dither` and `splitRange` to rely on their default values (`0.2`), or provide them explicitly to tune the generated distribution.

### Prompt Snippet
```text
To generate synthetic bounding boxes following a parcel distribution for benchmarking spatial joins, use the Beast spatial data generator: `val parcels = sc.generateSpatialData.parcel(1000000)`. This returns a `SpatialRDD` of generated geometries.
```

### Common Failure Modes
- **Missing Context Extensions:** Calling `sc.generateSpatialData` will fail with a "value not a member of SparkContext" compilation error if Beast implicits are not imported.
- **Standalone Call:** Attempting to call `parcel(...)` directly without the `sc.generateSpatialData` builder receiver.

### Fix Code Hint
```scala
// Ensure Beast implicits are imported to attach .generateSpatialData to SparkContext
import edu.ucr.cs.bdlab.beast._

// Correctly chain the parcel call onto the generator builder
val generatedParcels: SpatialRDD = sc.generateSpatialData.parcel(cardinality = 500000L)
```

## API Test: `part`
_Grounding: doc-repaired from source (docfix)._

### Signature
```scala
def part(i: Int): LiteList
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/LiteGeometry.scala:146_

### Goal
Retrieves a specific sub-geometry (a `LiteList` of coordinates) from a multi-part lightweight geometry (`LiteMultiList`). 
**Note: This is an INTERNAL/FRAMEWORK API used for vector tile generation. It should be excluded from main user-facing benchmark denominators.**

### Parameters
- `i` (`Int`): The zero-based index of the part to retrieve. Must be `0 <= i < parts.length`.

### Input
- A valid `LiteMultiList` instance (or its concrete subclasses like `LiteLineString` or `LitePolygon`). 
- **INTERNAL/FRAMEWORK Constraint:** Do not attempt to obtain the receiver via `IntermediateVectorTile.simplifyGeometry`. The API is testable only with explicit low-level construction of the underlying `LiteList` and `LiteLineString` objects using primitive `Array[Short]` inputs.

### Output
Returns `LiteList` — A lightweight coordinate sequence representing the requested geometry part.

### Valid Call Patterns
```scala
import edu.ucr.cs.bdlab.davinci.{LiteList, LiteLineString}

// Caller-owned low-level construction of coordinate arrays
val xs = Array[Short](0, 10, 20)
val ys = Array[Short](0, 10, 20)

// Caller-owned low-level construction of the geometry parts
val liteList = new LiteList(xs, ys)

// LiteLineString extends LiteMultiList, which defines the part() method
val multiLine = new LiteLineString(Array(liteList))

// Retrieve the part by index
val firstPart: LiteList = multiLine.part(0)
```

### LLM Instruction Prompt
- `part` is defined on `LiteMultiList` and its subclasses (like `LiteLineString` and `LitePolygon`), not on the base `LiteGeometry` trait.
- Do not attempt to use `IntermediateVectorTile.simplifyGeometry` to obtain a geometry, as it is inaccessible from outside the package.
- To construct a receiver for `part`, instantiate a `LiteLineString` directly by passing an `Array[LiteList]`, where each `LiteList` is created using `Array[Short]` for X and Y coordinates.

### Prompt Snippet
```text
`LiteMultiList.part(i: Int): LiteList` retrieves a sub-geometry part by index. INTERNAL API. Construct a `LiteLineString` directly from an `Array[LiteList]` to test. Do not use `IntermediateVectorTile`.
```

### Common Failure Modes
- **Inaccessible Framework Methods:** Attempting to obtain the receiver via `IntermediateVectorTile.simplifyGeometry(line)` fails with compilation errors because the method is inaccessible outside its package. This is an INTERNAL/FRAMEWORK API that must be tested via explicit low-level construction.
- **Missing Method on Base Trait:** Calling `part` on a `LiteGeometry` reference fails because `part` is defined on `LiteMultiList` (and subclasses like `LiteLineString`), not the base trait.
- **IndexOutOfBoundsException:** Passing an index `i` that is less than 0 or greater than or equal to the number of parts in the `LiteMultiList`.

### Fix Code Hint
```scala
// WRONG: Attempting to use inaccessible internal tile generators or base traits
val interTile = new IntermediateVectorTile(10, 0)
val simplifiedLine = interTile.simplifyGeometry(line) // Compilation fails (inaccessible)
val firstPart = simplifiedLine.part(0) // Compilation fails (part not on LiteGeometry)

// CORRECT: Explicit low-level construction of the receiver
import edu.ucr.cs.bdlab.davinci.{LiteList, LiteLineString}

val part1 = new LiteList(Array[Short](0, 10, 20), Array[Short](0, 10, 20))
val multiLine = new LiteLineString(Array(part1))
val firstPart: LiteList = multiLine.part(0)
```

## API Test: `partitionBy`

### Signature
```scala
def partitionBy(spatialPartitioner: SpatialPartitioner): PartitionedSpatialRDD
def partitionBy(partitionerKlass: Class[_ <: SpatialPartitioner], numPartitions: Int = rdd.getNumPartitions, opts: BeastOptions = new BeastOptions()): PartitionedSpatialRDD
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/indexing/IndexMixin.scala:35  (+1 more definition site/overload)_

### Goal
Distributes spatial vector data across a Spark cluster using a specialized spatial partitioner to optimize load balancing, spatial joins, and query pruning.

### Parameters
- `spatialPartitioner` (`SpatialPartitioner`): An instantiated spatial partitioner (e.g., `new GridPartitioner(...)`) that defines the spatial boundaries for distributing the data.
- *(Overload)* `partitionerKlass` (`Class[_ <: SpatialPartitioner]`): The class type of the partitioner to automatically instantiate and apply (e.g., `classOf[RSGrovePartitioner]`).
- *(Overload)* `numPartitions` (`Int`): The target number of partitions (defaults to the RDD's current partition count).
- *(Overload)* `opts` (`BeastOptions`): Additional configuration options for the partitioning process.

### Input
A `SpatialRDD` (typically containing `IFeature` objects) loaded from vector formats such as Esri Shapefile, GeoJSON, or CSV. 

### Output
Returns `PartitionedSpatialRDD` — an RDD where features are physically grouped by spatial proximity. This sets the RDD's partitioner property, enabling optimized distributed spatial joins, range queries, and spatial indexing.

### Valid Call Patterns
```scala
// Pattern 1: Partitioning by providing a partitioner class (from project README)
val partitionedStates = sparkContext.shapefile("ne_10m_admin_1_states_provinces.zip")
  .partitionBy(classOf[RSGrovePartitioner])

// Pattern 2: Partitioning by providing an instantiated partitioner (adapted from sibling test)
val mbr = data.summary
val gridPartitioner = new GridPartitioner(mbr, Array(2, 2))
val partitionedData = data.partitionBy(gridPartitioner)
```

### LLM Instruction Prompt
- Call `partitionBy` (or its sibling `spatialPartition`) on a `SpatialRDD` before performing distributed spatial joins that require partitioned data.
- The Distributed Join (`DJ`) algorithm requires *both* datasets to be spatially partitioned first. The Repartition Join (`REPJ`) requires at least *one* dataset to be spatially partitioned.
- To avoid duplicate results in custom algorithms, partitions must be disjoint. Only use `GridPartitioner`, `RSGrovePartitioner`, `KDTreePartitioner`, or `STRPartitioner` if disjoint partitioning is required.

### Prompt Snippet
```text
When preparing vector RDDs for spatial joins in Beast, use `rdd.partitionBy(classOf[RSGrovePartitioner])`. If using the `DJ` (Distributed Join) algorithm, you MUST partition both input RDDs first. If using `REPJ`, partition at least one. For custom algorithms requiring disjoint partitions to avoid duplicates, restrict your choice to `RSGrovePartitioner`, `GridPartitioner`, `KDTreePartitioner`, or `STRPartitioner`.
```

### Common Failure Modes
- **Missing Precondition for DJ Join:** Attempting to run `rdd1.spatialJoin(rdd2, ESJPredicate.Intersects, ESJDistributedAlgorithm.DJ)` without calling `partitionBy` on both `rdd1` and `rdd2` first, leading to execution failures.
- **Duplicate Results in Custom Algorithms:** Using a partitioner that does not support disjoint partitioning, resulting in overlapping boundaries and duplicate feature processing.
- **Calling on Raster Data:** Attempting to call `partitionBy` on a `RasterRDD` instead of a vector `SpatialRDD`. Raster retiling/partitioning is handled via `raster.retile` or `raster.explode`, not `partitionBy`.

### Fix Code Hint
```scala
// BAD: Attempting a DJ join without partitioning
// val sjResults = polygons.spatialJoin(points, ESJPredicate.Contains, ESJDistributedAlgorithm.DJ)

// GOOD: Partition both datasets before a DJ join
val partitionedPolygons = polygons.partitionBy(classOf[RSGrovePartitioner])
val partitionedPoints = points.partitionBy(classOf[RSGrovePartitioner])
val sjResults = partitionedPolygons.spatialJoin(partitionedPoints, ESJPredicate.Contains, ESJDistributedAlgorithm.DJ)
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
Distributes a spatial RDD across a Spark cluster using a specified spatial partitioner (such as R*-Grove or GridPartitioner) to optimize load balancing, enable query pruning, and satisfy preconditions for distributed spatial joins.

### Parameters
- `features` (`SpatialRDD`): The input RDD of vector geometries (features) to be spatially partitioned.
- `spatialPartitioner` / `partitionerClass` (`SpatialPartitioner` or `Class[_ <: SpatialPartitioner]`): Either an already initialized spatial partitioner instance (e.g., `new GridPartitioner(...)`) or the class type of the partitioner to use (e.g., `classOf[RSGrovePartitioner]`).
- `sizeFunction` (`IFeature=>Int`): A function to estimate the size or weight of a feature, used for load balancing when passing a partitioner class.
- `opts` (`BeastOptions`): Configuration options for the partitioning process when using the class-based overload.

### Input
A `SpatialRDD` of vector features, typically loaded via context extensions like `sc.shapefile` or `sc.geojsonFile`. 
*   **Preconditions:** If initializing a partitioner manually (like `GridPartitioner`), you must precompute the spatial summary of the features (e.g., using `Summary.computeForFeatures(features)`). 
*   **Algorithm Requirements:** Spatial partitioning is a strict precondition for certain spatial join algorithms: the Distributed Join (`DJ`) requires *both* datasets to be spatially partitioned, while the Repartition Join (`REPJ`) requires at least *one*.

### Output
Returns `PartitionedSpatialRDD` (or `JavaPartitionedSpatialRDD` / `JavaPairRDD[Integer, IFeature]` for Java APIs) — an RDD of `(partition number, IFeature)` where features are grouped into partitions based on spatial proximity.

### Valid Call Patterns
```scala
// Pattern 1: Using an initialized partitioner (requires precomputed summary)
val summary = Summary.computeForFeatures(features)
val partitionedFeatures = IndexHelper.partitionFeatures(
  features, 
  new GridPartitioner(summary, 1)
)

// Pattern 2: Using a partitioner class and size function
val partitionedFeatures2 = IndexHelper.partitionFeatures(
  features, 
  classOf[RSGrovePartitioner], 
  (f: IFeature) => 1, 
  new BeastOptions()
)
```

### LLM Instruction Prompt
- **Deprecation Warning:** The `partitionFeatures` method is officially marked as `@deprecated` in the source documentation. Instruct users to prefer `partitionFeatures2` if available, or use the RDD extension `rdd.spatialPartition(classOf[...])` for idiomatic Scala. If `partitionFeatures` must be used, it is called statically via `IndexHelper.partitionFeatures(...)`.
- **Disjoint Partitions:** If the user is implementing custom algorithms and needs to avoid duplicate results, they must use a partitioner that supports disjoint partitioning. Explicitly select `GridPartitioner`, `RSGrovePartitioner`, `KDTreePartitioner`, or `STRPartitioner`.
- **Join Preparation:** Always partition datasets before attempting a `DJ` (Distributed Join) to avoid runtime failures.

### Prompt Snippet
```text
To spatially partition vector data in Beast, use `IndexHelper.partitionFeatures`. Note that this specific method is deprecated in favor of `partitionFeatures2` or the `rdd.spatialPartition` extension method. If you must use it, ensure you choose a disjoint partitioner like `RSGrovePartitioner` if duplicate avoidance is required. For initialized partitioners like `GridPartitioner`, you must compute the dataset summary first.
```

### Common Failure Modes
- **Missing Summary for Initialization:** Attempting to instantiate a `GridPartitioner` without first computing the bounding box/summary of the `features` RDD, leading to incorrect or failed partitioning.
- **Duplicate Results in Custom Queries:** Using a non-disjoint partitioner for custom spatial algorithms, resulting in features spanning multiple partitions being processed multiple times.
- **Method Not Found:** Attempting to call `features.partitionFeatures(...)` directly on the RDD object instead of using the `IndexHelper` object.

### Fix Code Hint
```scala
// BAD: Calling directly on the RDD or missing the summary for GridPartitioner
val badPartition = features.partitionFeatures(new GridPartitioner(null, 1))

// GOOD: Using IndexHelper and computing the summary first
val summary = Summary.computeForFeatures(features)
val goodPartition = IndexHelper.partitionFeatures(features, new GridPartitioner(summary, 1))

// GOOD: Using the class-based overload with RSGrovePartitioner for disjoint partitions
val grovePartition = IndexHelper.partitionFeatures(
  features, 
  classOf[RSGrovePartitioner], 
  (f: IFeature) => 1, 
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
Distributes a set of spatial features across a Spark cluster using a specified spatial partitioner (such as a Grid or R*-Grove) to optimize load balancing and enable distributed spatial joins.

### Parameters
- `features` (`SpatialRDD`): The input RDD of vector geometries (`IFeature`) to be spatially partitioned.
- `partitionerClass` (`Class[_ <: SpatialPartitioner],
                        sizeFunction: IFeature=>Int`): The class type of the spatial partitioner to initialize (e.g., `classOf[RSGrovePartitioner]`). In the pre-initialized overloads, this is replaced by the instantiated `SpatialPartitioner` itself (e.g., `new GridPartitioner(...)`).
- `opts` (`BeastOptions`): Additional configuration options used when initializing the partitioner from a class.

### Input
A `SpatialRDD` (or `JavaSpatialRDD`) of vector features, typically loaded from formats like Shapefile, GeoJSON, or CSV. If the partitioned data will be used in custom algorithms that require disjoint partitions to avoid duplicate results, the chosen partitioner must support disjoint partitioning (e.g., `GridPartitioner`, `RSGrovePartitioner`, `KDTreePartitioner`, or `STRPartitioner`).

### Output
Returns `SpatialRDD` — The exact same set of input features, but physically reorganized across Spark partitions according to their spatial locations. The returned RDD will have its Spark `partitioner` property defined as the specified `SpatialPartitioner`.

### Valid Call Patterns
```scala
// Using an explicitly initialized partitioner via IndexHelper
val unitsquare = new EnvelopeNDLite(2, 0.0, 0.0, 1.0, 1.0)
val partitionedFeatures = IndexHelper.partitionFeatures2(
  features, 
  new GridPartitioner(unitsquare, Array(3, 3))
)

// Partitioning for a distributed spatial join
val partitioned1 = IndexHelper.partitionFeatures2(dataset1, new GridPartitioner(unitsquare, Array(5, 5)))
val partitioned2 = IndexHelper.partitionFeatures2(dataset2, new GridPartitioner(unitsquare, Array(5, 5)))
```

### LLM Instruction Prompt
- Call `partitionFeatures2` using the `IndexHelper` object (i.e., `IndexHelper.partitionFeatures2(...)`), as it is a helper method rather than an RDD extension method.
- When preparing datasets for a Distributed Join (`DJ`), you MUST spatially partition *both* datasets first. For a Repartition Join (`REPJ`), you MUST partition at least *one* dataset.
- To avoid duplicate results in custom algorithms, ensure you select a partitioner that supports disjoint partitioning (e.g., `GridPartitioner` or `RSGrovePartitioner`).

### Prompt Snippet
```text
To spatially partition an RDD of features for optimized querying or joining, use `IndexHelper.partitionFeatures2(features, partitioner)`. If preparing for a Distributed Join (DJ), both datasets must be partitioned. Use disjoint partitioners like `GridPartitioner` or `RSGrovePartitioner` to prevent duplicate results in custom algorithms.
```

### Common Failure Modes
- **Duplicate Results in Custom Algorithms:** Using a non-disjoint partitioner when disjoint partitions are required. Fix: Switch to `GridPartitioner`, `RSGrovePartitioner`, `KDTreePartitioner`, or `STRPartitioner`.
- **Spatial Join Failures (Missing Preconditions):** Attempting to run a Distributed Join (`ESJDistributedAlgorithm.PBSM` or `DJ`) without partitioning both datasets first, or a Repartition Join (`REPJ`) without partitioning at least one.
- **Compilation Error (Method Not Found):** Attempting to call `features.partitionFeatures2(...)` directly on the RDD. While Beast provides `rdd.spatialPartition` as an extension, `partitionFeatures2` specifically belongs to `IndexHelper`.

### Fix Code Hint
```scala
// WRONG: Calling directly on the RDD
val partitioned = features.partitionFeatures2(new GridPartitioner(env, Array(2, 2)))

// RIGHT: Using IndexHelper
val partitioned = IndexHelper.partitionFeatures2(features, new GridPartitioner(env, Array(2, 2)))
```

## API Test: `pixelLocations`

### Signature
```scala
def pixelLocations: Iterator[(Int, Int)]
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/ITile.scala:81_

_Source doc:_ An iterator that goes over all pixels in this tile @return an iterator that goes over all pixels (whether empty or not) in this tile

### Goal
Returns an iterator over the local `(x, y)` column and row indices of all pixels within a specific raster tile, regardless of whether the pixels contain valid data or are empty.

### Parameters
_None._

### Input
An `ITile[T]` instance, typically obtained by iterating over a `RasterRDD[T]` (e.g., loaded via `sc.geoTiff[T]`) or by reading individual tiles using a `GeoTiffReader`.

### Output
Returns `Iterator[(Int, Int)]` — an iterator yielding tuples of `(x, y)` integers representing the local column (`x`) and row (`y`) coordinates for every pixel in the tile.

### Valid Call Patterns
```scala
// Example 1: Iterating over all pixels in a tile and checking if they are defined
for ((x, y) <- tile.pixelLocations) {
  if (tile.isDefined(x, y)) {
    // Process valid pixel
  }
}

// Example 2: Using a guard in a for-comprehension to count non-empty pixels
var numNonEmptyPixels = 0
for ((x, y) <- tile.pixelLocations; if tile.isDefined(x, y)) {
  numNonEmptyPixels += 1
}
```

### LLM Instruction Prompt
- Use `tile.pixelLocations` when you need to manually iterate over the pixel coordinates of an `ITile[T]`.
- Because `pixelLocations` yields *all* pixels in the tile's grid (including empty/NoData pixels), you MUST check `tile.isDefined(x, y)` before attempting to read or process the pixel value to avoid processing invalid data.
- Remember that the yielded `(x, y)` values are local pixel indices within the tile, not global spatial coordinates (like longitude/latitude).

### Prompt Snippet
```text
`tile.pixelLocations` returns an `Iterator[(Int, Int)]` of all local (x, y) pixel coordinates in an `ITile`. It includes empty pixels, so always guard pixel access with `if (tile.isDefined(x, y))`.
```

### Common Failure Modes
- **Processing NoData/Empty Pixels:** Failing to check `tile.isDefined(x, y)` inside the loop, leading to incorrect calculations (e.g., treating a NoData fill value as a valid temperature or elevation).
- **Confusing Local Indices with Spatial Coordinates:** Assuming the `(x, y)` returned by `pixelLocations` are projected CRS coordinates (e.g., meters or degrees) rather than integer pixel offsets within the tile.

### Fix Code Hint
```scala
// WRONG: Blindly processing all pixels
for ((x, y) <- tile.pixelLocations) {
  val value = tile.getPixelValue(x, y) // May process NoData/fill values
}

// RIGHT: Guarding with isDefined
for ((x, y) <- tile.pixelLocations; if tile.isDefined(x, y)) {
  val value = tile.getPixelValue(x, y)
}
```

## API Test: `pixelType`
_Grounding: doc-repaired from source (docfix)._

### Signature
```scala
def pixelType: DataType
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/ITile.scala:138_

### Goal
ADVANCED/LOW-LEVEL API (Internal/Framework). Note: Recommended to exclude from the main user-facing denominator.
Returns the Spark SQL `DataType` representing the runtime type of pixel values in a raster tile. For single-band rasters, it returns a scalar type; for multi-band rasters, it wraps the scalar type in an `ArrayType`.

### Parameters
_None._

### Input
An instance of `ITile` (caller-owned, typically extracted via `rasterRDD.first()`). This is an ADVANCED/LOW-LEVEL internal framework representation, not a standard user-facing dataset.

### Output
Returns `org.apache.spark.sql.types.DataType`. Either a scalar type (e.g., `FloatType`) or an `ArrayType` (e.g., `ArrayType(FloatType, false)`).

### Valid Call Patterns
```scala
import org.apache.spark.sql.types.{DataType, ArrayType, FloatType}

// Caller-owned ITile extracted from a loaded raster dataset
val tile = rasterRDD.first()
val pType: DataType = tile.pixelType

// Safely handle both single-band and multi-band cases
pType match {
  case ArrayType(baseType, _) =>
    println(s"__CHECK__ pixelType is multi-band with base type $baseType")
  case scalarType =>
    println(s"__CHECK__ pixelType is single-band scalar type $scalarType")
}
```

### LLM Instruction Prompt
- ADVANCED/LOW-LEVEL API.
- If the raster has multiple bands (`numComponents > 1`), `pixelType` returns a Spark SQL `ArrayType` wrapping the base component type (e.g., `ArrayType(FloatType, false)`).
- If the raster is single-band (`numComponents == 1`), it returns the scalar Spark SQL `DataType` directly (e.g., `FloatType`).
- Callers must pattern match or check for `ArrayType` when inspecting `pixelType`, rather than blindly asserting against a scalar type like `FloatType`, as the dataset may be multi-band.

### Prompt Snippet
`pixelType` is an advanced internal API on `ITile` returning a Spark SQL `DataType`. For multi-band rasters, it returns an `ArrayType` (e.g., `ArrayType(FloatType, false)`). For single-band, it returns a scalar type (e.g., `FloatType`). Always pattern match to handle both cases safely.

### Common Failure Modes
- **ADVANCED/LOW-LEVEL API:** This operates on internal `ITile` plumbing and is excluded from standard user workflows.
- **Blindly asserting against a scalar type (The failure that just happened):** Assuming `pixelType` always returns a scalar like `FloatType` will fail with `AssertionError: Expected FloatType, but got ArrayType(FloatType,false)` if the loaded raster is multi-band. You must check for `ArrayType`.
- **Calling on the RDD instead of a Tile:** Attempting to call `rasterRDD.pixelType` fails at compile time. You must extract an `ITile` first (e.g., using `.first()`).

### Fix Code Hint
```scala
// WRONG: Blindly asserting or checking against a scalar type
// val pType = rasterRDD.first().pixelType
// assert(pType == org.apache.spark.sql.types.FloatType) // Fails on multi-band rasters

// RIGHT: Pattern matching to handle both single-band and multi-band (ArrayType) cases
val pType = rasterRDD.first().pixelType
pType match {
  case org.apache.spark.sql.types.ArrayType(baseType, _) =>
    println(s"Multi-band with base type $baseType")
  case scalarType =>
    println(s"Single-band with type $scalarType")
}
```

## API Test: `pixels`
_Grounding: doc-repaired from source (docfix)._

### Goal
Extract a lazy iterator of all valid (non-empty) pixel values along with their global grid coordinates (column, row) from an `ITile`. This is a user-facing API for pixel-level extraction and filtering.

### Valid Call Patterns
```scala
import edu.ucr.cs.bdlab.beast.geolite.ITile

// Assuming sc (SparkContext) is provided and the fixture exists
val rasterRDD = sc.geoTiff[Int]("glc2000_v1_1.tif")

val firstTile: ITile[Int] = rasterRDD.first()
val pixelsArray = firstTile.pixels.toArray
val numPixels = pixelsArray.length

assert(numPixels > 0, "Tile should have at least one pixel")

val minCol = pixelsArray.map(_._1).min
val minRow = pixelsArray.map(_._2).min
val maxCol = pixelsArray.map(_._1).max
val maxRow = pixelsArray.map(_._2).max

// Verify that the coordinates are valid global grid coordinates (not necessarily 0-indexed)
assert(minCol >= 0 && minRow >= 0, s"Expected valid global grid coordinates, got $minCol, $minRow")
assert(maxCol >= minCol && maxRow >= minRow, "Max coordinates should be >= min coordinates")

println(s"__CHECK__ pixels $numPixels")
```

### LLM Instruction Prompt
- Use `tile.pixels` to unpack an `ITile[T]` into an iterator of individual pixel values and their coordinates.
- **CRITICAL:** The `(Int, Int)` coordinates returned by `pixels` are the **global pixel grid coordinates** (column and row) within the entire raster, NOT local 0-indexed coordinates within the tile.
- The iterator only yields pixels that are defined; it automatically skips empty or fill values via `isDefined`.
- The type parameter `T` must exactly match the runtime pixel type of the raster to avoid `ClassCastException`s during iteration.

### Prompt Snippet
```text
To process individual valid pixels within an `ITile[T]`, call `tile.pixels`. This returns an `Iterator[(Int, Int, T)]` representing the global grid column, global grid row, and the pixel value. It automatically skips empty/fill values. Ensure your raster load operation (e.g., `sc.geoTiff[Int]`) uses the correct type parameter. Do not assert that coordinates start at 0,0.
```

### Common Failure Modes
- **Coordinate Assumption Failure (`java.lang.AssertionError: assertion failed: Expected min col/row to be 0, got 45, 87`):** Assuming the returned `(Int, Int)` coordinates are local 0-indexed coordinates within the tile. They are global grid coordinates within the entire raster.
- **Type Mismatch (`ClassCastException`):** Calling `pixels` on an `ITile[T]` where `T` was incorrectly specified during loading (e.g., using `sc.geoTiff[Float]` for an integer GeoTIFF). The type parameter must exactly match the runtime pixel type.

### Fix Code Hint
```scala
// BAD: Assuming local 0-indexed coordinates
val badPixels = tile.pixels.toArray
assert(badPixels.map(_._1).min == 0) // Fails: returns global grid coordinates (e.g., 45)

// GOOD: Treating coordinates as global grid coordinates and matching runtime type
val validPixels = tile.pixels.toArray
val minCol = validPixels.map(_._1).min
assert(minCol >= 0) // Global coordinates are >= 0, but rarely exactly 0 for arbitrary tiles
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
Generates a distributed RDD of Mapbox Vector Tiles (MVT) across a specified range of zoom levels for web-based visualization of vector features.

### Parameters
- `features` (`SpatialDataTypes.JavaSpatialRDD` or `SpatialRDD`): The distributed set of vector features (e.g., polygons, lines, points) to visualize.
- `minLevel` (`Int`): The minimum zoom level to visualize (inclusive). Used in the Java API.
- `maxLevel` (`Int`): The maximum zoom level to visualize (inclusive). Used in the Java API.
- `resolution` (`Int`): The pixel resolution of each generated tile (typically 256 or 512).
- `buffer` (`Int`): The buffer around each tile in pixels to consider when visualizing, which prevents clipping artifacts for features that cross tile boundaries.
- `opts` (`BeastOptions`): Additional configuration options for generating the tiles, such as simplification thresholds (e.g., `"threshold" -> "1m"`).

*(Note: The Scala overload replaces `minLevel` and `maxLevel` with a single `levels: Range` parameter).*

### Input
A distributed RDD of vector features (`SpatialRDD`). This is typically loaded from vector formats like Shapefile, GeoJSON, or CSV using SparkContext extensions (e.g., `sc.shapefile(...)`). For massive datasets and deep zoom levels, it is highly recommended that the input features are spatially partitioned and indexed first (e.g., loaded via `sc.spatialFile(...)` from an R-Tree index) to optimize the distributed tile generation.

### Output
Returns `JavaPairRDD[java.lang.Long, IntermediateVectorTile]` (or `RDD[(Long, IntermediateVectorTile)]` in Scala) — an RDD containing the generated vector tiles keyed by their encoded Tile ID (Long). These intermediate tiles are typically passed directly to `MVTDataVisualizer.saveTilesCompact` to be written to disk as a compressed MVT archive.

### Valid Call Patterns
```scala
import edu.ucr.cs.bdlab.beast.common.BeastOptions
import edu.ucr.cs.bdlab.davinci.MVTDataVisualizer

// Example 1: Standard usage with a loaded shapefile
val opts = new BeastOptions().set("threshold", 0)
val features = sparkContext.shapefile("ne_10m_admin_1_states_provinces.zip")
val tiles = MVTDataVisualizer.plotAllTiles(features, levels = 0 to 6, resolution = 256, buffer = 5, opts)
MVTDataVisualizer.saveTilesCompact(tiles, "provinces_mvt.zip", opts)

// Example 2: Optimized usage with a pre-built spatial index for deep zoom levels
val indexedFeatures = sparkContext.spatialFile("provinces_index")
val deepTiles = MVTDataVisualizer.plotAllTiles(
  indexedFeatures, 
  levels = 0 to 19, 
  resolution = 256, 
  buffer = 5, 
  opts = new BeastOptions().set("threshold", "1m")
)
MVTDataVisualizer.saveTilesCompact(deepTiles, "provinces_deep_mvt.zip", new BeastOptions())
```

### LLM Instruction Prompt
- Call `MVTDataVisualizer.plotAllTiles` to generate multilevel vector tile pyramids for web maps.
- When writing Scala code, prefer the overload that takes a `Range` (e.g., `levels = 0 to 6`) rather than separate `minLevel` and `maxLevel` arguments.
- Always call this method on the `MVTDataVisualizer` object.
- Do not use this API for raster visualization. The DaVinci Server raster visualization is deprecated; MVT is strictly for vector data.
- Always follow up `plotAllTiles` with `MVTDataVisualizer.saveTilesCompact(tiles, outputPath, opts)` to persist the generated tiles to a zip archive.

### Prompt Snippet
```text
To generate Mapbox Vector Tiles (MVT) in Beast, use `MVTDataVisualizer.plotAllTiles(features, levels = min to max, resolution = 256, buffer = 5, opts)`. This returns an RDD of intermediate tiles. You must then save them using `MVTDataVisualizer.saveTilesCompact(tiles, "output.zip", opts)`. For large datasets spanning many zoom levels, spatially partition and index the features first.
```

### Common Failure Modes
- **Missing Receiver:** Attempting to call `features.plotAllTiles(...)` directly on the RDD. It must be called as `MVTDataVisualizer.plotAllTiles(features, ...)`.
- **Using Raster Data:** Passing a `RasterRDD` instead of a `SpatialRDD`. MVT generation is exclusively for vector geometries.
- **Out of Memory on Deep Zooms:** Generating tiles up to zoom level 19 on unpartitioned data can cause massive shuffles and OOM errors. The input should be spatially partitioned (e.g., `RSGrovePartitioner`) and saved as an index first.
- **Missing Save Step:** Forgetting to call `saveTilesCompact`, resulting in the Spark DAG never executing because no action was triggered.

### Fix Code Hint
```scala
// BAD: Calling on the RDD directly or forgetting to save
val tiles = features.plotAllTiles(0, 6, 256, 5, opts)

// GOOD: Calling on MVTDataVisualizer and saving the output
val tiles = MVTDataVisualizer.plotAllTiles(features, levels = 0 to 6, resolution = 256, buffer = 5, opts)
MVTDataVisualizer.saveTilesCompact(tiles, "output_mvt.zip", opts)

// BEST (for large data): Partition, index, then plot
features.partitionBy(classOf[RSGrovePartitioner]).saveAsIndex("my_index", "rtree")
val indexedFeatures = sparkContext.spatialFile("my_index")
val deepTiles = MVTDataVisualizer.plotAllTiles(indexedFeatures, levels = 0 to 14, resolution = 256, buffer = 5, opts)
MVTDataVisualizer.saveTilesCompact(deepTiles, "output_mvt.zip", opts)
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
Plots a distributed set of spatial features to a single image (or a multilevel image pyramid), maintaining the aspect ratio of the input data and optionally filtering the visualization to a specific bounding box.

### Parameters
- `features` (`SpatialDataTypes.SpatialRDD`): The distributed set of vector features (e.g., points, lines, polygons) to visualize.
- `imageWidth` (`Int`): The maximum width of the output image in pixels (treated as an upper bound to maintain aspect ratio).
- `imageHeight` (`Int`): The maximum height of the output image in pixels (treated as an upper bound to maintain aspect ratio).
- `imagePath` (`String`): The file path where the resulting image (e.g., PNG) will be written.
- `plotterClass` (`Class[_ <: Plotter]`), default `classOf[GeometricPlotter]`: The class of the plotter to use for rendering the geometries.
- `canvasMBR` (`EnvelopeNDLite`), default `null`: (Optional) The minimum bounding rectangle specifying the extents of the data to plot. If `null`, defaults to the full extent of the input data.
- `opts` (`BeastOptions`), default `new BeastOptions()`: (Optional) Additional configuration options for the plotter, such as styling (e.g., `"stroke"`, `"fill"`).

### Input
- A `SpatialRDD` of vector features, typically loaded via context extensions like `sc.shapefile`, `sc.geojsonFile`, or `sc.readCSVPoint`.
- Valid output file paths for the generated image (e.g., a `.png` file for single-level plots, or a `.zip` archive for multilevel pyramids).
- Styling configurations passed via `BeastOptions` (e.g., `.set("stroke", "blue")`).

### Output
Returns `Unit` — The operation is executed for its side effect of writing a rendered image file (or a ZIP archive of image tiles for the multilevel overloads) to the specified `imagePath` or `outputPath`.

### Valid Call Patterns
```scala
// Single-level plot (inferred from signature and sibling object usage)
SingleLevelPlot.plotFeatures(
  features = vectorRDD,
  imageWidth = 1024,
  imageHeight = 1024,
  imagePath = "output_image.png",
  plotterClass = classOf[GeometricPlotter],
  canvasMBR = null,
  opts = new BeastOptions().set("stroke", "blue").set("fill", "#9999E6")
)

// Multilevel plot (adapted from the project's Java README example to Scala)
MultilevelPlot.plotFeatures(
  features = vectorRDD,
  levels = 0 to 9,
  plotterClass = classOf[GeometricPlotter],
  inputPath = null,
  outputPath = "counties_multilevel_portable.zip",
  opts = new BeastOptions().set("stroke", "blue").set("fill", "#9999E6").setLong("threshold", 0)
)
```

### LLM Instruction Prompt
- Use `SingleLevelPlot.plotFeatures` to generate a single static image (e.g., PNG) from a `SpatialRDD`.
- Use `MultilevelPlot.plotFeatures` (using the `Range` or `minLevel, maxLevel` overloads) to generate a zoomable image pyramid saved as a ZIP archive.
- Always pass `classOf[GeometricPlotter]` as the `plotterClass` unless a specific custom plotter is requested.
- Use `BeastOptions` to define visual styles like `"stroke"` (outline color) and `"fill"` (interior color).
- Do not invent file paths; use the exact output paths requested by the user.

### Prompt Snippet
```text
To visualize the spatial features, use `SingleLevelPlot.plotFeatures` for a single image or `MultilevelPlot.plotFeatures` for a pyramid. Pass `classOf[GeometricPlotter]` and configure colors using `BeastOptions`. The dimensions provided to the single-level plot act as upper bounds to preserve the data's aspect ratio.
```

### Common Failure Modes
- **Missing Object Qualifier:** Attempting to call `plotFeatures(...)` as a bare function or directly on the RDD without the implicit wrapper (e.g., `rdd.plotFeatures(...)` instead of `SingleLevelPlot.plotFeatures(...)`), resulting in compilation errors.
- **Incorrect Plotter Class Type:** Passing an instantiated object (e.g., `new GeometricPlotter()`) instead of the class type (`classOf[GeometricPlotter]`).
- **Opaque/Invisible Features:** Failing to set `"stroke"` or `"fill"` in `BeastOptions`, which may result in default rendering that is difficult to see depending on the background.

### Fix Code Hint
```scala
// WRONG: rdd.plotFeatures(1000, 1000, "out.png")
// WRONG: SingleLevelPlot.plotFeatures(rdd, 1000, 1000, "out.png", new GeometricPlotter())

// CORRECT:
SingleLevelPlot.plotFeatures(
  rdd, 
  1000, 
  1000, 
  "out.png", 
  classOf[GeometricPlotter], 
  null, 
  new BeastOptions().set("stroke", "red")
)
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
Renders a distributed spatial RDD of vector features into a single image file (e.g., PNG) with specified pixel dimensions for quick visualization.

### Parameters
- `rdd` (`JavaSpatialRDD`): The spatial RDD containing the vector features to plot. In Scala, this is typically passed implicitly as the receiver (e.g., `features.plotImage(...)`).
- `imageWidth` (`Int`): The width of the generated output image in pixels.
- `imageHeight` (`Int`): The height of the generated output image in pixels.
- `imagePath` (`String`): The file path where the generated image will be saved (e.g., `"output.png"`).
- `plotterClass` (`Class[_ <: Plotter], opts: BeastOptions`): The class of the plotter to use (defaults to `classOf[GeometricPlotter]`), and an optional `BeastOptions` object for additional user configuration.

### Input
A spatial RDD of vector features (e.g., loaded via `sc.shapefile`, `sc.geojsonFile`, or generated via `sc.generateSpatialData`). The operation requires the features to have valid geometries. 

### Output
Returns `Unit` — writes a single image file (typically a PNG) to the specified `imagePath` on the driver or accessible file system.

### Valid Call Patterns
```scala
// Pattern 1: Plotting a loaded vector dataset (Shapefile, GeoJSON, etc.)
val buildings = sc.shapefile("MSBuildings_data_index.zip")
buildings.plotImage(1000, 1000, "MSBuildings.png")

// Pattern 2: Plotting generated spatial data
sc.generateSpatialData
  .makeBoxes(0.1, 0.2)
  .uniform(100)
  .plotImage(300, 300, "uniform.png")
```

### LLM Instruction Prompt
- Use `rdd.plotImage(width, height, path)` as an implicit method on a spatial RDD to quickly generate a single PNG image of vector features.
- Do not use `plotImage` for massive datasets where a single image would be too dense or exceed memory limits; for web-based exploration of large datasets, prefer generating MVT (Mapbox Vector Tiles) or using `plotPyramid`.
- Do not use `plotImage` for raster visualization, as the DaVinci Server is deprecated and `plotImage` is designed for plotting vector features.

### Prompt Snippet
```text
To visualize the generated spatial data or loaded shapefiles, use the `plotImage` method directly on the RDD. Provide the desired width, height, and output file path (e.g., "output.png").
```

### Common Failure Modes
- **Calling on Raster Data:** Attempting to use `plotImage` on a `RasterRDD` instead of a vector feature RDD. `plotImage` is designed for vector features.
- **OOM on Driver:** Generating an extremely large single image (e.g., `imageWidth = 50000`) which exceeds the driver's memory capacity, as the final image must be collected and written.
- **Missing File Extension:** Providing an `imagePath` without a valid image extension (like `.png`), which may cause the underlying image writer to fail or produce an unreadable file.

### Fix Code Hint
```scala
// BAD: Attempting to plot a raster or missing the implicit receiver
// val raster = sc.geoTiff[Int]("data.tif")
// plotImage(raster, 1000, 1000, "out.png")

// GOOD: Plotting vector features using the implicit class syntax
val features = sc.shapefile("ne_10m_admin_0_countries.zip")
features.plotImage(1920, 1080, "countries.png")
```

## API Test: `plotPyramid`
_Grounding: doc-repaired from source (docfix)._

### Goal
Generates a multilevel tiled image pyramid from a spatial dataset (`SpatialRDD`) and writes it to a specified path (typically a ZIP archive) for web-based map visualization. This is a standard user-facing API included in the main denominator.

### Valid Call Patterns
```scala
import edu.ucr.cs.bdlab.beast._
import edu.ucr.cs.bdlab.beast.common.BeastOptions
import edu.ucr.cs.bdlab.davinci.GeometricPlotter

// Assuming `featuresRDD` is a valid SpatialRDD and `output_dir` is provided by the harness
val outZip = s"$output_dir/pyramid.zip"
val opts = new BeastOptions()
opts.put("mercator", "true")
opts.put("stroke", "blue")

// Spatial partitioning is optional; omit for minimal tests to avoid import errors
featuresRDD.plotPyramid(outZip, 3, classOf[GeometricPlotter], opts)
```

### LLM Instruction Prompt
- Call `plotPyramid(outPath, numLevels, plotterClass, opts)` on a spatial RDD to generate a multilevel image pyramid.
- Always provide a `.zip` extension for `outPath` and write to `output_dir`.
- **Required Imports:** You must explicitly import `edu.ucr.cs.bdlab.davinci.GeometricPlotter` and `edu.ucr.cs.bdlab.beast.common.BeastOptions`.
- Instantiate `BeastOptions` and use `.put(key, value)` with string values for configuration (e.g., `"mercator"`, `"stroke"`).
- **Do not guess packages** for spatial partitioners (like `RSGrovePartitioner`). Spatial partitioning is an optional optimization and should be omitted for minimal tests to prevent compilation failures.

### Prompt Snippet
```text
To visualize a spatial RDD, use `rdd.plotPyramid(s"$output_dir/out.zip", 3, classOf[GeometricPlotter], opts)`. Import `edu.ucr.cs.bdlab.davinci.GeometricPlotter` and `edu.ucr.cs.bdlab.beast.common.BeastOptions`. Populate `opts` using `opts.put("key", "value")`. Do not guess partitioner packages; omit partitioning for minimal tests.
```

### Common Failure Modes
- **Incorrect Package Imports:** Guessing incorrect packages for `GeometricPlotter` (e.g., `edu.ucr.cs.bdlab.beast.visualization`) or `RSGrovePartitioner` (e.g., `edu.ucr.cs.bdlab.beast.cg`) causes compilation errors. `GeometricPlotter` is strictly in `edu.ucr.cs.bdlab.davinci`.
- **Unnecessary Complexity:** Attempting to use `RSGrovePartitioner` for a minimal test. It is an optional optimization for large datasets and omitting it avoids missing-class errors.
- **Type Mismatches in Options:** Passing non-string values to `BeastOptions.put()`. `BeastOptions` extends `HashMap[String, String]`, so both keys and values must be strings.

### Fix Code Hint
```scala
// Wrong: Guessing incorrect packages, using optional partitioners, and passing Seq instead of BeastOptions
import edu.ucr.cs.bdlab.beast.visualization.GeometricPlotter
import edu.ucr.cs.bdlab.beast.cg.RSGrovePartitioner

val partitioned = features.spatialPartition(classOf[RSGrovePartitioner])
partitioned.plotPyramid("out.zip", 3, classOf[GeometricPlotter], Seq("stroke" -> "blue"))

// Fix: Use correct packages, omit optional partitioner, use BeastOptions.put with strings
import edu.ucr.cs.bdlab.davinci.GeometricPlotter
import edu.ucr.cs.bdlab.beast.common.BeastOptions

val opts = new BeastOptions()
opts.put("stroke", "blue")
features.plotPyramid(s"$output_dir/pyramid.zip", 3, classOf[GeometricPlotter], opts)
```

## API Test: `plotSingleTileParallel`
_Grounding: doc-repaired from source (docfix)._

### Goal
ADVANCED/LOW-LEVEL API: Generates a single Mapbox Vector Tile (MVT) from a distributed `SpatialRDD` of vector features using a Spark job. 
*Note: This API should generally be excluded from the main user-facing denominator. Users typically invoke pyramid-generation APIs (like `plotAllTiles`); this is exposed only for advanced/internal use cases where a specific tile needs to be generated on demand.*

### Input
- **Data:** A `SpatialRDD` (`edu.ucr.cs.bdlab.beast.cg.SpatialDataTypes.SpatialRDD`) containing vector geometries.
- **Preconditions:** ADVANCED/LOW-LEVEL. The `features` RDD **must not be empty**, as the API internally calls `features.first()` to determine the SRID and will throw an `UnsupportedOperationException` if empty. The `tileID` parameter requires a `Long` (pass `0L` directly for testing).

### Output
Returns `edu.ucr.cs.bdlab.davinci.VectorTile.Tile` — A Java Protobuf object representing a Mapbox Vector Tile containing the aggregated features.

### Valid Call Patterns
```scala
import edu.ucr.cs.bdlab.davinci.MVTDataVisualizer
import edu.ucr.cs.bdlab.davinci.VectorTile.Tile

// The API calls featuresRDD.first() internally to get the SRID.
// It will throw an UnsupportedOperationException if the RDD is empty.
if (!featuresRDD.isEmpty()) {
  val tileId: Long = 0L 
  val resolution: Int = 256
  val buffer: Int = 0

  val tile: Tile = MVTDataVisualizer.plotSingleTileParallel(
    featuresRDD, 
    resolution, 
    tileId, 
    buffer
  )

  assert(tile != null, "Generated tile should not be null")
  assert(tile.getLayersCount >= 0, "Tile should have a valid layer count")
}
```

### LLM Instruction Prompt
- `plotSingleTileParallel` is a method on the `edu.ucr.cs.bdlab.davinci.MVTDataVisualizer` object.
- You MUST wrap the invocation in `if (!featuresRDD.isEmpty())` to prevent crashes on empty fixtures, because the API internally calls `features.first()`.
- The `tileID` parameter is a `Long`. Pass a literal like `0L` directly to avoid missing `TileIndex` imports.
- The test must include strict, unconditional assertions on the returned `Tile` object (e.g., `assert(tile != null)` and `assert(tile.getLayersCount >= 0)`).

### Prompt Snippet
```text
ADVANCED API: To generate a single Mapbox Vector Tile from a SpatialRDD, call `edu.ucr.cs.bdlab.davinci.MVTDataVisualizer.plotSingleTileParallel(features, resolution, tileID, buffer)`. The `features` RDD must not be empty (wrap in `if (!features.isEmpty())`). Pass `0L` for `tileID`. Assert the result is not null and has a valid layer count.
```

### Common Failure Modes
- **Empty RDD Crash (`UnsupportedOperationException`):** The API internally calls `features.first()` to extract the source SRID. If the harness injects an empty RDD fixture, this crashes. Always wrap the call in `if (!features.isEmpty())`.
- **Insufficient Assertions (`AssertionError: The documented contract is insufficient...`):** The harness will fail the test if the snippet lacks strict, unconditional assertions on the result object. Always assert `tile != null` and `tile.getLayersCount >= 0`.
- **Missing `TileIndex` Import (`error: not found: value TileIndex`):** Attempting to use `TileIndex.encode(0, 0, 0)` without the exact package import causes a compilation failure. Bypass this by passing a `Long` literal (e.g., `0L`) directly.
- **API Misclassification:** Using this ADVANCED/LOW-LEVEL API for general map generation instead of the standard user-facing `plotAllTiles`.

### Fix Code Hint
```scala
// WRONG: Crashes on empty RDDs and lacks assertions
// val tile = MVTDataVisualizer.plotSingleTileParallel(featuresRDD, 256, 0L, 0)
// println(tile)

// CORRECT: Guard against empty RDDs and assert the result
if (!featuresRDD.isEmpty()) {
  val tile = edu.ucr.cs.bdlab.davinci.MVTDataVisualizer.plotSingleTileParallel(featuresRDD, 256, 0L, 0)
  assert(tile != null, "Generated tile should not be null")
  assert(tile.getLayersCount >= 0, "Tile should have a valid layer count")
}
```

## API Test: `pointSample`
_Grounding: doc-repaired from source (docfix)._

### Goal
**INTERNAL/FRAMEWORK API.** Extracts a random, bounded sample of point coordinates from a distributed vector dataset (`SpatialRDD`) to compute dataset statistics and partition boundaries. *Scoring recommendation: Exclude from main user-facing denominator; include only in advanced/internal buckets.*

### Input
- **Data:** A `SpatialRDD` (`RDD[IFeature]`). Because this is an internal API, testing requires explicit low-level construction using `GeometryReader.DefaultGeometryFactory`, `Coordinate`, and `Feature.create`. The caller owns the constructed RDD and geometry objects.
- **Parameters:** `sampleSize` (Int, max points to collect), `sampleRatio` (Double, fraction of dataset to read), `seed` (Long, optional).

### Output
Returns `Array[Array[Double]]` — A dimension-major 2D array collected to the driver. 
- **Empty behavior:** If sampling yields zero points, it returns an empty array (`Array.empty[Array[Double]]`) with length 0.
- **Populated behavior:** The *first* index is the spatial dimension (e.g., `0` for X, `1` for Y), and the *second* index is the specific point.

### Valid Call Patterns
```scala
import edu.ucr.cs.bdlab.beast.synopses.PointSampler
import edu.ucr.cs.bdlab.beast.cg.SpatialDataTypes.SpatialRDD
import edu.ucr.cs.bdlab.beast.geolite.{Feature, GeometryReader}
import org.locationtech.jts.geom.Coordinate

// 1. Low-level construction of SpatialRDD (Caller-owned)
val factory = GeometryReader.DefaultGeometryFactory
val point = factory.createPoint(new Coordinate(3, 4))
val featuresRDD: SpatialRDD = sc.parallelize(Seq(Feature.create(null, point)), 4)

// 2. Sample execution
val sampleSizeLimit = 1000
// Use sampleRatio = 1.0 for small test RDDs to guarantee points are sampled
val sample: Array[Array[Double]] = PointSampler.pointSample(featuresRDD, sampleSizeLimit, 1.0)

// 3. Safe access pattern
assert(sample != null, "Sample array should not be null")
if (sample.nonEmpty) {
  assert(sample.length >= 2, s"Expected at least 2 dimensions, got ${sample.length}")
  assert(sample(0).length == sample(1).length, "X and Y arrays must have the same number of elements")
  assert(sample(0).length <= sampleSizeLimit, s"Sample size ${sample(0).length} exceeded limit $sampleSizeLimit")
  
  val numPoints = sample(0).length
  val firstX = sample(0)(0) // Dimension 0 (X), Point 0
  val firstY = sample(1)(0) // Dimension 1 (Y), Point 0
  println(s"__CHECK__ pointSample $numPoints points. First: ($firstX, $firstY)")
} else {
  println("__CHECK__ pointSample 0")
}
```

### LLM Instruction Prompt
- **Internal API:** This is an internal framework API. Do not present it as a standard user workflow.
- **Empty Array Check:** If sampling yields zero points (common with small datasets and low `sampleRatio`), the method returns an empty array (`Array.empty[Array[Double]]`) with length 0. Callers MUST check `if (sample.nonEmpty)` before accessing dimension indices like `sample(0)`.
- **Test Configuration:** When testing with small datasets, use a `sampleRatio` of `1.0` to guarantee that points are actually sampled by Spark's probabilistic sampler.
- **Dimension-Major:** The returned array is dimension-major. `array(0)` contains all X coordinates; `array(1)` contains all Y coordinates.

### Prompt Snippet
```text
PointSampler.pointSample(features: SpatialRDD, sampleSize: Int, sampleRatio: Double): Array[Array[Double]]
INTERNAL API. Samples points from a SpatialRDD. Returns a dimension-major 2D array (index 0 is dimension, index 1 is point). If 0 points are sampled, returns an empty array (length 0). Always check `if (sample.nonEmpty)` before accessing. Use sampleRatio=1.0 for small test RDDs.
```

### Common Failure Modes
- **`java.lang.AssertionError: assertion failed: Expected 2 dimensions (X and Y), got 0`:** The test assumed the returned array would always have a length of 2. Spark's probabilistic sampling with a low `sampleRatio` (e.g., 0.1) on a small test RDD yields zero features, causing the method to return an empty array (length 0). Fix by using `sampleRatio = 1.0` and checking `if (sample.nonEmpty)`.
- **Assuming a point-major array:** Iterating over the outer array expecting each element to be a `[X, Y]` coordinate pair. The outer array represents dimensions (X-array, Y-array).
- **Calling as an RDD method:** Attempting to call `features.pointSample(...)` will fail to compile. It must be called via the `PointSampler` object.

### Fix Code Hint
```scala
// WRONG: Low sample ratio on small RDD, and missing empty check
val sample = PointSampler.pointSample(featuresRDD, 1000, 0.1)
val firstPointX = sample(0)(0) // Fails with IndexOutOfBoundsException if sample is empty

// RIGHT: sampleRatio=1.0 for tests, and explicit nonEmpty check
val sample = PointSampler.pointSample(featuresRDD, 1000, 1.0)
if (sample.nonEmpty) {
  val firstPointX = sample(0)(0)
  val firstPointY = sample(1)(0)
}
```

## API Test: `printOperationUsage`

### Signature
```scala
def printOperationUsage(operation: Operation, options: BeastOptions, out: PrintStream): Unit
```
_Source: beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/util/OperationHelper.scala:334_

_Source doc:_ Prints the usage of a specific operation. @param operation the operation to print the usage to @param out the print stream to write to

### Goal
Prints the command-line usage instructions and parameter details for a specific Beast operation to a provided output stream.

### Parameters
- `operation` (`Operation`): The metadata object representing the specific Beast operation (e.g., retrieved from the `OperationHelper.operations` registry) for which to print usage.
- `options` (`BeastOptions`): Configuration options for the Beast environment. Can safely be `null` if no specific options are required for formatting the output.
- `out` (`PrintStream`): The Java `PrintStream` (such as `System.out` or one wrapping a `ByteArrayOutputStream`) where the usage text will be written.

### Input
Requires a valid `Operation` instance (typically fetched by name from Beast's internal operation registry) and an open, writable `PrintStream`. 

### Output
Returns `Unit` — performs a side effect by writing the formatted usage string (including expected parameters and descriptions) to the provided `PrintStream`.

### Valid Call Patterns
```scala
import java.io.{ByteArrayOutputStream, PrintStream}
import edu.ucr.cs.bdlab.beast.util.OperationHelper

// 1. Writing usage to a byte array (useful for testing or capturing output)
val baos = new ByteArrayOutputStream()
val printer: PrintStream = new PrintStream(baos)

// Retrieve the operation by name and print its usage (options can be null)
val op = OperationHelper.operations("subtest1")
OperationHelper.printOperationUsage(op, null, printer)

printer.close()
val usageString = new String(baos.toByteArray)

// 2. Writing usage directly to standard output
OperationHelper.printOperationUsage(op, null, System.out)
```

### LLM Instruction Prompt
- Use `OperationHelper.printOperationUsage` when you need to programmatically output or capture the CLI help text and parameter requirements for a specific Beast operation.
- The `options` parameter of type `BeastOptions` can be passed as `null` if no specific configuration is needed.
- Always call this method on the `OperationHelper` object.

### Prompt Snippet
```text
To print or capture the usage instructions for a specific Beast operation, use `OperationHelper.printOperationUsage(operation, options, printStream)`. You can retrieve the `Operation` object from `OperationHelper.operations("operationName")`. The `options` parameter can safely be `null`.
```

### Common Failure Modes
- **Null Pointer Exception on Operation:** Attempting to fetch an unregistered operation name from `OperationHelper.operations("invalid_name")` will yield an error or `null` before `printOperationUsage` is even called.
- **Closed Stream:** Passing a `PrintStream` that has already been closed will result in the usage text not being written or throwing an `IOException`.

### Fix Code Hint
```scala
// Ensure the operation exists in the registry before printing
val opName = "my_operation"
if (OperationHelper.operations.contains(opName)) {
  val op = OperationHelper.operations(opName)
  OperationHelper.printOperationUsage(op, null, System.out)
} else {
  println(s"Operation $opName not found.")
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
Writes a file entry into an open ZIP archive without applying compression (using the `STORED` method), which is useful when packaging pre-compressed geospatial artifacts like MVT vector tiles or image pyramids.

### Parameters
- `zip` (`ZipOutputStream`): The open ZIP output stream (either `java.util.zip.ZipOutputStream` or Apache Commons `ZipArchiveOutputStream`) to which the new file entry will be appended.
- `filename` (`String`): The name and internal path of the entry to create within the ZIP archive (e.g., `"README.bin"` or `"data.bin"`).
- `data` (`Array[Byte]`): The raw binary data of the file to be written into the archive.

### Input
The caller must provide an open, writable `ZipOutputStream` (typically wrapping a `FileOutputStream` or Hadoop `FileSystem` output stream). The `data` must be a fully materialized byte array. The stream must not be closed prior to calling this method.

### Output
Returns `Unit` — modifies the provided `ZipOutputStream` in-place by appending a new uncompressed `ZipEntry` containing the provided byte array, calculating and setting the necessary CRC-32 checksum and size headers automatically.

### Valid Call Patterns
```scala
import edu.ucr.cs.bdlab.beast.util.ZipUtil
import java.util.zip.ZipOutputStream
import java.io.{File, FileOutputStream}

val file1 = new File(scratchDir, "test1.zip")
val zip1 = new ZipOutputStream(new FileOutputStream(file1))

// Write uncompressed files to the ZIP stream
ZipUtil.putStoredFile(zip1, "README.bin", Array[Byte](1, 2, 3, 4, 5, 6))
ZipUtil.putStoredFile(zip1, "data.bin", Array[Byte](1, 2, 3))

// The caller is responsible for closing the stream
zip1.close()
```

### LLM Instruction Prompt
- When writing raw byte arrays to a ZIP archive in Beast/RDPro without compression, use `ZipUtil.putStoredFile(zip, filename, data)`. Do not manually create `ZipEntry` objects or calculate CRC checksums, as this utility handles the `STORED` method requirements automatically. Always ensure the caller closes the `ZipOutputStream` after all files are added.

### Prompt Snippet
```text
ZipUtil.putStoredFile(zipStream, "filename.ext", byteArray)
```

### Common Failure Modes
- **Closed Stream Exception:** Calling this method on a `ZipOutputStream` that has already been closed will throw an `IOException`.
- **Corrupted Archive:** Failing to call `.close()` on the `ZipOutputStream` after adding all files will result in an incomplete or corrupted ZIP file that cannot be read by standard tools.
- **Duplicate Entry:** Attempting to write multiple files with the exact same `filename` to the same `ZipOutputStream` will throw a `ZipException`.

### Fix Code Hint
```scala
val zipStream = new ZipOutputStream(fileSystem.create(outPath))
try {
  ZipUtil.putStoredFile(zipStream, "tile_0_0.mvt", tileDataBytes)
} finally {
  zipStream.close() // Always close the stream to finalize the ZIP directory
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
Filters a spatial RDD to return only the vector features that intersect a specified geometric bounding box or spatial range.

### Parameters
- `rdd` (`JavaSpatialRDD` / `JavaPartitionedSpatialRDD`): The input RDD containing spatial features (explicit in the Java API overloads; in Scala, this is the implicit receiver of the extension method).
- `range` (`Geometry`): The spatial range to search for, typically provided as a JTS `Geometry`, `EnvelopeND`, or `EnvelopeNDLite`.
- `mbrCount` (`LongAccumulator`): An optional Spark accumulator used to count the number of Minimum Bounding Rectangle (MBR) tests performed during the query, useful for performance profiling. Defaults to `null`.

### Input
- **Data:** A `SpatialRDD` or `PartitionedSpatialRDD` of vector features (e.g., loaded from Shapefile, GeoJSON, or CSV).
- **Preconditions:** 
  - For optimal performance (query pruning), the input RDD should be spatially partitioned first (e.g., using `GridPartitioner` or `RSGrovePartitioner`). If it is not partitioned, a full dataset scan will occur.
  - The `range` geometry must be in the same Coordinate Reference System (CRS) as the input RDD. If they differ, the query geometry must be explicitly created with the matching SRID.

### Output
Returns `SpatialRDD` (or `PartitionedSpatialRDD` / `JavaSpatialRDD` depending on the overload) — A filtered distributed collection containing only the features that intersect the provided query range. If the input was partitioned, the output retains the partitioning scheme but typically contains fewer partitions (only those intersecting the range).

### Valid Call Patterns
```scala
// Pattern 1: Using EnvelopeNDLite (from README)
val range = new EnvelopeNDLite(2, -117.337182, 33.622048, -117.241395, 33.72865)
val matchedPolygons: RDD[IFeature] = polygons.rangeQuery(range)

// Pattern 2: Using EnvelopeND on a partitioned RDD (from test suite)
val mbr = data.summary
val gridPartitioner = new GridPartitioner(mbr, Array(2, 2))
val partitionedData = data.spatialPartition(gridPartitioner)
val filteredData = partitionedData.rangeQuery(
  new EnvelopeND(new GeometryFactory, 2, -100, 30, -90, 40)
)

// Pattern 3: Handling a specific CRS (from test suite)
val rangeWithCRS = new GeometryFactory(new PrecisionModel(), 3857)
  .toGeometry(new Envelope(-11131949.07, -10018754.17, 3503549.84, 4865942.27))
val filteredDataCRS = partitionedData.rangeQuery(rangeWithCRS)
```

### LLM Instruction Prompt
- Always call `rangeQuery` as an instance method on a `SpatialRDD` or `PartitionedSpatialRDD` in Scala (e.g., `rdd.rangeQuery(range)`).
- Pass a valid JTS `Geometry`, `EnvelopeND`, or `EnvelopeNDLite` as the `range` parameter.
- If the input RDD has a specific Coordinate Reference System (CRS), ensure the query geometry is created with the matching SRID using a `GeometryFactory`.
- To avoid duplicate results when features span multiple partitions, ensure the RDD is partitioned using a disjoint partitioner (`GridPartitioner`, `RSGrovePartitioner`, `KDTreePartitioner`, or `STRPartitioner`).

### Prompt Snippet
```text
To filter spatial features within a bounding box, use `rdd.rangeQuery(range)`. For best performance, ensure the RDD is spatially partitioned first (e.g., `rdd.spatialPartition(classOf[RSGrovePartitioner])`). The `range` can be an `EnvelopeNDLite` or a JTS `Geometry`. If your data uses a specific CRS (like EPSG:3857), construct the query geometry with a matching `GeometryFactory`.
```

### Common Failure Modes
- **CRS Mismatch:** Querying with a geometry in a different CRS than the RDD features will yield empty or incorrect results. The `rangeQuery` does not automatically reproject the bounding box.
- **Duplicate Results:** If the RDD is partitioned using a non-disjoint partitioner, features overlapping partition boundaries might be returned multiple times.
- **Unpartitioned Full Scan:** Calling `rangeQuery` on an unpartitioned RDD works but requires a full scan of the dataset, negating the performance benefits of spatial indexing.

### Fix Code Hint
```scala
// Fix CRS mismatch by assigning the correct SRID to the query geometry
val geomFactory = new GeometryFactory(new PrecisionModel(), 3857)
val range = geomFactory.toGeometry(new Envelope(minX, maxX, minY, maxY))
val filtered = rdd.rangeQuery(range)

// Fix duplicate results by ensuring disjoint partitioning before the query
val partitionedData = rdd.spatialPartition(classOf[RSGrovePartitioner])
val deduplicatedFiltered = partitionedData.rangeQuery(range)
```

## API Test: `raptorJoin`
_Grounding: doc-repaired from source (docfix)._

### Goal
USER-FACING. Performs a Raptor (Raster-Plus-Vector) join to concurrently match vector geometries (polygons, lines, points) with underlying raster pixels at scale. This is the primary operation for zonal statistics and raster masking.

### Valid Call Patterns
```scala
import edu.ucr.cs.bdlab.beast._
import edu.ucr.cs.bdlab.beast.cg.SpatialDataTypes.{SpatialRDD, RasterRDD}
import edu.ucr.cs.bdlab.raptor.RaptorJoinFeature
import org.apache.spark.rdd.RDD

// Assuming `sc` (SparkContext) is provided by the harness
// The test fixture is a multi-band raster, so the pixel type is Array[Float]
val rasterRDD: RasterRDD[Array[Float]] = sc.geoTiff[Array[Float]]("input_raster.tif")
val featuresRDD: SpatialRDD = sc.shapefile("input_vectors.shp")

// Perform the Raptor join using the implicit extension method
val joinResult: RDD[RaptorJoinFeature[Array[Float]]] = rasterRDD.raptorJoin(featuresRDD)

val count = joinResult.count()

if (count > 0) {
  val sample = joinResult.first()
  // Access the pixel value via .m, typed as Array[Float] to avoid ClassCastException
  val pixelValue: Array[Float] = sample.m
}
```

### LLM Instruction Prompt
- Use the instance method `raster.raptorJoin(vector)` for idiomatic Scala Spark pipelines.
- The test fixture raster provided by the harness is multi-band, meaning its pixel type `T` is `Array[Float]`, not a scalar `Float`.
- When accessing the pixel value via `.m` on the resulting `RaptorJoinFeature`, it must be typed as `Array[Float]` to avoid a `ClassCastException` (`[F cannot be cast to java.lang.Float`).
- Do not attempt to call `.getGeometry` on `RaptorJoinFeature` to verify integrity; restrict property access to `.m`.
- Remember the Raptor polygon predicate: pixels are only joined if their *center* falls inside the polygon.

### Prompt Snippet
```text
To perform raster-vector joins in RDPro, use `raster.raptorJoin(vector)`. The test fixture raster is multi-band, so you must load it as `sc.geoTiff[Array[Float]]`. The result is an `RDD[RaptorJoinFeature[Array[Float]]]`. Access the pixel value via the `.m` property, which must be typed as `Array[Float]` to avoid a `ClassCastException` (`[F cannot be cast to java.lang.Float`). Do not call `.getGeometry()` on `RaptorJoinFeature`; restrict property access to `.m`.
```

### Common Failure Modes
- **ClassCastException on Pixel Value:** The snippet failed at runtime with `java.lang.ClassCastException: [F cannot be cast to java.lang.Float` because it attempted to assign the pixel value (`sample.m`) to a scalar `Float`. The test fixture is a multi-band raster, meaning its pixel type `T` is `Array[Float]` (represented internally on the JVM as `[F`).
- **Guessing Undocumented Accessors:** Attempting to call `.getGeometry()` or similar undocumented methods on `RaptorJoinFeature` causes a compilation error (`value getGeometry is not a member of edu.ucr.cs.bdlab.raptor.RaptorJoinFeature`). Restrict access to `.m`.

### Fix Code Hint
```scala
// WRONG: Assuming scalar Float for a multi-band raster, causing ClassCastException
val rasterRDD = sc.geoTiff[Float]("raster.tif")
val joinResult = rasterRDD.raptorJoin(featuresRDD)
val pixelValue: Float = joinResult.first().m // Fails: [F cannot be cast to java.lang.Float

// CORRECT: Using Array[Float] for the multi-band test fixture and restricting access to .m
val rasterRDD = sc.geoTiff[Array[Float]]("raster.tif")
val joinResult = rasterRDD.raptorJoin(featuresRDD)
val pixelValue: Array[Float] = joinResult.first().m
```

## API Test: `raptorJoinFeature`

### Signature
```scala
def raptorJoinFeature[T](raster: RasterRDD[T], features: RDD[IFeature], opts: BeastOptions = new BeastOptions(), numTiles: LongAccumulator = null): RDD[RaptorJoinFeature[T]]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RaptorJoin.scala:73_

_Source doc:_ Performs a raptor join between a raster RDD and a set of features. The output contains information about all pixels that match with the set of features. @param raster the raster RDD that contains all the tiles to test @param features the set of features to join with the raster data @param opts additional options for the query processor @param numTiles an optional accumulator to count the number of tiles accesses during the query processing. @tparam T the type of the pixel values @return the set of overlaps between pixels and features

### Goal
Performs a distributed raster-vector join (Raptor join) to find all raster pixels that intersect with a set of vector features, enabling zonal statistics and spatial masking at scale.

### Parameters
- `raster` (`RasterRDD[T]`): The raster RDD containing the tiles and pixel data to test against the vector geometries.
- `features` (`RDD[IFeature]`): The set of vector features (polygons, lines, or points) to join with the raster data.
- `opts` (`BeastOptions`), default `new BeastOptions()`: Additional configuration options for the query processor.
- `numTiles` (`LongAccumulator`), default `null`: An optional Spark accumulator used to count the number of raster tiles accessed during query processing.

### Input
- **Raster Data:** A `RasterRDD[T]` loaded via `sc.geoTiff[T]` or `sc.hdfFile`. The type parameter `T` must exactly match the file's runtime pixel type (e.g., `Int` for `IntegerType`, `Float` for `FloatType`).
- **Vector Data:** An `RDD[IFeature]` loaded via context extensions like `sc.shapefile`, `sc.geojsonFile`, or `sc.readCSVPoint`.
- **Preconditions (Raptor Predicates):** The join matches geometries to pixels based on specific rules:
  - *Points* match the single pixel containing them.
  - *Lines* match pixels intersecting the line's crosshair.
  - *Polygons* match pixels whose **center** falls inside the polygon boundary.

### Output
Returns `RDD[RaptorJoinFeature[T]]` — an RDD containing the overlaps between individual raster pixels and vector features. Each record pairs a matched pixel value of type `T` with its corresponding vector feature, which can then be aggregated (e.g., grouped by feature ID) to compute zonal statistics.

### Valid Call Patterns
```scala
// Load raster with exact type matching the file
val raster: RasterRDD[Int] = sc.geoTiff[Int]("glc2000_v1_1.tif")

// Load vector features
val countries: RDD[IFeature] = sc.shapefile("ne_10m_admin_0_countries.zip")

// Perform the Raptor join using the object method
val result: RDD[RaptorJoinFeature[Int]] = RaptorJoin.raptorJoinFeature(raster, countries, new BeastOptions())

// Example aggregation: count pixels per country
val pixelCounts = result.map(x => x.feature.getAs[String]("NAME")).countByValue()
```

### LLM Instruction Prompt
- Use `RaptorJoin.raptorJoinFeature(raster, features)` to perform raster-vector joins for zonal statistics.
- **Crucial Type Rule:** The type parameter `T` of the `RasterRDD` must exactly match the underlying GeoTIFF pixel type (e.g., `Int` for IntegerType, `Float` for FloatType).
- **Crucial Matching Rule:** Remember that polygon joins only match pixels whose *center* falls inside the polygon boundary. Very small polygons may yield empty results if they do not cover any pixel centers.

### Prompt Snippet
```text
To join raster pixels with vector features for zonal statistics, use `RaptorJoin.raptorJoinFeature(raster, features)`. Ensure the raster's type parameter `T` matches the physical file type (e.g., `sc.geoTiff[Int]`). Polygons match pixels by their center point.
```

### Common Failure Modes
- **Type Mismatch Exceptions:** Loading the raster with the wrong type parameter (e.g., using `sc.geoTiff[Float]` for an integer raster) will cause runtime serialization or cast errors during the join.
- **Missing Pixel Matches for Small Polygons:** Because polygons only match pixels if the pixel's *center* falls inside the boundary, very small polygons (relative to the raster resolution) might not match any pixels, resulting in missing features in the output.
- **Incorrect Method Invocation:** Attempting to call `.raptorJoinFeature(...)` directly on the `RasterRDD` instance may fail if the implicit conversions are not in scope; always prefer the explicit `RaptorJoin.raptorJoinFeature(...)` object method.

### Fix Code Hint
```scala
// Ensure the raster type matches the file (e.g., Int)
val raster: RasterRDD[Int] = sc.geoTiff[Int]("landcover.tif")
val features: RDD[IFeature] = sc.shapefile("zones.zip")

// Call the object method directly rather than relying on implicits
val joined: RDD[RaptorJoinFeature[Int]] = RaptorJoin.raptorJoinFeature(raster, features, new BeastOptions())
```

## API Test: `raptorJoinIDFull`

### Signature
```scala
def raptorJoinIDFull[T](raster: RDD[ITile[T]], vector: RDD[(Long, IFeature)], opts: BeastOptions, numTiles: LongAccumulator = null, numRanges: LongAccumulator = null) : RDD[RaptorJoinResult[T]]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RaptorJoin.scala:180_

_Source doc:_ A Raptor join implementation that returns all the matches between features and pixels along with the raster metadata that puts the pixel in context. @param raster the RDD that contains the raster tiles @param vector the RDD that contains the vector features and their unique IDs @param opts additional options for the query processor @tparam T the type of the pixel values @return RDD that contains all overlaps between pixels and geometries

### Goal
Performs a distributed Raptor join between a raster dataset and a vector dataset, returning all pixel-geometry matches along with the pixel values, coordinates, and raster metadata for contextual analysis.

### Parameters
- `raster` (`RDD[ITile[T]]`): The RDD containing the raster tiles (e.g., loaded via `sc.geoTiff[T]` or instantiated as a `RasterFileRDD[T]`).
- `vector` (`RDD[(Long, IFeature)]`): The RDD containing the vector features paired with a unique `Long` identifier.
- `opts` (`BeastOptions`): Additional configuration options for the query processor (often just `new BeastOptions()`).
- `numTiles` (`LongAccumulator`), default `null`: An optional Spark accumulator to track the total number of raster tiles processed during the join.
- `numRanges` (`LongAccumulator`), default `null`: An optional Spark accumulator to track the total number of intersection ranges processed.

### Input
- **Raster Data:** Must be an `RDD[ITile[T]]`. The type parameter `T` must exactly match the file's runtime pixel type. Selection rules: `IntegerType` $\rightarrow$ `Int`, `FloatType` $\rightarrow$ `Float`, `ArrayType(IntegerType,true)` $\rightarrow$ `Array[Int]`, `ArrayType(FloatType, true)` $\rightarrow$ `Array[Float]`.
- **Vector Data:** Must be an `RDD[(Long, IFeature)]`. If you load vectors via `sc.shapefile` or similar (which returns `RDD[IFeature]`), you must map it to include a unique `Long` ID (e.g., using `zipWithIndex`).
- **Preconditions (Raptor Predicates):** The join matches geometries to pixels based on specific rules: Points match the single pixel containing them; Lines match pixels intersecting the line's crosshair; Polygons match pixels whose *center* falls inside the polygon boundary.

### Output
Returns `RDD[RaptorJoinResult[T]]` — an RDD representing all overlaps between pixels and geometries. Each `RaptorJoinResult` contains the pixel value (accessible via `.m`), the pixel coordinates (accessible via `.x` and `.y`), and the associated raster metadata.

### Valid Call Patterns
```scala
// Example 1: Single-band raster join
val raster: RasterFileRDD[Int] = new RasterFileRDD[Int](sparkContext, "glc2000_small.tif", new BeastOptions())
val features: RDD[IFeature] = sparkContext.parallelize(Seq(Feature.create(null, testPoly)))
val vector: RDD[(Long, IFeature)] = features.zipWithUniqueId().map(kv => (kv._2, kv._1))

val values: RDD[RaptorJoinResult[Int]] = RaptorJoin.raptorJoinIDFull(raster, vector, new BeastOptions())

// Example 2: Multiband raster join
val multiRaster: RasterFileRDD[Array[Int]] = new RasterFileRDD[Array[Int]](sparkContext, "FRClouds.tif", IRasterReader.OverrideSRID -> 4326)
val multiValues: RDD[RaptorJoinResult[Array[Int]]] = RaptorJoin.raptorJoinIDFull(multiRaster, vector, new BeastOptions())
```

### LLM Instruction Prompt
- Call `RaptorJoin.raptorJoinIDFull(raster, vector, opts)` as a method on the `RaptorJoin` object, not as an instance method on the raster RDD.
- Ensure the vector RDD is of type `RDD[(Long, IFeature)]`. If you have an `RDD[IFeature]`, you must assign unique IDs first (e.g., using `zipWithUniqueId()`).
- Ensure the generic type `T` matches the underlying raster data type exactly (e.g., `Int`, `Float`, `Array[Int]`, `Array[Float]`).

### Prompt Snippet
```text
When performing a full Raptor join to get pixel coordinates and metadata, use `RaptorJoin.raptorJoinIDFull(raster, vectorWithIds, new BeastOptions())`. The vector RDD must be mapped to `(Long, IFeature)` to provide unique IDs for the join.
```

### Common Failure Modes
- **Type Mismatch on Vector RDD:** Passing an `RDD[IFeature]` directly to `vector` will cause a compilation error. It must be `RDD[(Long, IFeature)]`.
- **Type Mismatch on Raster RDD:** Using `Int` for a float raster (or vice versa) will cause runtime casting exceptions. The type `T` must match the GeoTIFF/HDF pixel type.
- **Method Not Found:** Attempting to call `raster.raptorJoinIDFull(...)` directly on the RDD. While `raptorJoin` is available as an implicit extension, `raptorJoinIDFull` is typically called statically via the `RaptorJoin` object.

### Fix Code Hint
```scala
// WRONG: Passing RDD[IFeature] directly
// val join = RaptorJoin.raptorJoinIDFull(raster, features, new BeastOptions())

// RIGHT: Assign unique IDs to features first
val vectorWithIds: RDD[(Long, IFeature)] = features.zipWithUniqueId().map { case (f, id) => (id, f) }
val join = RaptorJoin.raptorJoinIDFull(raster, vectorWithIds, new BeastOptions())
```

## API Test: `rasterHeight`
_Grounding: doc-repaired from source (docfix)._

### Signature
```scala
def rasterHeight: Int
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/geolite/RasterMetadata.scala:52_

### Goal
Retrieves the total number of pixel rows (scanlines) in the raster layer from its metadata.
*Note: This is an ADVANCED/LOW-LEVEL internal framework API. It should be excluded from the main user-facing denominator. It is used internally for tiling and iteration.*

### Parameters
_None._

### Input
A valid `RasterMetadata` instance. Because this is an ADVANCED/LOW-LEVEL API, do not attempt to initialize a `GeoTiffReader` to obtain this metadata. Instead, construct `RasterMetadata` directly using its public constructor with standard primitive types and a `java.awt.geom.AffineTransform`.

### Output
Returns `Int` — the total vertical pixel dimension (number of rows) of the raster dataset, calculated as `y2 - y1`.

### Valid Call Patterns
```scala
import edu.ucr.cs.bdlab.beast.geolite.RasterMetadata
import java.awt.geom.AffineTransform

// Caller-owned low-level dependencies
val x1 = 0
val y1 = 0
val x2 = 1000
val y2 = 500 // Highest row index (exclusive)
val tileWidth = 256
val tileHeight = 256
val srid = 4326
val g2m = new AffineTransform() // Identity transform for grid-to-model

// Construct RasterMetadata directly
val metadata = new RasterMetadata(
  x1, y1, x2, y2, 
  tileWidth, tileHeight, 
  srid, g2m
)

val height: Int = metadata.rasterHeight
```

### LLM Instruction Prompt
- `rasterHeight` is an instance method on `RasterMetadata`.
- To test or use `rasterHeight` in isolation, do not attempt to initialize a `GeoTiffReader`. Instead, construct `RasterMetadata` directly using its public constructor: `new RasterMetadata(x1, y1, x2, y2, tileWidth, tileHeight, srid, g2m)`.
- The `g2m` parameter requires a `java.awt.geom.AffineTransform`.

### Prompt Snippet
```scala
val g2m = new java.awt.geom.AffineTransform()
val metadata = new edu.ucr.cs.bdlab.beast.geolite.RasterMetadata(0, 0, 1000, 500, 256, 256, 4326, g2m)
val rows: Int = metadata.rasterHeight
```

### Common Failure Modes
- **Missing/Incorrect Reader Imports:** Attempting to instantiate `GeoTiffReader` (e.g., from `edu.ucr.cs.bdlab.beast.io`) to access metadata. This fails because the reader class is either in a different package or unavailable in the compilation context. Bypass this by instantiating `RasterMetadata` directly.
- **Misunderstanding API Scope:** This is an ADVANCED/LOW-LEVEL API. Do not present low-level construction as the normal first-choice user workflow for reading rasters.
- **Confusing pixel dimensions with spatial extent:** Assuming `rasterHeight` returns geographic height in CRS units rather than the discrete integer count of pixel rows.

### Fix Code Hint
```scala
// WRONG: Attempting to use an unavailable reader to get metadata
// val reader = new edu.ucr.cs.bdlab.beast.io.GeoTiffReader[Float]()
// val h = reader.metadata.rasterHeight

// RIGHT: Constructing RasterMetadata directly
// val g2m = new java.awt.geom.AffineTransform()
// val metadata = new edu.ucr.cs.bdlab.beast.geolite.RasterMetadata(0, 0, 1000, 500, 256, 256, 4326, g2m)
// val h = metadata.rasterHeight
```

## API Test: `rasterWidth`
_Grounding: doc-repaired from source (docfix)._

### Goal
Retrieve the total number of pixel columns (the X-axis dimension) in a raster layer. Note: This is an ADVANCED/LOW-LEVEL internal framework API primarily used for internal plumbing (readers, writers, tile iterators). It is recommended to exclude this API from the main user-facing denominator.

### Input
A valid `RasterMetadata` object. Because this is an ADVANCED/LOW-LEVEL API, for standalone testing, this caller-owned object should be instantiated directly via its public constructor, bypassing complex I/O readers.

### Valid Call Patterns
```scala
import java.awt.geom.AffineTransform
import edu.ucr.cs.bdlab.beast.geolite.RasterMetadata

// Caller-owned objects for low-level construction
val g2m = new AffineTransform()
val metadata = new RasterMetadata(
  x1 = 0, 
  y1 = 0, 
  x2 = 1920, // highest column (exclusive)
  y2 = 1080, 
  tileWidth = 256, 
  tileHeight = 256, 
  srid = 4326, 
  g2m = g2m
)

val width: Int = metadata.rasterWidth
```

### LLM Instruction Prompt
- `RasterMetadata` can and should be instantiated directly via its public constructor `new RasterMetadata(x1, y1, x2, y2, tileWidth, tileHeight, srid, g2m)` when testing or constructing metadata manually.
- Do not attempt to instantiate `GeoTiffReader` to access this API in standalone tests, as it introduces unnecessary I/O dependencies and package resolution errors.
- `rasterWidth` is an instance method on `RasterMetadata` that calculates the width by subtracting `x1` from `x2`.

### Prompt Snippet
```text
To get the number of columns in a raster layer, access `.rasterWidth` on a `RasterMetadata` object. For testing, instantiate `RasterMetadata` directly using its public constructor rather than relying on a `GeoTiffReader`.
```

### Common Failure Modes
- **Unnecessary I/O Dependency (The failure that just happened):** Attempting to instantiate `edu.ucr.cs.bdlab.beast.io.GeoTiffReader` to obtain `RasterMetadata` in standalone tests. This fails with `error: type GeoTiffReader is not a member of package edu.ucr.cs.bd` because the reader is unavailable in the compilation context. Bypass the reader and use the public `RasterMetadata` constructor.
- **Misunderstanding API Scope:** Treating this ADVANCED/LOW-LEVEL internal API as a standard user-facing operation. It is recommended to exclude this from the main user-facing denominator.
- **Confusing pixels with map units:** Assuming `rasterWidth` returns spatial extent (e.g., degrees). It strictly returns the integer number of pixel columns (`x2 - x1`).

### Fix Code Hint
```scala
// ❌ WRONG: Attempting to use GeoTiffReader to get metadata (causes package resolution errors)
// val reader = new edu.ucr.cs.bdlab.beast.io.GeoTiffReader[Float]()
// val width = reader.metadata.rasterWidth

// ✅ CORRECT: Direct low-level construction of RasterMetadata
val g2m = new java.awt.geom.AffineTransform()
val metadata = new edu.ucr.cs.bdlab.beast.geolite.RasterMetadata(
  x1 = 0, y1 = 0, x2 = 1920, y2 = 1080,
  tileWidth = 256, tileHeight = 256, srid = 4326, g2m = g2m
)
val width: Int = metadata.rasterWidth
```

## API Test: `rasterizePixels`

### Signature
```scala
def rasterizePixels[T: ClassTag](pixels: RDD[(Int, Int, T)], metadata: RasterMetadata, rasterFeature: RasterFeature): RasterRDD[T]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsGlobal.scala:35  (+1 more definition site/overload)_

_Source doc:_ Creates a [[RasterRDD]] from a given set of pixel locations and values. @param pixels the pixel values @param metadata the metadata that describes the raster @tparam T the type of pixels @return a raster RDD that holds the given pixels

### Goal
Creates a distributed `RasterRDD` from an RDD of individual pixel coordinates and values, aligning them into tiles based on the provided spatial metadata grid.

### Parameters
- `pixels` (`RDD[(Int, Int, T)]`): A Spark RDD containing tuples of `(x, y, value)`, where `x` is the column index, `y` is the row index, and `value` is the pixel data of type `T`.
- `metadata` (`RasterMetadata`): The spatial configuration defining the raster's grid, including total width/height, tile dimensions, CRS (SRID), and the affine transform mapping pixel coordinates to geographic space.
- `rasterFeature` (`RasterFeature`): Metadata attributes for the resulting raster dataset, typically containing identifying information like the target file name.

### Input
- **Data:** An RDD of sparse or dense pixel values. The type `T` must match the runtime pixel type (e.g., `Int` for integer data, `Float` for continuous data).
- **Preconditions:** 
  - The `x` and `y` coordinates in the `pixels` RDD must fall within the bounds defined by `metadata` (i.e., `0 <= x < rasterWidth` and `0 <= y < rasterHeight`).
  - The `metadata` must specify uniform tile sizes (e.g., 90x90 or 1000x1000). According to GeoTIFF standards, all tiles must be of the same width and height, even if the last tile extends outside the raster boundary (outside pixels are filled with a fill value).

### Output
Returns `RasterRDD[T]` — A distributed raster dataset (an alias for `RDD[ITile[T]]`) partitioned into tiles. This output is ready for further RDPro operations (like `mapPixels` or `raptorJoin`) or can be saved directly to disk as a GeoTIFF using `GeoTiffWriter.saveAsGeoTiff`.

### Valid Call Patterns
```scala
// Construct metadata (x1, y1, x2, y2, tileWidth, tileHeight, srid, affineTransform)
val metadata = new RasterMetadata(0, 0, 360, 180, 90, 90, 4326, 
  new AffineTransform(1, 0, 0, -1, -180, 90))

// Create an RDD of pixel coordinates and values
val pixels = sparkContext.parallelize(Seq(
  (0, 0, 100f),
  (180, 0, 200f),
  (100, 50, 300f)
))

// Rasterize using RasterOperationsGlobal
val rasterRDD: RasterRDD[Float] = RasterOperationsGlobal.rasterizePixels(
  pixels, 
  metadata, 
  RasterFeature.create(Array("fileName"), Array("testFile.tif"))
)
```

### LLM Instruction Prompt
- When generating code to rasterize pixels, always use the 3-parameter signature `RasterOperationsGlobal.rasterizePixels(pixels, metadata, rasterFeature)`.
- Do not use the 2-parameter `sc.rasterizePixels` shorthand if the environment strictly requires the `rasterFeature` argument.
- Create the `rasterFeature` argument using `RasterFeature.create(Array("fileName"), Array("your_filename.tif"))`.
- Ensure the type parameter `T` (e.g., `Float`, `Int`) exactly matches the type of the values in the `pixels` RDD.

### Prompt Snippet
```text
To convert an RDD of (x, y, value) tuples into a RasterRDD, use `RasterOperationsGlobal.rasterizePixels(pixels, metadata, rasterFeature)`. You must provide a `RasterMetadata` object defining the grid and tile sizes, and a `RasterFeature` created via `RasterFeature.create(Array("fileName"), Array("out.tif"))`. Ensure the generic type `T` matches your pixel data type.
```

### Common Failure Modes
- **Missing `rasterFeature` Argument:** Attempting to call `rasterizePixels(pixels, metadata)` based on outdated documentation, resulting in a compilation error due to the missing third parameter.
- **Type Mismatch:** Providing an RDD of `(Int, Int, Double)` but expecting a `RasterRDD[Float]`. RDPro strictly binds the generic type `T` to the underlying GeoTIFF tile types (e.g., `FloatType` -> `Float`).
- **Out-of-Bounds Pixels:** Providing pixel coordinates `(x, y)` that exceed the `rasterWidth` or `rasterHeight` defined in the `RasterMetadata`, which may cause out-of-bounds exceptions during tile assignment.

### Fix Code Hint
```scala
// FIX: Ensure all 3 parameters are passed and types match exactly
val metadata = RasterMetadata.create(-180, 90, 180, -90, 4326, 360, 180, 90, 90)
val feature = RasterFeature.create(Array("fileName"), Array("output.tif"))

// If pixels are Float, the RDD and the method type parameter must be Float
val pixels: RDD[(Int, Int, Float)] = sc.parallelize(Seq((0, 0, 1.5f)))
val raster = RasterOperationsGlobal.rasterizePixels[Float](pixels, metadata, feature)
```

## API Test: `rasterizePoints`
_Grounding: doc-repaired from source (docfix)._

### Goal
Converts a distributed collection of spatial point coordinates and their associated values into a distributed raster dataset (`RasterRDD`) based on a defined spatial grid. This is a core user-facing data-ingestion operation.

### Valid Call Patterns
```scala
import org.apache.spark.rdd.RDD
import edu.ucr.cs.bdlab.beast.geolite.RasterMetadata
import edu.ucr.cs.bdlab.beast.geolite.RasterFeature
import edu.ucr.cs.bdlab.beast.cg.SpatialDataTypes.RasterRDD

// 1. Define the target grid metadata (x1, y1, x2, y2, srid, rasterWidth, rasterHeight, tileWidth, tileHeight)
val metadata = RasterMetadata.create(0, 0, 6, 4, 4326, 60, 40, 60, 40)

// 2. Create an RDD of (X, Y, Value)
val pixels: RDD[(Double, Double, Int)] = sc.parallelize(Seq(
  (2.20, 1.7, 100),
  (2.7, 2.0, 50),
  (5.3, 2.2, 25)
))

// 3. Call rasterizePoints. 
// The third argument (rasterFeature) is mandatory and has no default value.
// You MUST explicitly pass null if you do not have a RasterFeature.
val raster: RasterRDD[Int] = sc.rasterizePoints(pixels, metadata, null)
```

### LLM Instruction Prompt
- The `rasterizePoints` method strictly requires exactly three arguments: `points`, `metadata`, and `rasterFeature`.
- There is no two-argument overload or default value for `rasterFeature`, even when calling it as an implicit extension on `SparkContext`.
- If you do not have a `RasterFeature` to provide, you MUST explicitly pass `null` as the third argument (e.g., `sc.rasterizePoints(pixels, metadata, null)`).
- Never suggest or generate `sc.rasterizePoints(pixels, metadata)`.
- Always construct a `RasterMetadata` object first to define the target grid's bounds, SRID, and tile sizes.

### Prompt Snippet
```text
Create a RasterMetadata object for SRID 4326 with bounds (-124, 42) to (-114, 32) and tile size 100x100. Then, given an RDD of (Double, Double, Float) named `pointData`, rasterize it into a RasterRDD[Float] using `sc.rasterizePoints`, explicitly passing `null` for the third argument.
```

### Common Failure Modes
- **"Not enough arguments" compilation error:** Omitting the third argument (`rasterFeature`) causes a fatal compilation error. There is no default value. You must pass `null` (e.g., `sc.rasterizePoints(pixels, metadata, null)`).
- **Type Mismatch:** Providing an `RDD[(Double, Double, Double)]` but expecting a `RasterRDD[Float]` or `RasterRDD[Int]`. The type `T` must be consistent and align with supported GeoTIFF pixel types if saving the output.
- **Out of Bounds:** Points in the RDD that fall outside the spatial envelope defined in `RasterMetadata` will not be rasterized into the resulting tiles.

### Fix Code Hint
```scala
// BAD: Missing the third argument (causes "not enough arguments for method rasterizePoints" error)
val raster = sc.rasterizePoints(pixels, metadata)

// GOOD: Explicitly pass null for the mandatory rasterFeature argument
val raster = sc.rasterizePoints(pixels, metadata, null)
```

## API Test: `readCSVPoint`
_Grounding: doc-repaired from source (docfix)._

### Goal
Reads point geometries from a CSV file into a distributed `SpatialRDD` by specifying the columns containing the X (longitude) and Y (latitude) coordinates. This is a primary user-facing data-ingestion method.

### Valid Call Patterns
```scala
import edu.ucr.cs.bdlab.beast.cg.SpatialDataTypes.SpatialRDD

// Use the provided harness fixture (e.g., csv_path) instead of creating a mock file.
// When exact column names are unknown, use integer indices and explicitly skip the header.
val pointsRDD: SpatialRDD = sc.readCSVPoint(
  filename = csv_path,
  xColumn = 0,
  yColumn = 1,
  skipHeader = true
)

val count = pointsRDD.count()
```

### LLM Instruction Prompt
- Never generate mock CSV files at runtime using Java I/O; always use the provided `csv_path` fixture for input data.
- Spark's distributed readers require files to be accessible across all executors, which dynamically created local files may not be.
- When using a generic CSV fixture where exact column names are unknown, use integer indices (e.g., `xColumn = 0, yColumn = 1`) and explicitly set `skipHeader = true`.
- Always call `readCSVPoint` as an extension method on an initialized `SparkContext` (e.g., `sc.readCSVPoint(...)`).
- If passing `xColumn` or `yColumn` as `String` names, Beast automatically assumes a header exists and ignores `skipHeader`.

### Prompt Snippet
```text
Use `sc.readCSVPoint(csv_path, xColumn = 0, yColumn = 1, skipHeader = true)` to load CSV point data into a SpatialRDD. Never generate mock CSV files using Java I/O; always use the provided `csv_path` fixture, as Spark distributed readers cannot reliably access dynamically created local files across executors.
```

### Common Failure Modes
- **FileNotFoundException (Dynamic Local Files):** Attempting to dynamically generate a CSV file at runtime using standard Java I/O (e.g., `new PrintWriter("test.csv")`) and reading it back. Spark's distributed file reader fails to resolve dynamically created local files across executors. You must use the provided `csv_path` fixture.
- **Header Parsing Errors:** Using integer indices for `xColumn` and `yColumn` on a CSV that has a header row, but forgetting to set `skipHeader = true`. This causes Beast to attempt to parse the string header names as numeric coordinates.
- **Missing SparkContext:** Attempting to call `readCSVPoint(...)` as a standalone function rather than a method on `SparkContext`.

### Fix Code Hint
```scala
// WRONG: Generating a local mock file with Java I/O (causes FileNotFoundException on executors)
import java.io.PrintWriter
new PrintWriter("mock.csv") { write("x,y\n1,2"); close() }
val points = sc.readCSVPoint("mock.csv", xColumn = 0, yColumn = 1)

// CORRECT: Use the provided harness fixture and explicitly skip the header
val points = sc.readCSVPoint(csv_path, xColumn = 0, yColumn = 1, skipHeader = true)
```

## API Test: `readConfigurationXML`

### Signature
```scala
def readConfigurationXML(filename: String): java.util.Map[String, java.util.List[String]]
```
_Source: beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/util/OperationHelper.scala:60_

_Source doc:_ Read all XML configuration files of the given name in the class path and merge them into one object. This method internally caches the configuration so it does not have to be loaded multiple times. The XML is organized in three levels. The first level is the root element and it is always &lt;beast&gt;. The second level is a name of a collection, e.g., &lt;Indexers&gt;. Finally, the third level contains the contents of the collection in their text part. @param filename A path to an XML file that contains the configuration. @return the beast configuration as a map from each key to all values under this key.

### Goal
Reads, merges, and caches XML configuration files from the classpath into a map, organizing Beast configuration properties by their collection names.

### Parameters
- `filename` (`String`): The name or path of the XML configuration file to locate within the classpath (e.g., `"test-beast.xml"`).

### Input
An XML file present in the Java classpath. The XML must strictly follow a three-level hierarchy:
1. The root element must be `<beast>`.
2. The second level defines the collection name (e.g., `<Indexers>`, `<Operations>`), which becomes the map key.
3. The third level contains the actual configuration values in their text part, which populate the list for that key.

### Output
Returns `java.util.Map[String, java.util.List[String]]` — A Java Map where each key is a collection name (from the second-level XML tags) and the value is a Java List of strings representing the text contents of the third-level elements under that key.

### Valid Call Patterns
```scala
import edu.ucr.cs.bdlab.beast.util.OperationHelper
import java.util

// Read configuration from the classpath
val conf: util.Map[String, util.List[String]] = OperationHelper.readConfigurationXML("test-beast.xml")

// Access values using standard Java Map/List methods
val operations: util.List[String] = conf.get("Operations")
val firstOp: String = operations.get(0)
```

### LLM Instruction Prompt
- Use `OperationHelper.readConfigurationXML(filename)` to load Beast XML configurations from the classpath.
- Remember that the return type is a `java.util.Map` containing `java.util.List` values, not Scala collections. You must use Java collection methods (e.g., `.get()`, `.size()`) or explicitly convert them using Scala's Java converters if idiomatic Scala operations are required.
- Do not invent configuration file paths; use the exact filename expected in the classpath.

### Prompt Snippet
```text
To load Beast XML configurations, use `OperationHelper.readConfigurationXML("filename.xml")`. It parses a 3-level XML (`<beast>` -> `<Collection>` -> `<Item>value</Item>`) and returns a `java.util.Map[String, java.util.List[String]]`. Use Java collection methods to access the keys.
```

### Common Failure Modes
- **NullPointerException on Missing Keys:** Because the method returns a `java.util.Map`, calling `.get("NonExistentKey")` returns `null` rather than a Scala `Option`. Attempting to call `.size()` or `.get(0)` on the result will throw an NPE.
- **Malformed XML Structure:** If the XML does not have `<beast>` as the root element or lacks the required three-level depth, the configuration will not parse correctly into the expected Map/List structure.
- **File Not in Classpath:** Providing a local filesystem path instead of a classpath-relative filename will result in the file not being found, as the method specifically searches the classpath.

### Fix Code Hint
```scala
// WRONG: Using Scala map methods or assuming the key always exists
val conf = OperationHelper.readConfigurationXML("beast.xml")
val ops = conf.getOrElse("Operations", List()) // Fails: java.util.Map has no getOrElse

// RIGHT: Handling the Java Map safely
val conf: java.util.Map[String, java.util.List[String]] = OperationHelper.readConfigurationXML("beast.xml")
val opsList = conf.get("Operations")
if (opsList != null && opsList.size() > 0) {
  val firstOp = opsList.get(0)
  println(s"First operation: $firstOp")
}
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
Loads spatial vector data from a specified file or directory into a distributed Spark RDD, supporting various formats like shapefile, GeoJSON, and CSV.

### Parameters
- `sc` (`JavaSparkContext` or `SparkContext`): The active Spark context used to distribute the data loading.
- `opts` (`BeastOptions`): Configuration options for the reader (e.g., CSV parsing options). Can be empty (`new BeastOptions()`).
- `filename` (`String`): The path to the input file or directory (e.g., `"input.zip"`, `"Tweets.geojson.gz"`).
- `iFormat` (`String`): The string identifier for the input format (e.g., `"shapefile"`, `"geojson"`, `"csv"`).

### Input
Vector data files accessible to the Spark cluster. Supported input formats include CSV (points, WKT, envelopes), Esri Shapefile (compressed `.zip` or uncompressed), GeoJSON, JSON+WKT, and GPX. 
*Precondition:* This function is strictly for vector data. Raster data (GeoTIFF, HDF) must be loaded using raster-specific APIs like `sc.geoTiff[T]` or `new RasterFileRDD`.

### Output
Returns `JavaSpatialRDD` (or `SpatialRDD` for the Scala overload) — representing a distributed collection of spatial features (`IFeature`), which contain both geometries and their associated attributes.

### Valid Call Patterns
```scala
// Scala usage (from test suite)
val vectorFile = locateResource("/vectors/ne_110m_admin_1_states_provinces.zip")
val polygons: RDD[IFeature] = SpatialReader.readInput(sparkContext, new BeastOptions(), vectorFile.getPath, "shapefile")

// Java usage (from README)
JavaRDD<IFeature> points = SpatialReader.readInput(sparkContext, new BeastOptions(), "Tweets.geojson.gz", "geojson");
```

### LLM Instruction Prompt
- Use `SpatialReader.readInput` to load vector datasets when an explicit format string is required or when writing Java code.
- Always provide an instantiated `BeastOptions` object (e.g., `new BeastOptions()`) as the second argument.
- Ensure the `iFormat` string exactly matches the intended vector format (e.g., `"shapefile"`, `"geojson"`).
- Do NOT use `readInput` for raster files (GeoTIFF/HDF); use `sc.geoTiff[T]` instead.
- Do not invent file paths; use only provided input variables.

### Prompt Snippet
```text
To load vector data explicitly by format, use `SpatialReader.readInput(sc, new BeastOptions(), path, format)`. Valid formats include "shapefile", "geojson", and "csv". Do not use this for rasters.
```

### Common Failure Modes
- **Passing Raster Files:** Attempting to load a GeoTIFF or HDF file using `readInput`. This will fail because `readInput` expects vector formats. Rasters require `sc.geoTiff[T]`.
- **Missing `BeastOptions`:** Forgetting the `opts` parameter. The signature strictly requires a `BeastOptions` instance, even if no custom options are needed.
- **Mismatched Format String:** Providing an `iFormat` string that does not match the actual file contents (e.g., passing `"csv"` for a `.geojson` file).
- **CSV Geometry Auto-detection Failure:** When loading CSVs, geometry column auto-detection is a "best-effort" guess. If it fails, the resulting features may lack valid geometries unless explicitly configured in `BeastOptions`.

### Fix Code Hint
```scala
// ❌ BAD: Missing BeastOptions and using readInput for a raster
val raster = SpatialReader.readInput(sc, "image.tif", "geotiff")

// ✅ GOOD: Using readInput correctly for vectors with BeastOptions
val polygons: RDD[IFeature] = SpatialReader.readInput(sc, new BeastOptions(), "input.zip", "shapefile")

// ✅ GOOD: Using the correct API for rasters
val raster: RDD[ITile[Int]] = sc.geoTiff[Int]("image.tif")
```

## API Test: `readLocal`

### Signature
```scala
def readLocal(path: String, iformat: String, opts: BeastOptions, conf: Configuration): Iterator[IFeature]
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/SpatialFileRDD.scala:492_

_Source doc:_ Reads the given path locally without creating any RDDs. Useful for reading a small file when SparkContext is not accessible, e.g., inside a mapPartition function. @param path path to a single file or a directory @param iformat the format of the data @param opts additional options for reading the file @return an iterator to features in the given path

### Goal
Reads spatial vector data from a local file or directory directly into a local Scala iterator without creating a Spark RDD, which is ideal for loading small auxiliary datasets inside distributed operations (like `mapPartitions`).

### Parameters
- `path` (`String`): The path to a single file or a directory containing the spatial data to be read.
- `iformat` (`String`): The format identifier of the data (e.g., `"wkt(1)"`, `"shapefile"`, `"geojson"`).
- `opts` (`BeastOptions`): Additional configuration options for reading the file (e.g., skipping headers or setting separators). Can often be passed as a `Seq` of key-value pairs via implicit conversion.
- `conf` (`Configuration`): The Hadoop `Configuration` object, typically obtained via `sparkContext.hadoopConfiguration`.

### Input
A local file path or directory containing supported vector data (such as CSV, Shapefile, or GeoJSON). 
**Preconditions:** 
- The file must be physically accessible on the node executing the code. If `readLocal` is called inside a Spark task (e.g., `mapPartitions`), the file must exist on that specific worker node's local filesystem, or be accessible via a shared mount/HDFS path that the worker can resolve locally.
- The `iformat` string must correctly match the underlying data format.

### Output
Returns `Iterator[IFeature]` — a local, non-distributed Scala iterator over the spatial features parsed from the specified path.

### Valid Call Patterns
```scala
// From the project's test suite (using implicit Seq to BeastOptions conversion)
val input = new File(scratchDir, "inputdir")
val features = SpatialFileRDD.readLocal(
  input.getPath, 
  "wkt(1)",
  Seq(CSVFeatureReader.SkipHeader -> true, CSVFeatureReader.FieldSeparator -> '\t'), 
  sparkContext.hadoopConfiguration
)
```

### LLM Instruction Prompt
- Use `SpatialFileRDD.readLocal` ONLY when you need to read a small spatial file directly into local memory (e.g., inside a `mapPartitions` block where `SparkContext` is unavailable).
- Do not use `readLocal` for large datasets; use SparkContext extensions like `sc.shapefile` or `sc.geojsonFile` to leverage distributed partitioning.
- Always pass `sparkContext.hadoopConfiguration` for the `conf` parameter if executing on the driver.
- Ensure the `iformat` string accurately reflects the geometry column index or format (e.g., `"wkt(1)"` for WKT in the second column).

### Prompt Snippet
```text
`SpatialFileRDD.readLocal(path, iformat, opts, conf)` reads a spatial file directly into an `Iterator[IFeature]` without creating an RDD. Use this for loading small auxiliary files inside `mapPartitions` where `SparkContext` is inaccessible. Requires a Hadoop `Configuration` (e.g., `sc.hadoopConfiguration`).
```

### Common Failure Modes
- **FileNotFoundException on Workers:** Calling `readLocal` inside a distributed Spark transformation with a local file path (e.g., `C:\data\file.csv`) that only exists on the driver machine, causing worker nodes to fail when they attempt to resolve the path.
- **Memory Exhaustion (OOM):** Attempting to read a massive vector dataset using `readLocal` and converting the resulting `Iterator` to a `List` or `Array`, bypassing Spark's distributed memory management and crashing the JVM.
- **Format Parsing Errors:** Providing an incorrect `iformat` (like `"csv"` instead of `"wkt(1)"`) or failing to provide necessary `BeastOptions` (like `CSVFeatureReader.SkipHeader -> true`), causing the parser to fail on the header row or misinterpret geometry columns.

### Fix Code Hint
```scala
// ❌ BAD: Using readLocal for a large dataset on the driver, losing distributed processing
val largeDataIter = SpatialFileRDD.readLocal("hdfs:///large_polygons.shp", "shapefile", new BeastOptions(), sc.hadoopConfiguration)
val largeDataRDD = sc.parallelize(largeDataIter.toSeq) // OOM risk!

// ✅ GOOD: Use SparkContext extensions for large distributed loads
val largeDataRDD = sc.shapefile("hdfs:///large_polygons.shp")

// ✅ GOOD: Using readLocal inside mapPartitions for a small, locally distributed file
val joined = largeDataRDD.mapPartitions { partition =>
  // Assuming "small_reference.csv" was distributed to workers via SparkFiles
  val localRef = SpatialFileRDD.readLocal(SparkFiles.get("small_reference.csv"), "wkt(0)", new BeastOptions(), new Configuration()).toList
  // ... perform local operations ...
}
```

## API Test: `readPartition`

### Signature
```scala
def readPartition(partition: FilePartition, featureReaderClass: Class[_ <: FeatureReader], applyDuplicateAvoidance: Boolean, opts: BeastOptions): Iterator[IFeature]
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/SpatialFileRDD.scala:441_

_Source doc:_ Reads the given partition @param partition the partition to read @param featureReaderClass the class of the feature reader @param opts the user options @return an iterator to the features

### Goal
Reads a specific file partition of spatial data using a designated feature reader and returns an iterator of spatial features, acting as the internal plumbing for distributed vector data loading in Beast.

### Parameters
- `partition` (`FilePartition`): The specific chunk or partition of the file to read, typically generated by `SpatialFileRDD.createPartitions`.
- `featureReaderClass` (`Class[_ <: FeatureReader],
                    applyDuplicateAvoidance: Boolean, opts: BeastOptions`): This parameter block encompasses three arguments from the signature:
  1. `featureReaderClass`: The class of the reader responsible for parsing the specific file format (e.g., GeoJSON, Shapefile), usually obtained via `SpatialFileRDD.getFeatureReaderClass`.
  2. `applyDuplicateAvoidance`: A boolean flag indicating whether to filter out duplicate features that might span across multiple non-disjoint partitions.
  3. `opts`: The `BeastOptions` containing user configurations, such as the input format.

### Input
The caller must provide a valid `FilePartition` pointing to a supported vector data file (e.g., CSV, Esri Shapefile, GeoJSON, JSON+WKT). The `featureReaderClass` must exactly match the format of the data being read. The `opts` must be configured with the correct format (e.g., `SpatialFileRDD.InputFormat -> "geojson"`). 

### Output
Returns `Iterator[IFeature]` — an iterator over the spatial features (geometries and their associated attributes) contained within the specified file partition.

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
- Call `readPartition` as a method on the `SpatialFileRDD` object.
- Do not call this method in standard high-level Spark pipelines; prefer context extensions like `sc.shapefile` or `sc.geojsonFile` unless you are explicitly writing custom partition iteration logic.
- Always derive the `featureReaderClass` dynamically using `SpatialFileRDD.getFeatureReaderClass(path, opts)` rather than hardcoding a reader class.
- Set `applyDuplicateAvoidance` to `true` if the partitions are not strictly disjoint to prevent double-counting features that intersect partition boundaries.

### Prompt Snippet
```text
When manually iterating over spatial file partitions in Beast, use `SpatialFileRDD.readPartition(partition, readerClass, applyDuplicateAvoidance, opts)`. Ensure you first generate the partitions using `SpatialFileRDD.createPartitions` and obtain the correct reader class via `SpatialFileRDD.getFeatureReaderClass`.
```

### Common Failure Modes
- **Mismatched Reader Class:** Passing a `featureReaderClass` that does not match the actual file format (e.g., using a Shapefile reader for a GeoJSON partition), resulting in parsing errors.
- **Missing Input Format Option:** Failing to set `SpatialFileRDD.InputFormat` in the `BeastOptions`, causing the system to fail to resolve the correct `featureReaderClass`.
- **Duplicate Features:** Setting `applyDuplicateAvoidance` to `false` when reading from non-disjoint partitions, which can cause features spanning multiple partitions to be yielded multiple times.

### Fix Code Hint
```scala
// Ensure options and reader class are correctly initialized before reading
val opts = new BeastOptions().set(SpatialFileRDD.InputFormat, "geojson")
val readerClass = SpatialFileRDD.getFeatureReaderClass(filePath, opts)
val partitions = SpatialFileRDD.createPartitions(filePath, opts, sc.hadoopConfiguration)

// Read the first partition safely with duplicate avoidance enabled
val firstPartitionFeatures = SpatialFileRDD.readPartition(partitions(0), readerClass, true, opts)
```

## API Test: `readTile`
_Grounding: doc-repaired from source (docfix)._

### Goal
**ADVANCED/LOW-LEVEL API.** This is internal framework plumbing used to fetch physical chunks of raster data. It should be excluded from the main user-facing benchmark denominator (standard users should use RDD/DataFrame APIs like `sc.geoTiff`). For testing or low-level access, it reads a specific spatial chunk (tile) from an initialized file into an independent, memory-resident `ITile[T]` object that remains valid after the reader is closed.

### Valid Call Patterns
**Explicit Low-Level Construction:** The caller owns the instantiated reader and must explicitly close it.

```scala
import org.apache.hadoop.fs.Path
import edu.ucr.cs.bdlab.beast.common.BeastOptions
import edu.ucr.cs.bdlab.raptor.GeoTiffReader
import edu.ucr.cs.bdlab.beast.geolite.ITile

// Assuming `sc` (SparkContext) and `raster_file` (String path) are provided by the harness
val path = new Path(raster_file)
val fs = path.getFileSystem(sc.hadoopConfiguration)

// 1. Caller-owned low-level reader construction
val reader = new GeoTiffReader[Int]()

try {
  // 2. Initialize with FileSystem, path, layer ("0"), and options
  reader.initialize(fs, raster_file, "0", new BeastOptions())
  
  // 3. Obtain a valid tileID dynamically from metadata
  val tileID = reader.metadata.getTileIDAtPixel(0, 0)
  
  // 4. Read the tile
  val tile: ITile[Int] = reader.readTile(tileID)
  
  // 5. Access valid properties
  val width = tile.tileWidth
  val height = tile.tileHeight
  println(s"__CHECK__ readTile width=$width, height=$height")
} finally {
  reader.close() // Tile remains valid after closing
}
```

### LLM Instruction Prompt
- This is an ADVANCED/LOW-LEVEL API. Explicitly instantiate `GeoTiffReader[T]` (e.g., `GeoTiffReader[Int]()`), initialize it, and close it in a `finally` block.
- Do not use `HDF4Reader` or `hdf_file` for this test; `HDF4Reader` does not take type parameters. Use `GeoTiffReader[T]` and `raster_file`.
- `ITile` MUST be imported from `edu.ucr.cs.bdlab.beast.geolite.ITile`, NOT from the `raptor` package.
- To check the size of the returned `ITile`, use `tile.tileWidth` and `tile.tileHeight`. Do not invent properties like `numPixels`.
- Always obtain the `tileID` dynamically from `reader.metadata.getTileIDAtPixel(x, y)`.

### Prompt Snippet
To read a specific tile, use low-level construction: instantiate `GeoTiffReader[T]` (do not use `HDF4Reader`), call `initialize(fs, path, "0", new BeastOptions())`, and get a valid ID via `reader.metadata.getTileIDAtPixel(0, 0)`. Call `reader.readTile(tileID)` to get an `edu.ucr.cs.bdlab.beast.geolite.ITile[T]`. Check size using `tile.tileWidth` and `tile.tileHeight` (do not invent `numPixels`). Close the reader in a `finally` block.

### Common Failure Modes
- **Wrong Reader / Type Parameter (Just Happened):** Instantiating `HDF4Reader[Int]()` which fails because `HDF4Reader` does not take type parameters. Use `GeoTiffReader[Int]()` instead.
- **Wrong Import Package (Just Happened):** Guessing `edu.ucr.cs.bdlab.raptor.ITile`. The correct fully qualified name is `edu.ucr.cs.bdlab.beast.geolite.ITile`.
- **Inventing Properties (Just Happened):** Guessing a non-existent `numPixels` property on `ITile` instead of using the actual `tileWidth` and `tileHeight` properties.
- **ADVANCED/LOW-LEVEL Misuse:** Attempting to call this on high-level Spark objects instead of explicitly constructing a `GeoTiffReader`.

### Fix Code Hint
**Wrong:**
```scala
import edu.ucr.cs.bdlab.raptor.ITile // WRONG PACKAGE
import edu.ucr.cs.bdlab.raptor.HDF4Reader

// ...
val reader = new HDF4Reader[Int]() // WRONG: HDF4Reader does not take type parameters
// ...
val tile: ITile[Int] = reader.readTile(tileID)
val pixels = tile.numPixels // INVENTED PROPERTY
```

**Correct:**
```scala
import edu.ucr.cs.bdlab.beast.geolite.ITile // CORRECT PACKAGE
import edu.ucr.cs.bdlab.raptor.GeoTiffReader

// ...
val reader = new GeoTiffReader[Int]() // CORRECT
// ...
val tile: ITile[Int] = reader.readTile(tileID)
val width = tile.tileWidth
val height = tile.tileHeight
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
Reads a delimited text file (such as CSV or TSV) containing Well-Known Text (WKT) geometries into a distributed `SpatialRDD` of vector features.

### Parameters
- `filename` (`String`): The path to the input file or directory containing the WKT data.
- `wktColumn` (`Any`): The column containing the WKT-encoded geometry. This can be an `Integer` representing the 0-based index of the column, or a `String` representing the column's name.
- `delimiter` (`Char`), default `'\t'`: The character used to separate fields in the file (defaults to a tab character).
- `skipHeader` (`Boolean`), default `false`: Whether to skip the first line of the file. **Precondition:** If `wktColumn` is provided as a `String`, this parameter *must* be set to `true`.

### Input
A delimited text file (e.g., CSV, TSV) containing WKT-encoded geometries. The caller must have an initialized `SparkContext` (typically `sc` or `sparkContext`) with Beast context extensions loaded.

### Output
Returns `SpatialRDD` — a distributed Spark RDD of spatial features (`RDD[IFeature]`) parsed from the input file, ready for spatial partitioning, joins, or Raptor raster-vector operations.

### Valid Call Patterns
```scala
// Using an integer column index (0-based) with default tab delimiter
val data: RDD[IFeature] = sparkContext.readWKTFile(testFile.getPath, 0)

// Using a string column name with a comma delimiter (requires skipHeader = true)
val data: RDD[IFeature] = sc.readWKTFile("data.csv", "geometry", ',', true)
```

### LLM Instruction Prompt
- Call `sc.readWKTFile(filename, wktColumn)` to load WKT geometries from delimited text files.
- **CRITICAL:** If `wktColumn` is a `String` (column name), you MUST explicitly set `skipHeader = true`.
- If the file is a standard CSV, you MUST override the default tab delimiter by passing `delimiter = ','`.
- The receiver is always the SparkContext (`sc` or `sparkContext`).

### Prompt Snippet
```text
When loading WKT files using `sc.readWKTFile`, remember that the default delimiter is a tab ('\t'). If reading a CSV, pass `','` as the third argument. If specifying the WKT column by name (String) instead of index (Integer), you must set the fourth argument `skipHeader` to `true`.
```

### Common Failure Modes
- **Header Parsing Error:** Passing a `String` for `wktColumn` but leaving `skipHeader` as `false` (the default). Beast requires the header to be skipped to resolve the column name correctly.
- **Delimiter Mismatch:** Calling `sc.readWKTFile("file.csv", 0)` on a comma-separated file without specifying `delimiter = ','`. The parser will default to tab-separated and fail to extract the geometry.

### Fix Code Hint
```scala
// BAD: String column name without skipHeader=true, and missing comma delimiter for CSV
val badData = sc.readWKTFile("polygons.csv", "wkt_geom")

// GOOD: Explicitly providing the delimiter and setting skipHeader to true
val goodData = sc.readWKTFile("polygons.csv", "wkt_geom", ',', true)
```

## API Test: `reproject`
_Grounding: doc-repaired from source (docfix)._

### Goal
Reproject a distributed raster dataset (`RasterRDD`) to a new target Coordinate Reference System (CRS) while maintaining the original pixel resolution. This is a primary, user-facing transformation for geospatial data alignment.

### Valid Call Patterns
```scala
import org.geotools.referencing.CRS
import edu.ucr.cs.bdlab.raptor.RasterOperationsFocal
import edu.ucr.cs.bdlab.raptor.RasterOperationsFocal.InterpolationMethod

// Assuming rasterRDD is a loaded RasterRDD[Float] provided by the harness
val targetCRS = CRS.decode("EPSG:4326")

// Call the object method directly to avoid relying on implicit extension methods
val reprojected = RasterOperationsFocal.reproject(
  rasterRDD,
  targetCRS,
  unifiedRaster = false,
  interpolationMethod = InterpolationMethod.Average
)

val count = reprojected.count()
val firstTile = reprojected.first()

assert(count > 0, "Reprojected RasterRDD should contain tiles")
// Must use .rasterMetadata, not .metadata
assert(firstTile.rasterMetadata.srid == 4326, s"Expected SRID 4326, but got ${firstTile.rasterMetadata.srid}")

println(s"__CHECK__ reproject count: $count, first tile SRID: ${firstTile.rasterMetadata.srid}")
```

### LLM Instruction Prompt
- To call `reproject`, use `RasterOperationsFocal.reproject(rasterRDD, targetCRS, ...)` directly to avoid missing implicit extension methods. Alternatively, ensure `import edu.ucr.cs.bdlab.beast._` is present to use it as an extension method.
- The interpolation method enum is nested inside the object, so its path is `edu.ucr.cs.bdlab.raptor.RasterOperationsFocal.InterpolationMethod`.
- To access the metadata of an `ITile` object, you MUST use the `.rasterMetadata` property (e.g., `tile.rasterMetadata.srid`), never `.metadata`.
- Pass a decoded CRS object (e.g., `CRS.decode("EPSG:4326")`).

### Prompt Snippet
```text
To reproject a RasterRDD, call `RasterOperationsFocal.reproject(raster, CRS.decode("EPSG:4326"), unifiedRaster = false, interpolationMethod = RasterOperationsFocal.InterpolationMethod.Average)`. To access tile metadata, use `tile.rasterMetadata`, never `tile.metadata`.
```

### Common Failure Modes
- **Missing Extension Method / Implicit Conversion:** Attempting to call `rasterRDD.reproject(...)` without `import edu.ucr.cs.bdlab.beast._`. Fix by calling `RasterOperationsFocal.reproject(...)` directly.
- **Invalid InterpolationMethod Import:** Attempting to import `edu.ucr.cs.bdlab.raptor.InterpolationMethod`. It is not a top-level package object; it is nested inside `RasterOperationsFocal`.
- **Invalid Tile Metadata Access:** Attempting to access `.metadata` on an `ITile` object (e.g., `firstTile.metadata.srid`). This causes a compilation error (`value metadata is not a member of edu.ucr.cs.bdlab.beast.geolite.ITile`). The correct property is `.rasterMetadata`.

### Fix Code Hint
```scala
// Wrong: Missing extension method import, wrong enum import, and wrong metadata property
import edu.ucr.cs.bdlab.raptor.InterpolationMethod
val reprojected = rasterRDD.reproject(targetCRS, false, InterpolationMethod.Average)
val srid = reprojected.first().metadata.srid

// Correct: Direct object call, correct nested enum import, and .rasterMetadata
import edu.ucr.cs.bdlab.raptor.RasterOperationsFocal
import edu.ucr.cs.bdlab.raptor.RasterOperationsFocal.InterpolationMethod
val reprojected = RasterOperationsFocal.reproject(rasterRDD, targetCRS, false, InterpolationMethod.Average)
val srid = reprojected.first().rasterMetadata.srid
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
Transforms a spatial bounding box (`Envelope`) from one Coordinate Reference System (CRS/SRID) to another, ensuring spatial queries, raster reshaping, and vector alignments use matching coordinate spaces.

### Parameters
- `envelope` (`Envelope`): The JTS `Envelope` representing the bounding box with dimensions in the source coordinate system.
- `sourceSRID` (`Int`): The integer EPSG code (e.g., `4326` for WGS84) of the input envelope. In the overloaded method, this is a GeoTools `CoordinateReferenceSystem` object.
- `targetSRID` (`Int`): The desired integer EPSG code (e.g., `3857` for Web Mercator) for the output envelope. In the overloaded method, this is a GeoTools `CoordinateReferenceSystem` object.

### Input
A valid JTS `Envelope` object and valid source/target EPSG codes (or instantiated `CoordinateReferenceSystem` objects). The coordinates in the envelope must fall within the valid bounds of the `sourceSRID`.

### Output
Returns `Envelope` — A new JTS `Envelope` representing the minimum bounding box that fully contains the reprojected corners and edges of the original envelope in the target coordinate reference system.

### Valid Call Patterns
```scala
// Inferred from the signature and the Reprojector object context in the test suite
import org.locationtech.jts.geom.Envelope
import edu.ucr.cs.bdlab.beast.cg.Reprojector

val sourceEnvelope = new Envelope(-124.0, -114.0, 32.0, 42.0) // minX, maxX, minY, maxY
val targetEnvelope = Reprojector.reprojectEnvelope(sourceEnvelope, 4326, 3857)
```

### LLM Instruction Prompt
- When aligning bounding boxes for spatial partitioning, raster reshaping, or filtering across different coordinate systems, use `Reprojector.reprojectEnvelope`.
- Call it as a static method on the `Reprojector` object.
- Ensure you pass the correct integer EPSG codes (e.g., `4326`, `3857`) or valid GeoTools `CoordinateReferenceSystem` objects.
- Do not use this method to reproject complex geometries (polygons/lines); use `Reprojector.reprojectGeometry` for those.

### Prompt Snippet
```text
To reproject a bounding box in Beast, use `Reprojector.reprojectEnvelope(envelope, sourceSRID, targetSRID)`. This is useful when preparing an Envelope for `RasterOperationsFocal.reshapeNN` or spatial queries where the target dataset uses a different CRS.
```

### Common Failure Modes
- **Invalid or Unsupported SRID:** Passing an unrecognized integer as an SRID will cause a failure when Beast attempts to decode the EPSG code.
- **Axis Order Confusion:** JTS Envelopes are constructed using `(minX, maxX, minY, maxY)`. For EPSG:4326, this corresponds to `(minLongitude, maxLongitude, minLatitude, maxLatitude)`. Passing latitude as X will result in an out-of-bounds reprojection error.
- **Out of Bounds Coordinates:** Attempting to reproject an envelope whose coordinates fall outside the valid domain of the source CRS (e.g., longitudes > 180 in EPSG:4326) will throw a transformation exception.

### Fix Code Hint
```scala
// BAD: Passing latitude as X (minX, maxX, minY, maxY)
val badEnv = new Envelope(32.0, 42.0, -124.0, -114.0) 
val reprojected = Reprojector.reprojectEnvelope(badEnv, 4326, 3857) // Fails or yields garbage

// GOOD: Longitude is X, Latitude is Y
val goodEnv = new Envelope(-124.0, -114.0, 32.0, 42.0)
val reprojected = Reprojector.reprojectEnvelope(goodEnv, 4326, 3857)
```

## API Test: `reprojectEnvelopeInPlace`

### Signature
```scala
def reprojectEnvelopeInPlace(envelope: Array[Double], sourceSRID: Int, targetSRID: Int): Unit
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/Reprojector.scala:465_

_Source doc:_ Reproject an envelope (orthogonal rectangle) to the target CRS in-place @param envelope the input envelope to convert in the form (x1, y1, x2, y2) @param sourceSRID the source coordinate reference system (CRS) @param targetSRID the target coordinate reference system (CRS) @return the converted envelope

### Goal
Transforms the coordinates of a spatial bounding box (envelope) from a source Coordinate Reference System (CRS) to a target CRS, modifying the provided array directly.

### Parameters
- `envelope` (`Array[Double]`): A mutable 4-element array representing the input bounding box in the form `(x1, y1, x2, y2)`.
- `sourceSRID` (`Int`): The EPSG code of the original coordinate reference system (e.g., `4326` for WGS84).
- `targetSRID` (`Int`): The EPSG code of the destination coordinate reference system (e.g., `3857` for Web Mercator).

### Input
A mutable `Array[Double]` of exactly 4 elements representing an orthogonal rectangle's extents. The caller must provide valid integer EPSG codes for both the source and target spatial reference systems. If the envelope extends beyond the valid bounds of the target CRS, the resulting coordinates will be limited to the target's maximum extents.

### Output
Returns `Unit` — the operation performs an in-place mutation. The original `envelope` array is updated to contain the reprojected `(x1, y1, x2, y2)` coordinates in the target CRS.

### Valid Call Patterns
```scala
// Reprojecting an envelope from WGS84 (4326) to Web Mercator (3857)
val envelope = Array(-180.0, 0.0, 0.0, 90.0)
Reprojector.reprojectEnvelopeInPlace(envelope, 4326, 3857)

// The envelope array now contains the reprojected coordinates
// e.g., envelope(0) is approximately -20037508.0
```

### LLM Instruction Prompt
- When reprojecting an envelope, you MUST call `Reprojector.reprojectEnvelopeInPlace(envelope, source, target)`.
- Do NOT assign the result of this function to a variable; it returns `Unit` and modifies the `envelope` array in-place.
- Ensure the `envelope` argument is a mutable `Array[Double]` of exactly size 4 `(x1, y1, x2, y2)`. Do not pass a Tuple or a custom Envelope object.

### Prompt Snippet
```text
`Reprojector.reprojectEnvelopeInPlace(env: Array[Double], src: Int, tgt: Int): Unit` mutates a 4-element array `(x1, y1, x2, y2)` in-place to the target EPSG code. Do not assign its return value.
```

### Common Failure Modes
- **Type Mismatch on Return:** Assigning the result to a variable (e.g., `val newEnv = Reprojector.reprojectEnvelopeInPlace(...)`) and attempting to use `newEnv` as an array. The function returns `Unit`.
- **Array Bounds Error:** Passing an array with fewer than 4 elements, which will cause an `IndexOutOfBoundsException` during the in-place update.
- **Immutable Collection:** Passing an immutable collection (like a `List` or `Tuple4`) instead of a mutable `Array[Double]`.

### Fix Code Hint
```scala
// WRONG: Assigning the result of an in-place operation
val reprojectedEnv = Reprojector.reprojectEnvelopeInPlace(Array(-180.0, 0, 0, 90), 4326, 3857)
// reprojectedEnv is of type Unit!

// CORRECT: Mutating the array in-place
val envelope = Array(-180.0, 0.0, 0.0, 90.0)
Reprojector.reprojectEnvelopeInPlace(envelope, 4326, 3857)
// Use 'envelope' directly for subsequent operations
```

## API Test: `reprojectGeometry`

### Signature
```scala
def reprojectGeometry(geometry: Geometry, sourceCRS: CoordinateReferenceSystem, targetCRS: CoordinateReferenceSystem): Geometry
def reprojectGeometry(geometry: Geometry, targetSRID: Int): Geometry
def reprojectGeometry(geometry: Geometry, transform: TransformationInfo): Geometry
```
_Source doc:_ Reprojects the given geometry from source to target CRS. This method ignores the SRID of the geometry and assumes it to be in the source CRS. @param geometry the geometry to transform @param sourceCRS source coordinate reference system @param targetCRS target coordinate reference system @return a new geometry that is transformed

### Goal
Reprojects a spatial geometry from a source Coordinate Reference System (CRS) to a target CRS, returning a newly transformed geometry object.

### Parameters
- `geometry` (`Geometry`): The JTS `Geometry` (e.g., `Point`, `LineString`, `Polygon`) or Beast spatial type (e.g., `PointND`, `EnvelopeND`) to be transformed.
- `sourceCRS` (`CoordinateReferenceSystem`): The GeoTools coordinate reference system representing the original projection of the input geometry.
- `targetCRS` (`CoordinateReferenceSystem`): The GeoTools coordinate reference system representing the desired output projection.

### Input
A valid spatial `Geometry` object. The caller must provide valid GeoTools `CoordinateReferenceSystem` instances (typically obtained via `CRS.decode`). 
*Precondition:* The method explicitly ignores the internal SRID set on the input `geometry` and strictly assumes its coordinates are in the provided `sourceCRS`. 

### Output
Returns `Geometry` — A new JTS or Beast `Geometry` instance containing the transformed coordinates in the target CRS. The original input geometry is never mutated.

### Valid Call Patterns
```scala
import org.geotools.referencing.CRS
import edu.ucr.cs.bdlab.beast.cg.Reprojector

// Decode CRSs (using 'true' to force standard longitude/latitude X/Y axis order)
val sourceCRS = CRS.decode("EPSG:4326", true)
val targetCRS = CRS.decode("EPSG:3857", true)

// Reproject a geometry from source to target CRS
val transformedGeom = Reprojector.reprojectGeometry(originalGeometry, sourceCRS, targetCRS)

// Reproject using the target SRID overload (assumes source is known/handled by context)
val transformedGeomSrid = Reprojector.reprojectGeometry(originalGeometry, 3857)
```

### LLM Instruction Prompt
- Call `Reprojector.reprojectGeometry(...)` to transform vector geometries between coordinate systems.
- ALWAYS capture the return value; the function returns a new `Geometry` object and does not mutate the input geometry in place.
- Be aware that `reprojectGeometry` ignores the geometry's internal SRID property. You must explicitly provide the correct `sourceCRS` if using the full signature.
- When decoding EPSG codes for the CRS parameters, prefer `CRS.decode("EPSG:XXXX", true)` to enforce standard (longitude/latitude) axis ordering and prevent axis-flipping bugs.

### Prompt Snippet
```text
To reproject a geometry in Beast, use `Reprojector.reprojectGeometry(geom, sourceCRS, targetCRS)`. It returns a new `Geometry` and ignores the input's internal SRID. Capture the output. Use `CRS.decode("EPSG:...", true)` to ensure correct X/Y axis order.
```

### Common Failure Modes
- **Ignoring the Return Value:** Calling `Reprojector.reprojectGeometry(geom, ...)` without assigning the result, mistakenly assuming the original `geom` was modified in place.
- **Axis Order Reversal:** Passing a `CoordinateReferenceSystem` decoded without the `true` flag (e.g., `CRS.decode("EPSG:4326")`), which can result in flipped X/Y (Latitude/Longitude instead of Longitude/Latitude) coordinates during the math transformation.
- **Relying on Geometry SRID:** Expecting the method to automatically detect the source projection from `geometry.getSRID()`. The method explicitly ignores the geometry's SRID and relies entirely on the provided `sourceCRS` argument.

### Fix Code Hint
```scala
// WRONG: Assumes in-place mutation and relies on default axis order
val crs = CRS.decode("EPSG:3857")
Reprojector.reprojectGeometry(myPoint, crs) 

// CORRECT: Captures the new geometry and forces Longitude/Latitude axis order
val targetCRS = CRS.decode("EPSG:3857", true)
val sourceCRS = CRS.decode("EPSG:4326", true)
val projectedPoint = Reprojector.reprojectGeometry(myPoint, sourceCRS, targetCRS)
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
Reproject a distributed dataset of vector geometries (`SpatialRDD`) from its original Coordinate Reference System (CRS) to a new target CRS.

### Parameters
- `sourceRDD` (`SpatialRDD`): The input RDD of vector features (equivalent to `RDD[IFeature]`) to be transformed. The source CRS is automatically retrieved from the first element of this RDD.
- `targetCRS` (`CoordinateReferenceSystem`): The destination Coordinate Reference System to which the geometries will be projected. Overloads allow passing an `Int` (target SRID) or a `TransformationInfo` object instead.

### Input
A `SpatialRDD` (typically loaded via `sc.shapefile`, `sc.geojsonFile`, etc.) containing vector features. 
*   **Precondition:** The RDD must not be empty, and the first feature in the RDD *must* have a valid CRS attached to its geometry, as the source CRS is inferred directly from it.
*   **Type Rule:** This function is strictly for vector data (`SpatialRDD` / `RDD[IFeature]`). It cannot be used for raster data.

### Output
Returns `SpatialRDD` — A new RDD of vector features (`IFeature`) where all geometries have been mathematically transformed to the target CRS.

### Valid Call Patterns
```scala
// 1. Reprojecting using a CoordinateReferenceSystem object
val projectedPolygons: RDD[IFeature] = Reprojector.reprojectRDD(polygons, CRSServer.sridToCRS(3857))

// 2. Reprojecting using an integer SRID (via overload)
val projectedPolygonsSrid: RDD[IFeature] = Reprojector.reprojectRDD(polygons, 3857)
```

### LLM Instruction Prompt
- Call `Reprojector.reprojectRDD(sourceRDD, targetSRID)` to reproject vector datasets (`SpatialRDD` / `RDD[IFeature]`).
- NEVER use `Reprojector.reprojectRDD` for raster data (`RasterRDD` / `RDD[ITile[T]]`). To reproject or rescale rasters, you MUST use `RasterOperationsFocal.reshapeNN` or `RasterOperationsFocal.reshapeAverage`.
- Do not provide a source CRS argument; Beast automatically infers the source CRS from the first element of the `sourceRDD`.

### Prompt Snippet
```text
To reproject vector geometries in Beast, use `Reprojector.reprojectRDD(vectorRdd, targetSrid)`. The source CRS is automatically inferred from the first element. Do not use this function for rasters; raster reprojection requires `RasterOperationsFocal.reshapeNN` or `reshapeAverage` with a target `RasterMetadata`.
```

### Common Failure Modes
- **Passing a Raster RDD:** Attempting to pass a `RasterRDD` or `RDD[ITile[T]]` to `reprojectRDD`. This will fail compilation because `reprojectRDD` expects a `SpatialRDD` (vector features).
- **Empty RDD or Missing Source CRS:** If the `sourceRDD` is empty, or if the first feature's geometry lacks a defined CRS, the automatic source CRS inference will fail at runtime.
- **Calling as an instance method:** Attempting to call `sourceRDD.reprojectRDD(...)` instead of the correct object method `Reprojector.reprojectRDD(sourceRDD, ...)`.

### Fix Code Hint
```scala
// WRONG: Attempting to reproject a raster using Reprojector
// val projectedRaster = Reprojector.reprojectRDD(raster, 3857)

// RIGHT: Reprojecting a vector SpatialRDD
val projectedPolygons = Reprojector.reprojectRDD(polygons, 3857)

// RIGHT: Reprojecting a raster requires reshape API
// val reshapedRaster = RasterOperationsFocal.reshapeNN(raster, targetRasterMetadata)
```

## API Test: `rescale`
_Grounding: doc-repaired from source (docfix)._

### Goal
Changes the resolution of a raster to a new desired width and height in pixels without altering the tile size or Coordinate Reference System (CRS). This is a user-facing focal operation that prepares a `RasterRDD` for further analysis, alignment, or saving. It can also be applied directly to a `RasterMetadata` object to compute new dimensions without processing pixel data.

### Valid Call Patterns
```scala
import edu.ucr.cs.bdlab.beast.geolite.RasterMetadata
import edu.ucr.cs.bdlab.raptor.RasterOperationsFocal.InterpolationMethod
import java.awt.geom.AffineTransform

// 1. Rescale RasterMetadata directly
val sourceMetadata = new RasterMetadata(0, 0, 100, 100, 100, 100, 4326, new AffineTransform())
val targetMetadata = sourceMetadata.rescale(10, 10)

assert(targetMetadata.rasterWidth == 10, s"Expected rasterWidth 10, got ${targetMetadata.rasterWidth}")
assert(targetMetadata.rasterHeight == 10, s"Expected rasterHeight 10, got ${targetMetadata.rasterHeight}")

// 2. Rescale the continuous RasterRDD using Average interpolation as required
// (Assumes rasterRDD is provided in scope)
val rescaledRDD = rasterRDD.rescale(360, 180, interpolationMethod = InterpolationMethod.Average)
val rescaledCount = rescaledRDD.count()

println(s"__CHECK__ rescale ${targetMetadata.rasterWidth}x${targetMetadata.rasterHeight} with $rescaledCount tiles")
```

### LLM Instruction Prompt
- Call `rescale` as an extension method directly on a `RasterRDD` or `RasterMetadata` object (e.g., `raster.rescale(width, height)`).
- You MUST use the correct packages for required types: `RasterMetadata` is located in `edu.ucr.cs.bdlab.beast.geolite.RasterMetadata`.
- `InterpolationMethod` is NOT a top-level object; it is nested inside `RasterOperationsFocal`. Its fully qualified path is `edu.ucr.cs.bdlab.raptor.RasterOperationsFocal.InterpolationMethod`.
- If constructing `RasterMetadata` manually, import `java.awt.geom.AffineTransform`.
- When specifying the interpolation method on a `RasterRDD`, you must use named arguments (e.g., `interpolationMethod = InterpolationMethod.Average`) to avoid a positional type mismatch with the `unifiedRaster: Boolean` parameter.

### Prompt Snippet
When changing the resolution of a raster in RDPro, use the `rescale` extension method: `raster.rescale(newWidth, newHeight)`. For continuous data, specify `interpolationMethod = edu.ucr.cs.bdlab.raptor.RasterOperationsFocal.InterpolationMethod.Average` using named arguments to skip the `unifiedRaster` boolean. If manipulating metadata directly, use `edu.ucr.cs.bdlab.beast.geolite.RasterMetadata`.

### Common Failure Modes
- **Incorrect Package for RasterMetadata:** Guessing `edu.ucr.cs.bdlab.raptor.RasterMetadata` instead of the correct `edu.ucr.cs.bdlab.beast.geolite.RasterMetadata`, resulting in a `type RasterMetadata is not a member of package edu.ucr.cs.bdlab` compilation error.
- **Incorrect Import for InterpolationMethod:** Attempting to import `InterpolationMethod` as a top-level object (`edu.ucr.cs.bdlab.raptor.InterpolationMethod`). It is nested, so the correct path is `edu.ucr.cs.bdlab.raptor.RasterOperationsFocal.InterpolationMethod`, otherwise it throws `object InterpolationMethod is not a member of package`.
- **Positional Argument Mismatch:** Passing the interpolation method as the third positional argument. Because the third argument in the signature is `unifiedRaster: Boolean`, this causes a compilation error.

### Fix Code Hint
```scala
// WRONG: Incorrect packages for RasterMetadata/InterpolationMethod, and positional argument mismatch
import edu.ucr.cs.bdlab.raptor.RasterMetadata
import edu.ucr.cs.bdlab.raptor.InterpolationMethod
val rescaled = tempRaster.rescale(360, 180, InterpolationMethod.Average)

// CORRECT: Use geolite for RasterMetadata, nested path for InterpolationMethod, and named arguments
import edu.ucr.cs.bdlab.beast.geolite.RasterMetadata
import edu.ucr.cs.bdlab.raptor.RasterOperationsFocal.InterpolationMethod
val rescaled = tempRaster.rescale(360, 180, interpolationMethod = InterpolationMethod.Average)
```

## API Test: `reshapeAverage`
_Grounding: doc-repaired from source (docfix)._

### Goal
ADVANCED/LOW-LEVEL API. Reshapes a raster (reprojecting, regridding, rescaling) by computing the average value of overlapping source pixels. Designed exclusively for continuous numerical data. *Note: This is an internal framework method; exclude from standard user-facing recommendations. Higher-level alignment functions should be preferred.*

### Valid Call Patterns
```scala
import edu.ucr.cs.bdlab.raptor.RasterOperationsFocal
import edu.ucr.cs.bdlab.beast.geolite.RasterMetadata

// Reshape the raster using an identity metadata conversion (target metadata = source metadata).
// For continuous data, reshapeAverage is the correct method.
val reshaped = RasterOperationsFocal.reshapeAverage(rasterRDD, md => md)

// Materialize the reshaped raster
val outCount = reshaped.count()
println(s"__CHECK__ reshapeAverage $outCount")
```

### LLM Instruction Prompt
- Classify as ADVANCED/LOW-LEVEL. Do not present as the normal first-choice user workflow.
- Call `RasterOperationsFocal.reshapeAverage(raster, md => targetMetadata)` to align/reproject continuous rasters.
- Do not assert that the number of tiles (or partitions) in the output RDD will exactly match the input RDD.
- Because `reshapeAverage` computes spatial intersections using bounding boxes and affine transformations, the output tile count may differ from the input count even if the target metadata is identical to the source metadata.

### Prompt Snippet
`ADVANCED/LOW-LEVEL: Use RasterOperationsFocal.reshapeAverage(raster, md => targetMetadata) for continuous rasters. Do not assert output tile/partition counts match the input; spatial bounding box math and affine transformations can change tile counts even with identical metadata.`

### Common Failure Modes
- **Invalid Tile Count Assertion:** Asserting that the output RDD has the exact same number of tiles/partitions as the input RDD (`inCount == outCount`). Floating-point math in affine transformations and grid intersections causes boundary overlaps, changing the emitted tile count even with identical metadata.
- **Categorical Data Corruption:** Using `reshapeAverage` on categorical data (use `reshapeNN` instead).
- **Method Not Found:** Calling `raster.reshapeAverage(...)` instead of the object method `RasterOperationsFocal.reshapeAverage(...)`.

### Fix Code Hint
```scala
// WRONG: Asserting exact tile count match
// val reshaped = RasterOperationsFocal.reshapeAverage(raster, md => md)
// assert(reshaped.count() == raster.count()) // Fails due to spatial bounding box overlaps

// CORRECT: Executing without strict tile count assertions
val reshaped = RasterOperationsFocal.reshapeAverage(raster, md => md)
val outCount = reshaped.count()
println(s"__CHECK__ reshapeAverage $outCount")
```

## API Test: `reshapeNN`

### Signature
```scala
def reshapeNN[T: ClassTag](raster: RasterRDD[T], targetMetadataConv: RasterMetadata => RasterMetadata, numPartitions: Int = 0): RasterRDD[T]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsFocal.scala:408_

_Source doc:_ Converts the metadata of the input raster to the target metadata. This might involve any combination of the following: - reproject: Change the coordinate reference system (CRS) - regrid: Change the tiling of the raster - rescale: Change the resolution, i.e., number of pixels, in the raster - subset: Retrieve a subset of the data, even though, it would be an inefficient way to do just the subsetting Note: This is a low-level method that is normally not called directly by users. Instead, we provide higher-level easier to use functions for real use cases that all call this low-level function. Note: This method uses the nearest neighbor method to match source to target pixels. Each target pixel gets its value from the nearest source pixel. If that source pixel is empty or outside the range of the source raster, the target pixel will be empty. @param raster the input raster that should be reshaped @param targetMetadataConv a function that converts a source RasterMetadata to target RasterMetadata @param numPartitions the number of partitions in the output RDD. If not set, the input numPartitions is used @return the new raster with the target metadata

### Goal
Reshapes a raster dataset by altering its coordinate reference system (CRS), resolution, tiling, or spatial extent, using nearest-neighbor interpolation to assign pixel values.

### Parameters
- `raster` (`RasterRDD[T]`): The input raster dataset that needs to be reshaped, reprojected, rescaled, or retiled.
- `targetMetadataConv` (`RasterMetadata => RasterMetadata,
                             numPartitions: Int`), default `0`: A function that takes the source `RasterMetadata` and returns the target `RasterMetadata` (defining the new CRS, resolution, bounds, and tile size). The `numPartitions` parameter dictates the number of partitions in the output RDD; if `0` or not set, the input's partition count is preserved.

### Input
- A `RasterRDD[T]` typically loaded via `sc.geoTiff[T](...)` where `T` exactly matches the runtime pixel type of the file (e.g., `Int` for `IntegerType`, `Float` for `FloatType`).
- **Preconditions & Type Selection:** `reshapeNN` (Nearest Neighbor) should specifically be used for **categorical data** (e.g., land cover classes) or general downsizing. If the pixel data is numerical and continuous (e.g., temperature), `reshapeAverage` must be used instead.

### Output
Returns `RasterRDD[T]` — A new distributed raster dataset conforming to the target metadata. Empty source pixels or pixels outside the source range result in empty target pixels. The output can be saved directly via `saveAsGeoTiff` or used safely in multi-raster operations like `overlay`.

### Valid Call Patterns
```scala
// From the original project README (using an implicit or simplified metadata conversion)
val raster: RasterRDD[Int] = sc.geoTiff[Int]("glc2000_v1_1.tif")
val reshaped = RasterOperationsFocal.reshapeNN(raster,
  RasterMetadata.create(-124, 42, -114, 32, 4326, 1000, 1000, 100, 100))
reshaped.saveAsGeoTiff("glc_ca")

// Strict signature-matching pattern (derived from sibling test `reshapeAverage`)
val targetMetadata = RasterMetadata.create(-124, 42, -114, 32, 4326, 1000, 1000, 100, 100)
val reshapedStrict = RasterOperationsFocal.reshapeNN(raster, _ => targetMetadata)
```

### LLM Instruction Prompt
- Use `RasterOperationsFocal.reshapeNN` to align rasters before an `overlay` operation, as `overlay` strictly requires all input rasters to have identical metadata (resolution, CRS, and tile size).
- Always choose `reshapeNN` for categorical rasters. Do not use it for continuous numerical data; use `reshapeAverage` for that.
- Pass a function `_ => targetMetadata` as the second argument to satisfy the `RasterMetadata => RasterMetadata` signature when defining a completely new target grid.
- Ensure the type parameter `T` matches the underlying GeoTIFF pixel type (e.g., `Int` or `Float`).

### Prompt Snippet
```text
I have two categorical land-cover GeoTIFFs with different resolutions and CRSs. 
I need to combine them using `overlay`. How do I align their metadata first?
```

### Common Failure Modes
- **Interpolation Mismatch:** Using `reshapeNN` on continuous numerical data (like temperature or elevation) instead of `reshapeAverage`, leading to aliasing, blocky artifacts, or loss of precision.
- **Overlay Precondition Violation:** Attempting to call `raster1.overlay(raster2)` without first using `reshapeNN` to perfectly align their CRS, resolution, and tile sizes.
- **Type Mismatch:** Loading the raster with the wrong type (e.g., `sc.geoTiff[Float]` for an integer raster) before reshaping, causing runtime casting exceptions.

### Fix Code Hint
```scala
// BAD: Calling overlay on unaligned rasters
// val combined = raster1.overlay(raster2, ...)

// GOOD: Aligning the second raster to the first raster's metadata using reshapeNN before overlay
val alignedRaster2 = RasterOperationsFocal.reshapeNN(raster2, _ => raster1.metadata)
val combined = raster1.overlay(alignedRaster2, (p1: Int, p2: Int) => if (p1 > 0) p1 else p2)
```

## API Test: `retainIndex`

### Signature
```scala
def retainIndex(index: Int): BeastOptions
```
_Source: beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/common/BeastOptions.scala:168_

_Source doc:_ Keep only the parameters that do not have an index or the ones with the given index. In other words, remove any indexed parameter that have a different index than the one given. The index of the parameter is a suffix between square brackets, e.g., param[1] @param index the index to retain @return a new options with the given index retained

### Goal
Filters a `BeastOptions` configuration object to keep only unindexed parameters and parameters matching a specific integer index, stripping the index suffix from the retained keys.

### Parameters
- `index` (`Int`): The integer index to retain (e.g., passing `1` will keep keys formatted like `param[1]`).

### Input
A `BeastOptions` instance containing configuration key-value pairs. This is typically used when a single configuration object holds parameters for multiple inputs or operations simultaneously, distinguished by an index suffix in square brackets (e.g., `key[1]`, `key[2]`).

### Output
Returns `BeastOptions` — A new `BeastOptions` instance containing only the unindexed keys and the retained indexed keys. The retained indexed keys will have their `[index]` suffix removed in the returned object.

### Valid Call Patterns
```scala
val opts = new BeastOptions()
  .set("key1[1]", "val1")
  .set("key1[2]", "val2")
  .set("key3", "val3")
  .set("key4[2]", "val4")

// Retains "key1[1]" (renamed to "key1") and unindexed "key3"
val opts1 = opts.retainIndex(1)

// Retains "key1[2]" (renamed to "key1"), "key4[2]" (renamed to "key4"), and unindexed "key3"
val opts2 = opts.retainIndex(2)
```

### LLM Instruction Prompt
- Use `retainIndex` when you need to extract configuration parameters specific to a single dataset or operation from a combined `BeastOptions` object containing indexed keys (like `param[1]`, `param[2]`). 
- Remember that the returned `BeastOptions` will have the index suffix stripped from the keys (e.g., `key[1]` becomes `key`).
- Unindexed keys (e.g., global settings) are always retained regardless of the index provided.

### Prompt Snippet
```text
Use `opts.retainIndex(idx)` to filter a `BeastOptions` object, keeping unindexed keys and keys matching `[idx]`. The returned keys will have the `[idx]` suffix removed.
```

### Common Failure Modes
- **Querying with the old indexed key:** Attempting to retrieve a value from the new `BeastOptions` using the original indexed key string (e.g., `opts1("key1[1]")`). The method strips the suffix, so the key becomes just `"key1"`.
- **Losing parameters:** Passing an index that does not match any indexed keys in the `BeastOptions`. This will silently drop all indexed parameters and return an object containing *only* the unindexed parameters.

### Fix Code Hint
```scala
// WRONG: Trying to access the key with the index suffix after retaining
val opts1 = opts.retainIndex(1)
val value = opts1("key1[1]") // Will fail or return null

// RIGHT: Access the key without the suffix
val opts1 = opts.retainIndex(1)
val value = opts1("key1") // Returns "val1"
```

## API Test: `retile`
_Grounding: doc-repaired from source (docfix)._

### Goal
Regrids a distributed raster dataset (`RasterRDD`) into new internal tile dimensions (width and height in pixels) without altering the overall spatial resolution, extent, or actual pixel values. This is a standard user-facing operation (included in the main user-facing denominator) used to optimize chunking sizes for distributed processing (e.g., breaking large monolithic tiles into smaller ones before an `explode` operation).

### Valid Call Patterns
```scala
import edu.ucr.cs.bdlab.beast.cg.SpatialDataTypes.RasterRDD
import edu.ucr.cs.bdlab.raptor.RaptorMixin._
import scala.reflect.ClassTag

// The snippet MUST cast `rasterRDD` to `RasterRDD[Array[Float]]` before calling `retile`
// to ensure the correct implicit `ClassTag` is captured for multi-band data.
val correctRaster = rasterRDD.asInstanceOf[RasterRDD[Array[Float]]]
val retiledRDD = correctRaster.retile(64, 64)
val retiledExploded = retiledRDD.explode

val count = retiledExploded.count()
val originalCount = correctRaster.count()

assert(count >= originalCount, s"Exploded retiled RDD count ($count) should be >= original count ($originalCount)")
println(s"__CHECK__ retile exploded count: $count")
```

### LLM Instruction Prompt
- Use `raster.retile(tileWidth, tileHeight)` to change the internal chunking size of a raster.
- The snippet MUST cast `rasterRDD` to the exact array type (e.g., `RasterRDD[Array[Float]]`) before calling `retile` to ensure the correct implicit `ClassTag` is captured for multi-band data.
- Failing to cast the RDD to the exact array type will result in a Spark Catalyst type mismatch (`Unrecognized value [F`) during actions like `.count()` or `.explode`.
- Chain `.retile(w, h)` with `.explode` to break large monolithic tiles into smaller distributed partitions.

### Prompt Snippet
```text
To change the internal tile dimensions of a RasterRDD without altering its resolution or CRS, use `raster.retile(tileWidth, tileHeight)`. You MUST cast the RDD to the exact runtime pixel type (e.g., `rasterRDD.asInstanceOf[RasterRDD[Array[Float]]]` for multi-band data) before calling `retile`. This ensures the correct implicit `ClassTag` is captured to build the Spark SQL schema, preventing Catalyst type mismatch errors (`Unrecognized value [F`) during downstream actions like `.explode` or `.count()`.
```

### Common Failure Modes
- **Catalyst Type Mismatch (`Unrecognized value [F`):** The failure that just happened. Failing to cast the RDD to the exact array type (e.g., using a scalar `ClassTag` for multi-band `Array[Float]` data) causes Spark Catalyst to throw `java.lang.RuntimeException: Unrecognized value [F` during actions like `.count()` or `.explode`. The incorrect scalar `ClassTag` generates a bad schema that crashes `CatalystTypeConverters` when it encounters the array data.
- **Driver OutOfMemoryError on Save:** Calling `raster.retile(w, h).explode.saveAsGeoTiff("out")` without specifying the `"distributed"` write mode. The default `"compatibility"` mode attempts to collect all tiles to the driver.

### Fix Code Hint
```scala
// WRONG: Using a scalar ClassTag for multi-band array data crashes Catalyst on action
// val retiled = rasterRDD.asInstanceOf[RasterRDD[Float]].retile(64, 64).explode
// retiled.count() // Throws java.lang.RuntimeException: Unrecognized value [F...

// CORRECT: Cast to the exact array type so retile gets the correct ClassTag
val correctRaster = rasterRDD.asInstanceOf[RasterRDD[Array[Float]]]
val retiledRDD = correctRaster.retile(64, 64)
val retiledExploded = retiledRDD.explode
retiledExploded.count()
```

## API Test: `run`

### Signature
```scala
def run(opts: BeastOptions, inputs: Array[String], outputs: Array[String], sc: SparkContext): Any
def run(opts: BeastOptions, inputs: Array[String], outputs: Array[String], sc: SparkContext): Unit
def run(source: String, tileDir: String, indexFile:FileStatus, z: Int, currX: Int, currY: Int, sc: SparkContext): (BufferedImage,Int)
def run(inputs: Array[String], sc: SparkContext): String
def run(inputs: Array[String], sc: SparkContext): Array[Int]
def run(opts: BeastOptions, inputs: Array[String], sc: SparkContext): String
def run(inputs: Array[String], sc: SparkContext): BufferedImage
def run(): Unit
def run(opts: BeastOptions, inputs: Array[String], outputs: Array[String], sc: JavaSparkContext): Any
def run(opts: BeastOptions, inputs: Array[String], outputs: Array[String], ss: SparkSession): Any
```
_Source: beast/dynoviz/src/main/scala/edu/ucr/cs/bdlab/dynoviz/NPYTileGeneratorOnthefly.scala:29  (+28 more definition site/overload)_

### Goal
Executes a Beast/RDPro operation. The primary documented overload runs a main function (like `GeometricSummary` or `BeastServer`) using user command-line options, input/output paths, and a Spark context, while other internal overloads handle tasks like on-the-fly tile generation.

### Parameters
- `source` (`String`): Unknown (not provided in authoritative API facts; likely the source data path for tile generation).
- `tileDir` (`String`): Unknown (not provided in authoritative API facts; likely the directory for output tiles).
- `indexFile` (`FileStatus`): Unknown (not provided in authoritative API facts; likely the spatial index file).
- `z` (`Int`): Unknown (not provided in authoritative API facts; likely the zoom level).
- `currX` (`Int`): Unknown (not provided in authoritative API facts; likely the X coordinate of the tile).
- `currY` (`Int`): Unknown (not provided in authoritative API facts; likely the Y coordinate of the tile).
- `sc` (`SparkContext`): The Spark context used to run the operation.

*(Note: The authoritative API facts primarily document the `(opts: BeastOptions, inputs: Array[String], outputs: Array[String], sc: SparkContext)` overload).*

### Input
For the primary operation runner: requires a `BeastOptions` object configuring the operation (e.g., setting `iformat`, `skipheader`, `separator`), an `Array[String]` of input file paths, an `Array[String]` of output paths (or `null` if no output is written), and an initialized `SparkContext`. 
For the tile generator overload (pre-filled parameters): requires a source path, tile directory, spatial index `FileStatus`, and XYZ tile coordinates (exact semantics are unknown as they are not in the authoritative facts).

### Output
Returns `(BufferedImage,Int)` — Unknown (not provided in authoritative API facts; likely an image buffer of the generated tile and a status/count integer). 
*(Note: The primary documented `run` overload returns `Any`, representing an optional result of the operation, such as a `Summary` object, which must be cast by the caller).*

### Valid Call Patterns
```scala
// Example 1: Running a geometric summary operation (primary overload)
val inputfile = locateResource("/test.partitions")
val opts = new BeastOptions().set("iformat", "wkt(Geometry)")
  .set("skipheader", true)
  .set("separator", "\t")
val summary = GeometricSummary.run(opts, Array(inputfile.getPath), null, sparkContext).asInstanceOf[Summary]

// Example 2: Starting the Beast server (primary overload)
new BeastServer().run(new BeastOptions(), null, null, sparkContext)
```

### LLM Instruction Prompt
- Use the `run` method to execute Beast operations (e.g., `GeometricSummary.run` or `new BeastServer().run`).
- Always pass inputs and outputs as `Array[String]`. If an operation does not produce file output, pass `null` for the `outputs` array.
- The primary `run` method returns `Any`. You MUST cast the result to the expected type (e.g., `.asInstanceOf[Summary]`) to access its properties.
- Do not invent parameters. The authoritative JSON facts only define the `(opts, inputs, outputs, sc)` signature, despite internal overloads existing for tile generation.

### Prompt Snippet
```text
val opts = new BeastOptions().set("iformat", "wkt(Geometry)")
val summary = GeometricSummary.run(opts, Array("input.csv"), null, sc).asInstanceOf[Summary]
```

### Common Failure Modes
- **Type Mismatch on Inputs/Outputs:** Passing a single `String` instead of an `Array[String]` for the `inputs` or `outputs` parameters.
- **Missing Cast:** Failing to cast the `Any` return type of the primary `run` method, leading to compilation errors when trying to access result properties (like `summary.numFeatures`).
- **Null Pointer Exceptions:** Passing `null` for `inputs` when the specific operation (like `GeometricSummary`) requires an input dataset to process.

### Fix Code Hint
```scala
// WRONG: Passing a single string and forgetting to cast the result
// val summary = GeometricSummary.run(opts, "data.csv", null, sc)

// CORRECT: Wrap the input path in an Array and cast the return type
val summary = GeometricSummary.run(opts, Array("data.csv"), null, sc).asInstanceOf[Summary]
```

## API Test: `saveAsCSVPoints`
_Grounding: doc-repaired from source (docfix)._

### Goal
Save a distributed collection of point features to a CSV or text-delimited file, explicitly defining which columns will hold the X and Y coordinates. This is a user-facing output action provided as an extension method on `SpatialRDD` (which is a type alias for `RDD[IFeature]`).

### Valid Call Patterns
```scala
import edu.ucr.cs.bdlab.beast._
import edu.ucr.cs.bdlab.beast.geolite.Feature
import edu.ucr.cs.bdlab.beast.geolite.IFeature
import org.apache.spark.rdd.RDD

// If mapping from an existing RDD, you MUST explicitly cast to IFeature
val pointsRDD: RDD[IFeature] = featuresRDD
  .filter(_.getGeometry != null)
  .map(f => Feature.create(f, f.getGeometry.getCentroid).asInstanceOf[IFeature])
  .coalesce(1)

val outPath = output_dir + "/out_points.csv"

// Save the points, placing X in column 0 and Y in column 1
pointsRDD.saveAsCSVPoints(
  filename = outPath,
  xColumn = 0,
  yColumn = 1,
  delimiter = ',',
  header = true
)
```

### LLM Instruction Prompt
- `saveAsCSVPoints` is an extension method specifically on `SpatialRDD` (a type alias for `RDD[IFeature]`).
- Due to Scala's `RDD` invariance, if you create or map to `Feature` objects, you MUST explicitly cast them to `IFeature` (e.g., `.asInstanceOf[IFeature]`) so the resulting RDD is typed as `RDD[IFeature]`. Otherwise, the compiler will fail to resolve the extension method.
- Use this method only for point features.
- Always write outputs under the provided `output_dir`.

### Prompt Snippet
```text
To export point geometries to CSV, use `rdd.saveAsCSVPoints(filename, xColumn, yColumn, delimiter, header)`. The RDD must be strictly typed as `RDD[IFeature]`. If mapping to `Feature`, cast explicitly: `.map(f => Feature.create(...).asInstanceOf[IFeature])` to avoid RDD invariance compilation errors.
```

### Common Failure Modes
- **Missing Extension Method (Invariance Error):** `error: value saveAsCSVPoints is not a member of org.apache.spark.rdd.RDD[edu.ucr.cs.bdlab.beast.geolite.Feature]`. This happens because `RDD[T]` is invariant in Scala. An `RDD[Feature]` cannot trigger the implicit conversion to `SpatialRDD` (`RDD[IFeature]`), even though `Feature` implements `IFeature`. You must cast the elements to `IFeature` during the map operation.
- **Non-Point Geometries:** Calling this method on an RDD containing polygons or linestrings. The method is strictly designed for point geometries.
- **File Already Exists:** Standard Spark behavior applies; if the `filename` directory already exists, the job will fail.

### Fix Code Hint
```scala
// WRONG: Results in RDD[Feature], compiler cannot find saveAsCSVPoints due to RDD invariance
val wrongRDD = featuresRDD.map(f => Feature.create(f, f.getGeometry.getCentroid))
wrongRDD.saveAsCSVPoints(output_dir + "/out.csv", 0, 1, ',', true) // ERROR

// CORRECT: Explicitly cast to IFeature so the RDD is typed as RDD[IFeature]
val correctRDD = featuresRDD.map(f => Feature.create(f, f.getGeometry.getCentroid).asInstanceOf[IFeature])
correctRDD.saveAsCSVPoints(output_dir + "/out.csv", 0, 1, ',', true)
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
Save a distributed collection of spatial vector features (an RDD of geometries) to a file or directory in GeoJSON format.

### Parameters
- `filename` (`String`): The output path or filename where the GeoJSON data will be written.
- `opts` (`BeastOptions`), default `new BeastOptions()`: Optional configuration parameters for the Beast environment and underlying Spark writer.
- `rdd` (`JavaSpatialRDD`): *(Java overload only)* The Java spatial RDD containing the features to be saved.

### Input
A spatial vector RDD (e.g., `RDD[IFeature]` in Scala or `JavaSpatialRDD` in Java) containing geometries (points, lines, or polygons). This method is strictly for vector data and cannot be used on raster data (GeoTIFF/HDF).

### Output
Returns `Unit` — The operation produces no return value. Its side effect is writing the vector features to the specified `filename` as GeoJSON. Because Beast is built on Spark, this may write a directory containing multiple part-files if the RDD has multiple partitions.

### Valid Call Patterns
```scala
// Scala (via implicit extension on RDD[IFeature])
records.saveAsGeoJSON("output.geojson")

// Java (via static helper)
JavaSpatialRDDHelper.saveAsGeoJSON(records, "output.geojson")
```

### LLM Instruction Prompt
- Use `rdd.saveAsGeoJSON("path")` in Scala to export vector features to GeoJSON.
- Use `JavaSpatialRDDHelper.saveAsGeoJSON(rdd, "path")` when writing Java code.
- NEVER use `saveAsGeoJSON` on a `RasterRDD` or `RDD[ITile[T]]`. Raster data must be saved using `saveAsGeoTiff`.
- Do not invent a `saveAsGeoJSON` method on the `SparkContext` or `JavaSpatialSparkContext`; it is an action called directly on the RDD.

### Prompt Snippet
```text
RDPro/Beast vector export: Use `rdd.saveAsGeoJSON("path.geojson")` in Scala or `JavaSpatialRDDHelper.saveAsGeoJSON(rdd, "path.geojson")` in Java. Only valid for vector RDDs (`RDD[IFeature]`), not rasters.
```

### Common Failure Modes
- **Type Mismatch (Raster vs. Vector):** Attempting to call `saveAsGeoJSON` on a `RasterRDD` (e.g., after `mapPixels` or `reshapeNN`). GeoJSON is a vector format; rasters must use `saveAsGeoTiff`.
- **File Already Exists:** Like standard Spark actions, if the target `filename` directory already exists, the job will fail unless the output directory is cleared first or Spark's overwrite mode is configured.
- **Missing Implicit Conversions:** In Scala, if `saveAsGeoJSON` is not recognized on the RDD, the caller may have forgotten to import Beast's SparkContext extensions.

### Fix Code Hint
```scala
// WRONG: Attempting to save a raster as GeoJSON
val raster = sc.geoTiff[Int]("input.tif")
raster.saveAsGeoJSON("output.geojson") // Fails: saveAsGeoJSON is for vectors

// RIGHT: Save raster as GeoTiff
raster.saveAsGeoTiff("output_raster")

// RIGHT: Save vector features as GeoJSON
val features: RDD[IFeature] = sc.shapefile("input.zip")
features.saveAsGeoJSON("output.geojson")
```

## API Test: `saveAsGeoTiff`

### Signature
```scala
def saveAsGeoTiff(path: String, opts: BeastOptions = new BeastOptions): Unit
def saveAsGeoTiff[T](rasterRDD: RDD[ITile[T]], outPath: String, opts: BeastOptions): Unit
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/GeoTiffWriter.scala:476  (+1 more definition site/overload)_

### Goal
Save a distributed RasterRDD (a collection of image tiles) to disk as one or more GeoTIFF files.

### Parameters
- `rasterRDD` (`RDD[ITile[T]]`): The distributed raster dataset to be saved. (This parameter is implicit when calling the extension method directly on a `RasterRDD`).
- `outPath` (`String`): The destination directory or file path where the output GeoTIFF file(s) will be written (named `path` in the extension method).
- `opts` (`BeastOptions`): Additional configuration options for the writer, such as `GeoTiffWriter.BitsPerSample`, `GeoTiffWriter.BigTiff`, or `GeoTiffWriter.WriteMode`. Defaults to empty options.

### Input
A `RasterRDD` or `RDD[ITile[T]]` containing the processed raster data. 
**Preconditions and Configuration Rules:**
*   **Write Modes:** `GeoTiffWriter.WriteMode` supports `"distributed"` (writes each RDD partition to a separate file) and `"compatibility"` (writes a single file compatible with traditional GIS software). `"distributed"` is highly recommended if the raster was previously reshaped using `explode`.
*   **Bit Compaction:** `GeoTiffWriter.CompactBits` only works with integer pixel values. Float values are always represented in 32-bits. 
*   **Performance:** If using bit compaction on integers, you must explicitly provide `GeoTiffWriter.BitsPerSample` in the options; otherwise, the writer is forced to perform a full dataset scan to determine the maximum value.

### Output
Returns `Unit` — writes the raster data to the specified path as GeoTIFF file(s).

### Valid Call Patterns
```scala
// Pattern 1: Extension method on RasterRDD (most common)
val temperatureF: RasterRDD[Float] = temperatureK.mapPixels(k => (k-273.15f) * 9 / 5 + 32)
temperatureF.saveAsGeoTiff("temperature_f")

// Pattern 2: Extension method with inline filtering
temperatureK.filterPixels(_ > 300).saveAsGeoTiff("temperature_high")

// Pattern 3: Object method with specific BeastOptions (e.g., BitsPerSample)
val outputFile = new File(scratchDir, "glc.tif")
GeoTiffWriter.saveAsGeoTiff(rasterRDD, outputFile.getPath, GeoTiffWriter.BitsPerSample -> 8)

// Pattern 4: Object method with multiple BeastOptions
GeoTiffWriter.saveAsGeoTiff(rasterRDD, outputFile.getPath, 
  Seq(GeoTiffWriter.BitsPerSample -> 8, GeoTiffWriter.BigTiff -> "yes"))
```

### LLM Instruction Prompt
- Use `saveAsGeoTiff` to persist the results of raster operations (like `mapPixels`, `filterPixels`, or `reshapeNN`) to disk.
- Prefer the instance method `raster.saveAsGeoTiff("path")` for simple saves.
- When using `GeoTiffWriter.saveAsGeoTiff`, pass options using the `->` tuple syntax (e.g., `GeoTiffWriter.BitsPerSample -> 8`).
- NEVER attempt to use bit compaction on `Float` rasters; they are strictly 32-bit.
- ALWAYS specify `GeoTiffWriter.WriteMode -> "distributed"` if saving a raster immediately after an `explode` operation to avoid massive single-file bottlenecks.
- ALWAYS provide `GeoTiffWriter.BitsPerSample` if using integer bit compaction to prevent an expensive full-dataset scan.

### Prompt Snippet
```text
Write a Spark pipeline using RDPro that loads a GeoTIFF of integer land cover classes, filters for class 5, and saves the result to "forest_class.tif" using 8 bits per sample.
```

### Common Failure Modes
- **Full Dataset Scan Bottleneck:** Omitting `GeoTiffWriter.BitsPerSample` when saving integer rasters with bit compaction enabled, causing Spark to trigger an unexpected full action to compute the maximum pixel value.
- **OOM / Driver Crash on Large Rasters:** Attempting to save a massive, highly-partitioned raster (especially after `explode`) in `"compatibility"` mode (the default single-file mode) instead of `"distributed"` mode.
- **Invalid Bit Compaction:** Trying to compact a `RasterRDD[Float]` to 8-bit or 16-bit. Float rasters will ignore this and always save as 32-bit.

### Fix Code Hint
```scala
// BAD: Forces a full dataset scan to determine bit depth for compaction
GeoTiffWriter.saveAsGeoTiff(landCoverRDD, "output.tif", GeoTiffWriter.CompactBits -> true)

// GOOD: Explicitly provides BitsPerSample to avoid the scan
GeoTiffWriter.saveAsGeoTiff(landCoverRDD, "output.tif", 
  Seq(GeoTiffWriter.CompactBits -> true, GeoTiffWriter.BitsPerSample -> 8))

// BAD: Saving an exploded raster as a single file (can cause OOM)
explodedRaster.saveAsGeoTiff("huge_output")

// GOOD: Saving an exploded raster in distributed mode
GeoTiffWriter.saveAsGeoTiff(explodedRaster, "huge_output", GeoTiffWriter.WriteMode -> "distributed")
```

## API Test: `saveAsIndex`

### Signature
```scala
def saveAsIndex(indexPath: String, oformat: String = "rtree"): Unit
def saveAsIndex(partitionedRDD: JavaPartitionedSpatialRDD, indexPath: String): Unit
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/indexing/IndexMixin.scala:92  (+1 more definition site/overload)_

### Goal
Writes a spatially partitioned RDD to disk as a set of files (one for each partition) and generates a `_master` file that stores spatial metadata about the partitions for efficient future querying.

### Parameters
- `indexPath` (`String`): The output directory path where the partitioned files and the `_master` index file will be written.
- `oformat` (`String`), default `"rtree"`: The format of the local index to build within each partition file.

### Input
A spatially partitioned RDD of vector features. The RDD **must** be partitioned prior to calling this method using a spatial partitioner (e.g., `rdd.spatialPartition(classOf[RSGrovePartitioner])` or `rdd.partitionBy(...)`). If downstream tasks require disjoint partitions to avoid duplicate results, you must use a partitioner that supports disjoint partitioning (`GridPartitioner`, `RSGrovePartitioner`, `KDTreePartitioner`, or `STRPartitioner`).

### Output
Returns `Unit` — writes the partitioned data and a `_master` index file to the specified `indexPath` on the file system.

### Valid Call Patterns
```scala
// Indexing a dataset after spatial partitioning (from project README)
sparkContext.shapefile("ne_10m_admin_1_states_provinces.zip")
    .partitionBy(classOf[RSGrovePartitioner])
    .saveAsIndex("provinces_index", "rtree")

// Alternative using spatialPartition (based on test suite sibling patterns)
val data = sparkContext.readCSVPoint("points.csv")
val partitionedData = data.spatialPartition(classOf[RSGrovePartitioner])
partitionedData.saveAsIndex("points_index", "rtree")
```

### LLM Instruction Prompt
- ALWAYS ensure the RDD is spatially partitioned (e.g., via `spatialPartition` or `partitionBy`) before calling `saveAsIndex`.
- Use the instance method syntax `rdd.saveAsIndex(path, format)` for Scala RDDs.
- Do not invent file paths; use the exact output path provided by the user.
- If the user requires disjoint partitions, explicitly use `RSGrovePartitioner`, `GridPartitioner`, `KDTreePartitioner`, or `STRPartitioner` before saving.

### Prompt Snippet
```text
To persist a spatially partitioned RDD with an index, use `rdd.saveAsIndex(indexPath: String, oformat: String = "rtree")`. The RDD MUST be partitioned first (e.g., `rdd.spatialPartition(classOf[RSGrovePartitioner])`). This writes one file per partition plus a `_master` metadata file.
```

### Common Failure Modes
- **Missing Partitioning:** Calling `saveAsIndex` directly on an unpartitioned RDD (like the immediate output of `sc.shapefile`) will fail or produce an invalid index. It requires a spatially partitioned RDD.
- **Overlapping Partitions for Strict Queries:** Using a non-disjoint partitioner before saving, which can lead to duplicate results in custom algorithms or range queries loaded from this index later.

### Fix Code Hint
```scala
// WRONG: Calling saveAsIndex on an unpartitioned RDD
val features = sparkContext.shapefile("data.zip")
features.saveAsIndex("output_index") // Missing spatial partitioning

// CORRECT: Spatially partition the RDD first
val partitionedFeatures = features.spatialPartition(classOf[RSGrovePartitioner])
partitionedFeatures.saveAsIndex("output_index", "rtree")
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
Save a distributed collection of spatial vector features to disk in KML (Keyhole Markup Language) format, typically for visualization in GIS software or virtual globes.

### Parameters
- `rdd` (`JavaSpatialRDD`): The spatial RDD containing the vector features to be saved. This parameter is only used in the Java API overload (`JavaSpatialRDDHelper.saveAsKML`). In Scala, the RDD is the implicit receiver.
- `filename` (`String`): The destination file path or directory name where the KML output will be written.

### Input
A spatial RDD containing vector geometries (e.g., `RDD[IFeature]` in Scala or `JavaSpatialRDD` in Java). The input must consist of vector data (points, lines, polygons) loaded from formats like Shapefile, GeoJSON, or CSV, or generated via vector operations (like spatial joins or summaries). It cannot be a `RasterRDD`.

### Output
Returns `Unit` — this is a terminal action that triggers Spark job execution and writes the vector features to the specified `filename` as KML data.

### Valid Call Patterns
```scala
// Scala (called as an extension method on a Spatial RDD)
records.saveAsKML("output.kml")

// Java (called via the static helper)
JavaSpatialRDDHelper.saveAsKML(records, "output.kml")
```

### LLM Instruction Prompt
- Use `saveAsKML(filename)` as an extension method on vector RDDs (`RDD[IFeature]`) in Scala to export geometries to KML.
- For Java pipelines, use the static method `JavaSpatialRDDHelper.saveAsKML(rdd, filename)`.
- NEVER call `saveAsKML` on a `RasterRDD`. KML is strictly a vector output format in Beast; rasters must be saved using `saveAsGeoTiff`.

### Prompt Snippet
```text
To export vector features to KML in Beast, use `rdd.saveAsKML("path.kml")` in Scala or `JavaSpatialRDDHelper.saveAsKML(rdd, "path.kml")` in Java. Do not use this method for raster data (use `saveAsGeoTiff` instead).
```

### Common Failure Modes
- **Type Mismatch (Raster vs. Vector):** Attempting to call `saveAsKML` on a `RasterRDD` (e.g., after `sc.geoTiff` or `mapPixels`). KML is a vector-only format.
- **Missing Implicits in Scala:** If `saveAsKML` is not resolved on an `RDD[IFeature]`, the Beast SparkContext implicits may not be imported, preventing the extension method from being attached to the RDD.

### Fix Code Hint
```scala
// INCORRECT: Attempting to save a RasterRDD as KML
// val raster = sc.geoTiff[Int]("input.tif")
// raster.saveAsKML("output.kml") // Fails: KML is for vectors

// CORRECT: Saving vector features (e.g., from a Shapefile) as KML
import edu.ucr.cs.bdlab.beast._
val records = sc.shapefile("ne_10m_admin_0_countries.zip")
records.saveAsKML("countries_output.kml")
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
Save a distributed collection of spatial vector features (an RDD) to disk as an Esri Shapefile.

### Parameters
- `filename` (`String`): The output path and filename where the shapefile will be written (e.g., `"output.shp"` or a compressed `"output.zip"`).
- `opts` (`BeastOptions`), default `new BeastOptions()`: Optional configuration parameters to customize the write behavior.

### Input
A `SpatialRDD` (in Scala) or `JavaSpatialRDD` (in Java) containing vector features (points, lines, or polygons). This operation is strictly for vector data and cannot be used directly on raster data (`RasterRDD`).

### Output
Returns `Unit` — The operation produces no return value. Its side effect is writing the vector features to the specified file path as an Esri Shapefile (compressed `.zip` or uncompressed).

### Valid Call Patterns
```scala
// Scala (as an extension method on a SpatialRDD)
records.saveAsShapefile("output.shp")

// Java (using the helper class)
JavaSpatialRDDHelper.saveAsShapefile(records, "output.shp");
```

### LLM Instruction Prompt
- When saving vector features to a Shapefile in Scala, use the extension method `rdd.saveAsShapefile(filename)`.
- When writing Java code, use the static method `JavaSpatialRDDHelper.saveAsShapefile(rdd, filename)`.
- Never invent file paths; strictly use the output filename provided in the task.
- Ensure the dataset being saved is a vector RDD (e.g., `RDD[IFeature]`), not a `RasterRDD`. If you have raster data, use `saveAsGeoTiff` instead.

### Prompt Snippet
```text
To save vector features as a Shapefile in Beast:
Scala: `vectorRdd.saveAsShapefile("path/to/output.shp")`
Java: `JavaSpatialRDDHelper.saveAsShapefile(vectorRdd, "path/to/output.shp");`
Do not use this on RasterRDDs. Never invent file paths.
```

### Common Failure Modes
- **Type Mismatch (Raster vs Vector):** Attempting to call `saveAsShapefile` on a `RasterRDD` or `RDD[ITile[T]]`. Shapefiles only support vector geometries.
- **Missing Java Helper:** Attempting to call `rdd.saveAsShapefile(...)` in Java instead of using `JavaSpatialRDDHelper.saveAsShapefile(rdd, ...)`.

### Fix Code Hint
```scala
// WRONG: Calling saveAsShapefile on a RasterRDD
val raster = sc.geoTiff[Int]("input.tif")
raster.saveAsShapefile("output.shp") // Fails: RasterRDD does not support saveAsShapefile

// RIGHT: Calling saveAsShapefile on a Vector RDD
val vectors: RDD[IFeature] = sc.shapefile("input.zip")
val filtered = vectors.filter(f => f.getAsGeom.getArea > 100)
filtered.saveAsShapefile("output.shp")
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
Save a distributed collection of spatial features to a CSV or TSV file where the vector geometry is encoded in Well-Known Text (WKT) format.

### Parameters
- `rdd` (`JavaSpatialRDD`): (Java API overload only) The distributed collection of spatial features to be saved. In Scala, this method is called directly on the RDD as an extension method.
- `filename` (`String`): The path or name of the output file/directory where the data will be written.
- `wktColumn` (`Int`): The zero-based index of the column that will contain the WKT geometry string in the output file.
- `delimiter` (`Char`): The character used to separate attributes in the output file (defaults to `\t` for tab-separated values).
- `header` (`Boolean`): Whether to write a header line containing attribute names at the top of the file (defaults to `true`).

### Input
A Spatial RDD (`RDD[IFeature]` in Scala or `JavaSpatialRDD` in Java) containing vector geometries and their associated attributes. The caller must provide a valid output path (`filename`) that does not already exist, as per standard Spark behavior.

### Output
Returns `Unit` — writes the spatial features to the specified `filename` path as a distributed text file (typically a directory containing `part-xxxxx` files) formatted as CSV/TSV with WKT geometries.

### Valid Call Patterns
```scala
// Scala: Called as an extension method on a Spatial RDD
records.saveAsWKTFile("output.csv", 0, '\t', false)

// Java: Called via the JavaSpatialRDDHelper utility class
JavaSpatialRDDHelper.saveAsWKTFile(records, "output.csv", 0, '\t', false)
```

### LLM Instruction Prompt
- Use `saveAsWKTFile` to export vector RDDs to a text-based format (CSV/TSV) with geometries represented as WKT strings.
- In Scala, call this as an extension method directly on the `RDD[IFeature]` (e.g., `rdd.saveAsWKTFile(...)`). Do not pass the RDD as the first argument in Scala.
- Always specify the `wktColumn` index to dictate where the geometry string should be placed in the output row.
- Remember that Spark will write this as a directory of part-files, not a single flat file, and the target path must not already exist.

### Prompt Snippet
```text
To export vector features to a CSV with WKT geometries in Beast, use the `saveAsWKTFile` extension method on the RDD. Specify the output path, the zero-based index for the WKT column, the delimiter, and whether to include a header. Example: `features.saveAsWKTFile("out_path", 0, ',', true)`.
```

### Common Failure Modes
- **Path Already Exists:** Spark will throw an exception if the `filename` directory already exists. Ensure the output path is clear before saving.
- **Invalid Column Index:** Providing a `wktColumn` index that is out of bounds for the feature's schema or desired output format.
- **Syntax Error in Scala:** Attempting to call `saveAsWKTFile(rdd, ...)` in Scala. The explicit `rdd` parameter is only for the `JavaSpatialRDDHelper` Java API. In Scala, it must be called as `rdd.saveAsWKTFile(...)`.

### Fix Code Hint
```scala
// WRONG: Calling the Java signature in Scala
saveAsWKTFile(myRdd, "output.csv", 0, ',', true)

// CORRECT: Using the Scala extension method
myRdd.saveAsWKTFile("output.csv", 0, ',', true)
```

## API Test: `saveFeatures`

### Signature
```scala
def saveFeatures(features: SpatialRDD, oFormat: String, outPath: String, opts: BeastOptions): Unit
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/SpatialWriter.scala:123_

_Source doc:_ Saves the given set of features to the output using the provided output format. @param features the set of features to store to the output @param oFormat the output format to use for writing @param outPath the path to write the output to @param opts user options to configure the writer

### Goal
Saves a distributed collection of spatial vector features (`SpatialRDD`) to a specified output path in a supported vector format (e.g., GeoJSON, Shapefile).

### Parameters
- `features` (`SpatialRDD`): The distributed dataset of spatial features (`RDD[IFeature]`) to be written to disk.
- `oFormat` (`String`): The short name of the output format to use (e.g., `"geojson"`, `"shapefile"`, `"csv"`, `"kml"`, `"kmz"`).
- `outPath` (`String`): The destination file or directory path where the output will be written.
- `opts` (`BeastOptions`): Configuration options for the writer, such as compression settings or format-specific flags.

### Input
The caller must provide a valid `SpatialRDD` containing vector geometries. The `oFormat` string must match one of Beast's supported vector output formats: CSV, Esri Shapefile, GeoJSON, JSON+WKT, KML, or KMZ. Note that this API is strictly for vector data; raster data (GeoTIFF/HDF) uses different save methods (e.g., `saveAsGeoTiff`).

### Output
Returns `Unit` — writes the features to the filesystem at `outPath`. Depending on the format and `BeastOptions`, this may produce a single file, a directory of partitioned files, or compressed archives (e.g., `.bz2` or `.zip`). For example, writing a `"shapefile"` will generate the required `.shp`, `.shx`, and `.dbf` files.

### Valid Call Patterns
```scala
import edu.ucr.cs.bdlab.beast.io.SpatialWriter
import edu.ucr.cs.bdlab.beast.common.BeastOptions

// Example 1: Save features as a GeoJSON file
SpatialWriter.saveFeatures(features, "geojson", "output_path.geojson", new BeastOptions())

// Example 2: Save features as an Esri Shapefile
SpatialWriter.saveFeatures(features, "shapefile", "output_path.shp", new BeastOptions())
```

### LLM Instruction Prompt
- Always call `saveFeatures` statically on the `SpatialWriter` object, not as a method on the RDD itself.
- Ensure `oFormat` is a supported vector output format string (e.g., `"geojson"`, `"shapefile"`, `"csv"`, `"kml"`, `"kmz"`).
- Always provide a `BeastOptions` instance for the `opts` parameter, even if no special configuration is needed (use `new BeastOptions()`).
- Do not use this method for saving raster data; use `saveAsGeoTiff` for `RasterRDD`.

### Prompt Snippet
```text
To save a SpatialRDD of vector features to disk, use `SpatialWriter.saveFeatures(features, format, path, new BeastOptions())`. Supported formats include "geojson", "shapefile", "csv", "kml", and "kmz".
```

### Common Failure Modes
- **Calling on the RDD:** Attempting to call `features.saveFeatures(...)` will fail compilation. It must be called via `SpatialWriter.saveFeatures(...)`.
- **Missing Options Parameter:** Forgetting to pass the fourth argument (`opts: BeastOptions`) will cause a signature mismatch.
- **Unsupported Format:** Passing a raster format like `"geotiff"` or an unrecognized string to `oFormat` will cause a runtime failure, as this writer is designed for vector features.

### Fix Code Hint
```scala
// WRONG: features.saveFeatures("shapefile", "out.shp")
// WRONG: SpatialWriter.saveFeatures(features, "shapefile", "out.shp") // Missing BeastOptions

// RIGHT: 
SpatialWriter.saveFeatures(features, "shapefile", "out.shp", new BeastOptions())
```

## API Test: `saveIndex2`

### Signature
```scala
def saveIndex2(partitionFeatures: SpatialRDD, path: String, opts: BeastOptions): Unit
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/indexing/IndexHelper.scala:541_

_Source doc:_ Saves a partitioned RDD to disk. Each partition is stored to a separate file and an additional master file that stores the partition information. @param partitionFeatures a set of partitioned features @param path the path to store the files @param opts additional options for storing the data

### Goal
Saves a spatially partitioned RDD of vector features to disk, writing each partition to a separate file alongside a master index file that stores the partition boundaries and metadata.

### Parameters
- `partitionFeatures` (`SpatialRDD`): The spatially partitioned RDD of vector features (`RDD[IFeature]`) to be saved.
- `path` (`String`): The destination directory path where the partition files and the master index file will be written.
- `opts` (`BeastOptions`): Additional configuration options for storing the data, such as specifying the output format (e.g., `"oformat" -> "wkt(0)"`).

### Input
- **Data:** A `SpatialRDD` containing vector geometries.
- **Preconditions:** The input RDD **must** be spatially partitioned prior to calling this method (e.g., using `rdd.spatialPartition(classOf[RSGrovePartitioner])` or `IndexHelper.partitionFeatures2`). The RDD must have a defined `SpatialPartitioner` so that the master index file can be generated correctly.
- **Formats:** Output formats are controlled via `opts`. Valid vector output formats include CSV (WKT/points), Esri Shapefile, GeoJSON, KML, and KMZ.

### Output
Returns `Unit` — writes a directory to the specified `path` containing individual data files for each spatial partition and a master index file (which stores the partition information for optimized future loading).

### Valid Call Patterns
```scala
// Authoritative usage from the project test suite
val partitionedFeatures: RDD[IFeature] = IndexHelper.partitionFeatures2(features, 
  new GridPartitioner(new EnvelopeNDLite(2, 0.0, 0.0, 4.0, 4.0), Array(2, 2)))

val outPath = new File(scratchDir, "index")
IndexHelper.saveIndex2(partitionedFeatures, outPath.getPath, "oformat" -> "wkt(0)")
```

### LLM Instruction Prompt
- Call `saveIndex2` statically via the `IndexHelper` object (i.e., `IndexHelper.saveIndex2(...)`).
- **Crucial Precondition:** Ensure the input `SpatialRDD` is spatially partitioned before calling this method.
- Pass output format options via `BeastOptions`. If implicit conversions are in scope, a tuple like `"oformat" -> "wkt(0)"` or `"oformat" -> "csv"` can be passed directly as the `opts` argument.

### Prompt Snippet
```text
Use `IndexHelper.saveIndex2(partitionedRDD, path, opts)` to save a spatially partitioned vector RDD to disk along with a master index file. The RDD must be partitioned first (e.g., via `spatialPartition`).
```

### Common Failure Modes
- **Unpartitioned RDD:** Passing an RDD that lacks a `SpatialPartitioner`. The method expects the RDD to be partitioned so it can extract partition boundaries for the master index file.
- **Path Already Exists:** Spark will throw an exception if the target output directory already exists.
- **Missing Implicits for Options:** If Beast's implicit conversions are not in scope, passing a tuple like `"oformat" -> "wkt(0)"` will fail to compile. In such cases, explicitly instantiate the options object: `new BeastOptions().set("oformat", "wkt(0)")`.

### Fix Code Hint
```scala
// FIX: Ensure the RDD is partitioned before saving, and call via IndexHelper
val partitioned = features.spatialPartition(classOf[RSGrovePartitioner])
IndexHelper.saveIndex2(partitioned, "output_path", new BeastOptions().set("oformat", "geojson"))
```

## API Test: `saveTiles`
_Grounding: doc-repaired from source (docfix)._

### Signature
```scala
def saveTiles(tiles: JavaPairRDD[java.lang.Long, IntermediateVectorTile], outPath: String, opts: BeastOptions): Unit
def saveTiles(tiles: RDD[(Long, IntermediateVectorTile)], outPath: String, opts: BeastOptions): Unit
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/MVTDataVisualizer.scala:453_

### Goal
ADVANCED/LOW-LEVEL API (Note: recommended for exclusion from the main user-facing denominator). Saves a distributed RDD of intermediate Mapbox Vector Tiles (MVT) to a specified output path. It unconditionally generates an `index.html` viewer and `_visualization.properties` file, creating a ready-to-serve static web map directory.

### Parameters
- `tiles` (`RDD[(Long, IntermediateVectorTile)]`): The distributed set of vector tiles to save.
- `outPath` (`String`): The destination file system path.
- `opts` (`BeastOptions`): Configuration options for the Beast environment.

### Input
ADVANCED/LOW-LEVEL: Requires an `RDD[(Long, IntermediateVectorTile)]`. For testing, an empty RDD is sufficient because the driver-side metadata files are always written regardless of RDD content.

### Output
Returns `Unit`. Writes MVT files (if any) and driver-side metadata (`index.html`, `_visualization.properties`) to the filesystem at `outPath`.

### Valid Call Patterns
```scala
import edu.ucr.cs.bdlab.beast.common.BeastOptions
import edu.ucr.cs.bdlab.davinci.MVTDataVisualizer
import edu.ucr.cs.bdlab.davinci.IntermediateVectorTile
import org.apache.hadoop.fs.Path

// Caller-owned objects: BeastOptions, empty RDD
val opts = new BeastOptions()
val tilesRDD = sc.emptyRDD[(Long, IntermediateVectorTile)]

MVTDataVisualizer.saveTiles(tilesRDD, output_dir, opts)

// Verify execution via unconditionally written metadata
val outPath = new Path(output_dir, "index.html")
val fs = outPath.getFileSystem(sc.hadoopConfiguration)
assert(fs.exists(outPath), "index.html should be generated even for an empty RDD")
```

### LLM Instruction Prompt
- This is an ADVANCED/LOW-LEVEL API. Test it using `sc.emptyRDD[(Long, IntermediateVectorTile)]`.
- Do not deliberately fail the test with an `AssertionError`.
- Verify the output by checking for the existence of the `index.html` file in the output directory, which `saveTiles` writes regardless of whether the RDD contains any tiles.
- Always use the `MVTDataVisualizer` object as the receiver.

### Prompt Snippet
```text
To test `saveTiles`, use `sc.emptyRDD[(Long, IntermediateVectorTile)]` and verify success by asserting the existence of `index.html` in the output directory. Do not throw an AssertionError.
```

### Common Failure Modes
- **Test Abandonment (The failure that just happened):** Throwing an `AssertionError` because the author assumed an empty RDD would not produce verifiable output and lacked documentation to construct a valid `IntermediateVectorTile`. Fix: Use `sc.emptyRDD` and verify the unconditionally written `index.html`.
- **Type Mismatch:** Attempting to pass an `RDD[IFeature]` or `RasterRDD` directly to `saveTiles`. It strictly requires `RDD[(Long, IntermediateVectorTile)]`.
- **Missing Object Qualifier:** Calling `saveTiles(...)` as an RDD extension method instead of `MVTDataVisualizer.saveTiles(...)`.

### Fix Code Hint
```scala
// WRONG: Deliberately failing because IntermediateVectorTile is hard to construct
// throw new AssertionError("missing documentation for IntermediateVectorTile constructor")

// RIGHT: Use an empty RDD and verify the unconditionally generated index.html
val tilesRDD = sc.emptyRDD[(Long, IntermediateVectorTile)]
MVTDataVisualizer.saveTiles(tilesRDD, output_dir, new BeastOptions())
val outPath = new Path(output_dir, "index.html")
assert(outPath.getFileSystem(sc.hadoopConfiguration).exists(outPath), "index.html should be generated even for an empty RDD")
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
Saves a distributed collection of intermediate Mapbox Vector Tiles (MVT) into a single compact ZIP archive for web-based exploration and serving.

### Parameters
- `tiles` (`JavaPairRDD[java.lang.Long, IntermediateVectorTile]` or `RDD[(Long, IntermediateVectorTile)]`): The distributed set of intermediate vector tiles to save, keyed by their encoded tile ID.
- `outPath` (`String`): The destination file path where the output ZIP archive will be written (e.g., `"provinces_mvt.zip"`).
- `_opts` (`BeastOptions`): Additional configuration options that were used during the visualization/plotting phase (e.g., threshold settings).

### Input
- **Data/Formats:** Requires an RDD of intermediate vector tiles, which is typically generated by calling `MVTDataVisualizer.plotAllTiles(...)` on a vector dataset (like a Shapefile or GeoJSON). 
- **Preconditions:** The input vector data used to generate the tiles should ideally be spatially partitioned and indexed (e.g., using `RSGrovePartitioner` and saved as an rtree index) for efficient multilevel visualization. The `_opts` provided here should match the options used when generating the tiles.

### Output
Returns `Unit` — writes a ZIP file containing the MVT vector tile archive to the specified `outPath`. This archive can be served by the BeastServer or other MVT-compatible web map servers.

### Valid Call Patterns
```scala
// Define visualization options
val opts: BeastOptions = "threshold" -> 0

// Generate the multilevel visualization tiles from vector features
val tiles = MVTDataVisualizer.plotAllTiles(features, levels=0 to 6, resolution=256, buffer=5, opts)

// Save the tiles to a compact ZIP archive
MVTDataVisualizer.saveTilesCompact(tiles, "provinces_mvt.zip", opts)
```

### LLM Instruction Prompt
- When saving Mapbox Vector Tiles (MVT) generated by Beast, always call `MVTDataVisualizer.saveTilesCompact(tiles, outPath, opts)`.
- Do NOT attempt to call `saveTilesCompact` as a method directly on the RDD (e.g., `tiles.saveTilesCompact(...)`); it is a method on the `MVTDataVisualizer` object.
- Always pass the exact same `BeastOptions` instance to `saveTilesCompact` that was used in the preceding `plotAllTiles` call to ensure consistency.
- The `outPath` should typically end with `.zip` as the output format is a ZIP archive containing the tile hierarchy.

### Prompt Snippet
```text
To save generated vector tiles, use `MVTDataVisualizer.saveTilesCompact(tiles, "output.zip", opts)`. Do not call it as an RDD method. Pass the same `BeastOptions` used during `plotAllTiles`.
```

### Common Failure Modes
- **Method Not Found on RDD:** Attempting to call `tiles.saveTilesCompact(...)` will fail compilation because `saveTilesCompact` is not an implicit extension on `RDD`; it must be called on the `MVTDataVisualizer` object.
- **Mismatched Options:** Passing a new, empty `BeastOptions` instead of the one used during `plotAllTiles` can result in missing metadata or incorrect tile formatting in the final archive.
- **Invalid Output Path:** Providing an output path for a directory instead of a file path (e.g., ending in `.zip`) may cause write errors, as the function explicitly writes a single ZIP file.

### Fix Code Hint
```scala
// WRONG: Calling as an RDD method
tiles.saveTilesCompact("output_mvt.zip", opts)

// RIGHT: Calling on the MVTDataVisualizer object
MVTDataVisualizer.saveTilesCompact(tiles, "output_mvt.zip", opts)
```

## API Test: `selectFiles`

### Signature
```scala
def selectFiles(fileSystem: FileSystem, dir: String, range: Geometry): Array[String]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterFileRDD.scala:233_

_Source doc:_ Selects all the raster files that could potentially overlap the given query range from a directory of files. If that directory contains an index file, i.e., "_index.csv", then this index is used to prune files that are not relevant. If no index file is there, then all files are returned. @param fileSystem the file system at which the raster files exist @param dir the directory that contains the raster files @param range the query range to limit the files @return the list of files that potentially overlap the given query range

### Goal
Selects raster files from a directory that potentially overlap a given spatial query range, utilizing an optional `_index.csv` file for efficient pruning.

### Parameters
- `fileSystem` (`FileSystem`): The Hadoop `FileSystem` instance where the raster files reside (typically obtained via `FileSystem.get(sparkContext.hadoopConfiguration)`).
- `dir` (`String`): The path to the directory containing the raster files (and optionally the `_index.csv` file).
- `range` (`Geometry`): A JTS `Geometry` representing the spatial query range (e.g., a bounding box or polygon) used to limit the returned files.

### Input
A directory containing raster files (such as GeoTIFFs or HDFs) accessible via the provided Hadoop `FileSystem`. For the spatial pruning to work, the directory must contain an index file named `_index.csv` (usually generated via `RasterFileRDD.buildIndex`). If this index file is missing, the function will fall back to returning all files in the directory. The `range` parameter must be a valid JTS `Geometry` (often created from a JTS `Envelope`).

### Output
Returns `Array[String]` — An array of file paths (as strings) pointing to the raster files in the directory that potentially overlap the provided query range.

### Valid Call Patterns
```scala
// Assuming sparkContext is an initialized SparkContext and dir is a valid directory path
val geometryFactory = new GeometryFactory(new PrecisionModel(PrecisionModel.FLOATING_SINGLE), 4326)
val queryRange = geometryFactory.toGeometry(new Envelope(-100, -99, 27, 28))

val matchingFiles = RasterFileRDD.selectFiles(
  FileSystem.get(sparkContext.hadoopConfiguration), 
  dir.toString,
  queryRange
)
```

### LLM Instruction Prompt
- Call `selectFiles` on the `RasterFileRDD` object.
- Pass a valid Hadoop `FileSystem` object, the directory path as a `String`, and a JTS `Geometry` for the spatial range.
- Note that this function relies on the presence of an `_index.csv` file in the target directory to actually prune files; otherwise, it returns all files. If pruning is required, ensure `RasterFileRDD.buildIndex` is called beforehand.

### Prompt Snippet
```text
To find raster files overlapping a spatial range without loading them all into memory, use `RasterFileRDD.selectFiles(fileSystem, dir, geometry)`. It uses `_index.csv` in the directory to prune non-overlapping files, returning an Array[String] of matching file paths.
```

### Common Failure Modes
- **Silent Fallback (No Pruning):** Expecting the function to filter files when no `_index.csv` exists in the directory. The function will silently return all files instead of failing.
- **Uninitialized FileSystem:** Passing a null or improperly configured `FileSystem` object, which will cause runtime exceptions when attempting to read the directory or index file.
- **CRS Mismatch:** Providing a `Geometry` range in a Coordinate Reference System (CRS) that does not match the CRS of the bounding boxes stored in the `_index.csv`, leading to incorrect pruning (either missing files or returning non-overlapping files).

### Fix Code Hint
```scala
// Ensure the index is built before querying to guarantee pruning behavior
RasterFileRDD.buildIndex(sparkContext, dir.toString, new File(dir, "_index.csv").toString)

// Obtain the FileSystem from the SparkContext
val fs = FileSystem.get(sparkContext.hadoopConfiguration)

// Query the files
val matchingFiles = RasterFileRDD.selectFiles(fs, dir.toString, queryGeometry)
```

## API Test: `set`
_Grounding: doc-repaired from source (docfix)._

### Goal
Fluently sets a configuration key to a specified value (converting it to a string) within a `BeastOptions` instance. This is the primary user-facing configuration object used to pass parameters to Beast operations.

### Valid Call Patterns
```scala
import edu.ucr.cs.bdlab.beast.common.BeastOptions

val opts = new BeastOptions()
  .set("iformat", "wkt(Geometry)")
  .set("skipheader", true)
  .set("separator", "\t")
  .set("stroke", "blue")
  .set("some_number", 42)

// MUST use typed getters to retrieve unwrapped values
val iformatVal = opts.getString("iformat")
val skipheaderVal = opts.getString("skipheader")
val numberVal = opts.getString("some_number")

assert(iformatVal == "wkt(Geometry)", s"Expected 'wkt(Geometry)', got $iformatVal")
assert(skipheaderVal == "true", s"Expected 'true', got $skipheaderVal")
assert(numberVal == "42", s"Expected '42', got $numberVal")

println(s"__CHECK__ set $iformatVal, $skipheaderVal, $numberVal")
```

### LLM Instruction Prompt
- Use `.set(key, value)` on a `BeastOptions` instance to configure Beast operations.
- Chain multiple `.set()` calls fluently.
- Pass primitive types (like `true`, `false`, or numbers) directly as the `value` argument; the method accepts `Any` and handles string conversion internally.
- **CRITICAL:** `BeastOptions` extends `scala.collection.mutable.HashMap[String, String]`. Do NOT use the inherited `.get(key)` method for assertions, as it returns an `Option[String]`.
- To retrieve raw values for assertions or usage, callers MUST use the typed getters provided by `BeastOptions`, such as `.getString(key)`, `.getBoolean(key, default)`, or `.getInt(key, default)`.

### Prompt Snippet
```text
To configure Beast operations, instantiate `new BeastOptions()` and chain `.set(key, value)` calls. Because `BeastOptions` extends `HashMap[String, String]`, the inherited `.get(key)` returns an `Option[String]`. To retrieve raw values for assertions, you must use typed getters like `.getString(key)` or `.getBoolean(key, default)`.
```

### Common Failure Modes
- **Assertion failures from `Option` wrapping:** Calling `.get(key)` returns an `Option[String]` (e.g., `Some("wkt(Geometry)")`). Comparing this directly to a raw string `"wkt(Geometry)"` in an assertion will fail (`Expected 'wkt(Geometry)', got Some(wkt(Geometry))`).
- **Silent failures from misspelled keys:** Providing an invalid configuration key (e.g., `"format"` instead of `"iformat"`) will not throw an error during `.set()`, but downstream operations will ignore it.
- **Assuming type preservation:** Because `value` is converted to a string, passing complex objects expecting them to be retrieved as their original type later will fail.

### Fix Code Hint
```scala
// WRONG: Using inherited .get() which returns Option[String]
val opts = new BeastOptions().set("iformat", "wkt(Geometry)")
assert(opts.get("iformat") == "wkt(Geometry)") // Fails: Some("wkt(Geometry)") != "wkt(Geometry)"

// RIGHT: Using typed getters to retrieve unwrapped values
val opts = new BeastOptions().set("iformat", "wkt(Geometry)")
assert(opts.getString("iformat") == "wkt(Geometry)")
```

## API Test: `setBoolean`

### Signature
```scala
def setBoolean(key: String, value: Boolean): BeastOptions
```
_Source: beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/common/BeastOptions.scala:141_

_Source doc:_ Set key to a boolean value @param key @param value @return

### Goal
Sets a boolean configuration property within a `BeastOptions` object, returning the updated options to enable fluent method chaining.

### Parameters
- `key` (`String`): The configuration property name to set (e.g., `"fs.file.impl.disable.cache"`).
- `value` (`Boolean`): The boolean flag (`true` or `false`) to assign to the specified key.

### Input
An instantiated `BeastOptions` object that needs to be configured before passing it to a Beast/RDPro operation.

### Output
Returns `BeastOptions` — the updated configuration object itself, allowing multiple `.setBoolean()` or other setter calls to be chained sequentially.

### Valid Call Patterns
```scala
// Inferred from the signature and adapted from test-suite configuration patterns
val opts = new BeastOptions()
opts.setBoolean("fs.file.impl.disable.cache", true)
    .setBoolean("spatial.join.broadcast", false)
```

### LLM Instruction Prompt
- When configuring Beast operations that require boolean flags, call `setBoolean(key, value)` on a `BeastOptions` instance. Remember that it returns the `BeastOptions` object, so you can chain multiple configuration calls fluently. Do not pass string representations of booleans (e.g., `"true"`).

### Prompt Snippet
```text
Use `opts.setBoolean("key", true)` to set boolean flags in BeastOptions. Chain calls fluently since it returns the BeastOptions instance.
```

### Common Failure Modes
- **Type Mismatch:** Passing a string `"true"` or `"false"` instead of a native Scala `Boolean`.
- **Confusing with Hadoop Configuration:** Assuming the method returns `Unit` (like Hadoop's `Configuration.setBoolean`) and failing to take advantage of the fluent API for cleaner code.

### Fix Code Hint
```scala
// WRONG: Passing a string instead of a boolean
opts.setBoolean("fs.file.impl.disable.cache", "true")

// RIGHT: Passing a native boolean and chaining
opts.setBoolean("fs.file.impl.disable.cache", true)
    .setBoolean("another.flag", false)
```

## API Test: `setLong`

### Signature
```scala
def setLong(key: String, value: Long): BeastOptions
```
_Source: beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/common/BeastOptions.scala:122_

_Source doc:_ Set a key to a long value @param key @param value @return

### Goal
Sets a configuration key to a 64-bit integer (`Long`) value within a `BeastOptions` instance, used to parameterize Beast operations like multilevel plotting, spatial data loading, or algorithm tuning.

### Parameters
- `key` (`String`): The configuration property name to set (e.g., `"threshold"`).
- `value` (`Long`): The numeric value to assign to the specified property.

### Input
An existing or newly instantiated `BeastOptions` object. The `key` must be a valid configuration string recognized by the downstream Beast operation (such as visualization or spatial partitioning). 

### Output
Returns `BeastOptions` — The updated `BeastOptions` instance itself, enabling fluent method chaining.

### Valid Call Patterns
```scala
// From the project's documented usage for configuring a multilevel plot
val opts = new BeastOptions()
  .set("stroke", "blue")
  .set("fill", "#9999E6")
  .setLong("threshold", 0)
```

### LLM Instruction Prompt
- When configuring Beast operations (like `MultilevelPlot.plotFeatures`) that require numeric parameters, use `setLong(key, value)` on a `BeastOptions` instance. Because it returns `BeastOptions`, always chain it fluently with other `.set()` or `.setLong()` calls. Do not confuse this with `sparkContext.hadoopConfiguration.setLong`, which returns `Unit` and cannot be chained.

### Prompt Snippet
```text
Use `.setLong("key", value)` on a `BeastOptions` instance to configure numeric parameters for Beast operations. Chain it fluently with other configuration methods (e.g., `new BeastOptions().set("color", "red").setLong("threshold", 100L)`).
```

### Common Failure Modes
- **Type Mismatch:** Passing a `String` (e.g., `"0"`) instead of a numeric `Long` or `Int` value, which will cause a compilation error.
- **Chaining Hadoop Configuration:** Attempting to chain `setLong` calls on `sparkContext.hadoopConfiguration`. While Hadoop's configuration also has a `setLong` method, it returns `Unit` (void) and will break the chain, unlike `BeastOptions.setLong`.

### Fix Code Hint
```scala
// Incorrect: Passing a string instead of a Long
// val opts = new BeastOptions().setLong("threshold", "0")

// Incorrect: Attempting to chain Hadoop's Configuration
// sparkContext.hadoopConfiguration.setLong(SpatialFileRDD.MaxSplitSize, 1024).setBoolean(...)

// Correct: Chaining on BeastOptions with a valid numeric type
val opts = new BeastOptions()
  .set("stroke", "blue")
  .setLong("threshold", 0L)

// Correct: Sequential calls for Hadoop Configuration (no chaining)
sparkContext.hadoopConfiguration.setLong(SpatialFilePartitioner.MaxSplitSize, 500L)
sparkContext.hadoopConfiguration.setBoolean("fs.file.impl.disable.cache", true)
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
Mutates a specific pixel in a local raster tile (such as a `MemoryTile`) by setting its value at the given column and row coordinates.

### Parameters
- `i` (`Int`): The column position (x-coordinate) of the pixel within the tile.
- `j` (`Int`): The row position (y-coordinate) of the pixel within the tile.
- `value` (`T`): The value to set at the given pixel. The type must exactly match the tile's generic type parameter `T` (e.g., `Float` for single-band, `Array[Float]` for multi-band).

### Input
A mutable tile instance (e.g., `MemoryTile[T]`) that has been initialized with valid `RasterMetadata`. The coordinates `i` and `j` must fall within the tile's local dimensions. The type of the `value` provided must strictly align with the tile's runtime pixel type (e.g., `Int`, `Float`, `Array[Int]`, or `Array[Float]`).

### Output
Returns `Unit` — this is an in-place mutation that updates the internal pixel array of the tile.

### Valid Call Patterns
```scala
// Single-band tile mutation
val tile1 = new MemoryTile[Float](0, metadata, RasterFeature.create(Array("fileName"), Array("testFile.tif")))
tile1.setPixelValue(0, 0, 0.5f)
tile1.setPixelValue(1, 0, 0.25f)

// Multi-band tile mutation
val tile2 = new MemoryTile[Array[Float]](0, metadata, RasterFeature.create(Array("fileName"),Array("testFile.tif")))
tile2.setPixelValue(0, 0, Array(0.5f, 0.1f))
tile2.setPixelValue(1, 0, Array(0.25f, 0.4f))
```

### LLM Instruction Prompt
- When mutating a local raster tile (like `MemoryTile[T]`), use `tile.setPixelValue(i, j, value)`. 
- Ensure the type of `value` exactly matches the tile's type parameter `T`. Do not pass a scalar `Float` to a `MemoryTile[Array[Float]]`, and do not pass an `Int` to a `MemoryTile[Float]`.
- Remember that `i` represents the column (x) and `j` represents the row (y).
- This is a local, low-level tile operation, not a distributed `RasterRDD` operation.

### Prompt Snippet
```text
To set a pixel value in a local RDPro tile, use `tile.setPixelValue(i, j, value)`. Ensure `value` matches the tile's generic type `T` (e.g., `Float` for single-band, `Array[Float]` for multi-band). `i` is the column index and `j` is the row index.
```

### Common Failure Modes
- **Type Mismatch:** Passing an integer (e.g., `5`) to a `MemoryTile[Float]`, which expects a `Float` (e.g., `5.0f`). Scala's strict typing requires exact matches for generic type `T`.
- **Multi-band vs Single-band Confusion:** Attempting to pass a single numeric value to a multi-band tile (`MemoryTile[Array[Float]]`), which requires an `Array` of values.
- **Index Out of Bounds:** Providing `i` or `j` values that exceed the tile's width or height as defined by its `RasterMetadata`.

### Fix Code Hint
```scala
// BAD: Type mismatch (passing Int to a Float tile)
tile.setPixelValue(0, 0, 5) 

// GOOD: Match the generic type T exactly
tile.setPixelValue(0, 0, 5.0f)

// BAD: Passing a scalar to a multi-band tile
multiBandTile.setPixelValue(0, 0, 5.0f)

// GOOD: Passing an Array to a multi-band tile
multiBandTile.setPixelValue(0, 0, Array(5.0f, 2.0f))
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
Reads vector features from an Esri Shapefile into a distributed `SpatialRDD` for large-scale geospatial analysis, spatial joins, or raster-vector (Raptor) joins.

### Parameters
- `filename` (`String`): The path to the `.shp` file, a compressed `.zip` file that contains shapefiles, or a directory that contains shapefiles or ZIP files.

### Input
- Requires an initialized `SparkContext` (or `JavaSpatialSparkContext`) typically named `sc` or `sparkContext` with Beast context extensions loaded.
- The target file must be a valid Esri Shapefile format (either uncompressed `.shp`, compressed `.zip`, or a directory of these).
- Do not invent file paths; use only the paths provided by the user or environment.

### Output
Returns `SpatialRDD` — a distributed Spark RDD of vector features (`IFeature`) representing the geometries and attributes from the shapefile. For Java APIs, it returns a `JavaSpatialRDD`.

### Valid Call Patterns
```scala
// Load a compressed shapefile archive
val records = sparkContext.shapefile("input.zip")

// Load an uncompressed shapefile
val buildings = sc.shapefile("MSBuildings_data_index.shp")

// Typical usage in a Raptor Join pipeline
val countries: SpatialRDD = sc.shapefile("ne_10m_admin_0_countries.zip")
val join = treecover.raptorJoin(countries)
```

### LLM Instruction Prompt
- Always call `shapefile` as an extension method on an initialized `SparkContext` (e.g., `sc.shapefile(path)` or `sparkContext.shapefile(path)`). Do not call it as a standalone function.
- Pass the exact file path provided in the task; never invent file paths.
- Remember that `shapefile` natively supports reading compressed `.zip` archives containing shapefiles, so there is no need to unzip them manually before loading.

### Prompt Snippet
```text
Use `sc.shapefile(filename)` to load Esri Shapefiles (.shp, .zip, or directories) into a SpatialRDD. Call it as an extension on the SparkContext.
```

### Common Failure Modes
- **Missing Context Extension:** Attempting to call `shapefile` without importing Beast implicits, resulting in a "value shapefile is not a member of org.apache.spark.SparkContext" compilation error.
- **Invented File Paths:** Hardcoding a path like `"data.shp"` instead of using the variable provided in the user's prompt.
- **Incorrect Receiver:** Calling `shapefile(path)` directly instead of `sc.shapefile(path)`.

### Fix Code Hint
```scala
// Ensure Beast context extensions are imported to enable sc.shapefile
import edu.ucr.cs.bdlab.beast._

// Use the provided SparkContext (sc) and the provided file path variable
val features: SpatialRDD = sc.shapefile(providedFilePath)
```

## API Test: `sierpinski`
_Grounding: doc-repaired from source (docfix)._

### Goal
Generate synthetic spatial data following a Sierpinski (fractal) distribution for benchmarking and testing distributed spatial algorithms. *Note: The actual number of generated features may not exactly match the requested `cardinality` due to the mathematical constraints of the Sierpinski fractal pattern, which relies on recursive geometric subdivisions.*

### Valid Call Patterns
```scala
import edu.ucr.cs.bdlab.beast._
import edu.ucr.cs.bdlab.beast.cg.SpatialDataTypes.SpatialRDD

// sc is an existing SparkContext
val cardinality = 1000L
val fractalData: SpatialRDD = sc.generateSpatialData.sierpinski(cardinality)

val count = fractalData.count()
// Do not assert exact equality; fractal distributions approximate the requested cardinality
assert(count > 0, s"Expected generated features, but got $count")
println(s"__CHECK__ sierpinski $count")
```

### LLM Instruction Prompt
Use `sc.generateSpatialData.sierpinski(cardinality)` to generate a `SpatialRDD` of synthetic fractal data. You must import `edu.ucr.cs.bdlab.beast._` and `edu.ucr.cs.bdlab.beast.cg.SpatialDataTypes.SpatialRDD`. Callers must not assert strict equality between the requested `cardinality` and the resulting RDD's `.count()`. The Sierpinski generator yields a mathematically valid geometric set based on recursive depths, which only approximates the requested integer. Assert `count > 0` instead.

### Prompt Snippet
```text
Use `sc.generateSpatialData.sierpinski(cardinality)` to generate a SpatialRDD of synthetic data. Do not assert strict equality on the resulting count; fractal distributions approximate the requested cardinality.
```

### Common Failure Modes
- **Strict Cardinality Assertion Failure:** `java.lang.AssertionError: assertion failed: Expected 1000 features, but got 500`. Writing `assert(count == cardinality)` fails because the Sierpinski algorithm generates points based on recursive fractal depths. It cannot arbitrarily stop at the exact requested integer without breaking the fractal pattern, so it yields the closest valid geometric set.
- **Missing Context Extensions:** Attempting to call `sc.generateSpatialData` without importing `edu.ucr.cs.bdlab.beast._`, resulting in a compilation error.

### Fix Code Hint
```scala
// WRONG: Asserting exact equality on fractal generation
val fractalData = sc.generateSpatialData.sierpinski(1000L)
assert(fractalData.count() == 1000L)

// CORRECT: Asserting > 0 because fractal depths approximate the cardinality
val fractalData = sc.generateSpatialData.sierpinski(1000L)
val count = fractalData.count()
assert(count > 0, s"Expected generated features, but got $count")
```

## API Test: `size`

### Signature
```scala
def size: Long
def size: Int
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/SpatialPartition.scala:41  (+2 more definition site/overload)_

_Source doc:_ Size in bytes

### Goal
Retrieves the size of a spatial object, representing either the memory footprint in bytes (e.g., for a `SpatialPartition`) or the total number of elements (e.g., for spatial join result collections and iterators).

### Parameters
_None._

### Input
A valid Beast spatial data structure, such as a `SpatialPartition` (to get byte size), or a collection/iterator of spatial join results like `PlaneSweepSpatialJoinIterator` or an `Array` of features (to get element count).

### Output
Returns `Long` — The size in bytes when called on specific spatial data structures (like partitions). The overloaded `def size: Int` returns the number of elements when called on standard collections or spatial iterators.

### Valid Call Patterns
```scala
// 1. Element count on an array of spatial join results (from test suite)
val results = SpatialJoin.spatialJoinIntersectsPlaneSweepFeatures(r.toArray, s.toArray,
  new EnvelopeNDLite(2, 2.0, 0.0, 5.0, 3.0), ESJPredicate.Intersects, null)
val count: Int = results.size

// 2. Element count on a spatial join iterator (from test suite)
val joinResults = new PlaneSweepSpatialJoinIterator(s1, s2, null)
val iteratorCount: Int = joinResults.size

// 3. Size in bytes on a spatial partition (inferred from signature and source doc)
val byteSize: Long = partition.size
```

### LLM Instruction Prompt
- Use `.size` to determine the memory footprint (in bytes, returning `Long`) of Beast spatial partitions, or to count the number of elements (returning `Int`) in spatial join result arrays and iterators.
- **Warning:** When calling `.size` on a Scala `Iterator` (such as `PlaneSweepSpatialJoinIterator`), the iterator will be fully consumed. Do not call `.size` if you intend to iterate over the results afterward.

### Prompt Snippet
```text
Calculate the number of intersecting feature pairs from the `PlaneSweepSpatialJoinIterator` and store it in a variable, keeping in mind that this will consume the iterator.
```

### Common Failure Modes
- **Consuming Iterators:** Calling `.size` on a `PlaneSweepSpatialJoinIterator` or similar one-time traversal object exhausts the iterator. Subsequent attempts to map, filter, or collect the iterator will yield empty results.
- **Semantic Confusion:** Assuming `.size` always returns an element count. On core Beast partition objects (like `SpatialPartition`), it returns the estimated size in bytes (`Long`), not the number of features.

### Fix Code Hint
```scala
// BAD: Consumes the iterator, making the subsequent .toArray call return an empty array
val joinResults = new PlaneSweepSpatialJoinIterator(s1, s2, null)
println(s"Found ${joinResults.size} matches") 
val data = joinResults.toArray 

// GOOD: Convert to an array or collection first if you need both the size and the data
val joinResults = new PlaneSweepSpatialJoinIterator(s1, s2, null)
val data = joinResults.toArray
println(s"Found ${data.size} matches")
```

## API Test: `slidingWindow`

### Signature
```scala
def slidingWindow[T: ClassTag, U: ClassTag](raster: RasterRDD[T], w: Int, f: (Array[T], Array[Boolean]) => U): RasterRDD[U]
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/RasterOperationsFocal.scala:711_

_Source doc:_ Performs a sliding window calculation for a window of size (2w + 1) &times; (2w + 1) given an integer value w. The user-defined window calculation function takes all values in the window ordered in row-major order. Additionally, a Boolean array of the same size is passed to indicate which values are defined and which are not. The Boolean array is useful for two scenarios. 1. When the window is near the edge of the raster, there must be some undefined values outside the raster. 2. Some pixel values in raster might be undefined, e.g., due to cloud coverage. *Note*: This function will only work correctly if all input tiles have the same raster metadata. @param raster the input raster to process @param w the radius of the square window. The window size will be (2w + 1) &times; (2w + 1) @param f the function to perform the calculation. @tparam T the type of values in the input raster @tparam U the type of output values (the result of the user-defined function). @return a new raster with the same dimensions as the input after applying the window function.

### Goal
Performs a focal (neighborhood) operation over a raster by applying a user-defined function to a sliding window of size (2w + 1) × (2w + 1) around each pixel.

### Parameters
- `raster` (`RasterRDD[T]`): The input distributed raster dataset to process.
- `w` (`Int`): The radius of the square window. For example, `w = 1` creates a 3×3 window, `w = 2` creates a 5×5 window.
- `f` (`(Array[T], Array[Boolean]) => U`): The user-defined function applied to each window. It receives an array of pixel values in row-major order and a corresponding boolean array indicating which pixels are valid/defined (true) versus out-of-bounds or NoData (false).

### Input
A `RasterRDD[T]` loaded from a GeoTIFF or HDF file (e.g., via `sc.geoTiff[T]`), or generated via rasterization. 
**Precondition:** This function will only work correctly if all input tiles have the exact same raster metadata (resolution, CRS, and tile size). If the input raster has mixed metadata, you must align it first using the Reshape API (e.g., `RasterOperationsFocal.reshapeNN` or `reshapeAverage`).

### Output
Returns `RasterRDD[U]` — A new distributed raster with the same dimensions and metadata as the input, where each pixel's value is the computed result of the user-defined sliding window function.

### Valid Call Patterns
```scala
// Example: 3x3 window smoothing (average) over an integer raster
val smoothedRaster: RasterRDD[Double] = RasterOperationsFocal.slidingWindow(
  raster, 
  1, 
  (values: Array[Int], defined: Array[Boolean]) => {
    var sum: Int = 0
    var count: Int = 0
    for (i <- values.indices; if defined(i)) {
      sum += values(i)
      count += 1
    }
    if (count == 0) 0.0 else sum.toDouble / count
  }
)
```

### LLM Instruction Prompt
- Always call this function using the object qualifier: `RasterOperationsFocal.slidingWindow(raster, w, f)`.
- The window size is determined by the radius `w`. To get a 3x3 window, pass `w = 1`.
- The user-defined function `f` MUST check the `defined` boolean array before utilizing a value from the `values` array. This prevents errors at the edges of the raster or when encountering undefined pixels (like cloud coverage).
- Ensure the input `RasterRDD` has uniform tile metadata. If the data comes from disparate sources or unaligned tiles, instruct the user to use `RasterOperationsFocal.reshapeNN` or `reshapeAverage` prior to calling `slidingWindow`.

### Prompt Snippet
```text
To perform focal operations like smoothing or edge detection, use `RasterOperationsFocal.slidingWindow(raster, w, f)`. The radius `w` defines a (2w+1)x(2w+1) window. Your function `f` receives `(values, defined)` arrays; always check `if (defined(i))` before using `values(i)` to safely handle raster edges and NoData pixels.
```

### Common Failure Modes
- **Mismatched Tile Metadata:** Calling `slidingWindow` on a raster whose tiles have varying resolutions, CRSs, or sizes. This violates the precondition and yields incorrect spatial calculations.
- **Ignoring the `defined` Array:** Blindly iterating over the `values` array without checking the `defined` array, leading to skewed calculations (incorporating garbage/NoData values) or errors at the raster boundaries where the window extends outside the image.

### Fix Code Hint
```scala
// WRONG: Fails to check if the pixel is defined, leading to edge-case bugs
val badRaster = RasterOperationsFocal.slidingWindow(raster, 1, (vals, defs) => vals.sum / vals.length)

// CORRECT: Safely filters using the `defined` array
val goodRaster = RasterOperationsFocal.slidingWindow(raster, 1, (vals, defs) => {
  val validVals = vals.indices.filter(defs).map(vals)
  if (validVals.isEmpty) 0 else validVals.sum / validVals.length
})
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
Reads a spatial vector file or directory of files into a distributed `SpatialRDD`, optionally auto-detecting the format based on the file extension and contents.

### Parameters
- `filename` (`String`): The path to the input file or directory of files (e.g., local file system or HDFS path).
- `format` (`String`), default `null`: The spatial format of the file (e.g., `"wkt"`, `"envelope"`, `"gpx"`, `"envelope(0,1,2,3)"`). If `null`, Beast attempts to auto-detect the format.
- `opts` (`BeastOptions`), default `new BeastOptions`: Additional configuration options for the reader, such as specifying a custom delimiter (e.g., `new BeastOptions("separator:,")`).

### Input
- **Data/Formats:** Supported vector input formats include CSV (points, WKT, envelopes), Esri Shapefile (compressed `.zip` or uncompressed), GeoJSON, JSON+WKT, and GPX.
- **Preconditions:** The caller must invoke this method on an initialized `SparkContext` (or `JavaSpatialSparkContext`). 
- **Auto-detection Warning:** If `format` is omitted or `null`, CSV auto-detection for geometry columns is a "best-effort" guess with no guarantee of correctness. It is highly recommended to explicitly provide the `format` string.
- **Raster Data:** Do *not* use this method for raster formats (GeoTIFF, HDF). Use `sc.geoTiff[T]` or `sc.hdfFile` instead.

### Output
Returns `SpatialRDD` — A distributed Spark RDD containing spatial vector records (features).

### Valid Call Patterns
```scala
// Explicitly specifying the format (Recommended)
val parks = sparkContext.spatialFile(parksFile.getPath, "wkt")

// Loading a GPX file
val records = sparkContext.spatialFile("input.gpx", "gpx")

// Loading an envelope index
val r1Disk: SpatialRDD = sparkContext.spatialFile(index1Path, "envelope")

// Java API usage with BeastOptions
JavaRDD<IFeature> rects = spatialSparkContext.spatialFile("rects.csv", "envelope(0,1,2,3)", new BeastOptions("separator:,"));
```

### LLM Instruction Prompt
- Always call `spatialFile` as an extension method on an initialized `SparkContext` (e.g., `sc.spatialFile(...)` or `sparkContext.spatialFile(...)`). Never call it as a bare function.
- Always explicitly provide the `format` parameter (e.g., `"wkt"`, `"gpx"`, `"envelope"`) to avoid the unreliable best-effort CSV auto-detection.
- Use `spatialFile` strictly for vector data. For raster data, you must use `sc.geoTiff[T]` or `sc.hdfFile`.

### Prompt Snippet
```text
Load the vector dataset using `sc.spatialFile` and explicitly specify the format to avoid auto-detection issues. Do not use this for rasters.
```

### Common Failure Modes
- **Calling on Raster Data:** Attempting to load a GeoTIFF or HDF file using `spatialFile`. This will fail or yield garbage data; rasters require `sc.geoTiff[T]` or `sc.hdfFile`.
- **Missing SparkContext Receiver:** Calling `spatialFile("data.csv")` without the `sc.` or `sparkContext.` prefix, resulting in a compilation error.
- **Incorrect CSV Parsing:** Omitting the `format` parameter for a complex CSV file, causing Beast's best-effort auto-detection to misidentify the geometry column.

### Fix Code Hint
```scala
// BAD: Bare function call and relying on CSV auto-detection
val vectors = spatialFile("data.csv")
val rasters = sc.spatialFile("image.tif")

// GOOD: Called on SparkContext with explicit format for vectors, and using geoTiff for rasters
val vectors = sc.spatialFile("data.csv", "wkt")
val rasters = sc.geoTiff[Int]("image.tif")
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
Finds overlapping or contained features between two massive vector datasets using distributed spatial join algorithms.

### Parameters
- `r1` (`SpatialRDD`): The first (left) spatial dataset to join. When using the instance method `rdd1.spatialJoin(...)`, `rdd1` acts as this parameter.
- `r2` (`SpatialRDD`): The second (right) spatial dataset to join.
- `joinPredicate` (`ESJPredicate`), default `ESJPredicate.Intersects`: The spatial relationship to test (e.g., `ESJPredicate.Intersects`, `ESJPredicate.Contains`). The default finds all non-disjoint features.
- `joinMethod` (`ESJDistributedAlgorithm`), default `null`: The specific distributed join algorithm to use (e.g., `ESJDistributedAlgorithm.DJ`, `PBSM`, `REPJ`, `BNLJ`). If `null`, Beast automatically selects the optimal algorithm based on the partitioning state of the inputs and cluster parallelism.
- `mbrCount` (`LongAccumulator`), default `null`: An optional Spark accumulator to count the number of Minimum Bounding Rectangle (MBR) tests performed during the algorithm.
- `opts` (`BeastOptions`), default `new BeastOptions()`: Additional configuration options for the Beast engine.

### Input
Two vector datasets loaded as `SpatialRDD` (e.g., from Shapefile, GeoJSON, CSV, or WKT). 
**Preconditions:**
*   If explicitly requesting the Distributed Join (`ESJDistributedAlgorithm.DJ`), **both** datasets must be spatially partitioned first (e.g., using `rdd.spatialPartition(classOf[RSGrovePartitioner])`).
*   If explicitly requesting the Repartition Join (`ESJDistributedAlgorithm.REPJ`), at least **one** dataset must be spatially partitioned.
*   To avoid duplicate results in custom algorithms, partitions must be disjoint. Only `GridPartitioner`, `RSGrovePartitioner`, `KDTreePartitioner`, and `STRPartitioner` support disjoint partitioning.

### Output
Returns `RDD[(IFeature, IFeature)]` — an RDD containing pairs of matching features from the left and right datasets that satisfy the spatial join predicate.

### Valid Call Patterns
```scala
// 1. Auto-selected algorithm (recommended if unsure about partitioning)
val joinResults = dataset1.spatialJoin(dataset2, ESJPredicate.Intersects)

// 2. Explicit algorithm (PBSM)
val sjResults: RDD[(IFeature, IFeature)] = matchedPolygons.spatialJoin(
  matchedPoints, 
  ESJPredicate.Contains, 
  ESJDistributedAlgorithm.PBSM
)

// 3. Distributed Join (DJ) on explicitly partitioned data
val partitioned1 = dataset1.spatialPartition(classOf[RSGrovePartitioner])
val partitioned2 = dataset2.spatialPartition(classOf[RSGrovePartitioner])
val djResults = partitioned1.spatialJoin(
  partitioned2, 
  ESJPredicate.Intersects, 
  ESJDistributedAlgorithm.DJ
)
```

### LLM Instruction Prompt
- Always prefer the instance method syntax `rdd1.spatialJoin(rdd2, predicate, algorithm)`.
- If you specify `ESJDistributedAlgorithm.DJ`, you MUST ensure both RDDs are spatially partitioned first using `spatialPartition`.
- If you specify `ESJDistributedAlgorithm.REPJ`, you MUST ensure at least one RDD is spatially partitioned.
- If you are unsure of the partitioning state, omit the `joinMethod` parameter to let Beast auto-select the algorithm (it will choose PBSM, DJ, REPJ, or BNLJ based on heuristics).
- Be aware that using `ESJDistributedAlgorithm.PBSM` triggers an immediate Spark reduce action to calculate MBRs, even if the join output is not immediately collected.

### Prompt Snippet
```text
To perform a spatial join in Beast, use `rdd1.spatialJoin(rdd2, predicate, algorithm)`. If using `ESJDistributedAlgorithm.DJ`, you MUST spatially partition both RDDs first (e.g., `rdd.spatialPartition(classOf[RSGrovePartitioner])`). Omit the algorithm parameter to let Beast auto-select the best strategy based on the partitioning state.
```

### Common Failure Modes
- **Missing Partitioning for DJ:** Calling `spatialJoin` with `ESJDistributedAlgorithm.DJ` on unpartitioned RDDs will fail. Both datasets must be partitioned first.
- **Missing Partitioning for REPJ:** Calling `spatialJoin` with `ESJDistributedAlgorithm.REPJ` when neither dataset is partitioned will fail.
- **Duplicate Results:** Using non-disjoint partitions with custom algorithms can yield duplicate pairs. Ensure you use disjoint partitioners like `GridPartitioner` or `RSGrovePartitioner`.
- **Unexpected Action Execution:** Using `PBSM` triggers an immediate reduce action to calculate MBRs, which might cause unexpected execution delays in what is normally a lazy transformation pipeline.

### Fix Code Hint
```scala
// BAD: Requesting Distributed Join (DJ) without partitioning the inputs
val results = rdd1.spatialJoin(rdd2, ESJPredicate.Intersects, ESJDistributedAlgorithm.DJ)

// GOOD: Partition both datasets first for DJ
val p1 = rdd1.spatialPartition(classOf[RSGrovePartitioner])
val p2 = rdd2.spatialPartition(classOf[RSGrovePartitioner])
val results = p1.spatialJoin(p2, ESJPredicate.Intersects, ESJDistributedAlgorithm.DJ)

// GOOD: Let Beast auto-select the algorithm if partitioning is unknown
val autoResults = rdd1.spatialJoin(rdd2, ESJPredicate.Intersects)
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
Runs a distributed spatial join between two vector datasets using the block-nested-loop join (BNLJ) algorithm to find all pairs of features that satisfy a specified spatial relationship.

### Parameters
- `r1` (`SpatialRDD`): The first set of spatial features (vector geometries) to join.
- `r2` (`SpatialRDD`): The second set of spatial features (vector geometries) to join.
- `joinPredicate` (`ESJPredicate`): The spatial relationship condition that must be met to join a feature from `r1` with a feature in `r2` (e.g., `ESJPredicate.MBRIntersects`, `ESJPredicate.Contains`).
- `numMBRTests` (`LongAccumulator`), default `null`: An optional Spark accumulator used to track and count the total number of Minimum Bounding Rectangle (MBR) intersection tests performed during the execution of the join.

### Input
Two `SpatialRDD`s containing vector data (e.g., loaded from Shapefiles, GeoJSON, CSV, or parallelized collections). Unlike the Distributed Join (`DJ`) or Repartition Join (`REPJ`) algorithms which require one or both datasets to be spatially partitioned first, the Block-Nested-Loop Join evaluates the Cartesian product of the partitions of `r1` and `r2`. 

### Output
Returns `RDD[(IFeature, IFeature)]` — A Spark RDD containing pairs (tuples) of matched vector features. The first element is from `r1` and the second is from `r2`.

### Valid Call Patterns
```scala
// Using the SpatialJoin object to perform a Block-Nested-Loop Join
val results: RDD[(IFeature, IFeature)] = SpatialJoin.spatialJoinBNLJ(
  r1, 
  r2, 
  joinPredicate = ESJPredicate.MBRIntersects
)
```

### LLM Instruction Prompt
- Call `spatialJoinBNLJ` as a method on the `SpatialJoin` object, passing both RDDs as arguments, rather than as an instance method on the RDD itself.
- Always provide an `ESJPredicate` (e.g., `ESJPredicate.MBRIntersects` or `ESJPredicate.Contains`) to define the join condition.
- Do not confuse this explicit algorithm call with the general `rdd.spatialJoin(...)` instance method. Use `SpatialJoin.spatialJoinBNLJ` when you specifically need the block-nested-loop join algorithm.

### Prompt Snippet
```text
To perform a block-nested-loop spatial join in Beast, use the object method `SpatialJoin.spatialJoinBNLJ(r1, r2, ESJPredicate.MBRIntersects)`. Do not call it as an instance method (`r1.spatialJoinBNLJ(r2)`). Ensure both inputs are SpatialRDDs.
```

### Common Failure Modes
- **Method Not Found:** Attempting to call `r1.spatialJoinBNLJ(r2)` as an instance method on the RDD. It must be called as `SpatialJoin.spatialJoinBNLJ(r1, r2, ...)`.
- **Performance Degradation / OOM:** Because BNLJ compares every partition of `r1` against every partition of `r2`, using it on massive datasets without prior filtering or when a partitioned join (like PBSM or DJ) would be more appropriate can lead to severe performance bottlenecks or Out Of Memory errors.
- **Missing Predicate:** Failing to specify the `joinPredicate`, which is a required parameter (unlike some general join wrappers that might default to intersects).

### Fix Code Hint
```scala
// WRONG: Called as an instance method
val joined = r1.spatialJoinBNLJ(r2, ESJPredicate.Contains)

// RIGHT: Called as an object method on SpatialJoin
val joined = SpatialJoin.spatialJoinBNLJ(r1, r2, ESJPredicate.Contains)
```

## API Test: `spatialJoinDJ`

### Signature
```scala
def spatialJoinDJ(r1: SpatialRDD, r2: SpatialRDD, joinPredicate: ESJPredicate, numMBRTests: LongAccumulator = null): RDD[(IFeature, IFeature)]
```
_Source: beast/beast-spark/src/main/scala/edu/ucr/cs/bdlab/beast/operations/SpatialJoin.scala:461_

_Source doc:_ Distributed join algorithm between spatially partitioned RDDs @param r1            the first set of features @param r2            the second set of features @param joinPredicate the predicate that joins a feature from r1 with a feature in r2 @param numMBRTests   a counter that will contain the number of MBR tests @return a pair RDD for joined features

### Goal
Executes the Distributed Join (DJ) algorithm to find overlapping or contained features between two massive vector datasets that have already been spatially partitioned.

### Parameters
- `r1` (`SpatialRDD`): The first set of vector features, which must be spatially partitioned.
- `r2` (`SpatialRDD`): The second set of vector features, which must also be spatially partitioned.
- `joinPredicate` (`ESJPredicate`): The spatial relationship condition that must be met to join a feature from `r1` with a feature in `r2` (e.g., `ESJPredicate.Contains`, `ESJPredicate.Intersects`).
- `numMBRTests` (`LongAccumulator`), default `null`: An optional Spark accumulator used to track and count the number of Minimum Bounding Rectangle (MBR) intersection tests performed during the join.

### Input
Two `SpatialRDD` vector datasets (e.g., loaded from Shapefiles, GeoJSON, or CSV). 
**Crucial Precondition:** The Distributed Join (`DJ`) algorithm strictly requires *both* datasets to be spatially partitioned prior to calling this method. To avoid duplicate results in the output, the partitions must be disjoint. Only `GridPartitioner`, `RSGrovePartitioner`, `KDTreePartitioner`, and `STRPartitioner` support disjoint partitioning.

### Output
Returns `RDD[(IFeature, IFeature)]` — A pair RDD containing tuples of matched features. The first element is a feature from `r1` and the second is the matching feature from `r2` that satisfies the `joinPredicate`.

### Valid Call Patterns
```scala
// Inferred from signature (not verified in tests)
import edu.ucr.cs.bdlab.beast.indexing.RSGrovePartitioner
import edu.ucr.cs.bdlab.beast.operations.SpatialJoin

// Both datasets MUST be spatially partitioned first
val partitionedR1 = r1.spatialPartition(classOf[RSGrovePartitioner])
val partitionedR2 = r2.spatialPartition(classOf[RSGrovePartitioner])

// Execute the Distributed Join (DJ)
val joinedFeatures = SpatialJoin.spatialJoinDJ(
  partitionedR1, 
  partitionedR2, 
  ESJPredicate.Contains
)
```

### LLM Instruction Prompt
- When calling `spatialJoinDJ`, you MUST ensure both input `SpatialRDD`s are spatially partitioned first. If only one is partitioned, use `REPJ` instead, or partition the other.
- To prevent duplicate join results, instruct the user to partition the data using a disjoint partitioner like `RSGrovePartitioner`.
- Do not invent a method on the RDD itself for this specific algorithm; call it statically via `SpatialJoin.spatialJoinDJ(r1, r2, predicate)` unless using the general `rdd.spatialJoin(...)` wrapper.

### Prompt Snippet
```text
The `spatialJoinDJ` method implements the Distributed Join algorithm and requires both input datasets to be spatially partitioned beforehand. Use `rdd.spatialPartition(classOf[RSGrovePartitioner])` on both inputs to ensure disjoint partitions, which prevents duplicate matches in the output RDD.
```

### Common Failure Modes
- **Unpartitioned Inputs:** Passing raw `SpatialRDD`s that have not been spatially partitioned. The DJ algorithm relies on partition metadata to prune the search space; missing this metadata will cause the join to fail or produce incorrect results.
- **Duplicate Results:** Using a non-disjoint partitioner (or failing to partition correctly) can cause features spanning multiple partitions to be evaluated and joined multiple times, leading to duplicate `(IFeature, IFeature)` pairs in the output.

### Fix Code Hint
```scala
// BAD: Calling spatialJoinDJ on raw RDDs
// val joined = SpatialJoin.spatialJoinDJ(rawPoints, rawPolygons, ESJPredicate.Intersects)

// GOOD: Partition both datasets with a disjoint partitioner first
val partitionedPoints = rawPoints.spatialPartition(classOf[RSGrovePartitioner])
val partitionedPolygons = rawPolygons.spatialPartition(classOf[RSGrovePartitioner])
val joined = SpatialJoin.spatialJoinDJ(partitionedPoints, partitionedPolygons, ESJPredicate.Intersects)
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
Performs a distributed Partition-Based Spatial-Merge (PBSM) join to find overlapping or contained features between two massive vector datasets.

### Parameters
- `r1` (`SpatialRDD`): The first spatial dataset to be joined.
- `r2` (`SpatialRDD`): The second spatial dataset to be joined.
- `joinPredicate` (`ESJPredicate`): The spatial relationship condition that must be met for a pair to be joined (e.g., `ESJPredicate.MBRIntersects`, `ESJPredicate.Contains`).
- `numMBRTests` (`LongAccumulator`), default `null`: An optional Spark accumulator used as an output variable to track the total number of Minimum Bounding Rectangle (MBR) intersection tests performed during the execution of the algorithm.
- `opts` (`BeastOptions`), default `new BeastOptions()`: Additional configuration options for tuning the PBSM algorithm.

### Input
- Two `SpatialRDD`s (typically loaded from vector formats like Shapefile, GeoJSON, or CSV via `sc.shapefile`, `sc.geojsonFile`, etc.).
- Unlike the Distributed Join (`DJ`) algorithm which requires both datasets to be spatially partitioned first, PBSM can operate on unpartitioned datasets by dynamically partitioning them using a grid.
- If the average number of points per geometry exceeds 100, Beast will automatically trigger a quad-split optimization to recursively split complex geometries before joining.

### Output
Returns `RDD[(IFeature, IFeature)]` — A Spark Pair RDD containing tuples of matched features from `r1` and `r2` that satisfy the specified `joinPredicate`.

### Valid Call Patterns
```scala
// Direct call via the SpatialJoin object
import edu.ucr.cs.bdlab.beast.operations.SpatialJoin
import edu.ucr.cs.bdlab.beast.cg.SpatialJoinAlgorithms.ESJPredicate

val result = SpatialJoin.spatialJoinPBSM(dataset1, dataset2, ESJPredicate.MBRIntersects)

// With disjoint datasets, it efficiently returns an empty RDD
val emptyResult = SpatialJoin.spatialJoinPBSM(disjointData1, disjointData2, ESJPredicate.Intersects)
```

### LLM Instruction Prompt
- Call `spatialJoinPBSM` as a static-like method on the `SpatialJoin` object (`SpatialJoin.spatialJoinPBSM(r1, r2, predicate)`), NOT as an instance method on the RDD.
- Always provide a valid `ESJPredicate` (e.g., `ESJPredicate.MBRIntersects`, `ESJPredicate.Contains`, `ESJPredicate.Intersects`).
- Do not invent spatial predicates; use only those defined in `ESJPredicate`.
- If you need to join datasets using the generic RDD method instead of calling the algorithm directly, use `r1.spatialJoin(r2, ESJPredicate.Contains, ESJDistributedAlgorithm.PBSM)`.

### Prompt Snippet
```text
To perform a Partition-Based Spatial-Merge join directly, use `SpatialJoin.spatialJoinPBSM(r1, r2, ESJPredicate.MBRIntersects)`. Do not call `r1.spatialJoinPBSM(r2)`. Ensure both inputs are `SpatialRDD`s. Beast will automatically apply quad-split optimization if geometries are highly complex (>100 points/geometry).
```

### Common Failure Modes
- **Method Not Found:** Attempting to call `r1.spatialJoinPBSM(r2)` directly on the RDD. The specific PBSM function is located on the `SpatialJoin` object.
- **Type Mismatch:** Passing standard Spark `RDD[Row]` or `DataFrame` instead of Beast's `SpatialRDD` (`RDD[IFeature]`).
- **Out of Memory (OOM) on Driver:** Attempting to `collect()` the result of a massive spatial join without filtering or aggregating first. Always apply transformations or save the distributed output.

### Fix Code Hint
```scala
// ❌ WRONG: Calling as an instance method on the RDD
val joined = points.spatialJoinPBSM(polygons, ESJPredicate.Contains)

// ✅ RIGHT: Calling via the SpatialJoin object
val joined = SpatialJoin.spatialJoinPBSM(points, polygons, ESJPredicate.Contains)

// ✅ RIGHT (Alternative): Using the generic spatialJoin instance method with the PBSM enum
val joined = points.spatialJoin(polygons, ESJPredicate.Contains, ESJDistributedAlgorithm.PBSM)
```

## API Test: `spatialJoinRepJ`

### Signature
```scala
def spatialJoinRepJ(r1: SpatialRDD, r2: SpatialRDD, joinPredicate: ESJPredicate, numMBRTests: LongAccumulator = null): RDD[(IFeature, IFeature)]
```
_Source: beast/beast-spark/src/main/scala/edu/ucr/cs/bdlab/beast/operations/SpatialJoin.scala:488_

_Source doc:_ Repartition join algorithm between two datasets: r1 is spatially disjoint partitioned and r2 is not @param r1 the first dataset @param r2 the second dataset @param joinPredicate the join predicate @param numMBRTests an optional accumulator that counts the number of MBR tests @return an RDD of pairs of matching features

### Goal
Executes a distributed Repartition Join (REPJ) between two vector datasets to find matching features, optimized for scenarios where exactly one dataset is already spatially partitioned with disjoint boundaries.

### Parameters
- `r1` (`SpatialRDD`): The first vector dataset, which **must** be spatially partitioned with disjoint partitions prior to calling this function.
- `r2` (`SpatialRDD`): The second vector dataset, which is typically unpartitioned.
- `joinPredicate` (`ESJPredicate`): The spatial condition to evaluate between features (e.g., `ESJPredicate.Intersects`, `ESJPredicate.Contains`).
- `numMBRTests` (`LongAccumulator`), default `null`: An optional Spark accumulator used to track and count the number of Minimum Bounding Rectangle (MBR) intersection tests performed during the join.

### Input
Two `SpatialRDD`s containing vector geometries (e.g., loaded from Shapefiles, GeoJSON, or CSV). 
**Preconditions:** 
1. `r1` MUST be spatially partitioned using a disjoint partitioner. To avoid duplicate results, only `GridPartitioner`, `RSGrovePartitioner`, `KDTreePartitioner`, and `STRPartitioner` support the required disjoint partitioning.
2. `r2` does not need to be partitioned. If both datasets are already partitioned, the Distributed Join (`DJ`) algorithm is more appropriate.

### Output
Returns `RDD[(IFeature, IFeature)]` — A distributed collection of paired features (one from `r1`, one from `r2`) that satisfy the specified `joinPredicate`.

### Valid Call Patterns
```scala
// Inferred from the signature (no verbatim example provided in documentation)
// Note: r1 must be partitioned first
val partitionedR1: SpatialRDD = r1.spatialPartition(classOf[RSGrovePartitioner])

val joinedFeatures: RDD[(IFeature, IFeature)] = spatialJoinRepJ(
  partitionedR1, 
  unpartitionedR2, 
  ESJPredicate.Intersects
)
```

### LLM Instruction Prompt
- Use `spatialJoinRepJ` when explicitly implementing the Repartition Join (REPJ) algorithm where one dataset is disjoint-partitioned and the other is not.
- Ensure `r1` is partitioned using a disjoint partitioner (e.g., `RSGrovePartitioner`) before calling.
- Do not use this function if both datasets are partitioned (use `DJ` instead) or if neither is partitioned (use `PBSM` or the standard `rdd.spatialJoin` which auto-selects the algorithm).
- Note that Beast automatically triggers a quad-split optimization during spatial joins if the average number of points per geometry exceeds 100.

### Prompt Snippet
```text
spatialJoinRepJ(partitionedR1, unpartitionedR2, ESJPredicate.Contains)
```

### Common Failure Modes
- **Duplicate Results / Incorrect Join:** Occurs if `r1` is not partitioned using a disjoint partitioner. The REPJ algorithm relies on the disjoint boundaries of `r1`'s partitions to route `r2`'s features without producing duplicates.
- **Performance Degradation or Crash:** Passing an unpartitioned RDD as `r1` will cause the algorithm to fail or perform poorly, as it assumes `r1`'s partitions define the spatial boundaries for broadcasting and shuffling `r2`.

### Fix Code Hint
```scala
// FIX: Ensure r1 is partitioned with a disjoint partitioner before calling spatialJoinRepJ
val disjointPartitionedR1 = r1.spatialPartition(classOf[RSGrovePartitioner])
val joined = spatialJoinRepJ(disjointPartitionedR1, r2, ESJPredicate.Intersects)
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
Distribute a set of spatial features across a Spark cluster using a specialized spatial partitioner (e.g., R*-Grove or GridPartitioner) to optimize load balancing, query pruning, and enable distributed spatial joins.

### Parameters
- `rdd` (`JavaSpatialRDD`): The input Java spatial RDD to be partitioned (applicable when using the Java API overloads).
- `spatialPartitioner` (`SpatialPartitioner`): An initialized spatial partitioner instance (e.g., `GridPartitioner`) or class type (e.g., `classOf[RSGrovePartitioner]`) that defines how geometries are distributed across partitions.

### Input
A `SpatialRDD` (or `JavaSpatialRDD`) containing vector features, typically loaded from formats like CSV, Shapefile, or GeoJSON. 
*   **Precondition for Initialized Partitioners:** If passing an instantiated partitioner like `GridPartitioner`, you must first compute the dataset's Minimum Bounding Rectangle (MBR) using `rdd.summary`.
*   **Precondition for Distributed Joins:** The Distributed Join (`DJ`) algorithm requires *both* input datasets to be spatially partitioned first. The Repartition Join (`REPJ`) requires at least *one* dataset to be spatially partitioned.

### Output
Returns `JavaPartitionedSpatialRDD` (or `SpatialRDD` in the Scala API) — the exact same set of input features, but physically reorganized across Spark partitions according to their spatial locations, with the spatial partitioner attached to the RDD metadata.

### Valid Call Patterns
```scala
// Pattern 1: Using an initialized partitioner (requires computing summary/MBR first)
val mbr = data.summary
val gridPartitioner = new GridPartitioner(mbr, Array(2, 2))
val partitionedData = data.spatialPartition(gridPartitioner)

// Pattern 2: Using a partitioner class (automatically initializes)
val partitionedFeatures: RDD[IFeature] = features.spatialPartition(classOf[RSGrovePartitioner])

// Pattern 3: Using IndexHelper for advanced configuration (e.g., enforcing disjoint partitions)
import edu.ucr.cs.bdlab.beast.indexing.IndexHelper.{Fixed, NumPartitions}
import edu.ucr.cs.bdlab.beast.indexing.{IndexHelper, RSGrovePartitioner}
val partitioner = IndexHelper.createPartitioner(features, classOf[RSGrovePartitioner],
  NumPartitions(Fixed, features.getNumPartitions), _ => 1, "disjoint" -> true)
val partitionedFeatures = features.spatialPartition(partitioner)
```

### LLM Instruction Prompt
- Always spatially partition datasets before performing a Distributed Join (`DJ`) or Repartition Join (`REPJ`).
- If duplicate avoidance is required for custom algorithms, ensure the partitioner supports disjoint partitioning. Only `GridPartitioner`, `RSGrovePartitioner`, `KDTreePartitioner`, and `STRPartitioner` support disjoint partitioning.
- When passing an instantiated `GridPartitioner`, you must compute the dataset's summary (`rdd.summary`) first to provide the bounding box. Alternatively, pass the class type (e.g., `classOf[RSGrovePartitioner]`) to let Beast handle initialization.

### Prompt Snippet
```text
To optimize spatial joins or range queries, partition the RDD using `spatialPartition`. For disjoint partitions (to avoid duplicate results), prefer `RSGrovePartitioner` or `GridPartitioner`. Remember that the `DJ` spatial join algorithm requires both datasets to be spatially partitioned beforehand.
```

### Common Failure Modes
- **Missing Pre-Partitioning for Joins:** Attempting to run a `DJ` (Distributed Join) without calling `spatialPartition` on both input RDDs first, which will cause the join to fail or fall back to a less efficient algorithm.
- **Uninitialized MBR:** Attempting to instantiate a `GridPartitioner` without first calling `rdd.summary` to get the dataset's spatial envelope.
- **Duplicate Results in Custom Algorithms:** Using a non-disjoint partitioner when disjoint partitions are strictly required, leading to features being duplicated across partition boundaries.

### Fix Code Hint
```scala
// FIX: Compute summary first if using an initialized GridPartitioner
val mbr = features.summary
val partitioner = new GridPartitioner(mbr, Array(10, 10))
val partitioned = features.spatialPartition(partitioner)

// FIX: Or use the class-based overload for automatic initialization
val partitionedAuto = features.spatialPartition(classOf[RSGrovePartitioner])
```

## API Test: `splitGeometryAcrossDateLine`
_Grounding: doc-repaired from source (docfix)._

### Goal
ADVANCED/LOW-LEVEL API: Splits a single-ring polygon geometry across the International Date Line (-180 or +180 meridian) to prevent spatial join or rendering errors. *Note: This is an internal/advanced geometric utility and should be excluded from the main user-facing benchmark denominator.*

### Input
ADVANCED/LOW-LEVEL: A caller-owned JTS `Geometry` object.
**Strict Preconditions:**
1. Must have its SRID explicitly set to 4326.
2. Must be a simple geometry (`getNumGeometries == 1`).
3. Must be a Polygon (`getGeometryType == "Polygon"`).
4. Must have exactly one ring / no holes (`getNumInteriorRing == 0`).

### Output
Returns `Geometry` — Either the exact original geometry if its bounding box width is <= 180, or a new `MultiPolygon` split into two pieces (Eastern and Western hemispheres) if the width is > 180.

### Valid Call Patterns
```scala
import org.locationtech.jts.geom.{Coordinate, GeometryFactory, PrecisionModel}
import edu.ucr.cs.bdlab.beast.cg.GeometryQuadSplitter

// Caller-owned low-level construction: GeometryFactory MUST be initialized with SRID 4326
val gf = new GeometryFactory(new PrecisionModel(), 4326)
val coords = Array(
  new Coordinate(170.0, -10.0),
  new Coordinate(170.0, 10.0),
  new Coordinate(-170.0, 10.0),
  new Coordinate(-170.0, -10.0),
  new Coordinate(170.0, -10.0)
)
val polygon = gf.createPolygon(coords)

// Split the geometry (mutates underlying Coordinate objects if width > 180)
val splitGeom = GeometryQuadSplitter.splitGeometryAcrossDateLine(polygon)
```

### LLM Instruction Prompt
- Use `GeometryQuadSplitter.splitGeometryAcrossDateLine(geometry)` for advanced/low-level dateline normalization.
- The input `Geometry` MUST be constructed with an explicit SRID of 4326 (e.g., `new GeometryFactory(new PrecisionModel(), 4326)`).
- The input must be a simple `Polygon` (`getNumGeometries == 1`) with exactly one ring/no holes (`getNumInteriorRing == 0`).
- Do not call concurrently on the same geometry instance; it mutates the underlying `Coordinate` objects.

### Prompt Snippet
```text
For advanced dateline splitting, use `edu.ucr.cs.bdlab.beast.cg.GeometryQuadSplitter.splitGeometryAcrossDateLine(geom)`. The input must be a single-ring Polygon with its SRID explicitly set to 4326.
```

### Common Failure Modes
- **Missing SRID 4326 (The failure that just happened):** `java.lang.IllegalArgumentException: requirement failed: Can only work with geometries in the EPSG:4326 format`. Caused by constructing the input with a default `GeometryFactory` (which assigns SRID 0).
- **ADVANCED/LOW-LEVEL API:** This is an internal utility requiring explicit low-level JTS construction. It should be excluded from the main user-facing denominator.
- **Invalid Geometry Type:** Passing a `MultiPolygon` (`getNumGeometries != 1`), a non-Polygon, or a Polygon with holes (`getNumInteriorRing != 0`) triggers `require` failures.

### Fix Code Hint
```scala
// WRONG: Default GeometryFactory assigns SRID 0, causing IllegalArgumentException
val badGf = new org.locationtech.jts.geom.GeometryFactory()
val badPoly = badGf.createPolygon(coords)
edu.ucr.cs.bdlab.beast.cg.GeometryQuadSplitter.splitGeometryAcrossDateLine(badPoly)

// CORRECT: Explicitly set SRID to 4326
val gf = new org.locationtech.jts.geom.GeometryFactory(new org.locationtech.jts.geom.PrecisionModel(), 4326)
val polygon = gf.createPolygon(coords)
val splitGeom = edu.ucr.cs.bdlab.beast.cg.GeometryQuadSplitter.splitGeometryAcrossDateLine(polygon)
```

## API Test: `sridToCRS`

### Signature
```scala
def sridToCRS(srid: Int): CoordinateReferenceSystem
```
_Source: beast/cg/src/main/scala/org/apache/spark/beast/CRSServer.scala:352_

_Source doc:_ Convert the given SRID to CRS according to the following logic. 1. If the SRID is zero, it indicates an invalid SRID and `null` is returned. 2. It searches the local cache and retrieves the SRID. 3a. If SRID is positive, use it as an EPSG, retrieve the CRS, cache and return it. 3b. If SRID is negative, contact the server, retrieve the CRS, cache and return it. @param srid the SRID that needs to be converted to a CRS @return the converted CRS.

### Goal
Convert an integer Spatial Reference System Identifier (SRID) into a `CoordinateReferenceSystem` object, resolving standard EPSG codes locally and custom projections via the Beast `CRSServer`.

### Parameters
- `srid` (`Int`): The integer identifier for the CRS. Positive values are treated as standard EPSG codes, negative values indicate custom CRSs managed by the Beast server, and 0 indicates an invalid SRID.

### Input
An integer SRID. If the SRID is negative (indicating a custom, non-standard CRS), the Beast `CRSServer` must be actively running on the Spark cluster (via `CRSServer.startServer(sc)`) so the method can contact the server to retrieve the CRS definition.

### Output
Returns `CoordinateReferenceSystem` — A GeoTools/OpenGIS CRS object representing the spatial reference system. Returns `null` if the input SRID is `0`.

### Valid Call Patterns
```scala
// Standard EPSG resolution (e.g., WGS84)
val wgs84Crs = CRSServer.sridToCRS(4326)

// Custom CRS resolution (requires CRSServer to be running)
CRSServer.startServer(sc)
try {
  val customCrs = CRSServer.sridToCRS(sridSinusoidal) // where sridSinusoidal < 0
} finally {
  CRSServer.stopServer(true)
}
```

### LLM Instruction Prompt
- When needing to instantiate a `CoordinateReferenceSystem` from an integer SRID in Beast, use `CRSServer.sridToCRS(srid)`. 
- Remember the resolution logic: positive integers are treated as standard EPSG codes, negative integers are fetched from the Beast `CRSServer` (which must be running), and `0` returns `null`. Always handle the potential `null` return value if the SRID source is untrusted.

### Prompt Snippet
```text
Use CRSServer.sridToCRS(srid) to convert an integer SRID to a CoordinateReferenceSystem. Positive values are EPSG codes; negative values require a running CRSServer. Handle nulls if srid might be 0.
```

### Common Failure Modes
- **NullPointerException Downstream:** Passing `0` as the SRID explicitly returns `null`. If the caller immediately invokes methods on the returned CRS without a null check, it will crash.
- **Server Unreachable / Connection Refused:** Passing a negative SRID when `CRSServer.startServer(sc)` has not been called, or if the server has been stopped. The method will fail to contact the server to retrieve the custom CRS.
- **Unknown EPSG Code:** Passing a positive SRID that does not exist in the standard EPSG registry will fail during the local EPSG lookup phase.

### Fix Code Hint
```scala
// Ensure CRSServer is running if dealing with potentially custom (negative) SRIDs
CRSServer.startServer(sc)
try {
  val crs = CRSServer.sridToCRS(srid)
  if (crs != null) {
    // Proceed with valid CoordinateReferenceSystem
    println(crs.getName.toString)
  } else {
    // Handle invalid SRID (0)
    println("Invalid SRID provided.")
  }
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
Starts the Coordinate Reference System (CRS) HTTP server to manage and distribute non-standard CRS definitions across worker nodes in a Spark cluster.

### Parameters
- `defaultPort` (`Int`), default `DefaultPort`: The preferred network port number to bind the server to.
- `sc` (`SparkContext`) / `jsc` (`JavaSparkContext`): The active Spark context to attach the server to (used in the overloads).

### Input
- Requires an initialized `SparkContext` or `JavaSparkContext` when using the context-based overloads.
- The environment must allow binding to the specified network port (or an available fallback port).

### Output
Returns `Int` — The actual network port number on which the server is listening. (Note: The `SparkContext` and `JavaSparkContext` overloads return a `Boolean` indicating whether the server started successfully).

### Valid Call Patterns
```scala
// Start the server using an active SparkContext
CRSServer.startServer(sparkContext)
try {
  // Perform operations requiring custom/non-standard CRS definitions
  val port = sparkContext.getLocalProperty(CRSServer.CRSServerPort)
  // ...
} finally {
  // Always ensure the server is stopped to prevent resource leaks
  CRSServer.stopServer(true)
}
```

### LLM Instruction Prompt
- When generating code that registers or uses non-standard Coordinate Reference Systems (CRS) in Beast, you MUST start the `CRSServer` using `CRSServer.startServer(sc)`.
- Always wrap the subsequent spatial operations in a `try-finally` block and call `CRSServer.stopServer(true)` in the `finally` block to prevent resource leaks.
- Do not call `startServer` as a bare method; it must be qualified with the `CRSServer` object.

### Prompt Snippet
```text
To distribute non-standard CRS definitions across a Beast Spark cluster, call `CRSServer.startServer(sc)`. You MUST wrap subsequent operations in a `try-finally` block and invoke `CRSServer.stopServer(true)` in the `finally` clause to release the port.
```

### Common Failure Modes
- **Resource Leaks:** Failing to call `CRSServer.stopServer(true)` after the spatial operations complete, leaving the HTTP server running and the port bound.
- **Uninitialized Context:** Passing a null or stopped `SparkContext` to the overload, causing the server startup to fail or properties to not be set.
- **Missing Qualifier:** Attempting to call `startServer(sc)` without the `CRSServer` object qualifier, resulting in a compilation error.

### Fix Code Hint
```scala
// WRONG: No try-finally block, risking a leaked server process
CRSServer.startServer(sc)
val myCrs = CRS.decode("EPSG:3857")
// ... operations ...

// RIGHT: Safely start and stop the server
CRSServer.startServer(sc)
try {
  val myCrs = CRS.decode("EPSG:3857")
  // ... operations ...
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
Computes the total sum of the bounding box side lengths along each spatial dimension for a collection of geometries, enabling the calculation of average spatial extents.

### Parameters
_None._

### Input
A spatial summary or partition object (e.g., `Summary` or `SpatialPartition`) that contains aggregated geometric statistics from a vector dataset. This is typically obtained via `GeometricSummary.run(...)` or by calling `.summary` on a spatial RDD.

### Output
Returns `Array[Double]` — an array where each element represents the total sum of side lengths for a specific spatial dimension (e.g., index `0` for the X/longitude dimension, index `1` for the Y/latitude dimension).

### Valid Call Patterns
```scala
// Inferred from sibling API `numFeatures` on Summary/SpatialPartition
val inputfile = locateResource("/test.partitions")
val opts = new BeastOptions().set("iformat", "wkt(Geometry)")
  .set("skipheader", true)
  .set("separator", "\t")

val summary = GeometricSummary.run(opts, Array(inputfile.getPath), null, sparkContext).asInstanceOf[Summary]

// Retrieve the sum of side lengths per dimension
val sideLengths: Array[Double] = summary.sumSideLength

// Compute average side length per dimension (as recommended by source docs)
val avgSideLengthX = sideLengths(0) / summary.numNonEmptyGeometries
val avgSideLengthY = sideLengths(1) / summary.numNonEmptyGeometries
```

### LLM Instruction Prompt
- When calculating average geometry extents or side lengths per dimension in Beast, call `.sumSideLength` on a spatial summary object. 
- It takes no arguments and returns an `Array[Double]`, not a single scalar value. 
- To find the average side length per dimension, divide the respective array elements by `numNonEmptyGeometries`.

### Prompt Snippet
```text
def sumSideLength: Array[Double] // Call on a spatial summary/partition object. Returns sum of side lengths per dimension (index 0=X, 1=Y). Divide by numNonEmptyGeometries for averages.
```

### Common Failure Modes
- **Type Mismatch on Return:** Assuming the method returns a single `Double` representing total area or perimeter, rather than an `Array[Double]` representing lengths per dimension.
- **Passing Arguments:** Attempting to pass a dimension index directly to the method (e.g., `summary.sumSideLength(0)`). The method takes no arguments; you must index the returned array.

### Fix Code Hint
```scala
// WRONG: Attempting to get a single scalar or passing an argument
// val totalLength: Double = summary.sumSideLength
// val xLength = summary.sumSideLength(0) // Fails if interpreted as method argument

// RIGHT: Assign to an array first, or index the result of the parameterless call
val lengths: Array[Double] = summary.sumSideLength
val avgX = lengths(0) / summary.numNonEmptyGeometries
val avgY = lengths(1) / summary.numNonEmptyGeometries
```

## API Test: `summary`

### Signature
```scala
def summary: Summary
def summary(rdd: JavaSpatialRDD): Summary
```
_Source: beast/beast-spark/src/main/scala/edu/ucr/cs/bdlab/beast/JavaSpatialRDDHelper.scala:171  (+2 more definition site/overload)_

_Source doc:_ Compute the geometric summary of a set of features which includes size (in bytes), number of records, number of points, number of non empty geometries, average side length (width and height), and the geometry type. @return the computed summaries

### Goal
Compute the geometric summary and Minimum Bounding Rectangle (MBR) of a distributed vector dataset, providing essential statistics like feature count, size, and geometry type for approximate query processing or spatial partitioning.

### Parameters
- `rdd` (`JavaSpatialRDD`): The spatial RDD to compute the summary for. *Note: This parameter is only required when using the Java API (`JavaSpatialRDDHelper.summary(rdd)`). In Scala, `summary` is called as a parameterless extension method directly on the RDD (`rdd.summary`).*

### Input
A loaded vector `SpatialRDD` or `JavaSpatialRDD` containing spatial features (e.g., points, lines, or polygons loaded from CSV, Shapefile, or GeoJSON). The dataset does not need to be spatially partitioned prior to calling this method. This operation is specific to vector data and is not used for `RasterRDD` objects.

### Output
Returns `Summary` — an object representing the computed geometric summaries of the dataset. This includes the dataset's spatial envelope (MBR), size (in bytes), number of records, number of points, number of non-empty geometries, average side length (width and height), and the geometry type. The `Summary` object can be used directly as an `EnvelopeND` or bounding box when initializing spatial partitioners.

### Valid Call Patterns
```scala
// Scala: Parameterless extension method on a SpatialRDD
val data: SpatialRDD = sparkContext.readCSVPoint("points.csv")
val mbr = data.summary

// Using the summary to initialize a spatial partitioner
val gridPartitioner = new GridPartitioner(mbr, Array(2, 2))
val partitionedData = data.spatialPartition(gridPartitioner)

// Java: Using the helper class
// Summary summary = JavaSpatialRDDHelper.summary(rdd);
```

### LLM Instruction Prompt
- Use `rdd.summary` (Scala) or `JavaSpatialRDDHelper.summary(rdd)` (Java) to compute the bounding box and statistics of a vector dataset.
- Do not pass arguments to `summary` in Scala; it is a parameterless extension method on `SpatialRDD`.
- Use the returned `Summary` object when a spatial partitioner (like `GridPartitioner`) requires the dataset's Minimum Bounding Rectangle (MBR) for initialization.
- Do not attempt to call `summary` on a `RasterRDD`; it is a vector RDD operation.

### Prompt Snippet
```text
RDPro/Beast `summary`: Computes geometric stats (MBR, feature count, size) for a vector SpatialRDD. Call as `val mbr = rdd.summary` in Scala (no args). The returned `Summary` object acts as the dataset's bounding box and is typically passed to spatial partitioners like `new GridPartitioner(mbr, Array(2, 2))`.
```

### Common Failure Modes
- **Passing arguments in Scala:** Attempting to call `rdd.summary(something)` in Scala will fail to compile. The Scala signature is `def summary: Summary`.
- **Calling on Raster Data:** Attempting to call `summary` on a `RasterRDD` (e.g., loaded via `sc.geoTiff`). This is a vector-specific operation.
- **Type Mismatch for Partitioners:** Forgetting to compute the summary before initializing partitioners that require an MBR (like `GridPartitioner`), or trying to pass the raw RDD instead of the `Summary` object.

### Fix Code Hint
```scala
// WRONG: Passing arguments to summary in Scala
// val stats = data.summary(data)

// WRONG: Initializing a partitioner without the summary MBR
// val partitioner = new GridPartitioner(data, Array(2, 2))

// CORRECT: Call parameterless summary to get the MBR, then partition
val mbr = data.summary
val gridPartitioner = new GridPartitioner(mbr, Array(2, 2))
val partitionedData = data.spatialPartition(gridPartitioner)
```

## API Test: `tileIDs`
_Grounding: doc-repaired from source (docfix)._

### Goal
ADVANCED/LOW-LEVEL API. Provides a sequential iterator over all valid integer tile identifiers for a specific raster dataset. This is internal framework plumbing meant for custom readers/writers or explicit partition-level tile extraction, not standard user workflows. Note: Exclude this API from main user-facing benchmark denominators.

### Input
A `RasterMetadata` instance. As an INTERNAL/FRAMEWORK API, standard users do not call this. For testing or low-level operations, construct the receiver directly using the factory method `RasterMetadata.create(...)`.

### Output
Returns `Iterator[Int]` — A lazy iterator yielding the integer ID for every tile present in the raster dataset (from `0` to `numTiles - 1`).

### Valid Call Patterns
```scala
import edu.ucr.cs.bdlab.beast.geolite.RasterMetadata

// Caller-owned low-level construction for testing
val metadata = RasterMetadata.create(
  0.0, 0.0, 100.0, 100.0, // Model space corners (x1, y1, x2, y2)
  4326,                   // SRID
  1000, 1000,             // Total raster width and height in pixels
  256, 256                // Tile width and height in pixels
)

val ids = metadata.tileIDs.toList

assert(ids.nonEmpty, "Tile IDs iterator should not be empty for a valid raster")
assert(ids.distinct.size == ids.size, "Tile IDs should be unique")
println(s"__CHECK__ tileIDs ${ids.size}")
```

### LLM Instruction Prompt
`tileIDs` is an instance method on `RasterMetadata`. Do not use `GeoTiffReader` from `edu.ucr.cs.bdlab.beast.io` in examples, as it will cause a compilation error due to incorrect package resolution. To construct a `RasterMetadata` instance for testing or low-level operations, use the factory method `RasterMetadata.create(minX, minY, maxX, maxY, srid, width, height, tileWidth, tileHeight)`.

### Prompt Snippet
Use `metadata.tileIDs` on a `RasterMetadata` instance to get an `Iterator[Int]` of all tile IDs. For standalone testing, instantiate metadata via `edu.ucr.cs.bdlab.beast.geolite.RasterMetadata.create(...)`.

### Common Failure Modes
- **Package Resolution Error (GeoTiffReader):** Attempting to import and use `edu.ucr.cs.bdlab.beast.io.GeoTiffReader` to get metadata. This fails compilation because the class is either in a deeper subpackage or not publicly exposed. Use `RasterMetadata.create(...)` instead.
- **Calling on RDD:** Attempting to call `tileIDs` directly on a `RasterRDD`. This is an ADVANCED/LOW-LEVEL API that only exists on `RasterMetadata`.
- **Exclusion:** Including this in standard user-facing workflows. It should be excluded from main user-facing benchmark denominators.

### Fix Code Hint
```scala
// WRONG: Fails compilation due to incorrect package resolution
import edu.ucr.cs.bdlab.beast.io.GeoTiffReader
val reader = new GeoTiffReader()
val ids = reader.metadata.tileIDs

// CORRECT: Use explicit low-level construction for testing
import edu.ucr.cs.bdlab.beast.geolite.RasterMetadata
val metadata = RasterMetadata.create(0.0, 0.0, 100.0, 100.0, 4326, 1000, 1000, 256, 256)
val ids = metadata.tileIDs.toList
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
Generate a random numeric value within a specified range, or (via its overloads) generate a distributed `SpatialRDD` of synthetic spatial geometries (points, boxes, or polygons) uniformly distributed across a spatial extent for benchmarking and testing.

### Parameters
- `a` (`Double`): The inclusive lower bound of the uniform distribution range (for the scalar mathematical function).
- `b` (`Double`): The exclusive upper bound of the uniform distribution range (for the scalar mathematical function).

### Input
- **For the scalar function (`uniform(a, b)`):** Requires two `Double` values where `a < b`.
- **For the RDD generator (`uniform(cardinality)`):** Requires an initialized `SparkContext` (`sc`). The caller must provide a `cardinality` (`Long`) representing the total number of spatial features to generate. It is typically called on `sc.generateSpatialData` or a `SpatialGeneratorBuilder`.
- **Preconditions (RDD Generator):** If generating complex geometries (boxes or polygons), the builder should be configured first using `.config()` with keys like `UniformDistribution.GeometryType` (e.g., `"box"`, `"polygon"`), `UniformDistribution.MaxSize` (e.g., `"0.2,0.1"`), and optionally bounded by an MBR using `.mbr(envelope)`.

### Output
Returns `Double` — A randomly generated numeric value in the range `[a, b)`. 
*(Note: The overloads return a `SpatialRDD` or `JavaSpatialRDD` representing a distributed Spark dataset of generated spatial features (`IFeature`) uniformly distributed across the configured space).*

### Valid Call Patterns
```scala
import edu.ucr.cs.bdlab.beast._
import edu.ucr.cs.bdlab.beast.generator._
import edu.ucr.cs.bdlab.beast.geolite.EnvelopeNDLite

// 1. Generate a massive SpatialRDD of uniform random points using the context extension
val randomPoints: SpatialRDD = sc.generateSpatialData.uniform(1000000000L)

// 2. Generate a configured SpatialRDD of uniform random polygons within a specific MBR
val desiredMBR = new EnvelopeNDLite(2.0, 2.0, 3.0, 9.0, 8.0)
val randomPolygons: SpatialRDD = new SpatialGeneratorBuilder(sc)
  .mbr(desiredMBR)
  .config(UniformDistribution.GeometryType, "polygon")
  .config(UniformDistribution.MaxSize, "0.2,0.1")
  .config(UniformDistribution.NumSegments, 10)
  .config(SpatialGenerator.Seed, 1794)
  .uniform(100L)
```

### LLM Instruction Prompt
- When generating synthetic spatial data for benchmarking in Beast, use the `uniform(cardinality: Long)` overload via `sc.generateSpatialData.uniform(...)` or `new SpatialGeneratorBuilder(sc).uniform(...)`.
- Always configure the generator *before* calling `.uniform(cardinality)` if you need non-point geometries. Use `.config(UniformDistribution.GeometryType, "box")` or `"polygon"`.
- When configuring `UniformDistribution.MaxSize`, provide the dimensions as a comma-separated string (e.g., `"0.01,0.01"`).
- Do not confuse the scalar math utility `uniform(a: Double, b: Double)` with the RDD generator `uniform(cardinality: Long)`.

### Prompt Snippet
```text
Generate a SpatialRDD of 10 million random boxes uniformly distributed across the default space.
```

### Common Failure Modes
- **Missing Configuration Imports:** Failing to import `edu.ucr.cs.bdlab.beast.generator._` will cause compilation errors when trying to access configuration constants like `UniformDistribution.GeometryType`.
- **Malformed Configuration Values:** Passing invalid string formats to `.config()` (e.g., passing a single number to `MaxSize` instead of a comma-separated string like `"width,height"`) will cause runtime parsing errors during generation.
- **Type Mismatch on Cardinality:** Passing an `Int` instead of a `Long` for massive datasets (e.g., `10000000000` without the `L` suffix) will cause standard Scala integer overflow or compilation errors.

### Fix Code Hint
```scala
// BAD: Missing configuration for boxes, and missing 'L' on large cardinality
val badBoxes = sc.generateSpatialData.uniform(10000000000)

// GOOD: Properly configured builder with Long cardinality
import edu.ucr.cs.bdlab.beast.generator._
val goodBoxes = sc.generateSpatialData
  .config(UniformDistribution.GeometryType, "box")
  .config(UniformDistribution.MaxSize, "0.01,0.01")
  .uniform(10000000000L)
```

## API Test: `uniformHistogramCount`

### Signature
```scala
def uniformHistogramCount(histogramSize: Array[Int], prefixSum: Boolean = false): AbstractHistogram
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/CGOperationsMixin.scala:67_

_Source doc:_ Computes a uniform histogram with the given size that counts number of features in each cell @param histogramSize the size of the histogram as the number of partitions along each dimension @param prefixSum     compute the prefix sum on the result to speed up range tests @return the created histogram

### Goal
Computes a uniform spatial histogram over a vector dataset, counting the number of features that fall into each grid cell of a specified multi-dimensional grid.

### Parameters
- `histogramSize` (`Array[Int]`): The dimensions of the grid (e.g., `Array(100, 100)` for a 100x100 2D grid) representing the number of partitions/cells along each spatial axis.
- `prefixSum` (`Boolean`), default `false`: If `true`, computes the prefix sum (cumulative sum) over the grid cells, which allows for constant-time range queries (e.g., `histogram.getValue(min, max)`).

### Input
A spatial RDD of vector features (e.g., `RDD[IFeature]` or `SpatialRDD`) loaded via Beast context extensions like `sc.shapefile`, `sc.geojsonFile`, or `sc.readCSVPoint`. The data must have valid spatial geometries.

### Output
Returns `AbstractHistogram` — an object representing the spatial distribution of feature counts across the uniform grid. If `prefixSum` is true, it can be queried in constant time for range estimates.

### Valid Call Patterns
```scala
// Basic uniform histogram count
val countHistogram = features.uniformHistogramCount(Array(100, 100))

// Uniform histogram with prefix sum enabled for fast range queries
val histogram = polygons.uniformHistogramCount(Array(100, 100), prefixSum = true)
// The following function will run in constant time regardless of the size of the range
val rangeCount = histogram.getValue(Array(4, 3), Array(10, 10))
```

### LLM Instruction Prompt
- Call `uniformHistogramCount` directly on a spatial RDD (`RDD[IFeature]`).
- Provide the grid dimensions as an `Array[Int]` matching the spatial dimensions of the data (typically 2D, e.g., `Array(100, 100)`).
- Set `prefixSum = true` if the resulting histogram will be used for fast range tests or approximate query processing.
- Note that this is a simple histogram. It counts the number of features in each cell but does not account for features spanning multiple grid cells (which may lead to double-counting). If accurate accounting of overlapping features is required, use `eulerHistogramSize` instead.

### Prompt Snippet
```text
To compute a spatial distribution of vector features, use `rdd.uniformHistogramCount(Array(numX, numY))`. Set `prefixSum = true` if you need to perform constant-time range queries on the resulting `AbstractHistogram`. Remember that simple histograms may double-count features spanning multiple cells.
```

### Common Failure Modes
- **Dimension Mismatch:** Providing a 1D or 3D `histogramSize` array for 2D spatial data. The length of `histogramSize` must match the coordinate dimensions of the geometries.
- **Double Counting Large Features:** Assuming the sum of all cells equals the exact total feature count. Features that intersect multiple grid cells will be counted in each intersecting cell. (Use Euler histograms if exact topological accounting is needed).
- **Missing Spatial Context:** Attempting to call this on a standard Spark `RDD[String]` or `DataFrame` before parsing it into an `RDD[IFeature]` using Beast's spatial readers.

### Fix Code Hint
```scala
// Incorrect: Calling on raw text or missing prefixSum for range queries
// val lines = sc.textFile("data.csv")
// val hist = lines.uniformHistogramCount(Array(100, 100))

// Correct: Load as SpatialRDD first, then compute histogram
val points: RDD[IFeature] = sc.readCSVPoint("data.csv", "x", "y")
val hist = points.uniformHistogramCount(Array(100, 100), prefixSum = true)
val countInRange = hist.getValue(Array(0, 0), Array(50, 50))
```

## API Test: `uniformHistogramSize`

### Signature
```scala
def uniformHistogramSize(histogramSize: Array[Int], prefixSum: Boolean = false, sizeFunction: IFeature => Int = _.getStorageSize): AbstractHistogram
```
_Source: beast/cg/src/main/scala/edu/ucr/cs/bdlab/beast/cg/CGOperationsMixin.scala:78_

_Source doc:_ Computes a uniform histogram with the given size that calculates the size of the data in each cell @param histogramSize the size of the histogram as the number of partitions along each dimension @param prefixSum     compute the prefix sum on the result to speed up range tests @param sizeFunction  an optional function that computes the size of a feature. @return the created histogram

### Goal
Computes a uniform spatial histogram over a vector dataset where each grid cell records the total storage size (in bytes) of the features it intersects, which is useful for load balancing and approximate query processing.

### Parameters
- `histogramSize` (`Array[Int]`): The dimensions of the histogram grid, specified as the number of partitions/bins along each spatial axis (e.g., `Array(100, 100)` for a 100x100 2D grid).
- `prefixSum` (`Boolean`), default `false`: A flag indicating whether to compute a prefix sum over the histogram cells, which optimizes subsequent range tests.
- `sizeFunction` (`IFeature => Int`), default `_.getStorageSize`: A custom function to calculate the size of an individual `IFeature`. Defaults to the in-memory storage size, but can be overridden to estimate serialized size (e.g., using `FeatureWriterSizeFunction`).

### Input
A Spatial RDD of vector features (`RDD[IFeature]`), typically loaded via `sc.shapefile`, `sc.geojsonFile`, or similar context extensions. This operation is specific to vector data and cannot be called directly on a Raster RDD.

### Output
Returns `AbstractHistogram` — a spatial grid representation where each cell contains the aggregated size (based on `sizeFunction`) of all features falling within its spatial bounds.

### Valid Call Patterns
```scala
// Standard usage with default in-memory storage size
val sizeHistogram = features.uniformHistogramSize(Array(100, 100))

// Custom usage estimating the size if features were written as GeoJSON
val sizeGeoJsonHistogram = features.uniformHistogramSize(Array(100, 100),
    sizeFunction = new FeatureWriterSizeFunction("iformat" -> "geojson"))
```

### LLM Instruction Prompt
- Call `uniformHistogramSize` as an extension method on a Spatial RDD (`RDD[IFeature]`).
- Provide the grid dimensions as an `Array[Int]` matching the dimensionality of the data (typically 2D, e.g., `Array(100, 100)`).
- Use this method when you need to estimate data volume or storage size per spatial region (e.g., for spatial partitioning). If you only need the number of features per cell, use `uniformHistogramCount` instead.
- To estimate the size of features for a specific output format rather than in-memory size, override `sizeFunction` with `new FeatureWriterSizeFunction("iformat" -> "<format>")`.

### Prompt Snippet
```text
Use rdd.uniformHistogramSize(Array(x, y)) to compute a spatial grid of feature storage sizes for load balancing or partitioning.
```

### Common Failure Modes
- **Calling on Raster Data:** Attempting to call this on a `RasterRDD` or `RDD[ITile]`. This method is part of `CGOperationsMixin` and requires an `RDD[IFeature]`.
- **Dimensionality Mismatch:** Providing a 1D array for `histogramSize` when the underlying geometries are 2D. The array length must match the spatial dimensions.
- **Missing Imports:** Failing to import Beast implicits, which are required to expose `uniformHistogramSize` on a standard Spark `RDD`.

### Fix Code Hint
```scala
// Ensure the receiver is a vector RDD (RDD[IFeature]) and the array matches 2D space
import edu.ucr.cs.bdlab.beast._
val features: RDD[IFeature] = sc.shapefile("data.zip")
val sizeHistogram = features.uniformHistogramSize(Array(256, 256))
```

## API Test: `using`
_Grounding: doc-repaired from source (docfix)._

### Goal
INTERNAL/FRAMEWORK API. A generic Scala loan-pattern utility defined on the `DatasetProcessor` object to safely manage `AutoCloseable` lifecycles. *Note: Exclude this API from scored user-facing benchmark denominators, as it is a generic resource management utility, not a geospatial or Spark-specific operation.*

### Input
INTERNAL/FRAMEWORK API. Accepts an initialized `java.lang.AutoCloseable` resource (e.g., `java.io.ByteArrayOutputStream`) and a closure block `A => B`.

### Output
Returns the exact value returned by the execution of the closure block (type `B`), guaranteeing the resource is closed afterward.

### Valid Call Patterns
```scala
import edu.ucr.cs.bdlab.beast.dataExplorer.DatasetProcessor
import java.io.ByteArrayOutputStream

// Use an in-memory AutoCloseable to avoid filesystem dependencies
val result = DatasetProcessor.using(new ByteArrayOutputStream()) { out =>
  out.write("beast".getBytes("UTF-8"))
  out.size()
}
assert(result == 5)
```

### LLM Instruction Prompt
When testing or using the internal `DatasetProcessor.using` loan-pattern utility, prefer an in-memory `AutoCloseable` like `java.io.ByteArrayOutputStream` to avoid environmental file system failures. Call it explicitly via the `DatasetProcessor` object.

### Prompt Snippet
```scala
DatasetProcessor.using(new java.io.ByteArrayOutputStream()) { out => 
  out.write("data".getBytes)
  out.size() 
}
```

### Common Failure Modes
- **INTERNAL/FRAMEWORK Misclassification:** Attempting to use this as a geospatial operation. It is a generic Scala utility and should be excluded from user-facing benchmark denominators.
- **Environmental File System Failures (`FileNotFoundException`):** Passing a `new FileOutputStream(outFile)` fails before `using` is even invoked if the test harness `output_dir` is a URI string (e.g., `file:/...`) or if the directory was not pre-created. Always use an in-memory `AutoCloseable` (like `ByteArrayOutputStream`) for safe, deterministic testing.

### Fix Code Hint
```scala
// BAD: Fails with FileNotFoundException if output_dir is a URI or not pre-created
edu.ucr.cs.bdlab.beast.dataExplorer.DatasetProcessor.using(new java.io.FileOutputStream(s"$output_dir/test.txt")) { out =>
  out.write(1)
}

// GOOD: Uses in-memory AutoCloseable to avoid environmental dependencies
edu.ucr.cs.bdlab.beast.dataExplorer.DatasetProcessor.using(new java.io.ByteArrayOutputStream()) { out =>
  out.write(1)
}
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
Write a distributed `SpatialRDD` to disk as a spatial file in a specified format (e.g., CSV, GeoJSON, Shapefile) with optional configuration parameters.

### Parameters
- `rdd` (`JavaSpatialRDD`): The spatial RDD to write. This parameter is explicitly required when using the Java API (`JavaSpatialRDDHelper.writeSpatialFile`); in Scala, the function is called as an extension method directly on the `SpatialRDD` instance.
- `filename` (`String`): The destination file path or directory name where the output will be saved.
- `oformat` (`String`): The short name of the output file format (e.g., `"envelope"`, `"csv"`, `"shapefile"`, `"geojson"`, `"kml"`, `"kmz"`).
- `opts` (`BeastOptions`): Additional user options to configure the writer (e.g., specifying an output separator for CSVs). Defaults to an empty `BeastOptions`.

### Input
A `SpatialRDD` (or `JavaSpatialRDD`) containing vector features or geometric envelopes. The RDD can be spatially partitioned (e.g., via `spatialPartition`) or unpartitioned. The caller must provide a valid output format string supported by Beast for vector data. 

### Output
Returns `Unit` — the operation triggers a Spark job that writes the distributed RDD partitions to the specified `filename` on the file system in the requested `oformat`.

### Valid Call Patterns
```scala
// Scala: Writing an RDD of envelopes to disk without extra options
sparkContext.parallelize(r1)
  .asInstanceOf[SpatialRDD]
  .spatialPartition(grid)
  .writeSpatialFile(index1Path, "envelope")

// Scala: Writing with additional BeastOptions (passed as implicit tuples)
records.writeSpatialFile("output.csv", "envelope", "oseparator" -> ",")

// Java: Using the helper class
JavaSpatialRDDHelper.writeSpatialFile(records, "output.csv", "envelope", new BeastOptions("oseparator:,"));
```

### LLM Instruction Prompt
- In Scala, call `writeSpatialFile` as an extension method directly on a `SpatialRDD`.
- Always provide the `filename` and the `oformat` (e.g., `"csv"`, `"shapefile"`, `"geojson"`, `"envelope"`).
- Pass additional configuration options (like `"oseparator" -> ","`) as trailing arguments in Scala, which implicitly convert to `BeastOptions`.
- **Do not** use `writeSpatialFile` to save Raster RDDs (GeoTIFFs). For raster data, use `raster.saveAsGeoTiff(filename)` instead.

### Prompt Snippet
```text
To save vector features or spatial partitions to disk in Beast, use the `writeSpatialFile` extension method on the `SpatialRDD`. Specify the output path and the format short-name (e.g., "csv", "geojson", "shapefile"). You can pass extra options like `"oseparator" -> ","` for CSVs. Note: For saving raster data, use `saveAsGeoTiff` instead.
```

### Common Failure Modes
- **Using `writeSpatialFile` for Rasters:** Attempting to save a `RasterRDD` using `writeSpatialFile` instead of the dedicated `saveAsGeoTiff` method, leading to type errors or unsupported format exceptions.
- **Unsupported Output Format:** Providing an `oformat` string that Beast does not support for writing (e.g., trying to write to `"gpx"`, which is input-only). Supported vector outputs are CSV, Esri Shapefile, GeoJSON, JSON+WKT, KML, KMZ, and envelope.
- **Missing Separator Options:** Writing to `"csv"` or `"envelope"` without specifying the `"oseparator"` option when a specific delimiter is required by downstream tasks, resulting in default formatting that may not match expectations.

### Fix Code Hint
```scala
// Incorrect: Trying to save a raster using writeSpatialFile
// raster.writeSpatialFile("output.tif", "geotiff")

// Correct: Saving a raster
raster.saveAsGeoTiff("output.tif")

// Correct: Saving a vector SpatialRDD to CSV with a custom separator
vectorRdd.writeSpatialFile("output.csv", "csv", "oseparator" -> "|")
```

## API Test: `x1`

### Signature
```scala
def x1: Int
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/SlidingWindowTile.scala:14_

### Goal
Retrieves the minimum X coordinate (starting column index) of the raster tile's pixel grid.

### Parameters
_None._

### Input
An instantiated raster tile object (such as `ITile[T]` or `MemoryTile[T]`) representing a chunk of a raster dataset.

### Output
Returns `Int` — the starting column index (minimum X coordinate) of the tile's pixel grid.

### Valid Call Patterns
```scala
// Iterate over all defined pixels in a tile using x1, x2, y1, and y2
var pixelCount = 0
for (y <- tile.y1 to tile.y2; x <- tile.x1 to tile.x2; if tile.isDefined(x, y)) {
  pixelCount += 1
  // Access pixel value with tile.getPixelValue(x, y)
}
```

### LLM Instruction Prompt
- When generating code to iterate over pixels in an `ITile` or `MemoryTile`, use `tile.x1` as the starting bound for the X (column) loop. 
- Do not confuse `x1` with spatial coordinates (e.g., longitude or easting); it is strictly a pixel grid index.
- Always call `x1` on an individual tile instance, not on a distributed `RasterRDD`.

### Prompt Snippet
```text
To iterate over a tile's columns in RDPro, use `x <- tile.x1 to tile.x2`. Remember that `x1` is a pixel grid index, not a spatial coordinate.
```

### Common Failure Modes
- **Confusing grid indices with spatial coordinates:** Assuming `x1` returns a geographic bounding box coordinate (like longitude) rather than the integer column index of the pixel grid.
- **Calling on the wrong abstraction level:** Attempting to call `x1` directly on a `RasterRDD` instead of mapping over its constituent `ITile` elements.
- **Out-of-bounds access:** Iterating from `0` instead of `tile.x1`, which will fail or yield incorrect results if the tile's local grid does not start at `0`.

### Fix Code Hint
```scala
// WRONG: Assuming tile starts at 0 or using spatial coordinates
// for (x <- 0 to tile.width) { ... }

// RIGHT: Use x1 and x2 for the exact column bounds of the tile
for (y <- tile.y1 to tile.y2; x <- tile.x1 to tile.x2; if tile.isDefined(x, y)) {
  val value = tile.getPixelValue(x, y)
}
```

## API Test: `x2`

### Signature
```scala
def x2: Int
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/SlidingWindowTile.scala:16_

### Goal
Returns the maximum X-coordinate (column index) of the raster tile's pixel grid, representing the inclusive upper bound of the tile's width in pixel space.

### Parameters
_None._

### Input
A raster tile instance (such as `ITile[T]` or `MemoryTile[T]`) that has been loaded into memory, typically as part of a `RasterRDD` generated from reading a GeoTIFF or HDF file.

### Output
Returns `Int` — the maximum X-coordinate (column index) of the tile.

### Valid Call Patterns
```scala
// Pattern 1: Iterating over all valid pixels in a tile
var pixelCount = 0
for (y <- tile.y1 to tile.y2; x <- tile.x1 to tile.x2; if tile.isDefined(x, y)) {
  pixelCount += 1
}

// Pattern 2: Accessing or modifying the boundary pixel
tile.setPixelValue(tile.x2, tile.y2, Array[Byte](10, 20, 30))
```

### LLM Instruction Prompt
- Use `tile.x2` to retrieve the inclusive maximum X-coordinate (column index) of a raster tile.
- Combine `x2` with `x1`, `y1`, and `y2` to construct standard Scala `for` comprehensions (`x1 to x2`) when iterating over a tile's pixel grid.
- Do not confuse `x2` (a pixel/column index) with spatial coordinates (e.g., longitude or projected meters).
- Call this method on an individual tile (e.g., inside a `mapPixels` or `map` operation), not directly on a `RasterRDD`.

### Prompt Snippet
```text
To iterate over the pixels of an RDPro raster tile, use a for-comprehension with the tile's pixel bounds: `for (y <- tile.y1 to tile.y2; x <- tile.x1 to tile.x2; if tile.isDefined(x, y))`. `x2` provides the inclusive maximum column index.
```

### Common Failure Modes
- **Calling on the RDD instead of the Tile:** Attempting to call `rasterRDD.x2` will fail. `x2` is a property of the individual `ITile` or `MemoryTile` objects contained within the RDD.
- **Off-by-one errors (Exclusive vs. Inclusive):** Treating `x2` as an exclusive upper bound (e.g., using `until x2`). The test suite explicitly uses `to tile.x2`, indicating it is the inclusive maximum index.
- **Confusing Pixel Coordinates with Spatial Coordinates:** Assuming `x2` returns a geographic bounding box coordinate (like maximum longitude). It strictly returns an integer representing the pixel column index.

### Fix Code Hint
```scala
// WRONG: Attempting to get bounds from the RDD directly
// val maxX = rasterRDD.x2 

// RIGHT: Accessing x2 on the individual tiles within the RDD
val processedRaster = rasterRDD.map(tile => {
  for (y <- tile.y1 to tile.y2; x <- tile.x1 to tile.x2; if tile.isDefined(x, y)) {
    // Perform pixel-level math here
  }
  tile
})
```

## API Test: `y1`

### Signature
```scala
def y1: Int
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/SlidingWindowTile.scala:15_

### Goal
Returns the minimum Y coordinate (starting row index) of the raster tile's pixel grid.

### Parameters
_None._

### Input
An initialized raster tile object (such as `ITile[T]`, `MemoryTile[T]`, or `SlidingWindowTile`) that has been loaded from a raster dataset or created in memory.

### Output
Returns `Int` — the starting Y coordinate (row index) of the tile's bounding box in pixel space.

### Valid Call Patterns
```scala
// Iterate over all defined pixels in a tile using its coordinate bounds
var pixelCount = 0
for (y <- tile.y1 to tile.y2; x <- tile.x1 to tile.x2; if tile.isDefined(x, y)) {
  pixelCount += 1
}

// Accessing the boundary directly
val startY: Int = tile.y1
```

### LLM Instruction Prompt
- Use `tile.y1` in conjunction with `tile.y2`, `tile.x1`, and `tile.x2` to establish the correct bounding loops when iterating over the pixels of an `ITile`.
- NEVER assume a tile's local pixel grid starts at `0`. Distributed raster tiles often retain their global pixel coordinates or specific offsets.
- ALWAYS guard pixel access within the `y1` to `y2` range with `tile.isDefined(x, y)` to safely handle sparse tiles or masked pixels.

### Prompt Snippet
```text
To iterate over a raster tile's pixels in RDPro, loop from `tile.y1 to tile.y2` and `tile.x1 to tile.x2`, ensuring you check `if tile.isDefined(x, y)` before calling `getPixelValue`.
```

### Common Failure Modes
- **Assuming 0-based indexing:** Hardcoding loops from `0 until height` instead of using `y1` to `y2`. This will fail or read incorrect data for tiles that represent a sub-region of a larger global raster.
- **Unsafe pixel access:** Iterating from `y1` to `y2` and blindly calling `getPixelValue(x, y)` without checking `isDefined(x, y)`, which throws errors on sparse or masked pixels.

### Fix Code Hint
```scala
// Incorrect: Hardcoding 0-based indices and missing definition checks
for (y <- 0 until 100; x <- 0 until 100) {
  val v = tile.getPixelValue(x, y) 
}

// Correct: Using y1/y2 bounds and checking if the pixel is defined
for (y <- tile.y1 to tile.y2; x <- tile.x1 to tile.x2; if tile.isDefined(x, y)) {
  val v = tile.getPixelValue(x, y)
}
```

## API Test: `y2`

### Signature
```scala
def y2: Int
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/SlidingWindowTile.scala:17_

### Goal
Returns the maximum Y coordinate (inclusive row index) of the raster tile's pixel grid.

### Parameters
_None._

### Input
A valid raster tile object (such as `MemoryTile[T]` or `ITile[T]`) that has been loaded into memory or yielded by a raster RDD operation (e.g., during a Raptor join or pixel iteration).

### Output
Returns `Int` — the maximum Y coordinate (row index) of the tile.

### Valid Call Patterns
```scala
// Pattern 1: Iterating over all pixels in a tile using inclusive bounds
var pixelCount = 0
for (y <- tile.y1 to tile.y2; x <- tile.x1 to tile.x2; if tile.isDefined(x, y)) {
  pixelCount += 1
}

// Pattern 2: Accessing or modifying the bottom-most row of the tile
tile.setPixelValue(tile.x2, tile.y2, Array[Byte](10, 20, 30))
```

### LLM Instruction Prompt
- Use `tile.y2` to get the maximum Y coordinate (row index) of a raster tile.
- Always treat `y2` as an **inclusive** bound when iterating over the tile's grid (use `to tile.y2`, not `until tile.y2`).
- Combine `y2` with `y1`, `x1`, and `x2` to define the complete bounding box of the tile's pixel coordinates.

### Prompt Snippet
```text
To iterate over all pixels in an RDPro raster tile, use `tile.y1 to tile.y2` for the Y-axis and `tile.x1 to tile.x2` for the X-axis. `y2` represents the inclusive maximum row index of the tile. Always check `tile.isDefined(x, y)` before accessing the pixel value.
```

### Common Failure Modes
- **Off-by-one errors during iteration:** Treating `y2` as an exclusive upper bound (using `until tile.y2` instead of `to tile.y2`), which causes the bottom-most row of the tile to be skipped during processing.
- **Confusing pixel indices with spatial coordinates:** Assuming `y2` returns a spatial coordinate (like latitude or projected Y). It returns a discrete pixel row index.

### Fix Code Hint
```scala
// WRONG: 'until' skips the last row of the tile
for (y <- tile.y1 until tile.y2; x <- tile.x1 until tile.x2) {
  // ...
}

// RIGHT: 'to' correctly includes the y2 boundary
for (y <- tile.y1 to tile.y2; x <- tile.x1 to tile.x2; if tile.isDefined(x, y)) {
  // ...
}
```

## API Test: `zigzagDecode`

### Signature
```scala
def zigzagDecode(x: Int): Int
```
_Source doc:_ Decodes a value from Zigzag encoding

### Goal
Decodes a Zigzag-encoded integer back into its original signed integer value, typically used when parsing or inspecting raw Mapbox Vector Tile (MVT) geometry coordinates and commands.

### Parameters
- `x` (`Int`): The Zigzag-encoded integer value to decode.

### Input
A Zigzag-encoded integer. In the context of Beast's visualization and MVT generation, this is usually extracted directly from the raw geometry array of a compiled MVT feature (e.g., `feature.getGeometry(index)`).

### Output
Returns `Int` — The decoded signed integer, which typically represents a coordinate delta or command integer in the MVT image space.

### Valid Call Patterns
```scala
// Assuming `feature` is a VectorTile.Tile.Feature from an MVT layer
val encodedX = feature.getGeometry(1)
val encodedY = feature.getGeometry(2)

val decodedX = VectorLayerBuilder.zigzagDecode(encodedX)
val decodedY = VectorLayerBuilder.zigzagDecode(encodedY)
```

### LLM Instruction Prompt
- Use `VectorLayerBuilder.zigzagDecode(x)` to decode Zigzag-encoded integers when manually inspecting or parsing Mapbox Vector Tile (MVT) geometries.
- Do not use this for general raster pixel math or standard vector coordinates; it is strictly a low-level utility for MVT protocol buffer decoding.
- Always qualify the call with the `VectorLayerBuilder` object.

### Prompt Snippet
```text
To decode Zigzag-encoded integers from raw MVT geometries, use `VectorLayerBuilder.zigzagDecode(x)`.
```

### Common Failure Modes
- **Passing standard (non-encoded) integers:** Passing an already decoded or standard coordinate integer will result in an incorrect, mangled signed integer output. Only pass values known to be Zigzag-encoded.
- **Missing object qualifier:** Calling `zigzagDecode(x)` without the `VectorLayerBuilder` object qualifier will cause a compilation error.

### Fix Code Hint
```scala
// WRONG: Calling without the object qualifier
// val x = zigzagDecode(feature.getGeometry(1))

// RIGHT: Qualify with VectorLayerBuilder
val x = VectorLayerBuilder.zigzagDecode(feature.getGeometry(1))
```

## API Test: `zonalStats2`

### Signature
```scala
def zonalStats2[T](zones: RDD[IFeature], raster: RDD[ITile[T]], collectorClass: Class[_ <: Collector], opts: BeastOptions, numTiles: LongAccumulator = null)
```
_Source: beast/raptor/src/main/scala/edu/ucr/cs/bdlab/raptor/ZonalStatistics.scala:128_

_Source doc:_ Computes zonal statistics between a set of zones (polygons) and a raster file given by its path and a layer in that file. The result is an RDD of pairs of a feature and a collector value @param zones a set of polygons that represent the regions or zones @param raster the RDD of tiles @param collectorClass the class that collects the pixel values to compute the statistics @param opts additional user-defined options @param numTiles an optional accumulator to collect the total number of processed tiles @return a set of (Feature, Statistics)

### Goal
Computes zonal statistics (such as count, sum, min, max) by matching a set of vector zones (polygons) against a distributed raster dataset, returning an RDD of features paired with their computed statistics.

### Parameters
- `zones` (`RDD[IFeature]`): An RDD of vector features (typically polygons) representing the regions or administrative boundaries over which to aggregate raster pixels.
- `raster` (`RDD[ITile[T]]`): An RDD of raster tiles containing the pixel values to be aggregated. The type `T` must match the underlying raster data type.
- `collectorClass` (`Class[_ <: Collector],
                  opts: BeastOptions, numTiles: LongAccumulator`), default `null`: 
  *Note: The JSON signature parser merged three parameters here. They represent:*
  1. `collectorClass`: The class of the `Collector` (e.g., `classOf[Statistics]`) used to aggregate pixel values.
  2. `opts`: `BeastOptions` for user-defined configuration.
  3. `numTiles`: An optional Spark `LongAccumulator` to track the total number of processed tiles (defaults to `null`).

### Input
- **Vector Zones:** An `RDD[IFeature]` loaded from formats like Shapefile, GeoJSON, or CSV. If the vectors and raster have different Coordinate Reference Systems (CRS), the vectors must be reprojected first (e.g., using `Reprojector.reprojectRDD`).
- **Raster Tiles:** An `RDD[ITile[T]]` loaded via `sc.geoTiff[T]` or `new RasterFileRDD[T]`. 
- **Preconditions & Type Selection:** 
  - The generic type `T` must exactly match the raster's runtime pixel type (e.g., `Int` for `IntegerType`, `Float` for `FloatType`).
  - **Raptor Predicate Rule:** Polygons match pixels whose *center* falls inside the polygon boundary.

### Output
Returns `unspecified` — Represents an `RDD[(IFeature, Collector)]`. Each tuple contains the original vector feature and a `Collector` instance (e.g., `Statistics`) holding the aggregated pixel math (count, sum, etc.) for that specific zone.

### Valid Call Patterns
```scala
// Assuming sparkContext is available and BeastOptions is imported
val vectorFile = locateResource("/vectors/ne_110m_admin_1_states_provinces.zip")
val rasterFile = locateResource("/rasters/glc2000_small.tif")

val polygons: RDD[IFeature] = SpatialReader.readInput(sparkContext, new BeastOptions(), vectorFile.getPath, "shapefile")
val raster: RDD[ITile[Int]] = new RasterFileRDD[Int](sparkContext, rasterFile.getPath, new BeastOptions())

// Call ZonalStatistics.zonalStats2 statically
val zsResults: RDD[(IFeature, Collector)] = ZonalStatistics.zonalStats2(
  polygons, 
  raster, 
  classOf[Statistics], 
  new BeastOptions()
)

// Extracting statistics requires casting the Collector
val processedStats = zsResults.map { case (feature, collector) =>
  val stats = collector.asInstanceOf[Statistics]
  val count = stats.count(0)
  val sum = stats.sum(0)
  (feature, count, sum)
}
```

### LLM Instruction Prompt
- Call `ZonalStatistics.zonalStats2(zones, raster, classOf[Statistics], new BeastOptions())` statically; it is not an implicit method on the RDD.
- Ensure the generic type `T` of the raster `RDD[ITile[T]]` exactly matches the physical pixel type of the GeoTIFF (e.g., `Int` or `Float`).
- The returned `Collector` must be cast to the specific class passed in `collectorClass` (e.g., `.asInstanceOf[Statistics]`) before you can access its aggregation methods like `.count(band)` or `.sum(band)`.
- If the vector and raster datasets are in different CRSs, reproject the vector `RDD[IFeature]` to match the raster before calling `zonalStats2`.

### Prompt Snippet
```text
To compute zonal statistics in RDPro, use `ZonalStatistics.zonalStats2(zones, raster, classOf[Statistics], new BeastOptions())`. The raster type `T` must match the file's pixel type. Cast the resulting `Collector` to `Statistics` to access `.count(0)` and `.sum(0)`.
```

### Common Failure Modes
- **Type Mismatch:** Loading a Float GeoTIFF as `sc.geoTiff[Int]` or passing an `RDD[ITile[Float]]` to `zonalStats2` while expecting integer statistics. The type `T` must be strictly aligned.
- **ClassCastException on Output:** Attempting to call methods directly on the returned `Collector` trait without first casting it to the concrete class (e.g., `Statistics`) provided in the `collectorClass` parameter.
- **Empty Results due to CRS Mismatch:** Passing vector zones that do not overlap the raster because they are in a different coordinate reference system. Vectors must be reprojected to the raster's CRS prior to the join.

### Fix Code Hint
```scala
// BAD: Calling methods directly on the Collector trait
val badResults = ZonalStatistics.zonalStats2(zones, raster, classOf[Statistics], opts)
  .map(fc => fc._2.sum(0)) // ERROR: value sum is not a member of Collector

// GOOD: Cast the Collector to Statistics first
val goodResults = ZonalStatistics.zonalStats2(zones, raster, classOf[Statistics], opts)
  .map(fc => fc._2.asInstanceOf[Statistics].sum(0))
```

## API Test: `zonalStatsLocal`
_Grounding: doc-repaired from source (docfix)._

### Signature
```scala
def zonalStatsLocal[T](geometries: Array[Geometry], raster: IRasterReader[T], collectorClass: Class[_ <: Collector]) : Array[Collector]
def zonalStatsLocal[T](zones: Array[IFeature], raster: IRasterReader[T], collectorClass: Class[_ <: Collector]) : Array[Collector]
```

### Goal
**ADVANCED/LOW-LEVEL API.** Compute zonal statistics (e.g., count, sum) locally in a single thread for a small set of vector geometries against a raster. 
*Note: This API requires manual plumbing and should be excluded from the main user-facing benchmark denominator. Typical users should use the distributed `raptorJoin` or RDD-level zonal statistics methods.*

### Parameters
- `geometries` (`Array[Geometry]`): The array of vector geometries (or `IFeature` via overload) that define the zones for aggregation.
- `raster` (`IRasterReader[T]`): The initialized raster reader pointing to the raster file being aggregated.
- `collectorClass` (`Class[_ <: Collector]`): The class that computes the statistics (e.g., `classOf[Statistics]`).

### Input
- **Geometries:** A small local array of geometries or features.
- **Raster Reader (ADVANCED/LOW-LEVEL):** Requires explicit low-level construction of an `IRasterReader[T]` (e.g., `GeoTiffReader[T]`). The caller owns this object, must manually initialize it with exactly 4 arguments, and is responsible for closing it.

### Output
Returns `Array[Collector]` — An array of statistics collectors equal in length to the input array of features. Features that do not overlap any pixels will have `null` at their corresponding index.

### Valid Call Patterns
```scala
import org.apache.hadoop.fs.{Path, FileSystem}
import edu.ucr.cs.bdlab.beast.common.BeastOptions
import edu.ucr.cs.bdlab.raptor.{ZonalStatistics, GeoTiffReader, Statistics}

// 1. Explicit low-level construction of the IRasterReader (Caller-owned)
val path = new Path(raster_tif)
val fs: FileSystem = path.getFileSystem(sc.hadoopConfiguration)
val rasterReader = new GeoTiffReader[Float]()

// 2. Initialize requires exactly 4 arguments: (FileSystem, String, String, BeastOptions)
rasterReader.initialize(fs, path.toString, "0", new BeastOptions())

// 3. Call the local API statically
val featuresArray = featuresRDD.take(10)
val zsResults = ZonalStatistics.zonalStatsLocal(featuresArray, rasterReader, classOf[Statistics])

// 4. Safely extract results by filtering nulls (geometries with no overlapping pixels)
val validStats = zsResults.filter(_ != null).map(_.asInstanceOf[Statistics])
val sums = validStats.map(_.sum(0))

// 5. Cleanup caller-owned resources
rasterReader.close()
```

### LLM Instruction Prompt
- `zonalStatsLocal` is an ADVANCED/LOW-LEVEL API called statically via `ZonalStatistics.zonalStatsLocal(...)`.
- You must manually instantiate and initialize an `IRasterReader` (e.g., `new GeoTiffReader[Float]()`).
- The `initialize` method on the reader requires exactly four arguments: `(fileSystem: FileSystem, path: String, layer: String, opts: BeastOptions)`.
- The `path` argument to `initialize` must be a `String` (e.g., `path.toString`), not a Hadoop `Path` object.
- The `layer` argument is typically `"0"`, and `opts` should be a `new BeastOptions()`.
- You MUST handle `null` values in the returned `Array[Collector]`, as any geometry that does not overlap a pixel will return `null`.

### Prompt Snippet
```text
For local zonal stats, use `ZonalStatistics.zonalStatsLocal(featuresArray, rasterReader, classOf[Statistics])`. You must manually create the reader (e.g., `new GeoTiffReader[Float]()`) and call `initialize(fs, path.toString, "0", new BeastOptions())` using a String path, not a Hadoop Path. Filter out `null` results before casting to your Collector class.
```

### Common Failure Modes
- **Signature Mismatch on Initialize (Recent Failure):** Guessing `rasterReader.initialize(fs, path)` fails. The trait explicitly requires four arguments: `initialize(fileSystem: FileSystem, path: String, layer: String, opts: BeastOptions)`. Furthermore, the `path` argument must be a `String`, not a Hadoop `Path` object.
- **NullPointerException:** Failing to filter out `null` in the returned `Array[Collector]` before casting or accessing metrics.
- **Improper Use of Low-Level API:** Attempting to use this ADVANCED/LOW-LEVEL API for large datasets instead of the distributed `raptorJoin`, causing out-of-memory errors or severe performance degradation.

### Fix Code Hint
```scala
// WRONG: Missing arguments, passing a Hadoop Path object, and failing to filter nulls
val path = new Path(raster_tif)
rasterReader.initialize(fs, path)
val zsResults = ZonalStatistics.zonalStatsLocal(features, rasterReader, classOf[Statistics])
val sums = zsResults.map(_.asInstanceOf[Statistics].sum(0))

// CORRECT: 4 arguments, path as String, layer as "0", BeastOptions, and null filtering
val path = new Path(raster_tif)
rasterReader.initialize(fs, path.toString, "0", new BeastOptions())
val zsResults = ZonalStatistics.zonalStatsLocal(features, rasterReader, classOf[Statistics])
val validStats = zsResults.filter(_ != null).map(_.asInstanceOf[Statistics])
val sums = validStats.map(_.sum(0))
```

