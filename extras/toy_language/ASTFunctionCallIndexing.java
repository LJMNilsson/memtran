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

public class ASTFunctionCallIndexing extends ASTExpr {

    public ASTFunctionCall functionCall;
    public ArrayList<ASTExpr> indexings; // always more than zero


    public ASTFunctionCallIndexing(ASTFunctionCall functionCall, ArrayList<ASTExpr> indexings) {
        this.functionCall = functionCall;
        this.indexings = indexings;
    }

    public void print() {
        functionCall.print();
        for (ASTExpr indexing : indexings) {
            System.out.print("[");
            indexing.print();
            System.out.print("]");
        }
    }

    public boolean inferType(Dictionary<String, TypeSignature> globalFunTable, Dictionary<String, TypeAnnotation> globalSymTable, Dictionary<String, TypeAnnotation> localSymTable) {

        boolean success2 = functionCall.inferType(globalFunTable, globalSymTable, localSymTable);

        if (!success2) {
            return false;
        }

        ASTType type = functionCall.inferredType;

        for (int i = 0; i < indexings.size(); i++) {
            boolean success = indexings.get(i).inferType(globalFunTable, globalSymTable, localSymTable);

            if (!success) {
                return false;
            }

            if (!indexings.get(i).inferredType.isInt()) {
                System.out.println("ASTIndexing: Index to function call is not an Int!");
                return false;
            }


            if (type.isArrayType()) {
                type = ((ASTArrayType) type).constituentType;
            } else {
                System.out.println("ASTIndexing: Could not index this identifier as required.");
                return false;
            }
        }
    
        inferredType = type; 
        return true;        
    }

    public boolean inferType(Dictionary<String, TypeSignature> globalFunTable, Dictionary<String, TypeAnnotation> globalSymTable) {
         
        boolean success2 = functionCall.inferType(globalFunTable, globalSymTable);

        if (!success2) {
            return false;
        }

        ASTType type = functionCall.inferredType;

        for (int i = 0; i < indexings.size(); i++) {
            boolean success = indexings.get(i).inferType(globalFunTable, globalSymTable);

            if (!success) {
                return false;
            }

            if (!indexings.get(i).inferredType.isInt()) {
                System.out.println("ASTIndexing: Index to function call is not an Int!");
                return false;
            }

            if (type.isArrayType()) {
                type = ((ASTArrayType) type).constituentType;
            } else {
                System.out.println("ASTIndexing: Could not index this identifier as required.");
                return false;
            }
        }
    
        inferredType = type; 
        return true;  
    }

    public void generateGlobalIR(
        ArrayList<IRInstruction> instructions, 
        Dictionary<String, TypeSignature> globalFunctionTable,
        Dictionary<String, TypeAnnotation> globalSymTable,
        ArrayList<String> slotsMarkedForDestruction,
        AnonNameGenerator anongen,
        String returnValueHolder
    ) {

        // dummy -- should be transform-eliminated by this time

        

    }    
}
