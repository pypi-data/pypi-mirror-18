import protocol_parser
import unittest

class TestSanity(unittest.TestCase):

    def test_condition(self):
        var1_element = protocol_parser.VariableElement("v1", "B", True)
        var2_element = protocol_parser.VariableElement("v2", "B", True)
        lower_func = lambda name, length, data, variables: data.lower()
        upper_func = lambda name, length, data, variables: data.upper()
        if_elem = protocol_parser.UnsizedGroupElement("g_if", lower_func)
        else_elem = protocol_parser.UnsizedGroupElement("g_else", upper_func)
        condition_element = protocol_parser.ConditionElement("v1", "v2", [if_elem], [else_elem])
        protocol = protocol_parser.ProtocolParser()
        protocol.parsing_elements = [var1_element, var2_element, condition_element]
        groups = protocol.run_on_binary("11aA")
        assert groups == [("v1", 49), ("v2", 49), ("g_if", "aa")]
        groups = protocol.run_on_binary("12aA")
        assert groups == [("v1", 49), ("v2", 50), ("g_else", "AA")]
    
    def test_const(self):
        const_element = protocol_parser.ConstElement("abc")
        protocol = protocol_parser.ProtocolParser()
        protocol.parsing_elements = [const_element]
        groups = protocol.run_on_binary("abc")
        assert groups == []
    
    def test_length_variable(self):
        lvar_element = protocol_parser.LengthVariableElement("lvar", 3, 2, True)
        protocol = protocol_parser.ProtocolParser()
        protocol.parsing_elements = [lvar_element]
        groups = protocol.run_on_binary("101")
        assert groups == [("lvar", 5)]
    
    def test_sized_group(self):
        lower_func = lambda name, length, data, variables: data.lower()
        sg_element = protocol_parser.SizedGroupElement("g1", 2, lower_func)
        protocol = protocol_parser.ProtocolParser()
        protocol.parsing_elements = [sg_element]
        groups = protocol.run_on_binary("aA")
        assert groups == [("g1", "aa")]
    
    def test_switch(self):
        var1_element = protocol_parser.VariableElement("v1", "B", True)
        lower_func = lambda name, length, data, variables: data.lower()
        upper_func = lambda name, length, data, variables: data.upper()
        double_func = lambda name, length, data, variables: data * 2
        foo_func = lambda name, length, data, variables: "foo"
        case1_elem = protocol_parser.UnsizedGroupElement("g_case1", lower_func)
        case2_elem = protocol_parser.UnsizedGroupElement("g_case2", upper_func)
        case3_elem = protocol_parser.UnsizedGroupElement("g_case3", double_func)
        else_elem = protocol_parser.UnsizedGroupElement("g_else", foo_func)
        switch = {
            49:[case1_elem],
            50:[case2_elem],
            51:[case3_elem],
        }
        switch_element = protocol_parser.SwitchElement("v1", switch, [else_elem])
        protocol = protocol_parser.ProtocolParser()
        protocol.parsing_elements = [var1_element, switch_element]
        groups = protocol.run_on_binary("1aA")
        assert groups == [("v1", 49), ("g_case1", "aa")]
        groups = protocol.run_on_binary("2aA")
        assert groups == [("v1", 50), ("g_case2", "AA")]
        groups = protocol.run_on_binary("3aA")
        assert groups == [("v1", 51), ("g_case3", "aAaA")]
        groups = protocol.run_on_binary("4aA")
        assert groups == [("v1", 52), ("g_else", "foo")]
    
    def test_timed_loop(self):
        sg1_element = protocol_parser.SizedGroupElement("g1", 1)
        sg2_element = protocol_parser.SizedGroupElement("g2", 1)
        tl_element = protocol_parser.TimedLoopElement("t1", 2, [sg1_element, sg2_element])
        protocol = protocol_parser.ProtocolParser()
        protocol.parsing_elements = [tl_element]
        groups = protocol.run_on_binary("AabB")
        assert groups == [("g1", "A"), ("g2", "a"), ("g1", "b"), ("g2", "B")]
    
    def test_timed_loop_grouped_alone(self):
        sg1_element = protocol_parser.SizedGroupElement("g1", 1)
        sg2_element = protocol_parser.SizedGroupElement("g2", 1)
        tl_element = protocol_parser.TimedLoopElement("t1", 2, [sg1_element, sg2_element], True)
        protocol = protocol_parser.ProtocolParser()
        protocol.parsing_elements = [tl_element]
        groups = protocol.run_on_binary("AabB")
        assert groups == [("t1", [("g1", "A"), ("g2", "a"), ("g1", "b"), ("g2", "B")])]
    
    def test_unsized_group(self):
        lower_func = lambda name, length, data, variables: data.lower()
        ug_element = protocol_parser.UnsizedGroupElement("g1", lower_func)
        protocol = protocol_parser.ProtocolParser()
        protocol.parsing_elements = [ug_element]
        groups = protocol.run_on_binary("aA")
        assert groups == [("g1", "aa")]
    
    def test_untimed_loop(self):
        sg1_element = protocol_parser.SizedGroupElement("g1", 1)
        sg2_element = protocol_parser.SizedGroupElement("g2", 1)
        ul_element = protocol_parser.UntimedLoopElement("t1", [sg1_element, sg2_element])
        protocol = protocol_parser.ProtocolParser()
        protocol.parsing_elements = [ul_element]
        groups = protocol.run_on_binary("AabB")
        assert groups == [("g1", "A"), ("g2", "a"), ("g1", "b"), ("g2", "B")]
    
    def test_untimed_loop_grouped_alone(self):
        sg1_element = protocol_parser.SizedGroupElement("g1", 1)
        sg2_element = protocol_parser.SizedGroupElement("g2", 1)
        ul_element = protocol_parser.UntimedLoopElement("t1", [sg1_element, sg2_element], True)
        protocol = protocol_parser.ProtocolParser()
        protocol.parsing_elements = [ul_element]
        groups = protocol.run_on_binary("AabB")
        assert groups == [("t1", [("g1", "A"), ("g2", "a"), ("g1", "b"), ("g2", "B")])]
    
    def test_variable(self):
        var_element = protocol_parser.VariableElement("var", "L", True)
        protocol = protocol_parser.ProtocolParser()
        protocol.parsing_elements = [var_element]
        groups = protocol.run_on_binary("\xFF\x00\x00\x00")
        assert groups == [("var", 255)] 