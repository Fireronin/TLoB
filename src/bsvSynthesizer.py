from copy import deepcopy
import enum
import os
from re import S
from tempfile import TemporaryFile

from extractor import Position, Type as ExType, Type_ide, Value as ExValue
from extractor import Interface as ExInterface
from extractor import Type_formal as ExType_formal
from extractor import Function as ExFunction
from extractor import evaluateType,evaluateCustomStart
from extractor import Alias as ExAlias
from extractor import Typeclass as ExTypeclass
from extractor import Typeclass_instance as ExTypeclassInstance

from typing import Dict, List, Union

from typeDatabase import TypeDatabase



name_counter = 0
def get_name():
    global name_counter
    name_counter += 1
    return "_temp_" + str(name_counter)

class AccessTuple():
    access_name: str

    def __init__(self,access_name: str,thing):
        self.access_name = access_name
        self.thing = thing
    
    def __repr__(self) -> str:
        return f"{self.access_name} {self.thing}"

class InstanceV2():
    pass

instances = {}

def convertToTypeIde(arg):
    if type(arg) == Type_ide:
        return arg
    arg = str(arg)
    if arg[0].islower():
        return instances[arg]
    return evaluateCustomStart(arg,"type_def_type")

class InstanceV2():
    db: TypeDatabase
    type_ide : Type_ide

    def __init__(self,db: TypeDatabase,creator: ExType,
                creator_args : List[Union[InstanceV2,Type_ide]] =[],
                module_args:List[Type_ide]=[],
                instance_name:str=None):
        self.db = db
        self.creator = creator
        self.creator_args = creator_args
        self.instance_name = instance_name
        self.module_args = module_args
        self.update()
        global instances
        interfaces = self.list_all_Interfaces()
        for interface in interfaces:
            instances[interface.access_name] = interface.thing

    def list_all_Interfaces(self):
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
        if len(self.creator_args) != len(self.creator.arguments):
            raise Exception("Number of function arguments do not match the function")
        #convert to TypeIde arguments
        creator_args = [convertToTypeIde(arg) for arg in self.creator_args]
        module_args = [convertToTypeIde(arg) for arg in self.module_args]



        context = {}
        for i,pair in  enumerate( zip(self.creator.arguments.items(),creator_args)):
            arg,value = pair
            if type(value) == InstanceV2:
                value = value.type_ide
            if isinstance(value, Type_ide):
                context |= self.db.mergeV2(arg[1],value,context) 

            self.creator.arguments[arg[0]] = self.db.applyVariables(self.creator.arguments[arg[0]],context)

        ideCopy  = deepcopy(self.creator.type_ide)
        if len(module_args) == 0:
            module_args = ["a"+str(i) for i in range(len(ideCopy.formals))]
        for i,field in enumerate(ideCopy.formals):
            ideCopy.formals[i].type_ide = module_args[i]

        context |= self.db.mergeV2(self.creator.type_ide,ideCopy,context)

        #account for provisos
        context |= self.db.solveProvisos(self.creator.provisos,context)
        
        self.creator.type_ide = self.db.applyVariables(self.creator.type_ide,context)
        self.db.populateMembers(self.creator.type_ide)
        print('Works')

    def get(self):
        return AccessTuple(self.instance_name,self.creator.type_ide)

    def to_string(self):
        if type(self.creator) == ExFunction:
            return f"{self.creator.name}({','.join(map(str,self.creator_args))});\n"

def type_string(interface):
    if interface.type_ide.fields!=0:
            arguments = ""
            for i in range(len(interface.type_ide.fields)):
                stringified = str(interface.type_ide.fields[i])
                arguments += stringified
                if i != len(interface.type_ide.fields)-1:
                    arguments += ", "
            
    return interface.name + f"#({arguments})"

from busSynthesizer import OneWayBusV2, BusV2,AXI4BusV2

# enum with one way and two way and AXI4
class ConnectionType(enum.Enum):
    one_way = 1
    two_way = 2
    AXI4 = 3

class BusInstace():
    
    def __init__(self,ins,outs,insRanges,connectionType):
        self.ins = ins
        self.outs = outs
        self.insRanges = insRanges
        self.name = get_name()
        self.connectionType = connectionType

