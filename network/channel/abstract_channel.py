# coding=utf-8

import os
import select
import socket
import time
import warnings
from errno import *

_DISCONNECTED = frozenset((ECONNRESET, ENOTCONN, ESHUTDOWN, ECONNABORTED, EPIPE,
                           EBADF))

# 特性
# 1. 异步IO，通过Select查找就绪的socket，就绪包括 可写可读和异常
# 2. 可自由定义保活机制

channelSet = {}


class ExitNowException(Exception):
    pass


_reraised_exceptions = (ExitNowException, KeyboardInterrupt, SystemExit)


def _strerror(err):
    try:
        return os.strerror(err)
    except (ValueError, OverflowError, NameError):
        if err in errorcode:
            return errorcode[err]
        return "Unknown error %s" % err


def __read(obj):
    try:
        obj.handleReadEvent()
    except _reraised_exceptions:
        raise
    except Exception as e:
        obj.handleError(e)


def __write(obj):
    try:
        obj.handleWriteEvent()
    except _reraised_exceptions:
        raise
    except Exception as e:
        obj.handleError(e)


def __exception(obj):
    try:
        obj.handleExceptionEvent()
    except _reraised_exceptions:
        raise
    except Exception as e:
        obj.handleError(e)


def __notAlive(obj):
    try:
        obj.handleClose('Client not alive [from Abstract Channel]')
    except _reraised_exceptions:
        raise
    except Exception as e:
        obj.handleError(e)


def _poll(timeout=0.5):
    socketMap = channelSet
    if socketMap:
        na = []
        r = []
        w = []
        e = []
        for fd, channel in socketMap.items():
            if not channel.alive():
                na.append(channel)
                continue
            canRead = channel.readable()
            canWrite = channel.writable()
            if canRead:
                r.append(fd)
            if canWrite and not channel.listening:
                w.append(fd)
            if canRead or canWrite:
                e.append(fd)

        if [] == r == w == e:
            time.sleep(timeout)
            return

        try:
            r, w, e = select.select(r, w, e, timeout)
        except select.error, err:
            if err.args[0] != EINTR:
                raise
            else:
                return

        for channel in na:
            __notAlive(channel)

        for fd in r:
            channel = socketMap.get(fd)
            if channel is None:
                continue
            __read(channel)

        for fd in w:
            channel = socketMap.get(fd)
            if channel is None:
                continue
            __write(channel)

        for fd in e:
            channel = socketMap.get(fd)
            if channel is None:
                continue
            __exception(channel)


class AbstractChannel(object):
    def __init__(self, sock=None):
        self._map = channelSet
        self._fileno = None
        self.listening = False
        self.address = None
        self.socket = None
        if sock:
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
            sock.setblocking(False)
            self._setSocket(sock)
            try:
                self.address = sock.getpeername()
            except socket.error as e:
                self.delFromChannelSet()
                raise e

    def __repr__(self):
        status = [self.__class__.__module__ + "." + self.__class__.__name__]
        if self.listening and self.address:
            status.append('listening')
        if self.address is not None:
            try:
                status.append('%s:%d' % self.address)
            except TypeError:
                status.append(repr(self.address))
        return '<%s at %#x>' % (' '.join(status), id(self))

    __str__ = __repr__

    def __getattr__(self, attr):
        try:
            resAttr = getattr(self.socket, attr)
        except AttributeError:
            raise AttributeError("%s instance has no attribute '%s'"
                                 % (self.__class__.__name__, attr))
        else:
            msg = "%(me)s.%(attr)s is deprecated. Use %(me)s.socket.%(attr)s " \
                  "instead." % {'me': self.__class__.__name__, 'attr': attr}
            warnings.warn(msg, DeprecationWarning, stacklevel=2)
            return resAttr

    @property
    def fileno(self):
        return self._fileno

    def addToChannelSet(self):
        self._map[self._fileno] = self

    def delFromChannelSet(self):
        fd = self._fileno
        if fd in self._map:
            self._map.pop(fd)
        self._fileno = None

    def _reuseAddress(self):
        try:
            self.socket.setsockopt(
                socket.SOL_SOCKET, socket.SO_REUSEADDR,
                self.socket.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR) | 1)
        except socket.error:
            pass

    def _setSocket(self, sock):
        if self._fileno is not None:
            self.delFromChannelSet()
        self.socket = sock
        self._fileno = sock.fileno()
        self.addToChannelSet()

    # ==================================================
    # static methods
    # ==================================================

    @staticmethod
    def loopPiece(timeout=0.5):
        _poll(timeout)

    # ==================================================
    # socket object methods.
    # ==================================================

    def _listen(self, num):
        self.listening = True
        return self.socket.listen(num)

    def _bind(self, address):
        self.address = address
        return self.socket.bind(address)

    def _accept(self):
        try:
            pair = self.socket.accept()
        except socket.error as why:
            if why.args[0] in (EWOULDBLOCK, ECONNABORTED, EAGAIN):
                return None
            else:
                raise
        else:
            return pair

    def _send(self, data):
        try:
            result = self.socket.send(data)
            return result
        except socket.error as e:
            if e.args[0] == EWOULDBLOCK:
                return 0
            elif e.args[0] in _DISCONNECTED:
                self.handleClose('Client decline send [from Abstract Channel]')
                return 0
            else:
                raise

    # 以buffer_size接受字节，当远程连接关闭后，该方法将会调用handleClose尝试关闭，并返回空字符串
    def _recv(self, buffer_size):
        try:
            data = self.socket.recv(buffer_size)
            if not data:
                self.handleClose('Recv no data [from Abstract Channel]')
                return ''
            else:
                return data
        except socket.error as e:
            # 处理远程客户端主动断开连接
            if e.args[0] in _DISCONNECTED:
                self.handleClose('Client disconnect [from Abstract Channel]')
                return ''
            else:
                raise

    def _close(self):
        self.listening = False
        self.delFromChannelSet()
        try:
            self.socket.close()
        except socket.error as e:
            if e.args[0] not in (ENOTCONN, EBADF):
                raise

    # ==================================================
    # select处理回调
    # ==================================================

    def handleReadEvent(self):
        if self.listening:
            self.handleAccept()
        self.handleRead()

    def handleWriteEvent(self):
        if self.listening:
            return
        self.handleWrite()

    def handleExceptionEvent(self):
        err = self.socket.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
        if err != 0:
            self.handleClose('Handle Exception [from Abstract Channel]')
        else:
            self.handleException(err)

    # ==================================================
    # 为select提前过滤
    # ==================================================
    # 返回该通道是否活跃，用来进行保活
    def alive(self):
        raise NotImplementedError

    # 返回该通道是否可以读取信息，用来进行select前过滤
    def readable(self):
        raise NotImplementedError

    # 返回该通道是否可以写信息，用来进行select前过滤
    def writable(self):
        raise NotImplementedError

    # ==================================================
    # 关键处理
    # ==================================================
    def handleAccept(self):
        raise NotImplementedError

    def handleRead(self):
        raise NotImplementedError

    def handleWrite(self):
        raise NotImplementedError

    def handleException(self, ex):
        raise NotImplementedError

    def handleError(self, err):
        raise NotImplementedError

    def handleClose(self, reason):
        raise NotImplementedError
