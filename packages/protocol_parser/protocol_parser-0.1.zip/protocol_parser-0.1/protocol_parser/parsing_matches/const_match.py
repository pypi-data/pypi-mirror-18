from parsing_exceptions import *

class ConstMatch(object):
    """docstring for ConstMatch"""
    def __init__(self, elements):
        self.elements = elements

    def parse(self, element_id, data, variables):
        element = self.elements[element_id]
        if data[:element.size()] != element.value:
            raise ConstMismatchError()
        res = {"size":element.size()}
        return res
        