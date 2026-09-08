## API Test: `getFormatName`
_Grounding: doc-repaired from source (docfix)._

### Signature
```java
public String getFormatName()
```

### Goal
Retrieves the name of the image format that caused an `UnsupportedFormatException`. For testing purposes, this exception is instantiated directly.

### Parameters
_None._

### Input
An instance of `net.coobird.thumbnailator.tasks.UnsupportedFormatException`. For programmatic testing, instantiate directly via its public constructor: `new UnsupportedFormatException(String formatName, String message)`.

### Output
Returns `String` — the name of the unsupported format assigned during the exception's construction.

### Valid Call Patterns
```java
import net.coobird.thumbnailator.tasks.UnsupportedFormatException;

public class FormatNameTest {
    public static void main(String[] args) {
        String expectedFormat = "superfakeformat";
        UnsupportedFormatException ex = new UnsupportedFormatException(expectedFormat, "Format not supported");
        
        String actualFormat = ex.getFormatName();
        
        assert expectedFormat.equals(actualFormat) : "Format name should match the unsupported format requested";
        System.out.println("__CHECK__ getFormatName " + actualFormat);
    }
}
```

### LLM Instruction Prompt
- `Thumbnails.Builder.outputFormat(String)` eagerly validates the format and throws an `IllegalArgumentException` if it is unsupported, NOT an `UnsupportedFormatException`.
- `UnsupportedFormatException` is typically thrown deeper in the pipeline during read/write task execution when the underlying Image I/O fails.
- For testing or programmatic creation, `UnsupportedFormatException` must be directly instantiated using its public constructor.

### Prompt Snippet
```text
Do not catch `UnsupportedFormatException` from `outputFormat(String)`—it throws `IllegalArgumentException`. To test `getFormatName()`, instantiate `UnsupportedFormatException` directly.
```

### Common Failure Modes
- **Wrong Exception Expectation:** Attempting to trigger an `UnsupportedFormatException` by passing an invalid format to `Thumbnails.Builder.outputFormat(String)`. This fails because `outputFormat()` performs eager validation and immediately throws an `IllegalArgumentException` instead.

### Fix Code Hint
```java
// WRONG: Expecting UnsupportedFormatException from outputFormat()
try {
    Thumbnails.of("in.jpg").outputFormat("superfakeformat").toFile("out.jpg");
} catch (net.coobird.thumbnailator.tasks.UnsupportedFormatException e) {
    System.out.println(e.getFormatName());
}

// CORRECT: Test getFormatName by direct instantiation
net.coobird.thumbnailator.tasks.UnsupportedFormatException ex = 
    new net.coobird.thumbnailator.tasks.UnsupportedFormatException("superfakeformat", "Format not supported");
String format = ex.getFormatName();
```