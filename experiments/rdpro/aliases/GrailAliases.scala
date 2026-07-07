// AUTO-MANAGED by aideal alias-function synthesis — do not hand-edit entries;
// add/update via aideal.alias_functions.sync. Each wrapper encodes a verified,
// reusable call pattern so generated code calls one grounded name.
package edu.ucr.cs.bdlab.grail

import org.apache.spark.SparkContext
import org.apache.spark.rdd.RDD
import edu.ucr.cs.bdlab.beast._
import edu.ucr.cs.bdlab.beast.cg.SpatialDataTypes.{RasterRDD, SpatialRDD}
import edu.ucr.cs.bdlab.beast.geolite.{IFeature, ITile}

object GrailAliases {

  /** Load a GeoTIFF as a FLOAT raster (the common pixel type). For int/short rasters call sc.geoTiff[Int] / sc.geoTiff[Short]. (alias for `geoTiff`) */
  def readRaster(sc: SparkContext, path: String): RasterRDD[Float] = sc.geoTiff[Float](path)

  /** Load an ESRI shapefile (.shp + sidecars) as a vector SpatialRDD (RDD[IFeature]). (alias for `shapefile`) */
  def readVectorShapefile(sc: SparkContext, path: String): SpatialRDD = sc.shapefile(path)
}
