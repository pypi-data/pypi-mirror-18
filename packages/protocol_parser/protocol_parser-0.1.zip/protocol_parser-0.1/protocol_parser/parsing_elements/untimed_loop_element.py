
class UntimedLoopElement(object):
    """
        Class for untimed loop element.
        It must have data (sub-elements).
        It may have a name.

        Using it in a protocol will look like:
        [data = (length = 4)]
        or
        [data = (length = 4); name = name1]

        where:
        name - The name of the loop
        data - Sub-elements can be variables and even loops

            The main use of UntimedLoopElement will be for grouping groups
        by dinamically decided number of times, until a ConstElement matches
        the data.

    """
    def __init__(self, name="", elements=[], group_alone=False, declaration_len=0, **extras):
        self.declaration_len = declaration_len
        self.name = name
        self.elements = elements
        self.group_alone = group_alone

    def size(self):
        return -1

    def __len__(self):
        return self.declaration_len

    def __nonzero__(self):
        return self.times != -1

    def __repr__(self):
        repr_template = "{name:%s, elements:%s}"
        return repr_template % (self.name, str(self.elements))