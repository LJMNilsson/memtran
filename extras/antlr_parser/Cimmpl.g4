// Copyright (C) 2017 Martin Nilsson


// This file is part of the Memtran compiler.
//
//     The Memtran compiler is free software: you can redistribute it and/or modify
//     it under the terms of the GNU General Public License as published by
//     the Free Software Foundation, either version 3 of the License, or
//     (at your option) any later version.
// 
//     The Memtran compiler is distributed in the hope that it will be useful,
//     but WITHOUT ANY WARRANTY; without even the implied warranty of
//     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//     GNU General Public License for more details.
// 
//     You should have received a copy of the GNU General Public License
//     along with the Memtran compiler.  If not, see http://www.gnu.org/licenses/ . 


// Define a grammar called Cimmpl

// Note: this syntax is quite out of date, but should give an idea about the parsing procedure

grammar Cimmpl;

options {
    language = Java;
    
}

IF : 'if';
ELSE : 'else';
LOOP : 'loop';
BREAK : 'break';
CONTINUE : 'continue';
FOR : 'for';
TO : 'to';
STEP : 'step';
OVER : 'over';
IN : 'in';
OFFSET : 'offset';
FACTOR : 'factor';
RETURN : 'return';
MU : 'mu';
REF : 'ref';
INLINE : 'inline';
TYPESWITCH : 'typeswitch';
SWITCH : 'switch';
CASE : 'case';
DEFAULT : 'default';
TRUE : 'true';
FALSE : 'false';
NIL : 'nil';
FN : 'fn';
END : 'end';
AS : 'as';
IMPORT : 'import';
PREFIXIMPORT : 'prefiximport';
PRIVATE : 'private';
CONSTRUAND : 'construand';
UNSAFENOTHING : 'unsafenothing';
ABSTRACTED : 'abstracted';
TYPE : 'type';
LABEL : 'label';
FNTYPE : 'Fn';
NILTYPE : 'Nil';
BOOLTYPE : 'Bool';
I8 : 'I8';
I16 : 'I16';
I32 : 'I32';
I64 : 'I64';
INT : 'Int';
U8 : 'U8';
U16 : 'U16';
U32 : 'U32';
U64 : 'U64';
UINT : 'UInt';
F32 : 'F32';
F64 : 'F64';
INTEGERLITERAL : '-'? [0-9]+ ;
FLOATLITERAL : ('-'? [0-9]+ PERIOD [0-9]*) | ('-'? [0-9]* PERIOD [0-9]+) ;
STRING : '"' ( '\\"' | . )*? '"' ;
TRIPLECOLON : ':::';
LONGRARROW : '==>';
SQUARELSQUAREBRACKET : '#[';
DOUBLECOLON : '::';
SHORTRARROW : '->';
ORSYMBOL : '||';
ANDSYMBOL : '&&';
MODULOASSIGNMENTOPERATOR : '%=';
MULTIPLICATIONASSIGNMENTOPERATOR : '*=';
ADDITIONASSIGNMENTOPERATOR : '+=';
DIVISIONASSIGNMENTOPERATOR : '/=';
SUBTRACTIONASSIGNMENTOPERATOR : '-=';
GREATERTHANOREQUALS : '>=';
LESSTHANOREQUALS : '<=';
EQUALS : '==';
EQUALSNOT : '!=';
LSQUAREBRACKET : '[';
RSQUAREBRACKET : ']';
LPAREN : '(';
RPAREN : ')';
LBRACE : '{';
RBRACE : '}';
COLON : ':';
COMMA : ',';
SEMICOLON : ';';
MODULO : '%';
MULTIPLICATION : '*';
DIVISION : '/';
ADDITION : '+';
MINUS : '-';
ASSIGNMENTOPERATOR : '=';
GREATERTHAN : '>';
LESSTHAN : '<';
NOT : '!';
SQUARE : '#';
PERIOD : '.';
BACKTICK : '`';
TYPEOR : '|';
SINGLEQUOTE : '\'';
IDENTIFIER : ~('[' | ']' | '(' | ')' | '{' | '}' | ':' | ',' | ';' | '%' | '*' | '/' | '+' | '-' | '=' | '>' | '<' | '!' | '#' | '.' | '`' | '|' | '\'' | [0-9 \t\r\n]) (~('[' | ']' | '(' | ')' | '{' | '}' | ':' | ',' | ';' | '%' | '*' | '/' | '+' | '-' | '=' | '>' | '<' | '!' | '#' | '.' | '`' | '|' | '\'' | [ \t\r\n]))* ;
LINECOMMENT : '//' ~[\r\n]* '\r'? '\n' -> skip ;
MULTILINECOMMENT : '/*' .*? (MULTILINECOMMENT? .*?)*? '*/' -> skip ;
WS : [ \t\r\n]+ -> skip ; // skip spaces, tabs, newlines

