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



# returns an inferred type for the expression, or False if the inferring failed

def type_infer_and_annotate_expression(
    expr, inferredTypeFromBelow, typeDict, directlyImportedTypesDict, otherImportedModulesTypeDictDict, funDictsStack, directlyImportedFunsDict, otherImportedModulesFunDictDict
):
    
    if isinstance(expr, NIdentifierExpression):

        foundDefinition = None

        if expr.moduleNameOrNull is None:
            for funDict in reverse(funDictStack):
                if expr.name.name in funDict:
                    foundDefinition = funDict[expr.name.name]
                    break

            if foundDefinition is None:
                if expr.name.name in directlyImportedFunsDict:
                    foundDefinition = directlyImportedFunsDict[expr.name.name]

        else:
            if expr.moduleNameOrNull in otherImportedModulesFunDictDict:

                moduleDict = otherImportedModulesFunDictDict[expr.moduleNameOrNull]

                if expr.name.name in moduleDict:
                    foundDefinition = moduleDict[expr.name.name]            

            else:
                util.log_error(expr.lineNr, expr.rowNr, "Reference to module that has not been imported.")
                return False
                 
    
        if foundDefinition is None:
            util.log_error(expr.lineNr, expr.rowNr, "Usage of name that has not been declared.")
            return False

        if isinstance(foundDefinition, FunListEntry):

            # TODO

        elif isinstance(foundDefinition, VarEntry):

            # TODO    DOUBLE TODO: We have to check that the definition comes totally before!!! How!

        elif 


        # TODO

    elif isinstance(expr, NNilExpression):

        # TODO

    elif isinstance(expr, NTrueExpression):

        # TODO

    elif isinstance(expr, NFalseExpression):

        # TODO

    elif isinstance(expr, NIntegerExpression):

        # TODO

    elif isinstance(expr, NFloatingPointNumberExpression):

        # TODO

    elif isinstance(expr, NStringExpression):

        # TODO

    elif isinstance(expr, NArrayExpressionIndividualValues):

        # TODO

    elif isinstance(expr, NArrayExpressionNoInitialization):

        # TODO

    elif isinstance(expr, NArrayExpressionRepeatedValue):

        # TODO

    elif isinstance(expr, NStructExpression):

        # TODO

    elif isinstance(expr, NVariantBoxExpression):

        # TODO

    elif isinstance(expr, NTypeClarifiedExpression):

        # TODO

    elif isinstance(expr, NArrayIndexing):

        # TODO

    elif isinstance(expr, NStructIndexing):

        # TODO

    elif isinstance(expr, NVariantBoxCastExpression):

        # TODO

    elif isinstance(expr, NAndSymbolExpression):

        # TODO

    elif isinstance(expr, NOrSymbolExpression):

        # TODO

    elif isinstance(expr, NEndExpression):

        util.log_error(expr.lineNr, expr.rowNr, "SHOULD NOT HAPPEN: type inference encountered unexpanded end expression...")
        return False

    elif isinstance(expr, NFunctionCall):

        # TODO

    elif isinstance(expr, NIFExpression):

        # TODO

    elif isinstance(expr, NSWITCHExpression):

        # TODO

    elif isinstance(expr, NCONTENTTYPEExpression):

        # TODO

    else:
        util.log_error(expr.lineNr, expr.rowNr, "Type inference strangely encountered unknown expression.")
        return False



