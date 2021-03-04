# coding=utf-8

import logging

from common.serializer.json_serializer import JsonSerializer
from dispatch.dispatcher import Dispatcher
from network.codec.frame_codec import FrameCodec
from network.codec.packet_codec import PacketCodec
from packet.inbound.heart_beat import HeartBeat
from packet.inbound.inbound_packet import InboundPacket


class ChannelInboundHandler(object):
    def __init__(self):
        self.nextor = None

    def handle(self, context, obj):
        if not self.accept(obj):
            self.nextHandle(context, obj)
            return
        self.channelRead(context, obj)

    def nextHandle(self, context, obj):
        if self.nextor:
            self.nextor.handle(context, obj)

    def accept(self, obj):
        raise NotImplementedError

    def channelRead(self, context, obj):
        raise NotImplementedError

    # 如果handlers为空，返回None
    @staticmethod
    def buildChain(handlers):
        for handler in handlers:
            if not isinstance(handler, ChannelInboundHandler):
                raise Exception("Handler registered should extend type<ChannelInboundHandler>")
        chain = ChannelInboundHandler()
        node = chain
        for handler in handlers:
            node.nextor = handler
            node = node.nextor
        chainHeader = chain.nextor
        del chain
        return chainHeader


class DispatchHandler(ChannelInboundHandler):
    def __init__(self):
        super(DispatchHandler, self).__init__()

    def accept(self, obj):
        return isinstance(obj, InboundPacket)

    def channelRead(self, context, obj):
        Dispatcher().dispatch(context, obj)


class HeartBeatHandler(ChannelInboundHandler):
    def __init__(self):
        super(HeartBeatHandler, self).__init__()

    def accept(self, obj):
        return isinstance(obj, HeartBeat)

    def channelRead(self, context, obj):
        pass


class InboundPrintHandler(ChannelInboundHandler):
    def __init__(self, excludedTypes=None):
        ChannelInboundHandler.__init__(self)
        if excludedTypes is None:
            excludedTypes = []
        self.excludedTypes = excludedTypes

    def accept(self, obj):
        return True

    def channelRead(self, context, obj):
        if type(obj) not in self.excludedTypes:
            logging.info("[Channel#{}]Inbound<{}>: {}".format(context.channel.fileno, type(obj).__name__,
                                                              JsonSerializer().serialize(obj)))
        self.nextHandle(context, obj)


class FrameDecoder(ChannelInboundHandler):
    def __init__(self):
        ChannelInboundHandler.__init__(self)

    def accept(self, obj):
        return isinstance(obj, str)

    def channelRead(self, context, obj):
        while True:
            obj, frame = FrameCodec().decode(obj)
            if frame is None:
                break
            channel = context.channel
            if hasattr(channel, 'readBuff'):
                channel.readBuff = obj
            self.nextHandle(context, frame)


class PacketDecoder(ChannelInboundHandler):
    def __init__(self):
        ChannelInboundHandler.__init__(self)

    def accept(self, obj):
        return isinstance(obj, str)

    def channelRead(self, context, obj):
        packet = PacketCodec().decode(obj)
        # packet => InboundPacket
        self.nextHandle(context, packet)
