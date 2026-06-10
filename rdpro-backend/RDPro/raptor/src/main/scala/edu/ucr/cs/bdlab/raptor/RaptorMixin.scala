/*
 * Copyright 2020 University of California, Riverside
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package edu.ucr.cs.bdlab.raptor

import edu.ucr.cs.bdlab.beast.cg.SpatialDataTypes.{RasterRDD, SpatialRDD}
import edu.ucr.cs.bdlab.beast.common.BeastOptions
import edu.ucr.cs.bdlab.beast.geolite.{IFeature, ITile, RasterFeature, RasterMetadata}
import edu.ucr.cs.bdlab.raptor.RasterOperationsFocal.InterpolationMethod
import org.apache.spark.SparkContext
import org.apache.spark.beast.CRSServer
import org.apache.spark.rdd.RDD
import org.apache.spark.sql.types.StructType
import org.locationtech.jts.geom.Geometry
import org.opengis.referencing.crs.CoordinateReferenceSystem

import scala.reflect.ClassTag

trait RaptorMixin {

  implicit class RasterReadMixinFunctions(sc: SparkContext) {
    /**
     * Loads a GeoTIFF file as an RDD of tiles
     * @param path the path of the file
     * @param iLayer the index of the band to load (0 by default)
     * @param opts additional options for loading the file
     * @return a [[RasterRDD]] that represents all tiles in the file
     */
    def geoTiff[T](path: String, iLayer: Int = 0, opts: BeastOptions = new BeastOptions): RDD[ITile[T]] = {
      if (!opts.contains(IRasterReader.RasterLayerID))
        opts.set(IRasterReader.RasterLayerID, iLayer)
      new RasterFileRDD[T](sc, path, opts)
    }

    /**
     * Compatibility alias for generated code and users coming from other ecosystems.
     * This method does not add any Sedona/GeoTrellis/GDAL dependency; it delegates to [[geoTiff]].
     */
    def readGeoTiffAsRDD[T](path: String, opts: BeastOptions): RDD[ITile[T]] =
      geoTiff[T](path, 0, opts)

    /**
     * Compatibility alias for generated code and users coming from other ecosystems.
     * This method does not add any Sedona/GeoTrellis/GDAL dependency; it delegates to [[geoTiff]].
     */
    def readGeoTiffAsRDD[T](path: String, iLayer: Int = 0, opts: BeastOptions = new BeastOptions): RDD[ITile[T]] =
      geoTiff[T](path, iLayer, opts)

    /** GDAL-style naming alias. Delegates to [[geoTiff]]. */
    def gdalOpen[T](path: String, iLayer: Int = 0, opts: BeastOptions = new BeastOptions): RDD[ITile[T]] =
      geoTiff[T](path, iLayer, opts)

    /** GeoTrellis-style naming alias. Delegates to [[geoTiff]]. */
    def geotrellisRead[T](path: String, iLayer: Int = 0, opts: BeastOptions = new BeastOptions): RDD[ITile[T]] =
      geoTiff[T](path, iLayer, opts)

    /** Sedona-style naming alias. Delegates to [[geoTiff]]. */
    def sedonaReadRaster[T](path: String, iLayer: Int = 0, opts: BeastOptions = new BeastOptions): RDD[ITile[T]] =
      geoTiff[T](path, iLayer, opts)

    /** Generic loader alias. Delegates to [[geoTiff]]. */
    def loadGeoTiffRDD[T](path: String, iLayer: Int = 0, opts: BeastOptions = new BeastOptions): RDD[ITile[T]] =
      geoTiff[T](path, iLayer, opts)

    /** Generic loader alias. Delegates to [[geoTiff]]. */
    def readRasterRDD[T](path: String, iLayer: Int = 0, opts: BeastOptions = new BeastOptions): RDD[ITile[T]] =
      geoTiff[T](path, iLayer, opts)

    /** Generic loader alias. Delegates to [[geoTiff]]. */
    def openGeoTiffRDD[T](path: String, iLayer: Int = 0, opts: BeastOptions = new BeastOptions): RDD[ITile[T]] =
      geoTiff[T](path, iLayer, opts)

    /**
     * Generic readRDD alias for compatibility with generated code.
     * Supported formats:
     *  - tiff / geotiff / tif : delegates to [[geoTiff]]
     *  - hdf / hdf4 / hdf5    : delegates to [[hdfFile]] (expects layer in [[IRasterReader.RasterLayerID]] or defaults to "0")
     */
    def readRDD[T](path: String, format: String, iLayer: Int = 0, opts: BeastOptions = new BeastOptions): RDD[ITile[T]] = {
      val f = Option(format).getOrElse("tiff").trim.toLowerCase
      f match {
        case "tiff" | "geotiff" | "tif" =>
          geoTiff[T](path, iLayer, opts)
        case "hdf" | "hdf4" | "hdf5" =>
          val layer = if (opts.contains(IRasterReader.RasterLayerID)) opts.getString(IRasterReader.RasterLayerID) else "0"
          hdfFile(path, layer, opts).asInstanceOf[RDD[ITile[T]]]
        case other =>
          throw new IllegalArgumentException(
            s"Unsupported raster format '$other' in readRDD. Supported: tiff/geotiff/tif/hdf/hdf4/hdf5"
          )
      }
    }

    /** Short generic alias. Delegates to [[readRDD]]. */
    def read[T](path: String, format: String = "tiff", iLayer: Int = 0, opts: BeastOptions = new BeastOptions): RDD[ITile[T]] =
      readRDD[T](path, format, iLayer, opts)

    /** Short generic alias. Delegates to [[readRDD]]. */
    def load[T](path: String, format: String = "tiff", iLayer: Int = 0, opts: BeastOptions = new BeastOptions): RDD[ITile[T]] =
      readRDD[T](path, format, iLayer, opts)

    def hdfFile(path: String, layer: String, opts: BeastOptions = new BeastOptions()): RDD[ITile[Float]] = {
      opts.set(IRasterReader.RasterLayerID, layer)
      new RasterFileRDD(sc, path, opts)
    }

    /**
     * Creates a [[RasterRDD]] from a given set of pixel locations and values.
     * @param pixels the pixel values
     * @param metadata the metadata that describes the raster
     * @tparam T the type of pixels
     * @return a raster RDD that holds the given pixels
     */
    def rasterizePixels[T: ClassTag](pixels: RDD[(Int, Int, T)], metadata: RasterMetadata, rasterFeature: RasterFeature): RasterRDD[T] =
      RasterOperationsGlobal.rasterizePixels(pixels, metadata, rasterFeature)

    /**
     * Creates a raster from a list of point locations and values.
     * @param points point locations and raster values
     * @param metadata the metadata that describes the raster location
     * @tparam T the type of raster values
     * @return a raster that contains the given point locations
     */
    def rasterizePoints[T: ClassTag](points: RDD[(Double, Double, T)], metadata: RasterMetadata, rasterFeature: RasterFeature): RasterRDD[T] =
      RasterOperationsGlobal.rasterizePoints(points, metadata, rasterFeature)
  }

  implicit class RaptorMixinOperations3[T](raster: RasterRDD[T]) {
    /**
     * Returns the spatial reference ID (SRID) of the raster data.
     * This function returns the SRID of the first tile assuming that all tiles have the same SRID.
     * @return the SRID of the raster data or 0 if SRID is unknown or undefined
     */
    def getSRID: Int = raster.first().rasterMetadata.srid

    /**
     * Performs a Raptor join operation with a set of vector features.
     * @param features the set of features to join with
     * @param opts additional options to configure the operation
     * @tparam T the type of the value in the result. Should be compatible with the pixel type of the raster
     * @return all overlaps between the given features and the pixels.
     */
    def raptorJoin(features: SpatialRDD, opts: BeastOptions = new BeastOptions)(implicit t: ClassTag[T]):
      RDD[RaptorJoinFeature[T]] =
      RaptorJoin.raptorJoinFeature[T](raster, features, opts, null)

    /**
     * Overlays this raster RDD on top other ones
     * @param rasters the other rasters to stack this raster on
     * @return a new RasterRDD which contains the stack of this raster on top of the given ones
     */
    def overlay[V](rasters: RasterRDD[T]*)(implicit t: ClassTag[T], v: ClassTag[V]): RasterRDD[Array[V]] =
      RasterOperationsLocal.overlay((Seq(raster) ++ rasters):_*)

    /**
     * Save this RasterRDD as a set of geoTIFF files.
     * @param path the path to write the output geotiff files to
     * @param opts additional options for saving the GeoTIFF file
     *
     * Write options are:
     *  - *overwrite* - Overwrites the output path if exists
     *  - *bitspersample* - A comma-separated list of bits per sample for each band
     *  - *fillvalue* - A value to use for writing empty pixels. This should be a value that doesn't exist in the data.
     *  - *compression* - Type of compression to use for tile data (1=PackBits, 5=LZW, 8=Deflate)
     *  - *writemode* - How to write the output {compatibility, distributed} - Default = distributed
     *  - *noemptytiles* - If true, write an empty tile for non-existent tiles. If false, add a marker of zero offset
     *                     and zero length to indicate non-existent tiles.
     */
    def saveAsGeoTiff(path: String, opts: BeastOptions = new BeastOptions): Unit =
      GeoTiffWriter.saveAsGeoTiff[T](raster, path, opts)

    /**
     * Returns an array of all unique metadata in this RDD
     * @return
     */
    def allMetadata: Array[RasterMetadata] = RasterMetadata.allMetadata(raster)

    /**
     * Applies a mathematical function to each pixel in the input and produce the output raster.
     * @param f the function to apply on each pixel of the input
     * @tparam U the type of the output parameter
     * @return a new raster after the function is applied on each pixel
     */
    def mapPixels[U: ClassTag](f: T => U)(implicit t: ClassTag[T]): RasterRDD[U] =
      RasterOperationsLocal.mapPixels(raster, f)

    /**
     * Compatibility alias used by generated code from other raster APIs.
     * Applies a tile-level transformation.
     */
    def mapTiles[U: ClassTag](f: ITile[T] => ITile[U])(implicit t: ClassTag[T]): RasterRDD[U] =
      raster.map(f)

    /**
     * Removes pixels that do not pass the given filter. Each pixel in the input raster is tested using the given
     * function. If it returns true, the pixel is kept as-is. If it returns false, the filter is removed.
     * @param f the filter that tests which pixels to keep
     * @return a new raster with the same input resolution after removing non-matching pixels.
     */
    def filterPixels(f: T => Boolean)(implicit t: ClassTag[T]): RasterRDD[T] =
      RasterOperationsLocal.filterPixels(raster, f)

    /**
     * Rasterio-style compatibility alias for geometry masking with crop=true semantics.
     * When `noDataValue` is [[RasterOperationsLocal.NoDataValue]], uncovered pixels remain empty.
     */
    def mask(geometries: Seq[Geometry])(implicit t: ClassTag[T]): RasterRDD[T] =
      RasterVectorOperations.mask(raster, geometries)

    def mask(geometries: Seq[Geometry], noDataValue: RasterOperationsLocal.NoDataValue.type)
            (implicit t: ClassTag[T]): RasterRDD[T] =
      RasterVectorOperations.mask(raster, geometries, noDataValue)

    /**
     * Rasterio-style compatibility alias for geometry masking with crop=true semantics.
     * Uncovered pixels are filled with the provided `noDataValue`.
     */
    def mask(geometries: Seq[Geometry], noDataValue: T)(implicit t: ClassTag[T]): RasterRDD[T] =
      RasterVectorOperations.mask(raster, geometries, noDataValue)

    def mask(geometries: Array[Geometry], noDataValue: RasterOperationsLocal.NoDataValue.type)
            (implicit t: ClassTag[T]): RasterRDD[T] =
      RasterVectorOperations.mask(raster, geometries, noDataValue)

    def mask(geometries: Array[Geometry])(implicit t: ClassTag[T]): RasterRDD[T] =
      RasterVectorOperations.mask(raster, geometries)

    def mask(geometries: Array[Geometry], noDataValue: T)(implicit t: ClassTag[T]): RasterRDD[T] =
      RasterVectorOperations.mask(raster, geometries, noDataValue)

    def mask(features: RDD[IFeature])(implicit t: ClassTag[T]): RasterRDD[T] =
      RasterVectorOperations.mask(raster, features)

    def mask(features: RDD[IFeature], noDataValue: RasterOperationsLocal.NoDataValue.type)
            (implicit t: ClassTag[T]): RasterRDD[T] =
      RasterVectorOperations.mask(raster, features, noDataValue)

    def mask(features: RDD[IFeature], noDataValue: T)(implicit t: ClassTag[T]): RasterRDD[T] =
      RasterVectorOperations.mask(raster, features, noDataValue)

    /**
     * Regrids the given raster to the target tile width and height
     * @param tileWidth the new tile width in pixels
     * @param tileHeight the new tile height in pixels
     * @return a new raster with the given tile width and height
     */
    def retile(tileWidth: Int, tileHeight: Int)(implicit t: ClassTag[T]): RasterRDD[T] =
      RasterOperationsFocal.retile(raster, tileWidth, tileHeight)

    /**
     * Reproject a raster to a target coordinate reference system.
     * This method uses the same resolution (number of pixels) of the first tile in the source raster.
     * @param targetSRID the spatial reference identifier (SRID) of the desired coordinate reference system.
     * @return a new raster RDD with the desired coordinate reference system.
     */
    def reproject(targetSRID: Int)(implicit t: ClassTag[T]): RasterRDD[T] =
      RasterOperationsFocal.reproject(raster, CRSServer.sridToCRS(targetSRID))

    /**
     * Reproject a raster to a target coordinate reference system.
     * This method uses the same resolution (number of pixels) of the first tile in the source raster.
     * @param targetCRS the desired coordinate reference system
     * @return a new raster RDD with the desired coordinate reference system.
     */
    def reproject(targetCRS: CoordinateReferenceSystem, unifiedRaster: Boolean = false,
                  interpolationMethod: InterpolationMethod.InterpolationMethod =
        InterpolationMethod.NearestNeighbor)(implicit t: ClassTag[T]): RasterRDD[T] =
      RasterOperationsFocal.reproject(raster, targetCRS, unifiedRaster, interpolationMethod)

    /**
     * Changes the resolution of the raster to the desired resolution without changing tile size or CRS.
     * @param rasterWidth the new raster width in terms of pixels
     * @param rasterHeight the new height of the raster layer in terms of pixels
     * @return a new raster RDD with the desired width and height
     */
    def rescale(rasterWidth: Int, rasterHeight: Int, unifiedRaster: Boolean = false,
                interpolationMethod: InterpolationMethod.InterpolationMethod =
        InterpolationMethod.NearestNeighbor)(implicit t: ClassTag[T]): RasterRDD[T] =
      RasterOperationsFocal.rescale(raster, rasterWidth, rasterHeight, unifiedRaster, interpolationMethod)

    /**
     * Extract all pixel values into an RDD
     * @return an RDD that contains all pixel locations and values
     */
    def flatten: RDD[(Int, Int, RasterMetadata, T)] = RasterOperationsGlobal.flatten(raster)

    /**
     * Explodes the given raster RDD into separate tiles that are ready to be written to separate files.
     * @return
     */
    def explode: RasterRDD[T] = RasterOperationsLocal.explode(raster)
  }

  /**
   * Compatibility tile-level helpers for generated code.
   */
  implicit class ITileCompatOps[T](tile: ITile[T]) {
    def mapPixels[U: ClassTag](f: T => U): ITile[U] =
      new MapPixelsTile[T, U](tile, f)
  }
}

object RaptorMixin extends RaptorMixin
