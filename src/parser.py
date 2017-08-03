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


import util
from tokens import *
from ast import *

_lexed = []  

_lexedpos = 0

def _set_lextokens(lexedTokens): # TODO: use parseProgram to call this...
    global _lexed
    global _lexedpos

    _lexed = lexedTokens
    _lexedpos = 0


def _next_parse_token():
    global _lexedpos

    if len(_lexed) <= _lexedpos:   # safety measure
        return Token(0, 0, Tok.EOF, "")
    else:
        resultToken = _lexed[_lexedpos]
        _lexedpos += 1
        return resultToken


def _peek_parse_token(peekIndex):
    peekPos = _lexedpos + peekIndex
    if len(_lexed) <= peekPos:
        return Token(0, 0, Tok.EOF, "")
    else: 
        return _lexed[peekPos]     






####################################################################################################
####                        TYPES                                                           ########
####################################################################################################



########################### TYPE PEEKING ###########################################################

# Note: All peek functions return -1 on error.                    



def _peek_past_type_list(peekStart, displayErrorMessagesFlag):

   thePeekStart = peekStart;

   while True:

        newPeekStart = _peek_past_type(thePeekStart, displayErrorMessagesFlag)
        if newPeekStart == -1:
            return -1

        peek = _peek_parse_token(newPeekStart)

        if peek.kind == Tok.COMMA:

            thePeekStart = newPeekStart + 1
            continue

        else:

            return newPeekStart



def  _peek_past_type_param_list(peekStart, displayErrorMessagesFlag):

    thePeekStart = peekStart

    while True:

        peek1 = _peek_parse_token(thePeekStart)

        if peek1.kind == Tok.REF:

            peek15 = _peek_parse_token(thePeekStart + 1)

            newPeekStart = _peek_past_type(thePeekStart + 1, displayErrorMessagesFlag) # at least one argument is expected
            if newPeekStart == -1: 
                return -1

            peek2 = _peek_parse_token(newPeekStart)

            if peek2.kind == Tok.COMMA:

                thePeekStart = newPeekStart + 1
                continue

            else:

                return newPeekStart

                            

        elif peek1.kind == Tok.MUT:

            peek15 = _peek_parse_token(thePeekStart + 1)

            if peek15.kind == Tok.CONSTRUAND:

                newPeekStart = _peek_past_type(thePeekStart + 2, displayErrorMessagesFlag)
                if newPeekStart == -1: 
                    return -1

                peek2 = _peek_parse_token(newPeekStart)

                if peek2.kind == Tok.COMMA:

                    thePeekStart = newPeekStart + 1
                    continue

                else:

                    return newPeekStart


            else:

                newPeekStart = _peek_past_type(thePeekStart + 1, displayErrorMessagesFlag)
                if newPeekStart == -1: 
                    return -1

                peek2 = _peek_parse_token(newPeekStart)

                if peek2.kind == Tok.COMMA:

                    thePeekStart = newPeekStart + 1
                    continue

                else:

                    return newPeekStart

                

        elif peek1.kind == Tok.CONSTRUAND:

            peek15 = _peek_parse_token(thePeekStart + 1)

            if peek15.kind == Tok.MUT:

                newPeekStart = _peek_past_type(thePeekStart + 2, displayErrorMessagesFlag)
                if newPeekStart == -1:
                    return -1

                peek2 = _peek_parse_token(newPeekStart)

                if peek2.kind == Tok.COMMA:

                    thePeekStart = newPeekStart + 1
                    continue

                else:

                    return newPeekStart

                

            else:

                newPeekStart = _peek_past_type(thePeekStart + 1, displayErrorMessagesFlag)
                if newPeekStart == -1: 
                    return -1

                peek2 = _peek_parse_token(newPeekStart)

                if peek2.kind == Tok.COMMA:

                    thePeekStart = newPeekStart + 1
                    continue

                else:

                    return newPeekStart

                

            

        else:

            newPeekStart = _peek_past_type(thePeekStart, displayErrorMessagesFlag) # at least one argument is expected
            if newPeekStart == -1: 
                return -1
                
            peek2 = _peek_parse_token(newPeekStart)

            if peek2.kind == Tok.COMMA:

                thePeekStart = newPeekStart + 1
                continue

            else:

                return newPeekStart;

           




def _peek_past_post_type_eager(peekStart, displayErrorMessagesFlag):  # for peeking, we can do it recursively...

    peek = _peek_parse_token(peekStart)

    if peek.kind == Tok.SLASH:

        return _peek_past_type(peekStart + 1, displayErrorMessagesFlag)

    else:

        return peekStart

    


def _peek_past_struct_type_posts(peekStart, displayErrorMessagesFlag):

    thePeekStart = peekStart

    while True:

        peek = _peek_parse_token(thePeekStart)

        if peek.kind == Tok.IDENTIFIER:

            peek2 = _peek_parse_token(thePeekStart + 1)

            if peek2.kind == Tok.SINGLEQUOTE:

                newPeekStart = _peek_past_type(thePeekStart + 2, displayErrorMessagesFlag)
                if newPeekStart == -1:
                    return -1

                

                thePeekStart = newPeekStart

                

                continue

            else:

                util.maybe_log_error(peek2.lineNr, peek2.rowNr, "Expected a singlequote, found something else.", displayErrorMessagesFlag)
                return -1

                        

        else:

            return thePeekStart

        





    


def _peek_past_array_type_eager(peekStart, displayErrorMessagesFlag):

    peek = _peek_parse_token(peekStart)

    if peek.kind == Tok.ARR:

        return _peek_past_type(peekStart + 1, displayErrorMessagesFlag)

    else:

        util.maybe_log_error(peek.lineNr, peek.rowNr, "Expected 'arr', found something else.", displayErrorMessagesFlag)
        return -1

                


def _peek_past_fun_type_after_param_list(peekStart, displayErrorMessagesFlag):

    peekBefore = _peek_parse_token(peekStart)

    if peekBefore.kind == Tok.GREATERTHAN:

        return _peek_past_post_type_eager(peekStart + 1, displayErrorMessagesFlag)

    elif peekBefore.kind == Tok.TO:

        peekStart2 = _peek_past_type_list(peekStart + 1, displayErrorMessagesFlag)
        if peekStart2 == -1: 
            return -1

        peek3 = _peek_parse_token(peekStart2)

        if peek3.kind == Tok.GREATERTHAN:

            return _peek_past_post_type_eager(peekStart2 + 1, displayErrorMessagesFlag)

        else:

            util.maybe_log_error(peek3.lineNr, peek3.rowNr, "Expected a '>', found something else. #222", displayErrorMessagesFlag)
            return -1

        

    else:

        util.maybe_log_error(peekBefore.lineNr, peekBefore.rowNr, "Expected '>' or 'to', found something else.", displayErrorMessagesFlag)
        return -1

    



def _peek_past_fun_type_eager(peekStart, displayErrorMessagesFlag):

    peek = _peek_parse_token(peekStart)

    if peek.kind == Tok.FUN:

        peek2 = _peek_parse_token(peekStart + 1)
    
        if peek2.kind == Tok.LESSTHAN:

            peekBefore = _peek_parse_token(peekStart + 2)

            if peekBefore.kind == Tok.GREATERTHAN or peekBefore.kind == Tok.TO:

                return _peek_past_fun_type_after_param_list(peekStart + 2, displayErrorMessagesFlag)

            else:

                newPeekStart = _peek_past_type_param_list(peekStart + 2, displayErrorMessagesFlag)
                if newPeekStart == -1:
                    return -1

                return _peek_past_fun_type_after_param_list(newPeekStart, displayErrorMessagesFlag)

            

        else:

            util.maybe_log_error(peek2.lineNr, peek2.rowNr, "Expected a '(', found something else. #1", displayErrorMessagesFlag)
            return -1

        

    else:

        util.maybe_log_error(peek.lineNr, peek.rowNr, "Expected 'Fn', found something else.", displayErrorMessagesFlag)
        return -1

    





def _peek_past_struct_type_eager(peekStart, displayErrorMessagesFlag):

    peek = _peek_parse_token(peekStart)

    if peek.kind == Tok.IDENTIFIER:

        
        peek4 = _peek_parse_token(peekStart + 1)

        if peek4.kind == Tok.LCURLYBRACKET:

            newPeekStart = _peek_past_struct_type_posts(peekStart + 2, displayErrorMessagesFlag)
            if newPeekStart == -1: 
                return -1

            peek5 = _peek_parse_token(newPeekStart)

            if peek5.kind == Tok.RCURLYBRACKET:

                return _peek_past_post_type_eager(newPeekStart + 1, displayErrorMessagesFlag)

            else:

                util.maybe_log_error(peek5.lineNr, peek5.rowNr, "Expected a '}', found something else.", displayErrorMessagesFlag)
                return -1

           

        else:

            util.maybe_log_error(peek4.lineNr, peek4.rowNr, "Expected a '{', found something else. #111", displayErrorMessagesFlag)
            return -1
        

    else:

        util.maybe_log_error(peek.lineNr, peek.rowNr, "Expected a tag identifier, found something else.", displayErrorMessagesFlag)
        return -1






def _peek_past_type(peekStart, displayErrorMessagesFlag):

    peek = _peek_parse_token(peekStart)    

    if (peek.kind == Tok.I8 or peek.kind == Tok.I16 or peek.kind == Tok.I32 or peek.kind == Tok.I64 or peek.kind == Tok.ISIZE or
        peek.kind == Tok.U8 or peek.kind == Tok.U16 or peek.kind == Tok.U32 or peek.kind == Tok.U64 or peek.kind == Tok.USIZE or
        peek.kind == Tok.F32 or peek.kind == Tok.F64 or
        peek.kind == Tok.NILTYPE or peek.kind == Tok.BOOL
    ):

        return _peek_past_post_type_eager(peekStart + 1, displayErrorMessagesFlag)

    elif peek.kind == Tok.IDENTIFIER:

        peek2 = _peek_parse_token(peekStart + 1)

        if peek2.kind == Tok.LPAREN:

            newPeekStart = _peek_past_type_param_list(peekStart + 2, displayErrorMessagesFlag)
            if newPeekStart == -1: 
                return -1

            peek3 = _peek_parse_token(newPeekStart)

            if peek3.kind == Tok.RPAREN:

                return _peek_past_post_type_eager(newPeekStart + 1, displayErrorMessagesFlag)

            else:

                util.maybe_log_error(peek3.lineNr, peek3.rowNr, "Expected \')\', found something else.", displayErrorMessagesFlag)
                return -1

        elif peek2.kind == Tok.DOUBLEPERIOD:

            peek3 = _peek_parse_token(peekStart + 2)

            if peek3.kind == Tok.IDENTIFIER:

                peek4 = _peek_parse_token(peekStart + 3)

                if peek4.kind == Tok.LPAREN:

                    newPeekStart = _peek_past_type_param_list(peekStart + 4, displayErrorMessagesFlag)
                    if newPeekStart == -1:
                        return -1

                    peek5 = _peek_parse_token(newPeekStart)

                    if peek5.kind == Tok.RPAREN:
                        
                        return _peek_past_post_type_eager(newPeekStart + 1, displayErrorMessagesFlag)
    
                    else:
                        util.maybe_log_error(peek5.lineNr, peek5.rowNr, "Expected ')', found something else.", displayErrorMessagesFlag)
                        return -1
    
                else:

                    return _peek_past_post_type_eager(peekStart + 3, displayErrorMessagesFlag)

            else:
                util.maybe_log_error(peek3.lineNr, peek3.rowNr, "Expected an identifier after the doubleperiod.", displayErrorMessagesFlag)
                return -1                    

        elif peek2.kind == Tok.LCURLYBRACKET:

            return peek_past_struct_type_eager(peekStart, displayErrorMessagesFlag)    
        
        else:

            return _peek_past_post_type_eager(peekStart + 1, displayErrorMessagesFlag)
    
        

    elif peek.kind == Tok.ARR:

        return _peek_past_array_type_eager(peekStart, displayErrorMessagesFlag)

    elif peek.kind == Tok.FUN:

        return _peek_past_fun_type_eager(peekStart, displayErrorMessagesFlag)

    elif peek.kind == Tok.LPAREN:

        newPeekStart = _peek_past_type(peekStart + 1, displayErrorMessagesFlag)
        if newPeekStart == -1:
            return -1

        peek2 = _peek_parse_token(newPeekStart)

        if peek2.kind == Tok.RPAREN:

            return _peek_past_post_type_eager(newPeekStart + 1, displayErrorMessagesFlag)

        else:

            util.maybe_log_error(peek2.lineNr, peek2.rowNr, "Expected a ')', found something else. #6", displayErrorMessagesFlag)
            return -1

        

    else:

        util.maybe_log_error(peek.lineNr, peek.rowNr, "Expected a type, found something else.", displayErrorMessagesFlag)
        return -1



############################# TYPE PARSING ###############################################

def _parse_type_list():

    result = []    # empty to begin with

    while True:

        retType = _parse_type()
        if retType is None:
            return None

        result.append(retType)

        peek = _peek_parse_token(0)

        if peek.kind == Tok.COMMA:

            junk = _next_parse_token() # eat past the ,

            continue

        else:

            return result

        



def _parse_type_param_list():
    
    result = [] # empty to begin with

    while True:

        peek0 = _peek_parse_token(0)

        if peek0.kind == Tok.REF:

            junk = _next_parse_token() # eat past "ref"

            arg = _parse_type() # at least one argument is expected
            if arg is None:
                return None

            typeArg = NRefTypeArg(peek0.lineNr, peek0.rowNr, arg)

            result.append(typeArg)
                
            peek = _peek_parse_token(0)

            if peek.kind == Tok.COMMA:

                junk = _next_parse_token() # eat the ,

                continue

            else:

                return result

                    

        elif peek0.kind == Tok.MUT:

            junk = _next_parse_token()  # eat past "mu"

            peek1 = _peek_parse_token(0) 

            if peek1.kind == Tok.CONSTRUAND:

                junk = _next_parse_token() # eat past "construand"

                arg = _parse_type() # at least one argument is expected
                if arg is None: 
                    return None

                typeArg = NNormalTypeArg(peek0.lineNr, peek0.rowNr, True, True, arg)

                result.append(typeArg)
                    
                peek = _peek_parse_token(0)

                if peek.kind == Tok.COMMA:

                    junk = _next_parse_token() # eat the ,

                    continue

                else:

                    return result    

            else:

                arg = _parse_type() # at least one argument is expected
                if arg is None:
                    return None

                typeArg = NNormalTypeArg(peek0.lineNr, peek0.rowNr, True, False, arg)
                result.append(typeArg)
                
                peek = _peek_parse_token(0)
                if peek.kind == Tok.COMMA:

                    junk = _next_parse_token() # eat the ,
                    
                    continue

                else:

                    return result
                    
            

        elif peek0.kind == Tok.CONSTRUAND:

            junk = _next_parse_token()  # eat past "construand"

            peek1 = _peek_parse_token(0) 

            if peek1.kind == Tok.MUT:

                junk = _next_parse_token() # eat past "mu"

                arg = _parse_type() # at least one argument is expected
                if arg is None: 
                    return None

                typeArg = NNormalTypeArg(peek0.lineNr, peek0.rowNr, True, True, arg)

                result.append(typeArg)
                    
                peek = _peek_parse_token(0)

                if peek.kind == Tok.COMMA:

                    junk = _next_parse_token() # eat the ,

                    continue

                else:

                    return result    

            else:

                arg = _parse_type() # at least one argument is expected
                if arg is None:
                    return None

                typeArg = NNormalTypeArg(peek0.lineNr, peek0.rowNr, False, True, arg)
                result.append(typeArg)
                
                peek = _peek_parse_token(0)
                if peek.kind == Tok.COMMA:

                    junk = _next_parse_token() # eat the ,
                    
                    continue

                else:

                    return result
                    
             

        else:

            arg = _parse_type()    # at least one argument is expected by this function -- nota bene
            if arg is None: 
                return None

            typeArg = NNormalTypeArg(peek0.lineNr, peek0.rowNr, False, False, arg)

            result.append(typeArg)
                
            peek = _peek_parse_token(0)

            if peek.kind == Tok.COMMA:

                junk = _next_parse_token() # eat past the ,

                continue

            else:

                return result

           






