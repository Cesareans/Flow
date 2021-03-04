# -*- coding: GBK -*-
import sys

from common.reload.reloader import Reloader
from common.singleton import Singleton
from match.match_space import MatchSpace
from network.channel_host import ChannelHost

sys.path.append('..')


class Server(object):
    __metaclass__ = Singleton

    def __init__(self):
        super(Server, self).__init__()
        self.host = ChannelHost()
        self.worlds = []

    def start(self):
        self.host.start()
        while True:
            self.loop()

    def loop(self):
        self.host.loopPiece()
        MatchSpace().checkMatch()
        Reloader().loopPiece()
        for world in self.worlds:
            world.loopPiece()
        self.worlds = [world for world in self.worlds if world.alive]

    def addWorld(self, world):
        self.worlds.append(world)
