# Copyright (C) 2017 Martin Nilsson


# This file is part of the Memtran compiler.
#
#     The Memtran compiler is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
# 
#     The Memtran compiler is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
# 
#     You should have received a copy of the GNU General Public License
#     along with the Memtran compiler.  If not, see http://www.gnu.org/licenses/ . 



NOT_IMPLEMENTED = "You should implement this!"


class NIdentifier:

    # public long lineNr;
    # public long rowNr;
    # String name;

    def __init__(self, lineNr,
        rowNr,
        name):
    
        self.lineNr = lineNr
        self.rowNr = rowNr
        self.name = name

    

    def print_it(self):
        print("$", end='')
        print(self.name, end='')
    

    def get_line_nr(self):
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr

    def create_copy(self):
        return NIdentifier(self.lineNr, self.rowNr, self.name)
    

    def accept_visitor(self, visitor):
        return visitor.visit(self)    # leaf element




##################### TYPES ###################################


class NType:
    # abstract void print();

    # abstract long getLineNr();

    # abstract long getRowNr();

    # abstract NType createCopy();

    # abstract Any (default boolean) accept_visitor(AbstractASTVisitor visitor); 

    pass



    




class NIdentifierType(NType):

    # long lineNr;
    # long rowNr;
    # NIdentifier moduleNameOrNull;
    # NIdentifier name;

    def __init__(self, lineNr,
        rowNr,
        moduleNameOrNull,
        name):

        self.lineNr = lineNr
        self.rowNr = rowNr
        self.moduleNameOrNull = moduleNameOrNull
        self.name = name

    

    def print_it(self):

        if not self.moduleNameOrNull is None:
            self.moduleNameOrNull.print_it()
            print("..", end='')
        
        self.name.print_it()
        
    

    def get_line_nr(self):
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr

    def create_copy(self):
        if self.moduleNameOrNull is None:
            return NIdentifierType(self.lineNr, self.rowNr, None, self.name.create_copy())
        else:
            return NIdentifierType(self.lineNr, self.rowNr, self.moduleNameOrNull.create_copy(), self.name.create_copy())
    
    def accept_visitor(self, visitor):
        if not self.moduleNameOrNull is None:
            success = self.moduleNameOrNull.accept_visitor(visitor)
            if success == False:
                return False

        success = self.name.accept_visitor(visitor)
        if success == False:
            return False

        return visitor.visit(self) 
    


class NNilType(NType):

    # long lineNr;
    # long rowNr;

    def __init__(self, lineNr,
        rowNr):

        self.lineNr = lineNr
        self.rowNr = rowNr

    

    def print_it(self):
        print("Nil", end='')
    

    def get_line_nr(self):
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr

    def create_copy(self):
        return NNilType(self.lineNr, self.rowNr)


    def accept_visitor(self, visitor):
        return visitor.visit(self)     # concrete element




class NBoolType(NType):

    # long lineNr;
    # long rowNr;

    def __init__(self, lineNr,
        rowNr):

        self.lineNr = lineNr
        self.rowNr = rowNr

    

    def print_it(self):
        print("Bool", end='')
    

    def get_line_nr(self):
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr

    def create_copy(self):
        return NBoolType(self.lineNr, self.rowNr)

    def accept_visitor(self, visitor):
        return visitor.visit(self)     # concrete element
    
    

class NI8Type(NType):

    # long lineNr;
    # long rowNr;

    def __init__(self, lineNr,
        rowNr):
        self.lineNr = lineNr
        self.rowNr = rowNr

    def print_it(self):
        print("I8", end='')
    
    def get_line_nr(self): 
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr

    def create_copy(self):
        return NI8Type(self.lineNr, self.rowNr)

    def accept_visitor(self, visitor):
        return visitor.visit(self)    # concrete element



class NI16Type(NType):

    # long lineNr;
    # long rowNr;

    def __init__(self, lineNr,
        rowNr):
        self.lineNr = lineNr
        self.rowNr = rowNr

    def print_it(self):
        print("I16", end='')
    
    def get_line_nr(self): 
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr

    def create_copy(self):
        return NI16Type(self.lineNr, self.rowNr)

    def accept_visitor(self, visitor):
        return visitor.visit(self)     # concrete element




class NI32Type(NType):

    # long lineNr;
    # long rowNr;

    def __init__(self, lineNr,
        rowNr):
        self.lineNr = lineNr
        self.rowNr = rowNr

    def print_it(self):
        print("I32", end='')
    
    def get_line_nr(self): 
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr

    def create_copy(self):
        return NI32Type(self.lineNr, self.rowNr)

    def accept_visitor(self, visitor):
        return visitor.visit(self)     # concrete element





class NI64Type(NType):

    # long lineNr;
    # long rowNr;

    def __init__(self, lineNr,
        rowNr):
        self.lineNr = lineNr
        self.rowNr = rowNr

    def print_it(self):
        print("I64", end='')
    
    def get_line_nr(self): 
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr

    def create_copy(self):
        return NI64Type(self.lineNr, self.rowNr)

    def accept_visitor(self, visitor):
        return visitor.visit(self)     # concrete element




class NISizeType(NType):

    # long lineNr;
    # long rowNr;

    def __init__(self, lineNr,
        rowNr):
        self.lineNr = lineNr
        self.rowNr = rowNr

    def print_it(self):
        print("Int", end='')
    
    def get_line_nr(self): 
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr

    def create_copy(self):
        return NISizeType(self.lineNr, self.rowNr)

    def accept_visitor(self, visitor):
        return visitor.visit(self)     # concrete element




class NU8Type(NType):

    # long lineNr;
    # long rowNr;

    def __init__(self, lineNr,
        rowNr):
        self.lineNr = lineNr
        self.rowNr = rowNr

    def print_it(self):
        print("U8", end='')
    
    def get_line_nr(self): 
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr

    def create_copy(self):
        return NU8Type(self.lineNr, self.rowNr)

    def accept_visitor(self, visitor):
        return visitor.visit(self)    # concrete element





class NU16Type(NType):

    # long lineNr;
    # long rowNr;

    def __init__(self, lineNr,
        rowNr):
        self.lineNr = lineNr
        self.rowNr = rowNr

    def print_it(self):
        print("U16", end='')
    
    def get_line_nr(self): 
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr

    def create_copy(self):
        return NU16Type(self.lineNr, self.rowNr)

    def accept_visitor(self, visitor):
        return visitor.visit(self)    # concrete element





class NU32Type(NType):

    # long lineNr;
    # long rowNr;

    def __init__(self, lineNr,
        rowNr):
        self.lineNr = lineNr
        self.rowNr = rowNr

    def print_it(self):
        print("U32", end='')
    
    def get_line_nr(self): 
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr

    def create_copy(self):
        return NU32Type(self.lineNr, self.rowNr)

    def accept_visitor(self, visitor):
        return visitor.visit(self)     # concrete element




class NU64Type(NType):

    # long lineNr;
    # long rowNr;

    def __init__(self, lineNr,
        rowNr):
        self.lineNr = lineNr
        self.rowNr = rowNr

    def print_it(self):
        print("U64", end='')
    
    def get_line_nr(self): 
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr

    def create_copy(self):
        return NU64Type(self.lineNr, self.rowNr)

    def accept_visitor(self, visitor):
        return visitor.visit(self)     # concrete element




class NUSizeType(NType):

    # long lineNr;
    # long rowNr;

    def __init__(self, lineNr,
        rowNr):
        self.lineNr = lineNr
        self.rowNr = rowNr

    def print_it(self):
        print("UInt", end='')
    
    def get_line_nr(self): 
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr

    def create_copy(self):
        return NUSizeType(self.lineNr, self.rowNr)

    def accept_visitor(self, visitor):
        return visitor.visit(self)     # concrete element




class NF32Type(NType):

    # long lineNr;
    # long rowNr;

    def __init__(self, lineNr,
        rowNr):
        self.lineNr = lineNr
        self.rowNr = rowNr

    def print_it(self):
        print("F32", end='')
    
    def get_line_nr(self): 
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr

    def create_copy(self):
        return NF32Type(self.lineNr, self.rowNr)

    def accept_visitor(self, visitor):
        return visitor.visit(self)     # concrete element
    



class NF64Type(NType):

    # long lineNr;
    # long rowNr;

    def __init__(self, lineNr,
        rowNr):
        self.lineNr = lineNr
        self.rowNr = rowNr

    def print_it(self):
        print("F64", end='')
    
    def get_line_nr(self): 
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr

    def create_copy(self):
        return NF64Type(self.lineNr, self.rowNr)

    def accept_visitor(self, visitor):
        return visitor.visit(self)     # concrete element




class NDynamicArrayType(NType):
    # long lineNr;
    # long rowNr;
    
    # NType valueType;

    def __init__ (self, lineNr,
        rowNr,
        valueType):

        self.lineNr = lineNr
        self.rowNr = rowNr
        self.valueType = valueType

    

    def print_it(self):
        print("([]", end='')
        self.valueType.print_it()
        print(")", end='')
    

    def get_line_nr(self):
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr

    def create_copy(self):
        return NDynamicArrayType(self.lineNr, self.rowNr, self.valueType.create_copy())    
    
    
    def accept_visitor(self, visitor):
        success = self.valueType.accept_visitor(visitor)
        if success == False:
            return False

        return visitor.visit(self) 









