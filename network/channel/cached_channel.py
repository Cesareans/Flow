import logging
import threading
import time
import traceback

from base import config
from channel import AliveChannel
from channel_context import ChannelContext


class CachedChannel(AliveChannel):
    READ_BATCH = 4096
    WRITE_BATCH = 1024

    def __init__(self, sock):
        AliveChannel.__init__(self, sock)
        self.timeout = config.NET_HOST_DEFAULT_TIMEOUT
        self.wlock = threading.RLock()
        self.context = ChannelContext(self)
        self.readBuff = ''
        self.writeBuff = ''

        self.onClose = []

    def write(self, data):
        self.wlock.acquire()
        self.writeBuff += data
        self.wlock.release()

    def writable(self):
        return len(self.writeBuff) > 0

    def handleRead(self):
        data = self._recv(self.READ_BATCH)
        if data:
            self.readBuff += data
            self._active = time.time()
            self.context.fireInboundHandle(self.readBuff)

    def handleWrite(self):
        sent = self._send(self.writeBuff[:self.WRITE_BATCH])
        self.writeBuff = self.writeBuff[sent:]

    def handleError(self, e):
        logging.warn(traceback.format_exc())

    def handleClose(self, reason):
        self.context.fireCloseHandle(None)
        self.context = None
        logging.info('Cached channel {0} is closed! reason = {1}'.format(self._fileno, reason))
        self._close()
        for onClose in self.onClose:
            onClose()
