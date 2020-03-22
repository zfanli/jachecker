'''
Tokens, Symbols.
'''

import re

from pypeg2 import *


param_type = re.compile(r'([\w\d]+)')
param_type_flat_array = re.compile(r'([\w\d]+)(\[\])*')
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


def generic_type_limited_recursion(num):

    if num > 0:
        g = generic_type_limited_recursion(num - 1)
    else:
        g = word

    class GenericRecursion(str):
        grammar = (
            param_type,
            attr('generic', optional('<',  csl(g), '>')),
            attr('array_suffix', optional(array_symbols))
        )

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


class Parameter:
    '''Output: `json`
        {
            "name": str,
            "type": ParameterType,
        }
    '''

    grammar = attr('type', ParameterType), name()


class Parameters(List):
    '''Output: `json`
        [Parameter]
    '''
    grammar = csl(Parameter)
