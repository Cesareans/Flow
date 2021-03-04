# coding=utf-8
STREAM_ENDIAN = '<'

# 这是一个数据包的封包信息，使用的方法是length field based
# | 0x1a 0x2b 0x3d 0x4c | 0x01    | 0x01            | '<'    | 0x00 0x00    | 0x00 0x00 0x00 0x00 | ...        |
# |   Magic Number      | Version | Serializer Type | Endian | Content Type |     Content Size    | Content    |
# |                         Meta Prefix(7)                   |          Content Prefix(6)         | Payload    |
# |                                          Prefix(13)                                           | Packet     |
MAGIC_NUMBER = '\x1a\x2b\x3d\x4c'
VERSION = 1

MAGIC_NUMBER_LENGTH = 4
VERSION_LENGTH = 1
SERIALIZER_TYPE_LENGTH = 1
ENDIAN_LENGTH = 1

META_PREFIX_LENGTH = 7

CONTENT_TYPE_LENGTH = 2
CONTENT_SIZE_LENGTH = 4

CONTENT_PREFIX_LENGTH = 6

PREFIX_LENGTH = 13

VersionFmt = STREAM_ENDIAN + 'B'
SerializerFmt = STREAM_ENDIAN + 'B'
EndianFmt = STREAM_ENDIAN + 'c'
PacketTypeFmt = STREAM_ENDIAN + 'H'
PacketSizeFmt = STREAM_ENDIAN + 'I'
