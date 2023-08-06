from parsing_exceptions import *
from . import match_elements

class SwitchMatch(object):
    """docstring for ConditionMatch"""
    def __init__(self, elements):
        self.elements = elements

    def get_variable(self, var, variables):
        if type(var) == int:
            return var
        if var.isdigit():
            return int(var)
        else:
            if var in variables:
                return variables[var]
            else:
                raise parsing_exceptions.VariableNotDefinedError()

    def parse(self, element_id, data, variables):
        element = self.elements[element_id]
        var1 = self.get_variable(element.variable1, variables)
        elements = []
        key = [key for key in element.switch_cases.keys() if element.call_function(var1, self.get_variable(key, variables))]
        if len(key) > 0:
            elements = element.switch_cases[key[0]]
        else:
            elements  = element.else_elements
        return match_elements(data, elements, variables)