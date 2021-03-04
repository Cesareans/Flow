# coding=utf-8
# @Time : 2020/8/28 17:32
# @Author : 胡泽勇
# ${Description}

from game.castor.icastor import OmnipotentCastor
from game.concept.card import Card
from game.concept.card import CardType
from game.effector.heal_effector import HealEffector
from game.skill.amith_skill import AmithSkill
from test.data_prepared_test import WorldPreparedTest


class TestConsSkill(WorldPreparedTest):
    def testEffect(self):
        self.desLc.lifeState.max = 100
        self.desLc.lifeState.current = 1
        desLife = self.desLc.lifeState.current

        effector = HealEffector(value=2)
        healCard1 = Card.card(CardType.Support, [effector])
        self.srcCardController.addCard(healCard1)

        skill = AmithSkill.skill(cd=0, castor=OmnipotentCastor(),
                                 cardType=CardType.Support, castCount=2)
        skill.attach(self.srcEntity)
        self.srcCc.character.skill = skill

        # 第一次释放，证明存在护盾
        self.turnSystem.beginTurn()
        self.srcCc.castSkill(self.srcLattice)
        self.srcCardController.castCard(healCard1.serial, self.desLattice)
        self.turnSystem.endTurn()
        desLife += 4
        self.assertEqual(self.desLc.lifeState.current, desLife)

        # 第二次释放，证明技能进入cd
        self.srcCardController.addCard(healCard1)
        self.turnSystem.beginTurn()
        self.srcCardController.castCard(healCard1.serial, self.desLattice)
        self.turnSystem.endTurn()
        desLife += 2
        self.assertEqual(self.desLc.lifeState.current, desLife)
