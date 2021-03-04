from base.concept import Property
from packet.inbound.inbound_packet import InboundPacket
from packet.inbound.inbound_packet_type_id import InboundPacketCategory, InboundPacketTypeId


class AuthenticationPacket(InboundPacket):
    CATEGORY = InboundPacketCategory.Authentication


class LoginPacket(AuthenticationPacket):
    TYPE_ID = InboundPacketTypeId.Login

    username = Property(str, required=True)
    password = Property(str, required=True)


class LogoutPacket(AuthenticationPacket):
    TYPE_ID = InboundPacketTypeId.Logout


class RegisterPacket(AuthenticationPacket):
    TYPE_ID = InboundPacketTypeId.Register

    username = Property(str, required=True)
    password = Property(str, required=True)
