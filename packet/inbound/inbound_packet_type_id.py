# coding=utf-8
from base.enum import Enum


class InboundPacketCategory(Enum):
    HeartBeat = 0
    Authentication = 1
    AccountOperation = 2
    MatchOperation = 3
    PickOperation = 4
    ReconnectOperation = 6
    UpdateConfigFile = 7

    GameSynchronize = 10

    Meta = 100


class InboundPacketTypeId(Enum):
    # Heart Beat
    HeartBeat = 0

    # Authentication : 1xx
    Login = 100
    Register = 101
    Logout = 102

    # Account : 2xx
    FetchAccountInfo = 200
    UpdateAccountInfo = 201

    # Match: 3xx
    BeginMatch = 300  # 开始匹配
    CancelMatch = 301  # 取消匹配

    # Pick: 4xx
    EnterPick = 400  # 进入选择阶段
    PickCharacter = 401  # 选择人物
    ConfirmPick = 402  # 确定选择

    # Load: 5xx
    EnterLoad = 500  # 进入加载阶段

    # Reconnect = 6xx
    CheckWorld = 600
    EnterReconnect = 601

    AskMd5 = 700
    AskFile = 701
    # Game : 1xxx
    # GameMeta
    EnterGame = 1000
    ExitGame = 1001

    # Decision: 11xx
    Move = 1100
    CastCard = 1101
    CastSkill = 1102
    CastAttack = 1103

    CancelCastCard = 1111

    ChooseCard = 1120
    DiscardCard = 1121

    EndDecision = 1199

    # Meta : 1xxxx
    Reload = 10000
    QuickGame = 10001
