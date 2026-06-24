# RDPro Documentation Notes

## 1. Project purpose
RDPro is a Spark-based distributed raster processing library designed for large-scale geospatial analysis. It facilitates operations such as loading GeoTIFFs, performing per-pixel transformations, executing raster-vector joins, aligning datasets, and calculating zonal statistics.

## 2. Main workflows
- **Loading Raster Data**: Load raster data from GeoTIFF or HDF files.
- **Transforming Raster Data**: Apply pixel-level operations like `mapPixels`, `filterPixels`, and `flatten`.
- **Joining Raster and Vector Data**: Use `raptorJoin` to combine raster data with vector geometries.
- **Calculating Zonal Statistics**: Compute statistics over specified zones using `zonalStats`.
- **Reshaping and Reprojecting**: Change the shape or coordinate reference system of raster data.
- **Saving Outputs**: Write processed raster data to GeoTIFF or CSV formats.

## 3. Important APIs and usage patterns
- **Loading Raster Data**:
  ```scala
  val raster: RDD[ITile[Int]] = sc.geoTiff("path/to/file.tif")
  val temperature: RasterRDD[Float] = sc.hdfFile("path/to/file.hdf", "dataset_name")
  ```

- **Transforming Raster Data**:
  ```scala
  val transformedRaster = raster.mapPixels(pixel => pixel * 2)
  val filteredRaster = raster.filterPixels(pixel => pixel > 300)
  ```

- **Joining Raster and Vector Data**:
  ```scala
  val vector: RDD[IFeature] = sc.shapefile("path/to/vector.shp")
  val joined: RDD[(IFeature, Int, Int, Float)] = raster.raptorJoin[Float](vector)
  ```

- **Calculating Zonal Statistics**:
  ```scala
  val stats = raster.zonalStats(vector)
  ```

- **Reshaping and Reprojecting**:
  ```scala
  val reshapedRaster = raster.reshape(newMetadata)
  val reprojectedRaster = raster.reproject(newCRS)
  ```

- **Saving Outputs**:
  ```scala
  raster.saveAsGeoTiff("output.tif")
  raster.saveAsCSV("output.csv", xColumn = 0, yColumn = 1)
  ```

## 4. Inputs and file formats
- **Supported Input Formats**: GeoTIFF, HDF, CSV, Shapefile, GeoJSON.
- **Input Types**: RDD[ITile], RasterRDD, RDD[IFeature].
- **Example Input**:
  - GeoTIFF: `sc.geoTiff("path/to/file.tif")`
  - HDF: `sc.hdfFile("path/to/file.hdf", "dataset_name")`
  - Shapefile: `sc.shapefile("path/to/file.shp")`

## 5. Outputs and generated artifacts
- **Output Formats**: GeoTIFF, CSV.
- **Generated Artifacts**: Processed raster files, summary statistics, visualizations.
- **Example Output**:
  ```scala
  raster.saveAsGeoTiff("output.tif")
  ```

## 6. Configuration and environment assumptions
- Requires Spark and Scala environment.
- Java Development Kit (JDK) 1.8 or later is recommended.
- Apache Maven or SBT for project setup.
- Ensure that input files are accessible in the working directory.

## 7. Commands and examples
- **Load a GeoTIFF**:
  ```scala
  val raster: RDD[ITile[Int]] = sc.geoTiff("path/to/file.tif")
  ```

- **Perform NDVI Calculation**:
  ```scala
  val ndvi = raster.mapPixels(pixel => (pixel.red - pixel.nir) / (pixel.red + pixel.nir))
  ```

- **Zonal Statistics**:
  ```scala
  val stats = raster.zonalStats(vector)
  ```

- **Save Output**:
  ```scala
  raster.saveAsGeoTiff("output.tif")
  ```

## 8. Constraints and warnings
- Always match the pixel type when loading raster data (e.g., `sc.geoTiff[T]`).
- Outputs must be in specified formats (GeoTIFF or CSV).
- Do not invent file paths; use only provided input variables.
- Ensure that the input data is correctly formatted and accessible.

## 9. Facts to preserve in the final README
- RDPro is part of the UCR Beast project for distributed raster processing.
- It supports various raster operations including loading, transforming, joining, and saving.
- The library is designed for geospatial scientists and data engineers working with large datasets.

## 10. Missing or weak documentation
- Some API methods lack detailed examples or explanations of parameters.
- Specific error handling and troubleshooting steps for common issues are not well-documented.
- More examples of complex workflows involving multiple operations would be beneficial.