def _parse_variant_box_type_vector(
        leftHandSide
    ):

    result = [] # empty to begin with
    result.append(leftHandSide)

    while True:

        # starts after a slash symbol

        nextType = _parse_type_inside_or()
        if nextType is None:
            return None

        result.append(nextType)

        peek = _peek_parse_token(0)
         
        if peek.kind == Tok.SLASH:
            
            junk = _next_parse_token() # go past the slash

            continue

        else:

            return result

        




def _parse_type():
    
    firstType = _parse_type_inside_or()
    if firstType is None: 
        return None

    peek = _peek_parse_token(0)

    if peek.kind == Tok.SLASH:
    
        junk = _next_parse_token() # eat the slash
        
        orTypeVector = _parse_variant_box_type_vector(firstType)
        if orTypeVector is None: 
            return None

        return NVariantBoxType(peek.lineNr, peek.rowNr, orTypeVector)

    else:

        return firstType

   




def _parse_identifier(): 

    tok = _next_parse_token();

    if tok.kind == Tok.IDENTIFIER:

        return NIdentifier(tok.lineNr, tok.rowNr, tok.tokString)

    else:

        util.log_error(tok.lineNr, tok.rowNr, "Expected an identifier, found something else.")
        return None

   

def _parse_struct_type_posts():

    result = [] # empty to begin with

    while True:

        peek = _peek_parse_token(0)

        if peek.kind == Tok.IDENTIFIER:

            identifier = _parse_identifier()
            if identifier is None: 
                return None           # should never happen though in this case... but nevermind

            tok = _next_parse_token()

            if tok.kind == Tok.SINGLEQUOTE:

                identifiersType = _parse_type()
                if identifiersType is None: 
                    return None

                

                

                structTypeMember = NStructTypeMember(tok.lineNr, tok.rowNr, identifier, identifiersType)

                result.append(structTypeMember)

                continue

            else:

                util.log_error(tok.lineNr, tok.rowNr, "Expected a singlequote, found something else.")
                return None
        

        else:

            return result

        









def _parse_array_type():

    tok = _next_parse_token()

    if tok.kind == Tok.ARR:

        arrayIndicesType = _parse_type_inside_or()
        if arrayIndicesType is None: 
            return None

        return NDynamicArrayType(
            tok.lineNr, tok.rowNr,
            arrayIndicesType
        )     

    else:

        util.log_error(tok.lineNr, tok.rowNr, "Expected 'arr', found something else.")
        return None

    




def _parse_fun_type_eager():

    peek = _next_parse_token()

    if peek.kind == Tok.FUN:

        tok = _next_parse_token() 

        if tok.kind == Tok.LESSTHAN:

            peek3 = _peek_parse_token(0)

            if peek3.kind == Tok.GREATERTHAN:

                junk = _next_parse_token()

                argsList = []  
                returnTypes = []  

                return NFunctionType(
                    peek.lineNr, peek.rowNr, 
                    argsList, 
                    returnTypes
                )

            elif peek3.kind == Tok.TO:

                junk = _next_parse_token()    # go past the 'to'

                returnTypes = _parse_type_list()
                if returnTypes is None: 
                    return None

                argsList = []

                tok4 = _next_parse_token()

                if tok4.kind == Tok.GREATERTHAN:

                    return NFunctionType>(
                        peek.lineNr, peek.rowNr, 
                        argsList, 
                        returnTypes
                    )

                else:

                    util.log_error(tok4.lineNr, tok4.rowNr, "Expected a '>', found something else. #777")
                    return None

                

            else:

                argsList = _parse_type_param_list()
                if argsList is None: 
                    return None

                tok3 = _next_parse_token()

                if tok3.kind == Tok.GREATERTHAN:

                    returnTypes = [] # empty

                    return NFunctionType(
                        peek.lineNr, peek.rowNr, 
                        argsList, 
                        returnTypes
                    )

                elif tok3.kind == Tok.TO:

                    returnTypes = _parse_type_list()
                    if returnTypes is None: 
                        return None

                    tok4 = _next_parse_token()

                    if tok4.kind == Tok.GREATERTHAN:

                        return NFunctionType(
                            peek.lineNr, peek.rowNr, 
                            argsList, 
                            returnTypes
                        )

                    else:

                        util.log_error(tok4.lineNr, tok4.rowNr, "Expected a '>', found something else. #777")
                        return None

                    

                else:

                    util.log_error(tok3.lineNr, tok3.rowNr, "Expected '>' or 'to', found something else.")
                    return None

               
        else:

            util.log_error(tok.lineNr, tok.rowNr, "Expected a '<', found something else. #2")
            return None

        

    else:

        util.log_error(peek.lineNr, peek.rowNr, "Expected 'fn', found something else.")
        return None

    



def _parse_struct_type():

    peek = _peek_parse_token(0)   # save lineNr and rowNr on this

    tag = _parse_identifier()
    if tag is None: 
        return None

    tok3 = _next_parse_token()

    if tok3.kind == Tok.LCURLYBRACKET:

        members = _parse_struct_type_posts()
        if members is None:
            return None

        tok = _next_parse_token()

        if tok.kind == Tok.RCURLYBRACKET:

            
            return NStructType(peek.lineNr, peek.rowNr, tag, members)
            

        else:

            util.log_error(tok.lineNr, tok.rowNr, "Expected a '}', found something else.")
            return None        

    else:

        util.log_error(peek.lineNr, peek.rowNr, "Expected an identifier, found something else. #9")
        return None

    




def _parse_type_inside_or():

    peek = _peek_parse_token(0)

    if peek.kind == Tok.I8:

        junk = _next_parse_token()

        theType = NI8Type(peek.lineNr, peek.rowNr)

        return theType

    elif peek.kind == Tok.I16:

        junk = _next_parse_token()

        theType = NI16Type(peek.lineNr, peek.rowNr)

        return theType

    elif peek.kind == Tok.I32:

        junk = _next_parse_token()

        theType = NI32Type(peek.lineNr, peek.rowNr)

        return theType

    elif peek.kind == Tok.I64:

        junk = _next_parse_token()

        theType = NI64Type(peek.lineNr, peek.rowNr)

        return theType

    elif peek.kind == Tok.ISIZE:

        junk = _next_parse_token()

        theType = NISizeType(peek.lineNr, peek.rowNr)

        return theType

    elif peek.kind == Tok.U8:

        junk = _next_parse_token()

        theType = NU8Type(peek.lineNr, peek.rowNr)

        return theType

    elif peek.kind == Tok.U16:

        junk = _next_parse_token()

        theType = NU16Type(peek.lineNr, peek.rowNr)

        return theType

    elif peek.kind == Tok.U32:

        junk = _next_parse_token()

        theType = NU32Type(peek.lineNr, peek.rowNr)

        return theType

    elif peek.kind == Tok.U64:

        junk = _next_parse_token()

        theType = NU64Type(peek.lineNr, peek.rowNr)

        return theType

    elif peek.kind == Tok.USIZE:

        junk = _next_parse_token()

        theType = NUSizeType(peek.lineNr, peek.rowNr)

        return theType

    elif peek.kind == Tok.F32:

        junk = _next_parse_token()

        theType = NF32Type(peek.lineNr, peek.rowNr)

        return theType

    elif peek.kind == Tok.F64:

        junk = _next_parse_token()

        theType = NF64Type(peek.lineNr, peek.rowNr)

        return theType

    elif peek.kind == Tok.NILTYPE:

        junk = _next_parse_token()

        theType = NNilType(peek.lineNr, peek.rowNr)

        return theType

    elif peek.kind == Tok.BOOL:

        junk = _next_parse_token()

        theType = NBoolType(peek.lineNr, peek.rowNr)
        
        return theType
    
    elif peek.kind == Tok.IDENTIFIER:

        if _peek_parse_token(1).kind == Tok.LCURLYBRACKET:
            return _parse_struct_type()
    

        identifier1 = _parse_identifier()
        if identifier1 is None: 
            return None             # unnecessary check, låt stå

        peek2 = _peek_parse_token(0)

        if peek2.kind == Tok.LPAREN:

            junk = _next_parse_token()     # eat past the (

            params = _parse_type_list()
            if params is None: 
                return None

            tok = _next_parse_token()

            if tok.kind == Tok.RPAREN:

                parametrizedType = NParametrizedIdentifierType(peek.lineNr, peek.rowNr, None, identifier1, params)

                return parametrizedType

            else:

                util.log_error(tok.lineNr, tok.rowNr, "Expected \')\', found something else.")
                return None

            
        elif peek2.kind == Tok.DOUBLEPERIOD:

            junk = _next_parse_token()  # eat the ..

            identifier2 = _parse_identifier()
            if identifier2 is None:
                return None

            peek4 = _peek_parse_token(0) 

            if peek4.kind == Tok.LPAREN:

                junk = _next_parse_token()   # eat the (    

                params = _parse_type_list()
                if params is None:
                    return None

                tok = _next_parse_token()

                if tok.kind == Tok.RPAREN:

                    parametrizedType = NParametrizedIdentifierType(peek.lineNr, peek.rowNr, identifier1, identifier2, params)

                    return parametrizedType

                else:

                    util.log_error(tok.lineNr, tok.rowNr, "Expected ')', found something else.")
                    return None

            else:
                
                return NIdentifierType(peek.lineNr, peek.rowNr, identifier1, identifier2)

        else:

            identifierType = NIdentifierType(peek.lineNr, peek.rowNr, None, identifier1)

            return identifierType

        
        
    elif peek.kind == Tok.ARR:

        return _parse_array_type()
            
    elif peek.kind == Tok.FUN:

        return _parse_fun_type_eager() 

    elif peek.kind == Tok.LPAREN: 

        junk = _next_parse_token()    # go past the (

        aType = _parse_type() 
        if aType is None: 
            return None

        tok = _next_parse_token() 

        if tok.kind == Tok.RPAREN:

            return aType

        else:

            util.log_error(tok.lineNr, tok.rowNr, "Expected a ')', found something else. #3")
            return None

            

    else:

        util.log_error(peek.lineNr, peek.rowNr, "Expected a type, found something else.")
        return None    

    


        



    

##########################################################################################
######                       EXPRESSIONS                                     #############
##########################################################################################





##################### EXPRESSION PEEKING ##################################################    


def _peek_past_argument_list(peekStart, displayErrorMessagesFlag):

    thePeekStart = peekStart

    while True:

        peek = _peek_parse_token(thePeekStart)

        if peek.kind == Tok.IDENTIFIER:

            peek2 = _peek_parse_token(thePeekStart + 1)

            if peek2.kind == Tok.ASSIGNMENTOPERATOR:

                newPeekStart = _peek_past_expression(thePeekStart + 2, displayErrorMessagesFlag)
                if newPeekStart == -1: 
                    return -1

                peek3 = _peek_parse_token(newPeekStart)

                if peek3.kind == Tok.COMMA:

                    thePeekStart = newPeekStart + 1
                    continue

                else:

                    return newPeekStart

                

            else:

                newPeekStart = _peek_past_expression(thePeekStart, displayErrorMessagesFlag)
                if newPeekStart == -1: 
                    return -1

                peek3 = _peek_parse_token(newPeekStart)

                if peek3.kind == Tok.COMMA:

                    thePeekStart = newPeekStart + 1
                    continue

                else:

                    return newPeekStart

                

            

        elif peek.kind == Tok.REF:
            
            peek2 = _peek_parse_token(thePeekStart + 1)

            if peek2.kind == Tok.IDENTIFIER:

                peek3 = _peek_parse_token(thePeekStart + 2)

                if peek3.kind == Tok.ASSIGNMENTOPERATOR: # named ref argument

                    newPeekStart = _peek_past_expression_inside_infix(thePeekStart + 3, displayErrorMessagesFlag) # lvalue
                    if newPeekStart == -1: 
                        return -1

                    peek4 = _peek_parse_token(newPeekStart)

                    if peek4.kind == Tok.COMMA:

                        thePeekStart = newPeekStart + 1
                        continue

                    else:

                        return newPeekStart

                    

                else:   # ordinary identifier lvalue

                    newPeekStart = _peek_past_expression_inside_infix(thePeekStart + 1, displayErrorMessagesFlag)  # lvalue
                    if newPeekStart == -1: 
                        return -1

                    peek4 = _peek_parse_token(newPeekStart)

                    if peek4.kind == Tok.COMMA:

                        thePeekStart = newPeekStart + 1
                        continue

                    else:

                        return newPeekStart

                    

                

            else:    # ordinary identifier lvalue

                newPeekStart = _peek_past_lvalue(thePeekStart + 1, displayErrorMessagesFlag)   # lvalue  
                if newPeekStart == -1:
                    return -1

                peek3 = _peek_parse_token(newPeekStart)

                if peek3.kind == Tok.COMMA:

                    thePeekStart = newPeekStart + 1
                    continue

                else:

                    return newPeekStart

                

            

        elif peek.kind == Tok.RPAREN:

            return thePeekStart

        else:

            newPeekStart = _peek_past_expression(thePeekStart, displayErrorMessagesFlag)
            if newPeekStart == -1: 
                return -1

            peek2 = _peek_parse_token(newPeekStart)

            if peek2.kind == Tok.COMMA:

                thePeekStart = newPeekStart + 1
                continue

            else:

                return newPeekStart

            






def _peek_past_post_expressions_if_any(peekStart, displayErrorMessagesFlag):

    peek = _peek_parse_token(peekStart)

    if peek.kind == Tok.LSQUAREBRACKET:

        newPeekStart = _peek_past_expression(peekStart + 1, displayErrorMessagesFlag)
        if newPeekStart == -1: 
            return -1

        peek2 = _peek_parse_token(newPeekStart)

        if peek2.kind == Tok.RSQUAREBRACKET:

            return _peek_past_post_expressions_if_any(newPeekStart + 1, displayErrorMessagesFlag)

        else:

            util.maybe_log_error(peek2.lineNr, peek2.rowNr, "Expected a ']', found something else.", displayErrorMessagesFlag)
            return -1

        

    elif peek.kind == Tok.DOUBLESINGLEQUOTE or peek.kind == Tok.TRIPLEPERIOD:

        peekStart3 = _peek_past_type(peekStart + 1, displayErrorMessagesFlag)
        if peekStart3 == -1: 
            return -1

        return _peek_past_post_expressions_if_any(peekStart3, displayErrorMessagesFlag)

    elif peek.kind == Tok.PERIOD:

        peek2 = _peek_parse_token(peekStart + 1)

        if peek2.kind == Tok.IDENTIFIER:

            return _peek_past_post_expressions_if_any(peekStart + 2, displayErrorMessagesFlag)

        else:

            util.maybe_log_error(peek2.lineNr, peek2.rowNr, "Expected an identifier after '.', found something else.", displayErrorMessagesFlag)
            return -1


    else:

        return peekStart

    





def _peek_past_array_expression_inside_individual_values(peekStart, displayErrorMessagesFlag):  # expects at least one value

    thePeekStart = peekStart

    while True:

        newPeekStart = _peek_past_expression(thePeekStart, displayErrorMessagesFlag)
        if newPeekStart == -1: 
            return -1

        peek = _peek_parse_token(newPeekStart)

        if peek.kind == Tok.COMMA:

            thePeekStart = newPeekStart + 1
            continue

        else:
        
            return newPeekStart

        

    


def _peek_past_array_expression_inside(peekStart, displayErrorMessagesFlag):

    peek = _peek_parse_token(peekStart)

    if peek.kind == Tok.RSQUAREBRACKET:

        return peekStart   # don't eat past the ]

    elif peek.kind == Tok.TRASH or peek.kind == Tok.UNINITIALIZED:

        newPeekStart = _peek_past_expression(peekStart + 1, displayErrorMessagesFlag)
        if newPeekStart == -1: 
            return -1

        peek2 = _peek_parse_token(newPeekStart)

        if peek2.kind == Tok.RSQUAREBRACKET:

            return newPeekStart  # don't eat past the ]

        else:

            util.maybe_log_error(peek2.lineNr, peek2.rowNr, "Expected a ']', found something else.", displayErrorMessagesFlag)
            return -1

        

    else:

        newPeekStart = _peek_past_expression(peekStart, displayErrorMessagesFlag)
        if newPeekStart == -1: 
            return -1

        peek2 = _peek_parse_token(newPeekStart)

        if peek2.kind == Tok.COMMA:

            return _peek_past_array_expression_inside_individual_values(newPeekStart + 1, displayErrorMessagesFlag)

        elif peek2.kind == Tok.REPEAT:

            peekStart3 = _peek_past_expression(newPeekStart + 1, displayErrorMessagesFlag)
            if peekStart3 == -1:
                return -1

            peek3 = _peek_parse_token(peekStart3)

            if peek3.kind == Tok.RSQUAREBRACKET:

                return peekStart3    # don't eat past the ]

            else:

                util.maybe_log_error(peek3.lineNr, peek3.rowNr, "Expected a ']', found something else.", displayErrorMessagesFlag)
                return -1

            

        elif peek2.kind == Tok.RSQUAREBRACKET:

            return newPeekStart    # don't eat past the ]

        else:

            util.maybe_log_error(peek2.lineNr, peek2.rowNr, "Expected a ',' or a ';' or a ']', found something else.", displayErrorMessagesFlag)
            return -1

        

    




