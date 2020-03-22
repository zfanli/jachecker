'''
Unit Test.

Target: import
'''

import unittest
import json

from pypeg2 import *

# Test target
from parser.java_parser.method import Method

test = '''
	public static void main(String[] args) {
		SpringApplication.run(Application.class, args);
	}
'''


class TestMethod(unittest.TestCase):

    def test_case1(self):
        pass
        # parsed = parse(test, Method)
        # print(json.dumps(parsed.__dict__))
        # print(parsed)

        # assert False


if __name__ == '__main__':
    pass
