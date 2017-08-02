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





import java.util.Dictionary;
import java.util.ArrayList;

public class ASTInitialization extends ASTStatement {
    public boolean isMu;
    public String identifier;
    public ASTType type;
    public ASTExpr expr;

    public ASTInitialization(boolean isMu, String identifier, ASTType type, ASTExpr expr) {
        this.isMu = isMu;
        this.identifier = identifier;
        this.type = type;
        this.expr = expr;

    }

    public void print() {
        if (isMu) {System.out.print("mu ");}
        System.out.print(identifier + " : ");
        type.print();
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

        boolean isCompletelyImmutable = true;

        if (isMu) {
            isCompletelyImmutable = false;
        }

        TypeAnnotation myTypeAnnotation = new TypeAnnotation(type, isCompletelyImmutable);

        

        boolean pass = expr.inferType(globalFunTable, globalSymTable, localSymTable);

        if (!pass) {
            return false;
        }

        ASTType exprInferredType = expr.inferredType;

        if (localSymTable.get(identifier) == null) {
            localSymTable.put(identifier, myTypeAnnotation); // put it in here after, at the correct moment
        } else {
            System.out.println("Redefining local variable '" + identifier + "'!");
            return false;
        }

        if (type.identityEquals(exprInferredType)) {
            return true;
        } else {
            return false;
        }

    }

    public boolean typecheck(Dictionary<String, TypeSignature> globalFunTable, Dictionary<String, TypeAnnotation> globalSymTable) {

        System.out.println("Typechecking initialization!");

        boolean isCompletelyImmutable = true;

        if (isMu) {
            isCompletelyImmutable = false;
        }

        TypeAnnotation myTypeAnnotation = new TypeAnnotation(type, isCompletelyImmutable);

        boolean pass = expr.inferType(globalFunTable, globalSymTable);

        if (!pass) {
            return false;
        }

        ASTType exprInferredType = expr.inferredType;

        if (globalSymTable.get(identifier) == null) {
            globalSymTable.put(identifier, myTypeAnnotation); // put it in here after, at the correct moment
        } else {
            System.out.println("Redefining global variable '" + identifier + "'!");
            return false;
        }

        if (type.identityEquals(exprInferredType)) {
            return true;
        } else {
            System.out.println("ASTInitialization: Type mismatch.");
            return false;
        }

    }

