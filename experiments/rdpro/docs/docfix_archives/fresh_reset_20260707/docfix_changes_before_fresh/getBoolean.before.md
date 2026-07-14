## API Test: `getBoolean`

### Signature
```scala
def getBoolean(key: String, defaultValue: Boolean): Boolean
```
_Source: beast/common/src/main/scala/edu/ucr/cs/bdlab/beast/common/BeastOptions.scala:133_

_Source doc:_ Get value as boolean @param key @param defaultValue @return

### Goal
Retrieve a boolean option value (typically parsed from Beast/RDPro-style command-line options) by key, with a fallback default when the key is not set.

### Parameters
- `key` (`String`): The option name to read (for example, `"option2"`, `"option-3"`, `"option-4"` in tested usage).
- `defaultValue` (`Boolean`): The boolean value to return if `key` is not present in the options.

### Input
A parsed options container (receiver shown as `parsed.options` in tests) that stores key/value options from command-line-style arguments.

Preconditions from verified usage:
- Call this on an options object, e.g., `parsed.options.getBoolean(...)` (not as a bare function call).
- `key` should match the stored option name exactly, including dashes when present (e.g., `"option-3"`).
- This API is about option lookup; it does not take raster/vector files directly.

### Output
Returns `Boolean` — the resolved boolean value for `key`; if missing, returns `defaultValue`.

### Valid Call Patterns
```scala
val parsed = OperationHelper.parseCommandLineArguments("test", "path1",
  "option1:value1", "-option2", "-no-option3", "path2", "option4[0]:1", "-option4[1]")

parsed.options.getBoolean("option2", defaultValue = false)
parsed.options.getBoolean("option3", defaultValue = true)
```

```scala
val parsed = OperationHelper.parseCommandLineArguments("test", "path1",
  "option1:value1", "-no-option-3", "-option-4", "file-name:abc")

parsed.options.getBoolean("option-3", true)
parsed.options.getBoolean("option-4", false)
```

### LLM Instruction Prompt
- Use the instance call form exactly as verified: `parsed.options.getBoolean(key, defaultValue)`.
- Provide a concrete `String` key and a concrete `Boolean` default.
- Keep key spelling exact (including `-` characters).
- Do not invent overloads or omit the receiver.

### Prompt Snippet
```text
Given a parsed Beast options object `parsed`, read a boolean flag with:
`parsed.options.getBoolean("option-name", defaultValue = false)`.
Use the exact key string (including dashes), and always pass the fallback boolean.
```

### Common Failure Modes
- Calling `getBoolean(...)` without an options receiver (won’t match verified usage form).
- Using the wrong key spelling (e.g., dropping dashes: `"option3"` vs `"option-3"` when only one exists).
- Assuming missing keys throw an error; this method uses `defaultValue` fallback.

### Fix Code Hint
```scala
val enabled: Boolean = parsed.options.getBoolean("option-4", defaultValue = false)
val disabledByNoFlag: Boolean = parsed.options.getBoolean("option-3", defaultValue = true)
```