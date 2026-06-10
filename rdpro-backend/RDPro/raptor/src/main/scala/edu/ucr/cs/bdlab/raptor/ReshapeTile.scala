package edu.ucr.cs.bdlab.raptor

import edu.ucr.cs.bdlab.beast.geolite.{ITile, RasterFeature, RasterMetadata}
import edu.ucr.cs.bdlab.raptor.ReshapeTile.Computers
import org.apache.spark.sql.types._
import org.opengis.referencing.operation.MathTransform

import scala.reflect.ClassTag

/**
 * An intermediate structure that stores all the information needed to compute a given output tile from a reshape
 * function.
 * @param tileID the tile ID to compute
 * @param metadata the metadata of the output tile
 * @param rasterFeature additional features for the output raster
 * @param t
 * @tparam T
 */
class ReshapeTile[T](val tileID: Int, targetMetadata: RasterMetadata, rasterFeature: RasterFeature)
                    (implicit t: ClassTag[T]) extends Serializable {

  /** The list of all tiles that are used to calculate this tile */
  val inputTiles: scala.collection.mutable.ArrayBuffer[ITile[T]] = new scala.collection.mutable.ArrayBuffer[ITile[T]]()

  def getInputTiles: Seq[ITile[T]] = inputTiles.toSeq

  def withInputTiles(newTiles: Seq[ITile[T]]): ReshapeTile[T] = {
    val updated = new ReshapeTile[T](tileID, targetMetadata, rasterFeature)
    newTiles.foreach(updated.addTile)
    updated
  }

  def addTile(tile: ITile[T]): Unit = {
    inputTiles.append(tile)
  }

  def addSubsetTile(tile: ITile[T]): Unit = {
    // Map the corners of the target tile (this tile) to the source metadata to find the range of pixels of interest
    val locations = Array[Float](targetMetadata.getTileX1(tileID), targetMetadata.getTileY1(tileID),
      targetMetadata.getTileX2(tileID) + 1, targetMetadata.getTileY1(tileID),
      targetMetadata.getTileX1(tileID), targetMetadata.getTileY2(tileID) + 1,
      targetMetadata.getTileX2(tileID) + 1, targetMetadata.getTileY2(tileID) + 1)
    // Transform from
    val targetToSource = RasterMetadata.gridToGridTransform(targetMetadata, tile.rasterMetadata)
    targetToSource.transform(locations, 0, locations, 0, 4)
    val minX = (locations(0) min locations(2) min locations(4) min locations(6)).toInt
    val maxX = (locations(0) max locations(2) max locations(4) max locations(6)).toInt
    val minY = (locations(1) min locations(3) min locations(5) min locations(7)).toInt
    val maxY = (locations(1) max locations(3) max locations(5) max locations(7)).toInt
    inputTiles.append(new SubsetTile(tile, minX - 1, minY - 1, maxX + 1, maxY + 1))
  }

  def merge(other: ReshapeTile[T]): ReshapeTile[T] = {
    for (t <- other.inputTiles; if t != null)
      addTile(t)
    this
  }

  def resultTile: ITile[T] = {
    val tile = new MemoryTile[T](tileID, targetMetadata, rasterFeature)
    val averageComputer: ReshapeTile.AverageComputerFunction[Any] = Computers(tile.pixelType)
    val sourceMetadata = inputTiles.map(_.rasterMetadata).distinct
    val values = new Array[T](targetMetadata.tileWidth * targetMetadata.tileHeight)
    val counts = new Array[Int](targetMetadata.tileWidth * targetMetadata.tileHeight)
    val targetToSourceGrid = sourceMetadata.map(m => RasterMetadata.gridToGridTransform(targetMetadata, m))
    for (y <- targetMetadata.getTileY1(tileID) to targetMetadata.getTileY2(tileID);
         x <- targetMetadata.getTileX1(tileID) to targetMetadata.getTileX2(tileID)) {
      // Map the center of the target pixel to every source raster
      val targetPointLocation = Array[Float](x + 0.5f, y + 0.5f)
      // Try with one source metadata at a time until we find a matching tile
      // TODO: Consider the case of one pixel falling between two metadata, i.e., two source files
      for (iMetadata <- sourceMetadata.indices) {
        val sourcePointLocation = new Array[Float](2)
        targetToSourceGrid(iMetadata).transform(targetPointLocation, 0, sourcePointLocation, 0, 1)
        val sourceTileID = sourceMetadata(iMetadata).getTileIDAtPixel(sourcePointLocation(0).toInt, sourcePointLocation(1).toInt)
        // Check if we have this tile
        val sourceTileO: Option[ITile[T]] = inputTiles.find(t => t.tileID == sourceTileID && t.rasterMetadata == sourceMetadata(iMetadata))
        if (sourceMetadata(iMetadata).isPixelInRange(sourcePointLocation(0).toInt, sourcePointLocation(1).toInt) &&  sourceTileO.isDefined) {
          val sourceTile = sourceTileO.get
          val sourceValues = new Array[T](4)
          val sourcePixelExists = new Array[Boolean](4)
          // Check if we can find all four surrounding points within this tile. This will be true for most cases
          if (sourceMetadata(iMetadata).getTileX2(sourceTileID) - sourcePointLocation(0) > 1.0 &&
            sourceMetadata(iMetadata).getTileY2(sourceTileID) - sourcePointLocation(1) > 1.0) {
            // Can compute the target pixel value entirely from this pixel
            // Retrieve the four pixels that surround where the mapping landed
            var i = 0
            for (dy <- Array(0, 1); dx <- Array(0, +1)) {
              val xx: Int = sourcePointLocation(0).toInt + dx
              val yy: Int = sourcePointLocation(1).toInt + dy
              assert(sourceTile.isPixelInRange(xx, yy),
                s"Unexpected out-of-bound pixel with the simple case $xx $yy in tile $sourceTile, sourcePointLocation: ${sourcePointLocation.mkString(",")}")
              sourcePixelExists(i) = sourceTile.isDefined(xx, yy)
              if (sourcePixelExists(i))
                sourceValues(i) = sourceTile.getPixelValue(xx, yy)
              i += 1
            }
          } else {
            // Map each corner point to find up-to four tiles for the surrounding pixels
            // Retrieve the four pixels that surround where the target pixel maps in source raster
            var i = 0
            for (dy <- Array(0, 1); dx <- Array(0, +1)) {
              val xx: Int = sourcePointLocation(0).toInt + dx
              val yy: Int = sourcePointLocation(1).toInt + dy
              val sourceTileID = sourceMetadata(iMetadata).getTileIDAtPixel(xx, yy)
              val sourceTileO: Option[ITile[T]] = inputTiles.find(t => t.tileID == sourceTileID && t.rasterMetadata == sourceMetadata(iMetadata))
              if (sourceTileO.isDefined) {
                sourcePixelExists(i) = sourceTileO.get.isDefined(xx, yy)
                if (sourcePixelExists(i))
                  sourceValues(i) = sourceTileO.get.getPixelValue(xx, yy)
                i += 1
              }
            }
          }
          // Now, given the four values, apply the bilinear function by average the values horizontally,
          // and then averaging the two averages vertically
          // Since some pixels might be undefined, we will ignore them in average calculation
          val xRatio: Float = sourcePointLocation(0) - sourcePointLocation(0).toInt
          val yRatio: Float = sourcePointLocation(1) - sourcePointLocation(1).toInt
          val average1: T = if (sourcePixelExists(0) && sourcePixelExists(1))
            averageComputer(sourceValues(0), sourceValues(1), xRatio).asInstanceOf[T]
          else if (sourcePixelExists(0))
            sourceValues(0)
          else
            sourceValues(1)
          val average1Exists = sourcePixelExists(0) || sourcePixelExists(1)
          val average2: T = if (sourcePixelExists(2) && sourcePixelExists(3))
            averageComputer(sourceValues(2), sourceValues(3), xRatio).asInstanceOf[T]
          else if (sourcePixelExists(2))
            sourceValues(2)
          else
            sourceValues(3)
          val average2Exists = sourcePixelExists(2) || sourcePixelExists(3)
          val finalValue: T = if (average1Exists && average2Exists)
            averageComputer(average1, average2, yRatio).asInstanceOf[T]
          else if (average1Exists)
            average1
          else
            average2
          if (average1Exists || average2Exists) {
            val offset: Int = (y - targetMetadata.getTileY1(tileID)) * targetMetadata.tileWidth +
              (x - targetMetadata.getTileX1(tileID))
            if (counts(offset) == 0)
              values(offset) = finalValue
            else
              values(offset) = averageComputer(values(offset), finalValue, 1.0f).asInstanceOf[T]
            counts(offset) += 1
          }
        }
      }
    }
    // Use the values to fill in the table
    for (y <- tile.y1 to tile.y2; x <- tile.x1 to tile.x2) {
      val offset = (y - tile.y1) * tile.tileWidth + (x - tile.x1)
      if (counts(offset) > 0) {
        // Compute the final value as values(offset) / counts(offset)
        tile.setPixelValue(x, y, averageComputer(values(offset), values(offset), counts(offset) / 2.0f).asInstanceOf[T])
      }
    }
    tile // todo: clear all before return tile
  }
}

