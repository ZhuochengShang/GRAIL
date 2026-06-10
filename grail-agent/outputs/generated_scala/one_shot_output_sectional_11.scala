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
    val firstRaster = raster.take(1).headOption.getOrElse(
      throw new IllegalArgumentException("Raster is empty"))

    val vector: RDD[IFeature] = sc.shapefile(primaryVectorPathOpt.getOrElse(
      throw new IllegalArgumentException("vectorPaths is empty")))
    if (vector.take(1).isEmpty) {
      throw new IllegalArgumentException("No valid geometries found in shapefile")
    }

    println("__STEP__ LOAD_DATA_done")
// TODO SECTION_LOAD_DATA_END

    // TODO SECTION_TYPE_CHECK_START
// check pixel/schema/data types
    val pixelType = firstRaster.pixelType
    pixelType match {
      case IntegerType => println("Pixel type is IntegerType as expected.")
      case FloatType => println("Pixel type is FloatType, unexpected for this raster.")
      case other => throw new RuntimeException(s"Unsupported pixel type: $other")
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

    // Perform raster-vector join to associate raster values with vector geometries
    val joined: RDD[RaptorJoinFeature[Float]] = rasterFloat.raptorJoin(vector)

    // Validate the transformation by inspecting the first joined record
    val sample = joined.take(1).headOption.getOrElse(
      throw new IllegalArgumentException("No joined records found"))
    println(s"Sample joined value: ${sample.m}")
    println(s"Sample geometry type: ${sample.feature.getGeometry.getGeometryType}")

    println("__STEP__ TRANSFORM_done")
// TODO SECTION_TRANSFORM_END

    // TODO SECTION_ANALYTICS_START
// Aggregate the joined records to compute zonal statistics
    val zonalStats = joined
      .map { feature =>
        val zoneId = feature.feature.getAs[String]("name")
        val classValue = feature.m.toInt
        ((zoneId, classValue), 1)
      }
      .reduceByKey(_ + _)
      .map { case ((zoneId, classValue), count) =>
        (zoneId, (classValue, count))
      }
      .groupByKey()
      .mapValues { classCounts =>
        val total = classCounts.map(_._2).sum
        classCounts.map { case (classValue, count) =>
          (classValue, count, (count.toDouble / total) * 100.0)
        }.toList
      }

    // Validate by taking a sample of the results
    val sampleStats = zonalStats.take(1)
    sampleStats.foreach { case (zoneId, stats) =>
      println(s"Zone ID: $zoneId")
      stats.foreach { case (classValue, count, percent) =>
        println(s"Class: $classValue, Count: $count, Percent: $percent")
      }
    }

    println("__STEP__ ANALYTICS_done")
// TODO SECTION_ANALYTICS_END

    // TODO SECTION_OUTPUT_START
import java.io.{BufferedWriter, FileWriter}
    import scala.collection.JavaConverters._

    // Define the output CSV paths
    val outputCsvPath = "file:///Users/clockorangezoe/Documents/phd_projects/code/geoAI/LangGraph/Notebook/rdpro_section_codegen/generated_output/boston_land_use_by_neighborhood_sample.csv"
    val summaryCsvPath = "file:///Users/clockorangezoe/Documents/phd_projects/code/geoAI/LangGraph/Notebook/rdpro_section_codegen/generated_output/boston_land_use_summary_sample.csv"

    // Function to write rows to a CSV file
    def writeCsv(rows: Iterable[Map[String, Any]], outputPath: String): Unit = {
      if (rows.isEmpty) throw new IllegalArgumentException("No output rows were generated")
      
      val file = new java.io.File(new URI(outputPath))
      val writer = new BufferedWriter(new FileWriter(file))
      
      try {
        val header = rows.head.keys.mkString(",")
        writer.write(header)
        writer.newLine()
        
        for (row <- rows) {
          val line = row.values.mkString(",")
          writer.write(line)
          writer.newLine()
        }
      } finally {
        writer.close()
      }
    }

    // Convert the zonal statistics to a format suitable for CSV output
    val outputRows = zonalStats.flatMap { case (zoneId, stats) =>
      stats.map { case (classValue, count, percent) =>
        Map(
          "zone_id" -> zoneId,
          "class_value" -> classValue,
          "pixel_count" -> count,
          "percent" -> percent
        )
      }
    }.collect()

    // Write the detailed output rows to CSV
    writeCsv(outputRows, outputCsvPath)

    // Generate summary rows
    val summaryRows = zonalStats.map { case (zoneId, stats) =>
      val dominantClass = stats.maxBy(_._3)._1
      val dominantPercent = stats.maxBy(_._3)._3
      Map(
        "zone_id" -> zoneId,
        "dominant_class" -> dominantClass,
        "dominant_percent" -> dominantPercent
      )
    }.collect()

    // Write the summary rows to CSV
    writeCsv(summaryRows, summaryCsvPath)

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
