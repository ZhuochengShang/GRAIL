# Glow — LLM_readme

LLM-facing API documentation. Generated from the API surface, project profile, and distilled docs.

## API Test: `add_struct_fields`

### Signature
```scala
def add_struct_fields(struct: Column, fields: Column*): Column
```
_Source: source/core/src/main/scala/io/projectglow/functions.scala:62_

_Source doc:_ Adds fields to a struct. @group complex_type_manipulation @since 0.3.0 @param struct The struct to which fields will be added @param fields The new fields to add. The arguments must alternate between string-typed literal field names and field values. @return A struct consisting of the input struct and the added fields

### Goal
Appends new fields to an existing Spark SQL Struct column, which is useful for enriching complex nested genomic data structures (such as variant annotations or genotype arrays) with additional computed metrics.

### Parameters
- `struct` (`Column`): The existing struct column to which new fields will be added.
- `fields` (`Column*`): A varargs sequence of columns representing the new fields to add. The arguments must strictly alternate between string-typed literal field names (e.g., `lit("new_field_name")`) and their corresponding field values.

### Input
A Spark DataFrame containing a `StructType` column. The caller must provide an even number of arguments to the `fields` varargs parameter, where every odd-indexed argument (1st, 3rd, 5th...) is a string literal representing the new field's name, and every even-indexed argument (2nd, 4th, 6th...) is the column expression for that field's value.

### Output
Returns `Column` — A new struct column consisting of all the original fields from the input struct, followed by the newly added fields.

### Valid Call Patterns
```scala
import io.projectglow.functions._
import org.apache.spark.sql.functions.{col, lit}

// Scala API usage
val added = df.select(
  add_struct_fields(
    col("inner"), 
    lit("number"), lit(1), 
    lit("string"), lit("blah")
  ).as("struct")
)

// SQL Expression usage
val value = spark.sql("""
  SELECT expand_struct(
    add_struct_fields(inner, 'three', cast(3.14159 as double), 'four', true)
  ) FROM my_table
""")
```

### LLM Instruction Prompt
- When calling `add_struct_fields`, you MUST ensure the `fields` varargs alternate exactly between string-typed literal field names (using `lit("name")` in Scala or `'name'` in SQL) and their corresponding values.
- Do not pass column references as the field names; they must be string literals.
- Always `import io.projectglow.functions._` to access this function in Scala.

### Prompt Snippet
```text
Use `io.projectglow.functions.add_struct_fields(structCol, lit("name1"), valCol1, lit("name2"), valCol2)` to append fields to a struct. The varargs must strictly alternate between string literal names and column values.
```

### Common Failure Modes
- **Odd number of `fields` arguments:** Failing to provide a matching value for every field name will cause a runtime error.
- **Non-literal field names:** Passing a dynamic column reference (e.g., `col("my_string_col")`) instead of a string literal (e.g., `lit("my_string_col")`) for the field name position will fail because Spark requires static names for struct fields during schema resolution.
- **Missing imports:** Forgetting `import io.projectglow.functions._` will result in a compilation error for `add_struct_fields`.

### Fix Code Hint
```scala
// WRONG: Missing `lit()` for the field name, or passing an odd number of arguments
val bad = df.select(add_struct_fields(col("genotypes"), "gq_mean", col("gq")))

// CORRECT: Use `lit()` for the field name, alternating name and value
import io.projectglow.functions._
import org.apache.spark.sql.functions.{col, lit}

val good = df.select(add_struct_fields(col("genotypes"), lit("gq_mean"), col("gq")))
```

## API Test: `array_quantile`

### Signature
```scala
def array_quantile(arr: Column, quantile: Double, is_sorted: Column): Column
def array_quantile(arr: Column, quantile: Double): Column
```
_Source: source/core/src/main/scala/io/projectglow/functions.scala:331  (+1 more definition site/overload)_

_Source doc:_ Array quantile @group quality_control @since 2.1.0 @param arr An array of numeric values @param quantile The desired quantile @param is_sorted If true, the input array is assumed to already be sorted @return

### Goal
Computes a specific quantile (e.g., median, 90th percentile) for an array of numeric values within a Spark DataFrame, commonly used for quality control statistics in genomic workflows.

