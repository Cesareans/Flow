# coding=utf-8
# @Time : 2020/8/25 13:09
# @Author : 胡泽勇
# ${Description}

from unittest import TestCase

from prefab.equip_prefab import EquipPrefab
from registor import Registor


class TestEquipPrefab(TestCase):
    @classmethod
    def setUpClass(cls):
        Registor.register()

    def test_load(self):
        EquipPrefab().getEquip(1)
