# coding=utf-8
# @Time : 2020/8/16 11:04
# @Author : 胡泽勇
#

from unittest import TestCase

from game.component.card_controller import CardController
from game.component.character_controller import CharacterController
from game.component.effect_chain_controller import EffectChainController
from game.component.life_controller import LifeController
from game.component.move_controller import MoveController
from game.concept.character import Character
from game.concept.coord import AxisCoord
from game.ecs import Entity
from game.skill.iskill import ISkill
from game.system.turn_system import TurnSystem
from game.world import World
from prefab.game_map_prefab import GameMapPrefab
from test.mocked_channel_context import MockedChannelContext


class WorldPreparedTest(TestCase):
    def setUp(self):
        super(WorldPreparedTest, self).setUp()
        srcCharacter = Character.character(skill=ISkill.skill())
        srcMockedContext = MockedChannelContext()
        self.srcMc = MoveController(srcCharacter)
        self.srcCc = CharacterController(srcMockedContext.session.account, srcCharacter)
        self.srcLc = LifeController(srcCharacter.maxLife)
        self.srcCardController = CardController(srcCharacter)
        self.srcECC = EffectChainController()
        self.srcEntity = Entity(0, components=[self.srcMc, self.srcCc, self.srcLc, self.srcCardController, self.srcECC])
        desCharacter = Character.character(skill=ISkill.skill())
        desMockedContext = MockedChannelContext()
        self.desMc = MoveController(desCharacter)
        self.desCc = CharacterController(desMockedContext.session.account, desCharacter)
        self.desLc = LifeController(srcCharacter.maxLife)
        self.desCardController = CardController(desCharacter)
        self.desECC = EffectChainController()
        self.desEntity = Entity(1, components=[self.desMc, self.desCc, self.desLc, self.desCardController, self.desECC])

        self.turnSystem = TurnSystem()
        self.world = World()
        self.world.gameMap = GameMapPrefab().getMap()
        self.world.addSystem(self.turnSystem)

        coord = AxisCoord(row=0, col=0)
        self.srcLattice = self.world.gameMap.getLattice(coord)
        self.srcEntity.coord = coord
        coord = AxisCoord(row=0, col=-1)
        self.desLattice = self.world.gameMap.getLattice(coord)
        self.desEntity.coord = coord

        self.world.addEntity(self.srcEntity)
        self.world.addEntity(self.desEntity)
