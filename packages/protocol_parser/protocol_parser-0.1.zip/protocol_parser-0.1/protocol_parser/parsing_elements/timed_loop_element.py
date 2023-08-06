

class TimedLoopElement(object):
    """
        Class for timed loop element.
        It must have a numer of times and data (sub-elements).
        It may have a name.

        Using it in a protocol will look like:
        [times = 3; data = (length = 4)]
        or
        [times = 3; data = (length = 4); name = name1]

        where:
        times - The number of times the loop will be called
        name - The name of the loop
        data - Sub-elements can be variables and even loops

            The main use of TimedLoopElement will be for grouping groups
        by dinamically decided number of times.

    """
    def __init__(self, name="", times=-1, elements=[], group_alone=False, declaration_len=0, **extras):
        self.declaration_len = declaration_len
        self.name = name
        self.times = times
        self.elements = elements
        self.group_alone = group_alone

    def size(self):
        return self.times

    def __len__(self):
        return self.declaration_len

    def __nonzero__(self):
        return self.times != -1

    def __repr__(self):
        repr_template = "{name:%s, times:%d, elements:%s}"
        return repr_template % (self.name, self.times, str(self.elements))