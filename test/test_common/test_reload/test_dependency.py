# coding=utf-8
# @Time : 2020/9/14 19:41
# @Author : 胡泽勇
# ${Description}
from unittest import TestCase

from common.reload.dependency import DepGraph


class TestDepGraph(TestCase):
    class TestClass(object):
        def __init__(self, name):
            self.__name__ = name

    def testTraverse(self):
        t1 = self.TestClass("1")
        t2 = self.TestClass("2")
        t3 = self.TestClass("3")
        t4 = self.TestClass("4")
        t5 = self.TestClass("5")
        t6 = self.TestClass("6")
        """                
                           t6
                      - /  | 
                 - /       | 
               /           |
        t1 - t2 - t4      /
         \\     //      /
           - t3 - t5  - 
        """
        dg = DepGraph()
        dg.addDep(t2, t1)
        dg.addDep(t3, t1)
        dg.addDep(t4, t2)
        dg.addDep(t4, t3)
        dg.addDep(t5, t3)
        dg.addDep(t6, t2)
        dg.addDep(t6, t5)

        def printAction(c):
            print c.__name__

        dg.traverse(t3, printAction)
