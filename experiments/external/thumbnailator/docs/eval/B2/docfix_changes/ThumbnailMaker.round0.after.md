## API Test: `ThumbnailMaker`
_Grounding: doc-repaired from source (docfix)._

### Signature
```java
public ThumbnailMaker()
```

### Goal
Initializes foundational state (readiness tracker, default ARGB image type, default resizer factory) for an INTERNAL/FRAMEWORK thumbnail generation strategy. Note: This is an abstract base class excluded from the main user-facing denominator; standard users should use the fluent `Thumbnails` API instead.

### Parameters
_None._

### Input
No arguments. Because this is an INTERNAL/FRAMEWORK abstract class, execution requires explicit low-level construction via an anonymous concrete subclass implementing `make(BufferedImage)`.

### Output
Returns an initialized instance of the concrete subclass.

### Valid Call Patterns
```java
import net.coobird.thumbnailator.makers.ThumbnailMaker;
import java.awt.image.BufferedImage;

// ThumbnailMaker is abstract; instantiate via an anonymous concrete subclass
ThumbnailMaker maker = new ThumbnailMaker() {
    @Override
    public BufferedImage make(BufferedImage img) {
        // Delegate to the protected helper method provided by the base class
        return makeThumbnail(img, 100, 100);
    }
};

// Caller-owned objects
BufferedImage img = new BufferedImage(200, 200, BufferedImage.TYPE_INT_ARGB);
BufferedImage result = maker.make(img);
```

### LLM Instruction Prompt
- `ThumbnailMaker` is an `abstract` class and cannot be instantiated directly.
- To use this class, callers must define a concrete subclass (e.g., via an anonymous inner class) that implements the `public abstract BufferedImage make(BufferedImage img)` method.
- The snippet `new ThumbnailMaker();` is incorrect and must be replaced with an anonymous subclass implementation.

### Prompt Snippet
```text
// INTERNAL/FRAMEWORK usage requires an anonymous subclass
ThumbnailMaker maker = new ThumbnailMaker() {
    @Override
    public BufferedImage make(BufferedImage img) {
        return makeThumbnail(img, 100, 100);
    }
};
```

### Common Failure Modes
- **Direct Instantiation of Abstract Class**: Attempting `new ThumbnailMaker()` fails with `ThumbnailMaker is abstract; cannot be instantiated`. You must provide a concrete implementation of the `make` method.
- **Internal/Framework Misuse**: Using this low-level abstract class instead of the fluent `Thumbnails` API for standard user-facing tasks. This API is excluded from the main user-facing denominator.

### Fix Code Hint
```java
// WRONG: Fails to compile because ThumbnailMaker is abstract
ThumbnailMaker maker = new ThumbnailMaker();

// CORRECT: Provide a concrete subclass implementation
ThumbnailMaker maker = new ThumbnailMaker() {
    @Override
    public BufferedImage make(BufferedImage img) {
        return makeThumbnail(img, 100, 100);
    }
};
```