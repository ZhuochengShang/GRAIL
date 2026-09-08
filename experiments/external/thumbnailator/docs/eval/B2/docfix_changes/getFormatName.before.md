## API Test: `getFormatName`

### Signature
```java
public String getFormatName()
```
_Source: source/src/main/java/net/coobird/thumbnailator/tasks/UnsupportedFormatException.java:80_

_Source doc:_ Returns the format name which is not supported. @return			Format name.

### Goal
Retrieves the name of the image format that caused an `UnsupportedFormatException` because it is not supported by the underlying Java Image I/O implementation.

### Parameters
_None._

### Input
An instance of `UnsupportedFormatException` caught during a Thumbnailator pipeline execution. This exception typically occurs when attempting to read an unrecognized file type or when explicitly requesting an output format (via `Thumbnails.Builder.outputFormat(String)`) that the host JVM does not support.

### Output
Returns `String` — the name of the unsupported format (e.g., `"tiff"`, `"webp"`, or a custom extension) that triggered the exception.

### Valid Call Patterns
```java
// Inferred from the signature (not verified in tests, as test examples show javax.imageio.ImageReader.getFormatName())
try {
    Thumbnails.of(new File("input.jpg"))
        .size(640, 480)
        .outputFormat("webp") // May not be supported by default Java 8 Image I/O
        .toFile(new File("output.webp"));
} catch (UnsupportedFormatException e) {
    String unsupported = e.getFormatName();
    System.err.println("The JVM does not support the requested format: " + unsupported);
}
```

### LLM Instruction Prompt
- When catching an `UnsupportedFormatException` during a Thumbnailator operation, call `getFormatName()` on the exception instance to extract the specific format string that failed.
- Use this method to provide informative error messages or to trigger fallback logic (e.g., falling back to universally supported formats like `"jpg"` or `"png"`).
- Do not confuse this Thumbnailator exception method with the standard Java `javax.imageio.ImageReader.getFormatName()` method.

### Prompt Snippet
```text
When a Thumbnailator pipeline throws an `UnsupportedFormatException`, use `e.getFormatName()` to identify which format string the JVM's Image I/O rejected. Thumbnailator relies entirely on the host JVM for format support and has no external dependencies.
```

### Common Failure Modes
- **Assuming format support:** Developers often assume formats like WebP, HEIC, or TIFF are supported by default. Because Thumbnailator relies entirely on the host JVM's standard Image I/O capabilities, requesting these without the appropriate Image I/O plugins on the classpath will throw an `UnsupportedFormatException`.
- **Special constant values:** If the format was never explicitly set but could not be determined, the exception might carry the internal `ThumbnailParameter.DETERMINE_FORMAT` constant (which is `"\0"`) or `null`.

### Fix Code Hint
```java
try {
    Thumbnails.of(inputFile)
        .size(200, 200)
        .outputFormat(desiredFormat)
        .toFile(outputFile);
} catch (UnsupportedFormatException e) {
    // Fallback to a universally supported format if the requested one fails
    System.out.println("Format '" + e.getFormatName() + "' is unsupported. Falling back to JPEG.");
    Thumbnails.of(inputFile)
        .size(200, 200)
        .outputFormat("jpg")
        .toFile(new File(outputFile.getParentFile(), "fallback.jpg"));
}
```