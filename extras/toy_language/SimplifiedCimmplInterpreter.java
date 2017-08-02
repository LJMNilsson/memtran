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
import java.io.*;

public class SimplifiedCimmplInterpreter {

    public SimplifiedCimmplInterpreter() {

    }

    ASTProgram ast;

    ASTProgram transformedAST;

    
    Dictionary<String, TypeSignature> globalFunTable;
    Dictionary<String, TypeAnnotation> globalSymTable;


    int tempVariableCounter = 0;
    

    // ArrayList<CValue> heap;

    // ArrayList<Dictionary<String, CValue>> stack;

    // Dictionary<String, CFunction> functionDefinitions;

    // ArrayList<CInstruction> main;


    /*
    void createIntermediaryRepresentation() {

        functionDefinitions = new ArrayList<CFunction>();

        for (ASTFunctionDefinition funDef : ast.functionDefinitions) {
            functionDefinitions.addLast(funDef.generateIR());
        }

        main = new ArrayList<CInstruction>();

        for (ASTStatement statement : ast.main, globalSymTable) {
            statement.addInstructions(main);
        } 

    }
    */


    ASTFunctionCall transformFunctionCall(
            ASTFunctionCall functionCall, ArrayList<ASTStatement> preInsert, ArrayList<ASTStatement> postInsert,  Dictionary<String, TypeAnnotation> currentSymTable,
            Dictionary<String, BuildAnnotation> currentIsOwnerTable,
            Dictionary<String, TypeSignature> funTable
    ) {

        ArrayList<ASTExpr> newArgs = new ArrayList<ASTExpr>();

        int counter = 0;
        for (ASTExpr arg : functionCall.args) {
            
            if (arg instanceof ASTFunctionCall) {

                if (arg.inferredType.isArrayType()) {

                    if (functionCall.functionIdentifier.equals("allocateArray")) {

                        newArgs.add(arg); // allocateArray is not in the symtable, but has all arguments as constructands

                    } else {

                        TypeSignature mySignature = funTable.get(functionCall.functionIdentifier);
                            


                        if (mySignature.argConstructandStatuses.get(counter) == null) {

                            ArrayList<ASTStatement> myPreInsert = new ArrayList<ASTStatement>();
                            ArrayList<ASTStatement> myPostInsert = new ArrayList<ASTStatement>();

                            ASTFunctionCall transformedFunctionCall = transformFunctionCall((ASTFunctionCall) arg, myPreInsert, myPostInsert, currentSymTable, currentIsOwnerTable, funTable);

                            for (ASTStatement pre : myPreInsert) {
                                preInsert.add(pre);
                            }

                            String tempVarName = "#" + Integer.toString(tempVariableCounter);
                            tempVariableCounter++;

                            preInsert.add(new ASTExtraVarWithManualDestructInitialization(tempVarName, arg.inferredType, transformedFunctionCall));

                            for (ASTStatement post : myPostInsert) {
                                preInsert.add(post);
                            }


                            postInsert.add(new ASTDestructStatement(tempVarName));

                            ArrayList<ASTExpr> emptyIndexings = new ArrayList<ASTExpr>(); 
                            ASTExpr newArg = new ASTIndexing(tempVarName, emptyIndexings);
                            
                           
                            currentSymTable.put(tempVarName, new TypeAnnotation(arg.inferredType, true));
                            currentIsOwnerTable.put(tempVarName, new BuildAnnotation(true, false));

                            newArg.inferredType = arg.inferredType; 

                            newArgs.add(newArg);

                        } else {

                            ASTFunctionCall transformedFunctionCall = transformFunctionCall((ASTFunctionCall) arg, preInsert, postInsert, currentSymTable, currentIsOwnerTable, funTable);

                            newArgs.add(transformedFunctionCall);

                        }

                    }

                } else {

                    ASTFunctionCall transformedFunctionCall = transformFunctionCall((ASTFunctionCall) arg, preInsert, postInsert, currentSymTable, currentIsOwnerTable, funTable);

                    newArgs.add(transformedFunctionCall);  

                }

            } else if (arg instanceof ASTFunctionCallIndexing) {

                TypeSignature mySignature = funTable.get(functionCall.functionIdentifier);

                ASTFunctionCallIndexing argCasted = (ASTFunctionCallIndexing) arg;

                ArrayList<ASTStatement> myPreInsert = new ArrayList<ASTStatement>();
                ArrayList<ASTStatement> myPostInsert = new ArrayList<ASTStatement>();

                ASTFunctionCall transformedFunctionCall = transformFunctionCall(argCasted.functionCall, myPreInsert, myPostInsert, currentSymTable, currentIsOwnerTable, funTable);

                for (ASTStatement pre : myPreInsert) {
                    preInsert.add(pre);
                }

                String tempVarName = "#" + Integer.toString(tempVariableCounter);
                tempVariableCounter++;

                preInsert.add(new ASTInitialization(false, tempVarName, argCasted.functionCall.inferredType, transformedFunctionCall));

                for (ASTStatement post : myPostInsert) {
                    preInsert.add(post);
                }


                

                ASTExpr newArg = new ASTIndexing(tempVarName, argCasted.indexings);
                
               
                currentSymTable.put(tempVarName, new TypeAnnotation(arg.inferredType, true));
                currentIsOwnerTable.put(tempVarName, new BuildAnnotation(true, false));

                newArg.inferredType = arg.inferredType; 

                newArgs.add(newArg);

            } else {

                newArgs.add(arg);  

            }

            counter++;

        }

        ASTFunctionCall result = new ASTFunctionCall(functionCall.functionIdentifier, newArgs);
        result.inferredType = functionCall.inferredType;
        return result;

    }




