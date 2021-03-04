# coding=utf-8
# @Time : 2020/8/8 19:36
# @Author : 胡泽勇
# 服务器配置信息

# Host
NET_HOST_DEFAULT_TIMEOUT = 300

MAX_HOST_CLIENTS_INDEX = 0xffff
MAX_HOST_CLIENTS_BYTES = 16

NET_STREAM_ENDIAN = '<'

PORT = 6666
HOST = "0.0.0.0"

# Game
WORLD_IDLE_DURATION = 2  # 世界空闲等待时间
COUNT_DOWN_INTERVAL = 1  # 倒计时更新间隔

MATCH_USER_SIZE = 5  # 匹配用户数量
COUNT_DOWN = 30  # 选择人物倒计时

TREASURE_LIFE = 4  # 宝箱生命

DECISION_PHASE_DURATION = 60  # 决策阶段持续时间
EQUIP_ID_DROP_ON_DYING = 9  # 死亡必掉装备id

IN_ALL = 3
CAN_CHOOSE = 1
IN_ALL_ENERGIED = 4
CAN_CHOOSE_ENERGIED = 2

Config_File_Path = "static/"