class NStructTypeMember:

    # long lineNr;
    # long rowNr;
    # NIdentifier name;
    # NType theType;

    def __init__(self, lineNr,
        rowNr,
        name,
        theType):

        self.lineNr = lineNr
        self.rowNr = rowNr
        self.name = name
        self.theType = theType

    

    def print_it(self):
        self.name.print_it()
        print(" : ", end='')
        self.theType.print_it()
        print("; ", end='')
    

    def get_line_nr(self):
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr
    
    def create_copy(self):
        return NStructTypeMember(self.lineNr, self.rowNr, self.name.create_copy(), self.theType.create_copy())
    

    def accept_visitor(self, visitor):
        success = self.name.accept_visitor(visitor)
        if success == False:
            return False

        success = self.theType.accept_visitor(visitor)    
        if success == False:
            return False

        return visitor.visit(self)


class NStructType(NType):

    # long lineNr;
    # long rowNr;
    # NIdentifier tag;
    # ArrayList<NStructTypeMember> members;

    def __init__(self, lineNr,
        rowNr,
        tag,
        members):

        self.lineNr = lineNr
        self.rowNr = rowNr
        self.tag = tag
        self.members = members

    

    def print_it(self):
        print("'", end='')
        self.tag.print_it()
        print("'{", end='')
        for m in self.members:
            m.print_it()
        
        print("}", end='')
    

    def get_line_nr(self):
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr

    def create_copy(self):
        membersCopy = []
        for m in self.members:           # I guess there is a prettier way available.....
            membersCopy.append(m.create_copy())
        
        return NStructType(self.lineNr, self.rowNr, self.tag.create_copy(), membersCopy)
    

    def accept_visitor(self, visitor):
        success = self.tag.accept_visitor(visitor)
        if success == False:
            return False

        for member in self.members:
            success = member.accept_visitor(visitor)
            if success == False:
                return False

        return visitor.visit(self)


class NVariantBoxType(NType):

    # long lineNr;
    # long rowNr;
    # ArrayList<NType> types;

    def __init__(self, lineNr,
        rowNr,
        types):

        self.lineNr = lineNr
        self.rowNr = rowNr
        self.types = types

    

    def print_it(self):
        print("(", end='')
        if len(self.types) < 2:
            print("ERRATIC VARIANT-BOX TYPE!", end='')
        else:
            self.types[0].print_it()
            for i in range(1, len(self.types)):
                print(" / ", end='')
                self.types[i].print_it()
            
        
        print(")", end='')
    

    def get_line_nr(self):
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr

    def create_copy(self):
        typesCopy = []
        for t in self.types:
            typesCopy.append(t.create_copy())  # (Surely cooler ways to do this, but nevermind)
        

        return NVariantBoxType(self.lineNr, self.rowNr, typesCopy)
    

    def accept_visitor(self, visitor):
        for t in self.types:
            success = t.accept_visitor(visitor)
            if success == False:
                return False

        return visitor.visit(self)


class NTypeArg:

    # abstract void print();

    # abstract long getLineNr();

    # abstract long getRowNr();

    # abstract NTypeArg createCopy();

    # abstract Any accept_visitor(AbstractASTVisitor visitor);

    pass    



class NNormalTypeArg(NTypeArg):

    # long lineNr;
    # long rowNr;
    # boolean isMu;
    # boolean isConstruand;
    # NType argType;

    def __init__(self, lineNr,
        rowNr,
        isMu,
        isConstruand,
        argType):

        self.lineNr = lineNr
        self.rowNr = rowNr
        self.isMu = isMu
        self.isConstruand = isConstruand
        self.argType = argType

    

    def print_it(self):
        if self.isMu: 
            print("mu ", end='')
        
        if self.isConstruand:
            print("construand ", end='')
        
        self.argType.print_it()
    

    def get_line_nr(self):
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr

    def create_copy(self):
        return NNormalTypeArg(self.lineNr, self.rowNr, self.isMu, self.isConstruand, self.argType.create_copy())
    

    def accept_visitor(self, visitor):
        success = self.argType.acceptVisitor(visitor)
        if success == False:
            return False

        return visitor.visit(self)



class NRefTypeArg(NTypeArg):
    # long lineNr;
    # long rowNr;
    # NType argType;

    def __init__(
        self,
        lineNr,
        rowNr,
        argType
    ):

        self.lineNr = lineNr
        self.rowNr = rowNr
        self.argType = argType

    

    def print_it(self):
        print("ref ", end='')
        self.argType.print_it()
    

    def get_line_nr(self):
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr

    def create_copy(self):
        return NRefTypeArg(self.lineNr, self.rowNr, self.argType.create_copy())
    

    def accept_visitor(self, visitor):
        success = self.argType.accept_visitor(visitor)
        if success == False:
            return False

        return visitor.visit(self)





class NFunctionType(NType):
    # long lineNr;
    # long rowNr;
    # ArrayList<NTypeArg> typeArgs;
    # ArrayList<NType> returnTypes;

    def __init__(self, lineNr,
        rowNr,
        typeArgs,
        returnTypes):

        self.lineNr = lineNr
        self.rowNr = rowNr
        self.typeArgs = typeArgs
        self.returnTypes = returnTypes

    

    def print_it(self):
        print("Fn(", end='')
        if len(self.typeArgs) > 0:
            self.typeArgs[0].print_it()
            for i in range(1, len(self.typeArgs)):
                print(", ", end='')
                self.typeArgs[i].print_it()
   
        
        if len(self.returnTypes) > 0:
            print(" => ", end='')
            for i in range(0, len(self.returnTypes) - 1):
                self.returnTypes[i].print_it()
                print(", ", end='')
            
            self.returnTypes[len(self.returnTypes) - 1].print_it()
         
        print(")", end='')
    

    def get_line_nr(self):
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr

    def create_copy(self):
        typeArgsCopy = []
        for ta in self.typeArgs:
            typeArgsCopy.append(ta.create_copy()) # (There are cooler ways to do it definitely)
            

        returnTypesCopy = []
        for rt in self.returnTypes:
            returnTypesCopy.append(rt.create_copy())
        

        return NFunctionType(self.lineNr, self.rowNr, typeArgsCopy, returnTypesCopy)
    

    def accept_visitor(self, visitor):
        for typeArg in self.typeArgs:
            success = typeArg.accept_visitor(visitor)
            if success == False:
                return False

        for returnType in self.returnTypes:
            success = returnType.accept_visitor(visitor)
            if success == False:
                return False

        return visitor.visit(self)



class NParametrizedIdentifierType(NType):

    # long lineNr;
    # long rowNr;
    # NIdentifierType name;
    # ArrayList<NType> params; 

    def __init__(self, lineNr,
        rowNr,
        name,
        params):

        self.lineNr = lineNr
        self.rowNr = rowNr
        self.name = name
        self.params = params
    

    def print_it(self):
        self.name.print_it()
        print("(", end='')
        if len(self.params) < 1:
            print("ERRATIC PARAMETRIZED TYPE!", end='')
        else:
            for i in range(0, len(self.params) - 1):
                self.params[i].print_it()
                print(", ", end='')
            
            self.params[len(self.params) - 1].print_it()
        
        print(")", end='')
    

    def get_line_nr(self):
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr

    def create_copy(self):
        paramsCopy = []
        for p in self.params:
            paramsCopy.append(p.create_copy())
        

        return NParametrizedIdentifierType(self.lineNr, self.rowNr, self.name.create_copy(), paramsCopy)
    

    def accept_visitor(self, visitor):
        success = self.name.accept_visitor(visitor)
        if success == False:
            return False

        for param in self.params:
            success = param.accept_visitor(visitor)
            if success == False:
                return False

        return visitor.visit(self) 




#################### EXPRESSIONS ##############################


class NExpression:
    pass

    # NType inferredType = null;

    # boolean isValidLValue;

    # abstract void print();
    
    # abstract long getLineNr();

    # abstract long getRowNr();

    # abstract NExpression create_copy();



class NIdentifierExpression(NExpression):

    # public long lineNr;
    # public long rowNr;
    # public NIdentifier moduleNameOrNull;
    # public NIdentifier name;
    # public ArrayList<NIndexingIndex> indexings;

    # TODO: Find out and document how the indexings are supposed to be parsed/used

    def __init__(self, lineNr,
        rowNr,
        moduleNameOrNull,
        name,
        indexings
    ):
        
        self.lineNr = lineNr
        self.rowNr = rowNr
        self.moduleNameOrNull = moduleNameOrNull
        self.name = name
        self.indexings = indexings
        self.isValidLValue = True

    

    def print_it(self):
        if not self.moduleNameOrNull is None:
            self.moduleNameOrNull.print_it()
            print("::", end='')
        
        self.name.print_it()
        for ii in self.indexings:
            ii.print_it()
        
    

    def get_line_nr(self): 
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr

    
    def create_copy(self):
        indexingsCopy = []
        for indexing in self.indexings:
            indexingsCopy.append(indexing.create_copy())

        if self.moduleNameOrNull is None:
            return NIdentifierExpression(self.lineNr, self.rowNr, None, self.name.create_copy(), indexingsCopy)
        else:
            return NIdentifierExpression(self.lineNr, self.rowNr, self.moduleNameOrNull.create_copy(), self.name.create_copy(), indexingsCopy)        




