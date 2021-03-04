# coding=utf-8
# @Time : 2020/8/25 13:09
# @Author : 胡泽勇
# ${Description}

from unittest import TestCase

from prefab.character_prefab import CharacterPrefab
from registor import Registor


class TestEquipPrefab(TestCase):
    @classmethod
    def setUpClass(cls):
        Registor.register()

    def test_load(self):
        CharacterPrefab().getCharacter(0)
        CharacterPrefab().getCharacter(1)
        CharacterPrefab().getCharacter(2)
        CharacterPrefab().getCharacter(3)
        CharacterPrefab().getCharacter(4)
        CharacterPrefab().getCharacter(5)
