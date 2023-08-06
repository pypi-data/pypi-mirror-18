import protocol_parser
import unittest

class TestEdgeCases(unittest.TestCase):

    def test_variable_lengthed_variable(self):
        var1_element = protocol_parser.VariableElement("v1", "B", True)
        var2_element = protocol_parser.LengthVariableElement("v2", "v1", 10, True)
        sg_element = protocol_parser.SizedGroupElement("g1", "v2")
        protocol = protocol_parser.ProtocolParser()
        protocol.parsing_elements = [var1_element, var2_element, sg_element]
        groups = protocol.run_on_binary("\x0203abc")
        assert groups == [("v1", 2), ("v2", 3), ("g1", "abc")]
    
    def test_nested_loops(self):
        sg1_element = protocol_parser.SizedGroupElement("g1", 1)
        sg2_element = protocol_parser.SizedGroupElement("g2", 2)
        tl_element = protocol_parser.TimedLoopElement("t1", 2, [sg1_element, sg2_element])
        ul_element = protocol_parser.UntimedLoopElement("u1", [tl_element])
        protocol = protocol_parser.ProtocolParser()
        protocol.parsing_elements = [ul_element]
        groups = protocol.run_on_binary("abbcddabbcddabbcdd")
        groups = [("g1", "a"), ("g2", "bb"), ("g1", "c"), ("g2", "dd")] * 3
    
    def test_binary_tlv(self):
        def parsing_func(name, length, data, variables): 
            types = {1:"type a", 2:"type b"}
            return types[variables["type"]] + (" length %d " % length) + data
        var1_element = protocol_parser.LengthVariableElement("type", 8, 2, False)
        var2_element = protocol_parser.LengthVariableElement("length", 8, 2, False)
        sg_element = protocol_parser.SizedGroupElement("value", "length", parsing_func)
        protocol = protocol_parser.ProtocolParser()
        protocol.parsing_elements = [var1_element, var2_element, sg_element]
        groups = protocol.run_on_binary("0000001000000011aaa")
        assert groups == [("value", "type b length 3 aaa")]
    
    def test_sized_group_var_func(self):
        lower_func = lambda name, length, data, variables: data.lower() * variables["times"]
        var1_element = protocol_parser.VariableElement("times", "B", False)
        sg_element = protocol_parser.SizedGroupElement("g1", 2, lower_func)
        protocol = protocol_parser.ProtocolParser()
        protocol.parsing_elements = [var1_element, sg_element]
        groups = protocol.run_on_binary("\x02aA")
        assert groups == [("g1", "aaaa")]