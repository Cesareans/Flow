# coding=utf-8
# @Time : 2020/8/19 11:33
# @Author : 胡泽勇
#

from dispatch.handler.ihandler import PacketHandler, CheckLogin, IHandler
from game.world_event.loading_event import AccountEnterLoadEvent
from packet.inbound.load_operation import EnterLoad


@PacketHandler(EnterLoad)
class EnterLoadHandler(IHandler):
    @CheckLogin
    def handle(self, context, packet):
        gsn = context.session.gameSession
        account = context.session.account
        gsn.world.eventCenter.fire(AccountEnterLoadEvent(account.id))
