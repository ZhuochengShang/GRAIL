## API Test: `ThumbnailMaker`

### Signature
```java
public ThumbnailMaker()
```
_Source: source/src/main/java/net/coobird/thumbnailator/makers/ThumbnailMaker.java:163_

_Source doc:_ Creates and initializes an instance of {@link ThumbnailMaker}.

### Goal
Creates and initializes a new instance of `ThumbnailMaker` for advanced, manual thumbnail generation workflows.

### Parameters
_None._

### Input
No arguments are required to invoke the constructor. 

### Output
Returns `unspecified` (Constructor) — A newly initialized instance of `ThumbnailMaker` that can be subsequently configured to process `BufferedImage` objects.

### Valid Call Patterns
```java
// Inferred from signature (not verified by tests)
ThumbnailMaker maker = new ThumbnailMaker();
```

### LLM Instruction Prompt
- Use `new ThumbnailMaker()` ONLY when constructing advanced, custom image processing pipelines that cannot be satisfied by the standard fluent builder.
- Strongly prefer the fluent API (`Thumbnails.of(...)`) over manual `ThumbnailMaker` instantiation for standard resizing, cropping, and filtering tasks, as the fluent API automatically handles boilerplate `Graphics2D` manipulation and Image I/O.
- If using this low-level class, you must manually configure the rendering hints, resizers, and image filters.

### Prompt Snippet
```text
// Advanced usage for custom pipelines
ThumbnailMaker maker = new ThumbnailMaker(); 
// Note: The fluent API (Thumbnails.of(...)) is strictly preferred for standard usage.
```

### Common Failure Modes
- **Missing Default Configurations**: Manually instantiating `ThumbnailMaker` and failing to configure necessary parameters (like a `Resizer` or `ImageFilter` pipeline) that the fluent `Thumbnails.Builder` handles automatically.
- **Missing Exif Orientation**: Failing to parse and apply Exif metadata. The fluent API handles this automatically, but when using low-level makers, developers often forget to use `ExifUtils.getExifOrientation` and `ExifFilterUtils.getFilterForOrientation` to correct image rotation before processing.

### Fix Code Hint
```java
// Instead of manually wiring a ThumbnailMaker, use the strictly preferred fluent API:
BufferedImage thumbnail = Thumbnails.of(originalImage)
    .size(640, 480)
    .asBufferedImage();
```