# coding=utf-8
# @Time : 2020/9/15 9:13
# @Author : 胡泽勇
# 
import logging
import sys

RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"  # \033[显示方式;前景色;背景色m

'''
-------------------------------------------
-------------------------------------------
前景色     |       背景色     |      颜色描述
-------------------------------------------
30        |        40       |       黑色
31        |        41       |       红色
32        |        42       |       绿色
33        |        43       |       黃色
34        |        44       |       蓝色
35        |        45       |       紫红色
36        |        46       |       青蓝色
37        |        47       |       白色
-------------------------------------------
'''
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = [30 + i for i in range(8)]

COLORS = {
    'DEBUG': CYAN,
    'INFO': WHITE,
    'WARNING': YELLOW,
    'ERROR': RED,
    'CRITICAL': RED,
    'FATAL': RED
}


class ColoredFormatter(logging.Formatter):
    def __init__(self):
        logging.Formatter.__init__(self, "%(asctime)s[%(levelname)-7s] %(filename)-28s@%(lineno)3s: %(message)s")
        self.datefmt = '%Y-%m-%d %H:%M:%S'

    def format(self, record):
        if sys.stdout.isatty():
            return logging.Formatter.format(self, record)
        level = record.levelname
        return COLOR_SEQ % COLORS[level] + logging.Formatter.format(self, record) + RESET_SEQ


def init():
    handler = logging.StreamHandler()
    handler.setFormatter(ColoredFormatter())
    gettrace = getattr(sys, 'gettrace', None)
    logging.getLogger("urllib3.connectionpool").setLevel(logging.WARNING)
    if gettrace is None or not gettrace():  # 获取不到gettrace属性，或者不处于debug
        logging.root.level = logging.INFO
    else:  # 处于debug
        logging.root.level = logging.DEBUG
    for rh in logging.root.handlers:
        logging.root.removeHandler(rh)
    logging.root.addHandler(handler)
