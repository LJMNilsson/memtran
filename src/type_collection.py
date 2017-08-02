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
from ast import *
import name_mangler



# Returns a dictionary of type declarations with definitions, and annotated with mangled type name. 
# And checks for duplicate names.
# Returns False if a duplicate was found! 
# TODO: Add functionality to check for duplicate names in other modules (directly) imported

def gather(astProgram, mangledModuleName):

    typeDict = {}

    for statement in astProgram.statements:

        if isinstance(statement, NTypeDeclarationWithDefinition):

            if statement.name.name in typeDict:

                util.log_error(statement.name.lineNr, statement.name.typeNr, "Name collision.")
                return False

            else:
                dictAddition = statement.create_copy()

                dictAddition.mangledName = name_mangler.mangle_type_name(statement.name.name, mangledModuleName)

                typeDict[statement.name.name] = dictAddition


    return typeDict        




class _CheckTypesVisitor(AbstractASTVisitor):

    # TODO: add the whole module identifier business!


    def __init__(self, allowedNamesList, typeDict):
            
        self.allowedNamesSet = set(allowedNamesList)
        self.typeDict = typeDict
        


    def visit(self, node):

        if isinstance(node, NParametrizedIdentifierType):

            if not node.name.name in self.allowedNamesSet:
                util.log_error(node.lineNr, node.rowNr, "Undefined type name used.")
                return False

            paramsLen = len(node.params)
            typeParamsOrNull = self.typeDict[node.name.name].paramsOrNull

            if typeParamsOrNull is None:
                util.log_error(node.lineNr, node.rowNr, "Parametrized usage of non-parametrized named type.")
                return False
            else:
                if paramsLen != len(typeParamsOrNull):
                    util.log_error(node.lineNr, node.rowNr, "Wrong number of arguments to parametrized type.")
                    return False            
            
                return True
            
        
        elif isinstance(node, NIdentifierType):

            if not node.name.name in self.allowedNamesSet:

                util.log_error(node.lineNr, node.rowNr, "Undefined type name used.")
                return False

            else:

                if node.name.name in self.typeDict:   # not the case for params... this should kinda work    
                    if not (self.typeDict[node.name.name].paramsOrNull is None):
                        util.log_error(node.lineNr, node.rowNr, "Non-parametrized usage of parametrized named type.")
                        return False

                return True

        else:
            return True    

        



# Performs additional checks. Returns True for pass, or False for error.
# TODO: Allow mathching against module imported names

def check(typeDeclarationDict):

    basicAllowedNames = [] 
    for typeName in typeDeclarationDict.keys():
        basicAllowedNames.append(typeName)      # this conversion to list is needed I guess

    for typeName, declaration in typeDeclarationDict.items():

        params = []
        if not declaration.paramsOrNull is None:
            for param in declaration.paramsOrNull:
                params.append(param.name)

        allowedNamesList = basicAllowedNames + params

        # print(allowedNamesList)

        checker = _CheckTypesVisitor(allowedNamesList, typeDeclarationDict)

        success = declaration.theType.accept_visitor(checker)
        if success == False:
            return False

    
    return True






