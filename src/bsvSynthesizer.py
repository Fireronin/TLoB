from copy import deepcopy
import os
import subprocess
import time
from tokenize import Number

from parsingFormating import Function, Position, Type as ExType, Type_ide, Value as ExValue
from parsingFormating import Interface as ExInterface
from parsingFormating import Type_formal as ExType_formal
from parsingFormating import Function as ExFunction, Module as ExModule
from parsingFormating import evaluateCustomStart
from parsingFormating import Alias as ExAlias
from parsingFormating import Typeclass as ExTypeclass
from parsingFormating import Typeclass_instance as ExTypeclassInstance

from typing import Dict, List, Union,Set,Tuple
import warnings
from typeDatabase import TypeDatabase,Variable
from tqdm import tqdm
import json
class AccessTuple():
    access_name: str
    thing = None

    def __init__(self,access_name: str,thing):
        self.access_name = access_name
        self.thing = thing
    
    def __repr__(self) -> str:
        return f"{self.access_name} {self.thing}"

class InstanceV2():
    pass

class TopLevelModule():
    pass


class InstanceV2():
    db: TypeDatabase
    type_ide : Type_ide
    creator: Union[ExFunction,ExModule]

    def __init__(self,topLevel:TopLevelModule,creator: ExType,
                creator_args : List[str] =[],
                module_args:List[str]=[],
                instance_name:str="",
                input_context:Dict[str,str]={}):
        self.topLevel = topLevel
        self.db = topLevel.db
        self.creator = creator
        for i,arg in enumerate(creator_args):
            if type(arg) == int:
                creator_args[i] = str(arg)
                continue
            if type(arg) != str:
                raise Exception("Creator args must be strings")
        for i,arg in enumerate(module_args):
            if type(arg) == int:
                module_args[i] = str(arg)
                continue
            if type(arg) != str:
                raise Exception("Module args must be strings")
        self.creator_args = creator_args
        self.instance_name = instance_name
        self.module_args = module_args
        self.input_context = {key:Variable(evaluateCustomStart(val)) for key,val in input_context.items()}
        self.variables = {}
        self.topLevel.addInstance(self,instance_name)
        if creator_args is not None:
            self.update()


    def list_all_Interfaces(self)->List[AccessTuple]:
        MAX_DEPTH = 1
        def visitRecursively(parent_name: str, interface: Type_ide,depth:int=1):
            if depth > 1:
                return
            for name,value in interface.members.items():
                full_name = f"{parent_name}.{name}"
                yield AccessTuple(full_name,value)
                yield from visitRecursively(full_name,value,depth+1) 
        return [AccessTuple(self.instance_name,self.creator.return_type)] + list(visitRecursively(self.instance_name,self.creator.return_type))

    def update(self):
        print(f"Updating {self.instance_name}")
        self.creator.return_type.accessName = self.instance_name
        
        if len(self.creator_args) < len(self.creator.arguments):
            print(f"{self.instance_name} has {len(self.creator_args)} arguments, but {self.creator.name} has {len(self.creator.arguments)}")
            raise Exception("Number of function arguments do not match the number of arguments required")
        #convert to TypeIde arguments
        creator_args = [self.topLevel.convertToTypeIde(arg,self.instance_name) for arg in self.creator_args]
        module_args = [self.topLevel.convertToTypeIde(arg,self.instance_name) for arg in self.module_args]

        context = deepcopy(self.input_context)
        for i,pair in  enumerate( zip(self.creator.arguments.items(),creator_args)):
            arg,value = pair
            if type(value) == InstanceV2:
                value = value.type_ide
            if isinstance(value, Type_ide):
                self.db.merge(arg[1],value,self.variables) 
                # for key,val in newVariables.items():
                #     self.db.CAdd(context,key,val)
            #this is just to check if everything is ok
            self.db.applyVariables(deepcopy(self.creator.arguments[arg[0]]),self.variables)

        ideCopy  = deepcopy(self.creator.return_type)
        if len(module_args) == 0:
            module_args = ["unknownArg$"+str(i) for i in range(len(ideCopy.formals))]
        for i,field in enumerate(ideCopy.formals):
            ideCopy.formals[i].type_ide = module_args[i]

        self.db.merge(self.creator.return_type,ideCopy,self.variables)

        #account for provisos
        self.variables = self.db.solveProvisos(self.creator.provisos,self.variables)
        self.creator.return_type = self.db.applyVariables(self.creator.return_type,self.variables)
        if self.creator.name == "mkConnection":
            return
        self.creator.return_type.accessName = self.instance_name
        
        self.db.populateMembers(self.creator.return_type)
        self.interfaces = self.list_all_Interfaces()
        for interface in self.interfaces:
            self.topLevel.addName(interface.access_name,interface.thing)

    def get(self):
        return AccessTuple(self.instance_name,self.creator.return_type)

    def to_string(self):
        if type(self.creator) == ExFunction:
            return f"{self.creator.name}({','.join(map(str,self.creator_args))});\n"

    def toJSON(self):
        json_dict = {
            "name" : self.instance_name,
            "function": self.creator.full_name,
            "function_params": self.creator_args,
            "interface_params": self.module_args
        }
        return json_dict


