# Deep-dive: `load_wav`

model: google:gemini-3.1-pro-preview · tokens in=5,281 out=3,079 · wall 28s · 2026-09-08 01:41

---

**L0 AUDIENCE + TESTABILITY CLASSIFICATION**
- **Classification:** USER-FACING (Deprecated)
- **Testability:** TESTABLE FROM PUBLIC INPUTS
- **Explanation:** This is a public module-level function intended for end-users to load audio files, as evidenced by its presence in the documentation and test suite. It is fully testable from public inputs, provided a valid `.wav` file exists on disk (which can be programmatically generated during the test). Note that it is explicitly marked as deprecated and slated for removal in version 0.9.0, so it may be excluded from benchmarks targeting the latest library versions.

**L1 PURPOSE**
`load_wav` is an I/O helper function that reads a WAV audio file from disk, normalizes its integer PCM samples to floating-point values in the range `[-1.0, 1.0]`, and optionally downmixes multi-channel audio to mono. It serves as a standardized entry point for loading audio data into NumPy arrays for downstream evaluation metrics and displays within the `mir_eval` ecosystem.

**L2 CONTRACT**
- **Receiver:** None (module-level function in `mir_eval.io`).
- **Parameters:**
  - `path` (`str` or `os.Pathlike`): The file path to the `.wav` file to be loaded.
  - `mono` (`bool`, default `True`): If `True`, multi-channel audio will be averaged across channels to produce a single-channel (mono) signal. If `False`, the original channel dimensions are preserved.
- **Returns:** A tuple of `(audio_data, fs)`:
  - `audio_data` (`np.ndarray`): Array of audio samples, normalized to the float range `[-1.0, 1.0]`.
  - `fs` (`int`): The sampling rate of the audio data in Hz.
- **Visibility:** Public (Decorated with `@util.deprecated`).
- **Side Effects:** Reads from the local filesystem.

**L3 MECHANICS**
1. The function delegates file reading to `scipy.io.wavfile.read(path)`, which returns `(fs, audio_data)` (source: `source/mir_eval/io.py:432`).
2. It inspects `audio_data.dtype` to perform bit-depth specific normalization to the `[-1.0, 1.0]` range:
   - `int8`: divides by `2**8` (256.0).
   - `int16`: divides by `2**16` (65536.0).
   - `int32`: divides by `2**24` (16777216.0).
3. If the `dtype` is anything else (e.g., `float32` or `uint8`), it raises a `ValueError` with the message `"Got unexpected .wav data type {}"` (source: `source/mir_eval/io.py:441`).
4. If `mono=True` and the array has more than one dimension (`audio_data.ndim != 1`), it downmixes to mono by averaging across the channel axis using `audio_data.mean(axis=1)` (source: `source/mir_eval/io.py:444`).
5. It returns the tuple `(audio_data, fs)`.

**L4 CORRECT MINIMAL USAGE**
```python
import os
import numpy as np
import scipy.io.wavfile
import warnings
from mir_eval.io import load_wav

# 1. Create a temporary valid 16-bit PCM WAV file to satisfy the disk requirement
test_path = "temp_test_audio.wav"
fs_out = 44100
# 1 second of stereo silence in int16
raw_audio = np.zeros((fs_out, 2), dtype=np.int16)
scipy.io.wavfile.read = lambda *args: (fs_out, raw_audio) # Mocking to avoid disk I/O if preferred, but let's write it:
scipy.io.wavfile.write(test_path, fs_out, raw_audio)

try:
    # 2. Call the function, suppressing the deprecation warning for clean execution
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=DeprecationWarning)
        audio_data, fs_in = load_wav(test_path, mono=True)

    # 3. Verify contract
    assert fs_in == fs_out
    assert audio_data.ndim == 1  # Successfully downmixed to mono
    assert audio_data.shape[0] == fs_out
finally:
    # 4. Cleanup
    if os.path.exists(test_path):
        os.remove(test_path)
```

**L5 FAILURE FORENSICS**
- **`FileNotFoundError: [Errno 2] No such file or directory: '.../test_load.wav'`**: The execution harness attempted to call `load_wav` on a file path before actually generating and writing the dummy `.wav` file to disk. Because `load_wav` delegates directly to `scipy.io.wavfile.read`, it strictly requires the file to exist on the filesystem at the moment of invocation.

**L6 SELF-ASSESSMENT**
- **Inferences:** 
  - I inferred that the resulting `audio_data` array will be of type `np.float64`, as dividing an integer NumPy array by a Python float (e.g., `float(2**16)`) or calling `.mean()` implicitly casts the array to `float64` in standard NumPy behavior.
- **Information needed for certainty:** None. The provided source code contains the entirety of the function's logic and its direct dependencies.
- **Confidence Scores:**
  - **L2 (Contract): 10/10** - The docstring and return statements explicitly define the types, shapes, and tuple unpacking order.
  - **L3 (Mechanics): 10/10** - The function is short, self-contained, and all conditional branches (dtype checks, mono conversion) are fully visible in the provided snippet.
  - **L4 (Minimal Usage): 10/10** - Creating a dummy WAV file using `scipy.io.wavfile.write` is the standard, deterministic way to test audio I/O functions without relying on external binary fixtures.