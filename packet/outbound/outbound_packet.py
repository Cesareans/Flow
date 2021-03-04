from packet.packet import Packet


class OutboundPacket(Packet):
    def __init__(self):
        super(OutboundPacket, self).__init__()


class MessagePacket(OutboundPacket):
    def __init__(self, message):
        super(MessagePacket, self).__init__()
        self.message = message


class GeneralOperationPacket(OutboundPacket):
    def __init__(self, success, message):
        super(GeneralOperationPacket, self).__init__()
        # should be bool
        self.success = success
        # should be str
        self.message = message
