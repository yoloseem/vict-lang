Vict programming language
====

Vict is a programming language.  
This, the Vict programming language, takes it name from 'Victoria', a member of Korean idol girl group f(x).

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

`{"x":: 5, "y"::10, "z"::15}`, `{123:: "one two three", 456:: "four five six"}`

Binding
----

In Vict, there is no way to only assigning, but it exists with binding.  
You can bind literals or method with keyword `is` like following code:
    ten is 10
    fruits is ["Apple", "Banana", "Graph"]
    user is {"name":: "Jayden", "age":: 17, "likes":: ["watching movie", "playing soccer", "playing video games"]}

Method
----

You can define plus function like this: `method arg1 arg2 ... do expr1 expr2 ... end`.  
Following code defines a function calculates the average of two numbers.
    average is method x y do
        ((:!+: x y) :!/: 2)
    end

There is no return keyword, so the function will return last calculation result automatically.

Author
----

Kim Hyunjun <kim@hyunjun.kr>