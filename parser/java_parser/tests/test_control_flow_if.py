'''
Unit Test.

Target: Control Flow If
'''

import unittest
import json

from pypeg2 import *

# Test target
from parser.java_parser.control_flow import (
    Condition, ControlFlow,
    IfClause, ElseIfClause, ElseClause
)


class TestCondition(unittest.TestCase):

    def test_case_exp1(self):
        '''Single condition EXPRESSION'''

        expected = {
            'first': {
                'body': 'condition', 'isNot': False, 'type': 'EXPRESSION',
            },
            'rest': None,
        }
        test = 'condition'
        parsed = parse(test, Condition)
        print(parsed)
        self.assertEqual(parsed.object(), expected, 'Not matched.')

    def test_case_exp2(self):
        '''Single condition EXPRESSION'''

        expected = {
            'first': {
                'body': 'condition', 'isNot': True, 'type': 'EXPRESSION',
            },
            'rest': None,
        }
        test = '!condition'
        parsed = parse(test, Condition)
        print(parsed)
        self.assertEqual(parsed.object(), expected, 'Not matched.')

    def test_case_exp3(self):
        '''Single condition EXPRESSION'''

        expected = {
            'first': {
                'body': {'name': 'condition', 'parameters': [], 'chain': None},
                'isNot': True, 'type': 'EXPRESSION',
            },
            'rest': None,
        }
        test = '!condition()'
        parsed = parse(test, Condition)
        print(parsed)
        self.assertEqual(parsed.object(), expected, 'Not matched.')

    def test_case_exp4(self):
        '''Single condition EXPRESSION'''

        expected = {
            'first': {
                'body': {
                    'name': 'condition',
                    'parameters': ['some', 'value'],
                    'chain': None
                },
                'isNot': True, 'type': 'EXPRESSION',
            },
            'rest': None,
        }
        test = '!condition(some, value)'
        parsed = parse(test, Condition)
        print(parsed)
        self.assertEqual(parsed.object(), expected, 'Not matched.')

    def test_case_com1(self):
        '''Single condition COMPARISON'''

        expected = {
            'first': {
                'left': {
                    'body': 'part1', 'isNot': False, 'type': 'EXPRESSION',
                },
                'right': {
                    'body': 'part2', 'isNot': False, 'type': 'EXPRESSION',
                },
                'operator': '==',
                'type': 'COMPARISON',
            },
            'rest': None,
        }
        test = 'part1 == part2'
        parsed = parse(test, Condition)
        print(parsed)
        self.assertEqual(parsed.object(), expected, 'Not matched.')

    def test_case_com2(self):
        '''Single condition COMPARISON'''

        expected = {
            'first': {
                'left': {
                    'body': 'name.attribute', 'isNot': False, 'type': 'EXPRESSION',
                },
                'right': {
                    'body': 'part2', 'isNot': False, 'type': 'EXPRESSION',
                },
                'operator': '!=',
                'type': 'COMPARISON',
            },
            'rest': None,
        }
        test = 'name.attribute != part2'
        parsed = parse(test, Condition)
        print(parsed)
        self.assertEqual(parsed.object(), expected, 'Not matched.')

    def test_case_com3(self):
        '''Single condition COMPARISON'''

        expected = {
            'first': {
                'left': {
                    'body': {
                        'name': 'name.method',
                        'parameters': [],
                        'chain': None,
                    },
                    'isNot': False,
                    'type': 'EXPRESSION',
                },
                'right': {
                    'body': 0, 'isNot': False, 'type': 'EXPRESSION',
                },
                'operator': '>',
                'type': 'COMPARISON',
            },
            'rest': None,
        }
        test = 'name.method() > 0'
        parsed = parse(test, Condition)
        print(parsed)
        self.assertEqual(parsed.object(), expected, 'Not matched.')

    def test_case_com4(self):
        '''Single condition COMPARISON'''

        expected = {
            'first': {
                'left': {
                    'body': {'name': 'left.method', 'parameters': ['Arg'], 'chain': None},
                    'isNot': False, 'type': 'EXPRESSION',
                },
                'right': {
                    'body': {'name': 'rightPart', 'parameters': ['this', 'that'], 'chain': None},
                    'isNot': False, 'type': 'EXPRESSION',
                },
                'operator': '<=',
                'type': 'COMPARISON',
            },
            'rest': None,
        }
        test = 'left.method("Arg") <= rightPart(this, that)'
        parsed = parse(test, Condition)
        print(parsed)
        self.assertEqual(parsed.object(), expected, 'Not matched.')

    def test_case_nc1(self):
        '''Single condition NESTED_CONDITION'''

        expected = {
            'first': {
                'body': {
                    'first': {
                        'body': 'part1',
                        'isNot': False,
                        'type': 'EXPRESSION'
                    },
                    'rest': [
                        {
                            'operator': '||',
                            'body': {
                                'first': {
                                        'body': 'part2',
                                                'isNot': False,
                                    'type': 'EXPRESSION'
                                },
                                'rest': None
                            }
                        },
                        {
                            'operator': '&&',
                            'body': {
                                'first': {
                                        'body': {
                                            'first': {
                                                'body': 'another',
                                                        'isNot': False,
                                                        'type': 'EXPRESSION'
                                            },
                                            'rest': [
                                                {
                                                    'operator': '&&',
                                                    'body': {
                                                                'first': {
                                                                    'body': 'more',
                                                                            'isNot': True,
                                                                            'type': 'EXPRESSION'
                                                                },
                                                        'rest': None
                                                    }
                                                },
                                                {
                                                    'operator': '||',
                                                    'body': {
                                                                'first': {
                                                                    'body': 'last',
                                                                            'isNot': False,
                                                                            'type': 'EXPRESSION'
                                                                },
                                                        'rest': None
                                                    }
                                                }
                                            ]
                                        },
                                    'isNot': False,
                                    'type': 'NESTED_CONDITION'
                                },
                                'rest': None
                            }
                        }
                    ]
                },
                'isNot': False,
                'type': 'NESTED_CONDITION'
            },
            'rest': [
                {
                    'operator': '||',
                    'body': {
                        'first': {
                                'body': 'part3',
                                'isNot': False,
                                        'type': 'EXPRESSION'
                        },
                        'rest': None
                    }
                },
                {
                    'operator': '&&',
                    'body': {
                        'first': {
                                'body': 'part4',
                                'isNot': False,
                                        'type': 'EXPRESSION'
                        },
                        'rest': None
                    }
                },
                {
                    'operator': '||',
                    'body': {
                        'first': {
                                'body': 'part5',
                                'isNot': False,
                                        'type': 'EXPRESSION'
                        },
                        'rest': None
                    }
                }
            ]
        }
        test = '(part1 || part2 && (another && !more || last)) || part3 && part4 || part5'
        parsed = parse(test, Condition)
        print(parsed)
        self.assertEqual(parsed.object(), expected, 'Not matched.')