object ReshapeTile {

  /**
   * Get a list of target tiles that are affected by a source tile
   *
   * @param sourceTileID   the ID of the source tile to consider
   * @param targetMetadata the raster metadata that describes the target tile
   * @param sourceMetadata the raster metadata that describes the source layer
   * @return all valid target tile IDs that can be affected by the given source tile
   */
  def getTargetTilesForSourceTiles(sourceTileID: Int, targetMetadata: RasterMetadata, sourceMetadata: RasterMetadata): Array[Int] = {
    val sourceCornerPoints: Array[Double] = Array[Double](
      sourceMetadata.getTileX1(sourceTileID) - 1, sourceMetadata.getTileY1(sourceTileID) - 1,
      sourceMetadata.getTileX2(sourceTileID) + 1, sourceMetadata.getTileY1(sourceTileID) - 1,
      sourceMetadata.getTileX2(sourceTileID) + 1, sourceMetadata.getTileY2(sourceTileID) + 1,
      sourceMetadata.getTileX1(sourceTileID) - 1, sourceMetadata.getTileY2(sourceTileID) + 1,
    )
    val sourceGtoTargetG: MathTransform = RasterMetadata.gridToGridTransform(sourceMetadata, targetMetadata)
    val targetCornerPoints: Array[Double] = new Array[Double](8)
    sourceGtoTargetG.transform(sourceCornerPoints, 0, targetCornerPoints, 0, 4)

    val xs = Array[Double](targetCornerPoints(0), targetCornerPoints(2), targetCornerPoints(4), targetCornerPoints(6))
    val ys = Array[Double](targetCornerPoints(1), targetCornerPoints(3), targetCornerPoints(5), targetCornerPoints(7))
    val minX: Int = xs.min.floor.toInt
    val maxX: Int = xs.max.ceil.toInt
    val minY: Int = ys.min.floor.toInt
    val maxY: Int = ys.max.ceil.toInt
    var x = minX
    var y = minY
    var results = Array[Int]()
    while (y <= maxY && x <= maxX) {
      if (x >= targetMetadata.x1 && x < targetMetadata.x2 && y >= targetMetadata.y1 && y < targetMetadata.y2) {
        val tid = targetMetadata.getTileIDAtPixel(x, y)
        results = results :+ tid
      }
      x = (x + targetMetadata.tileWidth) / targetMetadata.tileWidth * targetMetadata.tileWidth
      if (x > maxX) {
        x = minX
        y = (y + targetMetadata.tileHeight) / targetMetadata.tileHeight * targetMetadata.tileHeight
      }
    }
    results.distinct
  }

