## API Test: `filters`

### Signature
```java
public ThumbnailParameterBuilder filters(List<ImageFilter> filters)
```
_Source: source/src/main/java/net/coobird/thumbnailator/builders/ThumbnailParameterBuilder.java:267_

_Source doc:_ Sets the {@link ImageFilter}s to apply to the thumbnail. <p> These filters will be applied after the original image is resized. @param filters		The output format type of the thumbnail. @return				A reference to this object.

### Goal
Sets a sequence of `ImageFilter` transformations to be applied to the image after the resizing step is complete.

### Parameters
- `filters` (`List<ImageFilter>`): A list of image filters (such as `Canvas`, `Caption`, `Colorize`, `Flip`, `Rotation`, `SwapDimensions`, `Transparency`, or `Watermark`) to apply sequentially to the thumbnail. *(Note: The original source Javadoc contains a typo referring to this as the "output format type", but it strictly accepts a list of filters).*

### Input
A valid `List` containing instantiated `ImageFilter` objects. The caller must be configuring a `ThumbnailParameterBuilder` (typically used in advanced workflows for constructing custom `ThumbnailTask` instances, rather than the standard `Thumbnails.of(...)` fluent API). 

### Output
Returns `ThumbnailParameterBuilder` — A reference to the current builder instance, allowing for fluent method chaining.

### Valid Call Patterns
```java
// Inferred from the signature (not verified by test suite)
ThumbnailParameterBuilder builder = new ThumbnailParameterBuilder();

List<ImageFilter> customFilters = Arrays.asList(
    new Rotation(90),
    new Watermark(Positions.BOTTOM_RIGHT, watermarkImage, 0.5f)
);

builder.filters(customFilters);
```

### LLM Instruction Prompt
- Use `filters(List<ImageFilter>)` when constructing a `ThumbnailParameterBuilder` to apply multiple transformations at once. 
- Remember that filters provided here are strictly applied **after** the original image is resized. 
- Do not confuse `ThumbnailParameterBuilder.filters(List)` with the standard fluent API's `Thumbnails.Builder.addFilter(ImageFilter)`. Use this method only when working directly with `ThumbnailParameterBuilder` in advanced task-abstraction workflows.

### Prompt Snippet
```text
When configuring a ThumbnailParameterBuilder, use `.filters(List<ImageFilter>)` to set the post-resize transformation pipeline. Note that these filters execute after resizing. For the standard `Thumbnails.of()` API, use `.addFilter()` instead.
```

### Common Failure Modes
- **Order of Operations Misconception**: Assuming the filters will be applied to the original, full-resolution image. The library explicitly applies these filters *after* the image has been resized.
- **API Confusion**: Attempting to call `.filters(List)` on a `Thumbnails.Builder` instance. The `Thumbnails.Builder` class uses `.addFilter(ImageFilter)` for adding filters one by one, whereas `.filters(List)` belongs to `ThumbnailParameterBuilder`.
- **Null Elements**: Passing a list that contains `null` elements may cause `NullPointerException`s during the pipeline execution when the library attempts to apply the transformations.

### Fix Code Hint
```java
// Incorrect: Trying to use filters(List) on the standard Thumbnails.Builder
// Thumbnails.of(file).size(100, 100).filters(myList); 

// Correct: Using addFilter on Thumbnails.Builder
Thumbnails.Builder<File> builder = Thumbnails.of(file).size(100, 100);
for (ImageFilter filter : myList) {
    builder.addFilter(filter);
}

// Correct: Using filters(List) on ThumbnailParameterBuilder
ThumbnailParameterBuilder paramBuilder = new ThumbnailParameterBuilder();
paramBuilder.size(100, 100).filters(myList);
```