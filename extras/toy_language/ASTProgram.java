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

public class ASTProgram {

    public ArrayList<ASTFunctionDefinition> functionDefinitions;

    public ArrayList<ASTStatement> main;

    public ASTProgram(ArrayList<ASTFunctionDefinition> functionDefinitions, ArrayList<ASTStatement> main) {
        this.functionDefinitions = functionDefinitions;
        this.main = main;
    }

    public void print() {
        System.out.println(" ");

        for (ASTStatement statement : main) {
            statement.print();
        }

        System.out.println(" ");

        for (ASTFunctionDefinition funDef : functionDefinitions) {
            funDef.print();
        }
    }

    /** 
        Only does type annotation so far, no checking...
    */
    public boolean typecheck(Dictionary<String, TypeSignature> globalFunTable, Dictionary<String, TypeAnnotation> globalSymTable) {

        // first, collect all function names...

        for (ASTFunctionDefinition funDef : functionDefinitions) {

            ArrayList<TypeAnnotation> argTypeAnnotations = new ArrayList<TypeAnnotation>();
            ArrayList<Boolean> argConstructandStatuses = new ArrayList<Boolean>();
            
            funDef.localSymTable = new Hashtable<String, TypeAnnotation>();

            for (ASTParamDeclaration param : funDef.params) {
                TypeAnnotation typeAnnotation = param.calculateTypeAnnotation();

                argTypeAnnotations.add(typeAnnotation);
                argConstructandStatuses.add(param.isConstructand);

                if (funDef.localSymTable.get(param.paramName) == null) {
                    funDef.localSymTable.put(param.paramName, typeAnnotation);
                } else {
                    System.out.println("Redefining parameter '" + param.paramName + "'!");
                    return false;
                }            
            }

            TypeAnnotation returnTypeAnnotationOrNull = null;

            if (funDef.returnTypeOrNull != null) {
                
                returnTypeAnnotationOrNull = new TypeAnnotation(funDef.returnTypeOrNull, true);
            }
            

            TypeSignature myTypeSignature = new TypeSignature(argTypeAnnotations, argConstructandStatuses, returnTypeAnnotationOrNull);

            if (globalFunTable.get(funDef.functionName) == null) {
                globalFunTable.put(funDef.functionName, myTypeSignature);
            } else {
                System.out.println("Redefining function '" + funDef.functionName + "'!");
                return false;
            }
        }
        

        // it's a simplification to do the global statements first, remember this for real compiler
        for (ASTStatement statement : main) {
            boolean success = statement.typecheck(globalFunTable, globalSymTable);

            if (!success) {
                return false;
            }
        }
 
        for (ASTFunctionDefinition funDef : functionDefinitions) {
             boolean success = funDef.typecheck(globalFunTable, globalSymTable);  // it needs the global symtable too, but builds its own too 
            
             if (!success) {
                return false;
             }  
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

        // TODO: generate the function definitions IR


        for (ASTStatement statement : main) {
             statement.generateGlobalIR(
                instructions, 
                globalFunctionTable,
                globalSymTable,
                slotsMarkedForDestruction,
                anongen
            );
        }
    }

}
