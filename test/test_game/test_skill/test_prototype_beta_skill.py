# coding=utf-8
# @Time : 2020/8/28 11:03
# @Author : 胡泽勇
# ${Description}

from game.castor.icastor import OmnipotentCastor
from game.skill.prototype_beta_skill import PrototypeBetaSkill, PBSkillInfo
from test.data_prepared_test import WorldPreparedTest


class TestPrototypeBetaSkill(WorldPreparedTest):
    def testEffect(self):
        self.desLc.lifeState.max = 100
        self.desLc.lifeState.current = 100
        desLife = self.desLc.lifeState.current
        level1 = PBSkillInfo(damage=3, heal=2, damageNeedToUpLevel=5)
        level2 = PBSkillInfo(damage=5, heal=4, damageNeedToUpLevel=5)
        level3 = PBSkillInfo(damage=7, heal=6, damageNeedToUpLevel=0)
        skill = PrototypeBetaSkill.skill(infos=[level1, level2, level3], castor=OmnipotentCastor())
        skill.attach(self.srcEntity)
        self.srcCc.character.skill = skill

        self.turnSystem.beginTurn()
        self.srcCc.castSkill(self.desLattice)
        self.turnSystem.endTurn()
        desLife -= 3
        self.assertEqual(self.desLc.lifeState.current, desLife)

        self.turnSystem.beginTurn()
        self.srcCc.castSkill(self.desLattice)
        self.turnSystem.endTurn()
        desLife -= 3
        self.assertEqual(self.desLc.lifeState.current, desLife)

        self.turnSystem.beginTurn()
        self.srcCc.castSkill(self.desLattice)
        self.turnSystem.endTurn()
        desLife -= 5
        self.assertEqual(self.desLc.lifeState.current, desLife)

        self.turnSystem.beginTurn()
        self.srcCc.castSkill(self.desLattice)
        self.turnSystem.endTurn()
        desLife -= 7
        self.assertEqual(self.desLc.lifeState.current, desLife)

        self.turnSystem.beginTurn()
        self.srcCc.castSkill(self.desLattice)
        self.turnSystem.endTurn()
        desLife -= 7
        self.assertEqual(self.desLc.lifeState.current, desLife)
