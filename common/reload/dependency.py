# coding=utf-8
# @Time : 2020/9/14 15:21
# @Author : 胡泽勇
#
import logging


# Dep : Dependency
class DepNode(object):
    def __init__(self, module):
        self.module = module
        self.reliers = {}

    def __hash__(self):
        return hash(self.module.__name__)

    def __repr__(self):
        return "DepNode<{}>".format(self.module.__name__)


class DepGraph(object):
    def __init__(self):
        self.nodes = {}

    def addDep(self, relier, dep):
        """
        Record dependency -> relier depends on dep
        """
        relierNode = self.nodes.setdefault(relier.__name__, DepNode(relier))
        depNode = self.nodes.setdefault(dep.__name__, DepNode(dep))
        if relier.__name__ in depNode.reliers:
            raise Exception("Already record the dependency pair.")

        depNode.reliers[relier.__name__] = relierNode

    def hasDep(self, relier, dep):
        """
        Check has dependency -> if relier depends on dep
        """
        # Check if both relier and dep are in record
        if relier.__name__ not in self.nodes or dep.__name__ not in self.nodes:
            return False
        # Check if dep has recorded relier
        return relier.__name__ in self.nodes[dep.__name__].reliers

    def hasModule(self, module):
        return module.__name__ in self.nodes

    def traverse(self, module, action):
        """
        遍历访问模块的依赖，得到拓扑依赖序后，按顺序对每个依赖执行指定的action
        @param module: 模块
        @param action: 对模块执行的行为
        """
        if module.__name__ not in self.nodes:
            logging.error("Module not registered.")
            return
        sequence = []
        self.__trace(self.nodes[module.__name__], set(), sequence)
        for node in reversed(sequence):
            action(node.module)

    def __trace(self, visiting, visited, lst):
        """
        BFS遍历依赖，进行单节点拓扑排序
        @param visiting: 当前访问节点
        @param visited: 已经访问的节点集合
        @param lst: 导出拓扑序
        """
        for node in visiting.reliers.values():
            if node in visited:
                continue
            self.__trace(node, visited, lst)
        visited.add(visiting)
        lst.append(visiting)
