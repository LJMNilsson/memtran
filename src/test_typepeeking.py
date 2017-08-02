# Copyright (C) 2017 Martin Nilsson


# This file is part of the Cimmpl compiler.
#
#     The Cimmpl compiler is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
# 
#     The Cimmpl compiler is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
# 
#     You should have received a copy of the GNU General Public License
#     along with the Cimmpl compiler.  If not, see http://www.gnu.org/licenses/ . 



import util
from tokens import *
import lexer
import parser

util.currentFileName = "parsertest.cip"

toks = lexer.lex_file("parsertest.cip")

if toks != False:
    # Print the tokens:
    for it in toks:
        it.print_it()
        print("  ", end='')

    print("")  # newline


    parser._set_lextokens(toks)

    peekResult = parser._peek_past_type(0, True)

    if not peekResult == -1:  # parse error
        print("Number of tokens in type: ", end='')
        print(str(peekResult))            

    
