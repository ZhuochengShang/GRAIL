# Deep-dive: `region`

model: google:gemini-3.1-pro-preview · tokens in=6,504 out=4,343 · wall 40s · 2026-09-08 02:22

---

L0 AUDIENCE + TESTABILITY CLASSIFICATION
This API is classified as ADVANCED/LOW-LEVEL. It is a configuration method on `ThumbnailParameterBuilder`, which is used to construct `ThumbnailParameter` objects that configure low-level `ImageSource` implementations (like `BufferedImageSource` or `FileImageSource`), rather than being part of the primary user-facing `Thumbnails` facade. 

The API is TESTABLE ONLY WITH EXPLICIT LOW-LEVEL CONSTRUCTION. It can be tested standalone by instantiating a `ThumbnailParameterBuilder` via its public no-argument constructor, instantiating a `Region` using geometry classes seen in the real call sites (e.g., `Positions.TOP_LEFT` and `AbsoluteSize`), calling the `region` method, and terminating the chain with `build()`.

L1 PURPOSE
The `region` method is used to specify a rectangular sub-area of a source image that should be extracted (cropped) before any resizing or filtering operations occur. It sits at the parameter-building stage of the library's data flow, allowing low-level image processing tasks to know exactly which portion of the original image to process.

L2 CONTRACT
- **Receiver**: `ThumbnailParameterBuilder`. Obtained by calling its public no-argument constructor `new ThumbnailParameterBuilder()`.
- **Parameter `sourceRegion`**: Type `Region`. Represents the position and dimensions of the area to extract from the source image.
- **Return value**: `ThumbnailParameterBuilder`. Returns a reference to the current builder instance (`this`) to allow fluent method chaining.
- **Visibility**: `public`.
- **Thread-safety**: Not thread-safe. The method mutates the internal `sourceRegion` instance field of the builder.

L3 MECHANICS
The method's internal logic is a simple state mutation. It assigns the provided `sourceRegion` parameter to the `sourceRegion` instance field of the `ThumbnailParameterBuilder` (source line 201). It performs no validation on the input (e.g., it does not check for `null`, though passing `null` or invalid regions may cause failures later in the pipeline). It then returns `this` to continue the builder chain (source line 202).

L4 CORRECT MINIMAL USAGE
```java
import net.coobird.thumbnailator.builders.ThumbnailParameterBuilder;
import net.coobird.thumbnailator.geometry.Region;
import net.coobird.thumbnailator.geometry.Positions;
import net.coobird.thumbnailator.geometry.AbsoluteSize;

public class ApiTest {
    public static void main(String[] args) {
        // Construct the Region using types seen in real call sites
        Region cropRegion = new Region(Positions.TOP_LEFT, new AbsoluteSize(40, 40));
        
        // Construct the builder, apply the region, and build the parameters
        new ThumbnailParameterBuilder()
            .region(cropRegion)
            .size(20, 20) // Required to avoid IllegalStateException on build()
            .build();
    }
}
```

L5 FAILURE FORENSICS
- **Compilation Error (`error: method calculate in class Region ca...`)**: The recorded failure is a compilation error. The attempted code successfully instantiates a `Region` and begins to instantiate a `ThumbnailParameterBuilder`. The truncated error message indicates that the test harness subsequently attempted to invoke a `calculate` method on the `Region` object (likely to verify its bounds or behavior), but provided incorrect arguments or the method signature differs from what the test expected. The failure is not in the usage of the `region` API itself, but in the test's assertion logic interacting with the `Region` class, whose full definition is truncated in the provided context.

L6 SELF-ASSESSMENT
- INFERENCE: `Positions.TOP_LEFT` and `AbsoluteSize` are valid implementations of `Position` and `Size` respectively, inferred from their usage in the provided real call sites.
- INFERENCE: `size(int, int)` is a valid method on `ThumbnailParameterBuilder` that satisfies the requirements for `build()`, inferred from the real call sites and the documentation entry.
- INFERENCE: The exact package imports for `Positions` and `AbsoluteSize` are inferred based on the `net.coobird.thumbnailator.geometry` package mentioned in the documentation and `Region` source.
- INFERENCE: The exact signature of `calculate` on `Region` cannot be determined because the `Region` source is truncated in the provided context.
- **Confidence score for L2 (Contract)**: 10/10. The contract is fully visible in the provided source code.
- **Confidence score for L3 (Mechanics)**: 10/10. The mechanics are a simple field assignment, fully visible in the provided source code.
- **Confidence score for L4 (Minimal Usage)**: 9/10. The usage relies on `Positions.TOP_LEFT` and `AbsoluteSize` which are proven by real call sites, though their exact package imports are inferred.