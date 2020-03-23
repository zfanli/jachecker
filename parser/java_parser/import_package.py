'''
Deal with import and package keywords in Java.
'''

from pypeg2 import *
from pypeg2 import blank, endl

from parser.java_parser.tokens import CommonName

# name allows start (*)
name_star = re.compile(r'\*|[\w\d]+')


class PathNameMixin:
    '''
    Get full name like `com.example.name`.
    Need `self.path` and `self.name`.
    '''

    def get_full_name(self):
        return f"{'.'.join(self.path)}.{self.name}"


class JsonMixin:
    '''Json output'''

    def object(self):
        '''Make object for json output'''

        return {
            'name': self.name,
            'type': self.keyword.upper(),
            'path': self.path,
            'lineno': self.position_in_text[0]
        }


class Pathnames(List):
    '''Path name'''

    grammar = some(word, '.')


def create_grammar(target_keyword, name_pattern):
    '''
    Create grammar with given keyword.
    Example: `keyword com.example.name;`
    '''

    return (
        target_keyword, blank, attr('path', Pathnames),
        attr('name', name_pattern), ';'
    )


class Import(str, PathNameMixin, JsonMixin):
    '''Java import'''

    keyword = 'import'
    grammar = create_grammar(keyword, name_star)


class Imports(List):
    '''Import may always be a list'''

    grammar = some(Import)


class Package(str, PathNameMixin, JsonMixin):
    '''Java package'''

    keyword = 'package'
    grammar = create_grammar(keyword, CommonName)


if __name__ == '__main__':
    pass
