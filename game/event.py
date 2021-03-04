# coding=utf-8
# @Time : 2020/8/14 14:52
# @Author : 胡泽勇
# 简易事件系统
import logging

from base.data import Data
from common.util.reflection_util import ReflectionUtil


# 事件基类，所有事件必须继承自该类
class Event(Data):
    pass


# 不应再使用如下二级装饰器将方法类型化，否则方法将会成为类的对象成员，在热加载的时候无法进行原地替换
# 事件处理器二级装饰器，用于将方法类型化
# class _EventHandlerWrapper(object):
#     def __init__(self, method, eventType):
#         if not issubclass(eventType, Event):
#             raise Exception
#         self.eventType = eventType
#         self.method = method
#
#     def __call__(self, *args, **kwargs):
#         return self.method(*args, **kwargs)
#
#     # noinspection PyArgumentList
#     def __get__(self, instance, owner):
#         # 基于instance与owner<class>建立新的方法，该方法bound在instance上
#         # 通过instance.this可以将instance作为self传递给该方法
#         return types.MethodType(self, instance, owner)
#
#     # 保证meta信息不发生变化
#     __doc__ = property(lambda self: self.method.__doc__)
#     __module__ = property(lambda self: self.method.__module__)
#     __name__ = property(lambda self: self.method.__name__)
#
#     @staticmethod
#     def checkIsWrapper(method):
#         return hasattr(method, "eventType")


# 事件处理器一级装饰器，为方法注入eventType参数
def EventHandler(eventType):
    def wrapper(func):
        func.eventType = eventType
        return func

    return wrapper


# 单一事件的观察者
class _EventObserver(object):
    def __init__(self):
        self.observers = set()

    def __iadd__(self, handler):
        self.observers.add(handler)
        return self

    def __isub__(self, handler):
        self.observers.remove(handler)
        return self

    def fire(self, event):
        """
        旧：
        正序遍历下如果有人在这个observer里面移除自己则导致self.observers被修改
        解决方案：
        1. 倒序遍历：添加则会出问题，使用这个方案只要禁止在监听事件处理中不添加就行
        2. 双向链表：麻烦
        新：使用集合
        """
        for observer in self.observers.copy():
            observer(event)


# 事件系统
class EventCenter(object):
    def __init__(self):
        self.__eventListeners = {}

    # 注意到这种方法在热更新时，会出大问题：在热更新前注册的是旧的方法代码
    # 而在热更新后，方法代码即使没有改变，也会因为热更新而与旧的不同，在此时则会出现问题就是热更新后无法解注册
    def register(self, eventHandler):
        self.__checkHandler(eventHandler)
        if eventHandler.eventType not in self.__eventListeners:
            self.__eventListeners[eventHandler.eventType] = _EventObserver()
        logging.debug("Event Center register method: " + ReflectionUtil.getMethodSignature(eventHandler))
        self.__eventListeners[eventHandler.eventType] += eventHandler

    def unregister(self, eventHandler):
        self.__checkHandler(eventHandler)
        if eventHandler.eventType not in self.__eventListeners:
            raise Exception
        logging.debug("Event Center unregister method: " + ReflectionUtil.getMethodSignature(eventHandler))
        self.__eventListeners[eventHandler.eventType] -= eventHandler

    def fire(self, event):
        eventType = type(event)
        if eventType not in self.__eventListeners:
            return
        logging.debug("Event Center fire event: " + str(event))
        self.__eventListeners[eventType].fire(event)

    def __iadd__(self, handler):
        self.register(handler)
        return self

    def __isub__(self, handler):
        self.unregister(handler)
        return self

    @staticmethod
    def __checkHandler(eventHandler):
        if eventHandler.eventType is None:
            raise Exception("注册{}方法缺失EventHandler装饰器".format(ReflectionUtil.getMethodSignature(eventHandler)))