class NIndexingIndex:

    # abstract void print();
    
    # abstract long getLineNr();

    # abstract long getRowNr();

    # abstract NIndexingIndex create_copy()

    pass




class NNilExpression(NExpression):

    # long lineNr;
    # long rowNr;

    def __init__(self, lineNr,
        rowNr):

        self.lineNr = lineNr
        self.rowNr = rowNr
        self.isValidLValue = False    

    

    def print_it(self):
        print("nil", end='')
    

    def get_line_nr(self): 
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr

    def create_copy(self):
        return NNilExpression(self.lineNr, self.rowNr) # no copying actually needed for literals, but whatever
    



class NTrueExpression(NExpression):

    # long lineNr;
    # long rowNr;

    def __init__(self, lineNr,
        rowNr):

        self.lineNr = lineNr
        self.rowNr = rowNr
        self.isValidLValue = False    

    

    def print_it(self):
        print("true", end='')
    

    def get_line_nr(self): 
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr

    def create_copy(self):
        return NTrueExpression(self.lineNr, self.rowNr)   # no copying actually needed for literals, but whatever
    





class NFalseExpression(NExpression):

    # long lineNr;
    # long rowNr;

    def __init__(self, lineNr,
        rowNr):

        self.lineNr = lineNr
        self.rowNr = rowNr
        self.isValidLValue = False    

    

    def print_it(self):
        print("false", end='')
    

    def get_line_nr(self): 
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr

    def create_copy(self):
        return NFalseExpression(self.lineNr, self.rowNr) # no copying actually needed for literals, but whatever
    




class NIntegerExpression(NExpression):

    # public long lineNr;
    # public long rowNr;
    # public String value;
    # public boolean isNegative;

    def __init__(self, lineNr,
        rowNr,
        value,
        isNegative):

        self.lineNr = lineNr
        self.rowNr = rowNr
        self.value = value
        self.isNegative = isNegative
        self.isValidLValue = False
    

    def print_it(self):
        if self.isNegative:
           print("-", end='')
        
        print("#", end='')
        print(self.value, end='')
    

    def get_line_nr(self): 
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr

    def create_copy(self):
        return NIntegerExpression(self.lineNr, self.rowNr, self.value, self.isNegative)
       






class NFloatingPointNumberExpression(NExpression):

    # long lineNr;
    # long rowNr;
    # String value;
    # boolean isNegative;

    def __init__(self, lineNr,
        rowNr,
        value,
        isNegative ):

        self.lineNr = lineNr
        self.rowNr = rowNr
        self.value = value
        self.isNegative = isNegative
        self.isValidLValue = False    

    def print_it(self):
        if self.isNegative:
            print("-", end='')
        
        print("##", end='')
        print(self.value, end='')
    

    def get_line_nr(self):
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr

    def create_copy(self):
        return NFloatingPointNumberExpression(self.lineNr, self.rowNr, self.value, self.isNegative)
    



class NStringExpression(NExpression):

    # long lineNr;
    # long rowNr;
    # String value;  
 
    def __init__(self, lineNr,
        rowNr,
        value ):

        self.lineNr = lineNr
        self.rowNr = rowNr
        self.value = value
        self.isValidLValue = False

    

    def print_it(self):
        print("\"", end='')
        print(self.value, end='') 
        print("\"", end='')  # funny printing of cr:s and newlines though
    

    def get_line_nr(self):
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr

    def create_copy(self):
        return NStringExpression(self.lineNr, self.rowNr, self.value)
    







class NArrayExpressionIndividualValues(NExpression):

    # long lineNr;
    # long rowNr;
    # ArrayList<NExpression> values;

    def __init__(
        self,
        lineNr,
        rowNr,
        values
    ):

        self.lineNr = lineNr
        self.rowNr = rowNr
        self.values = values
        self.isValidLValue = False
    

    def print_it(self):
        print("#[", end='')
        if len(self.values) > 0:        
            for i in range(0, len(self.values) - 1):
                self.values[i].print_it()
                print(", ", end='')
            
            self.values[len(self.values) - 1].print_it()
        
        print("]", end='')
    

    def get_line_nr(self): 
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr

    
    def create_copy(self):
        valuesCopy = []
        for value in self.values:
            valuesCopy.append(value.create_copy())

        return NArrayExpressionIndividualValues(self.lineNr, self.rowNr, valuesCopy)
    


class NArrayExpressionNoInitialization(NExpression):

    # long lineNr;
    # long rowNr;
    # boolean isUninitialized;  // if false, it is "trash"
    # NExpression length;

    def __init__(
        self,
        lineNr,
        rowNr,
        isUninitialized,
        length
    ):
        self.lineNr = lineNr
        self.rowNr = rowNr
        self.isUninitialized = isUninitialized
        self.length = length
        self.isValidLValue = False
    

    def print_it(self):
        print("#[", end='')
        if self.isUninitialized:
            print("uninitialized ", end='')
        else:
            print("trash ", end='')
        
        self.length.print_it()
        print("]", end='')
    

    def get_line_nr(self): 
        return self.lineNr
    
    def get_row_nr(self): 
        return self.rowNr


    def create_copy(self):
        return NArrayExpressionNoInitialization(self.lineNr, self.rowNr, self.inUninitialized, self.length.create_copy())



class NArrayExpressionRepeatedValue(NExpression):

    # long lineNr;
    # long rowNr;
    # NExpression repeatedValue;
    # NExpression length;

    def __init__(
        self,
        lineNr,
        rowNr,
        repeatedValue,
        length
    ):

        self.lineNr = lineNr
        self.rowNr = rowNr
        self.repeatedValue = repeatedValue
        self.length = length
        self.isValidLValue = False
    

    def print_it(self):
        print("#[", end='')
        self.repeatedValue.print_it()
        print(" repeat ", end='')        
        self.length.print_it()
        print("]", end='')
    

    def get_line_nr(self): 
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr

    
    def create_copy(self):
        return NArrayExpressionRepeatedValue(self.lineNr, self.rowNr, self.repeatedValue.createCopy(), self.length.createCopy())



class NStructExpressionPost:

    # long lineNr;
    # long rowNr;
    # NIdentifier name;
    # NExpression value;

    def __init__(
        self,
        lineNr,
        rowNr,
        name,
        value
    ):
        self.lineNr = lineNr
        self.rowNr = rowNr
        self.name = name
        self.value = value
        
    

    def print_it(self):
        self.name.print_it()
        print(" = ", end='')
        self.value.print_it()
        print("; ", end='')
    

    def get_line_nr(self): 
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr

    
    def create_copy(self):
        return NStructExpressionPost(self.lineNr, self.rowNr, self.name.create_copy(), self.value.create_copy())    





class NStructExpression(NExpression):

    # long lineNr;
    # long rowNr;
    # NIdentifier tag;
    # ArrayList<NStructExpressionPost> posts;

    def __init__(
        self,
        lineNr,
        rowNr,
        tag,
        posts
    ):
        self.lineNr = lineNr
        self.rowNr = rowNr
        self.tag = tag
        self.posts = posts
        self.isValidLValue = False
    

    def print_it(self):
        print("#'", end='')
        self.tag.print_it()
        print("'{", end='')
        for post in self.posts:
            post.print_it()
        
        print("}", end='')
    

    def get_line_nr(self): 
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr


    def create_copy(self):
        postsCopy = []
        for post in self.posts:
            postsCopy.append(post.create_copy())

        return NStructExpression(self.lineNr, self.rowNr, self.tag.create_copy(), postsCopy)




class NVariantBoxExpression(NExpression):

    # long lineNr;
    # long rowNr;
    # NExpression expression;    

    def __init__(self, lineNr, rowNr, expression):
        self.lineNr = lineNr
        self.rowNr = rowNr
        self.expression = expression

    def print_it(self):
        print("#/", end='')
        self.expression.print_it()
        print("\\", end='')

    def get_line_nr(self): 
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr

    
    def create_copy(self):
        return NVariantBoxExpression(self.lineNr, self.rowNr, self.expression.create_copy())




class NTypeClarifiedExpression(NExpression):

    # long lineNr;
    # long rowNr;
    # NExpression expression;
    # NType theType;

    def __init__(self, lineNr,
        rowNr,
        expression,
        theType):
    
        self.lineNr = lineNr
        self.rowNr = rowNr
        self.expression = expression
        self.theType = theType        
        self.isValidLValue = False # because it is only used when "expression" isn't a simple identifier expression
    

    def print_it(self):
        print("(", end='')
        self.expression.print_it()
        print(" ::: ", end='')
        self.theType.print_it()
        print(")", end='')
    

    def get_line_nr(self): 
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr

    
    def create_copy(self):
        return NTypeClarifiedExpression(self.lineNr, self.rowNr, self.expression.create_copy(), self.theType.create_copy())






