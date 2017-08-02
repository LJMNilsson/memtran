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

public class ASTFunctionCall extends ASTExpr {
    public String functionIdentifier;
    public ArrayList<ASTExpr> args;

    public ASTFunctionCall(String functionIdentifier, ArrayList<ASTExpr> args) {
        this.functionIdentifier = functionIdentifier;
        this.args = args;
    }

    public void print() {
        System.out.print(functionIdentifier + "(");
        for (ASTExpr arg : args) {
            arg.print();
            System.out.print(", ");
        }
        System.out.print(")");
    }

    public boolean inferType(Dictionary<String, TypeSignature> globalFunTable, Dictionary<String, TypeAnnotation> globalSymTable, Dictionary<String, TypeAnnotation> localSymTable) {
        for (ASTExpr arg : args) {
            boolean success = arg.inferType(globalFunTable, globalSymTable, localSymTable);
            
            if (!success) {
                return false;
            }            
        } 

        if (functionIdentifier.equals("allocateArray")) {

            if (args.size() == 0) {
            
                inferredType = new ASTAnyArrayType();
                return true;

            } else {

                ASTType argumentType = new ASTAnyArrayType(); // default

                boolean foundActualType = false;
                int counter = 0;
                while (!foundActualType && counter < args.size()) {
                    if (!args.get(counter).inferredType.isAnyArrayType()) {
                        argumentType = args.get(counter).inferredType;
                        foundActualType = true;
                    }
                    counter++;
                }

                

                for (ASTExpr arg : args) {
                    if (!argumentType.identityEquals(arg.inferredType)) {
                        System.out.println("ASTBuiltInFunctionCall: 'allocateArray' called with heterogenous type arguments!");
                        return false;
                    }
                }

                inferredType = new ASTArrayType(argumentType);
                return true;
                    

            }






        } else {  

            TypeSignature myTypeSignature = globalFunTable.get(functionIdentifier);

            if (myTypeSignature == null) {
                System.out.println("ASTFunctionCall : Could not find function \"" + functionIdentifier + "\" in global function table!");
                return false;
            }

            if (args.size() != myTypeSignature.argTypeAnnotations.size()) {
                System.out.println("ASTFunctionCall : Function call argument list length mismatch in call to \"" + functionIdentifier + "\"!");
                return false;
            }
        
            int counter = 0;
            for (ASTExpr arg : args) {
                

                if (!arg.inferredType.identityEquals(myTypeSignature.argTypeAnnotations.get(counter).theType)) {
                    System.out.println("ASTFunctionCall : Type signature mismatch in call to function \"" + functionIdentifier + "\"!");    
                    return false;
                }
                counter++;
            }

            if (myTypeSignature.returnTypeAnnotationOrNull == null) {
                System.out.println("ASTFunctionCall : Using void function \"" + functionIdentifier + "\" as an expression!");
                return false; // expressions must have a return type    
            }

            inferredType = myTypeSignature.returnTypeAnnotationOrNull.theType;
            return true;  

        }
    }



    public boolean inferType(Dictionary<String, TypeSignature> globalFunTable, Dictionary<String, TypeAnnotation> globalSymTable) {
        System.out.println("Inferring type of function call!");

        for (ASTExpr arg : args) {
            boolean success = arg.inferType(globalFunTable, globalSymTable);
            
            if (!success) {
                return false;
            }            
        } 


        if (functionIdentifier.equals("allocateArray")) { // has a variable argument list length

            if (args.size() == 0) {
            
                inferredType = new ASTAnyArrayType();
                return true;

            } else {

                ASTType argumentType = new ASTAnyArrayType(); // default

                boolean foundActualType = false;
                int counter = 0;
                while (!foundActualType && counter < args.size()) {
                    if (!args.get(counter).inferredType.isAnyArrayType()) {
                        argumentType = args.get(counter).inferredType;
                        foundActualType = true;
                    }
                    counter++;
                }

                

                for (ASTExpr arg : args) {
                    if (!argumentType.identityEquals(arg.inferredType)) {
                        System.out.println("ASTBuiltInFunctionCall: 'allocateArray' called with heterogenous type arguments!");
                        return false;
                    }
                }

                inferredType = new ASTArrayType(argumentType);
                return true;
                    

            }

        } else { 

            TypeSignature myTypeSignature = globalFunTable.get(functionIdentifier);

            if (myTypeSignature == null) {
                System.out.println("ASTFunctionCall : Could not find function \"" + functionIdentifier + "\" in global function table!");
                return false;
            }
        
            if (args.size() != myTypeSignature.argTypeAnnotations.size()) {
                System.out.println("ASTFunctionCall : Function call argument list length mismatch in call to \"" + functionIdentifier + "\"!");
                return false;
            }

            int counter = 0;
            for (ASTExpr arg : args) {

                if (!arg.inferredType.identityEquals(myTypeSignature.argTypeAnnotations.get(counter).theType)) {
                    System.out.println("ASTFunctionCall : Type signature mismatch in call to function \"" + functionIdentifier + "\"!");
                    return false;
                }
                counter++;
            }

            if (myTypeSignature.returnTypeAnnotationOrNull == null) {
                System.out.println("ASTFunctionCall : Using void function \"" + functionIdentifier + "\" as an expression!");
                return false; // expressions must have a return type    
            }

            inferredType = myTypeSignature.returnTypeAnnotationOrNull.theType;
            return true;  
        }
    }



