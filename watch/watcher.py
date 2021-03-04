# coding=utf-8
# @Time : 2020/9/17 21:16
# @Author : 胡泽勇
#
import gc
import logging
import threading
import time
from collections import deque

import watch.settings as settings
from base.data import Data, Prototype
from common.project_path import ProjectPath
from common.serializer.json_serializer import JsonSerializer
from game.ecs import Entity, System, Component
from game.world import World

try:
    canSend = True
    import requests
except ImportError:
    requests = None
    canSend = False


class ServerFrame(Data):
    def __init__(self):
        self.timestamp = 0
        self.clients = 0
        self.objCnt = Prototype()
        self.worldEntityCnt = {}


class Watcher(threading.Thread):
    CollectInterval = 2
    EnableLog = False
    EnableSend = True
    EnableCheckCycleReference = False

    def __init__(self, server):
        super(Watcher, self).__init__()
        self.name = "Watcher Thread"
        self.daemon = True
        self.server = server
        self.frames = deque()
        if not canSend:
            logging.error("Module requests is not import.")

    def run(self):
        while True:
            time.sleep(self.CollectInterval)
            self.collectFrame()
            if self.EnableSend and canSend:
                self.send()
            if self.EnableCheckCycleReference:
                self.checkCycleReference()

    def collectFrame(self):
        frame = ServerFrame()
        frame.timestamp = time.time()

        frame.objCnt.clients = self.server.host.count
        frame.objCnt.activeWorld = len(self.server.worlds)
        frame.objCnt.allWorld = len([ref for ref in gc.get_referrers(World) if type(ref) == World])
        frame.objCnt.allEntity = len([ref for ref in gc.get_referrers(Entity) if type(ref) == Entity])
        frame.objCnt.allComponent = self.getSubclassCnt(Component)
        frame.objCnt.allSystem = self.getSubclassCnt(System)

        frame.worldEntityCnt = {world.id: Prototype(entities=len(world.entities), tick=world.wctx.timer.delta)
                                for world in self.server.worlds}
        if self.EnableLog:
            self.log(frame)
        self.frames.append(frame)

    def send(self):
        try:
            while len(self.frames) > 0:
                frame = self.frames.popleft()
                requests.post(settings.SEND_PATH,
                              params={'username': 'cesare'},
                              data=JsonSerializer().serialize(frame))
        except Exception as e:
            return

    def log(self, frame):
        line1 = "\nBegin Frame # {}".format(frame.timestamp)
        objCnt = frame.objCnt
        line2 = "Host channel connected count : {}".format(objCnt.clients)
        line3 = "Active world count : {}.      All world count: {}".format(objCnt.activeWorld, objCnt.allWorld)
        line4 = "All entity count: {}.      All component count: {}.      All system count: {}.".format(
            objCnt.allEntity, objCnt.allComponent, objCnt.allSystem)
        lines = ["World # {} : Entity Count<{}>.  Tick<{}>".format(wid, obj.entities, obj.tick)
                 for wid, obj in frame.worldEntityCnt.items()]
        msgs = [line1, line2, line3, line4]
        msgs.extend(lines)
        logging.info("\n".join(msgs))

    @staticmethod
    def getSubclassCnt(tp):
        subClasses, cnt = tp.__subclasses__(), 0
        for cls in subClasses:
            cnt += len([ref for ref in gc.get_referrers(cls) if type(ref) == cls])
        return cnt

    @staticmethod
    def checkCycleReference():
        try:
            import objgraph
        except ImportError:
            return
        # for tp in objgraph.by_type("Entity"):
        #     filename = ProjectPath().filepath("output", 'chain_{}.png'.format(time.time()))
        #     objgraph.show_backrefs(tp, max_depth=10, filename=filename)
        logging.debug(objgraph.by_type("Entity"))
        filename = ProjectPath().filepath("output", 'chain_{}.png'.format(time.time()))
        objgraph.show_refs(objgraph.by_type("Entity"), max_depth=10, filename=filename)
