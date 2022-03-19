from math import log2
from sympy import *
from numpy import positive

INTMAX = 10 #2**31-1

counter = 0

class Proviso:
    name: str

    def __init__(self, name, args):
        self.name = name
        self.args = args
        self.fullName = name + str(counter)

    def nameOf(self,index):
        if type(self.args[index]) == str:
            return self.args[index]
        elif type(self.args[index]) == int:
            return f"{self.fullName}_{str(self.args[index])}"


#resolveProvisos(examples)

#Rewrite above code to use sympy

def resolveProvisosSympy(provisos):
    constrains = []
    v = {}
    for proviso in provisos:
        for arg in proviso.args:
            if arg in v:
                continue
            if type(arg) == str:
                v[arg] = Symbol(arg,integer = True,positive=True)
            elif type(arg) == int:
                v[arg] = arg
        if proviso.name == "Add":
            constrains.append(Eq(v[proviso.args[0]]+v[proviso.args[1]],v[proviso.args[2]]))
        elif proviso.name == "Mul":
            constrains.append(Eq(v[proviso.args[0]]*v[proviso.args[1]],v[proviso.args[2]]))
        elif proviso.name == "Div":
            constrains.append(Eq(v[proviso.args[0]]/v[proviso.args[1]],v[proviso.args[2]]))
        elif proviso.name == "Max":
            constrains.append(Eq(max(v[proviso.args[0]],v[proviso.args[1]]),v[proviso.args[2]]))
        elif proviso.name == "Log":
            constrains.append(Eq(Pow(2,v[proviso.args[1]]),v[proviso.args[0]]))

    print(constrains)
    s = []
    for sy in v.values():
        if type(sy) == Symbol:
            s.append(sy)
    sol = nonlinsolve(constrains,s)
    try:
        output = list(sol)[0]
    except Exception as e:
        print("Well sympy can't find solution, you are not satisfing provisos")
        raise Exception("Well sympy can't find solution, you are not satisfing provisos")
    outVars = {}
    for i,variable in enumerate(s):
        #check if after converting to int value didn't change
        if int(output[i]) != output[i]:
            raise Exception("Solution contains non integer values")
        outVars[str(s[i])] = int(output[i])
    return outVars


examples = [Proviso("Add",["a","b",5]),Proviso("Mul",["a","b",6]) ]

examples2 = [Proviso("Log",["a",3]),Proviso("Mul",["a","b",8*3]) ]

resolveProvisosSympy(examples)

for ex in [examples,examples2]:
    print(resolveProvisosSympy(ex))