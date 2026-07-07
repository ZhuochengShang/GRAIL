# KryoInputToObjectInput

_The `available` method returns the number of bytes that can be read from the input stream without blocking, which is useful for understanding how much data is…_

**Receiver:** instance — obtain a `KryoInputToObjectInput` value, then `<value>.<method>(...)`

**Members** (most robust first): ★ `available` **(primary)**, ⚠️ `read`

---

## API Test: `available`
_Grounding: sibling-grounded — a tested method on the same class shows the pattern._

### Signature
```scala
override def available(): Int
```
_Source: beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/util/BufferedFSDataInputStream.scala:99  (+1 more definition site/overload)_

### Goal
The `available` method returns the number of bytes that can be read from the input stream without blocking, which is useful for understanding how much data is ready for processing in a geospatial raster context.

### Parameters
_None._

### Input
No specific input is required for this method.

### Output
Returns `Int` — the number of bytes available to read from the input stream, indicating how much data can be processed immediately.

### Valid Call Patterns
```scala
val bytesAvailable: Int = value.available()
```

### LLM Instruction Prompt
- When calling `available`, ensure that the input stream is properly initialized and opened before invoking this method to avoid unexpected results.

### Prompt Snippet
```text
To check how many bytes are available for reading from the input stream, use the `available` method: `value.available()`.
```

### Common Failure Modes
- **[compile]** error: not enough arguments for constructor BufferedFSDataInputStream: (in: org.apache.hadoop.fs.FSDataInputStream, bufferSize: Int)edu.ucr.cs.bdlab.beast.util.BufferedFSDataInputStream. _(seen 4x)_

### Fix Code Hint
```scala
// Ensure the input stream is open before calling available
if (inputStream.isOpen) {
  val bytesAvailable: Int = inputStream.available()
} else {
  // Handle the case where the stream is not open
}
```

## API Test: `read`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
override def read(kryo: Kryo, input: Input, aClass: Class[IntermediateVectorTile]): IntermediateVectorTile
override def read(kryo: Kryo, input: Input, klass: Class[MemoryTile[Any]]): MemoryTile[Any]
override def read(kryo: Kryo, input: Input, klass: Class[MemoryTileWindow[T]]): MemoryTileWindow[T]
override def read(kryo: Kryo, input: Input, klass: Class[AbstractConvolutionTile[Any]]): AbstractConvolutionTile[Any]
override def read(kryo: Kryo, input: Input, tileClass: Class[MaskTile[T]]): MaskTile[T]
override def read(kryo: Kryo, input: Input, tileClass: Class[AbstractGeoTiffTile[T]]): AbstractGeoTiffTile[T]
override def read(kryo: Kryo, in: Input): Unit
override def read(kryo: Kryo, input: Input, tileClass: Class[ITile[T]]): ITile[T]
override def read(kryo: Kryo, input: Input, klass: Class[RasterFeature]): RasterFeature
override def read(kryo: Kryo, input: Input): Unit
override def read(kryo: Kryo, input: Input, klass: Class[RasterMetadata]): RasterMetadata
def read(spark: SparkSession, path: String, options: java.util.Map[String, String]): DataFrame
def read(spark: SparkSession, path: String, options: Map[String, Any]): DataFrame
def read: Int
override def read(b: Array[Byte]): Int
override def read(b: Array[Byte], off: Int, len: Int): Int
def read(in: FSDataInputStream): Unit
def read(buffer: Array[Byte], pos: Int, bufferLength: Int): Unit
override def read(): Int
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/IntermediateVectorTileSerializer.scala:29  (+23 more definition site/overload)_

### Goal
The `read` function deserializes data from a specified input source into a raster tile format suitable for further geospatial analysis.

### Parameters
- `kryo` (`Kryo`): An instance of the Kryo serialization framework used for efficient serialization and deserialization of objects.
- `input` (`Input`): The input source from which data is read, typically representing a stream of bytes or a file.
- `aClass` (`Class[IntermediateVectorTile]`): The class type that specifies the structure of the raster tile being read, allowing for the correct deserialization into an `IntermediateVectorTile`.

### Input
The caller must provide a valid `Kryo` instance, an `Input` source containing serialized raster data, and a class type that matches the expected output tile structure. The input data must be correctly formatted for the specified tile class.

### Output
Returns `IntermediateVectorTile` — an object representing a raster tile that has been deserialized from the input source, which can be used for further processing in geospatial analysis.

### Valid Call Patterns
```scala
val intermediateTile: IntermediateVectorTile = value.read(kryo, input, classOf[IntermediateVectorTile])
```

### LLM Instruction Prompt
- Ensure that the `kryo` instance is properly initialized and configured for the expected data types.
- The `input` must be a valid source containing serialized data compatible with the specified class type.
- Use the correct class type for the output tile to ensure successful deserialization.

### Prompt Snippet
```text
Read a raster tile from the input source using the specified Kryo instance and class type.
```

### Common Failure Modes
- **[runtime]** java.lang.IndexOutOfBoundsException: Index 71 out of bounds for length 0 _(seen 2x)_
- **[compile]** error: not found: value value _(seen 2x)_

### Fix Code Hint
```scala
// Ensure that the Kryo instance is configured correctly and the input source is valid.
val kryo = new Kryo()
val input = new Input(new FileInputStream("path/to/serialized/data"))
val intermediateTile: IntermediateVectorTile = value.read(kryo, input, classOf[IntermediateVectorTile])
```
