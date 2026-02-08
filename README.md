# ax Programming Language

this is my first attempt of creating a language.

## Hello World

```
show("Hello, World!")
```

## Literals

```
# Integer
90

# Floating-point Number
90.7

# String
"Your other programming language"

# Boolean
true
false
```

## Comments

```
# Oneline Comment

~ 
    Multiline 
    Comment 
~
```

## Variable Declaration & Assignment

```
var name = "Alexander The Great"

show(name)

set name = "Marcus Aurelius"

show(name)

var ints = 10
set ints += 80

show(ints)
```

## Function

```
prc power(x) {
    return x ^ 2
}

var result = power(9)

show(result)
```

## Closures

```
prc outer() {
    var counter = 0

    prc inner() {
        set counter = counter + 1

        return counter
    }

    return inner
}

var dec_outer = outer()

show(dec_outer())
show(dec_outer())
```

## Collections

```
# list declaration
var n_number = [1, 2, 3, 4, 5]

# mutation by index
set n_number[0] = [99, 98]

# indexing
show(n_number[0])

# slicing 
show(n_number[0:2])

show(n_number)

# hashmap declaration
var book = { "id" : 1, "name" : "Andrew" }

# mutation by key
set book["id"] = 888

# get value by key
show(book["id"])

show(book)
```

## if-maybe-whatever 

```
var ten = 10
var nine = 9

if (ten >= nine) {
    show("yes, it's bigger")
} maybe (ten <= nine) {
    show("no, it's not")
} maybe (ten == nine) {
    show("it's not equal")
} whatever {
    show("how that even possible?")
}
```

## loop

```
var index = 0

loop (index < 10) {
    show(index)

    index += 1
}

# list iteration

var i = 0
var lst = ["Apple", "Bitcoin", "China"]
var len_lst = length(lst)

loop (i < len_lst) {
    show(lst[i])

    i += 1
}
```
```
```

## TODO
- [x] syntax
- [x] lexer
- [x] parser
- [x] environment
- [x] interpreter
- [x] function declaration
- [x] function call
- [x] built-in functions
- [x] closure
- [x] list
- [x] hashmap
- [x] loop
- [x] if-else
- [x] return statement
- [ ] break statement
- [ ] continue statement
- [x] boolean
- [x] list operations 
    - [x] indexing
    - [x] slicing
    - [x] push
    - [x] mutation with index
- [x] hashmap operations
    - [x] get value by key
    - [x] mutation by key
- [ ] better error message
- [x] comment
    - [x] oneline comment
    - [x] multiline comment
