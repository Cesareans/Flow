# coding=utf-8

from common.serializer.json_serializer import JsonSerializer
from packet.outbound.outbound_packet import OutboundPacket
from packet.outbound.outbound_packet_type_id import OutboundPacketTypeId


class RemoveEntity(OutboundPacket):
    TYPE_ID = OutboundPacketTypeId.RemoveEntity

    def __init__(self, eid):
        super(RemoveEntity, self).__init__()
        self.eid = eid


class PlacePlayerCharacter(OutboundPacket):
    TYPE_ID = OutboundPacketTypeId.PlacePlayerCharacter

    def __init__(self, eid, name, characterId, coord):
        super(PlacePlayerCharacter, self).__init__()
        self.eid = eid
        self.name = name
        self.characterId = characterId
        self.coord = coord


class SetMainCharacter(OutboundPacket):
    TYPE_ID = OutboundPacketTypeId.SetMainCharacter

    def __init__(self, eid):
        super(SetMainCharacter, self).__init__()
        self.eid = eid


class UpdateSkillCd(OutboundPacket):
    TYPE_ID = OutboundPacketTypeId.UpdateSkillCd

    def __init__(self, eid, cd):
        super(UpdateSkillCd, self).__init__()
        self.eid = eid
        self.cd = cd


class UpdateSkillInfo(OutboundPacket):
    TYPE_ID = OutboundPacketTypeId.UpdateSkillInfo

    def __init__(self, eid, info):
        super(UpdateSkillInfo, self).__init__()
        self.eid = eid
        self.info = JsonSerializer().serialize(info)


class ProhibitCast(OutboundPacket):
    TYPE_ID = OutboundPacketTypeId.ProhibitCast

    def __init__(self, eid, castType, cardType):
        super(ProhibitCast, self).__init__()
        self.eid = eid
        self.castType = castType
        self.cardType = cardType


class CancelProhibitCast(OutboundPacket):
    TYPE_ID = OutboundPacketTypeId.CancelProhibitCast

    def __init__(self, eid, castType, cardType):
        super(CancelProhibitCast, self).__init__()
        self.eid = eid
        self.castType = castType
        self.cardType = cardType


class Move(OutboundPacket):
    TYPE_ID = OutboundPacketTypeId.Move

    def __init__(self, eid, coord):
        super(Move, self).__init__()
        self.eid = eid
        self.coord = coord


class EndMove(OutboundPacket):
    TYPE_ID = OutboundPacketTypeId.EndMove

    def __init__(self, eid):
        super(EndMove, self).__init__()
        self.eid = eid


class CastPacket(OutboundPacket):
    TYPE_ID = OutboundPacketTypeId.Cast

    def __init__(self, eid, coord, info):
        super(CastPacket, self).__init__()
        self.eid = eid
        self.coord = coord
        self.info = info


class Damage(OutboundPacket):
    TYPE_ID = OutboundPacketTypeId.Damage

    def __init__(self, eid, value):
        super(Damage, self).__init__()
        self.eid = eid
        self.value = value


class Heal(OutboundPacket):
    TYPE_ID = OutboundPacketTypeId.Heal

    def __init__(self, eid, value):
        super(Heal, self).__init__()
        self.eid = eid
        self.value = value


class BeginRound(OutboundPacket):
    TYPE_ID = OutboundPacketTypeId.BeginRound


class EndRound(OutboundPacket):
    TYPE_ID = OutboundPacketTypeId.EndRound


class BeginSettle(OutboundPacket):
    TYPE_ID = OutboundPacketTypeId.BeginSettle


class EndSettle(OutboundPacket):
    TYPE_ID = OutboundPacketTypeId.EndSettle


class UpdateSettleStage(OutboundPacket):
    TYPE_ID = OutboundPacketTypeId.UpdateSettleStage

    def __init__(self, stage):
        super(UpdateSettleStage, self).__init__()
        self.stage = stage


class SyncCards(OutboundPacket):
    TYPE_ID = OutboundPacketTypeId.SyncCards

    def __init__(self, eid, cards):
        super(SyncCards, self).__init__()
        self.eid = eid
        self.cards = cards


class GainCard(OutboundPacket):
    TYPE_ID = OutboundPacketTypeId.GainCard

    def __init__(self, eid, cardId, serial):
        super(GainCard, self).__init__()
        self.eid = eid
        self.cardId = cardId
        self.serial = serial


class DropCard(OutboundPacket):
    TYPE_ID = OutboundPacketTypeId.DropCard

    def __init__(self, eid, serial):
        super(DropCard, self).__init__()
        self.eid = eid
        self.serial = serial


class AvailableCards(OutboundPacket):
    TYPE_ID = OutboundPacketTypeId.AvailableCards

    def __init__(self, eid, cards, count):
        super(AvailableCards, self).__init__()
        self.eid = eid
        self.cards = cards
        self.count = count


class AvailableCardsEnd(OutboundPacket):
    TYPE_ID = OutboundPacketTypeId.AvailableCardsEnd

    def __init__(self, eid):
        super(AvailableCardsEnd, self).__init__()
        self.eid = eid


