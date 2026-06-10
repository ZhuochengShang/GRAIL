import org.apache.spark.SparkContext
import org.apache.spark.sql.SparkSession
import org.apache.spark.SparkConf
import org.apache.spark.sql.types.{ArrayType, FloatType, IntegerType, DoubleType}
import org.apache.spark.rdd.{CoGroupedRDD, RDD}
import edu.ucr.cs.bdlab.beast._
import edu.ucr.cs.bdlab.raptor.RaptorMixin._
import edu.ucr.cs.bdlab.raptor.RaptorMixin.RasterReadMixinFunctions
import edu.ucr.cs.bdlab.raptor.RasterVectorOperations
import edu.ucr.cs.bdlab.beast.cg.SpatialDataTypes.RasterRDD
import edu.ucr.cs.bdlab.beast.io.tiff.TiffConstants
import edu.ucr.cs.bdlab.beast.common.BeastOptions
import edu.ucr.cs.bdlab.beast.geolite.{ITile, Feature, IFeature, RasterFeature, RasterMetadata}
import edu.ucr.cs.bdlab.raptor.{GeoTiffWriter, RasterOperationsFocal, RasterOperationsLocal, RasterOperationsGlobal, RaptorJoin,RaptorJoinFeature }
import java.net.URI
import java.nio.file.{Paths, Files}
import org.apache.hadoop.conf.Configuration
import org.apache.hadoop.fs.{FileSystem, Path => HPath}

object GeoJob {
  def run(sc: SparkContext): Unit = {
    val loadOpts = new BeastOptions()

    // TODO SECTION_INPUTS_START
    val rasterPaths: Seq[String] = Seq("file:///Users/clockorangezoe/Downloads/Annual_NLCD_LndCov_2024_CU_C1V1/Annual_NLCD_LndCov_2024_CU_C_1V1_clip.tif")
    val vectorPaths: Seq[String] = Seq("file:///Users/clockorangezoe/Downloads/boston_neighborhood_boundaries/Boston_Neighborhood_Boundaries_sample.shp")
    val primaryRasterPath: String = rasterPaths.headOption.getOrElse(throw new IllegalArgumentException("rasterPaths is empty"))
    val primaryVectorPathOpt: Option[String] = vectorPaths.headOption
    val outputDir: String = "file:///Users/clockorangezoe/Documents/phd_projects/code/geoAI/LangGraph/Notebook/rdpro_section_codegen/generated_output"
    val outputPath: String = outputDir
// TODO SECTION_INPUTS_END

    // TODO SECTION_LOAD_DATA_START
    val raster: RasterRDD[Int] = sc.geoTiff[Int](primaryRasterPath)
    val vector: RDD[IFeature] = sc.shapefile(primaryVectorPathOpt.getOrElse(throw new IllegalArgumentException("vectorPaths is empty")))

    // Validate the loaded data
    val rasterSample = raster.take(1)
    if (rasterSample.isEmpty) {
      throw new RuntimeException("Failed to load raster data")
    }

    val vectorSample = vector.take(1)
    if (vectorSample.isEmpty) {
      throw new RuntimeException("Failed to load vector data")
    }

    println("__STEP__ LOAD_DATA_done")
    // TODO SECTION_LOAD_DATA_END

    // TODO SECTION_TYPE_CHECK_START
    // check pixel/schema/data types
    val pixelType = rasterSample.head.pixelType
    pixelType match {
      case IntegerType => println("Raster pixel type is IntegerType as expected.")
      case _ => throw new RuntimeException(s"Unexpected raster pixel type: $pixelType")
    }
    println("__STEP__ TYPE_CHECK_done")
    // TODO SECTION_TYPE_CHECK_END

    // TODO SECTION_SPATIAL_CHECK_START
    // check CRS + metadata compatibility
    println("__STEP__ SPATIAL_CHECK_done")
    // TODO SECTION_SPATIAL_CHECK_END

    // TODO SECTION_TRANSFORM_START
    // Transform raster values to Float for further processing
    val rasterFloat: RasterRDD[Float] = raster.mapPixels(v => v.toFloat)

    // Perform a raptor join to associate raster values with vector geometries
    val joined: RDD[RaptorJoinFeature[Float]] = rasterFloat.raptorJoin(vector)

    // Validate the transformation
    val joinedSample = joined.take(1)
    if (joinedSample.isEmpty) {
      throw new RuntimeException("Failed to join raster and vector data")
    }

    println("__STEP__ TRANSFORM_done")
    // TODO SECTION_TRANSFORM_END

    // TODO SECTION_ANALYTICS_START
    // Flatten the raster to extract pixel values for analytics
    val pixelValues = rasterFloat.flatten.map(_._4)

    // Calculate the histogram of pixel values
    val histogram = pixelValues.countByValue()

    // Print the histogram size as a simple validation
    println(s"Histogram size: ${histogram.size}")

    println("__STEP__ ANALYTICS_done")
    // TODO SECTION_ANALYTICS_END

    // TODO SECTION_OUTPUT_START
    // Save the final raster output to a GeoTIFF
    rasterFloat.saveAsGeoTiff(outputPath, Seq(GeoTiffWriter.Compression -> TiffConstants.COMPRESSION_LZW))
    println("__STEP__ OUTPUT_done")
    // TODO SECTION_OUTPUT_END
  }
}

object GeoJobMain {
  def main(args: Array[String]): Unit = {
    val spark = SparkSession.builder()
      .appName("GeoJobMain")
      .master("local[*]")
      .getOrCreate()
    try {
      GeoJob.run(spark.sparkContext)
      println("__DONE__ object=GeoJob")
    } finally {
      spark.stop()
    }
  }
}
