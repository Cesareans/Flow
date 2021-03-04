# coding=utf-8
# @Time : 2020/8/27 11:40
# @Author : 胡泽勇
# ${Description}

from game.effector.damage_effector import DamageType, DamageEffector
from game.effector.heal_effector import FullHealIfNoDamageLastTurnEffector, HealByCauseDamageOnceEffector, \
    HealByCauseDamageEffector
from test.data_prepared_test import WorldPreparedTest


class TestFullHealIfNoDamageLastTurnEffector(WorldPreparedTest):
    def testEffect(self):
        desMaxLife = self.desLc.lifeState.max
        desLife = self.desLc.lifeState.current

        self.turnSystem.beginTurn()
        damageOverTimeEffector = DamageEffector(value=2, damageType=DamageType.Normal)
        damageOverTimeEffector.effect(self.srcEntity, self.desLattice)
        self.turnSystem.endTurn()
        desLife -= 2
        self.assertEqual(self.desLc.lifeState.current, desLife)

        self.turnSystem.beginTurn()
        effector = FullHealIfNoDamageLastTurnEffector()
        effector.effect(self.desEntity, self.desLattice)
        self.turnSystem.endTurn()
        self.assertEqual(self.desLc.lifeState.current, desLife)

        self.turnSystem.beginTurn()
        effector = FullHealIfNoDamageLastTurnEffector()
        effector.effect(self.desEntity, self.desLattice)
        self.turnSystem.endTurn()
        desLife = desMaxLife
        self.assertEqual(self.desLc.lifeState.current, desLife)


class TestHealByCauseDamageOnceEffector(WorldPreparedTest):
    def testEffect(self):
        setValue = 1
        self.srcLc.lifeState.current = setValue
        desLife = self.desLc.lifeState.current

        self.turnSystem.beginTurn()
        effector = HealByCauseDamageOnceEffector(turn=1)
        effector.effect(self.srcEntity, self.srcLattice)
        effector = DamageEffector(value=2, damageType=DamageType.Normal)
        effector.effect(self.srcEntity, self.desLattice)
        effector = DamageEffector(value=2, damageType=DamageType.Normal)
        effector.effect(self.srcEntity, self.desLattice)
        self.turnSystem.endTurn()
        desLife -= 4
        setValue += 2
        self.assertEqual(self.desLc.lifeState.current, desLife)
        self.assertEqual(self.srcLc.lifeState.current, setValue)


class TestHealByCauseDamageEffector(WorldPreparedTest):
    def testEffect(self):
        setValue = 1
        self.srcLc.lifeState.current = setValue
        desLife = self.desLc.lifeState.current

        self.turnSystem.beginTurn()
        effector = HealByCauseDamageEffector(turn=1)
        effector.effect(self.srcEntity, self.srcLattice)
        effector = DamageEffector(value=2, damageType=DamageType.Normal)
        effector.effect(self.srcEntity, self.desLattice)
        effector = DamageEffector(value=2, damageType=DamageType.Normal)
        effector.effect(self.srcEntity, self.desLattice)
        self.turnSystem.endTurn()
        desLife -= 4
        setValue += 4
        self.assertEqual(self.desLc.lifeState.current, desLife)
        self.assertEqual(self.srcLc.lifeState.current, setValue)
