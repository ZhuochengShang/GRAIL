## API Test: `getOutputFormat`

### Signature
```java
public String getOutputFormat()
```
_Source: source/src/main/java/net/coobird/thumbnailator/ThumbnailParameter.java:878_

_Source doc:_ Returns the output format for the thumbnail. <p> If the output format is to use the same compression format as the original image, this method will return {@link ThumbnailParameter#ORIGINAL_FORMAT}. <p> If the output format should be determined from the information available such as the file name of the thumbnail, then this method will return {@link ThumbnailParameter#DETERMINE_FORMAT}. @return 		The output format for the thumbnail.

### Goal
Retrieves the configured output format string for the thumbnail generation task, which may be a specific format name or a constant indicating how the format should be resolved.

### Parameters
_None._

### Input
A valid, instantiated `ThumbnailParameter` object, typically constructed using a `ThumbnailParameterBuilder` or extracted from an active thumbnail pipeline.

### Output
Returns `String` — The output format for the thumbnail. This will be a specific format string (e.g., `"jpg"`, `"png"`), `ThumbnailParameter.ORIGINAL_FORMAT` if it is configured to match the source image's compression format, or `ThumbnailParameter.DETERMINE_FORMAT` (value `"\0"`) if the format should be inferred from the output destination (such as the file extension).

### Valid Call Patterns
```java
ThumbnailParameter param = new ThumbnailParameterBuilder()
        .size(100, 100)
        .build();

String format = param.getOutputFormat();

// The default behavior when no format is explicitly set is to retain the original format
if (ThumbnailParameter.ORIGINAL_FORMAT.equals(format)) {
    // Format will match the source image
}
```

### LLM Instruction Prompt
- When inspecting a `ThumbnailParameter`'s output format, use `getOutputFormat()`.
- Do not assume the returned string is always a standard file extension or Image I/O format name (like `"jpg"`). You MUST check if the returned string equals `ThumbnailParameter.ORIGINAL_FORMAT` or `ThumbnailParameter.DETERMINE_FORMAT` before passing it to standard Java Image I/O APIs.
- Use this method when building custom `ThumbnailTask` implementations or debugging pipeline configurations to verify the intended output format.

### Prompt Snippet
```text
When retrieving the output format from a `ThumbnailParameter` using `getOutputFormat()`, be prepared to handle the special constants `ThumbnailParameter.ORIGINAL_FORMAT` and `ThumbnailParameter.DETERMINE_FORMAT`. Do not pass the raw return value directly to `ImageIO.getImageWritersByFormatName()` without checking for these constants first.
```

### Common Failure Modes
- **Assuming a literal format string**: Blindly using the return value as a format name for `ImageIO` operations will fail if the value is `ThumbnailParameter.DETERMINE_FORMAT` (`"\0"`) or `ThumbnailParameter.ORIGINAL_FORMAT`.
- **NullPointerException**: Calling this method on an uninitialized or null `ThumbnailParameter` reference.

### Fix Code Hint
```java
String format = param.getOutputFormat();

if (ThumbnailParameter.ORIGINAL_FORMAT.equals(format)) {
    // Logic to extract format from the original ImageSource
} else if (ThumbnailParameter.DETERMINE_FORMAT.equals(format)) {
    // Logic to extract format from the destination filename/ImageSink
} else {
    // Safe to use 'format' as a literal format name (e.g., "jpg", "png")
    System.out.println("Explicit format requested: " + format);
}
```