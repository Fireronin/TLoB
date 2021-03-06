from copy import deepcopy
from typing import Dict, Set

from numpy import var
from extractor import Type as ExType
from extractor import *
from handlerV2 import *
from thefuzz import process
import pickle
from provisoSolverV3 import solveNonNumerical


def fuzzyException(name,list,exception_string):
    potential_matches = process.extract(name, list, limit=5)
    string_of_matches = ""
    for match in potential_matches:
        if match[1] > 80:
            string_of_matches += str(match[0]) + " \n"
    if string_of_matches == "":
        string_of_matches += str(potential_matches[0][0]) + " \n"
    raise Exception(exception_string.format(name,string_of_matches))

def CAdd(context,s,value):
    if s not in context:
        context[s] = value
    else:
        context[s].populate(value)


class TypeDatabase():
    aliases: Dict[str,Alias] = {}
    types: Dict[str,Type] = {}
    functions: Dict[str,Function] = {}
    typeclasses: Dict[str,Typeclass] = {}
    structs: Dict[str,Struct] = {}
    packages: Set[str] = set()
    logged_funcs: bytes = b""
    logged_types: bytes = b""

    def __init__(self,load=False):
        if load:
            self.loadStateFromPickle()
        self.parser = initalize_parser(start="tcl_type_full_list")
        # remove file failed_types.json and failed_functions.json
        try:
            os.remove("failed_types.json")
            os.remove("failed_functions.json")
            os.remove("failed_loads.json")
        except:
            pass

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
        for type_string in types:
            if len(type_string) == 0:
                continue
            try:
                t_type = parse_and_transform(type_string)[0]
            except Exception as e:
                # type_string from str to bytes
                type_string = str(type_string, encoding='utf-8')
                #save type_string to file failed_types.json
                with open("failed_types.json","a") as f:
                    f.write(type_string + "\n")

                print(e)
                t_type = "Parsing failed"
            
            if issubclass(type(t_type),Type):
                self.types[t_type.full_name] = t_type
            if type(t_type) == Struct:
                self.structs[t_type.full_name] = t_type
            if type(t_type)== Typeclass:
                self.typeclasses[t_type.full_name] = t_type
            elif type(t_type) == Alias:
                self.aliases[t_type.full_name] = t_type
            else:
                if type(t_type) == str:
                    #save type_string to file failed_types.json
                    with open("failed_types.json","a") as f:
                        f.write(type_string + "\n")
                    continue

    def addUnparsedFunctions(self,functions):
        try:
            trasformed_functions = parse_and_transform(functions)
        except Exception as e:
            # functions from str to bytes
            functions = str(functions, encoding='utf-8')
            #save functions to file failed_functions.json
            with open("failed_functions.json","a") as f:
                f.write(functions + "\n")
            return
        for function in trasformed_functions:
            self.functions[function.full_name] = function

    def evaluateTypedef(self,typedef):
        for type in self.types:
            if str(self.types[type].name) == typedef:
                return self.types[type].type
        fuzzyException(typedef,list(self.types), "Typedef {} not found. \n Do you mean: \n{}")

    def loadPackage(self,package_name):
        try:
            load_package(package_name=package_name)
        except Exception as e:
            print("Failed to load package {}".format(package_name))
            print(e)
            #save same message to file failed_loads.json
            with open("failed_loads.json","a") as f:
                f.write("Failed to load package {} \n".format(package_name))
                f.write(str(e) + "\n")
            return package_name
        return package_name
    
    def addPackage(self,package_name):
        # add package to database
        if package_name in self.packages:
            return
        if self.loadPackage(package_name) == None:
            return
        self.packages.add(package_name)
        funcs = list_funcs(package_name=package_name)
        types = read_all_types(package_name=package_name)
        self.logged_funcs += funcs + b"\n"
        self.logged_types += b"\n".join(types) + b"\n"
        self.writeToFile()
        self.addUnparsedTypes(types)
        self.addUnparsedFunctions(funcs)
        
    def addPackages(self,packages):
        loaded = []
        for package_name in packages:
            if self.loadPackage(package_name) != None:
                loaded.append(package_name)
        for package_name in loaded:
            self.addPackage(package_name)
    
    def checkToXMembership(self,t_type,typeclass: Typeclass):
        for instance in typeclass.instances:
            if t_type.name != instance[0].fields[0].name or t_type.package != instance[0].fields[0].package:
                continue
            return True
        return None

    def toXResultingType(self,t_type,typeclass):
        for instance in typeclass.instances:
            start = instance[0].fields[0]
            end = instance[0].fields[1]
            if type(start) == ExType:
                if t_type.full_name == start.full_name:
                    variables = {}
                    for i,field in enumerate(start.fields):
                        variables[str(field)] = t_type.type_ide.fields[i]
                    
                    if type(end) == str:
                        return variables[end]
                    else:
                        if type(end) == ExType:
                            end_copy = deepcopy(end)
                            end_copy.type_ide = Type_ide(end.name,end.package)
                            end_copy.type_ide.fields = end_copy.fields
                            for i,field in enumerate(end.fields):
                                end_copy.type_ide.fields[i] = variables[field]
                            return end_copy
                        else:
                            raise Exception(f"Unknown type (or a function) on the left side {typeclass}")
        return Exception(f"{t_type} not found in {typeclass}")

    def mergeV2(self,a: Union[Value,Type_ide,str],b: Union[Value,Type_ide,str],context: Dict[str,Union[Value,Type_ide]]):
        a,b = deepcopy(a),deepcopy(b)
        if type(a) == str and type(b) != str:
            CAdd(context,a,b)
        if type(b) == str and type(a) != str:
            CAdd(context,b,a)
        
        if type(a) == str and type(b) == str:
            if a in context and b in context:
                assert context[a] == context[b]
            elif a in context:
                CAdd(context,b,context[a])
            elif b in context:
                CAdd(context,a,context[b])
            else: 
                newType = Type_ide("nothing")
                context[a] = newType
                context[b] = newType
        
        if type(a) == Value and type(b) == Value:
            if a.value == b.value:
                return context
            else:
                raise Exception(f"Cannot merge different values, {a} and {b}")
        if type(a) == Value and type(b) == Type_ide:
            #swap a and b
            return context
        if type(a) == Type_ide and type(b) == Value:
            #handle sudo types 
            return context
        if type(a) == Type_ide and type(b) == Type_ide:
            if a.full_name != b.full_name:
                raise Exception(f"Cannot merge different types, {a} and {b}")
            for i,pair in enumerate(zip(a.children,b.children)):
                fa,fb = pair
                context |= self.mergeV2(fa,fb,context)
        return context

    def merge(self,a: Union[Value,Type_ide],b: Union[Value,Type_ide]) -> Union[Value,Type_ide,str]:
        a,b = deepcopy(a),deepcopy(b)
        variables = {}
        if type(a) == str or type(b) == str:
            if type(a) == str:
                variables[a] = b
            if type(b) == str:
                variables[b] = a
                b = a
            return b,variables

        if type(a) == Value and type(b) == Value:
            if a == b:
                return a,variables
            else:
                raise Exception(f"Cannot merge different values, {a} and {b}")
        if type(a) == Value and type(b) == Type_ide:
            #swap a and b
            a,b = b,a
        if type(a) == Type_ide and type(b) == Value:
            #handle sudo types like,
            return b,variables
        if type(a) == Type_ide and type(b) == Type_ide:
            if a.full_name != b.full_name:
                raise Exception(f"Cannot merge different types, {a} and {b}")
            for i,pair in enumerate(zip(a.formals,b.formals)):
                fa,fb = pair
                merged_type,newVars = self.merge(fa.type_ide,fb.type_ide)
                a.formals[i].type_ide = merged_type
                
                for key,value in newVars.items():
                    if key in variables:
                        if type(variables[key]) == str:
                            pass
                        
                    variables[key] = value
            return a,variables
        raise Exception(f"Cannot merge {type(a)} and {type(b)} Something weird Happened")

    def applyVariables(self,t_type: Type_ide, variables) -> Union[Type_ide,Value,str]:
        if type(t_type) == str:
            if t_type in variables:
                return variables[t_type]
            return t_type
        if type(t_type) == Value:
            return t_type
        if type(t_type) == Type_ide:
            for i,field in enumerate(t_type.formals):
                t_type.formals[i].type_ide = self.applyVariables(t_type.formals[i].type_ide,variables)
            return t_type
        raise Exception(f"Cannot apply variables to {type(t_type)}")

    def solveTypeclass(self,typeclass: Typeclass,t_type: Type_ide) -> Type_ide:
        newVars = self.mergeV2(typeclass.type_ide,t_type,{})
        #append vars
        variables = newVars
        ok = False
        for left,right in typeclass.dependencies:
            #check if left is resolved
            ok = True
            for var in left:
                if not (var in variables and type(variables[var]) != str):
                    ok = False
                    break
                if ok:
                    break
            if ok:
                break
        if not ok:
            #resolving not possible
            raise Exception(f"Cannot resolve {typeclass}")
        
        for instance in typeclass.instances:
            if instance.inputs[0].type_ide == 'void':
                continue
            try:
                newVars = self.mergeV2(t_type,instance.type_ide,context={})
                newVars = self.solveProvisos(instance.provisos,newVars)
                t_type = self.applyVariables(t_type,newVars)
            except Exception as e:
                continue
            return t_type
        raise Exception(f"Cannot solve {typeclass} {t_type}")

    def solveProvisos(self,provisos,context):
        if provisos == []:
            return context
        #scan for type class provisos
        NonTypeClassProvisos = ["None::Add","None::Mul","None::Div","None::Max","None::Log"]
        numerical = []
        nonNumerical = []

        for proviso in provisos:
            if proviso.full_name in NonTypeClassProvisos:
                numerical.append(proviso)
            else:
                nonNumerical.append(proviso)

        lastTodo = nonNumerical
        toDo = []
        while len(lastTodo) != 0:
            for proviso in lastTodo:
                if proviso.full_name not in self.typeclasses:
                    self.loadPackage(proviso.package)
                    if proviso.full_name not in self.typeclasses:
                        raise Exception(f"{proviso} not found, even after loading package {proviso.package}")
                try:
                    transformed = deepcopy(proviso.type_ide)
                    transformed = self.applyVariables(transformed,context)
                    newTypeIde = self.solveTypeclass(self.typeclasses[proviso.full_name],transformed)
                except Exception as e:
                    toDo.append(proviso)
                    continue
                
                context |= self.mergeV2(proviso.type_ide,newTypeIde,context)
                
            
            # if len(toDo) == len(lastTodo):
            #     continue
            #     #raise Exception(f"Cannot solve provisos {provisos}")
            # else:
            lastTodo = toDo
            toDo = []

        context |= solveNonNumerical(numerical,context)
        
        return context



    def evaluateAlias(self,alias):
        if alias in self.aliases:
            return self.aliases[alias].type
        else:
            package,name = alias.split("::")
            if package != "None":
                self.addPackage(package)
                if alias in self.aliases:
                    return self.aliases[alias].type
            print("Alias {} not found".format(alias))
            return None
            #fuzzyException(alias,list(self.aliases.keys()), "Alias {} not found. \n Do you mean: \n{}")
    

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

    def saveStateToPickle(self):
        with open("typeDatabase.pickle","wb") as f:
            pickle.dump(self,f)
            f.close()

    def loadStateFromPickle(self):
        with open("typeDatabase.pickle","rb") as f:
            self = pickle.load(f)
            f.close()
        return self