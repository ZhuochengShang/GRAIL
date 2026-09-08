# Deep-dive: `filters`

model: google:gemini-3.1-pro-preview · tokens in=5,110 out=3,261 · wall 30s · 2026-09-08 01:50

---

**L0 AUDIENCE + TESTABILITY CLASSIFICATION**
- **Audience**: ADVANCED/LOW-LEVEL
- **Testability**: TESTABLE ONLY WITH EXPLICIT LOW-LEVEL CONSTRUCTION
- **Explanation**: The API is a builder method on `ThumbnailParameterBuilder`, which the documentation notes is used in "advanced workflows for constructing custom ThumbnailTask instances" rather than the standard `Thumbnails.of()` fluent API. It is testable by instantiating `ThumbnailParameterBuilder` via its public no-argument constructor and passing a `List<ImageFilter>`. Because we only have the `ImageFilter` interface in the context, we must construct an anonymous implementation to satisfy the parameter. This API should be excluded from a main user-facing benchmark denominator because it targets internal/advanced configuration rather than typical user-facing image processing pipelines.

**L1 PURPOSE**
This API configures a `ThumbnailParameterBuilder` by specifying a sequence of `ImageFilter` transformations to be applied to an image. In the library's data flow, this builder accumulates configuration state which is eventually baked into a `ThumbnailParameter` object via the `build()` method, dictating the post-resize filtering steps of a thumbnail generation task.

**L2 CONTRACT**
- **Receiver**: `ThumbnailParameterBuilder`. Obtained by calling its public no-argument constructor `new ThumbnailParameterBuilder()`.
- **Parameter `filters`**: `List<ImageFilter>`. A list of image filters to apply sequentially. Must not be `null`.
- **Return value**: `ThumbnailParameterBuilder`. Returns a reference to the current builder instance to allow fluent method chaining.
- **Visibility**: `public`.
- **Thread-safety/laziness**: The method eagerly mutates the internal `filters` field of the builder. It is not thread-safe, as it modifies shared mutable state without synchronization.

**L3 MECHANICS**
The method first checks if the provided `filters` list is `null`. If it is, it throws a `NullPointerException` with the message `"Filters is null."` (source/src/main/java/net/coobird/thumbnailator/builders/ThumbnailParameterBuilder.java:268-270). If the list is valid, it assigns the parameter to the internal `this.filters` field (line 272) and returns `this` (line 273). The stored filters are later passed directly to the `ThumbnailParameter` constructor when `build()` is invoked (lines 374 and 389).

**L4 CORRECT MINIMAL USAGE**
```java
import net.coobird.thumbnailator.builders.ThumbnailParameterBuilder;
import net.coobird.thumbnailator.filters.ImageFilter;
import java.awt.image.BufferedImage;
import java.util.Collections;
import java.util.List;

public class MinimalUsage {
    public static void main(String[] args) {
        // Construct the receiver
        ThumbnailParameterBuilder builder = new ThumbnailParameterBuilder();
        
        // Create a dummy ImageFilter since we only have the interface definition
        ImageFilter noOpFilter = new ImageFilter() {
            @Override
            public BufferedImage apply(BufferedImage img) {
                return img; // No-op
            }
        };
        
        List<ImageFilter> filterList = Collections.singletonList(noOpFilter);
        
        // Exercise the API
        builder.filters(filterList);
    }
}
```

**L5 FAILURE FORENSICS**
- **Attempt 1**: Failed with `error: cannot find symbol`. The attempted code snippet was physically truncated, ending abruptly with `builder.si` instead of a complete method call (likely intending to call `builder.size(...)`). Additionally, it attempted to reference `net.coobird.thumbnailator.filters.Flip.HORIZONTAL`, which is not defined in the provided context and would trigger a missing symbol error if the compiler evaluated that line.

**L6 SELF-ASSESSMENT**
- INFERENCE: I inferred that `ThumbnailParameter` is an immutable configuration object based on how it is instantiated with all fields at once in the `build()` method.
- INFERENCE: I inferred that the truncation `builder.si` or the missing `Flip.HORIZONTAL` class was the primary cause of the compilation failure, as the exact compiler output pointing to the specific missing symbol is not fully provided.
- To be certain about the exact cause of the compilation failure, I would need the full compiler output including the specific symbol it could not find.
- **L2 Confidence**: 10/10. The contract is explicitly defined in the provided source code and Javadoc.
- **L3 Confidence**: 10/10. The mechanics are simple and fully visible in the provided source code (lines 267-274).
- **L4 Confidence**: 10/10. The minimal usage relies only on standard Java libraries and the provided public constructor and interface, guaranteeing compilation.