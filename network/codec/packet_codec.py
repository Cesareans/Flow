# coding=utf-8

import logging
import struct

import network.codec.codec_config as PacketConfig
from common.serializer.json_serializer import JsonSerializer
from common.singleton import Singleton
from packet.inbound.inbound_packet import InboundPacket


# 去解析之前frameCodec解析出来的序列帧
# =》 得到我们实际的数据包
class PacketCodec(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.Serializer = JsonSerializer()
        self.prefix = PacketConfig.MAGIC_NUMBER
        self.prefix += struct.pack(PacketConfig.VersionFmt, PacketConfig.VERSION)
        self.prefix += struct.pack(PacketConfig.SerializerFmt, self.Serializer.getType())
        self.prefix += struct.pack(PacketConfig.EndianFmt, PacketConfig.STREAM_ENDIAN)

    # encode outbound packet to bytes
    def encode(self, packet):
        payload = self.prefix
        payload += struct.pack(PacketConfig.PacketTypeFmt, packet.typeId)
        data = self.Serializer.serialize(packet)
        payload += struct.pack(PacketConfig.PacketSizeFmt, len(data))
        payload += data
        return payload

    # decode bytes to inbound event
    def decode(self, frame):
        # todo: 如果有需求，从数据流中获得序列化器的类型与端序做解析
        frame = frame[PacketConfig.META_PREFIX_LENGTH:]  # skip prefix
        packetTypeId = struct.unpack(PacketConfig.PacketTypeFmt, frame[:PacketConfig.CONTENT_TYPE_LENGTH])[0]
        packetContent = frame[PacketConfig.CONTENT_PREFIX_LENGTH:]
        # 通过在字节流中取出的type id取得指定的packet type
        packetType = InboundPacket.getType(packetTypeId)
        if packetType is None:
            logging.warn("Unrecognized type id {0} with content {1}! Please refer packet.inbound.__init__.py".
                         format(packetTypeId, packetContent))
            return None
        # 通过packet type去把我们得到的（字节流，type）解析成我们真正需要的数据包
        return self.Serializer.deserializeConcept(packetType, packetContent)
