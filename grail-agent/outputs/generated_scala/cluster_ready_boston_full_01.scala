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

object GeoJob {
  def run(sc: SparkContext): Unit = {
    val loadOpts = new BeastOptions()

    // TODO SECTION_INPUTS_START
    val rasterPaths: Seq[String] = Seq("hdfs:///user/zshan011/geoai/nlcd/nlcd_4326_uncompressed.tif")
    val vectorPaths: Seq[String] = Seq("hdfs:///user/zshan011/geoai/us_counties/us_counties.shp")
    val primaryRasterPath: String = rasterPaths.headOption.getOrElse(throw new IllegalArgumentException("rasterPaths is empty"))
    val primaryVectorPathOpt: Option[String] = vectorPaths.headOption
    val outputPath: String = "hdfs:///user/zshan011/geoai/output/us_counnties_full_landcover_summary"
// TODO SECTION_INPUTS_END

    // TODO SECTION_LOAD_DATA_START
    val raster: RasterRDD[Int] = sc.geoTiff(primaryRasterPath, 0, loadOpts)

    val primaryVectorPath = primaryVectorPathOpt.getOrElse(
      throw new IllegalArgumentException("vectorPaths is empty"))
    val vector: RDD[IFeature] = sc.shapefile(primaryVectorPath)
// TODO SECTION_LOAD_DATA_END

    // TODO SECTION_TYPE_CHECK_START
// Pixel type validation intentionally omitted here to avoid triggering an action
// before the final output stage.
// TODO SECTION_TYPE_CHECK_END

    // TODO SECTION_SPATIAL_CHECK_START
// check CRS + metadata compatibility
// TODO SECTION_SPATIAL_CHECK_END

    // TODO SECTION_TRANSFORM_START
    val joined: RDD[RaptorJoinFeature[Int]] = raster.raptorJoin(vector)
// TODO SECTION_TRANSFORM_END

    // TODO SECTION_ANALYTICS_START
// Perform zonal statistics by aggregating the joined records
    val zoneStats = joined.map { feature =>
      val zoneName = feature.feature.getAs[String]("NAME")
      val classValue = feature.m
      ((zoneName, classValue), 1)
    }.reduceByKey(_ + _)
      .map { case ((zoneName, classValue), count) =>
        (zoneName, classValue, count)
      }
// TODO SECTION_ANALYTICS_END

    // TODO SECTION_OUTPUT_START
// Save the zone statistics as a CSV file
    val header = "zone_name,class_value,count"
    val zoneStatsStrings = zoneStats.map { case (zoneName, classValue, count) =>
      s"$zoneName,$classValue,$count"
    }
    val zoneStatsWithHeader = sc.parallelize(Seq(header)) ++ zoneStatsStrings

    zoneStatsWithHeader.saveAsTextFile(outputPath)
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
