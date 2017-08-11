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
#     along with the Memtran compiler.  If not, see http://www.gnu.org/licenses/ 




class FunListEntryOrSlotEntry:

    pass



class FunListEntry(FunListEntryOrSlotEntry):  # can also hold template entries!!!!

    # ArrayList<FunOrTemplateEntry> funEntries;

    def __init__(self, funEntries):
        self.funEntries = funEntries

    def print_it(self):
        print("FUNCTIONS: [")

        for entry in self.funEntries:
            entry.print_it()
            print("")  # newline

        print("]")



class VarEntry(FunListEntryOrSlotEntry):

    # String mangledName;
    # boolean isMu;
    # boolean isInternal;
    # NType theType;

    def __init__(self, mangledName, isMu, isInternal, theType):
        self.mangledName = mangledName
        self.isMu = isMu
        self.isInternal = isInternal
        self.theType = theType

    def print_it(self):
        if self.isMu:
            print("mu ", end='')

        if self.isInternal:
            print("internal ", end='')        

        print("VAR: mangled name: ", end='')
        print(self.mangledName, end='')
        
        print(" ' ", end='')
    
        self.theType.print_it()

        print("") # newline

        

class BlockEntry(FunListEntryOrSlotEntry):

    # Dictionary<FunListEntryOrSlotEntry> localDict;

    def __init__(self, localDict, funDictEntryNameNr):
        self.localDict = localDict
        self.funDictEntryNameNr = funDictEntryNameNr

    def print_it(self):
        print("block: {")

        for key, value in self.localDict.items():

            print(key, end='')
            print(": ", end='')
            value.print_it()
            print("") # newline

        print("}")



class ParamEntry(FunListEntryOrSlotEntry):

    # String mangledName;
    # NParam definitionParam;

    def __init__(self, mangledName, definitionParam):
        self.mangledName = mangledName
        self.definitionParam = definitionParam

    def print_it(self):

        print("PARAM: mangled name:", end ='')
        print(self.mangledName, end='')
        print(" definition: ", end='')
        self.definitionParam.print_it()

        print("")  # newline


class NameIntoBlockEntry(FunListEntryOrSlotEntry):

    # NType theType

    def __init__(self, theType):
        self.theType = theType

    
    def print_it(self):

        print("INTONAME ' ", end='')
        self.theType.print_it()
        print("")  # newline







class FunOrTemplateEntry:
    pass


class FunEntry(FunOrTemplateEntry):
    
    # String mangledName;
    # FunSignature signature;
    # Dictionary<FunListEntryOrSlotEntry> localDict;
    # funsIndex

    # ADDED IN LATER PASSES:
    
    # forwardDependenciesList
    # slotList

    def __init__(self, mangledName, signature, localDict, funsIndex):
        self.mangledName = mangledName
        self.signature = signature
        self.localDict = localDict
        self.funsIndex = funsIndex

    
    def print_it(self):
        print("FUNCTION mangled name: ", end='')

        print(self.mangledName, end='')

        print(" signature: ", end='')

        self.signature.print_it()

        print(" funIndex: ", end='')

        print(str(self.funsIndex), end='')    

        print(" local dict: {")

        for key, value in self.localDict.items():

            print(key, end='')
            print(": ", end='')
            value.print_it()
            print("") # newline

        print("}")





class TemplateEntry(FunOrTemplateEntry):
    
    # String mangledBasicName;
    # ArrayList<NIdentifier> templateParams;
    # FunSignature signature;
    # funsIndex

    # ADDED IN LATER PASSES:

    # forwardDependenciesList   (? for templates??)
    # slotList

    def __init__(self, mangledBasicName, templateParams, signature, funsIndex):
        self.mangledBasicName = mangledBasicName
        self.templateParams = templateParams
        self.signature = signature
        self.funsIndex = funsIndex

    def print_it(self):
        print("TEMPLATE(", end='')
        
        if len(self.templateParams) > 0:   # It better should be...
            self.templateParams[0].print_it()

            for templateParam in self.templateParams[1:]:
                print(", ", end='')
                templateParam.print_it()

        print(") mangled name: ", end='')

        print(self.mangledBasicName, end='')

        print(" signature: ", end='')

        self.signature.print_it()

        print(" funsIndex ", end='')

        print(str(self.funsIndex), end='')    






class SpecializedTemplateEntry(FunOrTemplateEntry):

    # String templateMangledName;   # let's see if this is enough to find it
    # String mangledName;
    # FunSignature signature;
    # Dictionary<FunListEntryOrSlotEntry> localDict;
    # funsIndex

    # ADDED IN LATER PASSES:
    
    # forwardDependenciesList
    # slotList
    
    def __init__(self, templateMangledName, mangledName, signature, localDict, funsIndex):
        self.templateMangledName = templateMangledName
        self.mangledName = mangledName
        self.signature = signature
        self.localDict = localDict
        self.funsIndex = funsIndex

    
    def print_it(self):
        print("TSPEC template mangled name: ", end='')

        print(self.templateMangledName, end='')

        print(" mangled name: ", end='')

        print(self.mangledName, end='')

        print(" signature: ", end='')

        self.signature.print_it()

        print(" funIndex: ", end='')

        print(str(self.funsIndex), end='')    

        print(" local dict: {")

        for key, value in self.localDict.items():

            print(key, end='')
            print(": ", end='')
            value.print_it()
            print("") # newline

        print("}")



class FunSignature:

    # boolean isInternal;
    # boolean isInline;
    # String name;
    # ArrayList<NParam> params;
    # ArrayList<NType> returnTypes;

    def __init__(self, isInternal, isInline, name, params, returnTypes):
        self.isInternal = isInternal
        self.isInline = isInline
        self.name = name
        self.params = params
        self.returnTypes = returnTypes    


    def print_it(self):
        if (self.isInternal):
            print("internal ", end='')

        if (self.isInline):
            print("inline ", end='')

        print("fn ", end='')

        print(self.name, end='')

        print("(", end='')

        if len(self.params) > 0:
            self.params[0].print_it()

            for param in self.params[1:]:
                print(", ", end='')
                param.print_it()

        print(")", end='')

        if len(self.returnTypes) > 0:
            print(" : ", end='')

            self.returnTypes[0].print_it()
    
            for returnType in self.returnTypes[1:]:
                print(", ", end='')
                returnType.print_it()

















