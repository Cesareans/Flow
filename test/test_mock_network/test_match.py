# coding=utf-8
# @Time : 2020/8/18 14:36
# @Author : 胡泽勇
#

from match.match_space import MatchSpace
from packet.inbound.match_operation import BeginMatch
from test.mocked_network_test import MockedNetworkTest


class TestMatch(MockedNetworkTest):
    def testBeginMatch(self):
        for channel in self.channels:
            channel.fireInboundHandle(BeginMatch())
            MatchSpace().checkMatch()
