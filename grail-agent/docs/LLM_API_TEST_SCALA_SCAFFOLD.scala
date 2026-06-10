import org.apache.spark.SparkContext
import org.apache.spark.sql.SparkSession
import org.apache.spark.SparkConf
import edu.ucr.cs.bdlab.beast._
import edu.ucr.cs.bdlab.raptor.RaptorMixin._
import edu.ucr.cs.bdlab.raptor.RaptorMixin.RasterReadMixinFunctions
import edu.ucr.cs.bdlab.beast.cg.SpatialDataTypes.RasterRDD
import edu.ucr.cs.bdlab.beast.io.tiff.TiffConstants
import edu.ucr.cs.bdlab.beast.common.BeastOptions
import edu.ucr.cs.bdlab.beast.geolite.{ITile, RasterFeature, RasterMetadata}
import edu.ucr.cs.bdlab.raptor.{GeoTiffWriter, RasterOperationsFocal, RasterOperationsLocal, RasterOperationsGlobal}
import java.net.URI
import java.nio.file.{Paths, Files}

object ApiTest {
  def run(sc: SparkContext): Unit = {
    val inputA = "{{INPUT_A}}"
    val inputB = "{{INPUT_B}}"
    val output = "{{OUTPUT_PATH}}"

    // TODO API_TEST_START
    // Example skeleton (replace based on API under test):
    // val aRaw: RasterRDD[{{READ_TYPE_A}}] = sc.geoTiff[{{READ_TYPE_A}}](inputA)
    // val bRaw: RasterRDD[{{READ_TYPE_B}}] = sc.geoTiff[{{READ_TYPE_B}}](inputB)
    // val a: RasterRDD[Float] = aRaw.mapPixels(v => v.toFloat)
    // val b: RasterRDD[Float] = bRaw.mapPixels(v => v.toFloat)
    // println("a pixelType=" + a.first().pixelType)
    // println("b pixelType=" + b.first().pixelType)
    // val stacked: RasterRDD[Array[Float]] = a.overlay(b)
    // val out: RasterRDD[Float] = stacked.mapPixels(vs => (vs(1) - vs(0)) / (vs(1) + vs(0)))
    // out.saveAsGeoTiff(output, Seq(GeoTiffWriter.Compression -> TiffConstants.COMPRESSION_LZW,GeoTiffWriter.WriteMode -> "compatibility"))
    // println("count=" + out.count())
    // TODO API_TEST_END
  }
}

try {
  ApiTest.run(sc)
  println("__DONE__ object=ApiTest")
} catch {
  case t: Throwable =>
    Console.err.println("__RUN_ERR__ " + t.getClass.getName + ": " + t.getMessage)
    t.printStackTrace()
    throw t
}
System.exit(0)
