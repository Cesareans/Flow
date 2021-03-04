# coding=utf-8
from match.match_space import MatchSpace
from network.account_context import AccountContext
from persist.model.account import Account


# from persist.model.account_new import Account


class GameSession(object):
    def __init__(self):
        self.world = None
        self.characterEntity = None


class Session(object):
    def __init__(self):
        self.__account = None
        self.matchInfo = None
        self.gameSession = GameSession()

    @property
    def account(self):
        return self.__account

    @account.setter
    def account(self, value):
        self.__account = value
        AccountContext().logonAccount[value.id] = value

    def quitGame(self):
        aid = self.account.id
        # 关闭游戏会话
        if self.gameSession.world is not None:
            wctx = self.gameSession.world.wctx
            wctx.removeChannel(aid)
        self.gameSession.world = None

    def close(self):
        # 检查账户
        if self.account is None:
            return
        aid = self.account.id
        # 尝试退出游戏
        self.quitGame()
        # 退出context环境
        AccountContext().logonAccount.pop(aid)
        Account.update(self.account)
        # 检查匹配
        if self.matchInfo is not None:
            MatchSpace().removeMatchInfo(self.matchInfo)
            self.matchInfo = None
