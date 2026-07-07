# BeastOptions

_Retrieve an integer value associated with a specified key, returning a default value if the key is not found._

**Receiver:** instance — obtain a `BeastOptions` value, then `<value>.<method>(...)`

**Members** (most robust first): ★ `getInt` **(primary)**, ★ `getLong`, ★ `setBoolean`, ★ `setLong`, ⚠️ `getBoolean`, ⚠️ `mergeWith`, ⚠️ `retainIndex`, ⚠️ `set`, ⚠️ `this`

---

## API Test: `getInt`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
override def getInt(i: Int): Int
def getInt(key: String, defaultValue: Int): Int
```
_Source: beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/common/BeastOptions.scala:98  (+1 more definition site/overload)_

_Source doc:_ Get a value of a key as integer @param key @param defaultValue @return

### Goal
Retrieve an integer value associated with a specified key, returning a default value if the key is not found.

### Parameters
- `key` (`String`): The key for which the integer value is to be retrieved. This should be a valid string that corresponds to a stored configuration or option.
- `defaultValue` (`Int`): The integer value to return if the specified key does not exist or is not associated with a valid integer.

### Input
The caller must provide a valid key as a string and a default integer value. There are no specific file formats required for this function, as it operates on in-memory key-value pairs.

### Output
Returns `Int` — the integer value associated with the specified key, or the provided default value if the key is not found.

### Valid Call Patterns
```scala
value.getInt("someKey", 42)
```

### LLM Instruction Prompt
- When calling `getInt`, ensure that the key is a valid string and the default value is an integer. The function should be called on an instance of the class that contains this method.

### Prompt Snippet
```text
Retrieve the integer value for the specified key, using a default if the key is absent.
```

### Common Failure Modes
- (no failures observed yet)

### Fix Code Hint
```scala
// Ensure the key is a valid string and the default value is an integer.
val value = someObject.getInt("myKey", 10)
```

## API Test: `getLong`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def getLong(key: String, defaultValue: Long): Long
```
_Source: beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/common/BeastOptions.scala:114_

_Source doc:_ Get a key value as long @param key @param defaultValue @return

### Goal
Retrieve a configuration value associated with a specified key as a `Long`, returning a default value if the key is not found.

### Parameters
- `key` (`String`): The name of the configuration key whose value is to be retrieved. Expected values are any valid string that corresponds to a configuration setting.
- `defaultValue` (`Long`): The value to return if the specified key does not exist. This should be a valid `Long` number.

### Input
The caller must provide a valid configuration key as a string and a default value of type `Long`. There are no specific file formats required for this function, as it operates on in-memory configuration settings.

### Output
Returns `Long` — the value associated with the specified key if it exists; otherwise, it returns the provided `defaultValue`.

### Valid Call Patterns
```scala
val value: Long = someObject.getLong("someKey", 42L)
```

### LLM Instruction Prompt
- When calling `getLong`, ensure that the `key` is a valid string representing a configuration setting and that `defaultValue` is a valid `Long` number.

### Prompt Snippet
```text
Retrieve the configuration value for the key "someKey" as a Long, using 42 as the default if the key is not found.
```

### Common Failure Modes
- **[runtime]** java.lang.IllegalArgumentException: requirement failed: default value was returned, indicating the key was not found _(seen 3x)_

### Fix Code Hint
```scala
// Ensure that the key is a non-empty string and defaultValue is a valid Long.
val value: Long = someObject.getLong("validKey", 0L)
```

## API Test: `setBoolean`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def setBoolean(key: String, value: Boolean): BeastOptions
```
_Source: beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/common/BeastOptions.scala:141_

_Source doc:_ Set key to a boolean value @param key @param value @return

### Goal
The `setBoolean` function sets a specified configuration key to a boolean value within the context of BeastOptions, allowing for the customization of behavior in raster processing tasks.

### Parameters
- `key` (`String`): The name of the configuration option to be set. This should correspond to a valid key recognized by the BeastOptions configuration system.
- `value` (`Boolean`): The boolean value to assign to the specified key. This can be either `true` or `false`, depending on the desired configuration.

### Input
The caller must provide a valid configuration key as a string and a boolean value. There are no specific file formats required for this operation, but the key must be recognized by the BeastOptions system.

### Output
Returns `BeastOptions` — an instance of BeastOptions that reflects the updated configuration with the specified key set to the provided boolean value.

### Valid Call Patterns
```scala
value.setBoolean("fs.file.impl.disable.cache", true)
```

### LLM Instruction Prompt
- Ensure that the key provided is a valid configuration option recognized by the BeastOptions system. The value must be a boolean (`true` or `false`).

### Prompt Snippet
```text
Set a configuration option in BeastOptions using setBoolean, ensuring the key is valid and the value is a boolean.
```

### Common Failure Modes
- (no failures observed yet)

### Fix Code Hint
```scala
// Ensure the key is a valid configuration option and the value is a boolean
val options = new BeastOptions().setBoolean("fs.file.impl.disable.cache", true)
```

## API Test: `setLong`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def setLong(key: String, value: Long): BeastOptions
```
_Source: beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/common/BeastOptions.scala:122_

