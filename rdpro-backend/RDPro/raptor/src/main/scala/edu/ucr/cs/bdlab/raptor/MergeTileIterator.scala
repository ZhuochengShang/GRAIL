package edu.ucr.cs.bdlab.raptor

import edu.ucr.cs.bdlab.beast.geolite.ITile

import scala.reflect.ClassTag

/**
 * Converts a list of intersections and a list of tiles to a list of pixel values in the following format:
 * 1. Long: The feature (or geometry) ID
 * 2. RasterMetadata: the metadata of the raster file
 * 3. Int: x-coordinate
 * 4. Int: y-coordinate
 * 5. T: pixel value as provided in the raster data
 * Both inputs should be sorted on the key (RasterTileID) which is a concatenation of the raster file ID
 * in the most significant 32 bits and tile ID is the least significant 32 bits.
 *
 * @param intersections an iterator of intersections in the following format
 *                      (RasterTileID, (GeometryID, Y, X1, X2))
 * @param tiles a list of (RasterTileID, ITile) pairs sorted by the key
 */
class MergeTileIterator[T](iter: Iterator[(Long, ReshapeTile[T])]) extends Iterator[(Long, ReshapeTile[T])] {
  var currentCountTile = 0
  /** The tile currently being processed */
  var currentTile: (Long, ReshapeTile[T]) = _

  /** The current tile ID */
  var currentTileID: Long = -1

  /** The tuple that will be returned when next is called */
  var nextTuple: (Long, ReshapeTile[T]) = _

  /** A flag that is raised when end-of-file is reached */
  var eof: Boolean = false

  /** A flag */
  var fromBeginning: Boolean = true

  /**
   * Prefetches the next tuple and returns it. If end-of-file is reached, this function will return null
   *
   * @return the next record or null if end-of-file is reached
   */
  private def prefetchNext: (Long, ReshapeTile[T]) = {
    var mergeTile: ReshapeTile[T] = null
    while (iter.hasNext) {
      if (fromBeginning) {
        while (currentTile == null || currentTile._1 < currentTileID) {
          assert(iter.hasNext, "Could not locate a tile that has intersections")
          currentTile = iter.next()
        }
        fromBeginning = false
        mergeTile = currentTile._2
        currentCountTile = 0
      }
      val nextTuple = if (iter.hasNext) iter.next() else null
      if (nextTuple == null) {
        println(s"current tile $currentTileID maps to $currentCountTile tiles")
        currentCountTile = 0
        return (currentTileID, mergeTile)
      }
      if (nextTuple != null && nextTuple._1 == currentTileID) {
        // Same key: merge into mergeTile.
        mergeTile = mergeTile.merge(nextTuple._2)
        currentCountTile += 1
      }
      else {
        println(s"current tile $currentTileID maps to $currentCountTile tiles")
        currentCountTile = 0
        // A new key is encountered: update currentTile/currentTileID and flag for the next group.
        currentTile = nextTuple
        currentTileID = nextTuple._1
        fromBeginning = true
        // Return the merged tile for the current group.
        return (currentTileID, mergeTile)
      }
    }
    // End-of-file reached
    null
  }

  nextTuple = prefetchNext

  override def hasNext: Boolean = nextTuple != null

  override def next(): (Long,ReshapeTile[T]) = {
    val toReturn = nextTuple
    nextTuple = prefetchNext
    toReturn
  }

}