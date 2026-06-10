/*
 * Copyright 2022 University of California, Riverside
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

import edu.ucr.cs.bdlab.beast.cg.Reprojector
import edu.ucr.cs.bdlab.beast.cg.SpatialDataTypes.RasterRDD
import edu.ucr.cs.bdlab.beast.common.BeastOptions
import edu.ucr.cs.bdlab.beast.geolite.{Feature, IFeature, RasterMetadata}
import org.apache.spark.rdd.RDD
import org.locationtech.jts.geom.{Envelope, Geometry}

import java.awt.geom.Point2D
import scala.reflect.ClassTag

/**
 * Raster-vector operations and compatibility helpers that involve both raster and vector inputs.
 */
object RasterVectorOperations {
  case object NoDataValue

  private def typeName[T: ClassTag]: String =
    implicitly[ClassTag[T]].runtimeClass.getTypeName

  private def requireOp(condition: Boolean, op: String, message: => String): Unit =
    require(condition, s"[$op] $message")

  private def validateRasterForMask[T: ClassTag](inputRaster: RasterRDD[T]): RasterMetadata = {
    val allMetadata: Array[RasterMetadata] = RasterMetadata.allMetadata(inputRaster)
    requireOp(allMetadata.nonEmpty, "mask", s"input raster is empty (T=${typeName[T]})")
    requireOp(allMetadata.length == 1,
      "mask",
      s"expected one raster metadata, found ${allMetadata.length} (T=${typeName[T]})")
    val metadata = allMetadata.head
    requireOp(metadata.srid != 0, "mask", s"raster CRS is missing (srid=0, T=${typeName[T]})")
    requireOp(metadata.rasterWidth > 0 && metadata.rasterHeight > 0,
      "mask",
      s"invalid raster dimensions: ${metadata.rasterWidth}x${metadata.rasterHeight} (T=${typeName[T]})")
    requireOp(metadata.g2m != null, "mask", s"raster transform is missing (T=${typeName[T]})")
    metadata
  }

  private def normalizeGeometries(geometries: Seq[Geometry], targetSRID: Int): Seq[Geometry] = {
    val validGeometries = geometries.iterator
      .filter(_ != null)
      .filterNot(_.isEmpty)
      .map { geom =>
        if (geom.getSRID == 0 || geom.getSRID == targetSRID) geom
        else Reprojector.reprojectGeometry(geom, targetSRID)
      }
      .toVector
    requireOp(validGeometries.nonEmpty, "mask", "no valid geometries found")
    validGeometries
  }

  private def cropMetadata(metadata: RasterMetadata, geometries: Seq[Geometry]): RasterMetadata = {
    val envelope = new Envelope()
    geometries.foreach(g => envelope.expandToInclude(g.getEnvelopeInternal))

    val corners = Array(
      new Point2D.Double(envelope.getMinX, envelope.getMinY),
      new Point2D.Double(envelope.getMinX, envelope.getMaxY),
      new Point2D.Double(envelope.getMaxX, envelope.getMinY),
      new Point2D.Double(envelope.getMaxX, envelope.getMaxY)
    )
    val gridCorners = corners.map { corner =>
      val gridPoint = new Point2D.Double()
      metadata.modelToGrid(corner.x, corner.y, gridPoint)
      gridPoint
    }

    val minX = math.floor(gridCorners.map(_.x).min).toInt max metadata.x1
    val minY = math.floor(gridCorners.map(_.y).min).toInt max metadata.y1
    val maxX = math.ceil(gridCorners.map(_.x).max).toInt min metadata.x2
    val maxY = math.ceil(gridCorners.map(_.y).max).toInt min metadata.y2

    requireOp(minX < maxX && minY < maxY, "mask", "input geometries do not overlap the raster")

    val topLeft = new Point2D.Double()
    val bottomRight = new Point2D.Double()
    metadata.gridToModel(minX, minY, topLeft)
    metadata.gridToModel(maxX, maxY, bottomRight)

    RasterMetadata.create(
      topLeft.x,
      topLeft.y,
      bottomRight.x,
      bottomRight.y,
      metadata.srid,
      maxX - minX,
      maxY - minY,
      metadata.tileWidth min (maxX - minX),
      metadata.tileHeight min (maxY - minY)
    )
  }

