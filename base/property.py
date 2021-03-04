# coding=utf-8
# @Time : 2020/12/19
# @Author : 胡泽勇
# 属性声明对象，通过Class Level构建自己的数据体系
import sys

"""
关于热更：
1. 默认_reload_all=True，保证类级变量上的property能被修改。
另外关于热更的可能导致的坑：
    - 如果替换了property的名字 xx = Property(...) -> yy = Property(...), xx将仍然存在在热更前就存在的原对象上
2. 关于实例化的对象本身的数据，请合理的增加对于自身数据的判断。并且合理的重载init/persistent等方法
合理 = 不要忘了调用super

"""
# 提供给持久化使用
_ClientPersistent = 1 << 1
_ServerPersistent = 1 << 2

NOT_PERSISTENT = 0
CLIENT_ONLY = _ClientPersistent
SERVER_ONLY = _ServerPersistent
ALL = _ClientPersistent | _ServerPersistent

DUMP_CLIENT = 1
DUMP_SERVER = 2
DUMP_ALL    = 3


class PropertyMetaException(BaseException):
    _AliasRepetition = (1, 'Persistent alias repeat! class: {} alias: {}')
    _DefaultError = (2, 'default must be in [VALUE(x), NONE, LOAD(x), FUNC_RES(x)]! class: {} property: {}')
    _DefaultLoadNone = (3, 'default assign LOAD, but property load is None! class: {} property: {}')
    _ValueMutable = (3, 'VALUE should not be assigned with a mutable value [tuple, list, dict.]! class: {} property: {}')

    @classmethod
    def AliasRepetition(cls, *args):
        return PropertyMetaException(cls._AliasRepetition, *args)

    @classmethod
    def DefaultError(cls, *args):
        return PropertyMetaException(cls._DefaultError, *args)

    @classmethod
    def DefaultLoadNone(cls, *args):
        return PropertyMetaException(cls._DefaultLoadNone, *args)

    @classmethod
    def ValueMutable(cls, *args):
        return PropertyMetaException(cls._DefaultLoadNone, *args)

    def __init__(self, reason, *args):
        self.message = reason[1].format(*args)

    def __str__(self):
        return self.message


class _Default(object):
    pass


class VALUE(_Default):
    MutableTypes = {list, dict}
    """使用给定的值进行默认的初始化
    value请不要使用可变值
    """
    def __init__(self, value):
        self.value = value


# 设置为None
NONE = VALUE(None)


class LOAD(_Default):
    """ 调用指定的load根据给定的参数进行值的加载初始化
    """
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


class FUNC_RES(_Default):
    """ 根据给定的方法进行调用，将返回值进行值的加载初始化
    一般用于返回可变值等
    """
    def __init__(self, func):
        self.func = func


class Property(object):
    def __init__(self, default, alias=None, persistent=ALL, loadDump=None, external=False):
        """
        属性对象，在Class Level声明字段，声明后的值每个类一份，不会占据太多的额外空间.
        必须显式指定默认值
            1. 默认值是当初始化词典里没有对应key的时候所使用的值
            2. 默认值同时可以用于当元类对象增加一个property字段并reload时，作为默认的存盘值
        Args:
            default: 属性对象的默认值，在该字段初始化时分配的默认值
            alias: 属性别名，用于持久化
            persistent: 持久化选项
            loadDump: (load, dump)
                load = 加载器，默认是直接加载值，如果给定load，将会根据load内定义的逻辑进行值的特定转换
                dump = 转储（持久化）器，默认是直接转储值，如果给定dump，将会根据dump内定义的逻辑进行值的特定转储
            external: <高级属性> 为True时，表明是外部属性，在initFromDict时如果没有值则不会进行更新
        """
        self.alias = alias
        if loadDump is None or len(loadDump) != 2:
            loadDump = [None, None]
        self.load = loadDump[0]
        self.dump = Dumper if loadDump[1] is None else loadDump[1]

        self.persistent = persistent
        self._default = default
        self.name = None
        self.external = external

    def default(self):
        default = self._default
        if isinstance(default, VALUE):
            return default.value
        if isinstance(default, LOAD):
            return self.load(*default.args, **default.kwargs)
        if isinstance(default, FUNC_RES):
            return default.func()

        return self._default

    def __str__(self):
        return "Property<name: {}, alias:{}>"

    def __getattr__(self, item):
        # 仅是去除type hint
        raise AttributeError


