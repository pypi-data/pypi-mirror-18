import parsing_exceptions
from . import match_elements

class ConditionMatch(object):
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
        var2 = self.get_variable(element.variable2, variables)
        if element.function(var1, var2):
            elements = element.if_elements
        else:
            elements = element.else_elements
        return match_elements(data, elements, variables)
        