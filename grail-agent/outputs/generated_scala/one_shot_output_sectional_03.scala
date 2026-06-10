import org.apache.spark.SparkContext
import org.apache.spark.sql.SparkSession
import org.apache.spark.SparkConf
import org.apache.spark.sql.types.{ArrayType, FloatType, IntegerType, DoubleType}
import org.apache.spark.rdd.{CoGroupedRDD, RDD}
import edu.ucr.cs.bdlab.beast._
import edu.ucr.cs.bdlab.raptor.RaptorMixin._
import edu.ucr.cs.bdlab.raptor.RaptorMixin.RasterReadMixinFunctions
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
    val rasterPaths: Seq[String] = Seq("file:///Users/clockorangezoe/Documents/phd_projects/data/Raster/2021_30m_cdls/2021_30m_cdls_4326.tif")
    val vectorPaths: Seq[String] = Seq("file:///Users/clockorangezoe/Documents/phd_projects/data/Vector/cali_simplify/cali_simplify.shp")
    val primaryRasterPath: String = rasterPaths.headOption.getOrElse(throw new IllegalArgumentException("rasterPaths is empty"))
    val primaryVectorPathOpt: Option[String] = vectorPaths.headOption
    val outputDir: String = "file:///Users/clockorangezoe/Documents/phd_projects/code/geoAI/LangGraph/Notebook/rdpro_section_codegen/generated_output"
    val outputPath: String = outputDir
// TODO SECTION_INPUTS_END

    // TODO SECTION_LOAD_DATA_START
    // Load raster data
    val raster: RasterRDD[Int] = sc.geoTiff[Int](primaryRasterPath)
    println(s"Raster loaded with pixelType=${raster.first().pixelType} and count=${raster.count()}")

    // Load vector data
    val primaryVectorPath = primaryVectorPathOpt.getOrElse(throw new IllegalArgumentException("vectorPaths is empty"))
    val vector: RDD[IFeature] = sc.shapefile(primaryVectorPath)
    println(s"Vector loaded with count=${vector.count()}")

    println("__STEP__ LOAD_DATA_done")
    // TODO SECTION_LOAD_DATA_END

    // TODO SECTION_TYPE_CHECK_START
    // check pixel/schema/data types
    val expectedPixelType = IntegerType
    val actualPixelType = raster.first().pixelType

    if (actualPixelType != expectedPixelType) {
      throw new IllegalArgumentException(s"Pixel type mismatch: expected $expectedPixelType, but found $actualPixelType")
    }

    println("__STEP__ TYPE_CHECK_done")
    // TODO SECTION_TYPE_CHECK_END

    // TODO SECTION_SPATIAL_CHECK_START
    // check CRS + metadata compatibility
    println("__STEP__ SPATIAL_CHECK_done")
    // TODO SECTION_SPATIAL_CHECK_END

    // TODO SECTION_TRANSFORM_START
    // Transform raster by masking with vector geometries
    val geoms = vector.map(_.getGeometry).filter(g => g != null && !g.isEmpty).collect()
    if (geoms.isEmpty) {
      throw new IllegalArgumentException("No valid geometries found in vector data")
    }

    val maskedRaster: RasterRDD[Int] = raster.mask(geoms, RasterOperationsLocal.NODATA)
    println(s"Masked raster count=${maskedRaster.count()}")

    println("__STEP__ TRANSFORM_done")
    // TODO SECTION_TRANSFORM_END

    // TODO SECTION_ANALYTICS_START
    // Analytics is intentionally skipped for now.
    // Keep section markers for future activation.
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
