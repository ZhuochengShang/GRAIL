## API Test: `getInstance`
_Grounding: doc-repaired from source (docfix)._

### Signature
```java
public static SwapDimensions getInstance()
public static ResizerFactory getInstance()
```

### Goal
ADVANCED/LOW-LEVEL. Exclude from main user-facing denominator (standard users should use `Thumbnails.Builder`). Returns the singleton instance of specific stateless utility classes (`DefaultResizerFactory` or `SwapDimensions`).

### Parameters
_None._

### Input
ADVANCED/LOW-LEVEL. No arguments required. Call directly on the target class (`DefaultResizerFactory` or `SwapDimensions`). Do not attempt to pass the result into low-level builders to test execution.

### Output
Returns `ResizerFactory` or `SwapDimensions` — A reusable, thread-safe singleton instance of the requested class.

### Valid Call Patterns
```java
import net.coobird.thumbnailator.resizers.ResizerFactory;
import net.coobird.thumbnailator.resizers.DefaultResizerFactory;
import net.coobird.thumbnailator.filters.SwapDimensions;

// Obtain the singleton instances directly
ResizerFactory resizerFactory = DefaultResizerFactory.getInstance();
SwapDimensions swapFilter = SwapDimensions.getInstance();

if (resizerFactory == null || swapFilter == null) {
    throw new IllegalStateException("Instances should not be null");
}
```

### LLM Instruction Prompt
To test or use the API, simply call `DefaultResizerFactory.getInstance()` and `SwapDimensions.getInstance()` directly and assign them to their respective types. Do not attempt to use `ThumbnailParameterBuilder` to demonstrate `getInstance()`, as it is not publicly accessible in the expected package and will cause a compilation error.

### Prompt Snippet
```text
Call `DefaultResizerFactory.getInstance()` and `SwapDimensions.getInstance()` directly. Do not use `ThumbnailParameterBuilder` or constructors.
```

### Common Failure Modes
- **Builder Compilation Error (`cannot find symbol`)**: Attempting to instantiate `net.coobird.thumbnailator.ThumbnailParameterBuilder` to consume the instance. This builder is not publicly accessible in the expected package and fails compilation. The `getInstance()` methods are perfectly testable in isolation.
- **Constructor Compilation Error**: Attempting to instantiate these singleton classes using the `new` keyword (e.g., `new DefaultResizerFactory()`) instead of the `getInstance()` factory method.
- **ADVANCED/LOW-LEVEL Misuse**: Attempting to manually wire these singletons into a pipeline when the fluent `Thumbnails.Builder` already configures them internally.

### Fix Code Hint
```java
// Incorrect: Attempting to use an inaccessible builder, causing 'cannot find symbol'
// net.coobird.thumbnailator.ThumbnailParameter param = new net.coobird.thumbnailator.ThumbnailParameterBuilder()
//        .resizerFactory(net.coobird.thumbnailator.resizers.DefaultResizerFactory.getInstance())
//        .build();

// Correct: Testing the getInstance() API directly in isolation
net.coobird.thumbnailator.resizers.ResizerFactory resizerFactory = net.coobird.thumbnailator.resizers.DefaultResizerFactory.getInstance();
net.coobird.thumbnailator.filters.SwapDimensions swapFilter = net.coobird.thumbnailator.filters.SwapDimensions.getInstance();
```