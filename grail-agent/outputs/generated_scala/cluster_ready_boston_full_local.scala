import org.apache.spark.sql.SparkSession
import edu.ucr.cs.bdlab.beast.common.BeastOptions
import edu.ucr.cs.bdlab.beast.geolite.IFeature
import edu.ucr.cs.bdlab.raptor.{GeoTiffReader, IRasterReader, RaptorJoin}
import edu.ucr.cs.bdlab.beast.io.shapefile.ShapefileFeatureReader
import org.apache.hadoop.fs.Path
import org.apache.hadoop.conf.Configuration

object GeoJobLocal {

  // 0 is valid for Landsat Treecover (bare ground), not nodata.
  val NODATA: Set[Int] = Set(250, -9999, 32767, -32768)

  final class MutableStats(var min: Int, var max: Int, var count: Long)

  def run(hadoopConf: Configuration, vectorShpPath: String, rasterPath: String, outputPath: String): Unit = {
    val start = System.currentTimeMillis()

    val vectorReader = new ShapefileFeatureReader
    import scala.collection.JavaConverters._
    vectorReader.initialize(new Path(vectorShpPath), new BeastOptions())
    try {
      val features: Array[IFeature] = vectorReader.iterator().asScala.toArray
      val geometries = features.map(_.getGeometry)
      println(s"Loaded ${features.length} features")
      val featureNames: Array[String] = features.map(_.getAs[String]("GEOID"))

      val rasterHPath = new Path(rasterPath)
      val fs = rasterHPath.getFileSystem(hadoopConf)

      val rasterReaders: Array[IRasterReader[Int]] =
        if (fs.getFileStatus(rasterHPath).isDirectory) {
          val tifFiles = fs.listStatus(rasterHPath)
            .filter(_.getPath.getName.toLowerCase.endsWith(".tif"))
            .sortBy(_.getPath.getName)
          println(s"Found ${tifFiles.length} raster files in directory")
          tifFiles.map { status =>
            val reader = new GeoTiffReader[Int]
            reader.initialize(fs, status.getPath.toString, "0", new BeastOptions())
            reader.asInstanceOf[IRasterReader[Int]]
          }
        } else {
          val reader = new GeoTiffReader[Int]
          reader.initialize(fs, rasterPath, "0", new BeastOptions())
          Array(reader.asInstanceOf[IRasterReader[Int]])
        }

      try {
        // Use geometry overload so each hit carries featureID directly.
        val results = RaptorJoin.raptorJoinLocal(rasterReaders, geometries)

        val stats = scala.collection.mutable.HashMap.empty[String, MutableStats]
        for (r <- results) {
          val v = r.m.asInstanceOf[Int]
          if (!NODATA.contains(v)) {
            val name = featureNames(r.featureID.toInt)
            val stat = stats.getOrElseUpdate(name, new MutableStats(v, v, 0L))
            if (v < stat.min) stat.min = v
            if (v > stat.max) stat.max = v
            stat.count += 1L
          }
        }

        val elapsed = System.currentTimeMillis() - start
        println(s"Done. ${stats.size} zones. elapsed=${elapsed}ms")

        val out = new java.io.PrintWriter(outputPath)
        try {
          out.println("zone_name,min,max,count")
          stats.toSeq.sortBy(_._1).foreach { case (name, stat) =>
            out.println(s"$name,${stat.min},${stat.max},${stat.count}")
          }
        } finally {
          out.close()
        }
        println(s"Written to $outputPath")
      } finally {
        rasterReaders.foreach(_.close())
      }
    } finally {
      vectorReader.close()
    }
  }
}

object GeoJobMain {
  def main(args: Array[String]): Unit = {
    val rasterPath = "file:///home/zshan011/rdpro_codegen_demo/treecover_us_tiled"
    val vectorPath = "file:///home/zshan011/rdpro_codegen_demo/tract_refactored/tract_refactored.shp"
    val outputPath = s"/home/zshan011/rdpro_codegen_demo/output/treecover_global_counties_raptorLocal_${System.currentTimeMillis()}.csv"

    val spark = SparkSession.builder()
      .appName("GeoJobLocal")
      .master("local[*]")
      .getOrCreate()
    try {
      val t = System.currentTimeMillis()
      GeoJobLocal.run(spark.sparkContext.hadoopConfiguration, vectorPath, rasterPath, outputPath)
      println(s"Total elapsed=${System.currentTimeMillis() - t}ms")
      println("__DONE__")
    } finally { spark.stop() }
  }
}
