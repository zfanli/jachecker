import unittest
from pypeg2 import *
from parser.java_parser.java_parser import *
from parser.java_parser.tokens import *


class TestJavaParser(unittest.TestCase):

    def test_lineno(self):
        imported_test = '[999] import java.util.Arrays;'
        parsed = parse(imported_test, Imported)
        self.assertEqual(parsed.lineno, 999, 'Lineno is not ok.')

    def test_imported(self):
        imported_test = 'import java.util.Arrays;'
        parsed = parse('[0] ' + imported_test, Imported)
        self.assertEqual(str(parsed), imported_test, 'Import is not ok.')
        imported_test = '       import java.util.Arrays;'
        parsed = parse('[0] ' + imported_test, Imported)
        self.assertEqual(str(parsed), imported_test.strip(),
                         'Import is not ok with leading blank.')
        imported_test = 'import\n\n\n\n java.util.Arrays;'
        parsed = parse('[0] ' + imported_test, Imported)
        self.assertEqual(str(parsed), imported_test.strip().replace('\n', ''),
                         'Import is not ok with leading blank.')


if __name__ == '__main__':
    pass
