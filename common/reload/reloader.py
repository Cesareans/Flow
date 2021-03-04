# coding=utf-8
# @Time : 2020/8/26 16:37
# @Author : 胡泽勇
# 热更新工具
# 参考自： https://www.indelible.org/ink/python-reloading/
import gc
import importlib
import logging
import os
import sys
import time
from types import ModuleType, TypeType, FunctionType

from base.ireload import IReload
from common.project_path import ProjectPath
from common.reload.dependency import DepGraph
from common.singleton import Singleton
from common.util.reflection_util import ReflectionUtil


class ModuleInfo(object):
    def __init__(self, modulePath, module):
        self.filepath = getattr(module, '__file__')
        self.modulePath = modulePath
        self.module = module


class BoundInfo(object):
    def __init__(self, bound, dic):
        self.oldBound = bound
        self.dic = dic


class ReferrerInfo(object):
    def __init__(self, obj, keep):
        self.obj = obj
        self.keep = keep


# 1. 热更不能多线程，否则可能导致类级别方法代码不能及时更新
# 2. 不支持 from ... import [值]等
# 3. 暂时只实现了模块级别  类的深度热更新，暂未
# 4. 注意到方法和类在热更新前后哈希值以及equal等都会发生变化，故不能直接以其型作为key
# 5. 对于每个类的对象，在创建后，所有的类级别method都会进行bound并且分配独立地址
# 6. 所以实际上类对象的bound method不会在热更后改变地址
# 7. metaclass __new__会被重新执行，且metaclass中新建的字段在热更新后均会消失.
#    => 请不要使用metaclass实现单例. 或者Singleton应该保存一份instance引用词典
# 8. 类热更新后，任意持有的旧的类的缓存应该进行刷新
class Reloader(object):
    __metaclass__ = Singleton

    def __init__(self, interval=5):
        # 热更新监测
        self.__remainReload = {}
        self.__modifyTimes = {}
        self.__timer = time.time()
        self.__interval = interval
        # 热更新记录依赖
        self.depGraph = DepGraph()
        self.__blacklist = set()
        self.__depBlackList = {"test", ".idea", "reload"}
        self.__excludedModule = {"__builtin__", "sys", "inspect", "logging", "os"}
        self.__clsType = {TypeType, Singleton}
        # 热更新配置
        self.__inplaceUpdate = True  # 原地更新，用于配置是否需要在热更新时使得方法保持原有的地址。如维持回调等
        self.__clsUpdateExcluded = {"__doc__", "__dict__", "__weakref__"}
        self.build()
        pass

    def loopPiece(self):
        if time.time() - self.__timer > self.__interval:
            self.__timer = time.time()
            self.scan()

    def build(self):
        self.__visitPath(ProjectPath().path, [])

    def __visitPath(self, parent, modulePath):
        for sub in os.listdir(parent):
            path = os.path.join(parent, sub)
            # 对于文件夹进行遍历
            if os.path.isdir(path) and sub not in self.__depBlackList:
                modulePath.append(sub)
                self.__visitPath(path, modulePath)
                modulePath.pop()
            # python文件则进行导入
            elif sub.endswith('.py') and not sub.endswith('__init__.py'):
                modulePath.append(sub.partition('.')[0])
                path = ".".join(modulePath)
                module = importlib.import_module(path)
                for key in dir(module):
                    # 跳过模块设置的内置函数或者设置的non-public模块（原则上non-public必定不是来自其他模块，故无依赖）
                    if key.startswith("_"):
                        continue
                    self.__visitBound(module, getattr(module, key))
                modulePath.pop()

    def __visitBound(self, module, bound):
        """
        Module import bound as local. So module depends on bound = bound has module as relier
        @param module: The specified module that we are detecting dependencies.
        @param bound: The dependency of the module, which has been imported before.
        """
        if type(bound) is TypeType:
            if module.__name__ == bound.__module__:
                return
            boundModule = importlib.import_module(bound.__module__)
        elif type(bound) is ModuleType:
            boundModule = bound
        else:
            return
        # 排除设置的不进行热更新的模块
        if boundModule.__name__ in self.__excludedModule:
            return
        # 判断是否已经记录了依赖
        if self.depGraph.hasDep(module, boundModule):
            return
        # 若没有记录依赖，则进行记录
        self.depGraph.addDep(module, boundModule)

    def scan(self):
        # 只处理文件式模块，且只读取已经加载入python的模块
        # sys.modules: 包含从Python运行起被导入的所有模块的缓存，而自带模块在启动时就加载好了
        moduleInfos = [ModuleInfo(path, node.module)
                       for path, node in self.depGraph.nodes.items()
                       if hasattr(node.module, "__file__")]
        for moduleInfo in moduleInfos:
            filepath = moduleInfo.filepath
            # 如果是pyc或者pyo则移除尾缀
            if filepath.endswith('.pyc') or filepath.endswith('.pyo'):
                filepath = filepath[:-1]

            # 获得文件的信息
            try:
                stat = os.stat(filepath)
            except OSError:
                continue

            # 获得修改时间
            modifyTime = stat.st_mtime

            # 查看文件是否在记录内
            if filepath in self.__modifyTimes:
                # 看修改时间是否变化
                if modifyTime != self.__modifyTimes[filepath]:
                    logging.info("Monitor detected file<{}> has been modified.".format(filepath))
                    self.__remainReload[filepath] = moduleInfo
            # 更新文件的修改时间，修改时间相同时其实相当于没有修改，放这里统一修改与新建记录
            self.__modifyTimes[filepath] = modifyTime

    def reload(self):
        for moduleInfo in self.__remainReload.values():
            self.__reload(moduleInfo.module)
        self.__remainReload.clear()

    def __reload(self, module):
        logging.info("Reloader begin reload module<{}>.".format(module.__name__))
        name = module.__name__
        if name in self.__blacklist:
            return
        # 基于依赖图，进行拓扑遍历，并执行指定的__reloadAction
        # self.depGraph.traverse(module, self.__reloadAction)
        self.__reloadAction(module)

    def __reloadAction(self, module):
        logging.debug("Begin reload module<{}>".format(module.__name__))

        # 进行模块更新
        # 在sys.modules里头，a.b.c模块
        # 会有sys.modules['a'].b.c sys.modules['a.b'].c sys.modules['a.b.c']三级缓存
        moduleLevels = module.__name__.split('.')
        modules = ['.'.join(moduleLevels[0:i + 1]) for i in xrange(len(moduleLevels))]
        # 用新的模块替换缓存中的旧的模块 = sys.modules.pop + __import__
        # 故需要注意缓存旧模块，并再最后进行旧模块->新模块的替换
        sys.modules.pop(module.__name__)
        newModule = importlib.import_module(module.__name__)
        # 根据新模块对旧模块的引用对象进行更新
        for key in dir(newModule):
            # bound 指的是模块内对象，如全局变量、方法、类等
            bound = getattr(newModule, key)
            # 非模块内声明  或   非类
            if type(bound) in self.__clsType and bound.__module__ == module.__name__:
                # 更新类
                self.__updateCls(newModule, module, key)
            # 更新方法
            elif type(bound) is FunctionType:
                newFunc = getattr(newModule, key)
                oldFunc = getattr(module, key)
                ReflectionUtil.replaceFunc(newFunc, oldFunc)
            # 更新基本类型
            elif not hasattr(bound, '__dict__'):
                # 对于基本类型并不能进行原地更新，实际上地址还是会发生变化，故不能进行基本类型的from ... import ...
                setattr(module, key, bound)
        sys.modules[module.__name__] = module
        if len(modules) >= 2:
            setattr(sys.modules[modules[-2]], module.__name__, module)
        # todo: remove old object whose class have been deleted.

    def __updateCls(self, newModule, oldModule, key):
        oldBound = getattr(oldModule, key)
        newBound = getattr(newModule, key)
        # 寻找声明的类的gc引用对象
        objs = [ref for ref in gc.get_referrers(oldBound) if type(ref) == oldBound]
        boundReferrers = [
            ReferrerInfo(obj, obj.keep() if issubclass(type(obj), IReload) else None) for obj in objs
        ]
        # 遍历新模块对象的词典，将值赋予旧模块对象缓存的字典，并标记k已访问
        visited = set()
        # 注意这里不能使用getattr，而应直接使用__dict__，否则对于方法得到的是<bound method>
        for k, v in newBound.__dict__.items():
            visited.add(k)
            if k in self.__clsUpdateExcluded:
                continue
            # 用对象字典更新旧字典，维持对象方法的内存一致
            if type(v) is FunctionType:
                desFunc = oldBound.__dict__[k]
                ReflectionUtil.replaceFunc(v, desFunc)
            else:
                setattr(oldBound, k, v)
        setattr(oldModule, key, oldBound)

        # 对每个旧引用对象进行更新
        for referrer in boundReferrers:
            obj = referrer.obj
            if issubclass(type(obj), IReload):
                obj.reload(referrer.keep)

    @staticmethod
    def __dirDic(obj):
        return {k: getattr(obj, k) for k in dir(obj)}
