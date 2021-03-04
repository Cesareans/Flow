# coding=utf-8
from outbound_packet import GeneralOperationPacket
from outbound_packet_type_id import OutboundPacketTypeId


class FetchAccountInfoResult(GeneralOperationPacket):
    TYPE_ID = OutboundPacketTypeId.FetchAccountInfoResult

    def __init__(self, accountData, success=True, message='成功'):
        super(FetchAccountInfoResult, self).__init__(success, message)
        self.accountData = accountData


class UpdateAccountInfoResult(GeneralOperationPacket):
    TYPE_ID = OutboundPacketTypeId.UpdateAccountInfoResult

    def __init__(self, success=True, message='成功'):
        super(UpdateAccountInfoResult, self).__init__(success, message)
