

class UnsizedGroupElement(object):
    """
        Class for unsized group element.
        It may have a name, length and function.

        Using it in a protocol will look like:
        ()
        or
        (name = id)
        or
        (name = id; function = parse_id)

        where:
        name - The name of the group
        parse_id - if name is defined, it is possible to pass a function
                as an argument that will be called each the grouping element
                succeeds. The funtion should look like:
                def function_name(name, length, data)

            The main use of UnsizedGroupElement will be for grouping groups
        by without length (until the next ConstElement is matched) and
        extracting the data from the binary.

    """
    def __init__(self, name="", function=lambda name, length, data, variables: data, declaration_len=0, **extras):
        self.declaration_len = declaration_len
        self.name = name
        self.function = function

    def call_function(self, data, length, variables={}):
        return self.function(self.name, length, data, variables)

    def size(self):
        return -1

    def __len__(self):
        return self.declaration_len

    def __nonzero__(self):
        return len(self.declaration_len) > 0

    def __repr__(self):
        repr_template = "{name:%s}"
        return repr_template % (self.name)