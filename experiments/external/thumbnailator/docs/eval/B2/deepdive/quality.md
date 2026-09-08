# Deep-dive: `quality`

model: google:gemini-3.1-pro-preview · tokens in=5,340 out=2,353 · wall 23s · 2026-09-08 02:05

---

**L0 AUDIENCE + TESTABILITY CLASSIFICATION**
Audience: ADVANCED/LOW-LEVEL
Testability: TESTABLE FROM PUBLIC INPUTS

This API belongs to a builder class (`ThumbnailParameterBuilder`) used to construct `ThumbnailParameter` objects. While most users will interact with the higher-level `Thumbnails` fluent API, this builder is public and can be instantiated directly. It is testable from public inputs because its no-argument constructor `new ThumbnailParameterBuilder()` is public and requires no complex setup to invoke the `quality` method.

**L1 PURPOSE**
The `quality(float)` method configures the compression quality setting for the thumbnail being built. It stores this value in the builder's internal state so that when `build()` is eventually called, the resulting `ThumbnailParameter` object will carry the specified quality setting down to the underlying Java Image I/O writers (e.g., for JPEG compression).

**L2 CONTRACT**
- **Receiver**: `ThumbnailParameterBuilder`. It can be obtained directly via its public no-argument constructor `new ThumbnailParameterBuilder()`.
- **Parameter `quality`**: A `float` representing the compression quality. The documentation states acceptable values are in the range of `0.0f` (lowest quality/highest compression) to `1.0f` (highest quality/lowest compression). To use the default quality, the constant `ThumbnailParameter.DEFAULT_QUALITY` should be passed.
- **Return value**: Returns a reference to the current `ThumbnailParameterBuilder` instance (`this`), allowing for fluent method chaining.
- **Visibility**: `public`.
- **Thread-safety**: Not thread-safe. The builder mutates its internal state (`this.thumbnailQuality`) without synchronization.

**L3 MECHANICS**
The method is a simple setter. It assigns the provided `quality` float to the private instance variable `this.thumbnailQuality` (source: line 233). It then returns `this` (source: line 234). No validation (such as bounds checking for `0.0f` to `1.0f`) is performed at this stage. The stored `thumbnailQuality` is later consumed by the `build()` method (source: lines 372 and 387) where it is passed into the `ThumbnailParameter` constructor.

**L4 CORRECT MINIMAL USAGE**
```java
import net.coobird.thumbnailator.builders.ThumbnailParameterBuilder;

public class ApiTest {
    public static void main(String[] args) {
        ThumbnailParameterBuilder builder = new ThumbnailParameterBuilder();
        
        // Set the quality to 75%
        ThumbnailParameterBuilder returnedBuilder = builder.quality(0.75f);
        
        assert returnedBuilder == builder;
    }
}
```

**L5 FAILURE FORENSICS**
The recorded failed attempt:
```java
net.coobird.thumbnailator.builders.ThumbnailParameterBuilder builder = new net.coobird.thumbnailator.builders.ThumbnailParameterBuilder();
builder.size(100, 100);
net.coobird.thumbnailator.builders.ThumbnailParameterBuilder returnedBuilder = builder.quality(0.75f);
```
Failed with: `error: cannot find symbol` on the `builder.size(100, 100);` line.
**Why it failed:** The test harness attempted to call a `size(int, int)` method on `ThumbnailParameterBuilder`. However, looking at the provided type definitions for `ThumbnailParameterBuilder`, the only exposed `size` method takes a `java.awt.Dimension` object (`public ThumbnailParameterBuilder size(Dimension size)`). While that method internally delegates to a `size(size.width, size.height)` method, the `size(int, int)` method itself is either package-private or not exposed in the public API, causing the compiler to reject the call. The failure has nothing to do with the `quality` method itself.

**L6 SELF-ASSESSMENT**
- **Inferences:** I inferred that `ThumbnailParameter.DEFAULT_QUALITY` is a `float` constant (likely `Float.NaN` based on the documentation entry), though its exact definition is not in the provided source snippet. I also inferred that `size(int, int)` is not public based on the compiler error and its absence from the public signature list.
- **Information needed for certainty:** The exact source definition of `ThumbnailParameter` to confirm the value and type of `DEFAULT_QUALITY`, and the full source of `ThumbnailParameterBuilder` to confirm the visibility of `size(int, int)`.
- **Confidence Scores:**
  - L2 (Contract): 10/10 - The parameter, return type, and receiver are explicitly defined in the provided source and documentation.
  - L3 (Mechanics): 10/10 - The method body is exactly two lines long and its interaction with `build()` is fully visible in the source.
  - L4 (Minimal Usage): 10/10 - The builder is trivially instantiable and the method requires only a primitive `float`.