### Parameters
- `arr` (`Column`): A Spark Column containing an array of numeric values (e.g., variant qualities, depths, or other metrics).
- `quantile` (`Double`): The desired quantile to compute, expressed as a fraction between 0.0 and 1.0 (e.g., `0.50` for the median, `0.99` for the 99th percentile).
- `is_sorted` (`Column`): A boolean Spark Column indicating whether the input array is already sorted. If true, the function skips sorting to improve performance.

### Input
A Spark DataFrame containing an array column of numeric types. If `is_sorted` is set to true, the caller must guarantee the array is sorted ascendingly; otherwise, the result will be incorrect.

### Output
Returns `Column` — A Spark Column containing the computed quantile value (as a Double) for each row's array.

### Valid Call Patterns
```scala
// Using Spark SQL expressions (as demonstrated in the test suite)
val glowUnsortedQuantiles = df.withColumns(
  Map(
    "glow_25" -> expr("array_quantile(arr, 0.25)"),
    "glow_50" -> expr("array_quantile(arr, 0.50)")
  )
)

// Using Spark SQL expressions with the is_sorted flag
df.selectExpr("array_quantile(arr, 1, true)")
df.selectExpr("array_quantile(arr, 1, false)")

// Using the Scala API directly (inferred from signature)
import org.apache.spark.sql.functions.{col, lit}
df.withColumn("median", array_quantile(col("arr"), 0.50))
df.withColumn("max_val", array_quantile(col("arr"), 1.0, lit(true)))
```

### LLM Instruction Prompt
- When computing quantiles on array columns in Glow, use the `array_quantile` function. Pass the array column, the quantile as a Double (0.0 to 1.0), and optionally a boolean column indicating if the array is sorted. It can be called via the Scala API or as a registered Spark SQL function using `expr("array_quantile(col_name, 0.50)")`.

### Prompt Snippet
```text
Use Glow's `array_quantile` to compute the 90th percentile of the numeric array column. If the array is known to be sorted, pass `lit(true)` (or `true` in SQL) to optimize execution.
```

### Common Failure Modes
- **Incorrect `is_sorted` flag:** Passing `true` for `is_sorted` when the array is not actually sorted ascendingly. As shown in the test suite, calling `array_quantile(arr, 1, true)` on the descending array `[4, 3, 2, 1]` incorrectly returns `1` instead of `4`.
- **Out-of-bounds quantile:** Providing a `quantile` value outside the valid range of 0.0 to 1.0.
- **Type mismatch:** Applying the function to a non-array or non-numeric column.

### Fix Code Hint
```scala
// If the array is unsorted, omit the is_sorted parameter or explicitly pass false
df.withColumn("median", expr("array_quantile(qualities, 0.50)"))

// If using the Scala API with the is_sorted flag, ensure it is passed as a Column
df.withColumn("median", array_quantile(col("qualities"), 0.50, lit(false)))
```

## API Test: `array_summary_stats`

### Signature
```scala
def array_summary_stats(arr: Column): Column
```
_Source: source/core/src/main/scala/io/projectglow/functions.scala:74_

_Source doc:_ Computes the minimum, maximum, mean, standard deviation for an array of numerics. @group complex_type_manipulation @since 0.3.0 @param arr An array of any numeric type @return A struct containing double ``mean``, ``stdDev``, ``min``, and ``max`` fields

### Goal
Computes summary statistics (minimum, maximum, mean, and standard deviation) for a Spark Column containing an array of numeric values, commonly used for variant or sample quality control metrics.

### Parameters
- `arr` (`Column`): A Spark Column representing an array of any numeric type (e.g., integers or doubles).

### Input
A Spark DataFrame containing a column with an array of numeric values (such as genotype qualities, read depths, or other array-based genomic metrics). The input column must be of an array type containing numerics. If the array is empty, the function will process it without error but return nulls for all statistic fields.

### Output
Returns `Column` — A struct column containing four `double` fields: `mean`, `stdDev`, `min`, and `max`. If the input array is empty, all four fields in the resulting struct will be null.

### Valid Call Patterns
```scala
// 1. SQL Expression form (Authoritative - from test suite)
val statsDf = df.selectExpr("expand_struct(array_summary_stats(numbers))")

// 2. Scala Column API form (Inferred from signature)
import io.projectglow.functions.array_summary_stats
import org.apache.spark.sql.functions.col

val statsDf = df.select(array_summary_stats(col("numbers")).as("stats"))
```

