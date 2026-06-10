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

import edu.ucr.cs.bdlab.beast.cg.SpatialDataTypes.RasterRDD
import edu.ucr.cs.bdlab.beast.geolite.ITile
import org.apache.spark.api.java.JavaRDD.fromRDD
import org.apache.spark.{HashPartitioner, Partition, Partitioner, TaskContext}
import org.apache.spark.rdd.{CoGroupedRDD, RDD}

import scala.annotation.varargs
import scala.collection.mutable
import scala.reflect.ClassTag

/**
 * Raster local operations
 */
object RasterOperationsLocal {
  val NoDataValue: RasterVectorOperations.NoDataValue.type = RasterVectorOperations.NoDataValue
  val NODATA: RasterVectorOperations.NoDataValue.type = RasterVectorOperations.NoDataValue
  val nodata: RasterVectorOperations.NoDataValue.type = RasterVectorOperations.NoDataValue
  val noDataType: RasterVectorOperations.NoDataValue.type = RasterVectorOperations.NoDataValue
  val noDataValue: RasterVectorOperations.NoDataValue.type = RasterVectorOperations.NoDataValue
  object MaskOptions {
    val Default: RasterVectorOperations.NoDataValue.type = RasterVectorOperations.NoDataValue
  }
  val DEFAULT_MASK_OPTIONS: RasterVectorOperations.NoDataValue.type = RasterVectorOperations.NoDataValue
  val defaultMaskOptions: RasterVectorOperations.NoDataValue.type = RasterVectorOperations.NoDataValue
  val MASK_OPTIONS: RasterVectorOperations.NoDataValue.type = RasterVectorOperations.NoDataValue
  val cropMaskOptions: RasterVectorOperations.NoDataValue.type = RasterVectorOperations.NoDataValue

  private def typeName[T: ClassTag]: String =
    implicitly[ClassTag[T]].runtimeClass.getTypeName

  private def partitionerInfo(rdd: RDD[_]): String =
    rdd.partitioner.map(_.toString).getOrElse("None")

  private def requireOp(condition: Boolean, op: String, message: => String): Unit =
    require(condition, s"[$op] $message")

  /**
   * Apply a user-defined function for each pixel in the input raster to produce the output raster
   * @param inputRaster the input raster RDD
   * @param f the function to apply on each input pixel value to produce the output pixel value
   * @tparam T the type of pixels in the input
   * @tparam U the type of pixels in the output
   * @return the resulting RDD
   */
  def mapPixels[T: ClassTag, U: ClassTag](inputRaster: RasterRDD[T], f: T => U): RasterRDD[U] =
    {
      requireOp(f != null, "mapPixels", s"mapping function must be non-null (T=${typeName[T]}, U=${typeName[U]})")
      inputRaster.map { inputTile =>
        try {
          new MapPixelsTile(inputTile, f)
        } catch {
          case t: Throwable =>
            throw new IllegalArgumentException(
              s"[mapPixels] Failed to create mapped tile for tileID=${inputTile.tileID} " +
                s"(T=${typeName[T]}, U=${typeName[U]}): ${t.getMessage}",
              t
            )
        }
      }
    }
  def mapPixelsPreservePartitioner[T: ClassTag, U: ClassTag](
                                                              inputRaster: RasterRDD[T],
                                                              f: T => U
                                                            ): RasterRDD[U] = {
    requireOp(
      f != null,
      "mapPixelsPreservePartitioner",
      s"mapping function must be non-null (T=${typeName[T]}, U=${typeName[U]})"
    )
    inputRaster.mapPartitions(
      iter => iter.map { tile =>
        try {
          new MapPixelsTile(tile, f)
        } catch {
          case t: Throwable =>
            throw new IllegalArgumentException(
              s"[mapPixelsPreservePartitioner] Failed to create mapped tile for tileID=${tile.tileID} " +
                s"(T=${typeName[T]}, U=${typeName[U]}): ${t.getMessage}",
              t
            )
        }
      },
      preservesPartitioning = true
    )
  }
  def mapPixelsPreservePartitionerKeyed[T: ClassTag, U: ClassTag](
                                                                   input: RDD[(Int, ITile[T])],
                                                                   f: T => U
                                                                 ): RDD[(Int, ITile[U])] = {
    requireOp(
      f != null,
      "mapPixelsPreservePartitionerKeyed",
      s"mapping function must be non-null (T=${typeName[T]}, U=${typeName[U]})"
    )
    input.mapPartitions(
      iter => iter.map { case (id, tile) =>
        try {
          // Wrap the existing ITile[T] in a MapPixelsTile[T,U]
          (id, new MapPixelsTile(tile, f))
        } catch {
          case t: Throwable =>
            throw new IllegalArgumentException(
              s"[mapPixelsPreservePartitionerKeyed] Failed for key=$id tileID=${tile.tileID} " +
                s"(T=${typeName[T]}, U=${typeName[U]}): ${t.getMessage}",
              t
            )
        }
      },
      preservesPartitioning = true
    )
  }

