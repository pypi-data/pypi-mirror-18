
class VariableNotDefinedError(Exception):
    """Raise when trying to group with undefined variable's value"""

class ConstMismatchError(Exception):
    """Raise when a const element mismatches the binary data"""

class ConstMissingError(Exception):
    """Raise when a binary element is missing from the binary data"""

class EndOfElements(Exception):
    """Raise when all the parsing elements where matched but there is more binary data"""