def _peek_past_struct_expression_inside(peekStart, displayErrorMessagesFlag):

    thePeekStart = peekStart

    while True:

        peek = _peek_parse_token(thePeekStart)

        if peek.kind == Tok.IDENTIFIER:

            peek2 = _peek_parse_token(thePeekStart + 1)
            
            if peek2.kind == Tok.ASSIGNMENTOPERATOR:

                newPeekStart = _peek_past_expression(thePeekStart + 2, displayErrorMessagesFlag)
                if newPeekStart == -1: 
                    return -1
                
                thePeekStart = newPeekStart
                
                    
                continue

            else:

                util.maybe_log_error(peek2.lineNr, peek2.rowNr, "Expected an '=', found something else.", displayErrorMessagesFlag)
                return -1

            

        else:

            return thePeekStart

        

    




def _peek_past_expression_inside_infix(peekStart, displayErrorMessagesFlag):

    peek = _peek_parse_token(peekStart)

    if peek.kind == Tok.LPAREN:

        newPeekStart = _peek_past_expression(peekStart + 1, displayErrorMessagesFlag)
        if newPeekStart == -1:
            return -1

        peek2 = _peek_parse_token(newPeekStart)

        if peek2.kind == Tok.RPAREN:

            return _peek_past_post_expressions_if_any(newPeekStart + 1, displayErrorMessagesFlag)

        else:

            util.log_error(peek2.lineNr, peek2.rowNr, "Expected a ')', found something else.", displayErrorMessagesFlag)
            return -1

        

    elif peek.kind == Tok.MINUS or peek.kind == Tok.EXCLAMATION:

        return _peek_past_expression_inside_infix(peekStart + 1, displayErrorMessagesFlag)

    elif peek.kind == Tok.NILTYPE and _peek_parse_token(1).kind == Tok.LCURLYBRACKET and _peek_parse_token(2).kind == Tok.RCURLYBRACKET:

        return _peek_past_post_expressions_if_any(peekStart + 3, displayErrorMessagesFlag)

    elif (peek.kind == Tok.TRUE or peek.kind == Tok.FALSE or 
                peek.kind == Tok.INTEGER or peek.kind == Tok.FLOAT or peek.kind == Tok.STRING or
                peek.kind == Tok.END):

        return _peek_past_post_expressions_if_any(peekStart + 1, displayErrorMessagesFlag)

    elif peek.kind == Tok.IDENTIFIER:

        peek2 = _peek_parse_token(peekStart + 1)
        
        if peek2.kind == Tok.DOUBLEPERIOD:

            peek3 = _peek_parse_token(peekStart + 2)

            if peek3.kind == Tok.IDENTIFIER:

                peek6 = _peek_parse_token(peekStart + 3)

                if peek6.kind == Tok.LPAREN:   # function call paranentheses...!

                    newPeekStart = _peek_past_argument_list(peekStart + 4, displayErrorMessagesFlag)
                    if newPeekStart == -1: 
                        return -1

                    peek5 = _peek_parse_token(newPeekStart)

                    if peek5.kind == Tok.RPAREN:

                        return _peek_past_post_expressions_if_any(newPeekStart + 1, displayErrorMessagesFlag)

                    else:                        

                        util.maybe_log_error(peek5.lineNr, peek5.rowNr, "Expected a ')' after argument list, found something else.", displayErrorMesssagesFlag)
                        return None

                else:

                    return _peek_past_post_expressions_if_any(peekStart + 3, displayErrorMessagesFlag)

            else:

                util.maybe_log_error(peek3.lineNr, peek3.rowNr, "Expected an identifier after doubleperiod.", displayErrorMessagesFlag)
                return -1


        elif peek2.kind == Tok.LCURLYBRACKET:

            newPeekStart = _peek_past_struct_expression_inside(peekStart + 2, displayErrorMessagesFlag)
            if newPeekStart == -1:
                return -1

            peek6 = _peek_parse_token(newPeekStart)

            if peek6.kind == Tok.RCURLYBRACKET:

                return _peek_past_post_expressions_if_any(newPeekStart + 1, displayErrorMessagesFlag)

            else:

                util.maybe_log_error(peek6.lineNr, peek6.rowNr, "Expected a '}', found something else.", displayErrorMessagesFlag)
                return -1

        elif peek2.kind == Tok.LPAREN:     # function call paranentheses...!

            newPeekStart = _peek_past_argument_list(peekStart + 2, displayErrorMessagesFlag)
            if newPeekStart == -1:
                return -1
            
            peek5 = _peek_parse_token(newPeekStart)

            if peek5.kind == Tok.RPAREN:

                return _peek_past_post_expressions_if_any(newPeekStart + 1, displayErrorMessagesFlag)

            else:                        

                util.maybe_log_error(peek5.lineNr, peek5.rowNr, "Expected a ')' after argument list, found something else.", displayErrorMesssagesFlag)
                return None
            

        else:

            return _peek_past_post_expressions_if_any(peekStart + 1, displayErrorMessagesFlag)

        

    elif peek.kind == Tok.LSQUAREBRACKET:

        newPeekStart = _peek_past_array_expression_inside(peekStart + 1, displayErrorMessagesFlag)
        if newPeekStart == -1: 
            return -1

        peek2 = _peek_parse_token(newPeekStart)

        if peek2.kind == Tok.RSQUAREBRACKET:

            return _peek_past_post_expressions_if_any(newPeekStart + 1, displayErrorMessagesFlag)

        else:

            util.maybe_log_error(peek2.lineNr, peek2.rowNr, "Expected a ']', found something else.", displayErrorMessagesFlag)
            return -1



    elif peek.kind == Tok.VBOX:

        peek44444 = _peek_parse_token()
        if peek44444.kind != Tok.SLASH:
            util.maybe_log_error(peek44444.lineNr, peek44444.rowNr, "Expected '/' here.", displayErrorMessagesFlag)
            return -1

        newPeekStart = peek_past_expression(peekStart + 2, displayErrorMessagesFlag)
        if newPeekStart is None:
            return None

        peek2 = _peek_parse_token(newPeekStart, displayErrorMessagesFlag)
        
        if peek2.kind == Tok.BACKSLASH:

            return _peek_past_post_expressions_if_any(newPeekStart + 1, displayErrorMessagesFlag)

        else:
            util.maybe_log_error(peek2.lineNr, peek2.rowNr, "Expected a backslash, found something else. #80808", displayErrorMessagesFlag)
            return -1

    else:

        util.maybe_log_error(peek.lineNr, peek.rowNr, "Expected an expression, found something else. #11111", displayErrorMessagesFlag)
        return -1

 





def _peek_past_infix_if_any(peekStart, displayErrorMessagesFlag):

    thePeekStart = peekStart

    while True:

        peek = _peek_parse_token(thePeekStart)

        if (peek.kind == Tok.ANDSYMBOL or peek.kind == Tok.ORSYMBOL or
            peek.kind == Tok.EQUALS or
            peek.kind == Tok.EQUALSNOT or
            peek.kind == Tok.GREATERTHAN or
            peek.kind == Tok.LESSTHAN or
            peek.kind == Tok.GREATERTHANOREQUALS or
            peek.kind == Tok.LESSTHANOREQUALS or
            peek.kind == Tok.PLUS or
            peek.kind == Tok.MINUS or
            peek.kind == Tok.STAR or
            peek.kind == Tok.SLASH or
            peek.kind == Tok.PERCENT
        ):

            thePeekStart = _peek_past_expression_inside_infix(thePeekStart + 1, displayErrorMessagesFlag)

            continue

        elif peek.kind == Tok.BACKTICK:

            peek2 = _peek_parse_token(thePeekStart + 1)

            if peek2.kind == Tok.IDENTIFIER:      # (NOTE: We could actually do full expressions here, but no real use case though...)

                peek3 = _peek_parse_token(thePeekStart + 2)

                if peek3.kind == Tok.BACKTICK: 

                    thePeekStart = _peek_past_expression_inside_infix(thePeekStart + 3, displayErrorMessagesFlag)
                    
                    continue

                elif peek3.kind == Tok.DOUBLEPERIOD:

                    peek4 = _peek_parse_token(thePeekStart + 3)

                    if peek4.kind == Tok.IDENTIFIER:

                        peek5 = _peek_parse_token(thePeekStart + 4)

                        if peek5.kind == TOK_BACKTICK:

                            thePeekStart = _peek_past_expression_inside_infix(thePeekStart + 5, displayErrorMessagesFlag)
                            if thePeekStart == -1: 
                                return -1

                            continue

                        else:

                            util.maybe_log_error(peek5.lineNr, peek5.rowNr, "Expected a matching backtick, found something else. #76", displayErrorMessagesFlag)
                            return -1

                        

                    else:

                        util.maybe_log_error(peek4.lineNr, peek4.rowNr, "Expected an identifier after doubleperiod, found something else. #0", displayErrorMessagesFlag)
                        return -1

                    

                else:

                    util.maybe_log_error(peek2.lineNr, peek2.rowNr, "Expected a matching backtick (or a doubleperiod), found something else. #2", displayErrorMessagesFlag)
                    return -1            

                
            
            else:

                util.maybe_log_error(peek2.lineNr, peek2.rowNr, "Expected an identifier, found something else. #489", displayErrorMessagesFlag)
                return -1

            

        else:

            return thePeekStart






def _peek_past_expression_list(peekStart, displayErrorMessagesFlag):     # expects at least 1 expr in the comma-separated list!

    newPeekStart = _peek_past_expression(peekStart, displayErrorMessagesFlag)

    thePeekStart = newPeekStart

    while True:

        peek2 = _peek_parse_token(thePeekStart)

        if peek2.kind == Tok.COMMA:

            newPeekStart2 = _peek_past_expression(thePeekStart + 1, displayErrorMessagesFlag)
            if newPeekStart2 == -1:
                return -1
            
            thePeekStart = newPeekStart2

            continue

        else:
    
            return thePeekStart

                

        

def _peek_past_SWITCH_cases_if_any(peekStart, displayErrorMessagesFlag):
    
    thePeekStart = peekStart

    while True:

        peek = _peek_parse_token(thePeekStart)

        if peek.kind == Tok.CASEUPPERCASE:

            newPeekStart = _peek_past_expression_list(thePeekStart + 1, displayErrorMessagesFlag)
            if newPeekStart == -1:
                return -1

            peek88 = _peek_parse_token(newPeekStart)
            if peek88.kind != Tok.TILDE:
                util.maybe_log_error(peek88.lineNr, peek88.rowNr, "Expected a '~' here.", displayErrorMessagesFlag)
                return -1

            newPeekStart2 = _peek_past_expression(newPeekStart + 1, displayErrorMessagesFlag)
            if newPeekStart == -1:
                return -1

            thePeekStart = newPeekStart2

            continue

        else:   
            return thePeekStart


   

def _peek_past_CONTENTTYPE_cases_if_any(peekStart, displayErrorMessagesFlag):

    thePeekStart = peekStart

    while True:

        peek = _peek_parse_token(thePeekStart)

        if peek.kind == Tok.CASEUPPERCASE:

            newPeekStart = _peek_past_type_list(thePeekStart + 1, displayErrorMessagesFlag)
            if newPeekStart == -1:
                return -1

            peek88 = _peek_parse_token(newPeekStart)
            if peek88.kind != Tok.TILDE:
                util.maybe_log_error(peek88.lineNr, peek88.rowNr, "Expected a '~' here.", displayErrorMessagesFlag)
                return -1

            newPeekStart2 = _peek_past_expression(newPeekStart + 1, displayErrorMessagesFlag)
            if newPeekStart == -1:
                return -1

            thePeekStart = newPeekStart2
                
            continue

        else:
            return thePeekStart





def _peek_past_expression(peekStart, displayErrorMessagesFlag):

    peek = _peek_parse_token(peekStart)
     
    if peek.kind == Tok.IFUPPERCASE:

        newPeekStart1 = _peek_past_expression(peekStart + 1, displayErrorMessagesFlag)
        if newPeekStart1 == -1:
            return -1

        peek88 = _peek_parse_token(newPeekStart1)
        if peek88.kind != Tok.TILDE:
            util.maybe_log_error(peek88.lineNr, peek88.rowNr, "Expected a '~' here.", displayErrorMessagesFlag)
            return -1

        newPeekStart2 = _peek_past_expression(newPeekStart1 + 1, displayErrorMessagesFlag)
        if newPeekStart2 == -1:
            return -1

        peek2 = _peek_parse_token(newPeekStart2)

        if peek2.kind == Tok.ELSEUPPERCASE:

            peek88 = _peek_parse_token(newPeekStart2 + 1)
            if peek88.kind != Tok.TILDE:
                util.maybe_log_error(peek88.lineNr, peek88.rowNr, "Expected a '~' here.", displayErrorMessagesFlag)
                return -1

            newPeekStart3 = _peek_past_expression(newPeekStart2 + 2, displayErrorMessagesFlag)
            if newPeekStart3 == -1:
                return -1

            return newPeekStart3
           

        else:
            util.maybe_log_error(peek2.lineNr, peek2.rowNr, "Expected 'ELSE', found something -- else. #722", displayErrorMessagesFlag)
            return -1

    elif peek.kind == Tok.SWITCHUPPERCASE:

        newPeekStart1 = _peek_past_expression(peekStart + 1, displayErrorMessagesFlag)
        if newPeekStart1 == -1:
            return 1

        newPeekStart2 = _peek_past_SWITCH_cases_if_any(newPeekStart1, displayErrorMessagesFlag)
        if newPeekStart2 == -1:
            return -1

        peek2 = _peek_parse_token(newPeekStart2)
        
        if peek2.kind == Tok.DEFAULTUPPERCASE:

            peek88 = _peek_parse_token(newPeekStart2 + 1)
            if peek88.kind != Tok.TILDE:
                util.maybe_log_error(peek88.lineNr, peek88.rowNr, "Expected a '~' here.", displayErrorMessagesFlag)
                return -1

            newPeekStart3 = _peek_past_expression(newPeekStart2 + 2, displayErrorMessagesFlag)
            if newPeekStart3 == -1:
                return -1

            return newPeekStart3
            
        
        else:
            util.maybe_log_error(peek2.lineNr, peek2.rowNr, "Expected 'DEFAULT', found something else. #707072")    
            return -1

    elif peek.kind == Tok.CONTENTTYPEUPPERCASE:
   
        newPeekStart1 = _peek_past_expression(peekStart + 1, displayErrorMessagesFlag)
        if newPeekStart1 == -1:
            return -1

        newPeekStart2 = _peek_past_CONTENTTYPE_cases_if_any(newPeekStart1, displayErrorMessagesFlag)
        if newPeekStart2 == -1:
            return -1

        peek2 = _peek_parse_token(newPeekStart2)

        if peek2.kind == Tok.DEFAULTUPPERCASE:

            peek88 = _peek_parse_token(newPeekStart2 + 1)
            if peek88.kind != Tok.TILDE:
                util.maybe_log_error(peek88.lineNr, peek88.rowNr, "Expected a '~' here.", displayErrorMessagesFlag)
                return -1    

            newPeekStart3 = _peek_past_expression(newPeekStart2 + 2, displayErrorMessagesFlag)
            if newPeekStart3 == -1:
                return -1

            return newPeekStart3
        
        else:
            util.maybe_log_error(peek2.lineNr, peek2.rowNr, "Expected 'DEFAULT', found something else. #707072", displayErrorMessagesFlag)    
            return -1


    else:

        newPeekStart = _peek_past_expression_inside_infix(peekStart, displayErrorMessagesFlag)
        if newPeekStart == -1: 
            return -1

        return _peek_past_infix_if_any(newPeekStart, displayErrorMessagesFlag)

    




