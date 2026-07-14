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