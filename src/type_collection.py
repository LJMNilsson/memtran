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

def gather(astProgram, mangledModuleName, directlyImportedTypesDictDict):

    typeDict = {}

    for statement in astProgram.statements:

        if isinstance(statement, NTypeDeclarationWithDefinition):

            if statement.name.name in typeDict:

                util.log_error(statement.name.lineNr, statement.name.typeNr, "Name collision.")
                return False

            else:

                for moduleName, directlyImportedTypesDict in directlyImportedTypesDictDict.items():

                    if statement.name.name in directlyImportedTypesDict:

                        util.log_error(statement.name.lineNr, statement.name.typeNr, "Name collision with directly imported type.")
                        return False
               

                dictAddition = statement.create_copy()

                dictAddition.mangledName = name_mangler.mangle_type_name(statement.name.name, mangledModuleName)

                typeDict[statement.name.name] = dictAddition


    return typeDict        




class _CheckTypesVisitor(AbstractASTVisitor):

    # TODO: add the whole module identifier business!


    def __init__(self, allowedParamNamesList, typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict):
            

        self.allowedParamNamesSet = set(allowedParamNamesList)
        self.typeDict = typeDict
        self.directlyImportedTypesDictDict = directlyImportedTypesDictDict
        self.otherImportedModulesTypeDictDict = otherImportedModulesTypeDictDict
        


    def visit(self, node):

        if isinstance(node, NParametrizedIdentifierType):

            found = False
            typeParamsOrNull = None

            if node.moduleNameOrNull is None:

                if node.name.name in self.allowedParamNamesSet:
                    found = True   
                    typeParamsOrNull = None    # in this case, we may never have params so this will not work out below
 
                elif node.name.name in self.typeDict:
                    found = True
                    typeParamsOrNull = self.typeDict[node.name.name].paramsOrNull
          
                else:
                    for moduleName, directlyImportedTypesDict in self.directlyImportedTypesDictDict:
                        if node.name.name in directlyImportedTypesDict:
                            found = True
                            typeParamsOrNull = directlyImportedTypesDict[node.name.name].paramsOrNull

            else:
                if not node.moduleNameOrNull.name in self.otherImportedModulesTypeDictDict.items():
                    util.log_error(node.lineNr, node.rowNr, "Using a non-imported module name.")
                    return False

                moduleTypeDict = self.otherImportedModulesTypeDictDict[node.moduleNameOrNull.name]

                if node.name.name in moduleTypeDict:
                    found = True
                    typeParamsOrNull = moduleTypeDict[node.name.name].paramsOrNull



            if not found:
                util.log_error(node.lineNr, node.rowNr, "Undefined type name used.")
                return False

            paramsLen = len(node.params)

            if typeParamsOrNull is None:
                util.log_error(node.lineNr, node.rowNr, "Parametrized usage of non-parametrized named type (or param).")
                return False
            else:
                if paramsLen != len(typeParamsOrNull):
                    util.log_error(node.lineNr, node.rowNr, "Wrong number of arguments to parametrized type.")
                    return False            
            

            success = node.visit_children(self)
            if success == False:
                return False

            return True
            
        
        elif isinstance(node, NIdentifierType):

            found = False
            typeParamsOrNull = None

            if node.moduleNameOrNull is None:

                if node.name.name in self.allowedParamNamesSet:
                    found = True
                    typeParamsOrNull = None    
 
                elif node.name.name in self.typeDict:
                    found = True
                    typeParamsOrNull = self.typeDict[node.name.name].paramsOrNull

                else:
                    for moduleName, directlyImportedTypesDict in self.directlyImportedTypesDictDict.items():
                        if node.name.name in directlyImportedTypesDict:
                            found = True
                            typeParamsOrNull = directlyImportedTypesDict[node.name.name].paramsOrNull

            else:
                if not node.moduleNameOrNull.name in self.otherImportedModulesTypeDictDict:
                    util.log_error(node.lineNr, node.rowNr, "Using a non-imported module name.")
                    return False

                moduleTypeDict = self.otherImportedModulesTypeDictDict[node.moduleNameOrNull.name]

                if node.name.name in moduleTypeDict:
                    found = True
                    typeParamsOrNull = moduleTypeDict[node.name.name].paramsOrNull



            if not found:
                util.log_error(node.lineNr, node.rowNr, "Undefined type name used. #2707")
                return False

            else:

                if not typeParamsOrNull is None:    
                    util.log_error(node.lineNr, node.rowNr, "Non-parametrized usage of parametrized named type.")
                    return False


            return True




        else:
            success = node.visit_children(self)
            if success == False:
                return False

            return True    

        



# Performs additional checks. Returns True for pass, or False for error.
# TODO: Allow mathching against module imported names

def check(typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict):

    for typeName, declaration in typeDict.items():

        params = []

        if not declaration.paramsOrNull is None:
            for ident in declaration.paramsOrNull:
                params.append(ident.name)        

        checker = _CheckTypesVisitor(params, typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict)

        success = checker.visit(declaration.theType)
        if success == False:
            return False    


    
    return True






