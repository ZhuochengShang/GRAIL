### 1. Project purpose
Thumbnailator is a single-JAR, zero-dependency Java library designed to generate high-quality image thumbnails. It abstracts away the complexities of the Java Image I/O API, the Java 2D API, and manual image scaling techniques, allowing developers to perform complex image processing and resizing tasks safely and deterministically without needing to manually manipulate `BufferedImage` or `Graphics2D` objects.

### 2. Main workflows
The primary workflow utilizes a fluent builder interface to construct image processing pipelines. Users define one or more image sources, apply a sequence of transformations (such as resizing, cropping, rotating, or watermarking), configure rendering hints (like antialiasing or dithering), and finally route the processed images to a designated sink (files, streams, or memory). Advanced workflows involve constructing custom `ThumbnailTask` instances (e.g., `FileThumbnailTask`, `StreamThumbnailTask`) or building custom `Pipeline` objects containing multiple `ImageFilter` implementations.

### 3. Important APIs and usage patterns
*   **`Thumbnails` and `Thumbnails.Builder`**: The main entry points for the fluent API. `Thumbnails` provides static factory methods (`of`, `fromFiles`, `fromFilenames`, `fromImages`, `fromInputStreams`, `fromURLs`) that return a `Thumbnails.Builder`.
*   **Builder Configuration Methods**: `size(int, int)`, `forceSize(int, int)`, `crop(Position)`, `alphaInterpolation(AlphaInterpolation)`, `antialiasing(Antialiasing)`, `dithering(Dithering)`, `determineOutputFormat()`, `allowOverwrite(boolean)`.
*   **`ImageFilter`**: An interface for applying transformations. Built-in filters in `net.coobird.thumbnailator.filters` include `Canvas`, `Caption`, `Colorize`, `Flip`, `Rotation`, `SwapDimensions`, `Transparency`, and `Watermark`. Filters are added via `Thumbnails.Builder.addFilter(ImageFilter)`.
*   **`Resizer` and `ResizerFactory`**: Interfaces controlling the scaling algorithm. Implementations include `BicubicResizer`, `BilinearResizer`, `ProgressiveBilinearResizer`, and `NullResizer`. Factories include `DefaultResizerFactory` and `FixedResizerFactory`.
*   **Geometry and Positioning**: The `net.coobird.thumbnailator.geometry` package provides the `Position` interface (with the `Positions` enum and `Coordinate` class), as well as `Size` implementations (`AbsoluteSize`, `RelativeSize`) and `Region`.
*   **`Rename`**: A utility class used to dynamically generate output filenames during batch processing (e.g., `Rename.PREFIX_DOT_THUMBNAIL`).

### 4. Inputs and file formats
Thumbnailator accepts multiple input types via the `Thumbnails` factory methods or `ImageSource` implementations (`FileImageSource`, `InputStreamImageSource`, `URLImageSource`, `BufferedImageSource`):
*   `java.io.File` or `Iterable<File>`
*   `java.lang.String` (representing file paths) or `Iterable<String>`
*   `java.awt.image.BufferedImage` or `Iterable<BufferedImage>`
*   `java.io.InputStream` or `Iterable<? extends InputStream>`
*   `java.net.URL` or `Iterable<URL>`

### 5. Outputs and generated artifacts
Processed thumbnails are routed to sinks via terminal methods on `Thumbnails.Builder` or `ImageSink` implementations (`FileImageSink`, `OutputStreamImageSink`, `BufferedImageSink`):
*   **In-memory**: `asBufferedImage()` (returns a single `BufferedImage`) or `asBufferedImages()` (returns a `List<BufferedImage>`).
*   **Files**: `toFile(File)`, `toFiles(Rename)`, `toFiles(Iterable<File>)`, `asFiles(Rename)`, or `asFiles(Iterable<File>)`.
*   **Streams**: `toOutputStream(OutputStream)`.

### 6. Configuration and environment assumptions
*   **Environment**: The library is designed to run headless and requires no external dependencies, cameras, or desktop UI. It relies entirely on the host JVM's standard Image I/O capabilities for format support.
*   **Constants**: `ThumbnailParameter` defines defaults such as `DEFAULT_IMAGE_TYPE` (2), `DEFAULT_QUALITY` (NaN), `DETERMINE_FORMAT` ("\0"), and `ORIGINAL_IMAGE_TYPE` (-1).
*   **Configurations**: The `Configurations` enum and `ResizerConfiguration` interface manage rendering hints like `AlphaInterpolation`, `Antialiasing`, `Dithering`, `Rendering`, and `ScalingMode`.

### 7. Commands and examples
Creating JPEG thumbnails of image files in a directory, resized to a maximum dimension of 640x480 while preserving the aspect ratio, and saving them with a specific prefix:

```java
Thumbnails.of(new File("path/to/directory").listFiles())
    .size(640, 480)
    .outputFormat("jpg")
    .toFiles(Rename.PREFIX_DOT_THUMBNAIL);
```

### 8. Constraints, preconditions, compatibility rules, and type-selection rules
*   **Deprecations**: The legacy methods `Thumbnailator.createThumbnails` and `Thumbnailator.createThumbnailsAsCollection` are deprecated and must be replaced with the `Thumbnails.fromFiles(Iterable)` fluent interface.
*   **Spelling Corrections**: The constants `Rename.PREFIX_HYPTHEN_THUMBNAIL` and `Rename.SUFFIX_HYPTHEN_THUMBNAIL` are deprecated due to typos. Code must use `Rename.PREFIX_HYPHEN_THUMBNAIL` and `Rename.SUFFIX_HYPHEN_THUMBNAIL` instead.
*   **Exif Orientation Preconditions**: To ensure images are rotated correctly before processing, Exif metadata must be parsed. `ExifUtils.getExifOrientation` extracts the `Orientation`, and `ExifFilterUtils.getFilterForOrientation(Orientation)` returns the specific `ImageFilter` required to correct the image's orientation in the pipeline.
*   **Batch File Output Rules**: When outputting multiple files to a directory using `toFiles()` or `asFiles()`, a `Rename` strategy or an instance of `ConsecutivelyNumberedFilenames` must be provided to prevent filename collisions.
*   **Format Support**: If an output format is requested that the underlying Java Image I/O does not support, an `UnsupportedFormatException` is thrown.

### 9. Facts to preserve in the final README
*   The library is distributed as a single JAR with zero external dependencies.
*   It is licensed under the MIT License.
*   The fluent interface (`Thumbnails.of(...)`) is the strictly preferred paradigm over manual `Thumbnailator.createThumbnail(...)` static method calls.
*   The library handles the boilerplate of `Graphics2D` manipulation and Image I/O automatically.

### 10. Missing or weak documentation
*   **Filter Parameters**: The exact constructor arguments and behavioral nuances for complex filters like `Caption` (font, color, positioning), `Watermark`, and `Colorize` are visible in the Javadoc index but lack detailed prose explanations of their effects.
*   **Resizer Differences**: The specific algorithmic differences and performance trade-offs between `BicubicResizer`, `BilinearResizer`, and `ProgressiveBilinearResizer` are not clearly documented.
*   **Supported Formats**: The documentation does not explicitly list supported read/write formats, implicitly relying on the user to know what their specific JVM's Image I/O implementation supports.