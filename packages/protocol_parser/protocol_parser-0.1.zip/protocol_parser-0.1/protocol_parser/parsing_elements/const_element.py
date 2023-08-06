
class ConstElement(object):
    """
        Class for constant element.
        It must have a value.

        Using it in a protocol will look like:
        \x00\xFF (hex values for bytes)
        or 
        hey      (normal python string)

            The main use of ConstElement will be for space holding and
        validating the protocol

    """
    def __init__(self, value="", **extras):
        self.value = value

    def size(self):
        return len(self.value)

    def __len__(self):
        return len(self.value)

    def __nonzero__(self):
        return len(self.value) > 0

    def __repr__(self):
        repr_template = "{value:%s}"
        return repr_template % self.value