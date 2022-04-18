from copy import deepcopy
import enum
import os
from re import S
from tempfile import TemporaryFile

from extractor import Position, Type as ExType, Type_ide, Value as ExValue
from extractor import Interface as ExInterface
from extractor import Type_formal as ExType_formal
from extractor import Function as ExFunction, Module as ExModule
from extractor import evaluateType,evaluateCustomStart
from extractor import Alias as ExAlias
from extractor import Typeclass as ExTypeclass
from extractor import Typeclass_instance as ExTypeclassInstance

from typing import Dict, List, Union,Set,Tuple

from typeDatabase import TypeDatabase


class AccessTuple():
    access_name: str

    def __init__(self,access_name: str,thing):
        self.access_name = access_name
        self.thing = thing
    
    def __repr__(self) -> str:
        return f"{self.access_name} {self.thing}"

class InstanceV2():
    pass

#region utility functions (should be wrapped into toplevel module class)
name_counter = 0
def get_name():
    global name_counter
    name_counter += 1
    return "_temp_" + str(name_counter)

instances:Dict[str,InstanceV2] = {}
knownNames:Dict[str,Type_ide] = {}
subscribers:Dict[str,Set[str]] = {}

def convertToTypeIde(db:TypeDatabase,arg,caller=None):
    if isinstance(arg,Type_ide) or type(arg) == ExFunction:
        return arg
    arg = str(arg)
    if arg[0].islower():
        if caller is not None:
            global subscribers
            if arg not in subscribers:
                subscribers[arg] = set()
            subscribers[arg].add(caller)
        if arg not in knownNames:
            raise Exception(f"Unknown name {arg}")
        return knownNames[arg]
    if arg[0].isupper():
        type_t = evaluateCustomStart(arg,"type_def_type")
        return db.evaluateTypedef(type_t)
    return evaluateCustomStart(arg,"type_def_type")

def addInstance(instance,name):
    global instances
    if name in subscribers:
        #remove stale subscriptions
        for channel in subscribers.values():
            if name in channel:
                channel.remove(name)
    instances[name] = instance

def addName(name,type_ide):
    global knownNames
    knownNames[name] = type_ide
    if name in subscribers:
        for subscriber in subscribers[name]:
            instances[subscriber].update()
#endregion

class InstanceV2():
    db: TypeDatabase
    type_ide : Type_ide
    creator: Union[ExFunction,ExModule]

    def __init__(self,db: TypeDatabase,creator: ExType,
                creator_args : List[Union[InstanceV2,Type_ide]] =[],
                module_args:List[Type_ide]=[],
                instance_name:str=None,
                input_context:Dict[str,str]={}):
        self.db = db
        self.creator = creator
        self.creator_args = creator_args
        self.instance_name = instance_name
        self.module_args = module_args
        self.input_context = {key:evaluateCustomStart(val) for key,val in input_context.items()}
        addInstance(self,instance_name)
        if creator_args is not None:
            self.update()


    def list_all_Interfaces(self)->List[AccessTuple]:
        MAX_DEPTH = 1
        def visitRecursively(parent_name: str, interface: Type_ide,depth:int=1):
            if depth > 1:
                return
            if len(interface.members) == 0:
                return
            for name,value in interface.members.items():
                if type(value) == Type_ide:
                    full_name = f"{parent_name}.{name}"
                    yield AccessTuple(full_name,value)
                    yield from visitRecursively(full_name,value,depth+1) 
        return [AccessTuple(self.instance_name,self.creator.type_ide)] + list(visitRecursively(self.instance_name,self.creator.type_ide))

    def update(self):
        print(f"Updating {self.instance_name}")
        self.creator.type_ide.accessName = self.instance_name
        
        if len(self.creator_args) != len(self.creator.arguments):
            print(f"{self.instance_name} has {len(self.creator_args)} arguments, but {self.creator.name} has {len(self.creator.arguments)}")
            raise Exception("Number of function arguments do not match the number of arguments required")
        #convert to TypeIde arguments
        creator_args = [convertToTypeIde(self.db,arg,self.instance_name) for arg in self.creator_args]
        module_args = [convertToTypeIde(self.db,arg,self.instance_name) for arg in self.module_args]

        context = deepcopy(self.input_context)
        for i,pair in  enumerate( zip(self.creator.arguments.items(),creator_args)):
            arg,value = pair
            if type(value) == ExFunction:
                continue
            if type(value) == InstanceV2:
                value = value.type_ide
            if isinstance(value, Type_ide):
                context |= self.db.merge(arg[1],value,{}) 
            #this is just to check if everything is ok
            self.db.applyVariables(deepcopy(self.creator.arguments[arg[0]]),context)

        ideCopy  = deepcopy(self.creator.type_ide)
        if len(module_args) == 0:
            module_args = ["a"+str(i) for i in range(len(ideCopy.formals))]
        for i,field in enumerate(ideCopy.formals):
            ideCopy.formals[i].type_ide = module_args[i]

        context |= self.db.merge(self.creator.type_ide,ideCopy,context)

        #account for provisos
        context |= self.db.solveProvisos(self.creator.provisos,context)
        
        self.creator.type_ide = self.db.applyVariables(self.creator.type_ide,context)
        self.db.populateMembers(self.creator.type_ide)
        global instances
        interfaces = self.list_all_Interfaces()
        for interface in interfaces:
            addName(interface.access_name,interface.thing)

    def get(self):
        return AccessTuple(self.instance_name,self.creator.type_ide)

    def to_string(self):
        if type(self.creator) == ExFunction:
            return f"{self.creator.name}({','.join(map(str,self.creator_args))});\n"