  def mapPixelsPreservePartitionerKeyedEager[T: ClassTag, U: ClassTag](
                                                                        input: RDD[(Int, ITile[T])],
                                                                        f: T => U
                                                                      ): RDD[(Int, ITile[U])] = {
    requireOp(
      f != null,
      "mapPixelsPreservePartitionerKeyedEager",
      s"mapping function must be non-null (T=${typeName[T]}, U=${typeName[U]})"
    )
    input.mapPartitions(
      iter => iter.map { case (id, tile) =>
        try {
          // wrap + force materialization
          val eagerTile: ITile[U] = new MapPixelsTile(tile, f).forceEager()
          (id, eagerTile)
        } catch {
          case t: Throwable =>
            throw new IllegalArgumentException(
              s"[mapPixelsPreservePartitionerKeyedEager] Failed for key=$id tileID=${tile.tileID} " +
                s"(T=${typeName[T]}, U=${typeName[U]}): ${t.getMessage}",
              t
            )
        }
      },
      preservesPartitioning = true
    )
  }

  /**
   * Retains only the pixels that pass the user-defined filter and clears all other pixels (set to empty)
   * @param inputRaster the input raster
   * @param filter the filter function that tells which pixel values to keep in the output
   * @tparam T the thpe of the pixels in the input
   * @return a new raster where only pixels that pass the test are retained
   */
  def filterPixels[T: ClassTag](inputRaster: RasterRDD[T], filter: T => Boolean): RasterRDD[T] =
    {
      requireOp(
        filter != null,
        "filterPixels",
        s"filter function must be non-null (T=${typeName[T]})"
      )
      inputRaster.map { inputTile =>
        try {
          new FilterTile(inputTile, filter)
        } catch {
          case t: Throwable =>
            throw new IllegalArgumentException(
              s"[filterPixels] Failed to create filter tile for tileID=${inputTile.tileID} " +
                s"(T=${typeName[T]}): ${t.getMessage}",
              t
            )
        }
      }
    }

  /**
   * Overlays two raster layers that have equivalent metadata.
   * If the inputs are not compatible, i.e., with different metadata, this function fails early with a clear error.
   * An output pixel is defined if the corresponding inputs in the two rasters are both defined.
   * In that case, the pixel value is the concatenation of both values.
   * @param inputs the RDDs to overlay
   * @return a raster with the same metadata of the inputs where output pixels are the concatenation of input pixels.
   */
  def overlay[T: ClassTag, V](@varargs inputs: RDD[ITile[T]]*)
                                               (implicit v: ClassTag[V]): RasterRDD[Array[V]] = {
    requireOp(inputs.nonEmpty, "overlay", s"requires at least one input raster (T=${typeName[T]}, V=${v.runtimeClass.getTypeName})")
    if (inputs.length > 1) {
      val firstTileOpt = inputs.head.take(1).headOption
      requireOp(firstTileOpt.nonEmpty, "overlay", s"input[0] is empty; cannot validate metadata (T=${typeName[T]})")
      val baseMeta = firstTileOpt.get.rasterMetadata
      for ((input, idx) <- inputs.zipWithIndex.drop(1)) {
        val tileOpt = input.take(1).headOption
        requireOp(tileOpt.nonEmpty, "overlay", s"input[$idx] is empty; cannot validate metadata (T=${typeName[T]})")
        val currentMeta = tileOpt.get.rasterMetadata
        requireOp(
          currentMeta == baseMeta,
          "overlay",
          s"overlay metadata mismatch between input[0] and input[$idx]. " +
            s"T=${typeName[T]}, input[0]=$baseMeta, input[$idx]=$currentMeta. " +
            s"Fix: align input[$idx] first, e.g. " +
            s"val targetMeta = inputs.head.take(1).head.rasterMetadata; " +
            s"val input${idx}Aligned = RasterOperationsFocal.reshapeNN(inputs($idx), _ => targetMeta)"
        )
      }
    }
    val inputsByID: Seq[RDD[(Int, ITile[T])]] = inputs.map(i => i.map(t => (t.tileID, t)))
    val partitioner = Partitioner.defaultPartitioner(inputsByID.head, inputsByID:_*)
    val grouped: CoGroupedRDD[Int] = new CoGroupedRDD(inputsByID, partitioner)
    grouped.map(ts => {
      val tiles: Array[ITile[T]] = ts._2.flatMap(x => x.map(_.asInstanceOf[ITile[T]]))
      new StackedTile[V](tiles:_*)
    })
  }

