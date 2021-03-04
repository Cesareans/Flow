# coding=utf-8
# @Time : 2020/8/22 17:19
# @Author : 胡泽勇
# ${Description}

from game.concept.card import Card
from game.concept.card import CardType
from game.concept.cast_info import CastInfo
from game.effector.lattice_effector import TurnedDamageElementCreator
from game.world_event.decision_event import ClientCastEvent
from test.data_prepared_test import WorldPreparedTest


class TestTurnedDamageElementCreator(WorldPreparedTest):
    def testAliveEffect(self):
        creator = TurnedDamageElementCreator(radius=1, damage=1, turn=2)
        desLife = self.desLc.lifeState.current
        castInfo = CastInfo(self.srcEntity, self.desLattice, 0, Card.card(CardType.Damage, [creator]))

        self.turnSystem.beginTurn()
        self.world.eventCenter.fire(ClientCastEvent(castInfo))
        self.turnSystem.endTurn()
        desLife -= 1
        self.assertEqual(self.desLc.lifeState.current, desLife)

        self.turnSystem.beginTurn()
        self.turnSystem.endTurn()
        desLife -= 1
        self.assertEqual(self.desLc.lifeState.current, desLife)

        self.turnSystem.beginTurn()
        self.turnSystem.endTurn()
        self.assertEqual(self.desLc.lifeState.current, desLife)
