# -*- coding: GBK -*-

import logging

from common.singleton import Singleton
from common.util.reflection_util import ReflectionUtil
from dispatch.service import Service
from packet.inbound.inbound_packet_type_id import InboundPacketCategory


class Dispatcher(object):
    __metaclass__ = Singleton
    """
    �������������ݰ����䵽ָ���ķ����ϴ���
    """

    def __init__(self):
        self.__serviceMap = {}

    def dispatch(self, context, packet):
        """
        �������ݰ�
        @param context: ���ݰ�����Դͨ������
        @param packet: ��Ҫ���ɵ����ݰ�
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
        ���з����ע��
        @param svc: ��Ҫ����ע��ķ���
        """
        logging.info("Dispatcher Register Service Category <{}:{}>"
                     .format(ReflectionUtil.getStaticFieldName(InboundPacketCategory, svc.category),
                             svc.category)
                     )
        self.__serviceMap[svc.category] = svc

    def registerHandler(self, handler):
        """
        ���д�������ע��
        @param handler: ��Ҫ����ע��Ĵ�����
        """
        if handler.category not in self.__serviceMap:
            self.registerSvc(Service(handler.category))
        self.__serviceMap[handler.category].register(handler)
