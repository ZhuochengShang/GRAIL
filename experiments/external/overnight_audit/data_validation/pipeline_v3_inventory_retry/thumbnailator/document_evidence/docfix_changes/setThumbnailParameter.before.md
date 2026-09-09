## API Test: `setThumbnailParameter`

### Signature
```java
public void setThumbnailParameter(ThumbnailParameter param)
```
_Source: source/src/main/java/net/coobird/thumbnailator/tasks/io/AbstractImageSink.java:58  (+6 more definition site/overload)_

### Goal
Sets the `ThumbnailParameter` configuration object on an image source or sink to dictate the parameters (such as size, region, and output format) to use when reading, processing, or storing the image.

### Parameters
- `param` (`ThumbnailParameter`): The configuration object containing image reading, processing, and writing parameters. This is typically constructed using a `ThumbnailParameterBuilder`.

### Input
An instantiated `ImageSource` (e.g., `BufferedImageSource`, `FileImageSource`) or `ImageSink` (e.g., `FileImageSink`, `OutputStreamImageSink`). The caller must provide a fully constructed `ThumbnailParameter` instance containing the desired dimensions, regions, or formatting rules. 

### Output
Returns `void` — mutates the state of the target `ImageSource` or `ImageSink` by assigning the provided parameters for subsequent `read()` or `write()` operations.

### Valid Call Patterns
```java
// given
BufferedImage sourceImage = getImageFromResource("Thumbnailator/grid.png");
BufferedImageSource source = new BufferedImageSource(sourceImage);

// configure the source with parameters before reading
source.setThumbnailParameter(
    new ThumbnailParameterBuilder()
        .region(new Region(Positions.TOP_LEFT, new AbsoluteSize(40, 40)))
        .size(20, 20)
        .build()
);

// when
BufferedImage img = source.read();
```

### LLM Instruction Prompt
- When interacting with low-level `ImageSource` or `ImageSink` objects directly in advanced workflows, you must configure them by passing a `ThumbnailParameter` (built via `ThumbnailParameterBuilder`) to `setThumbnailParameter` before invoking `read()` or `write()`. 
- Note that the fluent `Thumbnails.of(...)` API is strictly preferred for standard workflows; only use `setThumbnailParameter` when manually constructing `ThumbnailTask`, `ImageSource`, or `ImageSink` pipelines.

### Prompt Snippet
```text
To configure a low-level Thumbnailator ImageSource or ImageSink, call `source.setThumbnailParameter(new ThumbnailParameterBuilder().size(w, h).build());` before executing `read()` or `write()`. Prefer the fluent `Thumbnails.of()` API for standard use cases.
```

### Common Failure Modes
- **Unconfigured Source/Sink**: Forgetting to call `setThumbnailParameter` before calling `read()` on an `ImageSource` or `write()` on an `ImageSink`, which can result in missing sizing constraints or default/unintended behavior.
- **Unnecessary Low-Level Usage**: Manually instantiating sources/sinks and calling `setThumbnailParameter` when the task could be safely and deterministically handled by the preferred fluent builder (`Thumbnails.of(...).size(...).asBufferedImage()`).
- **Null Parameter**: Passing `null` instead of a valid `ThumbnailParameter` object, leading to `NullPointerException` during the read/write phase.

### Fix Code Hint
```java
// Incorrect: Attempting to read from a source without configuring parameters
BufferedImageSource source = new BufferedImageSource(myImage);
// BufferedImage img = source.read(); // May lack required sizing context

// Correct: Build and set the ThumbnailParameter first
source.setThumbnailParameter(
    new ThumbnailParameterBuilder()
        .size(100, 100)
        .build()
);
BufferedImage img = source.read();
```