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

Dictionary::

    >>> dictionary.parse(u'{key::value}')
    [Dictionary({Identifier(u'key'): Identifier(u'value')})]
    >>> dictionary.parse(u'{a::123,b::"jkl"}')
    [Dictionary({Identifier(u'a'): Integer(123), Identifier(u'b'): String(u'jkl')})]
    >>> dictionary.parse(u'{1::"one",2::"two",3::"three"}')
    [Dictionary({Integer(1): String(u'one'), Integer(2): String(u'two'), Integer(3): String(u'three')})]
    >>> dictionary.parse(u'{"one"::1,"two"::2,"three"::3}')
    [Dictionary({String(u'one'): Integer(1), String(u'three'): Integer(3), String(u'two'): Integer(2)})]

"""
from lepl import *
import vict.tree


with DroppedSpace():
    identifier = Regexp(ur'[A-Za-z_<>=!@?$%^&*+-/][0-9A-Za-z_<>=!@?$%^&*+-/]*') > vict.tree.Identifier.parse

    string = String() > vict.tree.String.parse
    boolean = Literals(u'True', u'False') > vict.tree.Boolean.parse
    integer = Integer() > vict.tree.Integer.parse
    floating = Float() > vict.tree.Float.parse
    none = Literal(u'None') > vict.tree.None_.parse
    literal = string | boolean | integer | floating | none

    expression = Delayed()
    array = Literal(u"[") / (expression / u",")[:] / expression[:1] / u"]" > vict.tree.Array.parse

    key = literal | identifier | (Literal(u'(') / expression / u')')
    
    pair = key / u"::" / expression
    dictionary = Literal(u"{") / (pair / u",")[:] / pair[:1] / u"}" > vict.tree.Dictionary.parse

    expression += (literal | array | dictionary | identifier) \
                | ('(' / expression / ')')


if __name__ == "__main__":
    import doctest
    doctest.testmod()

