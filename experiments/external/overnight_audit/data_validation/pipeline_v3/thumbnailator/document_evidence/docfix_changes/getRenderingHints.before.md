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