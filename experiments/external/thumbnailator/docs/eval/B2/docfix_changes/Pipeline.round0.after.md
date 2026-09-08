## API Test: `Pipeline`
_Grounding: doc-repaired from source (docfix)._

### Signature
```java
public Pipeline()
public Pipeline(ImageFilter... filters)
public Pipeline(List<ImageFilter> filters)
public void add(ImageFilter filter)
public BufferedImage apply(BufferedImage img)
```

### Goal
ADVANCED/LOW-LEVEL API. Instantiates an execution engine that sequentially applies `ImageFilter` transformations to a `BufferedImage`. Note: This is an internal/framework-level class and should be excluded from the main user-facing benchmark denominator. Standard users should strictly prefer the fluent `Thumbnails.Builder` API.

### Parameters
- `filters` (`ImageFilter...` or `List<ImageFilter>`): The sequence of filters to apply. Must not be null.

### Input
ADVANCED/LOW-LEVEL. The caller must provide an in-memory `BufferedImage` and one or more `ImageFilter` implementations. Because concrete filter constructors (like `Rotation` or `Watermark`) are not in context, standalone tests must use an anonymous implementation of the `ImageFilter` interface to guarantee compilation.

### Output
`Pipeline.apply(BufferedImage)` returns a `BufferedImage` with all filters applied sequentially. If the pipeline is empty, it returns the original image; if not empty, it returns a modified deep copy.

### Valid Call Patterns
```java
import java.awt.image.BufferedImage;
import net.coobird.thumbnailator.filters.Pipeline;
import net.coobird.thumbnailator.filters.ImageFilter;

// 1. Create a source image
BufferedImage img = new BufferedImage(120, 60, BufferedImage.TYPE_INT_ARGB);

// 2. Create an anonymous ImageFilter to avoid guessing concrete constructors
ImageFilter dummyFilter = new ImageFilter() {
    @Override
    public BufferedImage apply(BufferedImage image) {
        // Perform custom image manipulation here; returning as-is for minimal usage
        return image;
    }
};

// 3. Instantiate Pipeline and apply
Pipeline pipeline = new Pipeline(dummyFilter);
BufferedImage result = pipeline.apply(img);
```

### LLM Instruction Prompt
- Do not use illustrative concrete filters like `Rotation` or `Watermark` in standalone snippets unless their exact constructors are known; instead, use an anonymous implementation of `ImageFilter`.
- `Pipeline` accepts instances of `ImageFilter` (via varargs or `List`), which is an interface requiring the implementation of `BufferedImage apply(BufferedImage img)`.
- `Pipeline.apply(BufferedImage)` returns a `BufferedImage` with all filters applied sequentially.

### Prompt Snippet
```text
To apply custom filters directly to a BufferedImage using the low-level Pipeline API, use an anonymous ImageFilter:
`Pipeline pipeline = new Pipeline(new ImageFilter() { public BufferedImage apply(BufferedImage img) { return img; } });`
`BufferedImage result = pipeline.apply(bufferedImage);`
```

### Common Failure Modes
- **Guessing Concrete Constructors**: Blindly copying illustrative concrete filters (e.g., `new Rotation(90)`) without knowing their exact constructor signatures, leading to compilation errors (`constructor Rotation in class Rotation cannot be applied to given types`).
- **ADVANCED/LOW-LEVEL Misuse**: Using this API for standard thumbnail generation instead of the fluent `Thumbnails` API. (This API should be excluded from standard user-facing denominators).
- **Null Inputs**: Passing a null array or list to the constructor, or passing a null filter to `add()`, throws a `NullPointerException`.

### Fix Code Hint
```java
// BAD: Guessing concrete filter constructors that are not in context
net.coobird.thumbnailator.filters.Pipeline pipeline = 
    new net.coobird.thumbnailator.filters.Pipeline(new net.coobird.thumbnailator.filters.Rotation(90));

// GOOD: Using an anonymous ImageFilter implementation for safe compilation
net.coobird.thumbnailator.filters.Pipeline pipeline = 
    new net.coobird.thumbnailator.filters.Pipeline(new net.coobird.thumbnailator.filters.ImageFilter() {
        @Override
        public java.awt.image.BufferedImage apply(java.awt.image.BufferedImage image) {
            return image;
        }
    });
```