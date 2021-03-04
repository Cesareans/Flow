# coding=utf-8
import logging
import time
import traceback

from base.ireload import IReload
from game.event import EventCenter


class Timer(object):
    def __init__(self):
        self.start = time.time()
        self.prev = time.time()
        self.current = time.time()
        self.lastTurnTime = self.current

    @property
    def delta(self):
        return self.current - self.prev

    @property
    def currentTimeInTurn(self):
        return self.current - self.lastTurnTime

    def tick(self):
        self.prev = self.current
        self.current = time.time()


class WorldContext(object):
    def __init__(self, world):
        self.world = world
        self.nextId = 0
        self.accountIds = []
        self.channels = {}
        self.timer = Timer()

    def generateId(self):
        self.nextId += 1
        res = self.nextId
        return res

    def broadcast(self, obj):
        for channel in self.channels.values():
            channel.context.fireOutboundHandle(obj)

    def singlecast(self, aid, obj):
        if aid in self.channels:
            self.channels[aid].context.fireOutboundHandle(obj)

    def addChannel(self, aid, channel):
        """
        添加账户的通道信息，同时在AccountWorldMap中记录账户与世界的映射信息
        @param aid: 账户id
        @param channel: 账户的连接通道
        """
        self.channels[aid] = channel
        self.accountIds.append(aid)

    def removeChannel(self, aid):
        """
        移除账户的通道信息，不解除账户与世界的映射信息
        @param aid: 账户id
        """
        self.channels.pop(aid, None)

    def close(self):
        self.world = None
        self.channels.clear()


class World(IReload):
    Current = 0

    def __init__(self):
        self.Current += 1
        self.id = self.Current
        self.entities = {}
        self.characterEntities = {}  # 记录在游戏里的玩家角色的实体
        self.systems = []
        self.gameMap = None
        self.wctx = WorldContext(self)
        self.eventCenter = EventCenter()

        self.alive = True
        logging.debug("世界开始运行")
        from network.game_server import Server
        Server().addWorld(self)

    def addSystem(self, system):
        system.world = self
        logging.debug("世界添加系统[{0}]".format(type(system).__name__))
        system.awake()
        self.systems.append(system)

    def addEntity(self, entity):
        entities = self.entities
        entity.world = self
        logging.debug("世界添加实体[id={}]: 包含组件[{}]"
                      .format(entity.id,
                              ','.join([str(c) for c in entity.components.values()]),
                              ))
        entity.awake()
        entities[entity.id] = entity

    def getEntity(self, eid):
        entities = self.entities
        return entities[eid] if eid in entities else None

    def removeEntity(self, eid):
        if eid in self.entities:
            self.entities.pop(eid)

    def reconnect(self, cctx):
        for system in self.systems:
            system.reconnect(cctx)

    # world life cycle
    def awakeOn(self, cctx):
        for system in self.systems:
            system.awakeOn(cctx)
        for entity in self.entities.values():
            entity.awakeOn(cctx)

    def update(self):
        for system in self.systems:
            system.update()

    def loopPiece(self):
        try:
            self.wctx.timer.tick()
            self.update()
            if not self.alive:
                logging.debug("世界停止运行")
                self.destroy(immediate=True)
                self.clearReference()
        except Exception as e:
            logging.error(e)
            logging.error(traceback.format_exc())

    def clearReference(self):
        self.systems = None
        self.entities = None

    def close(self):
        self.wctx.close()
        self.alive = False

    def destroy(self, immediate=False):
        for entity in self.entities.values():
            entity.destroy()
        for system in self.systems:
            system.destroy(immediate)

    def keep(self):
        return self.Current

    def reload(self, keep):
        self.Current = keep
