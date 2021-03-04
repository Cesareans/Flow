import logging

from common.util.reflection_util import ReflectionUtil
from packet.inbound.inbound_packet_type_id import InboundPacketCategory, InboundPacketTypeId


class Service(object):
    def __init__(self, category=None):
        self.category = category
        self.__handlerMap = {}

    def handle(self, context, packet):
        typeId = packet.TYPE_ID
        if typeId not in self.__handlerMap:
            logging.warn('Packet handler with type {0}<{1}> not registered. Please refer dispatch.__init__.py'.format(
                ReflectionUtil.getStaticFieldName(InboundPacketTypeId, typeId), typeId)
            )
            return
        self.__handlerMap[typeId].handle(context, packet)

    def register(self, handler):
        logging.info("Service Register Category <{:16s}:{:3d}> with Handler <{}:{}>"
                     .format(ReflectionUtil.getStaticFieldName(InboundPacketCategory, self.category),
                             self.category,
                             type(handler).__name__,
                             handler.typeId)
                     )
        self.__handlerMap[handler.typeId] = handler
