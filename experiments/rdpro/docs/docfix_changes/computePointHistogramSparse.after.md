## API Test: `computePointHistogramSparse`
_Grounding: doc-repaired from source (docfix)._

### Goal
Compute a sparse point histogram from a `SpatialRDD` by assigning each feature to histogram buckets within an `EnvelopeNDLite` (MBB) and aggregating per-bucket values. This avoids moving the entire histogram during the reduce step for very large histograms.

### Valid Call Patterns
**Required Imports and Types:**
- `edu.ucr.cs.bdlab.beast.synopses.HistogramOP` (Object containing the method)
- `edu.ucr.cs.bdlab.beast.synopses.UniformHistogram` (Return type)
- `edu.ucr.cs.bdlab.beast.geolite.EnvelopeNDLite` (MBB type)
- `edu.ucr.cs.bdlab.beast.geolite.IFeature` (Input type for size function)
- `edu.ucr.cs.bdlab.beast.cg.SpatialRDD` (Input RDD type)

**Corrected Call Sketch:**
```scala
import edu.ucr.cs.bdlab.beast.synopses.HistogramOP
import edu.ucr.cs.bdlab.beast.synopses.UniformHistogram
import edu.ucr.cs.bdlab.beast.geolite.EnvelopeNDLite
import edu.ucr.cs.bdlab.beast.geolite.IFeature
import edu.ucr.cs.bdlab.beast.cg.SpatialRDD

// Assuming featuresRDD is an available RDD of features
val points: SpatialRDD = featuresRDD.asInstanceOf[SpatialRDD]
val mbr: EnvelopeNDLite = points.summary

// sizeFunction must be IFeature => Int
val h: UniformHistogram = HistogramOP.computePointHistogramSparse(points, (f: IFeature) => 1, mbr, 4)

// Witness extraction: verify result without calling parameterless getNumPartitions
val witness: Boolean = h != null
```

### LLM Instruction Prompt
- Call `computePointHistogramSparse` as a method on the `HistogramOP` object.
- Pass a `SpatialRDD` as the `features` argument.
- The `sizeFunction` parameter must be a function from `IFeature` to `Int` (e.g., `_ => 1`).
- Pass an `EnvelopeNDLite` for the `mbb` argument (typically `features.summary`).
- Provide bucket counts as `Int` varargs (e.g., `4`).
- **CRITICAL:** Do not query the returned `UniformHistogram` with `getNumPartitions` without arguments in the test witness. Use `h != null` or `h.toString` to verify the result.

### Prompt Snippet
```text
Given a SpatialRDD `points`, compute a sparse histogram using `HistogramOP.computePointHistogramSparse`.
- size function: `_ => 1` (must be IFeature => Int)
- histogram bounds: `points.summary` (EnvelopeNDLite)
- bucket count: `4`
Verify the result using `h != null`. Do not use `h.getNumPartitions`.
```

### Common Failure Modes
- **Missing Argument List on Witness Extraction:** Attempting to extract a witness using `h.getNumPartitions.toLong` on the returned `UniformHistogram` without providing the required argument list (either `()` or a dimension index), causing a compilation error.
- **Unqualified Method Call:** Calling a bare `computePointHistogramSparse(...)` instead of the required `HistogramOP.computePointHistogramSparse(...)`.
- **Invalid Size Function Type:** Passing a size function that does not match the required `IFeature => Int` signature.

### Fix Code Hint
```scala
// WRONG: Fails compilation due to missing arguments on getNumPartitions
val h = HistogramOP.computePointHistogramSparse(points, _ => 1, mbr, 4)
val witness = h.getNumPartitions.toLong

// CORRECT: Use h != null for witness extraction
val h: UniformHistogram = HistogramOP.computePointHistogramSparse(points, _ => 1, mbr, 4)
val witness: Boolean = h != null
```