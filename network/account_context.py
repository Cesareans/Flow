# coding=utf-8

from common.singleton import Singleton


class AccountContext(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.logonAccount = {}
