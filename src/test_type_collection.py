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
import name_mangler
import type_collection

util.currentFileName = "typecollectiontest.mtr"

toks = lexer.lex_file("typecollectiontest.mtr")

if toks != False:
    print("LEXING SUCCESSFUL!")

    # Print the tokens:
    for it in toks:
        it.print_it()
        print("  ", end='')

    print("")  # newline
    print("")



    parseResult = parser.parse_program(toks, [])

    if parseResult != None:
        print("PARSING SUCCESSFUL!")

        parseResult.print_it()

        print("") # newline
        print("") # newline

        
        success = end_expansion.run_pass(parseResult)
        
        if success:
            print("END EXPANSION SUCCESSFUL!")

            parseResult.print_it()
            print("") # newline

            mangledModuleName = name_mangler.mangle_basic_name("typecollectiontest")

            directlyImportedTypesDictDict = {}  # should contains the directly imported types, sorted per imported module!

            otherImportedModulesTypeDictDict = {} # should be a dict of dicts

            typeDict = type_collection.gather(parseResult, mangledModuleName, directlyImportedTypesDictDict)
            if not (typeDict == False):

                    print("TYPE COLLECTION SUCCESSFUL!")
                
                    print(typeDict)

                    success = type_collection.check(typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict)

                    if success:

                        print("NAMED TYPE SIGNATURE CHECKING SUCCESSFUL!")


