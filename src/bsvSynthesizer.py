import enum
import os
from re import S
from tempfile import TemporaryFile
name_counter = 0
def get_name():
    global name_counter
    name_counter += 1
    return "__temp_" + str(name_counter)

class ModuleInstance():
    def __init__(self,creator_func,interface_args=[],func_args=[],instance_name=None):
        self.creator_func = creator_func
        self.func_args = func_args
        self.interface = creator_func.interface
        self.interface.type_ide.fields = []

        if interface_args != "auto":
            for i,field in enumerate(creator_func.interface.fields):
                if field.name[0].isUpper():
                    self.interface.type_ide.fields += str(field)
                else:
                    self.interface.type_ide.fields += str(interface_args[i])
        if(len(func_args) != len(creator_func.arguments)):
            raise Exception("Function arguments do not match the function")
        self.instance_name = instance_name
        if instance_name is None:
            self.instance_name = creator_func.name[:-2]+get_name()



    def submodule(self,name):
        try:
            subModule = self.interface.members[name]
        except Exception as e:
            print(f"{name} not found in {self.interface.name}")
            raise e
        subModule.instance_name = self.instance_name + "." + name
        return AccessTuple(subModule.instance_name,subModule)
    
    def get(self):
        return AccessTuple(self.instance_name,self.interface)

class AccessTuple():
    def __init__(self,access_name,thing):
        self.access_name = access_name
        self.thing = thing