class PropertyMeta(type):
    def __new__(mcs, name, bases, attrs):
        """ Property元对象，所有继承自概念对象的类型通过Property声明字段
        """
        # 建立props元数据

        # k：属性名 v：property对象
        allProps = {}
        serverProps = {}
        clientProps = {}
        # k：属性alias v：property对象
        propAlias = {}

        # 访问属性并追溯继承属性
        attributes = attrs.copy()
        for base in bases:
            if hasattr(base, '_properties'):
                attributes.update(base._properties)
        # 在继承属性中找到所有的property，并记录到props元数据
        for k, v in attributes.items():
            if type(v) == Property:
                PropertyMeta.validate(name, v)
                # 为属性对象增加名字这个元信息
                v.name = k
                allProps[k] = v
                if v.persistent & _ServerPersistent:
                    serverProps[k] = v
                if v.persistent & _ClientPersistent:
                    clientProps[k] = v
                # 处理别名与别名集合
                # _propAlias: k: 属性别名 v: property对象
                if v.alias is None:
                    v.alias = k
                # 处理alias重复
                if v.alias in propAlias:
                    raise PropertyMetaException.AliasRepetition(name, v.alias)
                propAlias[v.alias] = v
        # 建立元数据映射
        attrs['_properties'] = allProps
        attrs['_serverProps'] = serverProps
        attrs['_clientProps'] = clientProps
        attrs['_propAlias'] = propAlias
        return type.__new__(mcs, name, bases, attrs)

    @staticmethod
    def validate(name, prop):
        """ 处理元类生成时的一些约束
        @param name: 生成对象的类的名字
        @param prop: 验证合理性的属性
        """
        if not isinstance(prop._default, _Default):
            raise PropertyMetaException.DefaultError(name, prop.name)
        if isinstance(prop._default, LOAD) and prop.load is None:
            raise PropertyMetaException.DefaultLoadNone(name, prop.name)
        elif isinstance(prop._default, VALUE):
            tp = type(prop._default.value)
            if tp in VALUE.MutableTypes:
                raise PropertyMetaException.ValueMutable(name, prop.name)


class PersistentObject(object):
    __metaclass__ = PropertyMeta
    _reload_all = True

    def __init__(self):
        self._resetAllFields()

    def _resetAllFields(self):
        for name, prop in self._properties.items():
            self.__setattr__(name, prop.default())

    def load(self, data, partial=False):
        """ 根据给定的dict进行数据初始化。
        局部更新：当dict存在数据时进行覆盖，不存在时原数据不动。反之非局部更新以prop配置的default值进行原数据的替换
        Args:
            data: 给定的数据词典
            partial: 决定是否局部更新，默认为false。仅支持该对象的字段层级，因为list&set&dict等数据结构的存在，不支持递归。
        """
        if data is None:
            initDict = {}
        # 通过dic更新类的字段值
        for name, prop in self._properties.items():
            # 如果initDict中没有值
            if prop.alias not in data:
                # 如果是部分更新或者属性是外部属性，则不进行值的更新
                if partial or prop.external:
                    continue
            # 从字典中取指使用alias
            value = data.get(prop.alias, prop.default())
            load = prop.load
            setattr(self, name, value if load is None or value is None else load(value))

    def dump(self, persistent=ALL):
        # 如果没有property对应的值，则使用默认值
        return {prop.alias: prop.dump(self.__dict__.get(name, prop.default()), persistent)
                for name, prop in self._properties.iteritems() if prop.persistent & persistent}

    def dumpSpecific(self, fields, persistent=ALL):
        """ 根据给定的字段序列导出特定的字典集合
        Args:
            fields: 给定的字段序列，值为字段名或者类级别上声明的property对象
            persistent: 决定该字段序列的所对应的值的导出方式
        """
        # 找到指定的props
        props = {}
        for field in fields:
            if isinstance(field, Property):
                props[field.name] = self._properties.get(field.name, None)
            else:
                props[field] = self._properties.get(field, None)

        # 如果没有property对应的值，则使用默认值
        return {prop.alias: prop.dump(self.__dict__.get(name, prop.default()), persistent=persistent)
                for name, prop in props.iteritems() if prop is not None and prop.persistent & persistent}

    # def __str__(self):
    #     return str({k: str(self.__dict__[k]) for k, prop in self._properties.iteritems()})
    #
    # __repr__ = __str__


# 用于包装一个类，获得该类的元信息，在第一次读取该对象的时候进行import得到新的处于内存中的类
# => 解决在类的级别进行对其他的类的绑定的时候，热更新后，绑定的是新的类，当与代码中旧类交互时就会出现不匹配的问题
# 思想类似于延迟更新
class _ActualClass(object):
    def __init__(self, objectType):
        self.module = objectType.__module__
        self.name = objectType.__name__
        self.actualClass = None

    def __call__(self, *args, **kwargs):
        if self.actualClass is None:
            module = sys.modules.get(self.module, None)
            if module is None:
                return None
            self.actualClass = module.__dict__.get(self.name, None)
            if self.actualClass is None:
                return None
        return self.actualClass(*args, **kwargs)


