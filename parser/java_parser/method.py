'''
Deal with class methods.
'''

from pypeg2 import *
from pypeg2 import blank, endl

from parser.java_parser.tokens import *


class Method(List):

    grammar = (
        optional(attr('head_non_access_modifier', NonAccessModifier)), blank,
        optional(attr('access_modifier', AccessModifier)), blank,
        optional(attr('main_non_access_modifier', NonAccessModifier)), blank,
        optional(attr('second_non_access_modifier', NonAccessModifier)), blank,
        attr('return_type', ReturnType), blank,
        name(),
        '(', optional(attr('parameters', Parameters)), ')',
        '{', restline, '}',
    )

    def json(self):
        return {
            'name': self.name,
            'head_non_access_modifier': self.head_non_access_modifier,
            'access_modifier': self.access_modifier,
            'main_non_access_modifier': self.main_non_access_modifier,
            'second_non_access_modifier': self.second_non_access_modifier,
            'return_type': self.return_type,
            'parameters': self.parameters,
            'body': self,
        }


if __name__ == '__main__':
    pass
