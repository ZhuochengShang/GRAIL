# OperationHelper

_`checkOptions` validates the user-provided command line options to ensure that all required options are present and no unexpected options are included._

**Receiver:** static object — call `OperationHelper.<method>(...)`

**Members** (most robust first): ⚠️ `checkOptions` **(primary)**, ⚠️ `getOperationParams`, ⚠️ `printOperationUsage`, ⚠️ `readConfigurationXML`

---

## API Test: `checkOptions`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def checkOptions(options: ParsedCommandLineOptions, out: PrintStream): Boolean
```
_Source: beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/util/OperationHelper.scala:293_

_Source doc:_ Check if the user options are valid. This means that the user did not add any unexpected options or leave out any required option @param options parsed command line options. @return

### Goal
`checkOptions` validates the user-provided command line options to ensure that all required options are present and no unexpected options are included.

### Parameters
- `options` (`ParsedCommandLineOptions`): Represents the parsed command line options provided by the user. This includes both required and optional parameters that the user intends to use in the RDPro operations.
- `out` (`PrintStream`): A stream to which output messages can be printed, typically used for logging or displaying error messages related to the validation of options.

### Input
The caller must provide a valid instance of `ParsedCommandLineOptions` that contains the command line arguments parsed from user input. The input must conform to the expected structure defined by the RDPro application, including all required parameters.

### Output
Returns `Boolean` — `true` if the provided options are valid (i.e., all required options are present and no unexpected options are included), and `false` otherwise.

### Valid Call Patterns
```scala
// Example of checking user options with a PrintStream for output
val commandLineOptions = OperationHelper.parseCommandLineArguments("test", "path1", "option1:value1", "-option2", "-no-option3", "path2", "option4[0]:1", "-option4[1]")
assert(!OperationHelper.checkOptions(commandLineOptions, new PrintStream(new NullOutputStream)))

// Example of valid options
val parsedOptions2 = OperationHelper.parseCommandLineArguments("subtest1", "path1", "sparam2:1", "-sparam", "-no-param1[0]", "path2")
assert(OperationHelper.checkOptions(parsedOptions2, new PrintStream(new NullOutputStream)))
```

### LLM Instruction Prompt
- When calling `checkOptions`, ensure that the `options` parameter is a valid instance of `ParsedCommandLineOptions` containing the necessary command line arguments, and provide a `PrintStream` for output.

### Prompt Snippet
```text
Check if the command line options provided by the user are valid using the checkOptions function.
```

### Common Failure Modes
- **[runtime]** java.lang.NoClassDefFoundError: org/mortbay/jetty/handler/AbstractHandler _(seen 4x)_

### Fix Code Hint
```scala
Ensure that all required options are included in the command line arguments and that no unexpected options are present before calling checkOptions.
```

## API Test: `getOperationParams`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def getOperationParams(operation: Operation, opts: BeastOptions): Array[OperationParamInfo]
```
_Source: beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/util/OperationHelper.scala:209_

_Source doc:_ Returns all parameters that are allowed for the given operation. Operation parameters are all parameters annotated with [[OperationParam]] that appear in one of the following: - In the class associated with the given operation - In any additional classes defined in the [[OperationMetadata]] annotation on the class - In any classes that are added through the method [[IConfigurable]].addDependentClasses @param operation the operation in question @param opts any additional user options. This is used to add dependent classes if they depend on some user choice. For example, if the user selects a specific indexer, it can be used to add that specific indexer as a dependent class @return an array of parameters that are allowed

### Goal
The `getOperationParams` function retrieves all parameters that can be used with a specified raster operation in RDPro.

### Parameters
- `operation` (`Operation`): The specific raster operation for which parameters are being requested. This could be any operation defined within the RDPro library, such as a transformation or a join operation.
- `opts` (`BeastOptions`): Additional user options that may influence the parameters returned. This can include user-defined settings that affect the operation's behavior or dependencies.

### Input
The caller must provide a valid `Operation` instance representing the desired operation and an optional `BeastOptions` instance. The `Operation` should be one of the predefined operations in RDPro, and the `BeastOptions` can be null if no additional options are needed.

### Output
Returns `Array[OperationParamInfo]` — an array of parameter information objects that detail the parameters allowed for the specified operation. Each `OperationParamInfo` object contains metadata about the parameters, such as their names and types.

### Valid Call Patterns
```scala
val params = OperationHelper.getOperationParams(OperationHelper.operations("test"), null)
```

### LLM Instruction Prompt
- When calling `getOperationParams`, ensure that the `operation` parameter is a valid instance of `Operation` and that `opts` is either a valid `BeastOptions` instance or null.

### Prompt Snippet
```text
Retrieve the operation parameters for a specific raster operation using `getOperationParams`.
```

