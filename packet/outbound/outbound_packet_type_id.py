from base.enum import Enum


class OutboundPacketTypeId(Enum):
    # Message
    OK = 0

    # AuthenticationResult
    LoginResult = 100
    RegisterResult = 101

    # Account Info
    FetchAccountInfoResult = 200
    UpdateAccountInfoResult = 201

    # Match Operation Result
    BeginMatchResult = 300
    CancelMatchResult = 301
    GameMatched = 302
    MatchProgress = 303

    # Pick
    BeginPick = 400
    PickCharacterResult = 401
    CharacterLocked = 402
    CharacterUnlocked = 403
    PickCountDown = 404
    QuitPick = 405

    # Load
    BeginLoad = 500

    # Reconnect = 6xx
    BeginReconnect = 600

    # ConfigFile
    FileMD5 = 702
    FileContent = 703

    # Game
    RemoveEntity = 1000

    PlacePlayerCharacter = 1001
    SetMainCharacter = 1002
    UpdateSkillCd = 1003
    UpdateSkillInfo = 1004
    ProhibitCast = 1005
    CancelProhibitCast = 1006

    Move = 1100
    EndMove = 1101

    Cast = 1200
    Damage = 1201
    Heal = 1202
    BeginRound = 1203
    EndRound = 1204
    BeginSettle = 1205
    EndSettle = 1206
    UpdateSettleStage = 1207

    SyncCards = 1300
    GainCard = 1301
    DropCard = 1302
    AvailableCards = 1303
    AvailableCardsEnd = 1304
    SyncCardsCount = 1305
    SyncCardLimit = 1306

    SyncLifeState = 1400
    CharacterDead = 1401

    SyncEquip = 1500
    DropEquip = 1501
    AddEquip = 1502
    DropEquipDestroy = 1503

    AddMapElement = 1600
    RemoveMapElement = 1601

    AddEnergyLattice = 1700
    RemoveEnergyLattice = 1701

    MapCollapse = 1800
    MapPreCollapse = 1801

    AddModifier = 1900
    ModifierChange = 1901
    ModifierInEffect = 1902
    RemoveModifier = 1903

    BeginTurn = 2000
    EndDecision = 2001
    TurnCountDown = 2002

    GameResult = 2100

    # Exception
    GeneralFail = 30000
    NotLogin = 30001
    NoGame = 30002

    # in game
    LatticeNotExist = 31000
    LatticeIsNotWalkable = 31001
    CannotChoose = 31002
    HaveNoSuchCard = 31003
    CannotCast = 31004
