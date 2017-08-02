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

public class VirtualRegisterStore {

    Hashtable<String, RuntimeValue> globalRegisters; // all identifiers should start with "@"
    
    Hashtable<String, RuntimeValue> currentLocalRegisters; // all identifiers should with "%"


    public VirtualRegisterStore() {
        globalRegisters = new Hashtable<String, RuntimeValue>();
        currentLocalRegisters = new Hashtable<String, RuntimeValue>();
    }

    public void putGlobal(String id, RuntimeValue value) {
        if (globalRegisters.get(id) == null) {
            globalRegisters.put(id, value);
        } else {
            System.out.println("Trying to overwrite virtual global register " + id + " -- not SSA!");
        }        
    }

    public void putLocal(String id, RuntimeValue value) {
        if (currentLocalRegisters.get(id) == null) {
            currentLocalRegisters.put(id, value);
        } else {
            System.out.println("Trying to overwrite virtual local register " + id + " -- not SSA!");
        }
    }

    public RuntimeArrayHead getGlobalArrayHead(String id) {
        return (RuntimeArrayHead) (globalRegisters.get(id)); // if we don't find it, something is wrong
    }

    public RuntimeInt getGlobalInt(String id) {
        return (RuntimeInt) (globalRegisters.get(id));
    }

    public RuntimeStackAddress getGlobalStackAddress(String id) {
        return (RuntimeStackAddress) (globalRegisters.get(id));
    }

    public RuntimeArrayHead getLocalArrayHead(String id) {
        return (RuntimeArrayHead) (currentLocalRegisters.get(id));    
    }

    public RuntimeInt getLocalInt(String id) {
        return (RuntimeInt) (currentLocalRegisters.get(id));
    }

    public RuntimeStackAddress getLocalStackAddress(String id) {
        return (RuntimeStackAddress) (currentLocalRegisters.get(id));
    }

    public void newLocalContext() {
        currentLocalRegisters = new Hashtable<String, RuntimeValue>();
    }
}