def _peek_past_lvalue_postfix_if_any(peekStart, displayErrorMessagesFlag):

    peek = _peek_parse_token(peekStart)

    if peek.kind == Tok.LSQUAREBRACKET:

        newPeekStart = _peek_past_expression(peekStart + 1, displayErrorMessagesFlag)
        if newPeekStart == -1:
            return -1

        peek2 = _peek_parse_token(newPeekStart)

        if peek2.kind == Tok.RSQUAREBRACKET:

            return _peek_past_lvalue_postfix_if_any(newPeekStart + 1, displayErrorMessagesFlag)

        else:

            util.maybe_log_error(peek2.lineNr, peek2.rowNr, "Expected a ']', found something else. #587", displayErrorMessagesFlag)
            return -1

        

    elif peek.kind == Tok.PERIOD:

        peek2 = _peek_parse_token(peekStart + 1)

        if peek2.kind == Tok.IDENTIFIER:

            return _peek_past_lvalue_postfix_if_any(peekStart + 2, displayErrorMessagesFlag)

        else:

            util.maybe_log_error(peek2.lineNr, peek2.rowNr, "Expected an identifier after dot operator. #79", displayErrorMessagesFlag)
            return -1

        

    elif peek.kind == Tok.TRIPLEPERIOD or peek.kind == Tok.DOUBLESINGLEQUOTE:

        newPeekStart = _peek_past_type(peekStart + 1, displayErrorMessagesFlag)
        if newPeekStart == -1: 
            return -1

        return _peek_past_lValue_postfix_if_any(newPeekStart, displayErrorMessagesFlag)


    else:

        return peekStart

    




def _peek_past_lvalue(peekStart, displayErrorMessagesFlag):

    peek = _peek_parse_token(peekStart)

    if peek.kind == Tok.LPAREN:

        newPeekStart = _peek_past_lvalue(peekStart + 1, displayErrorMessagesFlag)
        if newPeekStart == -1: 
            return -1

        peek3 = _peek_parse_token(newPeekStart)

        if peek3.kind == Tok.RPAREN:

            return _peek_past_lvalue_postfix_if_any(newPeekStart + 1, displayErrorMessagesFlag)

        else:

            util.maybe_log_error(peek3.lineNr, peek3.rowNr, "Expected a ')' here. #11820", displayErrorMessagesFlag)
            return -1

        

    elif peek.kind == Tok.IDENTIFIER:

        peek2 = _peek_parse_token(peekStart + 1)

        if peek2.kind == Tok.DOUBLEPERIOD:

            peek3 = _peek_parse_token(peekStart + 2)

            if peek3.kind == Tok.IDENTIFIER:

                return _peek_past_lvalue_postfix_if_any(peekStart + 3, displayErrorMessagesFlag)

            else:

                util.maybe_log_error(peek3.lineNr, peek3.rowNr, "Expected an identifier after doubleperiod, found something else. #999", displayErrorMessagesFlag)
                return -1

            

        else:

            return _peek_past_lvalue_postfix_if_any(peekStart + 1, displayErrorMessagesFlag)

        

    else:

        util.maybe_log_error(peek.lineNr, peek.rowNr, "Not a valid lValue! #77777", displayErrorMessagesFlag)
        return -1

    


######################## EXPRESSION PARSING #######################################################



def _parse_integer(isNegative):

    tok = _next_parse_token()

    if tok.kind == Tok.INTEGER:

        return NIntegerExpression(tok.lineNr, tok.rowNr, tok.tokString, isNegative)

    else:

        util.log_error(tok.lineNr, tok.rowNr, "Expected an integer, found something else.")
        return None





def _parse_float(isNegative):

    tok = _next_parse_token()

    if tok.kind == Tok.FLOAT:

        return NFloatingPointNumberExpression(tok.lineNr, tok.rowNr, tok.tokString, isNegative)

    else:

        util.log_error(tok.lineNr, tok.rowNr, "Expected a floating point number, found something else.")
        return None



  
def _parse_string_expression():

    tok = _next_parse_token()

    if tok.kind == Tok.STRING:

        return NStringExpression(tok.lineNr, tok.rowNr, tok.tokString)

    else:

        util.log_error(tok.lineNr, tok.rowNr, "Expected a string, found something else.")
        return None        

    




def _parse_argument_list():

    util.log_debug("ARGS LIST")

    result = [] # empty to begin with

    while True:

        peek = _peek_parse_token(0)

        if peek.kind == Tok.IDENTIFIER:

            peek2 = _peek_parse_token(1)

            if peek2.kind == Tok.ASSIGNMENTOPERATOR:   # named argument

                argName = _parse_identifier()
                if argName is None: 
                    return None     # should probably not happen since we peeked

                junk = _next_parse_token()   # eat past the =

                argExpression = _parse_expression()
                if argExpression is None: 
                    return None

                arg = NNormalArg(peek.lineNr, peek.rowNr, argName, argExpression)
                result.append(arg)    

                peek3 = _peek_parse_token(0)

                if peek3.kind == Tok.COMMA:

                    junk = _next_parse_token() # eat past the ,
                    
                    continue

                else:

                    return result

                

            else:  # no named argument

                argExpression = _parse_expression()
                if argExpression is None: 
                    return None

                arg = NNormalArg(peek.lineNr, peek.rowNr, None, argExpression)
                result.append(arg)

                peek3 = _peek_parse_token(0)

                if peek3.kind == Tok.COMMA:

                    junk = _next_parse_token()  # eat past the ,

                    continue

                else:

                    return result

                

        elif peek.kind == Tok.REF:

            peek2 = _peek_parse_token(1)

            if peek2.kind == Tok.IDENTIFIER:

                peek3 = _peek_parse_token(2)

                if peek3.kind == Tok.ASSIGNMENTOPERATOR: # named ref argument

                    junk = _next_parse_token()  # eat past ref

                    argName = _parse_identifier()
                    if argName is None:
                        return None

                    junk = _next_parse_token()   # eat past =

                    lValueContainer = _parse_lvalue()
                    if lValueContainer is None: 
                        return None

                    refArg = NRefArg(peek.lineNr, peek.rowNr, argName, lValueContainer)

                    result.append(refArg)

                    peek4 = _peek_parse_token(0)

                    if peek4.kind == Tok.COMMA:

                        junk = _next_parse_token()    # eat past the ,                       

                        continue

                    else:

                        return result

                    

                else:   # ordinary identifier lvalue

                    util.log_debug("TJOOOO")

                    junk = _next_parse_token()    # eat past 'ref'

                    lValueContainer = _parse_lvalue()
                    if lValueContainer is None: 
                        return None

                    refArg = NRefArg(peek.lineNr, peek.rowNr, None, lValueContainer)

                    result.append(refArg)

                    peek4 = _peek_parse_token(0)

                    if peek4.kind == Tok.COMMA:

                        junk = _next_parse_token()   # eat past the ,                       

                        continue

                    else:

                        return result



            else:   # ordinary identifier lvalue

                util.log_debug("HEJJJJJJ")

                junk = _next_parse_token()   # eat past 'ref'

                lValueContainer = _parse_lvalue()
                if lValueContainer is None: 
                    return None

                refArg = NRefArg(peek.lineNr, peek.rowNr, None, lValueContainer)

                result.append(refArg)

                peek3 = _peek_parse_token(0)

                if peek3.kind == Tok.COMMA:

                    junk = _next_parse_token()  # eat past the ,                    

                    continue

                else:

                    return result

              

        elif peek.kind == Tok.RPAREN:

            return result

        else:   # no named argument

            argExpression = _parse_expression()
            if argExpression is None: 
                return None

            arg = NNormalArg(peek.lineNr, peek.rowNr, None, argExpression)
            result.append(arg)

            peek2 = _peek_parse_token(0)

            if peek2.kind == Tok.COMMA:

                junk = _next_parse_token()    # eat past the ,

                continue

            else:

                return result





def _parse_post_expressions_if_any(leftHandSide):

    peek = _peek_parse_token(0)

    if peek.kind == Tok.LSQUAREBRACKET:

        junk = _next_parse_token()   # eat past the [

        indexExpression = _parse_expression()
        if indexExpression is None:
            return None

        tok = _next_parse_token()

        if tok.kind == Tok.RSQUAREBRACKET:

            arrayIndexing = NArrayIndexing(peek.lineNr, peek.rowNr, leftHandSide, indexExpression)

            return _parse_post_expressions_if_any(arrayIndexing)

        else:

            util.log_error(tok.lineNr, tok.rowNr, "Expected a ']', found something else.")
            return None

        

    elif peek.kind == Tok.DOUBLESINGLEQUOTE:

        junk = _next_parse_token()   # eat past the ''

        theType = _parse_type()
        if theType is None: 
            return None

        typeClarifiedExpr = NTypeClarifiedExpression(peek.lineNr, peek.rowNr, leftHandSide, theType)

        return _parse_post_expressions_if_any(typeClarifiedExpr)

    elif peek.kind == Tok.TRIPLEPERIOD:

        junk = _next_parse_token()  # eat past the ...

        theType = _parse_type()        
        if theType is None: 
            return None

        ortypeCastExpr = NVariantBoxCastExpression(peek.lineNr, peek.rowNr, leftHandSide, theType)

        return _parse_post_expressions_if_any(ortypeCastExpr)

    elif peek.kind == Tok.PERIOD:

        junk = _next_parse_token()   # eat past the .

        fieldIdentifier = _parse_identifier()
        if fieldIdentifier is None: 
            return None

        structIndexing = NStructIndexing(peek.lineNr, peek.rowNr, leftHandSide, fieldIdentifier)

        return _parse_post_expressions_if_any(structIndexing)        

    else:

        return leftHandSide

    





def _parse_identifier_expression(keepParsingAfter):  # also parses indexings then

    identifier1 = _parse_identifier()
    if identifier1 is None:
        return None

    peek24 = _peek_parse_token(0)

    slotName = identifier1
    moduleNameOrNull = None

    if peek24.kind == Tok.DOUBLEPERIOD:
    
        junk = _next_parse_token() # eat the ..

        slot = _parse_identifier()
        if slot is None:
            return None
        else:
            moduleNameOrNull = slotName
            slotName = slot 


    indexings = []

    while True:

        peek = _peek_parse_token(0)

        if peek.kind == Tok.LSQUAREBRACKET:

            junk = _next_parse_token() # eat past the [

            indexExpression = _parse_expression()
            if indexExpression is None: 
                return None

            tok = _next_parse_token()

            if tok.kind == Tok.RSQUAREBRACKET:

                arrayIndexingIndex = NArrayIndexingIndex(peek.lineNr, peek.rowNr, indexExpression)  
                indexings.append(arrayIndexingIndex)
        
                continue

            else:
                util.log_error(tok.lineNr, tok.rowNr, "Expected a ']', found something else.")
                return None

        elif peek.kind == Tok.DOUBLESINGLEQUOTE:

            junk = _next_parse_token()   # eat past the ''

            theType = _parse_type()        
            if theType is None: 
                return None

            typeClarificationIndex = NTypeClarificationIndex(peek.lineNr, peek.rowNr, theType)
            indexings.append(typeClarificationIndex)

            continue 

        elif peek.kind == Tok.TRIPLEPERIOD:

            junk = _next_parse_token()   # eat past the ...

            theType = _parse_type()        
            if theType is None: 
                return None

            variantBoxCastIndex = NVariantBoxCastIndex(peek.lineNr, peek.rowNr, theType)
            indexings.append(variantBoxCastIndex)

            continue

        elif peek.kind == Tok.PERIOD:

            junk = _next_parse_token()   # eat the .

            ident = _parse_identifier()
            if ident is None:
                return None

            structIndex = NStructIndexingIndex(peek.lineNr, peek.rowNr, ident)
            indexings.append(structIndex)
    
            continue

        else:

            break

    
    identifierExpression = NIdentifierExpression(peek24.lineNr, peek24.rowNr, moduleNameOrNull, slotName, indexings)

    if keepParsingAfter:
        return _parse_post_expressions_if_any(identifierExpression)
    else:
        return identifierExpression







def _parse_lvalue():

    lValueExpr = _parse_identifier_expression(False)
    if lValueExpr is None:
        return None

    return NLValueContainer(lValueExpr.get_line_nr(), lValueExpr.get_row_nr(), lValueExpr)







def _parse_array_expression_inside_individual_values(
        firstExpression
    ):

    # expects at least one value

    result = []   # empty to begin with
    result.append(firstExpression)

    while True:

        individualExpr = _parse_expression()
        if individualExpr is None:
            return None

        result.append(individualExpr)

        peek = _peek_parse_token(0)

        if peek.kind == Tok.COMMA:

            junk = _next_parse_token()    # eat past the ,

            continue

        else:

            return result

        



def _parse_array_expression_inside():

    # does not eat past the ]

    peek = _peek_parse_token(0)

    if peek.kind == Tok.RSQUAREBRACKET:

        values = []  

        return NArrayExpressionIndividualValues(peek.lineNr, peek.rowNr, values)

    elif peek.kind == Tok.TRASH:

        junk = _next_parse_token()    # eat past trash

        expr = _parse_expression()
        if expr is None: 
            return None

        return NArrayExpressionNoInitialization(peek.lineNr, peek.rowNr, False, expr)

    elif peek.kind == Tok.UNINITIALIZED:

        junk = _next_parse_token()    # eat past uninitialized

        expr = _parse_expression()
        if expr is None:
            return None

        return NArrayExpressionNoInitialization(peek.lineNr, peek.rowNr, True, expr)


    else:

        expr1 = _parse_expression()
        if expr1 is None: 
            return None

        peek2 = _peek_parse_token(0)

        if peek2.kind == Tok.COMMA:

            junk = _next_parse_token()    # eat past the ,

            values = _parse_array_expression_inside_individual_values(expr1)
            if values is None: 
                return None

            return NArrayExpressionIndividualValues(peek.lineNr, peek.rowNr, values)

        elif peek2.kind == Tok.REPEAT:

            junk = _next_parse_token()   # eat past repeat

            expr2 = _parse_expression()
            if expr2 is None: 
                return None

            return NArrayExpressionRepeatedValue(peek.lineNr, peek.rowNr, expr1, expr2)

        elif peek2.kind == Tok.RSQUAREBRACKET:

            values = []
            values.append(expr1)

            return NArrayExpressionIndividualValues(peek.lineNr, peek.rowNr, values) 

        else:

            util.log_error(peek2.lineNr, peek2.rowNr, "Expected a ',' or 'repeat' or a ']', found something else.")
            return None

       

  
    


def _parse_struct_expression_inside():

    result = []    # empty to begin with

    while True:

        peek = _peek_parse_token(0)

        if peek.kind == Tok.IDENTIFIER:

            identifier = _parse_identifier()
            if identifier is None: 
                return None

            tok = _next_parse_token()

            if tok.kind == Tok.ASSIGNMENTOPERATOR:

                expr = _parse_expression()
                if expr is None: 
                    return None

                peek2 = _peek_parse_token(0)

                

                                

                post = NStructExpressionPost(peek.lineNr, peek.rowNr, identifier, expr)

                result.append(post)

                continue

            else:

                util.log_error(tok.lineNr, tok.rowNr, "Expected a '=', found something else.")
                return None

            

        else:

            return result

        


def _parse_expression_list(): # expects at least one expression!!!
    
    result = []

    expr1 = _parse_expression()
    if expr1 is None:
        return None

    result.append(expr1)

    while True:

        peek = _peek_parse_token(0)
    
        if peek.kind == Tok.COMMA:

            junk = _next_parse_token() # eat comma

            expr = _parse_expression()
            result.append(expr)

            continue

        else:
            return result

      





def _parse_SWITCH_cases_if_any():

    result = []

    while True:

        peek = _peek_parse_token(0)

        if peek.kind == Tok.CASEUPPERCASE:
    
            junk = _next_parse_token()  # eat CASE

            caseList = _parse_expression_list()
            if caseList is None:
                return None

            tok88 = _next_parse_token()
            if tok88.kind != Tok.TILDE:
                util.log_error(tok88.lineNr, tok88.rowNr, "Expected a '~' here. #7979797")
                return None

            expr = _parse_expression()
            if expr is None:
                return None

            case = NSWITCHNormalCase(peek.lineNr, peek.rowNr, caseList, expr)
            result.append(case)

            continue

        else:

            return result
        


           
