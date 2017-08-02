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



from tokens import *
from lexer import *

util.currentFileName = "lexertest.cip"

toks = lex_file("lexertest.cip")

if toks != False:
    for it in toks:
        it.print_it()
        print("  ", end='')

    print("")  # newline
