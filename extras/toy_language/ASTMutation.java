// Copyright (C) 2017 Martin Nilsson


// This file is part of the Memtran compiler.
//
//     The Memtran compiler is free software: you can redistribute it and/or modify
//     it under the terms of the GNU General Public License as published by
//     the Free Software Foundation, either version 3 of the License, or
//     (at your option) any later version.
// 
//     The Memtran compiler is distributed in the hope that it will be useful,
//     but WITHOUT ANY WARRANTY; without even the implied warranty of
//     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//     GNU General Public License for more details.
// 
//     You should have received a copy of the GNU General Public License
//     along with the Memtran compiler.  If not, see http://www.gnu.org/licenses/ . 




import java.util.*;

public class ASTMutation extends ASTStatement {
    ASTIndexing varIndexing;
    ASTExpr expr;

    public ASTMutation(ASTIndexing varIndexing, ASTExpr expr) {
        this.varIndexing = varIndexing;
        this.expr = expr;
    }

    public void print() {
        varIndexing.print();
        System.out.print(" = ");
        expr.print();
        System.out.println(";");
    }

    public boolean typecheck(
        Dictionary<String, TypeSignature> globalFunTable, 
        Dictionary<String, TypeAnnotation> globalSymTable, 
        Dictionary<String, TypeAnnotation> localSymTable,
        ASTType returnTypeOrNull
    ) {
        TypeAnnotation myTypeAnnotation = localSymTable.get(varIndexing.identifier);

        if (myTypeAnnotation == null) {
            myTypeAnnotation = globalSymTable.get(varIndexing.identifier);

            if (myTypeAnnotation == null) {

                System.out.println("ASTMutation: Could not find slot to be mutated in local or global symtable!");
                return false;
            }
        }

        if (myTypeAnnotation.isCompletelyImmutable) {
            return false;
        }

        boolean typeInferenceOfExprPassed = expr.inferType(globalFunTable, globalSymTable);

        if (!typeInferenceOfExprPassed) {
            return false;
        }

        if (!expr.inferredType.identityEquals(myTypeAnnotation.theType)) {
            return false;
        }


        return true;    
    }

    public boolean typecheck(Dictionary<String, TypeSignature> globalFunTable, Dictionary<String, TypeAnnotation> globalSymTable) {

        TypeAnnotation myTypeAnnotation = globalSymTable.get(varIndexing.identifier);

        if (myTypeAnnotation == null) {
            System.out.println("ASTMutation: Could not find slot to be mutated in global symtable!");
            return false;
        }

        if (myTypeAnnotation.isCompletelyImmutable) {
            return false;
        }
 
        boolean typeInferenceOfExprPassed = expr.inferType(globalFunTable, globalSymTable);

        if (!typeInferenceOfExprPassed) {
            return false;
        }

        if (!expr.inferredType.identityEquals(myTypeAnnotation.theType)) {
            return false;
        }

        return true;    
    }

    public void generateGlobalIR(
        ArrayList<IRInstruction> instructions, 
        Dictionary<String, TypeSignature> globalFunctionTable,
        Dictionary<String, TypeAnnotation> globalSymTable,
        ArrayList<String> slotsMarkedForDestruction,
        AnonNameGenerator anongen
    ) {
        // TODO
    }
}
