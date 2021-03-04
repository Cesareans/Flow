# coding=utf-8
# @Time : 2020/8/13 10:38
# @Author : 胡泽勇
# ${Description}

from game.concept.cast_info import CastInfo, GeneralCast
from game.effector.damage_effector import DamageType, DamageEffector
from game.world_event.decision_event import ClientCastEvent, ClientCancelCastEvent
from test.data_prepared_test import WorldPreparedTest


# noinspection DuplicatedCode
class TestTurnSystem(WorldPreparedTest):

    def testSettle(self):
        desLife = self.desLc.lifeState.current
        nde = DamageEffector(value=1, damageType=DamageType.Normal)
        castTarget = self.desLattice
        castInfo = CastInfo(self.srcEntity, castTarget, 0, GeneralCast([nde]))
        self.turnSystem.addCastInfo(castInfo)
        self.turnSystem.endTurn()
        desLife -= 1
        self.assertEqual(self.desLc.lifeState.current, desLife)

    def testHandleCastCard(self):
        desLife = self.desLc.lifeState.current
        nde = DamageEffector(value=1, damageType=DamageType.Normal)
        castTarget = self.desLattice
        castInfo = CastInfo(self.srcEntity, castTarget, 0, GeneralCast([nde]))
        self.world.eventCenter.fire(ClientCastEvent(castInfo))
        self.turnSystem.endTurn()
        desLife -= 1
        self.assertEqual(self.desLc.lifeState.current, desLife)

    def testCancelHandleCastCard(self):
        desLife = self.desLc.lifeState.current
        nde = DamageEffector(value=1, damageType=DamageType.Normal)
        castTarget = self.desLattice
        castInfo = CastInfo(self.srcEntity, castTarget, 0, GeneralCast([nde]))
        self.world.eventCenter.fire(ClientCastEvent(castInfo))
        self.world.eventCenter.fire(ClientCancelCastEvent(castInfo))
        self.turnSystem.endTurn()
        self.assertEqual(self.desLc.lifeState.current, desLife)
