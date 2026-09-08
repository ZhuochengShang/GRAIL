## API Test: `quality`

### Signature
```java
public ThumbnailParameterBuilder quality(float quality)
```
_Source: source/src/main/java/net/coobird/thumbnailator/builders/ThumbnailParameterBuilder.java:232_

_Source doc:_ Sets the compression quality setting of the thumbnail. <p> An acceptable value is in the range of {@code 0.0f} to {@code 1.0f}, where {@code 0.0f} is for the lowest quality setting and {@code 1.0f} for the highest quality setting. <p> If the default compression quality is to be used, then the value {@link ThumbnailParameter#DEFAULT_QUALITY} should be used. @param quality		The compression quality setting of the thumbnail. @return				A reference to this object.

### Goal
Sets the compression quality for the generated thumbnail, controlling the trade-off between file size and image fidelity for supported output formats.

### Parameters
- `quality` (`float`): The compression quality setting. Must be in the range of `0.0f` (lowest quality, highest compression) to `1.0f` (highest quality, lowest compression). To use the default compression quality, pass `ThumbnailParameter.DEFAULT_QUALITY` (which evaluates to `Float.NaN`).

### Input
A valid `float` value representing the desired quality. The underlying Java Image I/O writer for the chosen output format (e.g., JPEG) must support compression quality settings for this parameter to have a visible effect on the output file.

### Output
Returns `ThumbnailParameterBuilder` — A reference to the current builder instance, allowing for fluent method chaining.

### Valid Call Patterns
```java
// Inferred from signature (not verified by tests or README)
ThumbnailParameterBuilder builder = new ThumbnailParameterBuilder();
builder.quality(0.85f);

// Using the default quality constant
builder.quality(ThumbnailParameter.DEFAULT_QUALITY);
```

### LLM Instruction Prompt
- When configuring thumbnail compression, ensure the `quality` argument is a `float` strictly between `0.0f` and `1.0f` inclusive, or use `ThumbnailParameter.DEFAULT_QUALITY`. Always append the `f` suffix to literal decimal values to prevent `double` to `float` compilation errors.

### Prompt Snippet
```text
builder.quality(0.75f);
```

### Common Failure Modes
- **Compilation Error (Type Mismatch):** Passing a decimal literal without the `f` suffix (e.g., `0.8`) will be evaluated as a `double` by the Java compiler, resulting in a compilation error because the method strictly requires a `float`.
- **Out of Bounds Value:** Providing a value less than `0.0f` or greater than `1.0f` (other than `ThumbnailParameter.DEFAULT_QUALITY`) is invalid and will cause an `IllegalArgumentException` during parameter validation or when the underlying Image I/O writer attempts to apply the setting.
- **Unsupported Format:** Applying a quality setting to an output format that does not support lossy compression (like standard PNG or BMP in some Image I/O implementations) may be silently ignored by the underlying Java Image I/O writer.

### Fix Code Hint
```java
// INCORRECT: Missing 'f' suffix causes a double-to-float compilation error
// builder.quality(0.9); 

// CORRECT: Use the 'f' suffix for float literals
builder.quality(0.9f);

// CORRECT: Fallback to the default quality
builder.quality(ThumbnailParameter.DEFAULT_QUALITY);
```