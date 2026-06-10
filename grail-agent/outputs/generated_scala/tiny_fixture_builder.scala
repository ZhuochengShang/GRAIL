import org.apache.spark.SparkContext
import org.apache.spark.sql.SparkSession
import org.apache.spark.rdd.RDD

import edu.ucr.cs.bdlab.beast._
import edu.ucr.cs.bdlab.beast.cg.SpatialDataTypes.RasterRDD
import edu.ucr.cs.bdlab.beast.common.BeastOptions
import edu.ucr.cs.bdlab.beast.geolite.{Feature, IFeature}
import edu.ucr.cs.bdlab.raptor.RaptorMixin._
import edu.ucr.cs.bdlab.raptor.RasterOperationsLocal

import org.locationtech.jts.geom.{Envelope, GeometryFactory}

object TinyFixtureBuilder {
  def run(sc: SparkContext): Unit = {
    val realRasterPath = "file:///ABS/PATH/TO/REAL_RASTER.tif"
    val tinyRasterOut = "file:///ABS/PATH/TO/TINY_RASTER_OUT.tif"

    val raster: RasterRDD[Int] = sc.geoTiff[Int](realRasterPath)

    val factory = new GeometryFactory()
    val testPoly = factory.toGeometry(new Envelope(-82.76, -80.25, 31.91, 35.17))
    val features: RDD[IFeature] =
      sc.parallelize(Seq(Feature.create(null, testPoly).asInstanceOf[IFeature]))

    val tinyRaster: RasterRDD[Int] =
      raster.mask(features, RasterOperationsLocal.NoDataValue)

    tinyRaster.saveAsGeoTiff(tinyRasterOut)
    println(s"Wrote tiny raster fixture to $tinyRasterOut")
  }
}

object TinyFixtureBuilderMain {
  def main(args: Array[String]): Unit = {
    val spark = SparkSession.builder()
      .appName("TinyFixtureBuilder")
      .master("local[*]")
      .getOrCreate()
    try {
      TinyFixtureBuilder.run(spark.sparkContext)
    } finally {
      spark.stop()
    }
  }
}
