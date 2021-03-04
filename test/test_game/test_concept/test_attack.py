# coding=utf-8
# @Time : 2020/8/29 15:58
# @Author : 胡泽勇
# ${Description}

from test.data_prepared_test import WorldPreparedTest


class TestAttack(WorldPreparedTest):
    def testAttack(self):
        self.srcCc.character.attack = 4
        self.srcCc.character.buildAttackSkill()
        desLife = self.desLc.lifeState.current

        self.turnSystem.beginTurn()
        self.srcCc.castAttack(self.desLattice)
        self.turnSystem.endTurn()
        desLife -= 4
        self.assertEqual(self.desLc.lifeState.current, desLife)