    ASTStatement transformStatement(ASTStatement inStatement, ArrayList<ASTStatement> preInsert, ArrayList<ASTStatement> postInsert, Dictionary<String, TypeAnnotation> currentSymTable,
            Dictionary<String, BuildAnnotation> currentIsOwnerTable,
            Dictionary<String, TypeSignature> funTable
    ) {
        
        if (inStatement instanceof ASTFunctionCallStatement) {

            ASTFunctionCallStatement inCasted = (ASTFunctionCallStatement) inStatement;

            ArrayList<ASTExpr> newArgs = new ArrayList<ASTExpr>();

            int counter = 0;

            for (ASTExpr arg : inCasted.args) {
                if (arg instanceof ASTFunctionCall) {

                    if (arg.inferredType.isArrayType()) {

                        

                        TypeSignature mySignature = funTable.get(inCasted.functionIdentifier);

                        

                        if (mySignature.argConstructandStatuses.get(counter) == false) {

                            ArrayList<ASTStatement> myPreInsert = new ArrayList<ASTStatement>();
                            ArrayList<ASTStatement> myPostInsert = new ArrayList<ASTStatement>();

                            ASTFunctionCall transformedFunctionCall = transformFunctionCall((ASTFunctionCall) arg, myPreInsert, myPostInsert, currentSymTable, currentIsOwnerTable, funTable);

                            for (ASTStatement pre : myPreInsert) {
                                preInsert.add(pre);
                            }

                            String tempVarName = "#" + Integer.toString(tempVariableCounter);
                            tempVariableCounter++;

                            preInsert.add(new ASTExtraVarWithManualDestructInitialization(tempVarName, arg.inferredType, transformedFunctionCall));

                            for (ASTStatement post : myPostInsert) {
                                preInsert.add(post);
                            }


                            postInsert.add(new ASTDestructStatement(tempVarName));

                            ArrayList<ASTExpr> emptyIndexings = new ArrayList<ASTExpr>(); 
                            ASTExpr newArg = new ASTIndexing(tempVarName, emptyIndexings);
                            
                           
                            currentSymTable.put(tempVarName, new TypeAnnotation(arg.inferredType, true));
                            currentIsOwnerTable.put(tempVarName, new BuildAnnotation(true, false));

                            newArg.inferredType = arg.inferredType; 

                            newArgs.add(newArg);

                        } else {

                            ASTFunctionCall transformedFunctionCall = transformFunctionCall((ASTFunctionCall) arg, preInsert, postInsert, currentSymTable, currentIsOwnerTable, funTable);

                            newArgs.add(transformedFunctionCall);

                        }

                    } else {

                        ASTFunctionCall transformedFunctionCall = transformFunctionCall((ASTFunctionCall) arg, preInsert, postInsert, currentSymTable, currentIsOwnerTable, funTable);

                        newArgs.add(transformedFunctionCall);        
                
                    }

                } else if (arg instanceof ASTFunctionCallIndexing) {

                    TypeSignature mySignature = funTable.get(inCasted.functionIdentifier);

                    ASTFunctionCallIndexing argCasted = (ASTFunctionCallIndexing) arg;

                    ArrayList<ASTStatement> myPreInsert = new ArrayList<ASTStatement>();
                    ArrayList<ASTStatement> myPostInsert = new ArrayList<ASTStatement>();

                    ASTFunctionCall transformedFunctionCall = transformFunctionCall(argCasted.functionCall, myPreInsert, myPostInsert, currentSymTable, currentIsOwnerTable, funTable);

                    for (ASTStatement pre : myPreInsert) {
                        preInsert.add(pre);
                    }

                    String tempVarName = "#" + Integer.toString(tempVariableCounter);
                    tempVariableCounter++;

                    preInsert.add(new ASTInitialization(false, tempVarName, argCasted.functionCall.inferredType, transformedFunctionCall));

                    for (ASTStatement post : myPostInsert) {
                        preInsert.add(post);
                    }


                    

                    ASTExpr newArg = new ASTIndexing(tempVarName, argCasted.indexings);
                    
                   
                    currentSymTable.put(tempVarName, new TypeAnnotation(arg.inferredType, true));
                    currentIsOwnerTable.put(tempVarName, new BuildAnnotation(true, false));

                    newArg.inferredType = arg.inferredType; 

                    newArgs.add(newArg);

                    
                    
                } else {

                    

                    newArgs.add(arg);

                }

                counter++;                
            }      

            return new ASTFunctionCallStatement(inCasted.functionIdentifier, newArgs);     



        } else if (inStatement instanceof ASTInitialization) {

            ASTInitialization inCasted = (ASTInitialization) inStatement;

            if (inCasted.expr instanceof ASTFunctionCall) {

                ASTFunctionCall exprCasted = (ASTFunctionCall) (inCasted.expr);

                ASTFunctionCall newFunctionCall = transformFunctionCall(exprCasted, preInsert, postInsert, currentSymTable, currentIsOwnerTable, funTable);

                return new ASTInitialization(inCasted.isMu, inCasted.identifier, inCasted.type, newFunctionCall);

            } else if (inCasted.expr instanceof ASTFunctionCallIndexing) {
    
                ASTFunctionCallIndexing exprCasted = (ASTFunctionCallIndexing) inCasted.expr;

                ArrayList<ASTStatement> myPreInsert = new ArrayList<ASTStatement>();
                ArrayList<ASTStatement> myPostInsert = new ArrayList<ASTStatement>();

                ASTFunctionCall transformedFunctionCall = transformFunctionCall(exprCasted.functionCall, myPreInsert, myPostInsert, currentSymTable, currentIsOwnerTable, funTable);

                for (ASTStatement pre : myPreInsert) {
                    preInsert.add(pre);
                }

                String tempVarName = "#" + Integer.toString(tempVariableCounter);
                tempVariableCounter++;

                preInsert.add(new ASTInitialization(false, tempVarName, exprCasted.functionCall.inferredType, transformedFunctionCall));

                for (ASTStatement post : myPostInsert) {
                    preInsert.add(post);
                }

                

                ASTExpr newExpr = new ASTIndexing(tempVarName, exprCasted.indexings);
                                       
                currentSymTable.put(tempVarName, new TypeAnnotation(exprCasted.inferredType, true));
                currentIsOwnerTable.put(tempVarName, new BuildAnnotation(true, false));

                newExpr.inferredType = exprCasted.inferredType; 

                return new ASTInitialization(inCasted.isMu, inCasted.identifier, inCasted.type, newExpr);


            } else {

                return inStatement;

            }

        } else if (inStatement instanceof ASTMutation) {

            ASTMutation inCasted = (ASTMutation) inStatement;

            if (inCasted.expr instanceof ASTFunctionCall) {

                ASTFunctionCall exprCasted = (ASTFunctionCall) (inCasted.expr);

                ASTFunctionCall newFunctionCall = transformFunctionCall(exprCasted, preInsert, postInsert, currentSymTable, currentIsOwnerTable, funTable);

                return new ASTMutation(inCasted.varIndexing, newFunctionCall);

            } else if (inCasted.expr instanceof ASTFunctionCallIndexing) {

                ASTFunctionCallIndexing exprCasted = (ASTFunctionCallIndexing) inCasted.expr;

                ArrayList<ASTStatement> myPreInsert = new ArrayList<ASTStatement>();
                ArrayList<ASTStatement> myPostInsert = new ArrayList<ASTStatement>();

                ASTFunctionCall transformedFunctionCall = transformFunctionCall(exprCasted.functionCall, myPreInsert, myPostInsert, currentSymTable, currentIsOwnerTable, funTable);

                for (ASTStatement pre : myPreInsert) {
                    preInsert.add(pre);
                }

                String tempVarName = "#" + Integer.toString(tempVariableCounter);
                tempVariableCounter++;

                preInsert.add(new ASTInitialization(false, tempVarName, exprCasted.functionCall.inferredType, transformedFunctionCall));

                for (ASTStatement post : myPostInsert) {
                    preInsert.add(post);
                }

                

                ASTExpr newExpr = new ASTIndexing(tempVarName, exprCasted.indexings);
                                       
                currentSymTable.put(tempVarName, new TypeAnnotation(exprCasted.inferredType, true));
                currentIsOwnerTable.put(tempVarName, new BuildAnnotation(true, false));

                newExpr.inferredType = exprCasted.inferredType; 

                return new ASTMutation(inCasted.varIndexing, newExpr);

            } else {

                return inStatement;

            }

        } else if (inStatement instanceof ASTReturnStatement) {

            ASTReturnStatement inCasted = (ASTReturnStatement) inStatement;

            if (inCasted.exprOrNull != null) {

                if (inCasted.exprOrNull instanceof ASTFunctionCall) { 
                    
                    ArrayList<ASTStatement> myPreInsert = new ArrayList<ASTStatement>();
                    ArrayList<ASTStatement> myPostInsert = new ArrayList<ASTStatement>();

                    ASTFunctionCall transformedFunctionCall = transformFunctionCall((ASTFunctionCall) (inCasted.exprOrNull), myPreInsert, myPostInsert, 
                                currentSymTable, currentIsOwnerTable, funTable);

                    for (ASTStatement pre : myPreInsert) {
                        preInsert.add(pre);
                    }

                    String tempVarName = "#" + Integer.toString(tempVariableCounter);
                    tempVariableCounter++;

                    preInsert.add(new ASTExtraVarWithManualDestructInitialization(tempVarName, inCasted.exprOrNull.inferredType, transformedFunctionCall)); 
                    // this one is not destructed but transferred



                    for (ASTStatement post : myPostInsert) {
                        preInsert.add(post);
                    } 

                    ArrayList<ASTExpr> emptyIndexings = new ArrayList<ASTExpr>(); 
                    ASTExpr newExpr = new ASTIndexing(tempVarName, emptyIndexings);
                    
                    newExpr.inferredType = inCasted.exprOrNull.inferredType;
                   
                    currentSymTable.put(tempVarName, new TypeAnnotation(inCasted.exprOrNull.inferredType, true));
                    currentIsOwnerTable.put(tempVarName, new BuildAnnotation(true, false)); 

                    return new ASTReturnStatement(newExpr);

                } else if (inCasted.exprOrNull instanceof ASTFunctionCallIndexing) {

                    ASTFunctionCallIndexing exprCasted = (ASTFunctionCallIndexing) (inCasted.exprOrNull);

                    ArrayList<ASTStatement> myPreInsert = new ArrayList<ASTStatement>();
                    ArrayList<ASTStatement> myPostInsert = new ArrayList<ASTStatement>();

                    ASTFunctionCall transformedFunctionCall = transformFunctionCall(exprCasted.functionCall, myPreInsert, myPostInsert, currentSymTable, currentIsOwnerTable, funTable);

                    for (ASTStatement pre : myPreInsert) {
                        preInsert.add(pre);
                    }

                    String tempVarName = "#" + Integer.toString(tempVariableCounter);
                    tempVariableCounter++;

                    preInsert.add(new ASTInitialization(false, tempVarName, exprCasted.functionCall.inferredType, transformedFunctionCall));

                    for (ASTStatement post : myPostInsert) {
                        preInsert.add(post);
                    }

                    String resultVarName = "#" + Integer.toString(tempVariableCounter);
                    tempVariableCounter++;

                    ASTExpr newExpr = new ASTIndexing(tempVarName, exprCasted.indexings);
                    newExpr.inferredType = exprCasted.inferredType; 

                    preInsert.add(new ASTExtraVarWithManualDestructInitialization(resultVarName, exprCasted.inferredType, newExpr)); // no destr of this one, transfer.

                    

                    
                                           
                    currentSymTable.put(tempVarName, new TypeAnnotation(exprCasted.functionCall.inferredType, true));
                    currentIsOwnerTable.put(tempVarName, new BuildAnnotation(true, false));

                    currentSymTable.put(resultVarName, new TypeAnnotation(exprCasted.inferredType, true));
                    currentIsOwnerTable.put(tempVarName, new BuildAnnotation(true, false));

                    ArrayList<ASTExpr> emptyIndexings = new ArrayList<ASTExpr>(); 
                    ASTExpr newReturnExpr = new ASTIndexing(tempVarName, emptyIndexings);

                    newReturnExpr.inferredType = exprCasted.inferredType;

                    return new ASTReturnStatement(newReturnExpr);       

                } else {

                    return inStatement;

                }
        
            } else {
                return inStatement;
            }

        } else {
            return inStatement;
        }

    }




