## API Test: `retainIndex`
_Grounding: doc-repaired from source (docfix)._

### Goal
Creates a new `BeastOptions` instance containing all non-indexed key-value pairs from the original, plus any pairs whose key has a specific index suffix (e.g., `key[1]`). When an indexed key is retained, its index suffix is **stripped** from the key in the new instance.

### Valid Call Patterns|Valid Access Patterns
```scala
// Requires edu.ucr.cs.bdlab.beast.common.BeastOptions
import edu.ucr.cs.bdlab.beast.common.BeastOptions

val opts = new BeastOptions()
  .set("input[0]", "file1.tif")
  .set("input[1]", "file2.tif")
  .set("output", "output.tif")
  .set("crs[1]", "EPSG:4326")

// Retain non-indexed keys and keys with index 1.
val optsRetained = opts.retainIndex(1)

// Access retained values using the STRIPPED key.
val retainedInput: String = optsRetained.get("input").get // from original key "input[1]"
val retainedCrs: String = optsRetained.get("crs").get     // from original key "crs[1]"
val retainedOutput: String = optsRetained.get("output").get // non-indexed key is preserved

// The original indexed keys are not present in the result.
assert(optsRetained.get("input[1]").isEmpty)
assert(optsRetained.get("input[0]").isEmpty)
```

### LLM Instruction Prompt
Filter a `BeastOptions` instance using `retainIndex(index)`. The returned `BeastOptions` contains all non-indexed keys and any keys that originally ended with `[index]`. For the retained indexed keys, the `[index]` suffix is removed from the key name in the result. For example, after `retainIndex(1)`, the key `"input[1]"` becomes `"input"`.

### Prompt Snippet
```text
Filter BeastOptions by index using retainIndex. The key "key[1]" becomes "key" after retainIndex(1).
```

### Common Failure Modes
Code fails assertions or lookups because it incorrectly assumes the index suffix is preserved in the returned `BeastOptions`. For example, after `opts.retainIndex(1)`, code attempts to access `opts.get("input[1]")` which returns `None`, instead of the correct `opts.get("input")`.

### Fix Code Hint
```scala
val opts = new BeastOptions().set("input[1]", "file.tif")
val retainedOpts = opts.retainIndex(1)

// WRONG: Assumes the index suffix is kept. This will fail.
// val value = retainedOpts.get("input[1]")

// CORRECT: Access the key with the index suffix stripped.
val value = retainedOpts.get("input")
```