  /** A function that computes the weighted average of two values. The  */
  type AverageComputerFunction[T] = (T, T, Float) => T

  val AverageFloat: (Float, Float, Float) => Float = (x1, x2, ratio) => x1 * (1 - ratio) + x2 * ratio
  val AverageInt: (Int, Int, Float) => Int = (x1, x2, ratio) => AverageFloat(x1, x2, ratio).toInt
  val AverageDouble: (Double, Double, Float) => Double = (x1, x2, ratio) => x1 * (1 - ratio) + x2 * ratio
  val AverageFloatArray: (Array[Float], Array[Float], Float) => Array[Float] =
    (x1, x2, ratio) => x1.zip(x2).map(p => AverageFloat(p._1, p._2, ratio))
  val AverageIntArray: (Array[Int], Array[Int], Float) => Array[Int] =
    (x1, x2, ratio) => x1.zip(x2).map(p => AverageInt(p._1, p._2, ratio))
  val AverageDoubleArray: (Array[Double], Array[Double], Float) => Array[Double] =
    (x1, x2, ratio) => x1.zip(x2).map(p => AverageDouble(p._1, p._2, ratio))

  /** A map from a pixel type to a function that computed the weighted average */
  val Computers: Map[DataType, AverageComputerFunction[Any]] = Map(
    IntegerType -> AverageInt.asInstanceOf[AverageComputerFunction[Any]],
    FloatType -> AverageFloat.asInstanceOf[AverageComputerFunction[Any]],
    DoubleType -> AverageDouble.asInstanceOf[AverageComputerFunction[Any]],
    ArrayType(IntegerType, false) -> AverageIntArray.asInstanceOf[AverageComputerFunction[Any]],
    ArrayType(FloatType, false) -> AverageFloatArray.asInstanceOf[AverageComputerFunction[Any]],
    ArrayType(DoubleType, false) -> AverageDoubleArray.asInstanceOf[AverageComputerFunction[Any]]
  )
}