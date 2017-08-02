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



public class Token {
    public enum Kind {
        INTTYPE, LSQUAREBRACKET, RSQUAREBRACKET, LPAREN, RPAREN, MU, IDENTIFIER, ASSIGNMENTOPERATOR, RETURN, COMMA, SEMICOLON, COLON, INT, LCURLYBRACKET, RCURLYBRACKET, FN, SHORTLARROW,
        EOF, CONSTRUCTAND, ERRATIC
    }

    public String identifierString;
    public int integerValue;
    public Kind kind;

    public Token(Kind kind) {
        this.kind = kind;

        this.identifierString = ""; // safety measures
        this.integerValue = 0;
    }

    public Token(String identifierString) {
        this.identifierString = identifierString;
        this.kind = Kind.IDENTIFIER;
        this.integerValue = 0;
    }

    public Token(int integerValue) {
        this.integerValue = integerValue;
        this.kind = Kind.INT;
        this.identifierString = "";
    }
}