def _parse_CONTENTTYPE_cases_if_any():

    result = []

    while True:

        peek = _peek_parse_token(0)

        if peek.kind == Tok.CASEUPPERCASE:

            junk = _next_parse_token()  # eat CASE

            caseList = _parse_type_list()
            if caseList is None:
                return None

            tok88 = _next_parse_token()
            if tok88.kind != Tok.TILDE:
                util.log_error(tok88.lineNr, tok88.rowNr, "Expected a '~' here.")
                return None

            expr = _parse_expression()
            if expr is None:
                return None

            case = NSWITCHNormalCase(peek.lineNr, peek.rowNr, caseList, expr)
            result.append(case)

            continue

        else:

            return result




def _parse_function_call_with_module_name(doParsePostExpressions):

    peek = _peek_parse_token(0)  # to save the lineNr and rowNr...

    moduleName = _parse_identifier()
    if moduleName is None:
        return None

    junk = _next_parse_token()    # eat the ..

    functionName = _parse_identifier()
    if functionName is None:
        return None

    junk = _next_parse_token()    # eat the (

    args = _parse_argument_list()
    if args is None:
        return None

    tok44 = _next_parse_token()

    if tok44.kind == Tok.RPAREN:

        funcIdentExpr = NIdentifierExpression(peek.lineNr, peek.rowNr, moduleName, functionName, [])

        funCallExpr = NFunctionCall(peek.lineNr, peek.rowNr, funcIdentExpr, args)

        if doParsePostExpressions:

            return _parse_post_expressions_if_any(funCallExpr)

        else:

            return funCallExpr

    else:
        util.log_error(tok44.lineNr, tok44.rowNr, "Expected a ')' after argument list, found something else.")    
        return None




def _parse_function_call_without_module_name(doParsePostExpressions):

    peek = _peek_parse_token(0)    # to save the lineNr and rowNr...

    functionName = _parse_identifier()
    if functionName is None:
        return None

    junk = _next_parse_token()    # eat the (

    args = _parse_argument_list()
    if args is None:
        return None

    tok44 = _next_parse_token()

    if tok44.kind == Tok.RPAREN:

        funcIdentExpr = NIdentifierExpression(peek.lineNr, peek.rowNr, None, functionName, [])

        funCallExpr = NFunctionCall(peek.lineNr, peek.rowNr, funcIdentExpr, args)

        if doParsePostExpressions:

            return _parse_post_expressions_if_any(funCallExpr)

        else:

            return funCallExpr

    else:
        util.log_error(tok44.lineNr, tok44.rowNr, "Expected a ')' after argument list, found something else.")    
        return None





def _parse_expression_inside_infix(): 

    util.log_debug("INSIDE INFIX")   

    peek = _peek_parse_token(0)

    if peek.kind == Tok.LPAREN:

        junk = _next_parse_token()    # go past the (

        expr = _parse_expression()
        if expr is None: 
            return None

        tok = _next_parse_token()

        if tok.kind == Tok.RPAREN:

            return _parse_post_expressions_if_any(expr)        

        else:

            util.log_error(tok.lineNr, tok.rowNr, "Expected a ')', found something else. #116")
            return None

        

    elif peek.kind == Tok.MINUS:

        junk = _next_parse_token()    # eat past the -

        peek2 = _peek_parse_token(0)

        if peek2.kind == Tok.INTEGER:

            integerExpr = _parse_integer(True)
            if integerExpr is None: 
                return None

            return _parse_post_expressions_if_any(integerExpr)        

        elif peek2.kind == Tok.FLOAT:

            floatExpr = _parse_float(True)
            if floatExpr is None: 
                return None

            return _parse_post_expressions_if_any(floatExpr)

        else:    # minus as prefix operator

            funIdentifier = NIdentifier(peek.lineNr, peek.rowNr, "-")

            functionIdentifierExpr = NIdentifierExpression(peek.lineNr, peek.rowNr, None, funIdentifier, [])

            parameterExpr = _parse_expression_inside_infix()
            if parameterExpr is None:
                return None

            parameterArg = NNormalArg(peek.lineNr, peek.rowNr, None, parameterExpr)

            argsList = []
            argsList.append(parameterArg)

            functionCallExpr = NFunctionCall(peek.lineNr, peek.rowNr, functionIdentifierExpr, argsList)

            return _parse_post_expressions_if_any(functionCallExpr)

          

    elif peek.kind == Tok.EXCLAMATION:

        junk = _next_parse_token()    # eat the !

        funIdentifier = NIdentifier(peek.lineNr, peek.rowNr, "!")

        functionIdentifierExpr = NIdentifierExpression(peek.lineNr, peek.rowNr, None, funIdentifier, [])

        parameterExpr = _parse_expression_inside_infix()
        if parameterExpr is None: 
            return None

        parameterArg = NNormalArg(peek.lineNr, peek.rowNr, None, parameterExpr)

        argsList = []
        argsList.append(parameterArg)

        functionCallExpr = NFunctionCall(peek.lineNr, peek.rowNr, functionIdentifierExpr, argsList)

        return _parse_post_expressions_if_any(functionCallExpr)

    elif peek.kind == Tok.NILTYPE and _peek_parse_token(1).kind == Tok.LCURLYBRACKET and _peek_parse_token(2).kind == Tok.RCURLYBRACKET:

        junk = _next_parse_token()   # eat the nil
        junk = _next_parse_token()   # eat the {
        junk = _next_parse_token()   # eat the }

        nilExpr = NNilExpression(peek.lineNr, peek.rowNr)

        return _parse_post_expressions_if_any(nilExpr)

    elif peek.kind == Tok.TRUE:

        junk = _next_parse_token()   # eat the true

        trueExpr = NTrueExpression(peek.lineNr, peek.rowNr)

        return _parse_post_expressions_if_any(trueExpr)

    elif peek.kind == Tok.FALSE:

        junk = _next_parse_token()   # eat the false

        falseExpr = NFalseExpression(peek.lineNr, peek.rowNr)

        return _parse_post_expressions_if_any(falseExpr)

    elif peek.kind == Tok.INTEGER:

        integer = _parse_integer(False)
        if integer is None: 
            return None     # should not happen though

        return _parse_post_expressions_if_any(integer)

    elif peek.kind == Tok.FLOAT:

        floating = _parse_float(False)
        if floating is None: 
            return None

        return _parse_post_expressions_if_any(floating)

    elif peek.kind == Tok.STRING:

        stri = _parse_string_expression()
        if stri is None:
            return None

        return _parse_post_expressions_if_any(stri)

    elif peek.kind == Tok.END:

        junk = _next_parse_token()   # eat the end

        endExpr = NEndExpression(peek.lineNr, peek.rowNr)

        return _parse_post_expressions_if_any(endExpr)

    elif peek.kind == Tok.IDENTIFIER:

        util.log_debug("IDENTIFIER INSIDE INFIX!")

        peek2 = _peek_parse_token(1)

        if peek2.kind == Tok.DOUBLEPERIOD:
  

            peek3 = _peek_parse_token(2)

            if peek3.kind == Tok.IDENTIFIER:

                peek4 = _peek_parse_token(3)

                if peek4.kind == Tok.LPAREN:

                    util.log_debug("JOJO")

                    return _parse_function_call_with_module_name(True) 
                
                else:

                    return _parse_identifier_expression(True)   # also parses post-exprs, despite the naming        

            else:
    
                util.log_error(peek3.lineNr, peek3.rowNr, "Expected an identifier after doubleperiod.")   
                return None

        elif peek2.kind == Tok.LCURLYBRACKET:

            tag = _parse_identifier()
            if tag is None:
                return None

            junk = _next_parse_token()  # eat the {

            posts = _parse_struct_expression_inside()
            if posts is None: 
                return None

            tok5 = _next_parse_token()

            if tok5.kind == Tok.RCURLYBRACKET:

                structExpr = NStructExpression(peek.lineNr, peek.rowNr, tag, posts)

                return _parse_post_expressions_if_any(structExpr)

            else:

                util.log_error(tok5.lineNr, tok5.rowNr, "Expected a '}', found something else. #80808")
                return None

        elif peek2.kind == Tok.LPAREN:

            return _parse_function_call_without_module_name(True)

        else:

            return _parse_identifier_expression(True)   # also parses post-exprs, despite the naming        

      

    elif peek.kind == Tok.LSQUAREBRACKET:

        junk = _next_parse_token()   # eat past the #[

        arrayExpr = _parse_array_expression_inside()
        if arrayExpr is None: 
            return None

        tok = _next_parse_token()

        if tok.kind == Tok.RSQUAREBRACKET:

            return _parse_post_expressions_if_any(arrayExpr)

        else:

            util.log_error(tok.lineNr, tok.rowNr, "Expected a ']', found something else.")
            return None


    
    elif peek.kind == Tok.IFUPPERCASE:

        junk = _next_parse_token()   # eat past IF

        condition = _parse_expression()
        if condition is None:
            return None

        tok88 = _next_parse_token()
        if tok88.kind != Tok.TILDE:
            util.log_error(tok88.lineNr, tok88.rowNr, "Expected a '~' here.")
            return None

        thenExpr = _parse_expression()
        if thenExpr is None:
            return None

        peek2 = _peek_parse_token(0)

        if peek2.kind == Tok.ELSEUPPERCASE:

            junk = _next_parse_token()   # eat ELSE

            tok88 = _next_parse_token()
            if tok88.kind != Tok.TILDE:
                util.log_error(tok88.lineNr, tok88.rowNr, "Expected a '~' here.")
                return None

            elseExpr = _parse_expression()
            if elseExpr is None:
                return None

            return NIFExpression(peek.lineNr, peek.rowNr, condition, thenExpr, elseExpr)    

        else:
            util.log_error(peek2.lineNr, peek2.rowNr, "Expected 'ELSE', found something -- else. #722")
            return None


    elif peek.kind == Tok.SWITCHUPPERCASE:

        junk = _next_parse_token()   # eat SWITCH

        switchValue = _parse_expression()
        if switchValue is None:
            return None

        cases = _parse_SWITCH_cases_if_any()
        if cases is None:
            return None

        peek2 = _peek_parse_token(0)

        if peek2.kind == Tok.DEFAULTUPPERCASE:

            junk = _next_parse_token()   # eat DEFAULT

            tok88 = _next_parse_token()
            if tok88.kind != Tok.TILDE:
                util.log_error(tok88.lineNr, tok88.rowNr, "Expected a '~' here. #808082")
                return None
            
            defaultExpr = _parse_expression()
            if defaultExpr is None:
                return None

            return NSWITCHExpression(peek.lineNr, peek.rowNr, switchValue, cases, defaultExpr)

        else:
            util.log_error(peek2.lineNr, peek2.rowNr, "Expected 'DEFAULT', found something else. #707072")
            return None

        

    elif peek.kind == Tok.CONTENTTYPEUPPERCASE:

        junk = _next_parse_token()    # eat CONTENTTYPE

        switchValue = _parse_expression()
        if switchValue is None:
            return None

        cases = _parse_CONTENTTYPE_cases_if_any()
        if cases is None:
            return None

        peek2 = _peek_parse_token(0)

        if peek2.kind == Tok.DEFAULTUPPERCASE:

            junk = _next_parse_token()    # eat DEFAULT

            tok88 = _next_parse_token()
            if tok88.kind != Tok.TILDE:
                util.log_error(tok88.lineNr, tok88.rowNr, "Expected a '~' here.")
                return None

            defaultExpr = _parse_expression()
            if defaultExpr is None:
                return None

            return NCONTENTTYPEExpression(peek.lineNr, peek.rowNr, switchValue, cases, defaultExpr)

        else:
            return NCONTENTTYPEExpression(peek.lineNr, peek.rowNr, switchValue, cases, None)

    elif peek.kind == Tok.VBOX:

        junk = _next_parse_token()   # eat #/

        tok22 = _next_parse_token()
        if tok22.kind != Tok.SLASH:
            util.log_error(tok22.lineNr, tok22.rowNr, "Expected '/' here.")
            return None

        expr = _parse_expression()
        if expr is None:
            return None

        tok2 = _next_parse_token()

        if tok2.kind == Tok.BACKSLASH:

            return NVariantBoxExpression(peek.lineNr, peek.rowNr, expr)

        else:
            util.log_error(tok2.lineNr, tok2.rowNr, "Expected a backslash, found something else. #7972")
            return None

    else:

        util.log_error(peek.lineNr, peek.rowNr, "Expected an expression, found something else. #280")
        return None

    







def _precedence_of_token_kind(tk):

    if tk == Tok.STAR or tk == Tok.SLASH or tk == Tok.PERCENT:

        return 70

    elif tk == Tok.PLUS or tk == Tok.MINUS:

        return 60

    elif tk == Tok.BACKTICK:    # sort of hackish

        return 50

    elif (tk == Tok.LESSTHAN or tk == Tok.GREATERTHAN or tk == Tok.LESSTHANOREQUALS or tk == Tok.GREATERTHANOREQUALS or 
              tk == Tok.EQUALSNOT or tk == Tok.EQUALS 
    ):

        return 40

    elif tk == Tok.ANDSYMBOL or tk == Tok.ORSYMBOL:

        return 30

    else:

        return -1

    




