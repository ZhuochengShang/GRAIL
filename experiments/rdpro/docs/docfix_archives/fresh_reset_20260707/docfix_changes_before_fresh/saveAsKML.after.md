## API Test: `saveAsKML`
_Grounding: doc-repaired from source (docfix)._

### Goal
Saves a distributed collection of geospatial features (`RDD[IFeature]`) to a single KML file. This is an extension method for Scala users, enabled by importing from `ReadWriteMixin`. The method takes a single string argument for the output file path and returns `Unit`.

### Valid Call Patterns|Valid Access Patterns
```scala
// Required imports for the extension method and types
import edu.ucr.cs.bdlab.beast.io.ReadWriteMixin._
import edu.ucr.cs.bdlab.beast.geolite.IFeature
import org.apache.spark.rdd.RDD

// Given an existing RDD of features
val featuresRDD: RDD[IFeature] = ??? // e.g., sc.shapefile("input.shp")
val outputPath: String = "/path/to/output/features.kml"

// Call the extension method directly on the RDD[IFeature]
featuresRDD.saveAsKML(outputPath)
```
- **Receiver:** `org.apache.spark.rdd.RDD[edu.ucr.cs.bdlab.beast.geolite.IFeature]`
- **Required Import:** `import edu.ucr.cs.bdlab.beast.io.ReadWriteMixin._` to enable the `.saveAsKML` extension method.

### LLM Instruction Prompt
Write Scala code to save an `RDD[IFeature]` to a KML file. You must first import `edu.ucr.cs.bdlab.beast.io.ReadWriteMixin._` to make the `.saveAsKML` extension method available. Call the method directly on the `RDD[IFeature]` instance, passing the output file path as a string. Do not use or reference `JavaSpatialRDD`.

### Prompt Snippet
To save an RDD of features to KML, import the extension methods from `ReadWriteMixin` and then call `.saveAsKML` directly on your `RDD[IFeature]`.

### Common Failure Modes
A compile error `value saveAsKML is not a member of org.apache.spark.rdd.RDD[...IFeature]` occurs if the required import `edu.ucr.cs.bdlab.beast.io.ReadWriteMixin._` is missing. Another compile error occurs if the code incorrectly attempts to wrap the RDD in `JavaSpatialRDD`, which is a class intended for the Java API and does not have the correct methods for this Scala pattern.

### Fix Code Hint
```scala
// WRONG: Wrapping in JavaSpatialRDD or forgetting the import
// val javaRDD = JavaSpatialRDD.create(featuresRDD) // Compile error: 'create' not found
// featuresRDD.saveAsKML(outputPath) // Compile error: method not found without import

// CORRECT: Import the extension methods and call directly on the RDD
import edu.ucr.cs.bdlab.beast.io.ReadWriteMixin._

featuresRDD.saveAsKML(outputPath)
```