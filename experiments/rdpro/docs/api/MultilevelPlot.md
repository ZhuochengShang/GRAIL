# MultilevelPlot

_The `plotFeatures` function generates a visual representation of spatial features by plotting them onto a single image, allowing for customizable dimensions…_

**Receiver:** static object — call `MultilevelPlot.<method>(...)`

**Members** (most robust first): ⚠️ `plotFeatures` **(primary)**

---

## API Test: `plotFeatures`
_Grounding: GUESSED — no test; generated from the signature only. Verify by execution._

### Signature
```scala
def plotFeatures(features: SpatialDataTypes.SpatialRDD, imageWidth: Int, imageHeight: Int, imagePath: String, plotterClass: Class[_ <: Plotter] = classOf[GeometricPlotter], canvasMBR: EnvelopeNDLite = null, opts: BeastOptions = new BeastOptions()): Unit
def plotFeatures(features: JavaSpatialRDD, minLevel: Int, maxLevel: Int, plotterClass: Class[_ <: Plotter], inputPath: String, outputPath: String, opts: BeastOptions): Unit
def plotFeatures(features: SpatialRDD, levels: Range, plotterClass: Class[_ <: Plotter], inputPath: String, outputPath: String, opts: BeastOptions): Unit
```
_Source: beast/visualization/src/main/scala/edu/ucr/cs/bdlab/davinci/SingleLevelPlot.scala:58  (+2 more definition site/overload)_

_Source doc:_ Plots a set of features to a single image. By default, the aspect ratio of the input is maintained and the given dimensions are treated as upper bounds for image width and height, i.e., the produced image might have smaller dimensions. Also, by default, the extents of the canvas will be equal to the input data. This means that the plotted image will occupy the largest portion of the image. If you wish to visualize only a subset of the data or visualize the data on a small portion of the image, you can specify the [[canvasMBR]] parameter. @param features the set of features to plot @param imageWidth the width of the image in pixels @param imageHeight the height of the image in pixels. @param imagePath the path to which the image will be written @param plotterClass the class of the plotter to use for producing the image @param canvasMBR (Optional) the extents of the data (minimum bounding rectangle) @param opts (Optional) additional options to use with the plotter, e.g., colors

### Goal
The `plotFeatures` function generates a visual representation of spatial features by plotting them onto a single image, allowing for customizable dimensions and styling options.

### Parameters
- `features` (`SpatialDataTypes.SpatialRDD`): A distributed collection of spatial features that will be plotted onto the image. This should contain geometries such as points, lines, or polygons.
- `imageWidth` (`Int`): The maximum width of the output image in pixels. The actual width may be smaller to maintain the aspect ratio of the input features.
- `imageHeight` (`Int`): The maximum height of the output image in pixels. The actual height may be smaller to maintain the aspect ratio of the input features.
- `imagePath` (`String`): The file path where the generated image will be saved. This should be a valid path where the application has write permissions.
- `plotterClass` (`Class[_ <: Plotter]`), default `classOf[GeometricPlotter]`: The class of the plotter to use for rendering the image. By default, it uses `GeometricPlotter`, but other plotter implementations can be specified for different visual styles.

### Input
The caller must provide a valid `SpatialRDD` containing spatial features, along with specified dimensions for the image (width and height) and a valid file path for saving the output image. The `plotterClass` can be customized, and additional options can be provided through `BeastOptions`.

### Output
Returns `Unit` — this indicates that the function performs an action (plotting the features) without returning a value. The output image is saved to the specified `imagePath` in a format determined by the plotter.

### Valid Call Patterns
```scala
val counties = SpatialReader.readInput(sparkContext, new BeastOptions(), "tl_2018_us_county.zip", "shapefile")
MultilevelPlot.plotFeatures(counties, 800, 600, "counties_plot.png", classOf[GeometricPlotter], null, new BeastOptions().set("stroke", "blue").set("fill", "#9999E6"))
```

### LLM Instruction Prompt
- When calling `plotFeatures`, ensure that the `features` parameter is a valid `SpatialRDD` containing spatial geometries, and specify appropriate dimensions for `imageWidth` and `imageHeight`. Provide a valid `imagePath` for output, and optionally customize the `plotterClass` and `opts`.

### Prompt Snippet
```text
To visualize spatial features, use the plotFeatures function with a SpatialRDD of features, specify the desired image dimensions, and provide a path for the output image.
```

### Common Failure Modes
- **[compile]** error: not found: value plotFeatures _(seen 2x)_
- **[compile]** error: type mismatch; _(seen 2x)_

### Fix Code Hint
```scala
Ensure that the imagePath is valid and writable, and check that the features are correctly loaded into a SpatialRDD before calling plotFeatures.
```
