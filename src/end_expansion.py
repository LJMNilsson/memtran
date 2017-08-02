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




from ast import *










# Note: since the functionality of this pass does depend on where we are in the tree as concerning parent nodes,
# this pass does not utilize the visitor pattern functionality that exists on the ast module.



def _expand_expression(expr, expanderExpression):

    if isinstance(expr, NCONTENTTYPEExpression):

        success = _expand_expression(expr.switchValue, expanderExpression)
        if not success:
            return False

        for case in expr.cases:
            success = _expand_expression(case.value, expanderExpression)
            if not success:
                return False

        if not expr.defaultCaseOrNull is None:
            success = _expand_expression(expr.defaultCaseOrNull, expanderExpression)
            if not success:
                return False

    elif isinstance(expr, NSWITCHExpression):

        success = _expand_expression(expr.switchValue, expanderExpression)
        if not success:
            return False

        for case in expr.cases:
            for caseValue in case.caseValues:
                success = _expand_expression(caseValue, expanderExpression)
                if not success:
                    return False

            success = _expand_expression(case.value, expanderExpression)
            if not success:
                return False

        if not expr.defaultCaseOrNull is None:
            success = _expand_expression(expr.defaultCaseOrNull, expanderExpression)
            if not success:
                return False

    elif isinstance(expr, NIFExpression):

        success = _expand_expression(expr.condition, expanderExpression)
        if not success:
            return False

        success = _expand_expression(expr.thenExpression, expanderExpression)
        if not success:
            return False    

        success = _expand_expression(expr.elseExpression, expanderExpression)
        if not success:
            return False

    elif isinstance(expr, NFunctionCall):

        success = _expand_expression(expr.functionExpression, expanderExpression)
        if not success:
            return False
        
        for arg in expr.args:
            if type(arg) is NNormalArg:

                success = _expand_expression(arg.argExpression, expanderExpression)
                if not success:
                    return False

            else: # NRefArg hopefully

                success = _expand_expression(arg.lValueContainer.lValueExpression, expanderExpression)
                if not success:
                    return False

    elif isinstance(expr, NEndExpression):

        # here we do the real work...

        if expanderExpression is None:

            util.logError(expr.lineNr, expr.rowNr, "Using 'end' outside an array indexing.")
            return False
            
        else:
            expr.expansion = expanderExpression.create_copy()

    elif isinstance(expr, NAndSymbolExpression) or isinstance(expr, NOrSymbolExpression):

        success = _expand_expression(expr.leftExpression, expanderExpression)
        if not success:
            return False

        success = _expand_expression(expr.rightExpression, expanderExpression)    
        if not success:
            return False

    elif isinstance(expr, NVariantBoxCastExpression):

        success = _expand_expression(expr.expression, expanderExpression)
        if not success:
            return False


    elif isinstance(expr, NStructIndexing):

        success = _expand_expression(expr.structExpression, expanderExpression)
        if not success:
            return False

    elif isinstance(expr, NArrayIndexing):

        success = _expand_expression(expr.arrayExpression, expanderExpression)
        if not success:            
            return False

        minusIdentifier = NIdentifier(expr.arrayExpression.lineNr, expr.arrayExpression.rowNr, "-")

        minusIdentifierExpression = NIdentifierExpression(expr.arrayExpression.lineNr, expr.arrayExpression.rowNr, None, minusIdentifier, [])

        lenIdentifier = NIdentifier(expr.arrayExpression.lineNr, expr.arrayExpression.rowNr, "len")

        lenIdentifierExpression = NIdentifierExpression(expr.arrayExpression.lineNr, expr.arrayExpression.rowNr, None, lenIdentifier, [])

        lenFunctionCall = NFunctionCall(
            expr.arrayExpression.lineNr,
            expr.arrayExpression.rowNr,
            lenIdentifierExpression,
            [expr.arrayExpression]
        )

        newExpandExpression = NFunctionCall(
            expr.arrayExpression.lineNr, 
            expr.arrayExpression.rowNr,
            minusIdentifierExpression,
            [lenFunctionCall, NIntegerExpression(expr.arrayExpression.lineNr, expr.arrayExpression.rowNr, "1", False)] 
        )

        success = _expand_expression(expr.indexExpression, newExpandExpression)
        if not success:
            return False

    elif isinstance(expr, NTypeClarifiedExpression):

        success = _expand_expression(expr.expression, expanderExpression)
        if not success:
            return False

    elif isinstance(expr, NVariantBoxExpression):

        success = _expand_expression(expr.expression, expanderExpression)
        if not success:
            return False
     
    elif isinstance(expr, NStructExpression):

        for post in expr.posts:
            success = _expand_expression(post.value, expanderExpression)
            if not success:
                return False

    elif isinstance(expr, NArrayExpressionRepeatedValue):

        success = _expand_expression(expr.repeatedValue, expanderExpression)
        if not success:
            return False

        success = _expand_expression(expr.length, expanderExpression)
        if not success:
            return False

    elif isinstance(expr, NArrayExpressionNoInitialization):

        success = _expand_expression(expr.length, expanderExpression)
        if not success:
            return False

    elif isinstance(expr, NArrayExpressionIndividualValues):

        for value in expr.values:
            success = _expand_expression(value, expanderExpression)
            if not success:
                return False       
    
    elif isinstance(expr, NIdentifierExpression):

        accumulatedIndexing = NIdentifierExpression(expr.lineNr, expr.rowNr, expr.moduleNameOrNull, expr.name, [])   # lineNr, rowNr wrong here...

        for indexing in expr.indexings:

            if isinstance(indexing, NArrayIndexingIndex):

                minusIdentifier = NIdentifier(accumulatedIndexing.lineNr, accumulatedIndexing.rowNr, "-")

                minusIdentifierExpression = NIdentifierExpression(accumulatedIndexing.lineNr, accumulatedIndexing.rowNr, None, minusIdentifier, [])

                lenIdentifier = NIdentifier(accumulatedIndexing.lineNr, accumulatedIndexing.rowNr, "len")

                lenIdentifierExpression = NIdentifierExpression(accumulatedIndexing.lineNr, accumulatedIndexing.rowNr, None, lenIdentifier, [])

                lenFunctionCall = NFunctionCall(
                    accumulatedIndexing.lineNr,
                    accumulatedIndexing.rowNr,
                    lenIdentifierExpression,
                    [accumulatedIndexing]
                )

                newExpandExpression = NFunctionCall(
                    accumulatedIndexing.lineNr, 
                    accumulatedIndexing.rowNr,
                    minusIdentifierExpression,
                    [lenFunctionCall, NIntegerExpression(accumulatedIndexing.lineNr, accumulatedIndexing.rowNr, "1", False)] 
                )

                success = _expand_expression(indexing.indexExpression, newExpandExpression)
                if not success:
                    return False

                accumulatedIndexing.indexings.append(indexing)
          
            else:

                accumulatedIndexing.indexings.append(indexing)    

    else:    
        pass

    return True




