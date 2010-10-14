r""":mod:`vict.parse`
~~~~~~~~~~~~~~~~~~~~

Identifiers::

    >>> identifier.parse(u"xyz")
    [u'xyz']

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

Integer::
    
    >>> integer.parse(u'1234')
    [Integer(1234)]

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

None::

    >>> none.parse(u"None")
    [None_()]

"""
from lepl import *
import vict.tree


with DroppedSpace():
    identifier = Regexp(ur'[A-Za-z_<>=!@?$%^&*+-/][0-9A-Za-z_<>=!@?$%^&*+-/]*')

    string = String() > vict.tree.String.parse
    boolean = Literals(u'True', u'False') > vict.tree.Boolean.parse
    integer = Integer() > vict.tree.Integer.parse
    floating = Float()
    none = Literal(u'None') > vict.tree.None_.parse
    literal = string | boolean | integer | floating | none

    expression = Delayed()
    array = Literal(u"[") / (expression / u",")[:] / expression[:1] / u"]" > vict.tree.Array.parse

    key = literal | identifier | (Literal(u'(') / expression / u')')
    pair = key / u"::" / expression
    dictionary = Literal(u"{") / (pair / u",")[:] / pair[:1] / u"}"

    expression += (literal | array | dictionary | identifier) \
                | ('(' / expression / ')')


if __name__ == "__main__":
    import doctest
    doctest.testmod()

