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
import edu.ucr.cs.bdlab.beast.geolite.{ITile, ITileSerializer, RasterMetadata}
import org.apache.spark.sql.Row
import org.apache.spark.sql.types.DataType

import java.awt.geom.AffineTransform

/**
 * A tile that keeps only a subset of values in a predefined rectangular region.
 * All other values are set to empty. It also trims the tile around the predefined region.
 */
@DefaultSerializer(classOf[ITileSerializer[Any]])
class SubsetTile[T](tile: ITile[T], x1: Int, y1: Int, x2: Int, y2: Int)
  extends ITile[T](0, SubsetTile.subsetMetadata(tile.rasterMetadata, x1, y1, x2, y2), tile.rasterFeature) {

  // Note that the given coordinates are based on the subset so they are shifted from the underlying tile coordinates
  override def getPixelValue(i: Int, j: Int): T = tile.getPixelValue(i + x1, j + y1)

  override def isEmpty(i: Int, j: Int): Boolean = {
    // Note that the given coordinates are based on the subset so they are shifted from the underlying tile coordinates
    i < 0 || i > (x2 - x1) || j < 0 || j > (y2 - y1) || tile.isEmpty(i + x1, j + y1)
  }

  override def numComponents: Int = tile.numComponents

  override def componentType: DataType = tile.componentType

  override def copy(): Row = ???

}

object SubsetTile {
  def subsetMetadata(metadata: RasterMetadata, x1: Int, y1: Int, x2: Int, y2: Int): RasterMetadata = {
    val g2m = metadata.g2m.clone().asInstanceOf[AffineTransform]
    g2m.concatenate(AffineTransform.getTranslateInstance(x1 - metadata.x1, y1 - metadata.y1))
    new RasterMetadata(0, 0, x2 - x1 + 1, y2 - y1 + 1, x2 - x1 + 1, y2 - y1 + 1, metadata.srid, g2m)
  }
}
