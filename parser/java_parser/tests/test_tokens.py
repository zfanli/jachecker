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

    def test_case_am1(self):
        '''Check all keywords'''

        test = ['default', 'public', 'protected', 'private']
        parsed = parse(' '.join(test), some(AccessModifier))
        self.assertEqual(parsed, test, 'Access modifiers are not ok.')


class TestNonAccessModifiers(unittest.TestCase):

    def test_case_nam1(self):
        '''Check all keywords'''

        test = ['final', 'static', 'transient', 'synchronized', 'volatile']
        parsed = parse(' '.join(test), some(NonAccessModifier))
        self.assertEqual(parsed, test, 'Non-Access modifiers are not ok.')


class TestModifiers(unittest.TestCase):

    def test_case_m1(self):
        '''Simple case'''

        expected = [
            {'name': 'public', 'type': 'ACCESS_MODIFIER'},
            {'name': 'static', 'type': 'NON_ACCESS_MODIFIER'}
        ]
        test = ['public', 'static']
        parsed = parse(' '.join(test), some(Modifier))
        self.assertEqual([x.object() for x in parsed],
                         expected, 'Modifiers are not ok.')

    def test_case_m2(self):
        '''Object()'''

        expected = {'name': 'final', 'type': 'NON_ACCESS_MODIFIER'}
        test = 'final'
        parsed = parse(test, Modifier)
        self.assertEqual(parsed.object(), expected, 'Modifiers are not ok.')


class TestLiterals(unittest.TestCase):

    def test_case_literal1(self):
        '''String literal'''

        test = '"This is a String literal"'
        parsed = parse(test, LiteralString)
        self.assertEqual(parsed, test, 'Not matched.')

    def test_case_literal2(self):
        '''String literal'''

        test = '""'
        parsed = parse(test, LiteralString)
        self.assertEqual(parsed, test, 'Empty is not matched.')

    def test_case_literal3(self):
        '''String literal'''

        test = '"1 + 1"'
        parsed = parse(test, LiteralString)
        self.assertEqual(parsed.object(), test[1:-1], 'Not matched.')

    def test_case_literal4(self):
        '''String literal'''

        expected = 'some escaped quotes like \\"\\"\\"\\"'
        test = expected.replace('\\"', 'JC_ESCAPED_QUOTE')
        parsed = parse(f'"{test}"', LiteralString)
        self.assertEqual(parsed.object(), expected,
                         'Escaped quotes are not ok.')

    def test_case_literal5(self):
        '''String literal'''

        test = '"Special symbols: +-*/[]~!#$%^&()_`<>\t\n\n\n\n"'
        parsed = parse(test, LiteralString)
        self.assertEqual(parsed, test, 'Multiple line is not ok.')

    def test_case_literal6(self):
        '''Char literal'''

        expected = 'A'
        test = f"'{expected}'"
        parsed = parse(test, LiteralChar)
        self.assertEqual(parsed.object(), expected, 'Not matched.')

    def test_case_literal7(self):
        '''Number literal'''

        expected = 1234567
        test = f'{expected}'
        parsed = parse(test, LiteralNumber)
        self.assertEqual(parsed.object(), expected, 'Not matched.')

    def test_case_literal8(self):
        '''Float literal'''

        expected = 123.14124
        test = f'{expected}f'
        parsed = parse(test, LiteralFloat)
        self.assertEqual(parsed.object(), expected, 'Not matched.')

    def test_case_literal9(self):
        '''Float literal'''

        expected = 123.14124
        test = f'{expected}F'
        parsed = parse(test, LiteralFloat)
        self.assertEqual(parsed.object(), expected, 'Not matched.')

    def test_case_literal10(self):
        '''Long literal'''

        expected = 1234567890
        test = f'{expected}l'
        parsed = parse(test, LiteralLong)
        self.assertEqual(parsed.object(), expected, 'Not matched.')

    def test_case_literal11(self):
        '''Long literal'''

        expected = 1234567890
        test = f'{expected}L'
        parsed = parse(test, LiteralLong)
        self.assertEqual(parsed.object(), expected, 'Not matched.')

    def test_case_literal12(self):
        '''Double literal'''

        expected = 12345.6789
        test = f'{expected}'
        parsed = parse(test, LiteralDouble)
        self.assertEqual(parsed.object(), expected, 'Not matched.')

    def test_case_literal13(self):
        '''Double literal'''

        expected = 12345.6789
        test = f'{expected}d'
        parsed = parse(test, LiteralDouble)
        self.assertEqual(parsed.object(), expected, 'Not matched.')

    def test_case_literal14(self):
        '''Double literal'''

        expected = 12345.6789
        test = f'{expected}D'
        parsed = parse(test, LiteralDouble)
        self.assertEqual(parsed.object(), expected, 'Not matched.')

    def test_case_literal15(self):
        '''Double literal'''

        test = 'true'
        parsed = parse(test, LiteralBoolean)
        self.assertTrue(parsed.object(), 'Not matched.')

    def test_case_literal16(self):
        '''Double literal'''

        test = 'false'
        parsed = parse(test, LiteralBoolean)
        self.assertFalse(parsed.object(), 'Not matched.')


