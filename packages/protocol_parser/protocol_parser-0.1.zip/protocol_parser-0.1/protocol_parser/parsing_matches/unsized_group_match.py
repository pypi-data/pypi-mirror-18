from parsing_exceptions import *
from protocol_parser.parsing_elements import *

class UnsizedGroupMatch(object):
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
        if next_binary == None:
            group_data = binary_data
        else:
            end_ind = binary_data.find(next_binary.value)
            if end_ind == -1:
                raise ConstMissingError()
            else:
                group_data = binary_data[:end_ind]
        res = {"size":len(group_data), "group":[(self.elements[element_id].name, group_data)]}
        return res