    public void generateGlobalIR(
        ArrayList<IRInstruction> instructions, 
        Dictionary<String, TypeSignature> globalFunctionTable,
        Dictionary<String, TypeAnnotation> globalSymTable,
        ArrayList<String> slotsMarkedForDestruction,
        AnonNameGenerator anongen
    ) {

/*  

POSSIBLE GLOBAL CASES: 12 cases.

Type        Provider                                Receiver                            
-------------------------------------------------------------------------------
Array       immutable global var indexing           immutable global var                

Array       immutable global var indexing           mutable global var                  

Array       return slot indexing                    immutable global var        

Array       return slot indexing                    mutable global var

Array       mutable global var indexing             immutable global var

Array       mutable global var indexing             mutable global var

Int         immutable global var indexing           immutable global var                

Int         immutable global var indexing           mutable global var                  

Int         return slot indexing                    immutable global var    OBSERVE. GHOST SYSTEM: ON RETURN        

Int         return slot indexing                    mutable global var      OBSERVE. GHOST SYSTEM: ON RETURN

Int         mutable global var indexing             immutable global var

Int         mutable global var indexing             mutable global var


*/




        if (type.isArrayType()) {

            slotsMarkedForDestruction.add(identifier);

            if (expr instanceof ASTIndexing) { // Four cases here

                ASTIndexing exprCasted = (ASTIndexing) expr;

                TypeAnnotation indexingVarTypeAnnotation = globalSymTable.get(exprCasted.identifier); // should be there

                if (indexingVarTypeAnnotation.isCompletelyImmutable) { // immutable provider; two cases here

                    if (isMu) { // type: array; provider: immutable global var, receiver: mutable global var

                        String indexResultHolder = "%" + anongen.generate();

                        exprCasted.generateGlobalIR( // follows it to the final indexing, and checks bounds...
                            instructions, globalFunctionTable, globalSymTable,
                            slotsMarkedForDestruction,
                            anongen,
                            indexResultHolder
                        );

                        int depth = 0;
                            
                        ASTType recurseType = exprCasted.inferredType;

                        while (true) {
                            if (recurseType.isArrayType()) {
                                depth++;
                                recurseType = ((ASTArrayType) recurseType).constituentType;

                            } else {
                                break;
                            }
                    
                        }

                        String resultHolder = "%" + anongen.generate();

                        instructions.add(new IRWholeTreeCopyUnflagged(resultHolder, new IRRegArrayHead(indexResultHolder), depth));

                        String name = "@" + identifier;
                        instructions.add(new IRAlloca(name));
                        instructions.add(new IRStoreInt(new IRRegStackAddress(name), new IRRegInt(resultHolder)));

                    } else { // type: array; provider: immutable global var, receiver: immutable global var

                        String indexResultHolder = "%" + anongen.generate();

                        exprCasted.generateGlobalIR( // follows it to the final indexing
                            instructions, globalFunctionTable, globalSymTable,
                            slotsMarkedForDestruction,
                            anongen,
                            indexResultHolder
                        );

                        

                        instructions.add(new IRCopyHead("@" + identifier, new IRRegArrayHead(indexResultHolder)));

                        

                    }

                } else { // mutable provider; two cases here

                    if (isMu) { // type: array; provider: mutable global var, receiver: mutable global var

                        String indexResultHolder = "%" + anongen.generate();

                        exprCasted.generateGlobalIR( // follows it to the final indexing, and checks bounds...
                            instructions, globalFunctionTable, globalSymTable,
                            slotsMarkedForDestruction,
                            anongen,
                            indexResultHolder
                        );

                        int depth = 0;
                            
                        ASTType recurseType = exprCasted.inferredType;

                        while (true) {
                            if (recurseType.isArrayType()) {
                                depth++;
                                recurseType = ((ASTArrayType) recurseType).constituentType;

                            } else {
                                break;
                            }
                    
                        }

                        String resultHolder = "%" + anongen.generate();

                        instructions.add(new IRWholeTreeCopyUnflagged(resultHolder, new IRRegArrayHead(indexResultHolder), depth));

                        String name = "@" + identifier;
                        instructions.add(new IRAlloca(name));
                        instructions.add(new IRStoreInt(new IRRegStackAddress(name), new IRRegInt(resultHolder)));

                    } else { // type: array; provider: mutable global var, receiver: immutable global var

                        String indexResultHolder = "%" + anongen.generate();

                        exprCasted.generateGlobalIR( // follows it to the final indexing, and checks bounds...
                            instructions, globalFunctionTable, globalSymTable,
                            slotsMarkedForDestruction,
                            anongen,
                            indexResultHolder
                        );

                        int depth = 0;
                            
                        ASTType recurseType = exprCasted.inferredType;

                        while (true) {
                            if (recurseType.isArrayType()) {
                                depth++;
                                recurseType = ((ASTArrayType) recurseType).constituentType;

                            } else {
                                break;
                            }
                    
                        }

                        

                        instructions.add(new IRWholeTreeCopy("@" + identifier, new IRRegArrayHead(indexResultHolder), depth));

                        
                    }

                }


            } else if (expr instanceof ASTFunctionCall) { // Two cases here

                if (isMu) { // type: array; provider: return slot (indexings have been eliminated by transform pass), receiver: mutable global var

                    

                    ASTFunctionCall exprCasted = (ASTFunctionCall) expr;

                    
               

                    String resultHolder = "%" + anongen.generate();

                    exprCasted.generateGlobalIR( 
                            instructions, globalFunctionTable, globalSymTable,
                            slotsMarkedForDestruction,
                            anongen,
                            resultHolder
                    );






                    for (ASTExpr arg : exprCasted.args) {
                        if (arg instanceof ASTIndexing) {

                            ASTIndexing argCasted = (ASTIndexing) arg;

                            TypeAnnotation argAnnotation = globalSymTable.get(argCasted.identifier); // should be found there
                
                            if (argAnnotation.theType.isArrayType() && (!argAnnotation.isCompletelyImmutable)) {

                                String headHolder = "%" + anongen.generate();
                            
                                instructions.add(new IRLoadArrayHead(headHolder, new IRRegStackAddress("@" + argCasted.identifier)));
                               

                                instructions.add(new IRCheckForGhostAndDestructThoseRecursivelyIfSo(new IRRegArrayHead(headHolder)));
                                instructions.add(new IRUnghostflagTree(new IRRegArrayHead(headHolder)));     

                            }

                        }
                    }

                    instructions.add(new IRUnghostflagTree(new IRRegArrayHead(resultHolder)));                   


                    String name = "@" + identifier;
                    instructions.add(new IRAlloca(name));
                    instructions.add(new IRStoreArrayHead(new IRRegStackAddress(name), new IRRegArrayHead(resultHolder)));

                } else { // type: array; provider: return slot (any indexings have been eliminated by transform pass), receiver: mutable global var   

                    ASTFunctionCall exprCasted = (ASTFunctionCall) expr;

                    String name = "@" + identifier;

                    exprCasted.generateGlobalIR( 
                            instructions, globalFunctionTable, globalSymTable,
                            slotsMarkedForDestruction,
                            anongen,
                            name
                    );

                    for (ASTExpr arg : exprCasted.args) {
                        if (arg instanceof ASTIndexing) {

                            ASTIndexing argCasted = (ASTIndexing) arg;

                            TypeAnnotation argAnnotation = globalSymTable.get(argCasted.identifier); // should be found there
                
                            if (argAnnotation.theType.isArrayType() && (!argAnnotation.isCompletelyImmutable)) {

                                String headHolder = "%" + anongen.generate();
                            
                                instructions.add(new IRLoadArrayHead(headHolder, new IRRegStackAddress("@" + argCasted.identifier)));
                               

                                instructions.add(new IRCheckForGhostAndDestructThoseRecursivelyIfSo(new IRRegArrayHead(headHolder)));
                                instructions.add(new IRUnghostflagTree(new IRRegArrayHead(headHolder)));     

                            }

                        }
                    }

                }

            } else if (expr instanceof ASTIntegerLiteral) { 

                System.out.println("Global IR generation ASTInitialization, type error: array = Int.");

            } else {

                System.out.println("Global IR generation ASTInitialization, unknown expression type!");

            }


        } else { // type is Int

            if (expr instanceof ASTIndexing) { 

                ASTIndexing exprCasted = (ASTIndexing) expr;

                

                if (isMu) {

                    String resultHolder = "%" + anongen.generate();

                    exprCasted.generateGlobalIR( // follows it to the final indexing, and checks bounds...
                        instructions, globalFunctionTable, globalSymTable,
                        slotsMarkedForDestruction,
                        anongen,
                        resultHolder
                    );

                    String name = "@" + identifier;
                    instructions.add(new IRAlloca(name));
                    instructions.add(new IRStoreInt(new IRRegStackAddress(name), new IRRegInt(resultHolder)));

                } else {

                    String name = "@" + identifier;

                    exprCasted.generateGlobalIR( // follows it to the final indexing, and checks bounds...
                        instructions, globalFunctionTable, globalSymTable,
                        slotsMarkedForDestruction,
                        anongen,
                        name
                    );       

                }

                

            } else if ((expr instanceof ASTFunctionCall) || (expr instanceof ASTIntegerLiteral)) { // Two cases here

                if (isMu) {

                    ASTFunctionCall exprCasted = (ASTFunctionCall) expr;

                    
               

                    String resultHolder = "%" + anongen.generate();

                    exprCasted.generateGlobalIR( 
                            instructions, globalFunctionTable, globalSymTable,
                            slotsMarkedForDestruction,
                            anongen,
                            resultHolder
                    );

                    for (ASTExpr arg : exprCasted.args) {
                        if (arg instanceof ASTIndexing) {

                            ASTIndexing argCasted = (ASTIndexing) arg;

                            TypeAnnotation argAnnotation = globalSymTable.get(argCasted.identifier); // should be found there
                
                            if (argAnnotation.theType.isArrayType() && (!argAnnotation.isCompletelyImmutable)) {

                                String headHolder = "%" + anongen.generate();
                            
                                instructions.add(new IRLoadArrayHead(headHolder, new IRRegStackAddress("@" + argCasted.identifier)));
                               

                                instructions.add(new IRCheckForGhostAndDestructThoseRecursivelyIfSo(new IRRegArrayHead(headHolder)));
                                instructions.add(new IRUnghostflagTree(new IRRegArrayHead(headHolder)));     

                            }

                        }
                    }

                                


                    String name = "@" + identifier;
                    instructions.add(new IRAlloca(name));
                    instructions.add(new IRStoreInt(new IRRegStackAddress(name), new IRRegInt(resultHolder)));

                } else {

                    ASTFunctionCall exprCasted = (ASTFunctionCall) expr;

                    String name = "@" + identifier;

                    exprCasted.generateGlobalIR( 
                            instructions, globalFunctionTable, globalSymTable,
                            slotsMarkedForDestruction,
                            anongen,
                            name
                    );

                    for (ASTExpr arg : exprCasted.args) {
                        if (arg instanceof ASTIndexing) {

                            ASTIndexing argCasted = (ASTIndexing) arg;

                            TypeAnnotation argAnnotation = globalSymTable.get(argCasted.identifier); // should be found there
                
                            if (argAnnotation.theType.isArrayType() && (!argAnnotation.isCompletelyImmutable)) {

                                String headHolder = "%" + anongen.generate();
                            
                                instructions.add(new IRLoadArrayHead(headHolder, new IRRegStackAddress("@" + argCasted.identifier)));
                               

                                instructions.add(new IRCheckForGhostAndDestructThoseRecursivelyIfSo(new IRRegArrayHead(headHolder)));
                                instructions.add(new IRUnghostflagTree(new IRRegArrayHead(headHolder)));     

                            }

                        }
                    }

                }

            } else {

                System.out.println("ASTInitialization IR generation: Unknown expression of Int type.");

            }

        }



    }    








}
