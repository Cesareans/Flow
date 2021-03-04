# coding=utf-8
# @Time : 2020/8/18 11:52
# @Author : 胡泽勇
#

from packet.inbound.inbound_packet import InboundPacket
from packet.inbound.inbound_packet_type_id import InboundPacketCategory, InboundPacketTypeId


class MatchOperation(InboundPacket):
    CATEGORY = InboundPacketCategory.MatchOperation


class BeginMatch(MatchOperation):
    """
    开始匹配
    """
    TYPE_ID = InboundPacketTypeId.BeginMatch


class CancelMatch(MatchOperation):
    """
    取消匹配
    """
    TYPE_ID = InboundPacketTypeId.CancelMatch
