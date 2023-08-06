from parsing_exceptions import *
from protocol_parser.parsing_elements import *
from . import match_elements

class UntimedLoopMatch(object):
    """docstring for UnsizedGroupMatch"""
    def __init__(self, elements):
        self.elements = elements

    def get_next_binary_element(self, index=0):
        is_binary = lambda elem: type(elem) == ConstElement
        elements = filter(is_binary, self.elements[index:])
        if len(elements) > 0:
            return elements[0]
        else:
            return None

    def parse(self, element_id, binary_data, variables):
        next_binary = self.get_next_binary_element(element_id)
        group_results = []
        total_size = 0
        element = self.elements[element_id]
        while (next_binary == None or (binary_data[:next_binary.size()] != next_binary.value)) and len(binary_data) > 0:
            results = match_elements(binary_data, element.elements, variables)
            group_results += results["group"]
            binary_data = binary_data[results["size"]:]
            total_size += results["size"]
        if element.group_alone:
            group_results = [(element.name, group_results)]
        return {"size":total_size, "group":group_results}