_Source doc:_ Set a key to a long value @param key @param value @return

### Goal
`setLong` sets a specified configuration key to a long integer value within the context of BeastOptions, which is used for configuring various parameters in geospatial processing tasks.

### Parameters
- `key` (`String`): The name of the configuration parameter to be set. This should be a valid key recognized by the BeastOptions configuration system.
- `value` (`Long`): The long integer value to assign to the specified key. This value should be appropriate for the parameter being set.

### Input
The caller must provide a valid configuration key and a long integer value. The key must correspond to a parameter that can accept a long value within the BeastOptions context.

### Output
Returns `BeastOptions` — an instance of BeastOptions that has been updated with the new key-value pair, allowing subsequent operations to utilize the modified configuration.

### Valid Call Patterns
```scala
new BeastOptions().setLong("threshold", 0)
```

### LLM Instruction Prompt
- When calling `setLong`, ensure that the key is a valid configuration parameter and that the value is a long integer. The method should be called on an instance of `BeastOptions`.

### Prompt Snippet
```text
Set a configuration parameter in BeastOptions using setLong, ensuring the key is valid and the value is a long integer.
```

### Common Failure Modes
- (no failures observed yet)

### Fix Code Hint
```scala
// Ensure the key is valid and the value is of type Long
val options = new BeastOptions().setLong("maxSplitSize", 500L)
```

## API Test: `getBoolean`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def getBoolean(key: String, defaultValue: Boolean): Boolean
```
_Source: beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/common/BeastOptions.scala:133_

_Source doc:_ Get value as boolean @param key @param defaultValue @return

### Goal
Retrieve a boolean value associated with a specified key, returning a default value if the key is not found.

### Parameters
- `key` (`String`): The name of the option whose boolean value is to be retrieved. This should correspond to a valid option key defined in the command line arguments.
- `defaultValue` (`Boolean`): The value to return if the specified key does not exist. This allows the caller to specify a fallback boolean value.

### Input
The caller must provide a valid `key` that corresponds to an option defined in the command line arguments. The `defaultValue` should be a boolean indicating what to return if the key is not found.

### Output
Returns `Boolean` — the boolean value associated with the specified key if it exists; otherwise, it returns the provided `defaultValue`.

### Valid Call Patterns
```scala
val parsed = OperationHelper.parseCommandLineArguments("test", "path1", "option1:value1", "-option2", "-no-option3", "path2", "option4[0]:1", "-option4[1]")
assert(parsed.options.getBoolean("option2", defaultValue = false)) // returns false if "option2" is not present
assert(!parsed.options.getBoolean("option3", defaultValue = true)) // returns true if "option3" is not present
```

### LLM Instruction Prompt
- When calling `getBoolean`, ensure that the `key` corresponds to a valid command line option and provide a sensible `defaultValue` to handle cases where the key may not exist.

### Prompt Snippet
```text
Retrieve the boolean value for the specified option key, using a default value if the key is not found.
```

### Common Failure Modes
- **[runtime]** java.lang.NoClassDefFoundError: org/mortbay/jetty/handler/AbstractHandler _(seen 4x)_

### Fix Code Hint
```scala
// Ensure the key exists in the command line options or provide a meaningful default value.
val value = parsed.options.getBoolean("someOption", defaultValue = false)
```

## API Test: `mergeWith`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def mergeWith(another: VectorCanvas): VectorCanvas
def mergeWith(another: MemoryTileWindow[T]): Unit
def mergeWith(opts: BeastOptions): BeastOptions
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/VectorCanvas.scala:440  (+2 more definition site/overload)_

_Source doc:_ Merges this canvas with another vector canvas and returns this canvas after the merge. @param another the other canvas to merge with @return this canvas after the merge so that you can chain a number of mergeWidth operations.

### Goal
Merges the current `VectorCanvas` with another `VectorCanvas`, allowing for the combination of geometries from both canvases.

### Parameters
- `another` (`VectorCanvas`): The other vector canvas to merge with. It is expected to contain geometries that will be combined with the geometries of the current canvas.

### Input
The caller must provide two `VectorCanvas` instances that are compatible in terms of their geometries. The geometries should be defined within the same spatial reference system to ensure accurate merging.

### Output
Returns `VectorCanvas` — the resulting canvas after merging, which contains the combined geometries from both the current and the provided canvas.

### Valid Call Patterns
```scala
val canvas1 = new VectorCanvas(new Envelope(0, 256, 0, 256), 256, 256, 0, 1)
val canvas2 = new VectorCanvas(new Envelope(0, 256, 0, 256), 256, 256, 0, 1)
canvas1.mergeWith(canvas2)
```

### LLM Instruction Prompt
- When calling `mergeWith`, ensure that the `another` parameter is a valid `VectorCanvas` instance that contains geometries to be merged with the current canvas.

### Prompt Snippet
```text
To merge two vector canvases, use the mergeWith method on the first canvas, passing the second canvas as an argument.
```

### Common Failure Modes
- **[compile]** error: value getGeometryCount is not a member of edu.ucr.cs.bdlab.davinci.VectorCanvas _(seen 4x)_

### Fix Code Hint
```scala
Ensure both canvases have geometries defined in the same spatial reference system before calling mergeWith.
```

## API Test: `retainIndex`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def retainIndex(index: Int): BeastOptions
```
_Source: beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/common/BeastOptions.scala:168_

