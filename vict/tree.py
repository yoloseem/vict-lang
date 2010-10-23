""":mod:`vict.tree` --- Abstract syntax tree
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""

class Expression(object):

    @classmethod
    def parse(cls, result):
        return cls(result[0])

class Line(object):

    pass

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

class Pass_(Expression):

    @staticmethod
    def parse(result):
        return Pass_()

    def __init__(self):
        pass

    def __repr__(self):
        return "Pass_()"

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

class MethodArgument(Array):
   
    @staticmethod
    def parse(result):
        return MethodArgument(x for x in result if isinstance(x, Expression))
    
    def __repr__(self):
        if not self:
            return "MethodArgument()"
        endpos = -2 if len(self) == 1 else -1
        return "MethodArgument([{0}])".format(tuple.__repr__(self)[1:endpos])

class Method(Expression):

    __slots__ = "arguments", "program"

    def __init__(self, args, exprs):
        self.arguments = args
        self.program = exprs

    @staticmethod
    def parse(result):
        return Method(result[1], result[3])

    def __repr__(self):
        return "Method({0!r}, {1!r})".format(self.arguments, self.program)

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
        args = CallArgument(result[1]+result[6])
        return Call(result[4], args)

    def __init__(self, method, args):
        self.method = method
        self.arguments = args

    def __repr__(self):
        return "Call({0!r}, {1!r})".format(self.method, self.arguments)
