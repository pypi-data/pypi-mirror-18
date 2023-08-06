
class ConditionElement(object):
    """
        Class for condition element.

            The main use of ConditionElement will diverging into
        two continues of the protocol, according to an if else
        result

    """
    def __init__(self, variable1="", variable2="", if_elements=[], else_elements=[], function=lambda var1, var2: var1==var2, declaration_len=0, **extras):
        self.declaration_len = declaration_len
        self.variable1 = variable1
        self.variable2 = variable2
        self.if_elements = if_elements
        self.else_elements = else_elements
        self.function = function

    def size(self):
        return self.length

    def __len__(self):
        return self.declaration_len

    def __nonzero__(self):
        return self.length != -1

    def __repr__(self):
        repr_template = "{if_elements:%s, else_elements:%s}"
        return repr_template % (self.if_elements, self.else_elements)