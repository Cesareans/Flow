# coding=utf-8
# @Time : 2020/8/18 15:55
# @Author : 胡泽勇
#

from dispatch.handler.ihandler import PacketHandler, IHandler, CheckGame
from game.world_event.pick_event import PickEvent, ConfirmPickEvent, EnterPickEvent
from packet.inbound.pick_operation import EnterPick, PickCharacter, ConfirmPick


@PacketHandler(EnterPick)
class EnterPickHandler(IHandler):
    @CheckGame
    def handle(self, context, packet):
        channel = context.channel
        gsn = context.session.gameSession
        gsn.world.eventCenter.fire(EnterPickEvent(channel))


@PacketHandler(PickCharacter)
class PickCharacterHandler(IHandler):
    @CheckGame
    def handle(self, context, packet):
        channel = context.channel
        gsn = context.session.gameSession
        gsn.world.eventCenter.fire(PickEvent(channel, packet.characterId))


@PacketHandler(ConfirmPick)
class ConfirmPickHandler(IHandler):
    @CheckGame
    def handle(self, context, packet):
        channel = context.channel
        gsn = context.session.gameSession
        gsn.world.eventCenter.fire(ConfirmPickEvent(channel))
