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



import io
from tokens import *
import util



_CHAREMPTY = ''  # utf-8 is default encoding in Python 3.4, which we want
_CHARLINEBREAK = '\n'
_CHAR0 = '0'
_CHAR1 = '1'
_CHAR2 = '2'
_CHAR3 = '3'
_CHAR4 = '4'
_CHAR5 = '5'
_CHAR6 = '6'
_CHAR7 = '7' 
_CHAR8 = '8' 
_CHAR9 = '9'
_CHARSPACE = ' '
_CHARLCURLYBRACKET = '{'
_CHARRCURLYBRACKET = '}'
_CHARLSQUAREBRACKET = '['
_CHARRSQUAREBRACKET = ']'
_CHARLPAREN = '('
_CHARRPAREN = ')'
_CHARCOLON = ':'
_CHARSEMICOLON = ';'
_CHARPERIOD = '.'
_CHARCOMMA = ','
_CHARPERCENT = '%'
_CHARSTAR = '*'
_CHARPLUS = '+'
_CHARSLASH = '/'
_CHARMINUS = '-'
_CHAREQUALS = '='
_CHARLESSTHAN = '<'
_CHARGREATERTHAN = '>'
_CHAREXCLAMATION = '!'
_CHARET = '&'
_CHARBACKSLASH = '\\'
_CHARBACKTICK = '`'
_CHARVERTICAL = '|'
_CHARSINGLEQUOTE = '\''
_CHARDOUBLEQUOTE = '\"'
_CHARTILDE = '~'


_CHARN = 'n'
_CHARESCAPEN = '\n'
_CHART = 't'
_CHARESCAPET = '\t'
_CHARB = 'b'
_CHARESCAPEB = '\b'
_CHARR = 'r'
_CHARESCAPER = '\r'
_CHARF = 'f'
_CHARESCAPEF = '\f'
_CHARESCAPE0 = '\0'


_currLineNr = 1
_currRowNr = 1

_currentChar = _CHAREMPTY    
_nextPeekChar = _CHAREMPTY

_charPtrIsAtStartOfFile = True  

def _next_char(f):
    global _currLineNr
    global _currRowNr
    global _currentChar
    global _nextPeekChar
    global _charPtrIsAtStartOfFile

    if _charPtrIsAtStartOfFile:
        _charPtrIsAtStartOfFile = False

        _nextPeekChar = f.read(1)

        if _nextPeekChar == _CHAREMPTY:  # EOF
            return _CHAREMPTY
        else:
            _currentChar = _nextPeekChar
            _nextPeekChar = f.read(1)

            return _currentChar

    else:

        _currentChar = _nextPeekChar
        _nextPeekChar = f.read(1)

        if _currentChar == _CHAREMPTY:
            return _CHAREMPTY
        elif _currentChar == _CHARLINEBREAK:    # python automatically converts any variants of line endings to '\n', in this specific file opening mode   
            _currLineNr += 1 
            _currRowNr = 1
        
            return _currentChar
        else:
            _currRowNr += 1
            return _currentChar








# DON'T USE PEEK FUNCTIONS UNLESS nextChar has been called at least once!!!!!!!!!!

def _peek_char():
    return _nextPeekChar
       


def _char_is_digit(c):
    return (c == _CHAR0 or
        c == _CHAR1 or
        c == _CHAR2 or
        c == _CHAR3 or
        c == _CHAR4 or
        c == _CHAR5 or
        c == _CHAR6 or
        c == _CHAR7 or
        c == _CHAR8 or
        c == _CHAR9        
    )




