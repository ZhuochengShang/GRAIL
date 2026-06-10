package edu.ucr.cs.bdlab.raptor

import com.esotericsoftware.kryo.DefaultSerializer
import edu.ucr.cs.bdlab.beast.geolite.{ITile, RasterFeature, RasterMetadata}
import edu.ucr.cs.bdlab.beast.util.BitArray
import org.apache.spark.sql.Row
import org.apache.spark.sql.types.{DataType, FloatType}

import scala.reflect.ClassTag


/**
 * A tile that holds partial answer for the convolution operator
 * @param tileID the ID of this tile in the raster metadata
 * @param metadata the raster metadata that defines the underlying raster
 * @param sourceTile the first tile to add
 * @tparam T the type of measurement values in tiles*/
@DefaultSerializer(classOf[ReferenceTileSerializer])
class ReferenceTile[T](
                        override val tileID: Int,
                        override val rasterMetadata: RasterMetadata,
                        override val rasterFeature: RasterFeature
                      )(implicit ct: ClassTag[T]) extends ITile[T](tileID, rasterMetadata, rasterFeature) {

  @transient private var resolved: ITile[T] = _
  @transient private var _loadFunc: () => ITile[T] = _

  def setLoader(loader: () => ITile[T]): Unit = {
    _loadFunc = loader
  }

  def withLoaderFrom(map: Map[Int, ITile[T]]): ReferenceTile[T] = {
    val ref = new ReferenceTile[T](tileID, rasterMetadata, rasterFeature)
    ref.setLoader(() => map(tileID))
    ref
  }
  private def resolve(): ITile[T] = {
    if (resolved eq null) {
      if (_loadFunc == null)
        throw new IllegalStateException(s"No loader set for ReferenceTile with ID=$tileID")
      resolved = _loadFunc()
    }
    resolved
  }

  override def getPixelValue(i: Int, j: Int): T = resolve().getPixelValue(i, j)
  override def isDefined(i: Int, j: Int): Boolean = resolve().isDefined(i, j)
  override def isPixelInRange(i: Int, j: Int): Boolean = resolve().isPixelInRange(i, j)
  override def isEmpty(i: Int, j: Int): Boolean = resolve().isEmpty(i, j)
  override def numComponents: Int = resolve().numComponents
  override def componentType: DataType = resolve().componentType
  override def copy(): Row = resolve().copy()
}
