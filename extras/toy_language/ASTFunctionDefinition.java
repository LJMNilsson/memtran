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

public class ASTFunctionDefinition {
    public String functionName;
    public ArrayList<ASTParamDeclaration> params;
    public ASTType returnTypeOrNull;
    public ASTBlock body;

    public Dictionary<String, TypeAnnotation> localSymTable;

    public Dictionary<String, BuildAnnotation> localIsOwnerTable; // initialized by the findOwnerPass

    public ASTFunctionDefinition(String functionName, ArrayList<ASTParamDeclaration> params, ASTType returnTypeOrNull, ASTBlock body) {
        this.functionName = functionName;
        this.params = params;
        this.returnTypeOrNull = returnTypeOrNull;
        this.body = body;
    }

    public void print() {
        System.out.print("fn " + functionName + "(");
        for (ASTParamDeclaration param : params) {
            param.print();
            System.out.print(",");
        }
        System.out.println(") {");
        for (ASTStatement statement : body.statements) {
            System.out.print("    ");
            statement.print();
        }
        System.out.println("}");
    }

    public boolean typecheck(Dictionary<String, TypeSignature> globalFunTable, Dictionary<String, TypeAnnotation> globalSymTable) {


       

        for (ASTStatement statement : body.statements) {
            boolean success = statement.typecheck(globalFunTable, globalSymTable, localSymTable, returnTypeOrNull);
    
            if (!success) {
                return false;
            }
        }

        return true;

    }

    /*
    public CFunction generateIR() {
        return // TODO
    } 
    */   

}
