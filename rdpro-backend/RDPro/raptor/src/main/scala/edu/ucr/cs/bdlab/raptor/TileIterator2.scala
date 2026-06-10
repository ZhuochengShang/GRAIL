package edu.ucr.cs.bdlab.raptor

import edu.ucr.cs.bdlab.beast.geolite.ITile
import org.apache.spark.util.LongAccumulator

/**
 * Converts a list of intersections and a list of tiles to a list of pixel values in the following format:
 * 1. Long: The feature (or geometry) ID
 * 2. RasterMetadata: the metadata of the raster file
 * 3. Int: x-coordinate
 * 4. Int: y-coordinate
 * 5. T: pixel value as provided in the raster data
 * Both inputs should be sorted on the key (RasterTileID) which is a concatenation of the raster file ID
 * in the most significant 32 bits and tile ID is the least significant 32 bits.
 * @param intersections an iterator of intersections in the following format
 *                      (RasterTileID, (GeometryID, Y, X1, X2))
 * @param tiles a list of (RasterTileID, ITile) pairs sorted by the key
 */
class TileIterator2[T](mergeIterator: MergeTileIterator[T])extends Iterator[ReshapeTile[T]] {

  override def hasNext: Boolean = mergeIterator.hasNext

  override def next(): ReshapeTile[T] = {
    // Extract only the merged ReshapeTile from the (key, value) pair.
    mergeIterator.next()._2
  }

}
