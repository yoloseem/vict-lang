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

    def bf_add(*args):
        ret = list(args)[0]
        for x in list(args)[1:]:
            ret = ret + x
        return ret
    env.set_(u'+', vict.tree.Function(bf_add))
    
    def bf_sub(*args):
        ret = list(args)[0]
        for x in list(args)[1:]:
            ret = ret - x
        return ret
    env.set_(u'-', vict.tree.Function(bf_sub))
    
    def bf_mul(*args):
        ret = list(args)[0]
        for x in list(args)[1:]:
            ret = ret * x
        return ret
    env.set_(u'*', vict.tree.Function(bf_mul))
    
    def bf_div(*args):
        ret = list(args)[0]
        for x in list(args)[1:]:
            ret = ret / x
        return ret
    env.set_(u'/', vict.tree.Function(bf_div))
    
    env.set_(u'<', vict.tree.Function(lambda x, y: x<y))
    env.set_(u'<=', vict.tree.Function(lambda x, y: x<=y))
    env.set_(u'>', vict.tree.Function(lambda x, y: x>y))
    env.set_(u'>=', vict.tree.Function(lambda x, y: x>=y))
    env.set_(u'=', vict.tree.Function(lambda x, y: x==y))
    env.set_(u'!=', vict.tree.Function(lambda x, y: x!=y))

    def bf_str(x):
        try:
            return vict.tree.String(x.__vict__())
        except AttributeError:
            return vict.tree.String(unicode(x))
    env.set_(u'str', vict.tree.Function(bf_str))

    def bf_print(*args):
        for x in list(args):
            print x.__vict__()
    env.set_(u'print', vict.tree.Function(bf_print))

    return env
