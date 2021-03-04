# coding=utf-8
# @Time : 2020/8/11 11:01
# @Author : 胡泽勇
# ${Description}

from game.concept.card import Card, CardType
from game.effect.damage_effect import AlterDamageByValueHandler
from game.effector.damage_effector import DamageEffector, DamageOverTimeEffector, DamageViaCardCastEffector
from game.effector.heal_effector import HealEffector
from game.enum.damage_type import DamageType
from test.data_prepared_test import WorldPreparedTest


# noinspection DuplicatedCode
class TestDamageEffector(WorldPreparedTest):
    def testEffect(self):
        desLife = self.desLc.lifeState.current
        damageEffector = DamageEffector(value=1, damageType=DamageType.Normal)
        damageEffector.effect(self.srcEntity, self.desLattice)
        self.assertEqual(self.desLc.lifeState.current, desLife - 1)

    def testEffectWithHandler(self):
        desLife = self.desLc.lifeState.current
        damageEffector = DamageEffector(value=1, damageType=DamageType.Normal)
        self.srcECC.outboundChains.addHandler(AlterDamageByValueHandler(1))
        self.desECC.inboundChains.addHandler(AlterDamageByValueHandler(-2))
        damageEffector.effect(self.srcEntity, self.desLattice)
        self.assertEqual(self.desLc.lifeState.current, desLife)


class TestDamageOverTimeEffector(WorldPreparedTest):
    def test__alive_effect(self):
        desLife = self.desLc.lifeState.current

        effector = DamageOverTimeEffector(value=1, turn=2, damageType=DamageType.Normal)
        damageCard1 = Card.card(CardType.Damage, [effector])
        self.srcCardController.addCard(damageCard1)

        self.turnSystem.beginTurn()
        self.srcCardController.castCard(damageCard1.serial, self.desLattice)
        self.turnSystem.endTurn()
        desLife -= 1
        self.assertEqual(self.desLc.lifeState.current, desLife)

        self.turnSystem.beginTurn()
        self.turnSystem.endTurn()
        desLife -= 1
        self.assertEqual(self.desLc.lifeState.current, desLife)

        self.turnSystem.beginTurn()
        self.turnSystem.endTurn()
        self.assertEqual(self.desLc.lifeState.current, desLife)


class TestDamageViaCardCastEffector(WorldPreparedTest):
    def testEffect(self):
        multiplier = 1
        basic = 2
        desLife = self.desLc.lifeState.current

        effector = HealEffector(value=1)
        healCard1 = Card.card(CardType.Support, [effector])
        self.srcCardController.addCard(healCard1)
        healCard2 = Card.card(CardType.Support, [effector])
        self.srcCardController.addCard(healCard2)
        healCard3 = Card.card(CardType.Support, [effector])
        self.srcCardController.addCard(healCard3)

        effector = DamageViaCardCastEffector(cardType=CardType.Support, multiplier=multiplier, basic=basic,
                                             damageType=DamageType.Normal)
        damageCard1 = Card.card(CardType.Damage, [effector])
        self.srcCardController.addCard(damageCard1)
        damageCard2 = Card.card(CardType.Damage, [effector])
        self.srcCardController.addCard(damageCard2)

        self.turnSystem.beginTurn()
        self.srcCardController.castCard(healCard1.serial, self.srcLattice)
        self.srcCardController.castCard(healCard2.serial, self.srcLattice)
        self.srcCardController.castCard(healCard3.serial, self.srcLattice)
        self.srcCardController.castCard(damageCard1.serial, self.desLattice)
        self.turnSystem.endTurn()
        desLife -= (multiplier * 3 + basic)
        self.assertEqual(self.desLc.lifeState.current, desLife)

        self.turnSystem.beginTurn()
        self.srcCardController.castCard(damageCard2.serial, self.desLattice)
        self.turnSystem.endTurn()
        desLife -= basic
        self.assertEqual(self.desLc.lifeState.current, desLife)
