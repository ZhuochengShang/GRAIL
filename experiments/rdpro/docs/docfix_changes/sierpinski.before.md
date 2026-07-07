## API Test: `sierpinski`

### Signature
```scala
def sierpinski(cardinality: Long): JavaSpatialRDD
def sierpinski(cardinality: Long): SpatialRDD
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/generator/JavaSpatialGeneratorBuilder.scala:127  (+1 more definition site/overload)_

_Source doc:_ Generate data from the Sierpinski distribution @param cardinality the number of records to generate @return the RDD that contains the generated data

### Goal
The `sierpinski` function generates a specified number of records from the Sierpinski distribution, which is useful for creating spatial datasets in geospatial analysis.

### Parameters
- `cardinality` (`Long`): The number of records to generate. This value should be a positive integer representing how many points from the Sierpinski distribution you want to create.

### Input
No specific data formats are required as input; however, the caller must ensure that the Spark context is properly initialized and running. The `cardinality` parameter must be a valid positive long integer.

### Output
Returns `JavaSpatialRDD` or `SpatialRDD` — an RDD containing the generated spatial data points from the Sierpinski distribution, which can be used for further geospatial analysis or visualization.

### Valid Call Patterns
```scala
sc.generateSpatialData
  .sierpinski(1000)
```

### LLM Instruction Prompt
- When calling `sierpinski`, ensure that the `cardinality` parameter is a positive long integer and that the Spark context is properly initialized.

### Prompt Snippet
```text
Generate 1000 records from the Sierpinski distribution using the following call: sc.generateSpatialData.sierpinski(1000).
```

### Common Failure Modes
- Providing a negative or zero value for `cardinality` will result in an error, as the function expects a positive integer.
- Attempting to call `sierpinski` without an initialized Spark context will lead to runtime exceptions.

### Fix Code Hint
```scala
// Ensure the Spark context is initialized and use a positive integer for cardinality
val spatialData: SpatialRDD = sc.generateSpatialData.sierpinski(1000)
```