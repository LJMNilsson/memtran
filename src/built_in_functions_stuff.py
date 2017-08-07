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


from ast import *
from fun_dict_stuff import *


# Question: can we have multiple templates with the same name really?


builtInFunsDict = {}

builtInFunsDict["add_last"] = FunListEntry(
    [
        TemplateEntry(
            "", 
            [
                NIdentifier(0, 0, "t")
            ],
            FunSignature(
                False, 
                False, 
                "add_last", 
                [
                    NRefParam(0, 0, NIdentifier(0, 0, "array"), NDynamicArrayType(0, 0, NIdentifierType(0, 0, None, NIdentifier(0, 0, "t")))),
                    NNormalParam(0, 0, False, True, NIdentifier(0, 0, "element"), NIdentifierType(0, 0, None, NIdentifier(0, 0, "t")))
                ],
                []
            ),
            -1
        ),
        TemplateEntry(
            "",
            [
                NIdentifier(0, 0, "t")
            ],
            FunSignature(
                False,
                False,
                "add_last",
                [
                    NNormalParam(0, 0, False, True, NIdentifier(0, 0, "array"), NDynamicArrayType(0, 0, NIdentifierType(0, 0, None, NIdentifier(0, 0, "t")))),
                    NNormalParam(0, 0, False, True, NIdentifier(0, 0, "element"), NIdentifierType(0, 0, None, NIdentifier(0, 0, "t")))
                ],
                [
                    NDynamicArrayType(0, 0, NIdentifierType(0, 0, None, NIdentifier(0, 0, "t")))
                ]
            ),
            -1
        )
    ]
)

builtInFunsDict["concat"] = FunListEntry(
    [
        TemplateEntry(
            "",
            [
                NIdentifier(0, 0, "t")
            ],
            FunSignature(
                False,
                False,
                "concat",
                [
                    NRefParam(0, 0, NIdentifier(0, 0, "array"), NDynamicArrayType(0, 0, NIdentifierType(0, 0, None, NIdentifier(0, 0, "t")))),
                    NNormalParam(0, 0, False, False, NIdentifier(0, 0, "array2"), NDynamicArrayType(0, 0, NIdentifierType(0, 0, None, NIdentifier(0, 0, "t"))))
                ],
                []
            ),
            -1 
        ),
        TemplateEntry(
            "",
            [
                NIdentifier(0, 0, "t")
            ],
            FunSignature(
                False,
                False,
                "concat",
                [
                    NNormalParam(0, 0, False, True, NIdentifier(0, 0, "array"), NDynamicArrayType(0, 0, NIdentifierType(0, 0, None, NIdentifier(0, 0, "t")))),
                    NNormalParam(0, 0, False, False, NIdentifier(0, 0, "array2"), NDynamicArrayType(0, 0, NIdentifierType(0, 0, None, NIdentifier(0, 0, "t"))))
                ],
                [
                    NDynamicArrayType(0, 0, NIdentifierType(0, 0, None, NIdentifier(0, 0, "t")))
                ]
            ),
            -1
        )
    ]
)

builtInFunsDict["len"] = FunListEntry(
    [
        TemplateEntry(
            "",
            [
                NIdentifier(0, 0, "t")
            ],
            FunSignature(
                False,
                False,
                "len",
                [
                    NNormalParam(0, 0, False, False, NIdentifier(0, 0, "array"), NDynamicArrayType(0, 0, NIdentifierType(0, 0, None, NIdentifier(0, 0, "t"))))    
                ],
                [
                    NISizeType(0, 0)
                ]
            ),
            -1
        )
    ]
)


builtInFunsDict["remove_last"] = FunListEntry(
    [
        TemplateEntry(
            "",
            [
                NIdentifier(0, 0, "t")
            ],
            FunSignature(
                False, 
                False,
                "remove_last",
                [
                    NRefParam(0, 0, NIdentifier(0, 0, "array"), NDynamicArrayType(0, 0, NIdentifierType(0, 0, None, NIdentifier(0, 0, "t")))),
                    NNormalParam(0, 0, False, False, NIdentifier(0, 0, "number_of_elements_to_remove"), NISizeType(0, 0)) 
                ],
                []
            ),
            -1
        ),
        TemplateEntry(
            "",
            [
                NIdentifier(0, 0, "t")
            ],
            FunSignature(
                False,
                False,
                "remove_last",
                [
                    NNormalParam(0, 0, False, True, NIdentifier(0, 0, "array"), NDynamicArrayType(0, 0, NIdentifierType(0, 0, None, NIdentifier(0, 0, "t")))),
                    NNormalParam(0, 0, False, False, NIdentifier(0, 0, "number_of_elements_to_remove"), NISizeType(0, 0))
                ],
                [
                    NDynamicArrayType(0, 0, NIdentifierType(0, 0, None, NIdentifier(0, 0, "t")))
                ]
            ),
            -1            
        )
    ]
)


builtInFunsDict["to_f32"] = FunListEntry(
    [
        FunEntry(
            "",
            FunSignature(
                False,
                False,
                "to_f32",
                [
                    NNormalParam(0, 0, False, False, NIdentifier(0, 0, "f"), NF64Type(0, 0))
                ],
                [
                    NF32Type(0, 0)
                ]
            ),
            {},
            -1
        ),
        FunEntry(
            "",
            FunSignature(
                False,
                False,
                "to_f32",
                [
                    NNormalParam(0, 0, False, False, NIdentifier(0, 0, "i"), NISizeType(0, 0))
                ],
                [
                    NF32Type(0, 0)
                ]
            ),
            {},
            -1            
        ),
        FunEntry(
            "",
            FunSignature(
                False,
                False,
                "to_f32",
                [
                    NNormalParam(0, 0, False, False, NIdentifier(0, 0, "u"), NU8Type(0, 0))
                ],
                [
                    NF32Type(0, 0)
                ]
            ),
            {},
            -1            
        )
    ]
)


# TODO: add all the others here...
