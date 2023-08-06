
class SizedGroupElement(object):
    """
        Class for sized group element.
        It must have a length.
        It may have a name and function.

        Using it in a protocol will look like:
        (length = 4)
        or 
        (length = v) if v was defined in a variable element
        or
        (length = 4; name = id)
        or
        (length = 4; name = id; function = id_parse)

        where:
        length - The length in bytes to group from the data
        name - The name of the group
        function - if name is defined, it is possible to pass a function
                as an argument that will be called each the grouping element
                succeeds. The funtion should look like:
                def function_name(name, length, data)

            The main use of SizedGroupElement will be for grouping groups
        by length and extracting the data from the binary.

    """
    def __init__(self, name="", length=-1, function=lambda name, length, data, variables: data, declaration_len=0, **extras):
        self.declaration_len = declaration_len
        self.name = name
        self.length = length
        self.function = function

    def call_function(self, data, length, variables={}):
        return self.function(self.name, length, data, variables)

    def size(self):
        return self.length

    def __len__(self):
        return self.declaration_len

    def __nonzero__(self):
        return self.length != -1

    def __repr__(self):
        repr_template = "{name:%s, length:%s}"
        return repr_template % (self.name, self.length)