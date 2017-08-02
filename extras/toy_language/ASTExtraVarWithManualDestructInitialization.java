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

public class ASTExtraVarWithManualDestructInitialization extends ASTStatement { // is always immutable
    public String identifier;
    public ASTType type;
    public ASTExpr expr;

    public ASTExtraVarWithManualDestructInitialization(String identifier, ASTType type, ASTExpr expr) {
        this.identifier = identifier;
        this.type = type;
        this.expr = expr;
    }

    public void print() {
        System.out.print("manualdestruct ");
        System.out.print(identifier + " : ");
        type.print();
        System.out.print(" = ");
        expr.print();
        System.out.println(";");
    }

    public boolean typecheck(                              // dummy. (These vars are inserted after typecheck)
        Dictionary<String, TypeSignature> globalFunTable, 
        Dictionary<String, TypeAnnotation> globalSymTable, 
        Dictionary<String, TypeAnnotation> localSymTable,
        ASTType returnTypeOrNull
    ) {
        return true;
    }

    public boolean typecheck(Dictionary<String, TypeSignature> globalFunTable, Dictionary<String, TypeAnnotation> globalSymTable) {
        return true; // dummy
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
