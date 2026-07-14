## API Test: `getBoolean`
_Grounding: doc-repaired from source (docfix)._

### Goal
Read a boolean option from a `BeastOptions` instance by key, with explicit fallback.  
Method is on `edu.ucr.cs.bdlab.beast.common.BeastOptions`, not a standalone function.

### Valid Call Patterns|Valid Access Patterns
```scala
import edu.ucr.cs.bdlab.beast.common.BeastOptions

val opts = new BeastOptions()
opts.setBoolean("option-3", false)
opts.setBoolean("option-4", true)

val v1: Boolean = opts.getBoolean("option-3", defaultValue = true)
val v2: Boolean = opts.getBoolean("option-4", defaultValue = false)
val v3: Boolean = opts.getBoolean("missing-option", defaultValue = true)
```

Semantics (exactly from source):
```scala
super.getOrElse(key, defaultValue.toString).toBoolean
```
So it does string lookup, falls back to `defaultValue.toString`, then parses with Scala `toBoolean`.

### LLM Instruction Prompt
Use `getBoolean` only as an instance call on `BeastOptions`:
`opts.getBoolean(key: String, defaultValue: Boolean)`.  
Missing key returns the provided default (via `toString` then `toBoolean`), not an exception.  
If options are produced via `OperationHelper.parseCommandLineArguments`, ensure runtime/test classpath includes its transitive dependencies; otherwise failure may occur before `getBoolean` executes.

### Prompt Snippet
```text
Create or receive `edu.ucr.cs.bdlab.beast.common.BeastOptions`, then call:
opts.getBoolean("option-3", defaultValue = true)
Do not call getBoolean as a static/bare function.
If using OperationHelper.parseCommandLineArguments, verify transitive deps are on classpath.
```

### Common Failure Modes
- **Observed recent failure:** `NoClassDefFoundError`/classpath error for `org/mortbay/jetty/handler/AbstractHandler` when using parser setup; execution stops before `getBoolean` runs.
- Calling `getBoolean` without a `BeastOptions` receiver.
- Assuming missing keys throw; they do not—default is returned.

### Fix Code Hint
Wrong (environment/parser path breaks before API call):
```scala
val parsed = OperationHelper.parseCommandLineArguments(...) // fails if jetty transitive deps missing
val b = parsed.options.getBoolean("option-3", true)
```

Correct (direct API usage, compilable with BeastOptions type):
```scala
import edu.ucr.cs.bdlab.beast.common.BeastOptions
val opts = new BeastOptions()
opts.setBoolean("option-3", false)
val b: Boolean = opts.getBoolean("option-3", defaultValue = true)
```