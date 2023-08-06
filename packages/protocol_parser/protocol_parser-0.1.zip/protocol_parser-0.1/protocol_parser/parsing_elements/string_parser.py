from const_element import ConstElement
from variable_element import VariableElement
from sized_group_element import SizedGroupElement
from unsized_group_element import UnsizedGroupElement
from timed_loop_element import TimedLoopElement
from untimed_loop_element import UntimedLoopElement
from length_variable_element import LengthVariableElement

end_brackets = {
    "{":"}",
    "(":")",
    "[":"]"
}

def top_bracket_split(st, seperator):
    parts = []
    last_ind = 0
    brackets_counter = 0;
    for i in xrange(len(st)):
        if st[i] == seperator and brackets_counter == 0:
            parts.append(st[last_ind:i])
            last_ind = i + 1
        elif st[i] in end_brackets.keys():
            brackets_counter += 1
        elif st[i] in end_brackets.values():
            brackets_counter -= 1
    if last_ind < len(st):
        parts.append(st[last_ind:])
    return parts

def loop_attribute_string_to_dict(attributes_st, cut_attrs=[]):
    attributes = top_bracket_split(attributes_st, ";")
    attributes = map(lambda attribute: attribute.strip(), attributes)
    attributes = filter(lambda attr: attr not in cut_attrs, attributes)
    split_attributes = [
        map(lambda attribute: attribute.strip(), top_bracket_split(attribute, "=")) 
        for attribute 
        in attributes
        if len(attribute.strip()) > 0
    ]
    attributes = filter(lambda attr: attr[0] not in cut_attrs, split_attributes)
    return attributes


def cut_const_element(rule):
    rule_index = 0
    while (rule_index < len(rule) - 1) and rule[rule_index + 1] not in ("{", "}", "(", ")", "[", "]"):
        rule_index += 1
    return rule_index

def cut_brackets(rule, left_b):
    brackets_index = 0
    brackets_counter = 0
    while rule[brackets_index] != end_brackets[left_b] or brackets_counter != 1:
        if rule[brackets_index] == left_b:
            brackets_counter += 1
        elif rule[brackets_index] == end_brackets[left_b]:
            brackets_counter -= 1
        brackets_index += 1
    return brackets_index

def create_const_element(rule, functions={}):
    element_size = cut_const_element(rule)
    return ConstElement(rule[:element_size+1])

def create_variable_element(rule, functions={}):
    element_size = cut_brackets(rule, rule[0])
    rule = rule[:element_size+1]
    cuts = ["variable"]
    attributes = dict(loop_attribute_string_to_dict(rule[1:-1], cuts))
    attributes["declaration_len"] = len(rule)
    if "group" in attributes:
        attributes["group"] = attributes["group"].lower() == "true"
    if "length" in attributes:
        return LengthVariableElement(**attributes)
    else:
        return VariableElement(**attributes)

def create_sized_group_element(rule, functions={}):
    element_size = cut_brackets(rule, rule[0])
    rule = rule[:element_size+1]
    cuts = ["group"]
    attributes = dict(loop_attribute_string_to_dict(rule[1:-1], cuts))
    attributes["declaration_len"] = len(rule)
    if "function" in attributes:
        attributes["function"] = functions[attributes["function"]]
    return SizedGroupElement(**attributes)

def create_unsized_group_element(rule, functions={}):
    element_size = cut_brackets(rule, rule[0])
    rule = rule[:element_size+1]
    cuts = ["group"]
    attributes = dict(loop_attribute_string_to_dict(rule[1:-1], cuts))
    attributes["declaration_len"] = len(rule)
    if "function" in attributes:
        attributes["function"] = functions[attributes["function"]]
    return UnsizedGroupElement(**attributes)

def create_timed_loop_element(rule, functions={}):
    element_size = cut_brackets(rule, rule[0])
    rule = rule[:element_size+1]
    cuts = ["loop"]
    attributes = dict(loop_attribute_string_to_dict(rule[1:-1], cuts))
    attributes["declaration_len"] = len(rule)
    attributes["elements"] = parse_rule(attributes["data"], functions)
    return TimedLoopElement(**attributes)

def create_untimed_loop_element(rule, functions={}):
    element_size = cut_brackets(rule, rule[0])
    rule = rule[:element_size+1]
    cuts = ["loop"]
    attributes = dict(loop_attribute_string_to_dict(rule[1:-1], cuts))
    attributes["declaration_len"] = len(rule)
    attributes["elements"] = parse_rule(attributes["data"], functions)
    return UntimedLoopElement(**attributes)


def create_element(rule, functions={}):
    if rule[0] == "{":
        return create_variable_element(rule, functions)
    elif rule[0] == "(":
        element_size = cut_brackets(rule, rule[0])
        if "length" in rule[:element_size + 1]:
            return create_sized_group_element(rule, functions)
        else:
            return create_unsized_group_element(rule, functions)
    elif rule[0] == "[":
        element_size = cut_brackets(rule, rule[0])
        if "times" in rule[:element_size + 1]:
            return create_timed_loop_element(rule, functions)
        else:
            return create_untimed_loop_element(rule, functions)
    else:
        return create_const_element(rule, functions)

def parse_rule(rule, functions={}):
    elements = []
    element_size = 0
    while len(rule) > 0:
        element = create_element(rule, functions)
        elements.append(element)
        rule = rule[len(element):]
    return elements