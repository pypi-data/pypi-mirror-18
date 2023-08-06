import protocol_parser
import unittest

def create_rule(rule, functions={}):
    elements = protocol_parser.parsing_elements.parse_rule(rule, functions)
    assert type(elements) == list
    return elements

class TestStringParser(unittest.TestCase):

    def test_empty_rule(self):
        rule = ""
        elements = create_rule(rule)
        assert len(elements) == 0
    
    def test_defective_rule(self):
        rule = "{)"
        try:
            elements = create_rule(rule)
        except Exception, e:
            assert type(e) == IndexError
    
    def test_const_element(self):
        rule = "a"
        elements = create_rule(rule)
        assert len(elements) == 1
        assert type(elements[0]) == protocol_parser.parsing_elements.ConstElement
        assert elements[0].value == "a"
    
    def test_length_variable_element(self):
        rule = "{variable; name=var1; length=3; comment=var comment; group=true; base=2}"
        elements = create_rule(rule)
        assert len(elements) == 1
        assert type(elements[0]) == protocol_parser.parsing_elements.LengthVariableElement
        assert elements[0].name == "var1"
        assert elements[0].size() == "3"
        assert elements[0].comment == "var comment"
        assert elements[0].group
        assert elements[0].base == 2
    
    def test_sized_group_element(self):
        rule = "(length = 4; name = g1; function = g1_parse)"
        functions = {"g1_parse": lambda name, length, data, variables: True}
        elements = create_rule(rule, functions)
        assert len(elements) == 1
        assert type(elements[0]) == protocol_parser.parsing_elements.SizedGroupElement
        assert elements[0].name == "g1"
        assert elements[0].size() == "4"
        assert elements[0].call_function(False, False) == True
    
    def test_timed_loop_element(self):
        rule = "[times = 3; data = a; name = t1]"
        elements = create_rule(rule)
        assert len(elements) == 1
        assert type(elements[0]) == protocol_parser.parsing_elements.TimedLoopElement
        assert elements[0].name == "t1"
        assert elements[0].size() == "3"
        assert len(elements[0].elements) == 1
        assert type(elements[0].elements[0]) == protocol_parser.parsing_elements.ConstElement
        assert elements[0].elements[0].value == "a"
    
    def test_unsized_group_element(self):
        rule = "(name = g1; function = g1_parse)"
        functions = {"g1_parse": lambda name, length, data, variables: True}
        elements = create_rule(rule, functions)
        assert len(elements) == 1
        assert type(elements[0]) == protocol_parser.parsing_elements.UnsizedGroupElement
        assert elements[0].name == "g1"
        assert elements[0].call_function(False, False) == True
    
    def test_untimed_loop_element(self):
        rule = "[data = a; name = t1]"
        elements = create_rule(rule)
        assert len(elements) == 1
        assert type(elements[0]) == protocol_parser.parsing_elements.UntimedLoopElement
        assert elements[0].name == "t1"
        assert len(elements[0].elements) == 1
        assert type(elements[0].elements[0]) == protocol_parser.parsing_elements.ConstElement
        assert elements[0].elements[0].value == "a"
    
    def test_variable_element(self):
        rule = "{variable; name=var1; type=>I; comment=var comment; group=true}"
        elements = create_rule(rule)
        assert len(elements) == 1
        assert type(elements[0]) == protocol_parser.parsing_elements.VariableElement
        assert elements[0].name == "var1"
        assert elements[0].size() == 4
        assert elements[0].comment == "var comment"
        assert elements[0].group
    
    