    private TypeSignature getActualAllocateArrayFunctionTypeSignature() {
        if (args.size() == 0) {

            TypeAnnotation returnTypeAnnotation = new TypeAnnotation(new ASTAnyArrayType(), true);

            ArrayList<TypeAnnotation> argTypeAnnotations = new ArrayList<TypeAnnotation>();

            ArrayList<Boolean> argConstruandStatuses = new ArrayList<Boolean>();      

            return new TypeSignature(argTypeAnnotations, argConstruandStatuses, returnTypeAnnotation);

        } else {
            ASTExpr firstArg = args.get(0);               

            ArrayList<TypeAnnotation> argTypeAnnotations = new ArrayList<TypeAnnotation>();

            ArrayList<Boolean> argConstruandStatuses = new ArrayList<Boolean>();

            ASTType argType = new ASTIntType();
    
            ASTExpr argum = args.get(0);

            if (argum instanceof ASTFunctionCall) {
                ASTFunctionCall castedArg = (ASTFunctionCall) argum;
                if (castedArg.functionIdentifier.equals("allocateArray")) {
                    
                    TypeSignature recursiveSignature = castedArg.getActualAllocateArrayFunctionTypeSignature();
                    argType = recursiveSignature.returnTypeAnnotationOrNull.theType;                        
                    
                } else {
                    argType = argum.inferredType;
                }
            } else {

                argType = argum.inferredType;
    
            }
                
            

            TypeAnnotation annot = new TypeAnnotation(argType, true);
            for (ASTExpr arg : args) {    
                argTypeAnnotations.add(annot);
            }

           
            for (int i = 0; i < argTypeAnnotations.size(); i++) {
             
                argConstruandStatuses.add(true);
               
            }

            TypeAnnotation returnTypeAnnotation = new TypeAnnotation(new ASTArrayType(argType), true);

            return new TypeSignature(argTypeAnnotations, argConstruandStatuses, returnTypeAnnotation);
        }
    }
    


