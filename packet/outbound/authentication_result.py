# coding=utf-8
from outbound_packet import GeneralOperationPacket
from outbound_packet_type_id import OutboundPacketTypeId


class LoginResultPacket(GeneralOperationPacket):
    TYPE_ID = OutboundPacketTypeId.LoginResult

    def __init__(self, success=True, message='成功'):
        super(LoginResultPacket, self).__init__(success, message)


class RegisterResultPacket(GeneralOperationPacket):
    TYPE_ID = OutboundPacketTypeId.RegisterResult

    def __init__(self, success=True, message='成功'):
        super(RegisterResultPacket, self).__init__(success, message)
