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

# This pass also simultaneously checks for forward usage of slots (not functions though!!! check for those later please!)

def run_pass(
    programAST, funDict, mangledModuleName, varBlockNumberList, 
    typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict, 
    builtInFunsDict,
    directlyImportedFunsDictDict, otherImportedModulesFunDictDict
): 

    funDictStack = [funDict]
 
    for statement in programAST.statements:
        success = _slotcollect_statement(
            statement, funDictStack, mangledModuleName, varBlockNumberList, 0, 
            typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
            builtInFunsDict,
            directlyImportedFunsDictDict, otherImportedModulesFunDictDict,
            {}
        )
        if success == False:
            return False        

    return True   
    
    

# Adds slots to the funDict, and returns True or False depending on success    

def _slotcollect_statement(
    statement, funDictStack, mangledModuleName, varBlockNumberList, depth, 
    typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
    builtInFunsDict,
    directlyImportedFunsDictDict, otherImportedModulesFunDictDict,
    namesIntoBlock
):

    if isinstance(statement, NRefToFunctionDeclarationWithDefinition):

        actual = statement.funs[statement.funsIndex]              

        if len(varBlockNumberList) <= depth:
            for i in range(len(varBlockNumberList), depth + 1):
                varBlockNumberList.append(0)            
        else:
            varBlockNumberList[depth] += 1


        funcEntryList = funDictStack[len(funDictStack) - 1][actual.name.name].funEntries

        funcEntry = None # dummy
        for fentry in funcEntryList:
            if fentry.mangledName == actual.mangledName:
                funcEntry = fentry                 # we better find it... below code assumes != None
  


        intoNames = set([])
        for param in actual.params:

            # add the param to the funDict:
                        
            if param.name.name in funcEntry.localDict:
                util.log_error(param.name.lineNr, param.name.rowNr, "Name collision. #7979")  # can also be with recently added lhsEntries...
                return False
            
            funcEntry.localDict[param.name.name] = ParamEntry(name_mangler.mangle_param_name(param.name.name), param.create_copy())

        
        for stmt in actual.body.statements:
            success = _slotcollect_statement(
                stmt, funDictStack + [funcEntry.localDict], mangledModuleName, varBlockNumberList, depth + 1, 
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                builtInFunsDict, 
                directlyImportedFunsDictDict, otherImportedModulesFunDictDict,
                {}
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


        for nameIntoBlock, entry in namesIntoBlock.items():
            if nameIntoBlock in funDictStack[len(funDictStack) - 1][str(varBlockNumberList[depth])].localDict:
                util.log_error(0, 0, "Name collision with name into block: " + nameIntoBlock) # should already be checked for though
                return False
            else:
                funDictStack[len(funDictStack) - 1][str(varBlockNumberList[depth])].localDict[nameIntoBlock] = entry            


        statement.blockEntryNumStr = str(varBlockNumberList[depth])   # set this so that name into blockers can find the block later when specifiying their type just in time...


        for stmt in statement.statements:
            success = _slotcollect_statement(
                stmt, 
                funDictStack + [funDictStack[len(funDictStack) - 1][str(varBlockNumberList[depth])].localDict], 
                mangledModuleName, 
                varBlockNumberList, 
                depth + 1, 
                typeDict, 
                directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                builtInFunsDict, 
                directlyImportedFunsDictDict, otherImportedModulesFunDictDict,
                {}
            )
            if success == False:
                return False            
    

        return True        

    elif isinstance(statement, NIfStatement):

        success = _check_expression_for_forward_slot_usage(
            statement.condition, funDictStack, 
            typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
            builtInFunsDict,
            directlyImportedFunsDictDict, otherImportedModulesFunDictDict, 
            False
        )
        if success == False:
            return False

        success = _slotcollect_statement(
            statement.ifBlock, funDictStack, mangledModuleName, varBlockNumberList, depth, 
            typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
            builtInFunsDict,
            directlyImportedFunsDictDict, otherImportedModulesFunDictDict,
            {}
        )
        if success == False:
            return False

        for elseIfClause in statement.elseIfClauses:
            success = _check_expression_for_forward_slot_usage(
                elseIfClause.condition, funDictStack, 
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                builtInFunsDict, 
                directlyImportedFunsDictDict, otherImportedModulesFunDictDict, 
                False
            )
            if success == False:
                return False

            success = _slotcollect_statement(
                elseIfClause.block, funDictStack, mangledModuleName, varBlockNumberList, depth, 
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict, 
                builtInFunsDict,
                directlyImportedFunsDictDict, otherImportedModulesFunDictDict,
                {}
            )
            if success == False:
                return False
        
        if not statement.elseBlockOrNull is None:
            success = _slotcollect_statement(
                statement.elseBlockOrNull, funDictStack, mangledModuleName, varBlockNumberList, depth, 
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                builtInFunsDict,
                directlyImportedFunsDictDict, otherImportedModulesFunDictDict,
                {}
            )
            if success == False:
                return False

        return True

    elif isinstance(statement, NRefToTemplateDeclarationWithDefinition):

        return True    # don't go further here I guess...

    elif isinstance(statement, NLoopStatement):

        success = _slotcollect_statement(
            statement.block, funDictStack, mangledModuleName, varBlockNumberList, depth, 
            typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
            builtInFunsDict, 
            directlyImportedFunsDictDict, otherImportedModulesFunDictDict,
            {}
        )
        if success == False:
            return False

        return True

    elif isinstance(statement, NForStatement):
    
        intoNames = {}        

        if not statement.rangeOrNull is None:
            success = _check_expression_for_forward_slot_usage(
                statement.rangeOrNull.rangeFrom, funDictStack, 
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                builtInFunsDict,
                directlyImportedFunsDictDict, otherImportedModulesFunDictDict, 
                False
            )
            if success == False:
                return False

            success = _check_expression_for_forward_slot_usage(
                statement.rangeOrNull.rangeTo, funDictStack, 
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                builtInFunsDict,
                directlyImportedFunsDictDict, otherImportedModulesFunDictDict, 
                False
            )
            if success == False:
                return False

            if statement.rangeOrNull.counterName.name in intoNames:
                util.log_error(statement.rangeOrNull.counterName.lineNr, statement.rangeOrNull.counterName.rowNr, "Name collision.")
                return False
            else:
                intoNames[statement.rangeOrNull.counterName.name] = NameIntoBlockEntry(statement.rangeOrNull.counterType.create_copy())


        for iteration in statement.iterations:
            if isinstance(iteration, NIterationIn):
                success = _check_expression_for_forward_slot_usage(
                    iteration.arrayExpression, funDictStack, 
                    typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                    builtInFunsDict,
                    directlyImportedFunsDictDict, otherImportedModulesFunDictDict, 
                    False
                )
                if success == False:
                    return False

                if not iteration.indexfactorOrNull is None:
                    success = _check_expression_for_forward_slot_usage(
                        iteration.indexfactorOrNull, funDictStack, 
                        typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                        builtInFunsDict,
                        directlyImportedFunsDictDict, otherImportedModulesFunDictDict, 
                        False
                    )
                    if success == False:
                        return False

                if not iteration.indexoffsetOrNull is None:
                    success = _check_expression_for_forward_slot_usage(
                        iteration.indexoffsetOrNull, funDictStack, 
                        typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                        builtInFunsDict,
                        directlyImportedFunsDictDict, otherImportedModulesFunDictDict, 
                        False
                    )
                    if success == False:
                        return False

            else: # NIterationOver, hopefully:
        
                success = _check_expression_for_forward_slot_usage(
                    iteration.arrayLValue.lValueExpression, funDictStack, 
                    typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                    builtInFunsDict,
                    directlyImportedFunsDictDict, otherImportedModulesFunDictDict, 
                    False
                )
                if success == False:
                    return False

                if not iteration.indexfactorOrNull is None:
                    success = _check_expression_for_forward_slot_usage(
                        iteration.indexfactorOrNull, funDictStack, 
                        typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                        builtInFunsDict,
                        directlyImportedFunsDictDict, otherImportedModulesFunDictDict, 
                        False
                    )
                    if success == False:
                        return False

                if not iteration.indexoffsetOrNull is None:
                    success = _check_expression_for_forward_slot_usage(
                        iteration.indexoffsetOrNull, funDictStack, 
                        typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                        builtInFunsDict,
                        directlyImportedFunsDictDict, otherImportedModulesFunDictDict, 
                        False
                    )
                    if success == False:
                        return False



            if iteration.itName.name in intoNames:   # we call in the same way indepenently if it is an IterationOver or an IterationIn...
                util.log_error(iteration.itName.lineNr, iteration.itName.rowNr, "Name collision.")
                return False
            else:
                if iteration.itTypeOrNull is None:
                    intoNames[iteration.itName.name] = NameIntoBlockEntry(
                        NStructType(iteration.lineNr, iteration.rowNr, NIdentifier(iteration.lineNr, iteration.rowNr, "TYPE_UNKNOWN_AS_YET"), [])
                    )
                else:
                    intoNames[iteration.itName.name] = NameIntoBlockEntry(iteration.itTypeOrNull.create_copy())


        success = _slotcollect_statement(
            statement.block, funDictStack, mangledModuleName, varBlockNumberList, depth, 
            typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
            builtInFunsDict,
            directlyImportedFunsDictDict, otherImportedModulesFunDictDict,
            intoNames
        )
        if success == False:
            return False

        return True

    elif isinstance(statement, NSwitchStatement):

        success = _check_expression_for_forward_slot_usage(
            statement.switchValue, funDictStack, 
            typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
            builtInFunsDict,
            directlyImportedFunsDictDict, otherImportedModulesFunDictDict, 
            False
        )
        if success == False:
            return False

        for case in statement.cases:
            for caseValue in case.caseValues:
                success = _check_expression_for_forward_slot_usage(
                    caseValue, funDictStack, 
                    typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                    builtInFunsDict,
                    directlyImportedFunsDictDict, otherImportedModulesFunDictDict, 
                    False
                )
                if success == False:
                    return False

            success = _slotcollect_statement(
                case.block, funDictStack, mangledModuleName, varBlockNumberList, depth, 
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict, 
                builtInFunsDict,
                directlyImportedFunsDictDict, otherImportedModulesFunDictDict,
                {}
            )
            if success == False:
                return False

        if not statement.defaultCaseOrNull is None:
            success = _slotcollect_statement(
                statement.defaultCaseOrNull, funDictStack, mangledModuleName, varBlockNumberList, depth, 
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict, 
                builtInFunsDict,
                directlyImportedFunsDictDict, otherImportedModulesFunDictDict,
                {}
            )
            if success == False:
                return False

        return True

    elif isinstance(statement, NContenttypeStatement):

        success = _check_expression_for_forward_slot_usage(
            statement.switchValue, funDictStack, 
            typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
            builtInFunsDict,
            directlyImportedFunsDictDict, otherImportedModulesFunDictDict, 
            False
        )
        if success == False:
            return False

        intoNames = {}

        # if isinstance(statement.switchValue, NIdentifierExpression) and (statement.switchValue.moduleNameOrNull is None):
        #     intoNames[statement.switchValue.name.name] = NameIntoBlockEntry(NUnknownType(statement.switchValue.lineNr, statement.switchValue.rowNr))    
            # we have to separately check for module name specified when actually generating code........

            # we have to expand this statement simultaneously with type checking and annotation, so the above is probably bogus
            # since it isn't a proper new into-name... so it is commented out for now.

        for case in statement.cases:
            success = _slotcollect_statement(
                case.block, funDictStack, mangledModuleName, varBlockNumberList, depth, 
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict, 
                builtInFunsDict,
                directlyImportedFunsDictDict, otherImportedModulesFunDictDict,
                intoNames
            )
            if success == False:
                return False

        if not statement.defaultCaseOrNull is None:
            success = _slotcollect_statement(
                statement.defaultCaseOrNull, funDictStack, mangledModuleName, varBlockNumberList, depth, 
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                builtInFunsDict, 
                directlyImportedFunsDictDict, otherImportedModulesFunDictDict,
                intoNames
            )
            if success == False:
                return False

        return True

    elif isinstance(statement, NNormalAssignment):

        # first, we check the right hand side for forward calls. 
        # It is important that we do this _before_ we add the lhs var declarations, as we don't want recursive assignment to be possible...

        success = _check_expression_for_forward_slot_usage(
            statement.value, funDictStack, 
            typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
            builtInFunsDict,
            directlyImportedFunsDictDict, otherImportedModulesFunDictDict, 
            False
        )
        if success == False:
            return False


        for lhsEntry in statement.leftHandSide:

            if isinstance(lhsEntry, NVariableDeclaration):

                if depth != 0 and lhsEntry.isInternal:  # we might as well check for this here
                    util.log_error(lhsEntry.lineNr, lhsEntry.rowNr, "Local variable marked as 'internal'.")
                    return False
                
                elif depth == 0 and lhsEntry.name.name in typeDict:
                    util.log_error(lhsEntry.name.lineNr, lhsEntry.name.rowNr, "Name collision with named type.")
                    return False        

                elif lhsEntry.name.name in funDictStack[len(funDictStack) - 1]:
                    util.log_error(lhsEntry.name.lineNr, lhsEntry.name.rowNr, "Name collision.")  # can also be with recently added lhsEntries...
                    return False
                    
                elif depth == 0 and lhsEntry.name.name in builtInFunsDict:
                    util.log_error(lhsEntry.name.lineNr, lhsEntry.name.rowNr, "Name collision with built-in function.")
                    return False
                elif depth == 0:
                    for moduleName, directlyImportedTypesDict in directlyImportedTypesDictDict.items():
                        if lhsEntry.name.name in directlyImportedTypesDict:                            
                            util.log_error(lhsEntry.name.lineNr, lhsEntry.name.rowNr, "Name collision with imported named type.")
                            return False

                    for moduleName, directlyImportedFunsDict in directlyImportedFunsDictDict.items():
                        if lhsEntry.name.name in directlyImportedFunsDict:
                            entry = directlyImportedFunsDict[lhsEntry.name.name]

                            if isinstance(entry, FunListEntry):
                                for someFunOrTemplate in entry.funEntries:
                                    if not someFunOrTemplate.signature.isInternal:
                                        util.log_error(lhsEntry.name.lineNr, lhsEntry.name.rowNr, "Name collision with imported function or template.")
                                        return False

                            elif isinstance(entry, VarEntry):
                                if not entry.isInternal:
                                    util.log_error(lhsEntry.name.lineNr, lhsEntry.name.rowNr, "Name collision with imported name.")    
                                    return False

                            elif isinstance(entry, BlockEntry):
                                util.log_error(lhsEntry.name.lineNr, lhsEntry.name.rowNr, "Name collision with block. SHOULD NOT HAPPEN.")
                                return False

                            elif isinstance(entry, ParamEntry):
                                util.log_error(lhsEntry.name.lineNr, lhsEntry.name.rowNr, "Name collision with global param...??? SHOULD NOT HAPPEN.")
                                return False

                            elif isinstance(entry, NameIntoBlockEntry):
                                util.log_error(lhsEntry.name.lineNr, lhsEntry.name.rowNr, "Name collision with global name into block...??? SHOULD NOT HAPPEN.")
                                return False

                            else:
                                util.log_error(lhsEntry.name.lineNr, lhsEntry.name.rowNr, "Name collision with unknown entry. SHOULD NOT HAPPEN.")
                                return False                           


                
                isGlobal = True
                if depth > 0:
                    isGlobal = False

                mangledName = name_mangler.mangle_var_name(lhsEntry.name.name, mangledModuleName, isGlobal, varBlockNumberList[0:depth])

                funDictStack[len(funDictStack) - 1][lhsEntry.name.name] = VarEntry(mangledName, lhsEntry.isMut, lhsEntry.isInternal, lhsEntry.theType.create_copy())


            else: # lValueContainer hopefully...  
                
                success = _check_expression_for_forward_slot_usage(
                    lhsEntry.lValueExpression, funDictStack, 
                    typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                    builtInFunsDict,
                    directlyImportedFunsDictDict, otherImportedModulesFunDictDict, 
                    False
                )
                if success == False:
                    return False


        return True

    elif (isinstance(statement, NModuloAssignment) or
        isinstance(statement, NMultiplicationAssignment) or
        isinstance(statement, NDivisionAssignment) or
        isinstance(statement, NAdditionAssignment) or
        isinstance(statement, NSubtractionAssignment)
    ):

        success = _check_expression_for_forward_slot_usage(
            statement.value, funDictStack, 
            typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
            builtInFunsDict,
            directlyImportedFunsDictDict, otherImportedModulesFunDictDict, 
            False
        )
        if success == False:
            return False


        for lhsEntry in statement.leftHandSide:
            success = _check_expression_for_forward_slot_usage(
                lhsEntry.lValueExpression, funDictStack, 
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                builtInFunsDict,
                directlyImportedFunsDictDict, otherImportedModulesFunDictDict, 
                False
            )
            if success == False:
                return False

        return True


    elif isinstance(statement, NReturnStatement):

        for returnExpression in statement.returnExpressions:
            success = _check_expression_for_forward_slot_usage(
                returnExpression, funDictStack, 
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                builtInFunsDict,
                directlyImportedFunsDictDict, otherImportedModulesFunDictDict, 
                False
            )
            if success == False:
                return False

        return True

    elif isinstance(statement, NFunctionCallStatement):  # forgot this one...

        success = _check_expression_for_forward_slot_usage(
            statement.functionCall, funDictStack, 
            typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
            builtInFunsDict,
            directlyImportedFunsDictDict, otherImportedModulesFunDictDict, 
            False
        )
        if success == False:
            return False

        return True

    else:    
        return True








# We cannot use visitor here either because of fromFunctionCallFlag

# Returns True or False depending on success.

def _check_expression_for_forward_slot_usage(
    expr, funDictStack, 
    typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
    builtInFunsDict,    
    directlyImportedFunsDictDict, otherImportedModulesFunDictDict, 
    fromFunctionCallFlag
):

    if isinstance(expr, NIdentifierExpression):

        # first, check the indexings! :

        for indexing in expr.indexings:        

            if isinstance(indexing, NArrayIndexingIndex):

                success = _check_expression_for_forward_slot_usage(
                    indexing.indexExpression, funDictStack, 
                    typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                    builtInFunsDict,
                    directlyImportedFunsDictDict, otherImportedModulesFunDictDict, 
                    False
                )
                if success == False:
                    return False

            elif isinstance(indexing, NStructIndexingIndex):

                pass

            elif isinstance(indexing, NVariantBoxCastIndex):

                pass

            elif isinstance(indexing, NTypeClarificationIndex):

                pass

            else:
                util.log_error(expr.lineNr, expr.rowNr, "Slot collection: SHOULD NOT HAPPEN -- unknown indexing kind.")
                return False


        foundDefinition = None

        if expr.moduleNameOrNull is None:

            for funDict in reversed(funDictStack):
                if expr.name.name in funDict:
                    foundDefinition = funDict[expr.name.name]
                    break

            if foundDefinition is None:
                for moduleName, directlyImportedFunsDict in directlyImportedFunsDictDict.items():
                    if expr.name.name in directlyImportedFunsDict:
                        entry = directlyImportedFunsDict[expr.name.name]

                        if isinstance(entry, FunListEntry):
                            for someFunOrTemplate in entry.funEntries:
                                if not someFunOrTemplate.signature.isInternal:
                                    foundDefinition = entry
                                    break
                            
                            if not foundDefinition is None:
                                break     # instead of labeled break right above, which is not available
    
                        elif isinstance(entry, VarEntry):
                            if not entry.isInternal:
                                foundDefinition = entry
                                break

                        else:
                            util.log_error(expr.lineNr, expr.rowNr, "Undetermined definition of identifier expression. SHOULD NOT HAPPEN")
                            return False                

            if foundDefinition is None:
                if expr.name.name in builtInFunsDict:
                    foundDefinition = builtInFunsDict[expr.name.name]

        else:
            if expr.moduleNameOrNull in otherImportedModulesFunDictDict:

                moduleDict = otherImportedModulesFunDictDict[expr.moduleNameOrNull]

                if expr.name.name in moduleDict:
                    entry = moduleDict[expr.name.name]

                    if isinstance(entry, FunListEntry):
                        for someFunOrTemplate in entry.funEntries:
                            if not someFunOrTemplate.signature.isInternal:
                                foundDefinition = entry
                                break

                    elif isinstance(entry, VarEntry):
                        if not entry.isInternal:
                            foundDefinition = entry
                    
                    else:            
                        util.log_error(expr.lineNr, expr.rowNr, "Undetermined definition of module specified identifier expression. SHOULD NOT HAPPEN")
                        return False   


            else:
                util.log_error(expr.lineNr, expr.rowNr, "Reference to module that has not been imported.")
                return False
                 
    
        if foundDefinition is None:
            util.log_error(expr.lineNr, expr.rowNr, "Usage of name that has not been declared.")
            return False



        if isinstance(foundDefinition, NameIntoBlockEntry):

            return True

        elif isinstance(foundDefinition, FunListEntry):

            if fromFunctionCallFlag: # If we come from the name in a funcall, we can allow forward calling in some cases, 
                                # more checking needing in later passes on this though

                return True

            else:  # else it is a function name used as a function type value... but which of the listed???
                   # we cannot check this until later when the function value has been resolved together with type checking. So return True here too...
                
                return True     



        elif isinstance(foundDefinition, VarEntry):

            return True  # since we found it simultaneously, it should be declared before...

        elif isinstance(foundDefinition, BlockEntry):

            util.log_error(expr.lineNr, expr.rowNr, "SHOULD NEVER HAPPEN: We found a block entry as the definition during slot forward usage check...")            
            return False

        elif isinstance(foundDefinition, ParamEntry):

            return True  # since we found it simultaneously, it should be declared before...

        else:

            util.log_error(expr.lineNr, expr.rowNr, "SHOULD NOT HAPPEN: Found an unknown kind of definition entry during slot forward usage check...")        
            return False



    elif isinstance(expr, NNilExpression):

        return True

    elif isinstance(expr, NTrueExpression):

        return True

    elif isinstance(expr, NFalseExpression):

        return True

    elif isinstance(expr, NIntegerExpression):

        return True

    elif isinstance(expr, NFloatingPointNumberExpression):

        return True

    elif isinstance(expr, NStringExpression):

        return True

    elif isinstance(expr, NArrayExpressionIndividualValues):

        for subexpr in expr.values:
            success = _check_expression_for_forward_slot_usage(
                subexpr, funDictStack, 
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                builtInFunsDict,
                directlyImportedFunsDictDict, otherImportedModulesFunDictDict, 
                False
            )
            if success == False:
                return False

        return True

    elif isinstance(expr, NArrayExpressionNoInitialization):

        success = _check_expression_for_forward_slot_usage(
            expr.length, funDictStack, 
            typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
            builtInFunsDict,
            directlyImportedFunsDictDict, otherImportedModulesFunDictDict, 
            False
        )
        if success == False:
            return False

        return True

    elif isinstance(expr, NArrayExpressionRepeatedValue):

        success = _check_expression_for_forward_slot_usage(
            expr.repeatedValue, funDictStack, 
            typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
            builtInFunsDict,
            directlyImportedFunsDictDict, otherImportedModulesFunDictDict, 
            False
        )
        if success == False:
            return False

        success = _check_expression_for_forward_slot_usage(
            expr.length, funDictStack, 
            typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
            builtInFunsDict,
            directlyImportedFunsDictDict, otherImportedModulesFunDictDict, 
            False
        )
        if success == False:
            return False

        return True

    elif isinstance(expr, NStructExpression):

        for post in expr.posts:
            success = _check_expression_for_forward_slot_usage(
                post.value, funDictStack, 
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                builtInFunsDict,
                directlyImportedFunsDictDict, otherImportedModulesFunDictDict, 
                False
            )
            if success == False:
                return False

        return True

    elif isinstance(expr, NVariantBoxExpression):

        success = _check_expression_for_forward_slot_usage(
            expr.expression, funDictStack, 
            typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
            builtInFunsDict,    
            directlyImportedFunsDictDict, otherImportedModulesFunDictDict, 
            False
        )
        if success == False:
            return False

        return True

    elif isinstance(expr, NTypeClarifiedExpression):

        success = _check_expression_for_forward_slot_usage(
            expr.expression, funDictStack, 
            typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
            builtInFunsDict,
            directlyImportedFunsDictDict, otherImportedModulesFunDictDict, 
            False
        )
        if success == False:
            return False

        return True

    elif isinstance(expr, NArrayIndexing):

        success = _check_expression_for_forward_slot_usage(
            expr.arrayExpression, funDictStack, 
            typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
            builtInFunsDict,
            directlyImportedFunsDictDict, otherImportedModulesFunDictDict, 
            False
        )
        if success == False:
            return False

        success = _check_expression_for_forward_slot_usage(
            expr.indexExpression, funDictStack, 
            typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
            builtInFunsDict,
            directlyImportedFunsDictDict, otherImportedModulesFunDictDict, 
            False
        )
        if success == False:
            return False

        return True

    elif isinstance(expr, NStructIndexing):

        success = _check_expression_for_forward_slot_usage(
            expr.structExpression, funDictStack, 
            typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
            builtInFunsDict,
            directlyImportedFunsDictDict, otherImportedModulesFunDictDict, 
            False
        )
        if success == False:
            return False

        return True

    elif isinstance(expr, NVariantBoxCastExpression):

        success = _check_expression_for_forward_slot_usage(
            expr.expression, funDictStack, 
            typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
            builtInFunsDict,
            directlyImportedFunsDictDict, otherImportedModulesFunDictDict, 
            False
        )
        if success == False:
            return False

        return True

    elif isinstance(expr, NAndSymbolExpression) or isinstance(expr, NOrSymbolExpression):

        success = _check_expression_for_forward_slot_usage(
            expr.leftExpression, funDictStack, 
            typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
            builtInFunsDict,
            directlyImportedFunsDictDict, otherImportedModulesFunDictDict, 
            False
        )
        if success == False:
            return False

        success = _check_expression_for_forward_slot_usage(
            expr.rightExpression, funDictStack, 
            typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
            builtInFunsDict,
            directlyImportedFunsDictDict, otherImportedModulesFunDictDict, 
            False
        )
        if success == False:
            return False

        return True

    elif isinstance(expr, NEndExpression):

        util.log_error(expr.lineNr, expr.rowNr, "SHOULD NOT HAPPEN: slot forward usage checking encountered unexpanded end expression...")
        return False

    elif isinstance(expr, NFunctionCall):

        success = _check_expression_for_forward_slot_usage(
            expr.functionExpression, funDictStack, 
            typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
            builtInFunsDict,
            directlyImportedFunsDictDict, otherImportedModulesFunDictDict, 
            True   # observe the flag here, hackish...
        )
        if success == False:
            return False

        for arg in expr.args:
            if isinstance(arg, NNormalArg):

                success = _check_expression_for_forward_slot_usage(
                    arg.argExpression, funDictStack, 
                    typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                    builtInFunsDict,
                    directlyImportedFunsDictDict, otherImportedModulesFunDictDict, 
                    False
                )
                if success == False:
                    return False

            else: # NRefArg hopefully

                success = _check_expression_for_forward_slot_usage(
                    arg.lValueContainer.lValueExpression, funDictStack, 
                    typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                    builtInFunsDict,
                    directlyImportedFunsDictDict, otherImportedModulesFunDictDict, 
                    False
                )
                if success == False:
                    return False

        return True

    elif isinstance(expr, NIFExpression):

        success = _check_expression_for_forward_slot_usage(
            expr.condition, funDictStack, 
            typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
            builtInFunsDict,
            directlyImportedFunsDictDict, otherImportedModulesFunDictDict, 
            False
        )
        if success == False:
            return False

        success = _check_expression_for_forward_slot_usage(
            expr.thenExpression, funDictStack, 
            typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
            builtInFunsDict,
            directlyImportedFunsDictDict, otherImportedModulesFunDictDict, 
            False
        )
        if success == False:
            return False

        success = _check_expression_for_forward_slot_usage(
            expr.elseExpression, funDictStack, 
            typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
            builtInFunsDict,
            directlyImportedFunsDictDict, otherImportedModulesFunDictDict, 
            False
        )
        if success == False:
            return False

        return True

    elif isinstance(expr, NSWITCHExpression):

        success = _check_expression_for_forward_slot_usage(
            expr.switchValue, funDictStack, 
            typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
            builtInFunsDict,
            directlyImportedFunsDictDict, otherImportedModulesFunDictDict, 
            False
        )
        if success == False:
            return False

        for case in expr.cases:
            for caseValue in case.caseValues:
                success = _check_expression_for_forward_slot_usage(
                    caseValue, funDictStack, 
                    typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                    builtInFunsDict,
                    directlyImportedFunsDictDict, otherImportedModulesFunDictDict, 
                    False
                )
                if success == False:
                    return False

            success = _check_expression_for_forward_slot_usage(
                case.value, funDictStack, 
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                builtInFunsDict,
                directlyImportedFunsDictDict, otherImportedModulesFunDictDict, 
                False
            )
            if success == False:
                return False

        return True

    elif isinstance(expr, NCONTENTTYPEExpression):

        util.log_error(
            expr.lineNr, 
            expr.rowNr, 
            "STORETYPE expressions are not yet implemented, starting from slot collection pass -- for certain reasons of name-into-expression extra complexity stuff."
        )
        return False

    else:
        util.log_error(expr.lineNr, expr.rowNr, "Type inference strangely encountered unknown expression.")
        return False




        

