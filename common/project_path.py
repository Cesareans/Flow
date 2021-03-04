# coding=utf-8
# @Time : 2020/8/8 14:11
# @Author : 胡泽勇
# 项目路径，用于获得相对项目的路径在全局中的路径
from os.path import dirname, join, split

from common.singleton import Singleton


class ProjectPath(object):
    __metaclass__ = Singleton

    def __init__(self):
        """
        项目路径器
        """
        # 获得该文件所在的路径
        __FILE_DIR = dirname(__file__)
        # 取得项目的路径，对该文件位置有要求
        self.path = split(__FILE_DIR)[0]

    def filepath(self, *hierarchy):
        """
        获得指定相对路径的文件路径
        @param hierarchy: 相对项目根目录的相对路径
        @return: 全局文件路径
        """
        return join(self.path, *hierarchy)