  /**
   * Zip two *array‐band* streams, stacking their bands into a single tile.
   * Precondition: a.partitioner == b.partitioner == Some(part).
   */
  def zipTwoArrays[T: ClassTag](
                                 a: RDD[ITile[Array[T]]],
                                 b: RDD[ITile[Array[T]]]
                               ): RDD[ITile[Array[T]]] = {
    a.zipPartitions(b, preservesPartitioning = true) { (ita, itb) =>
      // Build a lookup from A’s tiles by ID
      val m = mutable.Map.empty[Int, ITile[Array[T]]]
      ita.foreach(t => m(t.tileID) = t)

      // For each tile in B, if A has the same ID, stack them
      itb.flatMap { tB =>
        m.get(tB.tileID).map { tA =>
          // This only allocates when you eventually call tile.toArray()
          new StackedTile[T](tA, tB)
        }
      }
    }
  }

  /**
   * Overlay N array‐band streams by folding `zipTwoArrays` over them.
   * Any tileID missing in any stream is pruned out.
   */
  def overlayArrayStreams[T: ClassTag](
                                        streams: RDD[(Int,ITile[Array[T]])]*
                                      ): RDD[(Int, ITile[Array[T]])] = {
    // 1) Check they all share the same Partitioner
    val parts = streams.map(_.partitioner)
    requireOp(
      parts.distinct.size == 1 && parts.head.isDefined,
      "overlayArrayStreams",
      s"All streams must share the same defined Partitioner (T=${typeName[T]}). " +
        s"Observed partitioners=${parts.map(_.map(_.toString).getOrElse("None")).mkString("[", ", ", "]")}"
    )
    val part = parts.head.get

    // 2) Zip-fold across them pairwise, pruning missing IDs
    //    We start with the first stream's pairs, then merge in each subsequent one.
    val head: RDD[(Int, ITile[Array[T]])] = streams.head
    val mergedPairs: RDD[(Int, ITile[Array[T]])] =
      streams.tail.foldLeft(head) { (accPairs, nextPairs) =>
        // zipPartitions on two PairRDDs gives you two iterators of (key,tile)
        accPairs.zipPartitions(nextPairs, preservesPartitioning = true) { (ita, itb) =>
          // Build a mutable map: tileID → tile from A
          val acc = mutable.Map.empty[Int, ITile[Array[T]]]
          ita.foreach { case (id, tileA) =>
            acc(id) = tileA
          }

          // For each tile in B, if A had the same ID, keep it; otherwise drop
          itb.flatMap { case (id, tileB) =>
            acc.remove(id).map { tileA =>
              // tileID=id, and stack A & B into one multi-band tile
              val stacked = new StackedTile[T](tileA, tileB)
              (id, stacked)
            }
          }
        }
      }

    // 3) Now mergedPairs has exactly the intersection of all tileIDs,
    //    each paired with one StackedTile[Array[T]] whose numComponents = sum of bands.
    //    We just drop the key and return the RasterRDD.
    mergedPairs
  }

