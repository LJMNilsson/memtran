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


def run_pass(programAST):

    return EndExpander().visit(programAST)
  





class EndExpander(AbstractASTExpressionVisitor):

    def __init__(self):
        self.expanderExpression = None

    def visit_expression(self, node):

        if isinstance(node, NEndExpression):

            if self.expanderExpression is None:

                util.logError(node.lineNr, node.rowNr, "Using 'end' outside an array indexing.")
                return False
                
            else:
                node.expansion = self.expanderExpression.create_copy()       
                return True

        elif isinstance(node, NArrayIndexing): 

            success = self.visit(node.arrayExpression)
            if not success:            
                return False

            minusIdentifier = NIdentifier(node.arrayExpression.lineNr, node.arrayExpression.rowNr, "-")

            minusIdentifierExpression = NIdentifierExpression(node.arrayExpression.lineNr, node.arrayExpression.rowNr, None, minusIdentifier, [])

            lenIdentifier = NIdentifier(node.arrayExpression.lineNr, node.arrayExpression.rowNr, "len")

            lenIdentifierExpression = NIdentifierExpression(node.arrayExpression.lineNr, node.arrayExpression.rowNr, None, lenIdentifier, [])

            lenFunctionCall = NFunctionCall(
                node.arrayExpression.lineNr,
                node.arrayExpression.rowNr,
                lenIdentifierExpression,
                [node.arrayExpression.create_copy()]
            )

            newExpandExpression = NFunctionCall(
                node.arrayExpression.lineNr, 
                node.arrayExpression.rowNr,
                minusIdentifierExpression,
                [lenFunctionCall, NIntegerExpression(node.arrayExpression.lineNr, node.arrayExpression.rowNr, "1", False)] 
            )

            prevExpander = self.expanderExpression
            self.expanderExpression = newExpandExpression
            success = self.visit(node.indexExpression)
            if not success:
                return False
            self.expanderExpression = prevExpander
           
        elif isinstance(node, NIdentifierExpression):

            accumulatedIndexing = NIdentifierExpression(node.lineNr, node.rowNr, node.moduleNameOrNull, node.name, [])   # lineNr, rowNr wrong here...

            for indexing in node.indexings:

                if isinstance(indexing, NArrayIndexingIndex):

                    minusIdentifier = NIdentifier(accumulatedIndexing.lineNr, accumulatedIndexing.rowNr, "-")

                    minusIdentifierExpression = NIdentifierExpression(accumulatedIndexing.lineNr, accumulatedIndexing.rowNr, None, minusIdentifier, [])

                    lenIdentifier = NIdentifier(accumulatedIndexing.lineNr, accumulatedIndexing.rowNr, "len")

                    lenIdentifierExpression = NIdentifierExpression(accumulatedIndexing.lineNr, accumulatedIndexing.rowNr, None, lenIdentifier, [])

                    lenFunctionCall = NFunctionCall(
                        accumulatedIndexing.lineNr,
                        accumulatedIndexing.rowNr,
                        lenIdentifierExpression,
                        [accumulatedIndexing.create_copy()]
                    )

                    newExpandExpression = NFunctionCall(
                        accumulatedIndexing.lineNr, 
                        accumulatedIndexing.rowNr,
                        minusIdentifierExpression,
                        [lenFunctionCall, NIntegerExpression(accumulatedIndexing.lineNr, accumulatedIndexing.rowNr, "1", False)] 
                    )

                    prevExpander = self.expanderExpression
                    self.expanderExpression = newExpandExpression
                    success = self.visit(indexing.indexExpression)
                    if not success:
                        return False
                    self.expanderExpression = prevExpander

                    accumulatedIndexing.indexings.append(indexing)
              
                else:

                    accumulatedIndexing.indexings.append(indexing)  

        else:
            success = node.visit_children(self)
            if success == False:
                return False

            return True













 
        
