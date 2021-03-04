# coding=utf-8
# @Time : 2020/8/8 14:11
# @Author : 胡泽勇
# 反射工具
from types import FunctionType


class ReflectionUtil(object):
    @staticmethod
    def getMethodSignature(method):
        moduleName = method.__module__
        methodClassName = ('.' + method.im_class.__name__) if hasattr(method, "im_class") else ''
        methodName = '.' + method.__name__ + "()"
        return moduleName + methodClassName + methodName

    @staticmethod
    def isSubclass(cls, cls2):
        """
        检查cls是否是cls2的真子类
        @return: cls是否为cls2的真子类
        """
        return cls is not cls2 and issubclass(cls, cls2)

    @staticmethod
    def getPublicStaticFields(cls):
        """
        获得一个类的所有声明的公开静态变量，注意这些静态变量不以下划线开头
        @param cls: 需要的类
        @return: 该类的公开静态变量
        """
        # 用getattr而非直接取__dict__.items()是为了使得class method生效，进而通过callable进行过滤
        return [(field, getattr(cls, field)) for field in cls.__dict__.keys() if
                not (field.startswith('_') or callable(getattr(cls, field)))]

    @staticmethod
    def getStaticFieldName(t, v):
        """
        根据给定的值获得类的静态成员的名称（无法应对重复问题）
        @param t: 给定的类
        @param v: 给定的值
        @return: 在该类中值为给定的值的静态成员名称，若不存在指定的值
        则返回None
        """
        for name in dir(t):
            if getattr(t, name) == v:
                return name
        return None

    funcReplaceKey = ["func_code", "func_dict", "func_doc"]

    @staticmethod
    def replaceFunc(src, des):
        if type(src) != FunctionType or type(des) != FunctionType:
            raise Exception("替换的方法必须均为Function")
        for k in ReflectionUtil.funcReplaceKey:
            setattr(des, k, getattr(src, k))