class TopLevelModule():
    db: TypeDatabase
    possibleConnections: Dict[str,AccessTuple] = {}
    accessableInterfaces: List[AccessTuple] = []
    cashed_considered_instances: Dict[str,AccessTuple] = {}

    modules: Dict[str,InstanceV2]

    def __init__(self,name,db,package_name=None) -> None:
        self.modules = {}
        self.connections = set()
        self.name = name
        if package_name is None:
            self.package_name = name
        else:
            self.package_name = package_name
        self.db = db
        self.buses = set()
        self.packages = set()
        self.typedefs = {}
        self.busesV2 = set()

    def add_moduleV2(self,creator_func,instance_name,interface_args=[],func_args=[]):
        #check if instance name starts with upercase character
        if instance_name[0].isupper():
            raise Exception("Instance name must start with lowercase character")
        if type(creator_func) == str:
            creator_func = self.db.getFunctionByName(creator_func)
        newModule = InstanceV2(self.db,creator_func,func_args,interface_args,instance_name)
        


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
        alias = ExAlias(Type_ide(name),evaluateType(str(type)),None)
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
                            self.db.mergeV2(old,value,{})
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
                result = self.db.solveTypeclass(connectableTypeclass, connection,connectable_instances[end.access_name])
            except Exception as e:
                continue
            if result is not None:
                  connectable_ends.append(end)
        return connectable_ends

    def add_connectionV2(self,start:str,end:str):
        creator_func = self.db.getFunctionByName("mkConnection")
        connection = InstanceV2(self.db,creator_func,[start,end],[],f"connection_{len(self.connections)}")
        self.connections.add(connection)

    def add_busV2(self,busType:ConnectionType ,name=None) -> BusV2:
        if busType == ConnectionType.one_way:
            bus = OneWayBusV2(self.db,name)
        elif busType == ConnectionType.two_way:
            raise Exception("Two way buses are not supported yet")
        elif busType == ConnectionType.AXI4:
            bus = AXI4BusV2(self.db,name)
        self.busesV2.add(bus)
        return bus

    def to_string(self):
        s = []
        s.append("package "+self.package_name + ";\n")
        self.packages.add("Connectable")
        self.packages.add("GetPut")
        for m in self.modules.values():
            self.packages.add(m.creator.package)
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

        # add bus routing functions
        for bus in self.buses:
            # generate routing function
            r_s = len(bus.outs)
            s.append(f"function Vector #({r_s}, Bool) route{bus.name} (r_t x) provisos ( Bits#(r_t,r_l) );\n")
            s.append(f"\tBit#(r_l) r_t_b = pack(x);\n")
            s.append(f"\tVector#({r_s}, Bool) r_t_v = replicate (False);\n")
            for i in range(len(bus.ins)):
                s.append(f"\tif (r_t_b >= {bus.insRanges[i][0]} && r_t_b <= {bus.insRanges[i][1]})\n")
                s.append(f"\t\tr_t_v[{i}] = True;\n")
            s.append(f"\treturn r_t_v;\n")
            s.append(f"endfunction\n\n")
        

        # add busesV2
        for bus in self.busesV2:
            s.append(bus.make_routing_function())

        s.append("module "+self.name+"();\n \n")
        
        # add modules
        for m in self.modules.values():
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
        for c in self.connections:
            s.append("\t"+c.to_string())

        # add busses
        for bus in self.buses:
            s.append(f"\tVector#({len(bus.ins)}, {type_string(bus.ins[0].thing)}) {bus.name}_ins;\n")
            for i in range(len(bus.ins)):
                s.append(f"\t{bus.name}_ins[{i}] = {bus.ins[i].access_name};\n")
            
            s.append(f"\tVector#({len(bus.outs)}, {type_string(bus.outs[0].thing)}) {bus.name}_outs;\n")
            for i in range(len(bus.outs)):
                s.append(f"\t{bus.name}_outs[{i}] = {bus.outs[i].access_name};\n")
            
            # depending on connection type generate bus
            if bus.connectionType == ConnectionType.one_way:
                s.append(f"\tmkOneWayBus(route{bus.name},{bus.name}_ins,{bus.name}_outs);\n")
            elif bus.connectionType == ConnectionType.two_way:
                s.append(f"\tmkTwoWayBus(route{bus.name},{bus.name}_ins,{bus.name}_outs);\n")
            elif bus.connectionType == ConnectionType.AXI4:
                s.append(f"\tmkAXI4Bus(route{bus.name},{bus.name}_ins,{bus.name}_outs);\n")

        # add bussesV2
        for bus in self.busesV2:
            s.append(bus.make_initialization_string())

        s.append("\n")
        s.append("endmodule\n")
        s.append("endpackage\n")
        s = "".join(s)
        return s
    
    def to_file(self,folder="."):
        with open(os.path.join(folder,self.package_name+".bsv"),'w') as f:
            f.write(self.to_string())


        
