// AIDEAL API-test scaffold — AUTO-GENERATED from the API surface.
// Run via: spark-shell --jars <uberjar> -i <thisfile>
// spark-shell provides `sc` (SparkContext) and `spark` (SparkSession).
// The generated snippet is spliced between API_TEST_START / END and may use
// the in-scope bindings: sc, inputA, inputB, output.

import org.apache.spark.SparkContext
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.types.{ArrayType, FloatType, IntegerType, DoubleType}
import org.apache.spark.rdd.RDD
import edu.ucr.cs.bdlab.beast._
import edu.ucr.cs.bdlab.raptor.RaptorMixin._
import edu.ucr.cs.bdlab.raptor._
import edu.ucr.cs.bdlab.raptor.RasterOperationsLocal._
import edu.ucr.cs.bdlab.raptor.RasterOperationsFocal._
import edu.ucr.cs.bdlab.raptor.RasterOperationsGlobal._
import edu.ucr.cs.bdlab.raptor.ZonalStatistics._
import edu.ucr.cs.bdlab.raptor.RaptorJoin._
import edu.ucr.cs.bdlab.beast.cg.SpatialDataTypes.{RasterRDD, SpatialRDD}
import edu.ucr.cs.bdlab.beast.io._
import edu.ucr.cs.bdlab.beast.io.tiff.TiffConstants
import edu.ucr.cs.bdlab.beast.common.BeastOptions
import edu.ucr.cs.bdlab.beast.geolite.{ITile, Feature, IFeature, RasterFeature, RasterMetadata}
import edu.ucr.cs.bdlab.raptor.{GeoTiffWriter, RasterOperationsFocal, RasterOperationsLocal, RasterOperationsGlobal, RaptorJoin, RaptorJoinFeature}
import org.locationtech.jts.geom.{Geometry, Envelope}
import org.apache.hadoop.fs.Path
import scala.collection.JavaConverters._
import java.net.URI
import java.nio.file.{Paths, Files}

// Compiled form (scalac + spark-submit --class GeoJobMain). This is the proven
// path: an implicit class like RaptorMixin's sc.geoTiff resolves when compiled
// inside an object, but NOT in the spark-shell -i REPL.
object GeoJob {
  def run(sc: SparkContext): Unit = {
    // Typed sample inputs (from comprehension.execute.sample_data). Use the
    // one(s) whose type matches the API's parameters.
    // AIDEAL_DATA_BINDINGS

    // TODO API_TEST_START
    // (generated snippet inserted here)
    // TODO API_TEST_END
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
