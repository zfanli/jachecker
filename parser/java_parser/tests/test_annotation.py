'''
Unit Test.

Target: annotation
'''

import unittest
import json

from pypeg2 import *

# Test target
from parser.java_parser.annotation import *


class TestAnnotationParameters(unittest.TestCase):

    def test_case_ap1(self):
        '''Annotation parameters.
        Pattern: Variable (parameter)
        '''

        expected = [{'key': 'value', 'value': ['Parameter']}]
        test = expected[0]['value'][0]
        parsed = parse(test, AnnotationParameters)
        self.assertEqual(parsed.object(), expected, 'Not matched.')

    def test_case_ap2(self):
        '''Annotation parameters.
        Pattern: Variable list (parameter, another)
        '''

        expected = [{'key': 'value',
                     'value': ['Parameter', 'AnotherParameter']}]
        test = ', '.join(expected[0]['value'])
        parsed = parse(test, AnnotationParameters)
        self.assertEqual(parsed.object(), expected, 'Not matched.')

    def test_case_ap3(self):
        '''Annotation parameters.
        Pattern: Variable with attribute (parameter.value)
        '''

        expected = [{'key': 'value', 'value': ['Parameter.attribute']}]
        test = expected[0]['value'][0]
        parsed = parse(test, AnnotationParameters)
        self.assertEqual(parsed.object(), expected, 'Not matched.')

    def test_case_ap4(self):
        '''Annotation parameters.
        Pattern: Variable with attribute list (parameter.value, parameter.another)
        '''

        expected = [{'key': 'value',
                     'value': ['Parameter.attribute', 'AnotherParameter.thatAttribute']}]
        test = ', '.join(expected[0]['value'])
        parsed = parse(test, AnnotationParameters)
        self.assertEqual(parsed.object(), expected, 'Not matched.')

    def test_case_ap5(self):
        '''Annotation parameters.
        Pattern: Key value pair (key=value)
        '''

        expected = {'key': 'KeyName', 'value': ['Value']}
        test = f'{expected["key"]}={expected["value"][0]}'
        parsed = parse(test, AnnotationParameters)
        self.assertEqual(parsed.object(), [expected], 'Not matched.')

    def test_case_ap6(self):
        '''Annotation parameters.
        Pattern: Key value pair list (key=value, anotherKey=anotherValue)
        '''

        expected = [
            {'key': 'KeyName', 'value': ['Value']},
            {'key': 'AnotherKeyName', 'value': ['AnotherValue']},
        ]
        test = ', '.join([f'{x["key"]}={x["value"][0]}' for x in expected])
        parsed = parse(test, AnnotationParameters)
        self.assertEqual(parsed.object(), expected, 'Not matched.')

    def test_case_ap7(self):
        '''Annotation parameters.
        Pattern: Key list value pair (key={value, another})
        '''

        expected = [{'key': 'KeyName', 'value': ['Value', 'AnotherValue']}]
        test = ', '.join(
            [f'{x["key"]}={"{"}{", ".join(x["value"])}{"}"}' for x in expected])
        parsed = parse(test, AnnotationParameters)
        self.assertEqual(parsed.object(), expected, 'Not matched.')

    def test_case_ap8(self):
        '''Annotation parameters.
        Pattern: Literals ("string", 123, true, 1.2)
        '''

        expected = [{'key': 'value', 'value': ['String Literal', 'Another']}]
        temp = ["\"" + x + "\"" for x in expected[0]["value"]]
        test = f'{", ".join(temp)}'
        parsed = parse(test, AnnotationParameters)
        self.assertEqual(parsed.object(), expected, 'Not matched.')

    def test_case_ap9(self):
        '''Annotation parameters.
        Pattern: Literals ("string", 123, true, 1.2)
        '''

        expected = [{'key': 'value', 'value': [123, 1.2]}]
        test = f'{", ".join([str(x) for x in expected[0]["value"]])}'
        parsed = parse(test, AnnotationParameters)
        self.assertEqual(parsed.object(), expected, 'Not matched.')

    def test_case_ap10(self):
        '''Annotation parameters.
        Pattern: Literals ("string", 123, true, 1.2)
        '''

        expected = [{'key': 'value', 'value': [True, False]}]
        test = f'{", ".join(["true" if x else "false" for x in expected[0]["value"]])}'
        parsed = parse(test, AnnotationParameters)
        self.assertEqual(parsed.object(), expected, 'Not matched.')


