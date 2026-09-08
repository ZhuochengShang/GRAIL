## API Test: `getExifOrientation`

### Signature
```java
public static Orientation getExifOrientation(ImageReader reader, int imageIndex)
```
_Source: source/src/main/java/net/coobird/thumbnailator/util/exif/ExifUtils.java:69_

_Source doc:_ Returns the orientation obtained from the Exif metadata. @param reader		An {@link ImageReader} which is reading the target image. @param imageIndex	The index of the image from which the Exif metadata should be read from. @return				The orientation information obtained from the Exif metadata, as a {@link Orientation} enum. Returns {@code null} if no orientation is found. @throws IOException				When an error occurs during reading. @throws IllegalArgumentException	If the {@link ImageReader} does not have the target image set, or if the reader does not have a JPEG open.

### Goal
Extracts the Exif orientation metadata from a JPEG image to determine if the image requires rotation correction before processing.

### Parameters
- `reader` (`ImageReader`): An `ImageReader` instance that is currently reading the target JPEG image and has its input source explicitly set.
- `imageIndex` (`int`): The zero-based index of the image within the input source from which the Exif metadata should be read (typically `0` for standard single-frame JPEGs).

### Input
The caller must provide an initialized `ImageReader` that specifically has a JPEG open. A critical precondition is that the reader must have its input set (e.g., via `reader.setInput(ImageIO.createImageInputStream(...))`) before calling this method. 

### Output
Returns `Orientation` — An enum representing the orientation information parsed from the Exif metadata (values typically corresponding to Exif tags 1 through 8). Returns `null` if no orientation metadata is found in the image.

### Valid Call Patterns
```java
// given
ImageReader reader = ImageIO.getImageReadersByFormatName("jpg").next();
InputStream is = new FileInputStream("image_with_exif.jpg");
reader.setInput(ImageIO.createImageInputStream(is));

// when
Orientation orientation = ExifUtils.getExifOrientation(reader, 0);
is.close();

// then (use the orientation to correct the image pipeline)
if (orientation != null) {
    // e.g., ExifFilterUtils.getFilterForOrientation(orientation)
}
```

### LLM Instruction Prompt
- When calling `ExifUtils.getExifOrientation`, you MUST ensure the `ImageReader` has its input set via `reader.setInput(...)` prior to the call.
- You MUST ensure the `ImageReader` is processing a JPEG image; otherwise, an `IllegalArgumentException` will be thrown.
- You MUST handle the case where the returned `Orientation` is `null` (which occurs when the image lacks Exif orientation metadata).

### Prompt Snippet
```text
To extract Exif orientation safely, initialize a JPEG `ImageReader`, set its input using `ImageIO.createImageInputStream`, and call `ExifUtils.getExifOrientation(reader, 0)`. Always check if the returned `Orientation` is null before passing it to `ExifFilterUtils.getFilterForOrientation`.
```

### Common Failure Modes
- **`IllegalArgumentException`**: Thrown if the `ImageReader` does not have the target image set (i.e., `setInput` was not called) or if the reader does not have a JPEG open.
- **`IOException`**: Thrown if an error occurs while reading the underlying image stream.
- **`NullPointerException`**: Occurs if the caller attempts to use the returned `Orientation` without checking for `null` when processing an image that lacks Exif metadata.

### Fix Code Hint
```java
ImageReader reader = ImageIO.getImageReadersByFormatName("jpg").next();
// FIX: Must set input before calling getExifOrientation
try (ImageInputStream iis = ImageIO.createImageInputStream(inputStream)) {
    reader.setInput(iis);
    Orientation orientation = ExifUtils.getExifOrientation(reader, 0);
    
    // FIX: Must check for null
    if (orientation != null) {
        ImageFilter rotationFilter = ExifFilterUtils.getFilterForOrientation(orientation);
        // apply filter...
    }
} finally {
    reader.dispose();
}
```