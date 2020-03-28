'''
Deal with control flows.

Such like if, switch, for, while, etc.
'''

import re

from pypeg2 import *

from parser.java_parser.tokens import *
from parser.java_parser.callable import CallableName
from parser.java_parser.operation import Operation
from parser.java_parser.mixins import Stringify


def condition_limited_recursion(num, flat=False):

    if num == 0:
        con = CommonName
        con_flat = CommonName
    else:
        con = condition_limited_recursion(num - 1)
        con_flat = condition_limited_recursion(num - 1, flat=True)

    class Expression(Stringify):

        grammar = (
            flag('isNot', '!'),
            attr('body', [
                CallableName,
                PrimaryType,
                CommonNameAttribute,
                CommonName,
            ]),
        )

        def object(self):
            return {
                'body': self.body.object(),
                'isNot':  self.isNot,
                'type': 'EXPRESSION',
            }

    class NestedCondition(Stringify):

        grammar = (
            flag('isNot', '!'),
            '(', attr('body', con), ')',
        )

        def object(self):
            return {
                'body': self.body.object(),
                'isNot': self.isNot,
                'type': 'NESTED_CONDITION',
            }

    class Comparison(Stringify):

        grammar = (
            attr('left', Expression),
            attr('operator', ComparisonOperator),
            attr('right', Expression),
        )

        def object(self):
            return {
                'left': self.left.object(),
                'right': self.right.object(),
                'operator': self.operator.object(),
                'type': 'COMPARISON',
            }

    class ConditionChain(Stringify):

        grammar = attr('operator', LogicalOperator), attr('body', con_flat)

        def object(self):
            return {
                'operator': self.operator.object(),
                'body': self.body.object(),
            }

    class ConditionConstructor(Stringify):

        grammar = (
            attr('first', [Comparison, NestedCondition, Expression, ]),
            attr('rest',  maybe_some(ConditionChain) if not flat else None),
        )

        def object(self):
            return {
                'first': self.first.object(),
                'rest': [x.object() for x in self.rest] if self.rest else None,
            }

    return ConditionConstructor


class Condition(condition_limited_recursion(10)):
    pass


class ControlFlowStringifyAdopter(Stringify):

    def object(self):
        return {
            'condition': self.condition.object(),
            'body': [x.object() for x in self.body],
            'type': self.type,
            'lineno': self.position_in_text[0],
        }


class IfStringifyAdopter(Stringify):

    def object(self):
        return self.condition.object() if hasattr(self, 'condition') else None,


def create_grammar_if(symbol):

    return (
        symbol,
        attr('condition', optional('(', Condition, ')')),
    )


class IfClause(List, IfStringifyAdopter):
    '''Output: `json`
        Condition
    '''

    type = 'IF'
    grammar = create_grammar_if('if')


class ElseIfClause(List, IfStringifyAdopter):
    '''Output: `json`
        Condition
    '''

    type = 'ELSE_IF'
    grammar = create_grammar_if('else if')


class ElseClause(List, IfStringifyAdopter):
    '''Output: `json`
        Condition
    '''

    type = 'ELSE'
    grammar = 'else'


def control_flow_limited_recursion(num):

    if num == 0:
        r = CommonName
    else:
        r = control_flow_limited_recursion(num - 1)

    class ControlFlowIfClause(ControlFlowStringifyAdopter):

        type = 'IF'
        grammar = (
            attr('condition', IfClause),
            '{', attr('body', some([Operation, r])), '}',
        )

    class ControlFlowElseIfClause(ControlFlowStringifyAdopter):

        type = 'ELSE_IF'
        grammar = (
            attr('condition', ElseIfClause),
            '{', attr('body', some([Operation, r])), '}',
        )

    class ControlFlowElseClause(ControlFlowStringifyAdopter):

        type = 'ELSE'
        grammar = (
            attr('condition', ElseClause),
            '{', attr('body', some([Operation, r])), '}',
        )

    class ControlFlowIf(Stringify):

        grammar = (
            attr('if', ControlFlowIfClause),
            attr('elseIf', maybe_some(ControlFlowElseIfClause)),
            attr('else', optional(ControlFlowElseClause)),
        )

        def object(self):
            return {
                'if': getattr(self, 'if').object(),
                'elseIf': [x.object() for x in getattr(self, 'elseIf')],
                'else': getattr(self, 'else').object() if getattr(self, 'else') else None,
                'lineno': self.position_in_text[0],
            }

    class ControlFlowConstructor(Stringify):

        grammar = (
            attr('body', [ControlFlowIf]),
        )

        def object(self):

            return self.body.object()

    return ControlFlowConstructor


class ControlFlow(control_flow_limited_recursion(10)):
    pass


if __name__ == '__main__':
    pass
