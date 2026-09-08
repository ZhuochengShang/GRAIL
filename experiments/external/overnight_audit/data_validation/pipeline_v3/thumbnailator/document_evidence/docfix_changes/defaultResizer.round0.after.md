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
Returns `ThumbnailMaker` — A reference to the current `ThumbnailMaker` object, allowing for fluent method chaining.

### Valid Call Patterns
```java
import net.coobird.thumbnailator.makers.FixedSizeThumbnailMaker;
import net.coobird.thumbnailator.makers.ThumbnailMaker;
import java.awt.image.BufferedImage;

// Instantiate a concrete subclass (caller-owned)
FixedSizeThumbnailMaker maker = new FixedSizeThumbnailMaker(50, 50);

// Configure the maker with the default resizer
ThumbnailMaker returnedMaker = maker.defaultResizer();

// MUST satisfy all other readiness tracker requirements before calling make()
returnedMaker.defaultImageType();

// Now safe to execute
BufferedImage result = returnedMaker.make(sourceImage);
```

### LLM Instruction Prompt
- `ThumbnailMaker` is an abstract class and must be instantiated via a concrete subclass like `FixedSizeThumbnailMaker`.
- `ThumbnailMaker` uses a readiness tracker and requires all configuration parameters to be set before calling `make()`.
- Calling `defaultResizer()` only satisfies the resizer requirement; callers must also satisfy the image type requirement (e.g., by calling `defaultImageType()`) to avoid an `IllegalStateException` during execution.

### Prompt Snippet
```text
When using the low-level `ThumbnailMaker` API, call `defaultResizer()` to set the scaling algorithm, but ensure you also call `defaultImageType()` before invoking `make()` to satisfy the readiness tracker.
```

### Common Failure Modes
- **`IllegalStateException: Maker not ready to make thumbnail`**: Occurs when calling `make()` after `defaultResizer()` if other required parameters (like image type) have not been set. `ThumbnailMaker` requires all configuration parameters to be satisfied before execution.
- **Instantiation Error**: Attempting to instantiate `ThumbnailMaker` directly. It is an ADVANCED/LOW-LEVEL abstract class and requires a concrete subclass like `FixedSizeThumbnailMaker`.

### Fix Code Hint
```java
// WRONG: Calling make() without satisfying all readiness tracker requirements
ThumbnailMaker maker = new FixedSizeThumbnailMaker(50, 50);
maker.defaultResizer();
BufferedImage result = maker.make(sourceImage); // Throws IllegalStateException

// CORRECT: Satisfy all requirements (e.g., image type) before make()
ThumbnailMaker maker = new FixedSizeThumbnailMaker(50, 50);
maker.defaultResizer();
maker.defaultImageType(); // Satisfies the remaining requirement
BufferedImage result = maker.make(sourceImage); // Succeeds
```