def _parse_infix_if_any(prevExprPrecedence, leftHandSide):


    # starts after a left hand side expression

    while True:        

        peek = _peek_parse_token(0)

        if _precedence_of_token_kind(peek.kind) < prevExprPrecedence:

            return leftHandSide
        

        if peek.kind == Tok.ANDSYMBOL:

            junk = _next_parse_token() # go past the &&        

            rightHandSide = _parse_expression_inside_infix()
            if rightHandSide is None: 
                return None

            peekNextInfixOperator = _peek_parse_token(0)

            if _precedence_of_token_kind(Tok.ANDSYMBOL) < _precedence_of_token_kind(peekNextInfixOperator.kind):

                rightHandSide = _parse_infix_if_any(_precedence_of_token_kind(Tok.ANDSYMBOL) + 1, rightHandSide)
                if rightHandSide is None: 
                    return None
            

            leftHandSide = NAndSymbolExpression(peek.lineNr, peek.rowNr, leftHandSide, rightHandSide) 

        elif peek.kind == Tok.ORSYMBOL:

            junk = _next_parse_token()   # go past the ||

            rightHandSide = _parse_expression_inside_infix()
            if rightHandSide is None: 
                return None

            peekNextInfixOperator = _peek_parse_token(0)

            if _precedence_of_token_kind(Tok.ORSYMBOL) < _precedence_of_token_kind(peekNextInfixOperator.kind):

                rightHandSide = _parse_infix_if_any(_precedence_of_token_kind(Tok.ORSYMBOL) + 1, rightHandSide)
                if rightHandSide is None: 
                    return None
            

            leftHandSide = NOrSymbolExpression(peek.lineNr, peek.rowNr, leftHandSide, rightHandSide)

        elif (peek.kind == Tok.EQUALS or
            peek.kind == Tok.EQUALSNOT or
            peek.kind == Tok.GREATERTHAN or
            peek.kind == Tok.LESSTHAN or
            peek.kind == Tok.GREATERTHANOREQUALS or
            peek.kind == Tok.LESSTHANOREQUALS or
            peek.kind == Tok.PLUS or
            peek.kind == Tok.MINUS or
            peek.kind == Tok.STAR or
            peek.kind == Tok.SLASH or
            peek.kind == Tok.PERCENT
        ):

            junk = _next_parse_token()    # go past the infix operator

            rightHandSide = _parse_expression_inside_infix()
            if rightHandSide is None: 
                return None

            # std::unique_ptr<NIdentifier> funIdentifier;

            if peek.kind == Tok.EQUALS:
                funIdentifier = NIdentifier(peek.lineNr, peek.rowNr, "==")
            elif peek.kind == Tok.EQUALSNOT:
                funIdentifier = NIdentifier(peek.lineNr, peek.rowNr, "!=")
            elif peek.kind == Tok.LESSTHAN:
                funIdentifier = NIdentifier(peek.lineNr, peek.rowNr, "<")
            elif peek.kind == Tok.GREATERTHAN:
                funIdentifier = NIdentifier(peek.lineNr, peek.rowNr, ">")
            elif peek.kind == Tok.GREATERTHANOREQUALS:
                funIdentifier = NIdentifier(peek.lineNr, peek.rowNr, ">=")
            elif peek.kind == Tok.LESSTHANOREQUALS:
                funIdentifier = NIdentifier(peek.lineNr, peek.rowNr, "<=")
            elif peek.kind == Tok.PLUS:
                funIdentifier = NIdentifier(peek.lineNr, peek.rowNr, "+")
            elif peek.kind == Tok.MINUS:        
                funIdentifier = NIdentifier(peek.lineNr, peek.rowNr, "-")
            elif peek.kind == Tok.STAR:
                funIdentifier = NIdentifier(peek.lineNr, peek.rowNr, "*")
            elif peek.kind == Tok.SLASH:
                funIdentifier = NIdentifier(peek.lineNr, peek.rowNr, "/")
            elif peek.kind == Tok.PERCENT:
                funIdentifier = NIdentifier(peek.lineNr, peek.rowNr, "%")
            else:

                util.log_error(peek.lineNr, peek.rowNr, "LOGICAL IMPOSSIBILITY. SHOULD NOT HAPPEN.")
                return None
                
            

            functionIdentifierExpr = NIdentifierExpression(peek.lineNr, peek.rowNr, None, funIdentifier, [])

            peekNextInfixOperator = _peek_parse_token(0);

            if _precedence_of_token_kind(peek.kind) < _precedence_of_token_kind(peekNextInfixOperator.kind):

                rightHandSide = _parse_infix_if_any(_precedence_of_token_kind(peek.kind) + 1, rightHandSide)
                if rightHandSide is None: 
                    return None
            

            parameter1Arg = NNormalArg(peek.lineNr, peek.rowNr, None, leftHandSide)    # row and line nrs are wrong here
            parameter2Arg = NNormalArg(peek.lineNr, peek.rowNr, None, rightHandSide)   # same here

            argsList = []
            argsList.append(parameter1Arg)
            argsList.append(parameter2Arg)

            leftHandSide = NFunctionCall(peek.lineNr, peek.rowNr, functionIdentifierExpr, argsList)

        elif peek.kind == Tok.BACKTICK:

            peek2 = _peek_parse_token(1)

            if peek2.kind == Tok.IDENTIFIER:

                peek3 = _peek_parse_token(2)

                if peek3.kind == Tok.DOUBLEPERIOD:

                    peek4 = _peek_parse_token(3)
    
                    if peek4.kind == Tok.IDENTIFIER:

                        peek5 = _peek_parse_token(4)

                        if peek5.kind == Tok.BACKTICK:

                            peek6 = _peek_parse_token(5)
                        
                           
                            junk = _next_parse_token()    # past the backtick

                            moduleIdentifier = _parse_identifier()
                            if moduleIdentifier is None: 
                                return None

                            junk = _next_parse_token()    # past the ..

                            identifier2 = _parse_identifier()
                            if identifier2 is None: 
                                return None

                            junk = _next_parse_token()    # past the matching backtick

                            rhs = _parse_expression_inside_infix()
                            if rhs is None: 
                                return None

                            peekNextInfixOperator = _peek_parse_token(0)

                            if _precedence_of_token_kind(Tok.BACKTICK) < _precedence_of_token_kind(peekNextInfixOperator.kind):

                                rhs = _parse_infix_if_any(_precedence_of_token_kind(Tok.BACKTICK) + 1, rhs)
                                if rhs is None: 
                                    return None
                            

                            rhsArg = NNormalArg(rhs.get_line_nr(), rhs.get_row_nr(), None, rhs)

                            parameter1Arg = NNormalArg(peek.lineNr, peek.rowNr, None, leftHandSide)  # row and line nrs are wrong here

                            argsList = []
                            argsList.append(parameter1Arg)
                            argsList.append(rhsArg)

                            funIdentifierExpr = NIdentifierExpression(peek.lineNr, peek.rowNr, moduleIdentifier, identifier2, [])

                            leftHandSide = NFunctionCall(peek.lineNr, peek.rowNr, funIdentifierExpr, argsList)

                            

                        else:

                            util.log_error(peek5.lineNr, peek5.rowNr, "Expected a matching backtick, found something else. #80808")
                            return None

                        

                    else:

                        util.log_error(peek4.lineNr, peek4.rowNr, "Expected an identifier after doubleperiod, found something else. #80")
                        return None

                    

                elif peek3.kind == Tok.BACKTICK:

                    peek6 = _peek_parse_token(3)

                    

                    junk = _next_parse_token()    # past the backtick

                    identifier = _parse_identifier()
                    if identifier is None: 
                        return None

                    junk = _next_parse_token()   # past the matching backtick

                    rhs = _parse_expression_inside_infix()
                    if rhs is None: 
                        return None

                    peekNextInfixOperator = _peek_parse_token(0)

                    if _precedence_of_token_kind(Tok.BACKTICK) < _precedence_of_token_kind(peekNextInfixOperator.kind):

                        rhs = _parse_infix_if_any(_precedence_of_token_kind(Tok.BACKTICK) + 1, rhs)
                        if rhs is None: 
                            return None
                    

                    rhsArg = NNormalArg(rhs.get_line_nr(), rhs.get_row_nr(), None, rhs)

                    parameter1Arg = NNormalArg(peek.lineNr, peek.rowNr, None, leftHandSide)    # row and line nrs are wrong here

                    argsList = []
                    argsList.append(parameter1Arg)
                    argsList.append(rhsArg)

                    funIdentifierExpr = NIdentifierExpression(peek.lineNr, peek.rowNr, None, identifier, [])

                    leftHandSide = NFunctionCall(peek.lineNr, peek.rowNr, funIdentifierExpr, argsList)

                    

                else:

                    util.log_error(peek3.lineNr, peek3.rowNr, "Expected a backtick or doubleperiod here. #1")
                    return None

                

            else:

                util.log_error(peek2.lineNr, peek2.rowNr, "Expected an identifier after backtick, found something else. #8")
                return None

                        

        else:

            return leftHandSide

       





def _parse_expression():    

    leftExpr = _parse_expression_inside_infix()
    if leftExpr is None: 
        return None

    return _parse_infix_if_any(0, leftExpr)

    





######################################################################################
################    STATEMENT PARSING   ##############################################
######################################################################################



def _parse_block(numberOfReturnValues, functionDefinitionListToAddTo):

    first = _next_parse_token()   # eat past the :

    statements = [] 

    while True:

        peek = _peek_parse_token(0)

        if peek.kind == Tok.SEMICOLON:

            junk = _next_parse_token()  # eat past the }

            result = NBlock(first.lineNr, first.rowNr, statements)

            return result    

        else:

            statement = _parse_statement(numberOfReturnValues, functionDefinitionListToAddTo)
            if statement is None: 
                return None

            statements.append(statement)

            continue

        


def _parse_type_declaration_statement():

    tok = _next_parse_token()

    if tok.kind != Tok.TYPE:

        util.log_error(tok.lineNr, tok.rowNr, "Expected the keyword 'type' here. #28")
        return None

   

    params = []

    typeName = _parse_identifier()
    if typeName is None:
        return None

    peekParams = _peek_parse_token(0)

    if peekParams.kind == Tok.LPAREN:

        junk = _next_parse_token()   # go past (

        firstIdentifier = _parse_identifier()    # at least one param is required
        if firstIdentifier is None:
            return None

        params.append(firstIdentifier)

        while True:

            tok2 = _next_parse_token()

            if tok2.kind == Tok.RPAREN:

                break

            elif tok2.kind == Tok.COMMA:

                identifier = _parse_identifier()
                if identifier is None: 
                    return None

                params.append(identifier)

                continue 

            else:

                util.log_error(tok2.lineNr, tok2.rowNr, "Expected ')' or ',' here. #180")
                return None

        

        assignTok = _next_parse_token()

        if assignTok.kind == Tok.ASSIGNMENTOPERATOR:

            definitionType = _parse_type()
            if definitionType is None: 
                return None

            peekSemi = _peek_parse_token(0)
            
            

            

            return NTypeDeclarationWithDefinition(tok.lineNr, 
                tok.rowNr,
                typeName, 
                params, 
                definitionType
            )

        else:

            util.log_error(assignTok.lineNr, assignTok.rowNr, "Expected '=' here, found something else. #11")
            return None

       

    elif peekParams.kind == Tok.ASSIGNMENTOPERATOR:

        junk = _next_parse_token()  # go past the =

        

        definitionType = _parse_type()
        if definitionType is None:
            return None

        peekSemi = _peek_parse_token(0)
        
       

        

        return NTypeDeclarationWithDefinition(tok.lineNr, 
            tok.rowNr, 
            typeName, 
            params, 
            definitionType
        )

    else:

        util.logeError(peekParams.lineNr, peekParams.rowNr, "Expected '=' or a parameter list here. #212")
        return None

    



def _parse_switch_normal_cases(numberOfReturnValues, functionDefinitionListToAddTo):

    normalCases = []

    while True:

        peek2 = _peek_parse_token(0)

        if peek2.kind == Tok.CASE:

            junk = _next_parse_token()

            cases = _parse_expression_list()
            if cases is None:
                return None

            block = _parse_block(numberOfReturnValues, functionDefinitionListToAddTo)
            if block is None:
                return None

            normalCase = NSwitchNormalCase(peek2.lineNr, peek2.rowNr, cases, block)
            normalCases.append(normalCase)

            continue

        else:
            return normalCases


    


def _parse_contenttype_normal_cases(numberOfReturnValues, functionDefinitionListToAddTo):

    normalCases = []

    while True:

        peek2 = _peek_parse_token(0)

        if peek2.kind == Tok.CASE:

            junk = _next_parse_token()

            cases = _parse_type_list()
            if cases is None:
                return None

            block = _parse_block(numberOfReturnValues, functionDefinitionListToAddTo)
            if block is None:
                return None

            normalCase = NContenttypeNormalCase(peek2.lineNr, peek2.rowNr, cases, block)
            normalCases.append(normalCase)

            continue

        else:
            return normalCases




def _parse_switch_statement(numberOfReturnValues, functionDefinitionListToAddTo):
    
    tok = _next_parse_token()

    if tok.kind == Tok.SWITCH:

        switchValue = _parse_expression()
        if switchValue is None:
            return None

        normalCases = _parse_switch_normal_cases(numberOfReturnValues, functionDefinitionListToAddTo)
        if normalCases is None:
            return None

        # NBlock defaultBlock;

        peekDefault = _peek_parse_token(0)

        if peekDefault.kind == Tok.DEFAULT:

            junk = _next_parse_token()     # go past "default"

            defaultBlockOrNull = _parse_block(numberOfReturnValues, functionDefinitionListToAddTo)
            if defaultBlockOrNull is None:
                return None

        else:

            if len(normalCases) < 1:
                util.log_error(tok.lineNr, tok.rowNr, "A 'switch' statement must have at least one normal case or, alternatively, one default case.")
                return None

            defaultBlockOrNull = None

        return NSwitchStatement(tok.lineNr, tok.rowNr, switchValue, normalCases, defaultBlockOrNull)

    else:
        util.log_error(tok.lineNr, tok.rowNr, "Expected 'switch' (for some strange reason), found something else. #2")
        return None
        



def _parse_contenttype_statement(numberOfReturnValues, functionDefinitionListToAddTo):

    tok = _next_parse_token()

    if tok.kind == Tok.CONTENTTYPE:

        switchValue = _parse_expression()
        if switchValue is None: 
            return None

        normalCases = _parse_contenttype_normal_cases(numberOfReturnValues, functionDefinitionListToAddTo)
        if normalCases is None:
            return None

        # NBlock defaultBlock;

        peekDefault = _peek_parse_token(0)

        if peekDefault.kind == Tok.DEFAULT:

            junk = _next_parse_token()    # go past "default"

            defaultBlockOrNull = _parse_block(numberOfReturnValues, functionDefinitionListToAddTo)
            if defaultBlockOrNull is None: 
                return None            

        else:

            if len(normalCases) < 1:
                util.log_error(tok.lineNr, tok.rowNr, "A 'contenttype' statement must have at least one normal case or, alternatively, one default case.")
                return None 

            defaultBlockOrNull = None

        

        return NContenttypeStatement(tok.lineNr, tok.rowNr, switchValue, normalCases, defaultBlockOrNull)

    else:

        util.log_error(tok.lineNr, tok.rowNr, "Expected 'contenttype' (for some strange reason), found something else. #2")
        return None

    







def _parse_param():


    peek = _peek_parse_token(0)

    if peek.kind == Tok.REF:

        junk = _next_parse_token()  # go past "ref"

        paramName = _parse_identifier()
        if paramName is None: 
            return None

        tok3 = _next_parse_token()

        if tok3.kind == Tok.SINGLEQUOTE:

            paramType = _parse_type()
            if paramType is None: 
                return None

            return NRefParam(peek.lineNr, peek.rowNr, paramName, paramType)

        else:

            util.log_error(tok3.lineNr, tok3.rowNr, "Expected a singlequote here! #7")
            return None

    else:

        isMut = False
        isConstruand = False

        peek2 = _peek_parse_token(0)

        if peek2.kind == Tok.CONSTRUAND:

            junk = _next_parse_token()

            peek3 = _peek_parse_token(0)

            if peek3.kind == Tok.MUT:

                junk = _next_parse_token()                

                isMut = True
                isConstruand = True

            else:
                isMut = False
                isConstruand = True
            
        elif peek2.kind == Tok.MUT:

            junk = _next_parse_token()

            peek3 = _peek_parse_token(0)

            if peek3.kind == Tok.CONSTRUAND:

                junk = _next_parse_token()

                isMut = True
                isConstruand = True

            else:
                isMut = True
                isConstruand = False

        else:
            isMut = False
            isConstruand = False



        paramName = _parse_identifier()
        if paramName is None:
            return None

        tok3 = _next_parse_token()

        if tok3.kind == Tok.SINGLEQUOTE:
            
            paramType = _parse_type()
            if paramType is None:
                return None

            return NNormalParam(peek.lineNr, peek.rowNr, isMut, isConstruand, paramName, paramType)
    
        else: 

            util.log_error(tok3.lineNr, tok3.rowNr, "Expected a singlequote here! #7333")
            return None

        

            
    


def _parse_function_declaration_statement(functionDefinitionListToAddTo):

    isInline = False
    isInternal = False

    tok = _next_parse_token()

    if tok.kind == Tok.INLINE:

        tok2 = _next_parse_token()

        if tok2.kind == Tok.INTERNAL:

            tok3 = _next_parse_token()

            if tok3.kind == Tok.FUN:

                isInline = True
                isInternal = True

            else:

                util.log_error(tok3.lineNr, tok3.rowNr, "Expected 'fn' here! #8887")
                return None


        elif tok2.kind == Tok.FUN:

            isInline = True
            isInternal = False

        else:

            util.log_error(tok2.lineNr, tok2.rowNr, "Expected 'internal' or 'fn' here! #888")
            return None

        

    elif tok.kind == Tok.INTERNAL:

        tok2 = _next_parse_token()

        if tok2.kind == Tok.INLINE:

            tok3 = _next_parse_token()
            
            if tok3.kind == Tok.FUN:

                isInline = True
                isInternal = True

            else:

                util.log_error(tok3.lineNr, tok3.rowNr, "Expected 'fn' here! #7773")
                return None


        elif tok2.kind == Tok.FUN:

            isInline = False
            isInternal = True

        else:

            util.log_error(tok2.lineNr, tok2.rowNr, "Expected 'inline' or 'fn' here! #11113")
            return None

        

    elif tok.kind == Tok.FUN:

        isInline = False
        isInternal = False

    else:

        util.log_error(tok.lineNr, tok.rowNr, "Expected 'internal' or 'inline' or 'fn' here, for some strange reason. #8080")
        return None

    

    functionName = _parse_identifier()
    if functionName is None:
        return None

    peekParam = _next_parse_token()

    if peekParam.kind == Tok.LPAREN:

        params = []

        while True:

            peek6 = _peek_parse_token(0)

            if peek6.kind == Tok.RPAREN:

                break

            else:

                param = _parse_param()
                if param is None: 
                    return None

                params.append(param)

                peek7 = _peek_parse_token(0)

                if peek7.kind == Tok.RPAREN:

                    break

                elif peek7.kind == Tok.COMMA:

                    junk = _next_parse_token()

                    continue

                else:

                    util.log_error(peek7.lineNr, peek7.rowNr, "Expected ',' or ')' here! #797")
                    return None

                

           

        

        junk = _next_parse_token()  # eat the )

        peek4 = _peek_parse_token(0)

        if peek4.kind == Tok.SINGLEQUOTE:

            junk = _next_parse_token()  # eat the '

            returnTypes = _parse_type_list()
            if returnTypes is None: 
                return None

            

            block = _parse_block(len(returnTypes), functionDefinitionListToAddTo)
            if block is None: 
                return None

            actual = NActualFunctionDeclarationWithDefinition(
                tok.lineNr,
                tok.rowNr,
                isInternal,
                isInline,
                functionName,
                params,
                returnTypes,
                block
            )

            functionDefinitionListToAddTo.append(actual)

            return NRefToFunctionDeclarationWithDefinition(len(functionDefinitionListToAddTo) - 1, functionDefinitionListToAddTo)   # BAD BAD architecture

            

            

        else:

            returnTypes = []

            block = _parse_block(len(returnTypes), functionDefinitionListToAddTo)
            if block is None: 
                return None

            actual = NActualFunctionDeclarationWithDefinition(
                tok.lineNr,
                tok.rowNr,
                isInternal,
                isInline,
                functionName,
                params,
                returnTypes,
                block
            )

            functionDefinitionListToAddTo.append(actual)

            return NRefToFunctionDeclarationWithDefinition(len(functionDefinitionListToAddTo) - 1, functionDefinitionListToAddTo)   # BAD BAD architecture

        

        

    else:

        util.log_error(peekParam.lineNr, peekParam.rowNr, "Expected '(' here! #111345")
        return None

    

    