    ASTFunctionDefinition transformFunctionDefinition(ASTFunctionDefinition inFunDef, Dictionary<String, TypeSignature> funTable) {
    
        ArrayList<ASTStatement> newStatements = new ArrayList<ASTStatement>();

        for (ASTStatement inStatement : inFunDef.body.statements) {

            ArrayList<ASTStatement> preInsert = new ArrayList<ASTStatement>();
            ArrayList<ASTStatement> postInsert = new ArrayList<ASTStatement>();

            ASTStatement newStatement = transformStatement(inStatement, preInsert, postInsert, inFunDef.localSymTable, inFunDef.localIsOwnerTable, funTable);

            for (ASTStatement pre : preInsert) {
                newStatements.add(pre);
            }

            newStatements.add(newStatement);

            for (ASTStatement post : postInsert) {
                newStatements.add(post);
            }

        }        

        ASTFunctionDefinition result = new ASTFunctionDefinition(inFunDef.functionName, inFunDef.params, inFunDef.returnTypeOrNull, new ASTBlock(newStatements));        
        result.localSymTable = inFunDef.localSymTable;
        result.localIsOwnerTable = inFunDef.localIsOwnerTable;
        return result;
    }



    ASTProgram transformProgram() {

        ArrayList<ASTFunctionDefinition> transformedFunctionDefinitions = new ArrayList<ASTFunctionDefinition>();
        ArrayList<ASTStatement> transformedMain = new ArrayList<ASTStatement>();

        
        
        for (ASTFunctionDefinition funDef : ast.functionDefinitions) {
            transformedFunctionDefinitions.add(transformFunctionDefinition(funDef, globalFunTable));
        }
        

        for (ASTStatement statement : ast.main) {
            ArrayList<ASTStatement> preInsert = new ArrayList<ASTStatement>();
            ArrayList<ASTStatement> postInsert = new ArrayList<ASTStatement>();

            Dictionary<String, BuildAnnotation> dummyEmptyIsOwnerTable = new Hashtable<String, BuildAnnotation>();

            ASTStatement statementTransformation = transformStatement(statement, preInsert, postInsert, globalSymTable, dummyEmptyIsOwnerTable, globalFunTable);

            for (ASTStatement pre : preInsert) {
                transformedMain.add(pre);
            }

            transformedMain.add(statementTransformation);

            for (ASTStatement post : postInsert) {
                transformedMain.add(post);
            }
        }
        
        ASTProgram transformedAST = new ASTProgram(transformedFunctionDefinitions, transformedMain);

        ast = null;

        return transformedAST;

    }
    





    void markOwnershipForFunctionDefinition(ASTFunctionDefinition funDef) {
        funDef.localIsOwnerTable = new Hashtable<String, BuildAnnotation>();

        for (ASTParamDeclaration param : funDef.params) {

            if (param.type.isArrayType()) {
                if (!(param.isMu)) {
                    if (param.isConstructand) {
                            BuildAnnotation annotation = new BuildAnnotation(true, false);
                            funDef.localIsOwnerTable.put(param.paramName, annotation);      
                    } else {
                        BuildAnnotation annotation = new BuildAnnotation(false, false);
                        funDef.localIsOwnerTable.put(param.paramName, annotation);
                    }
                }
            }
        }

        for (ASTStatement statement : funDef.body.statements) {
            if (statement instanceof ASTInitialization) {
                ASTInitialization statementCasted = (ASTInitialization) statement;

                if (!(statementCasted.isMu)) {
                    if (statementCasted.type.isArrayType()) {
                        

                        if (statementCasted.expr instanceof ASTIndexing) {
                            
                            ASTIndexing exprCasted = (ASTIndexing) (statementCasted.expr);

                            TypeAnnotation indexingVarTypeAnnotation = funDef.localSymTable.get(exprCasted.identifier);
                            if (indexingVarTypeAnnotation != null) {  // it can be a global variable else
                                

                                if (indexingVarTypeAnnotation.isCompletelyImmutable) {
                    
                                    BuildAnnotation indexingVarAnnotation = funDef.localIsOwnerTable.get(exprCasted.identifier);
                                    if (indexingVarAnnotation == null) {
                                        System.out.println("markOwnership : SHOULD NOT HAPPEN!");
                                        return;
                                    } else {
                                        if (indexingVarAnnotation.isOwner) {

                                            BuildAnnotation annotation = new BuildAnnotation(false, true);
                                            funDef.localIsOwnerTable.put(statementCasted.identifier, annotation);

                                        } else {

                                            if (indexingVarAnnotation.shouldBeEliminated) {

                                                BuildAnnotation annotation = new BuildAnnotation(false, true);
                                                funDef.localIsOwnerTable.put(statementCasted.identifier, annotation);

                                            } else {

                                                BuildAnnotation annotation = new BuildAnnotation(false, false); // in case the unowner is a param
                                                funDef.localIsOwnerTable.put(statementCasted.identifier, annotation);
                                            }
                                        }
                    
                                    }

                                } 

                            } else { // provider is global variable

                                TypeAnnotation indexingVarTypeAnnotationGlobal = globalSymTable.get(exprCasted.identifier);
                                if (indexingVarTypeAnnotationGlobal == null) {
                                    System.out.println("marOwnership : SHOLD NOT HAPPEN #36");
                                    return;
                                }

                                if (indexingVarTypeAnnotationGlobal.isCompletelyImmutable) {

                                    funDef.localIsOwnerTable.put(statementCasted.identifier, new BuildAnnotation(false, false));

                                } else {

                                    funDef.localIsOwnerTable.put(statementCasted.identifier, new BuildAnnotation(true, false));

                                }

                            }

                        } else if (statementCasted.expr instanceof ASTFunctionCall) {

                            funDef.localIsOwnerTable.put(statementCasted.identifier, new BuildAnnotation(true, false));

                        } else if (statementCasted.expr instanceof ASTFunctionCallIndexing) {

                            funDef.localIsOwnerTable.put(statementCasted.identifier, new BuildAnnotation(true, false)); // hope this is right

                        } else if (statementCasted.expr instanceof ASTIntegerLiteral) {

                            System.out.println("markOwnership : SHOULD NOT HAPPEN 2");

                        } else {

                            System.out.println("Initialization found that has an expr of a class unknown to markOwnership pass!");

                        }
                    }
                }
            }
        }
    }



