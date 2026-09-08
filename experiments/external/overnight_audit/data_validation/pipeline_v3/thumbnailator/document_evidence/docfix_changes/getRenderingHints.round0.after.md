## API Test: `getRenderingHints`
_Grounding: doc-repaired from source (docfix)._

### Signature
```java
public Map<RenderingHints.Key, Object> getRenderingHints()
```

### Goal
ADVANCED/LOW-LEVEL API. Exclude from main user-facing benchmark denominator. Returns the standard Java 2D rendering hints configuration map used by a specific `AbstractResizer` implementation.

### Parameters
_None._

### Input
ADVANCED/LOW-LEVEL. Requires explicit low-level construction of a concrete subclass of `AbstractResizer` (e.g., `BicubicResizer`). The receiver variable MUST be typed as `AbstractResizer` or a concrete subclass. Do not type the receiver as the `Resizer` interface.

### Output
Returns `Map<RenderingHints.Key, Object>` — An unmodifiable, read-only map containing `java.awt.RenderingHints.Key` instances and their corresponding values.

### Valid Call Patterns
```java
import net.coobird.thumbnailator.resizers.BicubicResizer;
import java.util.Map;
import java.awt.RenderingHints;

// Receiver MUST be typed as the concrete class or AbstractResizer
BicubicResizer resizer = new BicubicResizer();
Map<RenderingHints.Key, Object> hints = resizer.getRenderingHints();

Object interpValue = hints.get(RenderingHints.KEY_INTERPOLATION);
System.out.println("__CHECK__ getRenderingHints " + interpValue);
```

### LLM Instruction Prompt
Type the receiver as `AbstractResizer` or a concrete subclass (like `BicubicResizer`). Do not use the `Resizer` interface type, as it lacks this method and will cause a compilation failure.

### Prompt Snippet
To inspect rendering hints, instantiate a concrete resizer (e.g., `BicubicResizer resizer = new BicubicResizer();`) and call `resizer.getRenderingHints()`. The receiver must not be typed as the `Resizer` interface.

### Common Failure Modes
- **"cannot find symbol" on `getRenderingHints()`**: Occurs if the receiver is typed as the `Resizer` interface. The interface does not declare this method; it is defined in `AbstractResizer`.
- **ADVANCED/LOW-LEVEL API**: This is an internal/framework API requiring explicit low-level construction. Exclude from main user-facing denominator.
- **Modification Exceptions**: Attempting to modify the returned map will fail because it is unmodifiable.

### Fix Code Hint
```java
// WRONG: Typing as Resizer interface causes "cannot find symbol"
net.coobird.thumbnailator.resizers.Resizer resizer = new net.coobird.thumbnailator.resizers.BicubicResizer();
java.util.Map<java.awt.RenderingHints.Key, Object> hints = resizer.getRenderingHints();

// CORRECT: Type as concrete class or AbstractResizer
net.coobird.thumbnailator.resizers.BicubicResizer resizer = new net.coobird.thumbnailator.resizers.BicubicResizer();
java.util.Map<java.awt.RenderingHints.Key, Object> hints = resizer.getRenderingHints();
```