program : (importStatement SEMICOLON*?)* (topLevelStatement SEMICOLON*?)* ;

importStatement : normalImportStatement
                  | prefixImportStatement
                  ;

normalImportStatement : IMPORT STRING ;
prefixImportStatement : PREFIXIMPORT STRING ;

topLevelStatement :
    typeDeclarationStatement
    | functionTemplateDeclarationStatement
    | voidStatement
    ;

voidStatement : 
    voidBlock
    | assignmentStatement
    | functionDeclarationStatement
    | voidReturnStatement
    | voidSwitchStatement
    | voidTypeswitchStatement
    | voidIfStatement
    | voidLoopStatement 
    | voidForStatement
    | breakStatement
    | continueStatement
    ;

possiblyNonvoidStatement : 
    possiblyNonvoidBlock
    | assignmentStatement
    | functionDeclarationStatement
    | nonvoidReturnStatement
    | possiblyNonvoidSwitchStatement
    | possiblyNonvoidTypeswitchStatement
    | possiblyNonvoidIfStatement
    | possiblyNonvoidLoopStatement 
    | possiblyNonvoidForStatement
    | breakStatement
    | continueStatement
    ;

typeDeclarationStatement : ABSTRACTED? TYPE IDENTIFIER (LPAREN IDENTIFIER (COMMA IDENTIFIER)* RPAREN)? ASSIGNMENTOPERATOR type ;

functionTemplateDeclarationStatement :
    functionTemplateDeclarationStatementReturnVoid
    | functionTemplateDeclarationStatementReturnNonvoid
    ;

functionTemplateDeclarationStatementReturnVoid : 
    PRIVATE? INLINE? FN LPAREN (IDENTIFIER (COMMA IDENTIFIER)*)? RPAREN IDENTIFIER LPAREN params RPAREN voidBlock 
    INLINE PRIVATE FN LPAREN (IDENTIFIER (COMMA IDENTIFIER)*)? RPAREN IDENTIFIER LPAREN params RPAREN voidBlock 
    ;

functionTemplateDeclarationStatementReturnNonvoid : 
    PRIVATE? INLINE? FN LPAREN (IDENTIFIER (COMMA IDENTIFIER)*)? RPAREN IDENTIFIER LPAREN params returnTypes RPAREN possiblyNonvoidBlock 
    INLINE PRIVATE FN LPAREN (IDENTIFIER (COMMA IDENTIFIER)*)? RPAREN IDENTIFIER LPAREN params returnTypes RPAREN possiblyNonvoidBlock 
    ;




voidBlock : LBRACE (voidStatement SEMICOLON*?)* RBRACE ;
possiblyNonvoidBlock : LBRACE (possiblyNonvoidStatement SEMICOLON*?)* RBRACE ;




assignmentStatement :  
    variableDeclarationOrLValue (COMMA variableDeclarationOrLValue)* 
    (ASSIGNMENTOPERATOR | MODULOASSIGNMENTOPERATOR | MULTIPLICATIONASSIGNMENTOPERATOR | DIVISIONASSIGNMENTOPERATOR | ADDITIONASSIGNMENTOPERATOR | SUBTRACTIONASSIGNMENTOPERATOR)
    expr
    ;

variableDeclarationOrLValue :
    variableDeclaration 
    | lValue
    ;

variableDeclaration : MU? PRIVATE? IDENTIFIER COLON type
                      | PRIVATE MU IDENTIFIER COLON type
                      ;

lValue : identifierExpr
        |<assoc=left> lValue structIndexing
        |<assoc=left> lValue arrayIndexing
        |<assoc=left> lValue aliasing
        |<assoc=left> lValue ortypeCast
        ;

functionDeclarationStatement :
    functionDeclarationStatementReturnVoid
    functionDeclarationStatementReturnNonvoid
    ;

functionDeclarationStatementReturnVoid : 
    PRIVATE? INLINE? FN IDENTIFIER LPAREN params RPAREN voidBlock 
    | INLINE PRIVATE FN IDENTIFIER LPAREN params RPAREN voidBlock
    ;

