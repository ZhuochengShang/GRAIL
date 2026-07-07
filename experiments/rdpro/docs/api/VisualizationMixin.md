# VisualizationMixin

_`plotPyramid` generates a multilevel tiled image representation of a dataset and saves it to a specified output path._

**Receiver:** instance — obtain a `VisualizationMixin` value, then `<value>.<method>(...)`

**Members** (most robust first): ⚠️ `plotPyramid` **(primary)**

---

## API Test: `plotPyramid`
_Grounding: GUESSED — no test; generated from the signature only. Verify by execution._

### Signature
```scala
def plotPyramid(outPath: String, numLevels: Int, plotterClass: Class[_ <: Plotter] = classOf[GeometricPlotter], opts: BeastOptions = new BeastOptions()): Unit
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/VisualizationMixin.scala:53_

_Source doc:_ Plots the dataset as multilevel tiled image and write the output to the given path. @param outPath the output path to write the image tiles to. @param numLevels the number of levels to create @param plotterClass the plotter class to use for plotting @param opts additional options for the plotter

### Goal
`plotPyramid` generates a multilevel tiled image representation of a dataset and saves it to a specified output path.

### Parameters
- `outPath` (`String`): The file path where the output image tiles will be saved. This should be a valid path where the application has write permissions.
- `numLevels` (`Int`): The number of pyramid levels to create for the tiled image. This determines the resolution levels of the output tiles.
- `plotterClass` (`Class[_ <: Plotter]`), default `classOf[GeometricPlotter], opts: BeastOptions = new BeastOptions()`: The class of the plotter to use for generating the visual representation. The default is `GeometricPlotter`, which is suitable for general geometric visualizations.

### Input
The caller must provide a dataset that has been indexed and is ready for visualization. The dataset should be compatible with the plotting operation, and the output path must be accessible for writing. The input dataset is typically a spatial file that has been processed and is suitable for generating a multilevel visualization.

### Output
Returns `Unit` — this indicates that the function completes its operation without returning a value. The output is a set of image tiles saved in the specified format at the given `outPath`.

### Valid Call Patterns
```scala
sparkContext.shapefile("tl_2018_us_county.zip")
  .plotPyramid("counties_multilevel.zip", 20,
    opts = Seq("mercator" -> true, "stroke" -> "blue", "threshold" -> "1m"))
```

### LLM Instruction Prompt
- Ensure that the dataset is properly indexed and accessible before calling `plotPyramid`. The output path must be valid and writable.

### Prompt Snippet
```text
To visualize the dataset as a multilevel tiled image, use the plotPyramid function with the appropriate parameters.
```

### Common Failure Modes
- **[runtime]** java.lang.IllegalArgumentException: requirement failed: Output directory is empty or does not exist _(seen 4x)_

### Fix Code Hint
```scala
// Ensure the output path is valid and writable
val outputPath = "valid/output/path/counties_multilevel.zip"

// Ensure the dataset is indexed and ready for plotting
sparkContext.shapefile("tl_2018_us_county.zip")
  .plotPyramid(outputPath, 20, opts = new BeastOptions())
```