class TestAnnotation(unittest.TestCase):

    def test_case_an1(self):
        '''Annotation'''

        expected = {'name': 'Annotation', 'parameters': None, 'lineno': 1}
        test = f'@{expected["name"]}'
        parsed = parse(test, Annotation)
        self.assertEqual(str(parsed), json.dumps(expected),
                         'Not parsed correctly.')

    def test_case_an2(self):
        '''Annotation'''

        expected = {'name': 'Annotation',
                    'parameters': [{'key': 'value', 'value': ['SomeValues']}],
                    'lineno': 1}
        test = '@Annotation("SomeValues")'
        parsed = parse(test, Annotation)
        self.assertEqual(str(parsed), json.dumps(expected),
                         'Not parsed correctly.')

    def test_case_an3(self):
        '''Annotation'''

        expected = {'name': 'Annotation',
                    'parameters': [{'key': 'value', 'value': ['SomeValues', 'Another']}],
                    'lineno': 1}
        test = '@Annotation("SomeValues", "Another")'
        parsed = parse(test, Annotation)
        self.assertEqual(str(parsed), json.dumps(expected),
                         'Not parsed correctly.')

    def test_case_an4(self):
        '''Annotation'''

        expected = {'name': 'Annotation',
                    'parameters': [{'key': 'value', 'value': ['SomeValues', 'Another']}],
                    'lineno': 1}
        test = '@Annotation(value={"SomeValues", "Another"})'
        parsed = parse(test, Annotation)
        self.assertEqual(str(parsed), json.dumps(expected),
                         'Not parsed correctly.')

    def test_case_an5(self):
        '''Annotation'''

        expected = {'name': 'Annotation',
                    'parameters': [{'key': 'value',
                                    'value': ['Parameter.attribute', 'Parameter.another']}],
                    'lineno': 1}
        test = '@Annotation(Parameter.attribute, Parameter.another)'
        parsed = parse(test, Annotation)
        self.assertEqual(str(parsed), json.dumps(expected),
                         'Not parsed correctly.')

    def test_case_an6(self):
        '''Annotation'''

        expected = {'name': 'Annotation',
                    'parameters': [
                        {'key': 'Key', 'value': ['Parameter.attribute']},
                        {'key': 'Other', 'value': ['Parameter.another']}
                    ],
                    'lineno': 1}
        test = '@Annotation(Key=Parameter.attribute, Other=Parameter.another)'
        parsed = parse(test, Annotation)
        self.assertEqual(str(parsed), json.dumps(expected),
                         'Not parsed correctly.')

    def test_case_an6(self):
        '''Annotation'''

        expected = {'name': 'Annotation',
                    'parameters': [
                        {'key': 'Key', 'value': ['val1', 'val2']},
                        {'key': 'Other', 'value': ['Parameter.another']}
                    ],
                    'lineno': 1}
        test = '@Annotation(Key={"val1", "val2"}, Other=Parameter.another)'
        parsed = parse(test, Annotation)
        self.assertEqual(str(parsed), json.dumps(expected),
                         'Not parsed correctly.')

    def test_case_an7(self):
        '''Annotation'''

        expected = {
            'name': 'Annotation',
            'parameters': [
                {'key': 'value', 'value': ['/PATH']},
            ],
            'lineno': 1
        }
        test = '@Annotation("/PATH")'
        parsed = parse(test, Annotation)
        print(parsed)
        self.assertEqual(str(parsed), json.dumps(expected),
                         'Not parsed correctly.')


