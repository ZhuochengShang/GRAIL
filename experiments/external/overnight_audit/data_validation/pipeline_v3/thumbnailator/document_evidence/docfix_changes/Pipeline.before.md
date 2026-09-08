## API Test: `Pipeline`

### Signature
```java
public Pipeline()
public Pipeline(ImageFilter... filters)
public Pipeline(List<ImageFilter> filters)
```
_Source: source/src/main/java/net/coobird/thumbnailator/filters/Pipeline.java:73  (+2 more definition site/overload)_

_Source doc:_ Instantiates a new {@link Pipeline} with an array of {@link ImageFilter}s to apply. @param filters		An array of {@link ImageFilter}s to apply.

### Goal
Instantiates a new image processing pipeline that sequentially applies a collection of `ImageFilter` transformations to a `BufferedImage`.

### Parameters
- `filters` (`ImageFilter...`): An array (or varargs) of `ImageFilter` implementations (such as `Rotation`, `Watermark`, `Canvas`, or `Colorize`) to apply in order.

### Input
The caller must provide zero or more `ImageFilter` objects. If using the `List` overload, a valid `List<ImageFilter>` must be provided. The resulting `Pipeline` is designed to process in-memory `BufferedImage` objects via its `apply(BufferedImage)` method. 

### Output
Returns `unspecified` — a new `Pipeline` instance representing an ordered, executable sequence of image filters ready to transform a `BufferedImage`.

### Valid Call Patterns
```java
// 1. Using the varargs constructor
BufferedImage img = new BufferedImage(200, 200, BufferedImage.TYPE_INT_ARGB);
ImageFilter filter1 = mock(ImageFilter.class); // In production, use a real filter e.g., new Rotation(90)

Pipeline pipeline = new Pipeline(filter1);
pipeline.apply(img);

// 2. Using the List constructor
Pipeline listPipeline = new Pipeline(Arrays.asList(filter1));
listPipeline.apply(img);
```

### LLM Instruction Prompt
- Use `Pipeline` only when low-level, direct manipulation of a `BufferedImage` is strictly required (e.g., inside custom `ThumbnailTask` implementations). 
- For standard image processing and thumbnail generation, strictly prefer the fluent `Thumbnails.Builder` API (e.g., `Thumbnails.of(...).addFilter(...)`), which automatically handles Image I/O, Exif orientation, and boilerplate `Graphics2D` operations.
- When constructing a `Pipeline`, ensure the order of filters is logically sound (e.g., applying a `Canvas` crop before a `Watermark` may change the watermark's relative positioning).

### Prompt Snippet
```text
To apply a sequence of custom filters directly to an in-memory BufferedImage outside the standard builder, instantiate a Pipeline:
`Pipeline pipeline = new Pipeline(new Rotation(90), new Watermark(...)); pipeline.apply(bufferedImage);`
Note: For standard file/stream workflows, always use `Thumbnails.of().addFilter()` instead.
```

### Common Failure Modes
- **Bypassing Exif Correction**: Manually applying a `Pipeline` to a `BufferedImage` bypasses the automatic Exif orientation parsing (`ExifUtils.getExifOrientation`) provided by the fluent `Thumbnails` API, potentially resulting in incorrectly rotated images.
- **Null Inputs**: Passing a null array or list to the constructor, or passing a null `BufferedImage` to `apply()`, will result in a `NullPointerException`.
- **Missing Image I/O**: `Pipeline` only operates on `BufferedImage`. It cannot read from or write to files, streams, or URLs directly.

### Fix Code Hint
```java
// BAD: Manually managing a Pipeline and Image I/O for standard thumbnail generation
BufferedImage img = ImageIO.read(new File("input.jpg"));
Pipeline pipeline = new Pipeline(new Rotation(90));
pipeline.apply(img);
ImageIO.write(img, "jpg", new File("output.jpg"));

// GOOD: Use the strictly preferred fluent API which handles I/O and pipelines automatically
Thumbnails.of(new File("input.jpg"))
    .scale(1.0) // Required by builder if not resizing
    .addFilter(new Rotation(90))
    .toFile(new File("output.jpg"));
```