# coding=utf-8
import logging

from dispatch.handler.ihandler import IHandler, PacketHandler
from network.account_context import AccountContext
from packet.inbound.authentication import LoginPacket, LogoutPacket, RegisterPacket
from packet.outbound.authentication_result import LoginResultPacket, RegisterResultPacket
from persist.model.account import Account


# from persist.model.account_new import Account


@PacketHandler(LoginPacket)
class LoginHandler(IHandler):
    def handle(self, context, packet):
        if packet.username is None:
            packet.username = ''
        if packet.password is None:
            packet.password = ''
        account = Account.selectUnique(username=packet.username)
        if account is None or account.password != packet.password:
            logging.debug("用户({0})登录失败".format(packet.username))
            context.fireOutboundHandle(LoginResultPacket(False, '用户名或密码错误'))
            return

        if account.id in AccountContext().logonAccount:
            logging.debug("用户({0})登录失败".format(packet.username))
            context.fireOutboundHandle(LoginResultPacket(False, '账户已经登录'))
            return

        logging.debug("用户({0})登录成功".format(packet.username))
        context.session.account = account
        context.fireOutboundHandle(LoginResultPacket())


@PacketHandler(LogoutPacket)
class LogoutHandler(IHandler):
    def handle(self, context, packet):
        context.session.close()


@PacketHandler(RegisterPacket)
class RegisterHandler(IHandler):
    def handle(self, context, packet):
        if packet.username is None:
            packet.username = ''
        if packet.password is None:
            packet.password = ''
        if len(packet.username) == 0 or len(packet.password) == 0:
            context.fireOutboundHandle(RegisterResultPacket(False, '用户名或密码为空'))
            return
        account = Account.selectUnique(username=packet.username)
        if account is not None:
            context.fireOutboundHandle(RegisterResultPacket(False, '用户名已存在'))
            return
        account = Account()
        account.username = packet.username
        account.password = packet.password
        Account.insert(account)
        context.fireOutboundHandle(RegisterResultPacket())
