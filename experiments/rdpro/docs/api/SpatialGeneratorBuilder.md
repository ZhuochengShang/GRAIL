# SpatialGeneratorBuilder

_The `config` function sets configuration options for the spatial data generation process in RDPro._

**Receiver:** instance — obtain a `SpatialGeneratorBuilder` value, then `<value>.<method>(...)`

**Members** (most robust first): ★ `config` **(primary)**, ★ `diagonal`, ★ `distribution`, ★ `makeBoxes`, ★ `mbr`, ★ `parcel`, ★ `sierpinski`, ⚠️ `bit`, ⚠️ `gaussian`, ⚠️ `generate`, ⚠️ `numPartitions`

---

## API Test: `config`
_Grounding: test-backed — usage mined from a real, passing test._

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
The `config` function sets configuration options for the spatial data generation process in RDPro.

### Parameters
- `key` (`String`): The configuration option to set, such as `UniformDistribution.MaxSize` or `SpatialGenerator.Seed`. Expected values are specific keys defined in the context of spatial data generation.
- `value` (`Any`): The value to assign to the specified configuration key. This can be a numeric value, a string, or other types depending on the key being configured.

### Input
The caller must provide valid configuration keys and values that correspond to the spatial data generation process. There are no specific file formats required for this function, but it should be called in the context of a spatial data generation workflow.

### Output
Returns `JavaSpatialGeneratorBuilder` — an instance of the builder that allows further configuration and execution of spatial data generation tasks.

### Valid Call Patterns
```scala
val randomPoints: SpatialRDD = new SpatialGeneratorBuilder(sparkContext).mbr(desiredMBR)
  .config(UniformDistribution.MaxSize, "0.2,0.1")
  .config(UniformDistribution.NumSegments, 10)
  .config(UniformDistribution.GeometryType, "box")
  .config(SpatialGenerator.Seed, 1794)
  .uniform(10)
```

### LLM Instruction Prompt
- When calling `config`, ensure that the `key` and `value` parameters are valid and correspond to the expected configuration options for spatial data generation.

### Prompt Snippet
```text
Set the configuration for spatial data generation using the config method, specifying the key and value as needed.
```

### Common Failure Modes
- (no failures observed yet)

### Fix Code Hint
```scala
// Ensure that the key is valid and the value matches the expected type for that key.
val builder = new SpatialGeneratorBuilder(sparkContext)
builder.config(UniformDistribution.MaxSize, "0.2,0.1") // Correct usage
```

## API Test: `diagonal`
_Grounding: sibling-grounded — a tested method on the same class shows the pattern._

### Signature
```scala
def diagonal(cardinality: Long, percentage: Double = 0.5, buffer: Double = 0.2): JavaSpatialRDD
def diagonal(cardinality: Long, percentage: Double = 0.5, buffer: Double = 0.2): SpatialRDD
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/generator/JavaSpatialGeneratorBuilder.scala:106  (+1 more definition site/overload)_

_Source doc:_ Generate diagonally distributed data @param cardinality the number of records to generate @param percentage the percentage of records exactly on the diagonal line @param buffer the buffer around the diagonal line in which records can be generated @return the RDD that contains the generated data

### Goal
The `diagonal` function generates a set of spatial data points that are distributed along a diagonal line, with options to control the density and spread of the points.

### Parameters
- `cardinality` (`Long`): The total number of spatial records to generate. This value should be a positive integer representing how many points will be created.
- `percentage` (`Double`), default `0.5`: The fraction of the total records that will be placed exactly on the diagonal line. This value should be between `0.0` and `1.0`, where `0.0` means no points on the diagonal and `1.0` means all points on the diagonal.
- `buffer` (`Double`), default `0.2`: The distance around the diagonal line within which additional points can be generated. This value should be a non-negative number that defines the spread of points around the diagonal.

### Input
The function does not require any specific file formats or external data inputs. However, it must be called within a valid Spark context, and the parameters must be set according to the expected types and constraints.

### Output
Returns `JavaSpatialRDD` — a distributed collection of spatial data points generated according to the specified parameters. The output represents the spatial distribution of points, which can be used for further geospatial analysis or visualization.

### Valid Call Patterns
```scala
sc.generateSpatialData
  .diagonal(1000, percentage = 0.3, buffer = 0.2)