### LLM Instruction Prompt
- Use `array_summary_stats` to calculate the minimum, maximum, mean, and standard deviation of numeric arrays in a Spark DataFrame.
- Expect the return type to be a struct with `double` fields: `mean`, `stdDev`, `min`, and `max`.
- To flatten the resulting struct into separate columns, wrap the call in the `expand_struct` SQL function (e.g., `selectExpr("expand_struct(array_summary_stats(my_array))")`) or access fields via dot notation (e.g., `col("stats.mean")`).
- Account for empty arrays, which safely evaluate to a struct where all fields (`mean`, `stdDev`, `min`, `max`) are null.

### Prompt Snippet
```text
Glow's `array_summary_stats(arr: Column)` computes stats for numeric arrays. It returns a struct with `double` fields: `mean`, `stdDev`, `min`, and `max`. Empty arrays yield a struct of nulls. You can flatten the struct using Glow's `expand_struct` in a `selectExpr`.
```

### Common Failure Modes
- **Type Mismatch:** Passing a column that is not an array, or an array of non-numeric types (like strings or structs), will result in a Spark SQL AnalysisException during query planning.
- **Null Pointer Exceptions in Downstream Code:** Failing to account for null values in the output struct when the input array is empty (e.g., calling `.get` on an `Option` in Scala Dataset mapping without checking for `None`).

### Fix Code Hint
```scala
// If you need to handle empty arrays safely in strongly-typed Datasets:
case class ArraySummaryStats(mean: Option[Double], stdDev: Option[Double], min: Option[Double], max: Option[Double])

// Use expand_struct to flatten the struct fields into top-level columns
val stats = df
  .selectExpr("expand_struct(array_summary_stats(numbers))")
  .as[ArraySummaryStats]
  .head
```

## API Test: `array_to_dense_vector`

### Signature
```scala
def array_to_dense_vector(arr: Column): Column
```
_Source: source/core/src/main/scala/io/projectglow/functions.scala:86_

_Source doc:_ Converts an array of numerics into a ``spark.ml`` ``DenseVector``. @group complex_type_manipulation @since 0.3.0 @param arr The array of numerics @return A ``spark.ml`` ``DenseVector``

### Goal
Converts a Spark SQL array of numeric values into a `spark.ml` `DenseVector`, bridging genomic data transformations with Spark MLlib algorithms for downstream tasks like population stratification.

### Parameters
- `arr` (`Column`): A Spark DataFrame column containing an array of numeric values (e.g., `ArrayType(DoubleType)` or `ArrayType(IntegerType)`).

### Input
A Spark DataFrame containing a column of numeric arrays. This is typically required after extracting numeric features from genomic data (such as allele counts or genotype states) to prepare the dataset for machine learning pipelines that require Spark ML vector types.

### Output
Returns `Column` — A column containing a `spark.ml` `DenseVector` representation of the input numeric array, compatible with Spark MLlib estimators and transformers.

### Valid Call Patterns
```scala
// Inferred from sibling functions `genotype_states` and `lift_over_coordinates`
import org.apache.spark.sql.functions.col

// Assuming df contains a column "numeric_array" of type ArrayType(DoubleType)
val vectorizedDf = df.select(
  array_to_dense_vector(col("numeric_array")).as("features")
)
```

### LLM Instruction Prompt
- Use `array_to_dense_vector` when you need to pass genomic array data into Spark MLlib algorithms (e.g., PCA or logistic regression for genome-wide association studies).
- Ensure the input column is strictly an array of numerics; do not pass raw complex structs (like the raw VCF `genotypes` array) without first extracting numeric values (e.g., using `genotype_states`).
- Call this function as a bare function `array_to_dense_vector(col("..."))` mirroring other Glow SQL functions.

### Prompt Snippet
```text
To integrate Glow genomic data with Spark MLlib, extract numeric features into an array column, then convert it to a vector using `array_to_dense_vector(col("my_numeric_array"))`.
```

### Common Failure Modes
- **Type Mismatch:** Passing a column that is not an array, or an array containing non-numeric types (like Strings or Structs). This will cause a Spark SQL analysis exception at runtime.
- **Raw Genotypes Error:** Attempting to pass the raw `genotypes` column directly from a loaded VCF. The `genotypes` column is an array of structs, not numerics. It must first be transformed (e.g., using `genotype_states`) before vectorization.

