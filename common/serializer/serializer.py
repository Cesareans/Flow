# coding=utf-8
# @Time : 2020/8/8 14:11
# @Author : 胡泽勇
# 序列化器接口


class SerializerType(object):
    JSON = 1

    def __init__(self):
        pass


class ISerializer(object):
    def __init__(self):
        pass

    def getType(self):
        raise NotImplementedError

    # return : byte[]
    def serialize(self, obj):
        raise NotImplementedError

    # return : obj
    def deserialize(self, dataType, data):
        raise NotImplementedError
