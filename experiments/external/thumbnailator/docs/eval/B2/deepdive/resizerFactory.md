# Deep-dive: `resizerFactory`

model: google:gemini-3.1-pro-preview · tokens in=6,848 out=4,260 · wall 39s · 2026-09-08 02:24

---

L0 AUDIENCE + TESTABILITY CLASSIFICATION
- **Audience:** ADVANCED/LOW-LEVEL. While `Thumbnails.Builder` is the primary user-facing entry point, explicitly providing a `ResizerFactory` is an advanced configuration step used to override the library's default algorithm-selection logic.
- **Testability:** TESTABLE FROM PUBLIC INPUTS. The API can be tested by instantiating a `Thumbnails.Builder` or `ThumbnailParameterBuilder` and passing an anonymous implementation of the public `ResizerFactory` interface.

L1 PURPOSE
The `resizerFactory` method configures the builder with a factory responsible for dynamically selecting the appropriate `Resizer` (scaling algorithm) based on the original and target image dimensions. It sits in the configuration phase of the image processing pipeline, allowing advanced users to inject custom scaling logic or override default rendering hints.

L2 CONTRACT
- **Receiver:** `Thumbnails.Builder<T>` (obtained via `Thumbnails.of(...)`), `ThumbnailParameterBuilder`, or `ThumbnailMaker`.
- **Parameter:** `ResizerFactory resizerFactory` — An object that provides `Resizer` instances. Must not be null.
- **Return value:** `Builder<T>` (or the respective builder type) — A reference to the current builder object to allow fluent method chaining.
- **Visibility:** `public`.
- **State/Exceptions:** 
  - Throws `NullPointerException` if `resizerFactory` is null (via `checkForNull`).
  - Throws `IllegalStateException` if `resizerFactory` has already been set on this builder.
  - Throws `IllegalStateException` if a fixed `Resizer` was already set via `resizer(Resizer)`.
  - Throws `IllegalStateException` if any specific rendering hints (`scalingMode`, `alphaInterpolation`, `dithering`, `antialiasing`, `rendering`) were already set, because delegating to a `ResizerFactory` assumes the factory will fully encapsulate these decisions.

L3 MECHANICS
Inside `Thumbnails.Builder.resizerFactory(ResizerFactory)` (lines 1348-1362):
1. It validates the input by calling `checkForNull(resizerFactory, "ResizerFactory is null.")`.
2. It updates the internal `statusMap` via `updateStatus(Properties.RESIZER_FACTORY, Status.ALREADY_SET)`, which will throw an `IllegalStateException` if it was already set.
3. It explicitly locks out conflicting configurations by calling `updateStatus(..., Status.CANNOT_SET)` for `Properties.RESIZER`, `Properties.SCALING_MODE`, `Properties.ALPHA_INTERPOLATION`, `Properties.DITHERING`, `Properties.ANTIALIASING`, and `Properties.RENDERING`. If any of these were already set, `updateStatus` throws an `IllegalStateException`.
4. It assigns the provided factory to `this.resizerFactory`.
5. It returns `this` for method chaining.

L4 CORRECT MINIMAL USAGE
```java
import net.coobird.thumbnailator.builders.ThumbnailParameterBuilder;
import net.coobird.thumbnailator.resizers.ResizerFactory;
import net.coobird.thumbnailator.resizers.Resizer;
import java.awt.Dimension;

public class ApiTest {
    public static void main(String[] args) {
        // Implement the public ResizerFactory interface anonymously
        // to avoid relying on internal/undocumented factory implementations.
        ResizerFactory customFactory = new ResizerFactory() {
            @Override
            public Resizer getResizer() {
                return null; // Minimal stub for compilation/configuration test
            }
            
            @Override
            public Resizer getResizer(Dimension originalSize, Dimension thumbnailSize) {
                return null; // Minimal stub for compilation/configuration test
            }
        };

        // Apply the factory to a builder
        ThumbnailParameterBuilder builder = new ThumbnailParameterBuilder();
        builder.size(100, 100)
               .resizerFactory(customFactory)
               .build();
    }
}
```

L5 FAILURE FORENSICS
- **Failed Attempt:** `net.coobird.thumbnailator.resizers.ResizerFactory factory = net.coobird.thumbnailator.resizers.DefaultResizerFactory.getInstance();` resulting in `error: cannot find symbol`.
- **Why it failed:** The test harness attempted to use `DefaultResizerFactory`, which was likely inferred from the documentation or internal test code (`ThumbnailsBuilderTest.java:1344`). However, `DefaultResizerFactory` is either package-private, located in a different package than guessed, or excluded from the public API surface available to the external test harness. Because the compiler could not resolve the symbol, the build failed. The robust fix is to implement the public `ResizerFactory` interface directly rather than guessing the location/visibility of internal implementations.

L6 SELF-ASSESSMENT
- **Inferences:** 
  - I inferred that `DefaultResizerFactory` is either package-private or in an unexpected package, causing the `cannot find symbol` error in the external harness.
  - I inferred that `Resizer` is located in `net.coobird.thumbnailator.resizers` based on the package of `ResizerFactory`.
- **Information needed for certainty:** The exact package and visibility modifiers of `DefaultResizerFactory` and `Resizer` from the source tree.
- **Confidence Scores:**
  - L2 (Contract): 10/10 — The source code explicitly shows the null check, the status updates, and the return type.
  - L3 (Mechanics): 10/10 — The method body is provided in full and clearly delegates to `updateStatus` for state management.
  - L4 (Minimal Usage): 9/10 — The usage is correct and avoids the compilation error by using an anonymous class, though it relies on the inferred package for `Resizer`.