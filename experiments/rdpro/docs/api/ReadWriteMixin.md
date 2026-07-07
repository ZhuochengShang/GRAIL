# ReadWriteMixin

_`generateSpatialData` generates a `SpatialRDD` containing randomly created geometries based on specified distribution types and parameters, facilitating…_

**Receiver:** instance — obtain a `ReadWriteMixin` value, then `<value>.<method>(...)`

**Members** (most robust first): ★ `generateSpatialData` **(primary)**

---

## API Test: `generateSpatialData`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def generateSpatialData(distribution: DistributionType, cardinality: Long, numPartitions: Int = 0, opts: BeastOptions = new BeastOptions) : SpatialRDD
def generateSpatialData: SpatialGeneratorBuilder
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/io/ReadWriteMixin.scala:139  (+1 more definition site/overload)_

_Source doc:_ Return a [[SpatialRDD]] of randomly generated geometries according to the given options. @param distribution the type of distribution {[[UniformDistribution]], [[DiagonalDistribution]], [[GaussianDistribution]], [[SierpinskiDistribution]], [[BitDistribution]], [[ParcelDistribution]]} @param cardinality the number of geometries to generate @param opts additional options depending on the type of generator @return an RDD with the generated geometries

### Goal
`generateSpatialData` generates a `SpatialRDD` containing randomly created geometries based on specified distribution types and parameters, facilitating spatial analysis in geospatial applications.

### Parameters
- `distribution` (`DistributionType`): Specifies the type of distribution for generating geometries. Expected values include `UniformDistribution`, `DiagonalDistribution`, `GaussianDistribution`, `SierpinskiDistribution`, `BitDistribution`, and `ParcelDistribution`.
- `cardinality` (`Long`): Indicates the number of geometries to generate. This value determines the size of the resulting `SpatialRDD`.
- `numPartitions` (`Int`), default `0`: Defines the number of partitions for the resulting `SpatialRDD`. If set to `0`, the default partitioning strategy will be used.
- `opts` (`BeastOptions`), default `new BeastOptions`: Additional options that can modify the behavior of the geometry generator, depending on the selected distribution type.

### Input
The caller must provide a valid `DistributionType`, a positive `cardinality` value, and optionally specify `numPartitions` and `opts`. The input must be compatible with the expected types and formats as defined in the API.

### Output
Returns `SpatialRDD` — a distributed collection of geometries generated according to the specified distribution and parameters, suitable for further spatial analysis and processing.

### Valid Call Patterns
```scala
val spatialData: SpatialRDD = sparkContext.generateSpatialData(UniformDistribution, 100, opts = Seq("seed" -> 1, UniformDistribution.MaxSize -> "0.1,0.1", "geometry" -> "box"))
```

### LLM Instruction Prompt
- When calling `generateSpatialData`, ensure that the `distribution` is one of the specified types, `cardinality` is a positive long integer, and `opts` are provided as key-value pairs where applicable.

### Prompt Snippet
```text
Generate a SpatialRDD using the specified distribution and cardinality, ensuring that options are correctly formatted.
```

### Common Failure Modes
- (no failures observed yet)

### Fix Code Hint
```scala
Ensure that the distribution is valid and that cardinality is a positive integer. Check the format of opts to match expected key-value pairs.
```
