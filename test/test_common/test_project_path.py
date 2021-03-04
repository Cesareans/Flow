# coding=utf-8
# @Time : 2020/9/15 15:11
# @Author : 胡泽勇
# ${Description}
from unittest import TestCase

from common.project_path import ProjectPath


class TestProjectPath(TestCase):
    def test_filepath(self):
        print ProjectPath().path
