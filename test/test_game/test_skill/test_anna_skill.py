# coding=utf-8
# @Time : 2020/8/28 13:58
# @Author : 胡泽勇
# ${Description}

from game.castor.icastor import OmnipotentCastor
from game.concept.card import Card
from game.concept.card import CardType
from game.effector.damage_effector import DamageEffector
from game.skill.cons_skill import ConsSkill
from test.data_prepared_test import WorldPreparedTest


class TestAnnaSkill(WorldPreparedTest):
    def testEffect(self):
        self.desLc.lifeState.max = 100
        self.desLc.lifeState.current = 100
        desLife = self.desLc.lifeState.current

        effector = DamageEffector(value=1)
        damageCard1 = Card.card(CardType.Damage, [effector])
        self.srcCardController.addCard(damageCard1)
        damageCard2 = Card.card(CardType.Damage, [effector])
        self.srcCardController.addCard(damageCard2)

        skill = ConsSkill.skill(castor=OmnipotentCastor(), damage=1, cd=4,
                                cardTypeToUse=CardType.Damage, cardCountToUse=2)
        skill.attach(self.srcEntity)
        self.srcCc.character.skill = skill

        self.turnSystem.beginTurn()
        self.srcCc.castSkill(self.desLattice)
        self.turnSystem.endTurn()
        desLife -= 1
        self.assertEqual(self.desLc.lifeState.current, desLife)

        # turn 1
        self.turnSystem.beginTurn()
        self.srcCc.castSkill(self.desLattice)
        self.turnSystem.endTurn()
        self.assertEqual(self.desLc.lifeState.current, desLife)

        # turn 2
        self.turnSystem.beginTurn()
        self.srcCc.castSkill(self.desLattice)
        self.srcCardController.castCard(damageCard1.serial, self.desLattice)
        self.turnSystem.endTurn()
        desLife -= 1
        self.assertEqual(self.desLc.lifeState.current, desLife)

        # turn 3
        self.turnSystem.beginTurn()
        self.srcCc.castSkill(self.desLattice)
        self.srcCardController.castCard(damageCard2.serial, self.desLattice)
        self.turnSystem.endTurn()
        desLife -= 1
        self.assertEqual(self.desLc.lifeState.current, desLife)

        # turn 4
        self.turnSystem.beginTurn()
        self.srcCc.castSkill(self.desLattice)
        self.turnSystem.endTurn()
        desLife -= 1
        self.assertEqual(self.desLc.lifeState.current, desLife)
