# coding=utf-8
# @Time : 2020/8/11 16:05
# @Author : 胡泽勇
# 读取模块工具

import os
from types import ModuleType, TypeType

from project_path import ProjectPath


class ModuleLoad(object):
    @staticmethod
    def loadClassInModule(module, moduleNames=None, filters=None, actions=None):
        """
        @param module: 指定的模块
        @param moduleNames: 指定的模块名，类型：str[]
        @param filters: 指定的过滤器
        @param actions: 指定的过滤后行为
        """
        fileHierarchy = module.split(".")
        # 找到指定module的文件路径
        path = ProjectPath().filepath(*fileHierarchy)
        # 在该路径下寻找所有的python文件
        if moduleNames is None:
            moduleNames = sorted(set(str(i.partition('.')[0]) for i in os.listdir(path) if i.endswith('.py')))
        # 加载找到的所有python文件
        importedModules = __import__(module, fromlist=moduleNames)
        # 建立已经加载的类的集合
        registeredClass = set()
        # 对模块名进行遍历
        for moduleName in moduleNames:
            # 根据模块名找到指定的模块
            module = getattr(importedModules, moduleName)
            # 如果不是模块类型，则继续循环
            if type(module) != ModuleType:
                continue
            # 在该模块下寻找所有的key
            for key in dir(module):
                # 跳过模块内置函数
                if key.startswith("__"):
                    continue
                # 寻找模块对应key的属性
                klass = getattr(module, key)
                # 如果该属性并非类型，或者已经被注册过，则继续循环
                if type(klass) != TypeType or klass in registeredClass:
                    continue
                # 进行指定的过滤
                if filters is not None:
                    filterOut = False
                    for fit in filters:
                        if not fit(klass):
                            filterOut = True
                            break
                    if filterOut:
                        continue
                # 执行指定的行为
                if actions is not None:
                    for action in actions:
                        action(klass)
                # 添加入注册集合，便于后续过滤
                registeredClass.add(klass)
