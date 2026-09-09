## API Test: `getOutputFormat`
_Grounding: doc-repaired from source (docfix)._

### Signature
```java
public String getOutputFormat()
```

### Goal
Retrieves the configured output format string. **Note:** This is an ADVANCED/LOW-LEVEL internal framework API used by internal tasks (e.g., `SourceSinkThumbnailTask`). It should be excluded from the main user-facing benchmark denominator, as end-users typically configure formats via the fluent `Thumbnails.Builder` API.

### Parameters
_None._

### Input
An instantiated `ThumbnailParameter` object. Because this is an ADVANCED/LOW-LEVEL API, it requires explicit low-level construction using `net.coobird.thumbnailator.builders.ThumbnailParameterBuilder` (caller-owned) to be testable standalone.

### Output
Returns `String` — The output format. May be a literal format name (e.g., `"jpg"`), `ThumbnailParameter.DETERMINE_FORMAT`, or `ThumbnailParameter.ORIGINAL_FORMAT` (which is explicitly `null`).

### Valid Call Patterns
```java
import net.coobird.thumbnailator.ThumbnailParameter;
import net.coobird.thumbnailator.builders.ThumbnailParameterBuilder;

// Explicit low-level construction required for standalone testing
ThumbnailParameterBuilder builder = new ThumbnailParameterBuilder();
builder.size(100, 100);
ThumbnailParameter param = builder.build();

String format = param.getOutputFormat();

if (format == ThumbnailParameter.ORIGINAL_FORMAT) {
    System.out.println("Format is ORIGINAL_FORMAT (null)");
} else if (ThumbnailParameter.DETERMINE_FORMAT.equals(format)) {
    System.out.println("Format is DETERMINE_FORMAT");
} else {
    System.out.println("Explicit format: " + format);
}
```

### LLM Instruction Prompt
- `ThumbnailParameter.ORIGINAL_FORMAT` is defined as `null`.
- Do not call `.equals()` on `ThumbnailParameter.ORIGINAL_FORMAT` because it will throw a `NullPointerException`.
- To check if the format is the original format, use reference equality (`format == ThumbnailParameter.ORIGINAL_FORMAT`) or check if the returned string is `null`.

### Prompt Snippet
```text
When retrieving the output format from a `ThumbnailParameter`, remember that `ThumbnailParameter.ORIGINAL_FORMAT` is `null`. Never call `.equals()` on it. Use `format == ThumbnailParameter.ORIGINAL_FORMAT` or `format == null` to avoid a NullPointerException.
```

### Common Failure Modes
- **NullPointerException on ORIGINAL_FORMAT (Just Happened):** Calling `ThumbnailParameter.ORIGINAL_FORMAT.equals(format)` throws an NPE because `ORIGINAL_FORMAT` is `null`.
- **Misunderstanding API Scope:** Attempting to use this ADVANCED/LOW-LEVEL internal framework API for standard thumbnail generation instead of the fluent `Thumbnails` builder.

### Fix Code Hint
```java
// WRONG: Throws NullPointerException because ORIGINAL_FORMAT is null
if (ThumbnailParameter.ORIGINAL_FORMAT.equals(format)) { 
    // ...
}

// CORRECT: Use reference equality or null check
if (format == ThumbnailParameter.ORIGINAL_FORMAT) { 
    // ...
}
```