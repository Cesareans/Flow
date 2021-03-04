# coding=utf-8
# @Time : 2020/8/28 16:48
# @Author : 胡泽勇
# ${Description}

from game.castor.icastor import OmnipotentCastor
from game.concept.card import Card
from game.concept.card import CardType
from game.effector.damage_effector import DamageEffector
from game.effector.heal_effector import HealEffector
from game.skill.anna_skill import AnnaSkill
from test.data_prepared_test import WorldPreparedTest


class TestAmithSkill(WorldPreparedTest):
    def testEffect(self):
        self.desLc.lifeState.max = 100
        self.srcLc.lifeState.max = 100
        self.desLc.lifeState.current = 100
        self.srcLc.lifeState.current = 1
        desLife = self.desLc.lifeState.current

        effector = DamageEffector(value=4)
        damageCard1 = Card.card(CardType.Damage, [effector])
        self.srcCardController.addCard(damageCard1)
        effector = HealEffector(value=10)
        healCard1 = Card.card(CardType.Support, [effector])
        self.srcCardController.addCard(healCard1)

        skill = AnnaSkill.skill(cd=10, castor=OmnipotentCastor(),
                                shield=2, healNeed=8)
        skill.attach(self.srcEntity)
        self.srcCc.character.skill = skill

        # 第一次释放，证明存在护盾
        self.turnSystem.beginTurn()
        self.srcCc.castSkill(self.desLattice)
        self.srcCardController.castCard(damageCard1.serial, self.desLattice)
        self.turnSystem.endTurn()
        desLife -= 2
        self.assertEqual(self.desLc.lifeState.current, desLife)

        # 第二次释放，证明技能进入cd
        self.srcCardController.addCard(damageCard1)
        self.turnSystem.beginTurn()
        self.srcCc.castSkill(self.desLattice)
        self.srcCardController.castCard(damageCard1.serial, self.desLattice)
        self.turnSystem.endTurn()
        desLife -= 4
        self.assertEqual(self.desLc.lifeState.current, desLife)

        # 第三次对自己释放治疗
        self.turnSystem.beginTurn()
        self.srcCc.castSkill(self.desLattice)
        self.srcCardController.castCard(healCard1.serial, self.srcLattice)
        self.turnSystem.endTurn()
        self.assertEqual(self.desLc.lifeState.current, desLife)

        # 第四次释放，通过证明存在护盾测试证明技能恢复cd
        self.srcCardController.addCard(damageCard1)
        self.turnSystem.beginTurn()
        self.srcCc.castSkill(self.desLattice)
        self.srcCardController.castCard(damageCard1.serial, self.desLattice)
        self.turnSystem.endTurn()
        desLife -= 2
        self.assertEqual(self.desLc.lifeState.current, desLife)

        # 第五次对对方释放治疗
        self.srcCardController.addCard(healCard1)
        desLife = self.desLc.lifeState.current = 1
        self.turnSystem.beginTurn()
        self.srcCc.castSkill(self.desLattice)
        self.srcCardController.castCard(healCard1.serial, self.desLattice)
        self.turnSystem.endTurn()
        desLife += 10
        self.assertEqual(self.desLc.lifeState.current, desLife)

        # 第六次释放，通过证明不存在护盾测试证明技能未恢复cd
        self.srcCardController.addCard(damageCard1)
        self.turnSystem.beginTurn()
        self.srcCc.castSkill(self.desLattice)
        self.srcCardController.castCard(damageCard1.serial, self.desLattice)
        self.turnSystem.endTurn()
        desLife -= 4
        self.assertEqual(self.desLc.lifeState.current, desLife)
