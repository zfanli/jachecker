'''
Deal with most Java syntax inside method.
'''

import re

from pypeg2 import *

from parser.java_parser.tokens import CommonName, CommonNameAttribute, PrimaryType
from parser.java_parser.variable import VariableType
from parser.java_parser.callable import CallableName
from parser.java_parser.mixins import Stringify

operation = re.compile(r'^.+?(?=[};])', re.S)


class OperationAssignment(Stringify):
    '''Output: `json`
        {
            'name': str,
            'type': null | VariableType,
            'assignment': CallableName | PrimaryType | CommonNameAttribute | CommonName,
        }
    '''

    grammar = (
        [
            (attr('type', VariableType), attr('name', CommonName)),
            attr('name', CommonName),
        ],
        '=',
        flag('new', 'new'),
        attr('assignment',
             [CallableName, PrimaryType, CommonNameAttribute, CommonName, ]), ';'
    )

    def object(self):
        return {
            'name': self.name.object(),
            'type': self.type.object() if hasattr(self, 'type') else None,
            'assignment': self.assignment.object(),
            'isNew': self.new,
            'lineno': self.position_in_text[0],
        }


class OperationCallable(Stringify):

    grammar = attr('body', CallableName), ';'

    def object(self):
        return {
            'body': self.body.object(),
            'type': 'OPERATION',
            'lineno': self.position_in_text[0],
        }


class OperationReturn(Stringify):

    grammar = (
        'return',
        attr(
            'body',
            [CallableName, PrimaryType, CommonNameAttribute, CommonName, ]
        ),
        ';'
    )

    def object(self):
        return {
            'body': self.body.object(),
            'type': 'RETURN',
        }


class Operation(Stringify):
    '''Output: `json`
        {
            "operation": str,
            "lineno": number,
        }
    '''

    grammar = attr(
        'operation',
        [OperationReturn, OperationCallable, OperationAssignment]
    )

    def object(self):
        return {
            'operation': self.operation.object(),
            'lineno': self.position_in_text[0]
        }


class Operations(List, Stringify):
    '''Output: `json`
        [Operation]
    '''

    grammar = some(Operation)

    def object(self):
        return [x.object() for x in self]


if __name__ == '__main__':
    pass
