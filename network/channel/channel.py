# coding=utf-8

import logging
import time

from network.channel.abstract_channel import AbstractChannel


# 这个类为什么命名为channel：channel是个隧道的概念，表示的是一个字节流依序传输
class Channel(AbstractChannel):
    def __init__(self, sock=None):
        AbstractChannel.__init__(self, sock)

    # 表示这个隧道是否活跃，如果return false
    # channel会被abstract channel loop直接因为不活跃关闭
    def alive(self):
        return True

    # 用于筛选是否可读或者可写
    def readable(self):
        return True

    def writable(self):
        return True

    # 可以不管
    def handleAccept(self):
        pass

    def handleException(self, err):
        pass

    def handleRead(self):
        pass

    def handleWrite(self):
        pass

    def handleError(self, e):
        self.handleClose('Client error [from Channel]')

    def handleClose(self, r):
        self._close()


class AliveChannel(Channel):
    def __init__(self, sock):
        Channel.__init__(self, sock)
        self._active = time.time()
        self.timeout = 30

    def alive(self):
        live = time.time() - self._active < self.timeout
        if not live:
            logging.info('Channel {0} have been idle for too long thus have to be closed.'.format(self._fileno))
        return live


class EchoChannel(AliveChannel):
    def handleRead(self):
        data = self._recv(8192)
        if data:
            self._send(data)
            print data
            self._active = time.time()