    void markOwnershipPass() {
        for (ASTFunctionDefinition funDef : ast.functionDefinitions) {
            markOwnershipForFunctionDefinition(funDef);
        }

        // observe: no ownership marking for the globals
    }



    ASTIndexing conjoinIndexings(ASTIndexing identifierIndexing, ASTIndexing addOnIndexing) {

        ArrayList<ASTExpr> newIndexings = new ArrayList<ASTExpr>();

        for (ASTExpr indexing : identifierIndexing.indexings) {
            newIndexings.add(indexing);
        }
        
        for (ASTExpr indexing : addOnIndexing.indexings) {
            newIndexings.add(indexing);
        }

        ASTIndexing result = new ASTIndexing(identifierIndexing.identifier, newIndexings);
        result.inferredType = addOnIndexing.inferredType;
        return result;
    }



    ASTExpr eliminatePassExpr(ASTExpr inExpr, Dictionary<String, BuildAnnotation> annotations) {

        if (inExpr instanceof ASTIndexing) {

            ASTIndexing exprCasted = (ASTIndexing) inExpr;

            BuildAnnotation annotation = annotations.get(exprCasted.identifier);
            if (annotation != null) {

                if ((!annotation.isOwner) && annotation.shouldBeEliminated) {

                    ASTIndexing indexing = annotation.indexingOrNull; // should be set by the statement function below
                    if (indexing == null) {
                        System.out.println("eliminatePassExpr: SHOULD NOT HAPPEN! #897");
                        return null;
                    }
                    if (exprCasted.indexings.size() == 0) {
                        return indexing;
                    } else {
                        String dummyIdentifier = "BLAH!";
                        ASTIndexing construend = new ASTIndexing(dummyIdentifier, exprCasted.indexings);
                        construend.inferredType = exprCasted.inferredType;
                        

                        return conjoinIndexings(indexing, construend);
                        
                    }

                } else {

                    return inExpr;

                }

            } else {

                return inExpr;

            }

        } else if (inExpr instanceof ASTFunctionCall) {

            ArrayList<ASTExpr> newArgs = new ArrayList<ASTExpr>();

            ASTFunctionCall exprCasted = (ASTFunctionCall) inExpr;

            for (ASTExpr arg : exprCasted.args) {
                
                ASTExpr newArg = eliminatePassExpr(arg, annotations);
                newArgs.add(newArg);
                
            }

            ASTFunctionCall result = new ASTFunctionCall(exprCasted.functionIdentifier, newArgs);
            result.inferredType = inExpr.inferredType;

            return result;

        } else {
    
            return inExpr;    

        }

    }






    void eliminatePassFunctionDefinition(ASTFunctionDefinition funDef) {

        ArrayList<ASTStatement> newStatements = new ArrayList<ASTStatement>();

        for (ASTStatement statement : funDef.body.statements) {

            if (statement instanceof ASTFunctionCallStatement) {

                ASTFunctionCallStatement statementCasted = (ASTFunctionCallStatement) statement;

                ArrayList<ASTExpr> newArgs = new ArrayList<ASTExpr>();

                for (ASTExpr arg : statementCasted.args) {

                    
                    
                    newArgs.add(eliminatePassExpr(arg, funDef.localIsOwnerTable));
                }

                newStatements.add(new ASTFunctionCallStatement(statementCasted.functionIdentifier, newArgs));

            } else if (statement instanceof ASTInitialization) {

                ASTInitialization statementCasted = (ASTInitialization) statement;

                BuildAnnotation annotation = funDef.localIsOwnerTable.get(statementCasted.identifier);
                if (annotation != null) {

                    if ((!annotation.isOwner) && annotation.shouldBeEliminated) {

                        // remmember to set annotation.indexingOrNull, below

                        
                        if (statementCasted.expr instanceof ASTIndexing) {

                            ASTIndexing exprCasted = (ASTIndexing) (statementCasted.expr);

                                

                            BuildAnnotation exprAnnotation = funDef.localIsOwnerTable.get(exprCasted.identifier);
                            if (exprAnnotation == null || exprAnnotation.isOwner) {

                                System.out.println("YO!");

                                ArrayList<String> exprHolders = new ArrayList<String>();
                                 
                                for (ASTExpr indexExpr : exprCasted.indexings) {
                        
                                    String temp = "#" + Integer.toString(tempVariableCounter);
                                    tempVariableCounter++;
                                    exprHolders.add(temp);

                                    funDef.localSymTable.put(temp, new TypeAnnotation(new ASTIntType(), true));

                                    newStatements.add(new ASTInitialization(false, temp, new ASTIntType(), eliminatePassExpr(indexExpr, funDef.localIsOwnerTable)));
                                }
        
                                ArrayList<ASTExpr> indexings = new ArrayList<ASTExpr>();
                                for (String exprHolder : exprHolders) {
                                    ArrayList<ASTExpr> emptyIndexings = new ArrayList<ASTExpr>();
                                    indexings.add(new ASTIndexing(exprHolder, emptyIndexings));
                                }

                                // newStatements.add(new Initialization(false, statementCasted.identifier, statementCasted.type, new ASTIndexing(exprCasted.identifier, indexings)));
                                // (Unnecessary statement)
                                

                                annotation.indexingOrNull = new ASTIndexing(exprCasted.identifier, indexings);
 
                            } else { // exprAnnotation is not owner

                                System.out.println("YAY!");

                                ArrayList<String> exprHolders = new ArrayList<String>();
                                 
                                for (ASTExpr indexExpr : exprCasted.indexings) {
                        
                                    String temp = "#" + Integer.toString(tempVariableCounter);
                                    tempVariableCounter++;
                                    exprHolders.add(temp);

                                    funDef.localSymTable.put(temp, new TypeAnnotation(new ASTIntType(), true));

                                    newStatements.add(new ASTInitialization(false, temp, new ASTIntType(), eliminatePassExpr(indexExpr, funDef.localIsOwnerTable)));
                                }
        
                                ArrayList<ASTExpr> indexings = new ArrayList<ASTExpr>();
                                for (String exprHolder : exprHolders) {
                                    ArrayList<ASTExpr> emptyIndexings = new ArrayList<ASTExpr>();
                                    indexings.add(new ASTIndexing(exprHolder, emptyIndexings));
                                }

                                

                                annotation.indexingOrNull = conjoinIndexings(exprAnnotation.indexingOrNull, new ASTIndexing(exprCasted.identifier, indexings));

                            }                           

                        } else {

                            ASTExpr newExpr = eliminatePassExpr(statementCasted.expr, funDef.localIsOwnerTable);

                            newStatements.add(new ASTInitialization(statementCasted.isMu, statementCasted.identifier, statementCasted.type, newExpr));

                        }

                    } else {

                        ASTExpr newExpr = eliminatePassExpr(statementCasted.expr, funDef.localIsOwnerTable);

                        newStatements.add(new ASTInitialization(statementCasted.isMu, statementCasted.identifier, statementCasted.type, newExpr));

                    }

                } else {

                    ASTExpr newExpr = eliminatePassExpr(statementCasted.expr, funDef.localIsOwnerTable);

                    newStatements.add(new ASTInitialization(statementCasted.isMu, statementCasted.identifier, statementCasted.type, newExpr));

                }

            } else if (statement instanceof ASTMutation) {

                ASTMutation statementCasted = (ASTMutation) statement;

                ASTExpr newExpr = eliminatePassExpr(statementCasted.expr, funDef.localIsOwnerTable);

                newStatements.add(new ASTMutation(statementCasted.varIndexing, newExpr));

            } else if (statement instanceof ASTReturnStatement) {

                ASTReturnStatement statementCasted = (ASTReturnStatement) statement;

                if (statementCasted.exprOrNull == null) {

                    newStatements.add(statementCasted);

                } else {

                    ASTExpr newExpr = eliminatePassExpr(statementCasted.exprOrNull, funDef.localIsOwnerTable);

                    newStatements.add(new ASTReturnStatement(newExpr));

                }

            } else if (statement instanceof ASTDestructStatement) {

                newStatements.add(statement);

            } else if (statement instanceof ASTExtraVarWithManualDestructInitialization) {

                newStatements.add(statement);

            } else {

                System.out.println("Statement of kind unknown to eliminatePass!");
            }

        }

        funDef.body.statements = newStatements;

    }



