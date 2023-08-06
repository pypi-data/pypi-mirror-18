

class VariableElement(object):
    """
        Class for variables element.
        It must have a name and a binary_format.
        It may have a comment or group.

        Using it in a protocol will look like:
        {variable; name=variable_name; type=struct_type}
        or 
        {variable; name=variable_name; type=struct_type; comment=var_comment}
        or 
        {variable; name=variable_name; type=struct_type; comment=var_comment; group=to_group}

        where:
        variable_name - The variable name
        struct_type - The variable type as defined by the struct module:

            Character   Byte order              Size        Alignment
            @           native                  native      native
            =           native                  standard    none
            <           little-endian           standard    none
            >           big-endian              standard    none
            !           network (= big-endian)  standard    none
     
            fomrat  c type                  python type           size
            c       char                    string of length 1    1    
            b       signed char             integer               1  
            B       unsigned char           integer               1  
            ?       _Bool                   bool                  1  
            h       short                   integer               2  
            H       unsigned short          integer               2  
            i       int                     integer               4  
            I       unsigned int            integer               4  
            l       long                    integer               4  
            L       unsigned long           integer               4  
            q       long long               integer               8  
            Q       unsigned long long      integer               8  
            f       float                   float                 4  
            d       double                  float                 8  
            s       char[]                  string       
            p       char[]                  string       

        to_group - if this parameter is true, the variable will be grouped
            like it was a GroupElement.

            The main use of VariableElement will be for grouping groups
        with length that is decided dynamically (such as Type-Length-Value
        kind of protocols). Another reason to use this VariableElement is
        to loop a dynamically decided number of times.

    """
    def __init__(self, name="", type="", group=False, comment="", declaration_len=0, **extras):
        self.declaration_len = declaration_len
        self.name = name
        self.type = type
        self.comment = comment
        self.group = group

    def size(self):
        import struct
        return struct.calcsize(self.type)

    def __len__(self):
        return self.declaration_len

    def __nonzero__(self):
        return (len(self.name) > 0) and (len(self.type) > 0)

    def __repr__(self):
        repr_template = "{name:%s, type:%s, comment:%s, group:%s}"
        return repr_template % (self.name, self.type, self.comment,
            str(self.group))


