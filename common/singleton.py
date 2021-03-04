# coding=utf-8
# @Time : 2020/8/8 14:11
# @Author : 胡泽勇
# 单例装饰器
# Decorator
# class Singleton(object):
#     _instance = None
#
#     def __init__(self, cls):
#         self.cls = cls
#
#     def __call__(self, *args, **kwargs):
#         if self._instance is None:
#             self._instance = self.cls(*args, **kwargs)
#         return self._instance


import logging

# Meta Class
from base.ireload import IReload


class Singleton(type, IReload):
    _instances = {}

    def __new__(mcs, *args, **kwargs):
        mcs.instance = None
        return type.__new__(mcs, *args, **kwargs)

    def __call__(cls, *args, **kwargs):
        if cls.instance is None:
            if cls.__name__ in Singleton._instances:
                # 恢复热更新后的单例
                logging.debug("Restore Singleton Instance of {}".format(cls))
                cls.instance = Singleton._instances[cls.__name__]
            else:
                # 恢复热更新后的单例
                logging.debug("Create Singleton Instance of {}".format(cls))
                cls.instance = super(Singleton, cls).__call__(*args, **kwargs)
                Singleton._instances[cls.__name__] = cls.instance
        return cls.instance

    def keep(self):
        return self._instances

    def reload(self, keep):
        self._instances = keep

# class Singleton(IReload):
#     instance = None
#
#     def __new__(cls, *args, **kwargs):
#         if cls.instance is None:
#             # noinspection PyArgumentList
#             cls.instance = object.__new__(cls, *args, **kwargs)
#         return cls.instance
#
#     def keep(self):
#         return dict(instance=self.instance)
#
#     def reload(self, keep):
#         self.instance = keep.instance
