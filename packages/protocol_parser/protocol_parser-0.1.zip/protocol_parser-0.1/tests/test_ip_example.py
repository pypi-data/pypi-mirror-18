import protocol_parser
import unittest

class Ipv4PacketHeader(object):

    def __init__(self):
        self.version = ""
        self.ihl = ""
        self.type_of_service = ""
        self.total_length = ""
        self.identification = ""
        self.flags = ""
        self.fragment_offset = ""
        self.ttl = ""
        self.protocol = ""
        self.header_checksum = ""
        self.source_ip = ""
        self.dest_ip = ""
        self.options = ""

    def set_paramter(self, name, length, data, variables):
        if name in ("version", "ihl", "total_length", "identification", "fragment_offset", "ttl", "header_checksum"):
            setattr(self, name, int(data, 2))
        elif name in ("type_of_service", "flags", "options"):
            setattr(self, name, data)
        elif name == "protocol":
            protocols = ["HOPOPT", "ICMP", "IGMP", "GGP", "IP-in-IP", "ST", "TCP", "CBT", "EGP",
                        "IGP", "BBN-RCC-MON", "NVP-II", "PUP", "ARGUS", "EMCON", "XNET", "CHAOS",
                        "UDP", "MUX"]
            self.protocol = protocols[int(data, 2)]
        elif name in ("dest_ip", "source_ip"):
            address = "%d.%d.%d.%d" % (int(data[0:8], 2), int(data[8:16], 2), int(data[16:24], 2), int(data[24:32], 2))
            setattr(self, name, address)
        if name == "ihl":
            variables["ihl"] = int(data, 2)

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        for field in self.__dict__:
            if getattr(self, field) != getattr(other, field):
                return False
        return True


def make_packet_st(packet_binary):
    packet = Ipv4PacketHeader()
    protocol_string = "(name=version;length=4;function=f)(name=ihl;length=4;function=f)" \
    "(name=type_of_service;length=8;function=f)(name=total_length;length=16;function=f)" \
    "(name=identification;length=16;function=f)(name=flags;length=3;function=f)" \
    "(name=fragment_offset;length=13;function=f)(name=ttl;length=8;function=f)" \
    "(name=protocol;length=8;function=f)(name=header_checksum;length=16;function=f)" \
    "(name=source_ip;length=32;function=f)(name=dest_ip;length=32;function=f)" \
    "(name=options;function=f)"
    protocol = protocol_parser.ProtocolParser()
    elements = protocol_parser.parsing_elements.parse_rule(protocol_string, {"f":packet.set_paramter})
    protocol.parsing_elements = elements
    groups = protocol.run_on_binary(packet_binary)
    return packet

def make_packet_elements(packet_binary):
    packet = Ipv4PacketHeader()
    version_element = protocol_parser.SizedGroupElement("version", 4, packet.set_paramter)
    ihl_element = protocol_parser.SizedGroupElement("ihl", 4, packet.set_paramter)
    tos_element = protocol_parser.SizedGroupElement("type_of_service", 8, packet.set_paramter)
    length_element = protocol_parser.SizedGroupElement("total_length", 16, packet.set_paramter)
    iden_element = protocol_parser.SizedGroupElement("identification", 16, packet.set_paramter)
    flags_element = protocol_parser.SizedGroupElement("flags", 3, packet.set_paramter)
    offset_element = protocol_parser.SizedGroupElement("fragment_offset", 13, packet.set_paramter)
    ttl_element = protocol_parser.SizedGroupElement("ttl", 8, packet.set_paramter)
    protocol_element = protocol_parser.SizedGroupElement("protocol", 8, packet.set_paramter)
    checksum_element = protocol_parser.SizedGroupElement("header_checksum", 16, packet.set_paramter)
    source_element = protocol_parser.SizedGroupElement("source_ip", 32, packet.set_paramter)
    dest_element = protocol_parser.SizedGroupElement("dest_ip", 32, packet.set_paramter)
    options_element = protocol_parser.UnsizedGroupElement("options", packet.set_paramter)
    protocol = protocol_parser.ProtocolParser()
    protocol.parsing_elements = [version_element, ihl_element, tos_element, length_element,
        iden_element, flags_element, offset_element, ttl_element, protocol_element,
        checksum_element, source_element, dest_element, options_element]
    groups = protocol.run_on_binary(packet_binary)
    return packet

class TestIpExample(unittest.TestCase):

        
    def test_udp_packet(self):
        packet_header_bin = "0" + bin(0x450000cb6c9900008011b8f7010000080100008a)[2:]
        packet_header = make_packet_st(packet_header_bin)
        packet_header2 = make_packet_elements(packet_header_bin)
        assert packet_header == packet_header2
        assert packet_header.version == 4
        assert packet_header.ihl == 5
        assert packet_header.type_of_service == "00000000"
        assert packet_header.total_length == 203
        assert packet_header.identification == 0x6c99
        assert packet_header.flags == "000"
        assert packet_header.fragment_offset == 0
        assert packet_header.ttl == 128
        assert packet_header.protocol == "UDP"
        assert packet_header.header_checksum == 0xb8f7
        assert packet_header.source_ip == "1.0.0.8"
        assert packet_header.dest_ip == "1.0.0.138"
        assert packet_header.options == ""
    
    def test_tcp_packet(self):
        packet_header_bin = "0" + bin(0x450000281e304000800614f10100000801010101)[2:]
        packet_header = make_packet_st(packet_header_bin)
        packet_header2 = make_packet_elements(packet_header_bin)
        assert packet_header == packet_header2
        assert packet_header.version == 4
        assert packet_header.ihl == 5
        assert packet_header.type_of_service == "00000000"
        assert packet_header.total_length == 40
        assert packet_header.identification == 0x1e30
        assert packet_header.flags == "010"
        assert packet_header.fragment_offset == 0
        assert packet_header.ttl == 128
        assert packet_header.protocol == "TCP"
        assert packet_header.header_checksum == 0x14f1
        assert packet_header.source_ip == "1.0.0.8"
        assert packet_header.dest_ip == "1.1.1.1"
        assert packet_header.options == ""
