---
title: Memtran Reference Manual    
output:
  html_document:
    toc: true
...

Copyright (C) 2017 Martin Nilsson.

This document is provided under the Creative Commons Attribution-ShareAlike 4.0 International license (see https://creativecommons.org/licenses/by-sa/4.0/legalcode ).

Note that this document currently optimistically describes future functionality that is not yet implemented at all, as if it already existed. Scepsis is natural and healthy when reading such a document -- but be aware that I am absolutely aware that things might need to be changed in order to work. 

# About Memtran

Memtran is a memory managed programming language which is compiled, imperative, strongly typed, memory safe, and open source. 

Due to the special characteristics of how the Memtran language works (i.e. its semantics), the compiler will always know where in a program that memory can or should be freed. It can therefore insert necessary, automatically generated destruction operations at the right places in the executable file that it generates, without any need for a tracing garbage collector. 

Further, Memtran has the following features: runtime polymorphism (through its "variant-box" types), circumventable data abstraction, function overloading, first-class functions, multiple return values, generics, and local functions (but not "true closures" as is meant by the term in the Lisp family of languages). On the other hand, Memtran does _not_ provide OOP-style inheritance of code or data.

In contrast to most other languages, _assignment_ in Memtran follows the principle "assign-by-a-conceptually-unique-instance-of-the-whole-datastructure". When it comes to _argument passing_, on the other hand, you can choose between (1) "pass-by-a-conceptually-unique-instance-of-the-whole-datastructure", and (2) pass-by-reference. 

An important inspiration for Memtran is the language Euphoria, which can be both interpreted and compiled. In fact, one can say that Euphoria and Memtran have similar semantics. But the details of their implementation are very different, and also, Memtran has a comparatively more static type system. The ambition is that Memtran will both be a bit faster than Euphoria (on modern hardware), and provide some different or additional features. 
 
The Memtran compiler uses (will use) LLVM as its back-end; its front-end is currently written in Python. Memtran is provided under the GPL v3.0 license.

As this is free software, and a very early version, even, it can't be guaranteed that any of Memtran's features work as they are supposed to do. 

# The compiler

The Memtran compiler (not very well-tested at all) is written in Python, using the LLVM framework for its back-end.


# About this document

At this early stage in Memtran development, most anything in this manual may be subject to change.

Also, this document does not constitute a formal specification of Memtran (no such specification exists at the moment). In some cases implementation details are described that would probably not be part of a formal specification.

# Lexical structure

## Encoding

The compiler expects UTF8-encoded program files or module files.

## Case-sensitivity

Memtran programs are case-sensitive, i.e. '`A`' is considered a different character than '`a`', and so on.

## "Free-form layout" syntax

It bears noting that line-breaks are interpreted syntactically in the same way as whitespace (An exception is newlines within string literals, which is not allowed). So you can layout your Memtran statements as you wish -- i.e. you can have statements spanning over several lines, or alternatively have several statements on a single line. Also, special care has been taken during the design of Memtran's syntax so as to make semicolons after statements (or struct posts) completely optional.  

## Reserved characters

```
    [  ]  (  )  {  }  :  ,  ;  %  *  +  /  -  =  <  >  !  &  .  "  `  |  '  \  ~  whitespace  newline  CR  EOF
```

### Distinct tokens that are reserved characters, or combinations of reserved characters

```
    [  ]  (  )  {  }  :  ,  ;  %  *  +  /  -  =  <  >  !  .  `  '  \  ~  
    ..  ...  ||  &&  /*  */  //  %=  *=  +=  /=  -=   >=  <=  ==  !=  '' 
```

The lexer will parse these eagerly, i.e. prefer the longer ones. So '`...`' will always be parsed like one token, not as (for example) two tokens '`..`' and '`.`'. Apart from taking that into consideration (NOTE: and it is probably only legal syntax in one way anyway...), you don't need whitespace or newline inbetween these, or inbetween these and number literals, string literals, keywords or identifiers.

## Keywords (reserved words)

```
    if  else  loop  break  continue  for  to  downto  over  in  indexfactor  indexoffset  return  mu  ref  inline
    switch  contenttype  case  default  true  false  nil  fn  end  import  prefiximport  private  repeat  trash  uninitialized
    vbox  type  label  construand  nil  bool  i8  i16  i32  i64  int  u8  u16  u32  u64  uint  f32  f64  arr 
    IF  ELSE  SWITCH  CONTENTTYPE  CASE  DEFAULT
```

You need whitespace or newline inbetween these. You also need whitespace between keywords and number literals. 

## Identifiers

Any _identifier_ in Memtran is a sequence of one or more characters (alphanumeric or other symbols) pertaining to these rules:

* must not contain any reserved character
* must not start with a digit
* must not be a keyword   

Note that some identifiers are already "occupied" in the global scope as names of built-in functions. Overloading of these built-in function names is still possible though. 

Note that this has intentionally been designed so to allow any UTF-8 character that is not a reserved character, to be used in an identifier. This will go some way towards allowing programmers to think in their native language, which is something believed to be more for the good than not.


## Comments

_Examples:_

```
    // this is a comment to the end of the line

    /*
        This is a
        multiline comment. /* hello*/ hello
    */ 
```  

Comments are ignored by the lexer. Multiline comments can be nested. 

# Preliminary definitions

## BNF notation

In the BNF notation used in following chapters, reserved characters and combinations of reserved characters are surrounded by single quotes, while keywords are surrounded by double quotes. (NOTE: As an exception, the reserved character `'` will, for simplicity, be surrounded by double quotes.)

The BNF given does not rule out all non-well-formed constructions, but simply gives those expressions that are accepted by the parser stage of the compilation. After the parser stage, the compiler runs separate "semantic validation" passes in order to rule out all non-well-formed statements. The additional descriptions given in this manual should hopefully make clear what is required in order to form well-formed syntactical constructions.

For a BNF suitable for automatic parser generation, see the folder `extras/antlr4_parser`.

## Slots and subslots

This document will use the term _slot_ to refer to a variable (mutable or immutable, global or local), or a function parameter (mutable or immutable) or loop variable (mutable or immutable). The term _subslot_ will be used to refer to struct fields, array indices, xorbox type value casevalues, subfields, subindices or sub-casevalues of the value stored (conceptually speaking) in a slot.  

Due to Memtran's semantics, the terminology of slots is extra suitable -- it will not lead the user astray, semantically, to imagine the memory handled by a Memtran program as consisting simply of a number of slots, some of which will have the capacity to store values of arbitrary size. The actual implementation of these semantics is a wholly different matter though. Some of the following chapters will also give some idea of how the implementation handles memory behind the scenes, and knowledge of this will help the performance-aware programmer make good design decisions.   

## Scopes and subscopes

All Memtran statements belong to a _scope_. Statements in the top-level of a program belong to the so called "global" scope, unless they are within a block, in which case they belong to the ("local") subscope defined by that block. _Subscopes_ of a scope are all blocks within that scope, or blocks within blocks in that scope, and so on. A subscope of a scope _x_ is not the same scope as scope _x_. (NOTE: But according to the standard definition of scope, a subscope includes its containing scopes (but does not include other subscopes of such containing scopes). Update manual to reflect this standard definition.) 

## Identifier namespaces

In a Memtran program. the general rule is that the same identifier may not be used for two things. Function names, slot names and type names live in the same namespace. There are, though, a number of exceptions to this, as follows:

1. _Identical naming following block scope rules._
2. _Function overloading._ There may be several functions declared with the same name in the same scope, provided all those functions have different argument type lists. Likewise, function template names may be overloaded. For the rules of that, see the chapter on Generics. 
3. _Names declared in another module._ From a module imported using the keyword `import`, whereas all type names are imported, only those slot names and function full names not declared `private` are imported into the namespace of the importing program or module file. And from a module imported using the keyword `prefiximport`, only type names are directly imported -- no other names declared in that module are imported into the namespace of the importing program or module file (i.e. they have to be accessed through the module name). 
4. _Module names_. Speaking of that, module names belong to a separate namespace. All the names of the modules making up a program must be different though, not just the module names accessed per file. There is currently no way of resolving a module nameclash, other than renaming and recompiling all conflicting modules. 
5. _Typeswitch statement aliasing._ Within a typeswitch statement case, an identifier expression at the beginning of the typeswitch statement will change meaning so as to mean that identifier expression as outside the typeswitch statement case, casted into one of its value's xorbox type cases.
6. _Struct field names_. Struct field names are used in struct types, struct indexing expressions and struct expressions. The field names are considered local to a struct, and won't conflict with any other names declared in a program.
7. _Struct tags_. (NOTE: Elaborate somewhat here!)
8. _Labels_. The labels used with loops and their continue statements and break statements, belong to a separate namespace. You can probably even use the same label several times in the same program, for different "loop hierarchies", so to speak. (NOTE: elaborate on this when it is implemented...) 

## Memory safety exceptions

The following two listed cases should supposedly be the only exceptions to Memtran's promise of memory safety. If you refrain from triggering/using the things listed, you should supposedly not have any segmentation faults or erroneous overwrites of memory:

1. Stack overflow (like, due to infinite or extremely deep recursion).
2. Utilizing the `uninitialized` keyword
3. Using the as yet non-existing C interface.

But who knows! 

By the way, _reading_ uninitialized memory is possible with `trash` or when using the `--recovermode` compiler flag. But these reads should at least be type safe. Also, of course, depending on how you see things, runtime language errors like "array index out of bonds" are in a way simply cosmetics upon another runtime error.     

# Type system

``` 
                                                    // IMPLEMENTATIONAL CATEGORY
    type ::= 
        | "nil"                                     // just a head (of size 0)
        | "bool"                                    // just a head
        | "i8"                                      // just a head               (NOT YET IMPLEMENTED)
        | "i16"                                     // just a head               (NOT YET IMPLEMENTED)
        | "i32"                                     // just a head               (NOT YET IMPLEMENTED)
        | "i64"                                     // just a head               (NOT YET IMPLEMENTED)
        | "int"                                     // just a head
        | "u8"                                      // just a head
        | "u16"                                     // just a head               (NOT YET IMPLEMENTED)
        | "u32"                                     // just a head               (NOT YET IMPLEMENTED)
        | "u64"                                     // just a head               (NOT YET IMPLEMENTED)
        | "uint"                                    // just a head               (NOT YET IMPLEMENTED)
        | "f32"                                     // just a head
        | "f64"                                     // just a head
        | dynamic_size_array_type                   // head + memory pointed to  (and whose memory pointed to, may have fields pointing to further memory)
        | struct_type                               // just a head               (but whose fields may or may not point to further memory)
        | variant-box_type                          // just a head               (but whose "casevalue" field may or may not point to further memory)
        | function_type                             // just a head
        | identifier                                // N/A                       (a type defined in a type declaration statement)
        | parametrized_type                         // N/A                       (a type defined in a parametrized type declaration statement)
        | parenthesized_type                        // N/A

    parenthesized_type ::=
        '(' type ')'
```

Types are specified in many kinds of Memtran statements, for example type declaration statements. 

As pertains to Memtran, given an associated type, certain series of regions of bits in computer memory can be unambigously viewed as representing certain mathematical value constructions. (NOTE: I don't know if I can put it better than that.)
    
Syntactically, you may put parentheses around types in order to disambiguate them.

All Memtran types have an _extension_, by which is meant the set of values it can be the type _of_. The value sets that make up the extensions for the possible Memtran types, are considered completely disjoint. So, for example, the value 3 of type I8 is a completely different 3 than the value 3 of type U8. In a program, you have to convert between them explicitly, using a conversion function. (But note in this regard that named types, as defined in a type declaration statement, are considered identical to their definition type).

## `nil`

Type `nil` consists of the sole value `nil{}`. It can be considered as a predefined named struct type (see below).

The type `nil` has the following implementational memory layout:

```
    head
     _________________
    |                |
    | 0 bits of data |
    |________________|
``` 

NOTE 1: The word "head" in this and following depictions is just what the memory box right below it _is_, so in no way does it imply that "just a head" data types like this one would have a head separate from the rest of its memory.

## `bool`

Type `bool` has the two possible values `true` and `false`.

The short-circuiting infix operators `&&` and `||` (see Chapter X), the prefix operator `!`, and the infix operators `==` and `!=`, operate on `bool` type values. 

The type 'bool' has the following implementational memory layout:

```
     head
     ____________________________________
    |              |                    |
    | extra zeroes | the true/false bit |
    |______________|____________________|
```

Built-in functions that operate on `bool` type values: `print` (See Chapter X).


## `i8`, `i16`, `i32`, `i64` and `int`

`i8`, `i16`, `i32`, `i64` are signed integer types of the specified number of bits. The memory size of `int` is equal to the word size of the targeted machine.

The infix operators `+`, `-`, `*`, `/`, `==`, `!=`, `>`, `<`, `>=`, `<=`, `%`, and the prefix operator `-`, operate on these types of values. The special assignment operators `+=`, `-=`, `*=`, `/=`, and `%=` are also usable on these types of values, and work just like in any C-syntax style language. 

The signed integer types have the following implementational memory layout:

```
    head
     ________________
    |               |
    | numeric value |
    |_______________|

``` 

Built-in functions that operate on these types of values: `print`, conversion functions, and others (See Chapter X).

NOTE: i8, i16, i32, i64 are not yet implemented.

## `u8`, `u16`, `u32`, `u64` and `uint`

`u8`, `u16`, `u32`, `u64` are unsigned integer types of the specified number of bits. The memory size of `uint` is equal to the word size of the targeted machine.

The infix operators `+`, `-`, `*`, `/`, `==`, `!=`, `>`, `<`, `>=`, `<=`, `%`, and the prefix operator `-`, operate on these types of values. The special assignment operators `+=`, `-=`, `*=`, `/=`, and `%=` are also usable on these types of values, and work just like in any C-syntax style language. 

The unsigned integer types have the following implementational memory layout:

```
    head
     ________________
    |               |
    | numeric value |
    |_______________|

``` 

Built-in functions that operate on these types of values: `print`, conversion functions, and others (See Chapter X).

NOTE: u16, u32, u64, uint are not yet implemented. 

## `f32` and `f64`

`f32` and `f64` are single- and double-precision floating point number types.

The infix operators `+`, `-`, `*`, `/`, `==`, `!=`, `>`, `<`, `>=`, `<=`, `%`, and the prefix operator `-`, operate on these types of values. The special assignment operators `+=`, `-=`, `*=`, `/=`, and `%=` are also usable on these types of values, and work just like in any C-syntax style language. 

The floating point types have the following implementational memory layout:

```
    head
     ________________
    |               |
    | numeric value |
    |_______________|

``` 

Built-in functions that operate on these types of values: `print`, conversion functions, and others (See Chapter X).


## Dynamic size array types

```
    dynamic_size_array_type ::=
        "arr" type 
```

_Examples:_

```
    arr arr bool  // a dynamic size array of dynamic size arrays of Bool
    arr Int 
```

The built-in function `len` gives the length (number of indices) of a dynamic size array type value.

The implementational memory layout of a dynamic size array type value, is:

```
     head         
   _____________________________________________
   |     |        |             |       |      |
   |  o  | length | totalMemory | gflag | gptr |
   |__|__|________|_____________|_______|______|                    thing pointed to
      |                                                             ________________________________________________________________________
      |                                                            |                                               |                       |
      \----------------------------------------------------------> | array data (values of indices 0..length - 1)  | possibly extra memory |
                                                                   |_______________________________________________|_______________________|
```

The purposes of _gflag_ and _gptr_ are described in Chapter X. 

The individual indice values of a dynamic size array can be accessed through array indexing (see Chapter X and Chapter X (the latter chapter describes assigning to array indices)), which starts from index 0 for the first value of the array. 

Built-in functions that operate on dynamic size array type values: `add_last, concat, len, remove_last` (See Chapter X).


## Struct types

```
    struct_type ::=
       identifier '{' (identifier "'" type)* '}'
```

_Example:_

```
    player{
        healthPoints ' int 
        score ' int
        id ' arr u8
    }
```

A struct type has an associated "tag" specified by the leftmost identifier (i.e. "player" in the example above).

Each field of the type is optionally syntactically terminated by a semicolon.

The individual fields of a struct type value can be accessed through struct indexing. See Chapter X and Chapter X (the latter chapter describes assignment to fields).

The implementational memory layout of a normal struct type value is one contiguous block of memory, possibly with memory padding between the individual fields:

```
    head
    ______________________________________________________________________
    |         |                  ||        |                  ||         |
    | field 1 | possible padding || field2 | possible padding || etc.    |
    |_________|__________________||________|__________________||_________|
```

If you want your struct data as a thing pointed to, implementationwise, you can simply embed it in a one-element dynamic array.

Structs with zero fields are definitely allowed.

As would be expected, two fields of the same struct may not be named identically.


## Variant-box types

```
    variant-box_type ::=
        (type '/')* type 
```

_Example:_

```
    arr f32 / game_player{health_points ' int    score ' int} / nil     // parsed as (arr f32) / game_player{health_points ' int   score ' int} / nil    
```

As far as I can understand, Memtran variant-box types aren't proper "sum types" -- but rather a variant-box type value is to be regarded semantically as a container value _containing_ exactly one value -- which value can be of either of its type's definitional type cases! It is just that certain implicit conversion features are provided syntactically, between the variant-box type and its several definitional "type cases". This means that the Memtran type `T / U` is a completely distinct type from the types `T` or `U`, as regards type identity, not a proper supertype; and its extension is not defined as the set theoretical disjoint union of the extensions of its type cases. But rather, its extension is the set of possible variant-box type values for that particular variant-box type.  

Time will probably tell whether this variant-box type concept was a good idea or not. 

The implementational memory layout of a variant-box type value is:

```
    head                  
    ______________________________________________
    |        |           |                       |
    | caseNr | casevalue | possibly extra memory |
    |________|___________|_______________________|        
                                        
       
```

, where _caseNr_ is an integer specifying which of the types, among the type cases in the type declaration of the xorbox type, that _casevalue_ has.

In an assignment statement (see Chapter X), or in the implicit assignment of a function call statement (i.e. assigning the value of a non-ref argument expression to the parameter), a slot or subslot that has a variant-box type can be set directly to a value of any of the type cases in the type declaration of that variant-box type. A variant-box type value will in that case be calculated "implicitly", whose _caseNr_ field will be set to correspond to the correct type case, and whose _casevalue_ field is set to the assigned value. The same is also true about setting the individual values of an array expression or a struct expression (see chapters X, X, X and X).  

You can access the _casevalue_ field of a variant-box type value through a cast to one of the types among the type cases in the variant-box type. See Chapter X.

You can test which type, among the type cases of the variant-box type, the _casevalue_ field of an variant-box type value has, using a contenttype statement. This statement also replaces the need for many explicit variant-box casts. See Chapter X.

Two type cases of a variant-box type may not be identical types.

Implementational detail: In order to make it memory safe to use the `trash` keyword for the allowed kinds of variant-box type values with regard to that, all object code operations using _caseNr_ are actually done on _caseNr_ modulo the number of type cases of the relevant variant-box type.   

## Function types

```
    function_type ::=
        "fn" '<' [function_type_args] ["to" (type ',')* type] '>'    

    function_type_args ::=
        (function_type_arg ',')* function_type_arg
        
    function_type_arg ::=
        normal_function_type_arg
        | ref_function_type_arg

    normal_function_type_arg ::=
        ["mu" | "construand" | ("mu" "construand") | ("construand" "mu")] type

    ref_function_type_arg ::=
        "ref" type
       
```

_Examples:_

```
    fn<f64, f64 to f64>
    fn<>
    fn<int / nil to bool, bool>
    fn<ref int, construand u8, mu arr f32>
```

A function type has a number (zero or more) of argument types, which (if any) are specified, separated by commas, after the "triangular bracket" following after the keyword `fn`. 

A function type can have zero or more return types. If there are more than zero return types, these return types are specified after a keyword "to", separated by commas. Observe that the return type(s) are specified _within_ the "triangular brackets".   

Argument type(s) of a function type may be marked as `ref`. For an explanation of the ref argument functionality, see chapter X. Having contra not having the `ref` marker on an argument affects the identity of the function type, in an analogous way with the example with `mu` given right below. 

Function type normal argument types may have `mu` in front of them. For implementational reasons, this _does_ affect the identity of the function type, i.e.

    fn<int>

and
    
    fn<mu int>

are _not_ considered identical types.

Function type normal argument types may also have `construand` in front of them. This is a purely optimizational marker, and is explained in chapter X. It, too, does affect the identity of the function type.  

 Function type ref argument types are by default something like `mu`, and thus should _not_ be marked thus.  

The implementational memory layout of a function type value is:

```
    head
    ____________________
    |                  |
    | function pointer |
    |__________________|

```


Memtran currently does not provide function types with a variable argument number.

A function call (see chapter X) can be used to call the function implied by a value of function type.

## Parametrized types

These will be covered in Chapter X, "Generics".


## Memory layout example

As seen from the BNF syntax given above, certain types are constructed from other types. Let's say we have the following type definition, followed by a variable declaration with associated assignment of a value:

```
type my_struct_type = my_struct_type{
    the_array ' arr int
    other_stuff ' arr f32 / bool
}

my_struct : my_struct_type = my_struct_type{
    the_array = [1, 2, 3]
    other_stuff = [3.14]
}

```

Given this, the implementational memory layout of the value belonging to the slot `my_struct` will be like this:

``` 

    "theArray" field (array value)                                       "otherStuff" field (variant-box type value)
    __________________________________________________________________________________________________________________________________________________________________________
    |     |            |              |       |      |                  ||        |     |            |             |       |      |                       |                  |
    |  o  | length (3) | totalMemory  | gflag | gptr | possible padding || caseNr |  o  | length (1) | totalMemory | gflag | gptr | possibly extra memory | possible padding |
    |__|__|____________|______________|_______|______|__________________||________|__|__|____________|_____________|_______|______|_______________________|__________________|    
       |                                                                             |                                 
       v                                                                             v
      _____________________________________                                       ________________________________                                            
      |   |   |   |                       |                                       |      |                       |
      | 1 | 2 | 3 | possibly extra memory |                                       | 3.14 | possibly extra memory |
      |___|___|___|_______________________|                                       |______|_______________________|


```

The whole of this memory tree is considered one single value. Due to Memtran's semantics, you can, semantically speaking, conceptually regard the value as "stored" in the "slot" `my_struct`.
 

# Expressions

```
    expression ::=
        "nil{}" 
        | "true" 
        | "false"     
        | integer_literal
        | floating_point_number_literal
        | string_literal 
        | identifier_expression    
        | type_clarified_expression                                       
        | array_indexing_expression                 
        | struct_indexing_expression                               
        | array_expression
        | struct_expression 
        | prefix_function_call_expression
        | infix_function_call_expression
        | infix_operator_expression
        | prefix_operator_expression
        | xorbox_downcast_expression                    
        | &&_expression                  
        | ||_expression
        | "end"
        | IF_expression
        | SWITCH_expression
        | CONTENTTYPE_expression
        | parenthesized_expression        

    parenthesized_expression ::=
        '(' expression ')'

    
```

Expressions are used in many kinds of Memtran statements, for example assignment statements.

Syntactically, you may put parentheses around expressions in order to disambiguate and/or alter their combination order. Note: it is said "combination order" here, not "evaluation order". The actual evaluation order may be different. See Chapter X. 

## `nil{}`

This literal represents the sole value of the type `nil`.

## `true` and `false`

These two literals represent the possible values of the type `bool`.

## Number literals

_Examples:_

```
    0 
    -253458909
    32.3
    .83
    -23489.
``` 

Integer literals are sequences of at least one digit, possibly with a minus sign at the front.
Floating point number literals are sequences of at least one digit, with one period symbol interspersed among the digits, and possibly with a minus sign at the front. 

The exact type of a number literal, which is used as an expression, is deduced from the context. In cases where the compiler needs to guess the exact type,
per default, integer literals will be guessed in the order `Int`, `UInt`, `I64`, `U64`, `I32`, `U32`, `I16`, `U16`, `I8`, `U8` (NOTE: Change this order!), and floating point number literals will be guessed in the order `F64`, `F32`. If you need or want to, you can specify the exact type of the number by embedding the number literal in a type clarified expression (see chapter X).

Hexadecimal or binary notation for numbers are currently not available, but will be in the future.

## String literals

_Example:_

```
    "Hello world!\n"
```

(NOTE: Info about escape characters etc.)

A string literal represents a dynamic size array of `u8`, representing the text of the string literal (taking the interpretation of escape characters into account), in UTF-8 encoding. In order to actually print such byte arrays as text to standard output, or to do other interesting things with them, the "utf8.cim" standard library must be imported (using an import statement of some kind or another -- see Chapter X). This library provides the functions

```
    fn print_utf8(byte_array ' arr u8)
    fn prompt_utf8() ' arr u8
    ... 
```

, which operate directly on arrays of `u8`. 

The same library might also in later version provide an abstracted type `string_utf8`, with has further operations defined on it. 

## Identifier expressions

```
    identifier_expression ::=
       identifier
       | module_specified_identifier
``` 

An identifier expression consisting simply of an identifier will evaluate to the value stored (conceptually speaking) in the slot (mutable or immutable) with the same name, or to a function type value corresponding to a global function with the same name (but if the function name is overloaded, the exact function must sometimes be clarified by embedding the identifier expression in a type clarified expression (see Chapter X)). Also, built-in functions, or functions specified `inline`, cannot be accessed thus. To be able to get a function type value corresponding to a built-in or `inline` function, simply wrap it in another function definition, whose name can then be accessed thus. (The need for this may be obliviated in the future.)  

Names of types cannot be used in identifier expressions. (NOTE: they are not first class values in this initial, compiled, version of the language. But some syntactical care has been taken to make it possible to use types as first class values sometime far in the future, in some very different version of Memtran.)

If the name corresponding to the identifier used as an identifier expression is not declared in the program, the compiler will complain. For names of slots, the slot must be declared and assigned to at a previous point in the program to where the identifier expression is used. For names of functions, the function can be defined anywhere in the current file, or in an imported file. But there are restrictions to when functions thus used in expressions may actually be called (i.e. using the function name identifier expression in a function call expression or statement, in the scope that contains this function, or any parent scope). See Chapter X. (NOTE: maybe the same restrictions for getting a function type value. Yes. NEW NOTE: Getting a function type value is analogous to accessing a slot, i.e. the function must prolly be declared above the referring.)

Module specified identifiers will be covered in Chapter X.

## Type clarified expressions

```
    type_clarified_expression ::=
        expression "''" type
```

_Examples:_

```
    32.3 '' f32
    plus '' fn<int, int to Int>
```

## Array indexing expressions

```
    array_indexing_expression ::=
        expression '[' expression ']' 
```

_Example:_

```
    my_array[32][x + 19] 
```

The expression to the left should evaluate to a dynamic size array type value. The expression between the brackets should evaluate to an integer >= 0 of type `int` (NOTE: more type alternatives may be implemented later). 

This operation gets the value corresponding to the index specified by the expression between the brackets, of the array type value specified by the expression to the left. If the index is out of bounds for the array type value, a runtime error is thrown by the program. In the case when the `--recovermode` compiler flag is set, the error can be recovered from when the index type of the relevant array is any of the types nil, bool, u8, u16, u32, u64, uint, i8, i16, i32, i64, int, or struct types or variant-box types thereof, possibly recursively so. A non-specified value of the relevant index type will be returned in that case. For other index types, the program will always exit with an error message. 

## Struct indexing expressions

```
    struct_indexing_expression ::=
        expression '.' identifier
```

The expression to the left of the period symbol should evaluate to a struct type value. The identifier to the right of the period symbol should be an identifier representing one of the fields of the struct type value of the expression to the left.

This operation evaluates to the value of the field specified by the identifier to the right of the period symbol, of the struct type value specified by the expression to the left.

## Array expressions

```
    array_expression ::=
        array_expression_individual_values
        | array_expression_repeated_initialization
        | array_expression_no_initialization
```

### Array expressions of individual values

```
    array_expression_individual_values ::=
        '[' [(expression ',')* expression] ']'
```

_Examples:_

```
    []
    [2, 3, 8 + x, 15, 26]
    ["Hello", " world!\n"]
    [[1, 2 , 3], [1, 2]] 
```

This expression evaluates to an array containing, at consecutive indices starting from 0 for the leftmost expression between the brackets, the values of the consecutive comma separated expressions between the '`[`' and the '`]`'. 

The exact type of the array produced is deduced from the surrounding context. But there are some cases in which it would be theoretically possible to infer the exact type, but in which the current type inferrer of the compiler might still need to ask you to specify the exact type, by putting the array expression of individual values into a type clarified expression.

When the indices type of the array expression is deduced from the context as being a variant-box type, and the corresponding expression for an index in the array expression is of a type that is one of the type cases of the variant-box type, the expression's value will automatically be converted to a value of that variant-box type (i.e. at runtime, in the general case (NOTE: ??)), which will have its _caseNr_ and _casevalue_ fields set correspondingly.

If this expression were a regular (built-in) function, the constituting expressions would be considered 'construand' arguments. 

### Array expressions of repeated initialization

```
    array_expression_repeated_initialization ::=
       '[' expression "repeat" expression ']'
```

_Example:_

```
    [0 repeat 5] // gives the same value as [0, 0, 0, 0, 0]
```

These expressions evaluate to an array of length specified by the expression (which should evaluate to an integer >= 0 of type `int` (NOTE: more type alternatives may be implemented later)) to the right of the `repeat` keyword, containing the value of the expression to the left of the `repeat` keyword, _repeatedly evaluated_ across all the indices of the array. This means that if the expression to the left gives different values for consecutive evaluations of it, the produced array may come to have differing values at differing indices. Which can probably be useful as an array initialization technique. 

The >= 0 constraint is checked at runtime, and if the check fails a runtime error will occur. But if the `--recovermode` compiler flag is set, the expression will simply return an empty array in this case.

The exact type of the array value produced will be deduced from the surrounding context. But there are some cases in which it would be theoretically possible to infer the exact types, but in which the current type inferrer of the compiler might still need to ask you to specify the exact type, by putting the array expression of repeated values into a type clarified expression.

When the indices type of the array expression is deduced from the context as being an variant-box type, and the expression for the repeated value in the array expression is of a type that is one of the type cases of the variant-box type, that expression's value will automatically be converted to a value of the variant-box type, which will have its _caseNr_ and _casevalue_ fields set correspondingly.

If this expression were likened to a regular (built-in) function call, to the extent that such likening is possible, the repeated evaluation of the expression to the left of the semicolon would be considered to be producing the arguments to a series of 'construand' parameters.  

### Array expressions with no initialization
 
```
    array_expression_no_initialization ::=
        '[' ("trash" | "uninitialized") expression ']'
```     

_Examples:_

```
    [trash 13]
    [uninitialized x + 7]
```

These expressions evaluate to an array of length specified by the expression (which should evaluate to an integer >= 0 of type `int` (NOTE: more type alternatives may be implemented later)) to the right of the semicolon. 

The >= 0 constraint is checked at runtime, and if the check fails a runtime error will occur. But if the `--recovermode` compiler flag is set, this expression will simply return an empty array in that case.

The exact type of the array produced is deduced from the surrounding context. But there are some cases in which it would be theoretically possible to infer the exact type, but in which the current type inferrer of the compiler might still need to ask you to specify the exact type, by putting the array expression with no initialization into a type clarified expression.

Allowed types of the indices type of the array expression's type, for the `trash` variant, are: `nil`, `bool`, `i8`, `i16`, `i32`, `i64`, `int`, `u8`, `u16`, `u32`, `u64`, `uint`, `f32`, `f64`, or struct types or variant-box types thereof, possibly recursively so. This expression variant produces UNSPECIFIED values at the indices of the array -- actually uninitialized memory, but safe to access anyway from a crass memory safety perspective, since it will always possible to interpret the bit patterns accessed in some acceptable way with regards to memory safety, for the listed allowed types.

When programming generic functionality using function templates, and in some other circumstances, the restriction to the index types listed can be annoying. Therefore, the potentially memory unsafe, `uninitialized` variety of this kind of expression can be used instead. When actually initializing such memory (which should recommendably be done as soon as possible, and certainly before the end of the lifetime of the slot that ends up holding the produced value), the keyword `uninitialized` can also be specified in the assignment statement(s) used -- this prevents the program from trying to automatically destruct the previous value otherwise assumed to be stored in such a slot. 

If, using `uninitialized`, you are unsure whether the resulting program is memory safe, you should probably use an alternative solution instead, such as using an array expression with repeated initialization, initializing to a specific value of the type your array is indexed with, provided such an example value can be obtained. This can of course mean extra work for your program, so it is up to you to decide which strategy to use. 

(NOTE: Below follows old rants)

The allowed types of the indices type may be subject to change in the future, but this restriction is so as to prevent dangerous behaviour of the program such as segmentation faults and random overwrites of memory. (NOTE: together with generics, this restriction can be cumbersome. Maybe relax it... or not. (NOTE NOTE: keep this probably -- in such cases, most of the time, you have available an example value of the required indice type, and can use that to form an array of repeated values instead. Not as fast, but a good compromise.))

### Solution for v0.3:

As for v0.3, the syntax is:

``` 
    <array expression no initialization> ::=
        '#[' ["unsafenothing"] ';' ']' ["noextramemory"]

```

You will actually can use `noextramemory` on all three types of array expression. 

But for custom allocators, I guess you need unsafe typecasts too... Maybe the cInterface will provide such functionality... otherwise don't bother. 

## Struct expressions

```
    struct_expression ::=
        identifier '{' (identifier '=' expression)* '}'
```

_Example:_

```
    monster{
        health_points = 100 
        score = total_score + 3 
        id = id
    }
```

This expression evaluates to a struct of the type specified by the provided "tag", the field identifiers, and the types of the expressions to the right of the `=` operators, taken together. Additionaly, information from the surrounding context is sometimes also used to infer the exact type of the struct.   

When the type of a field of the struct expression is deduced from the context as being of a variant-box type, and the corresponding expression for the field in the struct expression is of a type that is one of the type cases of the variant-box type, the expression's value will automatically be converted to a value of that variant-box type, which will have its _caseNr_ and _casevalue_ fields set correspondingly.

If this expression were a regular (built-in) function, the subexpressions defining the values of the fields would be considered 'construand' arguments. 

## Function call expressions

```
    prefix_function_call_expression ::=
        identifier_expression '(' [(prefix_function_call_arg ',')* prefix_function_call_arg] ')'               
        
    prefix_function_call_arg ::=
        [identifier "="] expression
        | "ref" [identifier "="] lvalue

    infix_function_call_expression ::=
        expression '`' identifier_expression '`' expression                              

```

_Examples:_

```
    reverse(my_array)
    parse(file = "test.cip")

    concat(["a", "b"], ["c", "d"])

    ["a", "b"] `concat` ["c", "d"]
    next_token()
    modify_something_and_calculate_some_result(3.14, ref bernie[32])
```

A function call expression will evaluate its argument expressions (in an evaluation order discussed in Chapter X), and then call a function (a built-in function or one defined by a function definition statement (see Chapter X)), and the function call expression evaluates to the return value of that function (the function called must have exactly one return value).

Any side-effects of the argument expressions, or of the called function, will be performed.

There is a "prefix notation", usable in the general case, and a less general "infix notation", for function calls. 

In the prefix notation, the identifier expression to the left (which should be of a function type) (also, this expression is considered part of the general procedure for evaluation order! (NOTE: maybe...)) is evaluated to a function, and that function is then called with the values of the expressions of the comma separated function call arguments between the parentheses, such that their values are assigned to the parameters (as defined in the called function's function definition) of the function called, in their respective order of appearance. 

In prefix notation, prefix function call arguments may be named with an identifier (followed by the token `=`) for clarity, which must then correspond to the name of the parameter as declared in the function definition header of the called function. That this is so is checked by the compiler when the expression to the left of the '`(`' is a simple identifier expression referring to a function definition (i.e. not, for example, when it refers to a slot holding a function type value), but not when the expression to the left of '`(`' is referring to a slot holding a function type value. In such other cases, one can say that giving the wrong name for a parameter is actually allowed. Also, observe that named parameters in Memtran currently do not allow for reordering of the arguments in the function call. They are just something that can be inserted for extra clarity.

In the infix notation, the identifier expression between the backticks is evaluated to a function, which function must have exactly two argument types, which is then called, with the values of the two expressions on the left and the right assigned to its two parameters. 

So, for example:


```
    a `concat` b
```

is equivalent to

``` 
    concat(a, b)
```

When a parameter of some called function is of a variant-box type, and the corresponding expression for the argument in the function call is of a type that is one of the type cases of the xorbox type, the expression's value will automatically be converted to the right variant-box type, which will have its _caseNr_ and _casevalue_ fields set correspondingly. This is not true for the lvalues of ref arguments (NOTE: or is it? NO).

### Ref arguments

Function call expression arguments can also consist of the keyword `ref`, followed by an "lvalue", possibly with a named parameter identifier and an `=` inbetween (the possibility of a named parameter exists only for prefix notation function call expressions). For an explanation of the ref argument system and lvalues, see Chapters X and X.


## Non-short-circuited prefix and infix operator expressions

```
    prefix_operator_expression ::=
        ('!' | '-') expression                     

    infix_operator_expression ::=
        expression ('==' | '!=' | '>' | '<' | '>=' | '<=' | '+' | '-' | '*' | '/' | '%') expression
        
```

These are built-in functions that have a special operator syntax. They can have different precedence than normal function calls. The `-` token can be both a prefix operator and an infix operator. The parser will interpret it as an infix operator wherever that is possible to do.

For precedence rules, see Chapter X. 

To use these built-in operators as function type values, you have to embed them in another function definition. This is currently true for all built-in functions, but that may, perhaps, change. 


## variant-box downcast expressions

```
    xorbox_downcast_expression ::=
        expression '...' type
```

The expression to the left of the `...` should evaluate into a xorbox type value. This returns the value of the _casevalue_ field of the xorbox type value, provided it is of the type specified. This will throw a runtime error if the cast did not succeed. If the `--recovermode` compiler flag is set, and the type casted to is one of nil, bool, u8, u16, u32, u64, uint, i8, i16, i32, i64, int, or struct types or variant-box types thereof, possibly recursively so, the expression will simply return a non-specified value of the relevant type. In the case of casting to other types, the program will always exit with an error message.

## `&&` expressions and `||` expressions

(NOTE: short-circuited)

## `end`

`end` is a (perhaps somewhat silly?) abbreviation that can be used within array indexing expressions and array indexing lvalues.

Example:

```
    my_long_array_name[end - 4] = my_other_long_array_name[end]
```

Expands to:

```
    my_long_array_name[(len(my_long_array_name) - 1) - 4] = my_other_long_array_name[(len(my_other_long_array_name) - 1)]
```

If there are nested array indexings, `end` will use the closest array evaluating expression in its expansion.

Example:

```
    my_long_array_name[struct.field[end]]
```

Expands to:

```
    my_long_array_name[struct.field[(len(struct.field) - 1)]]
``` 

`end` cannot be used outside an array indexing.

## IF expressions, SWITCH expressions, and CONTENTTYPE expressions

``` 
    IF_expression ::=
        "IF" expression '~' expression "ELSE" '~' expression      // note: this can be chained

    SWITCH_expression ::=
        "SWITCH" expression ("CASE" (expression ',')* expression '~' expression)* "DEFAULT" '~' expression

    CONTENTTYPE_expression ::=
        "CONTENTTYPE" expression ("CASE" (type ',')* type '~' expression)* "DEFAULT" '~' expression
``` 

These are syntactically thematic expression variants of the if statement, the switch statement, and the contenttype statement.

TODO: document these more carefully. 

Automatic downcasting in CONTENTTYPE CASE expressions is enabled whenever the CONTENTTYPE expression is a simple identifier expression.

PERFORMANCE NOTE: These expressions are not to be counted as built-in functions with a special syntax, but are rather special short-circuited expressions. That means that they are simply "branchers" between different expression evaluations. I.e. these expressions are not to be seen as args to params which are then returned as implementational owners, which could have meant extra copying. Also, implementationally, possible automatically generated destruction operations will respect possible different transfer depending on which branch is chosen.  

# Lvalues

```
    lvalue ::=
        lvalue_identifier_expression
        | lvalue_array_indexing
        | lvalue_struct_indexing
        | lvalue_xorbox_downcast
        | lvalue_type_clarification
        | parenthesized_lvalue    

    lvalue_identifier_expression ::=
        identifier_expression

    lvalue_array_indexing ::=
        lvalue '[' expression ']'

    lvalue_struct_indexing ::=
        lvalue '.' identifier

    lvalue_xorbox_downcast ::=
        lvalue '...' type

    lvalue_type_clarification ::=      
        lvalue "''" type

    parenthesized_lvalue ::=
        '(' lvalue ')'    

```

Lvalues are a class of syntactical constructions in Memtran programs, which are syntactically identical to a subset of expressions, but considered a distinct class of syntactical constructions, expected at certain syntactical positions where expressions in general are not allowed. Lvalues are used in assignment statements, ref arguments, and in the `over` construct of for statements. 

Lvalues can be thought of as being either slot names, or path descriptions into the subslots of a slot containing an array, a struct, or a xorbox type value. There is also the "lvalue_type_clarification" syntactic construction, although such type clarification should not be needed actually. Identifiers corresponding to a function name (global or local), or a type name, may not be used in lvalue identifier expressions. (I.e. not a function name per se -- but it _can_ be a name of a slot holding a function value.) 

You may put parentheses around your lvalues for clarity. They aren't really needed for disambiguation purposes, though.

# Statements and top-level structure

```
    program ::=
        import_statement* ordinary_statement*

    ordinary_statement ::=
        block
        | type_declaration_statement
        | assignment_statement 
        | function_call_statement 
        | function_declaration_statement 
        | return_statement 
        | contenttype_statement                                   
        | if_statement 
        | switch_statement
        | loop_statement                                                                    
        | for_statement
        | break_statement                                                                 
        | continue_statement
        | template_declaration_statement
```

Import statements will be covered in chapter X.

A Memtran program has no "main" function, but simply lists a number of statements in the order they should be evaluated (although type declarations and function declarations have some "atemporal" qualities to them, so to speak).

## Blocks

```
    block ::=
        ':' ordinary_statement* ';'
```

A block defines a scope (NOTE: Or how do you put it?). It contains a sequence of zero or more statements, and any functions, or variables (mutable or immutable), declared within the block are local to the block. A block can be a statement by itself (NOTE: this may change).

Functions _may_ be declared within a block. 

Currently, and expected to stay that way, types may _not_ be declared within a block, but only in the global scope. 

Names of functions, or variables (mutable or immutable), declared within a block may overshadow identifiers declared in any surrounding context. Identifiers declared within a block may not overshadow names of parameters, variables or alias names that the statement containing the block brings into the block, such as in function declarations with definitions, for statements, typeswitch statements or `over` statements. 

Any identifiers defined in any of the containing contexts may be used within a block, provided they are defined at a previous point in the program to where the block is located. Functions names may also in many cases be used before they are defined in the program. See chapter X. Type names declared later in the same file can also be used.  

Functions or variables (mutable or immutable) declared within a block may not be marked as `internal` (the `internal` specifier being a feature of the module system, see chapter X). Only global variables (mutable or immutable) and functions may be marked `internal`.

## Type declaration statements

```        
    type_declaration_statement ::=
        "type" identifier '=' type 
        | "type" identifier '(' (identifer ',')* identifier ')' '=' type   // parametrized type
```

_Examples:_

```
    type my_array = arr f32
    type parse_error = parse_error{}
``` 

The definition type (the type specified after the `=` token) of a type declaration and definition may contain identifiers (or module specified identifiers) being the names of types defined in a file imported by the current file, or types defined anywhere in the current file. (No forward declarations of types are necessary within a file. And it is currently not possible to forward declare types between files.)

Similarly, named types used in any other statement than a type declaration statement must have been declared somewhere in the current file, or in a file imported by the current file.  

Types may only be declared and defined in the global scope. Type declarations may (currently) not be marked as `internal`.

Recursive type declarations are allowed. For some kinds of recursive declarations though, it will be impossible to actually instantiate a value of the declared type. Declaring such types is currently allowed anyway, and not checked for. (IMPL. NOTE: TODO/DONE Make sure compiler passes or helper procedure code generation don't stall on such types.)

Note: During the design of the language, it was discovered that type identity for recursive types (as defined using named types declared in a type declaration statement), is somewhat problematic to calculate. Therefore, in the current implementation, you cannot assume that Memtran will understand whether two recursive types that would seem to have the same structure, are equivalent. This should probably not matter much in practice, but may be improved upon, or lead to changes, in future versions. 

Parametrized types are covered in chapter X, "Generics".

## Assignment statements and variable declarations

```
    assignment_statement ::=
        assignment_receiver '=' expression                                                   // "normal" assignment
        | (assignment_receiver ',')+ assignment_receiver '=' function_call_expression        // assigning multiple return values
        | compound_assignment_statement                                                      // i.e. using +=, -=, *=, /= or %= instead of = 

    assignment_receiver ::=
        variable_declaration
        | ["uninitialized"] lvalue

```

_Example:_

```
    mu a ' f32 = 1.7 // a mutable variable 'a' is declared and assigned a value
    
    a = 3.14 // reassignment of the variable

    a, internal mu d ' u8 = strangeFunction() // multiple return value assignment

    mu array ' arr f32 = [2.3, 4.5, 6.7] 

    array[2] = 0.1 // index assignment

    array2 ' arr f32 = array  // an immutable 'array2' variable is initialized to the whole of 'array'                              

```

An assignment statement puts the value of the expression to the right of the assignment operator `=`, into the mutable slot or mutable subslot specified by the _lvalue_, or the variable (mutable or immutable) specified by the _variable declaration_, to the left of the assignment operator. The thing to the left must agree with the expression to the right as to its type.

Alternatively, an assignment statement puts the multiple return values of a function call to the right of the assignment operator `=`, into the mutable slot or mutable subslot specified by the comma separated multiple lvalues, and/or variables (mutable or immutable) specified by the variable declarations, to the left of the assignment operator. In this case, the number of comma-separated things to the left must correspond to the number of return values of the function called. Also, the things to the left must agree with the return values of the function to the right as to their type and order. (NOTE: skriv motsvarande för funktionsanrop-argument i vederbörande kapitel)

### Variable declarations

```
    variable_declaration ::=
        ["mu" | "internal" | ("internal" "mu") | ("internal" "private")] identifier "'" type
     
```

A variable (mutable or immutable) may not be referred to previous in the program to where it has been declared and assigned to (variable declaration is always simultaneous with assignment in Memtran).  

### Lifetime of slots

The lifetime of a slot is for the length of the block (taking into consideration that each function call can be considered to create a unique instance of the corresponding function definition's body block) its definition belongs to, or, for slots defined in the global scope, for the lifetime of the program. When a slot's lifetime is up, the computer memory used by the slot is freed for repeated usage by the program. (But for some additional details, see Chapter X, i.e., for example, if its ownership has been transferred, "under the hood", nothing is freed at this point.) 

### Compound assignment statements

```
    compound_assignment_statement ::=
        lvalue ('+=' | '-=' | '*=' | '/=' | '%=') expression
        | (lvalue ',')+ lvalue ('+=' | '-=' | '*=' | '/=' | '%=') function_call_expression  // "multiple compound assignment" -- (NOTE: elaborate on exactly what this does...) 
```

These are known from other C-style syntax languages. I.e.:

```
    i += 3 
```

will add 3 to the value held in a mutable slot, or subslot of a mutable slot, represented by the lvalue `i`, "in-place," so to speak.

(NOTE: "Multiple compound assignment not yet implemented.")

## Function call statements

```
    function_call_statement ::=
        function_call_expression
```

This looks and functions just like a function call expression, except that the function called should have exactly zero return types.

## Function declaration statements and return statements

```
    function_declaration_statement ::=
        ["inline" | "internal" | ("inline" "internal") | ("internal" "inline")] "fn" identifier '(' [(param ',')* param] ')' ["'" (type ',')* type] block

    param ::=
        ref_param
        | normal_param

    ref_param ::=
        "ref" identifier "'" type          

    normal_param ::=
        ["mu" | "construand" | ("mu" "construand") | ("construand" "mu")] identifier "'" type
   
```

_Examples:_

```
    // Add examples here...
```

A non-ref function parameter is, for the purposes of Memtran, a slot (mutable or immutable) with the lifetime of the instance of its function definition's body block, that is assigned as its (initial, in the case of `mu` parameters) value an argument provided in the function call. The argument must agree with the parameter as to its type. 

As in most other modern languages, functions can call themselves recursively, directly or indirectly. When a function calls itself, a new function block can be considered to be stored on the stack for each iteration of the function. So, it is not the same block that is being reused, which would lead to overwrites of its variables/parameters. In some cases, such recursion may fill the whole stack memory, in which case X will occur. Currently, Memtran does not provide tail call optimization.

In the global scope, or in a block, a function _F_ that has not yet been declared, may not be called directly. But a second function _G_ may be declared in the same scope, which calls the not yet declared _F_, but then _G_ may not be called directly until after the _F_ has been declared. (NOTE: ändra detta och elaborera, när typecheck pass 1 implementeras.)

### Ref parameters

A ref parameter expects a slot or subslot as its lvalue function call argument, instead of an expression value. 

Example:

```
    fn set_to_3(ref x ' int) :
        x = 3
    ;

    mu a ' int = 5
    set_to_3(ref a)   // a is now 3
```

You can provide an arbitrary lvalue as argument to a ref parameter, i.e. letting it refer to a subslot of some slot. But the slot which is passed, or whose subslot is passed, has to be mutable. 

Another thing: please do not use ref parameters unless you intend to modify the slot or subslot represented by the argument lvalue (i.e. or subslots of it) at the caller site, i.e. don't use ref parameters just because you think it would be faster than using normal parameters, unless you have a very good reason for that, as that will make your program harder to understand, the `ref` argument marker at the corresponding function calls being intended to notify a reader of a program that your function will modify that argument. 

When the lvalue passed as a ref argument is a subslot of a global variable, and this variable has a value having implementationwise both a head, and things pointed to (and maybe for structs too, but NO), a "mutlock" flag is set for that variable. This hinders the program from modifying that variable through other means than through the ref parameter, for the duration of the function call.

The following is an example of how to invoke the mutlock, runtime:

```
    mu array ' arr f64 = [1.2, 3.4, 5.6]

    fn add3(ref array_index : f64) :
        array = []             // this line will throw a runtime error: variable is mutlocked
        array_index += 3.0   
    ;

    add3(ref array[1])
```

There is currently no way of recovering from a mutlock invocation error, so setting the `--recovermode` compiler flag does not change anything in this case. But this may perhaps be improved on in future versions. 

The above is also true for certain local variables. Below is some musing about that for the future. 

For local variables or parameters, the compiler will protest already at compile time if you will, or even might (the latter in the presence of branching constructs), violate an imagined runtime mutlock. Since it throws an compile time error for all possible such mutlock-invoking cases, the runtime will not actually need to set any mutlock for any local slots. 
  
NOTE: Dessa två är fallen:

```
// A

fn foo() {
    mu a : [mu] Int = #[1, 2, 3, 4, 5]

    fn bar(ref i : Int) {
        a = #[]
        i += 1
    }

    bar(ref a[3])
}


// B

fn foo2() {
    mu a : [mu] Int = #[1, 2, 3, 4, 5]

    fn bar2(ref i : Int) {
        baz()
        i += 1
    }

    fn baz() {
        a = #[]
    }

    bar2(ref a[3])
}

```

Så frågan är: tar baz() en implicit ref-parameter. Eller en implicit reference-type-value? Eller ska vi strunta i local functions? Svar: lokala funktioner som modifierar sin lokala omgivning tar en implicit reference-type-value-parameter. Dessa kollar alltid mutlock först.

Angående statisk analys: analysera för fall A, om det finns berörande fall, använd mutlock-flagging-checking, samt ge kompilator-användaren en warning. 

### Return statements

``` 
return_statement ::=
    "return" [(expression ',')* expression]
```

Return statements can only be used inside a function definition's body block, not in the global scope, or in block statements used in the global scope (NOTE: but we could possibly define such usage as equivalent to calling an exit() function. But probably not desirable!!!). The number of return expressions must be equivalent to the number of return types of the containing function definition. Since semicolons are optional, giving the wrong number of return expressions (which is somewhat similar to forgetting to declare the return type(s) of a declared function!) will confuse the parser and hence give rise to somewhat cryptic parse errors.

The types of the return expressions must agree with the return types of the containing function definition.

The compiler will also check function definitions for missing return statements -- the rule being that it must be able to prove, using a specific basic proving algorithm, that a function with more than zero return types will return (a) value(s) of that/those type(s), with an explicit return statement -- for all branching possibilities. 



## Contenttype statements

```
    contenttype_statement ::=
        "contenttype" expression ("case" (type ',')* type block)+ ["default" block]
        | "contenttype" expression "default" block
```

_Example:_

```
    mu my_variant_box ' arr u8 / nil / bool / int 
        = "The value is of arr u8 type!\n"

    contenttype my_variant_box case arr u8 :
   
        print_utf8(my_variant_box)       // "my_variant_box" can here be treated as casted into arr u8 (i.e. the "raw string type", so to speak)
        my_variant_box = "Previous string was printed.\n"

    ; case nil :

        print_utf8("It's nil!\n")

    ; default :

        print_utf8("Default case.\n")

    ;
```

Contenttype statements let you check the actual type case of an variant-box type value's contents, that variant-box type value being the value of the expression at the beginning of the contenttype statement, and choose different execution paths depending on its type case. A `default` case can be inserted into the contenttype statement after the normal contentype statement cases, whose block will be the path of execution provided none of the above type cases match the variant-box type's type case. (Actually, it will expand to all the missing cases.)

As a comfortability feature, if the expression at the beginning of the contenttype statement consists of an _identifier expression_, then within a given typeswitch case, that identifier expression will be considered as an alias for its xorbox type value casted into the type after the keyword `case` of that typeswitch case. This alias can be used in lvalues or expressions. It will overshadow the meaning of that identifier expression as outside the typeswitch statement.  If the expression at the beginning of the typeswitch statement is any other expression than an identifier expression, you will have to xorbox cast it explicitly in order to access its type case value, even within a typeswitch statement case of that type case. 

For the comfortability feature of previous paragraph to be safe, when the relevant identifier expression refers to a global variable, or to certain local slots, mutlock is set on that slot for the execution duration of the relevant type case block, for mutation through other means than using the identifier within that block. Also, you can _only_ refer to it as downcasted within such a block. 

The comfortability feature might be expanded to work for lvalues in general, in the future. Or not. No, because array indexing may not give the same values for repeated occurrences.   

(NOTE: module specified identifier contra identifier, considered equal... or you may not refer to it both ways depending on how you imported it - YES)

The compiler will require that all the possible cases of a variant-box type are represented in a contenttype statement. Usage tip: If you want the compiler to tell you when a new type case has been added to a variant-box type, so you can add new handling code for that case, you should _not_ use a default case in your contenttype statements on that type. Use a default case only when there is a reasonable default thing to do (possibly nothing at all).

(((The compiler does currently _not_ require that all the possible type cases of an xorbox type are represented in a typeswitch statement, but this may change. In the case none of the cases match, execution resumes at the point after the typeswitch statement. (NOTE: return statements - maybe require this anyway... no, check it, and require a return statement afterwards otherwise, just like with an if statement. v0.1 that is.))))

## If statements

```
    if_statement ::=
        "if" expression block                                                                   // simple
        | "if" expression block "else" block                                                    // full
        | "if" expression block "else" if_statement                                             // nested
```

_Example_:

```
    if 9 > 4 :
        go_bananas()
    ; else if true :
        go_cucumbers()
    ; else :
        remain_silent()
        print_all_files()
    ;

```

Parentheses around the test expression are optional. 

## Loop statements

```
    loop_statement ::=
        "loop" ["label" identifier] block
```

An infinite loop. Use a break statement or a return statement to break out of the loop, or a continue statement to go to the next cycle of the loop. A label can optionally be provided.

## For statements

```
    for_statement ::=
        "for" ["label" identifier] variable_range block
        | "for" ["label" identifier] [variable_range ','] (array_iteration ',')* array_iteration block

    variable_range ::=
        identifier "'" type '=' expression ("to" | "downto") expression

    array_iteration ::=
        identifier ["'" type] "over" lvalue ["indexfactor" expression] ["indexoffset" expression]
        | identifier ["'" type] "in" expression ["indexfactor" expression] ["indexoffset" expression]
```

_Examples:_

```
    mu array ' arr f64 = [trash 200]

    for it over array :
        it = random() * 100.0
    ;

    mu array1 ' arr int = [1, 2, 3, 4, 5, 6, 7]
    array2 ' arr int = [8, 9, 10, 11, 12, 13, 14]

    for i ' int = 4 to len(array2) - 1,
        it over array1 indexoffset -3,
        jt in array2 
    :
        it = jt                    
    ;

    // array1 is now [1, 12, 13, 14, 5, 6, 7]
```

A for loop in Memtran iterates a finite number of times. An index variable (currently allowed types: int) can be provided into the for loop, whose value, for consecutive iterations of the for loop, will be set along a range of numbers given through a starting number and an end number (inclusive). Additionally, or alternatively, a number of arrays to be iterated through can be specified in the for loop, using either a construct with the keyword `over` or a construct with the keyword `in`.

The thinking behind the Memtran for loop is that it should be constructed so as to allow the compiler to optimize away array bounds checking to some extent (or rather do them just once in the for loop head). This might not boost performance more than marginally actually, but writing the loop heads has been found to be sort of stimulating, a bit like Sudoku. But the for statement is sufficiently flexible that you can write in a more traditional way too, with just a variable range, and explicit array indexings inside the loop body. 

If no range is provided, the range is from 0 to `len` - 1 (inclusive) of the first array iterated through. And the implicit type of the implicit range variable is `int`. In that case, no indexfactor or indexoffset may be given for the first array iteration.    

The `over` construct should be used with arrays where you intend to modify (some or all of) their indices within the for loop. This construct will mutlock the slot holding the array, or whose subslot holds the array, against modification through other means than through the "iteration alias", for the duration of the for loop. (The rules are (sort of) the same as for ref arguments/parameters). The identifier defines an alias that can be used both as an lvalue and as an expression within the for loop block, for referring to the current iterated through index of the array in question.

The `in` construct should be used with arrays where you don't intend to modify any of their indices within the for loop. The identifier provided defines a variable (immutable for the duration of each iteration) that can be used as an expression within the for loop block, for referring to the current iterated through index of the array in questions. It should be the same type as the indice type of the array value to which the expression to the right of the keyword "in", evaluates.

Expressions in a for loop head are only evaluated once, prior to the the repeated execution of the for loop block.

Break statements, continue statements and return statements may be used within the for loop block, having the expected effects on the execution of the for loop.

A label for the for loop may optionally be declared, to be used with break statements and continue statements.

Explicit type declaration for the alias/variable of the `over` and `in` constructs is optional in principle, but in certain cases that it cannot figure out, the compiler will tell you that it is needed. 

### Using for loops with container objects in general (i.e. abstracted types that the user or standard library will declare) (NOTE: for v0.2)

The plan is:

```
    it over container_object

    // where the container_object lvalue is of any type of the pattern container_type(t) 
    // will require the interface:

    fn boundscheck(c ' container_type(t), index ' int) ' bool
    fn get_index(c ' container_type(t), index ' int) ' t
    fn set_index(ref c ' container_type(t), index ' int, new_value ' t)

``` 

So it will only can work with containers with "random access". For other cases, you will have to use a custom `loop` statement...

Type declaring the iteration variable explicitly will probably be required quite often by the compiler.  

## Break statements

```
    break_statement ::=
        "break" ["label" identifier] 
```

## Continue statements

```
    continue_statement ::=
        "continue" ["label" identifier] 
```


# Operations that set the _rlock_ flag on copy-on-write values

(NOTE: Out-of-date but kept here until further)

Runtime setting of the _rlock_ flag on copy-on-write values, together with internal copying of their _content_ part if their _content_ part's _refcount_ > 1, are performed by for statement `over` construct (on the array lvalue, for the duration of the for loop), the `over` statement (on the struct lvalue, for its duration), and `ref` parameters (on their argument lvalue, for the duration of the function). The lock prevents wholesale modification of the value, and also prevents operations that increase the _refcount_ of the value. 

What this means might be a bit hard to develop an intuition about. In practice, it means mostly that using the associated slot name (or subslot defining expression) as an expression is not possible, with the big exception that expressions referring to a subvalue of the locked value are still allowed under such a lock.

Or should it be allowed, but with copying. Probably. 

modlock behöver inte en egen memory slot, kan vara flags på rlock. modlock sätts av ref argument function calls, for the duration of the function call, på alla överliggande copy-on-write memory structures. 

0 : no lock

1 : rlock

2 : modlock

3 : rlock + modlock

så

```
array1 : [] [] Int = #[#[1 2 3], #[4, 5, 6]]

array2 : [] [] Int = array1 // structure sharing with array1

fn strangeFunction(ref integer : Int) {
    array1[0] = #[]
    integer = 25
}

strangeFunction(ref array2[0][1])  // sätter modlock för de överliggande på lvalue:t -- detta går alltid att luska ut runtime, även för referenser
                                   // samt skickar en pekare
                        
                                   // rad 1 i strangeFunction måste separera då modlock är satt på array1[0] memory area. Men hur högt måste separationen gå? 
                                   // SVAR: Ända upp, vi börjar att söka efter modlock överst i strukturen. GOOD!!! 


array1[0] = #[1, 2, 3] // resetting array1[0]

array2 = array1

strangeFunction(ref array1[0][1]) // runtime error på första raden i strangeFunction -- "array is modlocked"

``` 

Om vi ska kunna sätta någe modlock måste vi separera. SVAR: Vi sätter modlock på alla överliggande. Om modlock är satt måste refcount-increasing or modifying operations separera först. GOOD!!!!!!!

Hur vet man om modlock ska leda till runtime error eller separation? 

If refcount > 1, separera. ? Så första raden i strangeFunction i första anropet encounters an array with modlock and refcount == 2. 

Steg 1. Separera översta:

```
    array1 ---> refcount: 1 [o, o]
                             |  \---------------------------------
                             v                                   v
                            refcount: 2 [1, 2, 3] modlocked      refcount: 2 [4, 5, 6]
                             ^                                   ^
                             |   /--------------------------------
    array2 ---> refcount: 1 [o, o] modlocked           

Steg 2. Funkar inte. Modlock måste sitta på pekaren/sloten. 


```

Alltså vad vi vill göra är att eliminate structure sharing lokalt. Så separera lokalt. Vid anropet av strangeFunction:

```
Steg 0.

array1 ----> refcount: 2 [o, o]
          ----^           |  \--------> refcount: 1 [4, 5, 6]
         /                v
array2 -/                 refcount: 1 [1, 2, 3]

```

Vi måste separera ända upp som första steg. Vilket är önskat, då ref-parametrar ska användas endast vid modifikation. Så sätt rlock och separera. Sätt sedan modlock på översta cow-värde. Skicka sedan en pekare.   


# Precedence rules

Operations with precedence (having a preceding, i.e. lesser number, in the below lists) are evaluated first, or "bind tighter," so to speak.

## Precedence order for types

1. function types, struct types, parentheses
2. Parametrized types with their argument lists                 (NOTE: Must this be a separate level? I don't remember my thinking here...)
3. Array type constructions.  
4. The variant-box type constructor `/`. This infix operator does not associate, but rather several variant-box type constructors on the same "evaluation order level" construct one single variant-box type. 

## Precedence order for expressions

1. These prefix expressions: parentheses, array expression, struct expression, prefix function call, module specified identifier expression with `..`, IF expressions, SWITCH expressions, CONTENTTYPE expressions. 
2. Postfix operations: struct indexing dot notation; the brackets of an array indexing. The constructions `'' <type>`, and `... <type>`, are also considered as postfix operations on par with these.  
3. These prefix operations: `! -`
4. These infix operations: `* / %`
5. These infix operations: `+ -`
6. Infix function calls using backticks
7. These infix operations: `< > <= >= != ==`
8. These infix operations: `&& ||`     

Given equal precedence, all expression infix operations associate to the left. 


# Overloaded functions and type inference

Due to syntactically implicit xorbox type upcasting, if the context where the expression is found does not provide further information, any expression that could be of type _T_ could in principle as well be of any xorbox type having _T_ as one of its type cases. But type inference will always prefer to infer _T_ in these cases -- i.e. unless something in the context necessitates inferring an xorbox type. (NOTE: This is sort of wrongly described. Or not.) 

Two functions defined with the same name (and in the same context/namespace (NOTE: unclear/erratic description)) must differ in their argument type list. They cannot differ only in their return types. 

Functions can be overloaded on ref arg versus normal arg. On the other hand, when it comes to `mu` arg, versus `construand` arg, versus `mu construand` arg, versus normal arg without any such annotations, whereas such param annotations _do_ affect function type identity, they cannot be overloaded on, since they are not specified in function call syntax.  

In the case where two functions with the same name are defined, such that they differ only in one of their argument types, in the way that that argument type is a type _A_ for the first function, and an xorbox type _A_ `\` _B_ for the second function, the compiler will resolve a call to the function with an argument of type _A_ so that the second function (with the xorbox type argument) is called. This is supposed to be somewhat useful for the technique exemplified in "extensible_animals.cip" in the examples folder. (NOTE: This may definitely change.)

You may even overload a function name like this: 

```
    fn myFunction(A \ B) {...}
    fn myFunction(A \ C) {...}

``` 

But in that case, if you then proceed to call one of those functions with an argument of type _A_, the compiler will protest. 

Well, basically actually, currently function overloading is in a sense maximalistic, in that the compiler will not protest any declared over-overloaded function signatures per se, but will only complain when it cannot resolve an actual function call.   

If the arguments to a call to an overloaded function contain integer literals or floating point number literals, the exact types for those literals will be guessed by the compiler in the order specified in Chapter X "Number literals", combinatorially for all ambiguous arguments, until a matching function is found. 

So, for a function call with two integer literal arguments, the compiler will make the following guesses for the integer literals, in order:

```
    Int, Int
    Int, UInt
    Int, I64
    Int, U64
    Int, I32
    Int, U32
    Int, I16
    Int, U16
    Int, I8
    Int, U8
    UInt, Int
    UInt, UInt
    UInt, I64
    etc.
```

(NOTE: Order given should be changed in both chapters, to something like: Int, I64, I32, I16, I8, UInt, U64, U32, U16, U8.) 

But this is only in case the type signature of the function cannot be found out "the other way around", i.e. starting from the root of the expression containing the function call (as part of an assignment statement or an argument passing), or from a type clarified expression surrounding the function call at some level of the expression containing it.

If the arguments to an overloaded function are array expressions, the current compiler will, in a few cases, ask you to specify the exact type of those expressions by embedding them in a type clarified statement, even in some cases where a type deduction would be theoretically possible. 

# Generics

For now, this is what we have:

## Parametrized types

The identifier before the parentheses of a parametrized type name may not clash with the name of a named non-parametrized type. All the parameter names must be different, and be used somewhere in the definition of the type. No overloading of type names is allowed. (NOTE: The last statement belongs somewhere else in the manual.)

It is currently only possible to parametrize over types, not over other things that make up types, such as struct tags or struct fields. But this may change. Or, alternatively, those properties of the type system may have to go. Or something else. 

The built in composite types can be considered as parametrized on the composing types that are in their definition, in that order. See the sorting function in the next subchapter. 

## Function templates

Function template definitions are currently only allowed in the global scope. (NOTE: though we will see about that soon...)

The compiler will compile different implementations for every call of the function template that has a distinct argument type signature. Such individual implementations can also be referred to as function type values. (NOTE: hard to implement?) (NOTE 2: you will often need a type clarification) 

If a function template is defined in a program or module, but not called with some concrete type arguments, it will only be parsed by the compiler, and partially semantically validated, but not completely semantically validated.

You may overload function template names (possibly mixed with regular functions overloading the same name). But there may happen clashes when instantiating them, which will make the compiler complain at that point. 

A template may call functions not yet defined in the module it is in. In order to give a hint about how to write rather abstract code in Memtran, below is given as example an implementation of insertion sort for any sequence type. Note that an interface consisting of a number of required functions on the types S(T) and T are specified in a comment, and these function names are then "forward called".

```
    /** This template forward requires the following interface for the types S(T) and T:
        fn greaterThan(a : T, b : T => Bool)
        fn getIndex(arr : S(T), index : Int => T)
        fn setIndex(ref arr : S(T), index : Int, elem : T)
        fn size(arr : S(T) => Int)
    */
    fn(S, T) seqInsertionSort(ref seq : S(T)) {               
        
        for i : Int = 1 to size(seq) - 1 {
            mu j : Int = i
            loop {
                if !((j > 0) && (getIndex(seq, j - 1) `greaterThan?` getIndex(seq, j))) {
                    break                                 
                }
                temp : T = getIndex(seq, j)
                setIndex(ref seq, j getIndex(seq, j - 1))
                setIndex(ref seq, j - 1, temp)
                j -= 1
            }
        }
    }

    /* ----- using the template function (typically in another file) --------- */

    // Note that this would be more useful (provided you find things like this useful at all) for some other, more complex, abstracted type, than for the 
    // regular dynamic array used here.

    fn greaterThan(a : F32, b : F32 => Bool) {
        return a > b
    }

    fn getIndex(array : [] F32, index : Int => F32) {
        return array[index]
    }

    fn setIndex(ref array : [] F32, index : Int, element : F32) {
        array[index] = element
    }

    fn size(array : [] F32 => UInt) {
        return array len
    }

    mu myArray : [] F32 = #[1.2, 7.8, 4.5, 3.4, 6.8, 2.3, 0.2, 5.5, 3.3, 2.8]

    seqInsertionSort(ref myArray)
    
``` 

Mostly for the reason of avoiding scary-looking notation, function template forward calls are not marked-out syntactically, but the compiler will simply mark function calls inside a function template, as forward called, whenever they aren't defined as per the module the function template is in. The gotcha is that if you have defined a private function with a matching type signature, that function will be preferred to a forward call. (In the case you have defined a non-private matching function, the same thing happens, but at least there will be name conflict when the user of the module is trying to define a function of the same signature.) 

Further, things like using parametrized xorbox types as the types of the function parameters of a function template may sometime create problems:

```
fn(A, B) test(foo : A \ B) {
    typeswitch foo case A {
        printUTF8("Apple")
    } case B {
        printUTF8("Banana")
    }
}

bar : [] F64 = #[1.2]

test(bar) // compiler will say stop, I don't know which xorbox type it is supposed to be
```



### Type name capture

Since types may currently only be declared in the global scope, may not be prefiximported, and may not be private to a module, type name capture in function templates should not be possible. 



# The `construand` keyword

The "construand" keyword is strictly for optimization purposes. 

Using "construand" together with "mu" makes no difference implementationwise, but, for completeness, it can still be provided in such cases, if you wish so. Also, and perhaps more importantly, "construand" does only make an implementational difference when used with parameters that are of array type, or whose type contains array types. 

You should or may use this keyword when the value held by the parameter is used simply in construction of a data structure that has that value as a constituting part, which in other terms means either:

1. The value held by the parameter is passed on to another function as a "construand" argument
2. The value is used as a subvalue of an array expression or a struct expression 
3. The value is given to an "implicit xorbox conversion" (i.e. that which happens when you assign a value of type A to a slot of type A | B).

It is allowed to use a construand parameter in construction twice or more times. TEST THIS OUT. Implementationwise, `construand` is just a signal to the compiler that the parameter should own the memory it points to. And this in turn sometimes enables ownership transfer to such a parameter. 

It would probably be possible for the compiler to do a global optimization pass in order to find out the information provided by the "construand" keyword, but since we would like separate compilation to be simple and fast, this optimization keyword must be provided manually by the programmer. 

 





# Implementation of Memtran's assign-by-value and pass-by-value/pass-by-reference semantics -- tables

Please see the document "cimmpl_memory_management_details.txt" in the "src" directory.


# Module system

```
    module_specified_identifier ::=
        identifier "::" identifier
```

Compiling a ".cim" module file produces both an object file, and a ".scim" file, which latter is more or less an automatically generated header file. It is the ".scim" file that should be named in an import/prefiximport statement, in order to import the module, not the ".cim" file.  

(NOTE: module specified identifier contra identifier, considered equal... or you may not refer to it both ways depending on how you imported it - YES)

There is import and prefiximport, that's it. See previous statement too. Types declared in a prefiximported module file are never prefiximported though, but always imported directly. 

If you want to know the type definition of an imported type (and you don't have access to its definition source code), abstracted or not, try to alias it to any type with `as`, and the compiler will print an error message telling you the type definition, or let it pass, in which latter case your guess was right. (This paragraph is out of date.)   

# Local functions

Local functions are permitted. In addition to being able to access global variables and functions, local functions can also access local slots that are defined (above them), and functions that are defined, within any containing block. But note that Memtran environments are not true closures, as per the Lisp tradition. Take the following Scheme example:

```
(define (test) 
    (let ((counter 0))
        (lambda () (inc! counter) (print counter))))

(let ((counter-function (test)))
    (counter-function)      ; prints 1
    (counter-function)      ; prints 2
    (counter-function))     ; prints 3

``` 
(NOTE: check the details of this Scheme example with an actual Scheme implementation!)
 
Doing a similar thing in Memtran will trigger a compile time error:

```
fn test(=> Fn()) {
    mu counter : Int = 0
    fn incAndPrint() {
        counter += 1
        print(counter)
    }
    return incAndPrint  // disallowed by the compiler
}

counterFunction : Fn() = test()
counterFunction()        
counterFunction()
counterFunction()

```   

Local functions can be used as an aid to structured programming, and also for certain kinds of event handling and similar. But several aspects of their implementation make them slower than global functions, so be aware of that. If you just want to restrict access to certain functions, you can use the `private` functionality of the module system. 

# Evaluation order

Somewhat unusually, evaluation order of the expressions inside Memtran statements, is defined like this:

Let the _level_ of a function call expression (in the sense, here, of expressions having explicit (prefix or infix) function call syntax -- operator expressions are not included!), inside a Memtran statement, be equal to  
         
* n + 1 if it is part of a non-function-call-expression argument to a function call expression of level n
* 1 otherwise

Then the evaluation order for the expressions in the statement is as follows:
        
For levels m downto 1, where m is the highest found level within the statement, first all function calls of the level are evaluated, in an _unspecified_ order; then all other expressions needed to supply function calls of level level-1 with arguments, are evaluated. 

So evaluation order in Memtran is defined (although with some undefined aspects to it) "per statement", not "per expression". 

The evaluation order procedure is like it is for technical reasons of implementation, so as to avoid segmentation errors and the like, i.e. due to premeditated sharing of resources that are subsequently modified by side-effecting function call expressions evaluated. 

Note: expressions inside other statements inside a block forming part of a statement, do not participate in the evaluation procedure discussed here. 

# Future extensions

## C interoperability

cInterface::CChar
cInterface::CUChar
cInterface::CShort
cInterface::CUShort
cInterface::CInt
cInterface::CUInt
cInterface::CLong
cInterface::CULong
cInterface::CLongLong
cInterface::CULongLong
cInterface::CFloat
cInterface::CDouble
cInterface::CLongDouble

fn toCChar(I8) => CChar
fn toCUChar(U8) => CUChar
fn toCShort(I16) => CShort
etc. 
fn(T) arrayToCPointer(ref [?] T) => CVoidPointer // e.d. 



Use separation statements. (NOTE: We will see about that!) 

New musings:

```
"clibrary.cim":

csignature addToDatabase(construand str : [] U8, Int length, Int totalMem)



"clibrary.h":

#if
    (lång typdefinitions-fixning för olika arkitekturer)
#endif


void addToDatabase(CimmplU8Ptr str, CimmplInt length, CimmplInt totalMem) {         


}
``` 


## Concurrency

It is speculated that Software Transactional Memory would be a nice fit for Memtran, for the following reasons:

* Due to the pass-by-value, assign-by-value semantics, there wouldn't be a problem with "leakage" of data between slots designated as part of the Software Transactional Memory scheme, and slots not thus designated.
* The semantics of so called "atomic" code blocks together with usage of exception handling facilities seems to be a hard nut to handle in a clean way. But Memtran has no exception handling, using multiple return values for most error handling.
* (NOTE: more?)

But we will see about such things, and it is all for the remote future.

## Switch statement

# Built-in functions

(NOTE: work in progress)

Below will be given function signatures for the built-in functions as if they were functions defined in Memtran itself. 

## Array functions

```
fn(T) addLast(ref array : [] T, construand element : T)
fn(T) addLast(construand array : [] T, construand element : T => [] T)      // Functional variant
fn(T) append(ref array : [] T, array2 : [] T)                               // (NOTE: array2 is not construand, and should not...)
fn(T) append(construand array : [] T, array2 : [] T)                        // Functional variant 
fn(T) len(array : [] T => Int)
fn(T) removeLast(ref array : [] T, numberOfElementsToRemove : Int)    /* simply removes all elements if len(array) < numberOfElementsToRemove;
                                                                        simply removes nothing if numberOfElementsToRemove is <= 0    */
fn(T) removeLast(construand array : [] T, numberOfElementsToRemove : Int => [] T)   // Functional variant
                                                                       
```

## Conversion

```
fn toF32(f : F64 => F32)
fn toF32(i : I8 => F32)                 // NOT YET IMPLEMENTED
fn toF32(i : I16 => F32)                // NOT YET IMPLEMENTED
fn toF32(i : I32 => F32)                // NOT YET IMPLEMENTED
fn toF32(i : I64 => F32)                // NOT YET IMPLEMENTED
fn toF32(i : Int => F32)
fn toF32(u : U8 => F32)
fn toF32(u : U16 => F32)                // NOT YET IMPLEMENTED
fn toF32(u : U32 => F32)                // NOT YET IMPLEMENTED
fn toF32(u : U64 => F32)                // NOT YET IMPLEMENTED
fn toF32(u : UInt => F32)               // NOT YET IMPLEMENTED
fn toF64(f : F32 => F64)
fn toF64(i : I8 => F64)                 // NOT YET IMPLEMENTED
fn toF64(i : I16 => F64)                // NOT YET IMPLEMENTED
fn toF64(i : I32 => F64)                // NOT YET IMPLEMENTED    
fn toF64(i : I64 => F64)                // NOT YET IMPLEMENTED
fn toF64(i : Int => F64)
fn toF64(u : U8 => F64)                 
fn toF64(u : U16 => F64)                // NOT YET IMPLEMENTED
fn toF64(u : U32 => F64)                // NOT YET IMPLEMENTED
fn toF64(u : U64 => F64)                // NOT YET IMPLEMENTED
fn toF64(u : UInt => F64)               // NOT YET IMPLEMENTED
fn toI8(u : U8 => I8, Bool)             // NOT YET IMPLEMENTED
fn toI8(u : U16 => I8, Bool)            // NOT YET IMPLEMENTED
fn toI8(u : U32 => I8, Bool)            // NOT YET IMPLEMENTED
fn toI8(u : U64 => I8, Bool)            // NOT YET IMPLEMENTED
fn toI8(u : UInt => I8, Bool)           // NOT YET IMPLEMENTED
fn toI8(i : I16 => I8, Bool)            // NOT YET IMPLEMENTED
fn toI8(i : I32 => I8, Bool)            // NOT YET IMPLEMENTED
fn toI8(i : I64 => I8, Bool)            // NOT YET IMPLEMENTED
fn toI8(i : Int => I8, Bool)            // NOT YET IMPLEMENTED
fn toI16(u : U8 => I16)                 // NOT YET IMPLEMENTED
fn toI16(u : U16 => I16, Bool)          // NOT YET IMPLEMENTED
fn toI16(u : U32 => I16, Bool)          // NOT YET IMPLEMENTED
fn toI16(u : U64 => I16, Bool)          // NOT YET IMPLEMENTED    
fn toI16(u : UInt => I16, Bool)         // NOT YET IMPLEMENTED
fn toI16(i : I8 => I16)                 // NOT YET IMPLEMENTED
fn toI16(i : I32 => I16, Bool)          // NOT YET IMPLEMENTED
fn toI16(i : I64 => I16, Bool)          // NOT YET IMPLEMENTED
fn toI16(i : Int => I16, Bool)          // NOT YET IMPLEMENTED    
fn toI32(u : U8 => I32)                 // NOT YET IMPLEMENTED
fn toI32(u : U16 => I32)                // NOT YET IMPLEMENTED
fn toI32(u : U32 => I32, Bool)          // NOT YET IMPLEMENTED
fn toI32(u : U64 => I32, Bool)          // NOT YET IMPLEMENTED
fn toI32(u : UInt => I32, Bool)         // NOT YET IMPLEMENTED
fn toI32(i : I8 => I32)                 // NOT YET IMPLEMENTED
fn toI32(i : I16 => I32)                // NOT YET IMPLEMENTED
fn toI32(i : I64 => I32, Bool)          // NOT YET IMPLEMENTED    
fn toI32(i : Int => I32, Bool)          // NOT YET IMPLEMENTED
fn toI64(u : U8 => I64)                 // NOT YET IMPLEMENTED
fn toI64(u : U16 => I64)                // NOT YET IMPLEMENTED
fn toI64(u : U32 => I64)                // NOT YET IMPLEMENTED
fn toI64(u : U64 => I64, Bool)          // NOT YET IMPLEMENTED    
fn toI64(u : UInt => I64, Bool)         // NOT YET IMPLEMENTED
fn toI64(i : I8 => I64)                 // NOT YET IMPLEMENTED
fn toI64(i : I16 => I64)                // NOT YET IMPLEMENTED
fn toI64(i : I32 => I64)                // NOT YET IMPLEMENTED    
fn toI64(i : Int => I64, Bool)          // NOT YET IMPLEMENTED
fn toInt(u : U8 => Int, Bool)
fn toInt(u : U16 => Int, Bool)          // NOT YET IMPLEMENTED
fn toInt(u : U32 => Int, Bool)          // NOT YET IMPLEMENTED
fn toInt(u : U64 => Int, Bool)          // NOT YET IMPLEMENTED
fn toInt(u : UInt => Int, Bool)         // NOT YET IMPLEMENTED
fn toInt(i : I8 => Int, Bool)           // NOT YET IMPLEMENTED
fn toInt(i : I16 => Int, Bool)          // NOT YET IMPLEMENTED
fn toInt(i : I32 => Int, Bool)          // NOT YET IMPLEMENTED
fn toInt(i : I64 => Int, Bool)          // NOT YET IMPLEMENTED
fn toU8(u : U16 => U8, Bool)            // NOT YET IMPLEMENTED
fn toU8(u : U32 => U8, Bool)            // NOT YET IMPLEMENTED
fn toU8(u : U64 => U8, Bool)            // NOT YET IMPLEMENTED
fn toU8(u : UInt => U8, Bool)           // NOT YET IMPLEMENTED
fn toU8(i : I8 => U8, Bool)             // NOT YET IMPLEMENTED
fn toU8(i : I16 => U8, Bool)            // NOT YET IMPLEMENTED
fn toU8(i : I32 => U8, Bool)            // NOT YET IMPLEMENTED    
fn toU8(i : I64 => U8, Bool)            // NOT YET IMPLEMENTED    
fn toU8(i : Int => U8, Bool)    
fn toU16(u : U8 => U16)                 // NOT YET IMPLEMENTED
fn toU16(u : U32 => U16, Bool)          // NOT YET IMPLEMENTED
fn toU16(u : U64 => U16, Bool)          // NOT YET IMPLEMENTED
fn toU16(u : UInt => U16, Bool)         // NOT YET IMPLEMENTED
fn toU16(i : I8 => U16, Bool)           // NOT YET IMPLEMENTED
fn toU16(i : I16 => U16, Bool)          // NOT YET IMPLEMENTED
fn toU16(i : I32 => U16, Bool)          // NOT YET IMPLEMENTED
fn toU16(i : I64 => U16, Bool)          // NOT YET IMPLEMENTED    
fn toU16(i : Int => U16, Bool)          // NOT YET IMPLEMENTED
fn toU32(u : U8 => U32)                 // NOT YET IMPLEMENTED
fn toU32(u : U16 => U32)                // NOT YET IMPLEMENTED
fn toU32(u : U64 => U32, Bool)          // NOT YET IMPLEMENTED
fn toU32(u : UInt => U32, Bool)         // NOT YET IMPLEMENTED
fn toU32(i : I8 => U32, Bool)           // NOT YET IMPLEMENTED
fn toU32(i : I16 => U32, Bool)          // NOT YET IMPLEMENTED
fn toU32(i : I32 => U32, Bool)          // NOT YET IMPLEMENTED
fn toU32(i : I64 => U32, Bool)          // NOT YET IMPLEMENTED
fn toU32(i : Int => U32, Bool)          // NOT YET IMPLEMENTED
fn toU64(u : U8 => U64)                 // NOT YET IMPLEMENTED
fn toU64(u : U16 => U64)                // NOT YET IMPLEMENTED
fn toU64(u : U32 => U64)                // NOT YET IMPLEMENTED
fn toU64(u : Uint => U64, Bool)         // NOT YET IMPLEMENTED
fn toU64(i : I8 => U64, Bool)           // NOT YET IMPLEMENTED
fn toU64(i : I16 => U64, Bool)          // NOT YET IMPLEMENTED
fn toU64(i : I32 => U64, Bool)          // NOT YET IMPLEMENTED
fn toU64(i : I64 => U64, Bool)          // NOT YET IMPLEMENTED
fn toU64(i : Int => U64, Bool)          // NOT YET IMPLEMENTED
fn toUInt(u : U8 => UInt, Bool)         // NOT YET IMPLEMENTED
fn toUInt(u : U16 => UInt, Bool)        // NOT YET IMPLEMENTED    
fn toUInt(u : U32 => UInt, Bool)        // NOT YET IMPLEMENTED    
fn toUInt(u : U64 => UInt, Bool)        // NOT YET IMPLEMENTED    
fn toUInt(i : I8 => UInt, Bool)         // NOT YET IMPLEMENTED
fn toUInt(i : I16 => UInt, Bool)        // NOT YET IMPLEMENTED
fn toUInt(i : I32 => UInt, Bool)        // NOT YET IMPLEMENTED    
fn toUInt(i : I64 => UInt, Bool)        // NOT YET IMPLEMENTED
fn toUInt(i : Int => UInt, Bool)        // NOT YET IMPLEMENTED
```

## Language error handling

```
fn runtimeLanguageErrorStatus(=> Int)         // Can be used when the '--recovermode' compilerflag is set. Reports the last occurred language error: 
                                              //    0 -- No errors
                                              //    1 -- Array indexing expression index out of bonds
                                              //    2 -- for loop head array index out of bonds  
                                              //    3 -- Mutlock invoked         (Mutlock invocation is always fatal, though, in this version, so this will never be reported.)
                                              //    4 -- Repeated value array expression of desired length < 0
                                              //    5 -- Array expression with no initialization of desired length < 0
                                              //    6 -- Xorbox downcast failure
                                              //    7 -- assignment lvalue array indexing out of bonds
                                              //    8 -- assignment lvalue xorbox downcast failure
                                              //    9 -- for loop "over" construct lvalue array indexing out of bonds
                                              //   10 -- for loop "over" construct lvalue xorbox downcast failure
                                              //   11 -- ref argument lvalue array indexing out of bonds             (FATAL? try it out...)
                                              //   12 -- ref argument lvalue xorbox downcast failure                 (FATAL? try it out...)
                                              //   13 -- slimmed conversion function conversion failure (for v0.2) NOT FITTING HERE
                                              // The act of calling this function will reset the status to 0 -- No errors. 
```

## Memory information

```
fn availableMemory(=> Int)
fn totalMemory(=> Int)
fn usedMemory(=> Int)
``` 

## Printing to standard output

```
fn print(n : Nil) 
fn print(b : Bool)          // move to stdlib later, but needed initially (before we have byte arrays)
fn print(i : I8)            // NOT YET IMPLEMENTED
fn print(i : I16)           // NOT YET IMPLEMENTED
fn print(i : I32)           // NOT YET IMPLEMENTED
fn print(i : I64)           // NOT YET IMPLEMENTED
fn print(i : Int)
fn print(u : U8)            
fn print(u : U16)           // NOT YET IMPLEMENTED
fn print(u : U32)           // NOT YET IMPLEMENTED
fn print(u : U64)           // NOT YET IMPLEMENTED
fn print(u : UInt)          // NOT YET IMPLEMENTED
fn print(f : F32)
fn print(f : F64)
fn printLn()
```

## Other

```
fn getArgs(=> [] [] U8)

fn printASCIIChar(c : U8)   // this will be moved to the "ascii.cim" standard library as soon as the C interface is completed
fn printUTF8Internal(str : [] U8)  // this will be moved to the "utf8.cim" standard library as soon as the C interface is completed
```

# Standard library

(NOTE: work in progress)

## array.cim

```
fn(T) reverse(array : [] T => [] T)
fn(T) reverse(ref array : [] T)
fn(T) slice(array : [] T, startInclusive : Int, endExclusive : Int => [] T)
fn(T) setSlice(ref array : [] T, start : Int, values : [] T)
fn(T) print(array : [] T)                                                   // forward-calls this informal interface: fn print(something : T)

``` 

## ascii.cim

```
fn equalsASCII(str1 : [] U8, str2 : [] U8 => Bool)
fn printASCII(str : [] U8)
fn promptASCII(=> [] U8)
fn toIntASCII(str : [] U8 => Int, Bool)
fn toF64ASCII(str : [] U8 => F64, Bool)
fn toASCII(i : Int => [] U8)
fn toASCII(f : F64 => [] U8)  
```

## random.cim
 
```
fn random(=> F64)        // Observe that this pseudo-random number generator is super-simplistic at the moment 
                         // and should not be used for anything serious. Also, there is no randomize functionality...
``` 

## utf8.cim

```
fn equalsUTF8(str1 : [] U8, str2 : [] U8 => Bool)
fn printUTF8(str : [] U8)
fn promptUTF8(=> [] U8)
fn substringUTF8(str : [] U8, startInclusive : Int, endExclusive : Int => [] U8) 
fn toIntUTF8(str : [] U8 => Int, Bool)
fn toF64UTF8(str : [] U8 => F64, Bool)
``` 

## util.cim

```
inline fn(T) swap(ref a : T, ref b : T) 
```