```

### LLM Instruction Prompt
- When calling `diagonal`, ensure that the `cardinality` is a positive `Long`, `percentage` is a `Double` between `0.0` and `1.0`, and `buffer` is a non-negative `Double`. The call must be made within a valid Spark context.

### Prompt Snippet
```text
Generate a diagonal spatial dataset with 1000 records, where 30% of the points are exactly on the diagonal and a buffer of 0.2 around the diagonal.
```

### Common Failure Modes
- (no failures observed yet)

### Fix Code Hint
```scala
// Ensure cardinality is positive, percentage is between 0.0 and 1.0, and buffer is non-negative
val spatialData = sc.generateSpatialData.diagonal(1000, percentage = 0.3, buffer = 0.2)
```

## API Test: `distribution`
_Grounding: sibling-grounded — a tested method on the same class shows the pattern._

### Signature
```scala
def distribution(distribution: DistributionType): JavaSpatialGeneratorBuilder
def distribution(distribution: DistributionType): SpatialGeneratorBuilder
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/generator/JavaSpatialGeneratorBuilder.scala:55  (+1 more definition site/overload)_

_Source doc:_ Set the distribution of the generated data @param distribution the distributed of the generated data as one of {[[UniformDistribution]], [[DiagonalDistribution]], [[GaussianDistribution]], [[BitDistribution]], [[SierpinskiDistribution]], [[ParcelDistribution]]} @return

### Goal
The `distribution` function sets the statistical distribution type for generating spatial data in a geospatial analysis context.

### Parameters
- `distribution` (`DistributionType`): Specifies the type of distribution to be used for generating spatial data. Expected values include:
  - `UniformDistribution`
  - `DiagonalDistribution`
  - `GaussianDistribution`
  - `BitDistribution`
  - `SierpinskiDistribution`
  - `ParcelDistribution`

### Input
The caller must provide a valid `DistributionType` as an argument. There are no specific file formats required for this function, but it is typically used in the context of generating spatial data within a Spark environment.

### Output
Returns `JavaSpatialGeneratorBuilder` — an object that allows further configuration and generation of spatial data based on the specified distribution type.

### Valid Call Patterns
```scala
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
- When calling `distribution`, ensure that the provided `DistributionType` is one of the specified valid types and that it is used in conjunction with the appropriate configuration methods for generating spatial data.

### Prompt Snippet
```text
Set the distribution for generating spatial data using one of the valid DistributionType options.
```

### Common Failure Modes
- (no failures observed yet)

### Fix Code Hint
```scala
Ensure that the distribution type is valid and that you follow up with necessary configuration calls before generating spatial data.
```

## API Test: `makeBoxes`
_Grounding: sibling-grounded — a tested method on the same class shows the pattern._

### Signature
```scala
def makeBoxes(maxSize: Int*): JavaSpatialGeneratorBuilder
def makeBoxes(maxSize: Double*): SpatialGeneratorBuilder
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/generator/JavaSpatialGeneratorBuilder.scala:76  (+1 more definition site/overload)_

_Source doc:_ Generate boxes around each generated point @param maxSize the maximum size for each side length of the generated box @return

### Goal
The `makeBoxes` function generates square boxes around each generated point, with the specified maximum size for each side length, facilitating spatial data generation for geospatial analysis.

### Parameters
- `maxSize` (`Int*`): The maximum size for each side length of the generated box. This can be one or more integer values representing the dimensions of the boxes.

### Input
The caller must provide a valid Spark context and ensure that the spatial data generation process is initiated prior to calling `makeBoxes`. The input must be compatible with the spatial data generation workflow.

### Output
Returns `JavaSpatialGeneratorBuilder` — an instance of `JavaSpatialGeneratorBuilder` that allows further configuration and generation of spatial data, specifically boxes around points.

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
- When calling `makeBoxes`, ensure that the maximum size parameters are provided as integers or doubles, and that the spatial data generation context is correctly set up.

### Prompt Snippet
```text
Generate boxes around each generated point using makeBoxes with specified maximum sizes.
```

### Common Failure Modes
- (no failures observed yet)

### Fix Code Hint
```scala
// Ensure the Spark context is initialized and spatial data generation is set up before calling makeBoxes
val boxes = sparkContext.generateSpatialData.makeBoxes(0.3, 0.4)
```

## API Test: `mbr`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def mbr : EnvelopeNDLite
def mbr: EnvelopeNDLite
def mbr(mbr: EnvelopeNDLite): SpatialGeneratorBuilder
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/generator/SpatialGeneratorBuilder.scala:97  (+2 more definition site/overload)_

_Source doc:_ Generates data in the given bounding box @param mbr the bounding box of the generated data @return

### Goal
The `mbr` function generates spatial data within a specified bounding box, facilitating the creation of raster datasets for geospatial analysis.

