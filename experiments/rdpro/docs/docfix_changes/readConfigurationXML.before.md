## API Test: `readConfigurationXML`

### Signature
```scala
def readConfigurationXML(filename: String): java.util.Map[String, java.util.List[String]]
```
_Source: beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/util/OperationHelper.scala:60_

_Source doc:_ Read all XML configuration files of the given name in the class path and merge them into one object. This method internally caches the configuration so it does not have to be loaded multiple times. The XML is organized in three levels. The first level is the root element and it is always &lt;beast&gt;. The second level is a name of a collection, e.g., &lt;Indexers&gt;. Finally, the third level contains the contents of the collection in their text part. @param filename A path to an XML file that contains the configuration. @return the beast configuration as a map from each key to all values under this key.

### Goal
Load and merge Beast XML configuration entries (from classpath resources with the same name) into a single cached key→list-of-values map.

### Parameters
- `filename` (`String`): Path/name of the XML configuration file to look up in the class path (e.g., `"test-beast.xml"` in the test).

### Input
`readConfigurationXML` expects an XML configuration file name/path that is resolvable from the class path.

Documented XML structure precondition:
1. Root element must be `<beast>`.
2. Second level contains collection names (for example `<Indexers>` or `<Operations>`).
3. Third level elements carry the collection values in their text content.

It reads **all XML configuration files of the given name in the class path** and merges them. It also caches loaded configuration internally.

### Output
Returns `java.util.Map[String, java.util.List[String]]` — a merged Beast configuration where:
- each map key is a second-level collection name (such as `"Operations"` / `"Indexers"`),
- each map value is the list of text values collected under that collection across matching classpath XML files.

### Valid Call Patterns
```scala
val conf: util.Map[String, util.List[String]] = OperationHelper.readConfigurationXML("test-beast.xml")
assert(4 == conf.get("Operations").size)
assert(1 == conf.get("Indexers").size)
assert("Op1" == conf.get("Operations").get(0))
```

### LLM Instruction Prompt
- Use the static receiver exactly as validated in tests: `OperationHelper.readConfigurationXML("...")`.
- Pass exactly one argument of type `String`.
- Provide a classpath-visible XML file name/path.
- Expect a Java map of string keys to Java lists of strings; do not assume Scala collections unless explicitly converted.
- Do not invent additional options, overloads, or schema fields beyond the documented 3-level XML organization.

### Prompt Snippet
```text
Call OperationHelper.readConfigurationXML(filename) with a classpath XML name (String). The XML must use <beast> as root, second-level collection tags (e.g., <Operations>), and third-level text entries. Treat the result as java.util.Map[String, java.util.List[String]].
```

### Common Failure Modes
- File not found on classpath: passing a filename that is not available as a classpath resource.
- Invalid XML layout: root not `<beast>` or unexpected nesting that does not match the documented three-level structure.
- Type mismatch in usage: treating returned Java collections as Scala collections without conversion.
- Expecting re-read side effects immediately after changing XML at runtime: method is documented to cache configuration internally.

### Fix Code Hint
```scala
import java.util
import edu.ucr.cs.bdlab.beast.util.OperationHelper

val conf: util.Map[String, util.List[String]] =
  OperationHelper.readConfigurationXML("test-beast.xml")

val operations: util.List[String] = conf.get("Operations")
if (operations != null) {
  println(s"Operations count = ${operations.size}")
}
```