class TestAnnotations(unittest.TestCase):

    def test_case_ans1(self):
        '''Annotation list'''

        expected = [
            # @Test
            {'name': 'Test', 'parameters': None, 'lineno': 2},
        ]
        test = '''
        @Test
        '''
        parsed = parse(test, Annotations)
        self.assertEqual(parsed.object(), expected, 'Not matched.')

    def test_case_ans2(self):
        '''Annotation list'''

        expected = [
            # @Test
            {'name': 'Test', 'parameters': None, 'lineno': 2},
            # @Annotation(Value)
            {'name': 'Annotation', 'parameters': [
                {'key': 'value', 'value': ['Value']}
            ], 'lineno': 3},
            # @MultiValues(value={Value1, value2})
            {'name': 'MultiValues', 'parameters': [
                {'key': 'value', 'value': ['Value1', 'value2']}
            ], 'lineno': 4},
            # @ListValues(Value1, Value2)
            {'name': 'ListValues', 'parameters': [
                {'key': 'value', 'value': ['Value1', 'Value2']}
            ], 'lineno': 5},
        ]
        test = '''
        @Test
        @Annotation(Value)
        @MultiValues(value={Value1, value2})
        @ListValues(Value1, Value2)
        '''
        parsed = parse(test, Annotations)
        self.assertEqual(parsed.object(), expected, 'Not matched.')

    def test_case_ans3(self):
        '''Annotation list'''

        expected = [
            # @Literal1("string")
            {'name': 'Literal1', 'parameters': [
                {'key': 'value', 'value': ['string']}],
                'lineno': 2},
            # @Literal2("string", "another")
            {'name': 'Literal2', 'parameters': [
                {'key': 'value', 'value': ['string', 'another']}],
                'lineno': 3},
            # @Literal3(123)
            {'name': 'Literal3', 'parameters': [
                {'key': 'value', 'value': [123]}],
                'lineno': 4},
            # @Literal4(123, 456)
            {'name': 'Literal4', 'parameters': [
                {'key': 'value', 'value': [123, 456]}],
                'lineno': 5},
            # @Literal5(1.1)
            {'name': 'Literal5', 'parameters': [
                {'key': 'value', 'value': [1.1]}],
                'lineno': 6},
            # @Literal6(1.1, 9.9)
            {'name': 'Literal6', 'parameters': [
                {'key': 'value', 'value': [1.1, 9.9]}],
                'lineno': 7},
            # @Literal7(true)
            {'name': 'Literal7', 'parameters': [
                {'key': 'value', 'value': [True]}],
                'lineno': 8},
            # @Literal8(false, true)
            {'name': 'Literal8', 'parameters': [
                {'key': 'value', 'value': [False, True]}],
                'lineno': 9},
        ]
        test = '''
        @Literal1("string")
        @Literal2("string", "another")
        @Literal3(123)
        @Literal4(123, 456)
        @Literal5(1.1)
        @Literal6(1.1, 9.9)
        @Literal7(true)
        @Literal8(false, true)
        '''
        parsed = parse(test, Annotations)
        self.assertEqual(parsed.object(), expected, 'Not matched.')

    def test_case_ans4(self):
        '''Annotation list'''

        expected = [
            # @KeyValue(key=value)
            {'name': 'KeyValue', 'parameters': [
                {'key': 'key', 'value': ['value']}],
                'lineno': 2},
            # @MoreKeyValue(key=value, key2=value2)
            {'name': 'MoreKeyValue', 'parameters': [
                {'key': 'key', 'value': ['value']},
                {'key': 'key2', 'value': ['value2']},
            ], 'lineno': 3},
        ]
        test = '''
        @KeyValue(key=value)
        @MoreKeyValue(key=value, key2=value2)
        '''
        parsed = parse(test, Annotations)
        self.assertEqual(parsed.object(), expected, 'Not matched.')
