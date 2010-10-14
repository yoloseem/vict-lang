""":mod:`vict.tree` --- Abstract syntax tree
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""

class Expression(object):

    @classmethod
    def parse(cls, result):
        return cls(result[0])


class Literal(Expression):

    pass

class Integer(Literal):

    __slots__ = "value",

    def __init__(self, value):
        self.value = int(value)

    def __repr__(self):
        return "Integer({0!r})".format(self.value)

class Float(Literal):

    __slots__ = "value",

    def __init__(self, value):
        self.value = float(value)

    def __repr__(self):
        return "Float({0!r})".format(self.value)

class String(Literal, unicode):

    def __repr__(self):
        return "String({0})".format(unicode.__repr__(self))


class Boolean(Literal):

    __slots__ = "value",

    @staticmethod
    def parse(result):
        return Boolean(result[0] == 'True')

    def __init__(self, value):
        self.value = bool(value)

    def __repr__(self):
        return "Boolean({0!r})".format(self.value)


class None_(Literal):

    @staticmethod
    def parse(result):
        return None_()

    def __init__(self):
        pass

    def __repr__(self):
        return "None_()"

class Array(Expression, tuple):

    @staticmethod
    def parse(result):
        return Array(x for x in result if isinstance(x, Expression))

    def __repr__(self):
        if not self:
            return "Array()"
        endpos = -2 if len(self) == 1 else -1
        return "Array([{0}])".format(tuple.__repr__(self)[1:endpos])

class Dictionary(Expression, dict):

    @staticmethod
    def parse(result):
        a = dict()
        for i, x in enumerate(result):
            if x == u'::':
                a.__setitem__(result[i-1], result[i+1])
        return Dictionary(a)

    def __repr__(self):
        if not self:
            return "Dictionary()"
        keys = [(repr(x), x) for x in self.keys()]
        keys.sort()
        repr_dict = [(x+": "+repr(self[y])) for x, y in keys]
        repr_dict = "{"+str.join(", ", repr_dict)+"}"
        return "Dictionary({0})".format(repr_dict)

class Identifier(Expression):

    __slots__ = "identifier",

    def __init__(self, identifier):
        self.identifier = identifier

    def __repr__(self):
        return "Identifier({0})".format(unicode.__repr__(self.identifier))
