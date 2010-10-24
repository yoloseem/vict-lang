""":mod:`vict.env` --- Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""

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

    def set(self, key, value):
        self.env.__setitem__(key, value)

def built_in_env():
    
    env = Environment()

    return env
