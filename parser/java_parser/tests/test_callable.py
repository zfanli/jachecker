'''
Unit Test.

Target: callable
'''

import unittest
import json

from pypeg2 import *

# Test target
from parser.java_parser.callable import CallableName


class TestCallableName(unittest.TestCase):

    def test_case_cn1(self):
        '''Callable name'''

        expected = {'name': 'callable', 'parameters': [], 'chain': None}
        test = 'callable()'
        parsed = parse(test, CallableName)
        print(parsed)
        self.assertEqual(parsed.object(), expected, 'Not matched.')

    def test_case_cn2(self):
        '''Callable name'''

        expected = {
            'name': 'CallableName',
            'parameters': ['Variable'],
            'chain': None
        }
        test = 'CallableName(Variable)'
        parsed = parse(test, CallableName)
        print(parsed)
        self.assertEqual(parsed.object(), expected, 'Not matched.')

    def test_case_cn3(self):
        '''Callable name'''

        expected = {
            'name': 'CallableName',
            'parameters': ['Variable', 'Another'],
            'chain': None
        }
        test = 'CallableName(Variable, Another)'
        parsed = parse(test, CallableName)
        print(parsed)
        self.assertEqual(parsed.object(), expected, 'Not matched.')

    def test_case_cn4(self):
        '''Callable name with literal parameters'''

        expected = {
            'name': 'CallableName',
            'parameters': ['Literal', 123],
            'chain': None
        }
        test = 'CallableName("Literal", 123)'
        parsed = parse(test, CallableName)
        print(parsed)
        self.assertEqual(parsed.object(), expected, 'Not matched.')

    def test_case_cn5(self):
        '''Callable name recursion'''

        expected = {
            'name': 'CallableName',
                    'parameters': [
                        {
                            'name': 'recursion',
                            'parameters': [],
                            'chain': None
                        },
                        'another'
                    ],
            'chain': None
        }
        test = 'CallableName(recursion(), another)'
        parsed = parse(test, CallableName)
        print(parsed)
        self.assertEqual(parsed.object(), expected, 'Not matched.')

    def test_case_cn6(self):
        '''Callable name recursion'''

        expected = {
            'name': 'CallableName',
                    'parameters': [
                        {
                            'name': 'recursion',
                            'parameters': [],
                            'chain': None
                        },
                        {
                            'name': 'another',
                            'parameters': ['someValues', 'last'],
                            'chain': None},
                    ],
            'chain': None
        }
        test = 'CallableName(recursion(), another(someValues, last))'
        parsed = parse(test, CallableName)
        print(parsed)
        self.assertEqual(parsed.object(), expected, 'Not matched.')

    def test_case_cn7(self):
        '''Callable name with attribute'''

        expected = {
            'name': 'CallableName.attribute',
                    'parameters': [
                        {
                            'name': 'recursion',
                            'parameters': [],
                            'chain': None
                        },
                        {
                            'name': 'another',
                            'parameters': ['someValues', 'last'],
                            'chain': None
                        },
                    ],
            'chain': None
        }
        test = 'CallableName.attribute(recursion(), another(someValues, last))'
        parsed = parse(test, CallableName)
        print(parsed)
        self.assertEqual(parsed.object(), expected, 'Not matched.')

    def test_case_cn8(self):
        '''Callable name with attribute'''

        expected = {
            'name': 'CallableName.attribute',
                    'parameters': [
                        {
                            'name': 'recursion.test',
                            'parameters': [],
                            'chain': None},
                        {
                            'name': 'another',
                            'parameters': ['someValues', 'last'],
                            'chain': None
                        },
                    ],
            'chain': None,
        }
        test = 'CallableName.attribute(recursion.test(), another(someValues, last))'
        parsed = parse(test, CallableName)
        print(parsed)
        self.assertEqual(parsed.object(), expected, 'Not matched.')

    def test_case_cn9(self):
        '''Callable name with generic type'''

        expected = {
            'name': 'target.<generic> doThat',
            'parameters': [],
            'chain': [{
                'name': 'doThis',
                'parameters': [],
                'chain':None
            }],
        }
        test = 'target.<generic> doThat().doThis()'
        parsed = parse(test, CallableName)
        print(parsed)
        self.assertEqual(parsed.object(), expected, 'Not matched.')

    def test_case_cn10(self):
        '''Callable name with attribute'''

        expected = {
            'name': 'CallableName.attribute',
            'parameters': [
                {
                    'name': 'recursion.test',
                    'parameters': [],
                    'chain': [
                            {
                                'name': 'other',
                                'parameters': [],
                                'chain': None
                            }
                    ]
                },
                {
                    'name': 'another',
                    'parameters': [
                        'someValues',
                        'last'
                    ],
                    'chain': [
                        {
                            'name': 'doThis',
                            'parameters': [],
                            'chain': None
                        },
                        {
                            'name': 'doThat',
                            'parameters': [],
                            'chain': None
                        }
                    ]
                }
            ],
            'chain': [
                {
                    'name': 'chainMethod',
                    'parameters': [],
                    'chain': None
                }
            ]
        }
        test = 'CallableName.attribute(recursion.test().other(), another(someValues, last).doThis().doThat()).chainMethod()'
        parsed = parse(test, CallableName)
        print(parsed)
        self.assertEqual(parsed.object(), expected, 'Not matched.')


if __name__ == '__main__':
    pass
