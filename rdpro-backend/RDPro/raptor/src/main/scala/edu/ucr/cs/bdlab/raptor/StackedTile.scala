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

import edu.ucr.cs.bdlab.beast.geolite.ITile
import org.apache.spark.sql.Row
import org.apache.spark.sql.types.{DataType}

import scala.reflect.ClassTag

/**
 * A tile that consists of several tiles stacked on top of each other.
 * All the stacked tiles must have the same ID and the same metadata which this tile will inherit.
 */
// TODO concatenate all raster features
class StackedTile[T](tiles: ITile[_]*)(implicit t: ClassTag[T])
  extends ITile[Array[T]](tiles.head.tileID, tiles.head.rasterMetadata, tiles.head.rasterFeature) {

  // TODO combine all the schemas of tiles in the same order
  // override def schema: StructType = super.schema

  // Make sure that all tiles have the same tile ID and metadata
  require(tiles.forall(_.tileID == tileID), "Cannot stack tiles with different IDs")
  require(tiles.forall(_.rasterMetadata == rasterMetadata), "Cannot stack tiles with different metadata")

  private def simpleTypeName(rawTypeName: String): String = rawTypeName match {
    case "[B" => "Array[Byte]"
    case "[S" => "Array[Short]"
    case "[I" => "Array[Int]"
    case "[J" => "Array[Long]"
    case "[F" => "Array[Float]"
    case "[D" => "Array[Double]"
    case s if s.startsWith("[L") && s.endsWith(";") =>
      s"Array[${simpleTypeName(s.substring(2, s.length - 1))}]"
    case "java.lang.Byte" => "Byte"
    case "java.lang.Short" => "Short"
    case "java.lang.Integer" => "Int"
    case "java.lang.Long" => "Long"
    case "java.lang.Float" => "Float"
    case "java.lang.Double" => "Double"
    case other => other.split('.').lastOption.getOrElse(other)
  }

  private def assignOrThrow(outVal: Array[T], i: Int, v: Any, tile: ITile[_], x: Int, y: Int): Unit = {
    try {
      outVal(i) = v.asInstanceOf[T]
    } catch {
      case cce: ClassCastException =>
        val actualType = if (v == null) "null" else simpleTypeName(v.getClass.getName)
        val expectedType = simpleTypeName(t.runtimeClass.getName)
        val scalarTarget = expectedType match {
          case "Byte" => "Byte"
          case "Short" => "Short"
          case "Int" => "Int"
          case "Long" => "Long"
          case "Float" => "Float"
          case "Double" => "Double"
          case s if s.startsWith("Array[") && s.endsWith("]") => s.substring(6, s.length - 1)
          case _ => "Float"
        }
        val conversionExpr =
          if (expectedType.startsWith("Array[")) s"vs => vs.map(_.to$scalarTarget)"
          else s"v => v.to$scalarTarget"
        val fixCode =
          s"Fix: convert inputs before overlay, e.g. val rC = r.mapPixels($conversionExpr)"
        val hint =
          s"Overlay type mismatch: $actualType cannot be cast to $expectedType " +
            s"(tileID=$tileID, x=$x, y=$y, sourceComponentType=${tile.componentType}). $fixCode"
        throw new RuntimeException(hint, cce)
    }
  }

  override def getPixelValue(x: Int, y: Int): Array[T] = {
    val outVal = new Array[T](numComponents)
    var i = 0
    tiles.foreach(tile => tile.getPixelValue(x, y) match {
      case vs: Array[_] =>
        for (v <- vs) {
          assignOrThrow(outVal, i, v, tile, x, y)
          i += 1
        }
      case v: Any =>
        assignOrThrow(outVal, i, v, tile, x, y)
        i += 1
    })
    outVal
  }

  /**
   * A pixel in a stacked tile is empty if any of the underlying tiles is empty
   * @param i the index of the column
   * @param j the index of the row
   *  @return `true` if this pixel is empty in any of the stacked tiles. `false` if at least one is empty.
   */
  override def isEmpty(i: Int, j: Int): Boolean = {
    for (t <- tiles)
      if (t.isEmpty(i, j))
        return true
    false
  }

  // 1) compute the largest single-tile component count
  private val maxPerTile: Int = tiles.map(_.numComponents).max

  // 2) total components = maxPerTile * number of tiles
  override val numComponents: Int = maxPerTile * tiles.size

  //override val numComponents: Int = tiles.map(_.numComponents).sum

  override def componentType: DataType = tiles.head.componentType

  override def copy(): Row = ???

}
