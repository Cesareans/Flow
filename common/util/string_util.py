# coding=utf-8
# @Time : 2020/8/8 14:11
# @Author : 胡泽勇
# 字符串工具


class StringUtil(object):
    @staticmethod
    def toHex(string):
        """
        将给定的字符串中的每一个字符以十六进制呈现并以：拼接
        @param string: 给定的字符串
        @return: 十六进制格式的字符串
        """
        return ':'.join(x.encode('hex') for x in string)
