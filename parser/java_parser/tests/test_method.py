'''
Unit Test.

Target: import
'''

import unittest
import json

from pypeg2 import *

# Test target
from parser.java_parser.method import Method
from parser.java_parser.comment import comment_doc, comment_line
from parser.java_parser.field import Field
from parser.java_parser.control_flow import ControlFlow
from parser.java_parser.operation import Operation
from parser.java_parser.variable import Parameter
from parser.java_parser.comment import Comment
from parser.java_parser.parser import JavaParser


test = '''
	public static void main(String[] args) {
		SpringApplication.run(Application.class, args);
	}
'''

with_comment = '''/**
     * Some comments.
     * 
     * @param param other things...
     */
    @Annotation("something here")
    public static void main(String[] args) {
		SpringApplication.run(Application.class, args);
	}
'''


class TestMethod(unittest.TestCase):

    def test_case1(self):

        parsed = parse(test, Method)
        print(parsed)
        # assert False

    def test_case2(self):

        parsed = parse(with_comment, [Field, Method], comment=[
                       comment_doc, comment_line])
        print(parsed)
        # assert False


if __name__ == '__main__':
    pass