  private def featureRDDFromGeometries(inputRaster: RasterRDD[_], geometries: Seq[Geometry]): RDD[IFeature] =
    inputRaster.sparkContext.parallelize(geometries, inputRaster.getNumPartitions max 1)
      .map(geom => Feature.create(null, geom).asInstanceOf[IFeature])

  private def fillEmptyPixels[T: ClassTag](inputRaster: RasterRDD[T], noDataValue: T): RasterRDD[T] =
    inputRaster.map { tile =>
      val out = new MemoryTile[T](tile.tileID, tile.rasterMetadata, tile.rasterFeature)
      var y = tile.y1
      while (y <= tile.y2) {
        var x = tile.x1
        while (x <= tile.x2) {
          if (tile.isEmpty(x, y))
            out.setPixelValue(x, y, noDataValue)
          else
            out.setPixelValue(x, y, tile.getPixelValue(x, y))
          x += 1
        }
        y += 1
      }
      out
    }

  private def maskAndCrop[T: ClassTag](inputRaster: RasterRDD[T], geometries: Seq[Geometry]): RasterRDD[T] = {
    val metadata = validateRasterForMask(inputRaster)
    val normalizedGeometries = normalizeGeometries(geometries, metadata.srid)
    val maskedRaster = RaptorJoin.mask(inputRaster, featureRDDFromGeometries(inputRaster, normalizedGeometries), new BeastOptions())
    requireOp(maskedRaster.take(1).nonEmpty, "mask", "input geometries do not overlap the raster")
    RasterOperationsFocal.reshapeNN(maskedRaster, _ => cropMetadata(metadata, normalizedGeometries))
  }

  def mask[T: ClassTag](inputRaster: RasterRDD[T], geometries: Seq[Geometry], noDataValue: NoDataValue.type): RasterRDD[T] =
    maskAndCrop(inputRaster, geometries)

  def mask[T: ClassTag](inputRaster: RasterRDD[T], geometries: Seq[Geometry]): RasterRDD[T] =
    mask(inputRaster, geometries, NoDataValue)

  def mask[T: ClassTag](inputRaster: RasterRDD[T], geometries: Seq[Geometry], noDataValue: T): RasterRDD[T] =
    fillEmptyPixels(maskAndCrop(inputRaster, geometries), noDataValue)

  def mask[T: ClassTag](inputRaster: RasterRDD[T], geometries: Array[Geometry], noDataValue: NoDataValue.type): RasterRDD[T] =
    mask(inputRaster, geometries.toSeq, noDataValue)

  def mask[T: ClassTag](inputRaster: RasterRDD[T], geometries: Array[Geometry]): RasterRDD[T] =
    mask(inputRaster, geometries.toSeq, NoDataValue)

  def mask[T: ClassTag](inputRaster: RasterRDD[T], geometries: Array[Geometry], noDataValue: T): RasterRDD[T] =
    mask(inputRaster, geometries.toSeq, noDataValue)

  def mask[T: ClassTag](inputRaster: RasterRDD[T], features: RDD[IFeature], noDataValue: NoDataValue.type): RasterRDD[T] =
    mask(inputRaster, features.map(_.getGeometry).collect().toSeq, noDataValue)

  def mask[T: ClassTag](inputRaster: RasterRDD[T], features: RDD[IFeature]): RasterRDD[T] =
    mask(inputRaster, features.map(_.getGeometry).collect().toSeq, NoDataValue)

  def mask[T: ClassTag](inputRaster: RasterRDD[T], features: RDD[IFeature], noDataValue: T): RasterRDD[T] =
    mask(inputRaster, features.map(_.getGeometry).collect().toSeq, noDataValue)
}
