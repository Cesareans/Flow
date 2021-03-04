# coding=utf-8

from packet.outbound.outbound_packet import OutboundPacket
from packet.outbound.outbound_packet_type_id import OutboundPacketTypeId


class FileMD5s(OutboundPacket):
    TYPE_ID = OutboundPacketTypeId.FileMD5

    def __init__(self, md5List):
        super(FileMD5s, self).__init__()
        self.md5List = md5List


class FileContent(OutboundPacket):
    TYPE_ID = OutboundPacketTypeId.FileContent

    def __init__(self, name, content, end):
        super(FileContent, self).__init__()
        self.name = name
        self.content = content
        self.isEnd = end
