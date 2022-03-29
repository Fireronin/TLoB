from sympy import *
from extractor import Proviso,Type_ide,Value
from typing import List,Dict,Union



def solveNonNumerical(provisos:List[Proviso],variables):
    sym: Dict[str,Symbol] = {}
    # to_remove = []
    # for var in variables.keys():
    #     if variables[var].full_name == 'nothing':
    #         to_remove.append(var)
        
    # for var in to_remove:
    #     del variables[var]

    def type_ide_to_expr(proviso:Union[Type_ide,Value,str]):
        if type(proviso) == str:
            if proviso in sym:
                return sym[proviso]
            if proviso in variables and variables[proviso].full_name != 'nothing':
                if type(variables[proviso].value) == int:
                    return variables[proviso].value
                else:
                    raise Exception("Variable is not an integer")

            sym[proviso] = Symbol(proviso,intiger=True,negative=False)
            return sym[proviso]
        if type(proviso) == Value:
            if type(proviso.value) != int:
                raise Exception("Value is not an int")
            return proviso.value
        if type(proviso) == Type_ide:
            #region go through special cases
            exprs = []
            for formal in proviso.formals:
                exprs.append(type_ide_to_expr(formal.type_ide))
            if proviso.full_name == "Add":
                return Eq(exprs[0]+exprs[1],exprs[2])
            if proviso.full_name == "Mul":
                return Eq(exprs[0]*exprs[1],exprs[2])
            if proviso.full_name == "Div":
                return Eq(exprs[0]/exprs[1],exprs[2])
            if proviso.full_name == "Max":
                return Eq(max(exprs[0],exprs[1]),exprs[2])
            if proviso.full_name == "Log":
                return Eq(log(exprs[0],2),exprs[1])
            #those sus types
            if proviso.full_name == "TAdd":
                return exprs[0]+exprs[1]
            if proviso.full_name == "TSub":
                return exprs[0]-exprs[1]
            if proviso.full_name == "TMul":
                return exprs[0]*exprs[1]
            if proviso.full_name == "TDiv":
                return ceiling(exprs[0]/exprs[1])
            if proviso.full_name == "TLog":
                return ceiling(log(exprs[0],2))
            if proviso.full_name == "TExp":
                return 2**exprs[0]
            if proviso.full_name == "TMax":
                return max(exprs[0],exprs[1])
            if proviso.full_name == "TMin":
                return min(exprs[0],exprs[1])
            raise Exception("Unknown proviso: "+proviso.full_name)
            #endregion

    Eqs = []    
    for proviso in provisos:
        Eqs.append(type_ide_to_expr(proviso.type_ide))

    sol = nonlinsolve(Eqs,list(sym.values()))
    try:
        output = list(sol)[0]
    except Exception as e:
        print("Well sympy can't find solution, you are not satisfing provisos")
        raise Exception("Well sympy can't find solution, you are not satisfing provisos")
    outVars = {}

    if len(output.free_symbols) != 0:
        # print free symbols
        print("Free symbols")
        for sym in output.free_symbols:
            print(sym)
        raise Exception("Too many solutions")
        
    
    for i,key in enumerate(sym.keys()):
        #check if after converting to int value didn't change
        if int(output[i]) != output[i]:
            raise Exception("Solution contains non integer values")
        outVars[key] = Value( int(output[i]))
    return outVars