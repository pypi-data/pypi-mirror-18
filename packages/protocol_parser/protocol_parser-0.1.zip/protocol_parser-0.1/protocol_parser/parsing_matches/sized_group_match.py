from parsing_exceptions import *

class SizedGroupMatch(object):
    """docstring for BinaryMatch"""
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
        data_size = self.get_variable(element.size(), variables)
        group_data = data[:data_size]
        #ret_data = element.call_function(group_data, len(group_data))
        return {"size":data_size, "group":[(element.name, group_data)]}
        