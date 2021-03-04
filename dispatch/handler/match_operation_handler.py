# coding=utf-8
# @Time : 2020/8/18 12:00
# @Author : 胡泽勇
#

from dispatch.handler.ihandler import PacketHandler, CheckLogin, IHandler
from match.match_space import MatchSpace, MatchInfo
from packet.inbound.match_operation import BeginMatch, CancelMatch
from packet.outbound.match_operation_result import BeginMatchResult, CancelMatchResult


@PacketHandler(BeginMatch)
class BeginMatchHandler(IHandler):
    @CheckLogin
    def handle(self, context, packet):
        channel = context.channel
        if context.session.matchInfo is not None:
            context.fireOutboundHandle(BeginMatchResult(False, "已经在匹配队列内"))
            return
        matchInfo = MatchInfo(channel, context.session.account)
        context.session.matchInfo = matchInfo
        MatchSpace().addMatchInfo(matchInfo)
        context.fireOutboundHandle(BeginMatchResult(True, "成功"))


@PacketHandler(CancelMatch)
class CancelMatchHandler(IHandler):
    @CheckLogin
    def handle(self, context, packet):
        matchInfo = context.session.matchInfo
        if matchInfo is None:
            context.fireOutboundHandle(CancelMatchResult(False, "尚未进入匹配"))
            return
        MatchSpace().removeMatchInfo(matchInfo)
        context.session.matchInfo = None
        context.fireOutboundHandle(CancelMatchResult(True, "成功"))