def _peek_char_is_identifier_end():
    return (_nextPeekChar == _CHAREMPTY or 
        _nextPeekChar == _CHARSPACE or
        _nextPeekChar == _CHARLINEBREAK or
        _nextPeekChar == _CHARLCURLYBRACKET or _nextPeekChar == _CHARRCURLYBRACKET or
        _nextPeekChar == _CHARLSQUAREBRACKET or _nextPeekChar == _CHARRSQUAREBRACKET or
        _nextPeekChar == _CHARLPAREN or _nextPeekChar == _CHARRPAREN or
        _nextPeekChar == _CHARCOLON or
        _nextPeekChar == _CHARSEMICOLON or
        _nextPeekChar == _CHARPERIOD or
        _nextPeekChar == _CHARCOMMA or
        _nextPeekChar == _CHARPERCENT or
        _nextPeekChar == _CHARSTAR or
        _nextPeekChar == _CHARPLUS or
        _nextPeekChar == _CHARSLASH or
        _nextPeekChar == _CHARMINUS or
        _nextPeekChar == _CHAREQUALS or
        _nextPeekChar == _CHARLESSTHAN or
        _nextPeekChar == _CHARGREATERTHAN or
        _nextPeekChar == _CHAREXCLAMATION or
        _nextPeekChar == _CHARET or
        _nextPeekChar == _CHARBACKSLASH or
        _nextPeekChar == _CHARBACKTICK or
        _nextPeekChar == _CHARVERTICAL or
        _nextPeekChar == _CHARSINGLEQUOTE or
        _nextPeekChar == _CHARDOUBLEQUOTE or
        _nextPeekChar == _CHARTILDE
     )   






def _peek_char_is_EOF_or_CR_or_newline():

    return _nextPeekChar == _CHAREMPTY or _nextPeekChar == _CHARLINEBREAK






def _lex_past_nestable_comment(f):          # return flag false signals error (no closing */)

    while True:

        lastChar = _next_char(f)

        if lastChar == _CHARSTAR:

            lastChar = _next_char(f) # eat past the star

            if lastChar == _CHARSLASH:                    

                break

            elif lastChar == _CHAREMPTY:

                util.log_error(_currLineNr, _currRowNr, "End of file before end of comment.")

                return False

        elif lastChar == _CHARSLASH:

            lastChar = _next_char(f) # eat past the slash

            if lastChar == _CHARSTAR:

                wasSuccessful = lex_past_nestable_comment(f)

                if not wasSuccessful:

                    return False

            elif lastChar == _CHAREMPTY:

                util.log_error(_currLineNr, _currRowNr, "End of file before end of comment.")

                return False


        elif lastChar == _CHAREMPTY:

            util.log_error(currLineNr, currRowNr, "End of file before end of comment.")

            return False
   

    return True









