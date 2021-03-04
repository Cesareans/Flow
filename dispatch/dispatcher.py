# -*- coding: GBK -*-

import logging

from common.singleton import Singleton
from common.util.reflection_util import ReflectionUtil
from dispatch.service import Service
from packet.inbound.inbound_packet_type_id import InboundPacketCategory


class Dispatcher(object):
    __metaclass__ = Singleton
    """
    分配器，将数据包分配到指定的服务上处理
    """

    def __init__(self):
        self.__serviceMap = {}

    def dispatch(self, context, packet):
        """
        分配数据包
        @param context: 数据包的来源通道环境
        @param packet: 需要分派的数据包
        """
        category = packet.category
        if category not in self.__serviceMap:
            raise Exception('Service with category <{}:{}> not exist.'.format(
                ReflectionUtil.getStaticFieldName(InboundPacketCategory, category),
                category
            ))

        self.__serviceMap[category].handle(context, packet)

    def registerSvc(self, svc):
        """
        进行服务的注册
        @param svc: 需要进行注册的服务
        """
        logging.info("Dispatcher Register Service Category <{}:{}>"
                     .format(ReflectionUtil.getStaticFieldName(InboundPacketCategory, svc.category),
                             svc.category)
                     )
        self.__serviceMap[svc.category] = svc

    def registerHandler(self, handler):
        """
        进行处理器的注册
        @param handler: 需要进行注册的处理器
        """
        if handler.category not in self.__serviceMap:
            self.registerSvc(Service(handler.category))
        self.__serviceMap[handler.category].register(handler)
