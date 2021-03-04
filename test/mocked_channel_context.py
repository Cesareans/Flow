# coding=utf-8
# @Time : 2020/8/18 14:46
# @Author : 胡泽勇
#

from network.channel.channel import Channel
from network.channel.channel_inbound_handler import \
    ChannelInboundHandler, InboundPrintHandler, \
    DispatchHandler
from network.channel.channel_outbound_handler import \
    ChannelOutboundHandler, OutboundPrintHandler
from network.session import Session
from packet.inbound.heart_beat import HeartBeat
from persist.model.account import Account


class MockedChannel(Channel):
    def __init__(self, context):
        Channel.__init__(self)
        self.context = context


idSerial = -1


class MockedChannelContext(object):
    def __init__(self):
        global idSerial
        self.session = Session()  # 这边的处理逻辑是面向于单台服务器的，不能支持分布式
        mockAccount = Account()
        mockAccount.id = idSerial
        idSerial -= 1
        mockAccount.username = '1'
        self.session.account = mockAccount
        self.channel = MockedChannel(self)
        # 进来的数据序列处理逻辑：解帧（处理封包单帧）->解包->打印->心跳->分发
        self.__inboundHandlerChain = ChannelInboundHandler.buildChain(
            [InboundPrintHandler(excludedTypes=[HeartBeat]),
             DispatchHandler()]
        )
        # 出去的数据序列处理逻辑：打印->封包->发送
        self.__outboundHandlerChain = ChannelOutboundHandler.buildChain(
            [OutboundPrintHandler()]
        )

    def fireInboundHandle(self, obj):
        self.__inboundHandlerChain.handle(self, obj)

    def fireOutboundHandle(self, obj):
        self.__outboundHandlerChain.handle(self, obj)

    def fireCloseHandle(self, obj):
        self.session.close()
