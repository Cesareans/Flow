# coding=utf-8
# @Time : 2020/8/12 10:20
# @Author : 胡泽勇
# ${Description}
from unittest import TestCase

from prefab.card_prefab import CardPrefab, CardChooser
from registor import Registor


class TestCardPrefab(TestCase):
    @classmethod
    def setUpClass(cls):
        Registor.register()

    def test_load(self):
        CardPrefab()

    def testRandomCard(self):
        card = CardPrefab().randomCard()
        print card


class TestCardChooser(TestCase):
    @classmethod
    def setUpClass(cls):
        Registor.register()

    def testInit(self):
        cardChooser = CardChooser(3, 1)
        cardChooser.choose(1)
        print cardChooser
        pass

    def testRandomCard(self):
        card = CardChooser(3, 1).choose(1)
