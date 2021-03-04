# coding=utf-8
# @Time : 2020/9/11 17:13
# @Author : 胡泽勇
#

from packet.inbound.inbound_packet import InboundPacket
from packet.inbound.inbound_packet_type_id import InboundPacketCategory, InboundPacketTypeId


class ReconnectOperation(InboundPacket):
    CATEGORY = InboundPacketCategory.ReconnectOperation


class CheckWorld(ReconnectOperation):
    TYPE_ID = InboundPacketTypeId.CheckWorld


class EnterReconnect(ReconnectOperation):
    TYPE_ID = InboundPacketTypeId.EnterReconnect
