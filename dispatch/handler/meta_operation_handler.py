# coding=utf-8
# @Time : 2020/8/26 16:25
# @Author : 胡泽勇
#

from common.reload.reloader import Reloader
from dispatch.handler.ihandler import PacketHandler, CheckLogin, IHandler
from game.system.lock_load_system import LockLoadSystem
from game.world import World
from game.world_event.loading_event import LoadInfoEvent
from packet.inbound.meta_operation import ReloadPacket, QuickGame


@PacketHandler(ReloadPacket)
class ReloadHandler(IHandler):
    def handle(self, context, packet):
        Reloader().scan()
        Reloader().reload()


@PacketHandler(QuickGame)
class QuickGameHandler(IHandler):
    @CheckLogin
    def handle(self, context, packet):
        gameWorld = World()

        channel = context.channel
        session = channel.context.session
        session.gameSession.world = gameWorld
        aid = session.account.id

        gameWorld.wctx.channels[aid] = channel
        gameWorld.addSystem(LockLoadSystem(1))
        gameWorld.eventCenter.fire(LoadInfoEvent(packet.characterId, channel))
