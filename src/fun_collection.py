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




def run_pass(programAST, mangledModuleName, blockNumberList):   # returns a funDict

    funDict = {}

    for statement in programAST.statements:
        success = _funcollect_statement(funDict, statement, mangledModuleName, True, blockNumberList, 0)
        if success == False:
            return False        

    return funDict







# These 'funcollect' functions add to the funDict, and return True or False signalling success or not.

def _funcollect_statement(funDict, statement, mangledModuleName, isGlobal, blockNumberList, depth):
    
    if isinstance(statement, NRefToFunctionDeclarationWithDefinition):

        actual = statement.funs[statement.funsIndex]

        overloadNr = 0   # default
        if actual.name.name in funDict:
            overloadNr = len(funDict[actual.name.name].funEntries)

        mangledName = name_mangler.mangle_function_name(actual.name.name, mangledModuleName, isGlobal, blockNumberList, overloadNr)

        paramsCopy = []
        for param in actual.params:
            paramsCopy.append(param.create_copy())

        returnTypesCopy = []
        for returnType in actual.returnTypes:
            returnTypesCopy.append(returnType.create_copy())                
        
        signature = FunSignature(actual.isInternal, actual.isInline, actual.name.name, paramsCopy, returnTypesCopy) 
    
        localDict = {}

        if len(blockNumberList) <= depth:
            for i in range(len(blockNumberList), depth):
                blockNumberList.append(0)            
        else:
            blockNumberList[depth] += 1

        for stmt in actual.body.statements:
            success = _funcollect_statement(localDict, stmt, mangledModuleName, False, blockNumberList, depth + 1)
            if success == False:
                return False

        
        if actual.name.name in funDict:
            funDict[actual.name.name].funEntries.append(FunEntry(mangledName, signature, localDict, statement.funsIndex))
        else:
            funDict[actual.name.name] = FunListEntry([FunEntry(mangledName, signature, localDict, statement.funsIndex)])



        return True

    elif isinstance(statement, NBlock):

        if len(blockNumberList) <= depth:
            for i in range(len(blockNumberList), depth):
                blockNumberList.append(0)
        else:
            blockNumberList[depth] += 1

        for stmt in statement.statements:
            success = _funcollect_statement(funDict, stmt, mangledModuleName, False, blockNumberList, depth + 1)
            if success == False:
                return False

        return True

    elif isinstance(statement, NIfStatement):

        success = _funcollect_statement(funDict, statement.ifBlock, mangledModuleName, False, blockNumberList, depth)
        if success == False:
            return False

        for elseIfClause in statement.elseIfClauses:
            success = _funcollect_statement(funDict, elseIfClause.block, mangledModuleName, False, blockNumberList, depth)
            if success == False:
                return False
        
        if not statement.elseBlockOrNull is None:
            success = _funcollect_statement(funDict, statement.elseBlockOrNull, mangledModuleName, False, blockNumberList, depth)
            if success == False:
                return False
        
        return True

    elif isinstance(statement, NRefToTemplateDeclarationWithDefinition):

        if depth > 0:  # better double-check than check too few times...
            util.log_error(statement.lineNr, statement.rowNr, "Local template declarations are not allowed.")
            return False

        actual = statement.templates[statement.templatesIndex]

        mangledBasicName = name_mangler.mangle_basic_name(actual.name.name)

        overloadNr = 0   # default
        if actual.name.name in funDict:
            overloadNr = len(funDict[actual.name.name].funEntries)

        templateParams = []
        for tp in actual.templateParams:
            templateParams.append(tp.create_copy())

        paramsCopy = []
        for param in actual.params:
            paramsCopy.append(param.create_copy())

        returnTypesCopy = []
        for returnType in actual.returnTypes:
            returnTypesCopy.append(returnType.create_copy())                
        
        signature = FunSignature(actual.isInternal, actual.isInline, actual.name.name, paramsCopy, returnTypesCopy)

        
        if actual.name.name in funDict:
            funDict[actual.name.name].funEntries.append(TemplateEntry(mangledBasicName, templateParams, signature, statement.templatesIndex))
        else:
            funDict[actual.name.name] = FunListEntry([TemplateEntry(mangledBasicName, templateParams, signature, statement.templatesIndex)])



        return True


    elif isinstance(statement, NLoopStatement):

        success = _funcollect_statement(funDict, statement.block, mangledModuleName, False, blockNumberList, depth)
        if success == False:
            return False

        return True

    elif isinstance(statement, NForStatement):

        success = _funcollect_statement(funDict, statement.block, mangledModuleName, False, blockNumberList, depth)
        if success == False:
            return False

        return True

    elif isinstance(statement, NSwitchStatement):

        for case in statement.cases:
            success = _funcollect_statement(funDict, case.block, mangledModuleName, False, blockNumberList, depth)
            if success == False:
                return False

        if not statement.defaultCaseOrNull is None:
            success = _funcollect_statement(funDict, statement.defaultCaseOrNull, mangledModuleName, False, blockNumberList, depth)
            if success == False:
                return False
             
        return True

    elif isinstance(statement, NContenttypeStatement):

        for case in statement.cases:
            success = _funcollect_statement(funDict, case.block, mangledModuleName, False, blockNumberList, depth)
            if success == False:
                return False

        if not statement.defaultCaseOrNull is None:
            success = _funcollect_statement(funDict, statement.defaultCaseOrNull, mangledModuleName, False, blockNumberList, depth)
            if success == False:
                return False
             
        return True


    else:
        return True




            

        



