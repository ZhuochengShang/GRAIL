## API Test: `readConfigurationXML`
_Grounding: doc-repaired from source (docfix)._

### Goal
Load and merge Beast XML configuration entries from classpath resources into a single cached key→list-of-values map.

### Valid Call Patterns
**Required Imports and Types:**
- Requires `edu.ucr.cs.bdlab.beast.util.OperationHelper` (Scala object).

```scala
import edu.ucr.cs.bdlab.beast.util.OperationHelper

// Must use a real classpath file like "beast.xml"
val conf = OperationHelper.readConfigurationXML("beast.xml")
val keyCount = if (conf == null) 0 else conf.size()
require(keyCount > 0, "empty configuration map for readConfigurationXML")

val ops = conf.get("Operations")
val opsCount = if (ops == null) 0 else ops.size()
require(opsCount > 0, "Operations list is empty in readConfigurationXML result")

println("__CHECK__ readConfigurationXML " + s"keys=$keyCount,operations=$opsCount")
```

### LLM Instruction Prompt
- To test this method successfully, you must use a filename that actually exists in the library's classpath, such as `"beast.xml"`. Do not invent dummy filenames like `"test-beast.xml"`.
- If the provided filename is not found in the classpath, the method does not throw an exception; it silently returns an empty `java.util.Map`.
- Always check for `null` when evaluating the returned map's size or retrieving specific keys (e.g., `"Operations"`), as missing files or keys will yield nulls or empty maps.
- The return type is strictly Java collections (`java.util.Map[String, java.util.List[String]]`); do not use Scala collection methods without conversion.

### Prompt Snippet
Call `OperationHelper.readConfigurationXML("beast.xml")`. Do not invent dummy filenames; missing files silently return an empty map instead of throwing an exception. Handle nulls safely when checking the map size and retrieving keys like `"Operations"`.

### Common Failure Modes
- **Silent empty map on missing file:** Passing a dummy filename (e.g., `"test-beast.xml"`) that does not exist in the classpath. The method silently returns an empty `java.util.HashMap` instead of throwing an exception, causing subsequent size assertions to fail.
- **Null pointer exceptions:** Failing to check for `null` before calling `.size()` on the returned map or on the lists returned by `.get("Operations")`.
- **Type mismatch:** Treating the returned Java Map/List as Scala collections.

### Fix Code Hint
```scala
// WRONG: Uses dummy filename, silently returns empty map, crashes on missing keys
val conf = OperationHelper.readConfigurationXML("test-beast.xml")
val ops = conf.get("Operations")
require(ops.size() > 0) // NullPointerException if ops is null

// CORRECT: Uses actual classpath file, handles nulls safely
val conf = OperationHelper.readConfigurationXML("beast.xml")
val keyCount = if (conf == null) 0 else conf.size()
require(keyCount > 0, "empty configuration map for readConfigurationXML")

val ops = conf.get("Operations")
val opsCount = if (ops == null) 0 else ops.size()
require(opsCount > 0, "Operations list is empty in readConfigurationXML result")
```