### Fix Code Hint
```scala
// BAD: Passing raw genotypes struct array directly
// df.select(array_to_dense_vector(col("genotypes")))

// GOOD: Extract numeric states first, then convert to DenseVector
df.select(
  array_to_dense_vector(genotype_states(col("genotypes"))).as("features")
)
```

## API Test: `array_to_sparse_vector`

### Signature
```scala
def array_to_sparse_vector(arr: Column): Column
```
_Source: source/core/src/main/scala/io/projectglow/functions.scala:98_

_Source doc:_ Converts an array of numerics into a ``spark.ml`` ``SparseVector``. @group complex_type_manipulation @since 0.3.0 @param arr The array of numerics @return A ``spark.ml`` ``SparseVector``

### Goal
Converts a Spark SQL array of numeric values (such as genotype dosages or variant QC metrics) into a `spark.ml.linalg.SparseVector` to enable downstream machine learning tasks like population stratification via Spark MLlib.

### Parameters
- `arr` (`Column`): A Spark `Column` containing an array of numeric values (e.g., integers or doubles) that will be converted into a sparse vector.

### Input
A Spark DataFrame containing an array column. The elements of the array must be of a numeric type (e.g., `ArrayType(IntegerType)` or `ArrayType(DoubleType)`). If the array contains non-numeric types (like strings), it must be explicitly cast to a numeric array first.

### Output
Returns `Column` — A column containing a `spark.ml` `SparseVector` (internally represented as a `VectorUDT`), where the array indices become the vector indices and the array elements are cast to `Double` values.

### Valid Call Patterns
```scala
// 1. SQL Expression (Authoritative from test suite)
df.selectExpr("array_to_sparse_vector(cast(array(1, 2, 3) as array<int>)) as features")

// 2. Scala Column API (Inferred from signature)
import io.projectglow.functions.array_to_sparse_vector
import org.apache.spark.sql.functions.col

df.select(array_to_sparse_vector(col("numeric_array")).alias("features"))
```

### LLM Instruction Prompt
- When preparing genomic data for Spark MLlib algorithms (e.g., PCA for population stratification), use Glow's `array_to_sparse_vector` to convert arrays of numeric values into `SparseVector` columns. Ensure the input array is explicitly cast to a numeric array type (like `array<int>` or `array<double>`) if it is not already numeric.

### Prompt Snippet
```text
Convert the array of genotype dosages into a Spark ML SparseVector using Glow's `array_to_sparse_vector` function so it can be used as features in MLlib PCA. Ensure the input is cast to an array of integers first.
```

### Common Failure Modes
- **Type Mismatch AnalysisException:** Passing an array of strings or structs instead of numerics. Spark will fail to resolve the function or throw a runtime error during vector conversion.
- **Missing SQL Registration:** Attempting to use `array_to_sparse_vector` in `selectExpr` without properly initializing the Glow Spark session extensions, resulting in an "Undefined function" error.
- **Dense vs Sparse Misunderstanding:** Assuming the output is a `DenseVector`. The function explicitly creates a `SparseVector`, which is highly efficient for genomic data containing many zero values (e.g., homozygous reference calls), but may behave differently if a specific MLlib algorithm strictly requires dense vectors.

### Fix Code Hint
```scala
// If the input array is not strictly numeric, cast it before conversion
df.selectExpr("array_to_sparse_vector(cast(genotype_calls as array<double>)) as features")

// Or using the Scala API:
df.select(array_to_sparse_vector(col("genotype_calls").cast("array<double>")).alias("features"))
```

## API Test: `calculateIntProbabilities`

### Signature
```scala
def calculateIntProbabilities(bitsPerProb: Int, probabilities: Seq[Double]): Seq[Long]
```
_Source: source/core/src/main/scala/io/projectglow/bgen/BgenRecordWriter.scala:339_

_Source doc:_ Given a vector v = (v_1, ... v_d) of d probabilities that sum to one, we find the integer representation (where each int is stored in B bits) as follows: - Multiply v by 2**B-1. - Compute the total fractional part F = sum_i (v_i - floor(v_i)). - Form x by rounding the F entries of v with the largest fractional parts up to the nearest integer, and the other d-F entries down to the nearest smaller integer.

### Goal
Converts a sequence of floating-point genotype probabilities into an exact integer representation of a specified bit depth, typically used for encoding and writing BGEN format files.

