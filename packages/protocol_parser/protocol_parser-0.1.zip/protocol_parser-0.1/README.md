# Protocol Parser


Protocol Parser is a python package that helps you parse and validate unparsed data.
The main features of the package are:

  - Grouping (like in regex) Type-Length-Value fields
  - Diverging protocol flows
  - Looping on data

This text you see here is *actually* written in Markdown! To get a feel for Markdown's syntax, type some text into the left window and watch the results in the right.

### Tech

The package was written and tested in python 2.7, thus having python 2.7 is critical.
The package also uses the built-in struct package.

Protocol Parser is an open source project with a [public repository][protocol_parser] on GitHub.

### Installation

Protocl Parser requires [Python 2.7](https://www.python.org/about/) to run.

Download and extract the [package][protocol_parser] or pip install it.


```sh
$ pip install protocol_parser
```

Readme can be found here:
* [Protocol Parser Readme] [git_readme]
 

### Usage

So, here goes the interesting part - how to use the package.
There are two main ways to use the package, the first one is by building "protocol rule"
from string and the second one is building it manually. There isn't any difference between the two ways, the first one
just includes a deserializer that create rule of parsing elements (like the second way).

Glossary:
- Elements - Basic units that define a protocol.
- Variables - There is a dictionary of variables that are used during the parsing. 
    this variables' values are decided dinamically from variables elements.
- Match - The action of parsing protocol's data. Each element has a match.
- Parsing function - In order to make some parsing easier, some elements can have parsing function,
    that will can change the value returned by matching the element.
    the function parameters are: element name, data length, data, variables.

The basic units of the rule called parsing elements:
* ConditionElement - This element was made for implementing a if-else like element.
    The element receives two variables, two lists of elements (one for the if and one for the else) and a comparison function.
* ConstElement - This element is for space holding or validating protocol fields.
    The element receives a const string it should match
* LengthVariableElement - The main use of this element is for creating a variables in ways that are not supported
    by "struct" module, the current option is casting the value to int with a changing base.
    The element receives a name, chars length, casting base, and whether to group the variable or not
* SizedGroupElement - This element is used in order to group groups with either predefined length or a variable's value length.
    The element receives a name, length (either a number or variable name) and a parsing function.
* SwitchElement - This element was made for implementing a switch-case like element.
    The element receives a variable, dictionary of variables(keys) and elements lists(values) and a comparison function.
* TimedLoopElement - This element is used to do loops. Groups that are grouped by the element can be grouped under the loop name or with all the groups.
    The element receives a name, times to loop, elements and whether to group results under its name or not.
* UnsizedGroupElement - This element is used in order to group groups until the next ConstElement is matched.
    The element receives a name, and a parsing function.
* UntimedLoopElement - This element is used to do loops until the next ConstElement is matched. Groups that are grouped by the element can be grouped under the loop name or with all the groups.
    The element receives a name, elements and whether to group results under its name or not.
* VariableElement - The main use of this element is for creating a variables in ways that are supported
    by "struct" module.
    The element receives a name, struct type, and whether to group the variable or not

String deserialize format:
* ConstElement - just the string itself, e.g. "aaa".
* LengthVariableElement - "{name=variable_name; length=3; group=to_group}".
* SizedGroupElement - "(length = 4; name = group_name; function = f_key)", length can be also a variable name.
* TimedLoopElement - "[times = 3; data = (length = 4); name = name1]", data can be any string that can be deserialized.
* UnsizedGroupElement - "(name = group_name; function = f_key)".
* UntimedLoopElement - "[data = (length = 4); name = name1]", data can be any string that can be deserialized.
* VariableElement - "{name=variable_name; type=<B; group=to_group}", type can be type that is defined by struct module.

License
----

MIT


   [protocol_parser]: <https://github.com/matan1008/protocol_parser>
   [git_readme]: <https://github.com/matan1008/protocol_parser/blob/master/README.md>
