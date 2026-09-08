## API Test: `getOrientationFromExif`

### Signature
```java
public static Orientation getOrientationFromExif(byte[] exifData)
```
_Source: source/src/main/java/net/coobird/thumbnailator/util/exif/ExifUtils.java:109_

_Source doc:_ Returns the orientation obtained from the Exif metadata. @param exifData		A byte array containing Exif data. @return				The orientation information obtained from the Exif metadata, as a {@link Orientation} enum. Returns {@code null} if no orientation is found.

### Goal
Parses a byte array of Exif metadata to extract the image's orientation information.

### Parameters
- `exifData` (`byte[]`): A byte array containing the raw Exif data extracted from an image.

### Input
Raw Exif metadata bytes. The caller is responsible for extracting this byte array from the image file or stream prior to calling this method.

### Output
Returns `Orientation` — an enum representing the orientation state found in the Exif data. Returns `null` if no orientation tag is found in the provided bytes.

### Valid Call Patterns
```java
// Note: Example inferred from signature (not verified by test suite)
byte[] exifBytes = /* ... extract Exif bytes from image ... */;
Orientation orientation = ExifUtils.getOrientationFromExif(exifBytes);

if (orientation != null) {
    // Use orientation to correct image rotation
}
```

### LLM Instruction Prompt
- Use `ExifUtils.getOrientationFromExif(byte[])` to parse raw Exif bytes into an `Orientation` enum. Always check if the returned `Orientation` is `null` before passing it to other utilities (such as `ExifFilterUtils.getFilterForOrientation(Orientation)`) to avoid `NullPointerException`s.

### Prompt Snippet
```text
When parsing Exif data to determine image orientation, call `ExifUtils.getOrientationFromExif(byte[])`. You must check for a `null` return value, which indicates no orientation metadata was found in the provided byte array.
```

### Common Failure Modes
- **`NullPointerException` on Return Value**: Failing to check if the returned `Orientation` is `null` before invoking methods on it or passing it to `ExifFilterUtils.getFilterForOrientation(Orientation)`. The method explicitly returns `null` when the orientation tag is missing.

### Fix Code Hint
```java
Orientation orientation = ExifUtils.getOrientationFromExif(exifBytes);
if (orientation != null) {
    // Safe to use the orientation enum
    ImageFilter filter = ExifFilterUtils.getFilterForOrientation(orientation);
}
```