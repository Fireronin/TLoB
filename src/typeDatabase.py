from extractor import *
from handlerV2 import *

class typeDatabase():
    def __init__(self):
        self.functions = {}
        self.types = {}
        self.typeclasses = {}
        self.parser = initalize_parser(start="tcl_type_full_list") 

    def getFunctionByName(self,name):
        return self.functions[name]
    
    def getTypeByName(self,name):
        return self.types[name]
    
    def getTypeclassByName(self,name):
        return self.typeclasses[name]

    def addUnparsedTypes(self,types):
        trasformed_types = parse_and_transform(types)
        for type in trasformed_types:
            if isinstance(type,Typeclass):
                self.typeclasses[type.full_name] = type
            else:
                self.types[type.full_name] = type

    def addUnparsedFunctions(self,functions):
        trasformed_functions = parse_and_transform(functions)
        for function in trasformed_functions:
            self.functions[function.full_name] = function

    def addPackage(self,package_name):
        load_package(package_name=package_name)
        funcs = list_funcs(package_name=package_name)
        types = read_all_types(package_name=package_name)
        self.addUnparsedTypes(funcs)
        self.addUnparsedFunctions(types)

    def checkToXMembership(self,type,typeclass):
        for instance in typeclass.instances:
            if type.name != instance.fields[0].name or type.package != instance.fields[0].package:
                continue
            accesed_type = instance.fields[1].type.name  
            for i,field in enumerate(instance.fields[0].type.fields):
                if field.name == accesed_type:
                    return type.fields[i].type
        return None

    def printTypes(self):
        for type in self.types:
            print(self.types[type])
    
    def printTypeclasses(self):
        for typeclass in self.typeclasses:
            print(self.typeclasses[typeclass])
        
    def printFunctions(self):
        for function in self.functions:
            print(self.functions[function])
    
    def printAll(self):
        self.printTypes()
        self.printTypeclasses()
        self.printFunctions()

    def printStats(self):
        print("Types:")
        print(len(self.types))
        print("Typeclasses:")
        print(len(self.typeclasses))
        print("Functions:")
        print(len(self.functions))