### Parameters
- `bitsPerProb` (`Int`): The number of bits $B$ used to store each probability (e.g., 8, 16, or 32).
- `probabilities` (`Seq[Double]`): A sequence of double-precision probabilities $v = (v_1, ... v_d)$ that must sum to exactly one.

### Input
The caller must provide a valid bit depth (typically 8, 16, or 32 for BGEN encoding) and a sequence of `Double` values representing genotype probabilities. The probabilities must sum to exactly 1.0 to satisfy the mathematical assumptions of the fractional rounding algorithm.

### Output
Returns `Seq[Long]` — The integer representations of the probabilities scaled by $2^B - 1$. The fractional parts are carefully rounded up or down such that the sum of the resulting integers exactly equals $2^B - 1$.

### Valid Call Patterns
```scala
import io.projectglow.bgen.BgenRecordWriter

// 8-bit encoding
val intProbs8 = BgenRecordWriter.calculateIntProbabilities(bitsPerProb = 8, Seq(0.99, 0.01))
// Returns: Seq(252, 3)

// 16-bit encoding
val intProbs16 = BgenRecordWriter.calculateIntProbabilities(bitsPerProb = 16, Seq(0.605, 0.283, 0.122))
// Returns: Seq(39649, 18547, 7995)

// 32-bit encoding
val intProbs32 = BgenRecordWriter.calculateIntProbabilities(bitsPerProb = 32, Seq(0.23, 0.27, 0.16, 0.34))
// Returns: Seq(987842478, 1159641170, 687194767, 1460288881)
```

### LLM Instruction Prompt
- When encoding genotype probabilities for BGEN files in Glow, use `BgenRecordWriter.calculateIntProbabilities(bitsPerProb, probabilities)`. Ensure the input `probabilities` sequence sums to exactly 1.0. Do not call this function without the `BgenRecordWriter` object qualifier.

### Prompt Snippet
```text
Glow BGEN probability encoding: Use `BgenRecordWriter.calculateIntProbabilities(bits: Int, probs: Seq[Double]): Seq[Long]`. The `probs` must sum to 1.0. The function scales the probabilities by 2^B - 1 and distributes the fractional remainders to ensure an exact integer sum.
```

### Common Failure Modes
- **Missing Object Qualifier:** Calling a bare `calculateIntProbabilities(...)` will fail to compile. It must be called on the `BgenRecordWriter` object.
- **Probabilities Do Not Sum to 1:** If the input `Seq[Double]` does not sum to exactly 1.0, the fractional rounding logic will produce an invalid integer representation that does not sum to $2^B - 1$, corrupting the BGEN encoding.
- **Incorrect Bit Depth:** Providing a `bitsPerProb` that does not match the target BGEN specification (usually 8, 16, or 32) will result in incorrectly scaled integers.

### Fix Code Hint
```scala
// BAD: Bare function call and probabilities don't sum to 1
val badProbs = calculateIntProbabilities(16, Seq(0.5, 0.4))

// GOOD: Qualified call with probabilities summing to 1.0
import io.projectglow.bgen.BgenRecordWriter
val goodProbs = BgenRecordWriter.calculateIntProbabilities(16, Seq(0.5, 0.4, 0.1))
```

## API Test: `call_summary_stats`

### Signature
```scala
def call_summary_stats(genotypes: Column): Column
```
_Source: source/core/src/main/scala/io/projectglow/functions.scala:243_

_Source doc:_ Computes call summary statistics for an array of genotype structs. See :ref:`variant-qc` for more details. @group quality_control @since 0.3.0 @param genotypes The array of genotype structs with ``calls`` field @return A struct containing ``callRate``, ``nCalled``, ``nUncalled``, ``nHet``, ``nHomozygous``, ``nNonRef``, ``nAllelesCalled``, ``alleleCounts``, ``alleleFrequencies`` fields. See :ref:`variant-qc`.

### Goal
Computes variant-level quality control summary statistics (such as call rate, allele frequencies, and heterozygosity counts) for an array of genotype structs in a genomic Spark DataFrame.

### Parameters
- `genotypes` (`Column`): The column containing an array of genotype structs. These structs must include a `calls` field (typically generated automatically when reading VCF, BGEN, or Plink files into Glow).