def type_string(interface):
    if interface.type_ide.fields!=0:
            arguments = ""
            for i in range(len(interface.type_ide.fields)):
                stringified = str(interface.type_ide.fields[i])
                arguments += stringified
                if i != len(interface.type_ide.fields)-1:
                    arguments += ", "
            
    return interface.name + f"#({arguments})"

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

    def add_module(self,creator_func,instance_name,interface_args=[],func_args=[]):
        #check if instance name starts with upercase character
        if instance_name[0].isupper():
            raise Exception("Instance name must start with lowercase character")
        self.modules[instance_name] = ModuleInstance(creator_func,interface_args,func_args,instance_name)
        return self.modules[instance_name]

    def add_typedef(self,name,type):
        self.typedefs[name] = type
        return name

    def add_connection(self,source,sink):
        if type(source) is str:
            source = AccessTuple(source,self.modules[source])
        if type(sink) is str:
            sink =  AccessTuple(sink,self.modules[sink])
        #check if connection is possible
        # this will simplify code
        inputs = [source.thing,sink.thing] 
        possible = False
        connectableTypeclass = self.db.getTypeclassByName("Connectable.Connectable")
        for instance in connectableTypeclass.instances:
            instanceFields = instance[0].fields
            variables = [{},{}]
            namesAreMatching = True
            # check name and package
            for i in range(len(instanceFields)):
                if type(instanceFields[i]) == str:
                    continue
                else:
                    if not instanceFields[i].full_name == str(inputs[i].type_ide):
                        namesAreMatching = False
                        break
            if not namesAreMatching:
                continue
            # # check if all fields are matching
            # for i in range(len(instanceFields)):
            #     if type(instanceFields[i]) == str:
            #         variables[i][instanceFields[i]] = inputs[i].interface_args[i]
            #     else:
            #         for j in range(len(instanceFields[i].fields)):
            #             variables[i][instanceFields[i].fields[j]] = inputs[i].interface_args[j]
            #compare sets of variables
            matching = True

            for i in variables[0]:
                if i not in variables[1]:
                    continue
                if variables[0][i] != variables[1][i]:
                    matching = False
                    break
            if matching:
                possible = True
                break

        if not possible: 
            print("No direct connection is possible falling back to GetPut")
            if not self.db.checkToXMembership(\
                source.interface,\
                self.db.getTypeclassByName("GetPut.ToPut")):
                raise Exception("Source is not a instace of ToPut")
            if not self.db.checkToXMembership(\
                sink.interface,\
                self.db.getTypeclassByName("GetPut.ToGet")):
                raise Exception("Sink is not a instace of ToGet")

            self.connections.add((source,sink,"GETPUT"))
        else:
            self.connections.add((source,sink,"Normal"))

    def add_onewaybus(self,ins,outs,insRanges):
        #check if ins have ToSource
        for i in ins:
            if not self.db.checkToXMembership(self.modules[i].interface,self.db.getTypeclassByName("SourceSink.ToSource")):
                raise Exception("Input is not a instance of ToSource") 
        #check if outs have ToSink
        for o in outs:
            if not self.db.checkToXMembership(self.modules[o].interface,self.db.getTypeclassByName("SourceSink.ToSink")):
                raise Exception("Output is not a instance of ToSink")
        self.buses.add(BusInstace(ins,outs,insRanges))

    def add_bus(self,ins,outs,insRanges,two_way=False):
        AcessIns = [AccessTuple(i,self.modules[i]) if type(i) is str else i for i in ins]
        AccessOuts = [AccessTuple(o,self.modules[o]) if type(o) is str else o for o in outs]
        
        ins = [i.thing for i in AcessIns]
        outs = [o.thing for o in AccessOuts]

        ins_type = ins[0]
        for i in ins:
            if i.full_name != ins_type.full_name:
                raise Exception("Inputs are not of the same type")
            if i.type_ide.fields != ins_type.type_ide.fields:
                raise Exception("Inputs have different interface arguments")
        outs_type = outs[0]
        for o in outs:
            if o.full_name != outs_type.full_name:
                raise Exception("Outputs are not of the same type")
            if o.type_ide.fields != outs_type.type_ide.fields:
                raise Exception("Outputs have different interface arguments")
        
        # check if AXI4
        is_AXI4 = True
        if ins_type.full_name != "AXI4_Types.AXI4_Master":
            is_AXI4 = False
        if outs_type.full_name != "AXI4_Types.AXI4_Slave":
            is_AXI4 = False
        
        self.packages.add("Vector")

        if not two_way:
            self.packages.add("OneWayBus")
            connection_type = ConnectionType.one_way
        if two_way:
            self.packages.add("TwoWayBus")
            connection_type = ConnectionType.two_way
        if is_AXI4:
            self.packages.add("AXI4_Interconnect")
            connection_type = ConnectionType.AXI4
            self.buses.add(BusInstace(AcessIns,AccessOuts,insRanges,connection_type))
            return
        
        # if not AXI4 check for typeclass membership
        for i in ins:
            if not self.db.checkToXMembership(i,self.db.getTypeclassByName("SourceSink.ToSource")):
                raise Exception("Input is not a instance of ToSource")
        for o in outs:
            if not self.db.checkToXMembership(o,self.db.getTypeclassByName("SourceSink.ToSink")):
                raise Exception("Output is not a instance of ToSink")

        self.buses.add(BusInstace(AcessIns,AccessOuts,insRanges,connection_type))
        

    def to_string(self):
        s = []
        s.append("package "+self.package_name + ";\n")
        self.packages.add("Connectable")
        self.packages.add("GetPut")
        for m in self.modules.values():
            self.packages.add(m.creator_func.package)
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
        
        s.append("module "+self.name+"();\n \n")
        
        # add modules
        for m in self.modules.values():
            s.append("\t")
            if m.interface.type_ide.fields == "auto":
                s.append("let") 
            else:             
                s.append(type_string(m.interface))
            s.append(" " + m.instance_name)
            s.append(" <- " + m.creator_func.name + "(")
            for i in range(len(m.func_args)):
                s.append(str(m.func_args[i]))
                if i != len(m.func_args)-1:
                    s.append(", ")
            s.append(");\n")
        s.append("\n")

        # add connections
        for c in self.connections:
            if c[2] == "GETPUT":
                s.append(f"\tmkConnection(toPut({c[0].access_name}),toGet({c[1].access_name}));\n")
            else:
                s.append(f"\tmkConnection({c[0].access_name},{c[1].access_name});\n")   

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

        s.append("\n")
        s.append("endmodule\n")
        s.append("endpackage\n")
        s = "".join(s)
        return s
    
    def to_file(self,folder="."):
        with open(os.path.join(folder,self.package_name+".bsv"),'w') as f:
            f.write(self.to_string())


        
