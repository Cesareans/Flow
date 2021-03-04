# coding=utf-8

from network.channel.channel_inbound_handler import \
    ChannelInboundHandler, FrameDecoder, PacketDecoder, InboundPrintHandler, \
    HeartBeatHandler, DispatchHandler
from network.channel.channel_outbound_handler import \
    ChannelOutboundHandler, PacketEncoder, WriteHandler, OutboundPrintHandler
from network.session import Session
from packet.inbound.heart_beat import HeartBeat
from packet.outbound.exception import ExceptionPacket
from packet.outbound.game_synchronize import TurnCountDown


class ChannelContext(object):
    def __init__(self, channel):
        self.channel = channel
        self.session = Session()  # 这边的处理逻辑是面向于单台服务器的，不能支持分布式
        # 进来的数据序列处理逻辑：解帧（处理封包单帧）->解包->打印->心跳->分发
        self.__inboundHandlerChain = ChannelInboundHandler.buildChain(
            [FrameDecoder(), PacketDecoder(),
             InboundPrintHandler(excludedTypes=[HeartBeat]),
             HeartBeatHandler(),
             DispatchHandler()]
        )
        # 出去的数据序列处理逻辑：打印->封包->发送
        self.__outboundHandlerChain = ChannelOutboundHandler.buildChain(
            [OutboundPrintHandler(errorType=ExceptionPacket, excludedTypes=[TurnCountDown]),
             PacketEncoder(), WriteHandler()]
        )

    def fireInboundHandle(self, obj):
        self.__inboundHandlerChain.handle(self, obj)

    def fireOutboundHandle(self, obj):
        self.__outboundHandlerChain.handle(self, obj)

    def fireCloseHandle(self, obj):
        self.session.close()
        self.channel = None
