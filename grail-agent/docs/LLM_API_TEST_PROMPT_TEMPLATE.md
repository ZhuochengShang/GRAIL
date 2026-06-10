You must return runnable Scala spark-shell code only (no markdown).

Rules:
1. Keep scaffold code unchanged except lines marked `TODO`.
2. Must compile in spark-shell.
3. Must include at least one Spark action (`count`, `first`, or `saveAsGeoTiff`).
4. Use provided paths exactly. Do not invent paths.
5. Keep one object with `def run(sc: SparkContext): Unit`.

Inputs:
- API under test: `{{API_NAME}}`
- Goal: `{{GOAL}}`
- Input A: `{{INPUT_A}}`
- Input B: `{{INPUT_B}}` (optional)
- Output: `{{OUTPUT_PATH}}` (optional)
- Read type A: `{{READ_TYPE_A}}` (e.g., `Int`, `Float`, `Array[Int]`)
- Read type B: `{{READ_TYPE_B}}` (optional)
- Write type: `{{WRITE_TYPE}}` (optional)

Instructions:
- Fill only the `TODO` block in the Scala scaffold.
- If overlay is used, enforce consistent rasterMetadata and numeric types before overlay.
- If metadata mismatch risk exists, align first using `reshapeNN` before overlay.
- If type mismatch risk exists, convert explicitly with `mapPixels`.
- Add one or two `println` checks for pixel types using `first().pixelType`.

Return only Scala code.
