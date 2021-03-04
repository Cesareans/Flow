# coding=utf-8

from packet.inbound.inbound_packet import InboundPacket, InboundPacketCategory
from packet.inbound.inbound_packet_type_id import InboundPacketTypeId


class UpdateConfigFile(InboundPacket):
    CATEGORY = InboundPacketCategory.UpdateConfigFile


class AskMd5(UpdateConfigFile):
    TYPE_ID = InboundPacketTypeId.AskMd5


class AskFile(UpdateConfigFile):
    TYPE_ID = InboundPacketTypeId.AskFile

    def __init__(self, data):
        super(AskFile, self).__init__()
        self.fileNames = data["fileNames"]
