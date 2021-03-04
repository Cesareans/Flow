# coding=utf-8
# @Time : 2020/8/12 10:20
# @Author : 胡泽勇
# ${Description}
from unittest import TestCase

from prefab.game_map_prefab import GameMapPrefab
from registor import Registor


class TestCardPrefab(TestCase):
    @classmethod
    def setUpClass(cls):
        Registor.register()

    def test_load(self):
        GameMapPrefab()
