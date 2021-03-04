# coding=utf-8
import logging


class Entity(object):
    def __init__(self, eid, components=None):
        self.id = eid
        self.components = {}
        self.coord = None
        self.world = None
        self.destroyed = False
        if components is not None:
            for component in components:
                self.addComponent(component)

    def addComponent(self, component):
        component.entity = self
        self.components[type(component)] = component
        return component

    def getComponent(self, tp):
        """
        获得类型是tp的component
        @param tp: 需要的component类型，类型：type
        @return: 类型是tp的component，类型：Component
        """
        return self.components[tp] if tp in self.components else None

    def removeComponent(self, tp):
        self.components.pop(tp)

    def awake(self):
        for component in self.components.values():
            component.awake()

    def awakeOn(self, cctx):
        components = sorted(self.components.values(), cmp=lambda c1, c2: c1.SyncOrder - c2.SyncOrder)
        for component in components:
            component.awakeOn(cctx)

    def destroy(self):
        self.destroyed = True
        for component in self.components.values():
            component.destroy()
        self.components.clear()
        self.world.removeEntity(self.id)
        self.world = None
        logging.debug("Entity<{}> destroy.".format(self.id))

    def __repr__(self):
        return "Entity<{}>".format(self.id)

    __str__ = __repr__


class Component(object):
    SyncOrder = 1

    def __init__(self):
        self.entity = None

    def getComponent(self, tp):
        if self.entity is None:
            return None
        return self.entity.getComponent(tp)

    def awake(self):
        pass

    def awakeOn(self, cctx):
        pass

    def destroy(self):
        self.onDestroy()
        self.entity = None

    def onDestroy(self):
        pass

    @property
    def entityId(self):
        if self.entity is None:
            return -1
        return self.entity.id

    @property
    def wctx(self):
        world = self.world
        if world is None:
            return None
        return world.wctx

    @property
    def world(self):
        if self.entity is None:
            return None
        return self.entity.world

    @property
    def timer(self):
        wctx = self.wctx
        if wctx is None:
            return None
        return wctx.timer

    def __repr__(self):
        return type(self).__name__

    __str__ = __repr__


def Components(*args):
    for cls in args:
        assert issubclass(cls, Component)

    def wrapper(entityCls):
        assert issubclass(entityCls, Entity)
        return _ComponentsWrapper(entityCls, args)

    return wrapper


class _ComponentsWrapper(object):
    def __init__(self, entityCls, components):
        self.entityCls = entityCls
        self.components = components

    def __call__(self, *args, **kwargs):
        entity = self.entityCls(*args, **kwargs)
        for c in self.components:
            entity.addComponent(c())
        return entity


class System(object):
    def __init__(self):
        self.world = None
        self.isOverdue = False

    def reconnect(self, cctx):
        pass

    def awakeOn(self, cctx):
        pass

    def awake(self):
        pass

    def update(self):
        pass

    def destroy(self, immediate=False):
        self.onDestroy(immediate)
        self.world = None

    def onDestroy(self, immediate=False):
        pass

    @property
    def wctx(self):
        return self.world.wctx

    @property
    def timer(self):
        return self.wctx.timer
