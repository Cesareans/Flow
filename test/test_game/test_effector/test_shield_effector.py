# coding=utf-8
# @Time : 2020/8/20 16:52
# @Author : 胡泽勇
# ${Description}

from game.concept.card import Card
from game.concept.card import CardType
from game.concept.cast_info import CastInfo
from game.effector.damage_effector import DamageType, DamageEffector
from game.effector.shield_effector import TurnedShieldEffector
from game.world_event.decision_event import ClientCastEvent
from test.data_prepared_test import WorldPreparedTest


class TestTurnedShieldEffector(WorldPreparedTest):
    def testAliveEffect(self):
        shield, damage = 8, 5
        desLife = self.desLc.lifeState.current
        effector = TurnedShieldEffector(value=shield, turn=2)
        castInfo = CastInfo(self.srcEntity, self.desLattice, 0, Card.card(CardType.Support, [effector]))
        self.world.eventCenter.fire(ClientCastEvent(castInfo))
        damageEffector = DamageEffector(value=damage, damageType=DamageType.Normal)
        castInfo = CastInfo(self.srcEntity, self.desLattice, 0, Card.card(CardType.Damage, [damageEffector]))
        self.world.eventCenter.fire(ClientCastEvent(castInfo))
        self.turnSystem.endTurn()
        self.assertEqual(self.desLc.lifeState.current, desLife)
        self.world.eventCenter.fire(ClientCastEvent(castInfo))
        self.turnSystem.endTurn()
        desLife -= 2
        self.assertEqual(self.desLc.lifeState.current, desLife)
        self.world.eventCenter.fire(ClientCastEvent(castInfo))
        self.turnSystem.endTurn()
        desLife -= 5
        self.assertEqual(self.desLc.lifeState.current, desLife)
