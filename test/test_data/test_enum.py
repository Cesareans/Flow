# coding=utf-8
# @Time : 2020/8/13 10:01
# @Author : 胡泽勇
# ${Description}

from unittest import TestCase

from base.enum import Enum


class TestEnum(TestCase):
    def test_values(self):
        class Value(Enum):
            i = 1
            j = 2

        self.assertEqual(Value(1), 1)
        self.assertEqual(Value(1), Value.i)
        self.assertNotEqual(Value(1), Value.j)

        self.assertEqual(1, Value(1))
        self.assertEqual(Value.i, Value(1))
        self.assertNotEqual(Value.j, Value(1))

        self.assertEqual(1, Value.i)
        self.assertNotEqual(3, Value.i)

        self.assertEqual(Value.i, 1)
        self.assertNotEqual(Value.i, 3)

        self.assertEqual(Value.i, Value.i)
        self.assertEqual(Value.i, Value(1))

        self.assertEqual(Value.i, Value(Value(1)))
