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

public class ASTReturnStatement extends ASTStatement {
    public ASTExpr exprOrNull;

    public ASTReturnStatement(ASTExpr exprOrNull) {

        this.exprOrNull = exprOrNull;
    }

    public void print() {
        System.out.print("return");
        if (exprOrNull != null) {
            System.out.print(" ");
            exprOrNull.print(); 
        }
        System.out.println(";");
    }

    public boolean typecheck(
        Dictionary<String, TypeSignature> globalFunTable, 
        Dictionary<String, TypeAnnotation> globalSymTable, 
        Dictionary<String, TypeAnnotation> localSymTable,
        ASTType returnTypeOrNull
    ) {

        System.out.println("Typechecking return statement.");

        if (exprOrNull == null) {

            System.out.println("exprOrNull == null");

            if (returnTypeOrNull == null) {
                return true;
            } else {
                return false;
            }

        } else {

            System.out.println("exprOrNull != null");

            if (returnTypeOrNull == null) {
                return false;
            } else {

                boolean typeInferenceOfExprPassed = exprOrNull.inferType(globalFunTable, globalSymTable, localSymTable);

                if (!typeInferenceOfExprPassed) {
                    return false;
                }

                ASTType exprInferredType = exprOrNull.inferredType;

                if (exprInferredType.identityEquals(returnTypeOrNull)) {
                    return true;
                } else {
                    return false;
                }   
            }
        }

    }

    public boolean typecheck(Dictionary<String, TypeSignature> globalFunTable, Dictionary<String, TypeAnnotation> globalSymTable) {
        System.out.println("ASTReturnStatement: Cannot use return statement outside a function definition!");
        return false;
    } 

    public void generateGlobalIR(
        ArrayList<IRInstruction> instructions, 
        Dictionary<String, TypeSignature> globalFunctionTable,
        Dictionary<String, TypeAnnotation> globalSymTable,
        ArrayList<String> slotsMarkedForDestruction,
        AnonNameGenerator anongen
    ) {
        System.out.println("Return statement on global level not caught by typechecker!");
    }

}
