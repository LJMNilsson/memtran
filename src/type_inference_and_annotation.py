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
from fun_dict_stuff import *
from type_identity import *



################### INTERNAL TYPES FOR TYPE INFERENCE AID ###################


class NAlternativePossibilitiesType(NType):

    # Arraylist<NType> alternativesList;
    
    def __init__(self, lineNr, rowNr, alternativesList):
        self.lineNr = lineNr
        self.rowNr = rowNr
        self.alternativesList = alternativesList


    def print_it(self):
        for alt in self.alternativesList:
            print("ALT: ", end='')
            alt.print_it()

    def get_line_nr(self):
        return self.lineNr

    def get_row_nr(self):
        return self.rowNr

    def create_copy(self):
        altListCopy = []
        for alt in self.alternativesList:
            altListCopy.append(alt.create_copy())

        return NAlternativePossibilitiesType(self.lineNr, self.rowNr, altListCopy)        

    def accept_visitor(self, visitor):
        for alt in self.alternativesList:
            success = alt.accept_visitor(visitor)
            if success == False:
                return False

        return visitor.visit(self)




class NUnknownType(NType):

    def __init__(self, lineNr, rowNr):
        self.lineNr = lineNr
        self.rowNr = rowNr

    def print_it(self):
        print("UNKNOWN_TYPE", end='')

    def get_line_nr(self):
        return self.lineNr

    def get_row_nr(self):
        return self.rowNr

    def create_copy(self):
        return NUnknownType(self.lineNr, self.rowNr)
    
    def accept_visitor(self, visitor):
        return False     # You should not visit these kinds of types actually




class NUnspecializedTemplateType(NType):

    # long lineNr;
    # long rowNr;
    # ArrayList<NIdentifier> params;
    # ArrayList<NTypeArg> typeArgs;
    # ArrayList<NType> returnTypes;

    pass

    # TODO (if needed)        


class NInsertVariantBoxingHere(NType):  # we probably won't need this type

    # NType constituentType

    def __init__(self, lineNr, rowNr, superType, constituentType):
        self.lineNr = lineNr
        self.rowNr = rowNr
        self.superType = superType
        self.constituentType = constituentType

    def print_it(self):
        print("VARIANT_BOX_ME/", end='')
        self.constituentType.print_it()
        print("\\ as ", end='')
        self.superType.print_it()

    def get_line_nr(self):
        return self.lineNr

    def get_row_nr(self):
        return self.rowNr

    def create_copy(self):
        return NInsertVariantBoxingHere(self.lineNr, self.rowNr, self.superType.create_copy(), self.constituentType.create_copy())

    def accept_visitor(self, visitor):
        return False     # You should not visit these kinds of types actually



############################## HELPER STUFF FOR TYPE CHECKING / INFERENCE ###########################

integerChoices = [NISizeType(0, 0), NU8Type(0, 0)]  # Add more choices later...

floatingChoices = [NF64Type(0, 0), NF32Type(0, 0)]


#####################################################################################################


# returns a tuple (inferredType, transformedExpression) . inferredType == False means the inferring failed

# Also annotates the newExpression with "inferredType" field

# Also annotates identifier expressions with "mangledName" field

# Also annotates (certain, currently) identifier expressions with "identifierType" field (which, in case of indexings may not be the same as 'inferredType')

