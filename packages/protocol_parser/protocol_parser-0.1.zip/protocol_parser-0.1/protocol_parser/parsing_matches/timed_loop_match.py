from parsing_exceptions import *
from . import match_elements

class TimedLoopMatch(object):
    """docstring for TimedLoopMatch"""
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
        group_results = []
        total_size = 0
        element = self.elements[element_id]
        for i in xrange(self.get_variable(element.size(), variables)):
            results = match_elements(data, element.elements, variables)
            group_results += results["group"]
            data = data[results["size"]:]
            total_size += results["size"]
        if element.group_alone:
            group_results = [(element.name, group_results)]
        return {"size":total_size, "group":group_results}
        