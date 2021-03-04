# coding=utf-8
# @Time : 2020/8/8 9:50
# @Author : 胡泽勇
# 数据对象


class Data(object):
    """
    数据对象，主要是为子类提供转化字符串的方法
    """

    def __repr__(self):
        return '<{0}>{1}'.format(type(self).__name__, str(self.__dict__))

    __str__ = __repr__


class Prototype(object):
    def __init__(self, dic=None, **kwargs):
        if dic is None:
            dic = {}
        dic.update(kwargs)
        for k, v in dic.items():
            setattr(self, k, v)

    def __setattr__(self, key, value):
        setattr(self, key, value)

    def __repr__(self):
        return str(self.__dict__)

    __str__ = __repr__
