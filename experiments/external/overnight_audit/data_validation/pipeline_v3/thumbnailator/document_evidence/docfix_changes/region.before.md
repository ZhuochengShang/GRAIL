## API Test: `region`

### Signature
```java
public ThumbnailParameterBuilder region(Region sourceRegion)
```
_Source: source/src/main/java/net/coobird/thumbnailator/builders/ThumbnailParameterBuilder.java:200_

_Source doc:_ Sets the region of the source image to use when creating a thumbnail. @param sourceRegion		The region of the source image to use when creating a thumbnail. @return			A reference to this object. @since	0.3.4

### Goal
Sets the specific rectangular area of the source image to be extracted and used as the base for the thumbnail generation process.

### Parameters
- `sourceRegion` (`Region`): The specific area of the source image to extract. This is typically constructed using a `Position` (such as the `Positions` enum or a `Coordinate`) and a `Size` (such as `AbsoluteSize`).

### Input
The caller must provide a valid `Region` object from the `net.coobird.thumbnailator.geometry` package. This method is called on an active `ThumbnailParameterBuilder` instance, which is typically used when constructing custom `ThumbnailTask` instances or configuring lower-level image sources (like `BufferedImageSource`). 

### Output
Returns `ThumbnailParameterBuilder` — A reference to the current builder instance to allow fluent method chaining.

### Valid Call Patterns
```java
// Extracting a region using a predefined Position (TOP_LEFT)
ThumbnailParameter params1 = new ThumbnailParameterBuilder()
    .region(new Region(Positions.TOP_LEFT, new AbsoluteSize(40, 40)))
    .size(20, 20)
    .build();

// Extracting a region using exact Coordinates
ThumbnailParameter params2 = new ThumbnailParameterBuilder()
    .region(new Region(new Coordinate(20, 20), new AbsoluteSize(100, 100)))
    .size(80, 80)
    .build();
```

### LLM Instruction Prompt
- When configuring a `ThumbnailParameterBuilder` to process only a sub-section of a source image, use `region(Region)`. 
- Construct the `Region` argument using `net.coobird.thumbnailator.geometry` classes: provide a `Position` (e.g., `Positions.TOP_LEFT` or `new Coordinate(x, y)`) and a `Size` (e.g., `new AbsoluteSize(width, height)`).
- Always chain this call with other required builder methods (like `size(int, int)`) and terminate the chain with `build()`.

### Prompt Snippet
```text
Use `.region(new Region(new Coordinate(x, y), new AbsoluteSize(w, h)))` on the ThumbnailParameterBuilder to crop the source image to a specific area before resizing.
```

### Common Failure Modes
- **Oversized Regions (Clamping):** If the specified `Region` dimensions exceed the actual bounds of the source image (e.g., requesting a 100x100 region starting at coordinate 20,20 on a 100x100 image), the library does not throw an exception. Instead, it safely clamps the region to the available image bounds (resulting in an 80x80 subimage).
- **Missing Terminal Operation:** Forgetting to call `.build()` at the end of the `ThumbnailParameterBuilder` chain, which returns the actual `ThumbnailParameter` required by image sources.
- **Missing Size Configuration:** Failing to specify the final thumbnail dimensions (e.g., `.size(w, h)`) on the builder before calling `.build()`.

### Fix Code Hint
```java
// Ensure the Region is instantiated with valid geometry objects and the builder is terminated with .build()
ThumbnailParameter params = new ThumbnailParameterBuilder()
    .region(new Region(new Coordinate(x, y), new AbsoluteSize(cropWidth, cropHeight)))
    .size(targetWidth, targetHeight)
    .build();
```