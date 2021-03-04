# coding=utf-8
# @Time : 2020/8/28 17:51
# @Author : 胡泽勇
# ${Description}

from game.castor.icastor import OmnipotentCastor
from game.concept.card import Card
from game.concept.card import CardType
from game.effector.damage_effector import DamageEffector
from game.effector.heal_effector import HealEffector
from game.effector.shield_effector import ModifyShieldEffector
from game.skill.change_every_turn_skill import ChangeEveryTurnSkill, CETSkillInfo
from test.data_prepared_test import WorldPreparedTest


class TestChangeEveryTurnSkill(WorldPreparedTest):
    def testEffect(self):
        self.desLc.lifeState.max = 100
        self.desLc.lifeState.current = 50
        desLife = self.desLc.lifeState.current

        info1 = CETSkillInfo(castor=OmnipotentCastor(), effectors=[HealEffector(value=1)])
        info2 = CETSkillInfo(castor=OmnipotentCastor(), effectors=[DamageEffector(value=1)])
        info3 = CETSkillInfo(castor=OmnipotentCastor(), effectors=[ModifyShieldEffector(value=2)])

        skill = ChangeEveryTurnSkill.skill(infos=[info1, info2, info3])
        skill.attach(self.srcEntity)
        self.srcCc.character.skill = skill

        effector = DamageEffector(value=3)
        damageCard = Card.card(CardType.Support, [effector])
        self.srcCardController.addCard(damageCard)

        self.turnSystem.beginTurn()
        self.srcCc.castSkill(self.desLattice)
        self.turnSystem.endTurn()
        desLife += 1
        self.assertEqual(self.desLc.lifeState.current, desLife)

        self.turnSystem.beginTurn()
        self.srcCc.castSkill(self.desLattice)
        self.turnSystem.endTurn()
        desLife -= 1
        self.assertEqual(self.desLc.lifeState.current, desLife)

        self.turnSystem.beginTurn()
        self.srcCardController.castCard(damageCard.serial, self.desLattice)
        self.srcCc.castSkill(self.desLattice)
        self.turnSystem.endTurn()
        desLife -= 1
        self.assertEqual(self.desLc.lifeState.current, desLife)