### Parameters
- `mbr` (`EnvelopeNDLite`): The bounding box that defines the spatial extent for the generated data. It is expected to be an instance of `EnvelopeNDLite` that specifies the minimum and maximum coordinates in N-dimensional space.

### Input
The caller must provide an `EnvelopeNDLite` object that defines the bounding box for the spatial data generation. This input must be properly initialized to represent valid spatial coordinates.

### Output
Returns `SpatialGeneratorBuilder` — an object that allows further configuration and generation of spatial data based on the specified bounding box. This object is used to build and execute spatial data generation tasks.

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
- When calling `mbr`, ensure that the `EnvelopeNDLite` parameter is correctly defined to represent the desired spatial extent for data generation.

### Prompt Snippet
```text
Generate spatial data within the bounding box defined by an EnvelopeNDLite instance.
```

### Common Failure Modes
- (no failures observed yet)

### Fix Code Hint
```scala
val validMBR = new EnvelopeNDLite(2, 1.0, 0.0, 4.0, 8.0) // Ensure the bounding box is correctly defined
val spatialData = new SpatialGeneratorBuilder(sparkContext).mbr(validMBR).uniform(1000)
```

## API Test: `parcel`
_Grounding: sibling-grounded — a tested method on the same class shows the pattern._

### Signature
```scala
def parcel(cardinality: Long, dither: Double = 0.2, splitRange: Double = 0.2): JavaSpatialRDD
def parcel(cardinality: Long, dither: Double = 0.2, splitRange: Double = 0.2): SpatialRDD
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/generator/JavaSpatialGeneratorBuilder.scala:153  (+1 more definition site/overload)_

_Source doc:_ Generates boxes from the parcel distribution @param cardinality the number of records to generate @param dither the amount of randomization to add to each generated box @param splitRange the range of splitting each box @return the RDD that contains the generated data

### Goal
The `parcel` function generates a specified number of spatial boxes with randomization and splitting characteristics, useful for simulating spatial distributions in geospatial analysis.

### Parameters
- `cardinality` (`Long`): The number of spatial boxes (records) to generate. This value should be a positive integer representing how many boxes you want in the output.
- `dither` (`Double`), default `0.2`: The amount of randomization applied to the position of each generated box. This value should be between `0.0` and `1.0`, where higher values introduce more randomness.
- `splitRange` (`Double`), default `0.2`: The range within which each box can be split into smaller boxes. This value should be a positive number that determines how much variability is allowed in the size of the generated boxes.

### Input
The caller must provide a valid Spark context and ensure that the `generateSpatialData` method is called prior to invoking `parcel`. The input must be compatible with the spatial data generation process.

### Output
Returns `JavaSpatialRDD` — an RDD containing the generated spatial boxes, which can be used for further spatial analysis or visualization.

### Valid Call Patterns
```scala
val parcels: SpatialRDD = sc.generateSpatialData
      .parcel(1000000, dither = 0.1, splitRange = 0.4)

sc.generateSpatialData
  .parcel(100, dither = 0.2, splitRange = 0.3)
  .plotImage(300, 300, "parcel.png")
```

### LLM Instruction Prompt
When calling `parcel`, ensure that the `cardinality` is a positive integer, and the `dither` and `splitRange` values are within the specified ranges. Use the method in conjunction with a valid spatial data generator.

### Prompt Snippet
```text
Generate a spatial distribution of boxes using the parcel function with a specified cardinality, dither, and split range.
```

### Common Failure Modes
- (no failures observed yet)

### Fix Code Hint
```scala
// Ensure cardinality is positive and dither/splitRange are within valid ranges
val parcels: SpatialRDD = sc.generateSpatialData
      .parcel(1000, dither = 0.1, splitRange = 0.2)
```

## API Test: `sierpinski`
_Grounding: sibling-grounded — a tested method on the same class shows the pattern._

### Signature
```scala
def sierpinski(cardinality: Long): JavaSpatialRDD
def sierpinski(cardinality: Long): SpatialRDD
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/generator/JavaSpatialGeneratorBuilder.scala:127  (+1 more definition site/overload)_

_Source doc:_ Generate data from the Sierpinski distribution @param cardinality the number of records to generate @return the RDD that contains the generated data

### Goal
The `sierpinski` function generates a dataset based on the Sierpinski distribution, which can be used for spatial analysis and visualization in geospatial applications.

### Parameters
- `cardinality` (`Long`): The number of records to generate. This value determines the size of the output dataset.

### Input
No specific data files or formats are required as input. The only precondition is that the `cardinality` parameter must be a positive integer representing the desired number of records.

### Output
Returns `JavaSpatialRDD` — an RDD containing the generated spatial data points based on the Sierpinski distribution, suitable for further spatial analysis or visualization.

