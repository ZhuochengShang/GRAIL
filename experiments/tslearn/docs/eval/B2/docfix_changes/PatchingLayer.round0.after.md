## API Test: `PatchingLayer`
_Grounding: doc-repaired from source (docfix)._

### Signature
```python
class PatchingLayer(shapelet_length, **kwargs)
```

### Goal
ADVANCED/LOW-LEVEL: Format 3D time-series data into 4D patches matching shapelet lengths. Note: This is an internal framework helper and should generally be excluded from the main user-facing denominator, but it is executable directly for testing.

### Parameters
- `shapelet_length` (int): Required. The length of the shapelet patches to extract.
- `**kwargs`: Additional keyword arguments passed to the base Keras `Layer`.

### Input
ADVANCED/LOW-LEVEL: A 3D NumPy array (or tensor) of shape `(batch_size, steps, features)`.

### Output
A 4D tensor (or array) of shape `(batch_size, steps - shapelet_length + 1, shapelet_length, features)`.

### Valid Call Patterns
```python
import numpy as np
from tslearn.shapelets import PatchingLayer

# Instantiate the layer with the required shapelet_length
layer = PatchingLayer(shapelet_length=3)

# Create a 3D NumPy array: (batch_size, steps, features)
X_np = np.zeros((2, 10, 1), dtype=np.float32)

# Call the layer directly with the NumPy array
out = layer(X_np)

assert len(out.shape) == 4
assert out.shape == (2, 8, 3, 1)
```

### LLM Instruction Prompt
- Use `PatchingLayer` to format 3D time-series arrays into 4D patch arrays.
- You MUST provide the `shapelet_length` parameter to the constructor.
- Pass a 3D NumPy array of shape `(batch_size, steps, features)` directly to the layer instance.
- Do not explicitly import `tensorflow` as it may not be available in all environments; rely on NumPy arrays for inputs.

### Prompt Snippet
```text
`tslearn.shapelets.PatchingLayer` is an advanced internal layer that formats 3D time-series arrays `(batch_size, steps, features)` into 4D patch arrays `(batch_size, steps - shapelet_length + 1, shapelet_length, features)`. Requires `shapelet_length` on init.
```

### Common Failure Modes
- *ADVANCED/LOW-LEVEL API*: This is an internal framework helper.
- Failing to provide the required `shapelet_length` parameter in the constructor (previously documented incorrectly as taking no parameters).
- Explicitly importing `tensorflow` in environments where it is not installed; the layer can process NumPy arrays directly.
- Passing a 2D array instead of the required 3D array `(batch_size, steps, features)`.

### Fix Code Hint
```python
# WRONG: Missing shapelet_length and importing tensorflow
import tensorflow as tf
from tslearn.shapelets import PatchingLayer
layer = PatchingLayer()
out = layer(tf.zeros((2, 10, 1)))

# CORRECT: Pass shapelet_length and use NumPy
import numpy as np
from tslearn.shapelets import PatchingLayer
layer = PatchingLayer(shapelet_length=3)
out = layer(np.zeros((2, 10, 1), dtype=np.float32))
```