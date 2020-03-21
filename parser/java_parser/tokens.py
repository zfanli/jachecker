'''
Tokens, Symbols.
'''

import re

from pypeg2 import *


param_type = re.compile(r'([a-zA-Z0-9]+)((<|\[|)(|[a-zA-Z0-9]+)(>|\]))')


class AccessModifier(Keyword):
    '''Access control modifiers'''

    grammar = Enum(
        K('default'),
        K('public'),
        K('protected'),
        K('private'),
    )


class NonAccessModifier(Keyword):
    '''Non-Access modifiers'''

    grammar = Enum(
        K('final'),
        K('static'),
        K('transient'),
        K('synchronized'),
        K('volatile'),
    )


class ReturnType(str):

    grammar = name()


class ParameterType(str):

    grammar = attr('name', param_type)


class Parameter:

    grammar = attr('type', ParameterType), name()

    def json(self):
        return {
            'name': self.name,
            'type': self.type
        }


class Parameters(List):

    grammar = csl(Parameter)
