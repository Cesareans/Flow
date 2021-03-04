# coding=utf-8
import types

from common.util.reflection_util import ReflectionUtil
from packet.inbound.inbound_packet import InboundPacket
from packet.outbound.exception import NotLoginException, NoGameException


def PacketHandler(packetType):
    if not ReflectionUtil.isSubclass(packetType, InboundPacket):
        raise Exception()

    def wrapper(cls):
        cls.PacketType = packetType
        return cls

    return wrapper


class IHandler(object):
    PacketType = None

    def handle(self, context, packet):
        raise NotImplementedError

    @property
    def typeId(self):
        if self.PacketType is None:
            raise Exception("应该配置该处理器<{}>的PacketType".format(type(self)))
        return self.PacketType.TYPE_ID

    @property
    def category(self):
        if self.PacketType is None:
            raise Exception("应该配置该处理器<{}>的PacketType".format(type(self)))
        return self.PacketType.CATEGORY


class CheckLogin(object):
    def __init__(self, handle):
        self.handle = handle
        self.__method = None

    def __call__(self, handler, context, packet, *args, **kwargs):
        account = context.session.account
        if account is None:
            context.fireOutboundHandle(NotLoginException())
            return
        self.handle(handler, context, packet)

    # noinspection PyArgumentList
    def __get__(self, instance, owner):
        if self.__method is None:
            self.__method = types.MethodType(self, instance, owner)
        return self.__method


class CheckGame(object):
    def __init__(self, handle):
        self.handle = handle
        self.__method = None

    def __call__(self, handler, context, packet, *args, **kwargs):
        gsn = context.session.gameSession
        if gsn.world is None:
            context.fireOutboundHandle(NoGameException())
            return
        self.handle(handler, context, packet)

    # noinspection PyArgumentList
    def __get__(self, instance, owner):
        if self.__method is None:
            self.__method = types.MethodType(self, instance, owner)
        return self.__method