class TestPrimaryType(unittest.TestCase):

    def test_case_pri1(self):
        '''Primary types'''

        expected = 'String'
        test = f'"{expected}"'
        parsed = parse(test, PrimaryType)
        self.assertEqual(parsed.object(), expected, 'Not matched')

    def test_case_pri2(self):
        '''Primary types'''

        expected = 'Z'
        test = f"'{expected}'"
        parsed = parse(test, PrimaryType)
        self.assertEqual(parsed.object(), expected, 'Not matched')

    def test_case_pri3(self):
        '''Primary types'''

        expected = 1234
        test = f'{expected}'
        parsed = parse(test, PrimaryType)
        self.assertEqual(parsed.object(), expected, 'Not matched')

    def test_case_pri4(self):
        '''Primary types'''

        expected = 1234
        test = f'{expected}l'
        parsed = parse(test, PrimaryType)
        self.assertEqual(parsed.object(), expected, 'Not matched')

    def test_case_pri5(self):
        '''Primary types'''

        expected = 1234.13
        test = f'{expected}F'
        parsed = parse(test, PrimaryType)
        self.assertEqual(parsed.object(), expected, 'Not matched')

    def test_case_pri6(self):
        '''Primary types'''

        expected = 1234.124
        test = f'{expected}f'
        parsed = parse(test, PrimaryType)
        self.assertEqual(parsed.object(), expected, 'Not matched')

    def test_case_pri7(self):
        '''Primary types'''

        expected = 1234.124
        test = f'{expected}d'
        parsed = parse(test, PrimaryType)
        self.assertEqual(parsed.object(), expected, 'Not matched')

    def test_case_pri8(self):
        '''Primary types'''

        expected = 1234.124
        test = f'{expected}D'
        parsed = parse(test, PrimaryType)
        self.assertEqual(parsed.object(), expected, 'Not matched')

    def test_case_pri9(self):
        '''Primary types'''

        expected = 1234.124
        test = f'{expected}'
        parsed = parse(test, PrimaryType)
        self.assertEqual(parsed.object(), expected, 'Not matched')


