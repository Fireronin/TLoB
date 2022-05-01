from sympy import *
from parsingFormating import Proviso,Type_ide,Value,evaluateCustomStart
from typing import List,Dict,Union



def solveNumerical(provisos:List[Proviso],variables):
    sym: Dict[str,Symbol] = {}

    def type_ide_to_expr(proviso:Union[Type_ide,Value,str]):
        if type(proviso) == str:
            if proviso in sym:
                return sym[proviso]
            if proviso in variables and variables[proviso].value.value != None:
                if type(variables[proviso].value.value) == int:
                    return variables[proviso].value.value
                else:
                    raise Exception(f"Variable name: {proviso} value:{variables[proviso].value.value} is not an integer")

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
                return Eq(ceiling(exprs[0]/exprs[1]),exprs[2])
            if proviso.full_name == "Max":
                return Eq(max(exprs[0],exprs[1]),exprs[2])
            if proviso.full_name == "Log":
                return Eq(ceiling(log(exprs[0],2)),exprs[1])
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
        eq = type_ide_to_expr(proviso.type_ide)
        if eq == True:
            continue
        Eqs.append(eq)

    if len(Eqs) == 0:
        return {}

    sol = solve(Eqs,list(sym.values()))
    if len(sol)==0:
        print("Well sympy can't find solution, you are not satisfing provisos")
        raise Exception("Well sympy can't find solution, you are not satisfing provisos")
    outVars = {}
        
    newInformation = False
    for key,val in sol.items():
        if not val.is_Atom or val.is_Symbol:
            continue
        newInformation = True
        #check if after converting to int value didn't change
        if int(val) != val:
            raise Exception("Solution contains non integer values")
        outVars[key] = Value( int(val))
    
    if not newInformation:
        raise Exception("No new information, this suggest that resolution might be stuck stuck")

    return outVars

if __name__ == "__main__":
    #region test
    variables = {}
    provisos = evaluateCustomStart("""{ provisos { 
        {Add#(2,a,y)}
        {Add#(a,5,7)} 
        } }""","tcl_provisos")[1]
    print(solveNumerical(provisos,variables))
    #endregion
    pass