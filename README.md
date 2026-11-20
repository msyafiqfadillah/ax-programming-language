# ax Programming Language
## Introduction
ax is a procedural, statically typed programming language and interpreted developed for educational purposes. It covers some concepts, including: static type, closures, collections (such as list (dynamic array) and hashmap).

## Features
### Static Type
in order to declare a name, ax required explicit type writing.
```
var param: number = 10

prc sumOdd(startNum: number): number {
    var index: number = 0
    var result: number = 0

    loop (index < startNum) {
      if (index % 2 != 0) {
        result += index
      }
    
      index++
    }

    return result
}

sumOdd(param)
```

### Unified Numeric Type
ax uses a unified numeric type called `number`. Integer and floating-point values are represented by the same language-level type.
```
var num1: number = 10
var num2: number = 89.55

show(num1 + num2)
```

## Examples
### Hello World
```
show("Hello, World!")
```

### Literals
```
# Integer
10

# Floating-point number
99.9

# string
"abc"

# Boolean
true
false
```

### Comments
```
# Oneline Comment

~ 
    Multiline 
    Comment 
~
```

### Variable Declaration & Assignment
```
var name: string = "Alexander The Great"

show(name)

set name = "Marcus Aurelius"

show(name)

var ints: number = 10
set ints: number += 80

show(ints)
```

### Function
```
prc power(x: number): number {
    return x ^ 2
}

var result: number = power(9)

show(result)
```

### Anonymous Function
```
var newFunc: func(number) -> string = prc (lc: number): string {
  if (lc > 10) {
    return "bigger than ten"
  }

  return "lower or same than ten"
}

newFunc(9.9)
```

### Collections
```
# list declaration
var n_number: list[number] = [1, 2, 3, 4, 5]

# mutation by index
set n_number[0] = 99

# indexing
show(n_number[0])

# slicing 
show(n_number[0:2])

show(n_number)

# hashmap declaration
# hashmap key always string, so the only type parameter is for the value
var book: hashmap[any] = { "id" : 1, "name" : "Andrew" }

# mutation by key
set book["id"] = 888

# get value by key
show(book["id"])

show(book)
```

## if-maybe-whatever 

```
var ten: number = 10
var nine: number = 9

if (ten >= nine) {
    show("it's bigger")
} maybe (ten <= nine) {
    show("it's smaller")
} maybe (ten == nine) {
    show("it's equal")
} whatever {
    show("how that even possible?")
}
```

### loop
```
var index: number = 0

loop (index < 10) {
    show(index)

    set index += 1
}

# list iteration

var i: number = 0
var lst: list[string] = ["Apple", "Bitcoin", "China"]
var len_lst: number = length(lst)

loop (i < len_lst) {
    show(lst[i])

    set i += 1
}

# continue & break

var c_index: number = 0

loop (c_index < 10) {
    show(c_index)

    if (c_index % 2 != 2) {
      c_index += 1
      continue
    } maybe (c_index == 8) {
      break
    }

    set c_index += 1
}
```
