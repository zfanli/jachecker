import re
from pypeg2 import *
from pypeg2 import blank
from parser.java_parser.tokens import *


class Imported(List):

    grammar = 'import', blank, some(word, '.'), name(), ';'

    def __str__(self):
        return 'import ' + '.'.join(self) + '.' + self.name + ';'


if __name__ == '__main__':
    pass
