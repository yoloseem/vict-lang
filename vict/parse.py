r""":mod:`vict.parse`
~~~~~~~~~~~~~~~~~~~~

Identifiers::

    >>> identifier.parse(u"xyz")
    [Identifier(u'xyz')]

Strings::

    >>> string.parse(u'"test"')
    [String(u'test')]
    >>> string.parse(ur'"\"hi\""')
    [String(u'"hi"')]

Booleans::

    >>> boolean.parse(u'True')
    [Boolean(True)]
    >>> boolean.parse(u'False')
    [Boolean(False)]

None::

    >>> none.parse(u"None")
    [None_()]

Integer::
    
    >>> integer.parse(u'1234')
    [Integer(1234)]

Float::

    >>> floating.parse(u'123.45')
    [Float(123.45)]

Array::

    >>> array.parse(u"[]")
    [Array()]
    >>> array.parse(u'["abc"]')
    [Array([String(u'abc')])]
    >>> array.parse(u'["abc",]')
    [Array([String(u'abc')])]
    >>> array.parse(u'["abc",1]')
    [Array([String(u'abc'), Integer(1)])]
    >>> array.parse(u'["abc",1,]')
    [Array([String(u'abc'), Integer(1)])]
    >>> array.parse(u'[1,2,3]')
    [Array([Integer(1), Integer(2), Integer(3)])]
    >>> array.parse(u'[1,2,3,]')
    [Array([Integer(1), Integer(2), Integer(3)])]
    >>> array.parse(u'[1,2,3,4]')
    [Array([Integer(1), Integer(2), Integer(3), Integer(4)])]
    >>> array.parse(u'[1,2,3,None]')
    [Array([Integer(1), Integer(2), Integer(3), None_()])]
    >>> array.parse(u'[1,[2,3],3]')
    [Array([Integer(1), Array([Integer(2), Integer(3)]), Integer(3)])]
    >>> array.parse(u'[1,   2  , 3]')
    [Array([Integer(1), Integer(2), Integer(3)])]
    >>> array.parse(u'[a,b]')
    [Array([Identifier(u'a'), Identifier(u'b')])]
    >>> array.parse(u'[a, b]')
    [Array([Identifier(u'a'), Identifier(u'b')])]

Dictionary::

    >>> dictionary.parse(u'{key::value}')
    [Dictionary({Identifier(u'key'): Identifier(u'value')})]
    >>> dictionary.parse(u'{a::123,b::"jkl"}')
    [Dictionary({Identifier(u'a'): Integer(123), Identifier(u'b'): String(u'jkl')})]
    >>> dictionary.parse(u'{1::"one",2::"two",3::"three"}')
    [Dictionary({Integer(1): String(u'one'), Integer(2): String(u'two'), Integer(3): String(u'three')})]
    >>> dictionary.parse(u'{"one"::1,"two"::2,"three"::3}')
    [Dictionary({String(u'one'): Integer(1), String(u'three'): Integer(3), String(u'two'): Integer(2)})]
    >>> dictionary.parse(u'{"name"::"hyunjun",likes::["books","musics","cs"]}')
    [Dictionary({Identifier(u'likes'): Array([String(u'books'), String(u'musics'), String(u'cs')]), String(u'name'): String(u'hyunjun')})]

Method Arguments::

    >>> method_args.parse(u'x y')
    [MethodArgument([Identifier(u'x'), Identifier(u'y')])]
    >>> method_args.parse(u'')
    [MethodArgument()]

Set::

    >>> setter.parse(u'somevariable is 123')
    [Set(Identifier(u'somevariable'), Integer(123))]

    >>> setter.parse(u'somehash is {"key"::"value"}')
    [Set(Identifier(u'somehash'), Dictionary({String(u'key'): String(u'value')}))]

    >>> setter.parse(u'somehash is {"key"::["value", 1, 2]}')
    [Set(Identifier(u'somehash'), Dictionary({String(u'key'): Array([String(u'value'), Integer(1), Integer(2)])}))]

    >>> setter.parse(u'somemethod is method x y do pass end')
    [Set(Identifier(u'somemethod'), Method(MethodArgument([Identifier(u'x'), Identifier(u'y')]), Program([Pass_()])))]

Method::
   
    >>> method.parse(u'method    a   b      c  do pass   end')
    [Method(MethodArgument([Identifier(u'a'), Identifier(u'b'), Identifier(u'c')]), Program([Pass_()]))]

    >>> method.parse(u'method do pass end')
    [Method(MethodArgument(), Program([Pass_()]))]

Call::

    >>> call.parse(u'(1 :plus: 2)')
    [Call(Identifier(u'plus'), CallArgument([Integer(1), Integer(2)]))]

    >>> call.parse(u'(1 2 3:manyargs:4 5 6)')
    [Call(Identifier(u'manyargs'), CallArgument([Integer(1), Integer(2), Integer(3), Integer(4), Integer(5), Integer(6)]))]

Line::

    >>> line.parse(u'pass')
    [Pass_()]
    >>> line.parse(u'somemethod is method x y do pass end')
    [Set(Identifier(u'somemethod'), Method(MethodArgument([Identifier(u'x'), Identifier(u'y')]), Program([Pass_()])))]
    >>> line.parse(u'methodwrapper is method x y do (x :method: y) end')
    [Set(Identifier(u'methodwrapper'), Method(MethodArgument([Identifier(u'x'), Identifier(u'y')]), Program([Call(Identifier(u'method'), CallArgument([Identifier(u'x'), Identifier(u'y')]))])))]

Program::

    >>> program.parse(u'''pass pass pass''')
    [Program([Pass_(), Pass_(), Pass_()])]


If::

    >>> expression.parse(u'if True do True end')
    [If(Boolean(True), Program([Boolean(True)]))]

    >>> expression.parse(u'if True do True else, pass end')
    [If(Boolean(True), Program([Boolean(True)]), Program([Pass_()]))]

"""

