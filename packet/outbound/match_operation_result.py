# coding=utf-8
# @Time : 2020/8/18 14:06
# @Author : 胡泽勇
#

from packet.outbound.outbound_packet import OutboundPacket, GeneralOperationPacket
from packet.outbound.outbound_packet_type_id import OutboundPacketTypeId


class BeginMatchResult(GeneralOperationPacket):
    TYPE_ID = OutboundPacketTypeId.BeginMatchResult


class CancelMatchResult(GeneralOperationPacket):
    TYPE_ID = OutboundPacketTypeId.CancelMatchResult


class MatchProgress(OutboundPacket):
    TYPE_ID = OutboundPacketTypeId.MatchProgress

    def __init__(self, current, needed):
        super(MatchProgress, self).__init__()
        self.current = current
        self.needed = needed


class GameMatched(OutboundPacket):
    TYPE_ID = OutboundPacketTypeId.GameMatched
