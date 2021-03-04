# coding=utf-8
# @Time : 2020/9/11 17:16
# @Author : 胡泽勇
#

from dispatch.handler.ihandler import IHandler, PacketHandler, CheckLogin
from game.world import AccountWorldMap
from packet.inbound.reconnection_operation import CheckWorld, EnterReconnect


@PacketHandler(CheckWorld)
class CheckWorldHandler(IHandler):
    @CheckLogin
    def handle(self, context, packet):
        account = context.session.account
        world = AccountWorldMap().getAccountWorld(account.id)
        if world is not None and world.alive:
            context.session.gameSession.world = world
            world.wctx.addChannel(account.id, context.channel)
            world.reconnect(context)


@PacketHandler(EnterReconnect)
class EnterReconnectHandler(IHandler):
    @CheckLogin
    def handle(self, context, packet):
        world = context.session.gameSession.world
        world.awakeOn(context)
