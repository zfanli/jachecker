'''
Tokens, Symbols.
'''

import re
import json

from pypeg2 import *
from parser.java_parser.mixins import Stringify, Literal


class CommonName(str, Literal):
    '''Matches like `AllName`'''

    grammar = re.compile(r'([\w\d]+)')


class CommonNameAttribute(str, Literal):
    '''Matches like `Name.attribute`'''

    grammar = re.compile(r'[\w\d]+\.[\w\d]+')


class SymbolArray(str, Literal):
    '''Matches only array suffix like `[]`, or more dimensions'''

    grammar = re.compile(r'(\[\])+')


class AccessModifier(Keyword, Stringify):
    '''Output: `json`
        {
            "name": str,
            "type": "ACCESS_MODIFIER"
        }
    '''

    grammar = Enum(
        K('default'), K('public'), K('protected'), K('private'),
    )

    def object(self):
        return {
            'name': self,
            'type': 'ACCESS_MODIFIER'
        }


class NonAccessModifier(Keyword, Stringify):
    '''Output: `json`
        {
            "name": str,
            "type": "NON_ACCESS_MODIFIER"
        }
    '''

    grammar = Enum(
        K('final'), K('static'), K('transient'),
        K('synchronized'), K('volatile'),
    )

    def object(self):
        return {
            'name': self,
            'type': 'NON_ACCESS_MODIFIER'
        }


class Modifier(Stringify):
    '''All modifiers

    Output: `json`
        {
            "name": str,
            "type": "ACCESS_MODIFIER" | "NON_ACCESS_MODIFIER"
        }
    '''

    grammar = attr('value', [AccessModifier, NonAccessModifier])

    def object(self):
        return self.value.object()


class LiteralString(str, Literal):

    grammar = re.compile(r'^".*?"', re.S)

    def object(self):
        result = self[1:-1]
        # Unescape quotes
        result = result.replace('JC_ESCAPED_QUOTE', '\\"')
        return result


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


class PrimaryType(Stringify):

    grammar = attr('value', [LiteralFloat, LiteralDouble, LiteralLong, LiteralNumber,
                             LiteralString, LiteralChar,  LiteralBoolean])

    def object(self):
        return self.value.object()


def generic_type_limited_recursion(num):

    if num > 0:
        g = generic_type_limited_recursion(num - 1)
    else:
        g = word

    class GenericRecursion(Stringify):

        grammar = (
            attr('name', CommonName),
            attr('generic', optional('<',  csl(g), '>')),
            attr('array_suffix', optional(SymbolArray))
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


class VariableType(ParameterType):
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
