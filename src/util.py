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





currentFileName = ""

def log_error(lineNr, rowNr, errorString):
    print(currentFileName, end='')
    print(": Line: " + str(lineNr), end='')
    print(" Row: " + str(rowNr), end='')
    print(" ", end='')
    print(errorString)


def maybe_log_error(lineNr, rowNr, errorString, displayErrorMessagesFlag):
    if displayErrorMessagesFlag:
        log_error(lineNr, rowNr, errorString)
 

displayDebugMessagesFlag = True

def log_debug(debugString):
    if displayDebugMessagesFlag:
        print(debugString)
   