#    These classes have an NIndexingIndex:
#
#      - NIdentifierExpression: type clarification indexings, array indexings, struct indexings, ortype cast indexings
#       - NIndexing : same kinds of indexings -- used for general indexing on expressions    
#
#    Subclasses:
#
#        -NArrayIndexingIndex
#        -NStructIndexingIndex
#        -NTypeClarificationIndex   // this may should be allowed in lvalues too, for interesting reasons
#        -NOrtypeCastIndex


class NArrayIndexing(NExpression):

    # -- this class is to be used in the "general case"

    # long lineNr;
    # long rowNr;
    # NExpression arrayExpression;
    # NExpression indexExpression;

    def __init__(
        self, 
        lineNr,
        rowNr,
        arrayExpression,
        indexExpression
    ):

        self.lineNr = lineNr
        self.rowNr = rowNr
        self.arrayExpression = arrayExpression
        self.indexExpression = indexExpression
        self.isValidLValue = False # because it is only used when "arrayExpression" isn't a valid lvalue
    

    def print_it(self):
        print("(", end='')
        self.arrayExpression.print_it()
        print("[", end='')
        self.indexExpression.print_it()
        print("])", end='')
    

    def get_line_nr(self):
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr

    
    def create_copy(self):
        return NArrayIndexing(self.lineNr, self.rowNr, self.arrayExpression.create_copy(), self.indexExpression.create_copy())




class NArrayIndexingIndex(NIndexingIndex):

    # long lineNr;
    # long rowNr;
    # NExpression indexExpression;

    def __init__ (self, lineNr,
        rowNr,
        indexExpression):

        self.lineNr = lineNr
        self.rowNr = rowNr
        self.indexExpression = indexExpression

    

    def print_it(self):
        print("[", end='')
        self.indexExpression.print_it()
        print("]", end='')
    

    def get_line_nr(self): 
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr


    def create_copy(self):
        return NArrayIndexingIndex(self.lineNr, self.rowNr, self.indexExpression.create_copy()) 
    



class NStructIndexing(NExpression):

    # long lineNr;
    # long rowNr;
    # NExpression structExpression;
    # NIdentifier indexName;

    def __init__(self, lineNr,
        rowNr,
        structExpression,
        indexName):

        self.lineNr = lineNr
        self.rowNr = rowNr
        self.structExpression = structExpression
        self.indexName = indexName
        self.isValidLValue = False   # because it is only used when "structExpression" isn't a valid lvalue
    

    def print_it(self):
        print("(", end='')
        self.structExpression.print_it()
        print(".", end='')
        self.indexName.print_it()
        print(")", end='')
    

    def get_line_nr(self): 
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr


    def create_copy(self):
        return NStructIndexing(self.lineNr, self.rowNr, self.structExpression.create_copy(), self.indexName.create_copy())

    


class NStructIndexingIndex(NIndexingIndex):
    # long lineNr;
    # long rowNr;
    # NIdentifier indexName;

    def __init__(self, lineNr,
        rowNr,
        indexName):

        self.lineNr = lineNr
        self.rowNr = rowNr
        self.indexName = indexName

    

    def print_it(self):
        print(".", end='')
        self.indexName.print_it()
    

    def get_line_nr(self): 
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr

    
    def create_copy(self):
        return NStructIndexingIndex(self.lineNr, self.rowNr, self.indexName.create_copy())





class NVariantBoxCastIndex(NIndexingIndex):

    # long lineNr;
    # long rowNr;
    # NType theType;

    def __init__(self, lineNr,
        rowNr,
        theType):

        self.lineNr = lineNr
        self.rowNr = rowNr
        self.theType = theType

    

    def print_it(self):
        print(" ==> ", end='')
        self.theType.print_it()
    

    def get_line_nr(self): 
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr

    
    def create_copy(self):
        return NVariantBoxCastIndex(self.lineNr, self.rowNr, self.theType.create_copy())




class NTypeClarificationIndex(NIndexingIndex):

    # long lineNr;
    # long rowNr;
    # NType theType;

    def __init__(self, lineNr,
        rowNr,
        theType):

        self.lineNr = lineNr
        self.rowNr = rowNr
        self.theType = theType

    

    def print_it(self):
        print(" ::: ", end='')
        self.theType.print_it()
    

    def get_line_nr(self): 
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr

    
    def create_copy(self):
        return NTypeClarificationIndex(self.lineNr, self.rowNr, self.theType.create_copy())




# NOT USED CURRENTLY:   

# class NIndexing(NExpression):
#
    # long lineNr;
    # long rowNr;
    # NExpression expression;
    # ArrayList<NIndexingIndex> indexingIndices;

#     def __init__(self, lineNr, rowNr, expression, indexingIndices):
#        
#         self.lineNr = lineNr
#         self.rowNr = rowNr
#         self.expression = expression
#         self.indexingIndices = indexingIndices
#         self.isValidLValue = self.expression.isValidLValue
#
#    
#
#     def print_it(self):
#         self.expression.print_it()
#         for ii in indexingIndices:
#             ii.print_it()
#        
#    
#
#     def get_line_nr(self): 
#         return self.lineNr
#
#     def get_row_nr(self): 
#         return self.rowNr
#
#     # createCopy() here????
    


 












class NVariantBoxCastExpression(NExpression):

    # long lineNr;
    # long rowNr;
    # NExpression expression;
    # NType theType;

    def __init__(self, lineNr,
        rowNr,
        expression,
        theType):
    
        self.lineNr = lineNr
        self.rowNr = rowNr
        self.expression = expression
        self.theType = theType
        self.isValidLValue = False # because it is only used when "expression" isn't a valid lvalue
    

    def print_it(self):
        print("(", end='')
        self.expression.print_it()
        print(" ==> ", end='')
        self.theType.print_it()
        print(")", end='')
    

    def get_line_nr(self): 
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr
    

    def create_copy(self):
        return NVariantBoxCastExpression(self.lineNr, self.rowNr, self.expression.create_copy(), self.theType.create_copy())




class NArg:
    pass




class NNormalArg(NArg): 

    # long lineNr;
    # long rowNr;
    # NIdentifier argNameOrNull;
    # NExpression argExpression;

    def __init__(self, lineNr,
        rowNr,
        argNameOrNull,
        argExpression):

        self.lineNr = lineNr
        self.rowNr = rowNr
        self.argNameOrNull = argNameOrNull
        self.argExpression = argExpression

    

    def print_it(self):
        if not self.argNameOrNull is None:
            self.argNameOrNull.print_it()
            print(" = ", end='')
        
        self.argExpression.print_it()
    

    def get_line_nr(self): 
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr


    def create_copy(self):
        if self.argNameOrNull is None:
            return NNormalArg(self.lineNr, self.rowNr, None, self.argExpression.create_copy())
        else:
            return NNormalArg(self.lineNr, self.rowNr, self.argNameOrNull.create_copy(), self.argExpression.create_copy())

    


class NRefArg(NArg):

    # long lineNr;
    # long rowNr;
    # NIdentifier argNameOrNull;
    # NLValueContainer lValueContainer;

    def __init__(self, lineNr,
        rowNr,
        argNameOrNull,
        lValueContainer):

        self.lineNr = lineNr
        self.rowNr = rowNr
        self.argNameOrNull = argNameOrNull
        self.lValueContainer = lValueContainer

    

    def print_it(self):
        print("ref ", end='')
        if not self.argNameOrNull is None:
            self.argNameOrNull.print_it()
            print(" = ", end='')
        
        self.lValueContainer.print_it() 
    

    def get_line_nr(self): 
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr

    
    def create_copy(self):
        if self.argNameOrNull is None:
            return NRefArg(self.lineNr, self.rowNr, None, self.lValueContainer.create_copy())
        else:
            return NRefArg(self.lineNr, self.rowNr, self.argNameOrNull.create_copy(), self.lValueContainer.create_copy())




class NAndSymbolExpression(NExpression):

    # long lineNr;
    # long rowNr;
    # NExpression leftExpression;
    # NExpression rightExpression;

    def __init__(
        self,
        lineNr,
        rowNr,
        leftExpression,
        rightExpression
    ):
        self.lineNr = lineNr
        self.rowNr = rowNr
        self.leftExpression = leftExpression
        self.rightExpression = rightExpression
        self.isValidLValue = False
    

    def print_it(self):
        print("(", end='')
        self.leftExpression.print_it()
        print(" && ", end='')
        self.rightExpression.print_it()
        print(")", end='')
    

    def get_line_nr(self): 
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr


    def create_copy(self):
        return NAndSymbolExpression(self.lineNr, self.rowNr, self.leftExpression.create_copy(), self.rightExpression.create_copy())



