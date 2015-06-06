Vict programming language
====

Vict is a programming language. Vict took its name from Victoria.

Run
----

### Source Code

Source code is available on GitHub repository.

    git clone git://github.com/kimjayd/vict-lang.git

### Installation

Python has to be installed to run Vict. 

    python setup.py install

### Usage

    python -m vict.main some/code.vict

You can also use REPL mode.

    python -m vict.main repl

or just
   
    python -m vict.main

    Vict-lang 0.1
    Type `help` for more information.
    vict> "Hello!"
    Hello!
    vict> 

You can type `exit` to leave.

Types
----

### Integer

`10`, `25`, `100`

### String

`"Hello, World!"`

### Boolean

`True` / `False`, `None`

### Array

`[1, 2, 3]`, `["apple", "banana", "grape"]`, `[["Kim Hyunjun", "Korea"], ["Victoria", "China"]]`

### Dictionary

`{"x":: 5, "y"::10, "z"::15}`, `{123:: "one two three", 456:: "four five six"}`

Binding
----

In Vict, there is no way to only assigning.
You can bind literals or method with keyword `is` like following code:

    ten is 10
    fruits is ["Apple", "Banana", "Graph"]
    user is {"name":: "Jayden", "age":: 17, "likes":: ["watching movie", "playing soccer", "playing video games"]}

Method
----

You can define the function with following syntax: `method arg1 arg2 ... do expr1 expr2 ... end`.  
Following code defines a function calculates the average of two numbers.

    average is method x y do
        ((:+: x y) :/: 2)
    end

There is no return keyword, so the function will return last calculation result automatically.

if-else Statements
----

You can make if statement with following syntax:

    (if cond do expr1 expr2 ... end)

You can also make if-else statement.

    (if cond do expr1 expr2 ... else expr3 expr4 ... end)

Following code defines the function calculate Factorial(n):

    vict> factorial is method n do (if (n :=: 1) do 1 else (n :*: (:factorial: (n :-: 1))) end ) end
    <Function at a1s2d3f4>
    vict> (5 :factorial:)
    120

Author
----

[Hyunjun Kim](https://yoloseem.github.io/)
