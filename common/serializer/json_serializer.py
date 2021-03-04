# coding=utf-8
# @Time : 2020/8/8 14:11
# @Author : 胡泽勇
# JSON序列化器

import json

from common.serializer.serializer import ISerializer, SerializerType
from common.singleton import Singleton


# noinspection PyMethodMayBeStatic
class JsonSerializer(ISerializer):  # todo: 没有异常处理
    __metaclass__ = Singleton

    def getType(self):
        return SerializerType.JSON

    def serialize(self, obj, **kwargs):
        jsr = json.dumps(obj, default=lambda o: self.__pickField(o), **kwargs)
        return bytes(jsr)

    def dic(self, data):
        return json.loads(data)

    def deserializeConcept(self, conceptType, data):
        return conceptType(json.loads(data))

    def deserialize(self, dataType, data):
        obj = dataType()  # 实际上是作为prototype
        return self.deserializeOverwrite(obj, data)

    def deserializeOverwrite(self, obj, data):
        jsonDic = json.loads(data)
        return self.__dataToObj(jsonDic, obj)

    def deserializeDic(self, ktp, vtp, data):
        dic = {}
        jsonData = json.loads(data)
        for k, v in jsonData.items():
            dic[self.__dataToObj(k, ktp())] = self.__dataToObj(v, vtp())
        return dic

    def __pickField(self, o):
        dic = {}
        for k, v in o.__dict__.items():
            if not k.startswith('_'):
                dic[k] = v
        return dic

    # obj实际上是作为prototype
    def __dataToObj(self, jsonData, obj):
        jdt = type(jsonData)
        if jdt is list:
            obj = self.__listToObj(jsonData, obj)
        elif jdt is dict:
            obj = self.__dicToObj(jsonData, obj)
        elif obj is None:
            obj = jsonData
        else:
            obj = type(obj)(jsonData)
        return obj

    # obj实际上是作为prototype，仅适合单类型列表，不支持JSON多态
    def __listToObj(self, jsonList, obj):
        if type(obj) is not list:
            obj = [obj]
        if len(jsonList) == 0:
            obj = []
        elif len(obj) == 0:  # 无法判断obj作为list的内容类型
            obj = jsonList
            # 这里应该打一份日志
        else:
            et = type(obj[0])
            obj = []
            for jsonData in jsonList:
                elem = et()
                obj.append(self.__dataToObj(jsonData, elem))
        return obj

    # obj实际上是作为prototype
    def __dicToObj(self, jsonDic, obj):
        publicFields = self.__getPublicFields(obj)
        for field in jsonDic:
            if field in publicFields:
                fieldValue = getattr(obj, field)
                fieldValue = self.__dataToObj(jsonDic[field], fieldValue)
                setattr(obj, field, fieldValue)
        return obj

    def __getPublicFields(self, obj):
        return [field for field in dir(obj) if not field.startswith('_')]
