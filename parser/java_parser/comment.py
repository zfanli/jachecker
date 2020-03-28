'''
Deal with comments.
'''

import re
import json

from pypeg2 import *

from parser.java_parser.mixins import Stringify

comment_doc = re.compile(r'/\*.*?\*/', re.S)
comment_line = re.compile(r'^//.*')


class Comment(List, Stringify):

    grammar = '/*', maybe_some(re.compile(r'\*.*'))

    def object(self):
        return self
