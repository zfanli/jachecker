import unittest
from pypeg2 import *
from parser.java_parser.java_parser import *
from parser.java_parser.tokens import *


class TestJavaParser(unittest.TestCase):

    def test_imported(self):
        imported_test = 'import java.util.Arrays;'
        parsed = parse(imported_test, Imported)
        print(parsed)
        self.assertEqual(str(parsed), imported_test, 'Import is not ok.')


if __name__ == '__main__':
    pass
