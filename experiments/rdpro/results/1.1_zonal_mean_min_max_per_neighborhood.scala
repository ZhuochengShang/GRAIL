// SECTION LOAD_DATA
val raster = sc.geoTiff(raster_tif)
val neighborhoods = sparkContext.shapefile(vector_shapefile)

// SECTION ANALYTICS
val joinedData = neighborhoods.raptorJoin(raster, new BeastOptions())
val stats = ZonalStatistics.zonalStats2(joinedData, raster, classOf[Statistics], new BeastOptions())
val output = stats.map { case (feature, statistics) =>
  val neighborhoodName = feature.getAs[String]("name")
  val meanValue = statistics.mean
  val minValue = statistics.min
  val maxValue = statistics.max
  val pixelCount = statistics.count
  (neighborhoodName, meanValue, minValue, maxValue, pixelCount)
}
output.saveAsTextFile(output_dir)
