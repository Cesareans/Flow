# -*- coding: GBK -*-

import sys

sys.path.append('..')

from network.channel.channel import Channel
from network.channel.cached_channel import CachedChannel
import logging
from base import config
import socket


class ChannelHost(Channel):
    def __init__(self):
        Channel.__init__(self)
        self.count = 0
        self.host = config.HOST
        self.port = config.PORT
        self.maxClient = config.MAX_HOST_CLIENTS_INDEX

    def start(self):
        logging.info("Server start at {0}:{1}".format(self.host, self.port))
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        self._setSocket(sock)
        self._reuseAddress()
        self._bind((self.host, self.port))
        self._listen(self.maxClient)

    def shutdown(self):
        self.handleClose('Host shutdown[from Channel Host]')
        for channel in self.channels:
            if channel is not None:
                channel.handleClose('Host shutdown[from Channel Host]')

    # 通过select当有连接请求时自动调用
    def handleAccept(self):
        pair = self._accept()
        if pair is not None:
            sock, address = pair
            if self.count >= self.maxClient:
                sock.close()
                return
            self.count += 1
            logging.info('Incoming connection from {0}'.format(address))
            handler = CachedChannel(sock)
            handler.onClose.append(self.channelOnClose)

    def channelOnClose(self):
        self.count -= 1

    # todo: 看需求是否需要：获得特定的channel，暂时不需要
    # getClient / closeClient / sendClient


if __name__ == '__main__':
    host = ChannelHost()
    host.start()
