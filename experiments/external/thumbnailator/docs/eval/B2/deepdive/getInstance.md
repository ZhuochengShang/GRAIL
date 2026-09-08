# Deep-dive: `getInstance`

model: google:gemini-3.1-pro-preview · tokens in=3,529 out=4,068 · wall 35s · 2026-09-08 01:58

---

L0 AUDIENCE + TESTABILITY CLASSIFICATION
This API is classified as ADVANCED/LOW-LEVEL. While standard users typically rely on the fluent `Thumbnails.Builder` which configures these components internally, advanced users constructing custom pipelines or parameters may need direct access to these singletons. 
Standalone testability is TESTABLE FROM PUBLIC INPUTS. The `getInstance()` methods are public, static, take no arguments, and return fully initialized singleton objects without requiring any prior setup or low-level construction.

L1 PURPOSE
The `getInstance` method serves as a static factory to retrieve the singleton instance of specific stateless utility classes in Thumbnailator. Specifically, it provides access to `DefaultResizerFactory` (which encapsulates the logic for selecting the appropriate resizing algorithm based on target dimensions) and `SwapDimensions` (an image filter that inverts an image's width and height). It ensures that only one instance of these stateless components exists in memory.

L2 CONTRACT
- **Receiver type**: None (this is a `public static` method). It is called directly on the `DefaultResizerFactory` or `SwapDimensions` classes.
- **Parameters**: None.
- **Return value**: Returns the singleton instance of the respective class (`ResizerFactory` for `DefaultResizerFactory`, and `SwapDimensions` for `SwapDimensions`).
- **Visibility**: `public static`.
- **Thread-safety/laziness**: Thread-safe and eagerly initialized. The instances are created at class-loading time and stored in `private static final` fields, ensuring safe concurrent access without synchronization overhead.

L3 MECHANICS
- The method simply returns a pre-instantiated `static final` instance of the class named `INSTANCE`.
- For `DefaultResizerFactory`, the instance is instantiated at `DefaultResizerFactory.java:106` and returned at line 119.
- For `SwapDimensions`, the instance is instantiated at `SwapDimensions.java:37` and returned at line 41.
- No delegation occurs, no internal state is mutated, and no exceptions or failure conditions can be raised by calling this method.

L4 CORRECT MINIMAL USAGE
```java
import net.coobird.thumbnailator.resizers.DefaultResizerFactory;
import net.coobird.thumbnailator.resizers.ResizerFactory;
import net.coobird.thumbnailator.filters.SwapDimensions;

public class ApiTest {
    public static void main(String[] args) {
        // Obtain the singleton instances using the static getInstance() methods
        ResizerFactory resizerFactory = DefaultResizerFactory.getInstance();
        SwapDimensions swapDimensions = SwapDimensions.getInstance();
        
        // Verify instances are successfully retrieved
        if (resizerFactory == null || swapDimensions == null) {
            throw new IllegalStateException("Singleton instances should not be null");
        }
    }
}
```

L5 FAILURE FORENSICS
For the recorded failed attempt:
```java
[fail/compile] ... ApiTest.java:52: error: cannot find symbol
  attempted code: net.coobird.thumbnailator.resizers.ResizerFactory resizerFactory = net.coobird.thumbnailator.resizers.DefaultResizerFactory.getInstance();
net.coobird.thumbnailator.ThumbnailParameter param = new net.coobird.thumbnailator.ThumbnailParameterBuilder()
        .size(100, 100)
        .resizerFactory(re
```
- **Why it failed**: The failure is a `cannot find symbol` compilation error. While the call to `DefaultResizerFactory.getInstance()` is perfectly correct, the test harness subsequently attempted to instantiate `net.coobird.thumbnailator.ThumbnailParameterBuilder`. This builder class (suggested by the documentation entry) either does not exist in the public API or is not located in the specified package. The compiler failed on the `new net.coobird.thumbnailator.ThumbnailParameterBuilder()` expression, not on the `getInstance()` call itself.

L6 SELF-ASSESSMENT
- **INFERENCE**: I inferred that `ThumbnailParameterBuilder` is the specific missing symbol causing the compilation error, as it does not appear in any of the provided real call sites or source definitions, only in the documentation and the failed attempt.
- **INFERENCE**: I inferred that `SwapDimensions` implements an `ImageFilter` interface based on the context in `Thumbnailator.java:160` (`hasSwapDimenionsFilter = imageFilter.equals(SwapDimensions.getInstance());`).
- **Information needed to be certain**: The full compiler output from the failed attempt to definitively confirm which symbol (`ThumbnailParameterBuilder`, `ThumbnailParameter`, or a specific method) triggered the `cannot find symbol` error.
- **Confidence for L2 (Contract)**: 10/10. The signatures, return types, and eager initialization patterns are explicitly visible in the provided source code.
- **Confidence for L3 (Mechanics)**: 10/10. The method bodies are trivial (returning a static field) and fully provided in the source snippets.
- **Confidence for L4 (Minimal Usage)**: 10/10. The minimal usage relies only on the static methods, requires no complex setup, and uses only types confirmed to exist in the provided context.