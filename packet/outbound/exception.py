# coding=utf-8

from packet.outbound.outbound_packet import MessagePacket
from packet.outbound.outbound_packet_type_id import OutboundPacketTypeId


class ExceptionPacket(MessagePacket):
    def __init__(self, message):
        super(ExceptionPacket, self).__init__(message)


class NotLoginException(ExceptionPacket):
    TYPE_ID = OutboundPacketTypeId.NotLogin

    def __init__(self):
        super(NotLoginException, self).__init__('请先登录')


class NoGameException(ExceptionPacket):
    TYPE_ID = OutboundPacketTypeId.NoGame

    def __init__(self):
        super(NoGameException, self).__init__('尚未进入游戏')


class LatticeNotExistException(ExceptionPacket):
    TYPE_ID = OutboundPacketTypeId.LatticeNotExist

    def __init__(self):
        super(LatticeNotExistException, self).__init__("指定的格子不存在")


class LatticeIsNotWalkableException(ExceptionPacket):
    TYPE_ID = OutboundPacketTypeId.LatticeNotExist

    def __init__(self):
        super(LatticeIsNotWalkableException, self).__init__("指定的格子无法通行")


class CannotChooseException(ExceptionPacket):
    TYPE_ID = OutboundPacketTypeId.CannotChoose

    def __init__(self):
        super(CannotChooseException, self).__init__("指定卡牌无法选择")


class HaveNoSuchCardException(ExceptionPacket):
    TYPE_ID = OutboundPacketTypeId.HaveNoSuchCard

    def __init__(self):
        super(HaveNoSuchCardException, self).__init__("无该手牌")


class CannotCastException(ExceptionPacket):
    TYPE_ID = OutboundPacketTypeId.CannotCast

    def __init__(self, serial=-1):
        super(CannotCastException, self).__init__("无法释放")
        self.serial = serial