class VectorInstance():
    items: List[str]
    flit_type_ide:  Type_ide = evaluateCustomStart("flit","type_def_type")
    type_ide: Type_ide = evaluateCustomStart(f"Vector::Vector#(0,flit)","type_def_type")
    instance_name: str = None

    def __init__(self,db,name):
        self.items = []
        self.instance_name = name
        self.db = db
        addInstance(self,name)
        addName(name,self.type_ide)

    def remove(self,item:str):
        self.items.remove(item)
        if len(self.items) == 0:
            self.flit_type_ide = evaluateCustomStart("flit","type_def_type")
        self.type_ide = evaluateCustomStart(f"Vector::Vector#({len(self.items)},{self.flit_type_ide})","type_def_type")


    def add(self,item:str):
        itemType_ide = convertToTypeIde(self.db,item,self.instance_name)
        try:
            context = self.db.merge(self.flit_type_ide,itemType_ide,{})
        except Exception as e:
            raise Exception("Adding item to vector failed types don't match")
        if len(self.items) == 0:
            self.flit_type_ide = self.db.applyVariables(self.flit_type_ide,context)
        self.items.append(item)
        self.type_ide = evaluateCustomStart(f"Vector::Vector#({len(self.items)},{self.flit_type_ide})","type_def_type")

    def update(self,silent=False):
        items =[convertToTypeIde(self.db,item,self.instance_name) for item in self.items]
        try:
            for item in items:
                self.db.merge(self.flit_type_ide,item,{})
        except Exception as e:
            print("Failed updaitng vector")
            print(e)
            raise Exception("Adding item to vector failed types don't match")
        if not silent:
            addName(self.instance_name,self.type_ide)

    def listAddable(self,proposed)->List[AccessTuple]:
        for item in proposed:
            try:
                vars = self.db.merge(self.flit_type_ide,item,{})
            except Exception as e:
                continue
            yield AccessTuple(self.instance_name,item)
        

    def __str__(self):
        output_str = []
        output_str.append(f"\t{self.type_ide} {self.instance_name};\n")
        for i,item  in enumerate(self.items):
            output_str.append(f"\t{self.instance_name}[{i}] = {item};\n")
        return "".join(output_str)

