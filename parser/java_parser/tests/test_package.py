'''
Unit Test.

Target: package
'''

import unittest
import json

from pypeg2 import *

# Test target
from parser.java_parser.import_package import Package


class TestPackage(unittest.TestCase):

    def test_case1(self):
        '''Normal Package'''

        test = 'package java.util.Arrays;'
        parsed = parse(test, Package)
        self.assertEqual(compose(parsed), test, 'Normal case is not ok.')

    def test_case2(self):
        '''Some leading whitespaces in import'''

        test = '       package java.util.Arrays;'
        parsed = parse(test, Package)
        self.assertEqual(compose(parsed), test.strip(),
                         'Leading whitespaces is not ok.')

    def test_case3(self):
        '''Linebreaking'''

        test = '\npackage \n\n\n\n java.util.Arrays;'
        parsed = parse(test, Package)
        self.assertEqual(compose(parsed), 'package java.util.Arrays;',
                         'Linebreaking is not ok.')

    def test_compose(self):
        '''Check compose'''

        test = 'package org.springframework.context.annotation.Bean;'
        parsed = parse(test, Package)
        composed = compose(parsed)
        self.assertEqual(composed, test, 'Compose is not ok.')

    def test_json(self):
        '''To json'''

        test = 'package org.springframework.context.annotation.Bean;'
        expected = {
            'name': 'Bean',
            'type': 'package',
            'path': ['org', 'springframework', 'context', 'annotation'],
            'lineno': 1
        }
        parsed = parse(test, Package)
        self.assertEqual(json.dumps(parsed.object()),
                         json.dumps(expected), 'To json not works.')

    def test_full_name(self):
        '''Get full name'''

        expected = 'org.springframework.context.annotation.Bean'
        test = f'package {expected};'
        parsed = parse(test, Package)
        self.assertEqual(parsed.get_full_name(), expected,
                         '`get_full_name` not works.')


if __name__ == '__main__':
    pass
