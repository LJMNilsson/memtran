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
#     along with the Memtran compiler.  If not, see http://www.gnu.org/licenses/ 


import util
from ast import *
import name_mangler
from fun_dict_stuff import *



# Since this pass needs context depending on where we are in the tree, it does not use the visitor stuff defined in ast.py



# Returns True or False depending on success

def run_pass(programAST, funDict, mangledModuleName, varBlockNumberList, typeDict, directlyImportedTypesDict, directlyImportedFunsDict): 
 
    for statement in programAST.statements:
        success = _slotcollect_statement(statement, funDict, mangledModuleName, varBlockNumberList, 0, typeDict, directlyImportedTypesDict, directlyImportedFunsDict, set([]))
        if success == False:
            return False        

    return True   
    
    

# Adds slots to the funDict, and returns True or False depending on success    

def _slotcollect_statement(statement, funDict, mangledModuleName, varBlockNumberList, depth, typeDict, directlyImportedTypesDict, directlyImportedFunsDict, namesIntoBlockSet):

    if isinstance(statement, NRefToFunctionDeclarationWithDefinition):

        actual = statement.funs[statement.funsIndex]              

        if len(varBlockNumberList) <= depth:
            for i in range(len(varBlockNumberList), depth + 1):
                varBlockNumberList.append(0)            
        else:
            varBlockNumberList[depth] += 1


        funcEntryList = funDict[actual.name.name].funEntries

        funcEntry = None # dummy
        for fentry in funcEntryList:
            if fentry.mangledName == actual.mangledName:
                funcEntry = fentry                 # we better find it... below code assumes != None
 


        intoNames = set([])
        for param in actual.params:
            intoNames.add(param.name.name)

            # also add the param to the funDict:
                        
            if param.name.name in funcEntry.localDict:
                util.log_error(param.name.lineNr, param.name.rowNr, "Name collision. #7979")  # can also be with recently added lhsEntries...
                return False
            
            funcEntry.localDict[param.name.name] = ParamEntry(param.create_copy())

        
        for stmt in actual.body.statements:
            success = _slotcollect_statement(
                stmt, funcEntry.localDict, mangledModuleName, varBlockNumberList, depth + 1, typeDict, directlyImportedTypesDict, directlyImportedFunsDict, intoNames
            )
            if success == False:
                return False



        return True

    elif isinstance(statement, NBlock):

        if len(varBlockNumberList) <= depth:
            for i in range(len(varBlockNumberList), depth + 1):
                varBlockNumberList.append(0)            
        else:
            varBlockNumberList[depth] += 1

        for stmt in statement.statements:
            success = _slotcollect_statement(
                stmt, 
                funDict[str(varBlockNumberList[depth])].localDict, 
                mangledModuleName, 
                varBlockNumberList, 
                depth + 1, 
                typeDict, 
                directlyImportedTypesDict, 
                directlyImportedFunsDict, 
                set([])
            )
            if success == False:
                return False            
    

        return True        

    elif isinstance(statement, NIfStatement):

        success = _slotcollect_statement(
            statement.ifBlock, funDict, mangledModuleName, varBlockNumberList, depth, typeDict, directlyImportedTypesDict, directlyImportedFunsDict, set([])
        )
        if success == False:
            return False

        for elseIfClause in statement.elseIfClauses:
            success = _slotcollect_statement(
                statement.elseIfClause, funDict, mangledModuleName, varBlockNumberList, depth, typeDict, directlyImportedTypesDict, directlyImportedFunsDict, set([])
            )
            if success == False:
                return False
        
        if not statement.elseBlockOrNull is None:
            success = _slotcollect_statement(
                statement.elseBlockOrNull, funDict, mangledModuleName, varBlockNumberList, depth, typeDict, directlyImportedTypesDict, directlyImportedFunsDict, set([])
            )
            if success == False:
                return False

        return True

    elif isinstance(statement, NRefToTemplateDeclarationWithDefinition):

        return True    # don't go further here I guess...

    elif isinstance(statement, NLoopStatement):

        success = _slotcollect_statement(
            statement.block, funDict, mangledModuleName, varBlockNumberList, depth, typeDict, directlyImportedTypesDict, directlyImportedFunsDict, set([])
        )
        if success == False:
            return False

        return True

    elif isinstance(statement, NForStatement):

        intoNames = set([])
        
        if not statement.rangeOrNull is None:
            if statement.rangeOrNull.counterName.name in intoNames:
                util.log_error(statement.rangeOrNull.counterName.lineNr, statement.rangeOrNull.counterName.rowNr, "Name collision.")
                return False
            else:
                intoNames.add(statement.rangeOrNull.counterName.name)

        for iteration in statement.iterations:
            if iteration.itName.name in intoNames:   # we call in the same way indepenently if it is an IterationOver or an IterationIn...
                util.log_error(iteration.itName.lineNr, iteration.itName.rowNr, "Name collision.")
                return False
            else:
                intoNames.add(iteration.itName.name)

        success = _slotcollect_statement(
            statement.block, funDict, mangledModuleName, varBlockNumberList, depth, typeDict, directlyImportedTypesDict, directlyImportedFunsDict, intoNames
        )
        if success == False:
            return False

        return True

    elif isinstance(statement, NSwitchStatement):

        for case in statement.cases:
            success = _slotcollect_statement(case.block, funDict, mangledModuleName, varBlockNumberList, depth, typeDict, directlyImportedTypesDict, directlyImportedFunsDict, set([]))
            if success == False:
                return False

        if not statement.defaultCaseOrNull is None:
            success = _slotcollect_statement(
                statement.defaultCaseOrNull, funDict, mangledModuleName, varBlockNumberList, depth, typeDict, directlyImportedTypesDict, directlyImportedFunsDict, set([])
            )
            if success == False:
                return False

        return True

    elif isinstance(statement, NContenttypeStatement):

        intoNames = set([])

        if isinstance(statement.switchValue, NIdentifierExpression) and (statement.switchValue.moduleNameOrNull is None):
            intoNames.add(statement.switchValue.name.name)    # we have to separately check for module name specified when actually generating code........

        for case in statement.cases:
            success = _slotcollect_statement(case.block, funDict, mangledModuleName, varBlockNumberList, depth, typeDict, directlyImportedTypesDict, directlyImportedFunsDict, intoNames)
            if success == False:
                return False

        if not statement.defaultCaseOrNull is None:
            success = _slotcollect_statement(
                statement.defaultCaseOrNull, funDict, mangledModuleName, varBlockNumberList, depth, typeDict, directlyImportedTypesDict, directlyImportedFunsDict, intoNames
            )
            if success == False:
                return False

        return True

    elif isinstance(statement, NNormalAssignment):

        for lhsEntry in statement.leftHandSide:

            if isinstance(lhsEntry, NVariableDeclaration):

                if depth != 0 and lhsEntry.isInternal:  # we might as well check for this here
                    util.log_error(lhsEntry.lineNr, lhsEntry.rowNr, "Local variable marked as 'internal'.")
                    return False
                
                elif depth == 0 and lhsEntry.name.name in typeDict:
                    util.log_error(lhsEntry.name.lineNr, lhsEntry.name.rowNr, "Name collision with named type.")
                    return False        
                elif depth == 0 and lhsEntry.name.name in directlyImportedTypesDict:
                    util.log_error(lhsEntry.name.lineNr, lhsEntry.name.rowNr, "Name collision with imported named type.")
                    return False
                elif lhsEntry.name.name in namesIntoBlockSet:
                    util.log_error(lhsEntry.name.lineNr, lhsEntry.name.rowNr, "Name collision with name going into this block.")
                    return False

                elif lhsEntry.name.name in funDict:
                    util.log_error(lhsEntry.name.lineNr, lhsEntry.name.rowNr, "Name collision.")  # can also be with recently added lhsEntries...
                    return False
                elif depth == 0 and lhsEntry.name.name in directlyImportedFunsDict:
                    util.log_error(lhsEntry.name.lineNr, lhsEntry.name.rowNr, "Name collision with imported name")    
                    return False

                
                isGlobal = True
                if depth > 0:
                    isGlobal = False

                mangledName = name_mangler.mangle_var_name(lhsEntry.name.name, mangledModuleName, isGlobal, varBlockNumberList[0:depth])

                funDict[lhsEntry.name.name] = VarEntry(mangledName, lhsEntry.isMut, lhsEntry.isInternal, lhsEntry.theType.create_copy())


            else:
                pass

        return True

    else:
        return True
