## API Test: `getBoolean`
_Grounding: doc-repaired from source (docfix)._

### Goal
Retrieve a boolean option value by key from a `BeastOptions` configuration object, with a fallback default when the key is not set.

### Valid Call Patterns
**Required Types & Imports:**
- Requires `edu.ucr.cs.bdlab.beast.common.BeastOptions` (Scala class). Reference directly or import.

```scala
import edu.ucr.cs.bdlab.beast.common.BeastOptions

// Instantiate directly to avoid Hadoop/Spark initialization overhead and classpath issues
val opts = new BeastOptions(false)

// Populate programmatically
opts.setBoolean("option-4", true)

// Retrieve with fallback defaults
val v1: Boolean = opts.getBoolean("option-4", defaultValue = false)
val v2: Boolean = opts.getBoolean("missing-option", defaultValue = true)

require(v1 == true, s"Expected option-4=true but got $v1")
require(v2 == true, s"Expected missing-option fallback=true but got $v2")
```

### LLM Instruction Prompt
- Do not use `OperationHelper.parseCommandLineArguments` to create `BeastOptions` in standalone tests, as it triggers Hadoop/Spark initialization that fails due to missing Jetty classpath dependencies.
- Instead, instantiate `BeastOptions` directly using `new BeastOptions(false)`.
- Populate the options programmatically using `.setBoolean(key, value)` before calling `.getBoolean(key, defaultValue)`.

### Prompt Snippet
```text
To test boolean options without triggering Hadoop/Spark Jetty classpath errors, instantiate `new edu.ucr.cs.bdlab.beast.common.BeastOptions(false)`, populate it with `.setBoolean(key, value)`, and read it with `.getBoolean(key, defaultValue)`.
```

### Common Failure Modes
- **Jetty Classpath Crash:** Using `OperationHelper.parseCommandLineArguments` to create the options object in standalone tests. This triggers Hadoop/Spark classloading that requires Jetty dependencies (`org/mortbay/jetty/handler/AbstractHandler`) not present on the standalone test classpath.
- **Assuming Exceptions on Missing Keys:** Assuming missing keys throw an error; this method safely uses the provided `defaultValue` fallback.

### Fix Code Hint
```scala
// WRONG: Triggers Hadoop/Spark Jetty classpath errors in standalone tests
val parsed = OperationHelper.parseCommandLineArguments("test", "-option-4")
val v1 = parsed.options.getBoolean("option-4", false)

// CORRECT: Instantiate BeastOptions directly and populate programmatically
val opts = new edu.ucr.cs.bdlab.beast.common.BeastOptions(false)
opts.setBoolean("option-4", true)
val v1 = opts.getBoolean("option-4", defaultValue = false)
```