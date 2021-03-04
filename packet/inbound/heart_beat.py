from packet.inbound.inbound_packet import InboundPacket
from packet.inbound.inbound_packet_type_id import InboundPacketCategory, InboundPacketTypeId


class HeartBeat(InboundPacket):
    CATEGORY = InboundPacketCategory.HeartBeat
    TYPE_ID = InboundPacketTypeId.HeartBeat