    void eliminatePass() {

        for (ASTFunctionDefinition funDef : transformedAST.functionDefinitions) {

            eliminatePassFunctionDefinition(funDef);

            
        }

        
    }



    void lastOccurrencePassExpr(ASTExpr inExpr, Hashtable<String, Boolean> hasBeenSeenMap) {

        if (inExpr instanceof ASTIndexing) {

            ASTIndexing exprCasted = (ASTIndexing) inExpr;

            if (hasBeenSeenMap.get(exprCasted.identifier) == null) {

                exprCasted.isLastOccurrence = true;
                hasBeenSeenMap.put(exprCasted.identifier, true);

            }

        } else if (inExpr instanceof ASTFunctionCall) {

            ASTFunctionCall exprCasted = (ASTFunctionCall) inExpr;
    
            for (int i = exprCasted.args.size() - 1; i >= 0; i--) {
                ASTExpr arg = exprCasted.args.get(i);

                lastOccurrencePassExpr(arg, hasBeenSeenMap);
            }

        } else {
    
            // do nothing

        }

    }



    void lastOccurrencePass() {
        // In the absence of branching, this is absolutely trivial...

        // Only checks local indexings...

        for (ASTFunctionDefinition funDef : transformedAST.functionDefinitions) {
            Hashtable<String, Boolean> hasBeenSeenMap = new Hashtable<String, Boolean>();

            for (int i = funDef.body.statements.size() - 1; i >= 0; i--) {

                ASTStatement statement = funDef.body.statements.get(i);

                if (statement instanceof ASTInitialization) {

                    ASTInitialization statementCasted = (ASTInitialization) statement;

                    if (hasBeenSeenMap.get(statementCasted.identifier) == null) {
                        hasBeenSeenMap.put(statementCasted.identifier, true);
                    }

                    lastOccurrencePassExpr(statementCasted.expr, hasBeenSeenMap);

                } else if (statement instanceof ASTMutation) {

                    

                    ASTMutation statementCasted = (ASTMutation) statement;

                    if (hasBeenSeenMap.get(statementCasted.varIndexing.identifier) == null) {
                        hasBeenSeenMap.put(statementCasted.varIndexing.identifier, true);
                    }

                    lastOccurrencePassExpr(statementCasted.expr, hasBeenSeenMap);

                } else if (statement instanceof ASTFunctionCallStatement) {

                    ASTFunctionCallStatement statementCasted = (ASTFunctionCallStatement) statement;
                
                    for (ASTExpr arg : statementCasted.args) {
                        lastOccurrencePassExpr(arg, hasBeenSeenMap);
                    }

                } else if (statement instanceof ASTReturnStatement) {

                    ASTReturnStatement statementCasted = (ASTReturnStatement) statement;

                    if (i < funDef.body.statements.size() - 1) {
                        System.out.println("WARNING: Unreachable statements in function '" + funDef.functionName + "'!");
                    }

                    if (statementCasted.exprOrNull != null) {
                        lastOccurrencePassExpr(statementCasted.exprOrNull, hasBeenSeenMap);
                    }

                } else if (statement instanceof ASTExtraVarWithManualDestructInitialization) {

                    ASTExtraVarWithManualDestructInitialization statementCasted = (ASTExtraVarWithManualDestructInitialization) statement;

                    lastOccurrencePassExpr(statementCasted.expr, hasBeenSeenMap);

                } else if (statement instanceof ASTDestructStatement) {

                    // do nothing                    

                } else {

                    System.out.println("Statement of unknown type found by lastOccurrencePass!");

                }
            }
        }


    }











    int currentChar;
    int nextPeekChar;

    boolean charPtrIsAtStartOfFile = true;

    int nextChar(FileInputStream in) throws IOException {
        if (charPtrIsAtStartOfFile) {
            charPtrIsAtStartOfFile = false;

            nextPeekChar = in.read();

            if (nextPeekChar == -1) {
                return -1;
            } else {
                currentChar = nextPeekChar;
                nextPeekChar = in.read();
                return currentChar;
            }

            
        } else {

            currentChar = nextPeekChar;
            nextPeekChar = in.read();
            return currentChar;

        }
    }

    int peekChar() {
        return nextPeekChar;
    }   



    Token prevToken;
    Token currentToken;


    void nextToken(FileInputStream in) throws IOException {

        prevToken = currentToken;

        

        int character = nextChar(in);
        if (character != -1) {

            if (character == 13 || character == 32 || character == 10) { // CR, SPACE, LF 
                nextToken(in);
            } else if (character == '[') {
                currentToken = new Token(Token.Kind.LSQUAREBRACKET);
                
            } else if (character == ']') {
                currentToken = new Token(Token.Kind.RSQUAREBRACKET);
                
            } else if (character == '(') {
                currentToken = new Token(Token.Kind.LPAREN);
                
            } else if (character == ')') {
                currentToken = new Token(Token.Kind.RPAREN);
                
            } else if (character == '=') {
                int peek = peekChar();

                if (peek == '>') {
                    
                    character = nextChar(in);
                    currentToken = new Token(Token.Kind.SHORTLARROW);
                    

                } else {

                    currentToken = new Token(Token.Kind.ASSIGNMENTOPERATOR);
                    
                }
        
            } else if (character == ',') {
                currentToken = new Token(Token.Kind.COMMA);
                
            } else if (character == ':') {
                currentToken = new Token(Token.Kind.COLON);
                
            } else if (character == ';') {
                currentToken = new Token(Token.Kind.SEMICOLON);
                
            } else if (character == '{') {
                currentToken = new Token(Token.Kind.LCURLYBRACKET);
                
            } else if (character == '}') {
                currentToken = new Token(Token.Kind.RCURLYBRACKET);
                
            } else if (('A' <= character && character <= 'Z') || ('a' <= character && character <= 'z')) {

                String identifierString = Character.toString((char) character);
                while (true) {
                    int peek = peekChar();
                    if (!(
                        ('A' <= peek && peek <= 'Z') || ('a' <= peek && peek <= 'z') || ('0' <= peek && peek <= '9')
                    )) {
                        break;
                    } else {
                        int characterChar = nextChar(in);
                        identifierString = identifierString + Character.toString((char) characterChar);
                    }
                }

                System.out.println(identifierString);

                if (identifierString.equals("Int")) {
                    currentToken = new Token(Token.Kind.INTTYPE);
                } else if (identifierString.equals("mu")) {
                    currentToken = new Token(Token.Kind.MU);
                } else if (identifierString.equals("return")) {
                    currentToken = new Token(Token.Kind.RETURN);
                } else if (identifierString.equals("fn")) {
                    currentToken = new Token(Token.Kind.FN);
                } else if (identifierString.equals("construand")) {
                    currentToken = new Token(Token.Kind.CONSTRUCTAND);
                } else {
                    currentToken = new Token(identifierString);
                }
                

            } else if (character == '-' || ('0' <= character && character <= '9')) {

                String numString = Character.toString((char) character);
                while (true) {
                    int peek = peekChar();
                    if (!('0' <= peek && peek <= '9')) {
                        break;
                    } else {
                        int numChar = nextChar(in);
                        numString = numString + Character.toString((char) numChar);
                    }

                    

                }

                int value = Integer.parseInt(numString);
                
                currentToken = new Token(value);
                

            } else {
                currentToken = new Token(Token.Kind.ERRATIC);
                
            }

        } else {
            currentToken = new Token(Token.Kind.EOF);
            
        }

        

    }