def ObjectLoaderWrapper(objectType):
    actualClass = _ActualClass(objectType)

    def load(value):
        if type(value) is not dict:
            return value
        obj = actualClass()
        obj.load(value)
        return obj

    return load


def SetLoaderWrapper(objectType=None):
    actualClass = _ActualClass(objectType) if objectType is not None else None

    def load(value):
        if type(value) is not list:
            return value
        if actualClass is not None:
            ret = set()
            for item in value:
                obj = actualClass()
                obj.load(item)
                ret.add(obj)
        else:
            ret = set(value)
        return ret

    return load


def ListLoaderWrapper(objectType):
    actualClass = _ActualClass(objectType)

    def load(value):
        if type(value) is not list:
            return value
        ret = []
        for item in value:
            obj = actualClass()
            obj.load(item)
            ret.append(obj)
        return ret

    return load


def DictSmartLoaderWrapper(objectType):
    actualClass = _ActualClass(objectType)

    def load(value):
        ret = {}
        if type(value) is list:
            # list是dict转的，每个元素是 (k, v)
            # 这样直接能解开 => k, v
            for k, v in value:
                ret[k] = actualClass()
                ret[k].load(v)
            return ret
        if type(value) is dict:
            for k, v in value.iteritems():
                ret[k] = actualClass()
                ret[k].load(v)
            return ret

        return ret

    return load


def DictFromListLoaderWrapper(objectType, key):
    actualClass = _ActualClass(objectType)

    def load(value):
        ret = {}
        if type(value) is list:
            for item in value:
                k = item.get(key, None)
                if k is None:
                    continue
                ret[k] = actualClass()
                ret[k].load(item)
            return ret
        return ret

    return load


def Dumper(value, persistent):
    """ 将值进行转储，根据persistent决定转储方式
    Args:
        value: 需要转储的值
        persistent: 转储方式

    Returns: 转储后的可序列化的值
    """
    if issubclass(type(value), PersistentObject):
        return value.dump(persistent)
    return value


def SetDumper(value, persistent):
    if type(value) is not set:
        return value
    return [Dumper(item, persistent) for item in value]


def ListDumper(value, persistent):
    if type(value) is not list:
        return value
    return [Dumper(item, persistent) for item in value]


def DictDumper(value, persistent):
    """ 字典Dumper，将一个字典数据对象进行dump，得到一个字典
    1. 当传入数据对象不是字典时，直接返回该数据对象
    """
    if type(value) is not dict:
        return value
    return {k: Dumper(item, persistent) for k, item in value.iteritems()}


def DictIntKeyDumper(value, persistent):
    """ key为Int的字典Dumper，因为BSON对象不支持Int key，所以这里将这个数据转化为tuple
    1. 当传入数据对象不是字典时，直接返回该数据对象
    """
    if type(value) is not dict:
        return value
    return [(k, Dumper(item, persistent)) for k, item in value.iteritems()]


def DictToListDumper(value, persistent):
    """ 字典到序列的Dumper，返回字典所有Values的序列，相当于 dic.items()
    1. 当传入数据对象不是字典时，直接返回该数据对象
    """
    if type(value) is not dict:
        return value
    return [Dumper(item, persistent) for k, item in value.iteritems()]


# 预定义的 load&dump Pair
def ObjectPair(objectType):
    """ 处理单个类型的值的转换
    Args:
        objectType: 指定的类型
    """
    return ObjectLoaderWrapper(objectType), Dumper


def SetPair(objectType=None):
    """ 处理将一个list转换成set的转换
    1. 当objectType不为None时，会将每个元素按objectType进行转换
    Args:
        objectType: 指定的类型
    """

    return SetLoaderWrapper(objectType), SetDumper


def ListPair(objectType):
    """ 处理 持久化对象的list 的转换
    Args:
        objectType: 指定的类型
    """
    return ListLoaderWrapper(objectType), ListDumper


def DictPair(objectType, isIntKey=False):
    """ 处理 持久化对象的dict 的转换
    Args:
        objectType: 指定的类型
        isIntKey: 该词典的键值是否为int，因为BSON持久化不支持数字作为key
    """
    if isIntKey:
        return DictSmartLoaderWrapper(objectType), DictDumper
    else:
        return DictSmartLoaderWrapper(objectType), DictIntKeyDumper


def DictFromListPair(objectType, key):
    """ 处理 持久化对象的list 到一个 dict的转换，要求指定该持久化对象的字段作为key
    Args:
        objectType: 指定的类型
        key: 该持久化对象的key
    """
    return DictFromListLoaderWrapper(objectType, key), DictToListDumper
