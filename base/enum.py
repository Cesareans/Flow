# coding=utf-8
# @Time : 2020/8/13 9:48
# @Author : 胡泽勇
# 
import inspect

from common.util.reflection_util import ReflectionUtil


class Enum(object):
    """
    枚举对象，提供允许value dic
    """
    _v2k = {}
    __enumName = None
    __inited__ = False

    def __init__(self, value):
        if not self.__inited__:
            self.__enum__()

        self.value = value
        self.name = self._v2k[value]

    def __get__(self, instance, owner):
        return self.value

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        return self.value == other

    def __repr__(self):
        return "{}[{}={}]".format(type(self).__name__, self.name, self.value)

    __str__ = __repr__

    @classmethod
    def __enum__(cls):
        if not cls.__inited__:
            cls.__inited__ = True
            for k, v in ReflectionUtil.getPublicStaticFields(cls):
                if inspect.ismethod(v):
                    continue
                cls._v2k[v] = k
                setattr(cls, k, cls(v))

    @classmethod
    def values(cls):
        if not cls.__inited__:
            cls.__enum__()
        return cls._v2k.keys()