def _expand_block(b):

    for statement in b.statements:
        success = _expand_statement(statement)
        if not success:
            return False

    return True







def _expand_statement(statement):

    if isinstance(statement, NContenttypeStatement):
        
        success = _expand_expression(statement.switchValue, None)
        if not success:
            return False
    
        for case in statement.cases:
            success = _expand_block(case.block)
            if not success:
                return False

        if not statement.defaultCaseOrNull is None:                
            success = _expand_block(statement.defaultCaseOrNull)
            if not success:
                return False

    elif isinstance(statement, NSwitchStatement):

        success = _expand_expression(statement.switchValue, None)
        if not success:
            return False

        for case in statement.cases:

            for caseValue in case.caseValues:
                success = _expand_expression(caseValue, None)
                if not success:
                    return False
    
            success = _expand_block(case.block)
            if not success:
                return False

        if not statement.defaultCaseOrNull is None:
            success = _expand_block(statement.defaultCaseOrNull)
            if not success:
                return False

    elif isinstance(statement, NReturnStatement):

        for retExpr in statement.returnExpressions:
            success = _expand_expression(retExpr, None)
            if not success:
                return False

    elif isinstance(statement, NFunctionCallStatement):

        success = _expand_expression(statement.functionCall, None)
        if not success:
            return False

    elif isinstance(statement, NForStatement):

        if not statement.rangeOrNull is None:

            success = _expand_expression(statement.rangeOrNull.rangeFrom, None)
            if not success:
                return False

            success = _expand_expression(statement.rangeOrNull.rangeTo, None)
            if not success:
                return False

        for iteration in statement.iterations:
            
            if isinstance(iteration, NIterationIn):

                success = _expand_expression(iteration.arrayExpression, None)
                if not success:
                    return False
                
                if not iteration.indexfactorOrNull is None:
                    success = _expand_expression(iteration.indexfactorOrNull, None)
                    if not success:
                        return False

                if not iteration.indexoffsetOrNull is None:
                    success = _expand_expression(iteration.indexOffsetOrNull, None)
                    if not success:
                        return False
                            
            else:  # NIterationOver hopefully

                success = _expand_expression(iteration.arrayLValue.lValueExpression, None)
                if not success:
                    return False

                if not iteration.indexfactorOrNull is None:
                    success = _expand_expression(iteration.indexfactorOrNull, None)
                    if not success:
                        return False

                if not iteration.indexoffsetOrNull is None:
                    success = _expand_expression(iteration.indexOffsetOrNull, None)
                    if not success:
                        return False


        success = _expand_block(statement.block)
        if not success:
            return False

    elif isinstance(statement, NLoopStatement):

        success = _expand_block(statement.block)
        if not success:
            return False

    elif (isinstance(statement, NDivisionAssignment) or 
        isinstance(statement, NMultiplicationAssignment) or
        isinstance(statement, NSubtractionAssignment) or
        isinstance(statement, NAdditionAssignment) or
        isinstance(statement, NModuloAssignment) 
    ):

        for lhsItem in statement.leftHandSide:
            success = _expand_expression(lhsItem.lValueExpression, None)
            if not success:
                return False

        success = _expand_expression(statement.value, None)
        if not success:
            return False

    elif isinstance(statement, NNormalAssignment):

        for lhsItem in statement.leftHandSide:

            if type(lhsItem) is NVariableDeclaration:

                pass

            else:  # NLValueContainer hopefully

                success = _expand_expression(lhsItem.lValueExpression, None)
                if not success:
                    return False

        success = _expand_expression(statement.value, None)
        if not success:
            return False

    elif isinstance(statement, NRefToTemplateDeclarationWithDefinition):

        success = _expand_block(statement.templates[statement.templatesIndex].body)
        if not success:
            return False

    elif isinstance(statement, NRefToFunctionDeclarationWithDefinition):

        success = _expand_block(statement.funs[statement.funsIndex].body)
        if not success:
            return False

    elif isinstance(statement, NIfStatement):

        success = _expand_expression(statement.condition, None)
        if not success:
            return False

        success = _expand_block(statement.ifBlock)
        if not success:
            return False

        for elseIfClause in statement.elseIfClauses:
            success = _expand_expression(elseIfClause.condition, None)
            if not success:
                return False

            success = _expand_block(elseIfClause.block)
            if not success:
                return False

        if not statement.elseBlockOrNull is None:
            success = _expand_block(statement.elseBlockOrNull)
            if not success:
                return False

    else:
        pass   
    

    return True







def run_pass(program_ast):

    for statement in program_ast.statements:
        success = _expand_statement(statement) 
        if not success:
            return False

    return True  
        
