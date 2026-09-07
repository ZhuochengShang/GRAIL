# Thumbnailator — LLM_readme

LLM-facing API documentation. Generated from the API surface, project profile, and distilled docs.

## API Test: `AbsoluteSize`

### Signature
```java
public AbsoluteSize(Dimension size)
public AbsoluteSize(int width, int height)
```
_Source: source/src/main/java/net/coobird/thumbnailator/geometry/AbsoluteSize.java:64  (+1 more definition site/overload)_

_Source doc:_ Instantiates an object which indicates size of an object. @param width		Width of the enclosed object. @param height	Height of the enclosed object. @throws IllegalArgumentException		If the width and/or height is less than or equal to {@code 0}.

### Goal
Instantiates an object representing fixed, absolute pixel dimensions, typically used to define exact sizes for cropping regions or source selections within an image processing pipeline.

### Parameters
- `width` (`int`): Width of the enclosed object in pixels. Must be strictly greater than 0.
- `height` (`int`): Height of the enclosed object in pixels. Must be strictly greater than 0.

### Input
Positive integer values representing the exact pixel width and height, or a `java.awt.Dimension` object containing positive dimensions. 

### Output
Returns `unspecified` — An instance of `AbsoluteSize` (which implements the `Size` interface) that encapsulates the specified fixed pixel dimensions for use in geometry operations like `Region`.

### Valid Call Patterns
```java
// Pattern 1: Used to construct a Region object for cropping
Region cropRegion = new Region(new Coordinate(0, 0), new AbsoluteSize(50, 50));

// Pattern 2: Used directly inline within the Thumbnails.Builder fluent API
BufferedImage thumbnail = Thumbnails.of(img)
        .sourceRegion(new Coordinate(0, 0), new AbsoluteSize(50, 50))
        .size(50, 50)
        .asBufferedImage();
```

### LLM Instruction Prompt
- When defining a fixed-pixel size for a `Region` or `sourceRegion` in Thumbnailator, instantiate `AbsoluteSize` with positive integers for width and height. Never pass `0` or negative values, as this will trigger an `IllegalArgumentException`.

### Prompt Snippet
```text
new AbsoluteSize(width, height)
```

### Common Failure Modes
- **`IllegalArgumentException`**: Thrown if the provided `width` and/or `height` is less than or equal to `0`.

### Fix Code Hint
```java
// Ensure dimensions are strictly positive before instantiating AbsoluteSize
int targetWidth = Math.max(1, requestedWidth);
int targetHeight = Math.max(1, requestedHeight);
AbsoluteSize size = new AbsoluteSize(targetWidth, targetHeight);
```

## API Test: `BicubicResizer`

### Signature
```java
public BicubicResizer()
public BicubicResizer(Map<RenderingHints.Key, Object> hints)
```
_Source: source/src/main/java/net/coobird/thumbnailator/resizers/BicubicResizer.java:51  (+1 more definition site/overload)_

_Source doc:_ Instantiates a {@link BicubicResizer} with the specified rendering hints. @param hints		Additional rendering hints to apply.

### Goal
Instantiates a resizer that uses the bicubic interpolation algorithm to scale images, optionally applying custom Java 2D rendering hints during the transformation.

### Parameters
- `hints` (`Map<RenderingHints.Key, Object>`): A map of Java 2D `RenderingHints` (such as `RenderingHints.KEY_ANTIALIASING` or `RenderingHints.KEY_RENDERING`) and their corresponding values to apply during the resizing operation.

### Input
A `Map` containing valid `RenderingHints.Key` objects and their strictly typed corresponding value objects (e.g., `RenderingHints.VALUE_ANTIALIAS_ON`). The caller must ensure the hints are compatible with standard Java 2D `Graphics2D` operations.

### Output
Returns `unspecified` — An instance of `BicubicResizer` that can be used within a `ResizerFactory` or a custom image processing pipeline to perform bicubic scaling.

### Valid Call Patterns
```java
// Inferred from signature (not verified by test suite or README)
Map<RenderingHints.Key, Object> hints = new HashMap<>();
hints.put(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
hints.put(RenderingHints.KEY_RENDERING, RenderingHints.VALUE_RENDER_QUALITY);

BicubicResizer resizer = new BicubicResizer(hints);
```

### LLM Instruction Prompt
- Use `BicubicResizer` when explicit control over the scaling algorithm (bicubic interpolation) is required, typically when building a custom `ResizerFactory` or manually constructing a `ThumbnailTask`.
- Pass a `Map<RenderingHints.Key, Object>` to configure specific Java 2D rendering behaviors.
- Remember that Thumbnailator's fluent API (`Thumbnails.of(...)`) is the strictly preferred paradigm; manual resizer instantiation should only be used for advanced, custom pipeline configurations.

### Prompt Snippet
```text
To use bicubic interpolation with custom rendering hints in a custom Thumbnailator pipeline, instantiate `new BicubicResizer(hintsMap)` where `hintsMap` is a `Map<RenderingHints.Key, Object>` containing standard Java 2D rendering hints.
```

### Common Failure Modes
- **Invalid Hint Values**: Providing an incompatible value type for a given `RenderingHints.Key` (e.g., passing a boolean or string instead of the required `RenderingHints` constant object), which will cause an `IllegalArgumentException` when the underlying `Graphics2D` attempts to apply the hints.
- **Unnecessary Manual Instantiation**: Attempting to manually instantiate and apply `BicubicResizer` when standard scaling could be handled automatically and more safely via the fluent `Thumbnails.Builder.size()` or `Thumbnails.Builder.resizer()` methods.

### Fix Code Hint
```java
// Ensure standard RenderingHints constants are used as values
Map<RenderingHints.Key, Object> hints = new HashMap<>();
hints.put(RenderingHints.KEY_INTERPOLATION, RenderingHints.VALUE_INTERPOLATION_BICUBIC);
BicubicResizer resizer = new BicubicResizer(hints);
```

## API Test: `BilinearResizer`

### Signature
```java
public BilinearResizer()
public BilinearResizer(Map<RenderingHints.Key, Object> hints)
```
_Source: source/src/main/java/net/coobird/thumbnailator/resizers/BilinearResizer.java:52  (+1 more definition site/overload)_

_Source doc:_ Instantiates a {@link BilinearResizer} with the specified rendering hints. @param hints		Additional rendering hints to apply.

### Goal
Instantiates a resizer that uses a bilinear interpolation algorithm to scale images, applying the specified Java 2D rendering hints during the transformation.

### Parameters
- `hints` (`Map<RenderingHints.Key, Object>`): A map containing `java.awt.RenderingHints.Key` objects and their corresponding configuration values to apply to the underlying `Graphics2D` context during the resizing operation.

### Input
A valid, non-null `Map` of rendering hints. The keys must be standard `RenderingHints.Key` instances, and the values must be the exact corresponding `RenderingHints` constant objects (e.g., `RenderingHints.VALUE_RENDER_QUALITY`). 

### Output
Returns `unspecified` — A new instance of `BilinearResizer` configured with the provided rendering hints, which can be used within a custom `ResizerFactory` or image processing pipeline.

### Valid Call Patterns
```java
// Inferred from signature (not verified)
import java.awt.RenderingHints;
import java.util.HashMap;
import java.util.Map;
import net.coobird.thumbnailator.resizers.BilinearResizer;

Map<RenderingHints.Key, Object> hints = new HashMap<>();
hints.put(RenderingHints.KEY_RENDERING, RenderingHints.VALUE_RENDER_QUALITY);
hints.put(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);

BilinearResizer resizer = new BilinearResizer(hints);
```

### LLM Instruction Prompt
- When instantiating `BilinearResizer` manually, provide a properly typed `Map<RenderingHints.Key, Object>`. 
- Note that manual instantiation of resizers is generally discouraged; the strictly preferred paradigm is to use the fluent `Thumbnails.of(...).resizer(...)` API or rely on `ResizerConfiguration` (like `ScalingMode`) to let Thumbnailator manage the boilerplate of `Graphics2D` manipulation.
- Only use this constructor when building highly customized `Pipeline` objects or custom `ResizerFactory` implementations.

### Prompt Snippet
```text
To create a `BilinearResizer` with custom rendering hints, initialize a `Map<RenderingHints.Key, Object>` with standard `java.awt.RenderingHints` constants and pass it to the constructor. Prefer the fluent `Thumbnails.Builder` API for standard resizing tasks.
```

### Common Failure Modes
- **Manual Instantiation Overhead**: Attempting to manually wire this resizer into a basic thumbnail generation task instead of using the fluent `Thumbnails.of(...)` builder, leading to unnecessary boilerplate and bypassing Thumbnailator's automatic format and I/O handling.
- **Invalid Hint Values**: Inserting values into the `hints` map that do not match the expected type for the given `RenderingHints.Key` (e.g., passing a `String` instead of a `RenderingHints` constant object), which will cause runtime exceptions when the underlying `Graphics2D` engine attempts to apply them.
- **Null Map**: Passing `null` instead of an empty map if no hints are desired, which may lead to a `NullPointerException` during pipeline execution.

### Fix Code Hint
```java
// Ensure the map is properly initialized and uses standard AWT constants
Map<RenderingHints.Key, Object> hints = new HashMap<>();
// Correct: Using the exact AWT constant object
hints.put(RenderingHints.KEY_COLOR_RENDERING, RenderingHints.VALUE_COLOR_RENDER_QUALITY);

BilinearResizer resizer = new BilinearResizer(hints);
```

## API Test: `BufferedImageBuilder`

### Signature
```java
public BufferedImageBuilder(Dimension size)
public BufferedImageBuilder(Dimension size, int imageType)
public BufferedImageBuilder(int width, int height)
public BufferedImageBuilder(int width, int height, int imageType)
```
_Source: source/src/main/java/net/coobird/thumbnailator/builders/BufferedImageBuilder.java:99  (+3 more definition site/overload)_

_Source doc:_ Instantiates a {@code BufferedImageBuilder} with the specified size and image type. @param width			The width of the {@link BufferedImage} to build. @param height		The height of the {@link BufferedImage} to build. @param imageType		The image type of the {@link BufferedImage} to build.

### Goal
Instantiates a builder object used to construct a new, blank `BufferedImage` with the specified dimensions and color model type, commonly used for generating in-memory test images.

### Parameters
- `width` (`int`): The width of the `BufferedImage` to build, in pixels.
- `height` (`int`): The height of the `BufferedImage` to build, in pixels.
- `imageType` (`int`): The image type constant of the `BufferedImage` to build (e.g., `java.awt.image.BufferedImage.TYPE_INT_ARGB`).

### Input
Requires valid, strictly positive integer dimensions for width and height, and a valid `java.awt.image.BufferedImage` type constant. The environment must support standard Java Image I/O (headless mode is fully supported).

### Output
Returns `unspecified` — A `BufferedImageBuilder` instance. To retrieve the actual `BufferedImage`, the caller must invoke the `.build()` method on this returned instance.

### Valid Call Patterns
```java
// Generate a blank 200x200 ARGB image in-memory
BufferedImage img = new BufferedImageBuilder(200, 200, BufferedImage.TYPE_INT_ARGB).build();

// Use the generated image as a source for Thumbnailator
Image thumbnail = Thumbnailator.createThumbnail((Image) img, 50, 50);
```

### LLM Instruction Prompt
- When generating a blank in-memory image for headless testing or as a pipeline source, instantiate `BufferedImageBuilder` with the desired dimensions and `BufferedImage` type constant, then immediately chain the `.build()` method to retrieve the `BufferedImage`. Do not attempt to use the builder object directly as an image.

### Prompt Snippet
```text
Use `new BufferedImageBuilder(width, height, BufferedImage.TYPE_INT_ARGB).build()` to safely generate in-memory images for headless testing without relying on external files.
```

### Common Failure Modes
- **Missing `.build()` call**: Forgetting to call `.build()` on the instantiated builder, resulting in a `BufferedImageBuilder` object being passed to methods expecting a `BufferedImage` or `Image`.
- **Invalid Dimensions**: Providing negative or zero dimensions for width or height, which will cause an exception when the underlying `BufferedImage` is constructed.
- **Invalid Image Type**: Passing an integer that does not correspond to a valid `BufferedImage` type constant.

### Fix Code Hint
```java
// Incorrect: Missing .build(), returns a builder instead of an image
// BufferedImage img = new BufferedImageBuilder(200, 200, BufferedImage.TYPE_INT_ARGB);

// Correct: Chain .build() to extract the actual BufferedImage
BufferedImage img = new BufferedImageBuilder(200, 200, BufferedImage.TYPE_INT_ARGB).build();
```

## API Test: `BufferedImageSource`

### Signature
```java
public BufferedImageSource(BufferedImage img)
```
_Source: source/src/main/java/net/coobird/thumbnailator/tasks/io/BufferedImageSource.java:54_

_Source doc:_ Instantiates a {@link BufferedImageSource} object with the {@link BufferedImage} that should be used as the source image for making thumbnails. @param img		The source image. @throws NullPointerException		If the image is null.

### Goal
Instantiates an `ImageSource` wrapper around an in-memory `BufferedImage` so it can be used as the input source for custom thumbnail generation tasks.

### Parameters
- `img` (`BufferedImage`): The in-memory source image to be processed by the thumbnail pipeline.

### Input
A valid, instantiated, non-null `java.awt.image.BufferedImage` object. The image must be fully loaded in memory.

### Output
Returns `unspecified` — An instance of `BufferedImageSource` that encapsulates the provided `BufferedImage`, ready to be passed into a `ThumbnailTask` (such as `SourceSinkThumbnailTask`).

### Valid Call Patterns
```java
// Constructing a source for a custom SourceSinkThumbnailTask
BufferedImageSource source = new BufferedImageSource(
        new BufferedImageBuilder(200, 200, BufferedImage.TYPE_INT_ARGB).build()
);
BufferedImageSink sink = new BufferedImageSink();

// Assuming 'param' is a configured ThumbnailParameter
Thumbnailator.createThumbnail(
        new SourceSinkThumbnailTask<BufferedImage, BufferedImage>(
                param, source, sink
        )
);
```

### LLM Instruction Prompt
- Use `BufferedImageSource` when you need to construct a custom `ThumbnailTask` (like `SourceSinkThumbnailTask`) that reads from an in-memory `BufferedImage`.
- Do not pass `null` to the constructor, as it will immediately throw a `NullPointerException`.
- Note: For standard workflows, prefer the fluent API (`Thumbnails.of(BufferedImage)`) which abstracts away the need to manually instantiate `BufferedImageSource` and `ThumbnailTask`.

### Prompt Snippet
```text
When building a custom `SourceSinkThumbnailTask` for an in-memory image, wrap the `BufferedImage` in a `BufferedImageSource`. Ensure the image is not null before instantiation to prevent a `NullPointerException`.
```

### Common Failure Modes
- **`NullPointerException`**: Thrown immediately during instantiation if the provided `img` argument is `null`.
- **Unnecessary Complexity**: Manually creating a `BufferedImageSource` and `SourceSinkThumbnailTask` when the fluent API (`Thumbnails.of(img).size(w, h).asBufferedImage()`) would suffice for the user's goal.

### Fix Code Hint
```java
// Ensure the image is not null before wrapping it in a BufferedImageSource
if (img == null) {
    throw new IllegalArgumentException("Source image cannot be null");
}
BufferedImageSource source = new BufferedImageSource(img);
```

## API Test: `Canvas`

### Signature
```java
public Canvas(int width, int height, Position position)
public Canvas(int width, int height, Position position, boolean crop)
public Canvas(int width, int height, Position position, Color fillColor)
public Canvas(int width, int height, Position position, boolean crop, Color fillColor)
```
_Source: source/src/main/java/net/coobird/thumbnailator/filters/Canvas.java:144  (+3 more definition site/overload)_

_Source doc:_ Instantiates a {@code Canvas} filter. @param width			The width of the filtered image. @param height		The height of the filtered image. @param position		The position to place the enclosed image. @param crop			Whether or not to crop the enclosed image if the enclosed image has dimensions which are larger than the specified {@code width} and {@code height}. @param fillColor		The color to fill portions of the image which is not covered by the enclosed image. Portions of the image which is transparent will be filled with the specified color as well.

### Goal
Instantiates an `ImageFilter` that places an image onto a canvas of specified dimensions, optionally cropping the enclosed image or filling the uncovered background with a specific color.

### Parameters
- `width` (`int`): The width of the resulting filtered image (the canvas).
- `height` (`int`): The height of the resulting filtered image (the canvas).
- `position` (`Position`): The position to place the enclosed image on the canvas (typically a value from the `Positions` enum, such as `Positions.CENTER`).
- `crop` (`boolean`): Whether or not to crop the enclosed image if its dimensions are larger than the specified `width` and `height`.
- `fillColor` (`Color`): The `java.awt.Color` used to fill portions of the canvas not covered by the enclosed image. Transparent portions of the original image will also be filled with this color.

### Input
Requires positive integer dimensions for the canvas size and a valid `Position` implementation (e.g., `net.coobird.thumbnailator.geometry.Positions`). If using the overloads with `fillColor`, a valid `java.awt.Color` must be provided. The resulting filter is designed to be applied to a `java.awt.image.BufferedImage` either directly or via the `Thumbnails.Builder` fluent pipeline.

### Output
Returns a new `Canvas` instance (which implements `ImageFilter`) representing the configured canvas transformation.

### Valid Call Patterns
```java
// 1. Direct application to a BufferedImage (from test suite)
BufferedImage originalImage = new BufferedImage(200, 200, BufferedImage.TYPE_INT_ARGB);
ImageFilter filter = new Canvas(100, 100, Positions.CENTER);
BufferedImage result = filter.apply(originalImage);

// 2. Direct application with cropping enabled (from test suite)
ImageFilter cropFilter = new Canvas(100, 100, Positions.CENTER, true);
BufferedImage croppedResult = cropFilter.apply(originalImage);

// 3. Integration into a fluent Thumbnails pipeline (inferred from context)
Thumbnails.of(new File("input.jpg"))
    .size(200, 200)
    .addFilter(new Canvas(300, 300, Positions.CENTER, Color.WHITE))
    .toFile(new File("output.jpg"));
```

### LLM Instruction Prompt
When creating a `Canvas` filter, ensure `width` and `height` are positive integers. Use the `Positions` enum (e.g., `Positions.CENTER`, `Positions.BOTTOM_RIGHT`) for the `position` argument. To use the filter in a standard Thumbnailator workflow, pass the instantiated `Canvas` to `Thumbnails.Builder.addFilter()`. For direct in-memory manipulation, call `.apply(BufferedImage)` on the instantiated filter.

### Prompt Snippet
```text
// Create a 500x500 canvas, center the image, crop if it exceeds 500x500, and fill the rest with black
ImageFilter canvasFilter = new Canvas(500, 500, Positions.CENTER, true, Color.BLACK);
```

### Common Failure Modes
- **Invalid Dimensions**: Passing negative or zero values for `width` or `height` will result in an `IllegalArgumentException` during instantiation or application.
- **Null Arguments**: Passing `null` for the `Position` or `Color` arguments will cause a `NullPointerException`.
- **Pipeline Omission**: Instantiating the `Canvas` object but forgetting to pass it to `Thumbnails.Builder.addFilter()` will result in the canvas transformation being silently ignored in the fluent workflow.

### Fix Code Hint
```java
// Incorrect: Missing position or using invalid dimensions
// ImageFilter badFilter = new Canvas(-100, 100, null);

// Correct: Use valid dimensions, the Positions enum, and add to the pipeline
ImageFilter canvasFilter = new Canvas(800, 600, Positions.CENTER, true, Color.WHITE);
Thumbnails.of(inputFile)
    .size(400, 400)
    .addFilter(canvasFilter) // Crucial step to apply the filter
    .toFile(outputFile);
```

## API Test: `Caption`

### Signature
```java
public Caption(String caption, Font font, Color c, float alpha, Position position, int insets)
public Caption(String caption, Font font, Color c, Position position, int insets)
```
_Source: source/src/main/java/net/coobird/thumbnailator/filters/Caption.java:92  (+1 more definition site/overload)_

_Source doc:_ Instantiates a filter which adds a text caption to an image. @param caption	The text of the caption. @param font		The font of the caption. @param c			The color of the caption. @param alpha		The opacity level of caption. <p> The value should be between {@code 0.0f} and {@code 1.0f}, where {@code 0.0f} is completely transparent, and {@code 1.0f} is completely opaque. @param position	The position of the caption. @param insets	The inset size around the caption. Cannot be negative.

### Goal
Instantiates an `ImageFilter` that draws a text caption onto an image during the thumbnail generation pipeline.

### Parameters
- `caption` (`String`): The text string to be drawn on the image.
- `font` (`Font`): The `java.awt.Font` used to render the text.
- `c` (`Color`): The `java.awt.Color` used to draw the text.
- `alpha` (`float`): The opacity level of the caption. Must be between `0.0f` (completely transparent) and `1.0f` (completely opaque). This parameter is omitted in the 5-argument overload.
- `position` (`Position`): The placement of the caption on the image (typically provided by the `net.coobird.thumbnailator.geometry.Positions` enum, e.g., `Positions.BOTTOM_CENTER`).
- `insets` (`int`): The padding or inset size in pixels around the caption. Cannot be negative.

### Input
The caller must provide valid AWT `Font` and `Color` objects, a valid `Position` implementation, and a non-negative `insets` integer. If using the 6-argument constructor, the `alpha` float must be strictly bounded between `0.0f` and `1.0f`. The environment must support headless AWT font rendering.

### Output
Returns an instantiated `Caption` object (which implements `ImageFilter`) that can be applied directly to a `BufferedImage` or passed into a fluent pipeline via `Thumbnails.Builder.addFilter(ImageFilter)`.

### Valid Call Patterns
```java
// Pattern 1: Direct instantiation and application to a BufferedImage (from test suite)
ImageFilter filter = new Caption(
        "Sample Caption",
        new Font("Monospaced", Font.PLAIN, 14),
        Color.BLACK,
        Positions.BOTTOM_CENTER,
        0
);
filter.apply(originalImage);

// Pattern 2: Instantiation with alpha transparency for use in a Thumbnails pipeline
Thumbnails.of(new File("input.jpg"))
        .size(640, 480)
        .addFilter(new Caption(
                "Watermark Text",
                new Font("SansSerif", Font.BOLD, 24),
                Color.WHITE,
                0.5f, // 50% opacity
                Positions.CENTER,
                10    // 10px inset
        ))
        .toFile(new File("output.jpg"));
```

### LLM Instruction Prompt
- To add text to an image in Thumbnailator, instantiate a `Caption` filter and pass it to `Thumbnails.Builder.addFilter()`. You must provide a `String`, `java.awt.Font`, `java.awt.Color`, `Position` (e.g., `Positions.BOTTOM_RIGHT`), and an `int` for insets. If specifying opacity, provide a `float` alpha between `0.0f` and `1.0f`. Never pass a negative value for `insets`.

### Prompt Snippet
```text
To overlay text on a thumbnail, create a `Caption` filter with your desired `Font`, `Color`, and `Positions` enum value, ensuring `insets` >= 0. Add it to the pipeline using `.addFilter(new Caption(...))`.
```

### Common Failure Modes
- **Negative Insets**: Passing a negative integer for the `insets` parameter will cause an `IllegalArgumentException` or rendering failure.
- **Out-of-Bounds Alpha**: Providing an `alpha` value less than `0.0f` or greater than `1.0f` violates the opacity constraints and will cause an `IllegalArgumentException`.
- **Null Parameters**: Passing `null` for the `caption`, `font`, `c`, or `position` parameters will result in a `NullPointerException` when the filter attempts to render the text.

### Fix Code Hint
```java
// Ensure alpha is clamped between 0.0f and 1.0f, and insets is >= 0
float safeAlpha = Math.max(0.0f, Math.min(1.0f, requestedAlpha));
int safeInsets = Math.max(0, requestedInsets);

ImageFilter captionFilter = new Caption(
        text, 
        font, 
        color, 
        safeAlpha, 
        Positions.BOTTOM_RIGHT, 
        safeInsets
);
```

## API Test: `Colorize`

### Signature
```java
public Colorize(Color c)
public Colorize(Color c, float alpha)
public Colorize(Color c, int alpha)
```
_Source: source/src/main/java/net/coobird/thumbnailator/filters/Colorize.java:69  (+2 more definition site/overload)_

_Source doc:_ Instantiates this filter with the color to use to tint the target image with and the transparency level provided as a {@code float} ranging from {@code 0.0f} to {@code 1.0f}, where {@code 0.0f} indicates completely transparent, and {@code 1.0f} indicates completely opaque. @param c				Color to tint with. @param alpha			The opacity of the tint.

### Goal
Instantiates an `ImageFilter` that tints a target image with a specified color and opacity level.

### Parameters
- `c` (`Color`): The `java.awt.Color` to use for tinting the target image.
- `alpha` (`float`): The opacity of the tint, provided as a `float` ranging from `0.0f` (completely transparent/no visible tint) to `1.0f` (completely opaque/solid color). An overloaded constructor also accepts an `int` for alpha.

### Input
A valid `java.awt.Color` instance and an opacity value. When used in a Thumbnailator workflow, the resulting `Colorize` filter expects to process a `java.awt.image.BufferedImage` (either passed directly to its `apply` method or handled automatically when added to a `Thumbnails.Builder` pipeline).

### Output
Returns `unspecified` — A new `Colorize` instance (which implements the `ImageFilter` interface) configured with the specified color and opacity, ready to be applied to an image or added to a processing pipeline.

### Valid Call Patterns
```java
// Direct instantiation and application (from test suite)
BufferedImage originalImage = new BufferedImage(200, 200, BufferedImage.TYPE_INT_ARGB);
BufferedImage copyImage = BufferedImages.copy(originalImage);

ImageFilter filter = new Colorize(Color.blue, 0.5f);

// Apply the filter to the image
filter.apply(originalImage);

// The original image's contents are not altered in place
assertTrue(BufferedImageComparer.isSame(originalImage, copyImage));

// Pipeline usage (inferred from project context)
Thumbnails.of(new File("input.jpg"))
    .size(640, 480)
    .addFilter(new Colorize(Color.red, 0.25f))
    .toFile(new File("output.jpg"));
```

### LLM Instruction Prompt
- To tint an image in Thumbnailator, instantiate `new Colorize(Color c, float alpha)` and pass it to `Thumbnails.Builder.addFilter()`.
- When using the `float` constructor, strictly ensure the `alpha` value is between `0.0f` and `1.0f`.
- Do not assume `Colorize` mutates the input `BufferedImage` in place. The filter safely leaves the original image unaltered and returns a new processed image.

### Prompt Snippet
```text
To apply a color tint to a thumbnail, create a `Colorize` filter with your desired `java.awt.Color` and a float opacity (0.0f to 1.0f), then add it to the pipeline: `.addFilter(new Colorize(Color.BLUE, 0.5f))`.
```

### Common Failure Modes
- **Out-of-bounds Alpha**: Passing a `float` value less than `0.0f` or greater than `1.0f` to the `alpha` parameter, which violates the standard bounds for alpha composites.
- **Assuming In-Place Mutation**: Calling `filter.apply(originalImage)` and expecting `originalImage` to contain the tinted result. The `Colorize` filter does not alter the input contents; it generates a new image.
- **Missing Pipeline Integration**: Forgetting to actually add the instantiated filter to the builder using `.addFilter(ImageFilter)`.

### Fix Code Hint
```java
// INCORRECT: Assuming the filter modifies the image in place
ImageFilter filter = new Colorize(Color.blue, 0.5f);
filter.apply(myImage);
// myImage is unchanged!

// CORRECT: Use the fluent builder pipeline to manage filter application and output
Thumbnails.of(myImage)
    .size(200, 200)
    .addFilter(new Colorize(Color.blue, 0.5f))
    .asBufferedImage();
```

## API Test: `ConsecutivelyNumberedFilenames`

### Signature
```java
public ConsecutivelyNumberedFilenames()
public ConsecutivelyNumberedFilenames(int start)
public ConsecutivelyNumberedFilenames(File dir)
public ConsecutivelyNumberedFilenames(String format)
public ConsecutivelyNumberedFilenames(File dir, int start)
public ConsecutivelyNumberedFilenames(File dir, String format)
public ConsecutivelyNumberedFilenames(String format, int start)
public ConsecutivelyNumberedFilenames(File dir, String format, int start)
```
_Source: source/src/main/java/net/coobird/thumbnailator/name/ConsecutivelyNumberedFilenames.java:295  (+7 more definition site/overload)_

_Source doc:_ <p> Instantiates an {@code ConsecutivelyNumberedFilenames} object which returns {@link File}s with file names which are based on a format string, located in the directory specified. The numbering will be consecutive from the specified value. </p> <p> The format string should contain the string {@code %d} which will be replaced with a consecutively counted number. Additional formatting can be applied. For more details, please refer to the section on <em>Numeric</em> formatting in the Java API specification for the {@link Formatter} class. </p> <p><strong>File name sequence</strong></p> <p> For a case where the parent directory is {@code /foo/bar/}, and the specified value is {@code 5}, with format string {@code image-%d}: </p> <ol> <li><code>/foo/bar/image-5</code></li> <li><code>/foo/bar/image-6</code></li> <li><code>/foo/bar/image-7</code></li> <li><code>/foo/bar/image-8</code></li> </ol> <p> and so on. </p> @param dir			The directory in which the files are to be located. @param format		The format string to use. @param start			The value from which to start counting. @throws IOException	If the specified directory path is not a directory, or if does not exist.

### Goal
Instantiates an iterable file name generator that produces consecutively numbered `File` objects based on a format string, used to prevent filename collisions during batch thumbnail output.

### Parameters
- `dir` (`File`): The target directory where the generated files will be located. Must exist and be a valid directory.
- `format` (`String`): The format string for the filenames. It must contain a numeric placeholder (e.g., `%d` or `%03d`) compatible with Java's `Formatter` class.
- `start` (`int`): The integer value from which to start counting (e.g., `0` or `1`).

### Input
The caller must provide an existing directory (`File`) if using an overload that accepts `dir`. The `format` string must be a valid Java format string containing a numeric placeholder (like `%d`) to ensure uniqueness. This object is typically passed directly into `Thumbnails.Builder.toFiles(Iterable<File>)` or `Thumbnails.Builder.asFiles(Iterable<File>)` when processing multiple input images.

### Output
Returns `unspecified` — An instance of `ConsecutivelyNumberedFilenames` (which implements `Iterable<File>`) representing the sequence of generated file paths.

### Valid Call Patterns
```java
// Pattern 1: Outputting directly to files using a format string and directory
Thumbnails.of(inputFile)
        .size(50, 50)
        .toFiles(new ConsecutivelyNumberedFilenames(temporaryFolder.getRoot(), "temp-%d.png"));

// Pattern 2: Generating files and returning a List of the generated File objects
List<File> thumbnails = Thumbnails.of(inputFile)
        .size(50, 50)
        .asFiles(new ConsecutivelyNumberedFilenames(temporaryFolder.getRoot(), "temp-%d.png"));
```

### LLM Instruction Prompt
- When outputting multiple files to a directory using `toFiles()` or `asFiles()`, you MUST provide a `Rename` strategy or an instance of `ConsecutivelyNumberedFilenames` to prevent filename collisions.
- Always ensure the `format` string contains a numeric placeholder like `%d` (e.g., `"image-%d.jpg"`).
- The `dir` argument must point to an existing directory, otherwise the constructor will throw an `IOException`. Ensure the directory is created before instantiating this class.

### Prompt Snippet
```text
To safely batch-process images and save them to a directory without overwriting, pass `new ConsecutivelyNumberedFilenames(outputDir, "thumb-%d.jpg")` to `toFiles()`. Ensure `outputDir` exists before calling this constructor to avoid an IOException.
```

### Common Failure Modes
- **`IOException`**: Thrown immediately by the constructor if the specified `dir` path is not a directory, or if it does not exist.
- **`IllegalFormatException` / `MissingFormatArgumentException`**: Thrown during iteration if the `format` string is invalid or lacks a numeric placeholder (like `%d`) for the underlying `Formatter`.
- **Filename Collisions**: If the format string is valid but does not include a dynamic numeric placeholder (e.g., `"image.jpg"` instead of `"image-%d.jpg"`), the generator will yield the exact same filename repeatedly, causing the pipeline to overwrite the same file for every image in the batch.

### Fix Code Hint
```java
// Ensure the target directory exists before instantiating
File outputDir = new File("path/to/output");
if (!outputDir.exists()) {
    outputDir.mkdirs();
}

// Use a format string with %d to guarantee unique filenames
Thumbnails.of(inputFiles)
    .size(100, 100)
    .toFiles(new ConsecutivelyNumberedFilenames(outputDir, "thumbnail-%03d.jpg", 1));
```

## API Test: `Coordinate`

### Signature
```java
public Coordinate(int x, int y)
```
_Source: source/src/main/java/net/coobird/thumbnailator/geometry/Coordinate.java:56_

_Source doc:_ Instantiates an object which calculates the position of an image, using the given coordinates. @param x			The horizontal component of the top-left corner of the image to be enclosed. @param y			The vertical component of the top-left corner of the image to be enclosed.

### Goal
Instantiates an object that defines an exact absolute 2D pixel position (x, y), typically used to specify the top-left corner of a cropping area, watermark, or source region.

### Parameters
- `x` (`int`): The horizontal component (in pixels) of the top-left corner of the image or region to be enclosed.
- `y` (`int`): The vertical component (in pixels) of the top-left corner of the image or region to be enclosed.

### Input
Integer values representing exact pixel coordinates. The caller must ensure these coordinates are valid relative to the target image's dimensions. It is typically passed into builder methods like `sourceRegion()` or `crop()`, often alongside a `Size` implementation (such as `AbsoluteSize`).

### Output
Returns `unspecified` — an instantiated `Coordinate` object (which implements the `Position` interface) representing the specified absolute (x, y) location.

### Valid Call Patterns
```java
// Defining a source region using Coordinate and AbsoluteSize directly in the builder
BufferedImage img = TestUtils.getImageFromResource("Thumbnailator/grid.png");
BufferedImage thumbnail = Thumbnails.of(img)
        .sourceRegion(new Coordinate(0, 0), new AbsoluteSize(50, 50))
        .size(50, 50)
        .asBufferedImage();

// Creating a Region object using Coordinate for use in the pipeline
Region region = new Region(new Coordinate(0, 0), new AbsoluteSize(50, 50));
BufferedImage thumbnailFromRegion = Thumbnails.of(img)
        .sourceRegion(region)
        .size(50, 50)
        .asBufferedImage();
```

### LLM Instruction Prompt
- Use `new Coordinate(x, y)` when an exact, absolute pixel position is required for operations like cropping or defining a source region.
- Pair it with `AbsoluteSize` or `RelativeSize` when defining a `Region`.
- Do not confuse `Coordinate` with the `Positions` enum (e.g., `Positions.TOP_LEFT`). Use `Coordinate` for exact pixel coordinates and `Positions` for relative alignment.

### Prompt Snippet
```text
To specify an exact pixel location for cropping or source regions in Thumbnailator, instantiate `new Coordinate(x, y)` from `net.coobird.thumbnailator.geometry.Coordinate`. Pass it to `.sourceRegion()` or `.crop()` alongside a `Size` object.
```

### Common Failure Modes
- **Out-of-Bounds Coordinates**: Providing `x` and `y` coordinates that, when combined with the specified `Size`, fall outside the bounds of the source image. This will cause the underlying Java 2D API to throw a `RasterFormatException` (e.g., "y + height is outside of Raster") during the pipeline execution.
- **Negative Coordinates**: Passing negative values for `x` or `y` when defining a standard crop region, which is generally invalid for standard image bounds starting at (0,0).

### Fix Code Hint
```java
// Ensure coordinates and size do not exceed the original image dimensions
int x = 0;
int y = 0;
int cropWidth = 50;
int cropHeight = 50;

// Safe usage with Coordinate
Thumbnails.of(img)
    .sourceRegion(new Coordinate(x, y), new AbsoluteSize(cropWidth, cropHeight))
    .size(50, 50)
    .asBufferedImage();

// Alternatively, if exact pixels aren't strictly required, use the Positions enum:
// .sourceRegion(Positions.TOP_LEFT, new AbsoluteSize(50, 50))
```

## API Test: `FileImageSink`

### Signature
```java
public FileImageSink(File destinationFile)
public FileImageSink(File destinationFile, boolean allowOverwrite)
public FileImageSink(String destinationFilePath)
public FileImageSink(String destinationFilePath, boolean allowOverwrite)
```
_Source: source/src/main/java/net/coobird/thumbnailator/tasks/io/FileImageSink.java:127  (+3 more definition site/overload)_

_Source doc:_ Instantiates a {@link FileImageSink} with the file to which the thumbnail should be written to. <p> The output format to use will be determined from the file extension. If another format should be used, then the {@link #setOutputFormatName(String)} should be called with the desired output format name. @param destinationFile		The destination file. @param allowOverwrite		Whether or not the {@code FileImageSink} should overwrite the destination file if it already exists. @throws NullPointerException	If the specified file is {@code null}.

### Goal
Instantiates an image sink that directs processed thumbnail output to a specified file on the filesystem, optionally allowing overwrites and automatically inferring the output format from the file extension.

### Parameters
- `destinationFile` (`File`): The destination file (or `String` file path in the overloaded constructors) where the processed thumbnail will be written.
- `allowOverwrite` (`boolean`): Whether the sink should overwrite the destination file if it already exists on the filesystem.

### Input
The caller must provide a valid, non-null `File` object or `String` path. To allow the sink to automatically determine the output format, the file name should include a standard image extension (e.g., `.jpg`, `.png`) supported by the host JVM's Image I/O capabilities. If the extension is missing or non-standard, the caller must explicitly configure the format later using `setOutputFormatName(String)`.

### Output
Returns `unspecified` — A new `FileImageSink` instance configured to write image data to the specified file during a `ThumbnailTask` execution.

### Valid Call Patterns
```java
// Using a File object (inferred from test suite)
File f = new File("test.png");
FileImageSink sink = new FileImageSink(f);

// Using a String path (inferred from test suite)
String path = "/absolute/path/to/test.png";
FileImageSink stringSink = new FileImageSink(path);

// Using a File object with explicit overwrite permission
FileImageSink overwriteSink = new FileImageSink(f, true);
```

### LLM Instruction Prompt
- Use `FileImageSink` when constructing custom `ThumbnailTask` pipelines that require routing processed images to the filesystem.
- Always ensure the provided `File` or `String` path is not `null` to prevent a `NullPointerException` during instantiation.
- Rely on the file extension (e.g., `.jpg`) to dictate the output format automatically, or be prepared to call `setOutputFormatName(String)` on the sink if the extension is absent.
- Note: For standard workflows, prefer the fluent builder API (`Thumbnails.of(...).toFile(...)`) over manually instantiating `FileImageSink`.

### Prompt Snippet
```text
When manually routing Thumbnailator output to a file via `FileImageSink`, provide a non-null `File` or `String` path. The output format is automatically inferred from the file extension. Use the two-argument constructor `new FileImageSink(file, true)` if you need to safely overwrite existing files.
```

### Common Failure Modes
- **`NullPointerException`**: Thrown immediately during instantiation if the `destinationFile` or `destinationFilePath` argument is `null`.
- **`UnsupportedFormatException`**: Thrown later during pipeline execution if the file extension does not map to a supported Java Image I/O format and no explicit format was set.
- **Overwrite Failures**: If `allowOverwrite` is `false` (or the single-argument constructor is used and defaults to preventing overwrites), attempting to write to an already existing file during task execution will fail.

### Fix Code Hint
```java
// BAD: Passing null or ignoring overwrite requirements
FileImageSink badSink = new FileImageSink(null); 

// GOOD: Providing a valid file with an extension and explicit overwrite flag
File outputFile = new File("output_thumbnail.jpg");
FileImageSink goodSink = new FileImageSink(outputFile, true);
```

## API Test: `FileImageSource`

### Signature
```java
public FileImageSource(File sourceFile)
public FileImageSource(String sourceFilePath)
```
_Source: source/src/main/java/net/coobird/thumbnailator/tasks/io/FileImageSource.java:86  (+1 more definition site/overload)_

_Source doc:_ Instantiates a {@link FileImageSource} with the specified file as the source image. @param sourceFile		The source image file. @throws NullPointerException	If the image is null.

### Goal
Instantiates an `ImageSource` that reads an image from a specified file or file path, typically used when constructing custom `ThumbnailTask` pipelines.

### Parameters
- `sourceFile` (`File`): The `java.io.File` representing the source image to be read. (An overload also accepts a `String sourceFilePath`).

### Input
A valid `java.io.File` or `String` path pointing to an image file. The file must exist and be readable when the source is eventually executed. The image format must be supported by the host JVM's standard Image I/O capabilities (e.g., JPEG, PNG, BMP). The input parameter must not be `null`.

### Output
Returns an instantiated `FileImageSource` object (an implementation of `ImageSource<File>`) that can be passed into a `ThumbnailTask` (such as `SourceSinkThumbnailTask`) to supply the source image data.

### Valid Call Patterns
```java
// Constructing a FileImageSource for a custom SourceSinkThumbnailTask
ThumbnailParameter param = new ThumbnailParameterBuilder().size(50, 50).format("jpg").build();
File sourceFile = new File("path/to/image.bmp");

FileImageSource source = new FileImageSource(sourceFile);
OutputStreamImageSink destination = new OutputStreamImageSink(new ByteArrayOutputStream());

Thumbnailator.createThumbnail(
    new SourceSinkThumbnailTask<File, OutputStream>(param, source, destination)
);
```

### LLM Instruction Prompt
- Use `FileImageSource` when manually constructing a `ThumbnailTask` (like `SourceSinkThumbnailTask`) that requires an explicit `ImageSource` abstraction.
- For standard thumbnail generation, strictly prefer the fluent `Thumbnails.of(File)` or `Thumbnails.fromFiles(Iterable)` API over manually instantiating `FileImageSource`.
- Do not pass `null` to the constructor, as it will immediately throw a `NullPointerException`.
- Be prepared to handle a `FileNotFoundException` when the `read()` method is subsequently called on the instantiated source if the file does not exist.

### Prompt Snippet
```text
When constructing custom `ThumbnailTask` instances, instantiate `FileImageSource` with a `java.io.File` or `String` path. Ensure the file exists and is in a format supported by Java Image I/O. Note: For standard usage, prefer the fluent `Thumbnails.of(File)` API instead of manual task construction.
```

### Common Failure Modes
- **`NullPointerException`**: Thrown immediately during instantiation if the provided `sourceFile` or `sourceFilePath` is `null`.
- **`FileNotFoundException`**: Thrown later when `source.read()` is invoked (often internally by the `ThumbnailTask`) if the specified file does not exist on the filesystem.
- **`UnsupportedFormatException`**: Thrown during the read phase if the file exists but its image format is not supported by the underlying Java Image I/O implementation.

### Fix Code Hint
```java
File sourceFile = new File("input.jpg");
if (!sourceFile.exists() || !sourceFile.isFile()) {
    throw new IllegalArgumentException("Source file must exist and be a valid file.");
}
// Safe to instantiate once existence is verified
FileImageSource source = new FileImageSource(sourceFile);
```

## API Test: `FileThumbnailTask`

### Signature
```java
public FileThumbnailTask(ThumbnailParameter param, File sourceFile, File destinationFile)
```
_Source: source/src/main/java/net/coobird/thumbnailator/tasks/FileThumbnailTask.java:61_

_Source doc:_ Creates a {@link ThumbnailTask} in which image data is read from the specified {@link File} and is output to a specified {@link File}, using the parameters provided in the specified {@link ThumbnailParameter}. @param param				The parameters to use to create the thumbnail. @param sourceFile		The {@link File} from which image data is read. @param destinationFile	The {@link File} to which thumbnail is written. @throws NullPointerException		If the parameter is {@code null}.

### Goal
Creates a `ThumbnailTask` that reads an image from a source file, applies the specified thumbnail parameters, and writes the processed image to a destination file.

### Parameters
- `param` (`ThumbnailParameter`): The configuration parameters (such as dimensions, output format, quality, and resizer algorithm) to use when creating the thumbnail. Must not be `null`.
- `sourceFile` (`File`): The `java.io.File` from which the original image data is read.
- `destinationFile` (`File`): The `java.io.File` to which the generated thumbnail is written.

### Input
Requires a fully constructed `ThumbnailParameter` instance containing the desired image transformations and rendering hints. The `sourceFile` must exist and be a readable image format supported by the host JVM's Image I/O. The `destinationFile` must be a valid path where the output can be written. 

### Output
Returns `unspecified` — A new `FileThumbnailTask` instance representing a pending file-to-file image processing operation that can be executed (e.g., by calling `read()`).

### Valid Call Patterns
```java
ThumbnailParameter param = new ThumbnailParameter(
        new Dimension(50, 50),
        null,
        true,
        "jpg",
        ThumbnailParameter.DEFAULT_FORMAT_TYPE,
        ThumbnailParameter.DEFAULT_QUALITY,
        BufferedImage.TYPE_INT_ARGB,
        null,
        Resizers.PROGRESSIVE,
        true,
        true
);

File inputFile = new File("input.jpg");
File outputFile = new File("output.png");

FileThumbnailTask task = new FileThumbnailTask(param, inputFile, outputFile);
task.read();
```

### LLM Instruction Prompt
- Use `FileThumbnailTask` only when building custom `ThumbnailTask` pipelines manually. For standard use cases, the fluent `Thumbnails.of(File).toFile(File)` API is strictly preferred.
- You must provide a non-null `ThumbnailParameter` to avoid a `NullPointerException`.
- Ensure the JVM's Image I/O supports the input and output formats specified in the parameters.

### Prompt Snippet
```text
When constructing a `FileThumbnailTask`, provide a non-null `ThumbnailParameter`, a source `File`, and a destination `File`. Note that the fluent `Thumbnails.of(file)...toFile(file)` builder is the strictly preferred paradigm for standard thumbnail generation; only use `FileThumbnailTask` for custom task abstractions.
```

### Common Failure Modes
- **`NullPointerException`**: Thrown immediately during instantiation if the `param` argument is `null`.
- **`UnsupportedFormatException`**: Thrown during task execution if the requested output format in `param` is not supported by the underlying Java Image I/O implementation.
- **File I/O Errors**: Thrown during execution if the `sourceFile` does not exist or the `destinationFile` cannot be written to (e.g., missing directory or permission issues).

### Fix Code Hint
```java
// If you encounter a NullPointerException, ensure param is initialized:
if (param == null) {
    throw new IllegalArgumentException("ThumbnailParameter cannot be null");
}
FileThumbnailTask task = new FileThumbnailTask(param, inputFile, outputFile);

// Alternatively, replace manual task creation with the preferred fluent API:
Thumbnails.of(inputFile)
    .size(50, 50)
    .outputFormat("jpg")
    .toFile(outputFile);
```

## API Test: `FixedResizerFactory`

### Signature
```java
public FixedResizerFactory(Resizer resizer)
```
_Source: source/src/main/java/net/coobird/thumbnailator/resizers/FixedResizerFactory.java:49_

_Source doc:_ Creates an instance of the {@link FixedResizerFactory} which returns the speicifed {@link Resizer} under all circumstances. @param resizer		The {@link Resizer} instance that is to be returned under all circumstances.

### Goal
Creates a `ResizerFactory` that unconditionally returns a specific `Resizer` implementation, bypassing the default dimension-based algorithm selection.

### Parameters
- `resizer` (`Resizer`): The specific `Resizer` instance (such as `Resizers.BICUBIC` or `Resizers.BILINEAR`) that this factory will return under all circumstances.

### Input
A valid, instantiated `Resizer` object. Typically, this is provided via the `Resizers` enum (e.g., `Resizers.BICUBIC`), which contains standard implementations of scaling algorithms.

### Output
Returns `unspecified` (constructor) — A new `FixedResizerFactory` instance that wraps and consistently yields the provided `Resizer`.

### Valid Call Patterns
```java
// Instantiate a factory that always returns a Bicubic resizer
Resizer resizer = Resizers.BICUBIC;
ResizerFactory factory = new FixedResizerFactory(resizer);

// The factory returns the exact same resizer regardless of source/target dimensions
Dimension sourceDimension = new Dimension(100, 100);
Dimension targetDimension = new Dimension(200, 200);
Resizer receivedResizer = factory.getResizer(sourceDimension, targetDimension);
```

### LLM Instruction Prompt
- When generating code that requires a strict, unchanging scaling algorithm across all image processing tasks, instantiate a `FixedResizerFactory` with the desired `Resizer`. This overrides the default behavior (which dynamically selects algorithms like `ProgressiveBilinearResizer` or `BicubicResizer` based on whether the image is being scaled up or down).

### Prompt Snippet
```text
To force a specific resizing algorithm regardless of the source and target image dimensions, wrap your chosen `Resizer` in a `FixedResizerFactory`:
`ResizerFactory factory = new FixedResizerFactory(Resizers.BICUBIC);`
```

### Common Failure Modes
- **Suboptimal Algorithm Selection**: Forcing a single resizer (like `BilinearResizer` or `BicubicResizer`) for all operations can lead to poor image quality or performance during extreme downscaling, where a `ProgressiveBilinearResizer` would normally be selected by the `DefaultResizerFactory`.

### Fix Code Hint
```java
// Safe instantiation using a known Resizer constant
Resizer resizer = Resizers.BICUBIC;
ResizerFactory factory = new FixedResizerFactory(resizer);

// Verify it returns the expected resizer even for arbitrary dimensions
Resizer activeResizer = factory.getResizer(new Dimension(1000, 1000), new Dimension(10, 10));
```

## API Test: `FixedSizeThumbnailMaker`

### Signature
```java
public FixedSizeThumbnailMaker()
public FixedSizeThumbnailMaker(int width, int height)
public FixedSizeThumbnailMaker(int width, int height, boolean aspectRatio)
public FixedSizeThumbnailMaker(int width, int height, boolean aspectRatio, boolean fit)
```
_Source: source/src/main/java/net/coobird/thumbnailator/makers/FixedSizeThumbnailMaker.java:158  (+3 more definition site/overload)_

_Source doc:_ Creates a {@link FixedSizeThumbnailMaker} which creates thumbnails with the specified size. Whether or not the aspect ratio of the original image should be preserved by the thumbnail, and whether to fit the thumbnail within the given dimensions is also specified at instantiation. @param width			The width of the thumbnail to produce. @param height		The height of the thumbnails to produce. @param aspectRatio	Whether or not to maintain the aspect ratio in the thumbnail the same as the original image. <p> If {@code true} is specified, then the thumbnail image will have the same aspect ratio as the original image. @param fit			Whether or not to fit the thumbnail within the specified dimensions. <p> If {@code true} is specified, then the thumbnail will be sized to fit within the specified {@code width} and {@code height}.

### Goal
Instantiates a `FixedSizeThumbnailMaker` that generates thumbnails at a specified size, with explicit control over aspect ratio preservation and bounding box fitting.

### Parameters
- `width` (`int`): The target width of the thumbnail to produce in pixels.
- `height` (`int`): The target height of the thumbnail to produce in pixels.
- `aspectRatio` (`boolean`): Whether to maintain the original image's aspect ratio (`true`) or allow the image to stretch/squash (`false`).
- `fit` (`boolean`): Whether to fit the thumbnail strictly within the specified `width` and `height` dimensions (`true`).

### Input
Requires valid positive integer dimensions for `width` and `height`. The instantiated maker is designed to process an in-memory `java.awt.image.BufferedImage` via its `make(BufferedImage)` method.

### Output
Returns a `FixedSizeThumbnailMaker` instance (a subclass of `ThumbnailMaker`) fully configured with the specified sizing and fitting rules, ready to process `BufferedImage` objects.

### Valid Call Patterns
```java
// Inferred from signature and test suite failure modes
BufferedImage img = new BufferedImage(200, 200, BufferedImage.TYPE_INT_ARGB);

// Use the 4-argument constructor to ensure the maker is fully initialized
FixedSizeThumbnailMaker maker = new FixedSizeThumbnailMaker(100, 100, true, true);
BufferedImage thumbnail = maker.make(img);
```

### LLM Instruction Prompt
- When manually constructing a `FixedSizeThumbnailMaker` (instead of using the preferred `Thumbnails.Builder` fluent API), you MUST use the 4-argument constructor `FixedSizeThumbnailMaker(int, int, boolean, boolean)` to ensure the maker is fully initialized.
- Do not use the 0-argument or 2-argument constructors followed immediately by `.make(img)`, as the test suite explicitly proves these leave the maker in an uninitialized state and will fail.

### Prompt Snippet
```text
To safely resize a BufferedImage using the lower-level ThumbnailMaker API, use `new FixedSizeThumbnailMaker(width, height, keepAspectRatio, fitWithinDimensions).make(bufferedImage)` to ensure all sizing rules are initialized.
```

### Common Failure Modes
- **Uninitialized Maker Exception**: Calling `make(BufferedImage)` on an instance created with the 0-argument or 2-argument constructor without further configuration results in a failure (e.g., `IllegalStateException`), as demonstrated by the `uninitializedWithNoArgConstructor` and `uninitializedWithTwoArgConstructor` tests.
- **Null Image**: Passing a `null` `BufferedImage` to the `make()` method of the constructed instance will cause a `NullPointerException`.

### Fix Code Hint
```java
// INSTEAD OF (Fails as uninitialized):
// new FixedSizeThumbnailMaker().make(img);
// new FixedSizeThumbnailMaker(100, 100).make(img);

// USE (Fully initialized):
BufferedImage thumbnail = new FixedSizeThumbnailMaker(100, 100, true, true).make(img);
```

## API Test: `IfdStructure`

### Signature
```java
public IfdStructure(int tag, int type, int count, int offsetValue)
```
_Source: source/src/main/java/net/coobird/thumbnailator/util/exif/IfdStructure.java:49_

_Source doc:_ Instantiates a IFD with the given attributes. @param tag			The tag element. @param type			The type element. @param count			The count of values. @param offsetValue	The offset or value.

### Goal
Instantiates an Image File Directory (IFD) data structure used internally for parsing Exif metadata tags (such as image orientation) from image files.

### Parameters
- `tag` (`int`): The integer identifier for the Exif tag element (e.g., `0x0112` for Orientation).
- `type` (`int`): The integer representing the data type of the tag (e.g., ASCII, SHORT, LONG, RATIONAL).
- `count` (`int`): The number of values associated with this tag.
- `offsetValue` (`int`): The actual inline value of the tag, or the offset to the value within the Exif data segment.

### Input
Four integers representing the parsed components of a standard 12-byte IFD entry from a TIFF/Exif metadata segment. The caller must have already extracted and converted these bytes into integers according to the image's byte order (endianness).

### Output
Returns `unspecified` — A new `IfdStructure` instance encapsulating the parsed Exif tag attributes.

### Valid Call Patterns
```java
// Inferred from signature (not verified)
int tag = 0x0112; // Orientation
int type = 3;     // SHORT
int count = 1;
int offsetValue = 6; // e.g., TopRight

IfdStructure ifdEntry = new IfdStructure(tag, type, count, offsetValue);
```

### LLM Instruction Prompt
- Do not use `IfdStructure` for standard image orientation correction; it is a low-level metadata parsing structure. Instead, use `ExifUtils.getExifOrientation` and `ExifFilterUtils.getFilterForOrientation` to handle Exif rotation automatically.
- If manually parsing Exif data, ensure the 12-byte IFD entry is correctly split and converted to integers (accounting for endianness) before passing to this constructor.

### Prompt Snippet
```text
When instantiating `IfdStructure`, provide the tag, type, count, and offsetValue integers parsed from the Exif IFD entry. For standard thumbnail orientation, prefer `ExifUtils.getExifOrientation` over manual IFD parsing.
```

### Common Failure Modes
- **Manual Parsing Errors**: Attempting to manually parse Exif data and passing raw bytes or incorrectly endian-swapped integers to the constructor, resulting in corrupted metadata reads.
- **Reinventing the Wheel**: Using this class to manually determine image orientation instead of leveraging Thumbnailator's built-in `ExifUtils`.

### Fix Code Hint
```java
// Instead of manually parsing IFD structures to fix orientation:
// IfdStructure ifd = new IfdStructure(...); 

// Use the built-in Exif utilities provided by Thumbnailator:
Orientation orientation = ExifUtils.getExifOrientation(imageInputStream);
ImageFilter orientationFilter = ExifFilterUtils.getFilterForOrientation(orientation);

Thumbnails.of(imageInputStream)
    .size(640, 480)
    .addFilter(orientationFilter)
    .toFile("output.jpg");
```

## API Test: `InputStreamImageSource`

### Signature
```java
public InputStreamImageSource(InputStream is)
```
_Source: source/src/main/java/net/coobird/thumbnailator/tasks/io/InputStreamImageSource.java:78_

_Source doc:_ Instantiates an {@link InputStreamImageSource} with the {@link InputStream} which will be used to read the source image. @param is		The {@link InputStream} which is to be used to obtain the source image. @throws NullPointerException		If the {@link InputStream} is {@code null}.

### Goal
Instantiates an `ImageSource` that reads a source image from a provided `InputStream` for use in custom `ThumbnailTask` processing pipelines.

### Parameters
- `is` (`InputStream`): The `InputStream` which is to be used to obtain the source image data.

### Input
An open `InputStream` containing image data in a format supported by the host JVM's standard Image I/O capabilities. The stream must not be `null`.

### Output
Returns `unspecified` — represents a newly constructed `InputStreamImageSource` instance that acts as the source component for a `SourceSinkThumbnailTask`.

### Valid Call Patterns
```java
// Constructing a custom task pipeline reading from an InputStream and writing to a BufferedImage
ThumbnailParameter param = new ThumbnailParameterBuilder().size(50, 50).build();

// 'is' represents a valid, open InputStream containing image data
InputStreamImageSource source = new InputStreamImageSource(is);
BufferedImageSink destination = new BufferedImageSink();

Thumbnailator.createThumbnail(
    new SourceSinkThumbnailTask<InputStream, BufferedImage>(param, source, destination)
);
BufferedImage thumbnail = destination.getSink();
```

### LLM Instruction Prompt
- Use `new InputStreamImageSource(is)` when manually constructing a `SourceSinkThumbnailTask` that reads from an `InputStream`.
- Do not pass a `null` `InputStream`, as it will immediately throw a `NullPointerException`.
- Note that for standard workflows, the fluent API `Thumbnails.of(InputStream...)` or `Thumbnails.fromInputStreams(Iterable)` is strictly preferred over manual task and source construction.
- The library relies entirely on the host JVM's standard Image I/O capabilities; ensure the stream provides a supported format.

### Prompt Snippet
```text
To use an InputStream as an image source in a custom ThumbnailTask pipeline, instantiate `new InputStreamImageSource(inputStream)`. Ensure the stream is not null and contains an image format supported by the JVM's Image I/O. For standard usage, prefer the fluent `Thumbnails.of(inputStream)` API instead.
```

### Common Failure Modes
- **`NullPointerException`**: Thrown immediately during instantiation if the provided `InputStream` is `null`.
- **`UnsupportedFormatException`**: Thrown later during task execution if the stream contains an image format that the underlying Java Image I/O does not support.

### Fix Code Hint
```java
// Ensure the InputStream is not null before instantiating the source
if (is == null) {
    throw new IllegalArgumentException("Source InputStream cannot be null");
}
InputStreamImageSource source = new InputStreamImageSource(is);
```

## API Test: `NullResizer`

### Signature
```java
public NullResizer()
```
_Source: source/src/main/java/net/coobird/thumbnailator/resizers/NullResizer.java:48_

_Source doc:_ Instantiates the {@code NullResizer} which draws the source image at the origin of the destination image.

### Goal
Instantiates a `NullResizer` that performs no actual scaling, but instead draws the unscaled source image directly at the origin (top-left corner, 0,0) of the destination image.

### Parameters
_None._

### Input
This constructor takes no arguments. The instantiated `NullResizer` expects a source `BufferedImage` and a destination `BufferedImage` when its `resize(BufferedImage, BufferedImage)` method is subsequently called.

### Output
Returns `unspecified` — an instance of `NullResizer` (which implements the `Resizer` interface) that can be used in an image processing pipeline or called directly to transfer image data without applying any scaling algorithms.

### Valid Call Patterns
```java
// given
BufferedImage srcImage = getImageFromResource("Thumbnailator/grid.png");
BufferedImage destImage = new BufferedImage(200, 200, BufferedImage.TYPE_INT_ARGB);

// when
new NullResizer().resize(srcImage, destImage);
```

### LLM Instruction Prompt
- Use `new NullResizer()` when you need to transfer a source image onto a destination `BufferedImage` canvas without altering the source image's original dimensions.
- Remember that because this resizer does not scale, if the destination image is smaller than the source image, the drawn image will be effectively cropped to the destination's dimensions.
- Do not use this if you need to fit or scale the image; use `BicubicResizer`, `BilinearResizer`, or `ProgressiveBilinearResizer` instead.

### Prompt Snippet
```text
When placing an image onto a larger canvas without scaling it, instantiate a `NullResizer` and call its `resize` method. It draws the source image exactly at the (0,0) origin of the destination `BufferedImage`.
```

### Common Failure Modes
- **Cropped Output**: If the destination `BufferedImage` provided to the `resize` method is smaller than the source image, the source image will be truncated/cropped because `NullResizer` enforces a 1:1 pixel mapping without scaling.
- **Null Image Arguments**: Passing `null` for either the source or destination `BufferedImage` to the subsequent `resize` method will result in a `NullPointerException` during the internal `Graphics2D` drawing phase.

### Fix Code Hint
```java
// Ensure the destination image is large enough to hold the source image if cropping is not desired
BufferedImage destImage = new BufferedImage(
    Math.max(srcImage.getWidth(), desiredWidth), 
    Math.max(srcImage.getHeight(), desiredHeight), 
    BufferedImage.TYPE_INT_ARGB
);
new NullResizer().resize(srcImage, destImage);
```

## API Test: `OutputStreamImageSink`

### Signature
```java
public OutputStreamImageSink(OutputStream os)
```
_Source: source/src/main/java/net/coobird/thumbnailator/tasks/io/OutputStreamImageSink.java:66_

_Source doc:_ Instantiates an {@link OutputStreamImageSink} with the {@link OutputStream} to which the thumbnail should be written to. @param os		The {@link OutputStream} to write the thumbnail to. @throws NullPointerException		If the {@link OutputStream} is {@code null}.

### Goal
Instantiates an image sink that directs the processed thumbnail output to a specified `OutputStream`.

### Parameters
- `os` (`OutputStream`): The destination stream (e.g., `ByteArrayOutputStream`, `FileOutputStream`) where the generated thumbnail image data will be written.

### Input
A valid, non-null `java.io.OutputStream`. The stream must be open and writable, as the underlying `ThumbnailTask` will attempt to write the encoded image bytes (e.g., JPEG, PNG) to it during execution.

### Output
Returns `unspecified` (Constructor) — An initialized `OutputStreamImageSink` instance that acts as the destination component for a custom `ThumbnailTask` (such as `SourceSinkThumbnailTask`).

### Valid Call Patterns
```java
// Constructing a sink for a custom SourceSinkThumbnailTask
ThumbnailParameter param = new ThumbnailParameterBuilder().size(50, 50).format("jpg").build();
InputStream is = TestUtils.getResourceStream("Thumbnailator/grid.png");
ByteArrayOutputStream os = new ByteArrayOutputStream();

InputStreamImageSource source = new InputStreamImageSource(is);
OutputStreamImageSink destination = new OutputStreamImageSink(os);

Thumbnailator.createThumbnail(
    new SourceSinkThumbnailTask<InputStream, OutputStream>(param, source, destination)
);
```

### LLM Instruction Prompt
- When building custom `SourceSinkThumbnailTask` pipelines that output to memory or network streams, instantiate `OutputStreamImageSink` with the target `OutputStream`.
- Do not pass a `null` stream, as it will immediately throw a `NullPointerException`.
- Note that while `OutputStreamImageSink` wraps the stream for the task, the caller is typically responsible for managing the stream's lifecycle (e.g., closing it in a `finally` block or try-with-resources) after the `Thumbnailator.createThumbnail(...)` execution completes.

### Prompt Snippet
```text
To route thumbnail output to a stream in a custom task pipeline, instantiate `new OutputStreamImageSink(os)` with a non-null `OutputStream`. Pass this sink to a `SourceSinkThumbnailTask`.
```

### Common Failure Modes
- **`NullPointerException`**: Thrown immediately during instantiation if the provided `OutputStream os` is `null`.
- **`IOException` during execution**: If the provided `OutputStream` is already closed or becomes unwritable, the sink will fail when the `ThumbnailTask` attempts to write the image data to it.
- **Unsupported Format**: If the `ThumbnailParameter` specifies an output format not supported by the JVM's Image I/O, the task writing to this sink will throw an `UnsupportedFormatException`.

### Fix Code Hint
```java
// Ensure the stream is non-null and safely managed
try (ByteArrayOutputStream os = new ByteArrayOutputStream()) {
    if (os == null) {
        throw new IllegalArgumentException("OutputStream cannot be null");
    }
    OutputStreamImageSink destination = new OutputStreamImageSink(os);
    // ... use destination in a SourceSinkThumbnailTask
} catch (IOException e) {
    // Handle stream errors
}
```

## API Test: `Pipeline`

### Signature
```java
public Pipeline()
public Pipeline(ImageFilter... filters)
public Pipeline(List<ImageFilter> filters)
```
_Source: source/src/main/java/net/coobird/thumbnailator/filters/Pipeline.java:73  (+2 more definition site/overload)_

_Source doc:_ Instantiates a new {@link Pipeline} with an array of {@link ImageFilter}s to apply. @param filters		An array of {@link ImageFilter}s to apply.

### Goal
Instantiates a new image processing pipeline that sequentially applies a collection of `ImageFilter` transformations to a `BufferedImage`.

### Parameters
- `filters` (`ImageFilter...`): An array (or varargs) of `ImageFilter` implementations (such as `Rotation`, `Watermark`, `Canvas`, or `Colorize`) to apply in order.

### Input
The caller must provide zero or more `ImageFilter` objects. If using the `List` overload, a valid `List<ImageFilter>` must be provided. The resulting `Pipeline` is designed to process in-memory `BufferedImage` objects via its `apply(BufferedImage)` method. 

### Output
Returns `unspecified` — a new `Pipeline` instance representing an ordered, executable sequence of image filters ready to transform a `BufferedImage`.

### Valid Call Patterns
```java
// 1. Using the varargs constructor
BufferedImage img = new BufferedImage(200, 200, BufferedImage.TYPE_INT_ARGB);
ImageFilter filter1 = mock(ImageFilter.class); // In production, use a real filter e.g., new Rotation(90)

Pipeline pipeline = new Pipeline(filter1);
pipeline.apply(img);

// 2. Using the List constructor
Pipeline listPipeline = new Pipeline(Arrays.asList(filter1));
listPipeline.apply(img);
```

### LLM Instruction Prompt
- Use `Pipeline` only when low-level, direct manipulation of a `BufferedImage` is strictly required (e.g., inside custom `ThumbnailTask` implementations). 
- For standard image processing and thumbnail generation, strictly prefer the fluent `Thumbnails.Builder` API (e.g., `Thumbnails.of(...).addFilter(...)`), which automatically handles Image I/O, Exif orientation, and boilerplate `Graphics2D` operations.
- When constructing a `Pipeline`, ensure the order of filters is logically sound (e.g., applying a `Canvas` crop before a `Watermark` may change the watermark's relative positioning).

### Prompt Snippet
```text
To apply a sequence of custom filters directly to an in-memory BufferedImage outside the standard builder, instantiate a Pipeline:
`Pipeline pipeline = new Pipeline(new Rotation(90), new Watermark(...)); pipeline.apply(bufferedImage);`
Note: For standard file/stream workflows, always use `Thumbnails.of().addFilter()` instead.
```

### Common Failure Modes
- **Bypassing Exif Correction**: Manually applying a `Pipeline` to a `BufferedImage` bypasses the automatic Exif orientation parsing (`ExifUtils.getExifOrientation`) provided by the fluent `Thumbnails` API, potentially resulting in incorrectly rotated images.
- **Null Inputs**: Passing a null array or list to the constructor, or passing a null `BufferedImage` to `apply()`, will result in a `NullPointerException`.
- **Missing Image I/O**: `Pipeline` only operates on `BufferedImage`. It cannot read from or write to files, streams, or URLs directly.

### Fix Code Hint
```java
// BAD: Manually managing a Pipeline and Image I/O for standard thumbnail generation
BufferedImage img = ImageIO.read(new File("input.jpg"));
Pipeline pipeline = new Pipeline(new Rotation(90));
pipeline.apply(img);
ImageIO.write(img, "jpg", new File("output.jpg"));

// GOOD: Use the strictly preferred fluent API which handles I/O and pipelines automatically
Thumbnails.of(new File("input.jpg"))
    .scale(1.0) // Required by builder if not resizing
    .addFilter(new Rotation(90))
    .toFile(new File("output.jpg"));
```

## API Test: `ProgressiveBilinearResizer`

### Signature
```java
public ProgressiveBilinearResizer()
public ProgressiveBilinearResizer(Map<RenderingHints.Key, Object> hints)
```
_Source: source/src/main/java/net/coobird/thumbnailator/resizers/ProgressiveBilinearResizer.java:70  (+1 more definition site/overload)_

_Source doc:_ Instantiates a {@link ProgressiveBilinearResizer} with the specified rendering hints. @param hints		Additional rendering hints to apply.

### Goal
Instantiates a resizer that performs progressive bilinear scaling, typically used for high-quality downscaling of images by iteratively halving the image dimensions.

### Parameters
- `hints` (`Map<RenderingHints.Key, Object>`): A map of Java 2D `RenderingHints` (e.g., antialiasing, dithering, or interpolation settings) to apply to the underlying `Graphics2D` object during the resizing process.

### Input
Valid `RenderingHints` keys and values if using the parameterized constructor. If no custom hints are needed, the caller should use the no-argument constructor. The resulting object is designed to operate strictly on in-memory `BufferedImage` instances.

### Output
Returns `unspecified` — A new `ProgressiveBilinearResizer` instance that implements the `Resizer` interface, ready to be used directly or returned by a custom `ResizerFactory`.

### Valid Call Patterns
```java
// 1. Default instantiation (verified in test suite)
Resizer resizer = new ProgressiveBilinearResizer();

// 2. Instantiation with custom rendering hints (inferred from signature)
Map<RenderingHints.Key, Object> hints = new HashMap<>();
hints.put(RenderingHints.KEY_RENDERING, RenderingHints.VALUE_RENDER_QUALITY);
hints.put(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
Resizer customResizer = new ProgressiveBilinearResizer(hints);
```

### LLM Instruction Prompt
- Use `ProgressiveBilinearResizer` when implementing a custom `ResizerFactory` or `ThumbnailMaker` that requires high-quality downscaling.
- Prefer the fluent `Thumbnails.Builder` API for standard workflows, as it automatically selects the appropriate resizer based on the target dimensions. Manually instantiate this class only for advanced, custom pipeline configurations.
- Use the no-argument constructor unless specific `Graphics2D` rendering hints are strictly required.
- Remember that `Resizer` implementations operate exclusively on `BufferedImage` objects, not files or streams.

### Prompt Snippet
```text
When building a custom `ResizerFactory` for Thumbnailator, return `new ProgressiveBilinearResizer()` to ensure high-quality progressive downscaling of `BufferedImage` instances. If custom Java 2D rendering behavior is needed, pass a `Map<RenderingHints.Key, Object>` to the constructor.
```

### Common Failure Modes
- **Null Hints Map**: Passing a `null` map to the parameterized constructor instead of using the no-argument constructor may lead to a `NullPointerException` during rendering.
- **Manual Resizer Misuse**: Attempting to use this resizer directly on files, streams, or URLs. `Resizer` implementations only operate on in-memory `BufferedImage` objects; I/O must be handled separately or via the `Thumbnails` fluent API.
- **Upscaling Inefficiency**: Progressive bilinear resizing is optimized for downscaling. While it will function for upscaling, it does not provide the same quality benefits as it does when reducing image dimensions.

### Fix Code Hint
```java
// Incorrect: Passing null to the hints constructor
// Resizer resizer = new ProgressiveBilinearResizer(null);

// Correct: Use the no-argument constructor for default hints
Resizer resizer = new ProgressiveBilinearResizer();

// Correct usage in a custom factory
ResizerFactory factory = new ResizerFactory() {
    @Override
    public Resizer getResizer(Dimension originalSize, Dimension thumbnailSize) {
        // Progressive bilinear is ideal for downscaling
        return new ProgressiveBilinearResizer();
    }
};
```

## API Test: `Region`

### Signature
```java
public Region(Position position, Size size)
```
_Source: source/src/main/java/net/coobird/thumbnailator/geometry/Region.java:59_

_Source doc:_ Instantiates a representation of a region from a {@link Position} and {@link Size}. @param position		Position of the region. @param size			Size of the region. @throws NullPointerException		When the position and/or the size is {@code null}.

### Goal
Instantiates a representation of a rectangular region defined by a specific position and size, typically used to define a cropping area or source region in an image processing pipeline.

### Parameters
- `position` (`Position`): The starting coordinate or alignment of the region (e.g., a `Coordinate` instance or a `Positions` enum value).
- `size` (`Size`): The dimensions of the region (e.g., an `AbsoluteSize` or `RelativeSize` instance).

### Input
Requires non-null `Position` and `Size` objects. The `Position` dictates where the region is anchored (such as an exact X/Y coordinate), and the `Size` dictates its width and height.

### Output
Returns a new `Region` instance representing the specified area, which can be passed to builder methods like `sourceRegion(Region)`.

### Valid Call Patterns
```java
// Defining a region using exact coordinates and absolute dimensions
Region region = new Region(new Coordinate(0, 0), new AbsoluteSize(50, 50));

// Applying the region to crop a source image in a Thumbnailator pipeline
BufferedImage thumbnail = Thumbnails.of(img)
        .sourceRegion(new Region(new Coordinate(0, 0), new AbsoluteSize(50, 50)))
        .size(50, 50)
        .asBufferedImage();
```

### LLM Instruction Prompt
- When defining a specific area of an image to crop or process, instantiate a `Region` using a concrete `Position` (like `Coordinate`) and a concrete `Size` (like `AbsoluteSize`). Pass this `Region` to `Thumbnails.Builder.sourceRegion()`. Never pass `null` for either parameter.

### Prompt Snippet
```text
new Region(new Coordinate(x, y), new AbsoluteSize(width, height))
```

### Common Failure Modes
- **`NullPointerException`**: Thrown immediately if either the `position` or `size` argument is `null`.

### Fix Code Hint
```java
// Ensure both Position and Size are instantiated before passing to Region
Position pos = new Coordinate(x, y);
Size dim = new AbsoluteSize(width, height);
Region cropRegion = new Region(pos, dim);
```

## API Test: `RelativeSize`

### Signature
```java
public RelativeSize(double scalingFactor)
```
_Source: source/src/main/java/net/coobird/thumbnailator/geometry/RelativeSize.java:52_

_Source doc:_ Instantiates an object which calculates the size of an object, using the given scaling factor. @param scalingFactor		The scaling factor to use to determine the size of the enclosing object. @throws IllegalArgumentException		When the scaling factor is not within the range of {@code 0.0d} and {@code 1.0d}, inclusive.

### Goal
Instantiates a geometry object that calculates dimensions relative to an enclosing object's size using a proportional scaling factor.

### Parameters
- `scalingFactor` (`double`): The scaling factor to use to determine the size of the enclosing object. Must be between `0.0d` and `1.0d`, inclusive.

### Input
A `double` representing the desired proportion (e.g., `0.5d` for 50% of the enclosing object's size). 
**Precondition:** The value must be strictly within the inclusive range of `0.0d` to `1.0d`.

### Output
Returns `unspecified` — A new `RelativeSize` instance (which implements the `Size` interface) for use in Thumbnailator geometry, cropping, or positioning operations.

### Valid Call Patterns
```java
// Inferred from signature (not verified)
RelativeSize halfSize = new RelativeSize(0.5d);
```

### LLM Instruction Prompt
- When instantiating `RelativeSize`, you MUST provide a `double` scaling factor between `0.0d` and `1.0d` inclusive. Do not pass whole-number percentages (e.g., `50.0`) or negative values, as these violate the strict preconditions of the constructor.

### Prompt Snippet
```text
RelativeSize relativeSize = new RelativeSize(0.75d);
```

### Common Failure Modes
- **`IllegalArgumentException`**: Thrown when the `scalingFactor` is not within the range of `0.0d` and `1.0d`, inclusive (e.g., passing `50.0` instead of `0.5`).

### Fix Code Hint
```java
// Ensure the scaling factor is normalized to a fraction between 0.0 and 1.0
double safeScalingFactor = Math.max(0.0d, Math.min(1.0d, rawPercentage / 100.0d));
RelativeSize size = new RelativeSize(safeScalingFactor);
```

## API Test: `ScaledThumbnailMaker`

### Signature
```java
public ScaledThumbnailMaker()
public ScaledThumbnailMaker(double factor)
public ScaledThumbnailMaker(double widthFactor, double heightFactor)
```
_Source: source/src/main/java/net/coobird/thumbnailator/makers/ScaledThumbnailMaker.java:128  (+2 more definition site/overload)_

_Source doc:_ Creates an instance of {@code ScaledThumbnailMaker} with the specified scaling factors for the width and height. @param widthFactor		The scaling factor to apply to the width when resizing an image to create a thumbnail. @param heightFactor		The scaling factor to apply to the height when resizing an image to create a thumbnail. @since	0.3.10

### Goal
Creates an instance of `ScaledThumbnailMaker` configured to resize images by multiplying their original width and height by the specified scaling factors.

### Parameters
- `widthFactor` (`double`): The scaling factor to apply to the width when resizing an image (e.g., `0.5` reduces the width by half).
- `heightFactor` (`double`): The scaling factor to apply to the height when resizing an image.

### Input
Requires positive `double` values for the scaling factors. The instantiated maker is designed to process an in-memory `java.awt.image.BufferedImage` passed to its `make(BufferedImage)` method.

### Output
Returns `unspecified` — A configured `ScaledThumbnailMaker` instance ready to process `BufferedImage` objects and output scaled `BufferedImage` thumbnails.

### Valid Call Patterns
```java
// Setup an in-memory image (e.g., 200x200)
BufferedImage img = new BufferedImage(200, 200, BufferedImage.TYPE_INT_ARGB);

// Using the one-argument constructor (proportional scaling)
BufferedImage proportionalThumbnail = new ScaledThumbnailMaker(0.5).make(img);

// Using the two-argument constructor (independent width/height scaling)
BufferedImage disproportionateThumbnail = new ScaledThumbnailMaker(0.5, 0.25).make(img);
```

### LLM Instruction Prompt
- Use `ScaledThumbnailMaker` only when constructing custom, low-level `ThumbnailTask` pipelines or extending the library's internals. For standard image resizing, strictly prefer the fluent API (e.g., `Thumbnails.of(img).scale(widthFactor, heightFactor)`).
- Never call `make()` on an uninitialized `ScaledThumbnailMaker` created with the no-arg constructor, as it will fail deterministically. Always use the parameterized constructors.

### Prompt Snippet
```text
Prefer the fluent `Thumbnails.of(img).scale(w, h)` API over manual `ScaledThumbnailMaker` instantiation. If you must use `ScaledThumbnailMaker` for custom pipelines, always use the parameterized constructors `(double)` or `(double, double)` to prevent uninitialized state errors when calling `.make(img)`.
```

### Common Failure Modes
- **Uninitialized State**: Instantiating the maker using the no-arg constructor (`new ScaledThumbnailMaker()`) and immediately calling `.make(img)` without setting the scale factors will throw an exception (as explicitly verified by the project's test suite).
- **Negative or Zero Factors**: Providing `0.0` or negative values for `widthFactor` or `heightFactor` will result in an `IllegalArgumentException` when the underlying geometry calculations are performed.

### Fix Code Hint
```java
// BAD: Uninitialized maker throws an exception upon calling make()
// BufferedImage thumbnail = new ScaledThumbnailMaker().make(img);

// GOOD: Initialize with scaling factors via the constructor
BufferedImage thumbnail = new ScaledThumbnailMaker(0.5, 0.5).make(img);
```

## API Test: `SourceSinkThumbnailTask`

### Signature
```java
public SourceSinkThumbnailTask(ThumbnailParameter param, ImageSource<S> source, ImageSink<D> destination)
```
_Source: source/src/main/java/net/coobird/thumbnailator/tasks/SourceSinkThumbnailTask.java:77_

_Source doc:_ Creates a {@link ThumbnailTask} in which an image is retrived from the specified {@link ImageSource} and written to the specified {@link ImageSink}, using the parameters provided in the specified {@link ThumbnailParameter}. @param param				The parameters to use to create the thumbnail. @param source			The source from which the image is retrieved or read from. @param destination		The destination to which the thumbnail is stored or written to. @throws NullPointerException		If either the parameter, {@link ImageSource} or {@link ImageSink} is {@code null}.

### Goal
Creates a `ThumbnailTask` that encapsulates the entire pipeline of reading an image from a source, applying transformations defined by parameters, and writing the result to a destination sink.

### Parameters
- `param` (`ThumbnailParameter`): The configuration parameters (such as size, output format, and filters) to use when creating the thumbnail. Typically constructed using a `ThumbnailParameterBuilder`.
- `source` (`ImageSource<S>`): The source abstraction (e.g., `FileImageSource`, `BufferedImageSource`) from which the original image is retrieved or read.
- `destination` (`ImageSink<D>`): The destination abstraction (e.g., `FileImageSink`, `BufferedImageSink`) to which the processed thumbnail is stored or written.

### Input
The caller must provide a fully constructed `ThumbnailParameter`, a valid `ImageSource`, and a valid `ImageSink`. None of these arguments can be `null`. If format resolution is required (e.g., `ThumbnailParameter.DETERMINE_FORMAT` or `ThumbnailParameter.ORIGINAL_FORMAT`), the `ImageSource` and `ImageSink` must be capable of reporting their input and preferred output formats respectively.

### Output
Returns `unspecified` — A new `SourceSinkThumbnailTask` instance representing the configured image processing job. This task is not executed upon instantiation; it must be passed to `Thumbnailator.createThumbnail(ThumbnailTask)` to run the pipeline.

### Valid Call Patterns
```java
// Constructing the parameters for the task
ThumbnailParameter param = new ThumbnailParameterBuilder()
    .size(50, 50)
    .format(ThumbnailParameter.ORIGINAL_FORMAT)
    .build();

// Assuming 'source' is a valid ImageSource and 'destination' is a valid ImageSink
// (e.g., BufferedImageSource and BufferedImageSink)
SourceSinkThumbnailTask task = new SourceSinkThumbnailTask(param, source, destination);

// Executing the task
Thumbnailator.createThumbnail(task);
```

### LLM Instruction Prompt
- When building advanced or custom image processing pipelines outside of the fluent `Thumbnails.Builder` API, instantiate a `SourceSinkThumbnailTask` with a `ThumbnailParameter`, an `ImageSource`, and an `ImageSink`.
- Never pass `null` to any of the constructor arguments.
- The task does not execute itself; you must pass the instantiated `SourceSinkThumbnailTask` to `Thumbnailator.createThumbnail(task)` to perform the actual image processing.

### Prompt Snippet
```text
To execute a custom source-to-sink pipeline in Thumbnailator, build a `ThumbnailParameter` using `ThumbnailParameterBuilder`, instantiate your `ImageSource` and `ImageSink`, and pass them to `new SourceSinkThumbnailTask(param, source, sink)`. Finally, execute it with `Thumbnailator.createThumbnail(task)`.
```

### Common Failure Modes
- **`NullPointerException`**: Thrown immediately during instantiation if `param`, `source`, or `destination` is `null`.
- **Format Resolution Failures**: If the `ThumbnailParameter` specifies `ORIGINAL_FORMAT` but the `ImageSource` cannot determine the original format (or if the underlying Java Image I/O does not support writing it), the execution phase (`Thumbnailator.createThumbnail`) will fail.

### Fix Code Hint
```java
if (param == null || source == null || destination == null) {
    throw new IllegalArgumentException("ThumbnailParameter, ImageSource, and ImageSink must not be null");
}
SourceSinkThumbnailTask task = new SourceSinkThumbnailTask(param, source, destination);
Thumbnailator.createThumbnail(task);
```

## API Test: `StreamThumbnailTask`

### Signature
```java
public StreamThumbnailTask(ThumbnailParameter param, InputStream is, OutputStream os)
```
_Source: source/src/main/java/net/coobird/thumbnailator/tasks/StreamThumbnailTask.java:66_

_Source doc:_ Creates a {@link ThumbnailTask} in which streamed image data from the specified {@link InputStream} is output to a specified {@link OutputStream}, using the parameters provided in the specified {@link ThumbnailParameter}. @param param		The parameters to use to create the thumbnail. @param is		The {@link InputStream} from which to obtain image data. @param os		The {@link OutputStream} to send thumbnail data to. @throws NullPointerException		If the parameter is {@code null}.

### Goal
Creates a task that reads source image data from an input stream, applies transformations defined by the provided parameters, and writes the resulting thumbnail to an output stream.

### Parameters
- `param` (`ThumbnailParameter`): The configuration parameters (such as dimensions, output format, image type, and resizer algorithms) to use when creating the thumbnail. Must not be `null`.
- `is` (`InputStream`): The stream from which to obtain the source image data.
- `os` (`OutputStream`): The stream to which the generated thumbnail image data will be written.

### Input
The caller must provide a fully constructed, non-null `ThumbnailParameter` object. The `InputStream` must provide valid image data in a format supported by the host JVM's standard Image I/O capabilities. Both the `InputStream` and `OutputStream` must be open and accessible. 

### Output
Returns `unspecified` — A new `StreamThumbnailTask` instance configured to process the image data between the provided streams.

### Valid Call Patterns
```java
ThumbnailParameter param = new ThumbnailParameter(
        new Dimension(50, 50),
        null,
        true,
        "png",
        ThumbnailParameter.DEFAULT_FORMAT_TYPE,
        ThumbnailParameter.DEFAULT_QUALITY,
        BufferedImage.TYPE_INT_ARGB,
        null,
        Resizers.PROGRESSIVE,
        true,
        true
);

InputStream is = new FileInputStream(inputFile);
OutputStream os = new FileOutputStream(outputFile);

// Create the task
StreamThumbnailTask task = new StreamThumbnailTask(param, is, os);

// The task can then be executed (e.g., task.read() to get the BufferedImage)
BufferedImage img = task.read();
```

### LLM Instruction Prompt
- Do not pass `null` for the `ThumbnailParameter`; doing so will immediately throw a `NullPointerException`.
- `StreamThumbnailTask` does **not** automatically close the provided `InputStream` or `OutputStream`. The caller is strictly responsible for managing the lifecycle of these streams (e.g., using try-with-resources).
- For standard workflows, prefer the fluent API (`Thumbnails.fromInputStreams(...).toOutputStream(...)`) over manually instantiating `StreamThumbnailTask`, unless building a highly customized `ThumbnailTask` pipeline.

### Prompt Snippet
```text
When constructing a `StreamThumbnailTask`, you must provide a non-null `ThumbnailParameter`, an open `InputStream`, and an open `OutputStream`. The task reads from the input and writes to the output but does not close either stream; you must manage stream closures manually.
```

### Common Failure Modes
- **NullPointerException**: Thrown immediately during instantiation if the `param` argument is `null`.
- **Resource Leaks**: Because `StreamThumbnailTask` does not close the `InputStream` or `OutputStream` (as verified by `verify(spyIs, never()).close()` in the test suite), failing to close them in the calling code will leak file handles or memory.
- **UnsupportedFormatException**: Occurs during task execution if the `InputStream` contains an image format, or the `ThumbnailParameter` requests an output format, that the underlying Java Image I/O does not support.

### Fix Code Hint
```java
// Wrap streams in try-with-resources to prevent resource leaks, 
// as StreamThumbnailTask will not close them for you.
try (InputStream is = new FileInputStream(inputFile);
     OutputStream os = new FileOutputStream(outputFile)) {
    
    StreamThumbnailTask task = new StreamThumbnailTask(param, is, os);
    // execute task...
}
```

## API Test: `ThumbnailMaker`

### Signature
```java
public ThumbnailMaker()
```
_Source: source/src/main/java/net/coobird/thumbnailator/makers/ThumbnailMaker.java:163_

_Source doc:_ Creates and initializes an instance of {@link ThumbnailMaker}.

### Goal
Creates and initializes a new instance of `ThumbnailMaker` for advanced, manual thumbnail generation workflows.

### Parameters
_None._

### Input
No arguments are required to invoke the constructor. 

### Output
Returns `unspecified` (Constructor) — A newly initialized instance of `ThumbnailMaker` that can be subsequently configured to process `BufferedImage` objects.

### Valid Call Patterns
```java
// Inferred from signature (not verified by tests)
ThumbnailMaker maker = new ThumbnailMaker();
```

### LLM Instruction Prompt
- Use `new ThumbnailMaker()` ONLY when constructing advanced, custom image processing pipelines that cannot be satisfied by the standard fluent builder.
- Strongly prefer the fluent API (`Thumbnails.of(...)`) over manual `ThumbnailMaker` instantiation for standard resizing, cropping, and filtering tasks, as the fluent API automatically handles boilerplate `Graphics2D` manipulation and Image I/O.
- If using this low-level class, you must manually configure the rendering hints, resizers, and image filters.

### Prompt Snippet
```text
// Advanced usage for custom pipelines
ThumbnailMaker maker = new ThumbnailMaker(); 
// Note: The fluent API (Thumbnails.of(...)) is strictly preferred for standard usage.
```

### Common Failure Modes
- **Missing Default Configurations**: Manually instantiating `ThumbnailMaker` and failing to configure necessary parameters (like a `Resizer` or `ImageFilter` pipeline) that the fluent `Thumbnails.Builder` handles automatically.
- **Missing Exif Orientation**: Failing to parse and apply Exif metadata. The fluent API handles this automatically, but when using low-level makers, developers often forget to use `ExifUtils.getExifOrientation` and `ExifFilterUtils.getFilterForOrientation` to correct image rotation before processing.

### Fix Code Hint
```java
// Instead of manually wiring a ThumbnailMaker, use the strictly preferred fluent API:
BufferedImage thumbnail = Thumbnails.of(originalImage)
    .size(640, 480)
    .asBufferedImage();
```

## API Test: `ThumbnailParameter`

### Signature
```java
public ThumbnailParameter( Dimension thumbnailSize, Region sourceRegion, boolean keepAspectRatio, String outputFormat, String outputFormatType, float outputQuality, int imageType, List<ImageFilter> filters, Resizer resizer, boolean fitWithinDimensions, boolean useExifOrientation
public ThumbnailParameter( double widthScalingFactor, double heightScalingFactor, Region sourceRegion, boolean keepAspectRatio, String outputFormat, String outputFormatType, float outputQuality, int imageType, List<ImageFilter> filters, Resizer resizer, boolean fitWithinDimensions,
public ThumbnailParameter( Dimension thumbnailSize, Region sourceRegion, boolean keepAspectRatio, String outputFormat, String outputFormatType, float outputQuality, int imageType, List<ImageFilter> filters, ResizerFactory resizerFactory, boolean fitWithinDimensions, boolean useExifOrientation
public ThumbnailParameter( double widthScalingFactor, double heightScalingFactor, Region sourceRegion, boolean keepAspectRatio, String outputFormat, String outputFormatType, float outputQuality, int imageType, List<ImageFilter> filters, ResizerFactory resizerFactory, boolean fitWithinDimensions,
```
_Source: source/src/main/java/net/coobird/thumbnailator/ThumbnailParameter.java:437  (+3 more definition site/overload)_

_Source doc:_ Creates an object holding the parameters needed in order to make a thumbnail. @param thumbnailSize		The size of the thumbnail to generate. @param sourceRegion		The region of the source image to use when creating a thumbnail. A value of {@code null} indicates that the entire source image should be used to create the thumbnail. @param keepAspectRatio	Indicates whether or not the thumbnail should maintain the aspect ratio of the original image. @param outputFormat		A string indicating the compression format that should be applied on the thumbnail. A value of {@link ThumbnailParameter#ORIGINAL_FORMAT} should be provided if the same image format as the original should	be used for the thumbnail. A value of {@link ThumbnailParameter#DETERMINE_FORMAT} should be provided if the output format of the thumbnail should be the determined from the information available, such as the output file name of the thumbnail. @param outputFormatType	A string indicating the compression type that should be used when writing the thumbnail. A value of {@link ThumbnailParameter#DEFAULT_FORMAT_TYPE} should be provided if the thumbnail should be written using the default compression type of the codec specified in {@code outputFormat}. @param outputQuality		A value from {@code 0.0f} to {@code 1.0f} which indicates the quality setting to use for the compression of the thumbnail. {@code 0.0f} indicates the lowest quality, {@code 1.0f} indicates the highest quality setting for the compression. {@link ThumbnailParameter#DEFAULT_QUALITY} should be specified when the codec's default compression quality settings should be used. @param imageType 		The {@link BufferedImage} image type of the thumbnail. A value of {@link ThumbnailParameter#DEFAULT_IMAGE_TYPE} should be specified when the default image type should be used when creating the thumbnail. @param filters			The {@link ImageFilter}s to apply to the thumbnail. A value of {@code null} will be recognized as no filters are to be applied. The filters are applied after the original image has been resized. @param resizer			The {@link Resizer} to use when performing the resizing operation to create a thumbnail. @param fitWithinDimensions	Whether or not to fit the thumbnail within the specified dimensions. <p> If {@code true} is specified, then the thumbnail will be sized to fit within the specified dimensions, if the thumbnail is going to exceed those dimensions. @param useExifOrientation	Whether or not to use the Exif metadata to determine the orientation of the thumbnail. <p> If {@code true} is specified, then the Exif metadata will be used to determine the orientation of the thumbnail. @throws IllegalArgumentException 	If size is {@code null} or if the dimensions are negative, or if the {@link Resizer} is null. @since	0.4.3

### Goal
Creates an immutable configuration object holding all the parameters, filters, and rendering hints needed to execute a deterministic thumbnail generation task.

### Parameters
- `thumbnailSize` (`Dimension`): The target width and height of the thumbnail to generate. Cannot be null or negative.
- `sourceRegion` (`Region`): The specific region of the source image to crop and use. A value of `null` indicates the entire source image should be used.
- `keepAspectRatio` (`boolean`): `true` to maintain the aspect ratio of the original image during resizing; `false` to stretch or squash the image to the exact dimensions.
- `outputFormat` (`String`): The compression format to apply (e.g., "jpg", "png"). Use `ThumbnailParameter.ORIGINAL_FORMAT` to retain the source format, or `ThumbnailParameter.DETERMINE_FORMAT` ("\0") to infer it from the output destination (like a filename).
- `outputFormatType` (`String`): The compression type for writing. Use `ThumbnailParameter.DEFAULT_FORMAT_TYPE` to use the codec's default.
- `outputQuality` (`float`): The compression quality from `0.0f` (lowest) to `1.0f` (highest). Use `ThumbnailParameter.DEFAULT_QUALITY` (NaN) to use the codec's default settings.
- `imageType` (`int`): The `BufferedImage` type (e.g., `BufferedImage.TYPE_INT_ARGB`). Use `ThumbnailParameter.DEFAULT_IMAGE_TYPE` (2) or `ThumbnailParameter.ORIGINAL_IMAGE_TYPE` (-1) for defaults.
- `filters` (`List<ImageFilter>`): A list of transformations (e.g., Watermark, Caption) to apply *after* the image has been resized. `null` means no filters are applied.
- `resizer` (`Resizer`): The scaling algorithm implementation to use (e.g., `Resizers.PROGRESSIVE`, `BicubicResizer`). Cannot be null.
- `fitWithinDimensions` (`boolean`): `true` to ensure the final thumbnail is sized to fit strictly within the specified `thumbnailSize` dimensions if it would otherwise exceed them.
- `useExifOrientatio` (`boolean`): `true` to parse Exif metadata and automatically apply the correct rotation filter to fix the image's orientation before processing.

### Input
Callers must provide valid, non-negative dimensions (or scaling factors for the overloads) and a non-null `Resizer` or `ResizerFactory`. This constructor is typically used when manually instantiating a `ThumbnailTask` (such as `FileThumbnailTask` or `StreamThumbnailTask`) rather than using the standard fluent builder API.

### Output
Returns a new `ThumbnailParameter` instance encapsulating the complete configuration for an image processing pipeline.

### Valid Call Patterns
```java
ThumbnailParameter param = new ThumbnailParameter(
        new Dimension(50, 50),
        null, // sourceRegion (null = entire image)
        true, // keepAspectRatio
        "jpg", // outputFormat
        ThumbnailParameter.DEFAULT_FORMAT_TYPE,
        ThumbnailParameter.DEFAULT_QUALITY,
        BufferedImage.TYPE_INT_ARGB,
        null, // filters (null = none)
        Resizers.PROGRESSIVE,
        true, // fitWithinDimensions
        true  // useExifOrientation
);

File inputFile = new File("input.jpg");
File outputFile = new File("output.png");
FileThumbnailTask task = new FileThumbnailTask(param, inputFile, outputFile);
task.read();
```

### LLM Instruction Prompt
- Prefer the fluent `Thumbnails.of(...).size(...)...` API for standard use cases. Only construct a `ThumbnailParameter` directly when you need to manually instantiate a `ThumbnailTask` (e.g., `FileThumbnailTask`) for advanced, low-level pipeline control.
- When constructing `ThumbnailParameter`, use the provided constants for defaults: `ThumbnailParameter.DEFAULT_QUALITY`, `ThumbnailParameter.DEFAULT_FORMAT_TYPE`, and `ThumbnailParameter.DEFAULT_IMAGE_TYPE`.
- Pass `null` for `sourceRegion` to use the whole image, and `null` for `filters` if no post-resize transformations are needed.

### Prompt Snippet
```text
When manually creating a ThumbnailTask in Thumbnailator, instantiate a ThumbnailParameter to hold the configuration. Use constants like ThumbnailParameter.DEFAULT_QUALITY and ThumbnailParameter.DEFAULT_FORMAT_TYPE for defaults. Pass null for sourceRegion to use the entire image, and null for filters if none are needed. Ensure the Dimension is non-null and non-negative, and provide a valid Resizer (e.g., Resizers.PROGRESSIVE).
```

### Common Failure Modes
- **`IllegalArgumentException`**: Thrown immediately during instantiation if `thumbnailSize` is `null`, if the dimensions are negative, or if the `resizer` argument is `null`.
- **`UnsupportedFormatException`**: Thrown later during task execution (not at instantiation) if the specified `outputFormat` is not supported by the host JVM's underlying Image I/O implementation.

### Fix Code Hint
```java
// BAD: Passing null for Dimension or Resizer will throw IllegalArgumentException
ThumbnailParameter param = new ThumbnailParameter(null, null, true, "jpg", null, 0.8f, 2, null, null, true, true);

// GOOD: Provide a valid Dimension, a valid Resizer, and use constants for defaults
ThumbnailParameter param = new ThumbnailParameter(
    new Dimension(100, 100), 
    null, 
    true, 
    "jpg", 
    ThumbnailParameter.DEFAULT_FORMAT_TYPE, 
    ThumbnailParameter.DEFAULT_QUALITY, 
    ThumbnailParameter.DEFAULT_IMAGE_TYPE, 
    null, 
    Resizers.PROGRESSIVE, 
    true, 
    true
);
```

## API Test: `ThumbnailParameterBuilder`

### Signature
```java
public ThumbnailParameterBuilder()
```
_Source: source/src/main/java/net/coobird/thumbnailator/builders/ThumbnailParameterBuilder.java:105_

_Source doc:_ Creates an instance of a {@link ThumbnailParameterBuilder}.

### Goal
Creates a new instance of `ThumbnailParameterBuilder` to fluently construct a `ThumbnailParameter` object, which encapsulates configuration settings for advanced, manual `ThumbnailTask` pipelines.

### Parameters
_None._

### Input
No arguments are required to instantiate the builder. After instantiation, the caller must provide configuration values (such as dimensions via `.size(int, int)` or scaling factors via `.scale(double)`) using the builder's fluent methods before finalizing the object.

### Output
Returns `unspecified` (Constructor) — A new, unconfigured instance of `ThumbnailParameterBuilder` that exposes fluent methods for setting image processing parameters and a `.build()` method to generate the final `ThumbnailParameter`.

### Valid Call Patterns
```java
// Example 1: Building parameters with absolute dimensions and a custom resizer factory
ResizerFactory resizerFactory = DefaultResizerFactory.getInstance();
ThumbnailParameter paramSize = new ThumbnailParameterBuilder()
        .size(100, 100)
        .resizerFactory(resizerFactory)
        .build();

// Example 2: Building parameters with a relative scale factor
ThumbnailParameter paramScale = new ThumbnailParameterBuilder()
        .scale(0.5)
        .resizerFactory(resizerFactory)
        .build();
```

### LLM Instruction Prompt
- Use `new ThumbnailParameterBuilder()` only for advanced workflows where you need to manually construct a `ThumbnailTask` (e.g., `SourceSinkThumbnailTask`). For standard image resizing, strictly prefer the `Thumbnails.of(...)` fluent API instead.
- Always chain configuration methods (like `.size()` or `.scale()`) and terminate the chain with `.build()` to extract the `ThumbnailParameter`.
- Ensure that either size or scale is provided to the builder; failing to define the output dimensions will result in an invalid parameter state for the resizing task.

### Prompt Snippet
```text
When manually constructing a `ThumbnailTask`, instantiate `new ThumbnailParameterBuilder()`, configure the required dimensions using `.size(w, h)` or `.scale(factor)`, and call `.build()` to generate the `ThumbnailParameter`.
```

### Common Failure Modes
- **Missing Terminal Operation**: Forgetting to call `.build()` at the end of the chain, resulting in a `ThumbnailParameterBuilder` being passed where a `ThumbnailParameter` is expected.
- **Missing Dimension Configuration**: Calling `.build()` without specifying either `.size()` or `.scale()`, which creates an invalid parameter object that will cause the underlying `ThumbnailTask` to fail during execution.
- **Overcomplicating Standard Workflows**: Using `ThumbnailParameterBuilder` and `ThumbnailTask` for basic file-to-file or stream-to-stream resizing instead of the much simpler and strictly preferred `Thumbnails.of(...).size(...).toFile(...)` API.

### Fix Code Hint
```java
// WRONG: Forgetting to call .build() or using it for basic workflows
ThumbnailParameter param = new ThumbnailParameterBuilder().size(100, 100); // Type mismatch

// RIGHT: Terminate with .build() for advanced Task-based workflows
ThumbnailParameter param = new ThumbnailParameterBuilder()
        .size(100, 100)
        .build();
Thumbnailator.createThumbnail(new SourceSinkThumbnailTask<>(param, source, sink));

// BETTER (for standard workflows): Use the Thumbnails fluent API directly
Thumbnails.of(inputFile).size(100, 100).toFile(outputFile);
```

## API Test: `Transparency`

### Signature
```java
public Transparency(float alpha)
public Transparency(double alpha)
```
_Source: source/src/main/java/net/coobird/thumbnailator/filters/Transparency.java:58  (+1 more definition site/overload)_

_Source doc:_ Instantiates a {@link Transparency} filter with the specified opacity. @param alpha		The opacity of the resulting image. The value should be between {@code 0.0f} (transparent) to {@code 1.0f} (opaque), inclusive. @throws IllegalArgumentException	If the specified opacity is outside of the range specified above.

### Goal
Instantiates an `ImageFilter` that applies a uniform opacity (alpha transparency) level to an image.

### Parameters
- `alpha` (`float`): The opacity of the resulting image. The value must be between `0.0f` (completely transparent) and `1.0f` (completely opaque), inclusive. An overloaded constructor also accepts a `double`.

### Input
A `float` or `double` representing the desired opacity level. The caller must ensure the value is strictly within the `[0.0, 1.0]` bounds. When applied in a pipeline, the underlying image must be processed into a format that supports an alpha channel (e.g., PNG) if the transparency is to be preserved in the final output file.

### Output
Returns an instantiated `Transparency` object (which implements `ImageFilter`). This filter safely generates a new `BufferedImage` with the applied opacity when executed, leaving the original input image unaltered.

### Valid Call Patterns
```java
// 1. Direct instantiation and application (from test suite)
BufferedImage originalImage = new BufferedImage(200, 200, BufferedImage.TYPE_INT_ARGB);
ImageFilter filter = new Transparency(0.5f); // or 0.5 for double
BufferedImage resultImage = filter.apply(originalImage);

// 2. Integration into a fluent Thumbnailator pipeline (derived from context)
Thumbnails.of(new File("input.jpg"))
    .size(640, 480)
    .addFilter(new Transparency(0.75f))
    .outputFormat("png") // Required to preserve transparency in the output file
    .toFile(new File("output.png"));
```

### LLM Instruction Prompt
- To adjust the opacity of an image in Thumbnailator, instantiate `new Transparency(alpha)` where `alpha` is a float or double between `0.0` and `1.0`.
- Pass this filter to the pipeline using `Thumbnails.Builder.addFilter(ImageFilter)`.
- Always ensure the output format is set to one that supports transparency (like PNG) using `.outputFormat("png")`, otherwise the underlying Java Image I/O will discard the alpha channel when writing to formats like JPEG.

### Prompt Snippet
```text
Apply a 50% transparency filter to the image pipeline:
builder.addFilter(new Transparency(0.5f)).outputFormat("png");
```

### Common Failure Modes
- **`IllegalArgumentException`**: Thrown immediately during instantiation if the `alpha` value is less than `0.0` or greater than `1.0`.
- **Loss of Transparency on Save**: If the pipeline routes the processed image to a file format that does not support alpha channels (e.g., standard JPEG), the transparency will be lost, often resulting in a solid black background.

### Fix Code Hint
```java
// Clamp the alpha value to prevent IllegalArgumentException
float safeAlpha = Math.max(0.0f, Math.min(1.0f, requestedAlpha));

Thumbnails.of(inputFile)
    .size(800, 600)
    .addFilter(new Transparency(safeAlpha))
    .outputFormat("png") // Fix: Ensure the output format supports the alpha channel
    .toFile(outputFile);
```

## API Test: `URLImageSource`

### Signature
```java
public URLImageSource(URL url)
public URLImageSource(String url)
public URLImageSource(URL url, Proxy proxy)
public URLImageSource(String url, Proxy proxy)
```
_Source: source/src/main/java/net/coobird/thumbnailator/tasks/io/URLImageSource.java:99  (+3 more definition site/overload)_

_Source doc:_ Instantiates an {@link URLImageSource} with the URL from which the source image should be retrieved from, along with the proxy to use to connect to the aforementioned URL. @param url		URL to the source image. @param proxy		Proxy to use to connect to the URL. @throws NullPointerException		If the URL and or the proxy is null

### Goal
Instantiates an `ImageSource` that retrieves a source image from a specified URL, optionally routing the connection through a provided proxy server.

### Parameters
- `url` (`URL`): The URL pointing to the source image to be retrieved. Overloads also accept a `String` representation of the URL.
- `proxy` (`Proxy`): The proxy server to use when connecting to the specified URL (e.g., `Proxy.NO_PROXY`).

### Input
A valid `java.net.URL` object (or a well-formed URL `String`) pointing to an image format supported by the host JVM's standard Image I/O capabilities. If using the proxy overload, a valid, non-null `java.net.Proxy` instance must be provided. In headless test environments where network access is prohibited, the URL must point to a local resource (e.g., a `file://` URL or a classpath resource).

### Output
Returns `unspecified` — An instantiated `URLImageSource` object (an implementation of `ImageSource`) that can be used to read the target URL into a `BufferedImage` via its `read()` method, or passed into a custom `ThumbnailTask`.

### Valid Call Patterns
```java
// Using a URL object and a Proxy (from project test suite)
Proxy proxy = Proxy.NO_PROXY;
URLImageSource source = new URLImageSource(
        TestUtils.getResource("Thumbnailator/grid.png"), 
        proxy
);

// Reading the image into memory
BufferedImage img = source.read();
```

### LLM Instruction Prompt
When constructing a `URLImageSource`, ensure neither the `url` nor the `proxy` arguments are null to avoid a `NullPointerException`. Use this class when you need to explicitly define proxy settings for URL-based image retrieval, as the standard `Thumbnails.fromURLs()` fluent API does not expose proxy configuration directly. In restricted test environments, ensure the URL points to a local classpath resource rather than an external web address.

### Prompt Snippet
```text
URLImageSource source = new URLImageSource(url, Proxy.NO_PROXY);
BufferedImage img = source.read();
```

### Common Failure Modes
- **`NullPointerException`**: Thrown immediately during instantiation if either the `url` or the `proxy` argument is `null`.
- **Network/Connectivity Failures**: If the URL points to an external resource and the environment prohibits network access (or the proxy is misconfigured), the subsequent `read()` operation will fail.
- **`UnsupportedFormatException`**: If the URL successfully resolves but points to an image format that the underlying Java Image I/O does not support, reading the image will fail.

### Fix Code Hint
```java
// Ensure URL and Proxy are non-null before instantiation
if (url == null) {
    throw new IllegalArgumentException("URL cannot be null.");
}
Proxy proxy = (userProxy != null) ? userProxy : Proxy.NO_PROXY;
URLImageSource source = new URLImageSource(url, proxy);
```

## API Test: `UnsupportedFormatException`

### Signature
```java
public UnsupportedFormatException(String formatName)
public UnsupportedFormatException(String formatName, String s)
```
_Source: source/src/main/java/net/coobird/thumbnailator/tasks/UnsupportedFormatException.java:70  (+1 more definition site/overload)_

_Source doc:_ Instantiates a {@link UnsupportedFormatException} with the unsupported format and a detailed message. @param formatName	Format name. @param s				A message detailing the exception.

### Goal
Instantiates an exception indicating that a requested image format is not supported by the host JVM's Java Image I/O capabilities.

### Parameters
- `formatName` (`String`): The name of the image format that could not be processed (e.g., "tiff", "webp").
- `s` (`String`): A detailed message explaining the exception context (e.g., "No suitable ImageWriter found").

### Input
A string representing the unsupported format name and a string containing the detailed error message. This is typically invoked internally when `Thumbnails.Builder.outputFormat(String)` specifies a format lacking a registered Java Image I/O reader or writer in the current environment.

### Output
Returns `unspecified` — yields a new `UnsupportedFormatException` instance to be thrown by the pipeline.

### Valid Call Patterns
```java
// Inferred from signature (not verified)
UnsupportedFormatException exception = new UnsupportedFormatException("webp", "No suitable ImageWriter found for webp.");
throw exception;
```

### LLM Instruction Prompt
- When configuring image pipelines with `outputFormat(String)`, anticipate `UnsupportedFormatException` if the target format is not supported by the standard Java 8 Image I/O (e.g., formats other than JPEG, PNG, GIF, BMP). Do not assume support for modern formats like WebP or HEIC unless external Image I/O plugins are explicitly guaranteed by the environment.

### Prompt Snippet
```text
Catch UnsupportedFormatException when calling terminal sink methods (like `toFile()` or `toOutputStream()`) on a Thumbnails.Builder if a non-standard `outputFormat` was requested.
```

### Common Failure Modes
- **Missing Image I/O Plugin**: A user specifies `.outputFormat("tiff")` or `.outputFormat("webp")` on a standard Java 8 JVM without external Image I/O plugins on the classpath. Thumbnailator will throw this exception during the terminal sink operation because it relies entirely on the host JVM's standard Image I/O capabilities.

### Fix Code Hint
```java
try {
    Thumbnails.of(new File("input.jpg"))
        .size(640, 480)
        .outputFormat("webp") // May throw UnsupportedFormatException on standard Java 8
        .toFile(new File("output.webp"));
} catch (UnsupportedFormatException e) {
    // Fallback to a universally supported format
    Thumbnails.of(new File("input.jpg"))
        .size(640, 480)
        .outputFormat("jpg")
        .toFile(new File("output.jpg"));
}
```

## API Test: `Watermark`

### Signature
```java
public Watermark(Position position, BufferedImage watermarkImg, float opacity, int insets)
public Watermark(Position position, BufferedImage watermarkImg, float opacity)
```
_Source: source/src/main/java/net/coobird/thumbnailator/filters/Watermark.java:76  (+1 more definition site/overload)_

_Source doc:_ Instantiates a filter which applies a watermark to an image. @param position			The position of the watermark. @param watermarkImg		The watermark image. @param opacity			The opacity of the watermark. <p> The value should be between {@code 0.0f} and {@code 1.0f}, where {@code 0.0f} is completely transparent, and {@code 1.0f} is completely opaque. @param insets			Inset size around the watermark. Cannot be negative.

### Goal
Instantiates an image filter that overlays a watermark image onto a base image at a specified position, opacity, and margin.

### Parameters
- `position` (`Position`): The placement of the watermark on the base image (typically provided by the `net.coobird.thumbnailator.geometry.Positions` enum, e.g., `Positions.BOTTOM_RIGHT`).
- `watermarkImg` (`BufferedImage`): The in-memory image to be used as the watermark overlay.
- `opacity` (`float`): The transparency level of the watermark. Must be between `0.0f` (completely transparent) and `1.0f` (completely opaque).
- `insets` (`int`): The margin size in pixels around the watermark. Cannot be negative. (Omitted in the 3-argument overload, which defaults to 0).

### Input
The caller must provide a valid `Position` instance, a fully loaded `BufferedImage` for the watermark, and a valid `float` for opacity. If using the 4-argument constructor, the `insets` value must be `>= 0`. The watermark image must be loaded into memory before constructing this filter.

### Output
Returns an instantiated `Watermark` object (which implements the `ImageFilter` interface) that can be passed to the Thumbnailator fluent builder or applied directly to a `BufferedImage`.

### Valid Call Patterns
```java
// Pattern 1: 3-argument constructor applied via the fluent builder
Watermark watermark = new Watermark(Positions.BOTTOM_RIGHT, WATERMARK_IMAGE, 0.5f);
BufferedImage image = Thumbnails.of(ORIGINAL_IMAGE)
        .scale(1.0)
        .watermark(watermark)
        .asBufferedImage();

// Pattern 2: 4-argument constructor used as a standalone ImageFilter
ImageFilter filter = new Watermark(
        Positions.CENTER,
        DEFAULT_WATERMARK,
        0.8f,
        10 // 10px inset
);
filter.apply(originalImage);
```

### LLM Instruction Prompt
- When applying a watermark in Thumbnailator, instantiate a `Watermark` object and pass it to `Thumbnails.Builder.watermark(Watermark)` or `Thumbnails.Builder.addFilter(ImageFilter)`.
- Ensure the `opacity` parameter is strictly a `float` between `0.0f` and `1.0f`.
- Ensure the `insets` parameter (if provided) is `0` or greater.
- Use the `net.coobird.thumbnailator.geometry.Positions` enum (e.g., `Positions.BOTTOM_RIGHT`) for the `Position` argument.

### Prompt Snippet
```text
Create a Watermark filter using `new Watermark(Positions.BOTTOM_RIGHT, watermarkImage, 0.5f, 5)` and apply it to the Thumbnails builder using `.watermark(watermark)`. Ensure opacity is between 0.0f and 1.0f and insets are non-negative.
```

### Common Failure Modes
- **IllegalArgumentException (Opacity)**: Thrown if the `opacity` argument is less than `0.0f` or greater than `1.0f`.
- **IllegalArgumentException (Insets)**: Thrown if the `insets` argument is negative.
- **NullPointerException**: Thrown if the `position` or `watermarkImg` is `null` when the filter is applied.
- **Memory Exhaustion**: Loading excessively large watermark images into a `BufferedImage` can cause an `OutOfMemoryError` in headless environments.

### Fix Code Hint
```java
// Incorrect: Invalid opacity and negative insets
// Watermark badWatermark = new Watermark(Positions.CENTER, myImage, 1.5f, -5);

// Correct: Opacity clamped to 1.0f max, insets >= 0
Watermark goodWatermark = new Watermark(Positions.CENTER, myImage, 1.0f, 5);
Thumbnails.of(inputFile)
    .size(800, 600)
    .watermark(goodWatermark)
    .toFile(outputFile);
```

## API Test: `add`

### Signature
```java
public void add(ImageFilter filter)
```
_Source: source/src/main/java/net/coobird/thumbnailator/filters/Pipeline.java:99_

_Source doc:_ Adds an {@code ImageFilter} to the pipeline. @param filter		An {@code ImageFilter}.

### Goal
Appends an `ImageFilter` to a custom image processing `Pipeline`, allowing multiple transformations to be chained and executed sequentially.

### Parameters
- `filter` (`ImageFilter`): An implementation of `ImageFilter` (such as `Rotation`, `Watermark`, `Canvas`, or `Flip`) to be added to the end of the pipeline.

### Input
An instantiated `Pipeline` object. The caller must provide a valid `ImageFilter` instance to be sequenced. This is typically used in advanced workflows where manual `BufferedImage` manipulation is required outside of the standard `Thumbnails.Builder` fluent API.

### Output
Returns `void` — the `Pipeline` is mutated in-place, storing the provided filter in its internal list for later execution.

### Valid Call Patterns
```java
// Given valid ImageFilter instances (e.g., filter1, filter2)
Pipeline pipeline = new Pipeline();
pipeline.add(filter1);
pipeline.add(filter2);

// The pipeline must then be applied to a BufferedImage
// pipeline.apply(img);
```

### LLM Instruction Prompt
- When constructing custom image processing pipelines outside the standard `Thumbnails.Builder` fluent API, instantiate a `Pipeline` and use `pipeline.add(ImageFilter)` to sequence transformations. 
- Always ensure the populated `Pipeline` is subsequently executed by calling `apply(BufferedImage)`. 
- Do not confuse `Pipeline.add(ImageFilter)` with the fluent builder's `Thumbnails.Builder.addFilter(ImageFilter)`. Use `Pipeline` only for advanced, manual `BufferedImage` workflows.

### Prompt Snippet
```text
To chain custom image filters manually outside the fluent builder, use `Pipeline pipeline = new Pipeline(); pipeline.add(filter);` and execute it with `pipeline.apply(bufferedImage);`.
```

### Common Failure Modes
- **Missing Execution**: Adding filters to a `Pipeline` but failing to call `apply(BufferedImage)` on the pipeline afterward, resulting in no transformations being executed.
- **API Confusion**: Attempting to call `add()` directly on a `Thumbnails.Builder` instance. The builder uses `addFilter(ImageFilter)`, whereas `add(ImageFilter)` belongs strictly to the `Pipeline` object.

### Fix Code Hint
```java
// Correct usage of Pipeline.add requires applying it to an image
BufferedImage img = new BufferedImage(200, 200, BufferedImage.TYPE_INT_ARGB);
Pipeline pipeline = new Pipeline();

pipeline.add(filter1);
pipeline.add(filter2);

// The filters are executed sequentially on the image
pipeline.apply(img);
```

## API Test: `addAll`

### Signature
```java
public void addAll(List<ImageFilter> filters)
```
_Source: source/src/main/java/net/coobird/thumbnailator/filters/Pipeline.java:125_

_Source doc:_ Adds a {@code List} of {@code ImageFilter}s to the pipeline. @param filters			A list of filters to add to the pipeline.

### Goal
Appends a list of `ImageFilter` transformations to an image processing pipeline for sequential execution.

### Parameters
- `filters` (`List<ImageFilter>`): A list of filters (such as `Rotation`, `Watermark`, `Caption`, or `Canvas`) to add to the pipeline.

### Input
An instantiated `Pipeline` object and a `List` containing valid `ImageFilter` implementations. The filters will be applied to the `BufferedImage` in the exact order they appear in the list.

### Output
Returns `void` — mutates the underlying `Pipeline` instance in-place by appending the provided filters to its internal execution sequence.

### Valid Call Patterns
```java
// given
BufferedImage img = new BufferedImage(200, 200, BufferedImage.TYPE_INT_ARGB);
ImageFilter filter1 = mock(ImageFilter.class);
ImageFilter filter2 = mock(ImageFilter.class);

Pipeline pipeline = new Pipeline();
pipeline.addAll(Arrays.asList(filter1, filter2));

// when
pipeline.apply(img);
```

### LLM Instruction Prompt
- When constructing a custom `Pipeline` for advanced image processing tasks, use `addAll(List<ImageFilter>)` to append multiple transformations at once. 
- Ensure the argument is a `List` (e.g., via `Arrays.asList()`). 
- Note: For standard workflows, prefer the fluent `Thumbnails.Builder.addFilter(ImageFilter)` instead of manually constructing a `Pipeline`.

### Prompt Snippet
```text
To add multiple filters to a custom `Pipeline`, call `pipeline.addAll(Arrays.asList(filter1, filter2))`. Filters are applied to the `BufferedImage` in the order they are added to the list.
```

### Common Failure Modes
- **Type Mismatch**: Attempting to pass a single `ImageFilter` directly to `addAll` instead of wrapping it in a `List`.
- **API Confusion**: Attempting to call `addAll` on the standard `Thumbnails.Builder` fluent interface. `addAll` belongs to the advanced `Pipeline` class; the builder uses `addFilter(ImageFilter)`.

### Fix Code Hint
```java
// Incorrect: Passing a single filter directly to addAll
// pipeline.addAll(myFilter);

// Correct: Wrap the filter(s) in a List
Pipeline pipeline = new Pipeline();
pipeline.addAll(Arrays.asList(myFilter));
```

## API Test: `addFilter`

### Signature
```java
public Builder<T> addFilter(ImageFilter filter)
```
_Source: source/src/main/java/net/coobird/thumbnailator/Thumbnails.java:1993_

_Source doc:_ Adds a {@link ImageFilter} to apply to the thumbnail. <p> This method can be called multiple times to apply multiple filters. <p> If multiple filters are to be applied, the filters will be applied in the order that this method is called. <p> Calling this method to set this parameter is optional. @param filter		An image filter to apply to the thumbnail. @return				Reference to this object.

### Goal
Appends an `ImageFilter` to the image processing pipeline to apply transformations such as watermarks, captions, or orientation corrections.

### Parameters
- `filter` (`ImageFilter`): An image filter implementation (e.g., `Canvas`, `Caption`, `Colorize`, `Flip`, `Rotation`, `SwapDimensions`, `Transparency`, `Watermark`, or an Exif orientation filter) to apply to the thumbnail.

### Input
The method must be called on an active `Thumbnails.Builder` instance (e.g., created via `Thumbnails.of(...)`). The caller must provide a valid, instantiated `ImageFilter`. If applying multiple filters, the caller must be aware that they are applied sequentially in the exact order `addFilter` is called.

### Output
Returns `Builder<T>` — A reference to the current `Thumbnails.Builder` object, allowing for fluent method chaining.

### Valid Call Patterns
```java
// Correcting Exif orientation when the source is a BufferedImage (which strips metadata)
BufferedImage result =
        Thumbnails.of(ImageIO.read(is))
                .addFilter(ExifFilterUtils.getFilterForOrientation(Orientation.typeOf(orientation)))
                .size(width, height)
                .asBufferedImage();
```

### LLM Instruction Prompt
- Use `addFilter` to inject custom or built-in `ImageFilter` implementations into the Thumbnailator pipeline.
- You may call `addFilter` multiple times on the same builder. Filters are strictly applied in the order they are added.
- When processing a `BufferedImage` source, Exif metadata is lost. To ensure correct orientation, you must manually extract the orientation (e.g., via `ExifUtils.getExifOrientation`) and apply the correction using `addFilter(ExifFilterUtils.getFilterForOrientation(orientation))`.

### Prompt Snippet
```text
To apply transformations like watermarks or manual Exif orientation corrections in Thumbnailator, use `Thumbnails.Builder.addFilter(ImageFilter)`. You can chain multiple `addFilter` calls; they execute in the exact order added. When reading from a `BufferedImage`, Exif data is lost, so you must manually apply the orientation filter using `addFilter(ExifFilterUtils.getFilterForOrientation(orientation))`.
```

### Common Failure Modes
- **Order of Operations Errors**: Because filters are applied in the order `addFilter` is called, adding a watermark filter before a crop or resize operation may yield a distorted or cropped watermark.
- **Missing Exif Correction on BufferedImage Sources**: Passing a `BufferedImage` directly to `Thumbnails.of()` bypasses Thumbnailator's automatic Exif orientation correction (since the metadata is not attached to the `BufferedImage`). Failing to manually add the Exif filter results in incorrectly rotated outputs.

### Fix Code Hint
```java
// Incorrect: Exif orientation is lost when reading directly into a BufferedImage without a filter
BufferedImage badResult = Thumbnails.of(ImageIO.read(sourceFile))
        .scale(0.5)
        .asBufferedImage();

// Correct: Manually apply the Exif orientation filter to the pipeline
BufferedImage goodResult = Thumbnails.of(ImageIO.read(sourceFile))
        .addFilter(ExifFilterUtils.getFilterForOrientation(Orientation.typeOf(orientation)))
        .scale(0.5)
        .asBufferedImage();
```

## API Test: `addFilters`

### Signature
```java
public Builder<T> addFilters(List<ImageFilter> filters)
```
_Source: source/src/main/java/net/coobird/thumbnailator/Thumbnails.java:2016_

_Source doc:_ Adds multiple {@link ImageFilter}s to apply to the thumbnail. <p> This method can be called multiple times to apply multiple filters. <p> If multiple filters are to be applied, the filters will be applied in the order that this method is called. <p> Calling this method to set this parameter is optional. @param filters		A list of filters to apply to the thumbnail. @return				Reference to this object.

### Goal
Appends a list of multiple `ImageFilter` transformations to the image processing pipeline, which will be applied sequentially to the thumbnail.

### Parameters
- `filters` (`List<ImageFilter>`): A list of filters (such as `Canvas`, `Caption`, `Colorize`, `Flip`, `Rotation`, `SwapDimensions`, `Transparency`, or `Watermark`) to apply to the thumbnail in the exact order they appear in the list.

### Input
The caller must have an active `Thumbnails.Builder` instance (e.g., created via `Thumbnails.of(...)`) and provide a valid, non-null `List` of `ImageFilter` implementations. 

### Output
Returns `Builder<T>` — A reference to the current `Thumbnails.Builder` instance, allowing for continued fluent method chaining.

### Valid Call Patterns
```java
// Inferred from the signature and project context (not verified by existing tests)
List<ImageFilter> myFilters = getMyCustomFilters(); // Provides a List<ImageFilter>

Thumbnails.of(new File("original.jpg"))
    .size(640, 480)
    .addFilters(myFilters)
    .toFile(new File("thumbnail.jpg"));
```

### LLM Instruction Prompt
- When building a Thumbnailator pipeline, use `addFilters(List<ImageFilter>)` to apply a batch of transformations at once. 
- Remember that filters are applied in the exact order they appear in the list. 
- This method can be called multiple times on the same builder; subsequent calls will append their filters to the end of the pipeline.

### Prompt Snippet
```text
To apply a collection of transformations sequentially, pass a `List<ImageFilter>` to `addFilters(filters)` on the `Thumbnails.Builder`. Filters execute in list order.
```

### Common Failure Modes
- **Null Pointer Exceptions**: Passing a `null` list instead of an empty or populated `List<ImageFilter>` will cause a failure when the builder attempts to iterate over the filters.
- **Order of Operations Errors**: Applying filters in an unintended sequence (e.g., applying a `Watermark` before a `Rotation` or `Crop` operation) can yield incorrect visual results or unexpected geometry.

### Fix Code Hint
```java
// Ensure the list is non-null and ordered correctly before passing to the builder
if (myFilters != null && !myFilters.isEmpty()) {
    builder.addFilters(myFilters);
}
```

## API Test: `addFirst`

### Signature
```java
public void addFirst(ImageFilter filter)
```
_Source: source/src/main/java/net/coobird/thumbnailator/filters/Pipeline.java:112_

_Source doc:_ Adds an {@code ImageFilter} to the beginning of the pipeline. @param filter		An {@code ImageFilter}.

### Goal
Adds an `ImageFilter` to the very beginning of an image processing `Pipeline`, ensuring it executes before any previously added filters.

### Parameters
- `filter` (`ImageFilter`): The image transformation filter (such as `Canvas`, `Caption`, `Colorize`, `Flip`, `Rotation`, `Watermark`, or a custom implementation) to prepend to the pipeline.

### Input
A valid, instantiated `Pipeline` object and an initialized `ImageFilter` implementation. If the filter is intended to correct Exif orientation, the Exif metadata must be parsed first (e.g., via `ExifUtils.getExifOrientation`) to obtain the correct filter from `ExifFilterUtils.getFilterForOrientation(Orientation)`.

### Output
Returns `void` — modifies the internal state of the `Pipeline` by inserting the specified filter at the head of the execution order.

### Valid Call Patterns
```java
// given
BufferedImage img = new BufferedImage(200, 200, BufferedImage.TYPE_INT_ARGB);
final List<Integer> order = new ArrayList<Integer>();

ImageFilter one = new ImageFilter() {
    public BufferedImage apply(BufferedImage img) {
        order.add(1);
        return img;
    }
};

ImageFilter two = new ImageFilter() {
    public BufferedImage apply(BufferedImage img) {
        order.add(2);
        return img;
    }
};

Pipeline pipeline = new Pipeline();
pipeline.add(one);
// Prepend 'two' so it executes before 'one'
pipeline.addFirst(two);

// when
pipeline.apply(img);
// order is now [2, 1]
```

### LLM Instruction Prompt
- When constructing a custom `Pipeline` of `ImageFilter` objects, use `pipeline.addFirst(filter)` to insert a filter at the beginning of the execution chain. This is particularly required for preconditions like Exif orientation correction, which must occur before spatial filters like cropping or watermarking are applied.

### Prompt Snippet
```text
To ensure a specific `ImageFilter` executes before all other filters currently in a `Pipeline`, call `pipeline.addFirst(filter)`.
```

### Common Failure Modes
- **Incorrect Filter Ordering for Exif Data**: Applying spatial filters (like cropping or watermarking) before correcting the image's Exif orientation. To ensure images are rotated correctly before processing, the Exif orientation filter must be prepended to the pipeline.

### Fix Code Hint
```java
Pipeline pipeline = new Pipeline();
pipeline.add(new Watermark(...)); // Spatial filter added first

// Fix: Prepend the orientation correction so it happens BEFORE the watermark
ImageFilter orientationFilter = ExifFilterUtils.getFilterForOrientation(orientation);
pipeline.addFirst(orientationFilter); 
```

## API Test: `allowOverwrite`

### Signature
```java
public Builder<T> allowOverwrite(boolean allowOverwrite)
```
_Source: source/src/main/java/net/coobird/thumbnailator/Thumbnails.java:1265_

_Source doc:_ Specifies whether or not to overwrite files which already exist if they have been specified as destination files. <p> This method will change the output behavior of the following methods: <ul> <li>{@link #toFile(File)}</li> <li>{@link #toFile(String)}</li> <li>{@link #toFiles(Iterable)}</li> <li>{@link #toFiles(Rename)}</li> <li>{@link #asFiles(Iterable)}</li> <li>{@link #asFiles(Rename)}</li> </ul> The behavior of methods which are not listed above will not be affected by calling this method. <p> Calling this method multiple times will result in an {@link IllegalStateException} to be thrown. @param allowOverwrite	If {@code true} then existing files will be overwritten if specified as a destination. If {@code false}, then the existing files will not be altered. For specific behavior, please refer to the specific output methods listed above. @return					Reference to this object. @since 	0.3.7

### Goal
Specifies whether the thumbnail generation pipeline should overwrite existing destination files when writing outputs to the filesystem.

### Parameters
- `allowOverwrite` (`boolean`): If `true`, existing files at the destination path will be overwritten. If `false`, existing files will not be altered.

### Input
A configured `Thumbnails.Builder` instance that is preparing to terminate with a file-based output method. The caller must ensure this method is invoked at most once per builder pipeline.

### Output
Returns `Builder<T>` — A reference to the current builder object to allow fluent method chaining.

### Valid Call Patterns
```java
// Example 1: Overwriting files using toFiles with an Iterable of destination files
Thumbnails.of(originalFile)
        .size(50, 50)
        .allowOverwrite(true)
        .toFiles(Collections.singletonList(outputFile));

// Example 2: Preventing overwrite and returning the resulting files as a List
List<File> outputFiles = Thumbnails.of(originalFile)
        .size(50, 50)
        .allowOverwrite(false)
        .asFiles(Collections.singletonList(outputFile));
```

### LLM Instruction Prompt
- Call `allowOverwrite(boolean)` exactly once per builder pipeline. Calling it multiple times on the same builder throws an `IllegalStateException`.
- Only use this method when the pipeline terminates with file-based output methods (`toFile(File)`, `toFile(String)`, `toFiles(Iterable)`, `toFiles(Rename)`, `asFiles(Iterable)`, `asFiles(Rename)`). It has no effect on stream or in-memory outputs like `asBufferedImage()` or `toOutputStream()`.

### Prompt Snippet
```text
Configure the `Thumbnails.Builder` with `.allowOverwrite(boolean)` before calling terminal file output methods like `toFile` or `toFiles`. Do not call it more than once per builder instance to avoid an IllegalStateException.
```

### Common Failure Modes
- **`IllegalStateException`**: Thrown if `allowOverwrite` is called multiple times on the same `Thumbnails.Builder` instance.
- **Silent No-Op**: Calling `allowOverwrite` when the pipeline terminates with a non-file sink (e.g., `asBufferedImage()`, `toOutputStream()`) will not affect the output behavior.

### Fix Code Hint
```java
// WRONG: Calling allowOverwrite multiple times throws IllegalStateException
Thumbnails.of(inputFile)
    .size(100, 100)
    .allowOverwrite(true)
    .allowOverwrite(false) // Crashes here
    .toFile(outputFile);

// RIGHT: Call allowOverwrite exactly once before the terminal file operation
Thumbnails.of(inputFile)
    .size(100, 100)
    .allowOverwrite(true)
    .toFile(outputFile);
```

## API Test: `alphaInterpolation`

### Signature
```java
public Builder<T> alphaInterpolation(AlphaInterpolation config)
```
_Source: source/src/main/java/net/coobird/thumbnailator/Thumbnails.java:1379_

_Source doc:_ Sets the alpha interpolation mode when performing the resizing operation to generate the thumbnail. <p> Calling this method to set this parameter is optional. <p> Calling this method multiple times will result in an {@link IllegalStateException} to be thrown. <p> This method cannot be called in conjunction with the {@link #resizerFactory(ResizerFactory)} method. @param config		The alpha interpolation mode. @return				Reference to this object.

### Goal
Sets the alpha interpolation rendering hint used during the resizing operation to generate the thumbnail.

### Parameters
- `config` (`AlphaInterpolation`): The alpha interpolation mode to apply (e.g., `AlphaInterpolation.SPEED`). Must not be null.

### Input
A valid `Thumbnails.Builder` instance that has been initialized with an image source (e.g., via `Thumbnails.of(...)`). The builder must not have had `alphaInterpolation` called on it previously, and it must not be configured with a custom `ResizerFactory` via `resizerFactory(ResizerFactory)`.

### Output
Returns `Builder<T>` — A reference to the current `Thumbnails.Builder` object to allow for fluent method chaining.

### Valid Call Patterns
```java
// Applying alpha interpolation alongside a specific resizer
BufferedImage thumbnail = Thumbnails.of(img)
        .size(50, 50)
        .resizer(Resizers.PROGRESSIVE)
        .alphaInterpolation(AlphaInterpolation.SPEED)
        .asBufferedImage();
```

### LLM Instruction Prompt
- Use `alphaInterpolation(AlphaInterpolation)` to explicitly set the alpha interpolation mode for the resizing pipeline.
- NEVER pass `null` to this method; it will throw a `NullPointerException`.
- NEVER call this method multiple times on the same `Thumbnails.Builder` instance.
- NEVER call this method if the pipeline also uses `resizerFactory(ResizerFactory)`.

### Prompt Snippet
```text
When configuring a Thumbnailator pipeline, use `.alphaInterpolation(AlphaInterpolation.SPEED)` to set the alpha interpolation mode. Do not pass null, do not call it more than once per builder, and do not mix it with `.resizerFactory()`.
```

### Common Failure Modes
- **`NullPointerException`**: Thrown if the `config` argument is `null` (e.g., `Alpha interpolation is null.`).
- **`IllegalStateException`**: Thrown if `alphaInterpolation` is called multiple times on the same builder instance.
- **`IllegalStateException`**: Thrown if this method is called in conjunction with `resizerFactory(ResizerFactory)`.

### Fix Code Hint
```java
// BAD: Calling alphaInterpolation multiple times or passing null
Thumbnails.of("image.png")
    .size(200, 200)
    .alphaInterpolation(AlphaInterpolation.SPEED)
    .alphaInterpolation(AlphaInterpolation.QUALITY); // Throws IllegalStateException

// GOOD: Call exactly once with a valid AlphaInterpolation enum value
Thumbnails.of("image.png")
    .size(200, 200)
    .alphaInterpolation(AlphaInterpolation.SPEED)
    .toFile("thumbnail.png");
```

## API Test: `antialiasing`

### Signature
```java
public Builder<T> antialiasing(Antialiasing config)
```
_Source: source/src/main/java/net/coobird/thumbnailator/Thumbnails.java:1425_

_Source doc:_ Sets the antialiasing mode when performing the resizing operation to generate the thumbnail. <p> Calling this method to set this parameter is optional. <p> Calling this method multiple times will result in an {@link IllegalStateException}. <p> This method cannot be called in conjunction with the {@link #resizerFactory(ResizerFactory)} method. @param config		The antialiasing mode. @return				Reference to this object.

### Goal
Sets the antialiasing rendering hint to control edge smoothing during the image resizing operation.

### Parameters
- `config` (`Antialiasing`): The antialiasing mode to apply (e.g., `Antialiasing.DEFAULT`, `Antialiasing.ON`, `Antialiasing.OFF`). Must not be null.

### Input
A valid `Thumbnails.Builder` pipeline that has not already had its antialiasing mode set and has not been configured with a custom `ResizerFactory`.

### Output
Returns `Builder<T>` — a reference to the current fluent builder object to allow method chaining.

### Valid Call Patterns
```java
// given
BufferedImage img = new BufferedImageBuilder(200, 200).build();

// when
BufferedImage thumbnail = Thumbnails.of(img)
        .size(50, 50)
        .resizer(Resizers.PROGRESSIVE)
        .antialiasing(Antialiasing.DEFAULT)
        .asBufferedImage();
```

### LLM Instruction Prompt
- Do not call `antialiasing()` multiple times on the same builder instance; doing so throws an `IllegalStateException`.
- Do not call `antialiasing()` in conjunction with `resizerFactory(ResizerFactory)` on the same builder.
- Never pass `null` as the `config` argument; this will immediately throw a `NullPointerException`.
- Setting this parameter is entirely optional; if omitted, the default rendering hints of the underlying resizer are used.

### Prompt Snippet
```text
When configuring a Thumbnailator pipeline, use `.antialiasing(Antialiasing.ON)` (or `OFF`/`DEFAULT`) to explicitly control edge smoothing. You must call this method at most once per builder. Do not combine it with `.resizerFactory()` and never pass `null`.
```

### Common Failure Modes
- **`NullPointerException`**: Thrown with the message `"Antialiasing is null."` if the `config` argument is `null`.
- **`IllegalStateException`**: Thrown if `antialiasing()` is called more than once on the same builder instance.
- **`IllegalStateException`**: Thrown if `antialiasing()` is called on a builder that has already been configured using `resizerFactory(ResizerFactory)`.

### Fix Code Hint
```java
// BAD: Passing null or calling multiple times
// builder.antialiasing(null);
// builder.antialiasing(Antialiasing.ON).antialiasing(Antialiasing.OFF);

// BAD: Combining with resizerFactory
// builder.resizerFactory(myFactory).antialiasing(Antialiasing.ON);

// GOOD: Call exactly once with a valid enum value
Thumbnails.of(inputFile)
    .size(200, 200)
    .antialiasing(Antialiasing.ON)
    .toFile(outputFile);
```

## API Test: `apply`

### Signature
```java
public BufferedImage apply(BufferedImage img)
public String apply(String name, ThumbnailParameter param)
public String apply(String fileName, ThumbnailParameter param)
public abstract String apply(String name, ThumbnailParameter param)
```
_Source: source/src/main/java/net/coobird/thumbnailator/name/Rename.java:51  (+16 more definition site/overload)_

### Goal
Applies a renaming function to a given filename (excluding its directory path) to dynamically generate output filenames during batch image processing.

### Parameters
- `name` (`String`): The original file name to apply the renaming function on. *The file name must not include the directory in which the file resides.*
- `param` (`ThumbnailParameter`): The parameters used to create the thumbnail, which can be inspected to determine the new name (e.g., checking the requested output format).

### Input
A valid filename string representing the base name of the source image (without any directory path components) and a configured `ThumbnailParameter` object. When implementing a custom `Rename` strategy for batch processing sinks like `Thumbnails.Builder.toFiles(Rename)`, this method is called internally by the library for each file in the batch.

### Output
Returns `String` — The new file name after the renaming logic has been applied. This should also be a base filename without directory paths.

### Valid Call Patterns
```java
// Defining a custom Rename strategy by overriding apply
Rename customRenamer = new Rename() {
    @Override
    public String apply(String name, ThumbnailParameter param) {
        if (name.endsWith(".gif")) {
            // Example: modifying the name based on the original extension
            return "thumbnail." + name + ".foobar"; 
        }
        return "thumbnail." + name;
    }
};

// The custom renamer is then passed to a batch processing method
// (Note: Thumbnailator.createThumbnails is deprecated in favor of Thumbnails.fromFiles(...).toFiles(customRenamer))
```

### LLM Instruction Prompt
- When generating batch output files using `toFiles(Rename)` or `asFiles(Rename)`, you may need to implement a custom `Rename` class. Override the `apply(String name, ThumbnailParameter param)` method to define the naming logic.
- NEVER include directory paths in the `name` parameter or the returned string; Thumbnailator handles directory resolution internally.
- Ensure the returned filename has an extension supported by the JVM's Image I/O (e.g., `.jpg`, `.png`), or an `UnsupportedFormatException` will be thrown during the write phase.

### Prompt Snippet
```text
To dynamically rename files during Thumbnailator batch processing, create an anonymous subclass of `Rename` and override `public String apply(String name, ThumbnailParameter param)`. Return only the new base filename; do not include directory paths. Ensure the resulting file extension is supported by Java Image I/O.
```

### Common Failure Modes
- **Unsupported Format Extension**: Returning a filename with an unrecognized or unsupported extension (e.g., `.foobar`) will cause the underlying Image I/O to fail with an `UnsupportedFormatException` when Thumbnailator attempts to write the file.
- **Including Directory Paths**: Returning a string that includes directory separators (e.g., `"/output/" + name`) violates the contract and will break Thumbnailator's internal path resolution when saving batch files.
- **Filename Collisions**: Failing to generate a unique name for each input in a batch process can result in files overwriting each other if `allowOverwrite(true)` is set, or throwing an exception if it is false.

### Fix Code Hint
```java
// Correct implementation of a custom Rename strategy
Rename safeRenamer = new Rename() {
    @Override
    public String apply(String name, ThumbnailParameter param) {
        // Strip existing extension and append a safe, supported extension
        int dotIndex = name.lastIndexOf('.');
        String baseName = (dotIndex == -1) ? name : name.substring(0, dotIndex);
        
        // Return only the filename, no directories
        return "thumb_" + baseName + ".jpg";
    }
};

Thumbnails.fromFiles(files)
    .size(50, 50)
    .outputFormat("jpg")
    .toFiles(safeRenamer);
```

## API Test: `asBufferedImage`

### Signature
```java
public BufferedImage asBufferedImage()
```
_Source: source/src/main/java/net/coobird/thumbnailator/Thumbnails.java:2342_

_Source doc:_ <p> Creates a thumbnail and returns it as a {@link BufferedImage}. </p> <p> To call this method, the thumbnail must have been created from a single source. </p> <p> If you intend to write the {@link BufferedImage} to a file, you're strongly encouraged to use one of the {@code toFile(...)} methods instead. See "Notes on image types" for details. </p> <p><strong>Notes on image types</strong></p> <p> The image type of the {@link BufferedImage} depends on the type of the input image. (Specifically, the type emitted by the {@link javax.imageio.ImageReader} associated for the file type.) Thumbnailator will attempt to use the same image type as the input if it is not specified through {@link #imageType(int)}. </p> <p> This has implications when writing {@code BufferedImage} to files using the default JPEG writer bundled with Java. There are issues with the JPEG writer <a href="https://bugs.openjdk.java.net/browse/JDK-8041459">outputting wrong colors</a> or <a href="https://bugs.openjdk.java.net/browse/JDK-8204188">throwing exceptions</a> when writing a image containing an alpha channel. </p> <p> If outputting to a file, consider using one of the {@link #toFile(File)} or {@link #toFile(String)} methods instead, as it contains workarounds to prevent issues mentioned in the previous paragraph. </p> <p> For more information on {@code BufferedImage} types, refer to {@link BufferedImage#getType()}. </p> @return		A thumbnail as a {@link BufferedImage}. @throws IOException					If a problem occurred during the reading of the original image. @throws IllegalArgumentException		If multiple original images are specified.

### Goal
Executes the image processing pipeline and returns the resulting thumbnail as an in-memory `BufferedImage`.

### Parameters
_None._

### Input
A configured `Thumbnails.Builder` pipeline that was initialized with exactly **one** image source (e.g., a single `File`, `InputStream`, or `BufferedImage`).

### Output
Returns `BufferedImage` — The processed thumbnail image. The image type matches the input image type (or the type emitted by the underlying `ImageReader`) unless explicitly overridden in the pipeline via `imageType(int)`.

### Valid Call Patterns
```java
// given
BufferedImage img = new BufferedImageBuilder(200, 200).build();

// when
BufferedImage thumbnail = Thumbnails.of(img)
    .size(100, 100)
    .asBufferedImage();

// when (with output format specified)
BufferedImage thumbnailWithFormat = Thumbnails.of(img)
    .size(100, 100)
    .outputFormat("png")
    .asBufferedImage();
```

### LLM Instruction Prompt
- ONLY call `asBufferedImage()` on a `Thumbnails.Builder` that has a single image source. If the builder has multiple sources, it will throw an `IllegalArgumentException`.
- DO NOT use `asBufferedImage()` if the immediate next step is writing the image to a file using standard Java `ImageIO.write()`. Instead, use the terminal `.toFile(...)` methods on the builder, which contain built-in workarounds for JDK JPEG writer bugs related to alpha channels.
- Use this method when you need to keep the image in memory for further programmatic manipulation or custom headless rendering.

### Prompt Snippet
```text
To get an in-memory BufferedImage from a single source, use `.asBufferedImage()` as the terminal operation on the Thumbnails.Builder. Fails with IllegalArgumentException if the builder has multiple sources (use `.asBufferedImages()` instead). Do not use this if you intend to write directly to a file; use `.toFile()` instead to avoid JDK JPEG alpha channel bugs.
```

### Common Failure Modes
- **`IllegalArgumentException`**: Thrown if the builder was initialized with multiple images (e.g., `Thumbnails.fromFiles(Iterable)` or `Thumbnails.of(File[])` with length > 1).
- **`IOException`**: Thrown if there is an error reading the original image from its source.
- **Corrupted Colors / Exceptions on Save**: Occurs if the returned `BufferedImage` (which may contain an alpha channel) is manually written to a JPEG file using standard Java `ImageIO`. The default Java JPEG writer has known bugs handling alpha channels.

### Fix Code Hint
```java
// BAD: Calling asBufferedImage() on multiple sources throws IllegalArgumentException
// BufferedImage img = Thumbnails.of(file1, file2).size(100, 100).asBufferedImage();

// GOOD: Use asBufferedImages() for multiple sources
List<BufferedImage> images = Thumbnails.of(file1, file2).size(100, 100).asBufferedImages();

// BAD: Manual file write after asBufferedImage() risks JPEG alpha bugs
// BufferedImage img = Thumbnails.of(file).size(100, 100).asBufferedImage();
// ImageIO.write(img, "jpg", outFile);

// GOOD: Direct to file using Thumbnailator's safe writer workarounds
Thumbnails.of(file).size(100, 100).toFile(outFile);
```

## API Test: `asBufferedImages`

### Signature
```java
public List<BufferedImage> asBufferedImages()
```
_Source: source/src/main/java/net/coobird/thumbnailator/Thumbnails.java:2277_

_Source doc:_ <p> Create the thumbnails and return as a {@link List} of {@link BufferedImage}s. </p> <p> If you intend to write these {@link BufferedImage}s to files, you're strongly encouraged to use one of the {@code toFiles(...)} or {@code asFiles(...)} methods instead. See "Notes on image types" for details. </p> <p><strong>Notes on image types</strong></p> <p> The image type of the {@link BufferedImage} depends on the type of the input image. (Specifically, the type emitted by the {@link javax.imageio.ImageReader} associated for the file type.) Thumbnailator will attempt to use the same image type as the input if it is not specified through {@link #imageType(int)}. </p> <p> This has implications when writing {@code BufferedImage} to files using the default JPEG writer bundled with Java. There are issues with the JPEG writer <a href="https://bugs.openjdk.java.net/browse/JDK-8041459">outputting wrong colors</a> or <a href="https://bugs.openjdk.java.net/browse/JDK-8204188">throwing exceptions</a> when writing a image containing an alpha channel. </p> <p> If outputting to a file, consider using one of the {@link #toFiles(Iterable)}, {@link #toFiles(Rename)}, {@link #toFiles(File, Rename)} {@link #asFiles(Iterable)}, {@link #asFiles(Rename)} or {@link #asFiles(File, Rename)} methods instead, as it contains workarounds to prevent issues mentioned in the previous paragraph. </p> <p> For more information on {@code BufferedImage} types, refer to {@link BufferedImage#getType()}. </p> <p><strong>Note about performance</strong></p> <p> This method will process all inputs and create the corresponding thumbnails at once before returning them as in a list. Therefore, if many thumbnails are generated at once, it is possible that the Java virtual machine's heap space will run out and an {@link OutOfMemoryError} could be thrown. </p> <p> If many thumbnails are being processed at once, then using the {@link #iterableBufferedImages()} method would be preferable. </p> @return		A list of thumbnails. @throws IOException					If a problem occurred during the reading of the original images.

### Goal
Executes the configured image processing pipeline on all provided inputs and returns the resulting thumbnails as an in-memory list of `BufferedImage` objects.

### Parameters
_None._

### Input
A fully configured `Thumbnails.Builder` pipeline containing one or more image sources (such as files, streams, or `BufferedImage` instances) and at least one resizing constraint (e.g., `size(int, int)`).

### Output
Returns `List<BufferedImage>` — A list containing all the processed thumbnails in memory. The image type of each `BufferedImage` will match the type emitted by the `ImageReader` for the input file, unless explicitly overridden in the builder using `imageType(int)`.

### Valid Call Patterns
```java
// Pattern 1: Basic in-memory processing of a single image source
BufferedImage img = new BufferedImageBuilder(200, 200).build();
List<BufferedImage> thumbnails = Thumbnails.of(img)
    .size(100, 100)
    .asBufferedImages();

// Pattern 2: Processing with an explicit output format specified
BufferedImage img2 = new BufferedImageBuilder(200, 200).build();
List<BufferedImage> thumbnails2 = Thumbnails.of(img2)
    .size(100, 100)
    .outputFormat("png")
    .asBufferedImages();
```

### LLM Instruction Prompt
- Use `asBufferedImages()` ONLY when you strictly need all processed images loaded into memory simultaneously as a `List<BufferedImage>`.
- DO NOT use this method if the ultimate goal is to write the images to files. Standard Java Image I/O has known bugs when writing JPEGs with alpha channels (resulting in wrong colors or exceptions). Instead, use `toFiles(...)` or `asFiles(...)`, which contain built-in workarounds for these bugs.
- DO NOT use this method for large batches of images. Because it processes and retains all thumbnails in memory at once, it is highly susceptible to `OutOfMemoryError`. For large batches, use `iterableBufferedImages()` instead.

### Prompt Snippet
```text
When generating in-memory thumbnails with Thumbnailator, use `Thumbnails.of(...).size(w, h).asBufferedImages()`. However, if processing a large batch of images, use `iterableBufferedImages()` to prevent `OutOfMemoryError`. If your goal is to save the images to disk, NEVER use `asBufferedImages()` followed by manual Image I/O; use `toFiles(...)` directly to avoid Java JPEG alpha-channel bugs.
```

### Common Failure Modes
- **`OutOfMemoryError`**: Occurs if the input contains many images or very large images, as the method attempts to process and store every resulting thumbnail in the JVM heap at the same time.
- **`IOException`**: Thrown if a problem occurs while reading the original input images (e.g., missing files or broken streams).
- **Corrupted JPEG Output (Downstream)**: If the caller takes the returned `List<BufferedImage>` and manually writes them to JPEG files using `ImageIO.write`, images with alpha channels may throw exceptions or output with incorrect colors due to JDK bugs (JDK-8041459, JDK-8204188).

### Fix Code Hint
```java
// BAD: Prone to OutOfMemoryError for large batches
List<BufferedImage> thumbs = Thumbnails.of(manyFiles).size(200, 200).asBufferedImages();

// GOOD: Use iterableBufferedImages() for memory-safe lazy processing
Iterable<BufferedImage> thumbs = Thumbnails.of(manyFiles).size(200, 200).iterableBufferedImages();

// BAD: Manual file writing risks JPEG alpha-channel bugs
List<BufferedImage> thumbs = Thumbnails.of(files).size(200, 200).asBufferedImages();
for (int i = 0; i < thumbs.size(); i++) {
    ImageIO.write(thumbs.get(i), "jpg", new File("out" + i + ".jpg"));
}

// GOOD: Let Thumbnailator handle file writing safely
Thumbnails.of(files)
    .size(200, 200)
    .outputFormat("jpg")
    .toFiles(Rename.PREFIX_DOT_THUMBNAIL);
```

## API Test: `asFiles`

### Signature
```java
public List<File> asFiles(Iterable<File> iterable)
public List<File> asFiles(Rename rename)
public List<File> asFiles(File destinationDir, Rename rename)
```
_Source: source/src/main/java/net/coobird/thumbnailator/Thumbnails.java:2519  (+2 more definition site/overload)_

_Source doc:_ Creates thumbnails and stores them to files in the directory specified by the given {@link File} object, and using the {@link Rename} function to determine the filenames. The thubnail files are returned as a {@link List}. <p> When the destination file exists, and overwriting files has been disabled by calling the {@link #allowOverwrite(boolean)} method with {@code false}, then the thumbnail with the destination file already existing will not be written and the corresponding {@code File} object will not be included in the {@code List} returned by this method. <p> Extra caution should be taken when using this method, as there are no protections in place to prevent file name collisions resulting from creating thumbnails from files in separate directories but having the same name. In such a case, the behavior will be depend on the behavior of the {@link #allowOverwrite(boolean)} as described in the previous paragraph. <p> To call this method, the thumbnails must have been creates from files by calling the {@link Thumbnails#of(File...)} method. @param destinationDir	The destination directory to which the thumbnails should be written to. @param rename			The rename function which is used to determine the filenames of the thumbnail files to write. @return					A list of {@link File}s of the thumbnails which were created. @throws IOException		If a problem occurs while reading the original images or writing the thumbnails to files. @throws IllegalStateException		If the original images are not from files. @throws IllegalArgumentException		If the destination directory is not a directory. @since 	0.4.7

### Goal
Executes the image processing pipeline, writes the resulting thumbnails to the filesystem, and returns a list of the successfully created `File` objects.

### Parameters
- `destinationDir` (`File`): The destination directory where the generated thumbnails should be written. Must be an existing directory.
- `rename` (`Rename`): The renaming strategy used to dynamically generate output filenames based on the original input filenames (e.g., `Rename.PREFIX_DOT_THUMBNAIL`).

### Input
- **Preconditions for `Rename` overloads**: The pipeline *must* have been initialized with file sources (e.g., `Thumbnails.of(File...)` or `Thumbnails.fromFiles(...)`). If initialized from streams, URLs, or memory, the original filenames are unknown, and the method will fail.
- **Preconditions for `Iterable<File>` overload**: The pipeline can be initialized from any source type, but the provided `Iterable<File>` must contain exactly one destination `File` for each input image in the pipeline.
- **Directory State**: When using `destinationDir`, the provided `File` object must point to a valid, existing directory.

### Output
Returns `List<File>` — A list containing the `File` objects of the thumbnails that were successfully created and written to disk. If `allowOverwrite(false)` was configured on the builder and a destination file already exists, that file is skipped and will *not* be included in this returned list.

### Valid Call Patterns
```java
// Pattern 1: Using an Iterable of destination files (works with any input source)
List<File> results = Thumbnails.fromInputStreams(getSources())
        .size(100, 100)
        .asFiles(Arrays.asList(outFile1, outFile2));

// Pattern 2: Using a Rename strategy (requires File input sources)
List<File> results = Thumbnails.fromFiles(getFileSources())
        .size(100, 100)
        .asFiles(Rename.PREFIX_DOT_THUMBNAIL);
```

### LLM Instruction Prompt
- When calling `asFiles(Rename)` or `asFiles(File, Rename)`, you MUST ensure the pipeline was started with `File` inputs (e.g., `Thumbnails.fromFiles(...)`).
- If the pipeline starts with `InputStream`, `URL`, or `BufferedImage`, you MUST use `asFiles(Iterable<File>)` instead to explicitly provide the output file paths.
- When using built-in rename strategies, use `Rename.PREFIX_HYPHEN_THUMBNAIL` or `Rename.SUFFIX_HYPHEN_THUMBNAIL`; NEVER use the deprecated typo versions containing `HYPTHEN`.
- Always handle or declare `java.io.IOException`, as this is a terminal I/O operation.

### Prompt Snippet
```text
Write a Java method that takes a List of image Files, resizes them to 200x200, and saves them to a specified destination directory using the `asFiles` method with a prefix rename strategy. Return the List of created Files.
```

### Common Failure Modes
- **`IllegalStateException`**: Thrown if `asFiles(Rename)` or `asFiles(File, Rename)` is called on a pipeline that was initialized from non-file sources (like `InputStream` or `BufferedImage`), because there are no original filenames to apply the `Rename` function to.
- **`IllegalArgumentException`**: Thrown if the `destinationDir` provided is not a valid directory.
- **`IOException`**: Thrown if the underlying Java Image I/O fails to read the source images or write the destination files (e.g., due to permissions or unsupported formats).
- **Filename Collisions**: If processing files with the exact same name from different source directories into a single `destinationDir`, they will overwrite each other unless `allowOverwrite(false)` is set (which will cause subsequent files to be skipped).

### Fix Code Hint
```java
// BAD: Calling a Rename overload on InputStream sources throws IllegalStateException
// List<File> out = Thumbnails.fromInputStreams(streams).size(100, 100).asFiles(Rename.PREFIX_DOT_THUMBNAIL);

// GOOD: Use Iterable<File> when sources are not files
List<File> out = Thumbnails.fromInputStreams(streams)
        .size(100, 100)
        .asFiles(Arrays.asList(new File("out1.jpg"), new File("out2.jpg")));

// GOOD: Use Rename when sources ARE files
List<File> out = Thumbnails.fromFiles(fileList)
        .size(100, 100)
        .asFiles(destinationDir, Rename.PREFIX_HYPHEN_THUMBNAIL);
```

## API Test: `build`

### Signature
```java
public ThumbnailParameter build()
public BufferedImage build()
```
_Source: source/src/main/java/net/coobird/thumbnailator/builders/ThumbnailParameterBuilder.java:362  (+1 more definition site/overload)_

_Source doc:_ Returns a {@link ThumbnailParameter} from the parameters which are currently set. <p> This method will throw a {@link IllegalArgumentException} required parameters for the {@link ThumbnailParameter} have not been set. @return		A {@link ThumbnailParameter} with parameters set through the use of this builder. @throws IllegalStateException	If neither the size nor the scaling factor has been set.

### Goal
Generates and returns a newly created `BufferedImage` or `ThumbnailParameter` from the configuration state accumulated in the respective builder.

### Parameters
_None._

### Input
A fully configured builder instance (such as `BufferedImageBuilder` or `ThumbnailParameterBuilder`). Preconditions dictate that when using `ThumbnailParameterBuilder`, either the size or the scaling factor **must** be set prior to invocation.

### Output
Returns `ThumbnailParameter` (or `BufferedImage`) — A newly instantiated object containing the exact parameters, dimensions, and image types specified during the builder's configuration phase, ready for use in headless image processing pipelines.

### Valid Call Patterns
```java
// From ThumbnailatorTest.java: Building an in-memory BufferedImage for testing
BufferedImage img = new BufferedImageBuilder(200, 200, BufferedImage.TYPE_INT_ARGB).build();
```

### LLM Instruction Prompt
- Always use `build()` as the terminal method to extract the constructed `BufferedImage` or `ThumbnailParameter` from its builder.
- When building a `ThumbnailParameter`, you MUST set either the size or the scaling factor on the builder before calling `build()`, otherwise an `IllegalStateException` will be thrown.
- Use `BufferedImageBuilder(...).build()` to safely generate deterministic, in-memory images for headless test harnesses without relying on external files.

### Prompt Snippet
```text
To instantiate a BufferedImage for testing or processing, use `new BufferedImageBuilder(width, height, type).build()`. When using `ThumbnailParameterBuilder`, ensure size or scale is set before calling `build()` to avoid an IllegalStateException.
```

### Common Failure Modes
- **`IllegalStateException`**: Thrown by `ThumbnailParameterBuilder.build()` if neither the size nor the scaling factor has been configured on the builder.
- **`IllegalArgumentException`**: Thrown if other required parameters for the `ThumbnailParameter` have not been set before calling `build()`.

### Fix Code Hint
```java
// FIX: Ensure size or scale is set before building a ThumbnailParameter
ThumbnailParameter param = new ThumbnailParameterBuilder()
    .size(100, 100) // Required precondition to prevent IllegalStateException
    .build();
```

## API Test: `calculate`

### Signature
```java
public Dimension calculate(int width, int height)
public Rectangle calculate( int outerWidth, int outerHeight, boolean flipHorizontal, boolean flipVertical, boolean swapDimensions )
public Point calculate(int enclosingWidth, int enclosingHeight, int width, int height, int insetLeft, int insetRight, int insetTop, int insetBottom)
public Point calculate( int enclosingWidth, int enclosingHeight, int width, int height, int insetLeft, int insetRight, int insetTop, int insetBottom )
```
_Source: source/src/main/java/net/coobird/thumbnailator/geometry/Positions.java:50  (+14 more definition site/overload)_

### Goal
Calculates the absolute X and Y coordinates to position an object within an enclosing object, applying specified directional insets.

### Parameters
- `enclosingWidth` (`int`): The width in pixels of the enclosing object (e.g., the base image or canvas) that is to contain the enclosed object.
- `enclosingHeight` (`int`): The height in pixels of the enclosing object.
- `width` (`int`): The width in pixels of the object that is to be placed inside (e.g., a watermark or cropped region).
- `height` (`int`): The height in pixels of the object that is to be placed inside.
- `insetLeft` (`int`): The inset (margin/padding) in pixels on the left-hand side of the object to be enclosed.
- `insetRight` (`int`): The inset in pixels on the right-hand side of the object to be enclosed.
- `insetTop` (`int`): The inset in pixels on the top side of the object to be enclosed.
- `insetBottom` (`int`): The inset in pixels on the bottom side of the object to be enclosed.

### Input
Eight integer values representing pixel dimensions and margins. This method is typically invoked on an implementation of the `net.coobird.thumbnailator.geometry.Position` interface (such as the `Positions` enum) to resolve a relative placement strategy (like center or bottom-right) into exact coordinates.

### Output
Returns `Point` — A `java.awt.Point` representing the absolute X and Y coordinates where the top-left corner of the enclosed object should be placed.

### Valid Call Patterns
```java
// Inferred from signature and project context (not verified by existing tests)
import net.coobird.thumbnailator.geometry.Position;
import net.coobird.thumbnailator.geometry.Positions;
import java.awt.Point;

Position position = Positions.BOTTOM_RIGHT;
Point placement = position.calculate(
    800, 600, // enclosingWidth, enclosingHeight
    200, 100, // width, height
    10, 10, 10, 10 // insetLeft, insetRight, insetTop, insetBottom
);
```

### LLM Instruction Prompt
- When calculating absolute placement coordinates for an image within a larger canvas (e.g., for custom watermarking or cropping logic), call `calculate` on a `Position` instance. You must provide all 8 integer arguments in the exact order: enclosing dimensions, object dimensions, and the four directional insets (left, right, top, bottom).

### Prompt Snippet
```text
Use the `Position.calculate` method to determine the exact `java.awt.Point` for placing an overlay. Ensure you pass the 8 integer parameters in the correct order: enclosing width/height, overlay width/height, and left/right/top/bottom insets.
```

### Common Failure Modes
- **Parameter Order Confusion**: Because the method takes 8 consecutive `int` parameters, it is extremely easy to accidentally swap width/height or the order of the insets (Left, Right, Top, Bottom).
- **Negative Coordinates**: If the enclosed object's dimensions plus the specified insets exceed the enclosing object's dimensions, the resulting `Point` may contain negative coordinates depending on the specific `Position` implementation's alignment logic, which can lead to the image being drawn off-canvas.

### Fix Code Hint
```java
// Incorrect: Swapping object dimensions with enclosing dimensions or mixing inset order
// Point p = position.calculate(objW, objH, encW, encH, top, bottom, left, right);

// Correct: Strictly follow (enclosingW, enclosingH, objW, objH, left, right, top, bottom)
Point p = position.calculate(
    baseImage.getWidth(), baseImage.getHeight(),
    watermark.getWidth(), watermark.getHeight(),
    insetLeft, insetRight, insetTop, insetBottom
);
```

## API Test: `clear`

### Signature
```java
static void clear()
```
_Source: source/src/main/java/net/coobird/thumbnailator/util/Configurations.java:130_

_Source doc:_ Clears the internal cache of properties. <p> This is intended only to be called from tests.

### Goal
Clears the internal cache of properties within the `Configurations` utility, intended exclusively for use in test environments to ensure test isolation.

### Parameters
_None._

### Input
No input is required. The caller must be executing within a test harness where resetting the internal property cache of `Configurations` is necessary. It is a strict precondition that this method is not invoked during standard production image processing workflows.

### Output
Returns `void` — performs the cache clearing operation as an internal side effect.

### Valid Call Patterns
*(Inferred from signature; not verified by existing tests or README examples)*
```java
// Typically used in a test setup or teardown method
Configurations.clear();
```

### LLM Instruction Prompt
- Only call `Configurations.clear()` when writing or executing unit tests for Thumbnailator to reset internal property caches. 
- Do not use this method in production image processing pipelines or fluent `Thumbnails.Builder` chains.

### Prompt Snippet
```text
Use `Configurations.clear()` exclusively in test teardown or setup blocks to clear the internal cache of properties. Never use it in production code.
```

### Common Failure Modes
- **Calling in production code**: Invoking this method outside of a test harness can cause unexpected cache misses, performance degradation, or race conditions if properties are cleared concurrently while image processing pipelines are actively running.

### Fix Code Hint
```java
// Remove from production code:
// Configurations.clear(); 

// Move to test lifecycle methods (e.g., JUnit @After or @Before):
@After
public void tearDown() {
    Configurations.clear();
}
```

## API Test: `copy`

### Signature
```java
public static BufferedImage copy(BufferedImage img)
public static BufferedImage copy(BufferedImage img, int imageType)
```
_Source: source/src/main/java/net/coobird/thumbnailator/util/BufferedImages.java:63  (+1 more definition site/overload)_

_Source doc:_ Returns a {@link BufferedImage} with the specified image type, where the graphical content is a copy of the specified image. @param img		The image to copy. @param imageType	The image type for the image to return. @return			A copy of the specified image.

### Goal
Creates an independent in-memory copy of a `BufferedImage`, optionally converting its underlying color model to a specified image type.

### Parameters
- `img` (`BufferedImage`): The source in-memory image to duplicate.
- `imageType` (`int`): An integer representing the desired image type for the new copy (e.g., `BufferedImage.TYPE_INT_ARGB`, `BufferedImage.TYPE_INT_RGB`).

### Input
A valid, non-null `BufferedImage` instance loaded in memory. If using the two-argument overload, the caller must provide a valid `BufferedImage.TYPE_*` constant for the `imageType` parameter.

### Output
Returns `BufferedImage` — A new, independent image instance containing the exact graphical content of the source image, safely decoupled from the original's memory reference and formatted to the requested image type.

### Valid Call Patterns
```java
// 1. Exact form from the test suite (1-arg overload)
BufferedImage originalImage = new BufferedImage(200, 200, BufferedImage.TYPE_INT_ARGB);
BufferedImage copyImage = BufferedImages.copy(originalImage);

// 2. Inferred from the signature (2-arg overload)
BufferedImage convertedCopy = BufferedImages.copy(originalImage, BufferedImage.TYPE_INT_RGB);
```

### LLM Instruction Prompt
- When testing `ImageFilter` implementations or needing a non-destructive backup of an image before processing, use `BufferedImages.copy(img)` to create an independent clone. Use the two-argument overload `BufferedImages.copy(img, imageType)` to simultaneously copy and convert the image to a specific `BufferedImage.TYPE_*` format.

### Prompt Snippet
```text
To safely duplicate a BufferedImage in memory without altering the original (e.g., for filter verification or non-destructive pipelines), use `BufferedImages.copy(originalImage)`. To force a specific color model during the copy, pass a standard `BufferedImage.TYPE_*` constant as the second argument.
```

### Common Failure Modes
- **`NullPointerException`**: Occurs if the provided `img` parameter is `null`.
- **`IllegalArgumentException`**: Occurs if an unrecognized or invalid integer is passed to the `imageType` parameter, causing the underlying `BufferedImage` constructor to fail with an "Unknown image type" error.

### Fix Code Hint
```java
// Ensure the source image is not null and use standard AWT image type constants
if (originalImage != null) {
    BufferedImage safeCopy = BufferedImages.copy(originalImage, BufferedImage.TYPE_INT_ARGB);
    // Proceed with applying destructive filters to the originalImage while preserving safeCopy
}
```

## API Test: `createOutputStream`

### Signature
```java
OutputStream createOutputStream(File destinationFile)
```
_Source: source/src/main/java/net/coobird/thumbnailator/tasks/io/FileImageSink.java:326_

### Goal
Creates and opens a file-backed output stream for a designated destination file, typically used internally by image sinks to write processed thumbnail data to disk.

### Parameters
- `destinationFile` (`File`): The target file object representing the path where the image data will be written.

### Input
A valid `java.io.File` instance pointing to a writable location on the filesystem. The host environment must have sufficient permissions to create or overwrite the file at the specified path.

### Output
Returns `OutputStream` — A standard Java byte output stream connected to the destination file, ready to receive the encoded binary image data from the Thumbnailator pipeline.

### Valid Call Patterns
```java
// Derived from the test suite's mocking pattern for FileImageSink
File outputFile = new File("test.png");
FileImageSink sink = new FileImageSink(outputFile);

// Direct invocation (often used internally by the sink's write() method)
OutputStream os = sink.createOutputStream(outputFile);
```

### LLM Instruction Prompt
- Do not use `createOutputStream` for standard thumbnail generation workflows; prefer the fluent `Thumbnails.Builder.toFile(File)` or `toFiles(Rename)` terminal methods.
- Only use `createOutputStream` when extending `FileImageSink`, building custom `ImageSink` implementations, or writing tests that require mocking I/O failures (e.g., using Mockito spies).
- The caller is strictly responsible for closing the returned `OutputStream` to prevent file handle leaks.

### Prompt Snippet
```text
When implementing custom sinks or testing I/O error handling in Thumbnailator, use `sink.createOutputStream(destinationFile)` to obtain the output stream. Ensure the stream is safely closed in a `finally` block or try-with-resources, as demonstrated by the library's internal error-handling tests.
```

### Common Failure Modes
- **Resource Leaks**: Failing to call `.close()` on the returned `OutputStream` after writing completes or an exception is thrown.
- **I/O Exceptions**: Throwing an `IOException` if the file path is invalid, points to a directory instead of a file, or lacks write permissions.
- **Write Errors**: As shown in the test suite, the underlying stream may throw an `IOException` during `.write(...)` operations (e.g., if the disk becomes full), which must be caught and handled by the caller.

### Fix Code Hint
```java
File outputFile = new File("output.png");
FileImageSink sink = new FileImageSink(outputFile);

// Always use try-with-resources to ensure the stream is closed, 
// even if an IOException occurs during the write process.
try (OutputStream os = sink.createOutputStream(outputFile)) {
    // Write image data to the stream
} catch (IOException e) {
    // Handle stream creation or write errors
    e.printStackTrace();
}
```

## API Test: `createThumbnail`

### Signature
```java
public static void createThumbnail(ThumbnailTask<?, ?> task)
public static BufferedImage createThumbnail( BufferedImage img, int width, int height )
public static void createThumbnail( File inFile, File outFile, int width, int height )
public static BufferedImage createThumbnail( File f, int width, int height )
public static Image createThumbnail( Image img, int width, int height )
public static void createThumbnail( InputStream is, OutputStream os, int width, int height )
public static void createThumbnail( InputStream is, OutputStream os, String format, int width, int height )
```
_Source: source/src/main/java/net/coobird/thumbnailator/Thumbnailator.java:356  (+6 more definition site/overload)_

_Source doc:_ Creates a thumbnail from image data streamed from an {@link InputStream} and streams the data out to an {@link OutputStream}, with the specified format for the output data. @param is			The {@link InputStream} from which to obtain image data. @param os			The {@link OutputStream} to send thumbnail data to. @param format		The image format to use to store the thumbnail data. @param width			The width of the thumbnail. @param height		The height of the thumbnail. @throws IOException	Thrown when a problem occurs when reading from {@code File} representing an image file. @throws IllegalArgumentException		If the specified output format is not supported.

### Goal
Generates a resized image thumbnail from an input stream and writes it directly to an output stream using a specified image format.

### Parameters
- `is` (`InputStream`): The `InputStream` from which to obtain the source image data. Must not be null.
- `os` (`OutputStream`): The `OutputStream` to send the generated thumbnail data to. Must not be null.
- `format` (`String`): The image format to use to store the thumbnail data (e.g., "jpg", "png"). Must be supported by the host JVM's Image I/O.
- `width` (`int`): The target width of the thumbnail in pixels.
- `height` (`int`): The target height of the thumbnail in pixels.

### Input
The caller must provide an open `InputStream` containing valid image data that the underlying Java Image I/O can decode, and an open `OutputStream` ready to receive the encoded bytes. The `format` string must be a format supported by the JVM's Image I/O implementation. The `width` and `height` must be positive integers. 

### Output
Returns `void` — the resulting thumbnail image bytes are written directly to the provided `OutputStream`.

### Valid Call Patterns
```java
// 4-argument overload (verbatim from test suite)
byte[] bytes = makeImageData("jpg", 200, 200);
InputStream is = new ByteArrayInputStream(bytes);
ByteArrayOutputStream os = new ByteArrayOutputStream();

Thumbnailator.createThumbnail(is, os, 50, 50);

// 5-argument overload (inferred from signature)
InputStream is2 = new ByteArrayInputStream(bytes);
ByteArrayOutputStream os2 = new ByteArrayOutputStream();

Thumbnailator.createThumbnail(is2, os2, "png", 50, 50);
```

### LLM Instruction Prompt
- **Strict Preference**: The fluent interface (`Thumbnails.of(...).size(...).toOutputStream(...)`) is the strictly preferred paradigm over manual `Thumbnailator.createThumbnail(...)` static method calls. Only use `createThumbnail` if explicitly maintaining legacy code.
- Do not pass `null` for `is` or `os`; the method will fail.
- Ensure the `format` string is supported by the standard Java Image I/O API.
- The library runs headless; do not attempt to use desktop UI components to supply the streams.

### Prompt Snippet
```text
Use Thumbnailator to read an image from `inputStream`, resize it to 100x100, and write it to `outputStream` as a "jpg". Note: While `Thumbnailator.createThumbnail` exists, you MUST use the preferred fluent builder API (`Thumbnails.of(inputStream)...`) instead.
```

### Common Failure Modes
- **Null Streams**: Passing `null` for the `InputStream` or `OutputStream` will cause the method to fail (as explicitly verified in the project's test suite).
- **Unsupported Format**: If the specified `format` string is not supported by the underlying Java Image I/O, an `IllegalArgumentException` (or `UnsupportedFormatException`) is thrown.
- **Invalid Image Data**: If the `InputStream` does not contain valid image data or cannot be read, an `IOException` is thrown.

### Fix Code Hint
```java
// Anti-pattern: Using the legacy static method with potential nulls
// Thumbnailator.createThumbnail(is, os, "jpg", 100, 100);

// Preferred pattern: Use the fluent builder API and ensure streams are valid
if (is != null && os != null) {
    Thumbnails.of(is)
        .size(100, 100)
        .outputFormat("jpg")
        .toOutputStream(os);
}
```

## API Test: `createThumbnails`

### Signature
```java
public static void createThumbnails( Collection<? extends File> files, Rename rename, int width, int height )
```
_Source: source/src/main/java/net/coobird/thumbnailator/Thumbnailator.java:453_

_Source doc:_ Creates thumbnails from a specified {@code Collection} of {@code File}s. The filenames of the resulting thumbnails are determined by applying the specified {@code Rename} function. @param files			A {@code Collection} containing {@code File} objects of image files. @param rename		The renaming function to use. @param width			The width of the thumbnail. @param height		The height of the thumbnail. @throws IOException	Thrown when a problem occurs when reading from {@code File} representing an image file. @deprecated		This method has been deprecated in favor of using the {@link Thumbnails#fromFiles(Iterable)} interface. This method will be removed in 0.5.0, and will not be further maintained.

### Goal
Creates thumbnails for a collection of image files and saves them to disk using a specified renaming strategy, though this legacy method is deprecated in favor of the fluent builder API.

### Parameters
- `files` (`Collection<? extends File>`): A collection containing `File` objects of the source image files to be processed. Must not be null.
- `rename` (`Rename`): The renaming strategy (e.g., `Rename.PREFIX_DOT_THUMBNAIL`) used to dynamically generate output filenames and prevent collisions during batch processing. Must not be null.
- `width` (`int`): The target width of the generated thumbnails in pixels.
- `height` (`int`): The target height of the generated thumbnails in pixels.

### Input
A non-null `Collection` of valid image `File` objects whose formats are supported by the host JVM's standard Image I/O capabilities. A non-null `Rename` instance must be provided to dictate how the output files are named relative to the input files.

### Output
Returns `void` — the method writes the processed thumbnail images directly to the file system as determined by the `Rename` function.

### Valid Call Patterns
```java
/* 
 * Note: This method is deprecated. The fluent API is strictly preferred.
 * This example demonstrates the legacy call form based on test suite usage.
 */
List<File> files = Collections.singletonList(new File("source.jpg"));
Thumbnailator.createThumbnails(
    files,
    Rename.PREFIX_DOT_THUMBNAIL,
    50,
    50
);
```

### LLM Instruction Prompt
- **DO NOT USE** this method for new code generation. It is deprecated and slated for removal. You MUST use the fluent interface `Thumbnails.fromFiles(Iterable)` instead.
- If modifying legacy code that already uses this method, ensure neither `files` nor `rename` is `null`, as this will immediately throw a `NullPointerException`.
- When specifying the `Rename` strategy, avoid the deprecated typo constants (e.g., `Rename.PREFIX_HYPTHEN_THUMBNAIL`); use the corrected versions (e.g., `Rename.PREFIX_HYPHEN_THUMBNAIL`).

### Prompt Snippet
```text
The static method `Thumbnailator.createThumbnails` is deprecated. For batch file processing, strictly use the fluent builder: `Thumbnails.fromFiles(files).size(width, height).toFiles(rename);`. If maintaining legacy calls, ensure `files` and `rename` are non-null to avoid NullPointerExceptions.
```

### Common Failure Modes
- **`NullPointerException`**: Thrown immediately if the `files` collection is `null` (message: `"Collection of Files is null."`) or if the `rename` argument is `null` (message: `"Rename is null."`).
- **`IOException`**: Thrown if a problem occurs when reading from or writing to a `File` representing an image.
- **`UnsupportedFormatException`**: Thrown if the underlying Java Image I/O does not support reading the input file format or writing the output format.

### Fix Code Hint
```java
// BAD: Using the deprecated static utility method
Thumbnailator.createThumbnails(files, Rename.PREFIX_DOT_THUMBNAIL, 640, 480);

// GOOD: Using the strictly preferred fluent builder API
Thumbnails.fromFiles(files)
    .size(640, 480)
    .toFiles(Rename.PREFIX_DOT_THUMBNAIL);
```

## API Test: `createThumbnailsAsCollection`

### Signature
```java
public static Collection<File> createThumbnailsAsCollection( Collection<? extends File> files, Rename rename, int width, int height )
```
_Source: source/src/main/java/net/coobird/thumbnailator/Thumbnailator.java:400_

_Source doc:_ Creates thumbnails from a specified {@link Collection} of {@link File}s. The filenames of the resulting thumbnails are determined by applying the specified {@link Rename}. <p> The order of the thumbnail {@code File}s in the returned {@code Collection} will be the same as the order as the source list. @param files			A {@code Collection} containing {@code File} objects of image files. @param rename		The renaming function to use. @param width			The width of the thumbnail. @param height		The height of the thumbnail. @throws IOException	Thrown when a problem occurs when reading from {@code File} representing an image file. @return 			A collection of {@code File}s to the thumbnails. @deprecated		This method has been deprecated in favor of using the {@link Thumbnails#fromFiles(Iterable)} interface. This method will be removed in 0.5.0, and will not be further maintained.

### Goal
Creates thumbnails from a collection of image files, applies a renaming strategy to generate output filenames, and returns a collection of the newly created thumbnail files (Note: this method is deprecated).

### Parameters
- `files` (`Collection<? extends File>`): A collection containing `File` objects of the source image files to be processed.
- `rename` (`Rename`): The renaming function/strategy (e.g., `Rename.PREFIX_DOT_THUMBNAIL`) used to dynamically generate output filenames and prevent collisions.
- `width` (`int`): The target width of the generated thumbnails in pixels.
- `height` (`int`): The target height of the generated thumbnails in pixels.

### Input
A non-null `Collection` of valid image `File` objects whose formats are supported by the host JVM's standard Image I/O capabilities. A non-null `Rename` instance must be provided to dictate how the output files are named relative to the input files.

### Output
Returns `Collection<File>` — A collection of `File` objects pointing to the successfully generated thumbnails. The order of the files in this returned collection strictly matches the order of the source list.

### Valid Call Patterns
```java
/*
 * The files to make thumbnails of.
 */
List<File> files = Collections.singletonList(
        new File("sourceImage.jpg")
);

// Note: This method is deprecated in favor of Thumbnails.fromFiles(...)
Collection<File> thumbnails = Thumbnailator.createThumbnailsAsCollection(
        files,
        Rename.PREFIX_DOT_THUMBNAIL,
        50,
        50
);
```

### LLM Instruction Prompt
- **DO NOT** use this method for new code generation; it is strictly deprecated. You MUST replace it with the fluent builder interface `Thumbnails.fromFiles(Iterable)`.
- If maintaining legacy code that uses this method, ensure neither `files` nor `rename` is `null` to avoid a `NullPointerException`.
- When specifying the `Rename` strategy, use correctly spelled constants (e.g., `Rename.PREFIX_HYPHEN_THUMBNAIL`) and avoid the deprecated typo versions (e.g., `Rename.PREFIX_HYPTHEN_THUMBNAIL`).

### Prompt Snippet
```text
The static method `Thumbnailator.createThumbnailsAsCollection` is deprecated and will be removed. Do not use it. Instead, use the fluent API: `Thumbnails.fromFiles(files).size(width, height).asFiles(rename)`. If modifying existing legacy calls, ensure `files` and `rename` are non-null.
```

### Common Failure Modes
- **Null Collection**: Passing `null` for the `files` parameter throws a `NullPointerException` with the exact message `"Collection of Files is null."`.
- **Null Rename Strategy**: Passing `null` for the `rename` parameter throws a `NullPointerException` with the exact message `"Rename is null."`.
- **Unsupported Formats**: If an input file uses an image format not supported by the underlying Java Image I/O implementation, an `UnsupportedFormatException` is thrown.
- **I/O Errors**: Throws an `IOException` if a problem occurs while reading from the source `File` or writing to the destination `File`.

### Fix Code Hint
```java
// ❌ BAD: Using the deprecated legacy method
Collection<File> thumbnails = Thumbnailator.createThumbnailsAsCollection(
    files, 
    Rename.PREFIX_DOT_THUMBNAIL, 
    640, 
    480
);

// ✅ GOOD: Using the strictly preferred fluent builder interface
List<File> thumbnails = Thumbnails.fromFiles(files)
    .size(640, 480)
    .asFiles(Rename.PREFIX_DOT_THUMBNAIL);
```

## API Test: `crop`

### Signature
```java
public Builder<T> crop(Position position)
```
_Source: source/src/main/java/net/coobird/thumbnailator/Thumbnails.java:1226_

_Source doc:_ Crops the thumbnail at the position specified by {@link Position}. This method must be used along with the {@link #size(int, int)} method to specify the size of the thumbnail. <p>This method will guarantee that the thumbnail will be exactly the dimensions specified in the {@link #size(int, int)} method. <p>Internally, the resizing is performed in two steps: <p>First, the thumbnail will be sized so that one of the dimensions will be exactly the dimension specified in the {@code size} method. The other dimension may overhang the specified dimension. For example, if the {@code .size(200, 200)} is called and the source image is 400 x 600, the image will be resized to 200 x 300, internally. <p>Next, the resized image will be cropped to the dimensions specified in the {@code size} method, positioned using the specified {@link Position} object. Continuing the example from the previous paragraph, the 200 x 300 image will be cropped to 200 x 200 using the specified positioning. <p>Once this method is called, calling the {@link #scale(double)} or {@link #scale(double, double)} method will throw an {@link IllegalStateException}. <p>Calling this method multiple times will throw an {@link IllegalStateException}. @param position		The position to which the thumbnail should be cropped to. For example, if {@link Positions#CENTER} is specified, the resulting thumbnail will be made by cropping to the center of the image. @return				Reference to this object. @throws NullPointerException		If the position is {@code null}. @since 	0.4.0

### Goal
Configures the image processing pipeline to crop the resized image to the exact dimensions specified by the `size` method, using the provided positioning strategy to determine which part of the overhanging image is kept.

### Parameters
- `position` (`Position`): The geometric position to which the thumbnail should be cropped (e.g., `Positions.CENTER` from the `net.coobird.thumbnailator.geometry` package). Cannot be `null`.

### Input
- A `Thumbnails.Builder` instance initialized with an image source.
- **Precondition**: The builder *must* also be configured with `size(int, int)` (either before or after calling `crop`).
- **Precondition**: The builder *must not* be configured with `scale(double)` or `scale(double, double)`.
- **Precondition**: `crop` must not have been called previously on this builder instance.

### Output
Returns `Builder<T>` — A reference to the current builder object to allow for fluent method chaining.

### Valid Call Patterns
```java
// Pattern 1: Calling size() before crop()
BufferedImage img = new BufferedImageBuilder(200, 200).build();
BufferedImage thumbnail = Thumbnails.of(img)
        .size(100, 50)
        .crop(Positions.CENTER)
        .asBufferedImage();

// Pattern 2: Calling crop() before size()
BufferedImage img2 = new BufferedImageBuilder(200, 200).build();
BufferedImage thumbnail2 = Thumbnails.of(img2)
        .crop(Positions.CENTER)
        .size(100, 50)
        .asBufferedImage();
```

### LLM Instruction Prompt
- When using `crop(Position)`, you MUST also call `size(int, int)` on the builder to define the exact dimensions of the final cropped thumbnail.
- NEVER call `scale(...)` on a builder that uses `crop(...)`. This will throw an `IllegalStateException`.
- NEVER call `crop(...)` multiple times on the same builder.
- Pass a valid `Position` implementation, such as `Positions.CENTER`. Do not pass `null`.

### Prompt Snippet
```text
To crop an image in Thumbnailator, use `.crop(Positions.CENTER)` on the `Thumbnails.Builder`. You MUST pair this with `.size(width, height)` to specify the final dimensions. The library will automatically resize the image to fit one dimension and crop the overhang. Do NOT use `.scale(...)` or call `.crop(...)` more than once per builder, as both will throw an IllegalStateException.
```

### Common Failure Modes
- **`IllegalStateException`**: Thrown if `scale(double)` or `scale(double, double)` is called on the builder after `crop` has been called.
- **`IllegalStateException`**: Thrown if `crop(Position)` is called multiple times on the same builder instance.
- **`NullPointerException`**: Thrown if the `position` argument is `null`.
- **Logical Failure / Missing Size**: Failing to call `size(int, int)` in the same pipeline will result in an incomplete configuration, as `crop` relies entirely on `size` to determine the final dimensions.

### Fix Code Hint
```java
// BAD: Using scale() with crop() throws IllegalStateException
Thumbnails.of(file)
    .scale(0.5)
    .crop(Positions.CENTER) // Throws IllegalStateException
    .toFile(outFile);

// GOOD: Use size() instead of scale() when cropping
Thumbnails.of(file)
    .size(200, 200)
    .crop(Positions.CENTER)
    .toFile(outFile);
```

## API Test: `defaultImageType`

### Signature
```java
public ThumbnailMaker defaultImageType()
```
_Source: source/src/main/java/net/coobird/thumbnailator/makers/ThumbnailMaker.java:240_

_Source doc:_ Sets the type of the {@link BufferedImage} to be the default type. @return				A reference to this object.

### Goal
Configures the `ThumbnailMaker` to output the generated thumbnail using the library's default `BufferedImage` type (typically `ThumbnailParameter.DEFAULT_IMAGE_TYPE`, which corresponds to `BufferedImage.TYPE_INT_ARGB`).

### Parameters
_None._

### Input
A valid, instantiated `ThumbnailMaker` (or one of its concrete subclasses, such as `FixedSizeThumbnailMaker` or `ScaledThumbnailMaker`) that is currently being configured before executing the image transformation.

### Output
Returns `ThumbnailMaker` — A reference to the current `ThumbnailMaker` instance, enabling fluent method chaining.

### Valid Call Patterns
```java
// Inferred from signature (not verified)
// Assuming 'maker' is an instantiated subclass of ThumbnailMaker and 'sourceImage' is a BufferedImage
maker.defaultImageType()
     .make(sourceImage);
```

### LLM Instruction Prompt
- Use `defaultImageType()` when working directly with the lower-level `ThumbnailMaker` API to explicitly reset or enforce the output image type to the library's default.
- Do not confuse this with the higher-level `Thumbnails.Builder` API, which uses `imageType(int)` instead.
- Remember that this method returns the `ThumbnailMaker` instance itself for fluent chaining, not the generated `BufferedImage`.

### Prompt Snippet
```text
`ThumbnailMaker.defaultImageType()` configures the maker to use the default `BufferedImage` type (TYPE_INT_ARGB) for the output image. It takes no parameters and returns the `ThumbnailMaker` instance for fluent chaining. Use this when building custom thumbnail tasks outside the standard `Thumbnails.of(...)` pipeline.
```

### Common Failure Modes
- **Type Mismatch on Return**: Attempting to assign the result of `defaultImageType()` directly to a `BufferedImage`. The method returns the builder/maker instance, not the image.
- **API Confusion**: Attempting to call `defaultImageType()` on a `Thumbnails.Builder` instance. This method is exclusive to the `ThumbnailMaker` class hierarchy.

### Fix Code Hint
```java
// Incorrect: Assigning the builder method to an image
// BufferedImage thumbnail = maker.defaultImageType();

// Correct: Chaining the configuration before calling make()
BufferedImage thumbnail = maker.defaultImageType().make(sourceImage);
```

## API Test: `defaultResizer`

### Signature
```java
public ThumbnailMaker defaultResizer()
```
_Source: source/src/main/java/net/coobird/thumbnailator/makers/ThumbnailMaker.java:263_

_Source doc:_ Sets the {@link Resizer} to use the default {@link Resizer}. @return				A reference to this object.

### Goal
Sets the image scaling algorithm used by the `ThumbnailMaker` to the library's default `Resizer` implementation.

### Parameters
_None._

### Input
The caller must invoke this method on an existing, non-null `ThumbnailMaker` instance. No arguments are required.

### Output
Returns `ThumbnailMaker` — A reference to the current `ThumbnailMaker` object, allowing for fluent method chaining.

### Valid Call Patterns
```java
// Inferred from signature (no verified test or README example provided)
thumbnailMaker.defaultResizer();
```

### LLM Instruction Prompt
- When configuring a `ThumbnailMaker` instance, call `defaultResizer()` to explicitly assign the default `Resizer` implementation for the scaling algorithm. 
- Utilize the return value to chain subsequent configuration methods, as it returns the same `ThumbnailMaker` instance.
- Do not confuse `ThumbnailMaker` with the primary `Thumbnails.Builder` fluent interface; this method specifically belongs to the `ThumbnailMaker` class.

### Prompt Snippet
```text
To explicitly use the default resizing algorithm in a custom `ThumbnailMaker` pipeline, call `thumbnailMaker.defaultResizer()` without arguments.
```

### Common Failure Modes
- **`NullPointerException`**: Attempting to call `defaultResizer()` on an uninitialized `ThumbnailMaker` reference.
- **Type Mismatch**: Attempting to call this method directly on a `Thumbnails.Builder` object instead of a `ThumbnailMaker` instance.

### Fix Code Hint
```java
// Ensure the ThumbnailMaker is instantiated before calling
if (thumbnailMaker != null) {
    thumbnailMaker.defaultResizer();
}
```

## API Test: `defaultResizerFactory`

### Signature
```java
public ThumbnailMaker defaultResizerFactory()
```
_Source: source/src/main/java/net/coobird/thumbnailator/makers/ThumbnailMaker.java:290_

_Source doc:_ Sets the {@link ResizerFactory} to use {@link DefaultResizerFactory}. @return				A reference to this object. @since	0.4.0

### Goal
Configures the `ThumbnailMaker` to use the `DefaultResizerFactory` for determining the appropriate image scaling algorithm.

### Parameters
_None._

### Input
An existing, instantiated `ThumbnailMaker` object on which to invoke the method. No arguments are required.

### Output
Returns `ThumbnailMaker` — A reference to the current `ThumbnailMaker` instance, allowing for fluent method chaining.

### Valid Call Patterns
```java
// Inferred from signature (not verified)
thumbnailMaker.defaultResizerFactory();
```

### LLM Instruction Prompt
- When configuring a `ThumbnailMaker` pipeline and you need to explicitly reset or ensure the use of the default resizing algorithms, call `defaultResizerFactory()`.
- Do not pass any arguments to this method.
- Utilize the return value to chain additional configuration methods on the `ThumbnailMaker`.

### Prompt Snippet
```text
To explicitly use the default resizing algorithms in a `ThumbnailMaker`, call `defaultResizerFactory()` with no arguments. It returns the `ThumbnailMaker` instance for method chaining.
```

### Common Failure Modes
- **Providing arguments**: Attempting to pass a specific `Resizer` or `ResizerFactory` instance into this method will cause a compilation error, as it takes no parameters.
- **Null reference**: Calling this method on an uninitialized `ThumbnailMaker` variable will result in a `NullPointerException`.

### Fix Code Hint
```java
// Incorrect: thumbnailMaker.defaultResizerFactory(new CustomResizerFactory());
// Correct:
thumbnailMaker.defaultResizerFactory();
```

## API Test: `determineOutputFormat`

### Signature
```java
public Builder<T> determineOutputFormat()
```
_Source: source/src/main/java/net/coobird/thumbnailator/Thumbnails.java:1720_

_Source doc:_ Indicates that the output format should be determined from the available information when writing the thumbnail image. <p> For example, calling this method will cause the output format to be determined from the file extension if thumbnails are written to files. <p> Calling this method multiple times will result in an {@link IllegalStateException} to be thrown. @return				Reference to this object. @since	0.4.0

### Goal
Instructs the builder to automatically infer the output image format from the destination's available information, such as the output file's extension.

### Parameters
_None._

### Input
An active `Thumbnails.Builder` pipeline where the terminal sink (e.g., `toFile(File)` or `toFiles(Rename)`) provides context, such as a file extension, that the underlying Java Image I/O can use to infer the format.

### Output
Returns `Builder<T>` — the current builder instance to allow fluent method chaining.

### Valid Call Patterns
```java
// given
File sourceFile = TestUtils.copyResourceToTemporaryFile(
        "Thumbnailator/grid.png", temporaryFolder
);
File destFile = new File(temporaryFolder.getRoot(), "dest.jpg");

// when
Thumbnails.of(sourceFile)
        .size(10, 10)
        .determineOutputFormat()
        .toFile(destFile);
```

### LLM Instruction Prompt
- Call `determineOutputFormat()` when writing thumbnails to files to automatically set the image format based on the destination file's extension (e.g., `.jpg`, `.png`).
- NEVER call this method multiple times on the same builder instance, as it will throw an `IllegalStateException`.
- Ensure the terminal sink provides a recognizable extension supported by the JVM's Image I/O; otherwise, an `UnsupportedFormatException` may be thrown.
- Do not use this method if writing to an `OutputStream` or in-memory `BufferedImage` where no file extension context is available.

### Prompt Snippet
```text
When writing thumbnails to files with specific extensions, use `.determineOutputFormat()` on the `Thumbnails.Builder` to automatically set the image format based on the destination file name. Do not call it more than once per pipeline.
```

### Common Failure Modes
- **`IllegalStateException`**: Thrown if `determineOutputFormat()` is called multiple times on the same `Thumbnails.Builder` instance.
- **`UnsupportedFormatException`**: Thrown if the inferred format (derived from the file extension) is not supported by the underlying Java Image I/O implementation.
- **Missing Context**: Using this method with a sink that lacks format information (like `toOutputStream(OutputStream)`) without explicitly setting the format elsewhere, which prevents the library from determining how to encode the image.

### Fix Code Hint
```java
// BAD: Calling determineOutputFormat() multiple times throws IllegalStateException
Thumbnails.of(sourceFile)
        .size(100, 100)
        .determineOutputFormat()
        .determineOutputFormat() 
        .toFile(new File("out.png"));

// GOOD: Call exactly once and ensure the destination file has a valid extension
Thumbnails.of(sourceFile)
        .size(100, 100)
        .determineOutputFormat()
        .toFile(new File("out.png"));
```

## API Test: `dithering`

### Signature
```java
public Builder<T> dithering(Dithering config)
```
_Source: source/src/main/java/net/coobird/thumbnailator/Thumbnails.java:1402_

_Source doc:_ Sets the dithering mode when performing the resizing operation to generate the thumbnail. <p> Calling this method to set this parameter is optional. <p> Calling this method multiple times will result in an {@link IllegalStateException} to be thrown. <p> This method cannot be called in conjunction with the {@link #resizerFactory(ResizerFactory)} method. @param config		The dithering mode. @return				Reference to this object.

### Goal
Sets the dithering mode rendering hint to be used during the image resizing operation in the thumbnail generation pipeline.

### Parameters
- `config` (`Dithering`): The dithering mode to apply (e.g., `Dithering.DEFAULT`, `Dithering.ENABLE`, `Dithering.DISABLE`).

### Input
A valid `Thumbnails.Builder` instance. The `config` argument must be a non-null `Dithering` enum value. 
**Preconditions:** 
1. `resizerFactory(ResizerFactory)` must not be called on this builder.
2. `dithering()` must not have been called previously on this builder instance.

### Output
Returns `Builder<T>` — a reference to the current fluent builder object to allow for method chaining.

### Valid Call Patterns
```java
// Applying dithering alongside a specific resizer
BufferedImage img = new BufferedImage(200, 200, BufferedImage.TYPE_INT_ARGB);
BufferedImage thumbnail = Thumbnails.of(img)
        .size(50, 50)
        .resizer(Resizers.PROGRESSIVE)
        .dithering(Dithering.DEFAULT)
        .asBufferedImage();
```

### LLM Instruction Prompt
- When applying dithering hints to a Thumbnailator pipeline, call `dithering(Dithering)` exactly once. Never pass `null`. Never combine this call with `resizerFactory(ResizerFactory)` on the same builder, as they are mutually exclusive.

### Prompt Snippet
```text
Use `.dithering(Dithering.DEFAULT)` or another valid `Dithering` enum value in the fluent chain. Do not call `dithering()` multiple times or alongside `resizerFactory()`.
```

### Common Failure Modes
- **`NullPointerException`**: Thrown with the message `"Dithering is null."` if the `config` argument is `null`.
- **`IllegalStateException`**: Thrown if `dithering()` is called multiple times on the same builder instance.
- **`IllegalStateException`**: Thrown if `dithering()` is called in conjunction with `resizerFactory(ResizerFactory)` on the same builder.

### Fix Code Hint
```java
// BAD: Passing null or calling multiple times
// Thumbnails.of(img).size(50, 50).dithering(null).asBufferedImage();
// Thumbnails.of(img).size(50, 50).dithering(Dithering.ENABLE).dithering(Dithering.DISABLE).asBufferedImage();

// GOOD: Call exactly once with a valid enum value
Thumbnails.of(img)
        .size(50, 50)
        .dithering(Dithering.DEFAULT)
        .asBufferedImage();
```

## API Test: `filters`

### Signature
```java
public ThumbnailParameterBuilder filters(List<ImageFilter> filters)
```
_Source: source/src/main/java/net/coobird/thumbnailator/builders/ThumbnailParameterBuilder.java:267_

_Source doc:_ Sets the {@link ImageFilter}s to apply to the thumbnail. <p> These filters will be applied after the original image is resized. @param filters		The output format type of the thumbnail. @return				A reference to this object.

### Goal
Sets a sequence of `ImageFilter` transformations to be applied to the image after the resizing step is complete.

### Parameters
- `filters` (`List<ImageFilter>`): A list of image filters (such as `Canvas`, `Caption`, `Colorize`, `Flip`, `Rotation`, `SwapDimensions`, `Transparency`, or `Watermark`) to apply sequentially to the thumbnail. *(Note: The original source Javadoc contains a typo referring to this as the "output format type", but it strictly accepts a list of filters).*

### Input
A valid `List` containing instantiated `ImageFilter` objects. The caller must be configuring a `ThumbnailParameterBuilder` (typically used in advanced workflows for constructing custom `ThumbnailTask` instances, rather than the standard `Thumbnails.of(...)` fluent API). 

### Output
Returns `ThumbnailParameterBuilder` — A reference to the current builder instance, allowing for fluent method chaining.

### Valid Call Patterns
```java
// Inferred from the signature (not verified by test suite)
ThumbnailParameterBuilder builder = new ThumbnailParameterBuilder();

List<ImageFilter> customFilters = Arrays.asList(
    new Rotation(90),
    new Watermark(Positions.BOTTOM_RIGHT, watermarkImage, 0.5f)
);

builder.filters(customFilters);
```

### LLM Instruction Prompt
- Use `filters(List<ImageFilter>)` when constructing a `ThumbnailParameterBuilder` to apply multiple transformations at once. 
- Remember that filters provided here are strictly applied **after** the original image is resized. 
- Do not confuse `ThumbnailParameterBuilder.filters(List)` with the standard fluent API's `Thumbnails.Builder.addFilter(ImageFilter)`. Use this method only when working directly with `ThumbnailParameterBuilder` in advanced task-abstraction workflows.

### Prompt Snippet
```text
When configuring a ThumbnailParameterBuilder, use `.filters(List<ImageFilter>)` to set the post-resize transformation pipeline. Note that these filters execute after resizing. For the standard `Thumbnails.of()` API, use `.addFilter()` instead.
```

### Common Failure Modes
- **Order of Operations Misconception**: Assuming the filters will be applied to the original, full-resolution image. The library explicitly applies these filters *after* the image has been resized.
- **API Confusion**: Attempting to call `.filters(List)` on a `Thumbnails.Builder` instance. The `Thumbnails.Builder` class uses `.addFilter(ImageFilter)` for adding filters one by one, whereas `.filters(List)` belongs to `ThumbnailParameterBuilder`.
- **Null Elements**: Passing a list that contains `null` elements may cause `NullPointerException`s during the pipeline execution when the library attempts to apply the transformations.

### Fix Code Hint
```java
// Incorrect: Trying to use filters(List) on the standard Thumbnails.Builder
// Thumbnails.of(file).size(100, 100).filters(myList); 

// Correct: Using addFilter on Thumbnails.Builder
Thumbnails.Builder<File> builder = Thumbnails.of(file).size(100, 100);
for (ImageFilter filter : myList) {
    builder.addFilter(filter);
}

// Correct: Using filters(List) on ThumbnailParameterBuilder
ThumbnailParameterBuilder paramBuilder = new ThumbnailParameterBuilder();
paramBuilder.size(100, 100).filters(myList);
```

## API Test: `fitWithinDimenions`

### Signature
```java
public boolean fitWithinDimenions()
```
_Source: source/src/main/java/net/coobird/thumbnailator/ThumbnailParameter.java:980_

_Source doc:_ Returns whether or not to fit the thumbnail within the specified dimensions. @return		{@code true} is returned when the thumbnail should be sized to fit within the specified dimensions, if the thumbnail is going to exceed those dimensions. @since	0.4.0

### Goal
Returns a boolean indicating whether the thumbnail is configured to be constrained entirely within the specified maximum dimensions.

### Parameters
_None._

### Input
An instantiated `ThumbnailParameter` object containing the configuration state for a thumbnail generation task.

### Output
Returns `boolean` — `true` if the thumbnail should be sized to fit within the specified dimensions (preventing it from exceeding them); `false` otherwise.

### Valid Call Patterns
```java
// Note: Example inferred from the signature (not verified by test suite or README)
ThumbnailParameter param = task.getParam(); // Obtained from a ThumbnailTask or similar context
boolean shouldFit = param.fitWithinDimenions();
```

### LLM Instruction Prompt
- You MUST use the exact spelling `fitWithinDimenions` (missing the 's' in "Dimensions") when calling this method on a `ThumbnailParameter` instance. Do not auto-correct the spelling to `fitWithinDimensions`, as it will cause a compilation failure.
- Use this method to inspect the configuration state of a thumbnail task, typically when building custom `ThumbnailTask` implementations or debugging pipeline parameters.

### Prompt Snippet
```text
When checking if a `ThumbnailParameter` enforces dimension constraints, call `fitWithinDimenions()`. Note the exact spelling (missing the 's' in Dimensions) to avoid `NoSuchMethodError` or compilation failures.
```

### Common Failure Modes
- **Compilation Error (Typo Correction)**: An LLM or developer might instinctively type `fitWithinDimensions()` (with the 's'). This method does not exist and will fail to compile. You must use the exact spelling `fitWithinDimenions()`.
- **NullPointerException**: Calling this method on a null `ThumbnailParameter` reference will throw an exception. Ensure the parameter object is properly initialized or retrieved from a valid task.

### Fix Code Hint
```java
// WRONG: Will not compile due to auto-corrected spelling
// boolean fit = param.fitWithinDimensions();

// CORRECT: Use the exact spelling from the API signature
boolean fit = param.fitWithinDimenions();
```

## API Test: `fitWithinDimensions`

### Signature
```java
public ThumbnailParameterBuilder fitWithinDimensions(boolean fit)
public FixedSizeThumbnailMaker fitWithinDimensions(boolean fit)
```
_Source: source/src/main/java/net/coobird/thumbnailator/builders/ThumbnailParameterBuilder.java:330  (+1 more definition site/overload)_

_Source doc:_ Sets whether or not the thumbnail should fit within the specified dimensions. @param fit		{@code true} if the thumbnail should be sized to fit within the specified dimensions, if the thumbnail is going to exceed those dimensions. @return			A reference to this object. @since	0.4.0

### Goal
Sets whether the generated thumbnail must be constrained to fit entirely within the specified target dimensions without exceeding them.

### Parameters
- `fit` (`boolean`): `true` if the thumbnail should be sized to fit strictly within the specified dimensions (preventing it from exceeding those bounds); `false` otherwise.

### Input
A boolean flag indicating the desired fitting behavior. This method is called on an active `ThumbnailParameterBuilder` or `FixedSizeThumbnailMaker` instance during the configuration phase of an image processing pipeline, prior to invoking a terminal execution method (like `make()`).

### Output
Returns `ThumbnailParameterBuilder` (or `FixedSizeThumbnailMaker` for the overload) — A reference to the current builder or maker object, allowing for fluent method chaining.

### Valid Call Patterns
```java
// Using FixedSizeThumbnailMaker to constrain an image within 100x100 bounds
BufferedImage img = makeTestImage200x200(); // Example in-memory image

BufferedImage thumbnail = new FixedSizeThumbnailMaker(100, 100)
        .keepAspectRatio(true)
        .fitWithinDimensions(true)
        .make(img);
```

### LLM Instruction Prompt
- When configuring a `FixedSizeThumbnailMaker` or `ThumbnailParameterBuilder`, use `.fitWithinDimensions(true)` to guarantee the resulting thumbnail does not exceed the specified target width and height bounds.
- Chain this method fluently before calling the terminal `.make(BufferedImage)` method.
- Often used in conjunction with `.keepAspectRatio(true)` to ensure the image scales down proportionally without clipping or stretching outside the bounding box.

### Prompt Snippet
```text
To ensure the resized image strictly fits inside a bounding box without exceeding the target width or height, chain `.fitWithinDimensions(true)` on your `FixedSizeThumbnailMaker` before calling `.make(image)`.
```

### Common Failure Modes
- **Missing Terminal Operation**: Calling `.fitWithinDimensions(true)` configures the builder but does not process the image. A terminal method like `.make(BufferedImage)` must be invoked to actually generate the thumbnail.
- **Conflicting Size Constraints**: Using this method while simultaneously forcing an exact size (e.g., via `forceSize` in the broader `Thumbnails` API) can lead to unexpected results if the aspect ratio and fit constraints contradict the forced dimensions.

### Fix Code Hint
```java
// Incorrect: Forgetting the terminal operation
FixedSizeThumbnailMaker maker = new FixedSizeThumbnailMaker(100, 100).fitWithinDimensions(true);
// maker does not contain the image data yet

// Correct: Chain the configuration and execute with make()
BufferedImage thumbnail = new FixedSizeThumbnailMaker(100, 100)
        .keepAspectRatio(true)
        .fitWithinDimensions(true)
        .make(originalImage);
```

## API Test: `forceSize`

### Signature
```java
public Builder<T> forceSize(int width, int height)
```
_Source: source/src/main/java/net/coobird/thumbnailator/Thumbnails.java:940_

_Source doc:_ Sets the size of the thumbnail. <p> The thumbnails will be forced to the specified size, therefore, the aspect ratio of the original image will not be preserved in the thumbnails. Calling this method will be equivalent to calling the {@link #size(int, int)} method in conjunction with the {@link #keepAspectRatio(boolean)} method with the value {@code false}. <p> Once this method is called, calling the {@link #scale(double)} method will result in an {@link IllegalStateException}. <p> Calling this method multiple times will result in an {@link IllegalStateException} to be thrown. @param width			The width of the thumbnail. @param height		The height of the thumbnail. @return				Reference to this object. @since 	0.3.2

### Goal
Sets the exact dimensions of the generated thumbnail, forcing the output to the specified width and height without preserving the original image's aspect ratio.

### Parameters
- `width` (`int`): The exact width of the resulting thumbnail in pixels.
- `height` (`int`): The exact height of the resulting thumbnail in pixels.

### Input
A `Thumbnails.Builder` instance initialized with an image source (e.g., `BufferedImage`, `File`, `InputStream`). The caller must not have previously called `size()`, `scale()`, or `forceSize()` on this builder instance.

### Output
Returns `Builder<T>` — A reference to the current `Thumbnails.Builder` object to allow method chaining in the fluent pipeline.

### Valid Call Patterns
```java
// Resizing an in-memory image to exact dimensions, ignoring aspect ratio
BufferedImage img = new BufferedImageBuilder(200, 200).build();

BufferedImage thumbnail = Thumbnails.of(img)
        .forceSize(50, 50)
        .asBufferedImage();
```

### LLM Instruction Prompt
- Use `forceSize(width, height)` when the exact output dimensions are strictly required and aspect ratio preservation is explicitly not wanted.
- Do not call `forceSize()` multiple times on the same builder instance.
- Do not combine `forceSize()` with `scale()` or `size()` in the same pipeline.
- If aspect ratio preservation is required, use `size(width, height)` instead.

### Prompt Snippet
```text
Use `forceSize(width, height)` to resize an image to exact dimensions, ignoring the original aspect ratio. Never chain multiple `forceSize()`, `size()`, or `scale()` calls on the same `Thumbnails.Builder` instance, as this will throw an `IllegalStateException`.
```

### Common Failure Modes
- **`IllegalStateException` (Multiple sizing calls)**: Calling `forceSize()` multiple times on the same builder (e.g., `Thumbnails.of(img).forceSize(50, 50).forceSize(50, 50)`) will throw an exception.
- **`IllegalStateException` (Conflicting scaling calls)**: Calling `scale(double)` after `forceSize()` has been called on the builder will result in an exception.

### Fix Code Hint
```java
// BAD: Chaining multiple sizing methods throws IllegalStateException
Thumbnails.of(img)
    .forceSize(100, 100)
    .scale(0.5) // Throws IllegalStateException
    .asBufferedImage();

// GOOD: Use only one sizing method per pipeline
Thumbnails.of(img)
    .forceSize(50, 50)
    .asBufferedImage();
```

## API Test: `format`

### Signature
```java
public ThumbnailParameterBuilder format(String format)
```
_Source: source/src/main/java/net/coobird/thumbnailator/builders/ThumbnailParameterBuilder.java:243_

_Source doc:_ Sets the output format of the thumbnail. @param format		The output format of the thumbnail. @return				A reference to this object.

### Goal
Sets the desired image output format (such as "jpg" or "png") for the thumbnail generation parameters.

### Parameters
- `format` (`String`): The output format of the thumbnail (e.g., "jpg", "png", "gif"), or the constant `ThumbnailParameter.DETERMINE_FORMAT` ("\0") to infer the format automatically.

### Input
A string representing an image format that is supported by the host JVM's standard Image I/O capabilities. The library relies entirely on the underlying Java Image I/O for format support.

### Output
Returns `ThumbnailParameterBuilder` — A reference to this builder object to allow fluent method chaining.

### Valid Call Patterns
```java
// Inferred from the signature (not verified by test suite examples)
ThumbnailParameterBuilder builder = new ThumbnailParameterBuilder();
builder.format("jpg");

// Using the constant to determine format automatically
builder.format(ThumbnailParameter.DETERMINE_FORMAT);
```

### LLM Instruction Prompt
- When configuring a `ThumbnailParameterBuilder`, use `format(String)` to specify the output image format. Ensure the provided string is a valid format supported by the JVM's Image I/O (e.g., "jpg", "png"). Do not confuse this method with `Thumbnails.Builder.outputFormat(String)`, which is used in the primary fluent API workflow.

### Prompt Snippet
```text
To set the output format on a ThumbnailParameterBuilder, call `format("jpg")` or `format("png")`. The format must be supported by the host JVM's Image I/O. To let the library infer the format, pass `ThumbnailParameter.DETERMINE_FORMAT` ("\0").
```

### Common Failure Modes
- **Unsupported Format**: Providing a format string that the underlying Java Image I/O does not support will result in an `UnsupportedFormatException` when the pipeline attempts to write the image.
- **API Confusion**: Attempting to call `format(String)` on a `Thumbnails.Builder` instead of a `ThumbnailParameterBuilder`. The main fluent entry point (`Thumbnails.Builder`) uses `outputFormat(String)` instead.

### Fix Code Hint
```java
// Correct usage on a ThumbnailParameterBuilder
ThumbnailParameterBuilder paramBuilder = new ThumbnailParameterBuilder();
paramBuilder.format("png"); // Ensure the format is supported by Java Image I/O
```

## API Test: `formatType`

### Signature
```java
public ThumbnailParameterBuilder formatType(String formatType)
```
_Source: source/src/main/java/net/coobird/thumbnailator/builders/ThumbnailParameterBuilder.java:254_

_Source doc:_ Sets the output format type of the thumbnail. @param formatType	The output format type of the thumbnail. @return				A reference to this object.

### Goal
Sets the specific output format type for the thumbnail being configured within the parameter builder.

### Parameters
- `formatType` (`String`): The output format type of the thumbnail (e.g., a specific compression type or sub-format recognized by the underlying Java Image I/O writer).

### Input
A valid `String` representing the desired format type. The caller must have an instantiated `ThumbnailParameterBuilder` to invoke this method. The provided format type must be supported by the host JVM's standard Image I/O capabilities for the target output format.

### Output
Returns `ThumbnailParameterBuilder` — A reference to this builder object to facilitate fluent method chaining.

### Valid Call Patterns
```java
// Inferred from the signature (not verified by existing tests or original README)
ThumbnailParameterBuilder builder = new ThumbnailParameterBuilder();
builder.formatType("JPEG");
```

### LLM Instruction Prompt
- Use `formatType(String)` only when working directly with a `ThumbnailParameterBuilder` to specify the output format type.
- Do not confuse this with the `outputFormat(String)` method found on the primary `Thumbnails.Builder` fluent interface.
- Chain this method with other `ThumbnailParameterBuilder` configuration methods, as it returns the builder instance.

### Prompt Snippet
```text
When building custom `ThumbnailParameter` objects via `ThumbnailParameterBuilder`, use `builder.formatType(String)` to set the output format type. It returns the builder for fluent chaining. Ensure the format type is supported by the JVM's Image I/O.
```

### Common Failure Modes
- **Unsupported Format Type**: Providing a format type string that the underlying Java Image I/O implementation does not support, which may result in an `UnsupportedFormatException` or the setting being ignored during rendering.
- **Receiver Type Mismatch**: Attempting to call `formatType(String)` directly on the main `Thumbnails.Builder` instead of `ThumbnailParameterBuilder`.

### Fix Code Hint
```java
// Ensure you are operating on a ThumbnailParameterBuilder, not Thumbnails.Builder
ThumbnailParameterBuilder paramBuilder = new ThumbnailParameterBuilder();
paramBuilder.formatType("JPEG"); // Use a format type supported by Java Image I/O
```

## API Test: `fromFilenames`

### Signature
```java
public static Builder<File> fromFilenames(Iterable<String> files)
```
_Source: source/src/main/java/net/coobird/thumbnailator/Thumbnails.java:292_

_Source doc:_ Indicate to make thumbnails for images with the specified filenames. @param files		File names of image files for which thumbnails are to be produced for. @return			Reference to a builder object which is used to specify the parameters for creating the thumbnail. @throws NullPointerException		If the argument is {@code null}. @throws IllegalArgumentException	If the argument is an empty collection. @since 	0.3.1

### Goal
Initializes a fluent image processing pipeline using a collection of file paths (strings) as the source images.

### Parameters
- `files` (`Iterable<String>`): A collection of strings representing the file paths of the source images to be processed.

### Input
An `Iterable` (such as a `List` or `Set`) containing one or more valid file path strings pointing to existing image files. The collection must not be `null` and must not be empty. The underlying image formats must be supported by the host JVM's standard Image I/O capabilities.

### Output
Returns `Builder<File>` — A fluent builder instance configured with the specified files as image sources, ready to accept transformation parameters (like `size()`, `crop()`, or `rotate()`) and a terminal sink operation (like `toFile()`, `toFiles()`, or `asBufferedImages()`).

### Valid Call Patterns
```java
// Single file path processing
String f = "path/to/grid.png";
File outFile = new File("path/to/grid.tmp.png");

Thumbnails.fromFilenames(Arrays.asList(f))
        .size(50, 50)
        .toFile(outFile);

// Multiple file paths processing (requires a Rename strategy for output)
List<String> filePaths = Arrays.asList("image1.jpg", "image2.jpg");

Thumbnails.fromFilenames(filePaths)
        .size(640, 480)
        .toFiles(Rename.PREFIX_DOT_THUMBNAIL);
```

### LLM Instruction Prompt
- When calling `Thumbnails.fromFilenames`, ensure the argument is a non-null, non-empty `Iterable<String>`. 
- If processing multiple files, the terminal operation must handle batch outputs (e.g., `toFiles(Rename)` or `asFiles(Rename)`) to avoid filename collisions. Do not use the single-file `toFile(File)` sink when providing multiple filenames.
- Always use the static factory method on the `Thumbnails` class (i.e., `Thumbnails.fromFilenames(...)`).

### Prompt Snippet
```text
Thumbnails.fromFilenames(Arrays.asList(filePath)).size(w, h).toFile(outFile);
```

### Common Failure Modes
- **`NullPointerException`**: Thrown immediately if the `files` argument is `null`.
- **`IllegalArgumentException`**: Thrown immediately if the `files` collection is empty.
- **Batch Output Collision**: Calling a single-output terminal method like `toFile(File)` or `toOutputStream(OutputStream)` when the builder was initialized with multiple filenames will cause an exception during execution.
- **`UnsupportedFormatException`**: Thrown during pipeline execution if the underlying Java Image I/O does not support reading the format of the provided files.

### Fix Code Hint
```java
// FIX: Ensure the collection is not empty and use a batch sink for multiple files
if (filePaths != null && !filePaths.isEmpty()) {
    Thumbnails.fromFilenames(filePaths)
            .size(200, 200)
            .toFiles(Rename.PREFIX_DOT_THUMBNAIL); // Use toFiles with Rename for batch processing
}
```

## API Test: `fromFiles`

### Signature
```java
public static Builder<File> fromFiles(Iterable<File> files)
```
_Source: source/src/main/java/net/coobird/thumbnailator/Thumbnails.java:309_

_Source doc:_ Indicate to make thumbnails from the specified {@link File}s. @param files		{@link File} objects of image files for which thumbnails are to be produced for. @return			Reference to a builder object which is used to specify the parameters for creating the thumbnail. @throws NullPointerException		If the argument is {@code null}. @throws IllegalArgumentException	If the argument is an empty collection. @since 	0.3.1

### Goal
Initialize a fluent thumbnail generation pipeline from a collection of source image files.

### Parameters
- `files` (`Iterable<File>`): A collection of `File` objects representing the source images for which thumbnails are to be produced.

### Input
The caller must provide a non-null, non-empty `Iterable` of `java.io.File` objects. The files must exist on the filesystem and contain image data in a format supported by the host JVM's standard Image I/O capabilities (e.g., JPEG, PNG). 

### Output
Returns `Builder<File>` — A fluent builder instance configured with the provided files as image sources, allowing the caller to chain transformations (e.g., `size()`, `crop()`) and terminal output operations (e.g., `toFiles()`, `asFiles()`).

### Valid Call Patterns
```java
// Example 1: Processing multiple files and returning a list of the generated thumbnail files
List<File> sources = Arrays.asList(new File("image1.jpg"), new File("image2.jpg"));
List<File> results = Thumbnails.fromFiles(sources)
        .size(100, 100)
        .asFiles(Rename.PREFIX_DOT_THUMBNAIL);

// Example 2: Processing multiple files and writing them directly to disk without returning a list
Thumbnails.fromFiles(sources)
        .size(100, 100)
        .toFiles(Rename.PREFIX_DOT_THUMBNAIL);
```

### LLM Instruction Prompt
- Always verify that the `Iterable<File>` is neither `null` nor empty before calling `fromFiles`, as it will throw an exception immediately upon invocation.
- When using `fromFiles` for batch processing and outputting back to files via `toFiles()` or `asFiles()`, you MUST provide a `Rename` strategy (e.g., `Rename.PREFIX_DOT_THUMBNAIL`) or an instance of `ConsecutivelyNumberedFilenames` to prevent filename collisions and accidental overwrites.
- Use `Thumbnails.fromFiles(Iterable)` as the strictly preferred paradigm over the deprecated legacy method `Thumbnailator.createThumbnailsAsCollection`.

### Prompt Snippet
```text
When processing multiple files with `Thumbnails.fromFiles(Iterable<File>)`, ensure the collection is not empty and always terminate the pipeline with a collision-safe output strategy like `toFiles(Rename.PREFIX_DOT_THUMBNAIL)`.
```

### Common Failure Modes
- **`NullPointerException`**: Thrown immediately if the `files` argument is `null`.
- **`IllegalArgumentException`**: Thrown immediately if the `files` argument is an empty collection.
- **Filename Collisions**: If the pipeline is terminated with a file output method but no `Rename` strategy is provided, the batch process may overwrite files or fail.
- **`UnsupportedFormatException`**: Thrown during pipeline execution (at the terminal step) if one of the files is in a format that the underlying Java Image I/O does not support.

### Fix Code Hint
```java
// Safely check for null and empty collections before initializing the builder
if (sources != null && !sources.isEmpty()) {
    Thumbnails.fromFiles(sources)
            .size(200, 200)
            // Use a Rename strategy to safely output batch files without collisions
            .toFiles(Rename.PREFIX_DOT_THUMBNAIL); 
}
```

## API Test: `fromImages`

### Signature
```java
public static Builder<BufferedImage> fromImages(Iterable<BufferedImage> images)
```
_Source: source/src/main/java/net/coobird/thumbnailator/Thumbnails.java:364_

_Source doc:_ Indicate to make thumbnails from the specified {@link BufferedImage}s. @param images	{@link BufferedImage}s for which thumbnails are to be produced for. @return			Reference to a builder object which is used to specify the parameters for creating the thumbnail. @throws NullPointerException		If the argument is {@code null}. @throws IllegalArgumentException	If the argument is an empty collection. @since 	0.3.1

### Goal
Initialize a fluent thumbnail generation pipeline using a collection of in-memory `BufferedImage` objects as the source.

### Parameters
- `images` (`Iterable<BufferedImage>`): A collection of one or more in-memory `BufferedImage` instances that will be processed by the pipeline.

### Input
An `Iterable` containing `BufferedImage` objects. The collection must not be `null` and must not be empty. Because the inputs are already decoded into memory, no file I/O or format parsing preconditions apply at this stage.

### Output
Returns `Builder<BufferedImage>` — A fluent builder object used to configure image transformations (such as resizing, cropping, or rotating) and to route the processed images to a designated sink (like a list, file, or stream).

### Valid Call Patterns
```java
// Processing a single in-memory image
BufferedImage img = new BufferedImage(200, 200, BufferedImage.TYPE_INT_ARGB);

BufferedImage thumbnail = Thumbnails.fromImages(Arrays.asList(img))
    .size(100, 100)
    .asBufferedImage();

// Processing multiple in-memory images
List<BufferedImage> thumbnails = Thumbnails.fromImages(Arrays.asList(img, img))
    .size(100, 100)
    .asBufferedImages();
```

### LLM Instruction Prompt
- Use `Thumbnails.fromImages(Iterable<BufferedImage>)` to start a processing pipeline from existing in-memory images.
- Never pass a `null` or empty collection to this method.
- If the `Iterable` contains multiple images, you MUST terminate the pipeline with a batch sink like `asBufferedImages()` or `toFiles(...)`. Calling the singular `asBufferedImage()` on a multi-image pipeline will throw an `IllegalArgumentException`.

### Prompt Snippet
```text
To process in-memory `BufferedImage` objects, use `Thumbnails.fromImages(Iterable<BufferedImage>)`. Ensure the collection is not null or empty. If processing multiple images, terminate the builder with `asBufferedImages()` or a batch file sink, as calling `asBufferedImage()` will fail.
```

### Common Failure Modes
- **`NullPointerException`**: Thrown immediately if the `images` argument is `null`.
- **`IllegalArgumentException` (Empty Collection)**: Thrown immediately if the provided `Iterable` contains no elements.
- **`IllegalArgumentException` (Sink Mismatch)**: Thrown at the end of the pipeline if `asBufferedImage()` is called on a builder initialized with multiple images (error message: "Cannot create one thumbnail from multiple original images.").

### Fix Code Hint
```java
// Incorrect: Attempting to extract a single image from a multi-image pipeline
// Thumbnails.fromImages(Arrays.asList(img1, img2)).size(100, 100).asBufferedImage();

// Correct: Use asBufferedImages() to return a List<BufferedImage>
List<BufferedImage> thumbnails = Thumbnails.fromImages(Arrays.asList(img1, img2))
    .size(100, 100)
    .asBufferedImages();
```

## API Test: `fromInputStreams`

### Signature
```java
public static Builder<InputStream> fromInputStreams(Iterable<? extends InputStream> inputStreams)
```
_Source: source/src/main/java/net/coobird/thumbnailator/Thumbnails.java:347_

_Source doc:_ Indicate to make thumbnails for images obtained from the specified {@link InputStream}s. <p> Note that the {@link InputStream#close()} method will not be called upon reading the source image from the {@link InputStream}. @param inputStreams		{@link InputStream}s which provide images for which thumbnails are to be produced. @return			Reference to a builder object which is used to specify the parameters for creating the thumbnail. @throws NullPointerException		If the argument is {@code null}. @throws IllegalArgumentException	If the argument is an empty collection. @since 	0.3.1

### Goal
Initialize a fluent thumbnail processing pipeline using a collection of `InputStream` objects as the image sources.

### Parameters
- `inputStreams` (`Iterable<? extends InputStream>`): A collection of input streams providing the source images to be processed.

### Input
- Must be a non-null, non-empty `Iterable` containing one or more `InputStream` objects.
- The streams must provide image data in a format supported by the host JVM's standard Image I/O capabilities.
- **Precondition**: The caller is strictly responsible for managing the lifecycle of the `InputStream`s. Thumbnailator will *not* call `close()` on the streams after reading the source images.

### Output
Returns `Builder<InputStream>` — A reference to a fluent builder object used to configure resizing, filtering, and output parameters for the thumbnail pipeline.

### Valid Call Patterns
```java
// Single stream to a single BufferedImage
InputStream is = TestUtils.getResourceStream("Thumbnailator/grid.png");
try {
    BufferedImage thumbnail = Thumbnails.fromInputStreams(Arrays.asList(is))
        .size(100, 100)
        .asBufferedImage();
} finally {
    is.close(); // Caller must close the stream
}
```

### LLM Instruction Prompt
- Use `Thumbnails.fromInputStreams(Iterable)` to start a pipeline from one or more input streams.
- You MUST manually close the `InputStream`s (e.g., using a `try-with-resources` block or a `finally` block) because Thumbnailator explicitly does not close them after reading.
- If the `Iterable` contains multiple streams, you MUST use a batch output method (like `asBufferedImages()` or `toFiles()`). Calling a singular output method like `asBufferedImage()` on a multi-stream pipeline will throw an `IllegalArgumentException`.
- Ensure the `Iterable` is neither `null` nor empty.

### Prompt Snippet
```text
When using `Thumbnails.fromInputStreams(Iterable)`, remember that the library does not close the streams; you must handle closing them yourself. Additionally, if passing multiple streams, you must use a batch output method like `asBufferedImages()` or `toFiles()`. Calling `asBufferedImage()` with multiple input streams will fail.
```

### Common Failure Modes
- **`NullPointerException`**: Thrown if the `inputStreams` argument is `null`.
- **`IllegalArgumentException` (Empty Collection)**: Thrown if the `inputStreams` argument is an empty collection.
- **`IllegalArgumentException` (Multiple Inputs to Singular Output)**: Thrown if `asBufferedImage()` is called on the builder when the `Iterable` contains more than one stream (Message: "Cannot create one thumbnail from multiple original images.").
- **Resource Leaks**: Occur if the caller assumes the library closes the streams and fails to close them manually.

### Fix Code Hint
```java
// WRONG: Fails to close streams and attempts singular output for multiple inputs
Thumbnails.fromInputStreams(Arrays.asList(stream1, stream2))
    .size(100, 100)
    .asBufferedImage(); 

// RIGHT: Manages resources and uses batch output for multiple inputs
try (InputStream is1 = getStream1(); InputStream is2 = getStream2()) {
    List<BufferedImage> thumbnails = Thumbnails.fromInputStreams(Arrays.asList(is1, is2))
        .size(100, 100)
        .asBufferedImages();
}
```

## API Test: `fromURLs`

### Signature
```java
public static Builder<URL> fromURLs(Iterable<URL> urls)
```
_Source: source/src/main/java/net/coobird/thumbnailator/Thumbnails.java:326_

_Source doc:_ Indicate to make thumbnails for images with the specified {@link URL}s. @param urls		URLs of the images for which thumbnails are to be produced. @return			Reference to a builder object which is used to specify the parameters for creating the thumbnail. @throws NullPointerException		If the argument is {@code null}. @throws IllegalArgumentException	If the argument is an empty collection. @since 	0.3.1

### Goal
Initialize a fluent thumbnail processing pipeline using a collection of image URLs as the source.

### Parameters
- `urls` (`Iterable<URL>`): A collection of `java.net.URL` objects pointing to the source images to be processed.

### Input
- The `urls` argument must be a non-null, non-empty `Iterable`.
- The URLs must point to valid image formats supported by the host JVM's standard Image I/O (e.g., JPEG, PNG).
- **Environment Precondition**: Because the execution environment prohibits network access, the URLs must point to local resources (e.g., `file://` protocols or classpath resources via `TestUtils.getResource(...)`).

### Output
Returns `Builder<URL>` — A fluent builder instance used to configure image transformations (such as `size`, `crop`, `rotate`) and route the processed images to a terminal sink (like files, streams, or memory).

### Valid Call Patterns
```java
// Processing a single URL into an in-memory BufferedImage
URL url = TestUtils.getResource("Thumbnailator/grid.png");

BufferedImage thumbnail = Thumbnails.fromURLs(Arrays.asList(url))
    .size(100, 100)
    .asBufferedImage();
```

### LLM Instruction Prompt
- Always pass a non-null, non-empty `Iterable<URL>` to `fromURLs`.
- **Sink Selection Rule**: If the `Iterable` contains exactly one URL, you may use the singular terminal operation `asBufferedImage()`. If the `Iterable` contains multiple URLs, you **must** use a batch terminal operation such as `asBufferedImages()` or `toFiles()`. Calling a singular sink on a multi-image builder will throw an `IllegalArgumentException`.
- Ensure URLs point to local or classpath resources to comply with the no-network constraint.

### Prompt Snippet
```text
When using `Thumbnails.fromURLs(Iterable<URL>)`, the collection must not be null or empty. If processing multiple URLs, you must route the output to a batch sink like `asBufferedImages()` or `toFiles(Rename)`. Calling `asBufferedImage()` on a multi-URL builder throws an IllegalArgumentException ("Cannot create one thumbnail from multiple original images.").
```

### Common Failure Modes
- **`NullPointerException`**: Thrown if the `urls` argument is `null`.
- **`IllegalArgumentException`**: Thrown if the `urls` collection is empty.
- **`IllegalArgumentException`**: Thrown at the end of the pipeline if `asBufferedImage()` is called but the `urls` collection contains more than one item.
- **`UnsupportedFormatException`**: Thrown if a URL points to an image format that the underlying Java Image I/O does not support.

### Fix Code Hint
```java
// INCORRECT: Attempting to extract a single BufferedImage from multiple URLs
// Thumbnails.fromURLs(Arrays.asList(url1, url2)).size(100, 100).asBufferedImage();

// CORRECT: Use a batch sink (asBufferedImages) for multiple URLs
List<BufferedImage> thumbnails = Thumbnails.fromURLs(Arrays.asList(url1, url2))
    .size(100, 100)
    .asBufferedImages();
```

## API Test: `getAlpha`

### Signature
```java
public float getAlpha()
```
_Source: source/src/main/java/net/coobird/thumbnailator/filters/Transparency.java:113_

_Source doc:_ Returns the opacity of this filter. @return		The opacity in the range of {@code 0.0f} (transparent) to {@code 1.0f} (opaque).

### Goal
Retrieves the configured opacity level of a `Transparency` image filter.

### Parameters
_None._

### Input
An instantiated `Transparency` filter object (which implements `ImageFilter`).

### Output
Returns `float` — The opacity value configured for the filter, strictly in the range of `0.0f` (completely transparent) to `1.0f` (completely opaque).

### Valid Call Patterns
```java
// Example inferred from the signature (not verified)
float opacity = transparencyFilter.getAlpha();
```

### LLM Instruction Prompt
- When inspecting a `Transparency` filter in a Thumbnailator pipeline, use `getAlpha()` to retrieve its opacity.
- Always handle the return type as a `float` ranging from `0.0f` to `1.0f`, not as an integer or a percentage.
- Do not attempt to call this method on the `Thumbnails.Builder` fluent interface; it is specific to the `Transparency` filter instance.

### Prompt Snippet
```text
To check the opacity level of a Transparency filter in Thumbnailator, call `getAlpha()` on the filter instance. It returns a float between 0.0f (transparent) and 1.0f (opaque).
```

### Common Failure Modes
- **Scale Misinterpretation**: Assuming the alpha value is returned as an integer byte range (`0` to `255`) or a percentage (`0` to `100`) rather than a normalized float (`0.0f` to `1.0f`).
- **Receiver Type Error**: Attempting to call `getAlpha()` directly on the `Thumbnails.Builder` instead of an instantiated `Transparency` filter object.

### Fix Code Hint
```java
// Incorrect: Expecting an integer byte range
// int alpha = transparencyFilter.getAlpha();

// Correct: Handling the normalized float range
float alpha = transparencyFilter.getAlpha();
if (alpha == 1.0f) {
    // Filter is fully opaque
}
```

## API Test: `getBoolean`

### Signature
```java
public boolean getBoolean()
```
_Source: source/src/main/java/net/coobird/thumbnailator/util/Configurations.java:143_

_Source doc:_ Returns whether the specified configuration is enabled or not. @return  {@code true} if the configuration is enabled, {@code false} otherwise.

### Goal
Returns whether the specified rendering configuration (such as antialiasing or dithering) is enabled or disabled.

### Parameters
_None._

### Input
An instance of the `Configurations` enum representing a rendering hint or configuration state.

### Output
Returns `boolean` — `true` if the configuration is enabled, `false` otherwise.

### Valid Call Patterns
```java
// Iterate through configurations and check if they are enabled
for (Configurations config : Configurations.values()) {
    boolean isEnabled = config.getBoolean();
}
```

### LLM Instruction Prompt
- When inspecting Thumbnailator rendering configurations, call `getBoolean()` on a `Configurations` enum instance to determine if that specific configuration state is enabled. Do not pass any arguments.

### Prompt Snippet
```text
Use `config.getBoolean()` to check if a `Configurations` enum value is enabled or disabled.
```

### Common Failure Modes
- **`NullPointerException`**: Attempting to call `getBoolean()` on a `null` reference instead of a valid `Configurations` enum instance.

### Fix Code Hint
```java
if (config != null) {
    boolean isEnabled = config.getBoolean();
}
```

## API Test: `getCount`

### Signature
```java
public int getCount()
```
_Source: source/src/main/java/net/coobird/thumbnailator/util/exif/IfdStructure.java:82_

_Source doc:_ Returns the count element in the IFD structure, indicating the number of values the value field.. @return		A count indicating the number of values.

### Goal
Returns the count element from an Image File Directory (IFD) structure, indicating the number of values contained in its value field during Exif metadata parsing.

### Parameters
_None._

### Input
An instantiated `IfdStructure` object. This object is typically created internally by Thumbnailator's Exif parsing utilities (such as those backing `ExifUtils.getExifOrientation`) when reading metadata from an image source.

### Output
Returns `int` — the number of values present in the IFD entry's value field.

### Valid Call Patterns
```java
// Inferred from the signature and source path (not verified by test suite)
IfdStructure ifdStructure = // ... obtained via Exif parsing utilities
int valueCount = ifdStructure.getCount();
```

### LLM Instruction Prompt
- When inspecting Exif metadata tags via `IfdStructure`, use `getCount()` to retrieve the number of values in the IFD value field.
- Note that Thumbnailator's primary fluent API (`Thumbnails.of(...)`) handles Exif orientation automatically; direct interaction with `IfdStructure` and `getCount()` is generally reserved for custom metadata extraction or low-level Exif debugging.

### Prompt Snippet
```text
To determine how many values are stored in a specific Exif IFD tag, call `getCount()` on the `IfdStructure` instance. Remember that this represents the number of items, not necessarily the total byte length (which depends on the IFD data type).
```

### Common Failure Modes
- **Null Reference**: Calling `getCount()` on an uninitialized or null `IfdStructure` reference will throw a `NullPointerException`.
- **Misinterpreting Count as Bytes**: Assuming `getCount()` returns the total byte size of the payload. It returns the *number of values* (e.g., a count of 3 for an IFD type of SHORT means 3 * 2 bytes = 6 bytes total).

### Fix Code Hint
```java
if (ifdStructure != null) {
    int count = ifdStructure.getCount();
    // Process the values based on the count and the IFD data type
}
```

## API Test: `getDestination`

### Signature
```java
public OutputStream getDestination()
public File getDestination()
public D getDestination()
public abstract D getDestination()
```
_Source: source/src/main/java/net/coobird/thumbnailator/tasks/StreamThumbnailTask.java:96  (+3 more definition site/overload)_

### Goal
Returns the destination object (such as a `File` or `OutputStream`) to which the processed thumbnail is stored or written by a task or sink.

### Parameters
_None._

### Input
An instantiated `ThumbnailTask` (such as `FileThumbnailTask` or `StreamThumbnailTask`) or an `ImageSink` that has been configured with a specific output target. The caller must hold a reference to this task or sink parameterized with the destination type `D`.

### Output
Returns `OutputStream` — (or `File` / generic `D`, depending on the specific implementation overload) representing the underlying sink where the generated thumbnail artifact is routed.

### Valid Call Patterns
```java
// Note: Example inferred from the API signature and project context (not verified by test suite).

// For a StreamThumbnailTask, the destination is an OutputStream
OutputStream out = streamThumbnailTask.getDestination();

// For a FileThumbnailTask, the destination is a File
File outFile = fileThumbnailTask.getDestination();
```

### LLM Instruction Prompt
- When inspecting a `ThumbnailTask` or `ImageSink` in advanced Thumbnailator workflows, use `getDestination()` to retrieve the underlying output target. 
- Pay attention to the generic type `D` or the specific task implementation (`FileThumbnailTask` vs. `StreamThumbnailTask`), as the return type will vary between `File`, `OutputStream`, or other custom sinks.
- Do not use this method in standard fluent builder pipelines (`Thumbnails.of(...)`), as the destination is handled internally by terminal methods like `toFile()` or `toOutputStream()`.

### Prompt Snippet
```text
To retrieve the output target from a Thumbnailator task, call `task.getDestination()`. The return type matches the task's destination parameter `D` (e.g., `File` for `FileThumbnailTask`, `OutputStream` for `StreamThumbnailTask`).
```

### Common Failure Modes
- **Type Mismatch / ClassCastException**: Assuming `getDestination()` always returns a `File` when working with a generic `ThumbnailTask<S, D>`. If the pipeline was built for streams, it will return an `OutputStream`.
- **Improper Abstraction Level**: Attempting to call `getDestination()` on the `Thumbnails.Builder` fluent interface. This method belongs to the lower-level `ThumbnailTask` and `ImageSink` abstractions.

### Fix Code Hint
```java
// INCORECT: Assuming the destination is always a File
File dest = (File) genericTask.getDestination(); // May throw ClassCastException if task is stream-based

// CORRECT: Use the specific task type or rely on the generic parameter D
if (genericTask instanceof FileThumbnailTask) {
    File dest = ((FileThumbnailTask) genericTask).getDestination();
} else if (genericTask instanceof StreamThumbnailTask) {
    OutputStream dest = ((StreamThumbnailTask) genericTask).getDestination();
}
```

## API Test: `getExifOrientation`

### Signature
```java
public static Orientation getExifOrientation(ImageReader reader, int imageIndex)
```
_Source: source/src/main/java/net/coobird/thumbnailator/util/exif/ExifUtils.java:69_

_Source doc:_ Returns the orientation obtained from the Exif metadata. @param reader		An {@link ImageReader} which is reading the target image. @param imageIndex	The index of the image from which the Exif metadata should be read from. @return				The orientation information obtained from the Exif metadata, as a {@link Orientation} enum. Returns {@code null} if no orientation is found. @throws IOException				When an error occurs during reading. @throws IllegalArgumentException	If the {@link ImageReader} does not have the target image set, or if the reader does not have a JPEG open.

### Goal
Extracts the Exif orientation metadata from a JPEG image to determine if the image requires rotation correction before processing.

### Parameters
- `reader` (`ImageReader`): An `ImageReader` instance that is currently reading the target JPEG image and has its input source explicitly set.
- `imageIndex` (`int`): The zero-based index of the image within the input source from which the Exif metadata should be read (typically `0` for standard single-frame JPEGs).

### Input
The caller must provide an initialized `ImageReader` that specifically has a JPEG open. A critical precondition is that the reader must have its input set (e.g., via `reader.setInput(ImageIO.createImageInputStream(...))`) before calling this method. 

### Output
Returns `Orientation` — An enum representing the orientation information parsed from the Exif metadata (values typically corresponding to Exif tags 1 through 8). Returns `null` if no orientation metadata is found in the image.

### Valid Call Patterns
```java
// given
ImageReader reader = ImageIO.getImageReadersByFormatName("jpg").next();
InputStream is = new FileInputStream("image_with_exif.jpg");
reader.setInput(ImageIO.createImageInputStream(is));

// when
Orientation orientation = ExifUtils.getExifOrientation(reader, 0);
is.close();

// then (use the orientation to correct the image pipeline)
if (orientation != null) {
    // e.g., ExifFilterUtils.getFilterForOrientation(orientation)
}
```

### LLM Instruction Prompt
- When calling `ExifUtils.getExifOrientation`, you MUST ensure the `ImageReader` has its input set via `reader.setInput(...)` prior to the call.
- You MUST ensure the `ImageReader` is processing a JPEG image; otherwise, an `IllegalArgumentException` will be thrown.
- You MUST handle the case where the returned `Orientation` is `null` (which occurs when the image lacks Exif orientation metadata).

### Prompt Snippet
```text
To extract Exif orientation safely, initialize a JPEG `ImageReader`, set its input using `ImageIO.createImageInputStream`, and call `ExifUtils.getExifOrientation(reader, 0)`. Always check if the returned `Orientation` is null before passing it to `ExifFilterUtils.getFilterForOrientation`.
```

### Common Failure Modes
- **`IllegalArgumentException`**: Thrown if the `ImageReader` does not have the target image set (i.e., `setInput` was not called) or if the reader does not have a JPEG open.
- **`IOException`**: Thrown if an error occurs while reading the underlying image stream.
- **`NullPointerException`**: Occurs if the caller attempts to use the returned `Orientation` without checking for `null` when processing an image that lacks Exif metadata.

### Fix Code Hint
```java
ImageReader reader = ImageIO.getImageReadersByFormatName("jpg").next();
// FIX: Must set input before calling getExifOrientation
try (ImageInputStream iis = ImageIO.createImageInputStream(inputStream)) {
    reader.setInput(iis);
    Orientation orientation = ExifUtils.getExifOrientation(reader, 0);
    
    // FIX: Must check for null
    if (orientation != null) {
        ImageFilter rotationFilter = ExifFilterUtils.getFilterForOrientation(orientation);
        // apply filter...
    }
} finally {
    reader.dispose();
}
```

## API Test: `getFilterForOrientation`

### Signature
```java
public static ImageFilter getFilterForOrientation(Orientation orientation)
```
_Source: source/src/main/java/net/coobird/thumbnailator/util/exif/ExifFilterUtils.java:56_

_Source doc:_ Returns a {@link ImageFilter} which will perform the transformations required to properly orient the thumbnail according to the Exif orientation. @param orientation	The Exif orientation @return				{@link ImageFilter}s required to properly orient the image.

### Goal
Returns an `ImageFilter` that applies the necessary rotation and flipping transformations to correct an image's orientation based on its Exif metadata.

### Parameters
- `orientation` (`Orientation`): The Exif orientation value extracted from the source image's metadata (often resolved via `Orientation.typeOf(int)`).

### Input
The caller must provide a valid `Orientation` enum value. Because standard Java `ImageIO.read()` strips Exif metadata and loads the raw pixel data as-is, callers processing raw `BufferedImage` objects must first parse the Exif metadata (e.g., using `ExifUtils.getExifOrientation`) to determine the correct orientation before passing it to this method.

### Output
Returns `ImageFilter` — A filter instance that can be added to a `Thumbnails.Builder` pipeline to physically rotate or flip the image to its correct upright orientation during processing.

### Valid Call Patterns
```java
// Correcting orientation when reading a BufferedImage from an InputStream
BufferedImage result =
        Thumbnails.of(ImageIO.read(is))
                .addFilter(ExifFilterUtils.getFilterForOrientation(Orientation.typeOf(orientation)))
                .size(width, height)
                .asBufferedImage();

// Correcting orientation when scaling a BufferedImage from a File
BufferedImage result =
        Thumbnails.of(ImageIO.read(sourceFile))
                .addFilter(ExifFilterUtils.getFilterForOrientation(Orientation.typeOf(orientation)))
                .scale(0.5)
                .asBufferedImage();
```

### LLM Instruction Prompt
- When processing `BufferedImage` sources (which lose Exif rotation data when read via `ImageIO`), extract the Exif orientation and generate a correction filter using `ExifFilterUtils.getFilterForOrientation(orientation)`. Apply this filter to the pipeline using `Thumbnails.Builder.addFilter(ImageFilter)` before resizing or scaling.

### Prompt Snippet
```text
To ensure images are rotated correctly before processing, Exif metadata must be parsed. Use `ExifFilterUtils.getFilterForOrientation(Orientation)` to get the specific `ImageFilter` required to correct the image's orientation, and add it to the fluent builder via `.addFilter()`.
```

### Common Failure Modes
- **Sideways or Upside-Down Output**: Failing to apply this filter when reading images via `ImageIO.read()` results in thumbnails that retain the raw, unrotated pixel orientation of the original camera sensor.
- **Missing Qualifier**: Attempting to call `getFilterForOrientation` without the `ExifFilterUtils` class qualifier will cause a compilation error.
- **Type Mismatch**: Passing a raw integer Exif tag (1-8) directly instead of converting it to the `Orientation` enum type (e.g., via `Orientation.typeOf(int)`).

### Fix Code Hint
```java
// Incorrect: Passing raw int or forgetting the filter
Thumbnails.of(ImageIO.read(file)).size(200, 200).asBufferedImage();

// Correct: Converting the int to Orientation and adding the filter
Thumbnails.of(ImageIO.read(file))
    .addFilter(ExifFilterUtils.getFilterForOrientation(Orientation.typeOf(exifInt)))
    .size(200, 200)
    .asBufferedImage();
```

## API Test: `getFilters`

### Signature
```java
public List<ImageFilter> getFilters()
```
_Source: source/src/main/java/net/coobird/thumbnailator/filters/Pipeline.java:140_

_Source doc:_ Returns a list of {@link ImageFilter}s which will be applied by this {@link Pipeline}. @return					A list of filters which are applied by this pipeline.

### Goal
Retrieves the ordered sequence of `ImageFilter` instances that are configured to be applied by the `Pipeline`.

### Parameters
_None._

### Input
An instantiated `Pipeline` object that has been constructed with either a `List<ImageFilter>` or varargs of `ImageFilter` instances (such as `Rotation`, `Watermark`, or `Canvas`).

### Output
Returns `List<ImageFilter>` — an ordered list representing the sequence of image transformations that this pipeline will apply to a `BufferedImage`.

### Valid Call Patterns
```java
// Example 1: Retrieving filters from a Pipeline initialized with a List
List<ImageFilter> filters = new ArrayList<ImageFilter>();
filters.add(filter1);
filters.add(filter2);
Pipeline pipeline = new Pipeline(filters);

List<ImageFilter> returned = pipeline.getFilters();

// Example 2: Retrieving filters from a Pipeline initialized with varargs
Pipeline pipelineVarargs = new Pipeline(filter1, filter2);
List<ImageFilter> returnedVarargs = pipelineVarargs.getFilters();
```

### LLM Instruction Prompt
- Use `pipeline.getFilters()` when you need to inspect, verify, or assert the sequence of transformations registered within a custom `Pipeline`.
- Do not assume the specific subclass of the returned `ImageFilter` elements; if you need to verify a specific filter (e.g., `Watermark` or `Rotation`), iterate through the list and use `instanceof`.

### Prompt Snippet
```text
To inspect the transformations configured in a Thumbnailator Pipeline, call `pipeline.getFilters()` to retrieve the `List<ImageFilter>`. Ensure you check the type of each filter using `instanceof` if you need to access specific filter properties.
```

### Common Failure Modes
- **Null Reference**: Calling `getFilters()` on an uninitialized (null) `Pipeline` reference will result in a `NullPointerException`.
- **Type Assumption Errors**: Blindly casting an element from the returned `List<ImageFilter>` to a specific implementation (like `Caption` or `Colorize`) without an `instanceof` check will cause a `ClassCastException` if the pipeline order differs from expectations.

### Fix Code Hint
```java
if (pipeline != null) {
    List<ImageFilter> activeFilters = pipeline.getFilters();
    for (ImageFilter filter : activeFilters) {
        if (filter instanceof Watermark) {
            // Safely handle the specific filter type
        }
    }
}
```

## API Test: `getFormatName`

### Signature
```java
public String getFormatName()
```
_Source: source/src/main/java/net/coobird/thumbnailator/tasks/UnsupportedFormatException.java:80_

_Source doc:_ Returns the format name which is not supported. @return			Format name.

### Goal
Retrieves the name of the image format that caused an `UnsupportedFormatException` because it is not supported by the underlying Java Image I/O implementation.

### Parameters
_None._

### Input
An instance of `UnsupportedFormatException` caught during a Thumbnailator pipeline execution. This exception typically occurs when attempting to read an unrecognized file type or when explicitly requesting an output format (via `Thumbnails.Builder.outputFormat(String)`) that the host JVM does not support.

### Output
Returns `String` — the name of the unsupported format (e.g., `"tiff"`, `"webp"`, or a custom extension) that triggered the exception.

### Valid Call Patterns
```java
// Inferred from the signature (not verified in tests, as test examples show javax.imageio.ImageReader.getFormatName())
try {
    Thumbnails.of(new File("input.jpg"))
        .size(640, 480)
        .outputFormat("webp") // May not be supported by default Java 8 Image I/O
        .toFile(new File("output.webp"));
} catch (UnsupportedFormatException e) {
    String unsupported = e.getFormatName();
    System.err.println("The JVM does not support the requested format: " + unsupported);
}
```

### LLM Instruction Prompt
- When catching an `UnsupportedFormatException` during a Thumbnailator operation, call `getFormatName()` on the exception instance to extract the specific format string that failed.
- Use this method to provide informative error messages or to trigger fallback logic (e.g., falling back to universally supported formats like `"jpg"` or `"png"`).
- Do not confuse this Thumbnailator exception method with the standard Java `javax.imageio.ImageReader.getFormatName()` method.

### Prompt Snippet
```text
When a Thumbnailator pipeline throws an `UnsupportedFormatException`, use `e.getFormatName()` to identify which format string the JVM's Image I/O rejected. Thumbnailator relies entirely on the host JVM for format support and has no external dependencies.
```

### Common Failure Modes
- **Assuming format support:** Developers often assume formats like WebP, HEIC, or TIFF are supported by default. Because Thumbnailator relies entirely on the host JVM's standard Image I/O capabilities, requesting these without the appropriate Image I/O plugins on the classpath will throw an `UnsupportedFormatException`.
- **Special constant values:** If the format was never explicitly set but could not be determined, the exception might carry the internal `ThumbnailParameter.DETERMINE_FORMAT` constant (which is `"\0"`) or `null`.

### Fix Code Hint
```java
try {
    Thumbnails.of(inputFile)
        .size(200, 200)
        .outputFormat(desiredFormat)
        .toFile(outputFile);
} catch (UnsupportedFormatException e) {
    // Fallback to a universally supported format if the requested one fails
    System.out.println("Format '" + e.getFormatName() + "' is unsupported. Falling back to JPEG.");
    Thumbnails.of(inputFile)
        .size(200, 200)
        .outputFormat("jpg")
        .toFile(new File(outputFile.getParentFile(), "fallback.jpg"));
}
```

## API Test: `getHeightScalingFactor`

### Signature
```java
public double getHeightScalingFactor()
```
_Source: source/src/main/java/net/coobird/thumbnailator/ThumbnailParameter.java:840_

_Source doc:_ Returns the scaling factor to apply to the height when creating the thumbnail. <p> Returns {@link Double#NaN} if the thumbnail size is set rather than the scaling factor. @return		The height scaling factor for the thumbnail. @since	0.3.10

### Goal
Retrieves the scaling multiplier applied to the height of the original image when generating a thumbnail.

### Parameters
_None._

### Input
A valid `ThumbnailParameter` instance, typically constructed via a `ThumbnailParameterBuilder` or extracted from an internal thumbnailing task, which has been configured with either a scaling factor or an absolute size.

### Output
Returns `double` — the height scaling factor for the thumbnail (e.g., `0.5` for 50% of the original height). It returns `Double.NaN` if the thumbnail was configured using absolute dimensions (e.g., via `size(int, int)`) rather than a scaling factor.

### Valid Call Patterns
```java
// Example based on the project's test suite
ThumbnailParameter param = new ThumbnailParameterBuilder()
        .size(100, 100)
        .build();

double heightScale = param.getHeightScalingFactor();
// heightScale evaluates to Double.NaN because absolute size was used
```

### LLM Instruction Prompt
- When inspecting a `ThumbnailParameter` via `getHeightScalingFactor()`, you MUST account for `Double.NaN`. Thumbnailator pipelines are configured with either absolute dimensions (`size`) or relative scales (`scale`), and this method returns `NaN` if absolute dimensions were used.

### Prompt Snippet
```text
Always check if `getHeightScalingFactor()` returns `Double.NaN`. If it does, the thumbnail was configured with an absolute `Dimension` rather than a scaling factor, and you should query `getSize()` instead.
```

### Common Failure Modes
- **Blindly performing math with the result**: Multiplying the original image height by the result of `getHeightScalingFactor()` without checking for `Double.NaN` will propagate `NaN` through your geometry calculations if the pipeline was configured using `.size(w, h)`.

### Fix Code Hint
```java
double heightScale = param.getHeightScalingFactor();
if (Double.isNaN(heightScale)) {
    // The parameter uses absolute sizing, not scaling.
    Dimension targetSize = param.getSize();
    // Use targetSize.height for calculations instead
} else {
    // Safe to use heightScale
    int newHeight = (int) (originalHeight * heightScale);
}
```

## API Test: `getImageFilters`

### Signature
```java
public List<ImageFilter> getImageFilters()
```
_Source: source/src/main/java/net/coobird/thumbnailator/ThumbnailParameter.java:919_

_Source doc:_ Returns the list of {@link ImageFilter}s which are applied to the thumbnail. <p> These filters are applied after the original image has been resized. @return		The {@link ImageFilter}s which are applied to the thumbnail.

### Goal
Retrieves the ordered list of `ImageFilter` transformations (such as watermarks, rotations, or captions) configured to be applied to the thumbnail after it has been resized.

### Parameters
_None._

### Input
A valid, instantiated `ThumbnailParameter` object, typically constructed using a `ThumbnailParameterBuilder`.

### Output
Returns `List<ImageFilter>` — the sequence of filters scheduled for application to the thumbnail post-resize. If no filters were added during the builder configuration, this returns an empty list (e.g., `Collections.emptyList()`).

### Valid Call Patterns
```java
ThumbnailParameter param = new ThumbnailParameterBuilder()
        .size(100, 100)
        .build();

List<ImageFilter> filters = param.getImageFilters();
// filters will be an empty list if no filters were added to the builder
```

### LLM Instruction Prompt
- Use `getImageFilters()` when inspecting a `ThumbnailParameter` configuration to verify which transformations are scheduled in the pipeline.
- Remember that the returned `ImageFilter` instances (e.g., `Watermark`, `Rotation`, `Caption`) are strictly applied *after* the original image has been resized by the `Resizer`.
- Do not assume the list contains filters for Exif orientation correction unless explicitly added; Exif correction requires parsing metadata first via `ExifUtils` and `ExifFilterUtils`.

### Prompt Snippet
```text
List<ImageFilter> appliedFilters = param.getImageFilters();
```

### Common Failure Modes
- **Misunderstanding Execution Order**: Assuming the returned filters are applied *before* resizing. The API explicitly guarantees these filters are applied to the already-resized thumbnail.
- **Null Reference**: Attempting to call `getImageFilters()` on an uninitialized `ThumbnailParameter` variable, resulting in a `NullPointerException`.

### Fix Code Hint
```java
// Correctly inspecting the post-resize filters from a built parameter object
ThumbnailParameter param = new ThumbnailParameterBuilder()
        .size(640, 480)
        .build();

List<ImageFilter> postResizeFilters = param.getImageFilters();
if (postResizeFilters.isEmpty()) {
    System.out.println("No post-resize filters configured.");
}
```

## API Test: `getInputFormatName`

### Signature
```java
public String getInputFormatName()
```
_Source: source/src/main/java/net/coobird/thumbnailator/tasks/io/FileImageSource.java:149  (+2 more definition site/overload)_

### Goal
Retrieves the name of the image format from an `ImageSource` after the image data has been read.

### Parameters
_None._

### Input
An instantiated `ImageSource` (such as `FileImageSource`, `InputStreamImageSource`, or `URLImageSource`). 
**Precondition:** The source image must have already been read (e.g., by invoking the `read()` method on the `ImageSource`) before calling this method.

### Output
Returns `String` — The name of the image format (e.g., "JPEG", "PNG") as identified by the underlying Java Image I/O reader. Returns `null` if no image format information is available.

### Valid Call Patterns
```java
// Inferred from test suite mocks and source documentation preconditions
ImageSource source = new FileImageSource(new File("input.jpg"));

// The image MUST be read before querying the format name
BufferedImage image = source.read(); 

// Now it is safe to get the format name
String formatName = source.getInputFormatName();
if (formatName != null) {
    System.out.println("Source format: " + formatName);
}
```

### LLM Instruction Prompt
- You MUST call `read()` on the `ImageSource` instance before calling `getInputFormatName()`.
- You MUST handle the possibility that `getInputFormatName()` returns `null` if the format cannot be determined.
- Do not assume the format name is always available; fallback logic (like `ThumbnailParameter.DETERMINE_FORMAT` or `ThumbnailParameter.ORIGINAL_FORMAT`) may be required in pipeline tasks.

### Prompt Snippet
```text
When using `ImageSource.getInputFormatName()`, always invoke `read()` on the source first to prevent an `IllegalStateException`. Check the returned String for `null`, as the underlying Image I/O may not provide format information for all sources.
```

### Common Failure Modes
- **`IllegalStateException`**: Thrown if `getInputFormatName()` is called before the source image has been read via `read()`.
- **`NullPointerException`**: Thrown in the caller's code if the returned format string is used (e.g., in a `.equals()` comparison or string concatenation) without checking for `null` first.

### Fix Code Hint
```java
// BAD: Querying format before reading throws IllegalStateException
// String format = source.getInputFormatName(); 
// source.read();

// GOOD: Read first, then query, and handle potential nulls
source.read();
String format = source.getInputFormatName();
String safeFormat = (format != null) ? format : "unknown";
```

## API Test: `getInstance`

### Signature
```java
public static SwapDimensions getInstance()
public static ResizerFactory getInstance()
```
_Source: source/src/main/java/net/coobird/thumbnailator/filters/SwapDimensions.java:40  (+1 more definition site/overload)_

### Goal
Returns a singleton or default instance of a specific Thumbnailator component, such as the default `ResizerFactory` or the `SwapDimensions` image filter.

### Parameters
_None._

### Input
No arguments are required. The caller must invoke this static method directly on the target class (e.g., `DefaultResizerFactory` or `SwapDimensions`) to retrieve its singleton instance.

### Output
Returns `ResizerFactory` (or `SwapDimensions`) — A reusable, thread-safe instance of the requested class, which can be passed into a `ThumbnailParameterBuilder` or added to a `Thumbnails.Builder` pipeline.

### Valid Call Patterns
```java
// 1. Obtaining the default ResizerFactory for a ThumbnailTask (from test suite)
ResizerFactory resizerFactory = DefaultResizerFactory.getInstance();

ThumbnailParameter param = new ThumbnailParameterBuilder()
        .size(100, 100)
        .resizerFactory(resizerFactory)
        .build();

// 2. Obtaining the SwapDimensions filter (inferred from signature)
SwapDimensions swapFilter = SwapDimensions.getInstance();
```

### LLM Instruction Prompt
- When configuring a `ThumbnailParameter` that requires a `ResizerFactory`, always use `DefaultResizerFactory.getInstance()` rather than attempting to instantiate it with `new`. 
- Similarly, use `SwapDimensions.getInstance()` to obtain the dimension-swapping `ImageFilter`. 
- Never call `getInstance()` without a class qualifier.

### Prompt Snippet
```text
To get a `ResizerFactory` or `SwapDimensions` filter in Thumbnailator, call their static `getInstance()` methods (e.g., `DefaultResizerFactory.getInstance()`). Do not use their constructors, as they are designed as singletons.
```

### Common Failure Modes
- **Constructor Compilation Error**: Attempting to instantiate these singleton classes using the `new` keyword (e.g., `new DefaultResizerFactory()`) instead of the `getInstance()` factory method, resulting in compilation errors due to private or protected constructors.
- **Missing Class Qualifier**: Calling `getInstance()` as a bare method without specifying the class (e.g., `DefaultResizerFactory` or `SwapDimensions`), which will fail to compile.

### Fix Code Hint
```java
// Incorrect: Attempting to use a constructor for a singleton
// ResizerFactory factory = new DefaultResizerFactory();
// SwapDimensions filter = new SwapDimensions();

// Correct: Using the static getInstance() factory method
ResizerFactory factory = DefaultResizerFactory.getInstance();
SwapDimensions filter = SwapDimensions.getInstance();
```

## API Test: `getKey`

### Signature
```java
public Key getKey()
public RenderingHints.Key getKey()
```
_Source: source/src/main/java/net/coobird/thumbnailator/resizers/configurations/Dithering.java:71  (+4 more definition site/overload)_

### Goal
Returns the underlying Java 2D `RenderingHints.Key` associated with a specific Thumbnailator resizer configuration (such as dithering, antialiasing, or alpha interpolation).

### Parameters
_None._

### Input
An instance of a `ResizerConfiguration` enum (e.g., `Dithering`, `Antialiasing`, `AlphaInterpolation`, `Rendering`, or `ScalingMode`) from which the AWT rendering hint key is being extracted.

### Output
Returns `RenderingHints.Key` — The specific AWT rendering hint key (e.g., `RenderingHints.KEY_DITHERING` or `RenderingHints.KEY_ANTIALIASING`) that corresponds to the configuration category.

### Valid Call Patterns
```java
/* Inferred from signature and context (not verified by test suite) */
RenderingHints.Key ditherKey = Dithering.ENABLE.getKey();
RenderingHints.Key aaKey = Antialiasing.ON.getKey();
```

### LLM Instruction Prompt
- Use `getKey()` when building custom `Resizer` implementations or manually manipulating `Graphics2D` objects to extract the correct `java.awt.RenderingHints.Key` from a Thumbnailator configuration enum.
- Do not confuse `getKey()` with the hint's value; `getKey()` returns the category (the key), while the specific setting (the value) is typically retrieved via a corresponding `getValue()` method on the same enum.

### Prompt Snippet
```text
When applying Thumbnailator configurations to a custom Graphics2D context, use `configEnum.getKey()` to get the `RenderingHints.Key` and `configEnum.getValue()` to get the corresponding hint value.
```

### Common Failure Modes
- **Confusing Key and Value**: Attempting to pass the result of `getKey()` as the *value* in a `Graphics2D.setRenderingHint(Key, Object)` call. The `getKey()` method only provides the first argument (the category).
- **Null Reference**: Calling `getKey()` on an uninitialized or null configuration variable, resulting in a `NullPointerException`.

### Fix Code Hint
```java
// Incorrect: Passing the key as the value
// g2d.setRenderingHint(RenderingHints.KEY_DITHERING, Dithering.ENABLE.getKey());

// Correct: Using getKey() for the key and getValue() for the value
g2d.setRenderingHint(Dithering.ENABLE.getKey(), Dithering.ENABLE.getValue());
```

## API Test: `getOffsetValue`

### Signature
```java
public int getOffsetValue()
```
_Source: source/src/main/java/net/coobird/thumbnailator/util/exif/IfdStructure.java:93_

_Source doc:_ Returns either the offset or value of the IFD. @return		Either the offset or value. The type of the returned value can be determined by the return of the {@link #isOffset()} or {@link #isValue()} method.

### Goal
Returns the integer representing either the memory offset or the direct value of an Image File Directory (IFD) entry during Exif metadata parsing.

### Parameters
_None._

### Input
An instantiated `IfdStructure` object representing an Exif IFD entry. The caller must have already parsed the Exif metadata to obtain this structure.

### Output
Returns `int` — the offset address or the actual value of the IFD entry. The semantic meaning of this integer depends on the specific IFD entry's size and type.

### Valid Call Patterns
```java
// Inferred from the signature (not verified by test suite or README)
int offsetOrValue = ifdStructure.getOffsetValue();
```

### LLM Instruction Prompt
- When calling `getOffsetValue()`, you MUST determine the semantic meaning of the returned integer by first calling `isOffset()` or `isValue()` on the same `IfdStructure` instance. Do not assume the returned integer is always a direct value or always a pointer.

### Prompt Snippet
```text
The `getOffsetValue()` method returns an `int` that can represent either a direct value or an offset pointer. Always guard its interpretation with `isOffset()` or `isValue()` to ensure correct Exif metadata parsing.
```

### Common Failure Modes
- **Misinterpreting the Return Value**: Treating an offset pointer as a direct value (or vice versa) because the caller failed to check `isOffset()` or `isValue()` before using the returned integer. This leads to incorrect Exif orientation parsing and subsequently incorrect image rotation.

### Fix Code Hint
```java
if (ifdStructure.isOffset()) {
    int offset = ifdStructure.getOffsetValue();
    // Handle as a pointer/offset to the actual data
} else if (ifdStructure.isValue()) {
    int value = ifdStructure.getOffsetValue();
    // Handle as the direct value
}
```

## API Test: `getOrientationFromExif`

### Signature
```java
public static Orientation getOrientationFromExif(byte[] exifData)
```
_Source: source/src/main/java/net/coobird/thumbnailator/util/exif/ExifUtils.java:109_

_Source doc:_ Returns the orientation obtained from the Exif metadata. @param exifData		A byte array containing Exif data. @return				The orientation information obtained from the Exif metadata, as a {@link Orientation} enum. Returns {@code null} if no orientation is found.

### Goal
Parses a byte array of Exif metadata to extract the image's orientation information.

### Parameters
- `exifData` (`byte[]`): A byte array containing the raw Exif data extracted from an image.

### Input
Raw Exif metadata bytes. The caller is responsible for extracting this byte array from the image file or stream prior to calling this method.

### Output
Returns `Orientation` — an enum representing the orientation state found in the Exif data. Returns `null` if no orientation tag is found in the provided bytes.

### Valid Call Patterns
```java
// Note: Example inferred from signature (not verified by test suite)
byte[] exifBytes = /* ... extract Exif bytes from image ... */;
Orientation orientation = ExifUtils.getOrientationFromExif(exifBytes);

if (orientation != null) {
    // Use orientation to correct image rotation
}
```

### LLM Instruction Prompt
- Use `ExifUtils.getOrientationFromExif(byte[])` to parse raw Exif bytes into an `Orientation` enum. Always check if the returned `Orientation` is `null` before passing it to other utilities (such as `ExifFilterUtils.getFilterForOrientation(Orientation)`) to avoid `NullPointerException`s.

### Prompt Snippet
```text
When parsing Exif data to determine image orientation, call `ExifUtils.getOrientationFromExif(byte[])`. You must check for a `null` return value, which indicates no orientation metadata was found in the provided byte array.
```

### Common Failure Modes
- **`NullPointerException` on Return Value**: Failing to check if the returned `Orientation` is `null` before invoking methods on it or passing it to `ExifFilterUtils.getFilterForOrientation(Orientation)`. The method explicitly returns `null` when the orientation tag is missing.

### Fix Code Hint
```java
Orientation orientation = ExifUtils.getOrientationFromExif(exifBytes);
if (orientation != null) {
    // Safe to use the orientation enum
    ImageFilter filter = ExifFilterUtils.getFilterForOrientation(orientation);
}
```

## API Test: `getOutputFormat`

### Signature
```java
public String getOutputFormat()
```
_Source: source/src/main/java/net/coobird/thumbnailator/ThumbnailParameter.java:878_

_Source doc:_ Returns the output format for the thumbnail. <p> If the output format is to use the same compression format as the original image, this method will return {@link ThumbnailParameter#ORIGINAL_FORMAT}. <p> If the output format should be determined from the information available such as the file name of the thumbnail, then this method will return {@link ThumbnailParameter#DETERMINE_FORMAT}. @return 		The output format for the thumbnail.

### Goal
Retrieves the configured output format string for the thumbnail generation task, which may be a specific format name or a constant indicating how the format should be resolved.

### Parameters
_None._

### Input
A valid, instantiated `ThumbnailParameter` object, typically constructed using a `ThumbnailParameterBuilder` or extracted from an active thumbnail pipeline.

### Output
Returns `String` — The output format for the thumbnail. This will be a specific format string (e.g., `"jpg"`, `"png"`), `ThumbnailParameter.ORIGINAL_FORMAT` if it is configured to match the source image's compression format, or `ThumbnailParameter.DETERMINE_FORMAT` (value `"\0"`) if the format should be inferred from the output destination (such as the file extension).

### Valid Call Patterns
```java
ThumbnailParameter param = new ThumbnailParameterBuilder()
        .size(100, 100)
        .build();

String format = param.getOutputFormat();

// The default behavior when no format is explicitly set is to retain the original format
if (ThumbnailParameter.ORIGINAL_FORMAT.equals(format)) {
    // Format will match the source image
}
```

### LLM Instruction Prompt
- When inspecting a `ThumbnailParameter`'s output format, use `getOutputFormat()`.
- Do not assume the returned string is always a standard file extension or Image I/O format name (like `"jpg"`). You MUST check if the returned string equals `ThumbnailParameter.ORIGINAL_FORMAT` or `ThumbnailParameter.DETERMINE_FORMAT` before passing it to standard Java Image I/O APIs.
- Use this method when building custom `ThumbnailTask` implementations or debugging pipeline configurations to verify the intended output format.

### Prompt Snippet
```text
When retrieving the output format from a `ThumbnailParameter` using `getOutputFormat()`, be prepared to handle the special constants `ThumbnailParameter.ORIGINAL_FORMAT` and `ThumbnailParameter.DETERMINE_FORMAT`. Do not pass the raw return value directly to `ImageIO.getImageWritersByFormatName()` without checking for these constants first.
```

### Common Failure Modes
- **Assuming a literal format string**: Blindly using the return value as a format name for `ImageIO` operations will fail if the value is `ThumbnailParameter.DETERMINE_FORMAT` (`"\0"`) or `ThumbnailParameter.ORIGINAL_FORMAT`.
- **NullPointerException**: Calling this method on an uninitialized or null `ThumbnailParameter` reference.

### Fix Code Hint
```java
String format = param.getOutputFormat();

if (ThumbnailParameter.ORIGINAL_FORMAT.equals(format)) {
    // Logic to extract format from the original ImageSource
} else if (ThumbnailParameter.DETERMINE_FORMAT.equals(format)) {
    // Logic to extract format from the destination filename/ImageSink
} else {
    // Safe to use 'format' as a literal format name (e.g., "jpg", "png")
    System.out.println("Explicit format requested: " + format);
}
```

## API Test: `getOutputFormatType`

### Signature
```java
public String getOutputFormatType()
```
_Source: source/src/main/java/net/coobird/thumbnailator/ThumbnailParameter.java:891_

_Source doc:_ Returns the output format type for the thumbnail. <p> If the default compression type of the compression format is to be used, then this method will return {@link ThumbnailParameter#DEFAULT_FORMAT_TYPE}. @return 		The output format type for the thumbnail.

### Goal
Retrieves the configured output format type (such as the specific compression type) that will be applied when writing the generated thumbnail.

### Parameters
_None._

### Input
A valid, instantiated `ThumbnailParameter` object, typically constructed via a `ThumbnailParameterBuilder` or extracted from an active thumbnail generation pipeline.

### Output
Returns `String` — The output format type for the thumbnail. If the default compression type of the compression format is configured to be used, this method returns the constant `ThumbnailParameter.DEFAULT_FORMAT_TYPE`.

### Valid Call Patterns
```java
// Inspecting the default format type from a newly built ThumbnailParameter
ThumbnailParameter param = new ThumbnailParameterBuilder()
        .size(100, 100)
        .build();

String formatType = param.getOutputFormatType();
// formatType will equal ThumbnailParameter.DEFAULT_FORMAT_TYPE
```

### LLM Instruction Prompt
- When inspecting a `ThumbnailParameter` object's configuration, use `getOutputFormatType()` to determine the specific compression format type.
- Do not confuse this method with `getOutputFormat()`. `getOutputFormat()` returns the image format (e.g., "jpg", "png"), whereas `getOutputFormatType()` returns the compression type string.
- Always account for the fact that this method will return `ThumbnailParameter.DEFAULT_FORMAT_TYPE` if no explicit format type was specified during the builder phase.

### Prompt Snippet
```text
To check the compression format type of a Thumbnailator pipeline configuration, call `param.getOutputFormatType()`. Note that if the default compression type is used, it returns `ThumbnailParameter.DEFAULT_FORMAT_TYPE`. Do not confuse this with the file format extension returned by `getOutputFormat()`.
```

### Common Failure Modes
- **NullPointerException**: Attempting to call `getOutputFormatType()` on an uninitialized or null `ThumbnailParameter` reference.
- **Semantic Confusion**: Assuming the method returns the file extension (like `"jpg"` or `"png"`). The file extension/format is retrieved via `getOutputFormat()`, while `getOutputFormatType()` dictates the compression scheme specific to the underlying Java Image I/O writer.

### Fix Code Hint
```java
// INCORRECT: Assuming getOutputFormatType() returns the file extension
if ("jpg".equals(param.getOutputFormatType())) { ... }

// CORRECT: Use getOutputFormat() for the file format, and getOutputFormatType() for the compression type
if ("jpg".equals(param.getOutputFormat())) {
    String compressionType = param.getOutputFormatType();
    if (ThumbnailParameter.DEFAULT_FORMAT_TYPE.equals(compressionType)) {
        // Handle default compression scenario
    }
}
```

## API Test: `getOutputQuality`

### Signature
```java
public float getOutputQuality()
```
_Source: source/src/main/java/net/coobird/thumbnailator/ThumbnailParameter.java:907_

_Source doc:_ Returns the compression quality settings for the thumbnail. <p> The value is in the range of {@code 0.0f} to {@code 1.0f}, where {@code 0.0f} is for the lowest quality setting and {@code 1.0f} for the highest quality setting. <p> If the default compression quality is to be used, then this method will return {@link ThumbnailParameter#DEFAULT_QUALITY}. @return 		The compression quality settings for the thumbnail.

### Goal
Retrieves the configured compression quality setting for the thumbnail output, ranging from lowest (0.0f) to highest (1.0f) quality.

### Parameters
_None._

### Input
A valid, instantiated `ThumbnailParameter` object, typically constructed via a `ThumbnailParameterBuilder` or extracted from an active image processing pipeline.

### Output
Returns `float` — the compression quality setting for the thumbnail. The value is strictly in the range of `0.0f` (lowest quality/highest compression) to `1.0f` (highest quality/lowest compression). If the default compression quality is configured, this returns `Float.NaN` (which corresponds to `ThumbnailParameter.DEFAULT_QUALITY`).

### Valid Call Patterns
```java
// Extracting the output quality from a built ThumbnailParameter
ThumbnailParameter param = new ThumbnailParameterBuilder()
        .size(100, 100)
        .build();

float quality = param.getOutputQuality();
boolean isDefault = Float.isNaN(quality);
```

### LLM Instruction Prompt
- When evaluating the result of `getOutputQuality()`, you MUST check if the value is `Float.NaN` using `Float.isNaN()` before using it in mathematical operations or strict comparisons, as `NaN` indicates the default quality setting is active.
- Do not assume the quality is represented as an integer percentage (0-100); it is strictly a fractional `float` between `0.0f` and `1.0f`.

### Prompt Snippet
```text
When reading `getOutputQuality()`, handle `Float.NaN` as the default quality indicator. Valid explicit qualities range from 0.0f to 1.0f. Never treat the return value as a 0-100 percentage.
```

### Common Failure Modes
- **Unsafe NaN Comparisons**: Attempting to compare the returned float directly using `==` without accounting for `Float.NaN` when the default quality is used, resulting in logic errors (since `NaN == NaN` evaluates to `false` in Java).
- **Scale Misinterpretation**: Assuming the returned quality is a percentage (e.g., `80.0f` for 80%) rather than a normalized float (e.g., `0.8f`), leading to out-of-bounds errors if passed to other Image I/O writers.

### Fix Code Hint
```java
float quality = param.getOutputQuality();
if (Float.isNaN(quality)) {
    // Handle default quality scenario
    System.out.println("Using default compression quality.");
} else {
    // Handle explicit quality scenario (0.0f to 1.0f)
    System.out.println("Explicit quality set to: " + quality);
}
```

## API Test: `getParam`

### Signature
```java
public ThumbnailParameter getParam()
```
_Source: source/src/main/java/net/coobird/thumbnailator/tasks/StreamThumbnailTask.java:86  (+2 more definition site/overload)_

### Goal
Retrieves the `ThumbnailParameter` configuration object assigned to a `ThumbnailTask` for a thumbnail generation operation.

### Parameters
_None._

### Input
An initialized instance of a `ThumbnailTask` (such as `FileThumbnailTask` or `StreamThumbnailTask`) that was constructed with a valid `ThumbnailParameter`.

### Output
Returns `ThumbnailParameter` — the configuration settings (such as dimensions, output format, quality, and resizer algorithms) to use when generating thumbnails.

### Valid Call Patterns
```java
// Example using FileThumbnailTask
ThumbnailParameter param = new ThumbnailParameter(
        new Dimension(50, 50),
        null,
        true,
        "jpg",
        ThumbnailParameter.DEFAULT_FORMAT_TYPE,
        ThumbnailParameter.DEFAULT_QUALITY,
        BufferedImage.TYPE_INT_ARGB,
        null,
        Resizers.PROGRESSIVE,
        true,
        true
);

File inputFile = new File("input.jpg");
File outputFile = new File("output.jpg");

FileThumbnailTask task = new FileThumbnailTask(param, inputFile, outputFile);

// Retrieve the parameters assigned to the task
ThumbnailParameter retrievedParam = task.getParam();
```

### LLM Instruction Prompt
- When working with advanced workflows involving explicit `ThumbnailTask` instances (like `FileThumbnailTask` or `StreamThumbnailTask`), use `getParam()` to inspect the underlying `ThumbnailParameter` configuration.
- Do not attempt to call `getParam()` on the fluent `Thumbnails.Builder` interface, as it is strictly a method of the `ThumbnailTask` abstraction.

### Prompt Snippet
```text
To inspect the configuration of an explicit thumbnail generation task, call `task.getParam()`. This returns the `ThumbnailParameter` object containing the dimensions, format, and rendering hints assigned to that specific `ThumbnailTask`.
```

### Common Failure Modes
- **Context Mismatch**: Attempting to call `getParam()` on a `Thumbnails.Builder` instance. The fluent builder manages parameters internally; `getParam()` is only available on concrete `ThumbnailTask` objects used in advanced, manual pipeline construction.
- **Null Reference**: Calling `getParam()` on an uninitialized `ThumbnailTask` variable, resulting in a `NullPointerException`.

### Fix Code Hint
```java
// INCORRECT: Attempting to get parameters from the fluent builder
// Thumbnails.Builder<File> builder = Thumbnails.of(new File("img.jpg")).size(200, 200);
// ThumbnailParameter p = builder.getParam(); // Does not compile

// CORRECT: Getting parameters from an explicit ThumbnailTask
StreamThumbnailTask task = new StreamThumbnailTask(param, inputStream, outputStream);
ThumbnailParameter activeParams = task.getParam();
```

## API Test: `getPosition`

### Signature
```java
public Position getPosition()
```
_Source: source/src/main/java/net/coobird/thumbnailator/geometry/Region.java:77_

_Source doc:_ Returns the position of the region. @return 				Position of the region.

### Goal
Retrieves the `Position` (such as an anchor point or coordinate) associated with a geometric `Region`.

### Parameters
_None._

### Input
An initialized `Region` instance.

### Output
Returns `Position` — the geometric position of the region, which dictates where an operation (like cropping or watermarking) is anchored. This may be a `Positions` enum constant or a `Coordinate` object.

### Valid Call Patterns
```java
// Inferred from signature (no verified examples available in project context)
Position position = region.getPosition();
```

### LLM Instruction Prompt
- When inspecting or extracting the layout of a `Region`, use `getPosition()` to retrieve its `Position` interface. Do not assume the returned `Position` is always a `Positions` enum; it may be a `Coordinate` or other custom implementation.

### Prompt Snippet
```text
Use region.getPosition() to get the Position interface of a Region. Handle the result as the Position interface, not strictly the Positions enum, as it could be a Coordinate.
```

### Common Failure Modes
- **`NullPointerException`**: Attempting to call `getPosition()` on a null `Region` reference.
- **`ClassCastException`**: Blindly casting the returned `Position` to the `Positions` enum, failing to account for `Coordinate` or other custom `Position` implementations.

### Fix Code Hint
```java
if (region != null) {
    Position pos = region.getPosition();
    // Rely on the Position interface methods (e.g., calculate) rather than casting to Positions enum
}
```

## API Test: `getProxy`

### Signature
```java
public Proxy getProxy()
```
_Source: source/src/main/java/net/coobird/thumbnailator/tasks/io/URLImageSource.java:180_

_Source doc:_ Returns the proxy to use when connecting to the URL to retrieve the source image. @return the proxy	The proxy used to connect to a URL.

### Goal
Retrieves the proxy configuration used when connecting to a URL to fetch a source image.

### Parameters
_None._

### Input
An instantiated `URLImageSource` object.

### Output
Returns `Proxy` — the proxy configuration used to connect to the URL.

### Valid Call Patterns
```java
// Inferred from signature (no verified examples provided)
Proxy proxy = urlImageSource.getProxy();
```

### LLM Instruction Prompt
- Use `getProxy()` when you need to inspect the proxy settings configured for a specific `URLImageSource` instance.
- Do not attempt to call this method on the generic `ImageSource` interface, as it is specific to the `URLImageSource` implementation.

### Prompt Snippet
```text
To retrieve the proxy configuration used for fetching an image from a URL, call `getProxy()` on the `URLImageSource` instance. Ensure the receiver is typed as `URLImageSource` rather than the base `ImageSource` interface.
```

### Common Failure Modes
- **Method Not Found on Interface**: Attempting to call `getProxy()` on a variable declared as the base `ImageSource` interface, resulting in a compilation error.

### Fix Code Hint
```java
// Check type and cast before calling getProxy()
if (source instanceof URLImageSource) {
    Proxy proxy = ((URLImageSource) source).getProxy();
    // Use proxy...
}
```

## API Test: `getRenderingHints`

### Signature
```java
public Map<RenderingHints.Key, Object> getRenderingHints()
```
_Source: source/src/main/java/net/coobird/thumbnailator/resizers/AbstractResizer.java:146_

_Source doc:_ Returns the rendering hints that the resizer uses. <p> The keys and values used for the rendering hints are those defined in the {@link RenderingHints} class. @see RenderingHints @return		Rendering hints used when resizing the image.

### Goal
Returns the standard Java 2D rendering hints configuration map used by a specific `Resizer` implementation during the image scaling process.

### Parameters
_None._

### Input
A valid, instantiated `Resizer` object (such as `BicubicResizer`, `BilinearResizer`, `ProgressiveBilinearResizer`, or `NullResizer`).

### Output
Returns `Map<RenderingHints.Key, Object>` — A map containing the specific `java.awt.RenderingHints.Key` instances and their corresponding value objects (e.g., `RenderingHints.VALUE_INTERPOLATION_BICUBIC`) that the resizer applies to the `Graphics2D` context.

### Valid Call Patterns
```java
// Inferred from signature and context (no verified test/README example available)
Resizer resizer = new BicubicResizer();
Map<RenderingHints.Key, Object> hints = resizer.getRenderingHints();

Object interpolationHint = hints.get(RenderingHints.KEY_INTERPOLATION);
```

### LLM Instruction Prompt
- Call `getRenderingHints()` on a `Resizer` instance when you need to inspect the underlying Java 2D rendering configuration (like interpolation, antialiasing, or dithering settings) applied by that specific scaling algorithm.
- Expect standard `java.awt.RenderingHints.Key` objects as keys, not Thumbnailator's internal configuration enums.

### Prompt Snippet
```text
To inspect the Java 2D rendering hints used by a Thumbnailator `Resizer`, call `resizer.getRenderingHints()`. This returns a `Map<RenderingHints.Key, Object>` containing standard AWT rendering hint keys and values.
```

### Common Failure Modes
- **Type Confusion**: Expecting the map to contain Thumbnailator's fluent configuration enums (e.g., `net.coobird.thumbnailator.resizers.configurations.Antialiasing.ON`) instead of standard `java.awt.RenderingHints` objects (e.g., `RenderingHints.VALUE_ANTIALIAS_ON`).
- **Modification Exceptions**: Attempting to modify the returned map. While not explicitly documented as unmodifiable, internal configuration maps in Thumbnailator should be treated as read-only to prevent unintended side effects across the pipeline.

### Fix Code Hint
```java
// Correctly querying the standard Java 2D RenderingHints keys
Map<RenderingHints.Key, Object> hints = resizer.getRenderingHints();

if (hints != null && hints.containsKey(RenderingHints.KEY_INTERPOLATION)) {
    Object interpValue = hints.get(RenderingHints.KEY_INTERPOLATION);
    // interpValue will be a standard AWT value, e.g., RenderingHints.VALUE_INTERPOLATION_BICUBIC
}
```

## API Test: `getResizer`

### Signature
```java
public Resizer getResizer()
public Resizer getResizer(Dimension originalSize, Dimension thumbnailSize)
```
_Source: source/src/main/java/net/coobird/thumbnailator/resizers/DefaultResizerFactory.java:126  (+6 more definition site/overload)_

### Goal
Returns a suitable `Resizer` implementation chosen by the factory to optimally scale an image based on the dimensions of the original image and the target thumbnail.

### Parameters
- `originalSize` (`Dimension`): The dimensions (width and height) of the original source image.
- `thumbnailSize` (`Dimension`): The dimensions (width and height) of the target thumbnail image.

### Input
The caller must provide valid `java.awt.Dimension` objects representing the source and target sizes. The method must be invoked on a `ResizerFactory` instance (such as `DefaultResizerFactory.getInstance()`). 

### Output
Returns `Resizer` — an implementation (such as `BicubicResizer`, `BilinearResizer`, or `ProgressiveBilinearResizer`) selected by the factory to perform the resizing operation for the given dimensional conditions.

### Valid Call Patterns
```java
// Obtain a ResizerFactory (e.g., the default factory)
ResizerFactory resizerFactory = DefaultResizerFactory.getInstance();

// Get the optimal resizer for scaling a 200x200 image down to 100x100
Dimension originalSize = new Dimension(200, 200);
Dimension thumbnailSize = new Dimension(100, 100);
Resizer resizer = resizerFactory.getResizer(originalSize, thumbnailSize);
```

### LLM Instruction Prompt
- Call `getResizer` on a `ResizerFactory` instance (e.g., `DefaultResizerFactory.getInstance()`), not as a static method.
- Pass `java.awt.Dimension` objects for both the original and thumbnail sizes.
- Do not manually instantiate specific `Resizer` implementations (like `BicubicResizer`) unless strictly necessary; prefer using `getResizer` to let the factory determine the optimal algorithm based on the scaling ratio.

### Prompt Snippet
```text
When determining the optimal scaling algorithm in Thumbnailator pipelines, use `ResizerFactory.getResizer(Dimension originalSize, Dimension thumbnailSize)` to obtain the correct `Resizer` for the specific source and target dimensions.
```

### Common Failure Modes
- **Static Context Error**: Attempting to call `getResizer` statically on the interface or factory class instead of an instantiated `ResizerFactory`.
- **Null Arguments**: Passing `null` for either `Dimension` argument, which can lead to a `NullPointerException` when the factory attempts to calculate the scaling ratio.
- **Manual Resizer Instantiation**: Hardcoding a specific resizer (e.g., `new ProgressiveBilinearResizer()`) instead of using the factory, which may result in suboptimal performance or quality if the scaling ratio changes (e.g., upscaling vs. downscaling).

### Fix Code Hint
```java
// Incorrect: Calling statically or hardcoding the resizer
// Resizer resizer = DefaultResizerFactory.getResizer(orig, thumb);
// Resizer resizer = new ProgressiveBilinearResizer();

// Correct: Use the factory instance to get the appropriate resizer
ResizerFactory factory = DefaultResizerFactory.getInstance();
Resizer resizer = factory.getResizer(new Dimension(originalWidth, originalHeight), new Dimension(targetWidth, targetHeight));
```

## API Test: `getResizerFactory`

### Signature
```java
public ResizerFactory getResizerFactory()
```
_Source: source/src/main/java/net/coobird/thumbnailator/ThumbnailParameter.java:942_

_Source doc:_ Returns the {@link ResizerFactory} for obtaining a {@link Resizer} which is to be used when performing the resizing operation to create a thumbnail. @return		The {@link ResizerFactory} to use to obtain the {@link Resizer}.

### Goal
Retrieves the `ResizerFactory` configured within a `ThumbnailParameter`, which is responsible for supplying the `Resizer` algorithm used during image scaling operations.

### Parameters
_None._

### Input
An initialized `ThumbnailParameter` instance, typically constructed using a `ThumbnailParameterBuilder`.

### Output
Returns `ResizerFactory` — the factory object (such as `DefaultResizerFactory`, `FixedResizerFactory`, or a custom implementation) used to obtain the specific `Resizer` (e.g., `BicubicResizer`, `BilinearResizer`) for the resizing pipeline.

### Valid Call Patterns
```java
// Pattern 1: Retrieving the factory when a specific Resizer was configured
ThumbnailParameter param = new ThumbnailParameterBuilder()
    .scale(0.5)
    .resizer(Resizers.BICUBIC)
    .build();

ResizerFactory factory = param.getResizerFactory();
Resizer resizer = factory.getResizer(); // Returns Resizers.BICUBIC

// Pattern 2: Retrieving a custom ResizerFactory
ResizerFactory customFactory = new ResizerFactory() {
    public Resizer getResizer(Dimension originalSize, Dimension thumbnailSize) {
        return Resizers.BILINEAR;
    }
    public Resizer getResizer() {
        return Resizers.BILINEAR;
    }
};

ThumbnailParameter customParam = new ThumbnailParameterBuilder()
    .scale(0.5)
    .resizerFactory(customFactory)
    .build();

ResizerFactory retrievedFactory = customParam.getResizerFactory();
```

### LLM Instruction Prompt
- Call `getResizerFactory()` on a `ThumbnailParameter` instance to inspect the factory responsible for determining the scaling algorithm.
- Do not assume the returned factory is always a `DefaultResizerFactory`; if the parameter was built using `.resizer(Resizer)`, the returned factory will be a fixed factory wrapping that specific resizer.

### Prompt Snippet
```text
To retrieve the configured scaling algorithm factory from a `ThumbnailParameter`, call `param.getResizerFactory()`. This returns a `ResizerFactory` which can be used to obtain the specific `Resizer` (e.g., bicubic or bilinear) that the pipeline will use.
```

### Common Failure Modes
- **NullPointerException**: Attempting to call `getResizerFactory()` on an uninitialized or null `ThumbnailParameter` reference.
- **Misunderstanding Factory vs. Resizer**: Expecting this method to return a `Resizer` directly. It returns a `ResizerFactory`, which must then be queried (via `getResizer()` or `getResizer(Dimension, Dimension)`) to get the actual scaling algorithm.

### Fix Code Hint
```java
// Incorrect: Expecting a Resizer directly
// Resizer resizer = param.getResizerFactory(); 

// Correct: Querying the factory for the Resizer
ResizerFactory factory = param.getResizerFactory();
Resizer resizer = factory.getResizer();
```

## API Test: `getSink`

### Signature
```java
public OutputStream getSink()
public T getSink()
public File getSink()
public BufferedImage getSink()
```
_Source: source/src/main/java/net/coobird/thumbnailator/tasks/io/OutputStreamImageSink.java:268  (+3 more definition site/overload)_

### Goal
Retrieves the destination object containing the processed thumbnail from an `ImageSink` after an image processing task has completed.

### Parameters
_None._

### Input
An instantiated `ImageSink` (such as `BufferedImageSink`, `FileImageSink`, or `OutputStreamImageSink`) that has already received a processed image. The caller must ensure the image has been stored to the sink, either manually via the sink's `write()` method or by executing a `ThumbnailTask` (e.g., `SourceSinkThumbnailTask`) that routes its output to this sink.

### Output
Returns `OutputStream` (or `BufferedImage`, `File`, or generic `T` depending on the specific `ImageSink` implementation) — The underlying destination object that holds the generated thumbnail.

### Valid Call Patterns
```java
// Pattern 1: Retrieving a BufferedImage from a sink after task execution
ThumbnailParameter param = new ThumbnailParameterBuilder().size(50, 50).build();
InputStream is = TestUtils.getResourceStream("Thumbnailator/grid.png");
InputStreamImageSource source = new InputStreamImageSource(is);
BufferedImageSink destination = new BufferedImageSink();

// Execute the task to write to the destination sink
Thumbnailator.createThumbnail(
        new SourceSinkThumbnailTask<InputStream, BufferedImage>(param, source, destination)
);

// Retrieve the processed thumbnail
BufferedImage thumbnail = destination.getSink();

// Pattern 2: Retrieving after a direct write
BufferedImage img = new BufferedImage(10, 10, BufferedImage.TYPE_INT_ARGB);
BufferedImageSink sink = new BufferedImageSink();
sink.write(img);

BufferedImage result = sink.getSink();
```

### LLM Instruction Prompt
- ALWAYS ensure that a thumbnail has been written to the `ImageSink` (e.g., via `Thumbnailator.createThumbnail(...)` or `sink.write(...)`) before calling `getSink()`.
- DO NOT call `getSink()` on a newly instantiated sink that has not yet processed an image, as this violates preconditions and will crash the pipeline.
- Match the expected return type to the specific `ImageSink` implementation being used (e.g., `BufferedImageSink` returns `BufferedImage`, `OutputStreamImageSink` returns `OutputStream`).

### Prompt Snippet
```text
When extracting the result from an ImageSink using `getSink()`, you must first execute the image pipeline or call `write()` on the sink. Calling `getSink()` prematurely throws an IllegalStateException.
```

### Common Failure Modes
- **`IllegalStateException`**: Thrown if `getSink()` is called before a thumbnail has been stored or written to the sink.

### Fix Code Hint
```java
// WRONG: Calling getSink() before the image is processed and written
BufferedImageSink sink = new BufferedImageSink();
BufferedImage img = sink.getSink(); // Throws IllegalStateException

// CORRECT: Execute the task to populate the sink first
BufferedImageSink sink = new BufferedImageSink();
Thumbnailator.createThumbnail(new SourceSinkThumbnailTask<>(param, source, sink));
BufferedImage img = sink.getSink();
```

## API Test: `getSize`

### Signature
```java
public Dimension getSize()
public Size getSize()
```
_Source: source/src/main/java/net/coobird/thumbnailator/ThumbnailParameter.java:808  (+1 more definition site/overload)_

_Source doc:_ Returns the size of the thumbnail. <p> Returns {@code null} if the scaling factor is set rather than the explicit thumbnail size. @return		The size of the thumbnail.

### Goal
Retrieves the explicitly configured dimensions of the thumbnail, returning `null` if a relative scaling factor was used instead.

### Parameters
_None._

### Input
An instantiated configuration object (such as `ThumbnailParameter`) that dictates the resizing behavior of the image processing pipeline.

### Output
Returns `Dimension` — the explicit width and height of the thumbnail in pixels, or `null` if the pipeline relies on a relative scaling factor rather than an absolute size. (The overload returns a `Size` interface implementation from `net.coobird.thumbnailator.geometry`).

### Valid Call Patterns
```java
// Extracted from ThumbnailatorTest.java
ArgumentCaptor<ThumbnailParameter> ac = ArgumentCaptor.forClass(ThumbnailParameter.class);
verify(rename).apply(eq(f.getName()), ac.capture());

ThumbnailParameter parameter = ac.getValue();
Dimension size = parameter.getSize();

if (size != null) {
    assertEquals(new Dimension(50, 50), size);
}
```

### LLM Instruction Prompt
- When inspecting a `ThumbnailParameter` or similar configuration object, you MUST check if `getSize()` returns `null` before accessing its fields (`width`, `height`). It will return `null` if the user configured the builder with a scaling factor (e.g., `.scale(...)`) rather than explicit dimensions (e.g., `.size(...)`).

### Prompt Snippet
```text
Always check getSize() for null before accessing Dimension fields; it returns null if the thumbnail uses a scaling factor instead of an explicit size.
```

### Common Failure Modes
- **`NullPointerException`**: Attempting to directly access `getSize().width` or `getSize().height` without a null check when the underlying pipeline was configured using a scaling factor instead of absolute dimensions.

### Fix Code Hint
```java
Dimension size = parameter.getSize();
if (size != null) {
    int width = size.width;
    int height = size.height;
    // Process explicit dimensions
} else {
    // Fallback logic: the image is being resized via a scaling factor
}
```

## API Test: `getSource`

### Signature
```java
public InputStream getSource()
public File getSource()
public S getSource()
public abstract S getSource()
public BufferedImage getSource()
public T getSource()
public URL getSource()
```
_Source: source/src/main/java/net/coobird/thumbnailator/tasks/StreamThumbnailTask.java:91  (+8 more definition site/overload)_

### Goal
Retrieves the underlying source object (such as a `File`, `InputStream`, `URL`, or `BufferedImage`) from which the original image is read by an `ImageSource` or `ThumbnailTask`.

### Parameters
_None._

### Input
An instantiated `ImageSource<S>` (e.g., `FileImageSource`, `InputStreamImageSource`, `URLImageSource`, `BufferedImageSource`) or a `ThumbnailTask` that wraps an image source. The caller must have already provided the underlying source object during the instantiation of the source or task.

### Output
Returns `InputStream` — (or the generic type `S` such as `File`, `URL`, or `BufferedImage`, depending on the specific implementation) representing the original source object provided when the `ImageSource` or task was created.

### Valid Call Patterns
```java
// Example based on FileImageSourceTest
File inputFile = new File("grid.png");
FileImageSource source = new FileImageSource(inputFile);

// Read the image into memory
source.read();

// Retrieve the underlying source object (e.g., for verification or cleanup)
File originalFile = source.getSource();
boolean isDeleted = originalFile.delete();
```

### LLM Instruction Prompt
- When interacting with Thumbnailator's `ImageSource` or `ThumbnailTask` abstractions, use `getSource()` to retrieve the underlying input object. Ensure the assigned variable matches the generic type `S` of the specific source implementation (e.g., `File` for `FileImageSource`, `InputStream` for `InputStreamImageSource`). Do not attempt to read from an `InputStream` returned by `getSource()` if `read()` has already been called, as the stream will be consumed.

### Prompt Snippet
```text
Use `source.getSource()` to retrieve the underlying input object from an `ImageSource` or `ThumbnailTask`. Match the return type to the specific implementation (e.g., `File` for `FileImageSource`). If the source is an `InputStream`, do not reuse it after `source.read()` is called.
```

### Common Failure Modes
- **Type Mismatch / ClassCastException**: Assigning the result of `getSource()` to the wrong type when using a raw `ImageSource` or `ThumbnailTask` instead of the properly parameterized generic type.
- **Stream Exhaustion**: Retrieving an `InputStream` via `getSource()` and attempting to read from it after `source.read()` has already been executed. The underlying Java Image I/O mechanism consumes the stream during the read phase.

### Fix Code Hint
```java
// WRONG: Using raw types and casting blindly
ImageSource rawSource = new InputStreamImageSource(myStream);
File f = (File) rawSource.getSource(); // Throws ClassCastException

// RIGHT: Use the correct specific implementation and generic type
InputStreamImageSource streamSource = new InputStreamImageSource(myStream);
InputStream originalStream = streamSource.getSource();

FileImageSource fileSource = new FileImageSource(new File("image.jpg"));
File originalFile = fileSource.getSource();
```

## API Test: `getSourceRegion`

### Signature
```java
public Region getSourceRegion()
```
_Source: source/src/main/java/net/coobird/thumbnailator/ThumbnailParameter.java:967_

_Source doc:_ Returns the region of the source image to use when creating a thumbnail, represented by a {@link Region} object. @return		The {@code Region} object representing the source region to use when creating a thumbnail. <p> A value of {@code null} indicates that the entire source image should be used to create the thumbnail.

### Goal
Retrieves the specific rectangular area of the original image designated for thumbnail generation, or `null` if the entire image is to be used.

### Parameters
_None._

### Input
An instantiated `ThumbnailParameter` object that holds the configuration for a thumbnail generation task. 

### Output
Returns `Region` — The `Region` object representing the cropped area of the source image to process, or `null` indicating that the full source image will be used.

### Valid Call Patterns
```java
// Inferred from the signature (not verified by tests/README)
Region sourceRegion = thumbnailParameter.getSourceRegion();

if (sourceRegion == null) {
    // The entire source image is used
} else {
    // A specific region (crop) of the source image is used
}
```

### LLM Instruction Prompt
- When calling `getSourceRegion()`, you MUST handle the `null` return case. A `null` value is a valid, expected state indicating that no specific source region (crop) was defined and the entire source image should be processed.
- Do not attempt to instantiate `ThumbnailParameter` directly in standard fluent workflows; this method is typically used when inspecting the parameters of a custom `ThumbnailTask` or `Pipeline`.

### Prompt Snippet
```text
Always check the result of `getSourceRegion()` for `null` before invoking methods on the returned `Region` object, as `null` signifies the entire image is targeted.
```

### Common Failure Modes
- **NullPointerException**: Occurs if the caller attempts to invoke methods (like getting dimensions or coordinates) on the returned `Region` without first checking if it is `null`.

### Fix Code Hint
```java
Region region = thumbnailParameter.getSourceRegion();
if (region != null) {
    // Safely interact with the defined Region
    // e.g., apply specific geometry calculations
} else {
    // Fallback to using the dimensions of the entire source image
}
```

## API Test: `getSupportedOutputFormatTypes`

### Signature
```java
public static List<String> getSupportedOutputFormatTypes(String format)
```
_Source: source/src/main/java/net/coobird/thumbnailator/util/ThumbnailatorUtils.java:97_

_Source doc:_ Returns a {@link List} of supported output formats types for a specified output format. @param format	The output format. @return		A {@link List} of supported output formats types. If no formats types are supported, or if compression is not supported for the specified format, then an empty list is returned.

### Goal
Queries the underlying Java Image I/O system to return a list of supported output format types (such as compression schemes) for a specified image format.

### Parameters
- `format` (`String`): The name of the output image format to query (e.g., `"JPEG"`, `"PNG"`, `"TIFF"`).

### Input
A string representing the target image format. The format relies entirely on the host JVM's standard Image I/O capabilities, so the provided string should match a format registered with the JVM's `ImageIO` writers.

### Output
Returns `List<String>` — A list of supported output format types for the specified format. If no format types are supported, or if compression is not supported for the specified format by the underlying Image I/O writer, an empty list is returned.

### Valid Call Patterns
```java
// Inferred from the signature (not verified by tests)
List<String> jpegFormatTypes = ThumbnailatorUtils.getSupportedOutputFormatTypes("JPEG");

if (!jpegFormatTypes.isEmpty()) {
    System.out.println("Supported types: " + jpegFormatTypes);
}
```

### LLM Instruction Prompt
- Use `ThumbnailatorUtils.getSupportedOutputFormatTypes(String format)` to dynamically discover available format types (like compression modes) for a specific image format before configuring advanced output parameters.
- Always handle the case where the returned list is empty, as formats that do not support compression or lack specific format types in the host JVM's Image I/O will return an empty list.
- Do not assume specific formats (like WebP or TIFF) are universally supported; support depends entirely on the host JVM's environment.

### Prompt Snippet
```text
To check supported compression or format types for an output format in Thumbnailator, use `ThumbnailatorUtils.getSupportedOutputFormatTypes("formatName")`. It returns a `List<String>` of types, or an empty list if none are supported by the JVM's Image I/O.
```

### Common Failure Modes
- **Assuming a populated list**: Blindly accessing elements (e.g., `types.get(0)`) without checking if the list is empty will cause an `IndexOutOfBoundsException` if the format does not support compression types (e.g., standard PNG or BMP in some JVMs).
- **Unsupported formats**: Passing a format string that the JVM's Image I/O does not recognize will yield an empty list, which might be misinterpreted as a valid but type-less format if not carefully validated.

### Fix Code Hint
```java
List<String> formatTypes = ThumbnailatorUtils.getSupportedOutputFormatTypes(targetFormat);
if (formatTypes != null && !formatTypes.isEmpty()) {
    // Safe to use a format type
    String selectedType = formatTypes.get(0);
} else {
    // Fallback: do not specify a format type/compression type
}
```

## API Test: `getSupportedOutputFormats`

### Signature
```java
public static List<String> getSupportedOutputFormats()
```
_Source: source/src/main/java/net/coobird/thumbnailator/util/ThumbnailatorUtils.java:55_

_Source doc:_ Returns a {@link List} of supported output formats. @return		A {@link List} of supported output formats. If no formats are supported, an empty list is returned.

### Goal
Retrieves a list of image output format names supported by the host JVM's underlying Java Image I/O implementation.

### Parameters
_None._

### Input
No input parameters. The available formats depend entirely on the host JVM's registered Image I/O writers and do not require any external dependencies.

### Output
Returns `List<String>` — A list of supported output format names (e.g., "jpg", "png", "gif"). If no formats are supported by the JVM, an empty list is returned.

### Valid Call Patterns
```java
// Inferred from signature (not verified)
List<String> supportedFormats = net.coobird.thumbnailator.util.ThumbnailatorUtils.getSupportedOutputFormats();

if (supportedFormats.contains("png")) {
    System.out.println("PNG output is supported.");
}
```

### LLM Instruction Prompt
- When dynamically setting an output format via `Thumbnails.Builder.outputFormat(String)`, use `ThumbnailatorUtils.getSupportedOutputFormats()` to verify the format is supported by the host JVM's Image I/O. This prevents an `UnsupportedFormatException` from being thrown during pipeline execution.

### Prompt Snippet
```text
Verify format support using net.coobird.thumbnailator.util.ThumbnailatorUtils.getSupportedOutputFormats() before calling outputFormat() to prevent UnsupportedFormatException on environments lacking specific Image I/O plugins.
```

### Common Failure Modes
- **Hardcoding unsupported formats**: Requesting an output format (e.g., "tiff", "webp", or "bmp") that the specific headless JVM does not support natively, which causes Thumbnailator to throw an `UnsupportedFormatException` when the pipeline terminates.
- **Assuming uniform cross-JVM support**: Failing to check this list when deploying across different Java versions or vendors, where the available Image I/O plugins may vary.

### Fix Code Hint
```java
String desiredFormat = "tiff";
List<String> supported = net.coobird.thumbnailator.util.ThumbnailatorUtils.getSupportedOutputFormats();

// Fallback to a universally supported format like "png" if the desired format is missing
String formatToUse = supported.contains(desiredFormat) ? desiredFormat : "png";

Thumbnails.of(new File("input.jpg"))
    .size(640, 480)
    .outputFormat(formatToUse)
    .toFile(new File("output." + formatToUse));
```

## API Test: `getTag`

### Signature
```java
public int getTag()
```
_Source: source/src/main/java/net/coobird/thumbnailator/util/exif/IfdStructure.java:63_

_Source doc:_ Returns the tag element in the IFD structure. @return		An integer representation of the tag element. Should be a value between 0x00 to 0xFF.

### Goal
Retrieves the integer representation of the tag element from an Exif Image File Directory (IFD) structure.

### Parameters
_None._

### Input
A valid instance of `IfdStructure` obtained during Exif metadata parsing.

### Output
Returns `int` — An integer representation of the Exif tag element. According to the source documentation, this should be a value between `0x00` and `0xFF`.

### Valid Call Patterns
```java
// Inferred from signature (no verified examples available in project context)
int tagValue = ifdStructure.getTag();
```

### LLM Instruction Prompt
- When inspecting parsed Exif metadata, use `getTag()` on an `IfdStructure` instance to retrieve the raw integer identifier of the tag. 
- Expect the returned integer to be bounded between `0x00` and `0xFF`. 
- Do not attempt to call this method expecting a String, Enum, or standard 16-bit Exif tag constant without verifying the value range.

### Prompt Snippet
```text
Use `ifdStructure.getTag()` to extract the integer tag element (0x00 to 0xFF) from an Exif IFD structure.
```

### Common Failure Modes
- **Type Mismatch in Comparisons**: Comparing the returned integer to standard 16-bit Exif tag constants (which often exceed `0xFF`) without accounting for the documented `0x00` to `0xFF` range constraint.
- **NullPointerException**: Attempting to call `getTag()` on an uninitialized or null `IfdStructure` reference if Exif parsing failed or was bypassed.

### Fix Code Hint
```java
if (ifdStructure != null) {
    int tag = ifdStructure.getTag();
    // Ensure comparisons align with the 0x00 to 0xFF expected range
    if (tag == 0x01) { 
        // Handle specific tag logic
    }
}
```

## API Test: `getType`

### Signature
```java
public int getType()
public IfdType getType()
```
_Source: source/src/main/java/net/coobird/thumbnailator/ThumbnailParameter.java:850  (+1 more definition site/overload)_

_Source doc:_ Returns the type of image. The value returned is the constant used for image types of {@link BufferedImage}. @return		The type of the image.

### Goal
Retrieves the configured `BufferedImage` type constant for a thumbnail processing task (`ThumbnailParameter`), or the IFD (Image File Directory) type during Exif metadata parsing.

### Parameters
_None._

### Input
A valid `ThumbnailParameter` instance containing image generation settings, an Exif directory object, or a `BufferedImage` generated by a Thumbnailator in-memory sink.

### Output
Returns `int` — An integer representing the image type. This corresponds to standard `BufferedImage.TYPE_*` constants (e.g., `BufferedImage.TYPE_INT_ARGB`), or Thumbnailator-specific configuration constants such as `ThumbnailParameter.ORIGINAL_IMAGE_TYPE` (-1) or `ThumbnailParameter.DEFAULT_IMAGE_TYPE` (2). The overload returns an `IfdType` enum when inspecting Exif metadata directories.

### Valid Call Patterns
```java
// Verifying the image type preserved by Thumbnailator's in-memory sink
BufferedImage img = new BufferedImage(200, 200, BufferedImage.TYPE_BYTE_INDEXED);

BufferedImage thumbnail = Thumbnails.of(img)
        .size(200, 200)
        .asBufferedImage();

// Retrieves the type constant (e.g., BufferedImage.TYPE_BYTE_INDEXED)
int type = thumbnail.getType(); 
```

### LLM Instruction Prompt
- When verifying the output of an in-memory Thumbnailator pipeline (`asBufferedImage()`) or inspecting a `ThumbnailParameter` configuration, use `getType()` to retrieve the integer constant representing the image's color model and layout. Do not confuse this integer with the file format extension (e.g., "jpg").

### Prompt Snippet
```text
Use `getType()` to retrieve the `BufferedImage.TYPE_*` integer constant of the generated image or the `ThumbnailParameter` configuration. Compare the result strictly against `BufferedImage` constants (e.g., `BufferedImage.TYPE_INT_ARGB`) or `ThumbnailParameter.ORIGINAL_IMAGE_TYPE`, never against string format names.
```

### Common Failure Modes
- **Confusing image type with output format**: Attempting to use `getType()` to determine if an image is a JPEG or PNG. `getType()` returns an integer representing the memory layout (like `TYPE_INT_ARGB`), not the encoded file format.
- **Unmapped original types**: If the pipeline is configured to use `ThumbnailParameter.ORIGINAL_IMAGE_TYPE` (-1), calling `getType()` on the parameter object will return `-1`, which does not map to a valid `BufferedImage` type until the pipeline resolves the source image.

### Fix Code Hint
```java
// WRONG: Comparing getType() to a file format string
// if (thumbnail.getType().equals("jpg")) { ... }

// RIGHT: Comparing getType() to a BufferedImage integer constant
if (thumbnail.getType() == BufferedImage.TYPE_INT_ARGB) {
    // Image has an alpha channel
}
```

## API Test: `getValue`

### Signature
```java
public Object getValue()
```
_Source: source/src/main/java/net/coobird/thumbnailator/resizers/configurations/Dithering.java:75  (+4 more definition site/overload)_

### Goal
Retrieves the underlying Java 2D rendering hint value associated with a Thumbnailator configuration enum (such as `Dithering`, `Antialiasing`, or `AlphaInterpolation`).

### Parameters
_None._

### Input
An instance of a `ResizerConfiguration` enum implementation (e.g., `Dithering.ENABLE`, `Antialiasing.ON`, `AlphaInterpolation.QUALITY`) from which the raw rendering hint is needed.

### Output
Returns `Object` — The raw Java 2D rendering hint value (typically a constant from `java.awt.RenderingHints`) that corresponds to the specific Thumbnailator configuration.

### Valid Call Patterns
```java
// Inferred from the signature and API facts (not verified in provided examples)
// Note: The provided test suite examples demonstrate Mockito's ArgumentCaptor.getValue(), 
// not Thumbnailator's ResizerConfiguration.getValue().
Dithering ditheringConfig = Dithering.ENABLE;
Object hintValue = ditheringConfig.getValue();

// Typical usage when bridging to standard Java 2D APIs:
// graphics2D.setRenderingHint(RenderingHints.KEY_DITHERING, ditheringConfig.getValue());
```

### LLM Instruction Prompt
- When bridging Thumbnailator's `ResizerConfiguration` enums (like `Antialiasing`, `Dithering`, `AlphaInterpolation`) with standard Java 2D `Graphics2D` objects, call `getValue()` to extract the raw `RenderingHints` value. 
- Do not confuse this API with Mockito's `ArgumentCaptor.getValue()`, which shares the same signature and appears frequently in Thumbnailator's test suite for asserting `ThumbnailParameter` states.

### Prompt Snippet
```text
Use `configEnum.getValue()` to extract the raw `java.awt.RenderingHints` object from a Thumbnailator `ResizerConfiguration` enum (e.g., `Dithering.ENABLE.getValue()`).
```

### Common Failure Modes
- **ClassCastException**: The returned value is an `Object`. Attempting to cast it to a specific type other than what `java.awt.RenderingHints` defines for that specific key will cause a runtime crash. It is safest to pass the `Object` directly to `Graphics2D.setRenderingHint(Key, Object)`.
- **Context Confusion in Tests**: Mistaking this method for Mockito's `ArgumentCaptor.getValue()` when writing tests. While both share the same signature, calling `getValue()` on a Thumbnailator configuration enum returns a rendering hint, whereas calling it on an `ArgumentCaptor` returns the captured mock argument.

### Fix Code Hint
```java
// Incorrect: Assuming getValue() returns a strongly-typed Thumbnailator object
// Dithering d = (Dithering) Antialiasing.ON.getValue(); 

// Correct: Treating the result as an opaque Object for Java 2D
Object rawHint = Antialiasing.ON.getValue();
// graphics2D.setRenderingHint(RenderingHints.KEY_ANTIALIASING, rawHint);
```

## API Test: `getWidthScalingFactor`

### Signature
```java
public double getWidthScalingFactor()
```
_Source: source/src/main/java/net/coobird/thumbnailator/ThumbnailParameter.java:826_

_Source doc:_ Returns the scaling factor to apply to the width when creating the thumbnail. <p> Returns {@link Double#NaN} if the thumbnail size is set rather than the scaling factor. @return		The width scaling factor for the thumbnail. @since	0.3.10

### Goal
Returns the scaling factor applied to the width of the original image when generating a thumbnail.

### Parameters
_None._

### Input
A valid `ThumbnailParameter` instance, typically constructed via a `ThumbnailParameterBuilder` or extracted from an image processing pipeline configuration.

### Output
Returns `double` — the width scaling factor for the thumbnail, or `Double.NaN` if the thumbnail was configured using absolute dimensions (e.g., via `size(int, int)`) rather than a scaling factor.

### Valid Call Patterns
```java
// Example based on the project's test suite demonstrating the NaN behavior when size is used
ThumbnailParameter param = new ThumbnailParameterBuilder()
        .size(100, 100)
        .build();

double widthScale = param.getWidthScalingFactor();
boolean isScaleSet = !Double.isNaN(widthScale);
```

### LLM Instruction Prompt
- When retrieving the width scaling factor from a `ThumbnailParameter`, you MUST check if the result is `Double.NaN` using `Double.isNaN()`. The method returns `NaN` if the thumbnail pipeline was configured with absolute dimensions (e.g., `.size(w, h)`) instead of a scale factor. Do not use the return value in mathematical operations without this check to prevent `NaN` propagation.

### Prompt Snippet
```text
Always check `Double.isNaN(param.getWidthScalingFactor())` before using the returned scale factor. Thumbnailator returns `NaN` if the thumbnail was configured with absolute dimensions (`size()`) rather than a relative scale (`scale()`).
```

### Common Failure Modes
- **`NaN` Propagation in Math Operations**: Assuming the method always returns a valid numeric scale factor and using it directly in calculations. If the `ThumbnailParameter` was built using `.size(w, h)` instead of `.scale(factor)`, the method returns `Double.NaN`, which will silently corrupt subsequent floating-point math.

### Fix Code Hint
```java
double widthScale = param.getWidthScalingFactor();
if (Double.isNaN(widthScale)) {
    // Handle the case where absolute size was used instead of a scaling factor
    Dimension size = param.getSize();
    // ... fallback logic using size.width ...
} else {
    // Safe to use widthScale
    int newWidth = (int) (originalWidth * widthScale);
}
```

## API Test: `height`

### Signature
```java
public Builder<T> height(int height)
public BufferedImageBuilder height(int height)
```
_Source: source/src/main/java/net/coobird/thumbnailator/Thumbnails.java:905  (+1 more definition site/overload)_

_Source doc:_ Sets the height of the thumbnail. <p> The thumbnail will have the dimensions constrained by the specified height, and the aspect ratio of the original image will be preserved by the thumbnail. <p> Once this method is called, calling the {@link #size(int, int)} or the {@link #scale(double)} method will result in an {@link IllegalStateException}. <p> Calling this method multiple times will result in an {@link IllegalStateException} to be thrown. @param height		The height of the thumbnail. @return				Reference to this object. @since 	0.3.5

### Goal
Sets the target height for the generated thumbnail while automatically calculating the width to preserve the original image's aspect ratio.

### Parameters
- `height` (`int`): The target height of the thumbnail in pixels.

### Input
A `Thumbnails.Builder` instance initialized with an image source (e.g., `BufferedImage`, `File`, `InputStream`). The builder must be in a state where no other mutually exclusive resizing operations (like `size`, `scale`, or a previous `height` call) have been applied.

### Output
Returns `Builder<T>` — The same builder instance for fluent chaining, now configured to resize the image to the specified height before routing to a sink.

### Valid Call Patterns
```java
// Create a dummy in-memory image for testing
BufferedImage img = new BufferedImageBuilder(200, 200).build();

// Resize the image to a height of 50 pixels, preserving aspect ratio
BufferedImage thumbnail = Thumbnails.of(img)
        .height(50)
        .asBufferedImage();
```

### LLM Instruction Prompt
- When a user requests to resize an image to a specific height while preserving the aspect ratio, use the `height(int)` method.
- **CRITICAL PRECONDITION**: You MUST NOT call `size(int, int)`, `scale(double)`, or `height(int)` again on the same builder instance after calling `height(int)`. Doing so will immediately throw an `IllegalStateException`. Choose exactly one resizing strategy per pipeline.

### Prompt Snippet
```text
Use `.height(int)` on the `Thumbnails.Builder` to resize an image to a specific height while automatically preserving its aspect ratio. Never combine `.height()` with `.size()`, `.scale()`, or additional `.height()` calls on the same builder, as this throws an IllegalStateException.
```

### Common Failure Modes
- **`IllegalStateException` (Multiple height calls)**: Calling `.height(int)` more than once on the same builder instance.
- **`IllegalStateException` (Conflicting resize strategies)**: Calling `.size(int, int)` or `.scale(double)` on a builder that has already been configured with `.height(int)`.

### Fix Code Hint
```java
// BAD: Throws IllegalStateException due to conflicting or duplicate resize rules
Thumbnails.of(img)
        .height(50)
        .size(50, 50) // CRASH
        .asBufferedImage();

Thumbnails.of(img)
        .height(50)
        .height(50) // CRASH
        .asBufferedImage();

// GOOD: Apply exactly one resizing strategy
Thumbnails.of(img)
        .height(50)
        .asBufferedImage();
```

## API Test: `if`

### Signature
```java
else if (thumbWidth > origWidth && thumbHeight > origHeight)
```
_Source: source/src/main/java/net/coobird/thumbnailator/resizers/DefaultResizerFactory.java:139_

### Goal
Acts as a native Java conditional control flow statement. In the context of the extracted signature, it evaluates whether the requested thumbnail dimensions (`thumbWidth`, `thumbHeight`) strictly exceed the original image dimensions (`origWidth`, `origHeight`), which is used internally by `DefaultResizerFactory` to determine the appropriate upscaling algorithm.

### Parameters
- `origHeight` (`thumbWidth > origWidth && thumbHeight >`): The original height of the source image, which is evaluated against the target thumbnail height to determine if upscaling is required. *(Note: The parameter type is a parser artifact derived from the conditional statement).*

### Input
Standard Java boolean expressions. For the specific signature extracted from `DefaultResizerFactory`, it requires the target thumbnail dimensions (`thumbWidth`, `thumbHeight`) and the original image dimensions (`origWidth`, `origHeight`) to be available in the local scope. 

### Output
Returns `else` — Represents the execution branch taken when the preceding `if` condition is false and this specific upscaling condition evaluates to true.

### Valid Call Patterns
```java
// 1. Authoritative usage from the test suite (custom Rename strategy)
if (name.endsWith(".gif")) {
    return "thumbnail." + name + ".foobar";
}

// 2. Inferred from the signature (not verified - internal factory logic)
else if (thumbWidth > origWidth && thumbHeight > origHeight) {
    // internal upscaling resizer selection
}
```

### LLM Instruction Prompt
- Recognize that `if` is a native Java language keyword, not a callable Thumbnailator API method. The provided signature reflects an internal upscaling check from `DefaultResizerFactory`.
- Do not attempt to invoke `if` as a function. 
- When writing custom Thumbnailator components (such as overriding the `apply` method in a `Rename` instance), use standard Java `if` statements to branch logic based on file extensions or `ThumbnailParameter` values.
- Rely on the `Thumbnails.Builder` fluent API (e.g., `size(int, int)`) to handle dimension checking and resizer selection automatically.

### Prompt Snippet
```text
// Note: 'if' is a Java control flow statement, not a Thumbnailator method.
// The signature 'else if (thumbWidth > origWidth && thumbHeight > origHeight)' 
// is handled internally by DefaultResizerFactory during Thumbnails.of().size() calls.
```

### Common Failure Modes
- **Treating `if` as a library method**: Attempting to call `if(...)` as a static or instance method on a Thumbnailator class will result in a syntax or compilation error.
- **Manual Resizer Dimension Checking**: Attempting to manually extract original dimensions to replicate this `if` check before resizing. Thumbnailator's `Thumbnails.Builder` and `ResizerFactory` handle these dimension comparisons and algorithm selections automatically.

### Fix Code Hint
```java
// Incorrect: Attempting to manually check dimensions using the extracted signature
// else if (thumbWidth > origWidth && thumbHeight > origHeight) { ... }

// Correct: Let Thumbnailator handle the upscaling condition internally
Thumbnails.of(new File("source.jpg"))
    .size(800, 600) // DefaultResizerFactory automatically evaluates the dimensions
    .toFile(new File("thumbnail.jpg"));
```

## API Test: `imageType`

### Signature
```java
public Builder<T> imageType(int type)
public ThumbnailParameterBuilder imageType(int type)
public BufferedImageBuilder imageType(int imageType)
public ThumbnailMaker imageType(int imageType)
```
_Source: source/src/main/java/net/coobird/thumbnailator/Thumbnails.java:1283  (+3 more definition site/overload)_

_Source doc:_ Sets the image type of the thumbnail. <p> Calling this method to set this parameter is optional. <p> Calling this method multiple times will result in an {@link IllegalStateException} to be thrown. @param type			The image type of the thumbnail. @return				Reference to this object.

### Goal
Sets the underlying `java.awt.image.BufferedImage` type (e.g., ARGB, RGB, grayscale) to be used when constructing the generated thumbnail in the processing pipeline.

### Parameters
- `type` (`int`): The integer constant representing the desired image type. This should be a standard `BufferedImage` type constant (e.g., `BufferedImage.TYPE_INT_ARGB`, `BufferedImage.TYPE_BYTE_GRAY`) or `ThumbnailParameter.ORIGINAL_IMAGE_TYPE` (-1) to match the source image.

### Input
The caller must have an active builder pipeline (e.g., initiated via `Thumbnails.of(...)`). The provided integer must be a valid `BufferedImage` type constant. This method is optional; if omitted, Thumbnailator defaults to `ThumbnailParameter.DEFAULT_IMAGE_TYPE` (2, which corresponds to `BufferedImage.TYPE_INT_ARGB`).

### Output
Returns `Builder<T>` (or the specific builder subclass like `BufferedImageBuilder` or `ThumbnailParameterBuilder`) — a reference to the current builder object to allow continued fluent method chaining.

### Valid Call Patterns
```java
BufferedImage img = new BufferedImage(200, 200, BufferedImage.TYPE_BYTE_GRAY);

BufferedImage thumbnail = Thumbnails.of(img)
        .size(200, 200)
        .imageType(BufferedImage.TYPE_BYTE_GRAY)
        .asBufferedImage();

assertEquals(BufferedImage.TYPE_BYTE_GRAY, thumbnail.getType());
```

### LLM Instruction Prompt
- Use standard `java.awt.image.BufferedImage` constants (e.g., `BufferedImage.TYPE_INT_ARGB`, `BufferedImage.TYPE_BYTE_GRAY`) or `ThumbnailParameter.ORIGINAL_IMAGE_TYPE` (-1) for the `type` argument.
- NEVER call `imageType(...)` more than once on the same builder instance; doing so will throw an `IllegalStateException`.
- Remember that setting this parameter is optional. Only invoke it if a specific output color model or memory layout is required (e.g., forcing grayscale or dropping the alpha channel).

### Prompt Snippet
```text
`imageType(int type)` sets the `BufferedImage` type for the output thumbnail (e.g., `BufferedImage.TYPE_BYTE_GRAY`). Optional. Throws `IllegalStateException` if called multiple times on the same builder. Returns the builder for chaining.
```

### Common Failure Modes
- **`IllegalStateException`**: Thrown if `imageType(int)` is called multiple times within the same fluent builder chain.
- **Unexpected Color/Transparency Loss**: Occurs if the chosen `imageType` does not support an alpha channel (e.g., `BufferedImage.TYPE_INT_RGB` or `BufferedImage.TYPE_BYTE_GRAY`) but the source image or applied filters (like `Watermark` or `Canvas`) require transparency.

### Fix Code Hint
```java
// WRONG: Calling imageType multiple times throws IllegalStateException
BufferedImage thumbnail = Thumbnails.of(img)
    .size(200, 200)
    .imageType(BufferedImage.TYPE_INT_RGB)
    .imageType(BufferedImage.TYPE_BYTE_GRAY) // Crashes here
    .asBufferedImage();

// RIGHT: Call imageType exactly once with the desired BufferedImage constant
BufferedImage thumbnail = Thumbnails.of(img)
    .size(200, 200)
    .imageType(BufferedImage.TYPE_BYTE_GRAY)
    .asBufferedImage();
```

## API Test: `init`

### Signature
```java
static void init()
```
_Source: source/src/main/java/net/coobird/thumbnailator/util/Configurations.java:108_

_Source doc:_ This method will initialize configurations from {@code thumbnailator.properties} on the classpath. <p> Implementation note: {@code thumbnailator.properties} is searched from the class loader associated with the current thread, rather than the system class loader. <p> This is intended only to be called from tests.

### Goal
Initializes library configurations by loading `thumbnailator.properties` from the classpath, strictly intended for use within test environments.

### Parameters
_None._

### Input
A `thumbnailator.properties` file located on the classpath. The file must be accessible via the class loader associated with the current thread (rather than the system class loader).

### Output
Returns `void` — updates the internal configuration state of the library based on the loaded properties file.

### Valid Call Patterns
```java
/* 
 * Note: This example is inferred from the signature as no verbatim 
 * examples were found in the project context. 
 */
Configurations.init();
```

### LLM Instruction Prompt
- Restrict usage of `Configurations.init()` exclusively to test harnesses and setup methods.
- Ensure `thumbnailator.properties` is placed in the test classpath (e.g., `src/test/resources/`).
- Do not invoke this method in production image-processing pipelines or standard `Thumbnails.Builder` workflows.

### Prompt Snippet
```text
`Configurations.init()` loads `thumbnailator.properties` from the thread context class loader. It is strictly intended for test environments and must not be used in production code.
```

### Common Failure Modes
- **Missing Properties File**: If `thumbnailator.properties` is not on the classpath or is invisible to the current thread's class loader, the configurations will not be initialized as expected.
- **Production Usage**: Calling this method outside of a test context violates the API's intended design and may cause unexpected global configuration state in production environments.

### Fix Code Hint
```java
// Ensure this is only called within a test setup method (e.g., JUnit @Before)
// and that thumbnailator.properties exists in the test classpath.
@Before
public void setUp() {
    Configurations.init();
}
```

## API Test: `isKeepAspectRatio`

### Signature
```java
public boolean isKeepAspectRatio()
```
_Source: source/src/main/java/net/coobird/thumbnailator/ThumbnailParameter.java:861_

_Source doc:_ Returns whether or not the thumbnail is to maintain the aspect ratio of the source image when creating the thumbnail. @return 		{@code true} if the thumbnail is to maintain the aspect ratio of the original image, {@code false} otherwise.

### Goal
Returns a boolean indicating whether the thumbnail generation process is configured to preserve the original image's aspect ratio.

### Parameters
_None._

### Input
An instantiated `ThumbnailParameter` object representing the configuration for a thumbnail generation task.

### Output
Returns `boolean` — `true` if the resizing operation will maintain the original image's proportions; `false` if the image may be stretched or squashed to exactly fit the target dimensions.

### Valid Call Patterns
```java
// Inferred from signature (not verified)
boolean keepRatio = thumbnailParameter.isKeepAspectRatio();
```

### LLM Instruction Prompt
- Use `isKeepAspectRatio()` strictly as a getter to inspect an existing `ThumbnailParameter` configuration. Do not attempt to use this method to configure or set the aspect ratio in a `Thumbnails.Builder` pipeline.
- To configure aspect ratio behavior during pipeline construction, use `size(int, int)` (which maintains aspect ratio) or `forceSize(int, int)` (which ignores aspect ratio).

### Prompt Snippet
```text
Use `thumbnailParameter.isKeepAspectRatio()` to check if a configured thumbnail task will preserve the source image's proportions. This is a read-only inspection method.
```

### Common Failure Modes
- **NullPointerException**: Calling this method on an uninitialized or null `ThumbnailParameter` reference.
- **Misusing as a Builder Method**: Attempting to call `isKeepAspectRatio()` on a `Thumbnails.Builder` to configure the pipeline. This method belongs to the underlying parameter object, not the fluent builder.

### Fix Code Hint
```java
// CORRECT: Inspecting an existing parameter object
boolean keepsRatio = thumbnailParameter.isKeepAspectRatio();

// CORRECT: Configuring aspect ratio behavior uses the Builder, not this getter
Thumbnails.of(new File("image.jpg"))
    .size(640, 480)      // Maintains aspect ratio
    // .forceSize(640, 480) // Ignores aspect ratio
    .toFile(new File("thumbnail.jpg"));
```

## API Test: `isOffset`

### Signature
```java
public boolean isOffset()
```
_Source: source/src/main/java/net/coobird/thumbnailator/util/exif/IfdStructure.java:122_

_Source doc:_ Returns whether the value returned by the {@link #getOffsetValue()} method is an offset value. @return		{@code true} if the value returned by the {@link #getOffsetValue()} method is a offset value, {@code false} otherwise.

### Goal
Returns whether the value associated with this Exif IFD (Image File Directory) structure represents an offset to data rather than the inline data itself.

### Parameters
_None._

### Input
An instantiated `IfdStructure` object, typically encountered when parsing Exif metadata to determine image orientation preconditions.

### Output
Returns `boolean` — `true` if the value returned by the `getOffsetValue()` method is an offset value, `false` otherwise.

### Valid Call Patterns
```java
// Inferred from signature (not verified)
boolean isOffsetValue = ifdStructure.isOffset();
```

### LLM Instruction Prompt
- When interacting with Thumbnailator's internal Exif parsing utilities (such as `IfdStructure`), always use `isOffset()` to determine if the parsed value is a pointer/offset to the actual data before interpreting it.

### Prompt Snippet
```text
Check `ifdStructure.isOffset()` before interpreting the result of `ifdStructure.getOffsetValue()` to ensure you correctly handle Exif metadata offsets rather than treating them as literal data values.
```

### Common Failure Modes
- **Misinterpreting Exif Data**: Treating the integer returned by `getOffsetValue()` as literal Exif data (like an orientation flag) when it is actually a memory/file offset pointer, because `isOffset()` was not checked first.

### Fix Code Hint
```java
if (ifdStructure.isOffset()) {
    int offset = ifdStructure.getOffsetValue();
    // Seek to the offset to read the actual Exif data
} else {
    // The value itself contains the data
}
```

## API Test: `isSupportedOutputFormat`

### Signature
```java
public static boolean isSupportedOutputFormat(String format)
```
_Source: source/src/main/java/net/coobird/thumbnailator/util/ThumbnailatorUtils.java:72_

_Source doc:_ Returns whether a specified format is supported for output. @param format	The format to check whether it is supported or not. @return			{@code true} if the format is supported, {@code false} otherwise.

### Goal
Checks whether the host JVM's underlying Java Image I/O mechanism supports writing images in the specified file format.

### Parameters
- `format` (`String`): The informal name of the image format to check (e.g., `"JPEG"`, `"PNG"`, `"GIF"`).

### Input
A string representing the desired output image format. Because Thumbnailator relies entirely on the host JVM's standard Image I/O capabilities with zero external dependencies, the supported formats are strictly limited to those with a registered `ImageWriter` in the current Java environment.

### Output
Returns `boolean` — `true` if the format is supported for output by the JVM, and `false` if it is unsupported (e.g., `"foobar"`).

### Valid Call Patterns
```java
// Check for a known supported format
boolean isSupported = ThumbnailatorUtils.isSupportedOutputFormat("JPEG");
assertTrue(isSupported);

// Check for an unsupported or invalid format
boolean isNotSupported = ThumbnailatorUtils.isSupportedOutputFormat("foobar");
assertFalse(isNotSupported);
```

### LLM Instruction Prompt
- When dynamically determining or accepting user input for an output format in a Thumbnailator pipeline, always validate the format using `ThumbnailatorUtils.isSupportedOutputFormat(format)` before passing it to `Thumbnails.Builder.outputFormat(String)`. This prevents the pipeline from throwing an `UnsupportedFormatException` during execution.

### Prompt Snippet
```text
Validate dynamic image formats using `ThumbnailatorUtils.isSupportedOutputFormat(format)` before applying them to the `Thumbnails.Builder` to avoid `UnsupportedFormatException` on JVMs lacking specific Image I/O plugins.
```

### Common Failure Modes
- **Assuming universal format support**: Attempting to output formats like WebP, TIFF, or HEIC without verifying support first. Standard Java 8 Image I/O does not support these out-of-the-box, which will cause `Thumbnails.Builder.outputFormat(...)` to eventually throw an `UnsupportedFormatException`.
- **Null format strings**: Passing `null` to this utility method may result in an `IllegalArgumentException` or `NullPointerException` from the underlying `ImageIO.getImageWritersByFormatName` call.

### Fix Code Hint
```java
String desiredFormat = "webp";
String safeFormat = ThumbnailatorUtils.isSupportedOutputFormat(desiredFormat) ? desiredFormat : "png";

Thumbnails.of(inputFile)
    .size(200, 200)
    .outputFormat(safeFormat)
    .toFile(outputFile);
```

## API Test: `isSupportedOutputFormatType`

### Signature
```java
public static boolean isSupportedOutputFormatType(String format, String type)
```
_Source: source/src/main/java/net/coobird/thumbnailator/util/ThumbnailatorUtils.java:130_

_Source doc:_ Returns whether a specified format type is supported for a specified output format. @param format	The format to check whether it is supported or not. @param type		The format type to check whether it is supported or not. @return			{@code true} if the format type is supported by the specified supported format, {@code false} otherwise.

### Goal
Checks whether a specific format type (such as a compression type) is supported by the underlying Java Image I/O for a given output image format.

### Parameters
- `format` (`String`): The output image format identifier to check (e.g., `"JPEG"`, `"PNG"`).
- `type` (`String`): The specific format type or compression type to verify against the specified format (e.g., `"JPEG"`).

### Input
Two `String` values representing the target image format and the specific format type. Because Thumbnailator relies entirely on the host JVM's standard Image I/O capabilities, the validity of these inputs depends on the `ImageWriter` plugins currently registered in the headless Java environment.

### Output
Returns `boolean` — `true` if the specified format type is supported by the given output format in the current JVM's Image I/O registry; `false` otherwise.

### Valid Call Patterns
```java
// Check if a known format and type are supported
String format = "JPEG";
String type = "JPEG";
boolean isSupported = ThumbnailatorUtils.isSupportedOutputFormatType(format, type);

// Check an unsupported or invalid type
boolean isUnsupported = ThumbnailatorUtils.isSupportedOutputFormatType("JPEG", "foobar");
```

### LLM Instruction Prompt
- Use `ThumbnailatorUtils.isSupportedOutputFormatType(format, type)` to safely verify if the host JVM supports a specific format type before configuring a Thumbnailator pipeline.
- Do not assume format support is universal; it depends entirely on the underlying Java Image I/O capabilities of the environment.
- Always qualify the static method with `ThumbnailatorUtils`.

### Prompt Snippet
```text
Before applying specific output format types in a Thumbnailator pipeline, verify support using `ThumbnailatorUtils.isSupportedOutputFormatType(format, type)` to prevent runtime `UnsupportedFormatException`s caused by missing Image I/O plugins.
```

### Common Failure Modes
- **Assuming universal format support**: Hardcoding format types without checking can lead to an `UnsupportedFormatException` during pipeline execution if the host JVM lacks the necessary Image I/O plugin.
- **Incorrect receiver**: Attempting to call this method on `Thumbnails` or `Thumbnails.Builder` instead of the utility class `ThumbnailatorUtils`.

### Fix Code Hint
```java
String targetFormat = "JPEG";
String targetType = "JPEG";

// Safely check for support before proceeding with pipeline configuration
if (ThumbnailatorUtils.isSupportedOutputFormatType(targetFormat, targetType)) {
    Thumbnails.of(new File("input.jpg"))
        .size(640, 480)
        .outputFormat(targetFormat)
        // (Format type configuration would be applied here if exposed by the builder)
        .toFile(new File("output.jpg"));
} else {
    System.err.println("The requested format type is not supported by this JVM.");
}
```

## API Test: `isValue`

### Signature
```java
public boolean isValue()
```
_Source: source/src/main/java/net/coobird/thumbnailator/util/exif/IfdStructure.java:105_

_Source doc:_ Returns whether the value returned by the {@link #getOffsetValue()} method is an actual value. @return		{@code true} if the value returned by the {@link #getOffsetValue()} method is a value, {@code false} otherwise.

### Goal
Determines whether the data stored in the offset/value field of an Exif Image File Directory (IFD) entry is an immediate value rather than a pointer to a data offset.

### Parameters
_None._

### Input
An instantiated `IfdStructure` object representing a parsed Exif IFD entry. This is typically encountered when manually traversing Exif metadata to determine image properties like orientation.

### Output
Returns `boolean` — `true` if the integer returned by `getOffsetValue()` represents the actual data value; `false` if it represents an offset (pointer) to where the data is stored elsewhere in the Exif structure.

### Valid Call Patterns
```java
// Note: Example inferred from signature (not verified by test suite)
boolean hasImmediateValue = ifdStructure.isValue();

if (hasImmediateValue) {
    int actualValue = ifdStructure.getOffsetValue();
    // Safely use actualValue as the data
} else {
    int dataOffset = ifdStructure.getOffsetValue();
    // Use dataOffset to locate the actual data in the Exif byte array
}
```

### LLM Instruction Prompt
- When parsing Exif metadata using Thumbnailator's internal utilities, always check `isValue()` on an `IfdStructure` before interpreting the result of `getOffsetValue()`.
- If `isValue()` returns `true`, the offset field contains the immediate data (because it fits within 4 bytes). If `false`, the field contains a pointer/offset to the actual data.

### Prompt Snippet
```text
When working with Exif IFD entries in Thumbnailator, you must verify if the entry holds an immediate value or an offset pointer. Call `ifdStructure.isValue()` before using `ifdStructure.getOffsetValue()`. If `isValue()` is true, the integer is the data itself. If false, it is an offset requiring further byte array traversal.
```

### Common Failure Modes
- **Misinterpreting Offsets as Values**: Calling `getOffsetValue()` and using its result as the actual Exif tag value without checking `isValue()` first. If the data exceeds 4 bytes, the Exif specification stores an offset instead, leading to garbage data if interpreted as an immediate value.
- **Manual Exif Parsing Errors**: Attempting to manually parse Exif data for orientation instead of using the provided, safer `ExifUtils.getExifOrientation` and `ExifFilterUtils.getFilterForOrientation(Orientation)` utilities.

### Fix Code Hint
```java
// Incorrect: Assuming getOffsetValue() is always the data
// int tagValue = ifdStructure.getOffsetValue(); 

// Correct: Check isValue() first
if (ifdStructure.isValue()) {
    int tagValue = ifdStructure.getOffsetValue();
    // Process the immediate value
} else {
    // Handle the offset pointer
}
```

## API Test: `iterableBufferedImages`

### Signature
```java
public Iterable<BufferedImage> iterableBufferedImages()
```
_Source: source/src/main/java/net/coobird/thumbnailator/Thumbnails.java:2213_

_Source doc:_ <p> Create the thumbnails and return as a {@link Iterable} of {@link BufferedImage}s. </p> <p> Thumbnail for a given input is lazily evaluated as the {@link Iterator#next()} method is called on the iterator. </p> <p> For situations where multiple thumbnails are being generated, this method is preferred over the {@link #asBufferedImages()} method, as (1) the processing does not have to complete before the method returns and (2) the thumbnails can be retrieved one at a time, potentially reducing the number of thumbnails which need to be retained in the heap memory, potentially reducing the chance of {@link OutOfMemoryError}s from occurring. </p> <p> If an {@link IOException} occurs during the processing of the thumbnail, the {@link Iterable} will return a {@code null} for that element. </p> <p><strong>Notes on image types</strong></p> <p> The image type of the {@link BufferedImage} depends on the type of the input image. (Specifically, the type emitted by the {@link javax.imageio.ImageReader} associated for the file type.) Thumbnailator will attempt to use the same image type as the input if it is not specified through {@link #imageType(int)}. </p> <p> This has implications when writing {@code BufferedImage} to files using the default JPEG writer bundled with Java. There are issues with the JPEG writer <a href="https://bugs.openjdk.java.net/browse/JDK-8041459">outputting wrong colors</a> or <a href="https://bugs.openjdk.java.net/browse/JDK-8204188">throwing exceptions</a> when writing a image containing an alpha channel. </p> <p> If outputting to a file, consider using one of the {@link #toFiles(Iterable)}, {@link #toFiles(Rename)}, {@link #toFiles(File, Rename)} {@link #asFiles(Iterable)}, {@link #asFiles(Rename)} or {@link #asFiles(File, Rename)} methods instead, as it contains workarounds to prevent issues mentioned in the previous paragraph. </p> <p> For more information on {@code BufferedImage} types, refer to {@link BufferedImage#getType()}. </p> @return		An {@link Iterable} which will provide an {@link Iterator} which returns thumbnails as {@link BufferedImage}s.

### Goal
Lazily generates and yields processed thumbnails one at a time as an `Iterable` of `BufferedImage` objects, minimizing heap memory usage during batch processing.

### Parameters
_None._

### Input
A configured `Thumbnails.Builder` pipeline containing one or more image sources (such as `File`s, `InputStream`s, `URL`s, or `BufferedImage`s) and at least one resizing constraint (e.g., `size(int, int)`).

### Output
Returns `Iterable<BufferedImage>` — an iterable collection that lazily evaluates the image processing pipeline upon calling `Iterator.next()`, yielding the resulting in-memory `BufferedImage`s. If an `IOException` occurs during the processing of a specific thumbnail, the iterator will yield `null` for that element.

### Valid Call Patterns
```java
// Given a source image (or multiple images)
BufferedImage img = new BufferedImageBuilder(200, 200).build();

// Lazily evaluate thumbnails without specifying an output format
Iterable<BufferedImage> thumbnails = Thumbnails.of(img)
    .size(50, 50)
    .iterableBufferedImages();

Iterator<BufferedImage> iter = thumbnails.iterator();
BufferedImage thumbnail = iter.next(); // Processing happens here

// Lazily evaluate thumbnails with a specified output format
Iterable<BufferedImage> pngThumbnails = Thumbnails.of(img)
    .size(50, 50)
    .outputFormat("png")
    .iterableBufferedImages();
```

### LLM Instruction Prompt
- Use `iterableBufferedImages()` instead of `asBufferedImages()` when processing multiple images to prevent `OutOfMemoryError`s, as it allows processing and garbage collecting one image at a time.
- Be aware that the actual image processing is deferred until `Iterator.next()` is called.
- You MUST check for `null` elements when iterating, because if an `IOException` occurs during the processing of a specific image, the iterator yields `null` rather than throwing an exception.
- Do NOT use this method if the ultimate goal is to write the images to files, especially JPEGs with alpha channels, due to known JDK bugs with the default JPEG writer outputting wrong colors or throwing exceptions. Use `toFiles(...)` or `asFiles(...)` instead, as they contain built-in workarounds.

### Prompt Snippet
```text
When batch processing images in memory with Thumbnailator, use `.iterableBufferedImages()` on the builder instead of `.asBufferedImages()`. Iterate through the result, checking each `BufferedImage` for `null` (which indicates an `IOException` occurred for that specific file). Do not collect them all into a List, as this defeats the memory-saving purpose of the lazy evaluation.
```

### Common Failure Modes
- **`NullPointerException` during iteration**: Failing to check if an element returned by the iterator is `null`. A `null` indicates an `IOException` occurred while reading or processing that specific input image.
- **`OutOfMemoryError`**: Accumulating the yielded `BufferedImage` objects into a `List` or other collection, which negates the memory benefits of lazy evaluation.
- **Corrupted JPEG Colors / Exceptions**: Manually writing the yielded `BufferedImage`s to JPEG files using `ImageIO.write` when the source image has an alpha channel. (Use `toFiles` instead to leverage Thumbnailator's workarounds).

### Fix Code Hint
```java
// WRONG: Accumulating lazily evaluated images or failing to check for null
Iterable<BufferedImage> thumbs = Thumbnails.of(files).size(100, 100).iterableBufferedImages();
List<BufferedImage> list = new ArrayList<>();
for (BufferedImage img : thumbs) {
    list.add(img); // Causes OutOfMemoryError on large batches
}

// RIGHT: Process one at a time and handle potential nulls
Iterable<BufferedImage> lazyThumbnails = Thumbnails.of(files)
    .size(100, 100)
    .iterableBufferedImages();

for (BufferedImage img : lazyThumbnails) {
    if (img == null) {
        // Handle the IOException failure for this specific image
        continue; 
    }
    // Process the image (e.g., analyze it), then let it be garbage collected
    processImage(img);
}
```

## API Test: `iterator`

### Signature
```java
public Iterator<File> iterator()
```
_Source: source/src/main/java/net/coobird/thumbnailator/name/ConsecutivelyNumberedFilenames.java:343_

_Source doc:_ Returns an iterator which generates file names according to the rules specified by this object. @return		An iterator which generates file names.

### Goal
Returns an iterator that sequentially generates `File` objects representing consecutively numbered filenames according to the rules configured in the parent generator object.

### Parameters
_None._

### Input
An instantiated `ConsecutivelyNumberedFilenames` object (which implements `Iterable<File>`). This object is typically configured to prevent filename collisions during batch processing.

### Output
Returns `Iterator<File>` — an iterator that yields a sequence of dynamically generated `File` objects (e.g., `0.jpg`, `1.jpg`, `2.jpg`) to be used as output destinations.

### Valid Call Patterns
```java
// Inferred from the signature and context (not verified in test suite)
ConsecutivelyNumberedFilenames fileGenerator = new ConsecutivelyNumberedFilenames();
Iterator<File> iter = fileGenerator.iterator();

if (iter.hasNext()) {
    File nextOutputFile = iter.next();
}
```

### LLM Instruction Prompt
- When outputting multiple files to a directory using `toFiles(Iterable<File>)` or `asFiles(Iterable<File>)`, you can pass a `ConsecutivelyNumberedFilenames` instance. The builder will internally call `iterator()` to generate safe, collision-free filenames for the batch output.
- If you need to manually inspect or retrieve the generated filenames before or after processing, call `iterator()` on the `ConsecutivelyNumberedFilenames` instance.

### Prompt Snippet
```text
Use `iterator()` on a `ConsecutivelyNumberedFilenames` instance to sequentially generate output `File` objects for batch processing, ensuring no filename collisions occur when saving multiple thumbnails.
```

### Common Failure Modes
- **Filename Collisions in Batch Processing**: Failing to use a `Rename` strategy or an `Iterable<File>` (like `ConsecutivelyNumberedFilenames` which provides this `iterator()`) when calling `toFiles()` or `asFiles()` on a batch of images will cause the pipeline to overwrite files or throw an exception.
- **Unbounded Iteration**: Assuming the iterator has a finite end without checking the specific configuration of the `ConsecutivelyNumberedFilenames` instance. Number generators often produce an infinite sequence of files, meaning a `while(iter.hasNext())` loop could run indefinitely if not bounded by the number of input images.

### Fix Code Hint
```java
// Correct usage: passing the Iterable directly to the builder, 
// which safely consumes the iterator() internally based on the number of inputs.
Thumbnails.fromFiles(inputFiles)
    .size(100, 100)
    .toFiles(new ConsecutivelyNumberedFilenames());
```

## API Test: `keepAspectRatio`

### Signature
```java
public Builder<T> keepAspectRatio(boolean keep)
public ThumbnailParameterBuilder keepAspectRatio(boolean keep)
public FixedSizeThumbnailMaker keepAspectRatio(boolean keep)
```
_Source: source/src/main/java/net/coobird/thumbnailator/Thumbnails.java:1491  (+2 more definition site/overload)_

_Source doc:_ Sets whether or not to keep the aspect ratio of the original image for the thumbnail. <p> Calling this method without first calling the {@link #size(int, int)} method will result in an {@link IllegalStateException} to be thrown. <p> If this method is not called when, by default the aspect ratio of the original image is preserved for the thumbnail. <p> Calling this method after calling the {@link #scale(double)} method or the {@link #scale(double, double)} method will result in a {@link IllegalStateException}. @param keep			{@code true} if the thumbnail is to maintain the aspect ratio of the original image, {@code false} otherwise. @return				Reference to this object. @throws IllegalStateException	If <ol> <li>the {@link #size(int, int)} has not yet been called to specify the size of the thumbnail, or</li> <li>the {@link #scale(double)} method has been called, or</li> <li>the {@link #scale(double, double)} method has been called, or</li> <li>the {@link #width(int)} and/or {@link #height(int)} has been called and not preserving the aspect ratio is desired.</li> </ol>

### Goal
Sets whether the thumbnail should maintain the aspect ratio of the original image or stretch/squash to exactly fit the specified bounding box.

### Parameters
- `keep` (`boolean`): `true` if the thumbnail must maintain the aspect ratio of the original image (the default behavior), or `false` to force the image to exactly match the requested dimensions.

### Input
A configured `Thumbnails.Builder` (or `ThumbnailParameterBuilder` / `FixedSizeThumbnailMaker`) in a fluent pipeline. 
**Preconditions:** 
1. The `size(int, int)` method MUST have been called prior to this method to specify the target dimensions.
2. The `scale(double)` or `scale(double, double)` methods MUST NOT have been called.
3. If `keep` is `false`, you MUST NOT have used the single-dimension constraints `width(int)` or `height(int)` instead of `size(int, int)`.

### Output
Returns `Builder<T>` — A reference to the current builder object, allowing for continued method chaining in the fluent image-processing pipeline.

### Valid Call Patterns
```java
// Example 1: Forcing exact dimensions (stretching/squashing)
BufferedImage thumbnail = Thumbnails.of(img)
        .size(120, 50)
        .keepAspectRatio(false)
        .asBufferedImage();

// Example 2: Explicitly preserving aspect ratio within a bounding box
BufferedImage thumbnail2 = Thumbnails.of(img)
        .size(120, 50)
        .keepAspectRatio(true)
        .asBufferedImage();
```

### LLM Instruction Prompt
When using `keepAspectRatio(boolean)` in Thumbnailator, you MUST call `size(int, int)` before it in the builder chain. Do NOT call `keepAspectRatio` if the pipeline uses `scale(...)`. Do NOT call `keepAspectRatio(false)` if you only specified `width(int)` or `height(int)` instead of `size(int, int)`.

### Prompt Snippet
```text
Call `.size(w, h)` before `.keepAspectRatio(boolean)`. Never mix with `.scale()`. Do not use `keepAspectRatio(false)` with only `.width()` or `.height()`.
```

### Common Failure Modes
- **`IllegalStateException` (Missing Size)**: Thrown if `keepAspectRatio` is called before `size(int, int)` has been called to specify the thumbnail's dimensions.
- **`IllegalStateException` (Mixed with Scale)**: Thrown if `keepAspectRatio` is called in a pipeline that already uses `scale(double)` or `scale(double, double)`.
- **`IllegalStateException` (Invalid Dimension Constraints)**: Thrown if `keepAspectRatio(false)` is called but only `width(int)` or `height(int)` was provided (aspect ratio must be preserved if only one dimension is constrained).

### Fix Code Hint
```java
// BAD: Calling keepAspectRatio before size, or mixing with scale
Thumbnails.of(file).keepAspectRatio(false).size(100, 100)...
Thumbnails.of(file).scale(0.5).keepAspectRatio(true)...

// GOOD: Call size(w, h) first, then keepAspectRatio
Thumbnails.of(file)
    .size(100, 100)
    .keepAspectRatio(false)
    .toFile(outFile);
```

## API Test: `make`

### Signature
```java
public BufferedImage make(BufferedImage img)
public abstract BufferedImage make(BufferedImage img)
```
_Source: source/src/main/java/net/coobird/thumbnailator/makers/ScaledThumbnailMaker.java:185  (+2 more definition site/overload)_

### Goal
Generates a thumbnail from a source `BufferedImage` using the specific resizing and formatting parameters configured on the underlying `ThumbnailMaker`.

### Parameters
- `img` (`BufferedImage`): The source image in memory that needs to be resized or transformed into a thumbnail.

### Input
A valid, non-null `BufferedImage`. The `ThumbnailMaker` instance (e.g., `FixedSizeThumbnailMaker`, `ScaledThumbnailMaker`) receiving this call must be fully initialized and configured with all required parameters (such as dimensions, scale factor, or fitting rules) prior to calling `make`. 

### Output
Returns `BufferedImage` — The newly created thumbnail image, processed deterministically according to the maker's configuration.

### Valid Call Patterns
```java
// Note: The fluent Thumbnails.of(...) API is strictly preferred over manual ThumbnailMaker usage.
// The following call form is inferred from the test suite's validation checks:

BufferedImage img = new BufferedImage(200, 200, BufferedImage.TYPE_INT_ARGB);

// 'maker' must be a fully configured instance of a ThumbnailMaker subclass.
// Calling make() on an uninitialized maker (e.g., new FixedSizeThumbnailMaker(100, 100)) 
// will throw an exception.
BufferedImage thumbnail = maker.make(img);
```

### LLM Instruction Prompt
- Strictly prefer the fluent `Thumbnails.of(img)...` builder API over manually instantiating `ThumbnailMaker` subclasses and calling `make(img)`. 
- If `make` must be used in an advanced pipeline, ensure the `ThumbnailMaker` is fully initialized with all required parameters before invocation, or it will fail validation.
- Never pass a `null` image to `make`.

### Prompt Snippet
```text
When generating thumbnails, use the fluent `Thumbnails.of(img).size(w, h).asBufferedImage()` API instead of manually calling `ThumbnailMaker.make(img)`. If you must use `make`, ensure the maker instance is fully configured first to avoid `IllegalStateException`.
```

### Common Failure Modes
- **`IllegalStateException`**: Thrown if `make(img)` is called on an uninitialized or partially configured `ThumbnailMaker` (e.g., calling `new FixedSizeThumbnailMaker(100, 100).make(img)` without setting required fitting parameters).
- **`NullPointerException`**: Thrown if the provided `img` argument is `null`.

### Fix Code Hint
```java
// BAD: Manual maker instantiation often fails due to missing configuration boilerplate
BufferedImage img = makeTestImage200x200();
BufferedImage thumb = new FixedSizeThumbnailMaker(100, 100).make(img); // Fails

// GOOD: Use the strictly preferred fluent API which handles configuration automatically
BufferedImage img = makeTestImage200x200();
BufferedImage thumb = Thumbnails.of(img)
    .size(100, 100)
    .asBufferedImage();
```

## API Test: `newRotator`

### Signature
```java
public static Rotator newRotator(final double angle)
```
_Source: source/src/main/java/net/coobird/thumbnailator/filters/Rotation.java:78_

_Source doc:_ Creates a new instance of {@code Rotator} which rotates an image at the specified angle. <p> When the {@link Rotator} returned by this method is applied, the image will be rotated clockwise by the specified angle. @param angle			The angle at which the instance of {@code Rotator} is to rotate a image it acts upon. @return				An instance of {@code Rotator} which will rotate a given image.

### Goal
Creates a new `Rotator` (an `ImageFilter` implementation) that applies a clockwise rotation of a specified angle to an image.

### Parameters
- `angle` (`final double`): The angle in degrees by which the image will be rotated clockwise.

### Input
A `double` representing the rotation angle. When the resulting `Rotator` is applied, it requires a valid, in-memory `BufferedImage` to act upon. The operation is performed in a headless environment and relies on standard Java 2D capabilities.

### Output
Returns `Rotator` — an instance of an `ImageFilter` that encapsulates the rotation transformation logic. It generates a new rotated `BufferedImage` when applied, retaining the original image type.

### Valid Call Patterns
```java
// Create a base image
BufferedImage originalImage = new BufferedImage(200, 200, BufferedImage.TYPE_INT_ARGB);

// Instantiate the Rotator as an ImageFilter
ImageFilter filter = Rotation.newRotator(45);

// Apply the filter (returns a new BufferedImage; the original is unaltered)
BufferedImage rotatedImage = filter.apply(originalImage);
```

### LLM Instruction Prompt
- Use `Rotation.newRotator(angle)` to create a custom rotation `ImageFilter`. 
- Note that the `angle` parameter specifies a **clockwise** rotation.
- The returned `Rotator` does not mutate the input `BufferedImage` in place; it safely returns a new `BufferedImage` instance with the transformation applied.

### Prompt Snippet
```text
To rotate an image by a specific angle, use `Rotation.newRotator(double angle)` to create an `ImageFilter`. The angle is applied clockwise. The filter does not alter the original image in place.
```

### Common Failure Modes
- **Assuming in-place mutation**: Callers might mistakenly assume `filter.apply(originalImage)` modifies `originalImage` in place. The library guarantees that input contents are not altered; the caller must capture the returned `BufferedImage` or rely on the `Thumbnails.Builder` pipeline to manage the new image.
- **Incorrect rotation direction**: Providing a positive angle expecting a counter-clockwise rotation. The documentation explicitly states the rotation is clockwise.

### Fix Code Hint
```java
// INCORRECT: Assuming the original image is modified in place
ImageFilter filter = Rotation.newRotator(90);
filter.apply(myImage);
save(myImage); // myImage is still unrotated!

// CORRECT: Capture the returned image
ImageFilter filter = Rotation.newRotator(90);
BufferedImage rotatedImage = filter.apply(myImage);
save(rotatedImage);

// ALTERNATIVE: Add to a fluent pipeline
Thumbnails.of(myImage)
    .size(200, 200)
    .addFilter(Rotation.newRotator(90))
    .asBufferedImage();
```

## API Test: `of`

### Signature
```java
public static Builder<File> of(String... files)
public static Builder<File> of(File... files)
public static Builder<URL> of(URL... urls)
public static Builder<? extends InputStream> of(InputStream... inputStreams)
public static Builder<BufferedImage> of(BufferedImage... images)
```
_Source: source/src/main/java/net/coobird/thumbnailator/Thumbnails.java:208  (+4 more definition site/overload)_

_Source doc:_ Indicate to make thumbnails for images with the specified filenames. @param files		File names of image files for which thumbnails are to be produced for. @return			Reference to a builder object which is used to specify the parameters for creating the thumbnail. @throws NullPointerException		If the argument is {@code null}. @throws IllegalArgumentException	If the argument is an empty array.

### Goal
Initialize a fluent builder pipeline to generate thumbnails or apply transformations to one or more image sources.

### Parameters
- `files` (`String...`): A varargs array of file paths representing the source images to be processed. (Note: Overloaded versions accept `File...`, `URL...`, `InputStream...`, or `BufferedImage...`).

### Input
- Must be one or more valid image sources (file paths, `File` objects, `URL`s, `InputStream`s, or `BufferedImage`s).
- The argument cannot be `null` and cannot be an empty array.
- The underlying image formats must be supported by the host JVM's standard Image I/O capabilities.
- When using `InputStream`s, the streams must be open and readable.

### Output
Returns `Builder<File>` (or `Builder<T>` corresponding to the input type, such as `Builder<BufferedImage>`) — A fluent builder object used to configure image transformations (e.g., `size`, `crop`, `rotate`) and route the processed images to a terminal sink (e.g., `asBufferedImage()`, `toFiles()`).

### Valid Call Patterns
```java
// Pattern 1: Processing a single in-memory BufferedImage
BufferedImage img = new BufferedImageBuilder(200, 200).build();
BufferedImage thumbnail = Thumbnails.of(img)
    .size(100, 100)
    .asBufferedImage();

// Pattern 2: Batch processing multiple files from a directory and saving with a Rename strategy
Thumbnails.of(new File("path/to/directory").listFiles())
    .size(640, 480)
    .outputFormat("jpg")
    .toFiles(Rename.PREFIX_DOT_THUMBNAIL);
```

### LLM Instruction Prompt
- Always use `Thumbnails.of(...)` as the entry point for the fluent API; do not use the deprecated `Thumbnailator.createThumbnails` methods.
- Never pass `null` or an empty array to `of(...)`.
- You must chain configuration methods (like `size(int, int)` or `forceSize(int, int)`) before calling a terminal sink method.
- **CRITICAL**: When passing multiple inputs to `of(...)` and routing the output to files via `toFiles()` or `asFiles()`, you MUST provide a `Rename` strategy (e.g., `Rename.PREFIX_DOT_THUMBNAIL`) or an instance of `ConsecutivelyNumberedFilenames` to prevent filename collisions.

### Prompt Snippet
```text
Use `Thumbnails.of(...)` to start the Thumbnailator fluent builder pipeline. Do not pass null or empty arrays. Chain configuration methods like `.size(w, h)` before calling a terminal sink like `.asBufferedImage()`. If batch processing multiple inputs to files, you must pass a `Rename` strategy to `.toFiles()` to avoid collisions.
```

### Common Failure Modes
- **`NullPointerException`**: Thrown if the argument passed to `of(...)` is `null`.
- **`IllegalArgumentException`**: Thrown if the varargs array passed to `of(...)` is empty.
- **Filename Collisions**: Occurs when batch processing multiple files to a directory without providing a `Rename` strategy to the terminal `toFiles()` method.
- **`UnsupportedFormatException`**: Thrown later in the pipeline if the JVM's Image I/O does not support reading the input format or writing the requested output format.

### Fix Code Hint
```java
// BAD: Passing an empty array or null
// Thumbnails.of(new String[0]).size(100, 100).toFiles(Rename.PREFIX_DOT_THUMBNAIL);

// GOOD: Ensure the input array is populated before calling
File[] inputFiles = new File("path/to/directory").listFiles();
if (inputFiles != null && inputFiles.length > 0) {
    Thumbnails.of(inputFiles)
        .size(640, 480)
        .toFiles(Rename.PREFIX_DOT_THUMBNAIL); // Rename strategy required for batch output
}
```

## API Test: `outputFormat`

### Signature
```java
public Builder<T> outputFormat(String format)
```
_Source: source/src/main/java/net/coobird/thumbnailator/Thumbnails.java:1658_

_Source doc:_ Sets the compression format to use when writing the thumbnail. <p> For example, to set the output format to JPEG, the following code can be used: <pre><code> Thumbnails.of(image) .size(640, 480) .outputFormat("JPEG") .toFile(thumbnail); </code></pre> or, alternatively: <pre><code> Thumbnails.of(image) .size(640, 480) .outputFormat("jpg") .toFile(thumbnail); </code></pre> <p> Currently, whether or not the compression format string is valid dependents on whether the Java Image I/O API recognizes the string as a format that it supports for output. (Valid format names can be obtained by calling the {@link ImageIO#getWriterFormatNames()} method.) <p> Calling this method to set this parameter is optional. <p> Calling this method in conjunction with {@link #asBufferedImage()} or {@link #asBufferedImages()} will not result in any changes to the final result. <p> Calling this method multiple times will result in an {@link IllegalStateException} to be thrown. @param format		The compression format to use when writing the thumbnail. @return				Reference to this object. @throws IllegalArgumentException	If an unsupported format is specified.

### Goal
Sets the compression format (such as "jpg" or "png") to use when writing the generated thumbnails to a file or stream sink.

### Parameters
- `format` (`String`): The compression format to use when writing the thumbnail (e.g., `"JPEG"`, `"jpg"`, `"png"`). Must be a valid format recognized by the underlying Java Image I/O API.

### Input
A string representing an image format supported by the host JVM's Image I/O capabilities (valid names can be obtained via `ImageIO.getWriterFormatNames()`). This method is called on an active `Thumbnails.Builder` instance in a fluent pipeline before routing the processed image to a terminal sink (like `toFile`, `toFiles`, or `toOutputStream`).

### Output
Returns `Builder<T>` — A reference to the current builder object, allowing for continued method chaining in the fluent interface.

### Valid Call Patterns
```java
// Pattern 1: Writing to files with a specified output format and rename strategy
Thumbnails.of(new File("path/to/directory").listFiles())
    .size(640, 480)
    .outputFormat("jpg")
    .toFiles(Rename.PREFIX_DOT_THUMBNAIL);

// Pattern 2: Specifying format in an in-memory pipeline (Note: format is ignored by asBufferedImage)
BufferedImage img = new BufferedImageBuilder(200, 200).build();
BufferedImage thumbnail = Thumbnails.of(img)
    .size(100, 100)
    .outputFormat("png")
    .asBufferedImage();
```

### LLM Instruction Prompt
- Call `outputFormat(String)` exactly once per builder pipeline if a specific output format is required for file or stream sinks.
- Do not call this method multiple times on the same builder, as it will throw an `IllegalStateException`.
- Ensure the format string is supported by the standard Java Image I/O API (e.g., `"jpg"`, `"png"`); otherwise, an `IllegalArgumentException` is thrown.
- Be aware that calling `outputFormat` is optional. If the pipeline terminates with in-memory sinks like `asBufferedImage()` or `asBufferedImages()`, calling this method is a no-op and will not change the final `BufferedImage` result.

### Prompt Snippet
```text
Use `.outputFormat("jpg")` or `.outputFormat("png")` on the `Thumbnails.Builder` to specify the output file format before calling terminal methods like `toFile()` or `toOutputStream()`. Do not call this method multiple times on the same builder. Note that this setting has no effect if the pipeline terminates with in-memory sinks like `asBufferedImage()`.
```

### Common Failure Modes
- **`IllegalStateException`**: Thrown if `outputFormat(...)` is called multiple times on the same `Thumbnails.Builder` instance.
- **`IllegalArgumentException`**: Thrown if the provided format string is not supported by the underlying Java Image I/O API.
- **Logical No-Op**: Calling `outputFormat` in conjunction with `asBufferedImage()` or `asBufferedImages()` will not result in any changes to the final in-memory result, as `BufferedImage` objects do not inherently store compression formats.

### Fix Code Hint
```java
// BAD: Calling outputFormat multiple times throws IllegalStateException
Thumbnails.of(image)
    .size(200, 200)
    .outputFormat("png")
    .outputFormat("jpg") // Throws IllegalStateException
    .toFile(outFile);

// GOOD: Call outputFormat exactly once with a valid Image I/O format string
Thumbnails.of(image)
    .size(200, 200)
    .outputFormat("jpg")
    .toFile(outFile);
```

## API Test: `outputFormatType`

### Signature
```java
public Builder<T> outputFormatType(String formatType)
```
_Source: source/src/main/java/net/coobird/thumbnailator/Thumbnails.java:1762_

_Source doc:_ Sets the compression format type of the thumbnail to write. <p> If the default type for the compression codec should be used, a value of {@link ThumbnailParameter#DEFAULT_FORMAT_TYPE} should be used. <p> Calling this method to set this parameter is optional. <p> Calling this method multiple times will result in an {@link IllegalStateException} to be thrown. <p> Furthermore, if this method is called, then calling the {@link #outputFormat} method is disabled, in order to prevent cases where the output format type does not exist in the format specified for the {@code outputFormat} method. <p> <em> Implementation note: Compression format type settings are ignored when the underlying image writer does not support compression. This behavior is subject to change in the future. </em> @param formatType	The compression format type @return				Reference to this object. @throws IllegalArgumentException	If an unsupported format type is specified for the current output format type. Or, if the output format has not been specified before this method was called.

### Goal
Sets the specific compression format type for the thumbnail being written, configuring how the underlying Java Image I/O writer compresses the output.

### Parameters
- `formatType` (`String`): The compression format type to use (e.g., `"JPEG"`). To explicitly use the default type for the compression codec, pass `ThumbnailParameter.DEFAULT_FORMAT_TYPE`.

### Input
The caller must provide a valid compression format type string that is supported by the underlying Java Image I/O writer for the chosen output format. 
**Preconditions:** 
1. The `outputFormat(String)` method **must** be called *before* calling `outputFormatType(String)`.
2. The specified `formatType` must be compatible with the previously specified output format (e.g., you cannot specify a `"JPEG"` compression type for a `"PNG"` output format).

### Output
Returns `Builder<T>` — a reference to the current `Thumbnails.Builder` instance to allow for fluent method chaining.

### Valid Call Patterns
```java
// given
BufferedImage img = TestUtils.getImageFromResource("Thumbnailator/grid.png");

// when
Thumbnails.of(img)
        .size(50, 50)
        .outputFormat("JPEG")
        .outputFormatType("JPEG"); // Must be called AFTER outputFormat()
```

### LLM Instruction Prompt
- You MUST call `outputFormat(String)` before calling `outputFormatType(String)`.
- Do NOT call `outputFormat(String)` after calling `outputFormatType(String)`, as it is disabled to prevent format mismatches.
- Do NOT call `outputFormatType(String)` multiple times on the same builder instance.
- Ensure the compression `formatType` is supported by the chosen `outputFormat` (e.g., do not apply `"JPEG"` compression to a `"PNG"` output format).

### Prompt Snippet
```text
When using `outputFormatType(String)` in Thumbnailator, strict ordering is required: you must call `outputFormat(String)` first. Calling `outputFormatType` without a prior `outputFormat` call, calling it multiple times, or specifying a compression type incompatible with the output format will throw exceptions.
```

### Common Failure Modes
- **`IllegalArgumentException` (Missing Output Format)**: Thrown if `outputFormatType` is called before `outputFormat` has been specified.
- **`IllegalArgumentException` (Unsupported Format Type)**: Thrown if the specified `formatType` is not supported by the current output format (e.g., calling `.outputFormat("PNG").outputFormatType("JPEG")`).
- **`IllegalStateException`**: Thrown if `outputFormatType(String)` is called multiple times on the same builder instance.

### Fix Code Hint
```java
// INCORRECT: Calling outputFormatType before outputFormat, or using incompatible types
Thumbnails.of(img)
    .size(50, 50)
    .outputFormatType("JPEG") // Throws IllegalArgumentException
    .outputFormat("JPEG");

// CORRECT: Call outputFormat first, then outputFormatType with a compatible type
Thumbnails.of(img)
    .size(50, 50)
    .outputFormat("JPEG")
    .outputFormatType("JPEG");
```

## API Test: `outputQuality`

### Signature
```java
public Builder<T> outputQuality(float quality)
public Builder<T> outputQuality(double quality)
```
_Source: source/src/main/java/net/coobird/thumbnailator/Thumbnails.java:1550  (+1 more definition site/overload)_

_Source doc:_ Sets the output quality of the compression algorithm used to compress the thumbnail when it is written to an external destination such as a file or output stream. <p> The value is a {@code float} between {@code 0.0f} and {@code 1.0f} where {@code 0.0f} indicates the minimum quality and {@code 1.0f} indicates the maximum quality settings should be used for by the compression codec. <p> Calling this method to set this parameter is optional. <p> Calling this method in conjunction with {@link #asBufferedImage()} or {@link #asBufferedImages()} will not result in any changes to the final result. <p> Calling this method multiple times, or the {@link #outputQuality(double)} in conjunction with this method will result in an {@link IllegalStateException} to be thrown. <p> <em> Implementation note: Compression quality settings are ignored when the underlying image writer does not support compression. This behavior is subject to change in the future. </em> @param quality		The compression quality to use when writing the thumbnail. @return				Reference to this object. @throws IllegalArgumentException	If the argument is less than {@code 0.0f} or is greater than {@code 1.0f}.

### Goal
Sets the compression quality level for the thumbnail when writing it to an external destination like a file or output stream.

### Parameters
- `quality` (`float` or `double`): The compression quality to use, ranging from `0.0f` (minimum quality / maximum compression) to `1.0f` (maximum quality / minimum compression).

### Input
A `Thumbnails.Builder` instance in an active fluent pipeline. The caller must provide a valid float or double between `0.0` and `1.0` inclusive. For this setting to have any effect, the pipeline must eventually write to an external destination (e.g., `toFile`, `toOutputStream`), and the underlying Java Image I/O writer for the chosen format (e.g., JPEG) must support compression.

### Output
Returns `Builder<T>` — A reference to the current builder object to allow continued method chaining.

### Valid Call Patterns
```java
InputStream is = TestUtils.getResourceStream("Thumbnailator/grid.jpg");
ByteArrayOutputStream os = new ByteArrayOutputStream();

Thumbnails.of(is)
        .size(50, 50)
        .outputFormat("jpg")
        .outputQuality(0.5f)
        .toOutputStream(os);
```

### LLM Instruction Prompt
- Provide a value strictly between `0.0f` and `1.0f`.
- Do not call `outputQuality` multiple times on the same builder, and do not mix the `float` and `double` overloads in the same chain, as this will throw an `IllegalStateException`.
- Do not use this method if the pipeline terminates with `asBufferedImage()` or `asBufferedImages()`, as the setting will be ignored for in-memory images.
- Ensure the output format supports compression (e.g., JPEG). If the underlying image writer does not support compression, the setting is silently ignored.

### Prompt Snippet
```text
When configuring image compression in Thumbnailator, use `.outputQuality(float)` with a value between 0.0f and 1.0f. Call it exactly once per builder chain. Only use it when writing to files or streams; it is ignored for in-memory `BufferedImage` outputs or formats that do not support compression.
```

### Common Failure Modes
- **`IllegalArgumentException`**: Thrown if the `quality` argument is less than `0.0f` or greater than `1.0f`.
- **`IllegalStateException`**: Thrown if `outputQuality` is called multiple times on the same builder instance.
- **Silent Failure (Ignored)**: Occurs if the pipeline terminates with an in-memory sink (`asBufferedImage()`) or if the chosen output format's Image I/O writer does not support compression settings.

### Fix Code Hint
```java
// BAD: Calling multiple times or using out-of-bounds values
Thumbnails.of(file)
    .size(100, 100)
    .outputQuality(0.8f)
    .outputQuality(0.9f) // Throws IllegalStateException
    .toFile(outFile);

// BAD: Value out of bounds
Thumbnails.of(file).size(100, 100).outputQuality(80.0f); // Throws IllegalArgumentException (must be <= 1.0f)

// GOOD: Call once with a valid float between 0.0f and 1.0f
Thumbnails.of(file)
    .size(100, 100)
    .outputFormat("jpg")
    .outputQuality(0.8f)
    .toFile(outFile);
```

## API Test: `preferredOutputFormatName`

### Signature
```java
public String preferredOutputFormatName()
```
_Source: source/src/main/java/net/coobird/thumbnailator/tasks/io/AbstractImageSink.java:72  (+2 more definition site/overload)_

### Goal
Retrieves the preferred output image format name (e.g., "jpg", "png") inferred from the destination's context, such as a file extension.

### Parameters
_None._

### Input
Requires an instantiated `ImageSink` (such as a `FileImageSink`). The method relies on the internal state of the sink (e.g., the destination file path) to infer the format. No direct arguments are passed.

### Output
Returns `String` — The name of the preferred output format. If the format cannot be determined from the sink's context (e.g., when writing to a generic `OutputStream`), it returns the constant `ThumbnailParameter.ORIGINAL_FORMAT`.

### Valid Call Patterns
```java
// Example based on Thumbnailator's internal SourceSinkThumbnailTaskTest
ImageSink destination = mock(ImageSink.class);
when(destination.preferredOutputFormatName()).thenReturn("jpg");

// Typical internal pipeline usage when ThumbnailParameter.DETERMINE_FORMAT is set:
String preferredFormat = destination.preferredOutputFormatName();
```

### LLM Instruction Prompt
- When implementing a custom `ImageSink`, implement `preferredOutputFormatName()` to return the format string (e.g., "png") if it can be inferred from the destination.
- If the format cannot be determined, you MUST return `ThumbnailParameter.ORIGINAL_FORMAT`. Do not return `null`.
- When writing custom `ThumbnailTask` logic, do not invoke this method if the `ThumbnailParameter` is explicitly configured to use `ThumbnailParameter.ORIGINAL_FORMAT`.

### Prompt Snippet
```text
When implementing ImageSink#preferredOutputFormatName() in Thumbnailator, return the inferred format string (like "jpg"). If the format is unknown (e.g., writing to an OutputStream), return ThumbnailParameter.ORIGINAL_FORMAT. Never return null.
```

### Common Failure Modes
- **Returning `null` in custom implementations**: If a custom `ImageSink` returns `null` instead of `ThumbnailParameter.ORIGINAL_FORMAT` when the format is unknown, it can cause `NullPointerException`s or `UnsupportedFormatException`s when the underlying Java Image I/O attempts to find a writer.
- **Unnecessary invocation**: Calling this method when the pipeline is already strictly configured to use the original image's format (via `ThumbnailParameter.ORIGINAL_FORMAT`). As shown in the test suite, the pipeline skips querying the destination's preferred format in this scenario.

### Fix Code Hint
```java
// In a custom ImageSink implementation:
@Override
public String preferredOutputFormatName() {
    if (this.inferredFormat != null) {
        return this.inferredFormat;
    }
    // FIX: Return the fallback constant, not null
    return ThumbnailParameter.ORIGINAL_FORMAT; 
}
```

## API Test: `quality`

### Signature
```java
public ThumbnailParameterBuilder quality(float quality)
```
_Source: source/src/main/java/net/coobird/thumbnailator/builders/ThumbnailParameterBuilder.java:232_

_Source doc:_ Sets the compression quality setting of the thumbnail. <p> An acceptable value is in the range of {@code 0.0f} to {@code 1.0f}, where {@code 0.0f} is for the lowest quality setting and {@code 1.0f} for the highest quality setting. <p> If the default compression quality is to be used, then the value {@link ThumbnailParameter#DEFAULT_QUALITY} should be used. @param quality		The compression quality setting of the thumbnail. @return				A reference to this object.

### Goal
Sets the compression quality for the generated thumbnail, controlling the trade-off between file size and image fidelity for supported output formats.

### Parameters
- `quality` (`float`): The compression quality setting. Must be in the range of `0.0f` (lowest quality, highest compression) to `1.0f` (highest quality, lowest compression). To use the default compression quality, pass `ThumbnailParameter.DEFAULT_QUALITY` (which evaluates to `Float.NaN`).

### Input
A valid `float` value representing the desired quality. The underlying Java Image I/O writer for the chosen output format (e.g., JPEG) must support compression quality settings for this parameter to have a visible effect on the output file.

### Output
Returns `ThumbnailParameterBuilder` — A reference to the current builder instance, allowing for fluent method chaining.

### Valid Call Patterns
```java
// Inferred from signature (not verified by tests or README)
ThumbnailParameterBuilder builder = new ThumbnailParameterBuilder();
builder.quality(0.85f);

// Using the default quality constant
builder.quality(ThumbnailParameter.DEFAULT_QUALITY);
```

### LLM Instruction Prompt
- When configuring thumbnail compression, ensure the `quality` argument is a `float` strictly between `0.0f` and `1.0f` inclusive, or use `ThumbnailParameter.DEFAULT_QUALITY`. Always append the `f` suffix to literal decimal values to prevent `double` to `float` compilation errors.

### Prompt Snippet
```text
builder.quality(0.75f);
```

### Common Failure Modes
- **Compilation Error (Type Mismatch):** Passing a decimal literal without the `f` suffix (e.g., `0.8`) will be evaluated as a `double` by the Java compiler, resulting in a compilation error because the method strictly requires a `float`.
- **Out of Bounds Value:** Providing a value less than `0.0f` or greater than `1.0f` (other than `ThumbnailParameter.DEFAULT_QUALITY`) is invalid and will cause an `IllegalArgumentException` during parameter validation or when the underlying Image I/O writer attempts to apply the setting.
- **Unsupported Format:** Applying a quality setting to an output format that does not support lossy compression (like standard PNG or BMP in some Image I/O implementations) may be silently ignored by the underlying Java Image I/O writer.

### Fix Code Hint
```java
// INCORRECT: Missing 'f' suffix causes a double-to-float compilation error
// builder.quality(0.9); 

// CORRECT: Use the 'f' suffix for float literals
builder.quality(0.9f);

// CORRECT: Fallback to the default quality
builder.quality(ThumbnailParameter.DEFAULT_QUALITY);
```

## API Test: `read`

### Signature
```java
public BufferedImage read()
public abstract BufferedImage read()
```
_Source: source/src/main/java/net/coobird/thumbnailator/tasks/StreamThumbnailTask.java:76  (+8 more definition site/overload)_

### Goal
Reads an image from its underlying source (such as a file, stream, or URL) and decodes it into an in-memory `BufferedImage` for processing.

### Parameters
_None._

### Input
An initialized source object (such as an `ImageSource` or `ThumbnailTask` implementation) that points to valid, accessible image data. The image data must be in a format supported by the host JVM's standard Image I/O capabilities. 

### Output
Returns `BufferedImage` — the fully decoded, in-memory representation of the source image, ready to be passed through the `ImageFilter` pipeline.

### Valid Call Patterns
```java
// Inferred from signature (not verified by test suite or readme)
// Typically called on an ImageSource or ThumbnailTask instance
BufferedImage image = imageSource.read();
```

### LLM Instruction Prompt
- Do not call `read()` directly for standard thumbnail generation; the fluent `Thumbnails.of(...)` builder automatically handles reading and abstracts away `BufferedImage` manipulation.
- Use `read()` only when manually implementing or exercising custom `ImageSource` or `ThumbnailTask` abstractions.
- Be aware of memory constraints: the current implementation loads the entire image into memory at once. (Note: The source documentation indicates the public interface of this method may change in the future to support tile-by-tile reading for large images).
- Ensure the underlying source (e.g., `InputStream`) is readable; if the underlying source throws an `IOException` during its own read operations, the Thumbnailator read process will fail.

### Prompt Snippet
```text
When working with Thumbnailator's internal abstractions (like `ImageSource` or `ThumbnailTask`), use `source.read()` to decode the input into a `BufferedImage`. For standard workflows, avoid manual reads and use the fluent `Thumbnails.of(...)` API instead. Note that `read()` currently loads the entire image into memory, though future versions may support tile-by-tile reading.
```

### Common Failure Modes
- **Underlying Stream/IO Errors**: If the underlying `InputStream` or `File` is inaccessible, closed, or throws an `IOException` during byte extraction (as demonstrated in the project's test suite), the read operation will fail.
- **Unsupported Formats**: If the image format is not supported by the underlying Java Image I/O implementation, the read operation cannot decode the image.
- **Memory Exhaustion**: Because the method currently returns a single `BufferedImage` containing the entire image, reading extremely large images may cause an `OutOfMemoryError`.

### Fix Code Hint
```java
// Instead of manually managing sources and calling read():
// BufferedImageSource source = ...;
// BufferedImage img = source.read();

// Prefer the fluent builder which safely manages the read/write lifecycle:
Thumbnails.of(new File("path/to/input.jpg"))
    .size(640, 480)
    .toFile(new File("path/to/output.jpg"));
```

## API Test: `region`

### Signature
```java
public ThumbnailParameterBuilder region(Region sourceRegion)
```
_Source: source/src/main/java/net/coobird/thumbnailator/builders/ThumbnailParameterBuilder.java:200_

_Source doc:_ Sets the region of the source image to use when creating a thumbnail. @param sourceRegion		The region of the source image to use when creating a thumbnail. @return			A reference to this object. @since	0.3.4

### Goal
Sets the specific rectangular area of the source image to be extracted and used as the base for the thumbnail generation process.

### Parameters
- `sourceRegion` (`Region`): The specific area of the source image to extract. This is typically constructed using a `Position` (such as the `Positions` enum or a `Coordinate`) and a `Size` (such as `AbsoluteSize`).

### Input
The caller must provide a valid `Region` object from the `net.coobird.thumbnailator.geometry` package. This method is called on an active `ThumbnailParameterBuilder` instance, which is typically used when constructing custom `ThumbnailTask` instances or configuring lower-level image sources (like `BufferedImageSource`). 

### Output
Returns `ThumbnailParameterBuilder` — A reference to the current builder instance to allow fluent method chaining.

### Valid Call Patterns
```java
// Extracting a region using a predefined Position (TOP_LEFT)
ThumbnailParameter params1 = new ThumbnailParameterBuilder()
    .region(new Region(Positions.TOP_LEFT, new AbsoluteSize(40, 40)))
    .size(20, 20)
    .build();

// Extracting a region using exact Coordinates
ThumbnailParameter params2 = new ThumbnailParameterBuilder()
    .region(new Region(new Coordinate(20, 20), new AbsoluteSize(100, 100)))
    .size(80, 80)
    .build();
```

### LLM Instruction Prompt
- When configuring a `ThumbnailParameterBuilder` to process only a sub-section of a source image, use `region(Region)`. 
- Construct the `Region` argument using `net.coobird.thumbnailator.geometry` classes: provide a `Position` (e.g., `Positions.TOP_LEFT` or `new Coordinate(x, y)`) and a `Size` (e.g., `new AbsoluteSize(width, height)`).
- Always chain this call with other required builder methods (like `size(int, int)`) and terminate the chain with `build()`.

### Prompt Snippet
```text
Use `.region(new Region(new Coordinate(x, y), new AbsoluteSize(w, h)))` on the ThumbnailParameterBuilder to crop the source image to a specific area before resizing.
```

### Common Failure Modes
- **Oversized Regions (Clamping):** If the specified `Region` dimensions exceed the actual bounds of the source image (e.g., requesting a 100x100 region starting at coordinate 20,20 on a 100x100 image), the library does not throw an exception. Instead, it safely clamps the region to the available image bounds (resulting in an 80x80 subimage).
- **Missing Terminal Operation:** Forgetting to call `.build()` at the end of the `ThumbnailParameterBuilder` chain, which returns the actual `ThumbnailParameter` required by image sources.
- **Missing Size Configuration:** Failing to specify the final thumbnail dimensions (e.g., `.size(w, h)`) on the builder before calling `.build()`.

### Fix Code Hint
```java
// Ensure the Region is instantiated with valid geometry objects and the builder is terminated with .build()
ThumbnailParameter params = new ThumbnailParameterBuilder()
    .region(new Region(new Coordinate(x, y), new AbsoluteSize(cropWidth, cropHeight)))
    .size(targetWidth, targetHeight)
    .build();
```

## API Test: `rendering`

### Signature
```java
public Builder<T> rendering(Rendering config)
```
_Source: source/src/main/java/net/coobird/thumbnailator/Thumbnails.java:1448_

_Source doc:_ Sets the rendering mode when performing the resizing operation to generate the thumbnail. <p> Calling this method to set this parameter is optional. <p> Calling this method multiple times will result in an {@link IllegalStateException} to be thrown. <p> This method cannot be called in conjunction with the {@link #resizerFactory(ResizerFactory)} method. @param config		The rendering mode. @return				Reference to this object.

### Goal
Sets the rendering mode (such as speed versus quality hints) to be used during the resizing operation in the thumbnail generation pipeline.

### Parameters
- `config` (`Rendering`): The rendering mode configuration to apply (e.g., `Rendering.DEFAULT`).

### Input
A valid `Thumbnails.Builder` instance that has been initialized with an image source. The `config` argument must be a non-null `Rendering` enum value. 
**Preconditions:** 
1. This method must not be called multiple times on the same builder instance.
2. This method cannot be called in conjunction with the `resizerFactory(ResizerFactory)` method on the same builder.

### Output
Returns `Builder<T>` — A reference to the current `Thumbnails.Builder` object to allow for fluent method chaining.

### Valid Call Patterns
```java
// given
BufferedImage img = new BufferedImageBuilder(200, 200).build();

// when
BufferedImage thumbnail = Thumbnails.of(img)
        .size(50, 50)
        .resizer(Resizers.PROGRESSIVE)
        .rendering(Rendering.DEFAULT)
        .asBufferedImage();
```

### LLM Instruction Prompt
- When configuring rendering hints in a Thumbnailator pipeline, use `rendering(Rendering config)`. You must pass a non-null `Rendering` value. Never call this method multiple times on the same builder, and never use it if `resizerFactory(ResizerFactory)` is also being used in the same pipeline.

### Prompt Snippet
```text
Use `rendering(Rendering config)` to set the rendering mode. Do not call it multiple times on the same builder or combine it with `resizerFactory()`. Ensure the argument is not null.
```

### Common Failure Modes
- **`NullPointerException`**: Thrown with the message `"Rendering is null."` if the `config` argument is `null`.
- **`IllegalStateException`**: Thrown if `rendering(...)` is called multiple times on the same `Thumbnails.Builder` instance.
- **`IllegalStateException`**: Thrown if this method is called on a builder that has already been configured with `resizerFactory(ResizerFactory)`.

### Fix Code Hint
```java
// Incorrect: Passing null or calling multiple times
// Thumbnails.of(img).size(50, 50).rendering(null).asBufferedImage();
// Thumbnails.of(img).size(50, 50).rendering(Rendering.QUALITY).rendering(Rendering.SPEED).asBufferedImage();

// Correct: Pass a valid Rendering enum exactly once
Thumbnails.of(img)
        .size(50, 50)
        .rendering(Rendering.DEFAULT)
        .asBufferedImage();
```

## API Test: `resize`

### Signature
```java
public void resize(BufferedImage srcImage, BufferedImage destImage)
```
_Source: source/src/main/java/net/coobird/thumbnailator/resizers/Resizers.java:97  (+6 more definition site/overload)_

### Goal
Performs a resize operation from a source image and draws the scaled result directly into a pre-allocated destination image using a specific scaling algorithm.

### Parameters
- `srcImage` (`BufferedImage`): The original source image to be resized.
- `destImage` (`BufferedImage`): The pre-allocated destination image where the resized output will be written.

### Input
Two instantiated `BufferedImage` objects. Neither image can be `null`. The caller is responsible for pre-allocating the `destImage` with the desired target dimensions (width and height) and an appropriate image type (e.g., `BufferedImage.TYPE_INT_ARGB`) before passing it to this method.

### Output
Returns `void` — the resized image data is written in-place directly into the provided `destImage` object.

### Valid Call Patterns
```java
// Derived from test suite usage of ProgressiveBilinearResizer and Resizer mocks
BufferedImage srcImage = new BufferedImage(200, 200, BufferedImage.TYPE_INT_ARGB);
BufferedImage destImage = new BufferedImage(100, 100, BufferedImage.TYPE_INT_ARGB);

Resizer resizer = new ProgressiveBilinearResizer();
resizer.resize(srcImage, destImage);
```

### LLM Instruction Prompt
- When calling `resize` on a `Resizer` implementation, you MUST ensure that neither `srcImage` nor `destImage` is `null`.
- You MUST pre-allocate the `destImage` `BufferedImage` to the exact target dimensions before calling this method.
- Note: For standard image resizing workflows, prefer the fluent `Thumbnails.of(srcImage).size(w, h).asBufferedImage()` API over manually instantiating a `Resizer` and calling `resize`, as the fluent builder automatically handles `BufferedImage` allocation, rendering hints, and Exif orientation corrections.

### Prompt Snippet
```text
When using Thumbnailator's `Resizer.resize(BufferedImage srcImage, BufferedImage destImage)`, ensure both images are non-null and `destImage` is pre-allocated to the target dimensions. Prefer the fluent `Thumbnails.of().size()` API for standard workflows to avoid manual `BufferedImage` management.
```

### Common Failure Modes
- **`NullPointerException`**: Thrown immediately if either the `srcImage` or the `destImage` is `null`.
- **Blank or Clipped Output**: Occurs if `destImage` is instantiated with incorrect dimensions (e.g., 0x0 or dimensions that do not match the intended scale factor) prior to calling `resize`.
- **Missing Exif Orientation**: Calling `resize` directly bypasses the `ExifFilterUtils` pipeline, meaning images with Exif orientation metadata will not be automatically rotated before resizing.

### Fix Code Hint
```java
// Ensure destImage is properly allocated and neither image is null
if (srcImage == null) {
    throw new IllegalArgumentException("Source image cannot be null");
}

int targetWidth = 100;
int targetHeight = 100;
// Pre-allocate the destination image
BufferedImage destImage = new BufferedImage(targetWidth, targetHeight, srcImage.getType() == BufferedImage.TYPE_CUSTOM ? BufferedImage.TYPE_INT_ARGB : srcImage.getType());

Resizer resizer = new ProgressiveBilinearResizer();
resizer.resize(srcImage, destImage);
```

## API Test: `resizer`

### Signature
```java
public Builder<T> resizer(Resizer resizer)
public ThumbnailParameterBuilder resizer(Resizer resizer)
public ThumbnailMaker resizer(Resizer resizer)
```
_Source: source/src/main/java/net/coobird/thumbnailator/Thumbnails.java:1323  (+2 more definition site/overload)_

_Source doc:_ Sets the resizing operation to use when creating the thumbnail. <p> Calling this method to set this parameter is optional. <p> Calling this method multiple times will result in an {@link IllegalStateException} to be thrown. <p> This method cannot be called in conjunction with the {@link #resizerFactory(ResizerFactory)} method. @param resizer		The scaling operation to use. @return				Reference to this object.

### Goal
Sets the specific scaling algorithm (such as progressive bilinear or bicubic) to be used when resizing the image in the thumbnail generation pipeline.

### Parameters
- `resizer` (`Resizer`): The scaling operation implementation to use. Common values include instances of `BicubicResizer`, `BilinearResizer`, `ProgressiveBilinearResizer`, `NullResizer`, or constants from the `Resizers` enum (e.g., `Resizers.PROGRESSIVE`).

### Input
A configured `Thumbnails.Builder` (or `ThumbnailParameterBuilder` / `ThumbnailMaker`) that is preparing to resize an image. The caller must provide a valid `Resizer` instance. The builder must not have already had a `resizer` or a `resizerFactory` set during its current configuration chain.

### Output
Returns `Builder<T>` (or the respective builder type) — a reference to the same builder object to allow for fluent method chaining.

### Valid Call Patterns
```java
// Explicitly setting a progressive resizer for high-quality downscaling
BufferedImage img = new BufferedImageBuilder(200, 200).build();

BufferedImage thumbnail = Thumbnails.of(img)
        .size(100, 100)
        .resizer(Resizers.PROGRESSIVE)
        .asBufferedImage();
```

### LLM Instruction Prompt
- Use `.resizer(Resizer)` to explicitly define the scaling algorithm for a Thumbnailator pipeline.
- NEVER call `.resizer()` multiple times on the same builder instance.
- NEVER call `.resizer()` if `.resizerFactory()` is also being used on the same builder.
- Setting this parameter is optional; if omitted, Thumbnailator will choose a default resizer based on the scaling mode and dimensions.

### Prompt Snippet
```text
When explicitly setting the scaling algorithm in Thumbnailator, use `.resizer(Resizer)`. Do not call this method multiple times per builder, and do not mix it with `.resizerFactory()`. Common values include `Resizers.PROGRESSIVE` for high-quality downscaling.
```

### Common Failure Modes
- **`IllegalStateException` (Multiple Invocations)**: Calling `.resizer(...)` more than once on the same builder instance will throw an `IllegalStateException`.
- **`IllegalStateException` (Factory Conflict)**: Calling `.resizer(...)` in conjunction with `.resizerFactory(...)` on the same builder will throw an `IllegalStateException`.

### Fix Code Hint
```java
// BAD: Calling resizer multiple times throws IllegalStateException
Thumbnails.of(img)
    .size(200, 200)
    .resizer(Resizers.PROGRESSIVE)
    .resizer(Resizers.BICUBIC) // Crashes here
    .asBufferedImage();

// GOOD: Call resizer exactly once, or omit it to use the default
Thumbnails.of(img)
    .size(200, 200)
    .resizer(Resizers.PROGRESSIVE)
    .asBufferedImage();
```

## API Test: `resizerFactory`

### Signature
```java
public Builder<T> resizerFactory(ResizerFactory resizerFactory)
public ThumbnailParameterBuilder resizerFactory(ResizerFactory resizerFactory)
public ThumbnailMaker resizerFactory(ResizerFactory resizerFactory)
```
_Source: source/src/main/java/net/coobird/thumbnailator/Thumbnails.java:1348  (+2 more definition site/overload)_

_Source doc:_ Sets the {@link ResizerFactory} object to use to decide what kind of resizing operation is to be used when creating the thumbnail. <p> Calling this method to set this parameter is optional. <p> Calling this method multiple times will result in an {@link IllegalStateException} to be thrown. <p> This method cannot be called in conjunction with the {@link #resizer(Resizer)} method. @param resizerFactory		The scaling operation to use. @return						Reference to this object. @since	0.4.0

### Goal
Sets the factory responsible for dynamically determining which resizing algorithm (e.g., bicubic, bilinear, progressive bilinear) to apply based on the original and target image dimensions.

### Parameters
- `resizerFactory` (`ResizerFactory`): The factory instance (such as `DefaultResizerFactory.getInstance()` or `FixedResizerFactory`) that will supply the `Resizer` for the scaling operation.

### Input
A valid `ResizerFactory` implementation. The builder instance must be in a state where neither `resizerFactory()` nor `resizer()` has been previously called.

### Output
Returns `Builder<T>` (or `ThumbnailParameterBuilder` / `ThumbnailMaker`, depending on the overload) — A reference to the current builder object to allow fluent method chaining.

### Valid Call Patterns
```java
// 1. Using ThumbnailParameterBuilder (Verified from test suite)
ResizerFactory resizerFactory = DefaultResizerFactory.getInstance();
ThumbnailParameter param = new ThumbnailParameterBuilder()
        .size(100, 100)
        .resizerFactory(resizerFactory)
        .build();

// 2. Using the fluent Thumbnails.Builder (Inferred from signature and standard usage)
Thumbnails.of(new File("original.jpg"))
        .size(200, 200)
        .resizerFactory(DefaultResizerFactory.getInstance())
        .toFile(new File("thumbnail.jpg"));
```

### LLM Instruction Prompt
- NEVER call `resizerFactory()` multiple times on the same builder instance.
- NEVER call `resizerFactory()` in conjunction with `resizer(Resizer)` on the same builder.
- Use `resizerFactory()` when you want the library to dynamically choose the best scaling algorithm based on the input and output dimensions, rather than hardcoding a specific `Resizer`.

### Prompt Snippet
```text
When configuring a Thumbnailator pipeline, use `.resizerFactory(ResizerFactory)` to dictate how the scaling algorithm is chosen. You must not call this method multiple times, nor can you mix it with `.resizer(Resizer)`. Doing so will throw an `IllegalStateException`.
```

### Common Failure Modes
- **`IllegalStateException` (Multiple Calls)**: Thrown if `resizerFactory(...)` is called more than once on the same builder instance.
- **`IllegalStateException` (Mutually Exclusive Configuration)**: Thrown if `resizerFactory(...)` is called on a builder that has already been configured with a specific resizer via `resizer(...)`, or vice versa.

### Fix Code Hint
```java
// BAD: Mixing resizer() and resizerFactory() causes an IllegalStateException
ThumbnailParameter param = new ThumbnailParameterBuilder()
        .size(100, 100)
        .resizer(new ProgressiveBilinearResizer())
        .resizerFactory(DefaultResizerFactory.getInstance()) // Throws IllegalStateException
        .build();

// GOOD: Choose exactly one strategy for defining the resizing behavior
ThumbnailParameter param = new ThumbnailParameterBuilder()
        .size(100, 100)
        .resizerFactory(DefaultResizerFactory.getInstance())
        .build();
```

## API Test: `rotate`

### Signature
```java
public Builder<T> rotate(double angle)
```
_Source: source/src/main/java/net/coobird/thumbnailator/Thumbnails.java:1969_

_Source doc:_ Sets the amount of rotation to apply to the thumbnail. <p> The thumbnail will be rotated clockwise by the angle specified. <p> This method can be called multiple times to apply multiple rotations. <p> If multiple rotations are to be applied, the rotations will be applied in the order that this method is called. <p> Calling this method to set this parameter is optional. @param angle			Angle in degrees. @return				Reference to this object.

### Goal
Adds a clockwise rotation transformation, specified in degrees, to the image processing pipeline for the generated thumbnail.

### Parameters
- `angle` (`double`): The angle in degrees by which the thumbnail will be rotated clockwise.

### Input
An active `Thumbnails.Builder<T>` pipeline initialized with an image source (e.g., `File`, `BufferedImage`, `InputStream`). Note that if the source image relies on Exif metadata for its correct initial orientation, manual rotation may compound incorrectly unless the Exif orientation is first parsed and corrected (e.g., via `ExifFilterUtils.getFilterForOrientation`).

### Output
Returns `Builder<T>` — A reference to the current `Thumbnails.Builder` instance, allowing for fluent method chaining.

### Valid Call Patterns
```java
// Inferred from the signature (not verified by test suite or README)
Thumbnails.of(new File("input.jpg"))
    .size(640, 480)
    .rotate(90.0)
    .toFile(new File("output.jpg"));
```

### LLM Instruction Prompt
- Use `rotate(double angle)` on a `Thumbnails.Builder` to rotate the image clockwise by the specified degrees.
- You may call this method multiple times on the same builder; the rotations will be applied sequentially in the exact order they are called.
- Do not confuse manual `rotate` with automatic Exif orientation correction. If correcting camera orientation, use `ExifFilterUtils` instead of guessing the `rotate` angle.
- Always terminate the builder chain with a valid sink operation (e.g., `toFile()`, `asBufferedImage()`).

### Prompt Snippet
```text
To rotate an image clockwise by a specific angle in degrees, chain `.rotate(double angle)` on the `Thumbnails.Builder`. Multiple calls apply rotations sequentially. Ensure you terminate the builder with an output method like `.toFile()`.
```

### Common Failure Modes
- **Unexpected Final Orientation**: Applying manual `rotate` to an image that already contains Exif orientation metadata without first normalizing it. The manual rotation will be applied on top of the raw pixel data, which might already be sideways.
- **Missing Terminal Operation**: Calling `.rotate(...)` but forgetting to invoke a terminal sink method (like `toFile` or `asBufferedImage`), resulting in the pipeline never executing and no image being produced.

### Fix Code Hint
```java
// Ensure the pipeline is properly terminated after configuring rotation
Thumbnails.of(new File("source.jpg"))
    .size(300, 300)
    .rotate(180.0) // Rotate 180 degrees clockwise
    .toFile(new File("upside_down_thumbnail.jpg")); // Required terminal operation
```

## API Test: `scale`

### Signature
```java
public Builder<T> scale(double scale)
public Builder<T> scale(double scaleWidth, double scaleHeight)
public ThumbnailParameterBuilder scale(double scalingFactor)
public ThumbnailParameterBuilder scale(double widthScalingFactor, double heightScalingFactor)
public ScaledThumbnailMaker scale(double factor)
public ScaledThumbnailMaker scale(double widthFactor, double heightFactor)
```
_Source: source/src/main/java/net/coobird/thumbnailator/Thumbnails.java:1023  (+5 more definition site/overload)_

_Source doc:_ Sets the scaling factor for the width and height of the thumbnail. <p> If the scaling factor for the width and height are not equal, then the thumbnail will not preserve the aspect ratio of the original image. <p> For example, to create thumbnails which are 50% the width of the original, while 75% the height of the original, the following code can be used: <pre><code> Thumbnails.of(image) .scale(0.5, 0.75) .toFile(thumbnail); </code></pre> <p> Once this method is called, calling the {@link #size(int, int)} method, or the {@link #scale(double)} method, or the {@link #keepAspectRatio(boolean)} method will result in an {@link IllegalStateException}. <p> Calling this method multiple times will result in an {@link IllegalStateException} to be thrown. @param scaleWidth	The scaling factor to use for the width when creating a thumbnail. <p> The value must be a {@code double} which is greater than {@code 0.0}, and not {@link Double#POSITIVE_INFINITY}. @param scaleHeight	The scaling factor to use for the height when creating a thumbnail. <p> The value must be a {@code double} which is greater than {@code 0.0}, and not {@link Double#POSITIVE_INFINITY}. @return				Reference to this object. @since 	0.3.10

### Goal
Sets the scaling factor for the width and height of the thumbnail, allowing independent scaling of each dimension which may alter the original aspect ratio.

### Parameters
- `scaleWidth` (`double`): The scaling factor to use for the width (e.g., `0.5` for 50% of the original width). Must be strictly greater than `0.0` and not `Double.POSITIVE_INFINITY`.
- `scaleHeight` (`double`): The scaling factor to use for the height (e.g., `0.75` for 75% of the original height). Must be strictly greater than `0.0` and not `Double.POSITIVE_INFINITY`.

### Input
A `Thumbnails.Builder` instance that has been initialized with an image source (such as a `File`, `BufferedImage`, `InputStream`, or `URL`). The caller must provide valid, finite, positive `double` values for the scaling factors.

### Output
Returns `Builder<T>` — a reference to the same builder object to allow for fluent method chaining in the image processing pipeline.

### Valid Call Patterns
```java
// From the source documentation (two-argument scale)
Thumbnails.of(image)
    .scale(0.5, 0.75)
    .toFile(thumbnail);

// Adapted from the test suite (single-argument scale for uniform scaling)
BufferedImage result = Thumbnails.of(sourceFile)
    .scale(0.5)
    .asBufferedImage();
```

### LLM Instruction Prompt
- When using `scale(double, double)` or `scale(double)`, you MUST NOT call `size(int, int)` or `keepAspectRatio(boolean)` on the same builder instance.
- Do not call `scale` multiple times on the same builder.
- Ensure the provided scaling factors are strictly greater than `0.0` and are not `Double.POSITIVE_INFINITY`.
- If `scaleWidth` and `scaleHeight` are different, the aspect ratio of the original image will not be preserved.

### Prompt Snippet
```text
Use `Thumbnails.of(input).scale(scaleWidth, scaleHeight)` to resize an image by specific multipliers. Do not mix `scale()` with `size()` or `keepAspectRatio()` in the same builder pipeline, as this will throw an IllegalStateException.
```

### Common Failure Modes
- **`IllegalStateException`**: Thrown if `scale()` is called multiple times on the same builder.
- **`IllegalStateException`**: Thrown if `scale()` is used in conjunction with `size(int, int)` or `keepAspectRatio(boolean)` on the same builder.
- **`IllegalArgumentException`**: Thrown if either `scaleWidth` or `scaleHeight` is less than or equal to `0.0`, or if they are set to `Double.POSITIVE_INFINITY` or `NaN`.

### Fix Code Hint
```java
// BAD: Mixing scale() with size() or keepAspectRatio()
Thumbnails.of(file).scale(0.5, 0.5).size(200, 200).toFile(out); // Throws IllegalStateException

// GOOD: Use either scale() OR size()
Thumbnails.of(file).scale(0.5, 0.5).toFile(out);
// OR
Thumbnails.of(file).size(200, 200).toFile(out);
```

## API Test: `scalingMode`

### Signature
```java
public Builder<T> scalingMode(ScalingMode config)
```
_Source: source/src/main/java/net/coobird/thumbnailator/Thumbnails.java:1300_

_Source doc:_ Sets the resizing scaling mode to use when creating the thumbnail. <p> Calling this method to set this parameter is optional. <p> Calling this method multiple times will result in an {@link IllegalStateException} to be thrown. @param config		The scaling mode to use. @return				Reference to this object.

### Goal
Sets the specific scaling algorithm mode (such as progressive bilinear) to be used by the resizer when generating the thumbnail.

### Parameters
- `config` (`ScalingMode`): The scaling mode configuration to apply to the resizing process (e.g., `ScalingMode.PROGRESSIVE_BILINEAR`).

### Input
A valid `Thumbnails.Builder` instance that has already been initialized with an image source (e.g., via `Thumbnails.of(...)`). Calling this method is entirely optional; if omitted, Thumbnailator will use its default scaling behavior.

### Output
Returns `Builder<T>` — A reference to the current fluent builder object, allowing for continued method chaining in the image processing pipeline.

### Valid Call Patterns
```java
// Applying a specific scaling mode during thumbnail generation
BufferedImage img = new BufferedImageBuilder(200, 200).build();

Thumbnails.of(img)
        .size(200, 200)
        .scalingMode(ScalingMode.PROGRESSIVE_BILINEAR)
        .asBufferedImage();
```

### LLM Instruction Prompt
- When configuring the scaling algorithm in a Thumbnailator pipeline, use `.scalingMode(ScalingMode.VALUE)`. 
- You MUST NOT call `scalingMode` more than once on the same builder instance, as doing so will throw an `IllegalStateException`.
- This method is optional; only invoke it if a specific scaling algorithm (like `PROGRESSIVE_BILINEAR`) is explicitly required by the user.

### Prompt Snippet
```text
To explicitly set the scaling algorithm for a thumbnail, chain `.scalingMode(ScalingMode.PROGRESSIVE_BILINEAR)` to the `Thumbnails.Builder`. Ensure this method is called at most once per pipeline to avoid an `IllegalStateException`.
```

### Common Failure Modes
- **`IllegalStateException`**: Thrown at runtime if `scalingMode(...)` is called multiple times on the same `Thumbnails.Builder` instance.

### Fix Code Hint
```java
// BAD: Calling scalingMode multiple times throws IllegalStateException
Thumbnails.of(img)
        .size(200, 200)
        .scalingMode(ScalingMode.PROGRESSIVE_BILINEAR)
        .scalingMode(ScalingMode.PROGRESSIVE_BILINEAR) // Crashes here
        .asBufferedImage();

// GOOD: Call scalingMode at most once per builder pipeline
Thumbnails.of(img)
        .size(200, 200)
        .scalingMode(ScalingMode.PROGRESSIVE_BILINEAR)
        .asBufferedImage();
```

## API Test: `setOutputFormatName`

### Signature
```java
public void setOutputFormatName(String format)
```
_Source: source/src/main/java/net/coobird/thumbnailator/tasks/io/AbstractImageSink.java:54  (+3 more definition site/overload)_

### Goal
Sets the output file format (e.g., "jpg", "png") for an `ImageSink` to dictate how the resulting image is encoded when written to its destination.

### Parameters
- `format` (`String`): The file format name with which to store the image.

### Input
A string representing an image format supported by the host JVM's standard Java Image I/O capabilities (commonly "jpg", "png", "gif", or "bmp"). 

### Output
Returns `void` — modifies the internal state of the `ImageSink` so that subsequent `write(BufferedImage)` operations encode the image using the specified format.

### Valid Call Patterns
```java
// Authoritative pattern from the project's test suite
ImageSink destination = mock(ImageSink.class);
when(destination.preferredOutputFormatName()).thenReturn("42a");

// The format is set on the sink prior to writing the image
destination.setOutputFormatName("42");
```

### LLM Instruction Prompt
- When manually configuring an `ImageSink` (such as a `FileImageSink` or `OutputStreamImageSink`) for a custom `ThumbnailTask`, you MUST call `setOutputFormatName(String)` before calling `write()`.
- Provide a standard format string supported by Java Image I/O.
- Be aware that for `ImageSink` implementations that store raw in-memory images (like `BufferedImageSink`), the format name specified by this method is ignored.

### Prompt Snippet
```text
When routing images to a custom `ImageSink`, call `destination.setOutputFormatName("jpg")` to configure the encoder before writing. Ensure the format string is supported by the JVM's Image I/O. Raw memory sinks will ignore this value.
```

### Common Failure Modes
- **Unsupported Format**: If the requested format string is not supported by the underlying Java Image I/O implementation, an `UnsupportedFormatException` will be thrown during the pipeline's write phase.
- **Silent Ignorance on Raw Sinks**: Calling this method on an `ImageSink` designed for raw images (e.g., returning a `BufferedImage` to memory) will not throw an error, but the format string will be safely ignored since no encoding takes place.

### Fix Code Hint
```java
// Ensure the format string is a standard, supported Image I/O format
ImageSink destination = new OutputStreamImageSink(myOutputStream);
destination.setOutputFormatName("png"); 
// Proceed to write the image to the sink
```

## API Test: `setThumbnailParameter`

### Signature
```java
public void setThumbnailParameter(ThumbnailParameter param)
```
_Source: source/src/main/java/net/coobird/thumbnailator/tasks/io/AbstractImageSink.java:58  (+6 more definition site/overload)_

### Goal
Sets the `ThumbnailParameter` configuration object on an image source or sink to dictate the parameters (such as size, region, and output format) to use when reading, processing, or storing the image.

### Parameters
- `param` (`ThumbnailParameter`): The configuration object containing image reading, processing, and writing parameters. This is typically constructed using a `ThumbnailParameterBuilder`.

### Input
An instantiated `ImageSource` (e.g., `BufferedImageSource`, `FileImageSource`) or `ImageSink` (e.g., `FileImageSink`, `OutputStreamImageSink`). The caller must provide a fully constructed `ThumbnailParameter` instance containing the desired dimensions, regions, or formatting rules. 

### Output
Returns `void` — mutates the state of the target `ImageSource` or `ImageSink` by assigning the provided parameters for subsequent `read()` or `write()` operations.

### Valid Call Patterns
```java
// given
BufferedImage sourceImage = getImageFromResource("Thumbnailator/grid.png");
BufferedImageSource source = new BufferedImageSource(sourceImage);

// configure the source with parameters before reading
source.setThumbnailParameter(
    new ThumbnailParameterBuilder()
        .region(new Region(Positions.TOP_LEFT, new AbsoluteSize(40, 40)))
        .size(20, 20)
        .build()
);

// when
BufferedImage img = source.read();
```

### LLM Instruction Prompt
- When interacting with low-level `ImageSource` or `ImageSink` objects directly in advanced workflows, you must configure them by passing a `ThumbnailParameter` (built via `ThumbnailParameterBuilder`) to `setThumbnailParameter` before invoking `read()` or `write()`. 
- Note that the fluent `Thumbnails.of(...)` API is strictly preferred for standard workflows; only use `setThumbnailParameter` when manually constructing `ThumbnailTask`, `ImageSource`, or `ImageSink` pipelines.

### Prompt Snippet
```text
To configure a low-level Thumbnailator ImageSource or ImageSink, call `source.setThumbnailParameter(new ThumbnailParameterBuilder().size(w, h).build());` before executing `read()` or `write()`. Prefer the fluent `Thumbnails.of()` API for standard use cases.
```

### Common Failure Modes
- **Unconfigured Source/Sink**: Forgetting to call `setThumbnailParameter` before calling `read()` on an `ImageSource` or `write()` on an `ImageSink`, which can result in missing sizing constraints or default/unintended behavior.
- **Unnecessary Low-Level Usage**: Manually instantiating sources/sinks and calling `setThumbnailParameter` when the task could be safely and deterministically handled by the preferred fluent builder (`Thumbnails.of(...).size(...).asBufferedImage()`).
- **Null Parameter**: Passing `null` instead of a valid `ThumbnailParameter` object, leading to `NullPointerException` during the read/write phase.

### Fix Code Hint
```java
// Incorrect: Attempting to read from a source without configuring parameters
BufferedImageSource source = new BufferedImageSource(myImage);
// BufferedImage img = source.read(); // May lack required sizing context

// Correct: Build and set the ThumbnailParameter first
source.setThumbnailParameter(
    new ThumbnailParameterBuilder()
        .size(100, 100)
        .build()
);
BufferedImage img = source.read();
```

## API Test: `size`

### Signature
```java
public Builder<T> size(int width, int height)
public int size()
public ThumbnailParameterBuilder size(Dimension size)
public ThumbnailParameterBuilder size(int width, int height)
public BufferedImageBuilder size(int width, int height)
public FixedSizeThumbnailMaker size(int width, int height)
```
_Source: source/src/main/java/net/coobird/thumbnailator/Thumbnails.java:843  (+5 more definition site/overload)_

_Source doc:_ Sets the size of the thumbnail. <p> For example, to create thumbnails which should fit within a bounding rectangle of 640 x 480, the following code can be used: <pre><code> Thumbnails.of(image) .size(640, 480) .toFile(thumbnail); </code></pre> <p> In the above code, the thumbnail will preserve the aspect ratio of the original image. If the thumbnail should be forced to the specified size, the {@link #forceSize(int, int)} method can be used instead of this method. <p> Once this method is called, calling the {@link #scale(double)} method will result in an {@link IllegalStateException}. <p> Calling this method multiple times will result in an {@link IllegalStateException} to be thrown. @param width			The width of the thumbnail. @param height		The height of the thumbnail. @return				Reference to this object.

### Goal
Sets the maximum dimensions for the generated thumbnail, scaling the image to fit within the specified bounding box while preserving its original aspect ratio.

### Parameters
- `width` (`int`): The maximum width of the thumbnail in pixels.
- `height` (`int`): The maximum height of the thumbnail in pixels.

### Input
A `Thumbnails.Builder` instance (or other builder like `ThumbnailParameterBuilder`) that has been initialized with an image source (e.g., `File`, `BufferedImage`, `InputStream`, `URL`). The environment must be headless.

### Output
Returns `Builder<T>` — A reference to the current builder object to allow method chaining in the fluent API pipeline.

### Valid Call Patterns
```java
// Resizing a single in-memory BufferedImage
BufferedImage thumbnail = Thumbnails.of(img)
    .size(100, 100)
    .asBufferedImage();

// Batch resizing files from a directory and saving them with a prefix
Thumbnails.of(new File("path/to/directory").listFiles())
    .size(640, 480)
    .outputFormat("jpg")
    .toFiles(Rename.PREFIX_DOT_THUMBNAIL);

// Configuring a ThumbnailParameterBuilder directly
ThumbnailParameter param = new ThumbnailParameterBuilder()
    .size(100, 100)
    .resizerFactory(resizerFactory)
    .build();
```

### LLM Instruction Prompt
- Use `.size(width, height)` to specify the bounding box for the thumbnail; the aspect ratio is preserved by default.
- If forcing exact dimensions without preserving the aspect ratio is required, use `.forceSize(int, int)` instead of `.size(int, int)`.
- NEVER call `.scale(double)` on a builder if `.size(int, int)` has already been called, as this will throw an `IllegalStateException`.
- NEVER call `.size(int, int)` multiple times on the same builder instance; this will also throw an `IllegalStateException`.

### Prompt Snippet
```text
When resizing images with Thumbnailator, use `.size(width, height)` on the `Thumbnails.Builder` to fit the image within the specified dimensions while preserving the aspect ratio. Never combine `.size()` with `.scale()` or call `.size()` multiple times on the same builder, as this throws an `IllegalStateException`. To ignore aspect ratio, use `.forceSize(width, height)` instead.
```

### Common Failure Modes
- **`IllegalStateException` (Mutually Exclusive Scaling)**: Thrown if `.scale(double)` is called on the same builder pipeline after `.size(int, int)` has been invoked.
- **`IllegalStateException` (Duplicate Sizing)**: Thrown if `.size(int, int)` is called more than once on the same builder instance.
- **Unexpected Aspect Ratio Distortion**: Occurs if a developer expects `.size(int, int)` to stretch the image to exact dimensions. `.size()` preserves aspect ratio; `.forceSize()` must be used for exact stretching.

### Fix Code Hint
```java
// BAD: Calling size() multiple times or mixing size() with scale()
Thumbnails.of(img)
    .size(200, 200)
    .scale(0.5) // Throws IllegalStateException
    .asBufferedImage();

// GOOD: Choose either size() OR scale(), not both
Thumbnails.of(img)
    .size(200, 200)
    .asBufferedImage();

// GOOD: If exact dimensions are needed without aspect ratio preservation
Thumbnails.of(img)
    .forceSize(200, 200)
    .asBufferedImage();
```

## API Test: `sourceRegion`

### Signature
```java
public Builder<T> sourceRegion(Region sourceRegion)
public Builder<T> sourceRegion(Position position, Size size)
public Builder<T> sourceRegion(int x, int y, int width, int height)
public Builder<T> sourceRegion(Position position, int width, int height)
public Builder<T> sourceRegion(Rectangle region)
```
_Source: source/src/main/java/net/coobird/thumbnailator/Thumbnails.java:1117  (+4 more definition site/overload)_

_Source doc:_ Specifies the region of the source image where the thumbnail will be created from. <p> Calling this method multiple times will result in an {@link IllegalStateException} to be thrown. @param x				The horizontal-component of the top left-hand corner of the source region. @param y				The vertical-component of the top left-hand corner of the source region. @param width			Width of the source region. @param height		Height of the source region. @return				Reference to this object. @throws IllegalArgumentException	If the width and/or height is less than or equal to {@code 0}. @since 	0.3.4

### Goal
Specifies a specific rectangular sub-region of the original source image to use for creating the thumbnail, effectively cropping the input before resizing or applying filters.

### Parameters
- `x` (`int`): The horizontal-component (X coordinate) of the top left-hand corner of the source region.
- `y` (`int`): The vertical-component (Y coordinate) of the top left-hand corner of the source region.
- `width` (`int`): Width of the source region. Must be strictly greater than `0`.
- `height` (`int`): Height of the source region. Must be strictly greater than `0`.

### Input
- An active `Thumbnails.Builder` instance (e.g., created via `Thumbnails.of(...)`).
- The `width` and `height` arguments must be strictly positive integers (`> 0`).
- If using the object-based overloads (`Region`, `Position`, `Size`, `Rectangle`), the provided objects must not be `null`.
- This method must be called at most **once** per builder pipeline.

### Output
Returns `Builder<T>` — A reference to the current `Thumbnails.Builder` object to allow method chaining in the fluent API.

### Valid Call Patterns
```java
// Using the Region overload (verified by test suite)
BufferedImage thumbnail1 = Thumbnails.of(img)
        .sourceRegion(new Region(new Coordinate(0, 0), new AbsoluteSize(50, 50)))
        .size(50, 50)
        .asBufferedImage();

// Using the primitive int overload (inferred from signature)
BufferedImage thumbnail2 = Thumbnails.of(img)
        .sourceRegion(0, 0, 50, 50)
        .size(50, 50)
        .asBufferedImage();
```

### LLM Instruction Prompt
- Use `sourceRegion` to crop the *input* image before resizing or applying filters.
- NEVER call `sourceRegion` more than once on the same builder instance; doing so throws an `IllegalStateException`.
- Ensure `width` and `height` are strictly positive (`> 0`).
- Do not pass `null` to the object-based overloads (e.g., `Region`, `Rectangle`).

### Prompt Snippet
```text
To crop a specific area from the source image before resizing, use `.sourceRegion(x, y, width, height)` or `.sourceRegion(new Region(...))` on the `Thumbnails.Builder`. Call this method exactly once per pipeline. Ensure width and height are > 0.
```

### Common Failure Modes
- **`IllegalStateException`**: Thrown if `sourceRegion` is called multiple times on the same `Thumbnails.Builder` instance.
- **`IllegalArgumentException`**: Thrown if the provided `width` and/or `height` is less than or equal to `0`.
- **`NullPointerException`**: Thrown if a `null` object is passed to one of the object-based overloads (e.g., `sourceRegion((Region) null)`).

### Fix Code Hint
```java
// BAD: Calling sourceRegion multiple times or with invalid dimensions
Thumbnails.of(img)
    .sourceRegion(0, 0, -10, 50) // throws IllegalArgumentException (width <= 0)
    .sourceRegion(10, 10, 20, 20) // throws IllegalStateException (called twice)
    .size(50, 50)
    .asBufferedImage();

// GOOD: Call exactly once with positive dimensions
Thumbnails.of(img)
    .sourceRegion(0, 0, 50, 50)
    .size(50, 50)
    .asBufferedImage();
```

## API Test: `toFile`

### Signature
```java
public void toFile(File outFile)
public void toFile(String outFilepath)
```
_Source: source/src/main/java/net/coobird/thumbnailator/Thumbnails.java:2652  (+1 more definition site/overload)_

_Source doc:_ Create a thumbnail and writes it to a {@link File}. <p> When the destination file exists, and overwriting files has been disabled by calling the {@link #allowOverwrite(boolean)} method with {@code false}, then an {@link IllegalArgumentException} will be thrown. <p> To call this method, the thumbnail must have been created from a single source. @param outFile			The file to which the thumbnail is to be written to. @throws IOException		If a problem occurs while reading the original images or writing the thumbnails to files. @throws IllegalArgumentException		If multiple original image files are	specified, or if the destination file exists, and overwriting files is disabled.

### Goal
Execute the configured image processing pipeline and write the resulting single thumbnail to the specified destination file.

### Parameters
- `outFile` (`File`): The destination file where the generated thumbnail will be written. (The overload accepts a `String` representing the file path).

### Input
A fully configured `Thumbnails.Builder` pipeline that was initialized with exactly **one** image source (e.g., a single `File`, `BufferedImage`, `InputStream`, or `URL`). The output format will be inferred from the destination file's extension unless explicitly overridden in the pipeline via `.outputFormat(String)`.

### Output
Returns `void` — The operation is a terminal sink; its side effect is the creation or overwriting of the thumbnail file on disk.

### Valid Call Patterns
```java
// Example 1: Writing a file source to a file destination with an explicit format
Thumbnails.of(sourceFile)
        .size(640, 480)
        .outputFormat("jpg")
        .toFile(destFile);

// Example 2: Writing an in-memory BufferedImage to a file, inferring format from extension
BufferedImage img = new BufferedImageBuilder(200, 200).build();
File destFile = new File(temporaryFolder.getRoot(), "tmp.png");

Thumbnails.of(img)
        .size(100, 100)
        .toFile(destFile);
```

### LLM Instruction Prompt
- Call `toFile` only when the `Thumbnails.Builder` was created from a single source. Do not use this method for batch processing multiple images.
- If the destination file already exists, it will be overwritten by default unless `.allowOverwrite(false)` was explicitly called on the builder.
- Ensure the requested output format (either inferred from the `outFile` extension or set via `.outputFormat()`) is supported by the host JVM's Image I/O capabilities.
- Handle `IOException` for potential read/write failures.

### Prompt Snippet
```text
Terminal operation `toFile(File)` or `toFile(String)` writes a single thumbnail to disk. MUST be called on a pipeline with exactly ONE source. Throws IllegalArgumentException if called on a multi-source builder or if the file exists and `.allowOverwrite(false)` was set. Throws IOException on I/O errors.
```

### Common Failure Modes
- **`IllegalArgumentException` (Multiple Sources)**: Thrown if the builder was initialized with multiple sources (e.g., `Thumbnails.of(file1, file2)` or an `Iterable`) because `toFile` can only write a single output file.
- **`IllegalArgumentException` (Overwrite Disabled)**: Thrown if the destination file already exists and the pipeline was configured with `.allowOverwrite(false)`.
- **`UnsupportedFormatException`**: Thrown if the output format (inferred from the file extension or explicitly requested) is not supported by the underlying Java Image I/O implementation.
- **`IOException`**: Thrown if the original image cannot be read or the destination file cannot be written (e.g., missing permissions or invalid path).

### Fix Code Hint
```java
// BAD: Calling toFile on a multi-source builder throws IllegalArgumentException
Thumbnails.of(new File("dir").listFiles())
    .size(100, 100)
    .toFile(new File("output.jpg")); // Fails!

// GOOD: Use toFiles() with a Rename strategy for multiple sources
Thumbnails.of(new File("dir").listFiles())
    .size(100, 100)
    .toFiles(Rename.PREFIX_DOT_THUMBNAIL);

// GOOD: Use toFile() for a single source
Thumbnails.of(new File("dir/single.jpg"))
    .size(100, 100)
    .toFile(new File("output.jpg"));
```

## API Test: `toFiles`

### Signature
```java
public void toFiles(Iterable<File> iterable)
public void toFiles(Rename rename)
public void toFiles(File destinationDir, Rename rename)
```
_Source: source/src/main/java/net/coobird/thumbnailator/Thumbnails.java:2627  (+2 more definition site/overload)_

_Source doc:_ Creates thumbnails and stores them to files in the directory specified by the given {@link File} object, and using the {@link Rename} function to determine the filenames. <p> When the destination file exists, and overwriting files has been disabled by calling the {@link #allowOverwrite(boolean)} method with {@code false}, then the thumbnail with the destination file already existing will not be written. <p> Extra caution should be taken when using this method, as there are no protections in place to prevent file name collisions resulting from creating thumbnails from files in separate directories but having the same name. In such a case, the behavior will be depend on the behavior of the {@link #allowOverwrite(boolean)} as described in the previous paragraph. <p> To call this method, the thumbnails must have been creates from files by calling the {@link Thumbnails#of(File...)} method. @param destinationDir	The destination directory to which the thumbnails should be written to. @param rename			The rename function which is used to determine the filenames of the thumbnail files to write. @throws IOException		If a problem occurs while reading the original images or writing the thumbnails to files. thumbnails to files. @throws IllegalStateException		If the original images are not from files. @throws IllegalArgumentException		If the destination directory is not a directory. @since 	0.4.7

### Goal
Executes the image processing pipeline and writes the resulting batch of thumbnails to the filesystem, either by applying a renaming strategy to the original filenames or by mapping them to an explicit iterable of destination files.

### Parameters
- `destinationDir` (`File`): The destination directory to which the thumbnails should be written. Must be an existing directory.
- `rename` (`Rename`): The renaming strategy used to dynamically generate output filenames (e.g., `Rename.PREFIX_DOT_THUMBNAIL`).

### Input
The caller must have constructed a valid `Thumbnails.Builder` pipeline containing one or more image sources. 
- **Precondition for `Rename` overloads**: If calling `toFiles(Rename)` or `toFiles(File, Rename)`, the original images *must* have been sourced from files (e.g., via `Thumbnails.of(File...)` or `Thumbnails.fromFiles(...)`). 
- **Precondition for `Iterable<File>` overload**: If the sources are not files (e.g., `InputStream`, `BufferedImage`, `URL`), the caller *must* use `toFiles(Iterable<File>)` to explicitly provide the destination files. The number of destination files must match the number of input sources.

### Output
Returns `void` — This is a terminal operation that triggers the execution of the image processing pipeline, writing the processed images directly to the specified files on disk.

### Valid Call Patterns
```java
// Pattern 1: Using a Rename strategy when inputs are Files (from README)
Thumbnails.of(new File("path/to/directory").listFiles())
    .size(640, 480)
    .outputFormat("jpg")
    .toFiles(Rename.PREFIX_DOT_THUMBNAIL);

// Pattern 2: Providing explicit destination files when inputs are InputStreams (from test suite)
File outFile1 = new File(temporaryFolder.getRoot(), "out1.jpg");
File outFile2 = new File(temporaryFolder.getRoot(), "out2.jpg");

Thumbnails.fromInputStreams(getSources())
    .size(100, 100)
    .toFiles(Arrays.asList(outFile1, outFile2));
```

### LLM Instruction Prompt
- Always use `toFiles` as a terminal operation to conclude a `Thumbnails.Builder` pipeline when batch processing images to disk.
- You MUST use `toFiles(Iterable<File>)` if the input sources are streams, URLs, or in-memory images.
- You may only use `toFiles(Rename)` or `toFiles(File, Rename)` if the input sources are explicitly `File` objects or file paths.
- When using `Rename` constants, strictly avoid the deprecated typos `Rename.PREFIX_HYPTHEN_THUMBNAIL` and `Rename.SUFFIX_HYPTHEN_THUMBNAIL`. Use `Rename.PREFIX_HYPHEN_THUMBNAIL` and `Rename.SUFFIX_HYPHEN_THUMBNAIL` instead.
- Be aware of filename collisions if processing files from different directories that share the same name; use `allowOverwrite(false)` on the builder if you want to prevent overwriting existing files.

### Prompt Snippet
```text
When batch processing images with Thumbnailator, terminate the `Thumbnails.Builder` pipeline using `toFiles(Rename)` ONLY if the inputs are files. If inputs are streams, URLs, or BufferedImages, you must use `toFiles(Iterable<File>)` to avoid an `IllegalStateException`. Never use the deprecated typo `Rename.PREFIX_HYPTHEN_THUMBNAIL`; use `Rename.PREFIX_HYPHEN_THUMBNAIL`.
```

### Common Failure Modes
- **`IllegalStateException`**: Thrown if `toFiles(Rename)` or `toFiles(File, Rename)` is called but the original images were not sourced from files (e.g., they were `InputStream` or `BufferedImage`).
- **`IllegalArgumentException`**: Thrown if the `destinationDir` provided to `toFiles(File, Rename)` is not a valid directory.
- **`IOException`**: Thrown if a problem occurs while reading the original images or writing the thumbnails to the filesystem.
- **`UnsupportedFormatException`**: Thrown if an output format is requested (via `.outputFormat(...)`) that the underlying Java Image I/O implementation does not support.
- **Silent Overwrites**: By default, if a destination file already exists, it will be overwritten. This can cause data loss if files from different source directories have the same name. Mitigate this by calling `.allowOverwrite(false)` on the builder before calling `toFiles`.

### Fix Code Hint
```java
// BAD: Using Rename with InputStream sources throws IllegalStateException
Thumbnails.fromInputStreams(streams)
    .size(200, 200)
    .toFiles(Rename.PREFIX_DOT_THUMBNAIL);

// GOOD: Provide explicit output files for non-file sources
Thumbnails.fromInputStreams(streams)
    .size(200, 200)
    .toFiles(Arrays.asList(file1, file2));

// GOOD: Use Rename when sources are explicitly Files
Thumbnails.fromFiles(files)
    .size(200, 200)
    .toFiles(Rename.PREFIX_DOT_THUMBNAIL);
```

## API Test: `toOutputStream`

### Signature
```java
public void toOutputStream(OutputStream os)
```
_Source: source/src/main/java/net/coobird/thumbnailator/Thumbnails.java:2728_

_Source doc:_ Create a thumbnail and writes it to a {@link OutputStream}. <p> To call this method, the thumbnail must have been created from a single source. <p> Note that the {@link OutputStream#close()} method will not be called upon the completion of the thumbnail being written to the {@link OutputStream}. @param os				The output stream to which the thumbnail is to be written to. @throws IOException		If a problem occurs while reading the original images or writing the thumbnails. @throws IllegalArgumentException		If multiple original image files are	specified. @throws IllegalStateException		If the output format has not been specified through the {@link #outputFormat(String)} method.

### Goal
Executes the image processing pipeline and writes the resulting single thumbnail to the provided `OutputStream`.

### Parameters
- `os` (`OutputStream`): The destination stream to which the encoded thumbnail image data will be written. The caller retains ownership of this stream; Thumbnailator will *not* call `close()` on it.

### Input
The caller must provide an open, writable `OutputStream`. 
**Preconditions:**
1. The `Thumbnails.Builder` must have been initialized with exactly *one* image source (e.g., a single `BufferedImage`, `File`, or `InputStream`).
2. The output format *must* be explicitly specified using `.outputFormat(String)` (e.g., `"png"`, `"jpg"`) prior to calling this method, because streams and in-memory images do not inherently provide a file extension to infer the format from.

### Output
Returns `void` — This is a terminal operation that consumes the builder pipeline, processes the image in memory, and flushes the encoded bytes to the provided stream.

### Valid Call Patterns
```java
// given
BufferedImage img = new BufferedImage(200, 200, BufferedImage.TYPE_INT_ARGB);
ByteArrayOutputStream os = new ByteArrayOutputStream();

// when
Thumbnails.of(img)
    .size(50, 50)
    .outputFormat("png") // REQUIRED before toOutputStream
    .toOutputStream(os);

// The caller is responsible for closing the stream
os.close(); 
```

### LLM Instruction Prompt
- When writing a Thumbnailator pipeline to an `OutputStream`, you MUST explicitly set the output format using `.outputFormat("jpg")` (or another valid format) before calling `.toOutputStream(os)`.
- You MUST ensure the builder was initialized with a single image source; batch processing to a single `OutputStream` is not supported.
- You MUST manually close the `OutputStream` in a `finally` block or try-with-resources, as `toOutputStream` explicitly does not close it.

### Prompt Snippet
```text
When terminating a Thumbnailator pipeline with `.toOutputStream(OutputStream)`, you must first call `.outputFormat(String)` to define the image encoding (e.g., "png", "jpg"). The pipeline must contain exactly one image source. Do not expect Thumbnailator to close the stream; wrap your stream in a try-with-resources block.
```

### Common Failure Modes
- **`IllegalStateException` ("Output format not specified.")**: Thrown if `.outputFormat(String)` was omitted. This is guaranteed to fail when the source is a `BufferedImage` or `InputStream` because there is no original file extension to fall back on.
- **`IllegalArgumentException`**: Thrown if the builder was initialized with multiple image sources (e.g., `Thumbnails.fromFiles(listOfFiles)`).
- **`IOException`**: Thrown if the underlying Java Image I/O fails to write to the provided stream.
- **Resource Leaks**: Occurs if the caller assumes Thumbnailator closes the `OutputStream` and fails to close it themselves.

### Fix Code Hint
```java
// BAD: Missing output format and stream closure
ByteArrayOutputStream os = new ByteArrayOutputStream();
Thumbnails.of(bufferedImage)
    .size(100, 100)
    .toOutputStream(os); // Throws IllegalStateException

// GOOD: Explicit format and try-with-resources
try (ByteArrayOutputStream os = new ByteArrayOutputStream()) {
    Thumbnails.of(bufferedImage)
        .size(100, 100)
        .outputFormat("jpg")
        .toOutputStream(os);
}
```

## API Test: `toOutputStreams`

### Signature
```java
public void toOutputStreams(Iterable<? extends OutputStream> iterable)
```
_Source: source/src/main/java/net/coobird/thumbnailator/Thumbnails.java:2777_

_Source doc:_ Creates the thumbnails and writes them to {@link OutputStream}s provided by the {@link Iterable}. <p> Note that the {@link OutputStream#close()} method will not be called upon the completion of the thumbnail being written to the {@link OutputStream}. @param iterable			An {@link Iterable} which returns an {@link Iterator} which returns the output stream which should be assigned to each thumbnail. @throws IOException		If a problem occurs while reading the original images or writing the thumbnails. @throws IllegalStateException		If the output format has not been specified through the {@link #outputFormat(String)} method.

### Goal
Executes the image processing pipeline and writes the resulting thumbnails to a sequence of output streams provided by an `Iterable`.

### Parameters
- `iterable` (`Iterable<? extends OutputStream>`): An `Iterable` (such as a `List`) that provides an `Iterator` returning the specific `OutputStream` to which each processed thumbnail should be written.

### Input
The caller must have an active `Thumbnails.Builder` pipeline containing one or more image sources. Because output streams do not have filenames from which an image format can be inferred, the caller **must** explicitly specify the output format using the `.outputFormat(String)` method before invoking `toOutputStreams`. The number of streams yielded by the `Iterable` should correspond to the number of input images being processed.

### Output
Returns `void` — the method's side effect is writing the encoded image bytes to the provided streams. The underlying `OutputStream` instances are **not** closed by this method upon completion.

### Valid Call Patterns
```java
// given
BufferedImage img = new BufferedImageBuilder(200, 200).build();
ByteArrayOutputStream os = new ByteArrayOutputStream();

// when
Thumbnails.of(img)
    .size(50, 50)
    .outputFormat("png") // REQUIRED before calling toOutputStreams
    .toOutputStreams(Arrays.asList(os));

// The caller is responsible for closing the stream(s)
os.close();
```

### LLM Instruction Prompt
- When routing Thumbnailator output to streams via `toOutputStreams`, you MUST explicitly set the image format using `.outputFormat("jpg")` (or similar) beforehand.
- Do not expect Thumbnailator to close the output streams; the caller must manage stream lifecycles (e.g., using try-with-resources).

### Prompt Snippet
```text
When calling `toOutputStreams(Iterable<? extends OutputStream>)` on a `Thumbnails.Builder`, you must first call `.outputFormat(String)` to specify the encoding format (e.g., "png", "jpg"). Failure to do so will result in an `IllegalStateException`. Additionally, Thumbnailator does not call `close()` on the provided streams, so ensure you close them manually or use try-with-resources.
```

### Common Failure Modes
- **`IllegalStateException` ("Output format not specified.")**: Thrown if the pipeline attempts to write to streams but `.outputFormat(String)` was never called on the builder.
- **`IOException`**: Thrown if a problem occurs while reading the original images or writing the bytes to the provided output streams.
- **Resource Leaks**: Occurs if the caller assumes `toOutputStreams` closes the streams and fails to close them manually.

### Fix Code Hint
```java
// BAD: Missing outputFormat and stream closure
ByteArrayOutputStream os = new ByteArrayOutputStream();
Thumbnails.of(image).size(100, 100).toOutputStreams(Arrays.asList(os));

// GOOD: Explicit format and try-with-resources
try (ByteArrayOutputStream os = new ByteArrayOutputStream()) {
    Thumbnails.of(image)
        .size(100, 100)
        .outputFormat("jpg") // Fixes IllegalStateException
        .toOutputStreams(Arrays.asList(os));
    // use os.toByteArray()
}
```

## API Test: `typeOf`

### Signature
```java
public static Orientation typeOf(int value)
public static IfdType typeOf(int value)
```
_Source: source/src/main/java/net/coobird/thumbnailator/util/exif/Orientation.java:124  (+1 more definition site/overload)_

_Source doc:_ Returns the {@link Orientation} corresponding to the given orientation value. @param value		The orientation value. @return			{@link Orientation} corresponding to the orientation value. Return {@code null} if the given value does not correspond to a	valid {@link Orientation}.

### Goal
Converts a raw integer Exif orientation or IFD type value into its corresponding `Orientation` or `IfdType` enum instance for use in image processing pipelines.

### Parameters
- `value` (`int`): The integer value representing the Exif orientation (typically 1 through 8) or the IFD type extracted from image metadata.

### Input
An integer extracted from an image's Exif metadata. The caller must parse the Exif metadata beforehand to obtain this integer, as Thumbnailator does not automatically extract this when reading directly from a `BufferedImage`.

### Output
Returns `Orientation` (or `IfdType` for the overload) — The enum instance corresponding to the provided integer value. Returns `null` if the given integer does not map to a valid, known orientation or IFD type.

### Valid Call Patterns
```java
// Correcting orientation when reading from a BufferedImage
BufferedImage result =
        Thumbnails.of(ImageIO.read(is))
                .addFilter(ExifFilterUtils.getFilterForOrientation(Orientation.typeOf(orientation)))
                .size(width, height)
                .asBufferedImage();
```

### LLM Instruction Prompt
- When applying Exif orientation corrections to a `BufferedImage` source, use `Orientation.typeOf(int)` to convert the raw integer orientation into an `Orientation` enum.
- Pass the resulting enum to `ExifFilterUtils.getFilterForOrientation()` and add the returned `ImageFilter` to the pipeline via `Thumbnails.Builder.addFilter()`.
- Always account for the fact that `typeOf` returns `null` if the integer is invalid; do not pass `null` blindly to filter utilities.

### Prompt Snippet
```text
To correct image orientation from raw Exif integer values, use `Orientation.typeOf(intValue)` to get the enum. Pass this enum to `ExifFilterUtils.getFilterForOrientation()` and add the resulting filter to the `Thumbnails.Builder` using `.addFilter()`. Ensure you handle potential `null` returns if the integer is invalid.
```

### Common Failure Modes
- **NullPointerException in Filter Creation**: Passing an invalid integer (e.g., `0` or `9`) to `Orientation.typeOf()` returns `null`. Passing this `null` directly into `ExifFilterUtils.getFilterForOrientation()` will cause a failure.
- **Missing Exif Extraction**: Attempting to guess the orientation integer without properly parsing the source file's Exif metadata first.

### Fix Code Hint
```java
Orientation orientationEnum = Orientation.typeOf(orientationValue);
if (orientationEnum != null) {
    builder.addFilter(ExifFilterUtils.getFilterForOrientation(orientationEnum));
}
```

## API Test: `useExifOrientation`

### Signature
```java
public boolean useExifOrientation()
public Builder<T> useExifOrientation(boolean useExifOrientation)
public ThumbnailParameterBuilder useExifOrientation(boolean use)
```
_Source: source/src/main/java/net/coobird/thumbnailator/Thumbnails.java:1700  (+2 more definition site/overload)_

_Source doc:_ Sets whether or not to use the Exif metadata when orienting the thumbnail. <p> Calling this method multiple times will result in an {@link IllegalStateException} to be thrown. @param useExifOrientation	{@code true} if the Exif metadata should be used to determine the orientation of the thumbnail, {@code false} otherwise. @return						Reference to this object. @since	0.4.3

### Goal
Configures the thumbnail generation pipeline to automatically read Exif metadata and correct the image orientation before applying further transformations.

### Parameters
- `useExifOrientation` (`boolean`): `true` if the Exif metadata should be used to determine and correct the orientation of the thumbnail, `false` to ignore Exif orientation data.

### Input
A `Thumbnails.Builder` instance that has been initialized with an image source (such as `File`, `InputStream`, or `URL`). The underlying image format must support and contain Exif metadata (typically JPEG) for this operation to have a visual effect.

### Output
Returns `Builder<T>` — A reference to the current builder object to allow for fluent method chaining.

### Valid Call Patterns
```java
// Example 1: Enabling Exif orientation correction for a stream-based pipeline
Thumbnails.of(source1, source2)
    .size(100, 100)
    .useExifOrientation(true)
    .toOutputStreams(Arrays.asList(baos1, baos2));

// Example 2: Explicitly disabling Exif orientation correction
Thumbnails.of(source1, source2)
    .size(100, 100)
    .useExifOrientation(false)
    .toOutputStreams(Arrays.asList(baos1, baos2));
```

### LLM Instruction Prompt
- When processing photographs (especially JPEGs from cameras or mobile devices), call `.useExifOrientation(true)` on the `Thumbnails.Builder` to ensure the image is rotated correctly before resizing or cropping.
- NEVER call `useExifOrientation` multiple times on the same builder instance, as this violates the builder's state constraints and will throw an `IllegalStateException`.

### Prompt Snippet
```text
To automatically rotate images based on their Exif orientation metadata, call `.useExifOrientation(true)` on the `Thumbnails.Builder`. Do not call this method more than once per builder instance to avoid an IllegalStateException.
```

### Common Failure Modes
- **`IllegalStateException`**: Thrown if `useExifOrientation(boolean)` is called more than once on the same `Thumbnails.Builder` instance.

### Fix Code Hint
```java
// BAD: Calling useExifOrientation multiple times throws IllegalStateException
Thumbnails.of(file)
    .useExifOrientation(true)
    .size(200, 200)
    .useExifOrientation(false) // Throws IllegalStateException
    .toFile(outputFile);

// GOOD: Call useExifOrientation exactly once in the pipeline
Thumbnails.of(file)
    .useExifOrientation(true)
    .size(200, 200)
    .toFile(outputFile);
```

## API Test: `useOriginalFormat`

### Signature
```java
public Builder<T> useOriginalFormat()
```
_Source: source/src/main/java/net/coobird/thumbnailator/Thumbnails.java:1680_

_Source doc:_ Sets the compression format to use the same format as the original image. <p> Calling this method multiple times will result in an {@link IllegalStateException} to be thrown. @return				Reference to this object. @since	0.4.0

### Goal
Sets the output compression format of the thumbnail to match the format of the original source image.

### Parameters
_None._

### Input
An active `Thumbnails.Builder` pipeline containing an image source with a determinable format (such as a file or stream parsed by Java Image I/O). This method must be called at most once per builder instance.

### Output
Returns `Builder<T>` — a reference to the current builder object to allow fluent method chaining.

### Valid Call Patterns
```java
// Preserving the original format (e.g., PNG) when resizing and saving to a file
Thumbnails.of(sourceFile)
        .size(10, 10)
        .useOriginalFormat()
        .toFile(destFile);
```

### LLM Instruction Prompt
- Call `useOriginalFormat()` on a `Thumbnails.Builder` when the output thumbnail must retain the exact image format (e.g., PNG, JPEG) of the input source.
- NEVER call this method multiple times on the same builder instance, as it will throw an `IllegalStateException`.
- Be aware of filename resolution when using `toFile()`: if the destination `File` has an extension that differs from the original format, Thumbnailator will append the original format's extension to the provided filename (e.g., writing a PNG source to `dest.jpg` with `useOriginalFormat()` results in a file named `dest.jpg.png`).

### Prompt Snippet
```text
To preserve the original image format during resizing, call `.useOriginalFormat()` on the `Thumbnails.Builder` chain. Do not call it more than once per builder. When saving to a file, ensure the destination filename either lacks an extension or matches the original format to avoid appended extensions like `output.jpg.png`.
```

### Common Failure Modes
- **`IllegalStateException`**: Thrown if `useOriginalFormat()` is called multiple times on the same `Thumbnails.Builder` instance.
- **Unexpected Output Filenames**: If the caller provides a destination file with a specific extension (e.g., `dest.jpg`) but the original source image is a different format (e.g., PNG), the library will append the correct extension to the output file, resulting in a double extension (e.g., `dest.jpg.png`).

### Fix Code Hint
```java
// BAD: Calling useOriginalFormat multiple times throws IllegalStateException
Thumbnails.of(sourceFile)
    .size(100, 100)
    .useOriginalFormat()
    .useOriginalFormat() // Throws IllegalStateException
    .toFile(new File("out"));

// GOOD: Call exactly once
Thumbnails.of(sourceFile)
    .size(100, 100)
    .useOriginalFormat()
    .toFile(new File("out")); // If source is PNG, outputs to "out.png"
```

## API Test: `useOriginalImageType`

### Signature
```java
public boolean useOriginalImageType()
```
_Source: source/src/main/java/net/coobird/thumbnailator/ThumbnailParameter.java:953_

_Source doc:_ Returns whether or not the original image type should be used for the thumbnail. @return		{@code true} if the original image type should be used, {@code false} otherwise.

### Goal
Returns a boolean indicating whether the thumbnail generation process is configured to preserve and use the original source image's `BufferedImage` type.

### Parameters
_None._

### Input
A valid, instantiated `ThumbnailParameter` object. This method is typically called internally by the Thumbnailator pipeline or by advanced users inspecting a custom `ThumbnailTask` configuration.

### Output
Returns `boolean` — `true` if the original image type (e.g., `BufferedImage.TYPE_INT_ARGB`, `BufferedImage.TYPE_3BYTE_BGR`) should be preserved for the output thumbnail; `false` otherwise.

### Valid Call Patterns
```java
// Note: Call form is inferred from the signature as no direct examples were found in the project context.
// Assumes 'parameter' is an existing ThumbnailParameter instance.
boolean keepOriginalType = parameter.useOriginalImageType();

if (keepOriginalType) {
    // The pipeline will use ThumbnailParameter.ORIGINAL_IMAGE_TYPE (-1) logic
    // to match the source BufferedImage type.
}
```

### LLM Instruction Prompt
- When inspecting a `ThumbnailParameter` configuration, call `useOriginalImageType()` to determine if the output `BufferedImage` is set to inherit the exact in-memory image type of the source image. Do not confuse this with the output file format (e.g., JPEG, PNG); this strictly refers to the Java 2D `BufferedImage` type.

### Prompt Snippet
```text
Use `useOriginalImageType()` on a `ThumbnailParameter` instance to check if the pipeline is configured to retain the source image's `BufferedImage` type (e.g., `TYPE_INT_ARGB`). This corresponds to the `ThumbnailParameter.ORIGINAL_IMAGE_TYPE` (-1) constant behavior.
```

### Common Failure Modes
- **NullPointerException**: Attempting to call this method on an uninitialized or null `ThumbnailParameter` reference.
- **Semantic Confusion (Type vs. Format)**: Mistaking "image type" for the file format (like "jpg" or "png"). This method checks the in-memory `BufferedImage` type (e.g., `TYPE_INT_RGB`), whereas file formats are managed by `outputFormat()` and checked via other parameter properties.

### Fix Code Hint
```java
// Ensure the receiver is a valid ThumbnailParameter instance
if (parameter != null) {
    boolean useOriginal = parameter.useOriginalImageType();
    // Use this boolean to understand the in-memory BufferedImage type behavior, 
    // not the file output format.
}
```

## API Test: `value`

### Signature
```java
public int value()
```
_Source: source/src/main/java/net/coobird/thumbnailator/util/exif/IfdType.java:102_

_Source doc:_ Returns the IFD type as a type value. @return	IFD type as a type value.

### Goal
Returns the integer representation of an Image File Directory (IFD) type used during Exif metadata parsing.

### Parameters
_None._

### Input
An instantiated `IfdType` object (typically an enum constant representing a specific Exif IFD section), which is used internally or during advanced Exif metadata extraction to determine image orientation.

### Output
Returns `int` — the raw integer value corresponding to the specific IFD type.

### Valid Call Patterns
```java
// Inferred from the signature (not verified by test suite or README)
int typeValue = ifdType.value();
```

### LLM Instruction Prompt
- Use `value()` when you need to extract the raw integer identifier of an `IfdType` instance, typically when manually inspecting Exif metadata structures to correct image orientation before processing.
- Do not invent `IfdType` instances; they are provided by the `net.coobird.thumbnailator.util.exif` package.

### Prompt Snippet
```text
When evaluating Exif metadata for image orientation correction, use `ifdType.value()` to retrieve the underlying integer value of the Image File Directory (IFD) type.
```

### Common Failure Modes
- **`NullPointerException`**: Occurs if `value()` is called on a null `IfdType` reference.

### Fix Code Hint
```java
if (ifdType != null) {
    int rawValue = ifdType.value();
    // Process the IFD type value
}
```

## API Test: `watermark`

### Signature
```java
public Builder<T> watermark(Watermark w)
public Builder<T> watermark(BufferedImage image)
public Builder<T> watermark(BufferedImage image, float opacity)
public Builder<T> watermark(Position position, BufferedImage image, float opacity)
public Builder<T> watermark(Position position, BufferedImage image, float opacity, int insets)
```
_Source: source/src/main/java/net/coobird/thumbnailator/Thumbnails.java:1944  (+4 more definition site/overload)_

_Source doc:_ Sets the image, opacity, position and insets for the watermark to apply on to the thumbnail. <p> This method can be called multiple times to apply multiple watermarks. <p> If multiple watermarks are to be applied, the watermarks will be applied in the order that this method is called. <p> Calling this method to set this parameter is optional. @param position		The position of the watermark. @param image			The image of the watermark. @param opacity		The opacity of the watermark. <p> The value should be between {@code 0.0f} and {@code 1.0f}, where {@code 0.0f} is completely transparent, and {@code 1.0f} is completely opaque. @param insets		Inset size around the watermark. Cannot be negative. @return				Reference to this object.

### Goal
Adds a watermark image overlay to the thumbnail processing pipeline at a specified position, opacity, and inset padding.

### Parameters
- `position` (`Position`): The placement of the watermark on the thumbnail (typically provided via the `net.coobird.thumbnailator.geometry.Positions` enum, such as `Positions.CENTER` or `Positions.TOP_LEFT`).
- `image` (`BufferedImage`): The in-memory image to be used as the watermark overlay.
- `opacity` (`float`): The transparency level of the watermark, where `0.0f` is completely transparent and `1.0f` is completely opaque.
- `insets` (`int`): The padding or margin size in pixels around the watermark. Cannot be negative.

### Input
The caller must have an active `Thumbnails.Builder` pipeline. The watermark image must be a valid, loaded `BufferedImage`. The `opacity` must be strictly bounded between `0.0f` and `1.0f`. If using the overload with `insets`, the inset value must be `0` or greater.

### Output
Returns `Builder<T>` — the same fluent builder instance, allowing for method chaining to add more transformations (including additional watermarks) or to route the output to a sink (e.g., `asBufferedImage()`, `toFile()`).

### Valid Call Patterns
```java
// Applying a centered watermark with 100% opacity
BufferedImage thumbnail = Thumbnails.of(ORIGINAL_IMAGE)
        .size(100, 100)
        .crop(Positions.CENTER)
        .watermark(Positions.CENTER, WATERMARK_IMAGE, 1.0f)
        .asBufferedImage();

// Applying a top-left watermark with 100% opacity
BufferedImage thumbnail2 = Thumbnails.of(ORIGINAL_IMAGE)
        .size(100, 100)
        .crop(Positions.CENTER)
        .watermark(Positions.TOP_LEFT, WATERMARK_IMAGE, 1.0f)
        .asBufferedImage();
```

### LLM Instruction Prompt
- When adding a watermark using Thumbnailator, chain the `.watermark()` method on the `Thumbnails.Builder`.
- Use the `Positions` enum (e.g., `Positions.BOTTOM_RIGHT`, `Positions.CENTER`) for the `Position` parameter.
- Ensure the `opacity` parameter is a `float` strictly between `0.0f` and `1.0f`.
- Ensure the `insets` parameter (if used) is not negative.
- You may call `.watermark()` multiple times on the same builder to apply multiple watermarks; they will be applied in the order called.

### Prompt Snippet
```text
To apply a watermark in Thumbnailator, chain `.watermark(Position, BufferedImage, float)` to the `Thumbnails.Builder`. Use the `Positions` enum for placement (e.g., `Positions.BOTTOM_RIGHT`). The opacity must be a float between 0.0f (transparent) and 1.0f (opaque). Multiple watermarks can be layered by calling the method multiple times.
```

### Common Failure Modes
- **IllegalArgumentException**: Thrown if the `opacity` is outside the valid range of `0.0f` to `1.0f` (e.g., passing `100.0f` instead of `1.0f`).
- **IllegalArgumentException**: Thrown if a negative value is provided for the `insets` parameter.
- **NullPointerException**: Thrown if the provided `BufferedImage` for the watermark or the `Position` is `null`.

### Fix Code Hint
```java
// Incorrect: Opacity is out of bounds (50.0f instead of 0.5f) and insets are negative
// builder.watermark(Positions.BOTTOM_RIGHT, watermarkImg, 50.0f, -5);

// Correct: Opacity is a float between 0.0f and 1.0f, and insets are non-negative
builder.watermark(Positions.BOTTOM_RIGHT, watermarkImg, 0.5f, 10);
```

## API Test: `width`

### Signature
```java
public Builder<T> width(int width)
public BufferedImageBuilder width(int width)
```
_Source: source/src/main/java/net/coobird/thumbnailator/Thumbnails.java:872  (+1 more definition site/overload)_

_Source doc:_ Sets the width of the thumbnail. <p> The thumbnail will have the dimensions constrained by the specified width, and the aspect ratio of the original image will be preserved by the thumbnail. <p> Once this method is called, calling the {@link #size(int, int)} or the {@link #scale(double)} method will result in an {@link IllegalStateException}. <p> Calling this method multiple times will result in an {@link IllegalStateException} to be thrown. @param width			The width of the thumbnail. @return				Reference to this object. @since 	0.3.5

### Goal
Sets the target width for the thumbnail while automatically calculating the height to preserve the original image's aspect ratio.

### Parameters
- `width` (`int`): The desired width of the generated thumbnail in pixels.

### Input
A `Thumbnails.Builder` instance initialized with an image source (e.g., `File`, `BufferedImage`, `InputStream`). The builder must be in a state where no other primary sizing operations (`size`, `scale`, or a previous `width`) have been applied.

### Output
Returns `Builder<T>` — The same builder instance for fluent chaining, now configured to resize the image to the specified width.

### Valid Call Patterns
```java
// Derived from test suite setup: resizing an in-memory image by width only
BufferedImage img = new BufferedImageBuilder(200, 200).build();

BufferedImage thumbnail = Thumbnails.of(img)
        .width(50)
        .asBufferedImage();
```

### LLM Instruction Prompt
- Use `width(int)` when you need to constrain an image to a specific width and want Thumbnailator to automatically preserve the aspect ratio.
- NEVER call `width(int)` multiple times on the same builder instance.
- NEVER combine `width(int)` with `size(int, int)` or `scale(double)` in the same pipeline. Doing so violates the builder's state constraints and will crash the pipeline.

### Prompt Snippet
```text
To resize an image to a specific width while preserving its aspect ratio, use `.width(int)`. Do not combine this with `.size()`, `.scale()`, or multiple `.width()` calls on the same builder, as this will throw an `IllegalStateException`.
```

### Common Failure Modes
- **`IllegalStateException` from multiple sizing calls**: Calling `width(int)` more than once on the same builder, or calling `size(int, int)` or `scale(double)` after `width(int)` has already been set, will throw an `IllegalStateException`. The test suite explicitly verifies these failure modes.

### Fix Code Hint
```java
// BAD: Throws IllegalStateException (combining width and size)
Thumbnails.of(img)
        .width(50)
        .size(50, 50)
        .asBufferedImage();

// BAD: Throws IllegalStateException (calling width twice)
Thumbnails.of(img)
        .width(50)
        .width(100)
        .asBufferedImage();

// GOOD: Use exactly one sizing method per builder pipeline
Thumbnails.of(img)
        .width(50)
        .asBufferedImage();
```

## API Test: `write`

### Signature
```java
public void write(BufferedImage img)
public abstract void write(BufferedImage img)
```
_Source: source/src/main/java/net/coobird/thumbnailator/tasks/StreamThumbnailTask.java:81  (+8 more definition site/overload)_

### Goal
Writes a processed `BufferedImage` thumbnail to the underlying destination (such as a file, output stream, or memory sink) configured by the implementing task or sink.

### Parameters
- `img` (`BufferedImage`): The processed in-memory image to write to the destination.

### Input
A valid, non-null `BufferedImage` that has typically completed its transformation pipeline (resizing, cropping, rotating, etc.). The underlying destination (e.g., `OutputStream` or `File`) must be open and writable. The configured output format must be supported by the host JVM's standard Image I/O capabilities.

### Output
Returns `void` — The image is written to the configured destination as a side effect.

### Valid Call Patterns
```java
// Note: This example is inferred from the signature (not verified by test/README examples).
// `write` is typically called internally by Thumbnailator's pipeline or when 
// implementing custom ImageSink / ThumbnailTask abstractions.

ImageSink<File> sink = new FileImageSink(new File("output.png"));
sink.write(processedBufferedImage);
```

### LLM Instruction Prompt
- When interacting with Thumbnailator's low-level `ImageSink` or `ThumbnailTask` abstractions, use `write(BufferedImage)` to output the final image to its destination. 
- Always handle `IOException` (for stream/file write failures) and `UnsupportedFormatException` (if the JVM's Image I/O does not support the target format). 
- Note: For standard workflows, strictly prefer the fluent builder API (e.g., `Thumbnails.of(...).toFile(...)`) over manually instantiating sinks and calling `write`.

### Prompt Snippet
```text
When implementing custom Thumbnailator sinks or tasks, use `write(BufferedImage img)` to output the processed image. You must handle `IOException` for underlying stream failures and `UnsupportedFormatException` if the requested output format is unsupported by the JVM. For standard use cases, prefer the fluent `Thumbnails.of().toFiles()` terminal methods instead of calling `write` manually.
```

### Common Failure Modes
- **`IOException`**: Thrown when an I/O problem occurs while writing the image to the underlying destination (e.g., writing to a closed `OutputStream`, or lacking file system permissions).
- **`UnsupportedFormatException`**: Thrown when the requested output format is not supported by the underlying Java Image I/O implementation.
- **`NullPointerException`**: Thrown if the provided `BufferedImage` is null.

### Fix Code Hint
```java
try {
    // Assuming 'sink' is an instantiated ImageSink or ThumbnailTask
    sink.write(processedImage);
} catch (UnsupportedFormatException e) {
    // Handle missing Image I/O codec (e.g., fallback to a standard format like "jpg" or "png")
    System.err.println("Format not supported by JVM Image I/O: " + e.getMessage());
} catch (IOException e) {
    // Handle underlying stream or file system write errors
    System.err.println("Failed to write thumbnail: " + e.getMessage());
}
```