class NOrSymbolExpression(NExpression):

    # long lineNr;
    # long rowNr;
    # NExpression leftExpression;
    # NExpression rightExpression;

    def __init__(
        self,
        lineNr,
        rowNr,
        leftExpression,
        rightExpression
    ):
        self.lineNr = lineNr
        self.rowNr = rowNr
        self.leftExpression = leftExpression
        self.rightExpression = rightExpression
        self.isValidLValue = False
    

    def print_it(self):
        print("(", end='')
        self.leftExpression.print_it()
        print(" || ", end='')
        self.rightExpression.print_it()
        print(")", end='')
    

    def get_line_nr(self): 
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr


    def create_copy(self):
        return NOrSymbolExpression(self.lineNr, self.rowNr, self.leftExpression.create_copy(), self.rightExpression.create_copy())


class NEndExpression(NExpression):

    # long lineNr;
    # long rowNr;

    # NExpression expansion;

    def __init__(
        self,
        lineNr,
        rowNr
    ):
        self.lineNr = lineNr
        self.rowNr = rowNr
        self.isValidLValue = False
    

    def print_it(self):
        if hasattr(self, 'expansion'):
            self.expansion.print_it()
        else:
            print("end", end='')
    

    def get_line_nr(self): 
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr


    def create_copy(self):
        result = NEndExpression(self.lineNr, self.rowNr)

        if hasattr(self, 'expansion'):
            result.expansion = self.expansion.create_copy()

        return result    # TODO: We have to do like this later with create_copy on all things that have annotations!!!!!!!!!!!    




class NFunctionCall(NExpression):

    # long lineNr;
    # long rowNr;
    # NExpression functionExpression;
    # ArrayList<NArg> args;

    def __init__(self, lineNr,
        rowNr,
        functionExpression,
        args):
    
        self.lineNr = lineNr
        self.rowNr = rowNr
        self.functionExpression = functionExpression
        self.args = args
        self.isValidLValue = False
    

    def print_it(self):        
        self.functionExpression.print_it()
        print("(", end='')
        if len(self.args) > 0:
            self.args[0].print_it()
            for i in range(1, len(self.args)):
                print(", ", end='')
                self.args[i].print_it()
            
        print(")", end='')
    

    def get_line_nr(self): 
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr

    
    def create_copy(self):
        argsCopy = []
        for arg in self.args:
            argsCopy.append(arg.create_copy())

        result = NFunctionCall(self.lineNr, self.rowNr, self.functionExpression.create_copy(), argsCopy)
        return result




class NIFExpression(NExpression):
    
    # long lineNr;
    # long rowNr;
    # NExpression condition;
    # NExpression thenExpression;
    # NExpression elseExpression;

    def __init__(self, lineNr, rowNr, condition, thenExpression, elseExpression):
        self.lineNr = lineNr
        self.rowNr = rowNr
        self.condition = condition
        self.thenExpression = thenExpression
        self.elseExpression = elseExpression
        self.isValidLValue = False            # We better not experiment with changing this!!!!!!


    def print_it(self):
        print("IF ", end='')
        self.condition.print_it()
        print(" ", end='')
        self.thenExpression.print_it()
        print(" ELSE ", end='')
        self.elseExpression.print_it()

    
    def get_line_nr(self): 
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr


    def create_copy(self):
        result = NIFExpression(self.lineNr, self.rowNr, self.condition.create_copy(), self.thenExpression.create_copy(), self.elseExpression.create_copy())
        return result


class NSWITCHNormalCase:

    # long lineNr;
    # long rowNr;
    # ArrayList<NExpression> caseValues;  // at least one of these!
    # NExpression value;

    def __init__(self, lineNr, rowNr, caseValues, value):
        self.lineNr = lineNr
        self.rowNr = rowNr
        self.caseValues = caseValues
        self.value = value

    def print_it(self):
        print(" CASE ", end='')

        if len(self.caseValues) == 0:
            print("MISSING CASE VALUE!!!", end='')
        else:
            self.caseValues[0].print_it()
            for i in range(1, len(self.caseValues)):
                print(", ", end='')
                self.caseValues[i].print_it()

        print(" ", end='')
        self.value.print_it()


    def get_line_nr(self): 
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr    


    def create_copy(self):
        caseValuesCopy = []
        for caseValue in self.caseValues:
            caseValuesCopy.append(caseValue.create_copy())

        result = NSWITCHNormalCase(self.lineNr, self.rowNr, caseValuesCopy, self.value.create_copy())
        return result    


class NCONTENTTYPENormalCase:

    # long lineNr;
    # long rowNr;
    # ArrayList<NType> typeCases;
    # NExpression value;

    def __init__(self, lineNr, rowNr, typeCases, value):
        self.lineNr = lineNr
        self.rowNr = rowNr
        self.typeCases = typeCases
        self.value = value

    def print_it(self):
        print(" CASE ", end='')

        if len(self.typeCases) == 0:
            print("MISSING TYPE CASE!!!", end='')
        else:
            self.typeCases[0].print_it()
            for i in range(1, len(self.typeCases)):
                print(",", end='')
                self.typeCases[i].print_it()

        print(" ", end='')
        self.value.print_it()


    def create_copy(self):
        typeCasesCopy = []
        for typeCase in self.typeCases:
            typeCasesCopy.append(typeCase.create_copy())

        result = NCONTENTTYPENormalCase(self.lineNr, self.rowNr, typeCasesCopy, self.value.create_copy())
        return result


class NSWITCHExpression(NExpression):
    
    # long lineNr;
    # long rowNr;
    # NExpression switchValue;
    # ArrayList<NSWITCHNormalCase> cases;
    # NExpression defaultCase;

    def __init__(self, lineNr, rowNr, switchValue, cases, defaultCase):
        self.lineNr = lineNr
        self.rowNr = rowNr
        self.switchValue = switchValue
        self.cases = cases
        self.defaultCase = defaultCase
        self.isValidLValue = False

    def print_it(self):
        print("SWITCH ", end='')
        self.switchValue.print_it()
        for c in self.cases:
            c.print_it()
        
        print(" DEFAULT ", end='')
        self.defaultCase.print_it()

    
    def get_line_nr(self): 
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr

    
    def create_copy(self):
        casesCopy = []
        for case in self.cases:
            casesCopy.append(case.create_copy())

        result = NSWITCHNormalCase(self.lineNr, self.rowNr, self.switchValue.create_copy(), casesCopy, self.defaultCase.create_copy())
        return result


class NCONTENTTYPEExpression(NExpression):
    # long lineNr;
    # long rowNr;
    # NExpression switchValue;
    # ArrayList<NCONTENTTYPENormalCase> cases;
    # NExpression defaultCaseOrNull;

    def __init__(self, lineNr, rowNr, switchValue, cases, defaultCaseOrNull):
        self.lineNr = lineNr
        self.rowNr = rowNr
        self.switchValue = switchValue
        self.cases = cases
        self.defaultCaseOrNull = defaultCaseOrNull
        self.isValidLValue = False

    def print_it(self):
        print("CONTENTTYPE ", end='')
        self.switchValue.print_it()
        for c in self.cases:
            c.print_it()
        
        if not self.defaultCaseOrNull is None:
            print(" DEFAULT ", end='')
            self.defaultCaseOrNull.print_it() 


    def get_line_nr(self): 
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr

        
    def create_copy(self):
        casesCopy = []
        for case in cases:
            casesCopy.append(case.create_copy())

        if self.defaultCaseOrNull is None:
            result = NCONTENTTYPEExpression(self.lineNr, self.rowNr, self.switchValue.create_copy(), casesCopy, None)
        else:
            result = NCONTENTTYPEExpression(self.lineNr, self.rowNr, self.switchValue.create_copy(), casesCopy, self.defaultCaseOrNull.create_copy())

        return result


##################### LVALUES ETC. #################################


class NLValueOrVariableDeclaration:    

    # abstract void print();

    # abstract long getLineNr();
    # abstract long getRowNr();

    pass






class NLValueContainer(NLValueOrVariableDeclaration):

    # long lineNr;
    # long rowNr;
    # NIdentifierExpression lValueExpression;

    def __init__(self, lineNr,
        rowNr,
        lValueExpression):

        self.lineNr = lineNr
        self.rowNr = rowNr
        self.lValueExpression = lValueExpression

    

    def print_it(self):
        print("(LVALUE ", end='')
        self.lValueExpression.print_it()
        print(")", end='')
    

    def get_line_nr(self): 
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr

    

    def create_copy(self):
        return NLValueContainer(self.lineNr, self.rowNr, self.lValueExpression.create_copy())








##################### STATEMENTS ##############################


class NStatement:

    # abstract void print();

    # abstract long getLineNr();
    # abstract long getRowNr();
    
    pass