class VectorInstance():
    items: List[str]
    flit_type_ide:  Union[Type_ide,str]
    type_ide: Type_ide
    instance_name: str = None

    def __init__(self,topLevel,name):
        self.flit_type_ide= "flit"
        self.type_ide = evaluateCustomStart(f"Vector::Vector#(0,flit)","type_def_type")
        self.items = []
        self.instance_name = name
        self.db = topLevel.db
        self.topLevel = topLevel
        self.topLevel.addInstance(self,name)
        self.topLevel.addName(name,self.type_ide)

    def remove(self,item:str):
        self.items.remove(item)
        if len(self.items) == 0:
            self.flit_type_ide = "flit"
        self.type_ide = evaluateCustomStart(f"Vector::Vector#({len(self.items)},{self.flit_type_ide})","type_def_type")


    def add(self,item:str):
        itemType_ide = self.topLevel.convertToTypeIde(item,self.instance_name)
        try:
            context = self.db.merge(self.flit_type_ide,itemType_ide,{})
        except Exception as e:
            raise Exception("Adding item to vector failed types don't match")
        if len(self.items) == 0:
            self.flit_type_ide = itemType_ide
        self.items.append(item)
        self.type_ide = evaluateCustomStart(f"Vector::Vector#({len(self.items)},{self.flit_type_ide})","type_def_type")

    def update(self,silent=False):
        items =[self.topLevel.convertToTypeIde(item,self.instance_name) for item in self.items]
        try:
            for item in items:
                self.db.merge(self.flit_type_ide,item,{})
        except Exception as e:
            print("Failed updaitng vector")
            print(e)
            raise Exception("Adding item to vector failed types don't match")
        if not silent:
            self.topLevel.addName(self.instance_name,self.type_ide)

    def listAddable(self,proposed)->List[Tuple[str,Type_ide]]:
        out =[]
        for name,value in proposed:
            try:
                vars = self.db.merge(self.flit_type_ide,value,{})
            except Exception as e:
                continue
            out.append(name)
        return out
        

    def __str__(self):
        output_str = []
        output_str.append(f"\t{self.type_ide} {self.instance_name};\n")
        for i,item  in enumerate(self.items):
            output_str.append(f"\t{self.instance_name}[{i}] = {item};\n")
        return "".join(output_str)

