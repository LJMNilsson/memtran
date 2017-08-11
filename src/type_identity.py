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




_MAX_TYPE_MATCH_LEVEL = 20



#   boolean match_as_below(  // this returns either False or True
    #    NType t,
    #    NType inferredMatchType, 
    #    Dictionary<TypeDeclarationWithDefinition> typeDict, 
    #    Dictionary<TypeDeclarationWithDefinition> directlyImportedTypesDictDict, 
    #    Dictionary<TypeDeclarationWithDefinition> otherImportedModulesTypeDictDict,
    #    int matchDepth    
    # ); 

def match_as_below(t, inferredMatchType, typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict, matchDepth):

    if isinstance(t, NIdentifierType):

        if isinstance(inferredMatchType, NParametrizedIdentifierType):

            if matchDepth >= _MAX_TYPE_MATCH_LEVEL:
                return False

            return match_as_below(
                t,
                create_substitution(inferredMatchType, typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict),
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                matchDepth + 1
            )

        elif isinstance(inferredMatchType, NIdentifierType):
            

            if (t.moduleNameOrNull is None) and (inferredMatchType.moduleNameOrNull is None) and (t.name.name == inferredMatchType.name.name):  
                # try identifier textual identity first...
                return True    # hope this is correct!!!
            elif ((not t.moduleNameOrNull is None) and
                (not inferredMatchType.moduleNameOrNull is None) and (t.name.name == inferredMatchType.name.name) and 
                    (t.moduleNameOrNull.name == inferredMatchType.moduleNameOrNull.name)
            ):
                return True 

            if matchDepth >= _MAX_TYPE_MATCH_LEVEL:
                return False

            return match_as_below(
                t.get_definition(typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict),
                inferredMatchType.get_definition(typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict),
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                matchDepth + 1
            )

        else:
            if matchDepth >= _MAX_TYPE_MATCH_LEVEL:
                return False

            return match_as_below(
                t.get_definition(typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict),
                inferredMatchType,
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                matchDepth + 1
            )

    elif isinstance(t, NNilType):

        if isinstance(inferredMatchType, NParametrizedIdentifierType):

            if matchDepth >= _MAX_TYPE_MATCH_LEVEL:
                return False

            return match_as_below(
                t,
                create_substitution(inferredMatchType, typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict),
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                matchDepth + 1
            )

        elif isinstance(inferredMatchType, NIdentifierType):

            if matchDepth >= _MAX_TYPE_MATCH_LEVEL:
                return False

            return match_as_below(
                t,
                inferredMatchType.get_definition(typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict),
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                matchDepth + 1
            )

        elif isinstance(inferredMatchType, NNilType):

            return True

        else:

            return False


    elif isinstance(t, NBoolType):

        if isinstance(inferredMatchType, NParametrizedIdentifierType):

            if matchDepth >= _MAX_TYPE_MATCH_LEVEL:
                return False

            return match_as_below(
                t,
                create_substitution(inferredMatchType, typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict),
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                matchDepth + 1
            )

        elif isinstance(inferredMatchType, NIdentifierType):

            if matchDepth >= _MAX_TYPE_MATCH_LEVEL:
                return False

            return match_as_below(
                t,
                inferredMatchType.get_definition(typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict),
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                matchDepth + 1
            )

        elif isinstance(inferredMatchType, NBoolType):

            return True

        else:

            return False

    elif isinstance(t, NI8Type):

        if isinstance(inferredMatchType, NParametrizedIdentifierType):

            if matchDepth >= _MAX_TYPE_MATCH_LEVEL:
                return False

            return match_as_below(
                t,
                create_substitution(inferredMatchType, typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict),
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                matchDepth + 1
            )

        elif isinstance(inferredMatchType, NIdentifierType):

            if matchDepth >= _MAX_TYPE_MATCH_LEVEL:
                return False

            return match_as_below(
                t,
                inferredMatchType.get_definition(typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict),
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                matchDepth + 1
            )

        elif isinstance(inferredMatchType, NI8Type):

            return True

        else:

            return False                

    elif isinstance(t, NI16Type):

        if isinstance(inferredMatchType, NParametrizedIdentifierType):

            if matchDepth >= _MAX_TYPE_MATCH_LEVEL:
                return False

            return match_as_below(
                t,
                create_substitution(inferredMatchType, typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict),
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                matchDepth + 1
            )

        elif isinstance(inferredMatchType, NIdentifierType):

            if matchDepth >= _MAX_TYPE_MATCH_LEVEL:
                return False

            return match_as_below(
                t,
                inferredMatchType.get_definition(typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict),
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                matchDepth + 1
            )

        elif isinstance(inferredMatchType, NI16Type):

            return True

        else:

            return False

    elif isinstance(t, NI32Type):

        if isinstance(inferredMatchType, NParametrizedIdentifierType):

            if matchDepth >= _MAX_TYPE_MATCH_LEVEL:
                return False

            return match_as_below(
                t,
                create_substitution(inferredMatchType, typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict),
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                matchDepth + 1
            )

        elif isinstance(inferredMatchType, NIdentifierType):

            if matchDepth >= _MAX_TYPE_MATCH_LEVEL:
                return False

            return match_as_below(
                t,
                inferredMatchType.get_definition(typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict),
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                matchDepth + 1
            )

        elif isinstance(inferredMatchType, NI32Type):

            return True

        else:

            return False

    elif isinstance(t, NI64Type):

        if isinstance(inferredMatchType, NParametrizedIdentifierType):

            if matchDepth >= _MAX_TYPE_MATCH_LEVEL:
                return False

            return match_as_below(
                t,
                create_substitution(inferredMatchType, typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict),
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                matchDepth + 1
            )

        elif isinstance(inferredMatchType, NIdentifierType):

            if matchDepth >= _MAX_TYPE_MATCH_LEVEL:
                return False

            return match_as_below(
                t,
                inferredMatchType.get_definition(typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict),
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                matchDepth + 1
            )

        elif isinstance(inferredMatchType, NI64Type):

            return True

        else:

            return False

    elif isinstance(t, NISizeType):

        if isinstance(inferredMatchType, NParametrizedIdentifierType):

            if matchDepth >= _MAX_TYPE_MATCH_LEVEL:
                return False

            return match_as_below(
                t,
                create_substitution(inferredMatchType, typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict),
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                matchDepth + 1
            )

        elif isinstance(inferredMatchType, NIdentifierType):

            if matchDepth >= _MAX_TYPE_MATCH_LEVEL:
                return False

            return match_as_below(
                t,
                inferredMatchType.get_definition(typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict),
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                matchDepth + 1
            )

        elif isinstance(inferredMatchType, NISizeType):

            return True

        else:

            return False

    elif isinstance(t, NU8Type):

        if isinstance(inferredMatchType, NParametrizedIdentifierType):

            if matchDepth >= _MAX_TYPE_MATCH_LEVEL:
                return False

            return match_as_below(
                t,
                create_substitution(inferredMatchType, typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict),
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                matchDepth + 1
            )

        elif isinstance(inferredMatchType, NIdentifierType):

            if matchDepth >= _MAX_TYPE_MATCH_LEVEL:
                return False

            return match_as_below(
                t,
                inferredMatchType.get_definition(typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict),
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                matchDepth + 1
            )

        elif isinstance(inferredMatchType, NU8Type):

            return True

        else:

            return False

    elif isinstance(t, NU16Type):

        if isinstance(inferredMatchType, NParametrizedIdentifierType):

            if matchDepth >= _MAX_TYPE_MATCH_LEVEL:
                return False

            return match_as_below(
                t,
                create_substitution(inferredMatchType, typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict),
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                matchDepth + 1
            )

        elif isinstance(inferredMatchType, NIdentifierType):

            if matchDepth >= _MAX_TYPE_MATCH_LEVEL:
                return False

            return match_as_below(
                t,
                inferredMatchType.get_definition(typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict),
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                matchDepth + 1
            )

        elif isinstance(inferredMatchType, NU16Type):

            return True

        else:

            return False

    elif isinstance(t, NU32Type):

        if isinstance(inferredMatchType, NParametrizedIdentifierType):

            if matchDepth >= _MAX_TYPE_MATCH_LEVEL:
                return False

            return match_as_below(
                t,
                create_substitution(inferredMatchType, typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict),
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                matchDepth + 1
            )

        elif isinstance(inferredMatchType, NIdentifierType):

            if matchDepth >= _MAX_TYPE_MATCH_LEVEL:
                return False

            return match_as_below(
                t,
                inferredMatchType.get_definition(typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict),
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                matchDepth + 1
            )

        elif isinstance(inferredMatchType, NU32Type):

            return True

        else:

            return False

    elif isinstance(t, NU64Type):

        if isinstance(inferredMatchType, NParametrizedIdentifierType):

            if matchDepth >= _MAX_TYPE_MATCH_LEVEL:
                return False

            return match_as_below(
                t,
                create_substitution(inferredMatchType, typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict),
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                matchDepth + 1
            )

        elif isinstance(inferredMatchType, NIdentifierType):

            if matchDepth >= _MAX_TYPE_MATCH_LEVEL:
                return False

            return match_as_below(
                t,
                inferredMatchType.get_definition(typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict),
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                matchDepth + 1
            )

        elif isinstance(inferredMatchType, NU64Type):

            return True

        else:

            return False

    elif isinstance(t, NUSizeType):

        if isinstance(inferredMatchType, NParametrizedIdentifierType):

            if matchDepth >= _MAX_TYPE_MATCH_LEVEL:
                return False

            return match_as_below(
                t,
                create_substitution(inferredMatchType, typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict),
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                matchDepth + 1
            )

        elif isinstance(inferredMatchType, NIdentifierType):

            if matchDepth >= _MAX_TYPE_MATCH_LEVEL:
                return False

            return match_as_below(
                t,
                inferredMatchType.get_definition(typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict),
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                matchDepth + 1
            )

        elif isinstance(inferredMatchType, NUSizeType):

            return True

        else:

            return False

    elif isinstance(t, NF32Type):

        if isinstance(inferredMatchType, NParametrizedIdentifierType):

            if matchDepth >= _MAX_TYPE_MATCH_LEVEL:
                return False

            return match_as_below(
                t,
                create_substitution(inferredMatchType, typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict),
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                matchDepth + 1
            )

        elif isinstance(inferredMatchType, NIdentifierType):

            if matchDepth >= _MAX_TYPE_MATCH_LEVEL:
                return False

            return match_as_below(
                t,
                inferredMatchType.get_definition(typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict),
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                matchDepth + 1
            )

        elif isinstance(inferredMatchType, NF32Type):

            return True

        else:

            return False

    elif isinstance(t, NF64Type):

        if isinstance(inferredMatchType, NParametrizedIdentifierType):

            if matchDepth >= _MAX_TYPE_MATCH_LEVEL:
                return False

            return match_as_below(
                t,
                create_substitution(inferredMatchType, typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict),
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                matchDepth + 1
            )

        elif isinstance(inferredMatchType, NIdentifierType):

            if matchDepth >= _MAX_TYPE_MATCH_LEVEL:
                return False

            return match_as_below(
                t,
                inferredMatchType.get_definition(typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict),
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                matchDepth + 1
            )

        elif isinstance(inferredMatchType, NF64Type):

            return True

        else:

            return False

    elif isinstance(t, NDynamicArrayType):

        if isinstance(inferredMatchType, NParametrizedIdentifierType):

            if matchDepth >= _MAX_TYPE_MATCH_LEVEL:
                return False

            return match_as_below(
                t,
                create_substitution(inferredMatchType, typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict),
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                matchDepth + 1
            )

        elif isinstance(inferredMatchType, NIdentifierType):

            if matchDepth >= _MAX_TYPE_MATCH_LEVEL:
                return False

            return match_as_below(
                t,
                inferredMatchType.get_definition(typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict),
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                matchDepth + 1
            )

        elif isinstance(inferredMatchType, NDynamicArrayType):

            return match_as_below(
                t.valueType,
                inferredMatchType.valueType,
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                matchDepth
            )

        else:

            return False

    elif isinstance(t, NStructType):

        if isinstance(inferredMatchType, NParametrizedIdentifierType):

            if matchDepth >= _MAX_TYPE_MATCH_LEVEL:
                return False

            return match_as_below(
                t,
                create_substitution(inferredMatchType, typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict),
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                matchDepth + 1
            )

        elif isinstance(inferredMatchType, NIdentifierType):

            if matchDepth >= _MAX_TYPE_MATCH_LEVEL:
                return False

            return match_as_below(
                t,
                inferredMatchType.get_definition(typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict),
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                matchDepth + 1
            )

        elif isinstance(inferredMatchType, NStructType):

            if t.tag.name != inferredMatchType.tag.name:
                return False

            if len(t.members) != len(inferredMatchType.members):
                return False

            for i in range(0, len(t.members)):
                if t.members[i].name.name != inferredMatchType.members[i].name.name:
                    return False

                postTypeMatchResult = match_as_below(
                    t.members[i].theType,
                    inferredMatchType.members[i].theType,
                    typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                    matchDepth
                )

                if postTypeMatchResult != True:
                    return postTypeMatchResult

            return True

        else:

            return False

    elif isinstance(t, NVariantBoxType):

        if isinstance(inferredMatchType, NParametrizedIdentifierType):

            if matchDepth >= _MAX_TYPE_MATCH_LEVEL:
                return False

            return match_as_below(
                t,
                create_substitution(inferredMatchType, typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict),
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                matchDepth + 1
            )

        elif isinstance(inferredMatchType, NIdentifierType):

            if matchDepth >= _MAX_TYPE_MATCH_LEVEL:
                return False

            return match_as_below(
                t,
                inferredMatchType.get_definition(typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict),
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                matchDepth + 1
            )

        elif isinstance(inferredMatchType, NVariantBoxType):

            if len(t.types) != len(inferredMatchType.types):
                return False

            for i in range(0, len(t.types)):
                matchResult = match_as_below(
                    t.types[i],
                    inferredMatchType.types[i],
                    typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                    matchDepth
                )

                if matchResult != True:
                    return matchResult

            return True

        else:

            return False

    elif isinstance(t, NFunctionType):

        if isinstance(inferredMatchType, NParametrizedIdentifierType):

            if matchDepth >= _MAX_TYPE_MATCH_LEVEL:
                return False

            return match_as_below(
                t,
                create_substitution(inferredMatchType, typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict),
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                matchDepth + 1
            )

        elif isinstance(inferredMatchType, NIdentifierType):

            if matchDepth >= _MAX_TYPE_MATCH_LEVEL:
                return False

            return match_as_below(
                t,
                inferredMatchType.get_definition(typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict),
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                matchDepth + 1
            )

        elif isinstance(inferredMatchType, NFunctionType):

            if len(t.typeArgs) != len(inferredMatchType.typeArgs):
                return False

            for i in range(0, len(t.typeArgs)):
                if isinstance(t.typeArgs[i], NNormalTypeArg):

                    if not isinstance(inferredMatchType.typeArgs[i], NNormalTypeArg):
                        return False

                    if t.typeArgs[i].isMu != inferredMatchType.typeArgs[i].isMu:
                        return False

                    if t.typeArgs[i].isConstruand != inferredMatchType.typeArgs[i].isConstruand:
                        return False

                    matchResult = match_as_below(
                        typeArgs[i].argType,
                        inferredMatchType.typeArgs[i].argType,
                        typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                        matchDepth
                    )
                    if matchResult != True:
                        return matchResult

                else:   # NRefTypeArg hopefully ...

                    if not isinstance(inferredMatchType.typeArgs[i], NRefTypeArg):
                        return False

                    matchResult = match_as_below(
                        t.typeArgs[i].argType,
                        inferredMatchType.typeArgs[i].argType,
                        typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                        matchDepth
                    )
                    if matchResult != True:
                        return matchResult

            
            if len(t.returnTypes) != len(inferredMatchType.returnTypes):
                return False

            for i in range(0, len(t.returnTypes)):
                matchResult = match_as_below(
                    t.returnTypes[i],
                    inferredMatchType.returnTypes[i],
                    typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                    matchDepth
                )
                if matchResult != True:
                    return matchResult            
           

            return True

        else:

            return False

    elif isinstance(t, NParametrizedIdentifierType):

        if isinstance(inferredMatchType, NParametrizedIdentifierType):

            if ((((t.moduleNameOrNull is None) and (inferredMatchType.moduleNameOrNull is None) and t.name.name == inferredMatchType.name.name) or
                ((not t.moduleNameOrNull is None) and (not inferredMatchType.moduleNameOrNull is None) and 
                (t.moduleNameOrNull.name == inferredMatchType.moduleNameOrNull.name) and (t.name.name == inferredMatchType.name.name))
            )) and (len(t.params) == len(inferredMatchType.params)):
                
                matchResults = []

                for i in range(0, len(t.params)):
                    matchResults.append(
                        match_as_below(
                            t.params[i],
                            inferredMatchType.params[i],
                            typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                            matchDepth
                        )
                    )

                if all(matchResults):
                    return True

            # otherwise, continue here below:

            if matchDepth >= _MAX_TYPE_MATCH_LEVEL:
                return False

            return match_as_below( 
                create_substitution(t, typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict),
                create_substitution(inferredMatchType, typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict),
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                matchDepth + 1
            )

        elif isinstance(inferredMatchType, NIdentifierType):

            if matchDepth >= _MAX_TYPE_MATCH_LEVEL:
                return False

            return match_as_below(
                create_substitution(t, typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict),
                inferredMatchType.get_definition(typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict),
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                matchDepth + 1
            )

        else:

            if matchDepth >= _MAX_TYPE_MATCH_LEVEL:
                return False            

            return match_as_below(
                create_substitution(t, typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict),
                inferredMatchType,
                typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict,
                matchDepth + 1
            )

    else:
        util.log_error(t.lineNr, t.rowNr, "Trying to match on unmatchy kind of type. SHOULD NOT HAPPEN")
        return False





