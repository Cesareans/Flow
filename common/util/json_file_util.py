# coding=utf-8
# @Time : 2020/8/8 14:11
# @Author : 胡泽勇
# JSON文件工具
from os.path import join

from common.project_path import ProjectPath
from common.serializer.json_serializer import JsonSerializer


class JsonFileUtil(object):
    def __init__(self):
        pass

    @staticmethod
    def read(path, dataType=None, inProject=True):
        if inProject:
            path = join(ProjectPath().path, path)
        with open(path, 'r') as f:
            data = f.read()
            if dataType is None:
                return JsonSerializer().dic(data)
            else:
                return JsonSerializer().deserialize(dataType, data)

    @staticmethod
    def write(obj, path, inProject=True):
        if inProject:
            path = join(ProjectPath().path, path)
        with open(path, 'w') as f:
            data = JsonSerializer().serialize(obj)
            f.write(data)
