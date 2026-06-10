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

import com.esotericsoftware.kryo.DefaultSerializer
import edu.ucr.cs.bdlab.beast.geolite.{ITile, ITileSerializer, RasterFeature, RasterMetadata}
import org.apache.spark.sql.Row
import org.apache.spark.sql.types.DataType
import org.opengis.referencing.operation.MathTransform

import scala.reflect.ClassTag

/**
 * A tile that filters the values of another tile according to a filter function
 */
@DefaultSerializer(classOf[ITileSerializer[Any]])
class LazyNNTile[T](
                     override val tileID: Int,
                     override val rasterMetadata: RasterMetadata,
                     override val rasterFeature: RasterFeature,
                     val sourceTileID: Int,
                     val targetToSource: MathTransform,
                     val sourceTileMetadata: RasterMetadata
                   )(implicit ct: ClassTag[T]) extends ITile[T](tileID, rasterMetadata, rasterFeature) {

  @transient private var resolved: MemoryTile[T] = _
  private var _sourceLoader: () => ITile[T] = _
  private val allSources = new scala.collection.mutable.ListBuffer[() => ITile[T]]()

  def setSourceLoader(loader: () => ITile[T]): Unit = {
    _sourceLoader = loader
    allSources += loader
  }

  def addSource(other: LazyNNTile[T]): Unit = {
    allSources ++= other.allSources
  }

  private def compute(): MemoryTile[T] = {
    val tile = new MemoryTile[T](tileID, rasterMetadata, rasterFeature)
    val sourceTile = _sourceLoader()
    var empty = true

    for (y <- tile.y1 to tile.y2; x <- tile.x1 to tile.x2) {
      val targetPoint = Array[Double](x + 0.5, y + 0.5)
      targetToSource.transform(targetPoint, 0, targetPoint, 0, 1)
      val sourceX = targetPoint(0).toInt
      val sourceY = targetPoint(1).toInt

      if (sourceTile.isDefined(sourceX, sourceY)) {
        tile.setPixelValue(x, y, sourceTile.getPixelValue(sourceX, sourceY))
        empty = false
      }
    }
    if (empty) null else tile
  }

  def resolve(): MemoryTile[T] = {
    if (resolved == null) resolved = compute()
    resolved
  }

  override def getPixelValue(i: Int, j: Int): T = resolve().getPixelValue(i, j)
  override def isDefined(i: Int, j: Int): Boolean = resolve().isDefined(i, j)
  override def isEmpty(i: Int, j: Int): Boolean = resolve().isEmpty(i, j)
  override def isPixelInRange(i: Int, j: Int): Boolean = resolve().isPixelInRange(i, j)
  override def numComponents: Int = resolve().numComponents
  override def componentType: DataType = resolve().componentType
  override def copy(): Row = resolve().copy()
}