### Valid Call Patterns
```scala
sc.generateSpatialData
  .sierpinski(1000)
```

### LLM Instruction Prompt
- When calling `sierpinski`, ensure that the `cardinality` parameter is a positive `Long` value to specify the number of records to generate.

### Prompt Snippet
```text
Generate a Sierpinski distribution dataset with a specified number of records.
```

### Common Failure Modes
- (no failures observed yet)

### Fix Code Hint
```scala
// Ensure cardinality is a positive number
val records: JavaSpatialRDD = sc.generateSpatialData.sierpinski(1000)
```

## API Test: `bit`
_Grounding: sibling-grounded — a tested method on the same class shows the pattern._

### Signature
```scala
def bit(cardinality: Long, digits: Int = 10, probability: Double = 0.2): JavaSpatialRDD
def bit(cardinality: Long, digits: Int = 10, probability: Double = 0.2): SpatialRDD
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/generator/JavaSpatialGeneratorBuilder.scala:139  (+1 more definition site/overload)_

_Source doc:_ Generate data from the bit distribution @param cardinality the number of records to generate @param digits the number of digits to set per coordinate @param probability the probability of setting each bit @return the RDD that contains the generated data

### Goal
The `bit` function generates spatial data based on a bit distribution, allowing users to create random points with specified characteristics.

### Parameters
- `cardinality` (`Long`): The total number of records (points) to generate. This value should be a positive integer representing how many spatial data points you want in the output.
- `digits` (`Int`), default `10`: The number of digits to set per coordinate. This parameter controls the precision of the generated coordinates, with higher values allowing for more detailed spatial representation.
- `probability` (`Double`), default `0.2`: The probability of setting each bit in the generated data. This value should be between `0.0` and `1.0`, where lower values result in sparser data and higher values lead to denser data.

### Input
The caller must provide the following:
- A valid Spark context (`SparkContext`) to execute the operation.
- Ensure that the `cardinality` is a positive integer.
- The `digits` and `probability` parameters are optional and will default to `10` and `0.2`, respectively, if not specified.

### Output
Returns `JavaSpatialRDD` — an RDD containing the generated spatial data points based on the specified bit distribution parameters. The output is structured as a collection of spatial records that can be further processed or analyzed.

### Valid Call Patterns
```scala
sc.generateSpatialData
  .bit(1000, digits = 10, probability = 0.2)
```

### LLM Instruction Prompt
- When calling `bit`, ensure that the `cardinality` is a positive integer and that the `digits` and `probability` parameters are within their expected ranges.

### Prompt Snippet
```text
Generate spatial data using the bit distribution with a specified number of records, digits per coordinate, and probability of setting each bit.
```

### Common Failure Modes
- **[compile]** error: value rawSpatialRDD is not a member of edu.ucr.cs.bdlab.beast.JavaSpatialRDD _(seen 2x)_
- **[compile]** error: value rawSpatialRDD is not a member of edu.ucr.cs.bdlab.beast.cg.SpatialDataTypes.SpatialRDD _(seen 2x)_

### Fix Code Hint
```scala
// Ensure cardinality is positive and digits are non-negative
val randomPoints: JavaSpatialRDD = sc.generateSpatialData.bit(1000, digits = 10, probability = 0.2)
```

## API Test: `gaussian`
_Grounding: sibling-grounded — a tested method on the same class shows the pattern._

### Signature
```scala
def gaussian(cardinality: Long): JavaSpatialRDD
def gaussian(cardinality: Long): SpatialRDD
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/generator/JavaSpatialGeneratorBuilder.scala:117  (+1 more definition site/overload)_

_Source doc:_ Generate Gaussian distributed data @param cardinality the number of records to generate @return the RDD that contains the generated data

### Goal
The `gaussian` function generates a specified number of records that follow a Gaussian distribution, useful for simulating spatial data in geospatial analysis.

### Parameters
- `cardinality` (`Long`): The number of records to generate. This value should be a positive integer representing how many Gaussian-distributed points you want to create.

### Input
No specific data formats are required as input; however, the caller must ensure that the Spark context is properly initialized and running. The `cardinality` must be a valid positive long integer.

### Output
Returns `JavaSpatialRDD` — an RDD containing the generated Gaussian distributed spatial data points, which can be used for further geospatial analysis or visualization.

### Valid Call Patterns
```scala
sc.generateSpatialData
  .gaussian(1000)
```

### LLM Instruction Prompt
- When calling `gaussian`, ensure that the `cardinality` parameter is a positive long integer. The Spark context must be initialized and running.

