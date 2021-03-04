# coding=utf-8
# @Time : 2020/8/26 16:21
# @Author : 胡泽勇
#

from base.concept import Property

from packet.inbound.inbound_packet import InboundPacket
from packet.inbound.inbound_packet_type_id import InboundPacketCategory, InboundPacketTypeId


class MetaPacket(InboundPacket):
    CATEGORY = InboundPacketCategory.Meta


class ReloadPacket(MetaPacket):
    TYPE_ID = InboundPacketTypeId.Reload


class QuickGame(MetaPacket):
    TYPE_ID = InboundPacketTypeId.QuickGame
    characterId = Property(int, required=True)
