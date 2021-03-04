# coding=utf-8

import struct

import network.codec.codec_config as PacketConfig
from common.singleton import Singleton


# 这个类是为了在字节流里面取出我们一个数据包所封装出来的序列帧
# =》 取得我们做了序列化后的字节流
class FrameCodec(object):
    __metaclass__ = Singleton

    def __init__(self):
        pass

    def decode(self, data):
        if len(data) < PacketConfig.PREFIX_LENGTH:
            return data, None
        prefix = data[:PacketConfig.META_PREFIX_LENGTH]
        magicNumber = prefix[0:PacketConfig.MAGIC_NUMBER_LENGTH]
        if magicNumber != PacketConfig.MAGIC_NUMBER:
            # todo: raise exception or should find magic number
            return data, None
        prefix = prefix[PacketConfig.MAGIC_NUMBER_LENGTH:]
        version = struct.unpack(PacketConfig.VersionFmt, prefix[0:PacketConfig.VERSION_LENGTH])
        if len(version) == 0 or version[0] != PacketConfig.VERSION:
            # todo: raise exception
            return data, None

        content = data[PacketConfig.META_PREFIX_LENGTH:]  # skip meta prefix
        packetSize = struct.unpack(PacketConfig.PacketSizeFmt,
                                   content[PacketConfig.CONTENT_TYPE_LENGTH:PacketConfig.CONTENT_PREFIX_LENGTH])[0]

        frameSize = PacketConfig.PREFIX_LENGTH + packetSize
        if len(data) >= frameSize:
            frame = data[:frameSize]
            data = data[frameSize:]
            return data, frame
        return data, None
