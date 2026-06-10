package edu.ucr.cs.bdlab.raptor

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
class ReduceNNTileIterator[T](iter: Iterator[(Int, MemoryTile[T])]) extends Iterator[(Int, MemoryTile[T])] {

  /** The tile currently being processed */
  var currentTile: (Int, MemoryTile[T]) = _

  /** The current tile ID */
  var currentTileID: Int = -1

  /** The tuple that will be returned when next is called */
  var nextTuple: (Int, MemoryTile[T]) = _

  /** A flag that is raised when end-of-file is reached */
  var eof: Boolean = false

  /** A flag */
  var fromBeginning: Boolean = true

  /**
   * Prefetches the next tuple and returns it. If end-of-file is reached, this function will return null
   *
   * @return the next record or null if end-of-file is reached
   */
  private def prefetchNext: (Int, MemoryTile[T]) = {
    var mergeTile: MemoryTile[T] = null
    while (iter.hasNext) {
      if (fromBeginning) {
        while (currentTile == null || currentTile._1 < currentTileID) {
          assert(iter.hasNext, "Could not locate a tile that has intersections")
          currentTile = iter.next()
        }
        fromBeginning = false
        mergeTile = currentTile._2
      }
      val nextTuple = if (iter.hasNext) iter.next() else null
      if (nextTuple == null) {
        return (currentTileID, mergeTile)
      }
      if (nextTuple != null && nextTuple._1 == currentTileID) {
        // Same key: merge into mergeTile.
        for ((x, y) <- nextTuple._2.pixelLocations) {
          if (nextTuple._2.isDefined(x, y)) {
            mergeTile.setPixelValue(x, y, nextTuple._2.getPixelValue(x, y))
          }
        }
        // Return the merged tile (mergeTile is updated in place)
        mergeTile
      }
      else {
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

  override def next(): (Int,MemoryTile[T]) = {
    val toReturn = nextTuple
    nextTuple = prefetchNext
    toReturn
  }

}