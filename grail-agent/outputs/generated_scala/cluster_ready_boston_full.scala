import org.apache.spark.SparkContext
import org.apache.spark.sql.SparkSession
import org.apache.spark.rdd.RDD
import org.apache.spark.broadcast.Broadcast
import edu.ucr.cs.bdlab.beast._
import edu.ucr.cs.bdlab.raptor.RaptorMixin._
import edu.ucr.cs.bdlab.raptor.RaptorMixin.RasterReadMixinFunctions
import edu.ucr.cs.bdlab.beast.cg.SpatialDataTypes.RasterRDD
import edu.ucr.cs.bdlab.beast.common.BeastOptions
import edu.ucr.cs.bdlab.beast.geolite.IFeature
import edu.ucr.cs.bdlab.raptor.RaptorJoin
import java.util.{HashMap => JHashMap}

object GeoJob {

  // 0 = bare ground in Landsat Treecover, valid pixel.
  @inline def isNodata(v: Int): Boolean =
    v == 250 || v == -9999 || v == 32767 || v == -32768

  // Stats as a flat 3-element array: (0)=min, (1)=max, (2)=count
  // Avoids tuple allocation on every update.
  type LocalStats = JHashMap[String, Array[Long]]

  def mergeInto(target: LocalStats, source: LocalStats): Unit = {
    val it = source.entrySet().iterator()
    while (it.hasNext) {
      val e = it.next()
      val s = target.get(e.getKey)
      if (s == null) {
        target.put(e.getKey, e.getValue)
      } else {
        val t = e.getValue
        if (t(0) < s(0)) s(0) = t(0)
        if (t(1) > s(1)) s(1) = t(1)
        s(2) += t(2)
      }
    }
  }

  def run(sc: SparkContext, vectorPath: String, rasterPath: String, outputPath: String): Unit = {
    val t0 = System.currentTimeMillis()
    val opts = new BeastOptions()

    // Assign stable Long IDs to features — no shuffle (zipWithUniqueId is local).
    val vectorWithID: RDD[(Long, IFeature)] = sc.shapefile(vectorPath)
      .zipWithUniqueId()
      .map { case (f, id) => (id, f) }

    // Broadcast tiny Long -> GEOID map (~1.5MB for 74k tracts).
    val idToGeoid: Map[Long, String] = vectorWithID
    .map { case (id, f) => (id, f.getAs[String]("CNTRY_NAME")) }
    //  .map { case (id, f) => (id, String.valueOf(f.getAs[Any]("GEOID"))) }
      .collect()
      .toMap
    val bcGeoid: Broadcast[Map[Long, String]] = sc.broadcast(idToGeoid)

    val raster: RasterRDD[Int] = sc.geoTiff[Int](rasterPath)

    // raptorJoinIDM returns RDD[(Long featureID, Int pixelValue)] — minimal per-pixel payload.
    val pixelPairs: RDD[(Long, Int)] = RaptorJoin.raptorJoinIDM[Int](raster, vectorWithID, opts)

    // CORE OPTIMIZATION: mapPartitions instead of aggregateByKey.
    //
    // aggregateByKey shuffles pixels by GEOID key across the network — every worker
    // that holds pixels for GEOID "06001" sends them to the same reducer node.
    // For millions of pixels that shuffle dominates network I/O.
    //
    // mapPartitions lets each partition compute a complete local (min,max,count)
    // HashMap independently — zero pixel shuffle. Each partition returns at most
    // one stats entry per zone it spatially covers, which is a tiny fraction of
    // all 73k zones. The driver then merges 288 small HashMaps — cheap.
    //
    // Network cost comparison:
    //   aggregateByKey: millions of (String, Int) pairs across the network
    //   mapPartitions:  288 × (zones_per_partition × 30 bytes) — orders of magnitude less
    val partialStats: RDD[LocalStats] = pixelPairs.mapPartitions { iter =>
      val local = new LocalStats(1024)
      val geoidMap = bcGeoid.value
      while (iter.hasNext) {
        val (id, v) = iter.next()
        if (!isNodata(v)) {
          val geoid = geoidMap.getOrElse(id, s"unknown_$id")
          val vL = v.toLong
          val s = local.get(geoid)
          if (s == null) {
            local.put(geoid, Array(vL, vL, 1L))
          } else {
            if (vL < s(0)) s(0) = vL
            if (vL > s(1)) s(1) = vL
            s(2) += 1L
          }
        }
      }
      Iterator.single(local)
    }

    // Merge all partition HashMaps on the driver.
    // treeAggregate reduces depth of the merge tree — instead of all partitions
    // sending to driver sequentially, it merges in log(depth) rounds on workers first.
    val merged: LocalStats = partialStats.treeAggregate(new LocalStats(8192))(
      (acc, m) => { mergeInto(acc, m); acc },
      (a, b)   => { mergeInto(a, b); a },
      depth = 3
    )

    val elapsed = System.currentTimeMillis() - t0
    println(s"Done. ${merged.size} zones. elapsed=${elapsed}ms")

    // Write to local disk — single file, no HDFS part files to merge.
    val out = new java.io.PrintWriter(outputPath)
    try {
      out.println("zone_name,min,max,count")
      val it = merged.entrySet().iterator()
      val buf = new scala.collection.mutable.ArrayBuffer[(String, Array[Long])](merged.size)
      while (it.hasNext) {
        val e = it.next()
        buf += ((e.getKey, e.getValue))
      }
      buf.sortBy(_._1).foreach { case (geoid, s) =>
        out.println(s"$geoid,${s(0)},${s(1)},${s(2)}")
      }
    } finally {
      out.close()
    }
    println(s"Written to $outputPath")
  }
}

object GeoJobMain {
  def main(args: Array[String]): Unit = {
    val rasterPath = "hdfs:///user/zshan011/LandsatTreecover_tiled"
val vectorPath = "hdfs:///user/zshan011/boundaries/boundaries.shp"    // Output to local disk — single CSV, no getmerge needed.
    val outputPath = s"/home/zshan011/rdpro_codegen_demo/output/treecover_country_dist_${System.currentTimeMillis()}.csv"

    val spark = SparkSession.builder()
      .appName("GeoJob-ShuffleFree")
      .master("spark://ec-hn.cs.ucr.edu:7077")
      .getOrCreate()

    try {
      val t = System.currentTimeMillis()
      GeoJob.run(spark.sparkContext, vectorPath, rasterPath, outputPath)
      println(s"Total elapsed=${System.currentTimeMillis() - t}ms")
      println("__DONE__")
    } finally { spark.stop() }
  }
}