_Source doc:_ Keep only the parameters that do not have an index or the ones with the given index. In other words, remove any indexed parameter that have a different index than the one given. The index of the parameter is a suffix between square brackets, e.g., param[1] @param index the index to retain @return a new options with the given index retained

### Goal
`retainIndex` filters the parameters in `BeastOptions` to keep only those without an index or those that match the specified index, facilitating the management of options with multiple indexed values.

### Parameters
- `index` (`Int`): The index to retain. This should be a non-negative integer that corresponds to the suffix of the parameters you wish to keep (e.g., `1` to retain parameters like `key1[1]`).

### Input
The caller must provide a `BeastOptions` instance that may contain parameters with indexed suffixes (e.g., `key1[1]`, `key1[2]`). There are no specific file formats required, but the parameters should be set in the `BeastOptions` prior to calling `retainIndex`.

### Output
Returns `BeastOptions` — a new instance of `BeastOptions` that contains only the parameters that do not have an index or those that match the specified index. This allows for streamlined access to relevant options based on the index.

### Valid Call Patterns
```scala
val opts = new BeastOptions().set("key1[1]", "val1")
  .set("key1[2]", "val2")
  .set("key3", "val3")
  .set("key4[2]", "val4")
val opts1 = opts.retainIndex(1) // Retains parameters with index 1
val opts2 = opts.retainIndex(2) // Retains parameters with index 2
```

### LLM Instruction Prompt
- When calling `retainIndex`, ensure that the `index` parameter is a valid non-negative integer and that the `BeastOptions` instance contains parameters with indexed suffixes.

### Prompt Snippet
```text
To filter parameters in BeastOptions, use the retainIndex method with a valid index.
```

### Common Failure Modes
- **[compile]** error: value getAllKeys is not a member of edu.ucr.cs.bdlab.beast.common.BeastOptions _(seen 4x)_

### Fix Code Hint
```scala
// Ensure that BeastOptions is properly initialized and contains indexed parameters before calling retainIndex.
val opts = new BeastOptions().set("key1[1]", "val1").set("key1[2]", "val2")
val filteredOpts = opts.retainIndex(1) // This should work as expected.
```

