# coding=utf-8
# @Time : 2020/9/11 19:52
# @Author : 胡泽勇
#

from packet.outbound.outbound_packet import OutboundPacket
from packet.outbound.outbound_packet_type_id import OutboundPacketTypeId


class BeginReconnect(OutboundPacket):
    TYPE_ID = OutboundPacketTypeId.BeginReconnect
