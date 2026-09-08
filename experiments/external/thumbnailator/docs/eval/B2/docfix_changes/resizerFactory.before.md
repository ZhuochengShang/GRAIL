## API Test: `resizerFactory`

### Signature
```java
public Builder<T> resizerFactory(ResizerFactory resizerFactory)
public ThumbnailParameterBuilder resizerFactory(ResizerFactory resizerFactory)
public ThumbnailMaker resizerFactory(ResizerFactory resizerFactory)
```
_Source: source/src/main/java/net/coobird/thumbnailator/Thumbnails.java:1348  (+2 more definition site/overload)_

_Source doc:_ Sets the {@link ResizerFactory} object to use to decide what kind of resizing operation is to be used when creating the thumbnail. <p> Calling this method to set this parameter is optional. <p> Calling this method multiple times will result in an {@link IllegalStateException} to be thrown. <p> This method cannot be called in conjunction with the {@link #resizer(Resizer)} method. @param resizerFactory		The scaling operation to use. @return						Reference to this object. @since	0.4.0

### Goal
Sets the factory responsible for dynamically determining which resizing algorithm (e.g., bicubic, bilinear, progressive bilinear) to apply based on the original and target image dimensions.

### Parameters
- `resizerFactory` (`ResizerFactory`): The factory instance (such as `DefaultResizerFactory.getInstance()` or `FixedResizerFactory`) that will supply the `Resizer` for the scaling operation.

### Input
A valid `ResizerFactory` implementation. The builder instance must be in a state where neither `resizerFactory()` nor `resizer()` has been previously called.

### Output
Returns `Builder<T>` (or `ThumbnailParameterBuilder` / `ThumbnailMaker`, depending on the overload) — A reference to the current builder object to allow fluent method chaining.

### Valid Call Patterns
```java
// 1. Using ThumbnailParameterBuilder (Verified from test suite)
ResizerFactory resizerFactory = DefaultResizerFactory.getInstance();
ThumbnailParameter param = new ThumbnailParameterBuilder()
        .size(100, 100)
        .resizerFactory(resizerFactory)
        .build();

// 2. Using the fluent Thumbnails.Builder (Inferred from signature and standard usage)
Thumbnails.of(new File("original.jpg"))
        .size(200, 200)
        .resizerFactory(DefaultResizerFactory.getInstance())
        .toFile(new File("thumbnail.jpg"));
```

### LLM Instruction Prompt
- NEVER call `resizerFactory()` multiple times on the same builder instance.
- NEVER call `resizerFactory()` in conjunction with `resizer(Resizer)` on the same builder.
- Use `resizerFactory()` when you want the library to dynamically choose the best scaling algorithm based on the input and output dimensions, rather than hardcoding a specific `Resizer`.

### Prompt Snippet
```text
When configuring a Thumbnailator pipeline, use `.resizerFactory(ResizerFactory)` to dictate how the scaling algorithm is chosen. You must not call this method multiple times, nor can you mix it with `.resizer(Resizer)`. Doing so will throw an `IllegalStateException`.
```

### Common Failure Modes
- **`IllegalStateException` (Multiple Calls)**: Thrown if `resizerFactory(...)` is called more than once on the same builder instance.
- **`IllegalStateException` (Mutually Exclusive Configuration)**: Thrown if `resizerFactory(...)` is called on a builder that has already been configured with a specific resizer via `resizer(...)`, or vice versa.

### Fix Code Hint
```java
// BAD: Mixing resizer() and resizerFactory() causes an IllegalStateException
ThumbnailParameter param = new ThumbnailParameterBuilder()
        .size(100, 100)
        .resizer(new ProgressiveBilinearResizer())
        .resizerFactory(DefaultResizerFactory.getInstance()) // Throws IllegalStateException
        .build();

// GOOD: Choose exactly one strategy for defining the resizing behavior
ThumbnailParameter param = new ThumbnailParameterBuilder()
        .size(100, 100)
        .resizerFactory(DefaultResizerFactory.getInstance())
        .build();
```