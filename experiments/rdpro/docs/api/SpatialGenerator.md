# SpatialGenerator

_The `affineTransform` function applies an affine transformation matrix to spatial data, enabling geometric transformations such as scaling, translation, and…_

**Receiver:** instance — obtain a `SpatialGenerator` value, then `<value>.<method>(...)`

**Members** (most robust first): ⚠️ `affineTransform` **(primary)**, ⚠️ `normal`, ⚠️ `uniform`

---

## API Test: `affineTransform`
_Grounding: sibling-grounded — a tested method on the same class shows the pattern._

### Signature
```scala
def affineTransform(matrix: AffineTransform): SpatialGeneratorBuilder
def affineTransform(geometry: Geometry): Geometry
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/generator/SpatialGeneratorBuilder.scala:85  (+1 more definition site/overload)_

_Source doc:_ Sets the affine transformation for the generated data. @param matrix the affine transformation matrix @return

### Goal
The `affineTransform` function applies an affine transformation matrix to spatial data, enabling geometric transformations such as scaling, translation, and rotation.

### Parameters
- `matrix` (`AffineTransform`): An instance of the `AffineTransform` class that defines the transformation to be applied to the spatial data. This matrix can include operations like scaling, translating, and rotating the data.

### Input
The caller must provide an `AffineTransform` object that specifies the desired transformation. There are no specific file formats required for this operation, but the spatial data must be compatible with the transformation being applied.

### Output
Returns `SpatialGeneratorBuilder` — an object that allows further configuration and generation of spatial data based on the applied affine transformation.

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
- When calling `affineTransform`, ensure that the provided `matrix` is a valid `AffineTransform` instance that accurately represents the desired geometric transformation.

### Prompt Snippet
```text
To apply an affine transformation to your spatial data, create an instance of AffineTransform and configure it with the desired scaling, translation, or rotation. Then, call the affineTransform method on your spatial data generator.
```

### Common Failure Modes
- **[compile]** error: value nonEmpty is not a member of edu.ucr.cs.bdlab.beast.synopses.Summary _(seen 3x)_
- **[compile]** error: value affineTransform is not a member of org.locationtech.jts.geom.Geometry

### Fix Code Hint
```scala
Ensure that the AffineTransform object is properly initialized and configured before passing it to the affineTransform method. For example, check that you have set the scale and translation values as needed.
```

## API Test: `normal`
_Grounding: sibling-grounded — a tested method on the same class shows the pattern._

### Signature
```scala
def normal(mu: Double, sigma: Double): Double
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/generator/SpatialGenerator.scala:40_

_Source doc:_ Generate a random number in the range (-inf, +inf) from a normal distribution

### Goal
The `normal` function generates a random number from a normal distribution, which can be useful for simulating random processes in geospatial analysis.

### Parameters
- `mu` (`Double`): The mean of the normal distribution. This value represents the center of the distribution and can be any real number.
- `sigma` (`Double`): The standard deviation of the normal distribution. This value must be a positive number, representing the spread or width of the distribution.

### Input
The caller must provide two `Double` values: `mu` and `sigma`. There are no specific file formats required for this function, as it operates purely on numerical inputs.

### Output
Returns `Double` — a random number generated from the specified normal distribution characterized by the provided `mu` and `sigma`.

### Valid Call Patterns
```scala
val randomValue: Double = value.normal(0.0, 1.0) // Example call with mean 0 and standard deviation 1
```

### LLM Instruction Prompt
- When calling `normal`, ensure that `mu` is a valid `Double` representing the mean, and `sigma` is a positive `Double` representing the standard deviation.

### Prompt Snippet
```text
Generate a random number using the normal distribution with mean and standard deviation specified.
```

### Common Failure Modes
- **[compile]** error: not found: value normal _(seen 2x)_
- **[compile]** error: not found: value value
- **[compile]** error: value normal is not a member of object edu.ucr.cs.bdlab.beast.generator.SpatialGenerator

### Fix Code Hint
```scala
// Ensure sigma is positive
val mu: Double = 0.0
val sigma: Double = 1.0 // Must be positive
val randomValue: Double = value.normal(mu, sigma)
```

## API Test: `uniform`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def uniform(cardinality: Long): JavaSpatialRDD
def uniform(cardinality: Long): SpatialRDD
def uniform(a: Double, b: Double): Double
```
_Source: beast/io/src/main/scala/edu/ucr/cs/bdlab/beast/generator/SpatialGenerator.scala:37  (+2 more definition site/overload)_

_Source doc:_ Generate a random value in the range [a, b) from a uniform distribution

### Goal
The `uniform` function generates a random value from a uniform distribution within a specified range, which is useful for creating random spatial data in geospatial analysis.

### Parameters
- `a` (`Double`): The lower bound of the range (inclusive) from which the random value will be generated.
- `b` (`Double`): The upper bound of the range (exclusive) for the random value generation.

### Input
The caller must provide two `Double` values representing the range for the random number generation. There are no specific file formats required for this function, as it operates purely on numerical inputs.

### Output
Returns `Double` — a random value that lies within the range [a, b), generated from a uniform distribution.

### Valid Call Patterns
```scala
val randomValue: Double = sc.generateSpatialData.uniform(0.0, 1.0)
```

### LLM Instruction Prompt
- When calling `uniform`, ensure that the parameters `a` and `b` are both `Double` values, with `a` being less than `b` to avoid unexpected results.

### Prompt Snippet
```text
Generate a random value using the uniform distribution with specified bounds.
```

### Common Failure Modes
- **[compile]** error: too many arguments (2) for method uniform: (cardinality: Long)edu.ucr.cs.bdlab.beast.cg.SpatialDataTypes.SpatialRDD _(seen 4x)_

### Fix Code Hint
```scala
// Ensure that the lower bound is less than the upper bound
val randomValue: Double = sc.generateSpatialData.uniform(0.0, 1.0) // Correct usage
```
