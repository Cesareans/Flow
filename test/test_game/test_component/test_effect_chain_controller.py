# coding=utf-8
# @Time : 2020/8/23 15:54
# @Author : 胡泽勇
# ${Description}
from unittest import TestCase

from game.component.effect_chain_controller import EffectChainController


class TestEffectChainController(TestCase):
    def testInit(self):
        ecc = EffectChainController()
