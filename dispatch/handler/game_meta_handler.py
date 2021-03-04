# coding=utf-8

from dispatch.handler.ihandler import PacketHandler, IHandler, CheckGame
from game.world import AccountWorldMap
from packet.inbound.game_synchronize import ExitGame


@PacketHandler(ExitGame)
class ExitGameHandler(IHandler):
    @CheckGame
    def handle(self, context, packet):
        aid = context.session.account.id
        context.session.quitGame()
        AccountWorldMap().detachAccount(aid)
        # todo: 当用户死亡后直接强行关闭游戏，还会进入游戏，并无法再进入大厅
