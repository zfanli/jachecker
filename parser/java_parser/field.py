'''
Deal with class fields.
'''

from pypeg2 import *

from parser.java_parser.tokens import Modifier, VariableType, CommonName
from parser.java_parser.mixins import Stringify


rest_before_end = re.compile(r'.*(?<!;)')


class Field(Stringify):
    '''Class field.

    Output: `json`
        {
            "name": str,
            "type": VariableType,
            "modifiers": [Modifier],
            "initialValue": str,
        }
    '''

    grammar = (
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
            'initialValue': self.initialValue,
            'lineno': self.position_in_text[0],
        }
