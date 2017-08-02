# Copyright (C) 2017 Martin Nilsson


# This file is part of the Memtran compiler.
#
#     The Memtran compiler is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
# 
#     The Memtran compiler is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
# 
#     You should have received a copy of the GNU General Public License
#     along with the Memtran compiler.  If not, see http://www.gnu.org/licenses/ . 


def enum(*sequential, **named):                                         # for Python 2.7 compatibility, I guess
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

Tok = enum(
    'EOF',                    #      
    'LCURLYBRACKET',          #    
    'RCURLYBRACKET',          #
    'LSQUAREBRACKET',         #
    'RSQUAREBRACKET',         #
    'LPAREN',                 # 
    'RPAREN',                 # 
    'COLON',                  # 
    'SEMICOLON',              # 
    'PERIOD',                 # 
    'COMMA',                  # 
    'STRING',                 # 
    'IF',                     #
    'ELSE',                   #
    'FOR',                    #
    'IN',                     # 
    'OVER',                   # 
    'RETURN',                 # 
    'INDEXOFFSET',            # 
    'INDEXFACTOR',            # 
    'LOOP',                   # 
    'MUT',                    # 
    'REF',                    # 
    'INLINE',                 # 
    'TO',                     # 
    'ASSIGNMENTOPERATOR',         # 
    'CASE',                       # 
    'DEFAULT',                    # 
    'ANDSYMBOL',                  # 
    'ORSYMBOL',                   # 
    'TRUE',                       # 
    'FALSE',                      # 
    'FUN',                        # 
    'END',                        #  
    'IMPORT',                     # 
    'INTERNAL',                   # 
    'TYPE',                       # 
    'LABEL',                      # 
    'IDENTIFIER',                 # 
    'INTEGER',                    # 
    'FLOAT',                      # 
    'NILTYPE',                    # 
    'BOOL',                       # 
    'I8',                         # 
    'I16',                        # 
    'I32',                        # 
    'I64',                        # 
    'ISIZE',                      # 
    'U8',                         # 
    'U16',                        # 
    'U32',                        # 
    'U64',                        # 
    'USIZE',                      # 
    'F32',                        # 
    'F64',                        # 
    'PERCENT',        # 
    'STAR',           # 
    'PLUS',           # 
    'SLASH',          # 
    'MINUS',          #  
    'LESSTHAN',        # 
    'GREATERTHAN',     # 
    'EXCLAMATION',     #  
    'BACKTICK',       # 
    'PERCENTASSIGNMENTOPERATOR', # 
    'STARASSIGNMENTOPERATOR',    # 
    'PLUSASSIGNMENTOPERATOR',     # 
    'SLASHASSIGNMENTOPERATOR',   # 
    'MINUSASSIGNMENTOPERATOR',    # 
    'LESSTHANOREQUALS',            # 
    'GREATERTHANOREQUALS',         # 
    'EQUALS',                     # 
    'EQUALSNOT',                  # 
    'BREAK',                      # 
    'CONTINUE',                   #  
    'SINGLEQUOTE',                # 
    'TRIPLECOLON',                #
    'CONTENTTYPE',                 #
    'PREFIXIMPORT',               #
    'CONSTRUAND',
    'DOWNTO',
    'REPEAT',
    'TRASH',
    'UNINITIALIZED',
    'IFUPPERCASE',
    'ELSEUPPERCASE',
    'SWITCHUPPERCASE',
    'CONTENTTYPEUPPERCASE',
    'CASEUPPERCASE',
    'DEFAULTUPPERCASE',
    'SWITCH',
    'BACKSLASH',
    'DOUBLEPERIOD',
    'TRIPLEPERIOD',
    'DOUBLESINGLEQUOTE',
    'ARR',
    'TILDE',
    'VBOX',
    'ERRATIC'
) 


