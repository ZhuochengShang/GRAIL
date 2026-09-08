## API Test: `getOrientationFromExif`
_Grounding: doc-repaired from source (docfix)._

### Signature
```java
public static Orientation getOrientationFromExif(byte[] exifData)
```

### Goal
INTERNAL/FRAMEWORK API. Parses a byte array of Exif metadata to extract the image's orientation information. Note: This API should be excluded from the main user-facing denominator; it is testable only with explicit low-level byte array construction.

### Parameters
- `exifData` (`byte[]`): Raw Exif data. Must be at least 4 bytes long to avoid a `BufferUnderflowException`.

### Input
INTERNAL/FRAMEWORK usage. A caller-owned raw byte array representing an Exif metadata segment. The method wraps this input in a `ByteBuffer` and unconditionally reads the first 4 bytes to check for the Exif magic string.

### Output
Returns an `Orientation` enum representing the orientation state. If the array is at least 4 bytes but does not start with the Exif magic string, the method safely returns `null`. Returns `null` if no orientation tag is found in otherwise valid bytes.

### Valid Call Patterns
```java
import net.coobird.thumbnailator.util.exif.ExifUtils;
import net.coobird.thumbnailator.util.exif.Orientation;

// Providing at least 4 bytes prevents the initial BufferUnderflowException.
// Because it does not match the Exif magic string, it safely returns null.
byte[] dummyExifData = new byte[] { 0, 0, 0, 0 };
Orientation orientation = ExifUtils.getOrientationFromExif(dummyExifData);

if (orientation == null) {
    // Expected behavior for non-Exif dummy bytes
}
```

### LLM Instruction Prompt
When testing the internal `ExifUtils.getOrientationFromExif(byte[])`, you must provide a byte array of at least 4 bytes. The method unconditionally reads 4 bytes into a `ByteBuffer`. If testing failure paths, a 4-byte array of zeros safely bypasses the underflow and returns `null`.

### Prompt Snippet
```text
For internal Exif parsing tests, call `ExifUtils.getOrientationFromExif(byte[])` with an array of at least 4 bytes to prevent `BufferUnderflowException`. It returns `null` if the Exif magic string is missing.
```

### Common Failure Modes
- **`BufferUnderflowException` on Short Array**: Passing an empty or truncated byte array (less than 4 bytes) causes an immediate `BufferUnderflowException` because the method unconditionally reads 4 bytes to check the magic string.
- **`BufferUnderflowException` on Malformed Data**: Passing truncated Exif data that passes the magic string check but lacks required TIFF headers or IFD fields will also underflow the `ByteBuffer`.
- **Internal API Misuse**: This is an INTERNAL/FRAMEWORK API not intended for general user workflows.

### Fix Code Hint
```java
// WRONG: Empty or short array causes BufferUnderflowException
byte[] badExif = new byte[0];
Orientation o = ExifUtils.getOrientationFromExif(badExif);

// CORRECT: Provide at least 4 bytes to safely fail the magic string check and return null
byte[] safeDummyExif = new byte[] { 0, 0, 0, 0 };
Orientation o = ExifUtils.getOrientationFromExif(safeDummyExif);
```