    public void generateGlobalIR(
        ArrayList<IRInstruction> instructions, 
        Dictionary<String, TypeSignature> globalFunctionTable,
        Dictionary<String, TypeAnnotation> globalSymTable,
        ArrayList<String> slotsMarkedForDestruction,
        AnonNameGenerator anongen,
        String returnValueHolder
        
    ) {

        /*
            Possible global cases:

            Type        Provider                                Receiver
            --------------------------------------------------------------------------
            Array       immutable global var indexing           immutable param (default)
            Array       immutable global var indexing           immutable param (construand)
            Array       return slot [indexing]                  immutable param (default)           (ELIMINATED BY TRANSFORM PASS)
            Array       return slot [indexing]                  immutable param (construand)
            Array       mutable global var indexing             immutable param (default) 
            Array       mutable global var indexing             immutable param (construand)
            Int         immutable global var indexing           immutable param (default)
            Int         immutable global var indexing           immutable param (construand)
            Int         return slot [indexing]                  immutable param (default)
            Int         return slot [indexing]                  immutable param (construand)
            Int         mutable global var indexing             immutable param (default) 
            Int         mutable global var indexing             immutable param (construand)
            
            // WHAT ABOUT THE MUTABLE PARAM CASES?
        */

        
       
        TypeSignature myTypeSignature;

        if (functionIdentifier.equals("allocateArray")) {

            if (args.size() == 0) {

                

                myTypeSignature = null;

                instructions.add(new IRAllocateEmptyArray(returnValueHolder));
                return;

            } else {                

                myTypeSignature = getActualAllocateArrayFunctionTypeSignature();
                   
            }

        } else {

            myTypeSignature = globalFunctionTable.get(functionIdentifier);

        }
        

        ArrayList<IRArg> argHolders = new ArrayList<IRArg>();

        int counter = 0;
        for (ASTExpr arg : args) {

            

            if (arg.inferredType.isArrayType()) {

                if (arg instanceof ASTIndexing) { // four cases here

                    ASTIndexing argCasted = (ASTIndexing) arg;

                    TypeAnnotation argAnnotation = globalSymTable.get(argCasted.identifier); // should be found there...

                    if (argAnnotation.isCompletelyImmutable) {

                        if (myTypeSignature.argConstructandStatuses.get(counter)) { // type: array; provider: immutable global var; receiver: immutable construand param

                            String rawArgHolder = "%" + anongen.generate();

                            arg.generateGlobalIR( 
                                instructions, globalFunctionTable, globalSymTable,
                                slotsMarkedForDestruction,
                                anongen,
                                rawArgHolder
                            );


                            String argHolder = "%" + anongen.generate();


                            int depth = 0;
                            
                            ASTType recurseType = argCasted.inferredType;

                            while (true) {
                                if (recurseType.isArrayType()) {
                                    depth++;
                                    recurseType = ((ASTArrayType) recurseType).constituentType;

                                } else {
                                    break;
                                }
                        
                            }

                            instructions.add(new IRWholeTreeCopy(argHolder, new IRRegArrayHead(rawArgHolder), depth));
    
                            argHolders.add(new IRRegArrayHead(argHolder));    

                        } else { // non-construand param

                            String rawArgHolder = "%" + anongen.generate();

                            arg.generateGlobalIR( 
                                instructions, globalFunctionTable, globalSymTable,
                                slotsMarkedForDestruction,
                                anongen,
                                rawArgHolder
                            );

                            argHolders.add(new IRRegArrayHead(rawArgHolder));

                        }

                    } else { 

                        if (myTypeSignature.argConstructandStatuses.get(counter)) { // type: array; provider: mutable global var; receiver: immutable construand param 

                            String rawArgHolder = "%" + anongen.generate();

                            arg.generateGlobalIR( 
                                instructions, globalFunctionTable, globalSymTable,
                                slotsMarkedForDestruction,
                                anongen,
                                rawArgHolder
                            );



                            String argHolder = "%" + anongen.generate();


                            int depth = 0;

                            ASTType recurseType = argCasted.inferredType;

                            while (true) {
                                if (recurseType.isArrayType()) {
                                    depth++;
                                    recurseType = ((ASTArrayType) recurseType).constituentType;

                                } else {
                                    break;
                                }
                        
                            }

                            instructions.add(new IRWholeTreeCopy(argHolder, new IRRegArrayHead(rawArgHolder), depth));
    
                            argHolders.add(new IRRegArrayHead(argHolder));    

                        } else { // type: array; provider: mutable global var; receiver: immutable default param

                            String rawArgHolder = "%" + anongen.generate();

                            argCasted.generateGlobalIRAndSetCflags( 
                                instructions, globalFunctionTable, globalSymTable,
                                slotsMarkedForDestruction,
                                anongen,
                                rawArgHolder
                            );

                            argHolders.add(new IRRegArrayHead(rawArgHolder));

                        }

                    }

                } else if (arg instanceof ASTFunctionCall) { // two cases here, one eliminated

                    boolean construandStatus = myTypeSignature.argConstructandStatuses.get(counter);

                    if (!construandStatus) {

                        System.out.println("ASTFunctionCall IR generation: this case should have been eliminated!");
                        return;

                    } else { // type: array; provider: return slot; receiver: immutable construand param

                        ASTFunctionCall argCasted = (ASTFunctionCall) arg;

                        String argHolder = "%" + anongen.generate();

                        argCasted.generateGlobalIR( 
                                instructions, globalFunctionTable, globalSymTable,
                                slotsMarkedForDestruction,
                                anongen,
                                argHolder
                        );

                        for (ASTExpr argArg : argCasted.args) {
                            if (arg instanceof ASTIndexing) {

                                ASTIndexing argArgCasted = (ASTIndexing) argArg;

                                TypeAnnotation argArgAnnotation = globalSymTable.get(argArgCasted.identifier); // should be found there
                    
                                if (argArgAnnotation.theType.isArrayType() && (!argArgAnnotation.isCompletelyImmutable)) {

                                    String headHolder = "%" + anongen.generate();
                                
                                    instructions.add(new IRLoadArrayHead(headHolder, new IRRegStackAddress("@" + argArgCasted.identifier)));
                                   

                                    instructions.add(new IRCheckForGhostAndDestructThoseRecursivelyIfSo(new IRRegArrayHead(headHolder)));
                                    instructions.add(new IRUnghostflagTree(new IRRegArrayHead(headHolder)));     

                                }

                            }
                        }

                        argHolders.add(new IRRegArrayHead(argHolder));

                    } 

                } else if (arg instanceof ASTIntegerLiteral) {

                    System.out.println("ASTFunctionCall IR generation: array = int error!");

                } else {

                    System.out.println("ASTFunctionCall IR generation: Unknown arg!");

                }

            } else { // arg is Int

                if (arg instanceof ASTIndexing) { // four cases here

                    ASTIndexing argCasted = (ASTIndexing) arg;

                    TypeAnnotation argAnnotation = globalSymTable.get(argCasted.identifier); // should be found there...

                    if (argAnnotation.isCompletelyImmutable) {

                        if (myTypeSignature.argConstructandStatuses.get(counter)) { // type: int; provider: immutable global var; receiver: immutable construand param

                            

                            String argHolder = "%" + anongen.generate();

                            argCasted.generateGlobalIR( 
                                    instructions, globalFunctionTable, globalSymTable,
                                    slotsMarkedForDestruction,
                                    anongen,
                                    argHolder
                            ); 

                            argHolders.add(new IRRegInt(argHolder));                               

                        } else {   // type: int; provider: immutable global var; receiver: immutable default param

                            

                            String argHolder = "%" + anongen.generate();

                            argCasted.generateGlobalIR( 
                                    instructions, globalFunctionTable, globalSymTable,
                                    slotsMarkedForDestruction,
                                    anongen,
                                    argHolder
                            ); 

                            argHolders.add(new IRRegInt(argHolder));    

                        }

                    } else {

                        if (myTypeSignature.argConstructandStatuses.get(counter)) { // type: int; provider: mutable global var; receiver: immutable construand param

                            

                            String argHolder = "%" + anongen.generate();

                            argCasted.generateGlobalIR( 
                                    instructions, globalFunctionTable, globalSymTable,
                                    slotsMarkedForDestruction,
                                    anongen,
                                    argHolder
                            ); 

                            argHolders.add(new IRRegInt(argHolder));                               

                        } else {   // type: int; provider: mutable global var; receiver: immutable default param

                            

                            String argHolder = "%" + anongen.generate();

                            argCasted.generateGlobalIR( 
                                    instructions, globalFunctionTable, globalSymTable,
                                    slotsMarkedForDestruction,
                                    anongen,
                                    argHolder
                            ); 

                            argHolders.add(new IRRegInt(argHolder));

                        }    


                    }
    
                } else if ((arg instanceof ASTFunctionCall)) {

                    if (myTypeSignature.argConstructandStatuses.get(counter)) { // type: int; provider: return slot; receiver: immutable construand param

                        ASTFunctionCall argCasted = (ASTFunctionCall) arg;

                        String argHolder = "%" + anongen.generate();

                        argCasted.generateGlobalIR( 
                                instructions, globalFunctionTable, globalSymTable,
                                slotsMarkedForDestruction,
                                anongen,
                                argHolder
                        ); 

                        for (ASTExpr argArg : argCasted.args) {
                            if (arg instanceof ASTIndexing) {

                                ASTIndexing argArgCasted = (ASTIndexing) argArg;

                                TypeAnnotation argArgAnnotation = globalSymTable.get(argArgCasted.identifier); // should be found there
                    
                                if (argArgAnnotation.theType.isArrayType() && (!argArgAnnotation.isCompletelyImmutable)) {

                                    String headHolder = "%" + anongen.generate();
                                
                                    instructions.add(new IRLoadArrayHead(headHolder, new IRRegStackAddress("@" + argArgCasted.identifier)));
                                   

                                    instructions.add(new IRCheckForGhostAndDestructThoseRecursivelyIfSo(new IRRegArrayHead(headHolder)));
                                    instructions.add(new IRUnghostflagTree(new IRRegArrayHead(headHolder)));     

                                }

                            }
                        }

                        argHolders.add(new IRRegInt(argHolder));

                    } else { // type: int; provider: return slot; receiver: immutable default param

                        // TODO

                    }

                } else if (arg instanceof ASTIntegerLiteral) {

                    ASTIntegerLiteral argCasted = (ASTIntegerLiteral) arg;

                    String argHolder = "%" + anongen.generate();

                    argCasted.generateGlobalIR( 
                            instructions, globalFunctionTable, globalSymTable,
                            slotsMarkedForDestruction,
                            anongen,
                            argHolder
                    ); 

                    argHolders.add(new IRRegInt(argHolder));


                } else {

                    System.out.println("Argument of type unknown to ASTFunctionCall IR generation!");
                    return;
                }
           
            }





            counter++;




           
            
        }

        
        
        if (functionIdentifier.equals("allocateArray")) {

            if (myTypeSignature.returnTypeAnnotationOrNull.theType.identityEquals(new ASTArrayType(new ASTIntType()))) {
                System.out.println("DEEEBUG!");
                instructions.add(new IRAllocateArrayOfInt(returnValueHolder, argHolders));
            } else {
                instructions.add(new IRAllocateArrayOfArrays(returnValueHolder, argHolders));
            }

        } else if (inferredType.isArrayType()) {
            instructions.add(new IRCallArrayHeadFunction(returnValueHolder, functionIdentifier, argHolders));
        } else {
            instructions.add(new IRCallIntFunction(returnValueHolder, functionIdentifier, argHolders));
        }

        
        
        
    
        

        
    }
}