def _next_token(f):

    lastChar = _next_char(f)

    while lastChar == _CHARSPACE or lastChar == _CHARLINEBREAK:
        lastChar = _next_char(f)


    if _char_is_digit(lastChar):

        numStr = "";
        numStr += lastChar

        periodHasBeenFound = False

        savedCurrLineNr = _currLineNr
        savedCurrRowNr = _currRowNr

        while _char_is_digit(_peek_char()) or (_peek_char() == _CHARPERIOD and not periodHasBeenFound):

            lastChar = _next_char(f)

            if lastChar == _CHARPERIOD:
                periodHasBeenFound = True

            numStr += lastChar


        if periodHasBeenFound:
            return Token(savedCurrLineNr, savedCurrRowNr, Tok.FLOAT, numStr)    
        else:
            return Token(savedCurrLineNr, savedCurrRowNr, Tok.INTEGER, numStr)

    else:

        if lastChar == _CHAREMPTY:
            return Token(_currLineNr, _currRowNr, Tok.EOF, "")    
               
        elif lastChar == _CHARLCURLYBRACKET:
            return Token(_currLineNr, _currRowNr, Tok.LCURLYBRACKET, "")
                
        elif lastChar == _CHARRCURLYBRACKET:
            return Token(_currLineNr, _currRowNr, Tok.RCURLYBRACKET, "")
                
        elif lastChar == _CHARLSQUAREBRACKET:
            return Token(_currLineNr, _currRowNr, Tok.LSQUAREBRACKET, "")
                
        elif lastChar == _CHARRSQUAREBRACKET:
            return Token(_currLineNr, _currRowNr, Tok.RSQUAREBRACKET, "")
                
        elif lastChar == _CHARLPAREN:
            return Token(_currLineNr, _currRowNr, Tok.LPAREN, "")
                
        elif lastChar == _CHARRPAREN:
            return Token(_currLineNr, _currRowNr, Tok.RPAREN, "")
                
        elif lastChar == _CHARCOLON:

                return Token(_currLineNr, _currRowNr, Tok.COLON, "")
                
        elif lastChar == _CHARSEMICOLON:
            return Token(_currLineNr, _currRowNr, Tok.SEMICOLON, "")
               
        elif lastChar == _CHARPERIOD:
            if _char_is_digit(_peek_char()):
                savedCurrLineNr = _currLineNr
                savedCurrRowNr = _currRowNr

                floatStr = "."

                lastChar = _next_char(f)

                floatStr +=  lastChar

                while _char_is_digit(_peek_char()):

                    lastChar = _next_char(f)

                    floatStr +=  lastChar

                return Token(savedCurrLineNr, savedCurrRowNr, Tok.FLOAT, floatStr)

            else:
                if _peek_char() == _CHARPERIOD:
                    savedCurrLineNr = _currLineNr
                    savedCurrRowNr = _currRowNr
                    lastChar = _next_char(f)

                    if _peek_char() == _CHARPERIOD:
                        lastChar = _next_char(f)
                        return Token(savedCurrLineNr, savedCurrRowNr, Tok.TRIPLEPERIOD, "")

                    else:                                
                        return Token(savedCurrLineNr, savedCurrRowNr, Tok.DOUBLEPERIOD, "")                    
        
                else:
                    return Token(_currLineNr, _currRowNr, Tok.PERIOD, "")
                
        elif lastChar == _CHARMINUS:
            if _peek_char() == _CHAREQUALS:
                savedCurrLineNr = _currLineNr
                savedCurrRowNr = _currRowNr
                lastChar = _next_char(f)
                return Token(savedCurrLineNr, savedCurrRowNr, Tok.MINUSASSIGNMENTOPERATOR, "")

            else:
                return Token(_currLineNr, _currRowNr, Tok.MINUS, "")
               
        elif lastChar == _CHARCOMMA:
            return Token(_currLineNr, _currRowNr, Tok.COMMA, "")
                
        elif lastChar == _CHARBACKSLASH:        
            return Token(_currLineNr, _currRowNr, Tok.BACKSLASH, "")
                
        elif lastChar == _CHARDOUBLEQUOTE:
            strValue = ""

            savedCurrLineNr = _currLineNr
            savedCurrRowNr = _currRowNr

            while _peek_char() != _CHARDOUBLEQUOTE:
                lastChar = _next_char(f)

                if lastChar == _CHAREMPTY:
                    util.log_error(_currLineNr, _currRowNr, "Unfinished string literal.")
                    return Token(_currLineNr, _currRowNr, Tok.ERRATIC, "")
                        
                elif lastChar == _CHARLINEBREAK:
                     util.log_error(_currLineNr, _currRowNr, "Unfinished string literal.")
                     return Token(_currLineNr, _currRowNr, Tok.ERRATIC, "")
                        
                elif lastChar == _CHARBACKSLASH:
                    lastChar = _next_char(f)                            
                    if lastChar == _CHAREMPTY:
                        util.log_error(_currLineNr, _currRowNr, "EOF after string literal escape character.")
                        return Token(_currLineNr, _currRowNr, Tok.ERRATIC, "")
                            
                    elif lastChar == _CHARLINEBREAK:
                        util.log_error(_currLineNr, _currRowNr, "Newline after string literal escape character.")
                        return Token(_currLineNr, _currRowNr, Tok.ERRATIC, "")
                            
                    elif lastChar == _CHARN:
                        strValue += _CHARESCAPEN
                          
                    elif lastChar == _CHART:
                        strValue += _CHARESCAPET
                          
                    elif lastChar == _CHARB:
                        strValue += _CHARESCAPEB
                        
                    elif lastChar == _CHARR:
                        strValue += _CHARESCAPER
                 
                    elif lastChar == _CHARF:
                        strValue += _CHARESCAPEF
                            
                    elif lastChar == _CHARBACKSLASH:
                        strValue += _CHARBACKSLASH
                           
                    elif lastChar == _CHARSINGLEQUOTE:
                        strValue += _CHARSINGLEQUOTE
                          
                    elif lastChar == _CHARDOUBLEQUOTE:
                        strValue += _CHARDOUBLEQUOTE
                          
                    elif lastChar == _CHAR0:
                        strValue += _CHARESCAPE0
                           
                    else:   # TODO: add support for octal and hexadecimal escape characters here...
                        util.log_error(_currLineNr, _currRowNr, "Unknown escape character in string literal.")
                        return Token(_currLineNr, _currRowNr, Tok.ERRATIC, "")
                      
                     
                else:
                    strValue += lastChar
                
            # end while

            lastChar = _next_char(f)
            return Token(savedCurrLineNr, savedCurrRowNr, Tok.STRING, strValue)
                    
        elif lastChar == _CHARPERCENT:
            if _peek_char() == _CHAREQUALS:
                savedCurrLineNrB = _currLineNr
                savedCurrRowNrB = _currRowNr

                lastChar = _next_char(f)

                return Token(savedCurrLineNrB, savedCurrRowNrB, Tok.PERCENTASSIGNMENTOPERATOR, "")
            else:
                return Token(_currLineNr, _currRowNr, Tok.PERCENT, "")       
               
        elif lastChar == _CHARSTAR:  # no need to handle end of multiline comment here...
            if _peek_char() == _CHAREQUALS:
                savedCurrLineNrC = _currLineNr
                savedCurrRowNrC = _currRowNr

                lastChar = _next_char(f)

                return Token(savedCurrLineNrC, savedCurrRowNrC, Tok.STARASSIGNMENTOPERATOR, "")
            else:
                return Token(_currLineNr, _currRowNr, Tok.STAR, "")
                
        elif lastChar == _CHARPLUS:
            if _peek_char() == _CHAREQUALS:
                savedCurrLineNrD = _currLineNr
                savedCurrRowNrD = _currRowNr

                lastChar = _next_char(f)

                return Token(savedCurrLineNrD, savedCurrRowNrD, Tok.PLUSASSIGNMENTOPERATOR, "")
            else:
                return Token(_currLineNr, _currRowNr, Tok.PLUS, "")
                
        elif lastChar == _CHARSLASH:
            peek = _peek_char()

            if peek == _CHAREQUALS:
                savedCurrLineNrE = _currLineNr
                savedCurrRowNrE = _currRowNr

                lastChar = _next_char(f)

                return Token(savedCurrLineNrE, savedCurrRowNrE, Tok.SLASHASSIGNMENTOPERATOR, "")
                    

            elif peek == _CHARSLASH:
                lastChar = _next_char(f)
                while not _peek_char_is_EOF_or_CR_or_newline():
                    lastChar = _next_char(f)
                
                if lastChar == _CHAREMPTY:
                    return Token(_currLineNr, _currRowNr, Tok.EOF, "")
                else:
                    return _next_token(f)
                   

            elif peek == _CHARSTAR:
                lastChar = _next_char(f)
                wasSuccessful = _lex_past_nestable_comment(f)
                if not wasSuccessful:
                    return Token(_currLineNr, _currRowNr, Tok.ERRATIC, "")
                else:
                    return _next_token(f)
                
                   
            else:
                return Token(_currLineNr, _currRowNr, Tok.SLASH, "")                    
            
                
        elif lastChar == _CHAREQUALS:
            peek = _peek_char()

            if peek == _CHAREQUALS:
                savedCurrLineNrF = _currLineNr
                savedCurrRowNrF = _currRowNr
                lastChar = _next_char(f)
                
                return Token(savedCurrLineNrF, savedCurrRowNrF, Tok.EQUALS, "")
                
                    
            else:
                return Token(_currLineNr, _currRowNr, Tok.ASSIGNMENTOPERATOR, "")
            
                
        elif lastChar == _CHARLESSTHAN:
            if _peek_char() == _CHAREQUALS:
                savedCurrLineNrH = _currLineNr
                savedCurrRowNrH = _currRowNr
                lastChar = _next_char(f)
                return Token(savedCurrLineNrH, savedCurrRowNrH, Tok.LESSTHANOREQUALS, "")
            else:
                return Token(_currLineNr, _currRowNr, Tok.LESSTHAN, "")
             
                
        elif lastChar == _CHARGREATERTHAN:
            if _peek_char() == _CHAREQUALS:
                savedCurrLineNrI = _currLineNr
                savedCurrRowNrI = _currRowNr
                lastChar = _next_char(f)
                return Token(savedCurrLineNrI, savedCurrRowNrI, Tok.GREATERTHANOREQUALS, "")
            else:
                return Token(_currLineNr, _currRowNr, Tok.GREATERTHAN, "")
            
               
        elif lastChar == _CHAREXCLAMATION:
            if _peek_char() == _CHAREQUALS:
                savedCurrLineNrJ = _currLineNr
                savedCurrRowNrJ = _currRowNr
                lastChar = _next_char(f)
                return Token(savedCurrLineNrJ, savedCurrRowNrJ, Tok.EQUALSNOT, "")
            else:
                return Token(_currLineNr, _currRowNr, Tok.EXCLAMATION, "")
                
        elif lastChar == _CHARET:
            if _peek_char() == _CHARET:
                savedCurrLineNrK = _currLineNr
                savedCurrRowNrK = _currRowNr
                lastChar = _next_char(f)
                return Token(savedCurrLineNrK, savedCurrRowNrK, Tok.ANDSYMBOL, "")
            else:
                return Token(_currLineNr, _currRowNr, Tok.ERRATIC, "")
                
        elif lastChar == _CHARBACKTICK:
            return Token(_currLineNr, _currRowNr, Tok.BACKTICK, "") 
                
        elif lastChar == _CHARVERTICAL:
            if _peek_char() == _CHARVERTICAL:
                savedCurrLineNrL = _currLineNr
                savedCurrRowNrL = _currRowNr
                lastChar = _next_char(f)
                return Token(savedCurrLineNrL, savedCurrRowNrL, Tok.ORSYMBOL, "")
            else:
                util.log_error(_currLineNr, _currRowNr, "Unknown token!")
                return Token(_currLineNr, _currRowNr, Tok.ERRATIC, "")    
                
        elif lastChar == _CHARSINGLEQUOTE:
            if _peek_char() == _CHARSINGLEQUOTE:
                savedCurrLineNr = _currLineNr
                savedCurrRowNr = _currRowNr
                lastChar = _next_char(f)
                return Token(savedCurrLineNr, savedCurrRowNr, Tok.DOUBLESINGLEQUOTE, "")

            else:
                return Token(_currLineNr, _currRowNr, Tok.SINGLEQUOTE, "")

        elif lastChar == _CHARTILDE:
            return Token(_currLineNr, _currRowNr, Tok.TILDE, "")
    
        else: # IDENTIFIER OR RESERVED WORD
                
                identifier = ""
                
                identifier += lastChar

                savedCurrLineNrM = _currLineNr
                savedCurrRowNrM = _currRowNr

                while not _peek_char_is_identifier_end():
                    lastChar = _next_char(f)
                
                    identifier += lastChar
               

                if identifier == "if":

                    return Token(savedCurrLineNrM, savedCurrRowNrM, Tok.IF, "")

                elif identifier == "else":

                    return Token(savedCurrLineNrM, savedCurrRowNrM, Tok.ELSE, "")

                elif identifier == "loop":

                    return Token(savedCurrLineNrM, savedCurrRowNrM, Tok.LOOP, "")

                elif identifier == "break":

                    return Token(savedCurrLineNrM, savedCurrRowNrM, Tok.BREAK, "")

                elif identifier == "continue":

                    return Token(savedCurrLineNrM, savedCurrRowNrM, Tok.CONTINUE, "")

                elif identifier == "for":

                    return Token(savedCurrLineNrM, savedCurrRowNrM, Tok.FOR, "")

                elif identifier == "to":

                    return Token(savedCurrLineNrM, savedCurrRowNrM, Tok.TO, "")

                elif identifier == "over":

                    return Token(savedCurrLineNrM, savedCurrRowNrM, Tok.OVER, "")

                elif identifier == "in":

                    return Token(savedCurrLineNrM, savedCurrRowNrM, Tok.IN, "")

                elif identifier == "indexoffset":

                    return Token(savedCurrLineNrM, savedCurrRowNrM, Tok.INDEXOFFSET, "")

                elif identifier == "indexfactor":

                    return Token(savedCurrLineNrM, savedCurrRowNrM, Tok.INDEXFACTOR, "")

                elif identifier == "return":

                    return Token(savedCurrLineNrM, savedCurrRowNrM, Tok.RETURN, "")

                elif identifier == "mu":

                    return Token(savedCurrLineNrM, savedCurrRowNrM, Tok.MUT, "")

                elif identifier == "ref":

                    return Token(savedCurrLineNrM, savedCurrRowNrM, Tok.REF, "")

                elif identifier == "inline":

                    return Token(savedCurrLineNrM, savedCurrRowNrM, Tok.INLINE, "")

                elif identifier == "case":

                    return Token(savedCurrLineNrM, savedCurrRowNrM, Tok.CASE, "")

                elif identifier == "default":

                    return Token(savedCurrLineNrM, savedCurrRowNrM, Tok.DEFAULT, "")

                elif identifier == "true":

                    return Token(savedCurrLineNrM, savedCurrRowNrM, Tok.TRUE, "")

                elif identifier == "false":

                    return Token(savedCurrLineNrM, savedCurrRowNrM, Tok.FALSE, "")

                elif identifier == "fn":

                    return Token(savedCurrLineNrM, savedCurrRowNrM, Tok.FUN, "")

                elif identifier == "end":

                    return Token(savedCurrLineNrM, savedCurrRowNrM, Tok.END, "")

                elif identifier == "import":

                    return Token(savedCurrLineNrM, savedCurrRowNrM, Tok.IMPORT, "")

                elif identifier == "internal":

                    return Token(savedCurrLineNrM, savedCurrRowNrM, Tok.INTERNAL, "")        

                elif identifier == "type":

                    return Token(savedCurrLineNrM, savedCurrRowNrM, Tok.TYPE, "")

                elif identifier == "label":

                    return Token(savedCurrLineNrM, savedCurrRowNrM, Tok.LABEL, "")

                elif identifier == "nil":

                    return Token(savedCurrLineNrM, savedCurrRowNrM, Tok.NILTYPE, "")

                elif identifier == "bool":

                    return Token(savedCurrLineNrM, savedCurrRowNrM, Tok.BOOL, "")

                elif identifier == "i8":

                    return Token(savedCurrLineNrM, savedCurrRowNrM, Tok.I8, "")

                elif identifier == "i16":

                    return Token(savedCurrLineNrM, savedCurrRowNrM, Tok.I16, "")

                elif identifier == "i32":

                    return Token(savedCurrLineNrM, savedCurrRowNrM, Tok.I32, "")

                elif identifier == "i64":

                    return Token(savedCurrLineNrM, savedCurrRowNrM, Tok.I64, "")

                elif identifier == "int":

                    return Token(savedCurrLineNrM, savedCurrRowNrM, Tok.ISIZE, "")

                elif identifier == "u8":

                    return Token(savedCurrLineNrM, savedCurrRowNrM, Tok.U8, "")

                elif identifier == "u16":

                    return Token(savedCurrLineNrM, savedCurrRowNrM, Tok.U16, "")

                elif identifier == "u32":

                    return Token(savedCurrLineNrM, savedCurrRowNrM, Tok.U32, "")

                elif identifier == "u64":

                    return Token(savedCurrLineNrM, savedCurrRowNrM, Tok.U64, "")

                elif identifier == "uint":

                    return Token(savedCurrLineNrM, savedCurrRowNrM, Tok.USIZE, "")

                elif identifier == "f32":

                    return Token(savedCurrLineNrM, savedCurrRowNrM, Tok.F32, "")

                elif identifier == "f64":

                    return Token(savedCurrLineNrM, savedCurrRowNrM, Tok.F64, "")

                elif identifier == "storetype":

                    return Token(savedCurrLineNrM, savedCurrRowNrM, Tok.CONTENTTYPE, "")

                elif identifier == "prefiximport":

                    return Token(savedCurrLineNrM, savedCurrRowNrM, Tok.PREFIXIMPORT, "")

                elif identifier == "construand":

                    return Token(savedCurrLineNrM, savedCurrRowNrM, Tok.CONSTRUAND, "")

                elif identifier == "downto":

                    return Token(savedCurrLineNrM, savedCurrRowNrM, Tok.DOWNTO, "")

                elif identifier == "repeat":

                    return Token(savedCurrLineNrM, savedCurrRowNrM, Tok.REPEAT, "")

                elif identifier == "trash":

                    return Token(savedCurrLineNrM, savedCurrRowNrM, Tok.TRASH, "")

                elif identifier == "uninitialized":

                    return Token(savedCurrLineNrM, savedCurrRowNrM, Tok.UNINITIALIZED, "")

                elif identifier == "IF":

                    return Token(savedCurrLineNrM, savedCurrRowNrM, Tok.IFUPPERCASE, "")

                elif identifier == "ELSE":

                    return Token(savedCurrLineNrM, savedCurrRowNrM, Tok.ELSEUPPERCASE, "")

                elif identifier == "SWITCH":

                    return Token(savedCurrLineNrM, savedCurrRowNrM, Tok.SWITCHUPPERCASE, "")

                elif identifier == "STORETYPE":

                    return Token(savedCurrLineNrM, savedCurrRowNrM, Tok.CONTENTTYPEUPPERCASE, "")

                elif identifier == "CASE":

                    return Token(savedCurrLineNrM, savedCurrRowNrM, Tok.CASEUPPERCASE, "")

                elif identifier == "DEFAULT":

                    return Token(savedCurrLineNrM, savedCurrRowNrM, Tok.DEFAULTUPPERCASE, "")

                elif identifier == "switch":

                    return Token(savedCurrLineNrM, savedCurrRowNrM, Tok.SWITCH, "")

                elif identifier == 'arr':

                    return Token(savedCurrLineNrM, savedCurrRowNrM, Tok.ARR, "")

                elif identifier == 'vbox':

                    return Token(savedCurrLineNrM, savedCurrRowNrM, Tok.VBOX, "")

                else: # IDENTIFIER

                    return Token(savedCurrLineNrM, savedCurrRowNrM, Tok.IDENTIFIER, identifier)

                





# Returns a list of Token:s, or False if a lex error or file error was encountered
def lex_file(filename):
    # Reset variables:
    global _currLineNr
    global _currRowNr
    global _currentChar
    global _nextPeekChar
    global _charPtrIsAtStartOfFile        
    _currLineNr = 1
    _currRowNr = 1
    _currentChar = _CHAREMPTY      # EOF marker; dummy
    _nextPeekChar = _CHAREMPTY     # EOF marker; dummy
    _charPtrIsAtStartOfFile = True       

    tokenList = []

    errorFree = True

    try: 
        with open(filename, mode = 'r') as f:

            while True: 
                t = _next_token(f)
                if t.kind == Tok.ERRATIC:
                    errorFree = False
                    break
                elif t.kind == Tok.EOF:
                    tokenList.append(t)
                    break
                else:
                    tokenList.append(t)

    except OSError:
        util.log_error("Could not access the file: " + filename)
        return False    
    
    if errorFree:
        return tokenList
    else:
        return False


















