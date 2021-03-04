# coding=utf-8
# @Time : 2020/9/15 19:35
# @Author : 胡泽勇
# 


class IReload(object):
    def keep(self):
        raise NotImplementedError

    def reload(self, keep):
        raise NotImplementedError
