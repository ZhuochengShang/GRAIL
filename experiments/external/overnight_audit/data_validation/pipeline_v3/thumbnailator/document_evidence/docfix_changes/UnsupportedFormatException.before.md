## API Test: `UnsupportedFormatException`

### Signature
```java
public UnsupportedFormatException(String formatName)
public UnsupportedFormatException(String formatName, String s)
```
_Source: source/src/main/java/net/coobird/thumbnailator/tasks/UnsupportedFormatException.java:70  (+1 more definition site/overload)_

_Source doc:_ Instantiates a {@link UnsupportedFormatException} with the unsupported format and a detailed message. @param formatName	Format name. @param s				A message detailing the exception.

### Goal
Instantiates an exception indicating that a requested image format is not supported by the host JVM's Java Image I/O capabilities.

### Parameters
- `formatName` (`String`): The name of the image format that could not be processed (e.g., "tiff", "webp").
- `s` (`String`): A detailed message explaining the exception context (e.g., "No suitable ImageWriter found").

### Input
A string representing the unsupported format name and a string containing the detailed error message. This is typically invoked internally when `Thumbnails.Builder.outputFormat(String)` specifies a format lacking a registered Java Image I/O reader or writer in the current environment.

### Output
Returns `unspecified` — yields a new `UnsupportedFormatException` instance to be thrown by the pipeline.

### Valid Call Patterns
```java
// Inferred from signature (not verified)
UnsupportedFormatException exception = new UnsupportedFormatException("webp", "No suitable ImageWriter found for webp.");
throw exception;
```

### LLM Instruction Prompt
- When configuring image pipelines with `outputFormat(String)`, anticipate `UnsupportedFormatException` if the target format is not supported by the standard Java 8 Image I/O (e.g., formats other than JPEG, PNG, GIF, BMP). Do not assume support for modern formats like WebP or HEIC unless external Image I/O plugins are explicitly guaranteed by the environment.

### Prompt Snippet
```text
Catch UnsupportedFormatException when calling terminal sink methods (like `toFile()` or `toOutputStream()`) on a Thumbnails.Builder if a non-standard `outputFormat` was requested.
```

### Common Failure Modes
- **Missing Image I/O Plugin**: A user specifies `.outputFormat("tiff")` or `.outputFormat("webp")` on a standard Java 8 JVM without external Image I/O plugins on the classpath. Thumbnailator will throw this exception during the terminal sink operation because it relies entirely on the host JVM's standard Image I/O capabilities.

### Fix Code Hint
```java
try {
    Thumbnails.of(new File("input.jpg"))
        .size(640, 480)
        .outputFormat("webp") // May throw UnsupportedFormatException on standard Java 8
        .toFile(new File("output.webp"));
} catch (UnsupportedFormatException e) {
    // Fallback to a universally supported format
    Thumbnails.of(new File("input.jpg"))
        .size(640, 480)
        .outputFormat("jpg")
        .toFile(new File("output.jpg"));
}
```