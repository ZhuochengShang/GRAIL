import org.apache.spark.SparkContext
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.types.IntegerType
import org.apache.spark.rdd.RDD

import edu.ucr.cs.bdlab.beast._
import edu.ucr.cs.bdlab.beast.cg.SpatialDataTypes.RasterRDD
import edu.ucr.cs.bdlab.beast.geolite.{Feature, IFeature}
import edu.ucr.cs.bdlab.raptor.RaptorMixin._
import edu.ucr.cs.bdlab.raptor.RasterOperationsLocal

import org.locationtech.jts.geom.{Envelope, GeometryFactory}

object TinyTestRunner {
  def run(sc: SparkContext): Unit = {
    val tinyRasterPath = "file:///ABS/PATH/TO/TINY_RASTER_OUT.tif"

    val raster: RasterRDD[Int] = sc.geoTiff[Int](tinyRasterPath)
    val factory = new GeometryFactory()
    val testPoly = factory.toGeometry(new Envelope(-82.76, -80.25, 31.91, 35.17))
    val vector: RDD[IFeature] =
      sc.parallelize(Seq(Feature.create(null, testPoly).asInstanceOf[IFeature]))

    val rasterSample = raster.take(1).headOption.getOrElse(
      throw new IllegalArgumentException("Tiny raster is empty"))
    if (rasterSample.pixelType != IntegerType) {
      throw new IllegalArgumentException(s"Unexpected pixel type: ${rasterSample.pixelType}")
    }

    // Keep this section aligned with the generated TRANSFORM logic.
    val maskedRaster: RasterRDD[Int] =
      raster.mask(vector, RasterOperationsLocal.NoDataValue)

    println("__STEP__ TRANSFORM_done")
  }
}

object TinyTestRunnerMain {
  def main(args: Array[String]): Unit = {
    val spark = SparkSession.builder()
      .appName("TinyTestRunner")
      .master("local[*]")
      .getOrCreate()
    try {
      TinyTestRunner.run(spark.sparkContext)
    } finally {
      spark.stop()
    }
  }
}