functionDeclarationStatementReturnNonvoid : 
    PRIVATE? INLINE? FN IDENTIFIER LPAREN params returnTypes RPAREN possiblyNonvoidBlock
    INLINE PRIVATE FN IDENTIFIER LPAREN params returnTypes RPAREN possiblyNonvoidBlock
    ;

params : param (COMMA param)* ;

param : normalParam 
        | refParam
        ;

normalParam : CONSTRUAND? MU? IDENTIFIER COLON type
              | MU CONSTRUAND IDENTIFIER COLON type
              ;

refParam : REF IDENTIFIER COLON type ;



voidReturnStatement : RETURN ;    // this parsing detail is the reason for the void/possiblyNonvoid system
nonvoidReturnStatement : RETURN expr (COMMA expr)* ;



voidSwitchStatement : 
    SWITCH expr (CASE INTEGERLITERAL voidBlock)+ (DEFAULT voidBlock)?
    | SWITCH expr (CASE INTEGERLITERAL voidBlock)* DEFAULT voidBlock
    ;

possiblyNonvoidSwitchStatement :
    SWITCH expr (CASE INTEGERLITERAL possiblyNonvoidBlock)+ (DEFAULT possiblyNonvoidBlock)?
    | SWITCH expr (CASE INTEGERLITERAL possiblyNonvoidBlock)* DEFAULT possiblyNonvoidBlock
    ;


voidTypeswitchStatement : 
    TYPESWITCH expr (CASE type voidBlock)+ (DEFAULT voidBlock)?
    | TYPESWITCH expr (CASE type voidBlock)* DEFAULT voidBlock
    ;

possiblyNonvoidTypeswitchStatement :
    TYPESWITCH expr (CASE type possiblyNonvoidBlock)+ (DEFAULT possiblyNonvoidBlock)?
    | TYPESWITCH expr (CASE type possiblyNonvoidBlock)* DEFAULT possiblyNonvoidBlock
    ;


voidIfStatement : IF expr voidBlock (ELSE IF expr voidBlock)* (ELSE voidBlock)? ;
possiblyNonvoidIfStatement : IF expr possiblyNonvoidBlock (ELSE IF expr possiblyNonvoidBlock)* (ELSE possiblyNonvoidBlock)? ;    



voidLoopStatement : LOOP (LABEL IDENTIFIER)? voidBlock ;
possiblyNonvoidLoopStatement : LOOP (LABEL IDENTIFIER)? possiblyNonvoidBlock ;



voidForStatement : forHead voidBlock ;
possiblyNonvoidForStatement : forHead possiblyNonvoidBlock ;

forHead : FOR (LABEL IDENTIFIER)? variableRange 
          | FOR (LABEL IDENTIFIER)? (variableRange COMMA)? iteration (COMMA iteration)*     
          ; 

variableRange : IDENTIFIER COLON type ASSIGNMENTOPERATOR expr TO expr (STEP expr)? ;

iteration : IDENTIFIER (COLON type)? OVER lValue (FACTOR expr)? (OFFSET expr)?
            | IDENTIFIER (COLON type)? OVER lValue OFFSET expr FACTOR expr
            IDENTIFIER (COLON type)? IN expr (FACTOR expr)? (OFFSET expr)?
            IDENTIFIER (COLON type)? IN expr OFFSET expr FACTOR expr
            ;


breakStatement : BREAK (LABEL IDENTIFIER)? ;

continueStatement : CONTINUE (LABEL IDENTIFIER)? ;





expr7 : | NIL
        | TRUE
        | FALSE
        | INTEGERLITERAL 
        | FLOATLITERAL
        | STRING
        | arrayExpr
        | structExpr
        | identifierExpr
        | END
        | LPAREN expr RPAREN
        ;

expr6 : <assoc=left> expr6 structIndexing
        |<assoc=left> expr6 arrayIndexing
        |<assoc=left> expr6 aliasing
        |<assoc=left> expr6 ortypeCast
        |<assoc=left> expr6 prefixFunctionCall
        |<assoc=left> expr6 typeClarification
        | expr7
        ; 

expr5 : notOpExpr
        | minusPrefixOpExpr
        | expr6
        ;

expr4 : <assoc=left> expr4 multiplicationOpExpr
        |<assoc=left> expr4 divisionOpExpr
        |<assoc=left> expr4 moduloOpExpr
        | expr5
        ;

expr3 : <assoc=left> expr3 additionOpExpr
        |<assoc=left> expr3 subtractionOpExpr
        | expr4
        ;

