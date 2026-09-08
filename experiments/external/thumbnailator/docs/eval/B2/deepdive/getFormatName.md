# Deep-dive: `getFormatName`

model: google:gemini-3.1-pro-preview · tokens in=3,035 out=3,837 · wall 34s · 2026-09-08 01:56

---

Write the report in EXACTLY these layers:

L0 AUDIENCE + TESTABILITY CLASSIFICATION
USER-FACING. TESTABLE FROM PUBLIC INPUTS.
The API is a public getter on a public exception class. While it is intended to be caught during pipeline execution, the exception itself has public constructors (`new UnsupportedFormatException(String)`), making it trivially testable by direct instantiation without needing to force a complex pipeline failure.

L1 PURPOSE
This API retrieves the name of the image format that caused an `UnsupportedFormatException`. It sits at the error-handling boundary of the library, allowing users to programmatically inspect which format string was rejected (e.g., during read or write operations) rather than parsing the exception message.

L2 CONTRACT
- **Receiver:** `UnsupportedFormatException`. It can be obtained by catching it during a Thumbnailator operation that fails due to an unsupported format, or by explicitly instantiating it via `new UnsupportedFormatException(String)` or `new UnsupportedFormatException(String, String)`.
- **Parameters:** None.
- **Return value:** `String` representing the unsupported format name.
- **Visibility:** `public`.
- **Thread-safety:** The `formatName` field is not marked `final` in the provided snippet, but it is only set in the constructor and has no setters, making it effectively immutable and thread-safe (INFERENCE: assuming no reflection or subclass mutation).

L3 MECHANICS
The method simply returns the `formatName` instance variable that was assigned during the object's construction (`source/src/main/java/net/coobird/thumbnailator/tasks/UnsupportedFormatException.java:81`). 

*Note on provided call sites:* The real call sites provided in the context (e.g., `FileImageSink.java:247`, `InputStreamImageSource.java:525`, `TestUtils.java:74`) do *not* actually invoke `UnsupportedFormatException.getFormatName()`. Instead, they invoke `javax.imageio.ImageReader.getFormatName()` or a static test utility method with the same name. The repository context shows no internal invocations of the exception's getter.

L4 CORRECT MINIMAL USAGE
```java
import net.coobird.thumbnailator.tasks.UnsupportedFormatException;

public class MinimalUsage {
    public static void main(String[] args) {
        // Directly instantiating the exception to test the getter
        // without needing to trigger a complex pipeline failure.
        UnsupportedFormatException ex = new UnsupportedFormatException("superfakeformat", "Format not supported");
        
        String format = ex.getFormatName();
        
        if (!"superfakeformat".equals(format)) {
            throw new IllegalStateException("Expected format name to match");
        }
    }
}
```

L5 FAILURE FORENSICS
The recorded failure attempted to trigger an `UnsupportedFormatException` by passing an invalid format (`"superfakeformat"`) to `Thumbnails.Builder.outputFormat()`. However, the test failed with an `IllegalArgumentException: Specified format is not supported: superfakeformat`. This reveals that `outputFormat()` performs eager validation of the requested format against the JVM's available `ImageWriter`s and throws an `IllegalArgumentException` immediately, rather than deferring the failure to the task execution phase where an `UnsupportedFormatException` might be thrown. The test failed because it expected the wrong exception type for that specific builder method.

L6 SELF-ASSESSMENT
- INFERENCE: I infer that `UnsupportedFormatException` extends a standard Java exception class (like `RuntimeException` or `IOException`) because it calls `super()` and `super(s)` and ends with "Exception".
- INFERENCE: I infer that the `formatName` field is effectively immutable since no setters are visible in the provided source.
- To be certain about where `UnsupportedFormatException` is actually thrown by the library, I would need to see the source code of the task execution classes (like `ReadTasks` or `WriteTasks`), as the provided context does not show any `throw new UnsupportedFormatException(...)` statements.
- Confidence score for L2: 10/10 - The signature and constructors are fully provided in the source snippet.
- Confidence score for L3: 10/10 - The method implementation is a trivial getter (`return formatName;`).
- Confidence score for L4: 10/10 - Direct instantiation of an exception class is standard Java and relies only on the provided public constructors.