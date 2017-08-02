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

public class ASTFunctionCallStatement extends ASTStatement {
    public String functionIdentifier;
    public ArrayList<ASTExpr> args;

    public ASTFunctionCallStatement(String functionIdentifier, ArrayList<ASTExpr> args) {
        this.functionIdentifier = functionIdentifier;
        this.args = args;
    }

    public void print() {
        System.out.print(functionIdentifier + "(");
        for (ASTExpr arg : args) {
            arg.print();
            System.out.print(", ");
        }
        System.out.println(");");
    }

    public boolean typecheck(
        Dictionary<String, TypeSignature> globalFunTable, 
        Dictionary<String, TypeAnnotation> globalSymTable, 
        Dictionary<String, TypeAnnotation> localSymTable,
        ASTType returnTypeOrNull
    ) {

        for (ASTExpr arg : args) {
            boolean success = arg.inferType(globalFunTable, globalSymTable, localSymTable);
            
            if (!success) {
                return false;
            }            
        } 

        if (functionIdentifier.equals("print")) {
    
            if (args.size() != 1) {
                System.out.println("Calling 'print' with wrong number of arguments!");
                return false;
            }

            return true;

        } else {    

            TypeSignature myTypeSignature = globalFunTable.get(functionIdentifier);

            if (myTypeSignature == null) {
                System.out.println("ASTFunctionCallStatement : Could not find function \"" + functionIdentifier + "\" in global function table!");
                return false;
            }

            if (args.size() != myTypeSignature.argTypeAnnotations.size()) {
                System.out.println("ASTFunctionCallStatement : Function call argument list length mismatch in call to \"" + functionIdentifier + "\"!");
                return false;
            }
        
            int counter = 0;
            for (ASTExpr arg : args) {
                

                if (!arg.inferredType.identityEquals(myTypeSignature.argTypeAnnotations.get(counter).theType)) {
                    System.out.println("ASTFunctionCallStatement : Type signature mismatch in call to function \"" + functionIdentifier + "\"!");    
                    return false;
                }
                counter++;
            }

            if (!(myTypeSignature.returnTypeAnnotationOrNull == null)) {
                System.out.println("ASTFunctionCallStatement : Using non-void function \"" + functionIdentifier + "\" as a statement!");
                return false; // statements must not have a return type    
            }

            return true;  

        }       
    }





    public boolean typecheck(Dictionary<String, TypeSignature> globalFunTable, Dictionary<String, TypeAnnotation> globalSymTable) {
        System.out.println("Typechecking function call statement!");
            

        for (ASTExpr arg : args) {
            boolean success = arg.inferType(globalFunTable, globalSymTable);
            
            if (!success) {
                return false;
            }            
        } 

        if (functionIdentifier.equals("print")) {
    
            if (args.size() != 1) {
                System.out.println("Calling 'print' with wrong number of arguments!");
                return false;
            }

            return true;

        } else {  

            TypeSignature myTypeSignature = globalFunTable.get(functionIdentifier);

            if (myTypeSignature == null) {
                System.out.println("ASTFunctionCallStatement : Could not find function \"" + functionIdentifier + "\" in global function table!");
                return false;
            }
        
            if (args.size() != myTypeSignature.argTypeAnnotations.size()) {
                System.out.println("ASTFunctionCallStatement : Function call argument list length mismatch in call to \"" + functionIdentifier + "\"!");
                return false;
            }

            int counter = 0;
            for (ASTExpr arg : args) {

                if (!arg.inferredType.identityEquals(myTypeSignature.argTypeAnnotations.get(counter).theType)) {
                    System.out.println("ASTFunctionCallStatement : Type signature mismatch in call to function \"" + functionIdentifier + "\"!");
                    return false;
                }
                counter++;
            }

            if (!(myTypeSignature.returnTypeAnnotationOrNull == null)) {
                System.out.println("ASTFunctionCall : Using non-void function \"" + functionIdentifier + "\" as a statement!");
                return false; // statements must not have a return type    
            }

            return true;  

        }
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
