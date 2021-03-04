# coding=utf-8
# @Time : 2020/8/8 14:11
# @Author : 胡泽勇
# 数学工具

TOLERANCE = 0.0001


class MathUtil(object):
    # clamp, 不限制m1与m2的大小，将v的值限制在两者之间
    @staticmethod
    def clamp(v, m1, m2):
        if m2 < m1:
            t = m1
            m1 = m2
            m2 = t
        return m1 if v < m1 else m2 if v > m2 else v

    @staticmethod
    def sign(i):
        return 0 if MathUtil.isZero(i) else 1 if i > 0 else -1

    @staticmethod
    def isZero(o):
        return abs(o) < TOLERANCE