def type_infer_and_annotate_expression(
    expr, inferredTypeFromBelow, 
    typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict, 
    funDictStack, builtInFunsDict, directlyImportedFunsDictDict, otherImportedModulesFunDictDict,
    beSilentFlag
):
    
    if isinstance(expr, NIdentifierExpression):  

        foundDefinitions = []      # actually, we have to gather all the definitions from all the three levels of dicts. For funlists.

        if expr.moduleNameOrNull is None:
            for funDict in reversed(funDictStack):
                if expr.name.name in funDict:
                    foundDefinitions.append(funDict[expr.name.name])

            for moduleName, directlyImportedFunsDict in directlyImportedFunsDictDict.items():
                if expr.name.name in directlyImportedFunsDict:
                    entry = directlyImportedFunsDict[expr.name.name]

                    if isinstance(entry, FunListEntry):
                        prunedList = []
                
                        for someFunOrTemplate in entry.funEntries:
                            if not someFunOrTemplate.signature.isInternal:
                                prunedList.append(someFunOrTemplate)

                        foundDefinitions.append(FunListEntry(prunedList))

                    elif isinstance(entry, VarEntry):
                        if not entry.isInternal:
                            foundDefinitions.append(entry)
    
                    else:
                        util.log_error(expr.lineNr, expr.rowNr, "Undetermined definition of identifier expression during type check. SHOULD NOT HAPPEN")
                        return (False, None)

            if expr.name.name in builtInFunsDict:
                foundDefinitions.append(builtInFunsDict[expr.name.name])

        else:
            if expr.moduleNameOrNull in otherImportedModulesFunDictDict:

                moduleDict = otherImportedModulesFunDictDict[expr.moduleNameOrNull]

                if expr.name.name in moduleDict:
                    entry = moduleDict[expr.name.name]

                    if isinstance(entry, FunListEntry): 
                        prunedList = []

                        for someFunOrTemplate in entry.funEntries:
                            if not someFunOrTemplate.signature.isInternal:
                                prunedList.append(someFunOrTemplate)

                        foundDefinitions.append(FunListEntry(prunedList))    

                    elif isinstance(entry, VarEntry):
                        if not entry.isInternal:
                            foundDefinitions.append(entry) 

                    else:
                        util.log_error(expr.lineNr, expr.rowNr, "Undetermined definition of module specified identifier expression during type check. SHOULD NOT HAPPEN")
                        return (False, None)           

            else:
                if not beSilentFlag:
                    util.log_error(expr.lineNr, expr.rowNr, "Reference to module that has not been imported.")
                return (False, None)
                 
    
        if len(foundDefinitions) == 0:
            if not beSilentFlag:
                util.log_error(expr.lineNr, expr.rowNr, "Usage of name that has not been declared.")
            return (False, None)

        if isinstance(foundDefinitions[0], FunListEntry):

            # We can assume that we are not coming from/as a function call name,
            # since the function call case does not recurse on its function name expression.

            # Assume that all definitions are fun list entries... I think it will work?

            myAlternativeList = []        # should contain tuples (typeAlternative, mangledName), or template entries...

            for foundFunList in foundDefinitions:
                for entry in foundFunList.funEntries:
        
                    if isinstance(entry, FunEntry):

                        typeArgs = []

                        for param in entry.signature.params:
                            if isinstance(param, NNormalParam):

                                typeArgs.append(NNormalTypeArg(param.lineNr, param.rowNr, param.isMut, param.isConstruand, param.argType.create_copy()))

                            else: # NRefParam hopefully...

                                typeArgs.append(NRefTypeArg(param.lineNr, parm.rowNr, param.argType.create_copy()))

                        returnTypes = []
                        for returnType in entry.signature.returnTypes:
                            returnTypes.append(returnType.create_copy())

                        myAlternativeList.append(
                            (NFunctionType(expr.lineNr, expr.rowNr, typeArgs, returnTypes), entry.mangledName)
                        )

                    elif isinstance(entry, SpecializedTemplateEntry):

                        typeArgs = []

                        for param in entry.signature.params:
                            if isinstance(param, NNormalParam):

                                typeArgs.append(NNormalTypeArg(param.lineNr, param.rowNr, param.isMut, param.isConstruand, param.argType.create_copy()))

                            else: # NRefParam hopefully...

                                typeArgs.append(NRefTypeArg(param.lineNr, parm.rowNr, param.argType.create_copy()))

                        returnTypes = []
                        for returnType in entry.signature.returnTypes:
                            returnTypes.append(returnType.create_copy())

                        myAlternativeList.append(
                            (NFunctionType(expr.lineNr, expr.rowNr, typeArgs, returnTypes), entry.mangledName)
                            # hope we don't need anything specifying it as a tspec rather than an ordinary fun entry...
                        )

                    elif isinstance(entry, TemplateEntry):

                        # How do we add this to the alternatives list without specialising it yet?

                        myAlternativeList.append(
                            entry      # we make use of Python's dynamic nature here and simply add the SpecializedTemplateEntry... let's see how this works out...
                        ) 

                    else:
                        util.log_error(expr.lineNr, expr.rowNr, "Type checking found FunList entry that is wrong kind, prolly template spec. SHOULD NOT HAPPEN")
                        return (False, None)

            
            if len(expr.indexings) > 0:
                util.log_error(expr.lineNr, expr.rowNr, "Trying to index a function type value somehow (no indexings are possible on such values).")
                return (False, None)


            matchResults = []

            for tupleOrTemplateEntry in myAlternativesList:
    
                if isinstance(tupleOrTemplateEntry, TemplateEntry):
                    matchResults.append(None)   # this stands for unresolved...                    
                else:
                    alt, mangleName = tupleOrTemplateEntry
    
                    matchResult = extended_match_as_below(
                        inferredTypeFromBelow,
                        alt,
                        typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict, 
                    )

                    matchResults.append(matchResult)

        
            nonFalseCount = 0
            for matchResult in matchResults:
                if matchResult != False:
                    nonFalseCount += 1


            if nonFalseCount == 0:
                if not beSilentFlag:
                    util.log_error(expr.lineNr, expr.rowNr, "Could not infer any suitable type for this identifier expression.")
                return (False, None)            
            
            elif nonFalseCount == 1:
                # We prefer already specialized tspecs to trying specializing anew here:

                theFoundIndex = -1
                for i in range(0, len(matchResults)):
                    if matchResults[i] != False:
                        theFoundIndex = i
                        break

                if matchResults[theFoundIndex] == None:
                
                    if not beSilentFlag:
                        util.log_error(expr.lineNr, expr.rowNr, "Please type specify the template specialization which here is referred to as a function type value.")
                    return (False, None)

                elif matchResults[theFoundIndex] == "several":
    
                    if not beSilentFlag:
                        util.log_error(expr.lineNr, expr.rowNr, "Several type cases can be selected with implicit variant-boxing. Please type specify.")
                    return (False, None)

                elif matchResults[theFoundIndex] == "vbox":

                    alt, mangleName = myAlternativesList[i]

                    if not beSilentFlag:
                        # annotation
                        expr.inferredType = alt
                        expr.mangledName = mangleName

                    vbox = NVariantBoxExpression(expr.lineNr, expr.rowNr, expr)

                    if not beSilentFlag:
                        # annotate
                        vbox.inferredType = inferredTypeFromBelow.create_copy()

                    return (inferredTypeFromBelow.create_copy(), vbox)

                else:  # Then it should be True hopefully...

                    alt, mangleName = myAlternativesList[i]

                    if not beSilentFlag:
                        # annotating...
                        expr.inferredType = alt
                        expr.mangledName = mangleName
        
                    return (alt.create_copy(), expr)    

            else: # > 1

                if not beSilentFlag:
                    util.log_error(expr.lineNr, expr.rowNr, "Please type specify the function which here is referred to as a function type value.") 
                return (False, None)
                # Should ideally print the alternatives too, but not for now...

        elif isinstance(foundDefinitions[0], VarEntry):

            # Assume there is only one def in the definitions list, which should be the case hopefully...

            if not beSilentFlag:
                expr.identifierType = foundDefinitions[0].theType.create_copy() 

            accumulatedType = foundDefinitions[0].theType

            for indexing in expr.indexings:

                if isinstance(indexing, NArrayIndexingIndex):

                    indexTypeResult, indexExprResult = type_infer_and_annotate_expression(
                        indexing.indexExpression, NISizeType(indexing.lineNr, indexing.rowNr),
                        typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict, 
                        funDictStack, builtInFunsDict, directlyImportedFunsDictDict, otherImportedModulesFunDictDict,
                        beSilentFlag
                    ) 
                    if indexTypeResult == False:
                        return (False, None)

                    if isinstance(accumulatedType, NDynamicArrayType):

                        if not beSilentFlag:
                            indexing.inferredType = accumulatedType.valueType.create_copy()

                        accumulatedType = indexing.inferredType

                    else:
                        # It may still match, just not concretely...

                        depthCounter = 0

                        while True:
                            if depthCounter > 20:
                                if not beSilentFlag:
                                    util.log_error(indexing.lineNr, indexing.rowNr, "Failed to concretize type (at depth 20).")
                                return (False, None)

                            if isinstance(accumulatedType, NIdentifierType):

                                accumulatedType = accumulatedType.get_definition(typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict)
                                depthCounter += 1

                            elif isinstance(accumulatedType, NParametrizedIdentifierType):

                                accumulatedType = create_substitution(accumulatedType, typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict)
                                depthCounter += 1

                            elif isinstance(accumulatedType, NDynamicArrayType):
                                break
                            else:
                                if not beSilentFlag:
                                    util.log_error(indexing.lineNr, indexing.rowNr, "Trying to array index something that isn't of array type.")
                                return (False, None)

                        # Now we can assume it's a NDynamicArrayType...:
                      
                        if not beSilentFlag:
                            indexing.inferredType = accumulatedType.valueType.create_copy()

                        accumulatedType = indexing.inferredType


                elif isinstance(indexing, NStructIndexingIndex):

                    if isinstance(accumulatedType, NStructType):

                        foundMemberType = None

                        for member in accumulatedType.members:
                            if member.name.name == indexing.indexName.name:
                                foundMemberType = member.theType.create_copy()
                                break
                        
                        if foundMemberType is None:
                            util.log_error(indexing.lineNr, indexing.rowNr, "Struct indexing a non-existing struct field.")
                            return (False, None)

                        if not beSilentFlag:
                            indexing.inferredType = foundMemberType.create_copy()

                        accumulatedType = foundMemberType.create_copy()

                    else:
                        if not beSilentFlag:
                            util.log_error(indexing.lineNr, indexing.rowNr, "Trying to struct index something that isn't of struct type.")
                        return (False, None)

                elif isinstance(indexing, NVariantBoxCastIndex):

                    if isinstance(accumulatedType, NVariantBoxType):

                        foundTypeCase = None

                        for typeCase in accumulatedType.types:
                            
                            matchResult = match_as_below(    # we better not do extended match here!!!
                                typeCase, 
                                indexing.theType,
                                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                                0
                            )
                            if matchResult:
                                if not foundTypeCase is None:
                                    if not beSilentFlag:
                                        util.log_error(indexing.lineNr, indexing.rowNr, "Here, strangely, down-conversion matches several type cases of the variant-box value...")
                                    return (False, None)                                    

                                else:
                                    foundTypeCase = typeCase.create_copy()

                        if not beSilentFlag:
                            indexing.inferredType = foundTypeCase
                        
                        accumulatedType = foundTypeCase.create_copy()

                    else:
                        if not beSilentFlag:
                            util.log_error(indexing.lineNr, indexing.rowNr, "Trying to variant-box down-convert non variant-box value.")
                        return (False, None)

                elif isinstance(indexing, NTypeClarificationIndex):

                    matchResult = match_as_below(    # should this be extended -- no!
                        accumulatedType, 
                        indexing.theType,
                        typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                        0
                    )
                    if matchResult:

                        if not beSilentFlag:
                            indexing.inferredType = indexing.theType.create_copy()

                        accumulatedType = indexing.theType.create_copy()

                    else:
                        if not beSilentFlag: 
                            util.log_error(indexing.lineNr, indexing.rowNr, "Type mismatch with type clarification...")
                        return (False, None)

                else:
                    util.log_error(indexing.lineNr, indexing.rowNr, "Type checking found unknown kind of indexing.")
                    return (False, None)


            matchResult = extended_match_as_below(
                inferredTypeFromBelow,
                accumulatedType,
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict, 
            ) 

            if matchResult == "several":
    
                if not beSilentFlag:
                    util.log_error(expr.lineNr, expr.rowNr, "Several type cases can be selected with implicit variant-boxing. Please type specify.")
                return (False, None)

            elif matchResult == "vbox":

                if not beSilentFlag:
                    # annotation
                    expr.inferredType = foundDefinitions[0].theType.create_copy()
                    expr.mangledName = foundDefinitions[0].mangledName

                vbox = NVariantBoxExpression(expr.lineNr, expr.rowNr, expr)

                if not beSilentFlag:
                    # annotate
                    vbox.inferredType = inferredTypeFromBelow.create_copy()

                return (inferredTypeFromBelow.create_copy(), vbox)

            elif matchResult:

                if not beSilentFlag:
                    expr.inferredType = foundDefinitions[0].theType.create_copy()
                    expr.mangledName = foundDefinitions[0].mangledName

                return (foundDefinitions[0].theType.create_copy(), expr)
                
            else:
                if not beSilentFlag:
                    util.log_error(expr.lineNr, expr.rowNr, "Type mismatch.")
                    print("Expected: ", end='')
                    inferredTypeFromBelow.print_it()
                    print("")  # newline
                    print("Found: ", end='')
                    foundDefinitions[0].theType.print_it()
                    print("") # newline

                return (False, None)

        elif isinstance(foundDefinitions[0], BlockEntry):

            if not beSilentFlag:
                util.log_error(expr.lineNr, expr.rowNr, "Identifier matched with block entry during type check. SHOULD NOT HAPPEN.")
            return (False, None)

        elif isinstance(foundDefinitions[0], ParamEntry):

            if not beSilentFlag:
                expr.identifierType = foundDefinitions[0].definitionParam.theType.create_copy() 

            accumulatedType = foundDefinitions[0].definitionParam.theType

            for indexing in expr.indexings:

                if isinstance(indexing, NArrayIndexingIndex):

                    if isinstance(accumulatedType, NDynamicArrayType):

                        indexTypeResult, indexExprResult = type_infer_and_annotate_expression(
                            indexing.indexExpression, accumulatedType.valueType,
                            typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict, 
                            funDictStack, builtInFunsDict, directlyImportedFunsDictDict, otherImportedModulesFunDictDict,
                            beSilentFlag
                        ) 
                        if indexTypeResult == False:
                            return (False, None)

                        if not beSilentFlag:
                            indexing.inferredType = indexTypeResult.create_copy()

                        accumulatedType = indexTypeResult

                    else:
                        if not beSilentFlag:
                            util.log_error(indexing.lineNr, indexing.rowNr, "Trying to array index something that isn't of array type.")
                        return (False, None)

                elif isinstance(indexing, NStructIndexingIndex):

                    if isinstance(accumulatedType, NStructType):

                        foundMemberType = None

                        for member in accumulatedType.members:
                            if member.name.name == indexing.indexName.name:
                                foundMemberType = member.theType.create_copy()
                                break
                        
                        if foundMemberType is None:
                            util.log_error(indexing.lineNr, indexing.rowNr, "Struct indexing a non-existing struct field.")
                            return (False, None)

                        if not beSilentFlag:
                            indexing.inferredType = foundMemberType.create_copy()

                        accumulatedType = foundMemberType.create_copy()

                    else:
                        if not beSilentFlag:
                            util.log_error(indexing.lineNr, indexing.rowNr, "Trying to struct index something that isn't of struct type.")
                        return (False, None)

                elif isinstance(indexing, NVariantBoxCastIndex):

                    if isinstance(accumulatedType, NVariantBoxType):

                        foundTypeCase = None

                        for typeCase in accumulatedType.types:
                            
                            matchResult = match_as_below(    # we better not do extended match here!!!
                                typeCase, 
                                indexing.theType,
                                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                                0
                            )
                            if matchResult:
                                if not foundTypeCase is None:
                                    if not beSilentFlag:
                                        util.log_error(indexing.lineNr, indexing.rowNr, "Here, strangely, down-conversion matches several type cases of the variant-box value...")
                                    return (False, None)                                    

                                else:
                                    foundTypeCase = typeCase.create_copy()

                        if not beSilentFlag:
                            indexing.inferredType = foundTypeCase
                        
                        accumulatedType = foundTypeCase.create_copy()

                    else:
                        if not beSilentFlag:
                            util.log_error(indexing.lineNr, indexing.rowNr, "Trying to variant-box down-convert non variant-box value.")
                        return (False, None)

                elif isinstance(indexing, NTypeClarificationIndex):

                    matchResult = match_as_below(    # should this be extended -- no!
                        accumulatedType, 
                        indexing.theType,
                        typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                        0
                    )
                    if matchResult:

                        if not beSilentFlag:
                            indexing.inferredType = indexing.theType.create_copy()

                        accumulatedType = indexing.theType.create_copy()

                    else:
                        if not beSilentFlag: 
                            util.log_error(indexing.lineNr, indexing.rowNr, "Type mismatch with type clarification...")
                        return (False, None)

                else:
                    util.log_error(indexing.lineNr, indexing.rowNr, "Type checking found unknown kind of indexing.")
                    return (False, None)


            matchResult = extended_match_as_below(
                inferredTypeFromBelow,
                accumulatedType,
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict, 
            ) 

            if matchResult == "several":
    
                if not beSilentFlag:
                    util.log_error(expr.lineNr, expr.rowNr, "Several type cases can be selected with implicit variant-boxing. Please type specify.")
                return (False, None)

            elif matchResult == "vbox":

                if not beSilentFlag:
                    # annotation
                    expr.inferredType = accumulatedType.create_copy()
                    expr.mangledName = foundDefinitions[0].mangledName 

                vbox = NVariantBoxExpression(expr.lineNr, expr.rowNr, expr)

                if not beSilentFlag:
                    # annotate
                    vbox.inferredType = inferredTypeFromBelow.create_copy()

                return (inferredTypeFromBelow.create_copy(), vbox)

            elif matchResult:

                if not beSilentFlag:
                    expr.inferredType = accumulatedType.create_copy()
                    expr.mangledName = foundDefinitions[0].mangledName

                return (accumulatedType.create_copy(), expr)
                
            else:
                if not beSilentFlag:
                    util.log_error(expr.lineNr, expr.rowNr, "Type mismatch.")
                    print("Expected: ", end='')
                    inferredTypeFromBelow.print_it()
                    print("")  # newline
                    print("Found: ", end='')
                    foundType.print_it()
                    print("") # newline

                return (False, None)

        elif isinstance(foundDefinitions[0], NameIntoBlockEntry): 

            # The name into block entry should have a real type at this point, we presume or hope...

            if not beSilentFlag:
                expr.identifierType = foundDefinitions[0].theType.create_copy() 

            accumulatedType = foundDefinitions[0].theType

            for indexing in expr.indexings:

                if isinstance(indexing, NArrayIndexingIndex):

                    if isinstance(accumulatedType, NDynamicArrayType):

                        indexTypeResult, indexExprResult = type_infer_and_annotate_expression(
                            indexing.indexExpression, accumulatedType.valueType,
                            typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict, 
                            funDictStack, builtInFunsDict, directlyImportedFunsDictDict, otherImportedModulesFunDictDict,
                            beSilentFlag
                        ) 
                        if indexTypeResult == False:
                            return (False, None)

                        if not beSilentFlag:
                            indexing.inferredType = indexTypeResult.create_copy()

                        accumulatedType = indexTypeResult

                    else:
                        if not beSilentFlag:
                            util.log_error(indexing.lineNr, indexing.rowNr, "Trying to array index something that isn't of array type.")
                        return (False, None)

                elif isinstance(indexing, NStructIndexingIndex):

                    if isinstance(accumulatedType, NStructType):

                        foundMemberType = None

                        for member in accumulatedType.members:
                            if member.name.name == indexing.indexName.name:
                                foundMemberType = member.theType.create_copy()
                                break
                        
                        if foundMemberType is None:
                            util.log_error(indexing.lineNr, indexing.rowNr, "Struct indexing a non-existing struct field.")
                            return (False, None)

                        if not beSilentFlag:
                            indexing.inferredType = foundMemberType.create_copy()

                        accumulatedType = foundMemberType.create_copy()

                    else:
                        if not beSilentFlag:
                            util.log_error(indexing.lineNr, indexing.rowNr, "Trying to struct index something that isn't of struct type.")
                        return (False, None)

                elif isinstance(indexing, NVariantBoxCastIndex):

                    if isinstance(accumulatedType, NVariantBoxType):

                        foundTypeCase = None

                        for typeCase in accumulatedType.types:
                            
                            matchResult = match_as_below(    # we better not do extended match here!!!
                                typeCase, 
                                indexing.theType,
                                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                                0
                            )
                            if matchResult:
                                if not foundTypeCase is None:
                                    if not beSilentFlag:
                                        util.log_error(indexing.lineNr, indexing.rowNr, "Here, strangely, down-conversion matches several type cases of the variant-box value...")
                                    return (False, None)                                    

                                else:
                                    foundTypeCase = typeCase.create_copy()

                        if not beSilentFlag:
                            indexing.inferredType = foundTypeCase
                        
                        accumulatedType = foundTypeCase.create_copy()

                    else:
                        if not beSilentFlag:
                            util.log_error(indexing.lineNr, indexing.rowNr, "Trying to variant-box down-convert non variant-box value.")
                        return (False, None)

                elif isinstance(indexing, NTypeClarificationIndex):

                    matchResult = match_as_below(    # should this be extended -- no!
                        accumulatedType, 
                        indexing.theType,
                        typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                        0
                    )
                    if matchResult:

                        if not beSilentFlag:
                            indexing.inferredType = indexing.theType.create_copy()

                        accumulatedType = indexing.theType.create_copy()

                    else:
                        if not beSilentFlag: 
                            util.log_error(indexing.lineNr, indexing.rowNr, "Type mismatch with type clarification...")
                        return (False, None)

                else:
                    util.log_error(indexing.lineNr, indexing.rowNr, "Type checking found unknown kind of indexing.")
                    return (False, None)


            matchResult = extended_match_as_below(
                inferredTypeFromBelow,
                accumulatedType,
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict, 
            ) 

            if matchResult == "several":
    
                if not beSilentFlag:
                    util.log_error(expr.lineNr, expr.rowNr, "Several type cases can be selected with implicit variant-boxing. Please type specify.")
                return (False, None)

            elif matchResult == "vbox":

                if not beSilentFlag:
                    # annotation
                    expr.inferredType = accumulatedType.create_copy()
                    # NOTA BENE -- we don't set a mangled name for these -- expect code generation to handle the names into block... 

                vbox = NVariantBoxExpression(expr.lineNr, expr.rowNr, expr)

                if not beSilentFlag:
                    # annotate
                    vbox.inferredType = inferredTypeFromBelow.create_copy()

                return (inferredTypeFromBelow.create_copy(), vbox)

            elif matchResult:

                if not beSilentFlag:
                    expr.inferredType = accumulatedType.create_copy()

                return (accumulatedType.create_copy(), expr)
                
            else:
                if not beSilentFlag:
                    util.log_error(expr.lineNr, expr.rowNr, "Type mismatch.")
                    print("Expected: ", end='')
                    inferredTypeFromBelow.print_it()
                    print("")  # newline
                    print("Found: ", end='')
                    foundType.print_it()
                    print("") # newline

                return (False, None)

        else:
            util.log_error(expr.lineNr, expr.rowNr, "Unknown entry found for identifier during type check. SHOULD NOT HAPPEN.")
            return (False, None)


    elif isinstance(expr, NNilExpression):

        foundType = NNilType(expr.lineNr, expr.rowNr)

        matchResult = extended_match_as_below(
            inferredTypeFromBelow,
            foundType,
            typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict, 
        ) 

        if matchResult == "several":
    
            if not beSilentFlag:
                util.log_error(expr.lineNr, expr.rowNr, "Several type cases can be selected with implicit variant-boxing. Please type specify.")
            return (False, None)

        elif matchResult == "vbox":

            if not beSilentFlag:
                # annotation
                expr.inferredType = foundType.create_copy() 

            vbox = NVariantBoxExpression(expr.lineNr, expr.rowNr, expr)

            if not beSilentFlag:
                # annotate
                vbox.inferredType = inferredTypeFromBelow.create_copy()

            return (inferredTypeFromBelow.create_copy(), vbox)

        elif matchResult:
            
            if not beSilentFlag:
                expr.inferredType = foundType

            return (foundType.create_copy(), expr)
            
        else:
            if not beSilentFlag:
                util.log_error(expr.lineNr, expr.rowNr, "Type mismatch.")
                print("Expected: ", end='')
                inferredTypeFromBelow.print_it()
                print("")  # newline
                print("Found: ", end='')
                foundType.print_it()
                print("") # newline

            return (False, None)        

    elif isinstance(expr, NTrueExpression) or isinstance(expr, NFalseExpression):

        foundType = NBoolType(expr.lineNr, expr.rowNr)

        matchResult = extended_match_as_below(
            inferredTypeFromBelow,
            foundType,
            typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict, 
        ) 

        if matchResult == "several":
    
            if not beSilentFlag:
                util.log_error(expr.lineNr, expr.rowNr, "Several type cases can be selected with implicit variant-boxing. Please type specify.")
            return (False, None)

        elif matchResult == "vbox":

            if not beSilentFlag:
                # annotation
                expr.inferredType = foundType.create_copy() 

            vbox = NVariantBoxExpression(expr.lineNr, expr.rowNr, expr)

            if not beSilentFlag:
                # annotate
                vbox.inferredType = inferredTypeFromBelow.create_copy()

            return (inferredTypeFromBelow.create_copy(), vbox)

        elif matchResult:

            if not beSilentFlag:
                expr.inferredType = foundType

            return (foundType.create_copy(), expr)
            
        else:
            if not beSilentFlag:
                util.log_error(expr.lineNr, expr.rowNr, "Type mismatch.")
                print("Expected: ", end='')
                inferredTypeFromBelow.print_it()
                print("")  # newline
                print("Found: ", end='')
                foundType.print_it()
                print("") # newline

            return (False, None)   

    elif isinstance(expr, NIntegerExpression):

        for foundType in integerChoices:

            matchResult = extended_match_as_below(
                inferredTypeFromBelow,
                foundType,
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict, 
            ) 

            if matchResult == "several":
        
                continue       # This case should be very rare or non-existent actually

            elif matchResult == "vbox":

                if not beSilentFlag:
                    # annotation
                    expr.inferredType = foundType.create_copy() 

                vbox = NVariantBoxExpression(expr.lineNr, expr.rowNr, expr)

                if not beSilentFlag:
                    # annotate
                    vbox.inferredType = inferredTypeFromBelow.create_copy()

                return (inferredTypeFromBelow.create_copy(), vbox)

            elif matchResult:

                if not beSilentFlag:
                    expr.inferredType = foundType.create_copy()

                return (foundType.create_copy(), expr)

                
        # (if we are still here, continue below)

        if not beSilentFlag:
            util.log_error(expr.lineNr, expr.rowNr, "Found no implemented functioning type alternative for this integer literal.")
            print("Expected: ", end='')
            inferredTypeFromBelow.print_it()
            print("")  # newline

        return (False, None)                

    elif isinstance(expr, NFloatingPointNumberExpression):

        for foundType in floatingChoices:
 
            matchResult = extended_match_as_below(
                inferredTypeFromBelow,
                foundType,
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict, 
            ) 

            if matchResult == "several":
        
                continue       # This case should be very rare or non-existent actually

            elif matchResult == "vbox":

                if not beSilentFlag:
                    # annotation
                    expr.inferredType = foundType.create_copy() 

                vbox = NVariantBoxExpression(expr.lineNr, expr.rowNr, expr)

                if not beSilentFlag:
                    # annotate
                    vbox.inferredType = inferredTypeFromBelow.create_copy()

                return (inferredTypeFromBelow.create_copy(), vbox)

            elif matchResult:

                if not beSilentFlag:
                    expr.inferredType = foundType.create_copy()

                return (foundType.create_copy(), expr)

                
        # (if we are still here, continue below)

        if not beSilentFlag:
            util.log_error(expr.lineNr, expr.rowNr, "Found no implmented functioning type alternative for this floating point number literal.")
            print("Expected: ", end='')
            inferredTypeFromBelow.print_it()
            print("")  # newline
    
        return (False, None)                   

    elif isinstance(expr, NStringExpression):

        foundType = NDynamicArrayType(expr.lineNr, expr.rowNr, NU8Type(expr.lineNr, expr.rowNr))

        matchResult = extended_match_as_below(
            inferredTypeFromBelow,
            foundType,
            typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict, 
        ) 

        if matchResult == "several":
    
            if not beSilentFlag:
                util.log_error(expr.lineNr, expr.rowNr, "Several type cases can be selected with implicit variant-boxing. Please type specify.")
            return (False, None)

        elif matchResult == "vbox":

            if not beSilentFlag:
                # annotation
                expr.inferredType = foundType.create_copy() 

            vbox = NVariantBoxExpression(expr.lineNr, expr.rowNr, expr)

            if not beSilentFlag:
                # annotate
                vbox.inferredType = inferredTypeFromBelow.create_copy()

            return (inferredTypeFromBelow.create_copy(), vbox)

        elif matchResult:

            if not beSilentFlag:
                expr.inferredType = foundType

            return (foundType.create_copy(), expr)
            
        else:
            if not beSilentFlag:
                util.log_error(expr.lineNr, expr.rowNr, "Type mismatch.")
                print("Expected: ", end='')
                inferredTypeFromBelow.print_it()
                print("")  # newline
                print("Found: ", end='')
                foundType.print_it()
                print("") # newline

            return (False, None) 

    elif isinstance(expr, NArrayExpressionIndividualValues):

        if isinstance(inferredTypeFromBelow, NUnknownType):
    
            if len(expr.values) == 0:

                if not beSilentFlag:
                    util.log_error(expr.lineNr, expr.rowNr, "Unable to infer exact type of empty array expression. Please type specify.")
                return (False, None)

            else:

                firstType = None

                newValues = []

                for value in expr.values:

                    typeResult, exprResult = type_infer_and_annotate_expression(
                        value, NUnknownType(value.lineNr, value.rowNr), 
                        typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict, 
                        funDictStack, builtInFunsDict, directlyImportedFunsDictDict, otherImportedModulesFunDictDict,
                        beSilentFlag
                    )

                    if typeResult == False:
                        return (False, None)

                    if firstType is None:
                        firstType = typeResult
                    else:
                        
                        # how do we match correctly here -- trying extended_match_as_below simply, hope it is enough...

                        matchResult = extended_match_as_below(
                            firstType,
                            typeResult,
                            typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict 
                        ) 

                        if matchResult != True:
                            if not beSilentFlag:
                                util.log_error(expr.lineNr, expr.rowNr, "Array of disparate types. (Or alternatively, the compiler may be unsufficiently smart here.)")
                            return (False, None)  

                    newValues.append(exprResult)
                
                if not beSilentFlag:
                    expr.values = newValues
                    expr.inferredType = NDynamicArrayType(expr.lineNr, expr.rowNr, firstType.create_copy())
                
                return (expr.inferredType.create_copy(), expr)


        elif isinstance(inferredTypeFromBelow, NDynamicArrayType):

            expectedValueType = inferredTypeFromBelow.valueType

            newValues = []

            for value in expr.values:
    
                typeResult, exprResult = type_infer_and_annotate_expression(
                    value, expectedValueType, 
                    typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict, 
                    funDictStack, builtInFunsDict, directlyImportedFunsDictDict, otherImportedModulesFunDictDict,
                    beSilentFlag
                )

                if typeResult == False:
                    return (False, None)

                matchResult = extended_match_as_below(
                    expectedValueType,
                    typeResult,
                    typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict
                )     

                if matchResult == "several":
            
                    if not beSilentFlag:
                        util.log_error(value.lineNr, value.rowNr, "Several type cases can be selected with implicit variant-boxing. Please type specify.")
                    return (False, None)

                elif matchResult == "vbox":

                    vbox = NVariantBoxExpression(value.lineNr, value.rowNr, value)

                    if not beSilentFlag:
                        # annotate
                        vbox.inferredType = expectedValueType.create_copy()

                    newValues.append(vbox)

                elif matchResult:

                    newValues.append(value)
                    
                else:
                    if not beSilentFlag:
                        util.log_error(expr.lineNr, expr.rowNr, "Type mismatch.")
                        print("Expected: ", end='')
                        expectedValueType.print_it()
                        print("")  # newline
                        print("Found: ", end='')
                        typeResult.print_it()
                        print("") # newline

                    return (False, None) 


            if not beSilentFlag:
                expr.values = newValues              
                expr.inferredType = inferredTypeFromBelow.create_copy()
                
            return (inferredTypeFromBelow.create_copy(), expr)

        else:
            # It may match a NVariantBoxType, or match an identifier type or parametrized identifier type resolving into a NVariantBoxType

            if len(expr.values) == 0:

                if not beSilentFlag:
                    util.log_error(expr.lineNr, expr.rowNr, "Current simple type inferrer unable to infer exact type of empty array expression. Please type specify.")
                return (False, None)

            else:

                firstType = None

                newValues = []

                for value in expr.values:

                    typeResult, exprResult = type_infer_and_annotate_expression(
                        value, NUnknownType(value.lineNr, value.rowNr), 
                        typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict, 
                        funDictStack, builtInFunsDict, directlyImportedFunsDictDict, otherImportedModulesFunDictDict,
                        beSilentFlag
                    )

                    if typeResult == False:
                        return (False, None)

                    if firstType is None:
                        firstType = typeResult
                    else:
                        
                        # how do we match correctly here -- trying extended_match_as_below simply, hope it is enough...

                        matchResult = extended_match_as_below(
                            firstType,
                            typeResult,
                            typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict
                        ) 

                        if matchResult != True:
                            if not beSilentFlag:
                                util.log_error(expr.lineNr, expr.rowNr, "Array of disparate types. (Or alternatively, the compiler may be unsufficiently smart here.)")
                            return (False, None)  

                    newValues.append(exprResult)


                inferredTypeFromTop = NDynamicArrayType(expr.lineNr, expr.rowNr, firstType.create_copy())

                matchResult = extended_match_as_below(
                    inferredTypeFromBelow,
                    inferredTypeFromTop,
                    typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict
                )
                if matchResult == "several":
            
                    if not beSilentFlag:
                        util.log_error(expr.lineNr, expr.rowNr, "Several type cases can be selected with implicit variant-boxing. Please type specify.")
                    return (False, None)

                elif matchResult == "vbox":

                    if not beSilentFlag:
                        # annotation
                        expr.values = newValues
                        expr.inferredType = inferredTypeFromTop 

                    vbox = NVariantBoxExpression(expr.lineNr, expr.rowNr, expr)

                    if not beSilentFlag:
                        # annotate
                        vbox.inferredType = inferredTypeFromBelow.create_copy()

                    return (inferredTypeFromBelow.create_copy(), vbox)

                elif matchResult:

                    if not beSilentFlag:
                        expr.value = newValues
                        expr.inferredType = inferredTypeFromTop

                    return (inferredTypeFromTop.create_copy(), expr)
                    
                else:
                    if not beSilentFlag:
                        util.log_error(expr.lineNr, expr.rowNr, "Type mismatch.")
                        print("Expected: ", end='')
                        inferredTypeFromBelow.print_it()
                        print("")  # newline
                        print("Found: ", end='')
                        inferredTypeFromTop.print_it()
                        print("") # newline

                    return (False, None)     

    elif isinstance(expr, NArrayExpressionNoInitialization):

        typeResult, exprResult = type_infer_and_annotate_expression(
            expr.length, NISizeType(expr.lineNr, expr.rowNr), 
            typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict, 
            funDictStack, builtInFunsDict, directlyImportedFunsDictDict, otherImportedModulesFunDictDict,
            beSilentFlag
        )
        if typeResult == False:
            return (False, None)

        if isinstance(inferredTypeFromBelow, NUnknownType):

            if not beSilentFlag:
                util.log_error(expr.lineNr, expr.rowNr, "Unable to infer exact type of array expression. Please type specify.")
            return (False, None)

        elif isinstance(inferredTypeFromBelow, NDynamicArrayType):

            if not beSilentFlag:
                expr.length = exprResult
                expr.inferredType = inferredTypeFromBelow.create_copy()

            return (inferredTypeFromBelow.create_copy(), expr)

        else:

            # If it is a variant-box type directly or indirectly, we don't have enough info on this expr construct:

            if not beSilentFlag:
                util.log_error(expr.lineNr, expr.rowNr, "Type mismatch, or alternatively not enough type information (perhaps you can specify the type).")
                print("Expected: ", end='')
                inferredTypeFromBelow.print_it()
                print("")  # newline

            return (False, None)

    elif isinstance(expr, NArrayExpressionRepeatedValue):

        if isinstance(inferredTypeFromBelow, NUnknownType):

            typeResult, exprResult = type_infer_and_annotate_expression(
                expr.repeatedValue, NUnknownType(expr.repeatedValue.lineNr, expr.repeatedValue.rowNr),
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict, 
                funDictStack, builtInFunsDict, directlyImportedFunsDictDict, otherImportedModulesFunDictDict,
                beSilentFlag
            )
            if typeResult == False:
                return (False, None)

            lenTypeResult, lenExprResult = type_infer_and_annotate_expression(
                expr.length, NISizeType(expr.length.lineNr, expr.length.rowNr),
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict, 
                funDictStack, builtInFunsDict, directlyImportedFunsDictDict, otherImportedModulesFunDictDict,
                beSilentFlag
            )
            if lenTypeResult == False:
                return (False, None)                

            if not beSilentFlag:
                expr.inferredType = NDynamicArrayType(expr.lineNr, expr.rowNr, typeResult.create_copy())
            
            return (expr.inferredType.create_copy(), expr)
            
        elif isinstance(inferredTypeFromBelow, NDynamicArrayType):

            expectedIndexType = inferredTypeFromBelow.valueType

            typeResult, exprResult = type_infer_and_annotate_expression(
                expr.repeatedValue, expectedIndexType,
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict, 
                funDictStack, builtInFunsDict, directlyImportedFunsDictDict, otherImportedModulesFunDictDict,
                beSilentFlag
            )
            if typeResult == False:
                return (False, None)

            lenTypeResult, lenExprResult = type_infer_and_annotate_expression(
                expr.length, NISizeType(expr.length.lineNr, expr.length.rowNr),
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict, 
                funDictStack, builtInFunsDict, directlyImportedFunsDictDict, otherImportedModulesFunDictDict,
                beSilentFlag
            )
            if lenTypeResult == False:
                return (False, None) 


            if not beSilentFlag:
                expr.inferredType = NDynamicArrayType(expr.lineNr, expr.rowNr, typeResult.create_copy())
            
            return (expr.inferredType.create_copy(), expr)            

        else:

            # It may match on a direct or indirect NVariantBoxType:

            typeResult, exprResult = type_infer_and_annotate_expression(
                expr.repeatedValue, NUnknownType(expr.repeatedValue.lineNr, expr.repeatedValue.rowNr),
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict, 
                funDictStack, builtInFunsDict, directlyImportedFunsDictDict, otherImportedModulesFunDictDict,
                beSilentFlag
            )
            if typeResult == False:
                return (False, None)

            lenTypeResult, lenExprResult = type_infer_and_annotate_expression(
                expr.length, NISizeType(expr.length.lineNr, expr.length.rowNr),
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict, 
                funDictStack, builtInFunsDict, directlyImportedFunsDictDict, otherImportedModulesFunDictDict,
                beSilentFlag
            )
            if lenTypeResult == False:
                return (False, None)

            inferredTypeFromTop = NDynamicArrayType(expr.lineNr, expr.rowNr, typeResult.create_copy())

            matchResult = extended_match_as_below(
                inferredTypeFromBelow,
                inferredTypeFromTop,
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict
            )     

            if matchResult == "several":
        
                if not beSilentFlag:
                    util.log_error(expr.lineNr, expr.rowNr, "Several type cases can be selected with implicit variant-boxing. Please type specify.")
                return (False, None)

            elif matchResult == "vbox":

                if not beSilentFlag:
                    expr.inferredType = inferredTypeFromTop

                vbox = NVariantBoxExpression(expr.lineNr, expr.rowNr, expr)

                if not beSilentFlag:
                    # annotate
                    vbox.inferredType = inferredTypeFromBelow.create_copy()
                    
                return (inferredTypeFromBelow.create_copy(), vbox)    

            elif matchResult:

                if not beSilentFlag:
                    expr.inferredType = inferredTypeFromTop

                return (inferredTypeFromTop.create_copy, expr)
                
            else:
                if not beSilentFlag:
                    util.log_error(expr.lineNr, expr.rowNr, "Type mismatch.")
                    print("Expected: ", end='')
                    inferredTypeFromBelow.print_it()
                    print("")  # newline
                    print("Found: ", end='')
                    inferredTypeFromTop.print_it()
                    print("") # newline

                return (False, None) 
  

    elif isinstance(expr, NStructExpression):

        if isinstance(inferredTypeFromBelow, NUnknownType):

            # TODO

            util.log_error(expr.lineNr, expr.rowNr, "Type checking struct expressions NOT IMPLEMENTED YET.")
            return (False, None)

        elif isinstance(inferredTypeFromBelow, NStructType):

            # TODO

            util.log_error(expr.lineNr, expr.rowNr, "Type checking struct expressions NOT IMPLEMENTED YET.")
            return (False, None)

        else:
            # TODO

            util.log_error(expr.lineNr, expr.rowNr, "Type checking struct expressions NOT IMPLEMENTED YET.")
            return (False, None) 

    elif isinstance(expr, NVariantBoxExpression):

        # TODO

        util.log_error(expr.lineNr, expr.rowNr, "Type checking variant-box expressions NOT IMPLEMENTED YET.")
        return (False, None)

    elif isinstance(expr, NTypeClarifiedExpression):

        # TODO

        util.log_error(expr.lineNr, expr.rowNr, "Type checking type clarified expressions NOT IMPLEMENTED YET.")
        return (False, None)

    elif isinstance(expr, NArrayIndexing):

        # TODO

        util.log_error(expr.lineNr, expr.rowNr, "Type checking general array indexing expressions NOT IMPLEMENTED YET.")
        return (False, None)

    elif isinstance(expr, NStructIndexing):

        # TODO

        util.log_error(expr.lineNr, expr.rowNr, "Type checking general struct indexing expressions NOT IMPLEMENTED YET.")
        return (False, None)

    elif isinstance(expr, NVariantBoxCastExpression):

        # TODO

        util.log_error(expr.lineNr, expr.rowNr, "Type checking variant-box cast expressions NOT IMPLEMENTED YET.")
        return (False, None)

    elif isinstance(expr, NAndSymbolExpression):

        # TODO

        util.log_error(expr.lineNr, expr.rowNr, "Type checking '&&' expressions NOT IMPLEMENTED YET.")
        return (False, None)

    elif isinstance(expr, NOrSymbolExpression):

        # TODO

        util.log_error(expr.lineNr, expr.rowNr, "Type checking '||' expressions NOT IMPLEMENTED YET.")
        return (False, None)

    elif isinstance(expr, NEndExpression):

        util.log_error(expr.lineNr, expr.rowNr, "SHOULD NOT HAPPEN: type inference encountered unexpanded end expression...")
        return (False, None)

    elif isinstance(expr, NFunctionCall):

        # TODO

        util.log_error(expr.lineNr, expr.rowNr, "Type checking function call expressions NOT IMPLEMENTED YET.")
        return (False, None)

    elif isinstance(expr, NIFExpression):

        # TODO

        util.log_error(expr.lineNr, expr.rowNr, "Type checking 'IF' expressions NOT IMPLEMENTED YET.")
        return (False, None)

    elif isinstance(expr, NSWITCHExpression):

        # TODO

        util.log_error(expr.lineNr, expr.rowNr, "Type checking 'SWITCH' expressions NOT IMPLEMENTED YET.")
        return (False, None)

    elif isinstance(expr, NCONTENTTYPEExpression):

        # TODO

        util.log_error(expr.lineNr, expr.rowNr, "Type checking 'STORETYPE' expressions NOT IMPLEMENTED YET.")
        return (False, None)

    else:
        util.log_error(expr.lineNr, expr.rowNr, "Type inference strangely encountered unknown expression.")
        return (False, None)



