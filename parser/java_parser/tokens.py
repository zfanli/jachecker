'''
Tokens, Symbols.
'''

import re
import json

from pypeg2 import *
from parser.java_parser.mixins import Stringify, Literal


common_name = re.compile(r'([\w\d]+)')
common_with_attribute = re.compile(r'[\w\d]+\.[\w\d]+')
array_symbols = re.compile(r'(\[\])+')


class AccessModifier(Keyword):
    '''Output: `str`
        keyword
    '''

    grammar = Enum(
        K('default'), K('public'), K('protected'), K('private'),
    )


class NonAccessModifier(Keyword):
    '''Output: `str`
        keyword
    '''

    grammar = Enum(
        K('final'), K('static'), K('transient'),
        K('synchronized'), K('volatile'),
    )


class Modifier(str, Literal):
    '''All modifiers'''

    grammar = [AccessModifier, NonAccessModifier]


class LiteralString(str, Literal):

    grammar = re.compile(r'^".*"$', re.S)

    def object(self):
        return self[1:-1]


class LiteralChar(str, Literal):

    grammar = re.compile(r"^'\w'$")

    def object(self):
        return self[1:-1]


class LiteralNumber(int, Literal):
    '''For int, short, byte'''

    grammar = re.compile(r'\d+')


class LiteralFloat(str, Literal):

    grammar = re.compile(r'\d+\.\d+(f|F)')

    def object(self):
        return float(self[:-1])


class LiteralLong(str, Literal):

    grammar = re.compile(r'\d+(l|L)')

    def object(self):
        return int(self[:-1])


class LiteralDouble(str, Literal):

    grammar = re.compile(r'\d+\.\d+(d|D)?')

    def object(self):
        return float(self[:-1] if 'd' in self or 'D' in self else self)


class LiteralBoolean(str, Stringify):

    grammar = re.compile(r'true|false')

    def object(self):
        return True if self == 'true' else False


primary_type = [LiteralFloat, LiteralDouble, LiteralLong, LiteralNumber,
                LiteralString, LiteralChar,  LiteralBoolean]


def generic_type_limited_recursion(num):

    if num > 0:
        g = generic_type_limited_recursion(num - 1)
    else:
        g = word

    class GenericRecursion(Stringify):

        grammar = (
            attr('name', common_name),
            attr('generic', optional('<',  csl(g), '>')),
            attr('array_suffix', optional(array_symbols))
        )

        def object(self):
            return {
                'name': self.name,
                'generic': [x.object() for x in self.generic] if len(self.generic) > 0 else None,
                'array_suffix': self.array_suffix,
            }

    return GenericRecursion


class ParameterType(generic_type_limited_recursion(5)):
    '''Limited recursion with 5 of the depth.

    Output: `json`
        {
            "name": str,
            "generic": ?[`ParameterType`],
            "array_suffix": ?str,
        }
    '''


class ReturnType(ParameterType):
    '''Alias of parameter type'''
    pass


class Parameter(Stringify):
    '''Output: `json`
        {
            "name": str,
            "type": ParameterType,
        }
    '''

    grammar = attr('type', ParameterType), name()

    def object(self):
        return {
            'name': self.name,
            'type': self.type.object(),
        }


class Parameters(List, Stringify):
    '''Output: `json`
        [Parameter]
    '''
    grammar = csl(Parameter)

    def object(self):
        return [x.object() for x in self]


class AnnotationKeyValuePair(Stringify):
    '''Output: `json`
        {
            "key": str,
            "value": str,
        }
    '''

    grammar = attr('key', common_name), '=', attr(
        'value', [common_name, primary_type])

    def object(self):
        return {
            'key': self.key,
            'value': self.value.object() if type(self.value) != str else self.value
        }


class AnnotationParameters(List, Stringify):
    '''Parameters of annotation, see details as shown below

    Output: `json`
        [str | PrimaryType | {"key": str, "value": any}]
    '''

    grammar = csl([
        AnnotationKeyValuePair,
        common_name,
        common_with_attribute,
        primary_type,
    ])

    def object(self):
        return [
            x.object() if type(x) != str else x
            for x in self
        ]


class Annotation(Stringify):
    '''Parameters of annotation maybe formatted as shown below.

        - @Annotation(variable[, another])
        - @Annotation("value"[, "another"])
        - @Annotation(Object.attribute[, Object.another])
        - @Annotation(key = value[, anotherKey = anotherValue])

    Output: `json`
        {
            "name": str,
            "parameters": ?[str],
        }
    '''

    grammar = '@', name(), attr('parameters', optional('(', AnnotationParameters, ')'))

    def object(self):
        return {
            'name': self.name,
            'parameters': self.parameters.object() if self.parameters is not None else None,
        }
