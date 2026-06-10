# API Test Plan For LLM-Generated Runnable Scala

## Use these docs in order
1. `API_TEST_BACKGROUND.md`
2. `geoTiff.md`
3. `mapPixels.md`
4. `overlay.md`
5. `saveAsGeoTiff.md`
6. `LLM_API_TEST_PROMPT_TEMPLATE.md`
7. `LLM_API_TEST_SCALA_SCAFFOLD.scala`

## Why this order
- `geoTiff`: verify read + runtime type introspection.
- `mapPixels`: verify explicit conversion/type normalization.
- `overlay`: verify stacking/alignment/type consistency.
- `saveAsGeoTiff`: verify final writer behavior and error logs.

## Per-test checklist
- Has `object ... { def run(sc: SparkContext): Unit }`
- Has imports required by RDPro
- Uses concrete input/output paths
- Includes at least one action (`count`, `first`, or `saveAsGeoTiff`)
- Prints `pixelType` before critical ops
- On failure, captures root cause + key frames + fix snippet

## LLM generation mode
- Provide scaffold file as immutable wrapper.
- Allow model to fill TODO block only.
- Reject output if wrapper is modified.

## Job generator
Use the helper script to generate per-API LLM prompts and scaffolds:

```bash
python3 run/build_api_test_jobs.py \
  --input-a "file:///ABS/PATH/A.tif" \
  --input-b "file:///ABS/PATH/B.tif" \
  --output "file:///ABS/PATH/out.tif"
```

Generated folder:
- `run/api_test_jobs/geoTiff/prompt.txt`
- `run/api_test_jobs/mapPixels/prompt.txt`
- `run/api_test_jobs/overlay/prompt.txt`
- `run/api_test_jobs/saveAsGeoTiff/prompt.txt`

Recommended execution:
1. Send each `prompt.txt` to LLM.
2. Save returned Scala into `run/api_test_jobs/<api>/generated.scala`.
3. Run with your existing spark-shell harness.