  def overlayArrayStreamsF[T: ClassTag](
                                         streams: RDD[(Int, ITile[T])]*
                                       ): RDD[(Int, ITile[Array[T]])] = {
    requireOp(streams.nonEmpty, "overlayArrayStreamsF", s"At least one input stream is required (T=${typeName[T]})")
    val parts = streams.map(_.partitioner).distinct
    requireOp(
      parts.size == 1 && parts.head.isDefined,
      "overlayArrayStreamsF",
      s"All inputs must share the same defined Partitioner (T=${typeName[T]}). " +
        s"Observed partitioners=${parts.map(_.map(_.toString).getOrElse("None")).mkString("[", ", ", "]")}"
    )
    val part = parts.head.get

    // 1) Wrap the first stream’s tiles in a StackedTile
    val head: RDD[(Int, ITile[Array[T]])] = streams.head.mapValues { tile =>
      new StackedTile[T](tile)
    }

    // 2) Iteratively zip in each additional stream
    val combined: RDD[(Int, ITile[Array[T]])] = streams.tail.foldLeft(head) {
      (acc, next) =>
        acc.zipPartitions(next, preservesPartitioning = true) { (accIt, nextIt) =>
          // build an in‐partition map of id→stackedTile
          val accMap = scala.collection.mutable.Map.empty[Int, ITile[Array[T]]]
          accIt.foreach { case (id, stacked) => accMap(id) = stacked }

          // for each (id,tileB) pair, combine with its stackedA
          nextIt.flatMap { case (id, tileB) =>
            accMap.remove(id).map { stackedA =>
              (id, new StackedTile[T](stackedA, tileB))
            }
          }
        }
    }

    // 3) No final shuffle needed – zipPartitions kept the partitioner intact
    combined
  }


  def overlayArrayStreamsF2[T: ClassTag](
                                          streams: RDD[(Int, ITile[Array[T]])]*
                                        ): RDD[(Int, ITile[Array[T]])] = {
    requireOp(streams.nonEmpty, "overlayArrayStreamsF2", s"At least one input stream is required (T=${typeName[T]})")

    val allParts = streams.map(_.partitioner)
    requireOp(
      allParts.forall(_.isDefined),
      "overlayArrayStreamsF2",
      s"All inputs must have a defined Partitioner (T=${typeName[T]}). " +
        s"Observed partitioners=${allParts.map(_.map(_.toString).getOrElse("None")).mkString("[", ", ", "]")}"
    )

    val firstPart = allParts.head.get
    requireOp(
      allParts.map(_.get).forall(_ == firstPart),
      "overlayArrayStreamsF2",
      s"All inputs must share the same defined Partitioner (T=${typeName[T]}). " +
        s"Expected=$firstPart, observed=${allParts.map(_.map(_.toString).getOrElse("None")).mkString("[", ", ", "]")}"
    )

    // wrap first stream
    val head = streams.head.mapValues(tile => new StackedTile[T](tile))

    // fold in the rest via zipPartitions, preserving the partitioning
    val combined = streams.tail.foldLeft(head) { (acc, next) =>
      acc.zipPartitions(next, preservesPartitioning = true) { (accIt, nextIt) =>
        val accMap = scala.collection.mutable.Map.empty[Int, ITile[Array[T]]]
        accIt.foreach { case (id, tile) => accMap(id) = tile }
        nextIt.flatMap { case (id, tileB) =>
          accMap.remove(id).map(tileA => (id, new StackedTile[T](tileA, tileB)))
        }
      }
    }

    // NO extra partitionBy – zipPartitions kept the same Partitioner already
    combined.asInstanceOf[RDD[(Int, ITile[Array[T]])]]
  }



  def overlayArrayStreams2[T: ClassTag](
                                         streams: RDD[(Int, ITile[T])]*
                                       ): RDD[(Int, ITile[Array[T]])] = {
    requireOp(streams.nonEmpty, "overlayArrayStreams2", s"At least one input RDD is required (T=${typeName[T]}).")
    requireOp(
      streams.forall(_.partitioner == streams.head.partitioner),
      "overlayArrayStreams2",
      s"All input RDDs must have the same partitioner (T=${typeName[T]}). " +
        s"Observed=${streams.zipWithIndex.map { case (s, i) => s"#$i:${partitionerInfo(s)}" }.mkString("[", ", ", "]")}"
    )

    val numStreams = streams.length
    val sharedPartitioner = streams.head.partitioner.getOrElse {
      throw new IllegalArgumentException(
        s"[overlayArrayStreams2] Input RDDs must all have a defined partitioner (T=${typeName[T]}). " +
          s"Observed=${streams.zipWithIndex.map { case (s, i) => s"#$i:${partitionerInfo(s)}" }.mkString("[", ", ", "]")}"
      )
    }

    new RDD[(Int, ITile[Array[T]])](streams.head.sparkContext, Nil) {
      override def getPartitions: Array[Partition] = streams.head.partitions
      override val partitioner: Option[Partitioner] = Some(sharedPartitioner)

      override def compute(split: Partition, context: TaskContext): Iterator[(Int, ITile[Array[T]])] = {
        val partitionIterators = streams.map(_.iterator(split, context)).toArray

        // Materialize all partition data into maps for fast key lookup
        val maps = partitionIterators.map(_.toMap)
        val commonKeys = maps.map(_.keySet).reduce(_.intersect(_))

        // Build new stacked tiles only for matching keys
        commonKeys.iterator.map { key =>
          val tiles = maps.map(_(key))
          (key, new StackedTile[T](tiles: _*))
        }
      }
    }
  }



