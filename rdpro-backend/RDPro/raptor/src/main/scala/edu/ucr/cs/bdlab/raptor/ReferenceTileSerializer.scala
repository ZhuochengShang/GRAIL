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

import com.esotericsoftware.kryo.io.{Input, Output}
import com.esotericsoftware.kryo.{Kryo, Serializer}
import edu.ucr.cs.bdlab.beast.geolite.{ITileSerializer, RasterFeature, RasterMetadata}
import edu.ucr.cs.bdlab.beast.util.BitArray

import java.io.{ByteArrayInputStream, ByteArrayOutputStream, ObjectInputStream, ObjectOutputStream}
import java.util.zip.{DeflaterOutputStream, InflaterInputStream}

/**
 * A Kryo serialize/deserializer for [[ConvolutionTileSingleBand]] and [[ConvolutionTileMultiBand]]
 */
class ReferenceTileSerializer extends Serializer[ReferenceTile[Any]] {
  override def write(kryo: Kryo, output: Output, tile: ReferenceTile[Any]): Unit = {
    output.writeInt(tile.tileID)
    kryo.writeObject(output, tile.rasterMetadata)
    kryo.writeObject(output, tile.rasterFeature)
  }

  override def read(kryo: Kryo, input: Input, cls: Class[ReferenceTile[Any]]): ReferenceTile[Any] = {
    val tileID = input.readInt()
    val metadata = kryo.readObject(input, classOf[RasterMetadata])
    val feature = kryo.readObject(input, classOf[RasterFeature])
    new ReferenceTile[Any](tileID, metadata, feature)
  }
}
