# coding=utf-8
# @Time : 2020/8/14 14:35
# @Author : 胡泽勇
#

from dispatch.handler.ihandler import PacketHandler, IHandler, CheckGame
from game.component.card_controller import CardController
from game.effect.card_relevant_effect import GetCardEffect
from game.effect.operation_effect import CastCardOperation, CastAttackOperation, CastSkillOperation, MoveOperation
from game.world_event.decision_event import ClientEndDecisionEvent
from packet.inbound.game_synchronize import \
    Move, CastSkill, CastAttack, CastCard, CancelCastCard, ChooseCard, DiscardCard, EndDecision
from packet.outbound.exception import \
    LatticeNotExistException, CannotChooseException, LatticeIsNotWalkableException
from packet.outbound.game_synchronize import AvailableCardsEnd


@PacketHandler(Move)
class MoveHandler(IHandler):
    @CheckGame
    def handle(self, context, packet):
        gsn = context.session.gameSession
        gameMap = gsn.world.gameMap
        entity = gsn.characterEntity
        for coord in packet.paths:
            lattice = gameMap.getLattice(coord)
            if lattice is None or not lattice.walkable:
                gsn.world.wctx.broadcast(LatticeIsNotWalkableException())
                return
        MoveOperation.impact(entity, entity, paths=packet.paths)


@PacketHandler(CastCard)
class CastCardHandler(IHandler):
    @CheckGame
    def handle(self, context, packet):
        gsn = context.session.gameSession
        gameMap = gsn.world.gameMap
        entity = gsn.characterEntity
        lattice = gameMap.getLattice(packet.coord)
        if lattice is None:
            gsn.world.wctx.broadcast(LatticeNotExistException())
            return
        # 自己让自己释放卡牌，所以第二个参数为entity
        CastCardOperation.impact(entity, entity, serial=packet.serial, lattice=lattice)


@PacketHandler(CastSkill)
class CastSkillHandler(IHandler):
    @CheckGame
    def handle(self, context, packet):
        gsn = context.session.gameSession
        gameMap = gsn.world.gameMap
        entity = gsn.characterEntity
        lattice = gameMap.getLattice(packet.coord)
        if lattice is None:
            gsn.world.wctx.broadcast(LatticeNotExistException())
            return
        # 自己让自己释放卡牌，所以第二个参数为entity
        CastSkillOperation.impact(entity, entity, lattice=lattice)


@PacketHandler(CastAttack)
class CastAttackHandler(IHandler):
    @CheckGame
    def handle(self, context, packet):
        gsn = context.session.gameSession
        gameMap = gsn.world.gameMap
        entity = gsn.characterEntity
        lattice = gameMap.getLattice(packet.coord)
        if lattice is None:
            gsn.world.wctx.broadcast(LatticeNotExistException())
            return
        # 自己让自己进行攻击，所以第二个参数为entity
        CastAttackOperation.impact(entity, entity, lattice=lattice)


@PacketHandler(CancelCastCard)
class CancelCastCardHandler(IHandler):
    @CheckGame
    def handle(self, context, packet):
        gsn = context.session.gameSession
        characterEntity = gsn.characterEntity
        cardController = characterEntity.getComponent(CardController)
        cardController.cancelCastCard(packet.serial)


@PacketHandler(ChooseCard)
class ChooseCardHandler(IHandler):
    @CheckGame
    def handle(self, context, packet):
        gsn = context.session.gameSession
        characterEntity = gsn.characterEntity
        cardController = characterEntity.getComponent(CardController)
        cardChooser = cardController.cardChooser
        for idx in packet.indexes:
            if cardChooser.cardNotAvailable(idx):
                context.fireOutboundHandle(CannotChooseException())
                return
            card = cardChooser.choose(idx)
            GetCardEffect.impact(characterEntity, characterEntity, card=card)
        cardChooser.hasChosen = True
        context.fireOutboundHandle(AvailableCardsEnd(characterEntity.id))


@PacketHandler(DiscardCard)
class DiscardCardHandler(IHandler):
    @CheckGame
    def handle(self, context, packet):
        gsn = context.session.gameSession
        characterEntity = gsn.characterEntity
        cardController = characterEntity.getComponent(CardController)
        if cardController is not None:
            cardController.removeCard(packet.serial)


@PacketHandler(EndDecision)
class EndDecisionHandler(IHandler):
    @CheckGame
    def handle(self, context, packet):
        gsn = context.session.gameSession
        characterEntity = gsn.characterEntity
        gsn.world.eventCenter.fire(ClientEndDecisionEvent(characterEntity.id))