  def overlayArrayStreams3[T: ClassTag](
                                         streams: RDD[(Int, ITile[Array[T]])]*
                                       ): RDD[(Int, ITile[Array[T]])] = {
    requireOp(streams.nonEmpty, "overlayArrayStreams3", s"At least one input RDD is required (T=${typeName[T]}).")
    requireOp(
      streams.forall(_.partitioner == streams.head.partitioner),
      "overlayArrayStreams3",
      s"All input RDDs must have the same partitioner (T=${typeName[T]}). " +
        s"Observed=${streams.zipWithIndex.map { case (s, i) => s"#$i:${partitionerInfo(s)}" }.mkString("[", ", ", "]")}"
    )

    val numStreams = streams.length
    val sharedPartitioner = streams.head.partitioner.getOrElse {
      throw new IllegalArgumentException(
        s"[overlayArrayStreams3] Input RDDs must all have a defined partitioner (T=${typeName[T]}). " +
          s"Observed=${streams.zipWithIndex.map { case (s, i) => s"#$i:${partitionerInfo(s)}" }.mkString("[", ", ", "]")}"
      )
    }

    new RDD[(Int, ITile[Array[T]])](streams.head.sparkContext, Nil) {
      override def getPartitions: Array[Partition] = streams.head.partitions
      override val partitioner: Option[Partitioner] = Some(sharedPartitioner)

      override def compute(split: Partition, context: TaskContext): Iterator[(Int, ITile[Array[T]])] = {
        val partitionIterators = streams.map(_.iterator(split, context)).toArray

        // Materialize all partition data into maps for fast key lookup
        val maps = partitionIterators.map(_.toMap)
        val commonKeys = maps.map(_.keySet).reduce(_.intersect(_))

        // Build new stacked tiles only for matching keys
        commonKeys.iterator.map { key =>
          val tiles = maps.map(_(key))
          (key, new StackedTile[T](tiles: _*))
        }
      }
    }
  }



  def overlayLargeNoShuffle[T: ClassTag, V: ClassTag](@varargs inputs: RDD[ITile[T]]*): RasterRDD[Array[V]] = {
    requireOp(
      inputs.nonEmpty,
      "overlayLargeNoShuffle",
      s"At least one input RDD is required (T=${typeName[T]}, V=${implicitly[ClassTag[V]].runtimeClass.getTypeName})."
    )

    // Validate partitioner consistency
    val firstPartitioner = inputs.head.partitioner.getOrElse {
      throw new IllegalArgumentException(
        s"[overlayLargeNoShuffle] Input RDDs must be partitioned (T=${typeName[T]}). " +
          s"input[0].partitioner=${partitionerInfo(inputs.head)}"
      )
    }
    inputs.zipWithIndex.foreach { case (rdd, idx) =>
      requireOp(
        rdd.partitioner.contains(firstPartitioner),
        "overlayLargeNoShuffle",
        s"All input RDDs must have the same partitioner (T=${typeName[T]}). " +
          s"Expected=$firstPartitioner, input[$idx]=${partitionerInfo(rdd)}"
      )
    }

    // Co-group by tileID without shuffle
    val inputsByID: Seq[RDD[(Int, ITile[T])]] = inputs.map(_.map(t => (t.tileID, t)))
    val grouped = new CoGroupedRDD(inputsByID, firstPartitioner)

    grouped.mapPartitions({ iter =>
      var count = 0
      iter.map { case (tileID, tileLists) =>
        count += 1
        if (count % 10000 == 0) {
          println(f"[OverlayPartition] Processed $count tiles, current tileID=$tileID")
        }
        val tiles: Array[ITile[T]] = tileLists.flatMap(_.asInstanceOf[Iterable[ITile[T]]]).toArray
        new StackedTile[V](tiles: _*)
      }
    }, preservesPartitioning = true)
  }



  /**
   * Returns a new RasterRDD where each tile is in its own raster.
   * @param inputRaster the raster data to explore
   * @tparam T
   * @return a new raster RDD with the same number of tiles but each tile is in a separate raster
   */
  def explode[T](inputRaster: RasterRDD[T]): RasterRDD[T] = inputRaster.map(tile => new ExplodedTile(tile))
}
