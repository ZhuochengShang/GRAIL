// COMPILED smoke test (the proven path: object + spark-submit, NOT spark-shell -i).
// spark-shell -i can't apply RaptorMixin's implicit class (sc.geoTiff); compiling
// an object works. Build + run with docs/run_smoke.sh.
// SUCCESS = "__APITEST_RESULT tiles=..." then "__DONE__".

import org.apache.spark.SparkContext
import org.apache.spark.sql.SparkSession
import edu.ucr.cs.bdlab.beast._
import edu.ucr.cs.bdlab.raptor.RaptorMixin._
import edu.ucr.cs.bdlab.raptor.RaptorMixin.RasterReadMixinFunctions
import edu.ucr.cs.bdlab.beast.cg.SpatialDataTypes.RasterRDD

object GeoJob {
  def run(sc: SparkContext): Unit = {
    // local file:// URI so Spark reads the local filesystem
    val raster_tif = "file:///Users/clockorangezoe/Documents/phd_projects/code/geoAI/GRAIL/grail-agent/examples/fixtures/nldas_boston_30m.tif"
    val raster: RasterRDD[Float] = sc.geoTiff[Float](raster_tif)
    println("__APITEST_RESULT tiles=" + raster.count())
  }
}

object GeoJobMain {
  def main(args: Array[String]): Unit = {
    val spark = SparkSession.builder().appName("ApiTest").master("local[*]").getOrCreate()
    try {
      GeoJob.run(spark.sparkContext)
      println("__DONE__ object=GeoJob")
    } catch {
      case t: Throwable =>
        Console.err.println("__RUN_ERR__ " + t.getClass.getName + ": " + t.getMessage)
        t.printStackTrace()
    } finally {
      spark.stop()
    }
  }
}