### Input
A Spark DataFrame containing genomic variant data. The target column must be an array of structs representing sample genotypes, and each struct must contain a `calls` field (an array of integers representing the called alleles). This schema is standard when loading genomic files via Glow's `spark.read.format("vcf").load(...)`.

### Output
Returns `Column` — A single struct column containing the computed quality control metrics: `callRate` (Double), `nCalled` (Long), `nUncalled` (Long), `nHet` (Long), `nHomozygous` (Long), `nNonRef` (Long), `nAllelesCalled` (Long), `alleleCounts` (Array[Long]), and `alleleFrequencies` (Array[Double]).

### Valid Call Patterns
```scala
// 1. Using Spark SQL expressions (as demonstrated in the project test suite)
// Note: expand_struct is a Glow SQL function used to flatten the resulting struct
val statsDf = spark.read.format("vcf").load(testVcf)
  .selectExpr(
    "contigName", 
    "start", 
    "expand_struct(call_summary_stats(genotypes))"
  )

// 2. Using the Scala Column API directly
import io.projectglow.functions.call_summary_stats
import org.apache.spark.sql.functions.col

val statsDfScala = df.select(
  col("contigName"),
  col("start"),
  call_summary_stats(col("genotypes")).as("stats")
)
```

### LLM Instruction Prompt
- When performing variant quality control (Variant QC) in Glow, use `call_summary_stats` to calculate standard metrics like call rate and allele frequencies.
- Pass the `genotypes` column as the argument.
- The function returns a nested struct. To flatten these metrics into top-level DataFrame columns, wrap the call in Glow's `expand_struct` SQL function via `selectExpr`, or use Spark's `.*` struct expansion in the DataFrame API.
- Do not invent individual functions for `callRate` or `alleleFrequencies`; they are all computed together and returned inside this single struct.

### Prompt Snippet
```text
Glow `call_summary_stats(genotypes: Column): Column` computes Variant QC metrics. Input: array of genotype structs with a `calls` field. Output: a struct column with `callRate`, `nCalled`, `nUncalled`, `nHet`, `nHomozygous`, `nNonRef`, `nAllelesCalled`, `alleleCounts`, `alleleFrequencies`. Use `expand_struct(call_summary_stats(genotypes))` in `selectExpr` to flatten the output struct into individual columns.
```

### Common Failure Modes
- **Missing `calls` field:** Passing an array of structs that does not contain a `calls` field will cause a Spark analysis exception. Ensure the data was loaded using Glow's genomic data sources (VCF/BGEN/Plink).
- **Nested Struct Querying Errors:** Forgetting that the return type is a single struct column. If you do not expand or alias the struct, attempting to filter directly on metrics like `callRate` will fail because the column is nested (e.g., it must be accessed as `stats.callRate` if aliased as `stats`).

### Fix Code Hint
```scala
// BAD: Attempting to select fields that are trapped inside the unexpanded struct
df.selectExpr("call_summary_stats(genotypes)")
  .filter("callRate > 0.9") // Fails: callRate is not a top-level column

// GOOD: Use expand_struct to flatten the struct into top-level columns
df.selectExpr("expand_struct(call_summary_stats(genotypes))")
  .filter("callRate > 0.9") // Succeeds
```

## API Test: `columnToExpr`

### Signature
```scala
def columnToExpr(col: Column): Expression
```
_Source: source/core/src/main/scala/org/apache/spark/sql/SQLUtils.scala:29_

_Source doc:_ Extract the Catalyst Expression from a Column. Needed because Column.expr is private[sql] in Spark 4.

### Goal
Extract the underlying Spark Catalyst `Expression` from a Spark DataFrame `Column`, providing a compatibility layer for custom genomic expressions in Spark 4 where direct access is restricted.

### Parameters
- `col` (`Column`): The Spark SQL `Column` object (e.g., a literal, a column reference, or a function result) from which to extract the internal Catalyst expression.

### Input
A valid Apache Spark SQL `Column` instance. This is typically generated using standard Spark SQL functions like `lit()`, `col()`, or by wrapping an existing Catalyst expression via `SQLUtils.exprToColumn`.

### Output
Returns `Expression` — The internal Spark Catalyst `Expression` tree that represents the computation or data reference defined by the input column.

