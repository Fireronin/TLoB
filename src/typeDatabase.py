from logging import Handler
from extractor import *
from handlerV2 import *
from thefuzz import process

def fuzzyException(name,list,exception_string):
    potential_matches = process.extract(name, list, limit=5)
    string_of_matches = ""
    for match in potential_matches:
        if match[1] > 80:
            string_of_matches += str(match[0]) + " \n"
    if string_of_matches == "":
        string_of_matches += str(potential_matches[0][0]) + " \n"
    raise Exception(exception_string.format(name,string_of_matches))
    

class typeDatabase():
    def __init__(self):
        self.packages = set()
        self.functions = {}
        self.types = {}
        self.typeclasses = {}
        self.parser = initalize_parser(start="tcl_type_full_list") 
        self.logged_funcs = b""
        self.logged_types = b""
        if child is None:
            create_bluetcl()

    def getFunctionByName(self,name):
        if name in self.functions:
            return self.functions[name]
        fuzzyException(name,list(self.functions), "Function {} not found. \n Do you mean: \n{}")
    
    def getTypeByName(self,name):
        if name in self.types:
            return self.types[name]
        fuzzyException(name,list(self.types), "Type {} not found. \n Do you mean: \n{}")
    
    def getTypeclassByName(self,name):
        if name in self.typeclasses:
            return self.typeclasses[name]
        fuzzyException(name,list(self.typeclasses), "Typeclass {} not found. \n Do you mean: \n{}")

    def addUnparsedTypes(self,types):
        transformed_types = parse_and_transform(types)
        for t_type in transformed_types:
            if type(t_type)== Typeclass:
                self.typeclasses[t_type.full_name] = t_type
            else:
                if type(t_type) == str:
                    continue
                self.types[t_type.full_name] = t_type

    def addUnparsedFunctions(self,functions):
        trasformed_functions = parse_and_transform(functions)
        for function in trasformed_functions:
            self.functions[function.full_name] = function

    def evaluateTypedef(self,typedef):
        for type in self.types:
            if str(self.types[type].name) == typedef:
                return self.types[type].type
        fuzzyException(typedef,list(self.types), "Typedef {} not found. \n Do you mean: \n{}")

    def addPackage(self,package_name):
        # add package to database
        self.packages.add(package_name)
        funcs = list_funcs(package_name=package_name)
        types = read_all_types(package_name=package_name)
        self.logged_funcs += funcs + b"\n"
        self.logged_types += types + b"\n"
        self.writeToFile()
        self.addUnparsedTypes(types)
        self.addUnparsedFunctions(funcs)
        
    def addPackages(self,packages):
        for package in packages:
            load_package(package_name=package)
        for package in packages:
            self.addPackage(package)

    def checkToXMembership(self,t_type,typeclass):
        for instance in typeclass.instances:
            if t_type.name != instance[0].fields[0].name or t_type.package != instance[0].fields[0].package:
                continue
            return True
        return None

    def checkifConnectable(self,type1,type2):
        connectableTypeclass = self.getTypeclassByName("Connectable.Connectable")
        for instance in connectableTypeclass.instances:
            variables1 = {}
            variables2 = {}
            if instance[0].fields[0].name == type1.name and instance[0].fields[0].package == type1.package and \
                instance[0].fields[1].name == type2.name and instance[0].fields[1].package == type2.package:
                for field in instance[0].fields[0].fields:
                   pass 

    def checkMembership(self,type,typeclass):
        # TODO: check if type is a member of typeclass
        pass

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

    def writeToFile(self):
        with open("typeDatabaseFuncs.json","w") as f:
            # convert to string
            f.write(self.logged_funcs.decode("utf-8"))
            f.close()
        with open("typeDatabaseTypes.json","w") as f:
            # convert to string
            f.write(self.logged_types.decode("utf-8"))
            f.close()