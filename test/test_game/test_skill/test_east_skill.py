# coding=utf-8
# @Time : 2020/8/28 15:22
# @Author : 胡泽勇
# ${Description}

from game.castor.icastor import OmnipotentCastor
from game.concept.card import Card, CardType
from game.effector.heal_effector import HealEffector
from game.skill.east_skill import EastSkill
from test.data_prepared_test import WorldPreparedTest


class TestEastSkill(WorldPreparedTest):
    def testEffect(self):
        self.desLc.lifeState.max = 100
        self.desLc.lifeState.current = 100
        desLife = self.desLc.lifeState.current

        effector = HealEffector(value=1)
        healCard1 = Card.card(CardType.Support, [effector])
        self.srcCardController.addCard(healCard1)
        healCard2 = Card.card(CardType.Support, [effector])
        self.srcCardController.addCard(healCard2)

        skill = EastSkill.skill(cd=0, castor=OmnipotentCastor(), basic=2,
                                cardTypeToUse=CardType.Support, increase=2)
        skill.attach(self.srcEntity)
        self.srcCc.character.skill = skill

        # 直接释放技能
        self.turnSystem.beginTurn()
        self.srcCc.castSkill(self.desLattice)
        self.turnSystem.endTurn()
        desLife -= 2
        self.assertEqual(self.desLc.lifeState.current, desLife)

        # 释放技能，释放辅助卡，注意技能在辅助卡之前所以此回合并未增加伤害
        self.turnSystem.beginTurn()
        self.srcCc.castSkill(self.desLattice)
        self.srcCardController.castCard(healCard1.serial, self.srcLattice)
        self.turnSystem.endTurn()
        desLife -= 2
        self.assertEqual(self.desLc.lifeState.current, desLife)

        # 释放技能，上回合释放过辅助卡，故伤害进行增加
        self.turnSystem.beginTurn()
        self.srcCc.castSkill(self.desLattice)
        self.turnSystem.endTurn()
        desLife -= 4
        self.assertEqual(self.desLc.lifeState.current, desLife)

        # 释放技能，上回合释放过技能，故伤害恢复
        self.turnSystem.beginTurn()
        self.srcCc.castSkill(self.desLattice)
        self.turnSystem.endTurn()
        desLife -= 2
        self.assertEqual(self.desLc.lifeState.current, desLife)