# Returns True, False, "several", or "vbox"...

# This version of match_as_below can also match against NUnknownType,
# And returns "vbox" if its possible to vbox to that type case to match,
# or returns "several" if there are several possible vboxing cases, which is practically impossible though

# A bit hackish, yes...

def extended_match_as_below(t, inferredMatchType, typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict):

    if isinstance(t, NUnknownType):
        return True
    else:
        matchResult = match_as_below(t, inferredMatchType, typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict, 0)

        if matchResult:
            return matchResult
        else:
            if isinstance(t, NVariantBoxType):

                theFound = False

                for typ in t.types:
                    matchRes = match_as_below(typ, inferredMatchType, typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict, 0)

                    if matchRes:
                        if theFound != False: # several possible matches -- does this really happen -- hardly since all extensions are distinct...
                            return "several"
                        else:
                            theFound = typ.create_copy()

                return theFound

            else:
                return False




def run_pass(
    programAST, 
    typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict, 
    funDict, builtInFunsDict, directlyImportedFunsDictDict, otherImportedModulesFunDictDict
):

    funDictStack = [funDict]

    blockNumberList = []

    for statement in programAST.statements:
        success = type_check_statement(
            statement, blockNumberList, 0,
            typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict, 
            funDictStack, builtInFunsDict, directlyImportedFunsDictDict, otherImportedModulesFunDictDict
        )
        if success == False:
            return False

    return True



