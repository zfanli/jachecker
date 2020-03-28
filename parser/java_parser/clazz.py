'''
Deal with class.
'''

from pypeg2 import *

from parser.java_parser.tokens import Modifier, CommonName
from parser.java_parser.mixins import Stringify
from parser.java_parser.import_package import Package, Import
from parser.java_parser.annotation import Annotation
from parser.java_parser.field import Field
from parser.java_parser.method import Method


class Clazz(List, Stringify):

    grammar = (
        attr('package', Package),
        attr('imports', maybe_some(Import)),
        attr('annotations', maybe_some(Annotation)),
        attr('modifiers', maybe_some(Modifier)),
        'class',
        attr('name', CommonName),
        '{',
        maybe_some([Field, Method]),
        '}',
    )

    def object(self):
        return {
            'name': self.name.object(),
            'package': self.package.object(),
            'imports': [x.object() for x in self.imports],
            'annotations': [x.object() for x in self.annotations],
            'modifiers': [x.object() for x in self.modifiers],
            'fields': [x.object() for x in filter(lambda item: item.type != 'METHOD', self.modifiers)],
            'methods': [x.object() for x in filter(lambda item: item.type == 'METHOD', self.modifiers)],
        }
