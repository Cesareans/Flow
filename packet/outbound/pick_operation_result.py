# coding=utf-8
# @Time : 2020/8/18 15:28
# @Author : 胡泽勇
#

from packet.outbound.outbound_packet import OutboundPacket, GeneralOperationPacket
from packet.outbound.outbound_packet_type_id import OutboundPacketTypeId


class BeginPick(OutboundPacket):
    TYPE_ID = OutboundPacketTypeId.BeginPick


class PickCharacterResult(GeneralOperationPacket):
    TYPE_ID = OutboundPacketTypeId.PickCharacterResult

    def __init__(self, success, message, characterId=0):
        super(PickCharacterResult, self).__init__(success, message)
        self.characterId = characterId


class CharacterLocked(OutboundPacket):
    TYPE_ID = OutboundPacketTypeId.CharacterLocked

    def __init__(self, characterId):
        super(CharacterLocked, self).__init__()
        self.characterId = characterId


class CharacterUnlocked(OutboundPacket):
    TYPE_ID = OutboundPacketTypeId.CharacterUnlocked

    def __init__(self, characterId):
        super(CharacterUnlocked, self).__init__()
        self.characterId = characterId


class PickCountDown(OutboundPacket):
    TYPE_ID = OutboundPacketTypeId.PickCountDown

    def __init__(self, countDown):
        super(PickCountDown, self).__init__()
        self.countDown = countDown


class QuitPick(OutboundPacket):
    TYPE_ID = OutboundPacketTypeId.QuitPick

    def __init__(self):
        super(QuitPick, self).__init__()
