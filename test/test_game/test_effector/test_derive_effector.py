# coding=utf-8
# @Time : 2020/8/20 10:34
# @Author : 胡泽勇
# ${Description}

from game.effector.card_relevant_effector import SelfDeriveCardEffector
from test.data_prepared_test import WorldPreparedTest


class TestDeriveCardEffector(WorldPreparedTest):
    def testAliveEffect(self):
        deriveCardEffector = SelfDeriveCardEffector(derivedCardId=1)
        self.assertEqual(len(self.srcCardController.cardsInHand()), 0)
        deriveCardEffector.effect(self.srcEntity, self.desLattice)
        self.assertEqual(len(self.srcCardController.cardsInHand()), 1)
