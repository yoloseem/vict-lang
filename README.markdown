Vict programming language
====

Vict is a programming language.

Types
----

### Integer

`10`, `25`, `100`

### String

`"Hello, World!"`

### Boolean

`True` / `False`, `None`

### Array

`[1, 2, 3]`, `["apple", "banana", "graph"]`, `[["Kim Hyunjun", "Korea"], ["Victoria", "China"]]`

### Dictionary

`["x":: 5, "y"::10, "z"::15]`, `[123:: "one two three", 456:: "four five six"]`

Method
----

You can define plus function like this: `method a b do (:!+: a b) end`.  
Following code defines a function calculates the average of two numbers.
    average is method x y do
        ((:!+: x y) :!/: 2)
    end

Author
----

Kim Hyunjun (kim@hyunjun.kr)
