# coding=utf-8
# @Time : 2020/8/19 9:55
# @Author : 胡泽勇
#

from packet.outbound.outbound_packet import OutboundPacket
from packet.outbound.outbound_packet_type_id import OutboundPacketTypeId


class BeginLoad(OutboundPacket):
    TYPE_ID = OutboundPacketTypeId.BeginLoad