def _parse_template_declaration_statement(functionDefinitionListToAddTo):

    isInline = False
    isInternal = False

    tok = _next_parse_token()

    if tok.kind == Tok.INLINE:

        tok2 = _next_parse_token()

        if tok2.kind == Tok.INTERNAL:

            tok3 = _next_parse_token()

            if tok3.kind == Tok.FUN:

                isInline = True
                isInternal = True

            else:

                util.log_error(tok3.lineNr, tok3.rowNr, "Expected 'fn' here! #8887")
                return None

         

        elif tok2.kind == Tok.FUN:

            isInline = True
            isInternal = False

        else:

            util.log_error(tok2.lineNr, tok2.rowNr, "Expected 'private' or 'fn' here! #888")
            return None

        

    elif tok.kind == Tok.INTERNAL:

        tok2 = _next_parse_token()

        if tok2.kind == Tok.INLINE:

            tok3 = _next_parse_token()
            
            if tok3.kind == Tok.FUN:

                isInline = True
                isInternal = True

            else:

                util.log_error(tok3.lineNr, tok3.rowNr, "Expected 'fn' here! #7773")
                return None

           

        elif tok2.kind == Tok.FUN:

            isInline = False
            isInternal = True

        else:

            util.log_error(tok2.lineNr, tok2.rowNr, "Expected 'inline' or 'fn' here! #11113")
            return None

       

    elif tok.kind == Tok.FUN:

        isInline = False
        isInternal = False

    else:

        util.log_error(tok.lineNr, tok.rowNr, "Expected 'private' or 'inline' or 'fn' here, for some strange reason. #8080")
        return None

    

   
    lParenTok = _next_parse_token()

    if lParenTok.kind != Tok.LPAREN:

        util.log_error(lParenTok.lineNr,  lParenTok.rowNr, "Expected a '(' here, for some strange reason. #7343")
        return None

   


    templateParams = []  # empty to begin with, 0 elements is actually allowed! NOTE: IS IT? REALLY?

    while True:

        peek34 = _peek_parse_token(0)

        if peek34.kind == Tok.RPAREN:

            junk = _next_parse_token()    # eat the )

            break

        else:

            param = _parse_identifier()
            if param is None: 
                return None

            templateParams.append(param)

            peek64 = _peek_parse_token(0)

            if peek64.kind == Tok.COMMA:

                junk = _next_parse_token()    # eat the ,

                continue

            elif peek64.kind == Tok.RPAREN:

                junk = _next_parse_token()     # eat the )

                break

            else:
    
                util.log_error(peek64.lineNr, peek64.rowNr, "Expected ')' or ',' here! #7291")
                return None

         
       
    




    templateName = _parse_identifier()
    if templateName is None: 
        return None

    peekParam = _next_parse_token()

    if peekParam.kind == Tok.LPAREN:

        params = []

        while True:

            peek6 = _peek_parse_token(0)

            if peek6.kind == Tok.RPAREN:

                break

            else:

                param = _parse_param()
                if param is None: 
                    return None

                params.append(param)

                peek7 = _peek_parse_token(0)

                if peek7.kind == Tok.RPAREN:

                    break

                elif peek7.kind == Tok.COMMA:

                    junk = _next_parse_token()

                    continue

                else:

                    util.log_error(peek7.lineNr, peek7.rowNr, "Expected ',' or ')' here! #797")
                    return None

                

        junk = _next_parse_token()  # eat the )

        peek4 = _peek_parse_token(0)

        if peek4.kind == Tok.SINGLEQUOTE:

            junk = _next_parse_token()   # eat the '

            returnTypes = _parse_type_list()
            if returnTypes is None: 
                return None

            

            block = _parse_block(len(returnTypes), functionDefinitionListToAddTo)
            if block is None: 
                return None

            actual = NActualTemplateDeclarationWithDefinition(
                tok.lineNr,
                tok.rowNr,
                isInternal,
                isInline,
                templateParams,
                templateName,
                params,
                returnTypes,
                block
            )

            functionDefinitionListToAddTo.append(actual)

            return NRefToTemplateDeclarationWithDefinition(len(functionDefinitionListToAddTo) - 1, functionDefinitionListToAddTo)

            

           

        else:

            returnTypes = []

            block = _parse_block(len(returnTypes), functionDefinitionListToAddTo)
            if block is None: 
                return None


            actual = NActualTemplateDeclarationWithDefinition(
                tok.lineNr,
                tok.rowNr,
                isInternal,
                isInline,
                templateParams,
                templateName,
                params,
                returnTypes,
                block
            )

            functionDefinitionListToAddTo.append(actual)

            return NRefToTemplateDeclarationWithDefinition(len(functionDefinitionListToAddTo) - 1, functionDefinitionListToAddTo)

        

        

    else:

        util.log_error(peekParam.lineNr, peekParam.rowNr, "Expected '(' here! #111345")
        return None

    






def _parse_return_statement(numberOfReturnValues):

    tok = _next_parse_token() 

    if tok.kind == Tok.RETURN:

        returnExpressions = []   # empty to begin with

        if numberOfReturnValues > 0:

            firstReturnExpression = _parse_expression()
            if firstReturnExpression is None: 
                return None

            returnExpressions.append(firstReturnExpression)            

            for i in range(1, numberOfReturnValues):

                tok2 = _next_parse_token()

                if tok2.kind == Tok.COMMA:

                    returnExpression = _parse_expression()
                    if returnExpression is None:
                        return None

                    returnExpressions.append(returnExpression)

                else:

                    util.log_error(tok2.lineNr, tok2.rowNr, "Expected a comma here! #7733")
                    return None



        semiTok = _peek_parse_token(0)

        

        

        return NReturnStatement(tok.lineNr, tok.rowNr, returnExpressions)

    else:

        util.log_error(tok.lineNr, tok.rowNr, "Expected 'return' here, for some strange reason... #87972")
        return None

    






def _parse_assignment_left_side_item():

    peek = _peek_parse_token(0)

    if peek.kind == Tok.MUT:

        junk = _next_parse_token()     # eat past "mu"

        peek2 = _peek_parse_token(0)

        if peek2.kind == Tok.INTERNAL:

            junk = _next_parse_token()    # eat past "internal"

            variableName = _parse_identifier()
            if variableName is None: 
                return None

            tok3 = _next_parse_token()

            if tok3.kind == Tok.SINGLEQUOTE:

                variableType = _parse_type()
                if variableType is None: 
                    return None

                return NVariableDeclaration(peek.lineNr, peek.rowNr, True, True, variableName, variableType)

            else:

                util.log_error(tok3.lineNr, tok3.rowNr, "Expected a singlequote here! #722")
                return None

            
        elif peek2.kind == Tok.IDENTIFIER:

            variableName = _parse_identifier()
            if variableName is None: 
                return None

            tok3 = _next_parse_token()

            if tok3.kind == Tok.SINGLEQUOTE:

                variableType = _parse_type()
                if variableType is None: 
                    return None

                return NVariableDeclaration(peek.lineNr, peek.rowNr, True, False, variableName, variableType)

            else:

                util.log_error(tok3.lineNr, tok3.rowNr, "Expected a singlequote here! #742")
                return None

        

        else:

            util.log_error(peek2.lineNr, peek2.rowNr, "Expected 'internal' or an identifier here! #72")
            return None

        

    elif peek.kind == Tok.INTERNAL:

        junk = _next_parse_token()   # eat past "internal"

        peek2 = _peek_parse_token(0)

        if peek2.kind == Tok.MUT:

            junk = _next_parse_token()    # eat past "mu"

            variableName = _parse_identifier()
            if variableName is None: 
                return None

            tok3 = _next_parse_token()

            if tok3.kind == Tok.SINGLEQUOTE:

                variableType = _parse_type()
                if variableType is None:
                    return None

                return NVariableDeclaration(peek.lineNr, peek.rowNr, True, True, variableName, variableType)

            else:

                util.log_error(tok3.lineNr, tok3.rowNr, "Expected a singlequote here! #323")
                return None

            
        
        elif peek2.kind == Tok.IDENTIFIER:

            variableName = _parse_identifier()
            if variableName is None: 
                return None

            tok3 = _next_parse_token()

            if tok3.kind == Tok.SINGLEQUOTE:

                variableType = _parse_type()
                if variableType is None:
                    return None

                return NVariableDeclaration(peek.lineNr, peek.rowNr, False, True, variableName, variableType)

            else:

                util.log_error(tok3.lineNr, tok3.rowNr, "Expected a singlequote here! #11")
                return None

            

        else:

            util.log_error(peek2.lineNr, peek2.rowNr, "Expected 'mu' or an identifier here. #1234")
            return None

        

    elif peek.kind == Tok.IDENTIFIER:

        peek2 = _peek_parse_token(1)

        if peek2.kind == Tok.SINGLEQUOTE:

            variableName = _parse_identifier()
            if variableName is None:
                return None

            tok3 = _next_parse_token()

            if tok3.kind == Tok.SINGLEQUOTE:

                variableType = _parse_type()
                if variableType is None:
                    return None

                return NVariableDeclaration(peek.lineNr, peek.rowNr, False, False, variableName, variableType)

            else:

                util.log_error(tok3.lineNr, tok3.rowNr, "Expected a singlequote here. Also, this error message should never happen... #11178")
                return None

            

        else:

            lValue = _parse_lvalue()
            if lValue is None:
                return None

            return lValue


    elif peek.kind == Tok.LPAREN:

        util.log_debug("PARSING LVALUE ASSIGNMENT WITH LEFT PAREN\n")

        lValue = _parse_lvalue()
        if lValue is None:
            return None

        return lValue

    else:

        util.log_error(peek.lineNr, peek.rowNr, "Expected a variable declaration or an lvalue here, for some reason. #1879")
        return None

    




def _parse_assignment_statement():

    leftSide = []    # empty, but gets at least one value below

    firstLeftSideItem = _parse_assignment_left_side_item()
    if firstLeftSideItem is None:
        return None

    myLineNr = firstLeftSideItem.get_line_nr()
    myRowNr = firstLeftSideItem.get_row_nr()

    leftSide.append(firstLeftSideItem)

    tok2 = _peek_parse_token(0)     # dummy value

    while True:

        tok2 = _next_parse_token()

        if tok2.kind == Tok.COMMA:

            leftSideItem = _parse_assignment_left_side_item()
            if leftSideItem is None:
                return None

            leftSide.append(leftSideItem)

            continue

        elif (tok2.kind == Tok.ASSIGNMENTOPERATOR or 
                    tok2.kind == Tok.PERCENTASSIGNMENTOPERATOR or
                    tok2.kind == Tok.STARASSIGNMENTOPERATOR or
                    tok2.kind == Tok.SLASHASSIGNMENTOPERATOR or
                    tok2.kind == Tok.PLUSASSIGNMENTOPERATOR or
                    tok2.kind == Tok.MINUSASSIGNMENTOPERATOR
        ):

            break        

        else:

            util.log_error(
                tok2.lineNr, 
                tok2.rowNr, 
                "Expected ',' or assign op. here! (Sometimes this is because the parser is confused because a function's return type(s) were not declared.)"
            )
            return None


    valueExpr = _parse_expression()
    if valueExpr is None:
        return None

    peek3 = _peek_parse_token(0)

    


    if tok2.kind == Tok.ASSIGNMENTOPERATOR:

        return NNormalAssignment(myLineNr, myRowNr, leftSide, valueExpr)

    elif tok2.kind == Tok.PERCENTASSIGNMENTOPERATOR:

        return NModuloAssignment(myLineNr, myRowNr, leftSide, valueExpr)

    elif tok2.kind == Tok.STARASSIGNMENTOPERATOR:

        return NMultiplicationAssignment(myLineNr, myRowNr, leftSide, valueExpr)

    elif tok2.kind == Tok.SLASHASSIGNMENTOPERATOR:

        return NDivisionAssignment(myLineNr, myRowNr, leftSide, valueExpr)

    elif tok2.kind == Tok.PLUSASSIGNMENTOPERATOR:
        return NAdditionAssignment(myLineNr, myRowNr, leftSide, valueExpr)

    elif tok2.kind == Tok.MINUSASSIGNMENTOPERATOR:

        return NSubtractionAssignment(myLineNr, myRowNr, leftSide, valueExpr)

    else:

        util.log_error(tok2.lineNr, tok2.rowNr, "UNKNOWN ASSIGNMENT OPERATOR. SHOULD NEVER HAPPEN. #1792")
        return None

    
    








def _parse_if_statement(numberOfReturnValues, functionDefinitionListToAddTo):

    tok = _next_parse_token()

    if tok.kind == Tok.IF:

        condition = _parse_expression()
        if condition is None: 
            return None

        thenBlock = _parse_block(numberOfReturnValues, functionDefinitionListToAddTo)
        if thenBlock is None: 
            return None


        elseIfClauses = []

        while True:

            peekElse = _peek_parse_token(0)

            if peekElse.kind == Tok.ELSE:

                peekElseIf = _peek_parse_token(1)

                if peekElseIf.kind == Tok.IF:

                    junk = _next_parse_token()
                    junk = _next_parse_token()

                    elseIfCondition = _parse_expression()
                    if elseIfCondition is None:
                        return None

                    elseIfThenBlock = _parse_block(numberOfReturnValues, functionDefinitionListToAddTo)
                    if elseIfThenBlock is None:
                        return None

                    elseIfClause = NElseIfClause(peekElse.lineNr, peekElse.rowNr, elseIfCondition, elseIfThenBlock)
                    elseIfClauses.append(elseIfClause)

                    continue    

                else:
                    break    
        
            else:
                break



        elseClauseOrNull = None

        peek80 = _peek_parse_token(0)

        if peek80.kind == Tok.ELSE:

            junk = _next_parse_token()

            elseClauseOrNull = _parse_block(numberOfReturnValues, functionDefinitionListToAddTo)
            if elseClauseOrNull is None:
                return None


        return NIfStatement(tok.lineNr, tok.rowNr, condition, thenBlock, elseIfClauses, elseClauseOrNull)


    else:

        util.log_error(tok.lineNr, tok.rowNr, "Expected 'if' here, for some strange reason... #1280")
        return None

    









def _parse_loop_statement(numberOfReturnValues, functionDefinitionListToAddTo):

    tok = _next_parse_token()

    if tok.kind == Tok.LOOP:

        peek2 = _peek_parse_token(0)

        if peek2.kind == Tok.LABEL:

            junk = _next_parse_token()     # eat "label"

            labelIdentifier = _parse_identifier()
            if labelIdentifier is None: 
                return None

            loopBlock = _parse_block(numberOfReturnValues, functionDefinitionListToAddTo)
            if loopBlock is None: 
                return None

            return NLoopStatement(tok.lineNr, tok.rowNr, loopBlock, labelIdentifier)

        else:

            loopBlock = _parse_block(numberOfReturnValues, functionDefinitionListToAddTo)
            if loopBlock is None: 
                return None

            return NLoopStatement(tok.lineNr, tok.rowNr, loopBlock, None)

        
    
    else:

        util.log_error(tok.lineNr, tok.rowNr, "Expected 'loop' here, for some strange reason... #1179")
        return None

    