class SyncCardsCount(OutboundPacket):
    TYPE_ID = OutboundPacketTypeId.SyncCardsCount

    def __init__(self, eid, count):
        super(SyncCardsCount, self).__init__()
        self.eid = eid
        self.count = count


class SyncCardLimit(OutboundPacket):
    TYPE_ID = OutboundPacketTypeId.SyncCardLimit

    def __init__(self, eid, limit):
        super(SyncCardLimit, self).__init__()
        self.eid = eid
        self.limit = limit


class SyncLifeState(OutboundPacket):
    TYPE_ID = OutboundPacketTypeId.SyncLifeState

    def __init__(self, eid, life):
        super(SyncLifeState, self).__init__()
        self.eid = eid
        self.life = life


class CharacterDead(OutboundPacket):
    TYPE_ID = OutboundPacketTypeId.CharacterDead

    def __init__(self, eid):
        super(CharacterDead, self).__init__()
        self.eid = eid


class SyncEquip(OutboundPacket):
    TYPE_ID = OutboundPacketTypeId.SyncEquip

    def __init__(self, eid, equipIds):
        super(SyncEquip, self).__init__()
        self.eid = eid
        self.equipIds = equipIds


class DropEquip(OutboundPacket):
    TYPE_ID = OutboundPacketTypeId.DropEquip

    def __init__(self, eid, coord, equipIds):
        super(DropEquip, self).__init__()
        self.eid = eid
        self.coord = coord
        self.equipIds = equipIds


class AddEquip(OutboundPacket):
    TYPE_ID = OutboundPacketTypeId.AddEquip

    def __init__(self, eid, equipId):
        super(AddEquip, self).__init__()
        self.eid = eid
        self.equipId = equipId


class DropEquipDestroy(OutboundPacket):
    TYPE_ID = OutboundPacketTypeId.DropEquipDestroy

    def __init__(self, eid):
        super(DropEquipDestroy, self).__init__()
        self.eid = eid


class AddMapElement(OutboundPacket):
    TYPE_ID = OutboundPacketTypeId.AddMapElement

    def __init__(self, eid, coord, elementType):
        super(AddMapElement, self).__init__()
        self.eid = eid
        self.coord = coord
        self.elementType = elementType


class RemoveMapElement(OutboundPacket):
    TYPE_ID = OutboundPacketTypeId.RemoveMapElement

    def __init__(self, eid):
        super(RemoveMapElement, self).__init__()
        self.eid = eid


class AddEnergyLattice(OutboundPacket):
    TYPE_ID = OutboundPacketTypeId.AddEnergyLattice

    def __init__(self, coord):
        super(AddEnergyLattice, self).__init__()
        self.coord = coord


class RemoveEnergyLattice(OutboundPacket):
    TYPE_ID = OutboundPacketTypeId.RemoveEnergyLattice

    def __init__(self, coord):
        super(RemoveEnergyLattice, self).__init__()
        self.coord = coord


class MapCollapse(OutboundPacket):
    TYPE_ID = OutboundPacketTypeId.MapCollapse

    def __init__(self, depth):
        super(MapCollapse, self).__init__()
        self.depth = depth


class MapPreCollapse(OutboundPacket):
    TYPE_ID = OutboundPacketTypeId.MapPreCollapse

    def __init__(self, depth):
        super(MapPreCollapse, self).__init__()
        self.depth = depth


class AddModifier(OutboundPacket):
    TYPE_ID = OutboundPacketTypeId.AddModifier

    def __init__(self, eid, serial, name, data):
        super(AddModifier, self).__init__()
        self.eid = eid
        self.serial = serial
        self.name = name
        self.data = JsonSerializer().serialize(data)


class ModifierChange(OutboundPacket):
    TYPE_ID = OutboundPacketTypeId.ModifierChange

    def __init__(self, eid, serial, data):
        super(ModifierChange, self).__init__()
        self.eid = eid
        self.serial = serial
        self.data = JsonSerializer().serialize(data)


class ModifierInEffect(OutboundPacket):
    TYPE_ID = OutboundPacketTypeId.ModifierInEffect

    def __init__(self, eid, serial):
        super(ModifierInEffect, self).__init__()
        self.eid = eid
        self.serial = serial


class RemoveModifier(OutboundPacket):
    TYPE_ID = OutboundPacketTypeId.RemoveModifier

    def __init__(self, eid, serial):
        super(RemoveModifier, self).__init__()
        self.eid = eid
        self.serial = serial


class BeginTurn(OutboundPacket):
    TYPE_ID = OutboundPacketTypeId.BeginTurn

    def __init__(self, duration):
        super(BeginTurn, self).__init__()
        self.duration = duration


class EndDecision(OutboundPacket):
    TYPE_ID = OutboundPacketTypeId.EndDecision


class TurnCountDown(OutboundPacket):
    TYPE_ID = OutboundPacketTypeId.TurnCountDown

    def __init__(self, countDown, turnTime):
        super(TurnCountDown, self).__init__()
        self.countDown = countDown
        self.turnTime = turnTime


class GameResult(OutboundPacket):
    TYPE_ID = OutboundPacketTypeId.GameResult

    def __init__(self, eid):
        super(GameResult, self).__init__()
        self.winEid = eid
