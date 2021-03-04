# coding=utf-8
# @Time : 2020/8/20 13:42
# @Author : 胡泽勇
# ${Description}

from game.concept.card import Card, CardType
from game.effector.heal_effector import HealEffector
from game.effector.life_effector import SetCurrentLifeEffector, SetMaxLifeEffector, TempModifyMaxLifeEffector
from test.data_prepared_test import WorldPreparedTest


class TestModifyCurrentLifeEffector(WorldPreparedTest):
    def testAliveEffect(self):
        self.aliveEffect(1)
        self.aliveEffect(10)
        self.aliveEffect(20)
        self.aliveEffect(30)

    def aliveEffect(self, targetValue):
        desMaxLife = self.desLc.lifeState.max
        mcle = SetCurrentLifeEffector(value=targetValue)
        mcle.effect(self.srcEntity, self.desLattice)
        if targetValue > desMaxLife:
            self.assertEqual(self.desLc.lifeState.current, desMaxLife)
        else:
            self.assertEqual(self.desLc.lifeState.current, targetValue)
        self.assertEqual(self.desLc.lifeState.max, desMaxLife)


class TestModifyMaxLifeEffector(WorldPreparedTest):
    def testAliveEffect(self):
        self.aliveEffect(1)
        self.aliveEffect(10)
        self.aliveEffect(20)
        self.aliveEffect(30)

    def aliveEffect(self, targetValue):
        desLife = self.desLc.lifeState.current
        mcle = SetMaxLifeEffector(value=targetValue)
        mcle.effect(self.srcEntity, self.desLattice)
        self.assertEqual(self.desLc.lifeState.max, targetValue)
        if targetValue < desLife:
            self.assertEqual(self.desLc.lifeState.current, targetValue)
        else:
            self.assertEqual(self.desLc.lifeState.current, desLife)


class TestTempModifyMaxLifeEffector(WorldPreparedTest):
    def testEffect(self):
        desLife = self.desLc.lifeState.current

        self.turnSystem.beginTurn()
        effector = TempModifyMaxLifeEffector(value=5, turn=-1)
        card1 = Card.card(CardType.Support, [effector])
        self.srcCardController.addCard(card1)

        effector = HealEffector(value=1)
        healCard1 = Card.card(CardType.Support, [effector])
        self.srcCardController.addCard(healCard1)

        self.turnSystem.beginTurn()
        self.srcCardController.castCard(healCard1.serial, self.desLattice)
        self.turnSystem.endTurn()
        self.assertEqual(self.desLc.lifeState.current, desLife)

        self.srcCardController.addCard(healCard1)
        self.turnSystem.beginTurn()
        self.srcCardController.castCard(card1.serial, self.desLattice)
        self.srcCardController.castCard(healCard1.serial, self.desLattice)
        self.turnSystem.endTurn()
        desLife += 1
        self.assertEqual(self.desLc.lifeState.current, desLife)
