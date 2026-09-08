## API Test: `defaultResizer`
_Grounding: doc-repaired from source (docfix)._

### Signature
```java
public ThumbnailMaker defaultResizer()
```

### Goal
ADVANCED/LOW-LEVEL API. Sets the image scaling algorithm used by the `ThumbnailMaker` to the library's default `Resizer`. Note: This is an internal/advanced API and should be excluded from standard user-facing benchmarks (typical users should use the `Thumbnails` facade instead).

### Parameters
_None._

### Input
ADVANCED/LOW-LEVEL API. The caller must invoke this on an instantiated concrete subclass of the abstract `ThumbnailMaker` (e.g., a caller-owned `FixedSizeThumbnailMaker`). 

### Output
Returns `ThumbnailMaker` — A reference to the current `ThumbnailMaker` object (`this`), allowing for fluent method chaining.

### Valid Call Patterns
```java
import net.coobird.thumbnailator.makers.FixedSizeThumbnailMaker;
import net.coobird.thumbnailator.makers.ThumbnailMaker;

// Instantiate a concrete subclass (caller-owned)
FixedSizeThumbnailMaker maker = new FixedSizeThumbnailMaker(50, 50);

// Configure the maker with the default resizer
ThumbnailMaker returnedMaker = maker.defaultResizer();

// Verify fluent return
System.out.println("__CHECK__ defaultResizer fluent return: " + (returnedMaker == maker));

// DO NOT call maker.make() here. The ReadinessTracker requires 
// additional undocumented parameters to be set.
```

### LLM Instruction Prompt
- `ThumbnailMaker` is an ADVANCED/LOW-LEVEL abstract class and must be instantiated via a concrete subclass like `FixedSizeThumbnailMaker`.
- `ThumbnailMaker` requires multiple undocumented parameters to be set before `make()` can be called; do not call `make()` in standalone snippets.
- The snippet should only instantiate a concrete subclass, call `defaultResizer()`, and verify the fluent return.
- Do not attempt to satisfy the readiness tracker manually, as the required parameters are not fully documented.

### Prompt Snippet
```text
When testing the low-level `ThumbnailMaker.defaultResizer()` API, instantiate a `FixedSizeThumbnailMaker`, call `defaultResizer()`, and assert the fluent return. Do not call `make()`, as it requires undocumented readiness parameters and will throw an IllegalStateException.
```

### Common Failure Modes
- **`IllegalStateException: Maker not ready to make thumbnail`**: Occurs when calling `make()` after `defaultResizer()`. The previous documentation incorrectly claimed that calling `defaultImageType()` was sufficient to satisfy the `ReadinessTracker`. In reality, `ThumbnailMaker` requires additional undocumented parameters to be set before `make()` can be legally invoked. Do not call `make()` in standalone snippets.
- **Instantiation Error**: Attempting to instantiate `ThumbnailMaker` directly. It is an ADVANCED/LOW-LEVEL abstract class and requires a concrete subclass like `FixedSizeThumbnailMaker`.

### Fix Code Hint
```java
// WRONG: Attempting to call make() or manually satisfy the readiness tracker
FixedSizeThumbnailMaker maker = new FixedSizeThumbnailMaker(50, 50);
maker.defaultResizer();
maker.defaultImageType();
BufferedImage result = maker.make(sourceImage); // Throws IllegalStateException

// CORRECT: Only verify the fluent return; do not call make()
FixedSizeThumbnailMaker maker = new FixedSizeThumbnailMaker(50, 50);
ThumbnailMaker returnedMaker = maker.defaultResizer();
System.out.println("__CHECK__ defaultResizer fluent return: " + (returnedMaker == maker));
```