class TestIfFlow(unittest.TestCase):
    '''
    The grammars inside `if` are all tested, 
    so for `if` it's just ok if parse is past.
    '''

    def test_case_if1(self):
        '''If single line'''

        test = 'if (someConditions) '
        parsed = parse(test, IfClause)
        print(parsed)
        # assert False

    def test_case_elif1(self):
        '''Else if multiple line'''

        test = 'else if (someConditions)'
        parsed = parse(test, ElseIfClause)
        print(parsed)
        # assert False

    def test_case_else1(self):
        '''Else multiple line'''

        test = 'else'
        parsed = parse(test, ElseClause)
        print(parsed)
        # assert False

    def test_case_cf1(self):
        '''If'''

        test = '''  if (someConditions) {
            doSomeThingHere(Parameter);
            doSomeThingHere(Parameter);
            doSomeThingHere(Parameter);
        } else if (otherConditions) {
            doOtherThingHere(OtherParameter);
            doOtherThingHere(OtherParameter);
            doOtherThingHere(OtherParameter);
        } else {
            maybeSomeCleanUpHere();
        }'''
        parsed = parse(test, ControlFlow)
        print(parsed)
        # assert False

    def test_case_cf2(self):
        '''If'''

        test = '''if (someConditions) {
            doSomeThingHere(Parameter);
            doSomeThingHere(Parameter);
            doSomeThingHere(Parameter);
        }'''
        parsed = parse(test, ControlFlow)
        print(parsed)
        # assert False

    def test_case_cf3(self):
        '''If'''

        test = '''if (someConditions) {
            doSomeThingHere(Parameter);
            doSomeThingHere(Parameter);
            doSomeThingHere(Parameter);
        } else {
            maybeSomeCleanUpHere();
        }'''
        parsed = parse(test, ControlFlow)
        print(parsed)
        # assert False

    def test_case_cf4(self):
        '''If'''

        test = '''if (someConditions) {
            doSomeThingHere(Parameter);
            doSomeThingHere(Parameter);
            doSomeThingHere(Parameter);
        } else {
            maybeSomeCleanUpHere();
        }
        if (another) {
            doSomeThingHere(Parameter);
        } else {
            maybeSomeCleanUpHere();
        }'''
        parsed = parse(test, some(ControlFlow))
        print([str(x) for x in parsed])
        # assert False

    def test_case_cf5(self):
        '''If'''

        test = '''if (someConditions) {
            if (another) {
                doSomeThingHere(Parameter);
            } else {
                maybeSomeCleanUpHere();
            }
            doSomeThingHere(Parameter);
            doSomeThingHere(Parameter);
            doSomeThingHere(Parameter);
        } else {
            maybeSomeCleanUpHere();
        }
        '''
        parsed = parse(test, ControlFlow)
        print(parsed)
        # assert False

    def test_case_cf6(self):
        '''If'''

        test = '''if (someConditions) {
            doSomeThingHere1(Parameter);
            doSomeThingHere2(Parameter);
            doSomeThingHere3(Parameter);
        }
        if (another) {
            doSomeThingHere(Parameter);
        }'''
        parsed = parse(test, some(ControlFlow))
        print([str(x) for x in parsed])
        # assert False


if __name__ == '__main__':
    pass
