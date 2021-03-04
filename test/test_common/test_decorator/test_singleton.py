# coding=utf-8
# @Time : 2020/8/17 13:48
# @Author : 胡泽勇
# ${Description}
from unittest import TestCase

from common.singleton import Singleton


class TestSingleton(TestCase):
    def testSingletonType(self):
        # @Singleton
        class A(object):
            __metaclass__ = Singleton

            def __init__(self):
                self.i = 1

        self.assertEqual(type(A()), A)
        # self.assertEqual(A(), A())
        A().i = 2
        a = A()
        self.assertEqual(A().i, 2)
