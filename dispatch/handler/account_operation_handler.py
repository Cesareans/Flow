# coding=utf-8
# @Time : 2020/8/18 11:52
# @Author : 胡泽勇
# 账户信息操作处理器

from dispatch.handler.ihandler import PacketHandler, IHandler, CheckLogin
from packet.inbound.account_operation import FetchAccountInfo, UpdateAccountInfo
from packet.outbound.account_operation_result import FetchAccountInfoResult, UpdateAccountInfoResult
# from persist.model.account import Account, AccountData
from persist.model.account import Account, AccountData


@PacketHandler(FetchAccountInfo)
class FetchAccountInfoHandler(IHandler):
    @CheckLogin
    def handle(self, context, packet):
        account = context.session.account
        context.fireOutboundHandle(FetchAccountInfoResult(AccountData(account)))


@PacketHandler(UpdateAccountInfo)
class UpdateAccountInfoHandler(IHandler):
    @CheckLogin
    def handle(self, context, packet):
        account = context.session.account
        if packet.password is None or len(packet.password) == 0:
            context.channel.fireOutboundHandle(UpdateAccountInfoResult(False, '密码为空'))
            return
        account.password = packet.password
        Account.update(account)
        context.fireOutboundHandle(UpdateAccountInfoResult())