from lepl import *
import vict.parse
import vict.tree

spaces = ~Space()[:]
with DroppedSpace():
    identifier = Regexp(ur'[A-Za-z_<>=@!?$%^&*+/-][0-9A-Za-z_<>=@!?$%^&*+/-]*') \
               > vict.tree.Identifier.parse

    elsekey = Literal(u'else')

    string = String() \
           > vict.tree.String.parse
    boolean = Literals(u'True', u'False') \
            > vict.tree.Boolean.parse
    integer = Integer() \
            > vict.tree.Integer.parse
    floating = Float() \
             > vict.tree.Float.parse
    none = Literal(u'None') \
         > vict.tree.None_.parse

    literal = string | boolean | integer | floating | none

    expression = Delayed()
    array = Literal(u"[") \
            & (expression & u",")[:] & expression[:1] \
            & u"]" \
          > vict.tree.Array.parse

    key = literal | identifier \
        | (Literal(u'(') & expression & u')')
    
    pair = key & u"::" & expression
    dictionary = Literal(u"{") \
                 & (pair & u",")[:] & pair[:1] \
                 & u"}" \
               > vict.tree.Dictionary.parse

    line = Delayed()

    program = ((line & (Literal(u'\n') | u'\t')[:]) | elsekey)[1:]  \
            > vict.tree.Program.parse

    method_args = identifier[:] \
                > vict.tree.MethodArgument.parse
    method = Literal(u"method") & method_args \
             & (u'do' & program & u'end') \
           > vict.tree.Method.parse

    call = Delayed()
    call_args = expression[:] \
              > vict.tree.CallArgument.parse
    caller = identifier | (Literal(u'(') & method & u')') \
           | call
    call += Literal(u'(') & call_args & u':' \
            & caller & u':' & call_args & u')' \
          > vict.tree.Call.parse

    pass_ = Literal(u'pass') \
          > vict.tree.Pass_.parse
    wrapped_expr = Literal(u'(') & expression & u')' \
                 > vict.tree.WrappedExpression.parse

    ifpraise = (Literal(u'if') & expression & u'do' & program & u'end') \
             | (u'if' & expression & u'do' & program & u'else,' & program & u'end') \
             > vict.tree.If.parse

    expression += ifpraise | method | call \
                | (literal | array | dictionary | identifier) \
                | wrapped_expr

    setter = identifier & Literal(u'is') & expression \
           > vict.tree.Set.parse
    
    line += (pass_ | setter | call) | expression \
	  > vict.tree.Line.parse


if __name__ == "__main__":
    import doctest
    doctest.testmod()

