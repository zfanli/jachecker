'''
Unit Test.

Target: tokens
'''

import unittest
import json

from pypeg2 import *

# Test target
from parser.java_parser.tokens import *


class TestAccessModifiers(unittest.TestCase):

    def test_case1(self):
        '''Check all keywords'''

        test = ['default', 'public', 'protected', 'private']
        parsed = parse(' '.join(test), some(AccessModifier))
        self.assertEqual(parsed, test, 'Access modifiers are not ok.')


class TestNonAccessModifiers(unittest.TestCase):

    def test_case1(self):
        '''Check all keywords'''

        test = ['final', 'static', 'transient', 'synchronized', 'volatile']
        parsed = parse(' '.join(test), some(NonAccessModifier))
        self.assertEqual(parsed, test, 'Non-Access modifiers are not ok.')


class TestParameterType(unittest.TestCase):

    def test_case1(self):
        '''Simple parameter'''

        test = 'String'
        parsed = parse(test, ParameterType)
        self.assertEqual(parsed, test, 'Not matched.')

    def test_case2(self):
        '''Array'''

        test = 'int[]'
        parsed = parse(test, ParameterType)
        self.assertEqual(parsed, 'int', 'Not matched.')
        self.assertEqual(parsed.array_suffix, '[]', 'Should be an array.')

    def test_case3(self):
        '''Generic'''

        test = 'List<String>'
        parsed = parse(test, ParameterType)
        self.assertEqual(parsed, 'List', 'Not matched.')
        self.assertEqual(parsed.generic, ['String'],
                         'Generic should be `[String]`.')

    def test_case4(self):
        '''Complicated case'''

        test = 'ArrayList<LinkedHashMap<String[], Object>>'
        parsed = parse(test, ParameterType)
        self.assertEqual(parsed, 'ArrayList', 'Not matched.')
        self.assertEqual(parsed.generic, ['LinkedHashMap'],
                         'Generic should be `[LinkedHashMap]`.')
        self.assertEqual(parsed.generic[0].generic, ['String', 'Object'],
                         'Generic should be `[String, Object]`.')
        self.assertEqual(parsed.generic[0].generic[0].array_suffix, '[]',
                         'Should be an array.')

    def test_case5(self):
        '''Another complicated case'''

        test = 'LinkedHashMap<String[], Object>[]'
        parsed = parse(test, ParameterType)
        self.assertEqual(parsed, 'LinkedHashMap', 'Not matched.')
        self.assertEqual(parsed.array_suffix, '[]', 'Should be an array.')
        self.assertEqual(parsed.generic, ['String', 'Object'],
                         'Should be `[String, Object]`.')
        self.assertEqual(parsed.generic[0].array_suffix,
                         '[]', 'Should be an array.')

    def test_case6(self):
        '''More dimensions of arrays'''

        test = 'String[][][]'
        parsed = parse(test, ParameterType)
        self.assertEqual(parsed.array_suffix, '[][][]', 'Not matched.')

    def test_case7(self):
        '''Recurision case, till 3 of the depth, enough for most case.'''

        test = 'ArrayList<LinkedHashMap<String[], HashMap<String, T<Object>>>>'
        parsed = parse(test, ParameterType)
        self.assertEqual(parsed, 'ArrayList', 'Not matched.')
        self.assertEqual(parsed.generic, ['LinkedHashMap'],
                         'Generic should be `[LinkedHashMap]`.')
        self.assertEqual(parsed.generic[0].generic, ['String', 'HashMap'],
                         'Generic should be `[String, HashMap]`.')
        self.assertEqual(parsed.generic[0].generic[0].array_suffix, '[]',
                         'Should be an array.')
        self.assertEqual(parsed.generic[0].generic[1].generic, ['String', 'T'],
                         'Generic should be `[String, T]`.')
        self.assertEqual(parsed.generic[0].generic[1].generic[1].generic, ['Object'],
                         'Generic should be `[Object]`.')


if __name__ == '__main__':
    pass
