Copyright (C) 2017 Martin Nilsson.

This document is provided under the Creative Commons Attribution-ShareAlike 4.0 International license (see https://creativecommons.org/licenses/by-sa/4.0/legalcode ).


# Memtran examples book

This will demonstrate the language Memtran by means of examples. 


# Installing Memtran


# Running Memtran


# Hello world

```
import "utf8.mh"

print_utf8("Hello World!\n")    

```

String literals in Memtran construct "byte arrays" representing Unicode characters using UTF-8 encoding. To actually print them as Unicode again, we have to import a library which provides the `print_utf8` function.

## Using `prefiximport` for avoiding name clashes 

```
prefiximport "utf8.mh"

utf8..print_utf8("Hello World!\n")
```

Observe the "double-dot" notation between the module name and the prefiximported functionality. 

## Separating out the string to a variable

``` 
import "utf8.mh"

str ' arr u8 = "Hello World!\n"

print_utf8(str)
```

Here, after the singlequote, we tell the type of the variable `str`. Whenever we declare the type of a variable like this, the compiler reads it as a declaration of a new variable. New variables must always be immediately initialized to a value in Memtran. Also observe how array type notation is with the keyword `arr`. (Insert pirate joke here.) 

## Looping and block syntax

```
import "utf8.mh"

loop :
    print_utf8("Hello World!\n")
;
```

This will loop forever. (Press Ctrl-C in the terminal to interrupt the program.) Observe that the loop statement includes a block, using Memtran's characteristic block syntax with colon -- semicolon. 


## Breaking out of the loop

```
import "utf8.mh"

letters ' arr arr u8 = ["H", "e", "l", "l", "o", " ", "W", "o", "r", "l", "d", "!"]

str ' arr u8 = ""
index ' int = 0

loop :
    concat(ref str, letters[index])

    print_utf8(str)
    println()

    index += 1

    if index >= len(letters) : 
        break 
    ;
;
```

In addition to the demonstrating the keyword `break`, this example also demonstrates array initialization, ref arguments (to the built-in function `concat`), array indexing, simple if statements, and the built-in function `len`.


# Fun with blocks

```
a ' int = 3
mu b ' int = 4

:
    a ' int = 5
    b += a
;

print(a)  // Will print: 3
println()

print(b)  // Will print: 9
println()
``` 

You can use blocks as statements by themselves. Every block is its own namespace, so any variables (or functions!) declared in a block will be local to that block. Also, in order to be able to reassign to `b`, we have to mark that variable as `mu` (mutable) when declaring it.  




TODO: continue with examples



# Evaluation order example

```
import "utf8.mh"

fn f(in ' int) ' int :
    print_utf8("f\n")
    return in + 1    
;

fn g() ' int :
    print_utf8("g\n")
    return 2
;

fn p(in ' int) ' int :
    print_utf8("p\n")
    return in + 3 
;

fn q() ' int :
    print_utf8("q\n")
    return 4
;


a ' int = f(g()) + p(q())
 
print(a)      // This will print: 10

// But the execution order of the other print statements, is undefined...

```

Compiled with the current implementation of the compiler, this will actually print:

```
g
q
f
p
10
``` 

But this should probably not be relied on. As a general rule, if a function has side effects, possibly with the exception of side effects of some rather insignificant kind, you might want to do the function call to that function in a separate statement.















