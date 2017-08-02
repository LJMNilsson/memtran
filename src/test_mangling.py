import name_mangler




mangledModuleName = name_mangler.mangle_basic_name("Björn$")

print(mangledModuleName)

mangledTypeName = name_mangler.mangle_type_name("monster_boat", mangledModuleName)

print(mangledTypeName)

mangledVarName = name_mangler.mangle_var_name("denotedA⊆B", mangledModuleName, True, [3, 26, 18])

print(mangledVarName)
