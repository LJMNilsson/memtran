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

public class ASTIndexing extends ASTExpr {

    public String identifier;
    public ArrayList<ASTExpr> indexings;

    public boolean isLastOccurrence; // possibly mutated by the lastOccurrencePass

    public ASTIndexing(String identifier, ArrayList<ASTExpr> indexings) {
        this.identifier = identifier;
        this.indexings = indexings;
        this.isLastOccurrence = false;
    }

    public void print() {
        System.out.print(identifier);
        for (ASTExpr indexing : indexings) {
            System.out.print("[");
            indexing.print();
            System.out.print("]");
        }
    }

    public boolean inferType(Dictionary<String, TypeSignature> globalFunTable, Dictionary<String, TypeAnnotation> globalSymTable, Dictionary<String, TypeAnnotation> localSymTable) {
        TypeAnnotation identifierTypeAnnotation = localSymTable.get(identifier);

        if (identifierTypeAnnotation == null) {
            identifierTypeAnnotation = globalSymTable.get(identifier);

            if (identifierTypeAnnotation == null) {
                System.out.println("ASTIndexing: Could not find identifier in symtables.");
                return false;    
            }
        }

        ASTType type = identifierTypeAnnotation.theType;

        for (int i = 0; i < indexings.size(); i++) {
            boolean success = indexings.get(i).inferType(globalFunTable, globalSymTable, localSymTable);

            if (!success) {
                return false;
            }

            if (!indexings.get(i).inferredType.isInt()) {
                System.out.println("ASTIndexing: Index to slot \"" + identifier + "\" is not an Int!");
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
        TypeAnnotation identifierTypeAnnotation = globalSymTable.get(identifier);

        if (identifierTypeAnnotation == null) {
            System.out.println("ASTIndexing: Could not find identifier in global symtable.");
            return false;    
        }

        ASTType type = identifierTypeAnnotation.theType;

        for (int i = 0; i < indexings.size(); i++) {
            boolean success = indexings.get(i).inferType(globalFunTable, globalSymTable);

            if (!success) {
                return false;
            }

            if (!indexings.get(i).inferredType.isInt()) {
                System.out.println("ASTIndexing: Index to slot \"" + identifier + "\" is not an Int!");
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

        

        TypeAnnotation identifierAnnotation = globalSymTable.get(identifier);
        if (identifierAnnotation == null) {
            System.out.println("ASTIndexing couldn't find its identifier '" + identifier + "' in global symtable!");
            return;
        }

        String ident = "@" + identifier;
        String name;

        if (identifierAnnotation.isCompletelyImmutable) {
            name = identifier;
        } else {
            name = "%" + anongen.generate();
            instructions.add(new IRLoadArrayHead(name, new IRRegStackAddress(ident)));
        }
               

        if (indexings.size() > 0) {

            String exprHolder = "%" + anongen.generate();

            ASTExpr indexingExpr = indexings.get(0);

            indexingExpr.generateGlobalIR(
                instructions, globalFunctionTable, globalSymTable, slotsMarkedForDestruction, 
                anongen,
                exprHolder
            );

            String followHolder = "%" + anongen.generate();  // a heap ptr

            instructions.add(new IRCheckBounds(new IRRegInt(exprHolder), new IRRegArrayHead(name)));

            instructions.add(new IRFollowHead(followHolder, new IRRegArrayHead(name), new IRRegInt(exprHolder)));


            if (indexings.size() > 1) {
                for (int i = 1; i < indexings.size() - 1; i++) {

                    

                    String exprHolder3 = "%" + anongen.generate();

                    ASTExpr indexingExpr3 = indexings.get(i);

                    indexingExpr.generateGlobalIR(
                        instructions, globalFunctionTable, globalSymTable, slotsMarkedForDestruction, 
                        anongen,
                        exprHolder3
                    );

                    String headHolder3 = "%" + anongen.generate();

                    instructions.add(new IRLoadArrayHeadAtHeapPtr(headHolder3, new IRRegHeapPtr(followHolder)));

                    followHolder = "%" + anongen.generate(); // reuse this in java

                    instructions.add(new IRCheckBounds(new IRRegInt(exprHolder), new IRRegArrayHead(headHolder3)));

                    instructions.add(new IRFollowHead(followHolder, new IRRegArrayHead(headHolder3), new IRRegInt(exprHolder3))); 

                }

                String exprHolder2 = "%" + anongen.generate();

                ASTExpr indexingExpr2 = indexings.get(indexings.size() - 1);

                indexingExpr2.generateGlobalIR(
                    instructions, globalFunctionTable, globalSymTable, slotsMarkedForDestruction,
                    anongen,
                    exprHolder2
                ); 

                String headHolder2 = "%" + anongen.generate();
                   
                instructions.add(new IRLoadArrayHeadAtHeapPtr(headHolder2, new IRRegHeapPtr(followHolder)));

                followHolder = "%" + anongen.generate(); // reuse this in java

                instructions.add(new IRCheckBounds(new IRRegInt(exprHolder2), new IRRegArrayHead(headHolder2)));

                instructions.add(new IRFollowHead(followHolder, new IRRegArrayHead(headHolder2), new IRRegInt(exprHolder2)));

                if (inferredType.isInt()) {
                    
                    instructions.add(new IRLoadIntAtHeapPtr(returnValueHolder, new IRRegHeapPtr(followHolder)));

                } else {

                    instructions.add(new IRLoadArrayHeadAtHeapPtr(returnValueHolder, new IRRegHeapPtr(followHolder)));

                } 

                    
            } else {  // size == 1 indexing

                if (inferredType.isInt()) {

                    instructions.add(new IRLoadIntAtHeapPtr(returnValueHolder, new IRRegHeapPtr(followHolder)));

                } else {

                    instructions.add(new IRLoadArrayHeadAtHeapPtr(returnValueHolder, new IRRegHeapPtr(followHolder)));
        
                }
                

            }
            
            

        } else { // 0 indexings

            instructions.add(new IRCopyHead(returnValueHolder, new IRRegArrayHead(name)));

        }

    }    



public void generateGlobalIRAndSetCflags(
        ArrayList<IRInstruction> instructions, 
        Dictionary<String, TypeSignature> globalFunctionTable,
        Dictionary<String, TypeAnnotation> globalSymTable,
        ArrayList<String> slotsMarkedForDestruction,
        AnonNameGenerator anongen,
        String returnValueHolder
    ) {

        

        TypeAnnotation identifierAnnotation = globalSymTable.get(identifier);
        if (identifierAnnotation == null) {
            System.out.println("ASTIndexing couldn't find its identifier '" + identifier + "' in global symtable!");
            return;
        }

        String ident = "@" + identifier;
        String name;

        if (identifierAnnotation.isCompletelyImmutable) { // it's never that, actually
            name = identifier;
        } else {
            name = "%" + anongen.generate();
            instructions.add(new IRLoadArrayHead(name, new IRRegStackAddress(ident)));
        }




        String ghostflaggedHeadHolder = "%" + anongen.generate();

        instructions.add(new IRSetCFlag(ghostflaggedHeadHolder, new IRRegArrayHead(name)));
        
        instructions.add(new IRStoreArrayHead(new IRRegStackAddress(ident), new IRRegArrayHead(ghostflaggedHeadHolder)));            
          




        if (indexings.size() > 0) {

            String exprHolder = "%" + anongen.generate();

            ASTExpr indexingExpr = indexings.get(0);

            indexingExpr.generateGlobalIR(
                instructions, globalFunctionTable, globalSymTable, slotsMarkedForDestruction, 
                anongen,
                exprHolder
            );

            String followHolder = "%" + anongen.generate();  // a heap ptr

            instructions.add(new IRCheckBounds(new IRRegInt(exprHolder), new IRRegArrayHead(name)));

            instructions.add(new IRFollowHead(followHolder, new IRRegArrayHead(name), new IRRegInt(exprHolder)));



            


            if (indexings.size() > 1) {
                for (int i = 1; i < indexings.size() - 1; i++) {

                    

                    String exprHolder3 = "%" + anongen.generate();

                    ASTExpr indexingExpr3 = indexings.get(i);

                    indexingExpr.generateGlobalIR(
                        instructions, globalFunctionTable, globalSymTable, slotsMarkedForDestruction, 
                        anongen,
                        exprHolder3
                    );

                    String headHolder3 = "%" + anongen.generate();

                    instructions.add(new IRLoadArrayHeadAtHeapPtr(headHolder3, new IRRegHeapPtr(followHolder)));

                    followHolder = "%" + anongen.generate(); // reuse this in java

                    instructions.add(new IRCheckBounds(new IRRegInt(exprHolder), new IRRegArrayHead(headHolder3)));

                    instructions.add(new IRFollowHead(followHolder, new IRRegArrayHead(headHolder3), new IRRegInt(exprHolder3)));



                    String unghostflaggedHeadHolder = "%" + anongen.generate();

                    instructions.add(new IRLoadArrayHeadAtHeapPtr(unghostflaggedHeadHolder, new IRRegHeapPtr(followHolder)));

                    String ghostflaggedHeadHolder2 = "%" + anongen.generate();

                    instructions.add(new IRSetCFlag(ghostflaggedHeadHolder2, new IRRegArrayHead(unghostflaggedHeadHolder)));
                    instructions.add(new IRStoreArrayHeadAtHeapPtr(new IRRegHeapPtr(followHolder), new IRRegArrayHead(ghostflaggedHeadHolder2))); 

                }

                String exprHolder2 = "%" + anongen.generate();

                ASTExpr indexingExpr2 = indexings.get(indexings.size() - 1);

                indexingExpr2.generateGlobalIR(
                    instructions, globalFunctionTable, globalSymTable, slotsMarkedForDestruction,
                    anongen,
                    exprHolder2
                ); 

                String headHolder2 = "%" + anongen.generate();
                   
                instructions.add(new IRLoadArrayHeadAtHeapPtr(headHolder2, new IRRegHeapPtr(followHolder)));

                followHolder = "%" + anongen.generate(); // reuse this in java

                instructions.add(new IRCheckBounds(new IRRegInt(exprHolder2), new IRRegArrayHead(headHolder2)));

                instructions.add(new IRFollowHead(followHolder, new IRRegArrayHead(headHolder2), new IRRegInt(exprHolder2)));

                

                instructions.add(new IRLoadArrayHeadAtHeapPtr(returnValueHolder, new IRRegHeapPtr(followHolder)));

                String ghostflaggedHeadHolder3 = "%" + anongen.generate();

                instructions.add(new IRSetCFlag(ghostflaggedHeadHolder3, new IRRegArrayHead(returnValueHolder)));
                instructions.add(new IRStoreArrayHeadAtHeapPtr(new IRRegHeapPtr(followHolder), new IRRegArrayHead(ghostflaggedHeadHolder3))); 

                    
            } else {  // size == 1 indexing

               

                

                instructions.add(new IRLoadArrayHeadAtHeapPtr(returnValueHolder, new IRRegHeapPtr(followHolder)));
        
                String ghostflaggedHeadHolder4 = "%" + anongen.generate();

                instructions.add(new IRSetCFlag(ghostflaggedHeadHolder4, new IRRegArrayHead(returnValueHolder)));
                instructions.add(new IRStoreArrayHeadAtHeapPtr(new IRRegHeapPtr(followHolder), new IRRegArrayHead(ghostflaggedHeadHolder4))); 
                

            }
            
            

        } else { // 0 indexings

            instructions.add(new IRCopyHead(returnValueHolder, new IRRegArrayHead(ghostflaggedHeadHolder)));

            

        }

    }    
}