# Parametrized Type substitution functions will have to be at home in this module simply...

def create_substitution(parametrizedType, typeDict, directlyImportedTypesDictDict, otherImportedModulesTypeDictDict):


    unsubstitutedTypeDecl = None

    if parametrizedType.moduleNameOrNull is None:
       
        if  parametrizedType.name.name in typeDict:
            unsubstitutedTypeDecl = typeDict[ parametrizedType.name.name]
        else:
            for moduleName, directlyImportedTypesDict in directlyImportedTypesDictDict.items():
                if parametrizedType.name.name in directlyImportedTypesDict:
                    unsubstitutedTypeDecl = directlyImportedTypesDict[parametrizedType.name.name]
                    break

            if unsubstitutedTypeDecl is None:  # (still)
                util.log_error( parametrizedType.lineNr,  parametrizedType.rowNr, "Type match: named type's definition not found. SHOULD NOT HAPPEN.")     
                return NStructType( parametrizedType.lineNr, parametrizedType.rowNr, NIdentifier( parametrizedType.lineNr,  parametrizedType.rowNr, "ERRORRR"), [])

    else:                

        if  parametrizedType.moduleNameOrNull.name in otherImportedModulesTypeDictDict:
            moduleTypeDict = otherImportedModulesTypeDictDict[parametrizedType.moduleNameOrNull.name]
            
            if parametrizedType.name.name in moduleTypeDict:
                unsubstitutedTypeDecl = moduleTypeDict[parametrizedType.name.name].theType                    
            else:
                util.log_error(parametrizedType.lineNr, parametrizedType.rowNr, "Named type's definition not found for type match. SHOULD NOT HAPPEN #18")
                return NStructType(parametrizedType.lineNr, parametrizedType.rowNr, NIdentifier(parametrizedType.lineNr, parametrizedType.rowNr, "ERRORRR"), [])              

        else:
            util.log_error(parametrizedType.lineNr, parametrizedType.rowNr, "Module not found for named type match. SHOULD NOT HAPPEN #8")
            return NStructType(parametrizedType.lineNr, parametrizedType.rowNr, NIdentifier(parametrizedType.lineNr, parametrizedType.rowNr, "ERRORRR"), [])



    unsubstitutedType = unsubstitutedTypeDecl.theType     

    paramDict = {}
    
    if unsubstitutedTypeDecl.paramsOrNull is None:
        util.log_error(parametrizedType.lineNr, parametrizedType.rowNr, "Found un-parametrized definition for parametrized type during type match. SHOULD NOT HAPPEN.")
        return NStructType(parametrizedType.lineNr, parametrizedType.rowNr, NIdentifier(parametrizedType.lineNr, parametrizedType.rowNr, "ERRORRR"), [])

    for i in range(0, len(unsubstitutedTypeDecl.paramsOrNull)):
        paramDict[unsubstitutedTypeDecl.paramsOrNull[i].name] = parametrizedType.params[i].create_copy()


    return create_substitution_helper(unsubstitutedType, paramDict) 