    boolean lexerIsAtStartOfFile = true;

    Token nextParseToken(FileInputStream in) throws IOException {
        
        if (lexerIsAtStartOfFile) {
            lexerIsAtStartOfFile = false;

            currentToken = new Token(""); // dummy value
                
            nextToken(in);
            nextToken(in);

            return prevToken;

        } else {

            nextToken(in);
            return prevToken;

        }

    }

    Token peekParseToken(FileInputStream in) throws IOException {
        if (lexerIsAtStartOfFile) {
            lexerIsAtStartOfFile = false;

            currentToken = new Token(""); // dummy value
            nextToken(in);
            return currentToken;
        } else {
            return currentToken;

        }
    }





    ASTBlock parseBlock(FileInputStream in) throws IOException {
        Token tok = nextParseToken(in);
        if (tok.kind != Token.Kind.LCURLYBRACKET) {
            System.out.println("Expected block to begin here, with '{', for some reason...");
            return null;
        }

        ArrayList<ASTStatement> statements = new ArrayList<ASTStatement>();

        while (true) {
            Token peek = peekParseToken(in);

            if (peek.kind == Token.Kind.RCURLYBRACKET) {
       
                Token junk = nextParseToken(in);
                break;

            } else if (peek.kind == Token.Kind.SEMICOLON) {

                Token junk = nextParseToken(in);
                continue;

            } else {
                ASTStatement statement = parseStatement(in);
                if (statement == null) {return null;}

                statements.add(statement);

                continue;

            }

        }

        return new ASTBlock(statements);
    }  





    ASTType parseType(FileInputStream in) throws IOException {
        
        Token tok = nextParseToken(in);

        if (tok.kind == Token.Kind.LSQUAREBRACKET) {

            Token tok2 = nextParseToken(in);
            if (tok2.kind != Token.Kind.RSQUAREBRACKET) {
                System.out.println("Nonmatching right square bracket in array type!");
                return null;
            }

            ASTType constituentType = parseType(in);
            if (constituentType == null) {return null;}

            return new ASTArrayType(constituentType);

        } else if (tok.kind == Token.Kind.INTTYPE) {

            return new ASTIntType();

        } else {
            System.out.println("Unknown type!");
            return null;
        }

    }

    

    ASTExpr parseExpression(FileInputStream in) throws IOException {
        Token tok = nextParseToken(in);

        if (tok.kind == Token.Kind.INT) {
            int value = tok.integerValue;

            return new ASTIntegerLiteral(value);

        } else if (tok.kind == Token.Kind.LPAREN) {

            ASTExpr expr = parseExpression(in);
            if (expr == null) {return null;}

            Token tok2 = nextParseToken(in);
            if (tok2.kind != Token.Kind.RPAREN) {
                System.out.println("Expected a matching right paren around expression!");
                return null;
            }

            return expr;

        } else if (tok.kind == Token.Kind.IDENTIFIER) {

            String identifier = tok.identifierString;

            Token peek = peekParseToken(in);

            if (peek.kind == Token.Kind.LPAREN) {

                Token junk = nextParseToken(in);

                ArrayList<ASTExpr> args = new ArrayList<ASTExpr>();

                while (true) {

                    Token peek2 = peekParseToken(in);

                    if (peek2.kind == Token.Kind.RPAREN) {

                        Token junk2 = nextParseToken(in);

                        break;

                    } else {

                        

                        ASTExpr arg = parseExpression(in);
                        if (arg == null) {return null;}

                            
                            

                        
                        

                        

                        
                        args.add(arg);

                        Token peek4 = peekParseToken(in);
                        if (peek4.kind == Token.Kind.COMMA) {
                            Token junk3 = nextParseToken(in);
                        }

                        continue;
                    }

                }

                Token peek97 = peekParseToken(in);

                if (peek97.kind == Token.Kind.LSQUAREBRACKET) {

                    ArrayList<ASTExpr> indexings = new ArrayList<ASTExpr>();

                    while (true) {
                        Token peek4 = peekParseToken(in);

                        if (peek4.kind == Token.Kind.LSQUAREBRACKET) {
                            Token junk2 = nextParseToken(in);

                            ASTExpr indexExpr = parseExpression(in);
                            if (indexExpr == null) {return null;}

                            indexings.add(indexExpr);

                            Token tok6 = nextParseToken(in);
                            if (tok6.kind != Token.Kind.RSQUAREBRACKET) {
                                System.out.println("Expected a matching ']' on function call indexing!");
                                return null;
                            }

                            continue;

                        } else {
                            break;
                        }
                    }

                    return new ASTFunctionCallIndexing(new ASTFunctionCall(identifier, args), indexings);

                } else {

                    return new ASTFunctionCall(identifier, args);

                }

            } else if (peek.kind == Token.Kind.LSQUAREBRACKET) {

                ArrayList<ASTExpr> indexings = new ArrayList<ASTExpr>();

                while (true) {
                    Token peek4 = peekParseToken(in);

                    if (peek4.kind == Token.Kind.LSQUAREBRACKET) {
                        Token junk = nextParseToken(in);

                        ASTExpr indexExpr = parseExpression(in);
                        if (indexExpr == null) {return null;}

                        indexings.add(indexExpr);

                        Token tok6 = nextParseToken(in);
                        if (tok6.kind != Token.Kind.RSQUAREBRACKET) {
                            System.out.println("Expected a matching ']' on indexing of identifier '" + identifier + "'!");
                            return null;
                        }

                        continue;

                    } else {
                        break;
                    }
                }
        
                return new ASTIndexing(identifier, indexings);

            } else {

                ArrayList<ASTExpr> emptyIndexings = new ArrayList<ASTExpr>();
                return new ASTIndexing(identifier, emptyIndexings);

            }

        } else {
            System.out.println("Unknown expression!");
            return null;

        }
    }


