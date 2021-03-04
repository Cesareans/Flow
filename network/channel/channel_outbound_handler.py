# coding=utf-8

import logging
import time

from common.serializer.json_serializer import JsonSerializer
from network.codec.packet_codec import PacketCodec
from packet.packet import Packet


class ChannelOutboundHandler(object):
    def __init__(self):
        self.nextor = None

    def handle(self, context, obj):
        if not self.accept(obj) and self.nextor:
            self.nextor.handle(context, obj)
            return
        self.channelWrite(context, obj)

    def nextHandle(self, context, obj):
        if self.nextor:
            self.nextor.handle(context, obj)

    def accept(self, obj):
        raise NotImplementedError

    def channelWrite(self, context, obj):
        raise NotImplementedError

    # 如果handlers为空，返回None
    @staticmethod
    def buildChain(handlers):
        for handler in handlers:
            if not isinstance(handler, ChannelOutboundHandler):
                logging.warn("Handler registered should extend type<ChannelOutboundHandler>")
                return None
        chain = ChannelOutboundHandler()
        node = chain
        for handler in handlers:
            node.nextor = handler
            node = node.nextor
        chainHeader = chain.nextor
        del chain
        return chainHeader


class PacketIDGenerator(ChannelOutboundHandler):
    def __init__(self):
        super(PacketIDGenerator, self).__init__()
        self.pid = 0

    def accept(self, obj):
        return isinstance(obj, Packet)

    def channelWrite(self, context, obj):
        self.pid += 1
        obj.pid = self.pid
        self.nextHandle(context, obj)


class OutboundPrintHandler(ChannelOutboundHandler):
    def __init__(self, excludedTypes=None, errorTypes=None, errorType=None):
        ChannelOutboundHandler.__init__(self)
        self.errorTypes = [] if errorTypes is None else errorTypes
        self.errorType = errorType
        self.excludedTypes = [] if excludedTypes is None else excludedTypes

    def accept(self, obj):
        return True

    def channelWrite(self, context, obj):
        msg = "[Channel#{}]Outbound<{}>: {}".format(context.channel.fileno, type(obj).__name__,
                                                    JsonSerializer().serialize(obj))
        if type(obj) in self.errorTypes or type(obj) is self.errorType:
            logging.error(msg)
        elif type(obj) not in self.excludedTypes:
            logging.info(msg)
        self.nextHandle(context, obj)


# 模拟慢网
class OutboundSleepHandler(ChannelOutboundHandler):
    def __init__(self, delay):
        ChannelOutboundHandler.__init__(self)
        self.__delay = delay

    def accept(self, obj):
        return True

    def channelWrite(self, context, obj):
        time.sleep(self.__delay)
        self.nextHandle(context, obj)


class PacketEncoder(ChannelOutboundHandler):
    def __init__(self):
        super(PacketEncoder, self).__init__()

    def accept(self, obj):
        return isinstance(obj, Packet)

    def channelWrite(self, context, obj):
        data = PacketCodec().encode(obj)
        self.nextHandle(context, data)


class ThroughPutHandler(ChannelOutboundHandler):
    def __init__(self):
        super(ThroughPutHandler, self).__init__()
        self.time = 0
        self.cnt = 0

    def accept(self, obj):
        return isinstance(obj, str)

    def channelWrite(self, context, obj):
        self.cnt += len(obj)
        if self.time == 0:
            self.time = time.time()
        if time.time() - self.time > 1:
            if self.cnt < 1000:
                logging.info("[Channel#{}]ThroughPut:{} B/s".format(context.channel.fileno, self.cnt))
            else:
                logging.info("[Channel#{}]ThroughPut:{} KB/s".format(context.channel.fileno, self.cnt / 1000))
            self.cnt = 0
            self.time = time.time()
        self.nextHandle(context, obj)


class WriteHandler(ChannelOutboundHandler):
    def __init__(self):
        super(WriteHandler, self).__init__()

    def accept(self, obj):
        return isinstance(obj, str)

    def channelWrite(self, context, obj):
        context.channel.write(obj)
