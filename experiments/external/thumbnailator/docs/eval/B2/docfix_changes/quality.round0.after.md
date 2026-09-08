## API Test: `quality`
_Grounding: doc-repaired from source (docfix)._

### Signature
```java
public ThumbnailParameterBuilder quality(float quality)
```
_Source: source/src/main/java/net/coobird/thumbnailator/builders/ThumbnailParameterBuilder.java:232_

### Goal
ADVANCED/LOW-LEVEL API. Recommended for exclusion from standard user-facing workflows (users should prefer the higher-level `Thumbnails` fluent API). Sets the compression quality setting in the builder's internal state.

### Parameters
- `quality` (`float`): The compression quality setting. Acceptable values range from `0.0f` (lowest quality, highest compression) to `1.0f` (highest quality, lowest compression). To use the default quality, pass `ThumbnailParameter.DEFAULT_QUALITY`.

### Input
A valid `float` literal (must include the `f` suffix). As an ADVANCED/LOW-LEVEL API, the receiver is a manually instantiated `ThumbnailParameterBuilder` (caller-owned), created directly via its public no-argument constructor.

### Output
Returns `ThumbnailParameterBuilder` — A reference to the current builder instance (`this`), allowing for fluent method chaining.

### Valid Call Patterns
```java
import net.coobird.thumbnailator.builders.ThumbnailParameterBuilder;

// The builder is caller-owned and instantiated directly via its public constructor
ThumbnailParameterBuilder builder = new ThumbnailParameterBuilder();
ThumbnailParameterBuilder returnedBuilder = builder.quality(0.75f);

// Optional: verify fluent chaining
assert returnedBuilder == builder;
```

### LLM Instruction Prompt
Instantiate `ThumbnailParameterBuilder` directly using `new ThumbnailParameterBuilder()`. Do not invent or call undocumented methods such as `size(int, int)`, `build()`, or `getQuality()` to verify state. Simply call `quality(float)` and optionally assert that it returns the same builder instance. Always append the `f` suffix to float literals to prevent compilation errors.

### Prompt Snippet
```text
ThumbnailParameterBuilder builder = new ThumbnailParameterBuilder();
ThumbnailParameterBuilder returnedBuilder = builder.quality(0.75f);
```

### Common Failure Modes
- **Hallucinating Undocumented Methods:** Attempting to call `size(int, int)`, `build()`, or `getQuality()` on `ThumbnailParameterBuilder` causes a "cannot find symbol" compilation error. These methods do not exist or are not public on this specific builder.
- **Compilation Error (Type Mismatch):** Passing a decimal literal without the `f` suffix (e.g., `0.75`) evaluates as a `double`, resulting in a compilation error because the method strictly requires a `float`.
- **Advanced API Misuse:** Attempting to use this low-level builder as if it were the main `Thumbnails` fluent API, leading to incorrect setup and missing dependencies.

### Fix Code Hint
```java
// INCORRECT: Hallucinating undocumented methods and missing 'f' suffix
// ThumbnailParameterBuilder builder = new ThumbnailParameterBuilder();
// builder.size(100, 100); // ERROR: cannot find symbol
// builder.quality(0.75);  // ERROR: double to float mismatch
// builder.build();        // ERROR: cannot find symbol

// CORRECT: Instantiate directly, use 'f' suffix, do not call undocumented methods
ThumbnailParameterBuilder builder = new ThumbnailParameterBuilder();
ThumbnailParameterBuilder returnedBuilder = builder.quality(0.75f);
```