## API Test: `set`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def set(key: String, value: Any): BeastOptions
```
_Source: beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/common/BeastOptions.scala:83_

_Source doc:_ Set a key to any value by converting it to string @param key key name @param value value @return

### Goal
The `set` function allows users to define configuration options by associating a string key with a corresponding value, which can be used in various geospatial processing tasks.

### Parameters
- `key` (`String`): The name of the configuration option to set. This should be a valid option recognized by the RDPro library, such as "iformat" or "separator".
- `value` (`Any`): The value to associate with the specified key. This can be any type, but it will be converted to a string for storage.

### Input
The caller must provide a valid key and value pair. The key should correspond to a recognized configuration option within the RDPro library, and the value should be appropriate for that key.

### Output
Returns `BeastOptions` — an instance of `BeastOptions` that contains the updated configuration settings, which can be used in subsequent operations within the RDPro framework.

### Valid Call Patterns
```scala
val opts = new BeastOptions().set("iformat", "wkt(Geometry)")
val optsWithSeparator = opts.set("separator", "\t")
```

### LLM Instruction Prompt
- When calling `set`, ensure that the key is a valid configuration option recognized by RDPro and that the value is appropriate for that key.

### Prompt Snippet
```text
Set the configuration option for input format to "wkt(Geometry)" and specify a tab as the separator.
```

### Common Failure Modes
- **[runtime]** java.lang.IllegalArgumentException: requirement failed: iformat not set correctly _(seen 4x)_

### Fix Code Hint
```scala
// Ensure the key is valid and the value is of a type that can be converted to a string.
val opts = new BeastOptions().set("validKey", "validValue")
```

## API Test: `this`
_Grounding: sibling-grounded — a tested method on the same class shows the pattern._

### Signature
```scala
def this(master: String, appName: String, sparkHome: String, jars: Array[String], environment: java.util.Map[String, String])
```
_Source: beast/beast-spark/src/main/scala/edu/ucr/cs/bdlab/beast/JavaSpatialSparkContext.scala:192  (+16 more definition site/overload)_

_Source doc:_ @param master Cluster URL to connect to (e.g. mesos://host:port, spark://host:port, local[4]). @param appName A name for your application, to display on the cluster web UI @param sparkHome The SPARK_HOME directory on the slave nodes @param jars Collection of JARs to send to the cluster. These can be paths on the local file system or HDFS, HTTP, HTTPS, or FTP URLs. @param environment Environment variables to set on worker nodes

### Goal
Initialize a Spark context for distributed raster processing in RDPro, enabling large-scale geospatial analysis.

### Parameters
- `master` (`String`): The URL of the cluster to connect to, which can be in formats such as `mesos://host:port`, `spark://host:port`, or `local[4]` for local execution.
- `appName` (`String`): A descriptive name for your application that will be displayed on the cluster's web UI, helping to identify the job.
- `sparkHome` (`String`): The path to the SPARK_HOME directory on the worker nodes, which is necessary for Spark to locate its resources.
- `jars` (`Array[String]`): An array of paths to JAR files that should be sent to the cluster. These can be local file system paths or URLs (HDFS, HTTP, HTTPS, or FTP).
- `environment` (`java.util.Map[String, String]`): A map of environment variables that will be set on the worker nodes, allowing for configuration of the execution environment.

### Input
The caller must provide a valid cluster URL, a unique application name, the path to the Spark installation on worker nodes, an array of JAR file paths, and a map of environment variables. Ensure that the Spark cluster is running and accessible.

### Output
Returns `unspecified` — this constructor initializes the Spark context but does not return a value. The context is used for subsequent operations in RDPro.

### Valid Call Patterns
```scala
val sparkContext = new RDPro(this.master, "MyGeospatialApp", "/path/to/spark", Array("path/to/jar1.jar", "path/to/jar2.jar"), new java.util.HashMap[String, String]())
```

### LLM Instruction Prompt
- When calling `this`, ensure that all parameters are provided with valid values according to the expected formats and types.

### Prompt Snippet
```text
Initialize the Spark context for distributed raster processing using the following parameters: master URL, application name, Spark home directory, JAR files, and environment variables.
```

### Common Failure Modes
- **[compile]** error: sparkContext is already defined as value sparkContext _(seen 4x)_

### Fix Code Hint
```scala
// Ensure that the master URL is correct and the Spark cluster is running
val sparkContext = new RDPro("spark://localhost:7077", "MyGeospatialApp", "/path/to/spark", Array("path/to/jar1.jar"), new java.util.HashMap[String, String]())
```