def _parse_iteration():

    it = _parse_identifier()
    if it is None: 
        return None

    
    typeOrNull = None

    peek2 = _peek_parse_token(0)

    if peek2.kind == Tok.SINGLEQUOTE:
        
        junk = _next_parse_token()

        typeOrNull = _parse_type()
        if typeOrNull is None:
            return None

    
    tok3 = _next_parse_token()

    if tok3.kind == Tok.IN:

        inExpression = _parse_expression()
        if inExpression is None: 
            return None

        
        factorExpression = None

        peek4 = _peek_parse_token(0)

        if peek4.kind == Tok.INDEXFACTOR:

            junk = _next_parse_token()    # go past "indexfactor"

            factorExpression = _parse_expression()
            if factorExpression is None: 
                return None

        
        offsetExpression = None

        peek5 = _peek_parse_token(0)

        if peek5.kind == Tok.INDEXOFFSET:

            junk = _next_parse_token()   # go past "indexoffset"

            offsetExpression = _parse_expression()
            if offsetExpression is None:
                return None

        return NIterationIn(peek2.lineNr, peek2.rowNr, it, typeOrNull, inExpression, factorExpression, offsetExpression)
                       
    
    elif tok3.kind == Tok.OVER:

        overLValue = _parse_lvalue()
        if overLValue is None: 
            return None


        factorExpression = None

        peek4 = _peek_parse_token(0)

        if peek4.kind == Tok.INDEXFACTOR:

            junk = _next_parse_token()    # go past "indexfactor"

            factorExpression = _parse_expression()
            if factorExpression is None: 
                return None

        
        offsetExpression = None

        peek5 = _peek_parse_token(0)

        if peek5.kind == Tok.INDEXOFFSET:

            junk = _next_parse_token()   # go past "indexoffset"

            offsetExpression = _parse_expression()
            if offsetExpression is None:
                return None


        return NIterationOver(peek2.lineNr, peek2.rowNr, it, typeOrNull, overLValue, factorExpression, offsetExpression)
              
       
    else:

        logError(peek2.lineNr, peek2.rowNr, "Unknown syntactic construction.")
        return None

    






def _parse_iterations():

    iterations = []   # empty now, but we will expect at least one iteration

    firstIteration = _parse_iteration()
    if firstIteration is None: 
        return None

    iterations.append(firstIteration)

    while True:

        peek5 = _peek_parse_token(0)

        if peek5.kind == Tok.COMMA:

            junk = _next_parse_token()

            iteration = _parse_iteration()
            if iteration is None: 
                return None

            iterations.append(iteration)

            continue

        else:

            return iterations








def _parse_range():

    rangeVariable = _parse_identifier()
    if rangeVariable is None:
        return None

    tok2 = _next_parse_token()

    if tok2.kind == Tok.SINGLEQUOTE:

        theType = _parse_type()
        if theType is None: 
            return None

        tok4 = _next_parse_token()
        
        if tok4.kind == Tok.ASSIGNMENTOPERATOR:

            fromExpr = _parse_expression()
            if fromExpr is None:
                return None

            
            isDownto = False

            tok6 = _next_parse_token()

            if tok6.kind == Tok.TO:
        
                isDownto = False

            elif tok6.kind == Tok.DOWNTO:

                isDownto = True

            else:
                util.log_error(tok6.lineNr, tok6.rowNr, "Expected 'to' or 'downto' here.")
                return None

            
            expr2 = _parse_expression()
            if expr2 is None:
                return None            
                        
            return NRange(tok2.lineNr, tok2.rowNr, rangeVariable, theType, fromExpr, isDownto, expr2)


        else:

            util.log_error(tok4.lineNr, tok4.rowNr, "Expected an '=' here! #833")
            return None


    else:

        util.log_error(tok2.lineNr, tok2.rowNr, "Expected a singlequote here! #7320")
        return None

 








def _parse_for_statement(numberOfReturnValues, functionDefinitionListToAddTo):


    tok1 = _next_parse_token() 

    if tok1.kind == Tok.FOR:

        labelOrNull = None

        peek2 = _peek_parse_token(0)

        if peek2.kind == Tok.LABEL:

            junk = _next_parse_token()

            labelOrNull = _parse_identifier()
            if labelOrNull is None:
                return None

            
        peek3 = _peek_parse_token(0)

        if peek3.kind == Tok.IDENTIFIER:

            peek4 = _peek_parse_token(1)

            if peek4.kind == Tok.SINGLEQUOTE:

                peekAfterType = _peek_past_type(2, True)
                if peekAfterType == -1: 
                    return None

                peek5 = _peek_parse_token(peekAfterType)

                if peek5.kind == Tok.ASSIGNMENTOPERATOR:

                    theRange = _parse_range()
                    if theRange is None: 
                        return None

                    peek6 = _peek_parse_token(0)

                    if peek6.kind == Tok.COMMA:

                        junk = _next_parse_token()   # go past the comma

                        iterations = _parse_iterations()
                        if iterations is None: 
                            return None

                        forBlock = _parse_block(numberOfReturnValues, functionDefinitionListToAddTo)
                        if forBlock is None: 
                            return None

                        return NForStatement(tok1.lineNr, tok1.rowNr, theRange, iterations, forBlock, labelOrNull)

                    else:

                        emptyIterations = []

                        forBlock = _parse_block(numberOfReturnValues, functionDefinitionListToAddTo)
                        if forBlock is None: 
                            return None

                        return NForStatement(tok1.lineNr, tok1.rowNr, theRange, emptyIterations, forBlock, labelOrNull)

                    

                elif peek5.kind == Tok.IN or peek5.kind == Tok.OVER:

                    iterations = _parse_iterations()
                    if iterations is None:
                        return None

                    forBlock = _parse_block(numberOfReturnValues, functionDefinitionListToAddTo)
                    if forBlock is None: 
                        return None

                    return NForStatement(tok1.lineNr, tok1.rowNr, None, iterations, forBlock, labelOrNull)

                else:

                    util.log_error(peek5.lineNr, peek5.rowNr, "Expected '=', 'in' or 'over' here! #9832")
                    return None

                
                
            elif peek4.kind == Tok.IN or peek4.kind == Tok.OVER:

                iterations = _parse_iterations()
                if iterations is None:
                    return None

                forBlock = _parse_block(numberOfReturnValues, functionDefinitionListToAddTo)
                if forBlock is None: 
                    return None

                return NForStatement(tok1.lineNr, tok1.rowNr, None, iterations, forBlock, labelOrNull)

            else:

                util.log_error(peek4.lineNr, peek4.rowNr, "Expected singlequote, 'in' or 'over' here! #1722")
                return None

        else:

            util.logError(peek2.lineNr, peek2.rowNr, "Unknown syntactical construct. #11792")
            return None

       

    else:

        util.log_error(tok1.lineNr, tok1.rowNr, "Expected 'for' here, for some strange reason.. #1182")
        return None

   






def _parse_break_statement():

    tok1 = _next_parse_token()

    if tok1.kind == Tok.BREAK:

        peek2 = _peek_parse_token(0)

        if peek2.kind == Tok.LABEL:

            junk = _next_parse_token()    # go past "label"

            labelIdentifier = _parse_identifier()
            if labelIdentifier is None:
                return None

            peek3 = _peek_parse_token(0)

            

            

            return NBreakStatement(tok1.lineNr, tok1.rowNr, labelIdentifier)

        else:

            peek3 = _peek_parse_token(0)

            

            

            return NBreakStatement(tok1.lineNr, tok1.rowNr, None)

        

    else:

        util.log_error(tok1.lineNr, tok1.rowNr, "Expected 'break' here, for some reason... #711")
        return None
    
   




def _parse_continue_statement():

    tok1 = _next_parse_token()

    if tok1.kind == Tok.CONTINUE:

        peek2 = _peek_parse_token(0)

        if peek2.kind == Tok.LABEL:

            junk = _next_parse_token()    # go past "label"

            labelIdentifier = _parse_identifier()
            if labelIdentifier is None:
                return None

            peek3 = _peek_parse_token(0)

            

            

            return NContinueStatement(tok1.lineNr, tok1.rowNr, labelIdentifier)

        else:

            peek3 = _peek_parse_token(0)

           

            

            return NContinueStatement(tok1.lineNr, tok1.rowNr, None)

        

    else:

        util.log_error(tok1.lineNr, tok1.rowNr, "Expected 'continue' here, for some reason... #711")
        return None








def _parse_function_call_statement():

    peek = _peek_parse_token(0)

    if peek.kind == Tok.IDENTIFIER:

        peek2 = _peek_parse_token(1)

        if peek2.kind == Tok.DOUBLEPERIOD:

            funCallExpr = _parse_function_call_with_module_name(False)
            if funCallExpr is None:
                return None

            

            return NFunctionCallStatement(peek.lineNr, peek.rowNr, funCallExpr)

        else:

            funCallExpr = _parse_function_call_without_module_name(False)
            if funCallExpr is None:
                return None

            

            return NFunctionCallStatement(peek.lineNr, peek.rowNr, funCallExpr)

    else:
        util.log_error(peek.lineNr, peek.rownr, "Expected an identifier here, for some reason.")    
        return None


    






def _parse_statement(numberOfReturnValues, functionDefinitionListToAddTo):    # numberOfReturnValues should be -1 for global statement!

    peek = _peek_parse_token(0)

    if peek.kind == Tok.COLON:

        # block

        return _parse_block(numberOfReturnValues)

    elif peek.kind == Tok.TYPE:

        if numberOfReturnValues == -1:

            return _parse_type_declaration_statement()

        else:
            util.log_error(peek.lineNr, peek.rowNr, "Local type declarations are not allowed.")
            return None

    elif peek.kind == Tok.CONTENTTYPE:

        return _parse_contenttype_statement(numberOfReturnValues, functionDefinitionListToAddTo)

    elif peek.kind == Tok.SWITCH:

        return _parse_switch_statement(numberOfReturnValues, functionDefinitionListToAddTo)

    elif peek.kind == Tok.INTERNAL:

        # function declaration or assignment (with declaration)
            
        peek2 = _peek_parse_token(1)

        if peek2.kind == Tok.FUN:

            peek3 = _peek_parse_token(2)

            if peek3.kind == Tok.LPAREN:

                if numberOfReturnValues == -1:

                    return _parse_template_declaration_statement(functionDefinitionListToAddTo)

                else:

                    util.log_error(peek.lineNr, peek.rowNr, "Local template declarations are not allowed. #242")
                    return None


            else:

                return _parse_function_declaration_statement(functionDefinitionListToAddTo)

                      

        elif peek2.kind == Tok.INLINE:

            peek3 = _peek_parse_token(2)

            if peek3.kind == Tok.FUN:

                peek4 = _peek_parse_token(3)

                if peek4.kind == Tok.LPAREN:

                    if numberOfReturnValues == -1:

                        return _parse_template_declaration_statement(functionDefinitionListToAddTo)

                    else:

                        util.log_error(peek.lineNr, peek.rowNr, "Local template declarations are not allowed. #245")
                        return None


                else:

                    return _parse_function_declaration_statement(functionDefinitionListToAddTo)

                

            else:

                util.log_error(peek3.lineNr, peek3.rowNr, "Expected 'fn' here! #7333")
                return None

           

        else:

            return _parse_assignment_statement()

        

    elif peek.kind == Tok.MUT:

        # assignment

        return _parse_assignment_statement()

    elif peek.kind == Tok.INLINE:

        peek2 = _peek_parse_token(1)

        if peek2.kind == Tok.INTERNAL:

            peek3 = _peek_parse_token(2)

            if peek3.kind == Tok.FUN:

                peek4 = _peek_parse_token(3)

                if peek4.kind == Tok.LPAREN:

                    if numberOfReturnValues == -1:

                        return _parse_template_declaration_statement(functionDefinitionListToAddTo)

                    else:

                        util.log_error(peek.lineNr, peek.rowNr, "Local template declarations are not allowed. #743")
                        return None

                  

                else:

                    return _parse_function_declaration_statement(functionDefinitionListToAddTo)

                

            else:

                util.log_error(peek3.lineNr, peek3.rowNr, "Expected 'fn' here! #111234")
                return None


        elif peek2.kind == Tok.FUN:
    
            peek4 = _peek_parse_token(2)

            if peek4.kind == Tok.LPAREN:

                if numberOfReturnValues == -1:

                    return _parse_template_declaration_statement(functionDefinitionListToAddTo)

                else:

                    util.log_error(peek.lineNr, peek.rowNr, "Local template declarations are not allowed. #743")
                    return None


            else:

                return _parse_function_declaration_statement(functionDefinitionListToAddTo)

            

        else:

            util.log_error(peek2.lineNr, peek2.rowNr, "Expected 'internal' or 'fn' here! #682")
            return None

        

    elif peek.kind == Tok.FUN:

        peek4 = _peek_parse_token(1)

        if peek4.kind == Tok.LPAREN:

            if numberOfReturnValues == -1:

                return _parse_template_declaration_statement(functionDefinitionListToAddTo)

            else:

                util.log_error(peek.lineNr, peek.rowNr, "Local template declarations are not allowed. #743")
                return None


        else:

            return _parse_function_declaration_statement(functionDefinitionListToAddTo)

        

    elif peek.kind == Tok.RETURN:

        if numberOfReturnValues != -1:

            return _parse_return_statement(numberOfReturnValues)

        else:

            util.log_error(peek.lineNr, peek.rowNr, "Return statements are not allowed in the global scope. #28")
            return None

 

    elif peek.kind == Tok.IF:

        return _parse_if_statement(numberOfReturnValues, functionDefinitionListToAddTo)

    elif peek.kind == Tok.LOOP:

        return _parse_loop_statement(numberOfReturnValues, functionDefinitionListToAddTo)

    elif peek.kind == Tok.FOR:

        return _parse_for_statement(numberOfReturnValues, functionDefinitionListToAddTo)

    elif peek.kind == Tok.BREAK:

        return _parse_break_statement()

    elif peek.kind == Tok.CONTINUE:

        return _parse_continue_statement()

    elif peek.kind == Tok.IDENTIFIER:

        peek2 = _peek_parse_token(1)

        # we first rule out that it is a function call

        if peek2.kind == Tok.DOUBLEPERIOD:

            peek3 = _peek_parse_token(2)

            if peek3.kind == Tok.IDENTIFIER:

                peek4 = _peek_parse_token(3)

                if peek4.kind == Tok.LPAREN:

                    return _parse_function_call_statement()

                else:

                    return _parse_assignment_statement()    # our best guess, may be invalid...


            else:

                util.log_error(peek3.lineNr, peek3.rowNr, "Expected an identifier after doubleperiod! #12")
                return None

            

        elif peek2.kind == Tok.LPAREN:

            return _parse_function_call_statement()

        else:

            return _parse_assignment_statement()


    elif peek.kind == Tok.LPAREN:

        return _parse_assignment_statement()

    else:

        util.log_error(peek.lineNr, peek.rowNr, "Expected a statement, found something else! #0812")
        return None

    


#################################################################################################
#######                        PROGRAM PARSING                                      #############
#################################################################################################


def parse_program(tokens, functionDefinitionListToAddTo):
    global _lexed
    global _lexedpos

    _lexed = tokens
    _lexedpos = 0


    # first, parse all import statements
    importStatements = []
    while True:

        peek = _peek_parse_token(0)
        
        if peek.kind == Tok.PREFIXIMPORT or peek.kind == Tok.IMPORT:

            junk = _next_parse_token()    # eat the import/prefiximport keyword

            importStringToken = _next_parse_token()
            if importString.kind != Tok.STRING:
                util.log_error(importStringToken.lineNr, importStringToken.rowNr, "Expected a string here.")
                
                # reset/nullify global data!    
                _lexed = []
                _lexedpos = 0
                return None    

            isPrefix = peek.kind == Tok.PREFIXIMPORT

            importStatement = NImportStatement(peek.lineNr, peek.rowNr, isPrefix, importStringToken.tokStr)
            importStatements.append(importStatement)

            continue

        else:
            break


    # then all ordinary statements
    ordinaryStatements = []
    while True:
        
        peek2 = _peek_parse_token(0)

        if peek2.kind == Tok.EOF:
           
            break

        else:

            ordinaryStatement = _parse_statement(-1, functionDefinitionListToAddTo)
            if ordinaryStatement is None:

                # rest/nullify global data!
                _lexed = []
                _lexedpos = 0
                return None

            ordinaryStatements.append(ordinaryStatement)

            continue
                    
    

    # reset/nullify global data!    
    _lexed = []
    _lexedpos = 0

    return NProgram(0, 0, importStatements, ordinaryStatements)






