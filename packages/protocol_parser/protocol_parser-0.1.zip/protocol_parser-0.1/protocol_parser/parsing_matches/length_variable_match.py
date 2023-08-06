from parsing_exceptions import *

class LengthVariableMatch(object):
    """docstring for LengthVariableMatch"""
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
        var_length = self.get_variable(element.size(), variables)
        value = int(data[:var_length], element.base)
        variables[element.name] = value
        res = {"size":var_length}
        if element.group:
            res["group"] = [(element.name, variables[element.name])]
        return res
        