class BusInstanceV3(InstanceV2):
    def __init__(self,topLevel:TopLevelModule,name,busCreator:str,masters:List[str],slaves:List[Tuple[str,List[Tuple[int,int]]]]):
        self.instance_name = name
        self.db = topLevel.db 
        self.topLevel = topLevel
        self.creator = self.db.getFunctionByName(busCreator)
        self.topLevel.addInstance(self,name)
        self.masters = masters
        self.slaves = slaves
        self.mastersV = VectorInstance(self.topLevel,name+"_masters")
        self.slavesV = VectorInstance(self.topLevel,name+"_slaves")
        for master in self.masters:
            self.mastersV.add(master)
        self.mastersV.update(silent=False)
        #addName(self.instance_name,self.type_ide)
        for slave in self.slaves:
            self.slavesV.add(slave[0])
        self.slavesV.update(silent=False)
        self.variables = {}
        #addName(self.instance_name,self.type_ide)
        self.creator_args = [f"route_{self.instance_name}",self.mastersV.type_ide,self.slavesV.type_ide]
        self.module_args = []
        self.input_context = {}
        
        self.update()


    def update(self):    
        functionString = \
        """
        {function route_{busName} {result Vector::Vector#({NSlaves}, Bool)
        } {arguments {
                {r_t 
                }
            }
        }
        {provisos {
                {Bits#(r_t,r_l)
                }
            }
        }	
        {position {../this.bsv 1 2
            }
        }
        }
        """
        functionString = functionString.replace("{NSlaves}",str(len(self.slaves)))
        functionString = functionString.replace("{busName}",self.instance_name)
        

        routingFunction = evaluateCustomStart(functionString,"tcl_function")
        self.creator_args[0] = routingFunction
        super().update()
        
    def routingFunctionString(self):
        """
        Generate a function that routes a flit from a master to a slave.
        """
        #check if there is at least one master and one slave
        if len(self.masters) == 0 or len(self.slaves) == 0:
            raise Exception(f"Bus {self.instance_name} has no masters or slaves. Slaves: {len(self.slaves)} Masters: {len(self.masters)}")

        output_str = []
        # generate routing function
        r_s = len(self.slaves)

        # create map from slave to id
        slave_to_id = {}
        for i, slave in enumerate(self.slaves):
            slave_to_id[slave[0]] = i
        output_str.append(f"function Vector #({r_s}, Bool) route_{self.instance_name} (r_t x) provisos ( Bits#(r_t,r_l) );\n")
        output_str.append(f"\tBit#(r_l) address = pack(x);\n")
        output_str.append(f"\tVector#({r_s}, Bool) oneHotaddress = replicate (False);\n")
        
        for name, route in self.slaves:
            if not route:
                raise Exception(f"Slave {name} has no route")
            slave_id = slave_to_id[name]
            output_str.append(f"\t// {name} -> {slave_id}\n")
            for start, end in route:
                output_str.append(f"\tif (address >= {start} && address < {end})\n")
                output_str.append(f"\t\toneHotaddress[{slave_id}] = True;\n")
        output_str.append(f"\treturn oneHotaddress;\n")
        output_str.append(f"endfunction\n\n")
        return "".join(output_str)

    def __str__(self):
        return f"\t{self.creator.full_name}(route_{self.instance_name},{self.mastersV.instance_name},{self.slavesV.instance_name});\n"

    def toJSON(self):
        json_dict = { 
            "name" : self.instance_name,
            "function": self.creator.full_name,
            "masters" : self.masters,
            "slaves" : [{
                "name" : slave[0],
                "routes" : [[start,end] for start,end in slave[1]]
            } for slave in self.slaves]
        }
        return json_dict

