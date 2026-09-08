# Deep-dive: `Pipeline`

model: google:gemini-3.1-pro-preview · tokens in=4,789 out=3,218 · wall 36s · 2026-09-08 01:41

---

**L0 AUDIENCE + TESTABILITY CLASSIFICATION**
This API is classified as **ADVANCED/LOW-LEVEL**. While it is a public class, the documentation explicitly states to "strictly prefer the fluent `Thumbnails.Builder` API" for standard workflows, and real call sites show it being used internally by `Thumbnails` (e.g., `Thumbnails.java:815`) and utility classes (`ExifFilterUtils.java:57`). It should be excluded from a main user-facing benchmark denominator. 

Standalone testability is **TESTABLE FROM PUBLIC INPUTS**. The class provides public constructors and methods that only require standard Java types (`List`, `BufferedImage`) and the `ImageFilter` interface, which can be implemented anonymously without needing internal library state.

**L1 PURPOSE**
`Pipeline` is a composite image filter that maintains an ordered sequence of `ImageFilter` instances and applies them sequentially to a `BufferedImage`. It sits between the high-level fluent builder API (which configures the operations) and the low-level `Graphics2D` execution, acting as the execution engine for all image transformations (like rotation, flipping, or watermarking) requested by the user.

**L2 CONTRACT**
- **Receiver**: `Pipeline`. Obtained via `new Pipeline()`, `new Pipeline(ImageFilter...)`, or `new Pipeline(List<ImageFilter>)`.
- **Parameters**:
  - `Pipeline()`: No parameters. Initializes an empty pipeline.
  - `Pipeline(ImageFilter... filters)`: A varargs array of `ImageFilter` objects.
  - `Pipeline(List<ImageFilter> filters)`: A `List` of `ImageFilter` objects. Must not be null.
- **Return values**: 
  - `getFilters()` returns an unmodifiable `List<ImageFilter>`.
  - `apply(BufferedImage img)` returns a `BufferedImage` (either the original if the pipeline is empty, or a new modified copy).
- **Visibility**: `public final class`.
- **Thread-safety/Laziness**: Not thread-safe. The internal `ArrayList` is mutated directly by `add`, `addFirst`, and `addAll` without synchronization. The `getFilters()` method returns a live unmodifiable view of this list, meaning mutations to the pipeline will be visible to holders of the view.

**L3 MECHANICS**
- **Initialization**: The constructors initialize an `ArrayList` named `filtersToApply` and wrap it in `Collections.unmodifiableList` to create `unmodifiableFiltersToApply` (lines 89-91). Passing a null list to the constructor throws a `NullPointerException` (line 85).
- **Mutation**: `add(ImageFilter)`, `addFirst(ImageFilter)`, and `addAll(List<ImageFilter>)` append or prepend filters to the internal list. All three methods explicitly check for null inputs and throw a `NullPointerException` if the filter or list is null (lines 101, 114, 127).
- **Execution (`apply`)**: 
  - If `filtersToApply` is empty, it returns the input `img` directly without copying (line 146).
  - If not empty, it creates a copy of the input image by delegating to `BufferedImages.copy(img)` (line 149).
  - It iterates through `filtersToApply`, sequentially reassigning the image reference via `image = filter.apply(image)` (line 152).
  - It returns the final transformed `image`.

**L4 CORRECT MINIMAL USAGE**
```java
import java.awt.image.BufferedImage;
import net.coobird.thumbnailator.filters.Pipeline;
import net.coobird.thumbnailator.filters.ImageFilter;

public class PipelineMinimalUsage {
    public static void main(String[] args) {
        // 1. Create a source image
        BufferedImage img = new BufferedImage(100, 100, BufferedImage.TYPE_INT_ARGB);
        
        // 2. Instantiate the Pipeline
        Pipeline pipeline = new Pipeline();
        
        // 3. Add an ImageFilter (using an anonymous class since specific filters aren't in context)
        pipeline.add(new ImageFilter() {
            @Override
            public BufferedImage apply(BufferedImage image) {
                // In a real scenario, this would manipulate the image.
                // For minimal usage, we just return it.
                return image;
            }
        });
        
        // 4. Apply the pipeline
        BufferedImage result = pipeline.apply(img);
    }
}
```

**L5 FAILURE FORENSICS**
- **Failed Attempt**: `error: constructor Rotation in class Rot[ation] cannot be applied to given types... attempted code: ... new net.coobird.thumbnailator.filters.Rotation(90)`
- **Why it failed**: The LLM blindly trusted the documentation snippet (`new Rotation(90)`) without having the definition of the `Rotation` class in its context. The compilation error indicates that the `Rotation` constructor does not accept a single `int` (it likely requires a `double`, or perhaps `Rotation` is an enum or requires different arguments). Because the exact signature of `Rotation` was unknown, the instantiation failed. The correct approach is to use an anonymous implementation of `ImageFilter` or a mock, as demonstrated in the `PipelineTest.java` call site (`mock(ImageFilter.class)`).

**L6 SELF-ASSESSMENT**
- **Inferences**: 
  - I inferred that `BufferedImages.copy(img)` creates a deep copy of the `BufferedImage` to prevent mutating the original input, based on standard image processing practices and the method name.
  - I inferred the exact nature of the `Rotation` constructor failure (e.g., `int` vs `double`) because the `Rotation` source code was not provided, but the compiler error explicitly flags the constructor signature mismatch.
- **Information needed for certainty**: The source code for `BufferedImages.copy` to confirm the exact copying mechanism, and the source code for `Rotation` to know its exact constructor signature.
- **Confidence Scores**:
  - **L2 (Contract)**: 10/10. The class definition, constructors, and methods are fully visible in the provided source.
  - **L3 (Mechanics)**: 9/10. The logic is entirely visible in the source, with a minor deduction only because the implementation of `BufferedImages.copy` is external to the provided context.
  - **L4 (Minimal Usage)**: 10/10. The usage relies strictly on the provided `Pipeline` and `ImageFilter` interfaces, bypassing unknown concrete filter classes by using an anonymous implementation, guaranteeing compilation.