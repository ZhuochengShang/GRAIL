# Deep-dive: `UnsupportedFormatException`

model: google:gemini-3.1-pro-preview · tokens in=3,393 out=3,487 · wall 32s · 2026-09-08 01:44

---

**L0 AUDIENCE + TESTABILITY CLASSIFICATION**
USER-FACING. 
TESTABLE FROM PUBLIC INPUTS.
This is a public exception class that users are expected to catch when configuring image pipelines with potentially unsupported formats. It can be tested standalone simply by invoking its public constructors with standard `String` inputs.

**L1 PURPOSE**
`UnsupportedFormatException` is a specialized `IOException` used to signal that the host JVM's Java Image I/O subsystem lacks the necessary plugins (readers or writers) to process a specific image format. It acts as a boundary exception between the standard `ImageIO` registry failures and Thumbnailator's task execution flow, typically originating in source or sink classes when reading from or writing to files and streams.

**L2 CONTRACT**
- **Constructors**: 
  - `public UnsupportedFormatException(String formatName)`
  - `public UnsupportedFormatException(String formatName, String s)`
- **Parameters**:
  - `formatName` (`String`): The name of the unsupported format (e.g., `"webp"`, `"tiff"`). Can be the constant `UnsupportedFormatException.UNKNOWN` (`"<unknown>"`) if the format cannot be determined from the source data.
  - `s` (`String`): A detailed error message providing context about the failure (e.g., `"No suitable ImageWriter found for webp."`).
- **Return value**: An initialized `UnsupportedFormatException` instance.
- **Visibility**: `public`.
- **Thread-safety**: Instances are immutable (the `formatName` field is `final` and `String` is immutable) and safe to share, though exceptions are typically thread-confined to the throwing thread.

**L3 MECHANICS**
The constructors delegate to the superclass (`IOException`) constructors—either `super()` or `super(s)`—and assign the provided `formatName` to a `private final String` field. This exception is instantiated and thrown internally by Thumbnailator's I/O components (e.g., `OutputStreamImageSink:104`, `FileImageSource:131`, `FileImageSink:204`, `InputStreamImageSource:442`) when `ImageIO.getImageWritersByFormatName(formatName)` or `ImageIO.getImageReaders(iis)` returns an empty iterator, indicating no suitable codec is registered in the JVM.

**L4 CORRECT MINIMAL USAGE**
```java
import net.coobird.thumbnailator.tasks.UnsupportedFormatException;

public class MinimalUsage {
    public static void main(String[] args) {
        // Instantiate using the single-argument constructor
        UnsupportedFormatException ex1 = new UnsupportedFormatException("webp");
        
        // Instantiate using the two-argument constructor and the UNKNOWN constant
        UnsupportedFormatException ex2 = new UnsupportedFormatException(
            UnsupportedFormatException.UNKNOWN,
            "No suitable ImageReader found for source data."
        );
        
        // Verify state
        System.out.println("Format 1: " + ex1.getFormatName());
        System.out.println("Format 2: " + ex2.getFormatName());
        System.out.println("Message 2: " + ex2.getMessage());
    }
}
```

**L5 FAILURE FORENSICS**
- **Failure**: `IllegalArgumentException: Specified format is not supported: superfakeformat`
- **Reason**: The recorded failure occurred because the test author likely attempted to trigger the exception organically by passing `"superfakeformat"` to a builder method like `Thumbnails.Builder.outputFormat(String)`. However, `outputFormat` eagerly validates the requested format against `ImageIO.getWriterFormatNames()` and throws an `IllegalArgumentException` immediately if it is missing. Consequently, the pipeline never reaches the terminal sink (e.g., `FileImageSink`) where `UnsupportedFormatException` is actually instantiated and thrown. While the truncated attempted code snippet shows direct instantiation, the error message proves the harness executed a pipeline configuration call that failed eagerly.

**L6 SELF-ASSESSMENT**
- **INFERENCE**: I inferred that `Thumbnails.Builder.outputFormat(String)` eagerly throws `IllegalArgumentException` based on the error message in the failure forensics, as the exception constructors themselves do not throw `IllegalArgumentException`.
- **INFERENCE**: I inferred that the attempted code snippet in the prompt was truncated and part of a larger test that included a pipeline execution using `"superfakeformat"`.
- **Information needed for certainty**: The full source of `Thumbnails.Builder.outputFormat(String)` and the complete, untruncated test snippet that failed.
- **L2 Confidence**: 10/10 - The constructors, parameters, and fields are fully visible in the provided source.
- **L3 Confidence**: 10/10 - The internal mechanics and call sites are explicitly shown in the provided context.
- **L4 Confidence**: 10/10 - Instantiating an exception directly is trivial, requires no complex setup, and is guaranteed to compile and run.