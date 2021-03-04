# coding=utf-8
# @Time : 2020/8/19 11:34
# @Author : 胡泽勇
#

from packet.inbound.game_synchronize import GameSynchronizePacket
from packet.inbound.inbound_packet_type_id import InboundPacketTypeId


class EnterLoad(GameSynchronizePacket):
    TYPE_ID = InboundPacketTypeId.EnterLoad
