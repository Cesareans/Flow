# coding=utf-8
# @Time : 2020/8/27 14:22
# @Author : 胡泽勇
# ${Description}

from game.castor.icastor import CastorTargetType
from game.concept.card import Card
from game.concept.card import CardType
from game.effector.damage_effector import DamageEffector
from game.effector.dodge_effector import DodgeCardEffectEffector
from test.data_prepared_test import WorldPreparedTest


class TestDodgeCardEffectEffector(WorldPreparedTest):
    def testEffect(self):
        desLife = self.desLc.lifeState.current

        effector = DamageEffector(value=1)
        damageCard1 = Card.card(CardType.Damage, [effector], castTargetType=CastorTargetType.CharacterEntity)
        self.srcCardController.addCard(damageCard1)
        damageCard2 = Card.card(CardType.Damage, [effector], castTargetType=CastorTargetType.CharacterEntity)
        self.srcCardController.addCard(damageCard2)
        damageCard3 = Card.card(CardType.Damage, [effector], castTargetType=CastorTargetType.CharacterEntity)
        self.srcCardController.addCard(damageCard3)

        effector = DodgeCardEffectEffector(probability=1, turn=1)
        dodgeCard = Card.card(CardType.Support, [effector], castTargetType=CastorTargetType.CharacterEntity)
        self.srcCardController.addCard(dodgeCard)

        self.turnSystem.beginTurn()
        self.srcCardController.castCard(dodgeCard.serial, self.desLattice)
        self.srcCardController.castCard(damageCard1.serial, self.desLattice)
        self.srcCardController.castCard(damageCard2.serial, self.desLattice)
        self.turnSystem.endTurn()
        self.assertEqual(self.desLc.lifeState.current, desLife)

        self.turnSystem.beginTurn()
        self.srcCardController.castCard(damageCard3.serial, self.desLattice)
        self.turnSystem.endTurn()
        desLife -= 1
        self.assertEqual(self.desLc.lifeState.current, desLife)

        self.srcCardController.addCard(damageCard1)
        effector = DodgeCardEffectEffector(probability=0, turn=1)
        dodgeCard = Card.card(CardType.Support, [effector])
        self.srcCardController.addCard(dodgeCard)
        self.turnSystem.beginTurn()
        self.srcCardController.castCard(dodgeCard.serial, self.srcLattice)
        self.srcCardController.castCard(damageCard1.serial, self.desLattice)
        self.turnSystem.endTurn()
        desLife -= 1
        self.assertEqual(self.desLc.lifeState.current, desLife)