class NTypeDeclarationWithDefinition(NStatement):

    # long lineNr;
    # long rowNr;
    # NIdentifier name;
    # ArrayList<NIdentifier> paramsOrNull;
    # NType theType;


    # str mangledName;

    def __init__(
        self,
        lineNr,
        rowNr,
        name,
        paramsOrNull, # this one should have at least 1 element if not None
        theType
    ):
        self.lineNr = lineNr
        self.rowNr = rowNr
        self.name = name
        self.paramsOrNull = paramsOrNull
        self.theType = theType
    

    def print_it(self):
        
        print("type ", end='')
        self.name.print_it()
        if not self.paramsOrNull is None:
            if len(self.paramsOrNull) > 0:
                print("(", end='')
                self.paramsOrNull[0].print_it()
                for i in range(1, len(self.paramsOrNull)):
                    print(", ", end='')
                    self.paramsOrNull[i].print_it()
                
                print(")", end='')
            
        print(" = ", end='')
        self.theType.print_it()
        print("; ", end='')
    

    def get_line_nr(self): 
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr


    def create_copy(self):    # this method needs not exist for all kinds of statements, but on this one it is needed 
        
        paramsOrNullCopy = None

        if not self.paramsOrNull is None:

            paramsOrNullCopy = []

            for param in self.paramsOrNull:
                paramsOrNullCopy.append(param.create_copy())

        if paramsOrNullCopy is None:

            result = NTypeDeclarationWithDefinition(self.lineNr, self.rowNr, self.name.create_copy(), None, self.theType.create_copy())

            if hasattr(self, "mangledName"):
                result.mangledName = self.mangledName

            return result

        else:

            result = NTypeDeclarationWithDefinition(self.lineNr, self.rowNr, self.name.create_copy(), paramsOrNullCopy, self.theType.create_copy())

            if hasattr(self, "mangledName"):
                result.mangledName = self.mangledName

            return result


class NBlock(NStatement):

    # long lineNr;
    # long rowNr;
    # ArrayList<NStatement> statements;

    def __init__(
        self,
        lineNr,
        rowNr,
        statements
    ):
        self.lineNr = lineNr
        self.rowNr = rowNr
        self.statements = statements
    

    def print_it(self):
        print("{", end='')
        for statement in self.statements:
            statement.print_it()
        
        print("} ", end='')
    

    def get_line_nr(self): 
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr





class NElseIfClause:

    # long lineNr;
    # long rowNr;
    # NExpression condition;
    # NBlock block;

    def __init__(self, lineNr, rowNr, condition, block):
        self.lineNr = lineNr
        self.rowNr = rowNr
        self.condition = condition
        self.block = block
         

    def print_it(self):
        print("else if ", end='')
        self.condition.print_it()
        print(" ", end='')
        self.block.print_it()
    

    def get_line_nr(self):
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr    





class NIfStatement(NStatement):

    # long lineNr;
    # long rowNr;
    # NExpression condition;
    # NBlock ifBlock;
    # ArrayList<NElseIfClause> elseIfClauses;
    # NBlock elseBlockOrNull;

    def __init__(self, lineNr, rowNr, condition, ifBlock, elseIfClauses, elseBlockOrNull):
        self.lineNr = lineNr
        self.rowNr = rowNr
        self.condition = condition
        self.ifBlock = ifBlock
        self.elseIfClauses = elseIfClauses
        self.elseBlockOrNull = elseBlockOrNull
    

    def print_it(self):
        print("if ", end='')
        self.condition.print_it()
        print(" ", end='')
        self.ifBlock.print_it()
        for clause in self.elseIfClauses:
            clause.print_it()
        
        if not self.elseBlockOrNull is None:
            print("else ", end='')
            self.elseBlockOrNull.print_it()
     
    
 
    def get_line_nr(self): 
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr




class NParam:

    # abstract void print();

    # abstract long getLineNr();

    # abstract long getRowNr();

    # abstract Param create_copy();
    
    pass




class NNormalParam(NParam):
    # long lineNr;
    # long rowNr;
    # boolean isMut;
    # boolean isConstruand;
    # NIdentifier name;
    # NType theType;

    def __init__(
        self,
        lineNr,
        rowNr,
        isMut,
        isConstruand, # TODO: can they be both?????? Yes, but then mu wins for impl. purposes I guess
        name,
        theType
    ):
        self.lineNr = lineNr
        self.rowNr = rowNr
        self.isMut = isMut
        self.isConstruand = isConstruand
        self.name = name
        self.theType = theType
    

    def print_it(self):
        if self.isMut:
            print("mu ", end='')
        
        if self.isConstruand:
            print("construand ", end='')
        
        self.name.print_it()
        print(" : ", end='')
        self.theType.print_it()
    

    def get_line_nr(self): 
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr


    def create_copy(self):
        return NNormalParam(self.lineNr, self.rowNr, self.isMut, self.isConstruand, self.name.create_copy(), self.theType.create_copy())






class NRefParam(NParam):

    # long lineNr;
    # long rowNr;
    # NIdentifier name;
    # NType type;

    def __init__(
        self,
        lineNr,
        rowNr,
        name,
        theType
    ):
        self.lineNr = lineNr
        self.rowNr = rowNr
        self.name = name
        self.theType = theType
    

    def print_it(self):
        print("ref ", end='')
        self.name.print_it()
        print(" : ", end='')
        self.theType.print_it()
    

    def get_line_nr(self): 
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr


    def create_copy(self):
        return NRefParam(self.lineNr, self.rowNr, self.name.create_copy(), self.theType.create_copy())





class NActualFunctionDeclarationWithDefinition(NStatement):

    # long lineNr;
    # long rowNr;
    # boolean isInternal;
    # boolean isInline;
    # NIdentifier name;
    # ArrayList<NParam> params;
    # ArrayList<NType> returnTypes;
    # NBlock body;

    def __init__(
        self,
        lineNr,
        rowNr,
        isInternal,
        isInline,
        name,
        params,
        returnTypes,
        body
    ): 
        self.lineNr = lineNr
        self.rowNr = rowNr
        self.isInternal = isInternal
        self.isInline = isInline
        self.name = name
        self.params = params
        self.returnTypes = returnTypes
        self.body = body
    

    def print_it(self):
        if self.isInternal:
            print("internal ", end='')
        
        if self.isInline:
            print("inline ", end='')
        
        print("fn ", end='')
        self.name.print_it()
        print("(", end='')
        if len(self.params) > 0:
            self.params[0].print_it()
            for i in range(1, len(self.params)):
                print(", ", end='')
                self.params[i].print_it()
                
        if len(self.returnTypes) > 0:
            print(" => ", end='')
            self.returnTypes[0].print_it()
            for i in range(1, len(self.returnTypes)):
                print(", ", end='')
                self.returnTypes[i].print_it()
      
        print(") ", end='')
        self.body.print_it()
    

    def get_line_nr(self): 
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr




class NRefToFunctionDeclarationWithDefinition(NStatement):

    # int funsIndex;
    # ArrayList<NActualFunctionDeclarationWithDefinition> funs; // need this ref for printing, sadly, in order to conform to the NStatement abstract

    def __init__ (
        self,
        funsIndex,
        funs
    ):
        self.funsIndex = funsIndex
        self.funs = funs
    

    def print_it(self):
        self.funs[self.funsIndex].print_it()
    

    def get_line_nr(self): 
        return self.funs[self.funsIndex].get_line_nr()

    def get_row_nr(self): 
        return self.funs[self.funsIndex].get_row_nr()






class NActualTemplateDeclarationWithDefinition(NStatement):

    # long lineNr;
    # long rowNr;
    # boolean isInternal;
    # boolean isInline;
    # ArrayList<NIdentifier> templateParams; // must have at least length 1
    # NIdentifier name;
    # ArrayList<NParam> params;
    # ArrayList<NType> returnTypes;
    # NBlock body;

    def __init__(
        self,
        lineNr,
        rowNr,
        isInternal,
        isInline,
        templateParams,
        name,
        params,
        returnTypes,
        body
    ):
        self.lineNr = lineNr
        self.rowNr = rowNr
        self.isInternal = isInternal
        self.isInline = isInline
        self.templateParams = templateParams
        self.name = name
        self.params = params
        self.returnTypes = returnTypes
        self.body = body


    def print_it(self):
        if self.isInternal:
            print("private ", end='')
        
        if self.isInline:
            print("inline ", end='')
        
        print("fn(", end='')
        if len(self.templateParams) > 0: # should be
            self.templateParams[0].print_it()
            for i in range(1, len(self.templateParams)):
                print(", ", end='')
                self.templateParams[i].print_it()
            
        print(") ", end='')
        self.name.print_it()
        print("(", end='')
        if len(self.params) > 0:
            self.params[0].print_it()
            for i in range(1, len(self.params)):
                print(", ", end='')
                self.params[i].print_it()
               
        if len(self.returnTypes) > 0:
            print(" => ", end='')
            self.returnTypes[0].print_it()
            for i in range(1, len(self.returnTypes)):
                print(", ", end='')
                self.returnTypes[i].print_it()
            
        print(") ", end='')
        self.body.print_it()
    

    def get_line_nr(self): 
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr




class NRefToTemplateDeclarationWithDefinition(NStatement):

    # int templatesIndex;
    # ArrayList<NActualTemplateDeclarationWithDefinition> templates; // need this ref for printing, sadly, in order to conform to the NStatement abstract

    def __init__(
        self,
        templatesIndex,
        templates
    ):
        self.templatesIndex = templatesIndex
        self.templates = templates
    

    def print_it(self):
        self.templates[self.templatesIndex].print_it()
    

    def get_line_nr(self):
        return self.templates[self.templatesIndex].get_line_nr()
    
    def get_row_nr(self): 
        return self.templates[self.templatesIndex].get_row_nr()