class TestParameterType(unittest.TestCase):

    def test_case_pt1(self):
        '''Simple parameter'''

        test = 'String'
        parsed = parse(test, ParameterType)
        self.assertEqual(parsed.name, test, 'Not matched.')

    def test_case_pt2(self):
        '''Array'''

        test = 'int[]'
        parsed = parse(test, ParameterType)
        self.assertEqual(parsed.name, 'int', 'Not matched.')
        self.assertEqual(parsed.arraySuffix, '[]', 'Should be an array.')

    def test_case_pt3(self):
        '''Generic'''

        test = 'List<String>'
        parsed = parse(test, ParameterType)
        self.assertEqual(parsed.name, 'List', 'Not matched.')
        self.assertEqual([x.name for x in parsed.generic], ['String'],
                         'Generic should be `[String]`.')

    def test_case_pt4(self):
        '''Complicated case'''

        test = 'ArrayList<LinkedHashMap<String[], Object>>'
        parsed = parse(test, ParameterType)
        self.assertEqual(parsed.name, 'ArrayList', 'Not matched.')
        self.assertEqual([x.name for x in parsed.generic], ['LinkedHashMap'],
                         'Generic should be `[LinkedHashMap]`.')
        self.assertEqual([x.name for x in parsed.generic[0].generic],
                         ['String', 'Object'], 'Generic should be `[String, Object]`.')
        self.assertEqual(parsed.generic[0].generic[0].arraySuffix, '[]',
                         'Should be an array.')

    def test_case_pt5(self):
        '''Another complicated case'''

        test = 'LinkedHashMap<String[], Object>[]'
        parsed = parse(test, ParameterType)
        self.assertEqual(parsed.name, 'LinkedHashMap', 'Not matched.')
        self.assertEqual(parsed.arraySuffix, '[]', 'Should be an array.')
        self.assertEqual([x.name for x in parsed.generic], ['String', 'Object'],
                         'Should be `[String, Object]`.')
        self.assertEqual(parsed.generic[0].arraySuffix,
                         '[]', 'Should be an array.')

    def test_case_pt6(self):
        '''More dimensions of arrays'''

        test = 'String[][][]'
        parsed = parse(test, ParameterType)
        self.assertEqual(parsed.arraySuffix, '[][][]', 'Not matched.')

    def test_case_pt7(self):
        '''Recurision case, till 3 of the depth, enough for most case.'''

        test = 'ArrayList<LinkedHashMap<String[], HashMap<String, T<Object>>>>'
        parsed = parse(test, ParameterType)
        self.assertEqual(parsed.name, 'ArrayList', 'Not matched.')
        self.assertEqual([x.name for x in parsed.generic], ['LinkedHashMap'],
                         'Generic should be `[LinkedHashMap]`.')
        self.assertEqual([x.name for x in parsed.generic[0].generic], ['String', 'HashMap'],
                         'Generic should be `[String, HashMap]`.')
        self.assertEqual(parsed.generic[0].generic[0].arraySuffix, '[]',
                         'Should be an array.')
        self.assertEqual([x.name for x in parsed.generic[0].generic[1].generic], ['String', 'T'],
                         'Generic should be `[String, T]`.')
        self.assertEqual([x.name for x in parsed.generic[0].generic[1].generic[1].generic], ['Object'],
                         'Generic should be `[Object]`.')

    def test_case_pt8(self):
        '''Test stringify'''

        test = 'LinkedHashMap<String[], Object>[]'
        expected = {
            'name': 'LinkedHashMap',
            'generic': [
                {'name': 'String', 'generic': None, 'arraySuffix': '[]'},
                {'name': 'Object', 'generic': None, 'arraySuffix': None}
            ],
            'arraySuffix': '[]'
        }
        parsed = parse(test, ParameterType)
        self.assertEqual(str(parsed), json.dumps(expected), 'Not matched.')


class TestParameters(unittest.TestCase):

    def test_case_p1(self):
        '''Parameter only'''

        test = 'String name'
        expected = {
            'name': 'name',
            'type': {'name': 'String', 'generic': None, 'arraySuffix': None}
        }
        parsed = parse(test, Parameter)
        self.assertEqual(str(parsed), json.dumps(expected), 'Not matched.')

    def test_case_ps1(self):
        '''Simple case'''

        test = 'String name, int age, Info info, String[] other'
        expected = [{
            "name": "name",
            "type": {"name": "String", "generic": None, "arraySuffix": None}
        }, {
            "name": "age",
            "type": {"name": "int", "generic": None, "arraySuffix": None}
        }, {
            "name": "info",
            "type": {"name": "Info", "generic": None, "arraySuffix": None}
        }, {
            "name": "other",
            "type": {"name": "String", "generic": None, "arraySuffix": "[]"}
        }]
        parsed = parse(test, Parameters)
        self.assertEqual(str(parsed), json.dumps(expected), 'Not matched.')


if __name__ == '__main__':
    pass
