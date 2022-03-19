from math import log2
from constraint import *

INTMAX = 30 #2**31-1

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


def resolveProvisos(provisos):
    problem = Problem()

    def provisoAdd(a,b,c):
        problem.addConstraint(lambda a,b,c: a+b == c ,(a,b,c))
    
    def provisoMul(a,b,c):
        problem.addConstraint(lambda a,b,c: a*b == c ,(a,b,c))

    def provisoDiv(a,b,c):
        problem.addConstraint(lambda a,b,c: a/b == c ,(a,b,c))

    def provisoMax(a,b,c):
        problem.addConstraint(lambda a,b,c: max(a,b) == c ,(a,b,c))
    
    def provisoLog(a,b):
        problem.addConstraint(lambda a,b: a == int(log2(b)) ,(a,b))

    variables = {}
    for proviso in provisos:
        for i,arg in enumerate(proviso.args):
            if proviso.nameOf(i) in variables:
                continue
            if type(arg) == int:
                problem.addVariable(proviso.nameOf(i),[arg])
            else:
                problem.addVariable(proviso.nameOf(i),range(0,INTMAX))    
            variables[proviso.nameOf(i)] = arg
            
            

    for proviso in provisos:
        if proviso.name == "Add":
            provisoAdd(proviso.nameOf(0),proviso.nameOf(1),proviso.nameOf(2))
        elif proviso.name == "Mul":
            provisoMul(proviso.nameOf(0),proviso.nameOf(1),proviso.nameOf(2))
        elif proviso.name == "Div":
            provisoDiv(proviso.nameOf(0),proviso.nameOf(1),proviso.nameOf(2))
        elif proviso.name == "Max":
            provisoMax(proviso.nameOf(0),proviso.nameOf(1),proviso.nameOf(2))
        elif proviso.name == "Log":
            provisoLog(proviso.nameOf(0),proviso.nameOf(1))
        else:
            raise Exception("Unknown proviso: "+proviso)
    
    iter = problem.getSolutionIter()
    print(next(iter))

examples = [Proviso("Add",["a","b",5]),Proviso("Mul",["a","b",6]) ]

resolveProvisos(examples)