class NVariableDeclaration(NLValueOrVariableDeclaration):

    # long lineNr;
    # long rowNr;
    # boolean isMut;
    # boolean isInternal;
    # NIdentifier name;
    # NType theType;

    def __init__(
        self,
        lineNr,
        rowNr,
        isMut,
        isInternal,
        name,
        theType
    ):
        self.lineNr = lineNr
        self.rowNr = rowNr
        self.isMut = isMut
        self.isInternal = isInternal
        self.name = name
        self.theType = theType
    

    def print_it(self):
        if self.isInternal:
            print("internal ", end='')
        
        if self.isMut:
            print("mu ", end='')
        
        self.name.print_it()
        print(" : ", end='')
        self.theType.print_it()
    

    def get_line_nr(self): 
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr






class NAssignment:
    pass


class NNormalAssignment(NAssignment):

    # long lineNr;
    # long rowNr;
    # ArrayList<NLValueOrVariableDeclaration> leftHandSide;
    # NExpression value;

    

    def __init__(
        self,
        lineNr,
        rowNr,
        leftHandSide, # should have at least 1 element
        value
    ):
        self.lineNr = lineNr
        self.rowNr = rowNr
        self.leftHandSide = leftHandSide
        self.value = value
    

    def print_it(self):
        self.leftHandSide[0].print_it()
        for i in range(1, len(self.leftHandSide)):
            print(", ", end='')
            self.leftHandSide[i].print_it()
        
        print(" = ", end='')
        self.value.print_it()
        print("; ", end='')
    

    def get_line_nr(self): 
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr








class NModuloAssignment(NAssignment):

    # long lineNr;
    # long rowNr;
    # ArrayList<NLValueContainer> leftHandSide;
    # NExpression value;

    

    def __init__(
        self,
        lineNr,
        rowNr,
        leftHandSide, # should have at least 1 element
        value
    ):
        self.lineNr = lineNr
        self.rowNr = rowNr
        self.leftHandSide = leftHandSide
        self.value = value
    

    def print_it(self):
        self.leftHandSide[0].print_it()
        for i in range(1, len(self.leftHandSide)):
            print(", ", end='')
            self.leftHandSide[i].print_it()
        
        print(" %= ", end='')
        self.value.print_it()
        print("; ", end='')
    

    def get_line_nr(self): 
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr






class NAdditionAssignment(NAssignment):

    # long lineNr;
    # long rowNr;
    # ArrayList<NLValueContainer> leftHandSide;
    # NExpression value;

    

    def __init__(
        self,
        lineNr,
        rowNr,
        leftHandSide, # should have at least 1 element
        value
    ):
        self.lineNr = lineNr
        self.rowNr = rowNr
        self.leftHandSide = leftHandSide
        self.value = value
    

    def print_it(self):
        self.leftHandSide[0].print_it()
        for i in range(1, len(self.leftHandSide)):
            print(", ", end='')
            self.leftHandSide[i].print_it()
        
        print(" += ", end='')
        self.value.print_it()
        print("; ", end='')
    

    def get_line_nr(self): 
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr



class NSubtractionAssignment(NAssignment):

    # long lineNr;
    # long rowNr;
    # ArrayList<NLValueContainer> leftHandSide;
    # NExpression value;

    

    def __init__(
        self,
        lineNr,
        rowNr,
        leftHandSide, # should have at least 1 element
        value
    ):
        self.lineNr = lineNr
        self.rowNr = rowNr
        self.leftHandSide = leftHandSide
        self.value = value
    

    def print_it(self):
        self.leftHandSide[0].print_it()
        for i in range(1, len(self.leftHandSide)):
            print(", ", end='')
            self.leftHandSide[i].print_it()
        
        print(" -= ", end='')
        self.value.print_it()
        print("; ", end='')
    

    def get_line_nr(self): 
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr






class NMultiplicationAssignment(NAssignment):

    # long lineNr;
    # long rowNr;
    # ArrayList<NLValueContainer> leftHandSide;
    # NExpression value;

    

    def __init(
        self,
        lineNr,
        rowNr,
        leftHandSide, # should have at least 1 element
        value
    ):
        self.lineNr = lineNr
        self.rowNr = rowNr
        self.leftHandSide = leftHandSide
        self.value = value
    

    def print_it(self):
        self.leftHandSide[0].print_it()
        for i in range(1, len(self.leftHandSide)):
            print(", ", end='')
            self.leftHandSide[i].print_it()
        
        print(" *= ", end='')
        self.value.print_it()
        print("; ", end='')
    

    def get_line_nr(self): 
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr






class NDivisionAssignment(NAssignment):

    # long lineNr;
    # long rowNr;
    # ArrayList<NLValueContainer> leftHandSide;
    # NExpression value;

    

    def __init__(
        self,
        lineNr,
        rowNr,
        leftHandSide, # should have at least 1 element
        value
    ):
        self.lineNr = lineNr
        self.rowNr = rowNr
        self.leftHandSide = leftHandSide
        self.value = value
    

    def print_it(self):
        self.leftHandSide[0].print_it()
        for i in range(1, len(self.leftHandSide)):
            print(", ", end='')
            self.leftHandSide[i].print_it()
        
        print(" /= ", end='')
        self.value.print()
        print("; ", end='')
    

    def get_line_nr(self): 
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr





class NLoopStatement(NStatement):

    # long lineNr;
    # long rowNr;
    # NBlock block;
    # NIdentifier labelOrNull;

    def __init__(
        self,
        lineNr,
        rowNr,
        block,
        labelOrNull  
    ):
        self.lineNr = lineNr
        self.rowNr = rowNr
        self.block = block
        self.labelOrNull = labelOrNull
    

    def print_it(self):
        print("loop ", end='')
        if not self.labelOrNull is None:
            print("label ", end='')
            self.labelOrNull.print_it()
            print(" ", end='') 
        
        self.block.print_it()
    

    def get_line_nr(self): 
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr





class NRange:

    # long lineNr;
    # long rowNr;
    # NIdentifier counterName;
    # NType counterType;
    # NExpression rangeFrom;
    # boolean isDownto;
    # NExpression rangeTo;    

    def __init__(
        self,
        lineNr,
        rowNr,
        counterName,
        counterType,
        rangeFrom,
        isDownto,
        rangeTo
    ):
        self.lineNr = lineNr
        self.rowNr = rowNr
        self.counterName = counterName
        self.counterType = counterType
        self.rangeFrom = rangeFrom
        self.isDownto = isDownto
        self.rangeTo = rangeTo
       
    

    def print_it(self):
        self.counterName.print_it()
        print(" : ", end='')
        self.counterType.print_it()
        print(" = ", end='')
        self.rangeFrom.print_it()
        if self.isDownto:
            print(" downto ", end='')
        else:    
            print(" to ", end='')
        
        self.rangeTo.print_it()
        
    

    def get_line_nr(self): 
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr







class NIteration:

    # abstract void print();

    # abstract long getLineNr();
    # abstract long getRowNr();

    pass




class NIterationIn(NIteration):

    # long lineNr;
    # long rowNr;
    # NIdentifier itName;
    # NType itTypeOrNull;
    # NExpression arrayExpression;
    # NExpression indexfactorOrNull;
    # NExpression indexoffsetOrNull;

    
 
    def __init__(
        self,
        lineNr,
        rowNr,
        itName,
        itTypeOrNull,
        arrayExpression,
        indexfactorOrNull,
        indexoffsetOrNull    
    ):
        self.lineNr = lineNr
        self.rowNr = rowNr
        self.itName = itName
        self.itTypeOrNull = itTypeOrNull
        self.arrayExpression = arrayExpression
        self.indexfactorOrNull = indexfactorOrNull
        self.indexoffsetOrNull = indexoffsetOrNull
    

    def print_it(self):
        self.itName.print_it()
        if not self.itTypeOrNull is None:
            print(" : ", end='')
            self.itTypeOrNull.print_it()
        
        print(" in ", end='')
        self.arrayExpression.print_it()
        if not self.indexfactorOrNull is None:
            print(" indexfactor ", end='')
            self.indexfactorOrNull.print_it()
        
        if not self.indexoffsetOrNull is None:
            print(" indexoffset ", end='')
            self.indexoffsetOrNull.print_it()
        
    

    def get_line_nr(self): 
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr






class NIterationOver(NIteration):

    # long lineNr;
    # long rowNr;
    # NIdentifier itName;
    # NType itTypeOrNull;
    # NLValueContainer arrayLValue;
    # NExpression indexfactorOrNull;
    # NExpression indexoffsetOrNull;

    

    def __init__(
        self,
        lineNr,
        rowNr,
        itName,
        itTypeOrNull,
        arrayLValue,
        indexfactorOrNull,
        indexoffsetOrNull    
    ):
        self.lineNr = lineNr
        self.rowNr = rowNr
        self.itName = itName
        self.itTypeOrNull = itTypeOrNull
        self.arrayLValue = arrayLValue
        self.indexfactorOrNull = indexfactorOrNull
        self.indexoffsetOrNull = indexoffsetOrNull
    

    def print_it(self):
        self.itName.print_it()
        if not self.itTypeOrNull is None:
            print(" : ", end='')
            self.itTypeOrNull.print_it()
        
        print(" over ", end='')
        self.arrayLValue.print_it()
        if not self.indexfactorOrNull is None:
            print(" indexfactor ", end='')
            self.indexfactorOrNull.print_it()
        
        if not self.indexoffsetOrNull is None:
            print(" offsetvalue ", end='')
            self.indexoffsetOrNull.print_it()
        
    
    def get_line_nr(self): 
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr






