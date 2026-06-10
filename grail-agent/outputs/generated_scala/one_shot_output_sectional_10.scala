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
    val outputPath: String = "file:///Users/clockorangezoe/Documents/phd_projects/code/geoAI/LangGraph/Notebook/rdpro_section_codegen/generated_output/output.tif"
// TODO SECTION_INPUTS_END

    // TODO SECTION_LOAD_DATA_START
val raster: RasterRDD[Int] = sc.geoTiff(primaryRasterPath, 0, loadOpts)
    val vector: RDD[IFeature] = sc.shapefile(primaryVectorPathOpt.getOrElse(throw new IllegalArgumentException("vectorPaths is empty")))

    // Validate raster and vector loads
    val firstRasterTile = raster.take(1).headOption.getOrElse(throw new IllegalArgumentException("Raster is empty"))
    val firstVectorFeature = vector.take(1).headOption.getOrElse(throw new IllegalArgumentException("No valid geometries found in shapefile"))

    println("__STEP__ LOAD_DATA_done")
// TODO SECTION_LOAD_DATA_END

    // TODO SECTION_TYPE_CHECK_START
// check pixel/schema/data types
    val pixelType = firstRasterTile.pixelType
    pixelType match {
      case IntegerType => println("Raster pixel type is IntegerType as expected.")
      case FloatType => println("Raster pixel type is FloatType, unexpected for this dataset.")
      case other => throw new RuntimeException(s"Unsupported pixel type: $other")
    }
    println("__STEP__ TYPE_CHECK_done")
// TODO SECTION_TYPE_CHECK_END

    // TODO SECTION_SPATIAL_CHECK_START
    // check CRS + metadata compatibility
    println("__STEP__ SPATIAL_CHECK_done")
    // TODO SECTION_SPATIAL_CHECK_END

    // TODO SECTION_TRANSFORM_START
// Apply a transformation to the raster data using mapPixels
    val transformedRaster: RasterRDD[Float] = raster.mapPixels(v => v.toFloat)

    // Perform a raster-vector join using raptorJoin
    val joined: RDD[RaptorJoinFeature[Float]] = transformedRaster.raptorJoin(vector)

    // Validate the transformation and join by inspecting the first element
    val sample = joined.take(1).headOption.getOrElse(throw new IllegalArgumentException("Join operation resulted in an empty RDD"))
    println(s"Sample value: ${sample.m}")
    println(s"Sample geometry type: ${sample.feature.getGeometry.getGeometryType}")

    println("__STEP__ TRANSFORM_done")
// TODO SECTION_TRANSFORM_END

    // TODO SECTION_ANALYTICS_START
// Perform analytics on the joined data
    val zoneStats = joined.map { feature =>
      val zoneId = feature.feature.getAs[String]("name")
      val classValue = feature.m.toInt
      (zoneId, classValue)
    }.groupByKey()
      .mapValues { values =>
        val counts = values.groupBy(identity).mapValues(_.size)
        val total = counts.values.sum
        counts.map { case (classValue, count) =>
          (classValue, (count, (count.toDouble / total) * 100.0))
        }
      }

    // Validate analytics by inspecting the first result
    val firstZoneStats = zoneStats.take(1).headOption.getOrElse(throw new IllegalArgumentException("Analytics resulted in an empty RDD"))
    println(s"Zone ID: ${firstZoneStats._1}, Stats: ${firstZoneStats._2}")

    println("__STEP__ ANALYTICS_done")
// TODO SECTION_ANALYTICS_END

    // TODO SECTION_OUTPUT_START
    // save GeoTIFF
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
