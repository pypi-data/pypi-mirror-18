from parsing_exceptions import *
import struct

class VariableMatch(object):
    """docstring for VariableMatch"""
    def __init__(self, elements):
        self.elements = elements

    def parse(self, element_id, data, variables):
        element = self.elements[element_id]
        value = struct.unpack(element.type, data[:element.size()])
        variables[element.name] = value[0]
        res = {"size":element.size()}
        if element.group:
            res["group"] = [(element.name, variables[element.name])]
        return res
        