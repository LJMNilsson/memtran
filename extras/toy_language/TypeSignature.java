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

public class TypeSignature {

    public ArrayList<TypeAnnotation> argTypeAnnotations;

    public ArrayList<Boolean> argConstructandStatuses;
    
    public TypeAnnotation returnTypeAnnotationOrNull;

    public TypeSignature(ArrayList<TypeAnnotation> argTypeAnnotations, ArrayList<Boolean> argConstructandStatuses, TypeAnnotation returnTypeAnnotationOrNull) {
        this.argTypeAnnotations = argTypeAnnotations;
        this.argConstructandStatuses = argConstructandStatuses;
        this.returnTypeAnnotationOrNull = returnTypeAnnotationOrNull;
    }
}
