# coding=utf-8

import logging

from common.util.reflection_util import ReflectionUtil
from packet.inbound.inbound_packet_type_id import InboundPacketCategory
from packet.packet import Packet


class InboundPacket(Packet):
    CATEGORY = None

    __packetMap = {}

    @classmethod
    def getCategory(cls):
        if cls.CATEGORY is None:
            raise Exception('应该配置该数据包<{}>的类目', cls)
        return cls.CATEGORY

    @property
    def category(self):
        return self.getCategory()

    @classmethod
    def register(cls):
        typeId = cls.getTypeId()
        category = cls.getCategory()
        if typeId is not None:
            if typeId in cls.__packetMap:
                logging.error("InboundPacket<{}:{}> already registered!"
                              .format(cls.__name__,
                                      typeId)
                              )
            else:
                logging.info("Register Category <{:16s}:{:3d}> with InboundPacket<{}:{}>  "
                             .format(ReflectionUtil.getStaticFieldName(InboundPacketCategory, category),
                                     category,
                                     cls.__name__,
                                     typeId)
                             )
                cls.__packetMap[typeId] = cls

    @classmethod
    def getType(cls, tid):
        return cls.__packetMap[tid] if tid in cls.__packetMap else None
