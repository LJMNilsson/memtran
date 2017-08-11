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

    collectorAndChecker = SlotCollectorAndForwardChecker(funDict, mangledModuleName,
        typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
         builtInFunsDict,
        directlyImportedFunsDictDict, otherImportedModulesFunDictDict    
    )

    return collectorAndChecker.visit(programAST)
 


#    funDictStack = [funDict]
# 
#    for statement in programAST.statements:
#        success = _slotcollect_statement(
#            statement, funDictStack, mangledModuleName, varBlockNumberList, 0, 
#            typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
#            builtInFunsDict,
#            directlyImportedFunsDictDict, otherImportedModulesFunDictDict,
#            {}
#        )
#        if success == False:
#            return False        
#
#    return True   



# This adds slot to the funDict, and returns True or False

# -- also, for identifier expressions, this simultaneously checks so that these (but not function calls) are defined before usage
# (it is handy to do this simultaneously with slot collection as we thus can simply check whether the slot has already been added to the dict...)    
    
class SlotCollectorAndForwardChecker(AbstractASTVisitor):


    def __init__(self, funDict, mangledModuleName,
        typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
        builtInFunsDict,
        directlyImportedFunsDictDict, otherImportedModulesFunDictDict
    ): 
        self.funDictStack = [funDict]
        self.mangledModuleName = mangledModuleName
        self.typeDict = typeDict
        self.directlyImportedTypesDictDict = directlyImportedTypesDictDict
        self.otherImportedModulesTypeDictDict = otherImportedModulesTypeDictDict
        self.builtInFunsDict = builtInFunsDict
        self.directlyImportedFunsDictDict = directlyImportedFunsDictDict
        self.otherImportedModulesFunDictDict = otherImportedModulesFunDictDict

        self.depth = 0
        self.namesIntoBlock = {}
        self.varBlockNumberList = []


    def visit(self, node):

        if isinstance(node, NStatement):
            if isinstance(node, NRefToFunctionDeclarationWithDefinition):

                actual = node.funs[node.funsIndex]             

                funcEntryList = self.funDictStack[len(self.funDictStack) - 1][actual.name.name].funEntries

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

                
                self.depth += 1
                self.funDictStack.append(funcEntry.localDict)
                self.varBlockNumberList.append(node.blockNumberStr)
                ###
                for statement in actual.body.statements:
                    success = self.visit(statement)
                    if success == False:
                        return False
                ###
                self.varBlockNumberList.pop()          
                self.funDictStack.pop()
                self.depth -= 1
             

                return True


            elif isinstance(node, NBlock):

                for nameIntoBlock, entry in self.namesIntoBlock.items():
                    if nameIntoBlock in self.funDictStack[len(self.funDictStack) - 1][node.blockEntryNumStr].localDict:
                        util.log_error(0, 0, "Name collision with name into block: " + nameIntoBlock) # should already be checked for though
                        return False
                    else:
                        self.funDictStack[len(self.funDictStack) - 1][node.blockEntryNumStr].localDict[nameIntoBlock] = entry            

        
                self.namesIntoBlock = {}

                self.depth += 1
                self.funDictStack.append(self.funDictStack[len(self.funDictStack) - 1][node.blockEntryNumStr].localDict)
                self.varBlockNumberList.append(node.blockEntryNumStr)
                ###    
                success = node.visit_children(self)
                if success == False:
                    return False
                ###
                self.varBlockNumberList.pop()
                self.funDictStack.pop()
                self.depth -= 1         
            

                return True      

            elif isinstance(node, NRefToTemplateDeclarationWithDefinition):

                return True  # we better have this here

            elif isinstance(node, NForStatement):

                intoNames = {}        

                if not node.rangeOrNull is None:                
                    if node.rangeOrNull.counterName.name in intoNames:
                        util.log_error(node.rangeOrNull.counterName.lineNr, node.rangeOrNull.counterName.rowNr, "Name collision.")
                        return False
                    else:
                        intoNames[node.rangeOrNull.counterName.name] = NameIntoBlockEntry(node.rangeOrNull.counterType.create_copy())


                for iteration in node.iterations:
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

                self.namesIntoBlock = intoNames

                success = node.visit_children(self)
                if success == False:
                    return False


                return True

            elif isinstance(node, NNormalAssignment):

                # first, we check the right hand side for forward calls. 
                # It is important that we do this _before_ we add the lhs var declarations, as we don't want recursive assignment to be possible...

                success = self.visit(node.value)
                if success == False:
                    return False


                for lhsEntry in node.leftHandSide:

                    if isinstance(lhsEntry, NVariableDeclaration):

                        if self.depth != 0 and lhsEntry.isInternal:  # we might as well check for this here
                            util.log_error(lhsEntry.lineNr, lhsEntry.rowNr, "Local variable marked as 'internal'.")
                            return False
                        
                        elif self.depth == 0 and lhsEntry.name.name in self.typeDict:
                            util.log_error(lhsEntry.name.lineNr, lhsEntry.name.rowNr, "Name collision with named type.")
                            return False        

                        elif lhsEntry.name.name in self.funDictStack[len(self.funDictStack) - 1]:
                            util.log_error(lhsEntry.name.lineNr, lhsEntry.name.rowNr, "Name collision.")  # can also be with recently added lhsEntries...
                            return False
                            
                        elif self.depth == 0 and lhsEntry.name.name in self.builtInFunsDict:
                            util.log_error(lhsEntry.name.lineNr, lhsEntry.name.rowNr, "Name collision with built-in function.")
                            return False
                        elif self.depth == 0:

                            for moduleName, directlyImportedFunsDict in self.directlyImportedFunsDictDict.items():
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
                        if self.depth > 0:
                            isGlobal = False

                        mangledName = name_mangler.mangle_var_name(lhsEntry.name.name, self.mangledModuleName, isGlobal, self.varBlockNumberList)

                        self.funDictStack[len(self.funDictStack) - 1][lhsEntry.name.name] = VarEntry(mangledName, lhsEntry.isMut, lhsEntry.isInternal, lhsEntry.theType.create_copy())


                    else: # lValueContainer hopefully...  
                        
                        success = self.visit(lhsEntry)
                        if success == False:
                            return False


                return True

            else:
                return node.visit_children(self)  # not completely needed for completely _all_ stmt kinds, but cannot hurt

        elif (isinstance(node, NProgram) or
            isinstance(node, NLValueContainer) or isinstance(node, NRange) or isinstance(node, NIteration) or
            isinstance(node, NElseIfClause) or 
            isinstance(node, NSwitchNormalCase) or isinstance(node, NContenttypeNormalCase)
        ):

            return node.visit_children(self)

        elif isinstance(node, NExpression):

            if isinstance(node, NIdentifierExpression):

                # first, check the indexings! :

                for indexing in node.indexings:        

                    if isinstance(indexing, NArrayIndexingIndex):

                        success = self.visit(indexing.indexExpression)
                        if success == False:
                            return False

                    elif isinstance(indexing, NStructIndexingIndex):

                        pass

                    elif isinstance(indexing, NVariantBoxCastIndex):

                        pass

                    elif isinstance(indexing, NTypeClarificationIndex):

                        pass

                    else:
                        util.log_error(node.lineNr, node.rowNr, "Slot collection: SHOULD NOT HAPPEN -- unknown indexing kind.")
                        return False


                foundDefinition = None

                if node.moduleNameOrNull is None:

                    for funDict in reversed(self.funDictStack):
                        if node.name.name in funDict:
                            foundDefinition = funDict[node.name.name]
                            break

                    if foundDefinition is None:
                        for moduleName, directlyImportedFunsDict in self.directlyImportedFunsDictDict.items():
                            if node.name.name in directlyImportedFunsDict:
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
                                    util.log_error(node.lineNr, node.rowNr, "Undetermined definition of identifier expression. SHOULD NOT HAPPEN")
                                    return False                

                    if foundDefinition is None:
                        if node.name.name in self.builtInFunsDict:
                            foundDefinition = self.builtInFunsDict[node.name.name]

                else:
                    if node.moduleNameOrNull in self.otherImportedModulesFunDictDict:

                        moduleDict = self.otherImportedModulesFunDictDict[node.moduleNameOrNull]

                        if node.name.name in moduleDict:
                            entry = moduleDict[node.name.name]

                            if isinstance(entry, FunListEntry):
                                for someFunOrTemplate in entry.funEntries:
                                    if not someFunOrTemplate.signature.isInternal:
                                        foundDefinition = entry
                                        break

                            elif isinstance(entry, VarEntry):
                                if not entry.isInternal:
                                    foundDefinition = entry
                            
                            else:            
                                util.log_error(node.lineNr, node.rowNr, "Undetermined definition of module specified identifier expression. SHOULD NOT HAPPEN")
                                return False   


                    else:
                        util.log_error(node.lineNr, node.rowNr, "Reference to module that has not been imported.")
                        return False
                         
            
                if foundDefinition is None:
                    util.log_error(node.lineNr, node.rowNr, "Usage of name that has not been declared.")
                    return False



                if isinstance(foundDefinition, NameIntoBlockEntry):

                    return True

                elif isinstance(foundDefinition, FunListEntry):

                    # If we come from the name in a funcall, we can allow forward calling in some cases, 
                    # more checking needing in later passes on this though

                    # else it is a function name used as a function type value... but which of the listed???
                    # we cannot check this until later when the function value has been resolved together with type checking. So return True here too...
                        
                    return True     



                elif isinstance(foundDefinition, VarEntry):

                    return True  # since we found it simultaneously, it should be declared before...

                elif isinstance(foundDefinition, BlockEntry):

                    util.log_error(node.lineNr, node.rowNr, "SHOULD NEVER HAPPEN: We found a block entry as the definition during slot forward usage check...")            
                    return False

                elif isinstance(foundDefinition, ParamEntry):

                    return True  # since we found it simultaneously, it should be declared before...

                else:

                    util.log_error(node.lineNr, node.rowNr, "SHOULD NOT HAPPEN: Found an unknown kind of definition entry during slot forward usage check...")        
                    return False

                return True # never reached though........

            elif isinstance(node, NCONTENTTYPEExpression):

                util.log_error(
                    node.lineNr, 
                    node.rowNr, 
                    "STORETYPE expressions are not yet implemented, starting from slot collection pass -- for certain reasons of name-into-expression extra complexity stuff."
                )
                return False
        
            else:
                return node.visit_children(self)

        elif isinstance(node, NIndexingIndex) or isinstance(node, NArg) or isinstance(node, NSWITCHNormalCase) or isinstance(node, NCONTENTTYPENormalCase): 
            # last one won't happen though  
            # we only reach these through expressions though

            return node.visit_children(self)

        else:
            return True






        

