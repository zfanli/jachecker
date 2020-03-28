'''
Variables.
'''

import re
import json

from pypeg2 import *

from parser.java_parser.tokens import CommonName, SymbolArray
from parser.java_parser.annotation import Annotation
from parser.java_parser.mixins import Stringify, Literal


def generic_type_limited_recursion(num):

    if num > 0:
        g = generic_type_limited_recursion(num - 1)
    else:
        g = word

    class GenericRecursion(Stringify):

        grammar = (
            attr('name', CommonName),
            attr('generic', optional('<',  csl(g), '>')),
            attr('arraySuffix', optional(SymbolArray))
        )

        def object(self):
            return {
                'name': self.name,
                'generic': [x.object() for x in self.generic] if len(self.generic) > 0 else None,
                'arraySuffix': self.arraySuffix,
            }

    return GenericRecursion


class ParameterType(generic_type_limited_recursion(5)):
    '''Limited recursion with 5 of the depth.

    Output: `json`
        {
            "name": str,
            "generic": ?[`ParameterType`],
            "arraySuffix": ?str,
        }
    '''
    pass


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

    grammar = (
        attr('annotation', optional(Annotation)),
        attr('type', ParameterType),
        attr('name', CommonName),
    )

    def object(self):
        return {
            'name': self.name.object(),
            'type': self.type.object(),
            'annotation': self.annotation.object() if self.annotation else None,
        }


class Parameters(List, Stringify):
    '''Output: `json`
        [Parameter]
    '''
    grammar = csl(Parameter)

    def object(self):
        return [x.object() for x in self]


if __name__ == '__main__':
    pass