class NForStatement(NStatement): # check this during validation so that there is either range or at least 1 iteration...

    # long lineNr;
    # long rowNr;
    # NRange rangeOrNull;
    # ArrayList<NIteration> iterations;
    # NBlock block;
    # NIdentifier labelOrNull;

    def __init__(
        self,
        lineNr,
        rowNr,
        rangeOrNull,
        iterations,
        block,
        labelOrNull
    ):
        self.lineNr = lineNr
        self.rowNr = rowNr
        self.rangeOrNull = rangeOrNull
        self.iterations = iterations
        self.block = block
        self.labelOrNull = labelOrNull
    

    def print_it(self):
        print("for ", end='')
        if not self.labelOrNull is None:
            print("label ", end='')
            self.labelOrNull.print_it()
            print(" ", end='')
        
        if not self.rangeOrNull is None:
            self.rangeOrNull.print_it()

            if len(self.iterations) > 0:
                print(", ", end='')
            

        if len(self.iterations) > 0:
            self.iterations[0].print_it()
            for i in range(1, len(self.iterations)):
                print(", ", end='')
                self.iterations[i].print_it()
                        
        self.block.print_it()
    

    def get_line_nr(self): 
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr






class NFunctionCallStatement(NStatement):

    # long lineNr;
    # long rowNr;
    # NFunctionCall functionCall;

    

    def __init__(
        self,
        lineNr,
        rowNr,
        functionCall
    ):
        self.lineNr = lineNr
        self.rowNr = rowNr
        self.functionCall = functionCall
    

    def print_it(self):
        self.functionCall.print_it()
        print("; ", end='')
    

    def get_line_nr(self): 
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr




class NReturnStatement(NStatement):

    # long lineNr;
    # long rowNr;
    # ArrayList<NExpression> returnExpressions;


    def __init__(
        self,
        lineNr,
        rowNr,
        returnExpressions        
    ):
        self.lineNr = lineNr
        self.rowNr = rowNr
        self.returnExpressions = returnExpressions
    

    def print_it(self):
        print("return", end='')
        if len(self.returnExpressions) > 0:
            print(" ", end='')
            self.returnExpressions[0].print_it()
            for i in range(1, len(self.returnExpressions)):
                print(", ", end='')
                self.returnExpressions[i].print_it()
            
        print("; ", end='')
    

    def get_line_nr(self): 
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr






class NBreakStatement(NStatement):

    # long lineNr;
    # long rowNr;
    # NIdentifier labelOrNull;

    def __init__(
        self,
        lineNr,
        rowNr,
        labelOrNull
    ):
        self.lineNr = lineNr
        self.rowNr = rowNr
        self.labelOrNull = labelOrNull
    

    def print_it(self):
        print("break", end='')
        if not self.labelOrNull is None:
            print(" label ", end='')
            self.labelOrNull.print_it()
        
        print("; ", end='')
    

    def get_line_nr(self): 
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr





class NContinueStatement(NStatement):

    # long lineNr;
    # long rowNr;
    # NIdentifier labelOrNull;

    def __init__(
        self,
        lineNr,
        rowNr,
        labelOrNull
    ):
        self.lineNr = lineNr
        self.rowNr = rowNr
        self.labelOrNull = labelOrNull
    

    def print_it(self):
        print("continue", end='')
        if not self.labelOrNull is None:
            print(" label ", end='')
            self.labelOrNull.print_it()
        
        print("; ", end='')
    

    def get_line_nr(self): 
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr




class NSwitchNormalCase:
    
    # long lineNr;
    # long rowNr;
    # ArrayList<NExpression> caseValues; // at least one of these!
    # NBlock block;

    def __init__(self, lineNr, rowNr, caseValues, block):
        self.lineNr = lineNr
        self.rowNr = rowNr
        self.caseValues = caseValues
        self.block = block

    def print_it(self):
        print("case ", end='')
        if len(self.caseValues) == 0:
            print("MISSING CASE VALUE!!!", end='');
        else:
            self.caseValues[0].print_it()
            for i in range(1, len(self.caseValues)):
                print(", ", end='')
                self.caseValues[i].print_it()

        print(" ", end='')
        self.block.print_it()

    def get_line_nr(self): 
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr







class NContenttypeNormalCase:

    # long lineNr;
    # long rowNr;
    # ArrayList<NType> caseTypes; // should have at least 1 element
    # NBlock block;

    def __init__(
        self,
        lineNr,
        rowNr,
        caseTypes,
        block
    ):
        self.lineNr = lineNr
        self.rowNr = rowNr
        self.caseTypes = caseTypes
        self.block = block
    

    def print_it(self):
        print("case ", end='')
        if len(self.caseTypes) == 0:
            print("MISSING TYPE CASE!!!", end='');
        else:
            self.caseTypes[0].print_it()
            for i in range(1, len(self.caseTypes)):
                print(", ", end='')
                self.caseTypes[i].print_it()

        print(" ", end='')
        self.block.print_it()
    

    def get_line_nr(self): 
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr









class NSwitchStatement(NStatement):

    # long lineNr;
    # long rowNr;
    # NExpression switchValue
    # ArrayList<NSwitchNormalCase> cases;
    # NBlock defaultCaseOrNull;

    def __init__(self, lineNr, rowNr, switchValue, cases, defaultCaseOrNull):
        self.lineNr = lineNr
        self.rowNr = rowNr
        self.switchValue = switchValue
        self.cases = cases
        self.defaultCaseOrNull = defaultCaseOrNull

    def print_it(self):
        print("switch ", end='')
        self.switchValue.print_it()
        print(" ", end='')
        for c in self.cases:
            c.print_it()
        
        if not self.defaultCaseOrNull is None:
           print("default ", end='') 
           self.defaultCaseOrNull.print_it()

    def get_line_nr(self): 
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr




class NContenttypeStatement(NStatement):

    # long lineNr;
    # long rowNr;
    # NExpression switchValue;
    # ArrayList<NContenttypeNormalCase> cases; // can have 0 length!
    # NBlock defaultCaseOrNull;


    
    
    # but must have either default or 1 normal case, check this during validation!

    def __init__(
        self,
        lineNr,
        rowNr,
        switchValue,
        cases,
        defaultCaseOrNull
    ):
        self.lineNr = lineNr
        self.rowNr = rowNr
        self.switchValue = switchValue
        self.cases = cases
        self.defaultCaseOrNull = defaultCaseOrNull
    

    def print_it(self):
        print("contenttype ", end='')
        self.switchValue.print_it()
        print(" ", end='')
        for c in self.cases:
            c.print_it()
        
        if not self.defaultCaseOrNull is None:
           print("default ", end='')
           self.defaultCaseOrNull.print_it() 
        
    

    def get_line_nr(self): 
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr






class NImportStatement:

    # long lineNr;
    # long rowNr;
    # boolean isPrefixImport;
    # String path;

    def __init__(self, lineNr, rowNr, isPrefixImport, path):
        self.lineNr = lineNr
        self.rowNr = rowNr
        self.isPrefixImport = isPrefixImport
        self.path = path
    

    def print_it(self):
        if self.isPrefixImport:
            print("prefiximport\"", end='')
        else:
            print("import\"", end='')
        
        print(self.path, end='')  # will print newlines and escapes in a funny way though...
        print("\"; ", end='')
    

    def get_line_nr(self): 
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr










class NProgram:

    # long lineNr;
    # long rowNr;
    # ArrayList<NImportStatement> importStatements;
    # ArrayList<NStatement> statements;

    def __init__(
        self,
        lineNr,
        rowNr,
        importStatements,
        statements
    ):
        self.lineNr = lineNr
        self.rowNr = rowNr
        self.importStatements = importStatements
        self.statements = statements
    

    def print_it(self):
        for importStatement in self.importStatements:
            importStatement.print_it()
        
        for statement in self.statements:
            statement.print_it()        

    
    def get_line_nr(self): 
        return self.lineNr

    def get_row_nr(self): 
        return self.rowNr    



######################################### VISITOR #########################################


class AbstractASTVisitor:

    def visit(self, node):
        raise NotImplementedError(NOT_IMPLEMENTED)



# class ExampleASTVisitor(AbstractASTVisitor):
#
#     def visit(self, node):
# 
#         if isinstance(node, NIdentifier):
#             if len(node.name) < 3:  
#               return False
# 
#             node.name = "FNORD"
#             return True
#     
#         elif isinstance(node, NIntegerExpression):
# 
#             node.numString = "42"
#             return True
# 
#         else:
#             return True




  