### Valid Call Patterns
```scala
import org.apache.spark.sql.functions.lit

// Extracting an expression from a literal column
val expr = SQLUtils.columnToExpr(lit(7))

// Round-tripping an expression through a column
val roundTripped = SQLUtils.columnToExpr(SQLUtils.exprToColumn(expr))
```

### LLM Instruction Prompt
- When extracting a Catalyst `Expression` from a Spark `Column` in Glow, ALWAYS use `SQLUtils.columnToExpr(col)`.
- NEVER call `col.expr` directly, as this property is `private[sql]` in Spark 4 and will cause compilation failures in environments using newer Spark versions.
- Ensure the receiver is `SQLUtils` as demonstrated in the project's test suite.

### Prompt Snippet
```text
To extract a Catalyst Expression from a Spark Column in Glow, use `SQLUtils.columnToExpr(col)`. Do not use `col.expr`, which breaks Spark 4 compatibility because it is private[sql].
```

### Common Failure Modes
- **Directly accessing `col.expr`:** Attempting to read the expression directly from the column object will fail to compile in Spark 4 environments due to `private[sql]` access restrictions.
- **Missing `SQLUtils` qualifier:** Calling `columnToExpr(col)` without the `SQLUtils` object qualifier will result in a "not found" compilation error.

### Fix Code Hint
```scala
// BAD: Fails to compile in Spark 4
val myExpr = myColumn.expr

// GOOD: Uses Glow's compatibility shim
val myExpr = SQLUtils.columnToExpr(myColumn)
```

## API Test: `convert`

### Signature
```scala
def convert(line: Text): InternalRow
def convert(row: InternalRow): Option[VariantContext]
def convert(row: InternalRow): BgenRow
```
_Source: source/core/src/main/scala/io/projectglow/vcf/VCFLineToInternalRowConverter.scala:130  (+2 more definition site/overload)_

_Source doc:_ Converts a VCF line into an [[InternalRow]] @param line A text object containing the VCF line @return The converted row or null to represent a parsing failure or filtered row

### Goal
Converts genomic data records between raw text formats (like VCF lines), Spark SQL `InternalRow` representations, and specialized genomic types (like `BgenRow` or HTSJDK `VariantContext`).

### Parameters
- `line` (`Text`): A Hadoop `Text` object containing a single raw VCF line to be parsed. *(Note: Overloads accept `row: InternalRow` representing a parsed variant record).*

### Input
Requires an instantiated converter object (e.g., `VCFLineToInternalRowConverter`, `InternalRowToVariantContextConverter`, or `InternalRowToBgenRowConverter`). The input data must be a valid Hadoop `Text` VCF line or a Spark `InternalRow` that strictly conforms to the schema provided during the converter's initialization. Converters are typically used on the underlying RDD of a Spark DataFrame.

### Output
Returns `InternalRow` — A Spark SQL internal row representing the parsed VCF variant. Note that this specific overload returns `null` to represent a parsing failure or a filtered row. Overloads return a `BgenRow` or an `Option[VariantContext]`.

### Valid Call Patterns
```scala
// Converting InternalRow to VariantContext inside mapPartitions
val vc = df.queryExecution.toRdd.mapPartitions { it =>
  val header = VCFSchemaInferrer.headerLinesFromSchema(schema)
  val converter = new InternalRowToVariantContextConverter(
    schema,
    header.toSet,
    ValidationStringency.STRICT
  )
  it.flatMap(converter.convert)
}.first()

// Converting InternalRow to BgenRow
val converter = new InternalRowToBgenRowConverter(BgenRow.schema, 10, 2, false)
val bgenRow = converter.convert(internalRow)
```

### LLM Instruction Prompt
- When generating code to convert Spark DataFrames to specific genomic types (like `VariantContext` or `BgenRow`), instantiate the specific converter class (e.g., `InternalRowToVariantContextConverter`) and call `.convert()` on the `InternalRow`. 
- Ensure this is done within RDD operations like `mapPartitions` because converter instances are stateful and should be instantiated per partition. 
- Handle `null` returns explicitly when converting from `Text` to `InternalRow`, as it does not return an `Option`.

### Prompt Snippet
```text
Instantiate a converter (e.g., InternalRowToVariantContextConverter) inside an RDD `mapPartitions` block and call `converter.convert(row)` on each `InternalRow`.
```

