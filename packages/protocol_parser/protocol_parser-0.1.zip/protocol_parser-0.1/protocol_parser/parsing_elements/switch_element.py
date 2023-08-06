
class SwitchElement(object):
    """
        Class for switch element.

            The main use of SwitchElement will diverging into
        several continues of the protocol, according to a switch
        case result

    """
    def __init__(self, variable1="", switch_cases={}, else_elements=[], function=lambda var1, var2: var1==var2, declaration_len=0, **extras):
        self.declaration_len = declaration_len
        self.variable1 = variable1
        self.switch_cases = switch_cases
        self.else_elements = else_elements
        self.function = function

    def size(self):
        return self.length

    def call_function(self, var1, var2):
        return self.function(var1, var2)

    def __len__(self):
        return self.declaration_len

    def __nonzero__(self):
        return self.length != -1

    def __repr__(self):
        repr_template = "{switch_elements:%s, else_elements:%s}"
        return repr_template % (self.switch_cases.values(), self.else_elements)