class Token:
   
    # public long lineNr;
    # public long rowNr;
    # public Tok kind;
    # public String tokString; 

    def __init__(self, lineNr, rowNr, kind, tokString):
        self.lineNr = lineNr
        self.rowNr = rowNr
        self.kind = kind
        self.tokString = tokString
    

    # def __init__(self, toBeCopied):
    #    self.lineNr = toBeCopied.lineNr
    #    self.rowNr = toBeCopied.rowNr
    #    self.kind = toBeCopied.kind
    #    self.tokString = toBeCopied.tokString
    



    def print_it(self):         # for testing purposes
        if self.kind == Tok.EOF:
            print("EOF", end='')
        elif self.kind == Tok.LCURLYBRACKET:
            print("{", end='')
        elif self.kind == Tok.RCURLYBRACKET:
            print("}", end='')
        elif self.kind == Tok.LSQUAREBRACKET:
            print("[", end='')
        elif self.kind == Tok.RSQUAREBRACKET:
            print("]", end='')
        elif self.kind == Tok.LPAREN:
            print("(", end='')
        elif self.kind == Tok.RPAREN:
            print(")", end='')
        elif self.kind == Tok.COLON: 
            print(":", end='')
        elif self.kind == Tok.SEMICOLON:
            print(";", end='')
        elif self.kind == Tok.PERIOD: 
            print(".", end='')
        elif self.kind == Tok.COMMA:
            print(",", end='')
        elif self.kind == Tok.STRING:
            print("\"" + self.tokString + "\"", end='') # will print newlines and cr:s and escape chars in a funny way though
        elif self.kind == Tok.IF:
            print("if", end='')
        elif self.kind == Tok.ELSE:
            print("else", end='')
        elif self.kind == Tok.FOR:
            print("for", end='')
        elif self.kind == Tok.IN:
            print("in", end='')
        elif self.kind == Tok.OVER:
            print("over", end='')
        elif self.kind == Tok.RETURN:
            print("return", end='')
        elif self.kind == Tok.INDEXOFFSET:
            print("indexoffset", end='')
        elif self.kind == Tok.INDEXFACTOR:
            print("indexfactor", end='')
        elif self.kind == Tok.LOOP:
            print("loop", end='')
        elif self.kind == Tok.MUT:
            print("mu", end='')
        elif self.kind == Tok.REF:
            print("ref", end='')
        elif self.kind == Tok.INLINE:
            print("inline", end='')
        elif self.kind == Tok.TO:
            print("to", end='')
        elif self.kind == Tok.ASSIGNMENTOPERATOR:
            print("=", end='')
        elif self.kind == Tok.CASE:
            print("case", end='')
        elif self.kind == Tok.DEFAULT:
            print("default", end='')
        elif self.kind == Tok.ANDSYMBOL:
            print("&&", end='')  
        elif self.kind == Tok.ORSYMBOL:
            print("||", end='')
        elif self.kind == Tok.TRUE:
            print("true", end='')
        elif self.kind == Tok.FALSE:
            print("false", end='')
        elif self.kind == Tok.FUN:
            print("fn", end='')
        elif self.kind == Tok.END:
            print("end", end='')
        elif self.kind == Tok.IMPORT:
            print("import", end='')
        elif self.kind == Tok.INTERNAL:
            print("internal", end='')
        elif self.kind == Tok.TYPE:
            print("type", end='')
        elif self.kind == Tok.LABEL:
            print("label", end='')
        elif self.kind == Tok.IDENTIFIER:
            print("$" + self.tokString, end='')
        elif self.kind == Tok.INTEGER:
            print("#" + self.tokString, end='')
        elif self.kind == Tok.FLOAT:
            print("##" + self.tokString, end='')
        elif self.kind == Tok.NILTYPE:
            print("nil", end='')
        elif self.kind == Tok.BOOL:
            print("bool", end='')
        elif self.kind == Tok.I8:
            print("i8", end='')
        elif self.kind == Tok.I16:
            print("i16", end='')
        elif self.kind == Tok.I32:
            print("i32", end='')
        elif self.kind == Tok.I64:
            print("i64", end='')
        elif self.kind == Tok.ISIZE:
            print("int", end='')
        elif self.kind == Tok.U8:
            print("u8", end='')
        elif self.kind == Tok.U16:
            print("u16", end='')
        elif self.kind == Tok.U32:
            print("u32", end='')
        elif self.kind == Tok.U64:
            print("u64", end='')
        elif self.kind == Tok.USIZE:
            print("uint", end='')       
        elif self.kind == Tok.F32:
            print("f32", end='')
        elif self.kind == Tok.F64:
            print("f64", end='')
        elif self.kind == Tok.PERCENT:
            print("%", end='')
        elif self.kind == Tok.STAR:
            print("*", end='')   
        elif self.kind == Tok.PLUS:
            print("+", end='')
        elif self.kind == Tok.SLASH:
            print("/", end='')
        elif self.kind == Tok.MINUS:
            print("-", end='')
        elif self.kind == Tok.LESSTHAN:
            print("<", end='')
        elif self.kind == Tok.GREATERTHAN:
            print(">", end='')
        elif self.kind == Tok.EXCLAMATION:
            print("!", end='')
        elif self.kind == Tok.BACKTICK: 
            print("`", end='')
        elif self.kind == Tok.PERCENTASSIGNMENTOPERATOR:
            print("%=", end='')
        elif self.kind == Tok.STARASSIGNMENTOPERATOR:
            print("*=", end='')
        elif self.kind == Tok.PLUSASSIGNMENTOPERATOR:
            print("+=", end='')
        elif self.kind == Tok.SLASHASSIGNMENTOPERATOR:
            print("/=", end='')
        elif self.kind == Tok.MINUSASSIGNMENTOPERATOR:
            print("-=", end='')
        elif self.kind == Tok.LESSTHANOREQUALS:
            print("<=", end='')
        elif self.kind == Tok.GREATERTHANOREQUALS:
            print(">=", end='')
        elif self.kind == Tok.EQUALS:
            print("==", end='')
        elif self.kind == Tok.EQUALSNOT:
            print("!=", end='')
        elif self.kind == Tok.BREAK:
            print("break", end='')
        elif self.kind == Tok.CONTINUE:
            print("continue", end='')
        elif self.kind == Tok.SINGLEQUOTE:
            print("'", end='')
        elif self.kind == Tok.TRIPLECOLON:
            print(":::", end='')
        elif self.kind == Tok.CONTENTTYPE:
            print("storetype", end='')
        elif self.kind == Tok.PREFIXIMPORT:
            print("prefiximport", end='')
        elif self.kind == Tok.CONSTRUAND:
            print("construand", end='') 
        elif self.kind == Tok.DOWNTO:
            print("downto", end='') 
        elif self.kind == Tok.REPEAT:
            print("repeat", end='')
        elif self.kind == Tok.TRASH:
            print("trash", end='')
        elif self.kind == Tok.UNINITIALIZED:
            print("uninitialized", end='');
        elif self.kind == Tok.IFUPPERCASE:
            print("IF", end='') 
        elif self.kind == Tok.ELSEUPPERCASE:
            print("ELSE", end='')
        elif self.kind == Tok.SWITCHUPPERCASE:
            print("SWITCH", end='')
        elif self.kind == Tok.CONTENTTYPEUPPERCASE:
            print("STORETYPE", end='')
        elif self.kind == Tok.CASEUPPERCASE:
            print("CASE", end='') 
        elif self.kind == Tok.DEFAULTUPPERCASE:
            print("DEFAULT", end='')
        elif self.kind == Tok.SWITCH:
            print("switch", end='')
        elif self.kind == Tok.BACKSLASH:
            print("\\", end='')
        elif self.kind == Tok.DOUBLEPERIOD:
            print("..", end='')
        elif self.kind == Tok.TRIPLEPERIOD:
            print("...", end='')
        elif self.kind == Tok.DOUBLESINGLEQUOTE:
            print("''", end='')
        elif self.kind == Tok.ARR:
            print("arr", end='')
        elif self.kind == Tok.TILDE:
            print("~", end='')
        elif self.kind == Tok.VBOX:
            print("vbox", end='')
        elif self.kind == Tok.ERRATIC:
            print("ERRATIC", end='')
        else:
            print("Token not found. Should not happen.");

