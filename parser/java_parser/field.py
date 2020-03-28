'''
Deal with class fields.
'''

from pypeg2 import *

from parser.java_parser.tokens import Modifier, CommonName
from parser.java_parser.annotation import Annotation
from parser.java_parser.variable import VariableType
from parser.java_parser.mixins import Stringify
from parser.java_parser.comment import Comment


rest_before_end = re.compile(r'.*(?<!;)')


class Field(Stringify):
    '''Class field.

    Output: `json`
        {
            "name": str,
            "type": VariableType,
            "modifiers": [Modifier],
            "initialValue": str,
            "lineno": number,
        }
    '''

    grammar = (
        attr('comments', optional(Comment)),
        attr('annotations', maybe_some(Annotation)),
        attr('modifiers', maybe_some(Modifier)),
        attr('type', VariableType),
        attr('name', CommonName),
        attr('initialValue', optional('=', rest_before_end)), ';'
    )

    def object(self):
        return {
            'name': self.name.object(),
            'type': self.type.object(),
            'modifiers': [x.object() for x in self.modifiers],
            'annotations': [x.object() for x in self.annotations],
            'initialValue': self.initialValue,
            'lineno': self.position_in_text[0],
        }


if __name__ == '__main__':
    pass
