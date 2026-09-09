## API Test: `region`
_Grounding: doc-repaired from source (docfix)._

### Signature
```java
public ThumbnailParameterBuilder region(Region sourceRegion)
```

### Goal
Sets the specific rectangular area of the source image to be extracted before resizing. Note: This is an ADVANCED/LOW-LEVEL API used for internal configuration and is recommended for inclusion only in the advanced/internal bucket.

### Parameters
- `sourceRegion` (`Region`): The specific area of the source image to extract.

### Input
The caller must provide a valid `Region` object. As an ADVANCED/LOW-LEVEL API, it is testable only with explicit low-level construction: the caller instantiates and owns a `ThumbnailParameterBuilder`, instantiates and owns a `Region` (using `Coordinate` and `AbsoluteSize`), and passes it to `region()`.

### Output
Returns `ThumbnailParameterBuilder` — A reference to the current builder instance (`this`) to allow fluent method chaining.

### Valid Call Patterns
```java
import net.coobird.thumbnailator.builders.ThumbnailParameterBuilder;
import net.coobird.thumbnailator.geometry.Region;
import net.coobird.thumbnailator.geometry.Coordinate;
import net.coobird.thumbnailator.geometry.AbsoluteSize;

// Explicit low-level construction for testing
Region expectedRegion = new Region(
    new Coordinate(10, 15),
    new AbsoluteSize(50, 60)
);

ThumbnailParameterBuilder builder = new ThumbnailParameterBuilder();
builder.region(expectedRegion);

// Note: To successfully terminate the builder chain, size must be configured
builder.size(20, 20).build();
```

### LLM Instruction Prompt
- The `region` method is called on a `ThumbnailParameterBuilder` instance and returns the builder itself.
- To test the API, simply instantiate a `ThumbnailParameterBuilder`, create a `Region` using `Coordinate` and `AbsoluteSize`, and pass it to `region()`.
- Do NOT attempt to call `calculate` on the `Region` object to verify bounds, as its signature may vary or be incompatible with simple `(int, int)` arguments.

### Prompt Snippet
```text
Instantiate a ThumbnailParameterBuilder, create a Region using Coordinate and AbsoluteSize, and pass it to region(). Do not call calculate() on the Region to verify bounds.
```

### Common Failure Modes
- **Hallucinating Verification Methods:** The previous snippet failed because it attempted to verify the result by calling `calculate(100, 100)` on the `Region` object. The arguments provided do not match the method's signature in this version of the library. Do not attempt to call `calculate` to verify bounds.
- **Advanced/Low-Level Misuse:** This is an ADVANCED/LOW-LEVEL API. It requires explicit low-level construction of `ThumbnailParameterBuilder` and `Region` rather than using the standard `Thumbnails` facade.
- **Missing Size Configuration:** Failing to specify the final thumbnail dimensions (e.g., `.size(w, h)`) on the builder before calling `.build()` throws an `IllegalStateException`.

### Fix Code Hint
```java
// WRONG: Hallucinating a calculate() method to verify bounds
Region region = new Region(new Coordinate(10, 15), new AbsoluteSize(50, 60));
ThumbnailParameterBuilder builder = new ThumbnailParameterBuilder();
builder.region(region);
region.calculate(100, 100); // Compilation error!

// CORRECT: Just pass the Region to the builder and terminate with size() and build()
Region expectedRegion = new Region(new Coordinate(10, 15), new AbsoluteSize(50, 60));
ThumbnailParameterBuilder builder = new ThumbnailParameterBuilder();
builder.region(expectedRegion)
       .size(20, 20)
       .build();
```