### Prompt Snippet
```text
Generate Gaussian distributed spatial data with a specified number of records using the gaussian function.
```

### Common Failure Modes
- **[compile]** error: value rawSpatialRDD is not a member of edu.ucr.cs.bdlab.beast.JavaSpatialRDD _(seen 4x)_

### Fix Code Hint
```scala
// Ensure the cardinality is a positive integer
val points: JavaSpatialRDD = sc.generateSpatialData.gaussian(1000)
```

## API Test: `generate`
_Grounding: sibling-grounded — a tested method on the same class shows the pattern._

### Signature
```scala
def generate(cardinality: Long): JavaSpatialRDD
def generate(cardinality: Long): SpatialRDD
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/generator/JavaSpatialGeneratorBuilder.scala:87  (+1 more definition site/overload)_

_Source doc:_ Generate the data as an RDD. @param cardinality the number of records to generate @return the RDD that contains the generated data

### Goal
The `generate` function creates a distributed dataset (RDD) of spatial features based on the specified number of records, facilitating large-scale geospatial analysis.

### Parameters
- `cardinality` (`Long`): The number of spatial records to generate. This value should be a positive integer representing the desired size of the output dataset.

### Input
No specific data formats are required as input; however, the caller must ensure that the Spark context is properly initialized and that the environment is set up for executing RDPro operations.

### Output
Returns `JavaSpatialRDD` — a distributed collection of spatial features generated according to the specified cardinality. This output can be used for further geospatial analysis or processing within the RDPro framework.

### Valid Call Patterns
```scala
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
- When calling `generate`, ensure that the cardinality parameter is a positive long integer representing the number of records to generate. The Spark context must be initialized and ready for use.

### Prompt Snippet
```text
Generate a spatial dataset with a specified number of records using the generate function.
```

### Common Failure Modes
- **[compile]** error: value rawSpatialRDD is not a member of edu.ucr.cs.bdlab.beast.JavaSpatialRDD _(seen 3x)_
- **[compile]** error: value generate is not a member of org.apache.spark.SparkContext

### Fix Code Hint
```scala
// Ensure cardinality is a positive long integer
val cardinality: Long = 10000000 // Example of a valid cardinality
val randomData: JavaSpatialRDD = sc.generate(cardinality)
```

## API Test: `numPartitions`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def numPartitions(num: Int): JavaSpatialGeneratorBuilder
def numPartitions(num: Int): SpatialGeneratorBuilder
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/generator/JavaSpatialGeneratorBuilder.scala:66  (+1 more definition site/overload)_

_Source doc:_ Set the number of partitions in the output. If not set or set to zero, one partition will be generated for each one million records @param num the number of partitions in the generated RDD @return

### Goal
The `numPartitions` function sets the number of partitions for the output RDD in a distributed raster processing operation, optimizing performance for large-scale geospatial analysis.

### Parameters
- `num` (`Int`): The desired number of partitions for the output RDD. If set to zero or not specified, the default behavior generates one partition for every one million records.

### Input
The caller must provide a valid integer for `num`. The input must be part of a larger operation that generates an RDD, such as a spatial dataset created from raster data.

### Output
Returns `JavaSpatialGeneratorBuilder` — an object that allows further configuration of the spatial data generation process, enabling the user to specify additional parameters for the output RDD.

### Valid Call Patterns
```scala
val dataset = new RandomSpatialRDD(sparkContext, UniformDistribution, 16000, opts = Seq("maxSize" -> "0.1,0.1", "geometry" -> "box"))
val partitioner = IndexHelper.createPartitioner(dataset, classOf[GridPartitioner], NumPartitions(IndexHelper.Size, 1024 * 1024), { f: IFeature => 1024 }, new BeastOptions())
```

### LLM Instruction Prompt
- When calling `numPartitions`, ensure that the `num` parameter is a positive integer that reflects the desired number of partitions for the output RDD.

### Prompt Snippet
```text
Set the number of partitions for the output RDD using the numPartitions function, ensuring that the num parameter is a positive integer.
```

### Common Failure Modes
- **[compile]** error: value numPartitions is not a member of edu.ucr.cs.bdlab.beast.generator.RandomSpatialRDD _(seen 3x)_
- **[compile]** error: value numPartitions is not a member of org.apache.spark.rdd.RDD[edu.ucr.cs.bdlab.beast.geolite.ITile[Nothing]]

### Fix Code Hint
```scala
// Ensure that the num parameter is a positive integer
val numPartitionsValue = 16 // Example value
val builder = someSpatialGeneratorBuilder.numPartitions(numPartitionsValue)
```
