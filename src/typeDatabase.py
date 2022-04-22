from copy import deepcopy, copy
from typing import Dict, Set

from numpy import var
from extractor import Type as ExType
from extractor import *
from handlerV2 import Handler
from thefuzz import process
import pickle
from provisoSolverV3 import solveNumerical


def fuzzyException(name,list,exception_string):
    potential_matches = process.extract(name, list, limit=5)
    string_of_matches = ""
    for match in potential_matches:
        if match[1] > 80:
            string_of_matches += str(match[0]) + " \n"
    if string_of_matches == "":
        string_of_matches += str(potential_matches[0][0]) + " \n"
    raise Exception(exception_string.format(name,string_of_matches))

class Variable():
    value = None

    def __init__(self,value=None):
        self.value = value

def CAdd(variables:Dict[str,Variable],s,value):
    if s not in variables:
        variables[s] = Variable(deepcopy(value))
    else:
        if variables[s].value != value:
            raise Exception("Conflicting values for variable: "+s)
        else:
            variables[s].value = value

def variablesToStr(variables:Dict[str,Variable]):
    string = ""
    for s in variables:
        string += s + " = " + str(variables[s].value) + "\n"
    return string

class TypeDatabase():
    aliases: Dict[str,Alias] = {}
    types: Dict[str,Type] = {}
    functions: Dict[str,Function] = {}
    typeclasses: Dict[str,Typeclass] = {}
    structs: Dict[str,Struct] = {}
    functionNameCache: Dict[str,str] = {}
    packages: Set[str] = set()
    logged_funcs: bytes = b""
    logged_types: bytes = b""
    handler: Handler

    def __init__(self,load=True,saveLocation=os.path.join(".","saved"),librariesRoot='/mnt/e/Mega/Documents/CS/TLoB'):
        self.saveLocation = saveLocation
        #check if saveLocation exists
        if not os.path.exists(saveLocation):
            os.mkdir(saveLocation)
        loaded = False
        self.handler = Handler(librariesRoot)
        if load:
            try:
                self.loadStateFromPickle()
                loaded = True
                self.functionNameCache = {function.name:function.full_name for function in self.functions.values()}
                print("Loaded state from pickle")
            except Exception as e:
                print("Failed to load typeDatabase state from pickle")
        self.parser = initalize_parser(start="tcl_type_full_list")
        # remove file failed_types.json and failed_functions.json
        if not loaded:
            FILES = ["failed_types.json","failed_functions.json","typeDatabase.pickle","typeDatabaseFunctions.json","typeDatabaseTypes.json"]
            for file in FILES:
                try:
                    if os.path.exists(os.path.join(saveLocation,file)):
                        os.remove(os.path.join(saveLocation,file))
                except Exception as e:
                    print(e)
                    print("Failed to remove file: " + file)
    
    def addLibraryFolder(self,folder):
        self.handler.add_folder(folder)

    
    def populateFunctionNames(self):
        
        # add functions from typeclasses
        for typeclass in self.typeclasses:
            for member in self.typeclasses[typeclass].members.values():
                if type(member) == Function:
                    self.functions[member.full_name] = member

        proposedAdditions = {}
        duplicateNames = set()
        for function in self.functions.values():
            if function.name in self.functionNameCache:
                duplicateNames.add(function.name)
                continue
            if function.name not in self.functions:
                proposedAdditions[function.name] = function            

        for key,value in proposedAdditions.items():
            if key in duplicateNames:
                continue
            self.functionNameCache[key] = value.full_name

    def getFunctionByName(self,name):
        if name in self.functions:
            return deepcopy(self.functions[name])
        else:
            if name in self.functionNameCache:
                return deepcopy(self.functions[self.functionNameCache[name]])
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
                self.preprocessTypeclass(t_type)
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
        if typedef == None:
            return typedef
        if type(typedef) == str:
            return typedef
        if type(typedef) == Value:
            return typedef
        if typedef.name in self.aliases:
            return self.aliases[typedef.name].result_type_ide
        else:
            return typedef

    def _loadPackage(self,package_name):
        try:
            self.handler.load_package(package_name=package_name)
        except Exception as e:
            print("Failed to load package {}".format(package_name))
            print(e)
            #save same message to file failed_loads.json
            with open("failed_loads.json","a") as f:
                f.write("Failed to load package {} \n".format(package_name))
                f.write(str(e) + "\n")
            return package_name
        return package_name
    
    def _addPackage(self,package_name):
        # add package to database
        if package_name in self.packages:
            return
        if self._loadPackage(package_name) == None:
            return
        self.packages.add(package_name)
        funcs = self.handler.list_funcs(package_name=package_name)
        types = self.handler.read_all_types(package_name=package_name)
        self.logged_funcs += funcs + b"\n"
        self.logged_types += b"\n".join(types) + b"\n"
        self.writeToFile()
        self.addUnparsedTypes(types)
        self.addUnparsedFunctions(funcs)
        
    def addPackages(self,packages):
        loaded = []
        for package_name in packages:
            if package_name in self.packages:
                continue
            if self._loadPackage(package_name) != None:
                loaded.append(package_name)
        for package_name in loaded:
            self._addPackage(package_name)
        self.saveStateToPickle()
        self.populateFunctionNames()
    
    def loadDependencies(self):
        known_packages = self.handler.list_packages()
        self.addPackages(known_packages)

    def merge(self,a: Union[Value,Type_ide,str,Function],b: Union[Value,Type_ide,str,Function],variables: Dict[str,Variable]):
        a,b = deepcopy(self.evaluateTypedef(a)),deepcopy(self.evaluateTypedef(b))
        if type(a) == Type_ide and a.is_polymorphic:
            a = a.name
        if type(b) == Type_ide and b.is_polymorphic:
            b = b.name
        if type(a) == str and type(b) != str:
            CAdd(variables,a,b)
        if type(b) == str and type(a) != str:
            CAdd(variables,b,a)
        
        if type(a) == str and type(b) == str:
            if a in variables and b in variables:
                assert variables[a] == variables[b]
            elif a in variables:
                CAdd(variables,b,variables[a])
            elif b in variables:
                CAdd(variables,a,variables[b])
            else: 
                CAdd(variables,a,None)
                variables[b] = variables[a]         
        
        if type(a) == Value and type(b) == Value:
            if a.value == b.value:
                return variables
            else:
                raise Exception(f"Cannot merge different values, {a} and {b}")
        if a == None or b == None:
            return variables
        
        if type(a) == Value and type(b) == Type_ide:
            a,b = b,a
        if type(a) == Type_ide and type(b) == Value:
            #handle sudo types 
            if type(b.value) == str:
                if a.full_name != "String":
                    raise Exception(f"Cannot merge {a} and {b} because {a} is not a string")
            if type(b.value) == int:
                if a.full_name == "String":
                    raise Exception(f"Cannot merge {a} and {b} because {a} is a string and {b} is an int")
            return variables
        if type(a) == Type_ide and type(b) == Type_ide:
            if a.full_name != b.full_name:
                raise Exception(f"Cannot merge different types, {a} and {b}")
            for i,pair in enumerate(zip(a.children,b.children)):
                fa,fb = pair
                newVariables = self.merge(fa,fb,variables)
                for key in newVariables:
                    CAdd(variables,key,newVariables[key].value)
        if type(b) == Function and type(a) != Function:
            a,b = b,a
        if type(a) == Function and type(b) != Function and type(b) != str:
            raise Exception(f"Cannot merge {a} and {b}")
        if type(a) == Function and type(b) == Function:
            newVariables = self.merge(a.return_type,b.return_type,variables)
            for key in newVariables.keys():
                CAdd(variables,key,newVariables[key].value)
            if len(a.arguments) != len(b.arguments):
                raise Exception(f"Cannot merge functions with different number of arguments, {a} and {b}")
            for pair in zip(a.arguments.values(),b.arguments.values()):
                fa,fb = pair
                newVariables = self.merge(fa,fb,variables)
                for key in newVariables.keys():
                    CAdd(variables,key,newVariables[key].value)

        return variables

    def applyVariables(self,t_type: Type_ide, variables) -> Union[Type_ide,Value,str]:
        if type(t_type) == str:
            if t_type in variables:
                if variables[t_type].value == None:
                    return t_type
                return variables[t_type].value
            return t_type
        if type(t_type) == Value:
            return t_type
        if type(t_type) == Type_ide:
            if t_type.full_name in variables:
                return variables[t_type.full_name].value
            for i,field in enumerate(t_type.formals):
                t_type.formals[i].type_ide = self.applyVariables(t_type.formals[i].type_ide,variables)
            return t_type
        if type(t_type) == Function:
            t_type.return_type = self.applyVariables(t_type.return_type,variables)
            for i,arg in t_type.arguments.items():
                t_type.arguments[i] = self.applyVariables(t_type.arguments[i],variables)
            return t_type
        raise Exception(f"Cannot apply variables to {type(t_type)}")

    def preprocessTypeclass(self,typeclass: Typeclass):
        lookUpDictionaries: Dict[Dict[str,str],List[Typeclass_instance]] = {}
        universalInstances: List[Typeclass_instance] = []
        for instance in typeclass.instances:
            skip = False
            for input in instance.inputs:
                if type(input.type_ide) == str and input.type_ide == 'void':
                    skip = True
                if type(input.type_ide) == Function:
                    skip = False
            if skip:
                continue
            variables = self.merge(typeclass.type_ideAlpha,instance.type_ide,{})  

            if len(typeclass.dependencies) != 0:
                for left,right in typeclass.dependencies:
                    fail = False
                    keyDict = {}
                    for var in left:
                        if var in variables:
                            value = variables[var].value
                            if value == None:
                                fail = True
                            else:
                                keyDict[var] = value.full_name
                    if fail:
                        universalInstances.append(instance)
                        break
                    lookUpDictionaries[str(keyDict)] = lookUpDictionaries.get(str(keyDict),[]) + [instance]
            else:
                keyDict = {}
                for member in typeclass.type_ideAlpha.children:
                    if member in variables:
                        memberValue = variables[member].value
                        if memberValue == None:
                            universalInstances.append(instance)
                            break
                        keyDict[member] = memberValue.full_name
                lookUpDictionaries[str(keyDict)] = lookUpDictionaries.get(str(keyDict),[]) + [instance]
        
        typeclass.lookUpDictionaries = lookUpDictionaries
        typeclass.universalInstances = universalInstances

    def resolveTypeclass(self,typeclass: Typeclass,t_type: Type_ide,instance_hint:Typeclass_instance=None) -> Type_ide:
        typeclass = self.getTypeclassByName(typeclass.full_name)
        variables = self.merge(typeclass.type_ideAlpha,t_type,{})
        #append vars
        keyDict = {}
        considered_instances = copy( typeclass.universalInstances)
        if len(typeclass.dependencies) != 0:
            ok = False
            for left,right in typeclass.dependencies:
                #check if left is resolved
                ok = True
                for var in left:
                    if var in variables:
                        if variables[var].value == None:
                            ok = False
                            break
                        keyDict[var] = variables[var].value.full_name
                if ok:
                    considered_instances = typeclass.lookUpDictionaries[str(keyDict)]+typeclass.universalInstances
                    break
            if not ok:
                pass
        else:
            keyDict = {}
            for member in typeclass.type_ideAlpha.children:
                if member in variables:
                    if variables[member].value == None:
                        continue
                    keyDict[member] = variables[member].value.full_name
            considered_instances += typeclass.lookUpDictionaries.get(str(keyDict),[])
        
        for instance in considered_instances:
            try:
                newVars = self.merge(t_type,instance.type_ide,variables={})
                newVars = self.solveProvisos(instance.provisos,newVars)
                solvedInstance = self.applyVariables(deepcopy(instance.type_ide),newVars)
                solvedVariables = self.merge(typeclass.type_ide,solvedInstance,{})
            except Exception as e:
                continue
            self.merge(t_type,instance.type_ide,variables={})
            return solvedVariables
        raise Exception(f"Cannot solve {typeclass} {t_type}")

    def solveProvisos(self,provisos,variables):
        if provisos == []:
            return variables
        #scan for type class provisos
        NonTypeClassProvisos = ["Add","Mul","Div","Max","Log"]
        numerical = []
        nonNumerical = []

        for proviso in provisos:
            if proviso.full_name in NonTypeClassProvisos:
                numerical.append(proviso)
            else:
                if proviso.full_name == 'IsModule':
                    continue
                if proviso.full_name not in self.typeclasses:
                    self._loadPackage(proviso.package)
                    if proviso.full_name not in self.typeclasses:
                        raise Exception(f"{proviso} not found, even after loading package {proviso.package}")
                nonNumerical.append(proviso)
            


        lastTodo = nonNumerical
        toDo = []
        while len(lastTodo) != 0:
            numericalProgress = False
            if len(numerical) != 0:
                numericalProgress = True
                try:
                    solvedVariables = solveNumerical(numerical,variables)
                
                    for key,val in solvedVariables.items():
                        CAdd(variables,key,val)        

                    # for key in variables.keys():
                    #     if type(variables[key].value.name) == Value:
                    #         variables[key] = variables[key].name
                except Exception as e:
                    numericalProgress = False

            for proviso in lastTodo:
                try:
                    transformed = deepcopy(proviso.type_ide)
                    transformed = self.applyVariables(transformed,variables)
                    newVariables = self.resolveTypeclass(self.typeclasses[proviso.full_name],transformed)
                except Exception as e:
                    toDo.append(proviso)
                    continue
                
                variables |= newVariables
                
            
            if len(toDo) == len(lastTodo) and not numericalProgress:  
                raise Exception(f"Cannot solve provisos {provisos} with variables \
                {variablesToStr(variables)}")
            else:
                lastTodo = toDo
                toDo = []

        return variables

    def populateMembers(self,t_type : Type_ide):
        if type(t_type) == Value or type(t_type) == Function:
            t_type.members = {}
            return
        if t_type.full_name not in self.types:
            if t_type.full_name == "nothing":
                raise Exception("Cannot populate members of nothing")
            if t_type.full_name != "nothing":
                print(f"{t_type.full_name} not found")
            return
        other = self.types[t_type.full_name]
        variables = self.merge(t_type,other.type_ide,{})
        t_type.members = {}
        for key in other.members.keys():
            if type(other.members[key]) == Function:
                t_type.members[key] = self.applyVariables(deepcopy(other.members[key]),variables)
                t_type.members[key].accessName = key
            if type(other.members[key]) == Type_ide:
                t_type.members[key] = self.applyVariables(deepcopy(other.members[key]),variables)
                t_type.members[key].accessName = key
            if type(other.members[key]) == Interface:
                t_type.members[key] = self.applyVariables(deepcopy(other.members[key].type_ide),variables)
                t_type.members[key].accessName = key
            self.populateMembers(t_type.members[key])
        return

    def evaluateAlias(self,alias):
        if alias in self.aliases:
            return self.aliases[alias].type
        else:
            package,name = alias.split("::")
            if package != "None":
                self._addPackage(package)
                if alias in self.aliases:
                    return self.aliases[alias].type
            print("Alias {} not found".format(alias))
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

    def writeToFile(self):
        with open(os.path.join(self.saveLocation,"typeDatabaseFunctions.json"),"w") as f:
            # convert to string
            f.write(self.logged_funcs.decode("utf-8"))
            f.close()
        with open(os.path.join(self.saveLocation,"typeDatabaseTypes.json"),"w") as f:
            # convert to string
            f.write(self.logged_types.decode("utf-8"))
            f.close()

    def saveStateToPickle(self):
        with open(os.path.join(self.saveLocation,"typeDatabase.pickle"),"wb") as f:
            d = {}
            d["types"] = self.types
            d["typeclasses"] = self.typeclasses
            d["functions"] = self.functions
            d["aliases"] = self.aliases
            d["packages"] = self.packages
            d["structs"] = self.structs
            d["logged_funcs"] = self.logged_funcs
            d["logged_types"] = self.logged_types
            d["functionNameCache"] = self.functionNameCache
            pickle.dump(d,f)
            f.close()

    def loadStateFromPickle(self):
        with open(os.path.join(self.saveLocation,"typeDatabase.pickle"),"rb") as f:
            d = pickle.load(f)
            self.types = d["types"]
            self.typeclasses = d["typeclasses"]
            self.functions = d["functions"]
            self.aliases = d["aliases"]
            self.packages = d["packages"]
            self.structs = d["structs"]
            self.logged_funcs = d["logged_funcs"]
            self.logged_types = d["logged_types"]
            self.functionNameCache = d["functionNameCache"]
            f.close()