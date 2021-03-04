# coding=utf-8

from base.concept import DictConcept


class Packet(DictConcept):
    TYPE_ID = None

    @classmethod
    def getTypeId(cls):
        if cls.TYPE_ID is None:
            raise Exception('应该配置该数据包<{}>的类型标识符', cls)
        return cls.TYPE_ID

    @property
    def typeId(self):
        return self.getTypeId()
