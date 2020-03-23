'''
Unit Test.

Target: import
'''

import unittest
import json

from pypeg2 import *
from pypeg2 import endl

# Test target
from parser.java_parser.import_package import Import, Imports


class TestImport(unittest.TestCase):

    def test_case1(self):
        '''Normal import'''

        test = 'import java.util.Arrays;'
        parsed = parse(test, Import)
        self.assertEqual(compose(parsed), test,
                         'Normal case is not ok.')

    def test_case2(self):
        '''Some leading whitespaces in import'''

        test = '       import java.util.Arrays;'
        parsed = parse(test, Import)
        self.assertEqual(compose(parsed), test.strip(),
                         'Leading whitespaces is not ok.')

    def test_case3(self):
        '''Linebreaking in import'''

        test = '\nimport \n\n\n\n java.util.Arrays;'
        parsed = parse(test, Import)
        self.assertEqual(compose(parsed), 'import java.util.Arrays;',
                         'Linebreaking is not ok.')

    def test_case4(self):
        '''Multi import'''

        import_list = [
            'import org.springframework.boot.CommandLineRunner;',
            'import org.springframework.boot.SpringApplication;',
            'import org.springframework.boot.autoconfigure.SpringBootApplication;',
            'import org.springframework.context.ApplicationContext;',
            'import org.springframework.context.annotation.Bean;'
        ]
        test = f'''
            {import_list[0]}
            {import_list[1]}
            {import_list[2]}
            {import_list[3]}
            {import_list[4]}
        '''
        parsed = parse(test, Imports)
        self.assertEqual(
            import_list,
            [compose(x)for x in parsed],
            'Multiple import is not ok.'
        )

    def test_case5(self):
        '''Import all'''

        test = 'import java.util.*;'
        parsed = parse(test, Import)
        self.assertEqual(parsed.name, '*', 'Import all is not ok.')

    def test_compose(self):
        '''Check compose'''

        test = 'import org.springframework.context.annotation.Bean;'
        parsed = parse(test, Import)
        composed = compose(parsed)
        self.assertEqual(composed, test, 'Compose is not ok.')

    def test_json(self):
        '''To json'''

        test = 'import org.springframework.context.annotation.Bean;'
        expected = {
            'name': 'Bean',
            'type': 'import'.upper(),
            'path': ['org', 'springframework', 'context', 'annotation'],
            'lineno': 1
        }
        parsed = parse(test, Import)
        self.assertEqual(json.dumps(parsed.object()),
                         json.dumps(expected), 'To json not works.')

    def test_full_name(self):
        '''Get full name'''

        expected = 'org.springframework.context.annotation.Bean'
        test = f'import {expected};'
        parsed = parse(test, Import)
        self.assertEqual(parsed.get_full_name(), expected,
                         '`get_full_name` not works.')


if __name__ == '__main__':
    pass
