# coding=utf-8
# @Time : 2020/8/18 15:53
# @Author : 胡泽勇
#

from base.concept import Property
from packet.inbound.inbound_packet import InboundPacket
from packet.inbound.inbound_packet_type_id import InboundPacketCategory, InboundPacketTypeId


class PickOperation(InboundPacket):
    CATEGORY = InboundPacketCategory.PickOperation


class EnterPick(PickOperation):
    """
    开始匹配
    """
    TYPE_ID = InboundPacketTypeId.EnterPick


class PickCharacter(PickOperation):
    """
    开始匹配
    """
    TYPE_ID = InboundPacketTypeId.PickCharacter
    characterId = Property(int, required=True)


class ConfirmPick(PickOperation):
    """
    取消匹配
    """
    TYPE_ID = InboundPacketTypeId.ConfirmPick
