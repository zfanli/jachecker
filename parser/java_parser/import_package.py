'''
Deal with import and package keywords in Java.
'''

from pypeg2 import *
from pypeg2 import blank

from parser.java_parser.tokens import CommonName
from parser.java_parser.mixins import Stringify

# name allows start (*)
name_star = re.compile(r'\*|[\w\d]+')


class PathNameMixin:
    '''
    Get full name like `com.example.name`.
    Need `self.path` and `self.name`.
    '''

    def get_full_name(self):
        return f"{'.'.join(self.path)}.{self.name}"


class StringifyAdopter(Stringify):
    '''Json output'''

    def object(self):
        '''Make object for json output'''

        return {
            'name': self.name,
            'type': self.keyword.upper(),
            'path': self.path.object(),
            'lineno': self.position_in_text[0]
        }


class Pathnames(List, Stringify):
    '''Path name'''

    grammar = some(word, '.')

    def object(self):
        return '.'.join(self)


def create_grammar(target_keyword, name_pattern):
    '''
    Create grammar with given keyword.
    Example: `keyword com.example.name;`
    '''

    return (
        target_keyword, blank, attr('path', Pathnames),
        attr('name', name_pattern), ';'
    )


class Import(str, PathNameMixin, StringifyAdopter):
    '''Java import

    Output: `json`
        {
            "name": str,
            "type": "IMPORT",
            "path": str,
            "lineno": number,
        }
    '''

    keyword = 'import'
    grammar = create_grammar(keyword, name_star)


class Imports(List):
    '''Import may always be a list.

    Output: `json`
        [Import]
    '''

    grammar = some(Import)


class Package(str, PathNameMixin, StringifyAdopter):
    '''Java package

    Output: `json`
        {
            "name": str,
            "type": "PACKAGE",
            "path": str,
            "lineno": number,
        }
    '''

    keyword = 'package'
    grammar = create_grammar(keyword, CommonName)


if __name__ == '__main__':
    pass
