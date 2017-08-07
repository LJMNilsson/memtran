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


import re


# Note that mangling the same identifier twice might give different results.
# So first check if the name is already found/defined in the scope. 


# This mangler does NOT generate an ASCII string. Rather it generates a Python string in internal UTF-8 encoding,
# but with only LLVM IR-valid characters in it. 

# Expects 'moduleName' to be already mangled!!! Maybe problematic if not the same always?





# chr()  ord()

def mangle_basic_name(identifier):    # To be used for module names, struct tags, labels, and such.

    resultString = ""

    for i in range(0, len(identifier)):
        
        charStr = identifier[i:i+1]  # this should work but a bit slow

        test = re.match('[a-zA-Z0-9_$]', charStr)     # We should compile this

        if test:
            
            resultString += charStr
            
        else:

            ordCharStr = ord(charStr)

            resultString += '-'
            resultString += str(ordCharStr)
            resultString += '-'



    return resultString

                        



def mangle_type_name(identifier, mangledModuleName):

    # We will have to reconsider the moduleName part maybe:

    return "type." + mangledModuleName + "." + mangle_basic_name(identifier)



def mangle_template_name(identifier, mangledModuleName):

    return "template." + mangledModuleName + "." + mangle_basic_name(identifier)    



def mangle_var_name(identifier, mangledModuleName, isGlobal, blockNumberList):

    resultString = ""

    if isGlobal:
        resultString += "@var."
    else:
        resultString += "%var."

    
    resultString += mangledModuleName
    resultString += "."
        
    for blockNumber in blockNumberList:
        resultString += str(blockNumber)
        resultString += "."

    resultString += mangle_basic_name(identifier)

    return resultString





def mangle_param_name(identifier):
    resultString = "%param."

    resultString += mangle_basic_name(identifier)
    
    return resultString





def mangle_function_name(identifier, mangledModuleName, isGlobal, blockNumberList, overloadNr):

    resultString = "@fn."

    # we don't need isGlobal actually

    resultString += mangledModuleName
    resultString += "."

    for blockNumber in blockNumberList:
        resultString += str(blockNumber)
        resultString += "."

    resultString += mangle_basic_name(identifier)
    resultString += "."
    resultString += str(overloadNr)

    return resultString    
    


def mangle_template_specialisation_name(mangledTemplateName, mangledModuleName, overloadNr):

    resultString = "@tspec."

    resultString += mangledModuleName
    resultString += "."
    
    resultString += mangledTemplateName
    resultString += "."

    resultString += str(overloadNr)

    return resultString

            

    



    
