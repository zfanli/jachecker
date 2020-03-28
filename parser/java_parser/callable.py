'''
Deal with single callable operation.
'''

import re
import json

from pypeg2 import *

from parser.java_parser.tokens import CommonName, CommonNameAttribute, PrimaryType
from parser.java_parser.mixins import Stringify, Literal

RECURSION_LEVEL = 5


class ChainNameWithGeneric(Stringify):

    grammar = (
        attr('name', CommonName),
        attr('chain', some('.', re.compile(r'(<.*?>(\s?))?([\w\d_]+)+'))),
    )

    def object(self):
        return '.'.join([self.name] + self.chain)


def callable_limited_recursion(num, flat=False):

    if num == 0:
        cal = CommonName
        cal_flat = CommonName
    else:
        cal = callable_limited_recursion(num - 1)
        cal_flat = callable_limited_recursion(num - 1, flat=True)

    class CallableConstructor(Stringify):

        grammar = (
            attr('name', [ChainNameWithGeneric, CommonName]),
            '(',
            attr(
                'parameters',
                optional(csl([cal, PrimaryType, CommonNameAttribute, CommonName]))),
            ')',
            attr('chain', maybe_some('.', cal_flat) if not flat else None),
        )

        def object(self):
            return {
                'name': self.name.object(),
                'parameters': [x.object() for x in self.parameters],
                'chain': [x.object() for x in self.chain] if self.chain else None,
            }

    return CallableConstructor


class CallableName(callable_limited_recursion(RECURSION_LEVEL)):
    pass


if __name__ == '__main__':
    pass
