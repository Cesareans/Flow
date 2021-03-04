# coding=utf-8
# @Time : 2020/8/15 13:53
# @Author : 胡泽勇
# ${Description}
from unittest import TestCase

from game.event import Event, EventHandler, EventCenter


class E1(Event):
    pass


class E2(Event):
    pass


class TestEventHandlerWrapper(TestCase):
    def setUp(self):
        self.ec = EventCenter()

    def testWrapperMethod(self):
        class TestClass(object):
            def __init__(self, ec):
                ec += self.m1
                ec += self.m2

            @EventHandler(E1)
            def m1(self, ev):
                return self

            @EventHandler(E2)
            def m2(self, ev):
                return self

        tc1 = TestClass(self.ec)
        tc2 = TestClass(self.ec)
        self.ec.fire(E1())
