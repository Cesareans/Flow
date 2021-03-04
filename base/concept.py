# coding=utf-8
# @Time : 2020/8/12 9:21
# @Author : 胡泽勇
# 概念对象，通过Class Level构建自己的数据体系
import inspect

from data import Data


class Property(Data):
    def __init__(self, pt, default=None, required=False):
        """
        属性对象，为Concept对象在Class Level声明字段
        @param pt: 属性对象的类型，如果设置为None，则直接将设置的值不通过任何转型而进行赋值
        @param default: 属性对象的默认值，在该字段初始化时分配的默认值
        @param required: 对该对象是否必要，在对象初始化时进行确定
        """
        self.type = pt
        self.default = default
        self.required = required


# why don't use meta class here:
# doing oop. And Meta class should be used in very advanced and extremely dynamic program flow from my perspective.
# And here we can use inheritance to archive the same thing thus we don't need high level techniques.
class Concept(object):
    def __init__(self):
        """
        概念对象，所有继承自概念对象的类型通过Property声明字段
        """
        self.__props = {}
        for k, v in inspect.getmembers(type(self)):
            if type(v) == Property:
                self.props[k] = v
                self.__setattr__(k, v.default if v.default is not None else None)

    @property
    def props(self):
        """
        @return: 该概念对象的属性列表
        """
        return self.__props

    @staticmethod
    def parseValue(pt, value):
        """
        根据给定的值与类型，建立转化后的值
        @param pt: 对应类型
        @param value: 对应的值
        @return: 转化后的值
        """
        # 前一个条件：类型申请时为动态类型
        # 后一个条件：给予dict的值已经是转化后的概念对象
        # 在这两个条件下，都直接返回值对象
        if pt is None or issubclass(type(value), Concept):
            return value
        else:
            return pt(value)

    def __repr__(self):
        return str({k: getattr(self, k) for k, v in self.props.items()})


class ConceptException(Exception):
    def __init__(self, *args):
        super(ConceptException, self).__init__(*args)


class DictConcept(Concept):
    def __init__(self, dic=None, **kwargs):
        """
        字典概念对象，从一个字典中构建对象实体，并对每个字段进行赋值
        @param dic: 赋值来源
        """
        super(DictConcept, self).__init__()
        if dic is None:
            dic = {}
        # 使用kwargs更新输入的字典
        dic.update(kwargs)
        # 通过dic更新类的字段值
        for name, prop in self.props.items():
            # 判断属性是否在提供的词典内
            if name in dic:
                try:
                    # 通过属性配置的类型，进行对于数据的转换取得指定的值
                    setattr(self, name, self.parseValue(prop.type, dic[name]))
                except Exception as ex:
                    raise ConceptException("转化概念对象<{}>时出错，对应字段<{}>，原因:\n{}".format(type(self).__name__, name, ex))
            # 不在且必须，则抛出异常
            elif prop.required:
                raise ConceptException("转化概念对象<{}>时出错，参数缺乏必要字段<{}>".format(type(self).__name__, name))


class ListConcept(Concept):
    def __init__(self, lst):
        """
        列表概念对象，从一个列表中构建对象实体，并对每个字段进行赋值
        @param lst: 赋值来源
        """
        super(ListConcept, self).__init__()
        self.list = []
        for element in lst:
            self.list.append(self.parseValue(self.elementType, element))

    def __getattr__(self, item):
        return getattr(self.list, item)

    def __getitem__(self, item):
        return self.list[item]

    def __len__(self):
        return len(self.list)

    def __iter__(self):
        return iter(self.list)

    def __repr__(self):
        return repr(self.list)

    def __str__(self):
        return str(self.list)

    @property
    def elementType(self):
        raise NotImplementedError

    @staticmethod
    def of(inType):
        class ListConceptWrapper(ListConcept):
            @property
            def elementType(self):
                return inType

        return ListConceptWrapper
