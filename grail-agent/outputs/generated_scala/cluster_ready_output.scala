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
    val rasterPaths: Seq[String] = Seq("file:///path/to/cluster/input_raster.tif")
    val vectorPaths: Seq[String] = Seq("file:///path/to/cluster/input_vector.shp")
    val primaryRasterPath: String = rasterPaths.headOption.getOrElse(throw new IllegalArgumentException("rasterPaths is empty"))
    val primaryVectorPathOpt: Option[String] = vectorPaths.headOption
    val outputDir: String = "file:///path/to/cluster/output"
    val outputPath: String = "file:///path/to/cluster/output/result.csv"
// TODO SECTION_INPUTS_END

    // TODO SECTION_LOAD_DATA_START
// Shared read options for raster loaders (reuse this variable; do not redeclare inside match/case)
    val raster: RasterRDD[Int] = sc.geoTiff(primaryRasterPath, 0, loadOpts)
      throw new IllegalArgumentException("Raster is empty"))

    val primaryVectorPath = primaryVectorPathOpt.getOrElse(throw new IllegalArgumentException("vectorPaths is empty"))
    val vector: RDD[IFeature] = sc.shapefile(primaryVectorPath)
      throw new IllegalArgumentException("No valid geometries found in shapefile")
    }
// TODO SECTION_LOAD_DATA_END

    // TODO SECTION_TYPE_CHECK_START
// check pixel/schema/data types
    val pixelType = firstRaster.pixelType
    pixelType match {
    }
// TODO SECTION_TYPE_CHECK_END

    // TODO SECTION_SPATIAL_CHECK_START
// check CRS + metadata compatibility
// TODO SECTION_SPATIAL_CHECK_END

    // TODO SECTION_TRANSFORM_START
val joined: RDD[RaptorJoinFeature[Int]] = raster.raptorJoin(vector)
      throw new IllegalArgumentException("No joined records found"))
// TODO SECTION_TRANSFORM_END

    // TODO SECTION_ANALYTICS_START
// Perform zonal statistics by aggregating the joined records
    val zoneStats = joined.map { feature =>
      val zoneName = feature.feature.getAs[String]("name")
      val classValue = feature.m
      ((zoneName, classValue), 1)
    }.reduceByKey(_ + _)
      .map { case ((zoneName, classValue), count) =>
        (zoneName, classValue, count)
      }

    // Take a sample to validate the analytics step
// TODO SECTION_ANALYTICS_END

    // TODO SECTION_OUTPUT_START
// Save the zone statistics as a CSV file
    val outputCSVPath = outputDir + "/zone_statistics.csv"
    val header = "zone_name,class_value,count"
    val zoneStatsStrings = zoneStats.map { case (zoneName, classValue, count) =>
      s"$zoneName,$classValue,$count"
    }
    val zoneStatsWithHeader = sc.parallelize(Seq(header)) ++ zoneStatsStrings

    zoneStatsWithHeader.saveAsTextFile(outputCSVPath)
// TODO SECTION_OUTPUT_END
  }
}

object GeoJobMain {
  def main(args: Array[String]): Unit = {
    val spark = SparkSession.builder()
      .appName("GeoJobMain")
      .master("spark://ec-hn.cs.ucr.edu:7077")
      .getOrCreate()
    try {
      GeoJob.run(spark.sparkContext)
      println("__DONE__ object=GeoJob")
    } finally {
      spark.stop()
    }
  }
}