### Common Failure Modes
- **[runtime]** java.lang.NoClassDefFoundError: org/mortbay/jetty/handler/AbstractHandler _(seen 4x)_

### Fix Code Hint
```scala
Ensure that the `operation` parameter is correctly instantiated and corresponds to a valid operation in the RDPro library before calling `getOperationParams`.
```

## API Test: `printOperationUsage`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def printOperationUsage(operation: Operation, options: BeastOptions, out: PrintStream): Unit
```
_Source: beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/util/OperationHelper.scala:334_

_Source doc:_ Prints the usage of a specific operation. @param operation the operation to print the usage to @param out the print stream to write to

### Goal
The `printOperationUsage` function provides a description of how to use a specific raster processing operation within the RDPro library.

### Parameters
- `operation` (`Operation`): The specific operation for which usage information is being requested. This should be one of the predefined operations available in the RDPro library.
- `options` (`BeastOptions`): Configuration options that may affect the operation's behavior. This can include parameters like input/output formats or processing options, though the exact expected values are not specified.
- `out` (`PrintStream`): The output stream where the usage information will be printed. This is typically a standard output stream or a file output stream.

### Input
The caller must provide a valid `Operation` instance that corresponds to a defined operation in RDPro, a `BeastOptions` instance (which can be null if no options are needed), and a valid `PrintStream` to capture the output.

### Output
Returns `Unit` — this indicates that the function does not return a value but instead performs a side effect by printing the usage information directly to the provided `PrintStream`.

### Valid Call Patterns
```scala
val baos = new ByteArrayOutputStream()
val printer: PrintStream = new PrintStream(baos)
OperationHelper.printOperationUsage(OperationHelper.operations("subtest1"), null, printer)
printer.close()
```

### LLM Instruction Prompt
- Ensure that the `operation` parameter is a valid instance of `Operation` from the RDPro library.
- The `options` parameter can be null if no specific options are required for the operation.
- The `out` parameter must be a valid `PrintStream` to capture the output.

### Prompt Snippet
```text
Print the usage information for the specified operation using the provided PrintStream.
```

### Common Failure Modes
- **[runtime]** java.lang.NoClassDefFoundError: org/mortbay/jetty/handler/AbstractHandler _(seen 4x)_

### Fix Code Hint
```scala
// Ensure that the operation is valid and the PrintStream is not null before calling the function.
val operation = OperationHelper.operations.get("validOperationName")
if (operation.isDefined) {
    val printer: PrintStream = new PrintStream(new ByteArrayOutputStream())
    printOperationUsage(operation.get, null, printer)
} else {
    println("Invalid operation specified.")
}
```

## API Test: `readConfigurationXML`
_Grounding: test-backed — usage mined from a real, passing test._

### Signature
```scala
def readConfigurationXML(filename: String): java.util.Map[String, java.util.List[String]]
```
_Source: beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/util/OperationHelper.scala:60_

_Source doc:_ Read all XML configuration files of the given name in the class path and merge them into one object. This method internally caches the configuration so it does not have to be loaded multiple times. The XML is organized in three levels. The first level is the root element and it is always &lt;beast&gt;. The second level is a name of a collection, e.g., &lt;Indexers&gt;. Finally, the third level contains the contents of the collection in their text part. @param filename A path to an XML file that contains the configuration. @return the beast configuration as a map from each key to all values under this key.

### Goal
The `readConfigurationXML` function reads and merges XML configuration files from the class path, providing a structured representation of configuration settings for use in geospatial raster processing.

### Parameters
- `filename` (`String`): A path to an XML configuration file that contains the settings to be read and merged.

### Input
The caller must provide a valid path to an XML file that is accessible in the class path. The XML file should be structured with a root element `<beast>`, containing collections defined at the second level (e.g., `<Indexers>`), and the third level should contain the actual configuration values.

### Output
Returns `java.util.Map[String, java.util.List[String]]` — a map where each key corresponds to a collection name from the XML, and the associated value is a list of strings representing the contents of that collection.

### Valid Call Patterns
```scala
val conf: util.Map[String, util.List[String]] = OperationHelper.readConfigurationXML("test-beast.xml")
```

### LLM Instruction Prompt
- When calling `readConfigurationXML`, ensure that the provided filename points to a valid XML configuration file in the class path, and be aware that the function caches the configuration for efficiency.

### Prompt Snippet
```text
Read the configuration from the XML file using `readConfigurationXML`, ensuring the file is correctly formatted and accessible in the class path.
```

### Common Failure Modes
- **[runtime]** java.lang.IllegalArgumentException: requirement failed: empty result for readConfigurationXML _(seen 4x)_

### Fix Code Hint
```scala
// Ensure the XML file exists and is correctly formatted before calling the function.
val conf: util.Map[String, util.List[String]] = OperationHelper.readConfigurationXML("path/to/your/config.xml")
```
