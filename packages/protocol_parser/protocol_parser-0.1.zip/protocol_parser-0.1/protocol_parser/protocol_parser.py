import parsing_elements
import parsing_matches

class ProtocolParser(object):
    """docstring for ProtocolParser"""
    def __init__(self, protocol_rule=""):
        self.protocol_rule = ""
        self.parsing_elements = []
        if len(protocol_rule) > 0:
            self.protocol_rule = protocol_rule
            self.parsing_elements = parsing_elements.parse_rule(protocol_rule)


    def get_next_binary_element(self, index=0):
        is_binary = lambda elem: type(elem) == parsing_elements.BinaryElement
        elements = filter(is_binary, self.parsing_elements[index:])
        if len(elements) > 0:
            return elements[0]
        else:
            return None

    def run_on_binary(self, binary_data):
        variables = {}
        group_results = []
        for loc, element in enumerate(self.parsing_elements):
            result = parsing_matches.match(loc, self.parsing_elements, binary_data, variables)
            binary_data = binary_data[result["size"]:]
            if "group" in result:
                group_results += result["group"]
        if len(binary_data):
            raise parsing_matches.parsing_exceptions.EndOfElements()
        return group_results