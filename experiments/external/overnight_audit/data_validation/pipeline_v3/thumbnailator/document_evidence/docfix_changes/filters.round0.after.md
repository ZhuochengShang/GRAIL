## API Test: `filters`
_Grounding: doc-repaired from source (docfix)._

### Signature
```java
public ThumbnailParameterBuilder filters(List<ImageFilter> filters)
```

### Goal
Configures a `ThumbnailParameterBuilder` by specifying a sequence of `ImageFilter` transformations to apply after resizing. This is an ADVANCED/LOW-LEVEL internal API used for constructing custom task instances. *Note: Exclude this API from main user-facing benchmark denominators as it targets internal framework configuration rather than standard image processing pipelines.*

### Parameters
- `filters` (`List<ImageFilter>`): A list of image filters to apply sequentially. Must not be `null`.

### Input
A valid `List` containing instantiated `ImageFilter` objects. The caller must explicitly construct the receiver (`ThumbnailParameterBuilder`) via its public no-argument constructor. Because this is an ADVANCED/LOW-LEVEL API, concrete filter implementations (like `Flip` or `Rotation`) may not be in scope; callers must provide an anonymous implementation of `ImageFilter` to guarantee compilation when testing in isolation.

### Output
Returns `ThumbnailParameterBuilder` — A reference to the current builder instance.

### Valid Call Patterns
```java
import net.coobird.thumbnailator.builders.ThumbnailParameterBuilder;
import net.coobird.thumbnailator.filters.ImageFilter;
import java.awt.image.BufferedImage;
import java.util.List;
import java.util.Collections;

// Caller-owned low-level construction
ThumbnailParameterBuilder builder = new ThumbnailParameterBuilder();

// Provide an anonymous implementation since concrete filters may not be in scope
List<ImageFilter> myFilters = Collections.singletonList(
    new ImageFilter() {
        @Override
        public BufferedImage apply(BufferedImage img) {
            return img; // No-op
        }
    }
);

builder.filters(myFilters);
```

### LLM Instruction Prompt
- This is an ADVANCED/LOW-LEVEL API. Instantiate `ThumbnailParameterBuilder` via its no-argument constructor.
- `ThumbnailParameterBuilder` does not have a `size(int, int)` method; do not chain fabricated methods when configuring it.
- Do not assume the presence of concrete filter classes like `Flip` or `Rotation`; if testing the API in isolation, provide an anonymous implementation of the `ImageFilter` interface.
- Do not call `.build()` or attempt to retrieve state via `.getFilters()` unless those methods are explicitly defined in your available source context.

### Prompt Snippet
```text
When configuring a ThumbnailParameterBuilder, use `.filters(List<ImageFilter>)` to set the post-resize transformation pipeline. Instantiate the builder directly via `new ThumbnailParameterBuilder()`. Do not chain non-existent methods like `.size()`, and use an anonymous ImageFilter if concrete implementations are unavailable.
```

### Common Failure Modes
- **Fabricating Methods (The failure that just happened):** Blindly chaining methods like `.size(100, 100)` onto `ThumbnailParameterBuilder`. This class does *not* have a `size` method, causing a `cannot find symbol` compilation error.
- **Missing Concrete Filters:** Attempting to use `Flip.HORIZONTAL` or `Rotation` when they are not guaranteed to be in scope, resulting in missing symbol errors.
- **Calling Unavailable Methods:** Calling `.build()` or `.getFilters()` when they are not provided in the immediate context.
- **API Confusion:** This is an ADVANCED/LOW-LEVEL API. Do not confuse it with the standard `Thumbnails.of()` fluent API. Exclude from standard user-facing benchmarks.
- **Null Elements:** Passing a `null` list throws a `NullPointerException`.

### Fix Code Hint
```java
// WRONG: Fabricating .size() and using unavailable concrete filters/methods
ThumbnailParameterBuilder builder = new ThumbnailParameterBuilder();
builder.size(100, 100).filters(Arrays.asList(Flip.HORIZONTAL)).build();

// CORRECT: Using only available methods and an anonymous ImageFilter
ThumbnailParameterBuilder builder = new ThumbnailParameterBuilder();
java.util.List<net.coobird.thumbnailator.filters.ImageFilter> myFilters = java.util.Collections.singletonList(
    new net.coobird.thumbnailator.filters.ImageFilter() {
        @Override
        public java.awt.image.BufferedImage apply(java.awt.image.BufferedImage img) {
            return img;
        }
    }
);
builder.filters(myFilters);
```