    ASTStatement parseStatement(FileInputStream in) throws IOException {
        Token tok = nextParseToken(in);

        if (tok.kind == Token.Kind.IDENTIFIER) {

            String identifier = tok.identifierString;

            Token tok2 = nextParseToken(in);

            if (tok2.kind == Token.Kind.LPAREN) {

                ArrayList<ASTExpr> args = new ArrayList<ASTExpr>();

                while (true) {
                    Token peek = peekParseToken(in);

                    if (peek.kind == Token.Kind.RPAREN) {

                        Token junk = nextParseToken(in); // eat ')'

                        break;

                    } else {

                        ASTExpr arg = parseExpression(in);
                        if (arg == null) {return null;}

                        args.add(arg);

                        Token peek24 = peekParseToken(in);

                        if (peek24.kind == Token.Kind.COMMA) {

                            Token junk = nextParseToken(in);

                        }

                        continue;

                       

                    }                    

                }

                return new ASTFunctionCallStatement(identifier, args);


            } else if (tok2.kind == Token.Kind.LSQUAREBRACKET) {

                ArrayList<ASTExpr> indexings = new ArrayList<ASTExpr>();

                while (true) {
                    ASTExpr indexingExpr = parseExpression(in);
                    if (indexingExpr == null) {return null;}

                    Token tok3 = nextParseToken(in);
                    if (tok3.kind != Token.Kind.RSQUAREBRACKET) {
                        System.out.println("Expected a matching ']' on array indexing!");
                        return null;
                    }

                    indexings.add(indexingExpr);

                    Token peek42 = peekParseToken(in);

                    if (peek42.kind == Token.Kind.LSQUAREBRACKET) {
                        continue;
                    } else {
                        break;    
                    }
                }

                ASTIndexing indexing = new ASTIndexing(identifier, indexings);

                Token tok8 = nextParseToken(in);
                if (tok8.kind != Token.Kind.ASSIGNMENTOPERATOR) {
                    System.out.println("Expected an assignment operator '=' after indexing!");
                    return null;
                }

                ASTExpr expr = parseExpression(in);
                if (expr == null) {return null;}

                return new ASTMutation(indexing, expr);

            } else if (tok2.kind == Token.Kind.COLON) {

                ASTType type = parseType(in);
                if (type == null) {return null;}

                Token tok24 = nextParseToken(in);
                if (tok24.kind != Token.Kind.ASSIGNMENTOPERATOR) {
                    System.out.println("Expected an assignment operator here!");
                    return null;
                }

                ASTExpr expr = parseExpression(in);
                if (expr == null) {return null;}

                return new ASTInitialization(false, identifier, type, expr);

            } else if (tok2.kind == Token.Kind.ASSIGNMENTOPERATOR) {

                ArrayList<ASTExpr> emptyIndexings = new ArrayList<ASTExpr>();

                ASTIndexing indexing = new ASTIndexing(identifier, emptyIndexings);

                ASTExpr expr = parseExpression(in);
                if (expr == null) {return null;}

                return new ASTMutation(indexing, expr);

            } else {

                System.out.println("Strange statement -- expected '[' or '(' or ':' or '=' after identifier.");
                return null;

            }

        } else if (tok.kind == Token.Kind.MU) {

            Token tok2 = nextParseToken(in);
            if (tok2.kind != Token.Kind.IDENTIFIER) {
                System.out.println("Expected an identifier after 'mu'!");
                return null;
            }

            String identifier = tok2.identifierString;

            Token tok82 = nextParseToken(in);
            if (tok82.kind != Token.Kind.COLON) {
                System.out.println("Expected a colon after slot name of mutable slot!");
                return null;
            }

            ASTType type = parseType(in);
            if (type == null) {return null;}

            Token tok3 = nextParseToken(in);
            if (tok3.kind != Token.Kind.ASSIGNMENTOPERATOR) {
                System.out.println("Expected an assignment operator after declaration of mutable slot!");
                return null;
            }

            ASTExpr expr = parseExpression(in);
            if (expr == null) {return null;}

            return new ASTInitialization(true, identifier, type, expr);

        } else if (tok.kind == Token.Kind.RETURN) {

            Token peek2 = peekParseToken(in);

            if (peek2.kind == Token.Kind.SEMICOLON) {
                return new ASTReturnStatement(null);
            }

            ASTExpr expr = parseExpression(in);
            if (expr == null) {return null;}

            return new ASTReturnStatement(expr);            

        } else {
            System.out.println("Unknown statement!");
            return null;
        }
    }  


    ASTFunctionDefinition parseFunctionDefinition(FileInputStream in) throws IOException {

        Token tok = nextParseToken(in);

        if (tok.kind != Token.Kind.FN) {
            System.out.println("Expected 'fn' for some reason, here.");
            return null;
        }

        Token tok2 = nextParseToken(in);
        if (tok2.kind != Token.Kind.IDENTIFIER) {
            System.out.println("Expected an identifier after 'fn'!");
            return null;
        }
        
        String identifier = tok2.identifierString;

        Token tok3 = nextParseToken(in);
        if (tok3.kind != Token.Kind.LPAREN) {
            System.out.println("Expected a '(' after function identifier!");
            return null;
        }

        ArrayList<ASTParamDeclaration> params = new ArrayList<ASTParamDeclaration>();

        ASTType returnTypeOrNull = null;

        while (true) {
            Token tok4 = nextParseToken(in);

            if (tok4.kind == Token.Kind.IDENTIFIER) {

                String paramName = tok4.identifierString;

                Token tok5 = nextParseToken(in);
                if (tok5.kind != Token.Kind.COLON) {
                    System.out.println("Expected a colon in param declaration!");
                    return null;
                }

                ASTType paramType = parseType(in);
                if (paramType == null) {return null;}

                Token peek234 = peekParseToken(in);

                ASTParamDeclaration decl = new ASTParamDeclaration(false, false, paramName, paramType);
                params.add(decl);

                if (peek234.kind == Token.Kind.COMMA) {
                    Token junk = nextParseToken(in);
                }

                continue;

            } else if (tok4.kind == Token.Kind.RPAREN) {

                break;

            } else if (tok4.kind == Token.Kind.MU) {

                Token tok45 = nextParseToken(in);
                if (tok45.kind != Token.Kind.IDENTIFIER) {
                    System.out.println("Expected a param identifier after 'mu'!");
                    return null;
                }

                String paramName = tok45.identifierString;

                Token tok5 = nextParseToken(in);
                if (tok5.kind != Token.Kind.COLON) {
                    System.out.println("Expected a colon in param declaration!");
                    return null;
                }

                ASTType paramType = parseType(in);
                if (paramType == null) {return null;}

                Token peek234 = peekParseToken(in);

                ASTParamDeclaration decl = new ASTParamDeclaration(false, true, paramName, paramType);
                params.add(decl);

                if (peek234.kind == Token.Kind.COMMA) {
                    Token junk = nextParseToken(in);
                }

                continue;

            } else if (tok4.kind == Token.Kind.CONSTRUCTAND) {

                Token tok9 = nextParseToken(in);

                if (tok9.kind == Token.Kind.MU) {

                    Token tok45 = nextParseToken(in);
                    if (tok45.kind != Token.Kind.IDENTIFIER) {
                        System.out.println("Expected a param identifier after 'mu'!");
                        return null;
                    }

                    String paramName = tok45.identifierString;

                    Token tok5 = nextParseToken(in);
                    if (tok5.kind != Token.Kind.COLON) {
                        System.out.println("Expected a colon in param declaration!");
                        return null;
                    }

                    ASTType paramType = parseType(in);
                    if (paramType == null) {return null;}

                    Token peek234 = peekParseToken(in);

                    ASTParamDeclaration decl = new ASTParamDeclaration(true, true, paramName, paramType);
                    params.add(decl);

                    if (peek234.kind == Token.Kind.COMMA) {
                        Token junk = nextParseToken(in);
                    }

                    continue;

                } else if (tok9.kind == Token.Kind.IDENTIFIER) {

                    String paramName = tok9.identifierString;

                    Token tok5 = nextParseToken(in);
                    if (tok5.kind != Token.Kind.COLON) {
                        System.out.println("Expected a colon in param declaration!");
                        return null;
                    }

                    ASTType paramType = parseType(in);
                    if (paramType == null) {return null;}

                    Token peek234 = peekParseToken(in);

                    ASTParamDeclaration decl = new ASTParamDeclaration(true, false, paramName, paramType);
                    params.add(decl);

                    if (peek234.kind == Token.Kind.COMMA) {
                        Token junk = nextParseToken(in);
                    }

                    continue;

                } else {

                    System.out.println("Expected an identifier or 'mu' after 'constructand'!");
                    return null;

                }
 
            } else if (tok4.kind == Token.Kind.SHORTLARROW) {

                returnTypeOrNull = parseType(in);
                if (returnTypeOrNull == null) {return null;}

                Token tok5 = nextParseToken(in);
                if (tok5.kind != Token.Kind.RPAREN) {
                    System.out.println("Expected a matching ')' on function declaration head!");
                    return null;
                }
        
                break;

            } else {
                System.out.println("Expected ')' or 'mu' or an identifier here!");
                return null;
            }

        }

        ASTBlock block = parseBlock(in);
        if (block == null) {return null;}

        return new ASTFunctionDefinition(identifier, params, returnTypeOrNull, block);

    }




