# coding=utf-8
# @Time : 2020/8/11 16:24
# @Author : 胡泽勇
#

from common.module_load import ModuleLoad
from common.util.reflection_util import ReflectionUtil
from dispatch.dispatcher import Dispatcher
from dispatch.handler.ihandler import IHandler


class Registor(object):
    __registered = False

    @staticmethod
    def register():
        if Registor.__registered:
            return
        Registor.__registered = True
        ModuleLoad.loadClassInModule("dispatch.handler",
                                     filters=[
                                         lambda klass: ReflectionUtil.isSubclass(klass, IHandler),
                                         lambda klass: klass.PacketType is not None
                                     ], actions=[lambda handlerType: Dispatcher().registerHandler(handlerType())]
                                     )
