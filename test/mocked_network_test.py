# coding=utf-8
# @Time : 2020/8/18 14:50
# @Author : 胡泽勇
#

import unittest

from test.mocked_channel_context import MockedChannelContext


class MockedNetworkTest(unittest.TestCase):
    def setUp(self):
        self.channel1 = MockedChannelContext()
        self.channel2 = MockedChannelContext()
        self.channels = [MockedChannelContext() for i in range(6)]
