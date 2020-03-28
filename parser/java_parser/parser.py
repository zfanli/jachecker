'''
Java parser entry.
'''

import re

from pypeg2 import parse, comment_cpp, comment_c, comment_pas

from parser.java_parser.clazz import Clazz
from parser.java_parser.comment import comment_doc, comment_line


class JavaParser:

    target = ''

    def __init__(self, target):
        self.target = target

    def escape(self):
        '''Do some escape before parse'''

        self.target = self.target.replace('\\"', 'JC_ESCAPED_QUOTE')

    def parse(self):
        '''Parse target'''

        self.escape()
        result = parse(self.target, Clazz, comment=[comment_doc, comment_line])

        return result.object()
