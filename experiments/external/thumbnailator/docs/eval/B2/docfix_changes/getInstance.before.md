## API Test: `getInstance`

### Signature
```java
public static SwapDimensions getInstance()
public static ResizerFactory getInstance()
```
_Source: source/src/main/java/net/coobird/thumbnailator/filters/SwapDimensions.java:40  (+1 more definition site/overload)_

### Goal
Returns a singleton or default instance of a specific Thumbnailator component, such as the default `ResizerFactory` or the `SwapDimensions` image filter.

### Parameters
_None._

### Input
No arguments are required. The caller must invoke this static method directly on the target class (e.g., `DefaultResizerFactory` or `SwapDimensions`) to retrieve its singleton instance.

### Output
Returns `ResizerFactory` (or `SwapDimensions`) — A reusable, thread-safe instance of the requested class, which can be passed into a `ThumbnailParameterBuilder` or added to a `Thumbnails.Builder` pipeline.

### Valid Call Patterns
```java
// 1. Obtaining the default ResizerFactory for a ThumbnailTask (from test suite)
ResizerFactory resizerFactory = DefaultResizerFactory.getInstance();

ThumbnailParameter param = new ThumbnailParameterBuilder()
        .size(100, 100)
        .resizerFactory(resizerFactory)
        .build();

// 2. Obtaining the SwapDimensions filter (inferred from signature)
SwapDimensions swapFilter = SwapDimensions.getInstance();
```

### LLM Instruction Prompt
- When configuring a `ThumbnailParameter` that requires a `ResizerFactory`, always use `DefaultResizerFactory.getInstance()` rather than attempting to instantiate it with `new`. 
- Similarly, use `SwapDimensions.getInstance()` to obtain the dimension-swapping `ImageFilter`. 
- Never call `getInstance()` without a class qualifier.

### Prompt Snippet
```text
To get a `ResizerFactory` or `SwapDimensions` filter in Thumbnailator, call their static `getInstance()` methods (e.g., `DefaultResizerFactory.getInstance()`). Do not use their constructors, as they are designed as singletons.
```

### Common Failure Modes
- **Constructor Compilation Error**: Attempting to instantiate these singleton classes using the `new` keyword (e.g., `new DefaultResizerFactory()`) instead of the `getInstance()` factory method, resulting in compilation errors due to private or protected constructors.
- **Missing Class Qualifier**: Calling `getInstance()` as a bare method without specifying the class (e.g., `DefaultResizerFactory` or `SwapDimensions`), which will fail to compile.

### Fix Code Hint
```java
// Incorrect: Attempting to use a constructor for a singleton
// ResizerFactory factory = new DefaultResizerFactory();
// SwapDimensions filter = new SwapDimensions();

// Correct: Using the static getInstance() factory method
ResizerFactory factory = DefaultResizerFactory.getInstance();
SwapDimensions filter = SwapDimensions.getInstance();
```