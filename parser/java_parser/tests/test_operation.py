'''
Unit Test.

Target: Operation
'''

import unittest
import json

from pypeg2 import *

# Test target
from parser.java_parser.operation import Operation, Operations, OperationAssignment, OperationReturn


class TestAssignment(unittest.TestCase):

    def test_case_ass1(self):
        '''Assignment'''

        expected = {
            'name': 'name',
            'type': {
                'name': 'String',
                'generic': None,
                'arraySuffix': None
            },
            'assignment': 'This is a string',
            'isNew': False,
            'lineno': 1
        }
        test = 'String name = "This is a string";'
        parsed = parse(test, OperationAssignment)
        print(parsed)
        self.assertEqual(parsed.object(), expected, 'Not matched.')

    def test_case_ass2(self):
        '''Assignment'''

        expected = {
            'name': 'name',
            'type': {
                'name': 'String',
                'generic': None,
                'arraySuffix': None
            },
            'assignment': 'AssignmentFromVariable',
            'isNew': False,
            'lineno': 1
        }
        test = 'String name = AssignmentFromVariable;'
        parsed = parse(test, OperationAssignment)
        print(parsed)
        self.assertEqual(parsed.object(), expected, 'Not matched.')

    def test_case_ass3(self):
        '''Assignment'''

        expected = {
            'name': 'name',
            'type': {
                'name': 'String',
                'generic': None,
                'arraySuffix': None
            },
            'assignment': 'SomeVariable.attribute',
            'isNew': False,
            'lineno': 1
        }
        test = 'String name = SomeVariable.attribute;'
        parsed = parse(test, OperationAssignment)
        print(parsed)
        self.assertEqual(parsed.object(), expected, 'Not matched.')

    def test_case_ass4(self):
        '''Assignment'''

        expected = {
            'name': 'name',
            'type': {
                'name': 'String',
                'generic': None,
                'arraySuffix': None
            },
            'assignment': {
                'name': 'someMethod',
                'parameters': [],
                'chain': None
            },
            'isNew': False,
            'lineno': 1
        }
        test = 'String name = someMethod();'
        parsed = parse(test, OperationAssignment)
        print(parsed)
        self.assertEqual(parsed.object(), expected, 'Not matched.')

    def test_case_ass5(self):
        '''Assignment'''

        expected = {
            'name': 'name',
            'type': None,
            'assignment': {
                'name': 'someMethod',
                'parameters': ['Parameters'],
                'chain': None
            },
            'isNew': False,
            'lineno': 1
        }
        test = 'name = someMethod(Parameters);'
        parsed = parse(test, OperationAssignment)
        print(parsed)
        self.assertEqual(parsed.object(), expected, 'Not matched.')

    def test_case_ass6(self):
        '''Operation'''

        expected = {
            'name': 'someStrangeClassABC',
            'type': {
                'name': 'SomeStrangeClassErrABC',
                'generic': None,
                'arraySuffix': None
            },
            'assignment': {
                'name': 'SomeStrangeClassErrABC',
                        'parameters': [],
                        'chain': None
            },
            'isNew': True,
            'lineno': 1
        }
        test = 'SomeStrangeClassErrABC someStrangeClassABC = new SomeStrangeClassErrABC();'
        parsed = parse(test, OperationAssignment)
        print(parsed)
        self.assertEqual(parsed.object(), expected, 'Not matched.')


class TestReturn(unittest.TestCase):

    def test_case_re1(self):

        expected = {
            'body': 'someThing',
            'type': 'RETURN',
        }
        test = 'return someThing;'
        parsed = parse(test, OperationReturn)
        print(parsed)
        self.assertEqual(parsed.object(), expected, 'Not matched.')


class TestOperation(unittest.TestCase):
    '''Just check the result'''

    def test_case_op1(self):
        '''Operation'''

        test = 'assertThat(response.getBody().equals("Greetings from Spring Boot!"));'
        parsed = parse(test, Operation)
        print(parsed)
        # assert False

    def test_case_op2(self):
        '''Operation'''

        test = 'assertThat(response.getBody()\n.equals("Greetings from Spring Boot!").equals("R"));'
        parsed = parse(test, Operation)
        print(parsed)
        # assert False

    def test_case_op3(self):
        '''Operation'''

        test = '''assertThat(
            response.getBody().equals("Greetings from Spring Boot!")
        );'''
        parsed = parse(test, Operation)
        print(parsed)
        # assert False


class TestOperations(unittest.TestCase):

    def test_case_os1(self):
        '''Operation list'''

        test = '''ResponseEntity<String> response = template.getForEntity(base.toString(),
                String.class);
        assertThat(response.getBody().equals("Greetings from Spring Boot!"));'''
        parsed = parse(test, Operations)
        print(parsed)
        # assert False


if __name__ == '__main__':
    pass
