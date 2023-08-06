

class LengthVariableElement(object):
    """
        Class for variables element.
        It must have a name and a length.
        It may have a comment or group.

        Using it in a protocol will look like:
        {variable; name=variable_name; length=3}
        or 
        {variable; name=variable_name; length=3; base=2}
        or 
        {variable; name=variable_name; length=3; comment=var_comment}
        or 
        {variable; name=variable_name; length=3; comment=var_comment; group=to_group}

        where:
        variable_name - The variable name
        length - The variable length
        to_group - if this parameter is true, the variable will be grouped
            like it was a GroupElement.

            The main use of LengthVariableElement will be for grouping groups
        with length that is decided dynamically (such as Type-Length-Value
        kind of protocols). Another reason to use this LengthVariableElement is
        to loop a dynamically decided number of times.
        When matching a string, the value 1 of variable should be the char "1"
        and not \x01

    """
    def __init__(self, name="", length=0, base=10, group=False, comment="", declaration_len=0, **extras):
        self.declaration_len = declaration_len
        self.name = name
        self.length = length
        self.comment = comment
        self.group = group
        self.base = int(base)

    def size(self):
        return self.length

    def __len__(self):
        return self.declaration_len

    def __nonzero__(self):
        return (len(self.name) > 0) and (len(self.length) > 0)

    def __repr__(self):
        repr_template = "{name:%s, length:%s, comment:%s, group:%s}"
        return repr_template % (self.name, self.length, self.comment,
            str(self.group))


