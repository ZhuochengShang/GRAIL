## API Test: `UnsupportedFormatException`
_Grounding: doc-repaired from source (docfix)._

### Signature
```java
public UnsupportedFormatException(String formatName)
public UnsupportedFormatException(String formatName, String s)
public String getFormatName()
```
_Source: source/src/main/java/net/coobird/thumbnailator/tasks/UnsupportedFormatException.java:70_

### Goal
Instantiate and test `UnsupportedFormatException`, a specialized `IOException` used to signal that the host JVM lacks the necessary Image I/O plugins for a specific format. While typically thrown internally by Thumbnailator's I/O components at the terminal sink, testing this API requires direct instantiation.

### Parameters
- `formatName` (`String`): The name of the unsupported format (e.g., `"webp"`). Can be the constant `UnsupportedFormatException.UNKNOWN` if the format cannot be determined from the source data.
- `s` (`String`): A detailed error message providing context about the failure (e.g., `"No suitable ImageWriter found"`).

### Input
A string representing the unsupported format name (or `UnsupportedFormatException.UNKNOWN`) and an optional string containing the detailed error message. Passed directly to the public constructors for testing.

### Output
An initialized `UnsupportedFormatException` instance whose format name can be retrieved via `getFormatName()`.

### Valid Call Patterns
```java
import net.coobird.thumbnailator.tasks.UnsupportedFormatException;

// Instantiate using the single-argument constructor
UnsupportedFormatException ex1 = new UnsupportedFormatException("webp");
assert "webp".equals(ex1.getFormatName());

// Instantiate using the two-argument constructor and the UNKNOWN constant
UnsupportedFormatException ex2 = new UnsupportedFormatException(
    UnsupportedFormatException.UNKNOWN, 
    "No suitable ImageWriter found"
);
assert UnsupportedFormatException.UNKNOWN.equals(ex2.getFormatName());
assert "No suitable ImageWriter found".equals(ex2.getMessage());
```

### LLM Instruction Prompt
To test or use the `UnsupportedFormatException` API itself, instantiate it directly using its public constructors `(String formatName)` or `(String formatName, String message)`. The exception provides a `getFormatName()` method to retrieve the unsupported format name, and the class provides a `public static final String UNKNOWN` constant to represent unidentified formats. Do not attempt to trigger this exception organically via `Thumbnails.Builder.outputFormat(String)`.

### Prompt Snippet
```text
Instantiate `UnsupportedFormatException` directly using `new UnsupportedFormatException("format")` or `new UnsupportedFormatException(UnsupportedFormatException.UNKNOWN, "message")` to test its state and `getFormatName()` method.
```

### Common Failure Modes
- **Wrong Exception Expectation (Eager Validation):** Attempting to trigger this exception organically by passing an unsupported format (like `"superfakeformat"`) to `Thumbnails.Builder.outputFormat(String)`. `outputFormat(String)` eagerly validates the requested format against registered ImageIO writers and throws an `IllegalArgumentException` immediately. It does NOT throw `UnsupportedFormatException`. Consequently, the pipeline never reaches the terminal sink where `UnsupportedFormatException` is actually instantiated and thrown.

### Fix Code Hint
```java
// WRONG: Trying to trigger the exception organically via builder configuration
try {
    Thumbnails.of(new java.io.File("input.jpg"))
        .size(100, 100)
        .outputFormat("superfakeformat"); // Throws IllegalArgumentException eagerly!
} catch (net.coobird.thumbnailator.tasks.UnsupportedFormatException e) {
    // Unreachable
}

// CORRECT: Directly instantiate the exception to test its API
net.coobird.thumbnailator.tasks.UnsupportedFormatException ex = 
    new net.coobird.thumbnailator.tasks.UnsupportedFormatException(
        net.coobird.thumbnailator.tasks.UnsupportedFormatException.UNKNOWN, 
        "No suitable ImageWriter found"
    );
assert net.coobird.thumbnailator.tasks.UnsupportedFormatException.UNKNOWN.equals(ex.getFormatName());
```