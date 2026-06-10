package edu.ucr.cs.bdlab.raptor

import com.esotericsoftware.kryo.Kryo
import com.esotericsoftware.kryo.io.{Input, Output}
import edu.ucr.cs.bdlab.beast.geolite.{ITile, RasterFeature, RasterMetadata}
import org.apache.commons.io.output.ByteArrayOutputStream
import org.apache.spark.test.ScalaSparkTest
import org.junit.runner.RunWith
import org.scalatest.funsuite.AnyFunSuite
import org.scalatestplus.junit.JUnitRunner

import java.awt.geom.{AffineTransform, Point2D}
import java.io.ByteArrayInputStream

@RunWith(classOf[JUnitRunner])
class SubsetTileTest extends AnyFunSuite with ScalaSparkTest {
  test("subset part of a middle tile") {
    val metadata = new RasterMetadata(0, 0, 100, 100, 10, 10, 4326,
      new AffineTransform())
    // Take a subset of tile #13
    val subsetMetadata = SubsetTile.subsetMetadata(metadata, 32, 17, 35, 19)
    assertResult(4)(subsetMetadata.rasterWidth)
    assertResult(1)(subsetMetadata.numTiles)
    val outpoint = new Point2D.Double()
    subsetMetadata.gridToModel(1.5, 2.5, outpoint)
    assert((outpoint.x - 33.5).abs < 0.01)
    assert((outpoint.y - 19.5).abs < 0.01)
  }

  test("subset tile with integer values") {
    val metadata = new RasterMetadata(0, 0, 100, 100, 10, 5, 4326,
      new AffineTransform())
    val tile: MemoryTile[Int] = new MemoryTile(31, metadata, RasterFeature.create(Array("fileName"), Array("testFile.tif")))
    println(tile)
    tile.setPixelValue(13, 17, 100)
    tile.setPixelValue(15, 18, 200)

    val subsetTile = new SubsetTile(tile, 12, 16, 13, 19)
    assertResult(2)(subsetTile.tileWidth)
    assertResult(4)(subsetTile.tileHeight)
    assert(subsetTile.isEmpty(0, 0))
    assert(subsetTile.isDefined(1, 1))
    assert(subsetTile.isEmpty(3, 2)) // Because it's out of range
    assertResult(100)(subsetTile.getPointValue(13.5, 17.5))
  }

}

