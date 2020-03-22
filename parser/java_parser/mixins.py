'''
Common Mixins.
'''

import json


class Stringify:

    def object(self):
        raise NotImplementedError()

    def __str__(self):
        return json.dumps(self.object())


class Literal(Stringify):

    def object(self):
        return self
