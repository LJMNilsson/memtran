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



public class ASTArrayType extends ASTType {
    public ASTType constituentType;

    public ASTArrayType(ASTType constituentType) {
        this.constituentType = constituentType;
    }

    public void print() {
        System.out.print("[] ");
        constituentType.print();
    }

    public boolean isInt() {return false;}
    public boolean isArrayType() {return true;}
    public boolean isAnyArrayType() {return false;}

    public boolean identityEquals(ASTType type2) {
        System.out.println("Identity checking ASTArrayType!");

        if (type2.isArrayType()) {
            if (type2.isAnyArrayType()) {
                return true;
            } else {
                return constituentType.identityEquals(((ASTArrayType) type2).constituentType);
            } 

        } else {
            return false;
        }
    }
}
