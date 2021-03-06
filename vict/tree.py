""":mod:`vict.tree` --- Abstract syntax tree
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""

import vict.parse

class Expression(object):

    @classmethod
    def parse(cls, result):
        return cls(result[0])

class WrappedExpression(Expression):

    @staticmethod
    def parse(result):
        return result[1]

class Line(object):

    @staticmethod
    def parse(result):
        return result[0]

class If(object):

    __slots__ = "cond", "ifp", "elsep",

    @staticmethod
    def parse(result):
        if len(result) == 7:
            for i, x in enumerate(result[4].lines):
                if type(x) is Identifier:
                    if x.identifier == u"else":
                        return If(result[2], Program(result[4].lines[:i]), Program(result[4].lines[i+1:]))
            return If(result[2], result[4])
        elif len(result) == 9:
            return If(result[2], result[4], result[6])
    
    def __init__(self, cond, ifp, elsep=None):
        self.cond = cond
        self.ifp = ifp
        self.elsep = elsep

    def __repr__(self):
        if self.elsep:
            return "If({0!r}, {1!r}, {2!r})".format(self.cond, self.ifp, self.elsep)
        else:
            return "If({0!r}, {1!r})".format(self.cond, self.ifp)

class Set(Line):

    __slots__ = "left", "right",

    @staticmethod
    def parse(result):
        return Set(result[0], result[2])

    def __init__(self, left_operand, right_operand):
        self.left = left_operand
        self.right = right_operand
    
    def __repr__(self):
        return "Set({0!r}, {1!r})".format(self.left, self.right)

class Program(object):

    __slots__ = "lines",

    @staticmethod
    def parse(result):
        return Program(result)

    def __init__(self, lines):
        self.lines = lines

    def __repr__(self):
        return "Program({0!r})".format(self.lines)

class Literal(Expression):

    pass

class Integer(Literal):

    __slots__ = "value",

    def __init__(self, value):
        self.value = int(value)

    def __repr__(self):
        return "Integer({0!r})".format(self.value)

    def __vict__(self):
        return str(self.value)

    def __add__(self, other):
        return Integer(self.value + other.value)

    def __sub__(self, other):
    	return Integer(self.value - other.value)

    def __mul__(self, other):
        return Integer(self.value * other.value)

    def __div__(self, other):
        return Integer(self.value / other.value)

    def __eq__(self, other):
        return Boolean(self.value == other.value)

    def __ne__(self, other):
        return Boolean(self.value != other.value)

    def __lt__(self, other):
        return Boolean(self.value < other.value)

    def __le__(self, other):
        return Boolean(self.value <= other.value)

    def __gt__(self, other):
        return Boolean(self.value > other.value)

    def __ge__(self, other):
        return Boolean(self.value >= other.value)

class Float(Literal):

    __slots__ = "value",

    def __init__(self, value):
        self.value = float(value)

    def __repr__(self):
        return "Float({0!r})".format(self.value)

    def __vict__(self):
        return str(self.value)

    def __add__(self, other):
        return self.value + other.value

    def __sub__(self, other):
	return Integer(self.value - other.value)
    
    def __mul__(self, other):
        return Integer(self.value * other.value)

    def __div__(self, other):
        return Integer(self.value / other.value)

    def __eq__(self, other):
        return Boolean(self.value == other.value)

    def __ne__(self, other):
        return Boolean(self.value != other.value)

    def __lt__(self, other):
        return Boolean(self.value < other.value)

    def __le__(self, other):
        return Boolean(self.value <= other.value)

    def __gt__(self, other):
        return Boolean(self.value > other.value)

    def __ge__(self, other):
        return Boolean(self.value >= other.value)

class String(Literal, unicode):

    def __repr__(self):
        return "String({0})".format(unicode.__repr__(self))

    def __add__(self, other):
        return String(unicode(self) + unicode(other.__vict__()))

    def __mul__(self, other):
        if type(other) is Integer:
            return String(unicode(self) * other.value)
        elif type(other) is int:
            return String(unicode(self) * other)
        else:
            raise TypeError('* is only supported for String with Integer')

    def __vict__(self):
        return unicode(self)

class Boolean(Literal):

    __slots__ = "value",

    @staticmethod
    def parse(result):
        return Boolean(result[0] == 'True')

    def __init__(self, value):
        self.value = bool(value)

    def __repr__(self):
        return "Boolean({0!r})".format(self.value)

    def __vict__(self):
        return unicode(self.value)


class None_(Literal):

    @staticmethod
    def parse(result):
        return None_()

    def __init__(self):
        pass

    def __repr__(self):
        return "None_()"

    def __vict__(self):
        return unicode(None)

class Pass_(Expression):

    @staticmethod
    def parse(result):
        return Pass_()

    def __init__(self):
        pass

    def __repr__(self):
        return "Pass_()"

    def __vict__(self):
        return ""

class Array(Expression, tuple):

    @staticmethod
    def parse(result):
        return Array(x for x in result if isinstance(x, Expression))

    def __repr__(self):
        if not self:
            return "Array()"
        endpos = -2 if len(self) == 1 else -1
        return "Array([{0}])".format(tuple.__repr__(self)[1:endpos])

    def __add__(self, other):
        return Array(list(self) + list(other))

    def __vict__(self):
        return u'[' + u', '.join([x.__vict__() for x in self]) + u']'

class Dictionary(Expression, dict):

    @staticmethod
    def parse(result):
        a = dict()
        for i, x in enumerate(result):
            if type(x) is unicode:
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

class MethodArgument(Array):
   
    @staticmethod
    def parse(result):
        return MethodArgument(x for x in result if isinstance(x, Expression))
    
    def __repr__(self):
        if not self:
            return "MethodArgument()"
        endpos = -2 if len(self) == 1 else -1
        return "MethodArgument([{0}])".format(tuple.__repr__(self)[1:endpos])

class Binder(object):

    __slots__ = "place",    

    def __init__(self, thing):
        self.place = thing

class Method(Expression):

    __slots__ = "arguments", "program", "bind",

    def __init__(self, args, exprs):
        self.arguments = args
        self.program = exprs
        self.bind = Binder(self)

    @staticmethod
    def parse(result):
        return Method(result[1], result[3])

    def __repr__(self):
        return "Method({0!r}, {1!r})".format(self.arguments, self.program)

    def __vict__(self):
        return "<Function at {0}>".format(repr(self.bind).split("at ")[1][:-1])

class CallArgument(Array):
   
    @staticmethod
    def parse(result):
        return CallArgument(x for x in result if isinstance(x, Expression))
    
    def __repr__(self):
        if not self:
            return "CallArgument()"
        endpos = -2 if len(self) == 1 else -1
        return "CallArgument([{0}])".format(tuple.__repr__(self)[1:endpos])

class Call(Expression, Line):
    
    __slots__ = "method", "arguments"

    @staticmethod
    def parse(result):
        args = CallArgument(result[1]+result[5])
        return Call(result[3], args)

    def __init__(self, method, args):
        self.method = method
        self.arguments = args

    def __repr__(self):
        return "Call({0!r}, {1!r})".format(self.method, self.arguments)

class Function(object):

    __slots__ = "func",

    def __init__(self, func):
        self.func = func

    def __repr__(self):
        return "Function({0!r})".format(self.func)

    def __vict__(self):
        return "<Function at {0}>".format(repr(self.func).split('at ')[1][:-1])
