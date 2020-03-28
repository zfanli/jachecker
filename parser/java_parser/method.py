'''
Deal with class methods.
'''

from pypeg2 import *

from parser.java_parser.tokens import *
from parser.java_parser.variable import ReturnType, Parameters
from parser.java_parser.control_flow import ControlFlow
from parser.java_parser.operation import Operation
from parser.java_parser.annotation import Annotation
from parser.java_parser.comment import Comment


class Method(List, Stringify):

    grammar = (
        # attr('comments', optional(Comment)),
        attr('annotations', maybe_some(Annotation)),
        attr('modifiers', maybe_some(Modifier)),
        attr('returnType', ReturnType),
        attr('name', CommonName),
        '(', attr('parameters', optional(Parameters)), ')',
        '{', some([ControlFlow, Operation]), '}',
    )

    def object(self):
        return {
            'name': self.name.object(),
            'annotations': [x.object() for x in self.annotations],
            'modifiers': [x.object() for x in self.modifiers],
            'returnType': self.returnType.object(),
            'parameters': self.parameters.object() if self.parameters else None,
            'body': [x.object() for x in self],
            'type': 'METHOD',
        }


if __name__ == '__main__':
    pass
