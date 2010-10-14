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

    def __init__(self, value):
        self.value = int(value)

    def __repr__(self):
        return "Integer({0!r})".format(self.value)

class Float(Literal):

    pass

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

class Identifier(Expression):

    pass

