from math import log2
from constraint import *
problem = Problem()

problem.addVariable("a", [1,2,3])
problem.addVariable("b", [1,2,3])

problem.addVariable("c", [1,2,4,5,8])

problem.addConstraint(lambda a, b,c: a+b == int(log2(c)) , ("a", "b","c"))

problem.getSolutions()