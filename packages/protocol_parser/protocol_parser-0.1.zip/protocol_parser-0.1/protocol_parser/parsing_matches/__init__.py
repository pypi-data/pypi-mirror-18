from protocol_parser.parsing_elements import *


def is_function_call(element):
    return type(element) in (SizedGroupElement, UnsizedGroupElement)

def match(element_id, elements, data, variables):
    matched = element_matches[type(elements[element_id])](elements)
    parse_res = matched.parse(element_id, data, variables)
    if is_function_call(elements[element_id]):
        group_data = elements[element_id].call_function(parse_res["group"][0][1], parse_res["size"], variables)
        parse_res["group"][0] = (parse_res["group"][0][0], group_data)
    return parse_res

def match_elements(binary_data, elements, variables={}):
    group_results = []
    size = 0
    for index in xrange(len(elements)):
        result = match(index, elements, binary_data, variables)
        binary_data = binary_data[result["size"]:]
        size += result["size"]
        if "group" in result:
            group_results += result["group"]
    return {"group":group_results, "size":size}


import const_match
import sized_group_match
import unsized_group_match
import variable_match
import timed_loop_match
import untimed_group_match
import condition_match
import switch_match
import length_variable_match


element_matches = {
    ConstElement:const_match.ConstMatch,
    VariableElement:variable_match.VariableMatch,
    SizedGroupElement:sized_group_match.SizedGroupMatch,
    UnsizedGroupElement:unsized_group_match.UnsizedGroupMatch,
    TimedLoopElement:timed_loop_match.TimedLoopMatch,
    UntimedLoopElement:untimed_group_match.UntimedLoopMatch,
    ConditionElement:condition_match.ConditionMatch,
    SwitchElement:switch_match.SwitchMatch,
    LengthVariableElement:length_variable_match.LengthVariableMatch
}

