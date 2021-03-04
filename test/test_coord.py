# coding=utf-8
# @Time : 2020/8/8 14:02
# @Author : 胡泽勇
# ${Description}
import sys

sys.path.append("../")
from game.concept.coord import AxisCoord
from unittest import TestCase


class TestAxisCoord(TestCase):
    def testDistance(self):
        c1 = AxisCoord.fromCubic(1, -1, 0)
        c2 = AxisCoord.fromCubic(-3, 1, 2)

        self.assertEqual(c1.distance(c2), 4)

    def testRing(self):
        center = AxisCoord(col=1, row=-1)
        for i in center.ring(1):
            print i
