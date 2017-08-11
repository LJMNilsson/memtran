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







def run_pass(programAST, mangledModuleName, blockNumberList, typeDict, directlyImportedTypesDictDict):   # returns a funDict, or False on no success...

    funDict = {}

    funCollector = FunCollector(funDict, mangledModuleName, blockNumberList, typeDict, directlyImportedTypesDictDict)

    result = funCollector.visit(programAST)
    if result == False:
        return False
    else:
        return funCollector.funDict 








# This adds to the funDict, and return True or False signalling success or not.

class FunCollector(AbstractASTVisitor):

    def __init__(self, funDict, mangledModuleName, blockNumberList, typeDict, directlyImportedTypesDictDict):
        self.funDict = funDict
        self.blockNumberList = blockNumberList
        self.mangledModuleName = mangledModuleName
        self.typeDict = typeDict
        self.directlyImportedTypesDictDict = directlyImportedTypesDictDict

        self.depth = 0
        self.isGlobal = True
        self.isInsideExpanded = False

    
    def visit(self, node):
        if isinstance(node, NRefToFunctionDeclarationWithDefinition):

            if self.isInsideExpanded:
                util.log_error(node.lineNr, node.rowNr, "For simplicity, function definitions are currently not allowed inside blocks that may/will be expanded by the compiler.")
                return False

            actual = node.funs[node.funsIndex]


            if self.depth == 0 and actual.name.name in self.typeDict:
                util.log_error(actual.name.lineNr, actual.name.rowNr, "Name collision with named type.")
                return False
            elif self.depth == 0:
                for moduleName, directlyImportedTypesDict in self.directlyImportedTypesDictDict.items():
                    if actual.name.name in directlyImportedTypesDict:
                        util.log_error(actual.name.lineNr, actual.name.rowNr, "Name collision with imported named type.")
                        return False 


            overloadNr = 0   # default
            if actual.name.name in self.funDict:
                overloadNr = len(self.funDict[actual.name.name].funEntries)

            mangledName = name_mangler.mangle_function_name(actual.name.name, self.mangledModuleName, self.isGlobal, self.blockNumberList[0:self.depth], overloadNr)

            # set the mangledName on the actual too, we need it to find our fun in the list later, somewhat hackishly
            actual.mangledName = mangledName

            paramsCopy = []
            for param in actual.params:
                paramsCopy.append(param.create_copy())

            returnTypesCopy = []
            for returnType in actual.returnTypes:
                returnTypesCopy.append(returnType.create_copy())                
            
            signature = FunSignature(actual.isInternal, actual.isInline, actual.name.name, paramsCopy, returnTypesCopy) 
        
            localDict = {}

            if len(self.blockNumberList) <= self.depth:
                for i in range(len(self.blockNumberList), self.depth + 1):
                    self.blockNumberList.append(0)            
            else:
                self.blockNumberList[self.depth] += 1

            funDictEntryNameNr = str(self.blockNumberList[self.depth])
            node.blockNumberStr = funDictEntryNameNr    # set this so that name into blockers can find the block later..
                                                # ... and several other uses for this...        


            if actual.name.name in self.funDict:
                self.funDict[actual.name.name].funEntries.append(FunEntry(mangledName, signature, localDict, node.funsIndex))
            else:
                self.funDict[actual.name.name] = FunListEntry([FunEntry(mangledName, signature, localDict, node.funsIndex)])
            

            self.depth += 1
            prevFunDict = self.funDict
            self.funDict = localDict
            prevIsGlobal = self.isGlobal
            self.isGlobal = False
            prevIsInsideExpanded = self.isInsideExpanded
            self.isInsideExpanded = False
            ###
            for statement in actual.body.statements: 
                # we have to do this explic. (instead of calling visit_children) as we do it somewhat differently from blocks, with regard to the localDict 
                success = self.visit(statement)
                if success == False:
                    return False
            ###
            self.isInsideExpanded = prevIsInsideExpanded
            self.isGlobal = prevIsGlobal
            self.funDict = prevFunDict
            self.depth -= 1
    

            return True

        elif isinstance(node, NBlock):

            if len(self.blockNumberList) <= self.depth:
                for i in range(len(self.blockNumberList), self.depth + 1):
                    self.blockNumberList.append(0)
            else:
                self.blockNumberList[self.depth] += 1

            localDict = {}

            funDictEntryNameNr = str(self.blockNumberList[self.depth])
            node.blockEntryNumStr = funDictEntryNameNr    # set this so that name into blockers can find the block later when specifiying their type just in time...
                                                # ... and several other uses for this...

            self.funDict[funDictEntryNameNr] = BlockEntry(localDict, funDictEntryNameNr)


            self.depth += 1
            prevFunDict = self.funDict
            self.funDict = localDict
            prevIsGlobal = self.isGlobal
            self.isGlobal = False
            # no changing of isInsideExpanded!
            ###
            success = node.visit_children(self)
            if success == False:
                return False
            ###
            self.isGlobal = prevIsGlobal
            self.funDict = prevFunDict
            self.depth -= 1

            return True

        elif isinstance(node, NRefToTemplateDeclarationWithDefinition):

            if self.depth > 0:  # better double-check than check too few times...
                util.log_error(node.lineNr, node.rowNr, "Local template declarations are not allowed.")
                return False

            actual = node.templates[node.templatesIndex]


            if self.depth == 0 and actual.name.name in self.typeDict:
                util.log_error(actual.name.lineNr, actual.name.rowNr, "Name collision with named type.")
                return False
            elif self.depth == 0:
                for moduleName, directlyImportedTypesDict in self.directlyImportedTypesDictDict.items():
                    if actual.name.name in directlyImportedTypesDict:
                        util.log_error(actual.name.lineNr, actual.name.rowNr, "Name collision with imported named type.")
                        return False 


            mangledBasicName = name_mangler.mangle_basic_name(actual.name.name)

            overloadNr = 0   # default
            if actual.name.name in self.funDict:
                overloadNr = len(self.funDict[actual.name.name].funEntries)

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

            
            if actual.name.name in self.funDict:
                self.funDict[actual.name.name].funEntries.append(TemplateEntry(mangledBasicName, templateParams, signature, node.templatesIndex))
            else:
                self.funDict[actual.name.name] = FunListEntry([TemplateEntry(mangledBasicName, templateParams, signature, node.templatesIndex)])



            return True

        elif isinstance(node, NContenttypeStatement):

            # for a certain silly reason, we have to do this explicitly/manually here

            success = self.visit(node.switchValue)
            if success == False:
                return False

            for case in node.cases:
                # no need to visit the caseTypes themselves as no fun defs in them...

                if len(case.caseTypes) > 1:
                    prevIsInsideExpanded = self.isInsideExpanded
                    self.isInsideExpanded = True
                    ###
                    success = self.visit(case.block)
                    if success == False:                
                        return False
                    ###
                    self.isInsideExpanded = prevIsInsideExpanded
                else:
                    success = self.visit(case.block)
                    if success == False:
                        return False


            if not node.defaultCaseOrNull is None:
                prevIsInsideExpanded = self.isInsideExpanded
                self.isInsideExpanded = True
                ###
                success = self.visit(node.defaultCaseOrNull)
                if success == False:
                    return False
                ###
                self.isInsideExpanded = prevIsInsideExpanded

            return True

        elif (isinstance(node, NIfStatement) or isinstance(node, NLoopStatement) or
            isinstance(node, NForStatement) or isinstance(node, NSwitchStatement) or
            isinstance(node, NSwitchNormalCase) or isinstance(node, NContenttypeNormalCase) or
            isinstance(node, NProgram)  # don't forget this one!  
        ):

             # (these are the statement with blocks in them, that may contain further fun definitions) 

            return node.visit_children(self)

        else:
            return True









            

        