class BusInstanceV3(InstanceV2):
    def __init__(self,db,name,busCreator:str,masters:List[str],slaves:List[Tuple[str,List[Tuple[int,int]]]]):
        self.instance_name = name
        self.db = db 
        self.creator = self.db.getFunctionByName(busCreator)
        addInstance(self,name)
        self.masters = masters
        self.slaves = slaves
        self.mastersV = VectorInstance(self.db,name+"_masters")
        self.slavesV = VectorInstance(self.db,name+"_slaves")
        for master in self.masters:
            self.mastersV.add(master)
        self.mastersV.update(silent=False)
        #addName(self.instance_name,self.type_ide)
        for slave in self.slaves:
            self.slavesV.add(slave[0])
        self.slavesV.update(silent=False)
        #addName(self.instance_name,self.type_ide)
        self.creator_args = [f"route_{self.instance_name}",self.mastersV.type_ide,self.slavesV.type_ide]
        self.module_args = []
        self.input_context = {}
        self.update()


    def update(self):    
        # convertToTypeIde(self.mastersV.instance_name,self.instance_name)
        # convertToTypeIde(self.slavesV.instance_name,self.instance_name)

        functionString = \
        """
        {function route_{busName} {result Vector#({NSlaves}, Bool)
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
        output_str.append(f"\tBit#(r_l) adress = pack(x);\n")
        output_str.append(f"\tVector#({r_s}, Bool) oneHotAdress = replicate (False);\n")
        
        for name, route in self.slaves:
            slave_id = slave_to_id[name]
            output_str.append(f"\t// {name} -> {slave_id}\n")
            for start, end in route:
                output_str.append(f"\tif (adress >= {start} && adress < {end})\n")
                output_str.append(f"\t\toneHotAdress[{slave_id}] = True;\n")
        output_str.append(f"\treturn oneHotAdress;\n")
        output_str.append(f"endfunction\n\n")
        return "".join(output_str)

    def __str__(self):
        return f"\t{self.creator.full_name}(route_{self.instance_name},{self.mastersV.instance_name},{self.slavesV.instance_name});\n"

class TopLevelModule():
    db: TypeDatabase
    possibleConnections: Dict[str,AccessTuple] = {}
    accessableInterfaces: List[AccessTuple] = []
    cashed_considered_instances: Dict[str,AccessTuple] = {}

    modules: Dict[str,InstanceV2] = {}
    connections: Dict[str,InstanceV2] = {}
    buses: Dict[str,BusInstanceV3] = {}
    name: str
    package_name: str
    typedefs: Dict[str,ExAlias] = {}


    def __init__(self,name,db,package_name=None) -> None:
        self.name = name
        if package_name is None:
            self.package_name = name
        else:
            self.package_name = package_name
        self.db = db
        self.packages = set()

    def add_moduleV2(self,creator_func,instance_name,interface_args=[],func_args=[],input_context={}) -> InstanceV2:
        #check if instance name starts with upercase character
        if instance_name[0].isupper():
            raise Exception("Instance name must start with lowercase character")
        if type(creator_func) == str:
            creator_func = self.db.getFunctionByName(creator_func)
        #try:
        newModule = InstanceV2(self.db,creator_func,func_args,interface_args,instance_name,input_context)
        # except Exception as e:
        #     raise Exception(f"""Error creating module {instance_name}: {e}
        #         Arguments:
        #             creator function: {creator_func}
        #             function arguments: {func_args}
        #             interface arguments: {interface_args}
        #             instance name: {instance_name}
        #     """)
        
        #populate possible connections
        for current in newModule.list_all_Interfaces():
            self.possibleConnections[current.access_name] = self.list_connectableV2(current,self.accessableInterfaces)
            for interface in self.accessableInterfaces:
                self.possibleConnections[interface.access_name] += self.list_connectableV2(interface,[current])

        self.accessableInterfaces += newModule.list_all_Interfaces()

        self.modules[instance_name] = newModule
        return self.modules[instance_name]

    def add_typedef(self,name,type):
        self.typedefs[name] = type
        alias = ExAlias(Type_ide(name),evaluateCustomStart(str(type)),None)
        self.db.aliases[alias.full_name] = alias
        return name

    def list_connectableV2(self,start:AccessTuple,ends:List[AccessTuple]=[]):
        if len(ends) == 0:
            return []

        connectableTypeclass : ExTypeclass = self.db.getTypeclassByName("Connectable::Connectable")
        #ends = []
        connectable_ends : List[AccessTuple]  = []
        
        #inital triming of connectable rules
        #it cashes results, allowing for this function to be roughly O(len(ends))
        if start.access_name in self.cashed_considered_instances:
            considered_instances = self.cashed_considered_instances[start.access_name]
        else:   
            considered_instances : List[ExTypeclassInstance] = []
            for instance in connectableTypeclass.instances:
                instanceFields = instance.inputs
                #check if both Fields are types
                if type(instanceFields[0].type_ide) == Type_ide and type(instanceFields[1].type_ide) == Type_ide:
                    #check if name matches start point
                    if instanceFields[0].type_ide.full_name == start.thing.full_name:
                        considered_instances.append(instance)
            self.cashed_considered_instances[start.access_name] = considered_instances
        
        connectable_instances : Dict[str,ExTypeclassInstance] = {}
        #check if end is a connectable
        for end in ends:
            for instance in considered_instances:
                instanceFields = instance.inputs
                #check if both Fields are types
                if instanceFields[1].type_ide.full_name != end.thing.full_name:
                    continue
                variables = {}
                def add_variable(name,value):
                    if name in variables:
                        old = variables[name]
                        try:
                            self.db.merge(old,value,{})
                        except Exception as e:
                            raise Exception(f"Variable {name} has different values")
                    else:
                        variables[name] = value

                #check if values that can be polymorphic are the same
                variableMissmatch = False
                for i,field in enumerate(instanceFields[0].type_ide.children):
                    try:
                        add_variable(str(field),start.thing.children[i])
                    except Exception as e:
                        variableMissmatch = True
                        break
                for i,field in enumerate(instanceFields[1].type_ide.children):
                    try:
                        add_variable(str(field),end.thing.children[i])
                    except Exception as e:
                        variableMissmatch = True
                        break
                if variableMissmatch:
                    continue

                connectable_instances[end.access_name] = instance
                break
        for end in ends:
            if end.access_name not in connectable_instances:
                continue
            result = None
            try:
                connection = deepcopy(connectableTypeclass.type_ide)
                connection.formals[0].type_ide = start.thing
                connection.formals[1].type_ide = end.thing
                result = self.db.resolveTypeclass(connectableTypeclass, connection,connectable_instances[end.access_name])
            except Exception as e:
                continue
            if result is not None:
                connectable_ends.append(end)
        return connectable_ends

    def add_connectionV2(self,start:str,end:str,connection_name:str=None):
        if connection_name is None:
            connection_name = f"connection_{len(self.connections)}"
        creator_func = self.db.getFunctionByName("mkConnection")
        connection = InstanceV2(self.db,creator_func,[start,end],[],connection_name)
        self.connections[connection_name] = connection

    def add_busV3(self,name,busCreator:str,masters:List[str],slaves:List[Tuple[str,List[Tuple[int,int]]]]):
        bI = BusInstanceV3(self.db,name,busCreator,masters,slaves)
        self.buses[name] = bI

    def remove(self,name:str):
        #in accessable interfaces find name* use start with and fiter
        self.accessableInterfaces.filter(lambda x: not x.access_name.startswith(name))

        global instances
        if name in instances:
            instances.remove(name)
        global knownNames
        knownNames = {k:v for k,v in knownNames.items() if not k.startswith(name)}
        global subscribers
        for subscriber in subscribers:
            if name in subscriber:
                subscriber.remove(name)
        
        if name in self.modules:
            del self.modules[name]
        if name in self.connections:
            del self.connections[name]
        if name in self.buses:
            del self.buses[name]
        if name in self.typedefs:
            del self.typedefs[name]

    def to_string(self):
        s = []
        s.append("package "+self.package_name + ";\n")
        self.packages.add("Connectable")
        self.packages.add("GetPut")
        for m in self.modules.values():
            if m.creator.package is not None:
                self.packages.add(m.creator.package)
        for b in self.buses.values():
            if b.creator.package is not None:
                self.packages.add(b.creator.package)
        # necessary packages
        s.append("// necessary packages\n")
        for p in self.packages:
            s.append("import "+p+"::*;\n")
        # imported packages
        s.append("// imported packages\n")
        for p in self.db.packages:
            #check if package is already imported
            if p not in self.packages:
                s.append("import "+p+"::*;\n")
        s.append("\n")
        
        # typedefs example. typedef 1 DATASIZE;
        for t in self.typedefs.keys():
            s.append("typedef " + str(self.typedefs[t]) + " " + str(t) + ";\n")
        s.append("\n")

        for bus in self.buses.values():
            s.append(bus.routingFunctionString())

        s.append("module "+self.name+"();\n \n")
        
        # add modules
        for m in self.modules.values():
            if m.creator_args is None:
                s.append("Awiaiting for args for ")
                continue
            s.append("\t")
        
            s.append(str(m.creator.type_ide))
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

        for bus in self.buses.values():
            s.append(str(bus))

        s.append("\n")
        s.append("endmodule\n")
        s.append("endpackage\n")
        s = "".join(s)
        return s
    
    def to_file(self,folder="."):
        with open(os.path.join(folder,self.package_name+".bsv"),'w') as f:
            f.write(self.to_string())


        