    public ASTProgram parseProgram() {

        ArrayList<ASTFunctionDefinition> functionDefinitions = new ArrayList<ASTFunctionDefinition>();
        ArrayList<ASTStatement> main = new ArrayList<ASTStatement>();

        FileInputStream in = null;

        try {

            in = new FileInputStream("input.cip");

            while (true) {
                Token peek = peekParseToken(in);

                if (peek.kind == Token.Kind.ERRATIC) {

                    System.out.println("Erratic token!");
                    return null;

                } else if (peek.kind == Token.Kind.EOF) {
                    break;

                } else if (peek.kind == Token.Kind.FN) {
                    ASTFunctionDefinition funDef = parseFunctionDefinition(in);

                    if (funDef != null) {
                        functionDefinitions.add(funDef);
                        continue;

                    } else {
                        return null;
                    }

                } else if (peek.kind == Token.Kind.SEMICOLON) {

                    Token junk = nextParseToken(in);

                    continue;

                } else {

                    ASTStatement statement = parseStatement(in);

                    if (statement != null) {
                        System.out.println("PARSED A STATEMENT!");
            
                        

                        main.add(statement);

                        
                        
                        continue;
                    } else {
                        return null;
                    }

                }
            }

        } catch (IOException e) {
            
            System.out.println("IOException happened!");

        
            
        } finally {
            if (in != null) {
                try {
                    in.close();
                } catch (IOException e) {
                    System.out.println("Exception exception on close!");
                }
            }
        }
        

        // dummy implementation in the lack of a parser:
/*
        ArrayList<ASTFunctionDefinition> functionDefinitions = new ArrayList<ASTFunctionDefinition>();


        ArrayList<ASTParamDeclaration> params = new ArrayList<ASTParamDeclaration>();
        params.add(new ASTParamDeclaration(true, "myParam", new ASTIntType()));
        params.add(new ASTParamDeclaration(true, "myArrayParam", new ASTArrayType(new ASTIntType())));

        ArrayList<ASTStatement> myFunStatements = new ArrayList<ASTStatement>();
        myFunStatements.add(new ASTReturnStatement(new ASTIntegerLiteral(19))); 
       
        ASTFunctionDefinition myFun = new ASTFunctionDefinition("myFun", params, new ASTIntType(), new ASTBlock(myFunStatements));

        functionDefinitions.add(myFun);

        
        ArrayList<ASTParamDeclaration> params2 = new ArrayList<ASTParamDeclaration>();
        params2.add(new ASTParamDeclaration(true, "myParam", new ASTIntType()));
        params2.add(new ASTParamDeclaration(true, "myArrayParam", new ASTArrayType(new ASTIntType())));

        ArrayList<ASTStatement> myFun2Statements = new ArrayList<ASTStatement>(); // empty

        ASTFunctionDefinition myFun2 = new ASTFunctionDefinition("myFun2", params2, null, new ASTBlock(myFun2Statements));

        functionDefinitions.add(myFun2);
        


        ArrayList<ASTStatement> main = new ArrayList<ASTStatement>();

        ArrayList<ASTExpr> args = new ArrayList<ASTExpr>();
        args.add(new ASTIntegerLiteral(25));
        args.add(new ASTBuiltInFunctionCall("allocate", new ArrayList<ASTExpr>()));        

        ASTInitialization xInitialization = new ASTInitialization(true, "x", new ASTIntType(), new ASTFunctionCall("myFun", args));        

        main.add(xInitialization);

        ArrayList<ASTExpr> indexings = new ArrayList<ASTExpr>();
        // indexings.add(new ASTIntegerLiteral(35));

        ASTIndexing indexingExpr = new ASTIndexing("x", indexings);
        
        ASTInitialization initialization = new ASTInitialization(true, "myVariable", new ASTIntType(), indexingExpr);       
    
        main.add(initialization);

        ASTIndexing myVariableIndexing = new ASTIndexing("myVariable", indexings); // reusing empty indexings here
        ASTMutation mutation = new ASTMutation(myVariableIndexing, new ASTIntegerLiteral(13));

        main.add(mutation);

        ArrayList<ASTExpr> args2 = new ArrayList<ASTExpr>();
        args2.add(new ASTIntegerLiteral(58));

        ArrayList<ASTExpr> allocateArgs = new ArrayList<ASTExpr>();
        allocateArgs.add(new ASTIntegerLiteral(8972));
        args2.add(new ASTBuiltInFunctionCall("allocate", allocateArgs));  

        ASTFunctionCallStatement funCallStatement1 = new ASTFunctionCallStatement("myFun2", args2);
        main.add(funCallStatement1);
*/


        return new ASTProgram(functionDefinitions, main);

    }

    

    public boolean parse() {
        ast = parseProgram(); 

        if (ast == null) {
            return false;
        } else {
            return true;
        }
    }

    public boolean typecheck() {
        globalFunTable = new Hashtable<String, TypeSignature>();
        globalSymTable = new Hashtable<String, TypeAnnotation>();       

        boolean typecheckPassed = ast.typecheck(globalFunTable, globalSymTable);

        if (!typecheckPassed) {
            return false;
        }

        return true;
    }

    public void eliminatePassAndPrint() {
        eliminatePass();

        transformedAST.print();





        // DEBUG
        for (ASTFunctionDefinition funDef : transformedAST.functionDefinitions) {
            

            System.out.println(funDef.localIsOwnerTable);

            Enumeration e = funDef.localIsOwnerTable.elements();

            while (e.hasMoreElements())
            {
                BuildAnnotation ba = (BuildAnnotation) e.nextElement();
                System.out.println(Boolean.toString(ba.isOwner) + "; " + Boolean.toString(ba.shouldBeEliminated));        
            }
        }
         
        
    }

    public void generateAndPrintIR() {

        AnonNameGenerator anongen = new AnonNameGenerator();

        ArrayList<IRInstruction> globalInstructions = new ArrayList<IRInstruction>();

        ArrayList<String> slotsMarkedForDestruction = new ArrayList<String>();

        transformedAST.generateGlobalIR(
            globalInstructions, 
            globalFunTable,
            globalSymTable,
            slotsMarkedForDestruction,
            anongen
        );

        for (IRInstruction instr : globalInstructions) {
            System.out.println(instr.print());
        }   

    }

    public void transformAndPrintTransformed() {
        transformedAST = transformProgram();
        transformedAST.print();
        System.out.println(" ");
    }
    
    public static void main(String[] args) {

        SimplifiedCimmplInterpreter interpreter = new SimplifiedCimmplInterpreter();

        boolean parseSuccess = interpreter.parse();
        if (!parseSuccess) {return;}

        boolean typecheckPassed = interpreter.typecheck();
        if (typecheckPassed) {
            System.out.println("Type check passed!");
        } else {
            System.out.println("Type check failed!");
        }

        if (!typecheckPassed) {return;}

        interpreter.markOwnershipPass();

        interpreter.transformAndPrintTransformed();

        interpreter.eliminatePassAndPrint();

        interpreter.lastOccurrencePass();

        interpreter.generateAndPrintIR();

        
        

        /*
        createIntermediaryRepresentation();  // from ast

        interpret();
        */
    }
}
