from base.concept import Property
from packet.inbound.inbound_packet import InboundPacket
from packet.inbound.inbound_packet_type_id import InboundPacketCategory, InboundPacketTypeId


class AccountInfoPacket(InboundPacket):
    CATEGORY = InboundPacketCategory.AccountOperation


class FetchAccountInfo(AccountInfoPacket):
    TYPE_ID = InboundPacketTypeId.FetchAccountInfo


class UpdateAccountInfo(AccountInfoPacket):
    TYPE_ID = InboundPacketTypeId.UpdateAccountInfo

    username = Property(str, required=True)
    password = Property(str, required=True)
