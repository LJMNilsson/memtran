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
import lexer
import ast
import parser
import end_expansion

util.currentFileName = "endexpansiontest.cip"

toks = lexer.lex_file("endexpansiontest.cip")

if toks != False:
    # Print the tokens:
    for it in toks:
        it.print_it()
        print("  ", end='')

    print("")  # newline
    print("")



    parseResult = parser.parse_program(toks, [])

    if parseResult != None:
        parseResult.print_it()

        print("") # newline
        print("") # newline

        
        success = end_expansion.run_pass(parseResult)
        
        if success:
            parseResult.print_it()
            print("") # newline
        