class TopLevelModule():
    db: TypeDatabase
    possibleConnections: Dict[str,List[str]] = {}
    accessableInterfaces: List[AccessTuple] = []
    cashed_considered_instances: Dict[str,AccessTuple] = {}

    modules: Dict[str,InstanceV2] = {}
    connections: Dict[str,InstanceV2] = {}
    buses: Dict[str,BusInstanceV3] = {}
    name: str
    package_name: str
    typedefs: Dict[str,ExAlias] = {}
    instances:Dict[str,InstanceV2] = {}
    knownNames:Dict[str,Type_ide] = {}
    subscribers:Dict[str,Set[str]] = {}
    exported_interface: ExInterface
    interface_members: Dict[str,str] = {}

    def __init__(self,name,db,package_name=None) -> None:
        self.possibleConnections = {}
        self.accessableInterfaces = []
        self.cashed_considered_instances = {}
        self.db = db
        self.modules = {}
        self.connections = {}
        self.buses = {}
        self.typedefs = {}
        self.instances = {}
        self.knownNames = {}
        self.subscribers = {}
        self.exported_interface: ExInterface = None
        self.name = name
        if package_name is None:
            self.package_name = name
        else:
            self.package_name = package_name
        self.db = db
        self.packages = set()

    @property
    def reversedPossibleConnections(self):
        out = {}
        for start,ends in self.possibleConnections.items():
            for end in ends:
                if end not in out:
                    out[end] = []
                out[end].append(start)
        return out

    def validArguments(self,function:Union[ExFunction,ExModule])->bool:
        validOptions = {}
        for key,arg in function.arguments.items():
            validList = []
            for name,value in self.knownNames.items():
                try:
                    self.db.merge(arg,value,{})
                except Exception as e:
                    continue
                validList.append(name)
            for name,value in self.db.aliases.items():
                try:
                    self.db.merge(arg,value.result_type_ide,{})
                except Exception as e:
                    continue
                validList.append(name)
            if type(arg) == ExFunction:
                for name,value in self.db.functions.items():
                    if type(value) == ExModule:
                        continue
                    try:
                        self.db.merge(arg,value,{})
                    except Exception as e:
                        continue
                    validList.append(name)
            validOptions[key] = validList
        return validOptions

    name_counter = 0
    def get_name(self):
        self.name_counter += 1
        return "_temp_" + str(self.name_counter)

    def convertToTypeIde(self,arg,caller=None):
        if isinstance(arg,Type_ide) or type(arg) == ExFunction:
            return arg
        arg = str(arg)
        if arg.startswith("tagged"):
            #for each struct in data base find struck with member with that name
            splited = arg.split(" ")
            for name,value in self.db.structs.items():
                for name in value.members.keys():
                    if name == splited[1]:
                        return value.type_ide  
            raise Exception(f"Could not find struct with member {splited[1]}")

        if arg[0].islower():
            if caller is not None:
                self.subscribers
                if arg not in self.subscribers:
                    self.subscribers[arg] = set()
                self.subscribers[arg].add(caller)
            if arg not in self.knownNames:
                return arg
            return self.knownNames[arg]
        if arg[0].isupper():
            type_t = evaluateCustomStart(arg,"type_def_type")
            return self.db.evaluateTypedef(type_t)
        return evaluateCustomStart(arg,"type_def_type")

    def addInstance(self,instance,name):
        if name in self.subscribers:
            #remove stale subscriptions
            for channel in self.subscribers.values():
                if name in channel:
                    channel.remove(name)
        self.instances[name] = instance

    def addName(self,name,type_ide):
        self.knownNames[name] = type_ide
        if name in self.subscribers:
            for subscriber in self.subscribers[name]:
                pass
                #self.instances[subscriber].update()

    def addModule(self,creator_func,instance_name,interface_args=[],func_args=[],input_context={}) -> InstanceV2:
        #check if instance name starts with upercase character
        if instance_name[0].isupper():
            raise Exception("Instance name must start with lowercase character")
        if type(creator_func) == str:
            creator_func = self.db.getFunctionByName(creator_func)
        #try:
        start_time = time.time()
        newModule = InstanceV2(self,creator_func,func_args,interface_args,instance_name,input_context=input_context)
        print(f"Created module {instance_name} in {time.time()-start_time}s")
        # except Exception as e:
        #     raise Exception(f"""Error creating module {instance_name}: {e}
        #         Arguments:
        #             creator function: {creator_func}
        #             function arguments: {func_args}
        #             interface arguments: {interface_args}
        #             instance name: {instance_name}
        #     """)
        
        #populate possible connections
        for current in tqdm(newModule.list_all_Interfaces()):
            #if number of dots in interface name is more than 1 skip
            if current.access_name.count(".") > 1:
                continue
            self.possibleConnections[current.access_name] =[x.access_name for x in self.listConnectable(current,self.accessableInterfaces)]
            for interface in self.accessableInterfaces:
                if interface.access_name not in self.possibleConnections:
                    self.possibleConnections[interface.access_name] = []
                if current.access_name not in self.possibleConnections[interface.access_name]: 
                    self.possibleConnections[interface.access_name] +=[x.access_name for x in self.listConnectable(interface,[current])]

        self.accessableInterfaces += newModule.list_all_Interfaces()

        self.modules[instance_name] = newModule
        return self.modules[instance_name]

    def addTypedef(self,name,type):
        self.typedefs[name] = type
        alias = ExAlias(Type_ide(name),evaluateCustomStart(str(type)),None)
        self.db.aliases[alias.full_name] = alias
        return name

    def listConnectable(self,start:AccessTuple,ends:List[AccessTuple]=[]):
        connectableTypeclass : ExTypeclass = self.db.getTypeByName("Connectable::Connectable")
        connectable_ends : List[AccessTuple]  = []
        for end in ends:
            if end.access_name.count(".") > 1:
                continue
            try:
                connection = deepcopy(connectableTypeclass.type_ide)
                connection.formals[0].type_ide = start.thing
                connection.formals[1].type_ide = end.thing
                self.db.resolveTypeclass(connectableTypeclass, connection)
            except Exception as e:
                continue
            connectable_ends.append(end)
        return connectable_ends

    def addConnection(self,start:str,end:str,connection_name:str=None):
        if connection_name is None:
            connection_name = f"connection_{len(self.connections)}"
        creator_func = self.db.getFunctionByName("mkConnection")
        connection = InstanceV2(self,creator_func,[start,end],[],connection_name)
        self.connections[connection_name] = connection

    def addBus(self,name,busCreator:str,masters:List[str],slaves:List[Tuple[str,List[Tuple[int,int]]]]):
        bI = BusInstanceV3(self,name,busCreator,masters,slaves)
        self.buses[name] = bI

    def setExportedInterface(self,name,members:Union[str,List[Tuple[str,str]]]):
        if type(members) == str:
            self.exported_interface = members
            return
        if name in self.db.types:
            self.exported_interface = deepcopy(self.db.types[name])
            variables = {}
            for name,value in members:
                if name == '':
                    name = value.replace(".","_")
                try:
                    variables = self.db.merge(self.exported_interface.members[name],self.knownNames[value],variables)
                except Exception as e:
                    raise Exception(f"Assigning member {name} to {value} failed: {e}")
            self.interface_members = {name:value for name,value in members}
            self.exported_interface = self.db.applyVariables(self.exported_interface,variables)
        else:
            self.exported_interface = ExInterface(Type_ide(deepcopy(name)),{})
            for name,value in members:
                self.exported_interface.members[name] = self.knownNames[value]
            #self.db.types[name] = self.exported_interface
            for name,value in members:
                if name == '':
                    name = value.replace(".","_")
                self.interface_members[name] =value
        
    def remove(self,name:str):
        #in accessable interfaces find name* use start with and fiter
        self.accessableInterfaces = list(filter(lambda x: not x.access_name.startswith(name),self.accessableInterfaces))
        if name in self.instances:
            if name in self.instances: 
                del self.instances[name]
        self.knownNames = {k:v for k,v in self.knownNames.items() if not k.startswith(name)}
        for subscriber in self.subscribers:
            if name in subscriber:
                if name in subscriber:
                    del subscriber[name]
        
        if name in self.modules:
            del self.modules[name]
        if name in self.connections:
            del self.connections[name]
        if name in self.buses:
            del self.buses[name]
        if name in self.typedefs:
            del self.typedefs[name]

    @property
    def topologicalySortedModules(self) -> List[str]:
        #self.subscribes have edges 
        edges = {}
        for name,subscribers in self.subscribers.items():
            instance_name = name.split(".")[0]
            if instance_name not in self.modules:
                warnings.warn(f"Instance {instance_name} not found in topological sort, this might be a function")
                continue
            for subscriber in subscribers:
                if subscriber not in self.modules:
                    continue
                if instance_name not in edges:
                    edges[instance_name] = []
                if subscriber not in edges[instance_name]:
                    edges[instance_name].append(subscriber)

        sorted_nodes = []
        visited = set()
        def topologicalSortHelper(node:str):
            if node in visited:
                return
            visited.add(node)
            for edge in edges[node]:
                topologicalSortHelper(edge)
            sorted_nodes.append(node)
        for node in edges:
            topologicalSortHelper(node)
        #reverse
        
        
        sorted_nodes.reverse()
        for module in self.modules.keys():
            if module not in sorted_nodes:
                sorted_nodes.append(module)
        return sorted_nodes

    @property
    def necessaryPackages(self) -> List[str]:
        packages = set(["Connectable","Vector"])
        for m in self.modules.values():
            if m.creator.package is not None:
                packages.add(m.creator.package)
            if m.creator.return_type.package is not None:
                packages.add(m.creator.return_type.package)
        for b in self.buses.values():
            if b.creator.package is not None:
                packages.add(b.creator.package)
        return list(packages)

    def __str__(self):
        s = []
        s.append("package "+self.package_name + ";\n")
        # necessary packages
        s.append("// necessary packages\n")
        for p in self.necessaryPackages:
            s.append("import "+p+"::*;\n")
        s.append("\n")

        for t in self.typedefs.keys():
            s.append("typedef " + str(self.typedefs[t]) + " " + str(t) + ";\n")
        s.append("\n")

        for bus in self.buses.values():
            s.append(bus.routingFunctionString())

        if self.exported_interface is not None and type(self.exported_interface) == ExInterface:
            if self.exported_interface.name not in self.db.types:
                s.append(f"interface {self.exported_interface.name};\n")
                for name,value in self.interface_members.items():
                    typeName = ""
                    value = self.knownNames[value]
                    if type(value) == Function:
                        typeName = "method"
                        value_copy = deepcopy(value)
                        value_copy.name = name
                        s.append(f"\t{typeName} {value_copy};\n")  
                    elif type(value) == Type_ide:
                        typeName = "interface"
                        s.append(f"\t{typeName} {value} {name};\n")  
                s.append(f"endinterface\n\n")

        interfaceString = ""
        if self.exported_interface is not None:
            if type(self.exported_interface) == str:
                interfaceString = str(self.knownNames[self.exported_interface])
            else:
                interfaceString = str(self.exported_interface.type_ide)

        s.append(f"module {self.name} ({interfaceString});\n \n")
        
        # add modules
        for name in self.topologicalySortedModules:
            m = self.modules[name]
            if m.creator_args is None:
                s.append("Awiaiting for args for ")
                continue
            s.append("\t")
        
            s.append(str(m.creator.return_type))
            s.append(" " + m.instance_name)
            s.append(" <- " + m.creator.name + "(")
            for i in range(len(m.creator_args)):
                s.append(str(m.creator_args[i]))
                if i != len(m.creator_args)-1:
                    s.append(", ")
            s.append(");\n")
        s.append("\n")

        # add connections
        for c in self.connections.values():
            s.append("\t"+c.to_string())
        s.append("\n")


        for bus in self.buses.values():
            s.append(str(bus.mastersV))
            s.append(str(bus.slavesV))
            s.append(str(bus))
            s.append("\n")

        if self.exported_interface is not None:
            if type(self.exported_interface) == str:
                s.append(f"\treturn {self.exported_interface};\n")
            else:
                for name,value in self.interface_members.items():
                    typeName = ""
                    if type(self.knownNames[value]) == Function:
                        typeName = "method"
                    elif type(self.knownNames[value]) == Type_ide:
                        typeName = "interface"
                    s.append(f"\t{typeName} {name} = {value};\n")

        s.append("\n")
        s.append("endmodule\n")
        s.append("endpackage\n")
        s = "".join(s)
        return s

    def toJSON(self):
        json_dict = {}
        json_dict["aditional folders"] = list(self.db.additionalLibraryFolders)
        json_dict["packages"] = self.necessaryPackages
        json_dict["name"] = self.name
        json_dict["package_name"] = self.package_name
        json_dict["typedefs"] = [{
            "name":name,
            "value":str(value)
            } for name,value in self.typedefs.items()]
        json_dict["modules"] = [module.toJSON() for module in self.modules.values()]
        json_dict["connections"] = [{
            "from": connection.module_args[0],
            "to": connection.module_args[1]
        } for connection in self.connections.values()]
        json_dict["buses"] = [bus.toJSON() for bus in self.buses.values()]
        if self.exported_interface is not None:
            if type(self.exported_interface) == str:
                json_dict["interface"] = self.exported_interface
            else:
                json_dict["interface"] = { 
                    "name": self.exported_interface.name,
                    "members": [{
                    "name": name,
                    "value": member
                } for name,member in self.interface_members.items()]}
        
        return json_dict

    def to_file(self,folder="."):
        with open(os.path.join(folder,self.package_name+".bsv"),'w') as f:
            f.write(self.__str__())

    def buildAndRun(self,folder="."):
        cwd = os.path.join(".",self.db.saveLocation,"..")
        print("CWD",cwd)
        self.to_file(cwd)
        additionalFoldersStr =".:"+ ":".join(self.db.additionalLibraryFolders) + ":+"
        buildFolder = "./bscBuild/"
        bscLocation = "bsc"
        cFiles ="Flute/libs/BlueStuff/BlueUtils/MemSim.c Flute/libs/BlueStuff/BlueUtils/SimUtils.c"
        buildString = f"{bscLocation} -p {additionalFoldersStr} -sim -bdir {buildFolder} -g {self.name} -u {self.package_name}.bsv"
        simulationString = f"{bscLocation} -p {additionalFoldersStr} -sim -simdir {buildFolder} -o {buildFolder}{self.name} -e {self.name} {buildFolder}{self.name}.ba {cFiles}"
        
        def runAndGrabOutput(string,timeout=15):
            Error = False
            try:
                process = subprocess.run([string],shell=True,cwd=cwd,capture_output = True,timeout=timeout)
                Error = process.returncode != 0
            except subprocess.SubprocessError as e:
                Error = True
                process = e
            stdout = (process.stdout if process.stdout is not None else b"")
            stderr = (process.stderr if process.stderr is not None else b"")
            processOuput = stdout+b"STDERR:\n"+stderr
            processOuput = str(processOuput, encoding='utf-8')
            return Error,processOuput
                
        toRun = [buildString,simulationString,os.path.join(buildFolder,self.name)]
        outputs = ["","",""]

        for i,string in enumerate(toRun):
            Error,processOuput = runAndGrabOutput(string)
            outputs[i] = processOuput
            if Error:
                print("Error with: " + string)
                print(processOuput)
                return outputs
        return outputs   

        
        

