'''
Unit Test.

Target: field
'''

import unittest
import json

from pypeg2 import *

# Test target
from parser.java_parser.field import *


class TestField(unittest.TestCase):

    def test_case_f1(self):
        '''Field'''

        expected = {
            'name': 'SOME_CONSTANT',
            'type': {'name': 'String', 'generic': None, 'arraySuffix': None},
            'modifiers': [
                {'name': 'private', 'type': 'ACCESS_MODIFIER'},
                {'name': 'static', 'type': 'NON_ACCESS_MODIFIER'},
                {'name': 'final', 'type': 'NON_ACCESS_MODIFIER'},
            ],
            'annotations': [],
            'initialValue': '"SOME_CONSTANT"',
            'lineno': 1,
        }
        test = 'private static final String SOME_CONSTANT = "SOME_CONSTANT";'
        parsed = parse(test, Field)
        print(parsed)
        self.assertEqual(parsed.object(), expected, 'Not matched')

    def test_case_f2(self):
        '''Field'''

        expected = {
            'name': 'number',
            'type': {'name': 'int', 'generic': None, 'arraySuffix': None},
            'modifiers': [
                {'name': 'private', 'type': 'ACCESS_MODIFIER'},
            ],
            'annotations': [],
            'initialValue': '12345',
            'lineno': 1,
        }
        test = 'private int number = 12345;'
        parsed = parse(test, Field)
        self.assertEqual(parsed.object(), expected, 'Not matched')

    def test_case_f3(self):
        '''Field'''

        expected = {
            'name': 'map',
            'type': {
                'name': 'Map',
                'generic': [
                    {'name': 'String', 'generic': None, 'arraySuffix': None},
                    {'name': 'String', 'generic': None, 'arraySuffix': None},
                ],
                'arraySuffix': None
            },
            'modifiers': [
                {'name': 'protected', 'type': 'ACCESS_MODIFIER'},
            ],
            'annotations': [],
            'initialValue': 'new HashMap<>()',
            'lineno': 1,
        }
        test = 'protected Map<String, String> map = new HashMap<>();'
        parsed = parse(test, Field)
        self.assertEqual(parsed.object(), expected, 'Not matched')

    def test_case_f4(self):
        '''Field'''

        expected = {
            'name': 'sb',
            'type': {'name': 'StringBuilder', 'generic': None, 'arraySuffix': None},
            'modifiers': [
                {'name': 'private', 'type': 'ACCESS_MODIFIER'},
            ],
            'annotations': [],
            'initialValue': None,
            'lineno': 1,
        }
        test = 'private StringBuilder sb;'
        parsed = parse(test, Field)
        self.assertEqual(parsed.object(), expected, 'Not matched')

    def test_case_f5(self):
        '''Field'''

        expected = {
            'name': 'flag',
            'type': {'name': 'boolean', 'generic': None, 'arraySuffix': None},
            'modifiers': [
                {'name': 'public', 'type': 'ACCESS_MODIFIER'},
            ],
            'annotations': [],
            'initialValue': 'false',
            'lineno': 1,
        }
        test = 'public boolean flag = false;'
        parsed = parse(test, Field)
        self.assertEqual(parsed.object(), expected, 'Not matched')

    def test_case_f6(self):
        '''Field'''

        expected = {
            'name': 'flag',
            'type': {'name': 'boolean', 'generic': None, 'arraySuffix': None},
            'modifiers': [],
            'annotations': [],
            'initialValue': 'false',
            'lineno': 1,
        }
        test = 'boolean flag = false;'
        parsed = parse(test, Field)
        self.assertEqual(parsed.object(), expected, 'Not matched')

    def test_case_f6(self):
        '''Field, just check pass'''

        test = '''@Annotation
        @Another(Some, Values, Here)
        boolean flag = false;'''
        parsed = parse(test, Field)
        print(parsed)
        # assert False


if __name__ == '__main__':
    pass