### Common Failure Modes
- **Mixed Phasing in BGEN:** Calling `convert` on an `InternalRow` containing mixed phasing for BGEN data throws an `IllegalStateException`.
- **Serialization Errors:** Attempting to instantiate a converter outside of a `mapPartitions` block and passing it into a closure will cause Spark task serialization failures.
- **NullPointerExceptions:** Failing to check for `null` return values when using the `Text` to `InternalRow` overload (which returns `null` on parsing failures instead of throwing or returning an `Option`).

### Fix Code Hint
```scala
// Wrap converter usage in mapPartitions to avoid Spark serialization issues
df.queryExecution.toRdd.mapPartitions { iter =>
  // Instantiate converter inside the partition closure
  val converter = new InternalRowToVariantContextConverter(schema, header, ValidationStringency.STRICT)
  iter.flatMap(row => converter.convert(row))
}
```

## API Test: `createVCFCodec`

### Signature
```scala
def createVCFCodec(path: URI, conf: Configuration): (VCFHeader, VCFCodec)
```
_Source: source/core/src/main/scala/io/projectglow/vcf/VCFFileFormat.scala:251_

_Source doc:_ Reads the header of a VCF file to generate an object representing the information in the header and a derived [[VCFCodec]] that can parse the rest of the file. The logic to parse the header is adapted from [[org.seqdoop.hadoop_bam.VCFRecordReader]].

### Goal
Reads the header of a Variant Call Format (VCF) file to extract its metadata and initializes a codec capable of parsing the remaining genomic variant records.

### Parameters
- `path` (`URI`): The `java.net.URI` pointing to the location of the VCF file to be read.
- `conf` (`Configuration`): The Hadoop `Configuration` object required to access the file system where the VCF resides.

### Input
A valid `java.net.URI` pointing to an accessible VCF file and a valid Hadoop `Configuration` (typically extracted from the active `SparkSession`). The target file must be a properly formatted VCF so that the header logic (adapted from `org.seqdoop.hadoop_bam.VCFRecordReader`) can successfully parse the metadata.

### Output
Returns `(VCFHeader, VCFCodec)` — A Scala Tuple2 where the first element is the parsed `VCFHeader` containing the file's metadata (e.g., format lines, sample names, contigs), and the second element is the `VCFCodec` initialized to parse the variant records in the remainder of the file.

### Valid Call Patterns
```scala
import java.net.URI
import io.projectglow.vcf.VCFFileFormat

// Assuming `spark` is an active SparkSession and `vcfPath` is a string path
val (header, codec) = VCFFileFormat.createVCFCodec(
  new URI(vcfPath), 
  spark.sessionState.newHadoopConf()
)

// The header can then be used to inspect VCF metadata, e.g.:
// val formatLines = header.getFormatHeaderLines
```

### LLM Instruction Prompt
- Always call this method on the `VCFFileFormat` object: `VCFFileFormat.createVCFCodec(...)`.
- You MUST convert string file paths to `java.net.URI` before passing them to the `path` parameter.
- You MUST provide a Hadoop `Configuration` object. The standard way to obtain this in a Spark environment is via `spark.sessionState.newHadoopConf()`.
- Expect a tuple `(VCFHeader, VCFCodec)` as the return type.

### Prompt Snippet
```text
To manually parse a VCF header and initialize a codec in Glow, use `io.projectglow.vcf.VCFFileFormat.createVCFCodec`. Pass the file path as a `java.net.URI` and provide the Hadoop configuration from the Spark session using `spark.sessionState.newHadoopConf()`.
```

### Common Failure Modes
- **Type Mismatch on `path`:** Passing a plain `String` instead of a `java.net.URI`. This will cause a compilation error.
- **Missing Hadoop Configuration:** Attempting to pass `null` or an uninitialized configuration, which will cause file system resolution to fail when reading the VCF.
- **Invalid VCF Format:** Pointing the URI to a file that is not a valid VCF (e.g., a BGEN or Plink file), causing the underlying `VCFRecordReader` logic to fail during header extraction.

### Fix Code Hint
```scala
// Incorrect: Passing a string path directly
// val (header, codec) = VCFFileFormat.createVCFCodec("/path/to/variants.vcf", conf)

// Correct: Wrapping the path in a java.net.URI and extracting the Hadoop conf from Spark
val (header, codec) = VCFFileFormat.createVCFCodec(
  new java.net.URI("/path/to/variants.vcf"),
  spark.sessionState.newHadoopConf()
)
```

