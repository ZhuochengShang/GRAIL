## API Test: `resizerFactory`
_Grounding: doc-repaired from source (docfix)._

### Signature
```java
public Builder<T> resizerFactory(ResizerFactory resizerFactory)
public ThumbnailParameterBuilder resizerFactory(ResizerFactory resizerFactory)
public ThumbnailMaker resizerFactory(ResizerFactory resizerFactory)
```

### Goal
ADVANCED/LOW-LEVEL API. Sets the factory responsible for dynamically determining which resizing algorithm to apply based on image dimensions. Note: This is an advanced configuration step used to override default logic; it should be excluded from the main user-facing denominator and used only for internal/advanced testing.

### Parameters
- `resizerFactory` (`ResizerFactory`): An object providing `Resizer` instances. Must not be null. Callers must provide a custom implementation of the public `net.coobird.thumbnailator.resizers.ResizerFactory` interface.

### Input
ADVANCED/LOW-LEVEL: A valid, caller-owned implementation of `ResizerFactory`. The builder instance must be in a state where neither `resizerFactory()`, `resizer()`, nor any specific rendering hints (`scalingMode`, `alphaInterpolation`, `dithering`, `antialiasing`, `rendering`) have been previously set.

### Output
Returns `Builder<T>` (or `ThumbnailParameterBuilder` / `ThumbnailMaker`, depending on the overload) — A reference to the current builder object to allow fluent method chaining.

### Valid Call Patterns
```java
import net.coobird.thumbnailator.Thumbnails;
import net.coobird.thumbnailator.resizers.ResizerFactory;
import net.coobird.thumbnailator.resizers.Resizer;
import java.awt.Dimension;
import java.awt.image.BufferedImage;

// 1. Advanced/Low-Level Construction using an anonymous ResizerFactory
ResizerFactory customFactory = new ResizerFactory() {
    @Override
    public Resizer getResizer() {
        return null; // Stub for configuration test
    }
    
    @Override
    public Resizer getResizer(Dimension originalSize, Dimension thumbnailSize) {
        return null; // Stub for configuration test
    }
};

Thumbnails.Builder<BufferedImage> builder = 
    Thumbnails.of(new BufferedImage(100, 100, BufferedImage.TYPE_INT_ARGB))
        .size(50, 50)
        .resizerFactory(customFactory);
```

### LLM Instruction Prompt
- Classify as ADVANCED/LOW-LEVEL.
- NEVER use `DefaultResizerFactory`; it is not part of the public API and will cause a compilation error.
- ALWAYS implement the `net.coobird.thumbnailator.resizers.ResizerFactory` interface directly.
- NEVER call `resizerFactory()` if `resizer()`, `scalingMode()`, `alphaInterpolation()`, `dithering()`, `antialiasing()`, or `rendering()` have been called on the same builder.

### Prompt Snippet
```text
When configuring a Thumbnailator pipeline with `.resizerFactory(ResizerFactory)`, you must implement the `ResizerFactory` interface yourself. Do not use internal classes like `DefaultResizerFactory`. This method is mutually exclusive with `.resizer()` and all rendering hint methods.
```

### Common Failure Modes
- **`cannot find symbol` (Internal Class Access)**: Attempting to use `DefaultResizerFactory.getInstance()` fails because it is package-private/internal. Callers must implement the public `ResizerFactory` interface themselves.
- **`IllegalStateException` (Mutually Exclusive Configuration)**: Thrown if called after `resizer()`, `scalingMode()`, `alphaInterpolation()`, `dithering()`, `antialiasing()`, or `rendering()`. As an ADVANCED/LOW-LEVEL API, failures often stem from mixing this with standard user-facing rendering hints.
- **`IllegalStateException` (Multiple Calls)**: Thrown if called more than once on the same builder.
- **`NullPointerException`**: Thrown if `resizerFactory` is null.

### Fix Code Hint
```java
// BAD: Relying on internal/undocumented factory causes "cannot find symbol"
builder.resizerFactory(net.coobird.thumbnailator.resizers.DefaultResizerFactory.getInstance());

// GOOD: Implement the public interface directly
builder.resizerFactory(new net.coobird.thumbnailator.resizers.ResizerFactory() {
    @Override
    public net.coobird.thumbnailator.resizers.Resizer getResizer() { 
        return null; 
    }
    @Override
    public net.coobird.thumbnailator.resizers.Resizer getResizer(java.awt.Dimension orig, java.awt.Dimension thumb) { 
        return null; 
    }
});
```