'''
Deal with annotations.
'''

from pypeg2 import *

from parser.java_parser.tokens import CommonName, CommonNameAttribute, PrimaryType
from parser.java_parser.mixins import Stringify, Literal


class AnnotationKeyValuePair(Stringify):
    '''Output: `json`
        {
            "key": str,
            "value": [str],
        }
    '''

    grammar = (attr('key', CommonName), '=',
               attr('value', [CommonNameAttribute, CommonName, PrimaryType]))

    def object(self):
        return {
            'key': self.key,
            'value': [self.value.object()]
        }


class AnnotationKeyListValuePair(Stringify):
    '''Output: `json`
        {
            "key": str,
            "value": [str],
        }
    '''

    grammar = (attr('key', CommonName), '=', '{',
               attr('value', csl([CommonName, PrimaryType]))), '}'

    def object(self):
        return {
            'key': self.key,
            'value': [x.object() for x in self.value]
        }


class AnnotationParameters(List, Stringify):
    '''Parameters of annotation, see details as shown below

    Output: `json`
        If key is specified:
        [{
            "key": str, 
            "value": [str],
        }]
        Or none of key is specified:
        [{
            "key": "value",
            "value": [str]
        }]
    '''

    grammar = csl([
        AnnotationKeyValuePair,
        AnnotationKeyListValuePair,
        PrimaryType,
        CommonNameAttribute,
        CommonName,
    ])

    def object(self):

        if type(self[0]) in (CommonNameAttribute, CommonName, PrimaryType):
            objected = [{
                'key': 'value',
                'value': [x.object() for x in self],
            }]
        else:
            objected = [x.object() for x in self]

        return objected


class Annotation(Stringify):
    '''Parameters of annotation maybe formatted as shown below.

        - @Annotation(variable[, another])
        - @Annotation(Object.attribute[, Object.another])
        - @Annotation(key=value[, anotherKey=anotherValue])
        - @Annotation(key={value[, another]})

    Output: `json`
        {
            "name": str,
            "parameters": ?[str],
        }
    '''

    grammar = ('@', attr('name', CommonName),
               attr('parameters', optional('(', AnnotationParameters, ')')))

    def object(self):
        return {
            'name': self.name.object(),
            'parameters': self.parameters.object() if self.parameters is not None else None,
            'lineno': self.position_in_text[0],
        }


class Annotations(List, Stringify):
    '''Annotation list.

    Output: `json`
    [Annotation]
    '''

    grammar = some(Annotation)

    def object(self):
        return [x.object() for x in self]
