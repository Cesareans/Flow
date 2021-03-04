# coding=utf-8

from base.concept import ListConcept, Property
from game.concept.coord import AxisCoord
from packet.inbound.inbound_packet import InboundPacket
from packet.inbound.inbound_packet_type_id import InboundPacketCategory, InboundPacketTypeId


class GameSynchronizePacket(InboundPacket):
    CATEGORY = InboundPacketCategory.GameSynchronize


class EnterGame(GameSynchronizePacket):
    TYPE_ID = InboundPacketTypeId.EnterGame


class ExitGame(GameSynchronizePacket):
    TYPE_ID = InboundPacketTypeId.ExitGame


# 决策数据包
class Move(GameSynchronizePacket):
    """
    移动决策
    """
    TYPE_ID = InboundPacketTypeId.Move
    paths = Property(ListConcept.of(AxisCoord), required=True)  # 移动路径


class CastCard(GameSynchronizePacket):
    """
    释放卡牌
    """
    TYPE_ID = InboundPacketTypeId.CastCard
    serial = Property(int, required=True)  # 表示需要释放的卡牌的序号（该序号每个人物在获得卡牌的时候自动分配）
    coord = Property(AxisCoord, required=True)  # 表示需要释放的格子目标


class CastSkill(GameSynchronizePacket):
    """
    释放技能
    """
    TYPE_ID = InboundPacketTypeId.CastSkill
    coord = Property(AxisCoord, required=True)  # 表示技能需要释放的格子目标


class CastAttack(GameSynchronizePacket):
    """
    进行攻击
    """
    TYPE_ID = InboundPacketTypeId.CastAttack
    coord = Property(AxisCoord, required=True)  # 表示攻击的格子目标


class CancelCastCard(GameSynchronizePacket):
    """
    取消释放卡牌
    """
    TYPE_ID = InboundPacketTypeId.CancelCastCard
    serial = Property(int, required=True)  # 表示需要取消释放的卡牌的序号


class ChooseCard(GameSynchronizePacket):
    """
    选择卡牌
    """
    TYPE_ID = InboundPacketTypeId.ChooseCard
    indexes = Property(ListConcept.of(int), required=True)  # 表示选择的卡牌的ids


class DiscardCard(GameSynchronizePacket):
    """
    弃置卡牌
    """
    TYPE_ID = InboundPacketTypeId.DiscardCard
    serial = Property(int, required=True)  # 表示弃置的卡牌的序号s


class EndDecision(GameSynchronizePacket):
    """
    弃置卡牌
    """
    TYPE_ID = InboundPacketTypeId.EndDecision