def type_check_statement(
    statement, blockNumberList, depth,
    typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict, 
    funDictStack, builtInFunsDict, directlyImportedFunsDictDict, otherImportedModulesFunDictDict
):


    if isinstance(statement, NRefToFunctionDeclarationWithDefinition):

        actual = statement.funs[statement.funsIndex]              

        if len(blockNumberList) <= depth:
            for i in range(len(blockNumberList), depth + 1):
                blockNumberList.append(0)            
        else:
            blockNumberList[depth] += 1


        funcEntryList = funDictStack[len(funDictStack) - 1][actual.name.name].funEntries

        funcEntry = None # dummy
        for fentry in funcEntryList:
            if fentry.mangledName == actual.mangledName:
                funcEntry = fentry                 # we better find it... below code assumes != None


        for stmt in actual.body.statements:
            success = type_check_statement(
                stmt, blockNumberList, depth + 1,
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict, 
                funDictStack + [funcEntry.localDict], builtInFunsDict, directlyImportedFunsDictDict, otherImportedModulesFunDictDict
            )
            if success == False:
                return False

        return True

            
    elif isinstance(statement, NBlock):

        if len(blockNumberList) <= depth:
            for i in range(len(blockNumberList), depth + 1):
                blockNumberList.append(0)            
        else:
            blockNumberList[depth] += 1

        for stmt in statement.statements:
            success = type_check_statement(
                stmt, blockNumberList, depth + 1,
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict, 
                funDictStack + [funDictStack[len(funDictStack) - 1][str(blockNumberList[depth])].localDict], builtInFunsDict, directlyImportedFunsDictDict, otherImportedModulesFunDictDict
            )
            if success == False:
                return False

        return True

    elif isinstance(statement, NIfStatement):

        typeResult, exprResult = type_infer_and_annotate_expression(
            statement.condition, NUnknownType(statement.condition.lineNr, statement.condition.rowNr), 
            typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict, 
            funDictStack, builtInFunsDict, directlyImportedFunsDictDict, otherImportedModulesFunDictDict,
            False
        )
        if typeResult == False:
            return False
        else:
            statement.condition = exprResult

        success = type_check_statement(
            statement.ifBlock, blockNumberList, depth,
            typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict, 
            funDictStack, builtInFunsDict, directlyImportedFunsDictDict, otherImportedModulesFunDictDict
        )
        if success == False:
            return False

        for elseIfClause in statement.elseIfClauses:

            typeResult, exprResult = type_infer_and_annotate_expression(
                elseIfClause.condition, NUnknownType(statement.condition.lineNr, statement.condition.rowNr), 
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict, 
                funDictStack, builtInFunsDict, directlyImportedFunsDictDict, otherImportedModulesFunDictDict,
                False
            )
            if typeResult == False:
                return False
            else:
                elseIfClause.condition = exprResult           

            success = type_check_statement(
                elseIfClause.block, blockNumberList, depth,
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict, 
                funDictStack, builtInFunsDict, directlyImportedFunsDictDict, otherImportedModulesFunDictDict
            )
            if success == False:
                return False
            
        
        if not statement.elseBlockOrNull is None:
            success = type_check_statement(
                statement.elseBlockOrNull, blockNumberList, depth,
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict, 
                funDictStack, builtInFunsDict, directlyImportedFunsDictDict, otherImportedModulesFunDictDict
            )
            if success == False:
                return False

        return True

    elif isinstance(statement, NRefToTemplateDeclarationWithDefinition):

        return True    # don't go further here I guess...

    elif isinstance(statement, NLoopStatement):

        success = type_check_statement(
            statement.block, blockNumberList, depth,
            typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict, 
            funDictStack, builtInFunsDict, directlyImportedFunsDictDict, otherImportedModulesFunDictDict
        )
        if success == False:
            return False

        return True

    elif isinstance(statement, NForStatement):

        if not statement.rangeOrNull is None:
            typeResult, exprResult = type_infer_and_annotate_expression(
                statement.rangeOrNull.rangeFrom, statement.rangeOrNull.counterType, 
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict, 
                funDictStack, builtInFunsDict, directlyImportedFunsDictDict, otherImportedModulesFunDictDict,
                False
            )
            if typeResult == False:
                return False
            else:
                statement.rangeOrNull.rangeFrom = exprResult  

            typeResult, exprResult = type_infer_and_annotate_expression(
                statement.rangeOrNull.rangeTo, statement.rangeOrNull.counterType, 
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict, 
                funDictStack, builtInFunsDict, directlyImportedFunsDictDict, otherImportedModulesFunDictDict,
                False
            )
            if typeResult == False:
                return False
            else:
                statement.rangeOrNull.rangeTo = exprResult

        for iteration in statement.iterations:

            if isinstance(iteration, NIterationIn):

                itType = NUnknownType(iteration.lineNr, iteration.rowNr)
                arrayType = NUnknownType(iteration.lineNr, iteration.rowNr)

                if not iteration.itTypeOrNull is None:
                    itType = iteration.itTypeOrNull
                    arrayType = NDynamicArrayType(iteration.lineNr, iteration.rowNr, itType.create_copy())                

                typeResult, exprResult = type_infer_and_annotate_expression(
                    iteration.arrayExpression, arrayType, 
                    typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict, 
                    funDictStack, builtInFunsDict, directlyImportedFunsDictDict, otherImportedModulesFunDictDict,
                    False
                )
                if typeResult == False:
                    return False
                else:
                    iteration.arrayExpression = exprResult

                # now set the name into block's type...                     
                dictOfTheBodyBlock = funDictStack[len(funDictStack) - 1][statement.block.blockEntryNumStr].localDict
                dictOfTheBodyBlock[iteration.itName.name].theType = iteration.arrayExpression.inferredType.valueType # hope this is good enough

            else: # NIterationOver hopefully...

                itType = NUnknownType(iteration.lineNr, iteration.rowNr)
                arrayType = NUnknownType(iteration.lineNr, iteration.rowNr)

                if not iteration.itTypeOrNull is None:
                    itType = iteration.itTypeOrNull
                    arrayType = NDynamicArrayType(iteration.lineNr, iteration.rowNr, itType.create_copy())

                typeResult, exprResult = type_infer_and_annotate_expression(
                    iteration.arrayLValue.lValueExpression, arrayType, 
                    typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict, 
                    funDictStack, builtInFunsDict, directlyImportedFunsDictDict, otherImportedModulesFunDictDict,
                    False
                )
                if typeResult == False:
                    return False
                else:
                    iteration.arrayLValue.lValueExpression = exprResult

                # now set the name into block's type...                     
                dictOfTheBodyBlock = funDictStack[len(funDictStack) - 1][statement.block.blockEntryNumStr].localDict
                dictOfTheBodyBlock[iteration.itName.name].theType = iteration.arrayLValue.lValueExpression.inferredType.valueType # hope this is good enough 

            # the rest can in Python be done for both iteration classes at the same time:

            if not iteration.indexfactorOrNull is None:
                typeResult, exprResult = type_infer_and_annotate_expression(
                    iteration.indexfactorOrNull, NISizeType(iteration.lineNr, iteration.rowNr), 
                    typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict, 
                    funDictStack, builtInFunsDict, directlyImportedFunsDictDict, otherImportedModulesFunDictDict,
                    False
                )
                if typeResult == False:
                    return False
                else:
                    iteration.indexfactorOrNull = exprResult
            
            if not iteration.indexoffsetOrNull is None: 
                typeResult, exprResult = type_infer_and_annotate_expression(
                    iteration.indexoffsetOrNull, NISizeType(iteration.lineNr, iteration.rowNr), 
                    typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict, 
                    funDictStack, builtInFunsDict, directlyImportedFunsDictDict, otherImportedModulesFunDictDict,
                    False
                )
                if typeResult == False:
                    return False
                else:
                    iteration.indexoffsetOrNull = exprResult          


        success = type_check_statement(
            statement.block, blockNumberList, depth,
            typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict, 
            funDictStack, builtInFunsDict, directlyImportedFunsDictDict, otherImportedModulesFunDictDict
        )
        if success == False:
            return False

        return True

    elif isinstance(statement, NSwitchStatement):

        typeResult, exprResult = type_infer_and_annotate_expression(
            statement.switchValue, NUnknownType(statement.switchValue.lineNr, statement.switchValue.rowNr), 
            typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict, 
            funDictStack, builtInFunsDict, directlyImportedFunsDictDict, otherImportedModulesFunDictDict,
            False
        )
        if typeResult == False:
            return False
        else:
            statement.switchValue = exprResult


        for case in statement.cases:

            for caseValue in case.caseValues:
                
                typeResult, exprResult = type_infer_and_annotate_expression(
                    caseValue, statement.switchValue.inferredType,    # this will allow vboxing here though... 
                    typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict, 
                    funDictStack, builtInFunsDict, directlyImportedFunsDictDict, otherImportedModulesFunDictDict,
                    False
                )
                if typeResult == False:
                    return False
                else:
                    pass  # we actually don't have to set it here actually... TODO UNLESS VBOXING.....!!!!!! which should not be here TODO

            success = type_check_statement(
                case.block, blockNumberList, depth,
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict, 
                funDictStack, builtInFunsDict, directlyImportedFunsDictDict, otherImportedModulesFunDictDict
            )
            if success == False:
                return False     

        if not statement.defaultCaseOrNull is None:
            success = type_check_statement(
                statement.defaultCaseOrNull, blockNumberList, depth,
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict, 
                funDictStack, builtInFunsDict, directlyImportedFunsDictDict, otherImportedModulesFunDictDict
            )
            if success == False:
                return False  

        return True

    elif isinstance(statement, NContenttypeStatement):

        # TODO

        util.log_error(statement.lineNr, statement.rowNr, "Typechecking/expanding 'storetype' statements is NOT YET IMPLEMENTED.")
        return False               

    
    elif isinstance(statement, NNormalAssignment):

        if len(statement.leftHandSide) == 1:

            lhsType = None

            if isinstance(statement.leftHandSide[0], NVariableDeclaration):

                lhsType = statement.leftHandSide[0].theType.create_copy()

            else: # LValueContainer hopefully...

                typeResult, exprResult = type_infer_and_annotate_expression(
                    statement.leftHandSide[0].lValueExpression, NUnknownType(statement.lineNr, statement.rowNr),    
                    typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict, 
                    funDictStack, builtInFunsDict, directlyImportedFunsDictDict, otherImportedModulesFunDictDict,
                    False
                )
                if typeResult == False:
                    return False
                else:
                    statement.leftHandSide[0].lValueExpression = exprResult

                lhsType = typeResult.create_copy()


            typeResult, exprResult = type_infer_and_annotate_expression(
                statement.value, lhsType,    
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict, 
                funDictStack, builtInFunsDict, directlyImportedFunsDictDict, otherImportedModulesFunDictDict,
                False
            )
            if typeResult == False:
                return False
            else:
                statement.value = exprResult

            return True

        else:
            # TODO
    
            util.log_error(statement.lineNr, statement.rowNr, "Typechecking multiple assignment NOT YET IMPLEMENTED.")
            return False


        return True
  
    elif (isinstance(statement, NModuloAssignment) or
        isinstance(statement, NMultiplicationAssignment) or
        isinstance(statement, NDivisionAssignment) or
        isinstance(statement, NAdditionAssignment) or
        isinstance(statement, NSubtractionAssignment)
    ):

        if len(statement.leftHandSide) == 1:

            typeResult, exprResult = type_infer_and_annotate_expression(
                statement.leftHandSide[0].lValueExpression, NUnknownType(statement.lineNr, statement.rowNr),    
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict, 
                funDictStack, builtInFunsDict, directlyImportedFunsDictDict, otherImportedModulesFunDictDict,
                False
            )
            if typeResult == False:
                return False
            else:
                statement.leftHandSide[0].lValueExpression = exprResult

            lhsType = typeResult.create_copy()


            typeResult, exprResult = type_infer_and_annotate_expression(
                statement.value, lhsType,    
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict, 
                funDictStack, builtInFunsDict, directlyImportedFunsDictDict, otherImportedModulesFunDictDict,
                False
            )
            if typeResult == False:
                return False
            else:
                statement.value = exprResult

            return True

        else:
            util.log_error(statement.lineNr, statement.rowNr, "Typechecking multiple compound assignment NOT YET IMPLEMENTED.")
            return False


    elif isinstance(statement, NReturnStatement):

        for returnExpression in statement.returnExpressions:
            typeResult, exprResult = type_infer_and_annotate_expression(
                returnExpression, NUnknownType(statement.lineNr, statement.rowNr),    
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict, 
                funDictStack, builtInFunsDict, directlyImportedFunsDictDict, otherImportedModulesFunDictDict,
                False
            )
            if typeResult == False:
                return False
            else:
                pass # no problem here

        return True

    elif isinstance(statement, NFunctionCallStatement):

        # TODO

        util.log_error(statement.lineNr, statement.rowNr, "Typechecking function call statements is NOT YET IMPLEMENTED.")
        return False                    
    
    else:
        return True


