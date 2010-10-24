""":mod:`vict.env` --- Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""

import vict.parse
from vict.tree import *

class Environment(object):

    __slots__ = "env", "parent",

    def __init__(self, parent=None):
        self.env = dict()
        self.parent = parent

    def get(self, key):
        if self.env.has_key(key):
            return self.env[key]
        else:
            if self.parent is not None:
                return self.parent.get(key)
            raise NameError('Nondeclared {0!r}'.format(key))

    def set_(self, key, value):
        self.env.__setitem__(key, value)

def built_in_env():
    
    env = Environment()

    env.set_(u'+', vict.tree.Function(lambda x, y: x+y))
    env.set_(u'-', vict.tree.Function(lambda x, y: x-y))
    env.set_(u'*', vict.tree.Function(lambda x, y: x*y)) 
    env.set_(u'/', vict.tree.Function(lambda x, y: x/y))

    def printfunc(*lst):
        for x in list(lst):
            print x.__vict__()
    env.set_(u'print', vict.tree.Function(printfunc))

    return env