def create_substitution_helper(unsubstitutedType, paramsDict):
    
    if isinstance(unsubstitutedType, NIdentifierType):

        if (unsubstitutedType.moduleNameOrNull is None) and (unsubstitutedType.name.name in paramsDict):
            return paramsDict[unsubstitutedType.name.name].create_copy()
        else:
            return unsubstitutedType.create_copy()

    elif isinstance(unsubstitutedType, NDynamicArrayType):

        return NDynamicArrayType(
            unsubstitutedType.lineNr,
            unsubstitutedType.rowNr,
            create_substitution_helper(unsubstitutedType.valueType, paramsDict)
        )

    elif isinstance(unsubstitutedType, NStructType):

        newMembers = []
        for member in unsubstitutedType.members:
            newMembers.append(
                NStructTypeMember(
                    member.lineNr,
                    member.rowNr,
                    member.name.create_copy(),
                    create_substitution_helper(member, paramsDict)
                )
            )

        return NStructType(
            unsubstitutedType.lineNr,
            unsubstitutedType.rowNr,
            unsubstitutedType.tag.create_copy(),
            newMembers
        )

    elif isinstance(unsubstitutedType, NVariantBoxType):

        newTypes = []
        for t in unsubstitutedType.types:
            newTypes.append(
                create_substitution_helper(t, paramsDict)
            )

        return NVariantBoxType(
            unsubstitutedType.lineNr,
            unsubstitutedType.rowNr,
            newTypes
        )

    elif isinstance(unsubstitutedType, NFunctionType):

        newArgs = []
        for arg in unsubstitutedType.typeArgs:
            if isinstance(arg, NNormalTypeArg):

                newArgs.append(
                    NNormalTypeArg(
                        arg.lineNr,
                        arg.rowNr,
                        arg.isMu,
                        arg.isConstruand,
                        create_substitution_helper(arg.argType, paramsDict)
                    )
                )

            else: # NRefTypeArg hopefully

                newArgs.append(
                    NRefTypeArg(
                        arg.lineNr,
                        arg.rowNr,
                        create_substitution_helper(arg.argType, paramsDict)
                    )
                )    


        newReturnTypes = []
        for returnType in unsubstitutedType.returnTypes:
            newReturnTypes.append(
                create_substitution_helper(returnType, paramsDict)
            )

        
        return NFunctionType(
            unsubstitutedType.lineNr,
            unsubstitutedType.rowNr,
            newArgs,
            newReturnTypes
        )

    elif isinstance(unsubstitutedType, NParametrizedIdentifierType):

        newParams = []
        for param in unsubstitutedType.params:
            newParams.append(
                create_substitution_helper(param, paramsDict)
            )

        return NParametrizedIdentifierType(
            unsubstitutedType.lineNr,
            unsubstitutedType.rowNr,
            unsubstitutedType.moduleNameOrNull,  # we don't bother to copy this...
            unsubstitutedType.name.create_copy(),
            newParams
        )

    else:
        return unsubstitutedType    





# NOTE: A CONCRETIZER IS A BAD IDEA DUE TO RECURSIVE TYPES. AVOID IT AT ALL COSTS.







