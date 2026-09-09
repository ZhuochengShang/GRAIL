## API Test: `setThumbnailParameter`
_Grounding: doc-repaired from source (docfix)._

### Signature
```java
public void setThumbnailParameter(ThumbnailParameter param)
```

### Goal
ADVANCED/LOW-LEVEL API. Sets the `ThumbnailParameter` configuration object on an image source or sink to dictate parameters (such as size and output format) for reading or writing. Because this is an internal/advanced configuration method, it should be excluded from the main user-facing benchmark denominator (users should prefer the fluent `Thumbnails.of()` API).

### Parameters
- `param` (`ThumbnailParameter`): The configuration object containing image reading, processing, and writing parameters.

### Input
ADVANCED/LOW-LEVEL. Requires explicit low-level construction of caller-owned objects: an `ImageSource` (e.g., `BufferedImageSource`) or `ImageSink`, and a fully constructed `ThumbnailParameter` instance built via `net.coobird.thumbnailator.builders.ThumbnailParameterBuilder`.

### Output
Returns `void` — mutates the state of the target `ImageSource` or `ImageSink` by assigning the provided parameters for subsequent `read()` or `write()` operations.

### Valid Call Patterns
```java
import net.coobird.thumbnailator.ThumbnailParameter;
import net.coobird.thumbnailator.builders.ThumbnailParameterBuilder;
import net.coobird.thumbnailator.tasks.io.BufferedImageSource;
import java.awt.image.BufferedImage;

// given
BufferedImage sourceImage = new BufferedImage(100, 100, BufferedImage.TYPE_INT_ARGB);
BufferedImageSource source = new BufferedImageSource(sourceImage);

// when
ThumbnailParameter param = new ThumbnailParameterBuilder()
    .size(20, 20)
    .build();

source.setThumbnailParameter(param);
```

### LLM Instruction Prompt
- `ThumbnailParameterBuilder` is located in the `net.coobird.thumbnailator.builders` package, not the root `net.coobird.thumbnailator` package. Code examples must use the correct fully-qualified imports.
- Avoid using complex geometry classes like `Region` or `AbsoluteSize` in basic examples without providing their exact fully-qualified package names. Stick to basic `.size(w, h)` configurations when testing low-level sources/sinks.

### Prompt Snippet
```text
To configure a low-level Thumbnailator ImageSource, call `source.setThumbnailParameter(new net.coobird.thumbnailator.builders.ThumbnailParameterBuilder().size(w, h).build());`.
```

### Common Failure Modes
- **Missing Symbol / Wrong Package (Recent Failure):** Failing with `cannot find symbol` because the code incorrectly assumes `ThumbnailParameterBuilder` is in the root `net.coobird.thumbnailator` package. It must be imported from `net.coobird.thumbnailator.builders.ThumbnailParameterBuilder`.
- **Missing Symbol / Guessed Geometry Packages:** Failing with `cannot find symbol` by attempting to guess the packages for `Region` and `AbsoluteSize`. Avoid these classes in basic examples.
- **Unnecessary Low-Level Usage:** ADVANCED/LOW-LEVEL API. Manually instantiating sources/sinks and calling `setThumbnailParameter` when the task should be safely handled by the preferred fluent builder (`Thumbnails.of(...)`). Exclude from standard user-facing tests.

### Fix Code Hint
```java
// Incorrect: Assuming builder is in the root package, and guessing geometry packages
// import net.coobird.thumbnailator.ThumbnailParameterBuilder;
// source.setThumbnailParameter(new ThumbnailParameterBuilder().region(new Region(...)).build());

// Correct: Use the correct builders package and stick to basic size parameters
import net.coobird.thumbnailator.builders.ThumbnailParameterBuilder;

source.setThumbnailParameter(
    new ThumbnailParameterBuilder()
        .size(20, 20)
        .build()
);
```