// SECTION LOAD_DATA
val raster: RDD[ITile[Int]] = sc.geoTiff[Int](raster_tif)
val neighborhoods: SpatialRDD = sc.geojsonFile(vector_geojson)

// SECTION ANALYTICS
val joined = raster.raptorJoin(neighborhoods, new BeastOptions())
val mFirstBand = joined.first().m match {
  case arr: Array[Int] => arr.headOption.getOrElse(Int.MinValue)
  case f: Int => f
  case _ => Int.MinValue
}
require(mFirstBand != Int.MinValue, s"invalid pixel value in raptorJoin result: $mFirstBand")

val zsResults: Array[Collector] =
  ZonalStatistics.zonalStats2(neighborhoods, raster, classOf[Statistics], new BeastOptions())
    .map(fc => (fc._1.getAs[Int]("index"), fc._2))
    .collect
    .sortBy(_._1)
    .map(_._2)