expr2 : <assoc=left> expr2 infixFunctionExpr
        | expr3
        ;

expr :  <assoc=left> expr lessThanOpExpr
        |<assoc=left> expr greaterThanOpExpr
        |<assoc=left> expr lessThanOrEqualsOpExpr
        |<assoc=left> expr greaterThanOrEqualsOpExpr
        |<assoc=left> expr equalsNotOpExpr
        |<assoc=left> expr equalsOpExpr
        |<assoc=left> expr andOpExpr
        |<assoc=left> expr orOpExpr
        | expr2
        ;

arrayExpr : arrayExprIndividualValues
            | arrayExprRepeatedValue
            | arrayExprNoInitialization
            | arrayExprUnsafeNothing
            ;




structExpr : SQUARE structTypeTag LBRACE structExprField* RBRACE ;

structExprField : IDENTIFIER ASSIGNMENTOPERATOR expr SEMICOLON? ;

arrayExprIndividualValues : SQUARELSQUAREBRACKET expr (COMMA expr)* RSQUAREBRACKET ;
arrayExprRepeatedValue : SQUARELSQUAREBRACKET expr SEMICOLON expr RSQUAREBRACKET ;
arrayExprNoInitialization : SQUARELSQUAREBRACKET SEMICOLON expr RSQUAREBRACKET ;
arrayExprUnsafeNothing : SQUARELSQUAREBRACKET UNSAFENOTHING SEMICOLON expr RSQUAREBRACKET ;


typeClarification : TRIPLECOLON type ;

prefixFunctionCall : LPAREN arg (COMMA arg)* RPAREN ;

arg : refArg 
      | normalArg
      ;

normalArg : expr ;
refArg : REF expr ;

structIndexing : PERIOD IDENTIFIER ;
arrayIndexing :  LSQUAREBRACKET expr RSQUAREBRACKET ;
ortypeCast :  LONGRARROW type ;
aliasing :  AS type ;

notOpExpr : NOT expr5 ;
minusPrefixOpExpr : MINUS expr5 ; // test this!

multiplicationOpExpr :  MULTIPLICATION expr5 ;
divisionOpExpr :  DIVISION expr5 ;
moduloOpExpr :  MODULO expr5 ;

additionOpExpr :  ADDITION expr4 ;
subtractionOpExpr :  MINUS expr4 ;

infixFunctionExpr :  BACKTICK identifierExpr BACKTICK expr3 ;

lessThanOpExpr :  LESSTHAN expr2 ;
greaterThanOpExpr :  GREATERTHAN expr2 ;
lessThanOrEqualsOpExpr :  LESSTHANOREQUALS expr2 ;
greaterThanOrEqualsOpExpr :  GREATERTHANOREQUALS expr2 ;
equalsNotOpExpr :  EQUALSNOT expr2 ;
equalsOpExpr :  EQUALS expr2 ;
andOpExpr :  ANDSYMBOL expr2 ;
orOpExpr :  ORSYMBOL expr2 ;

type : type2
       | ortype
       ;

type2 : LPAREN type RPAREN
       | NILTYPE 
       | BOOLTYPE
       | I8
       | I16
       | I32
       | I64
       | INT
       | U8
       | U16 
       | U32
       | U64
       | UINT
       | F32
       | F64
       | arrayType
       | structType
       | functionType
       | identifierExpr
       | parametrizedType
       ;




arrayType : LSQUAREBRACKET RSQUAREBRACKET type ;

structType : structTypeTag LBRACE structTypeField* RBRACE ;

structTypeTag : SINGLEQUOTE IDENTIFIER SINGLEQUOTE ;

structTypeField : IDENTIFIER COLON type SEMICOLON? ;

ortype : type2 (TYPEOR type2)* ;

functionType : FNTYPE LPAREN functionTypeArgs? returnTypes? RPAREN ;

returnTypes : SHORTRARROW type (COMMA type)* ;

functionTypeArgs : functionTypeArg (COMMA functionTypeArg)* ;

functionTypeArg : normalTypeArg
                  | refTypeArg
                  ;

normalTypeArg : type ;

refTypeArg : REF type ;

identifierExpr : IDENTIFIER 
                 | moduleSpecifiedIdentifier
                 ;

moduleSpecifiedIdentifier : IDENTIFIER COLON IDENTIFIER ;

parametrizedType : identifierExpr LPAREN type (COMMA type)* RPAREN ;




