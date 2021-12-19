import enum
import os
from re import S
name_counter = 0
def get_name():
    global name_counter
    name_counter += 1
    return "__temp_" + str(name_counter)

class ModuleInstance():
    def __init__(self,creator_func,interface_args=[],func_args=[],instance_name=None):
        self.creator_func = creator_func
        self.interface_args = interface_args
        self.func_args = func_args
        self.interface = creator_func.interface
        if(len(interface_args) != len(creator_func.interface.fields)):
            raise Exception("Interface arguments do not match the interface")
        if(len(func_args) != len(creator_func.arguments)):
            raise Exception("Function arguments do not match the function")
        self.instance_name = instance_name
        if instance_name is None:
            self.instance_name = creator_func.name[:-2]+get_name()

    def type_string(self):
        if self.creator_func.interface.fields!=0:
                arguments = ""
                for i in range(len(self.interface_args)):
                    stringified = str(self.interface_args[i])
                    arguments += stringified
                    if i != len(self.interface_args)-1:
                        arguments += ", "
                
        return "\t" + self.creator_func.interface.name + f"#({arguments})"

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
    
    def __init__(self,name,db) -> None:
        self.modules = {}
        self.connections = set()
        self.name = name
        self.db = db
        self.buses = set()
        self.packages = set()

    def add_module(self,creator_func,instance_name,interface_args=[],func_args=[]):
        self.modules[instance_name] = ModuleInstance(creator_func,interface_args,func_args,instance_name)
        return self.modules[instance_name]

    def add_connection(self,source,sink):
        if type(source) is str:
            source = self.modules[source]
        if type(sink) is str:
            sink = self.modules[sink]
        if not self.db.checkToXMembership(\
            source.interface,\
            self.db.getTypeclassByName("GetPut.ToPut")):
            raise Exception("Source is not a instace of ToPut")
        if not self.db.checkToXMembership(\
            sink.interface,\
            self.db.getTypeclassByName("GetPut.ToGet")):
            raise Exception("Sink is not a instace of ToGet")
        self.connections.add((source,sink))

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
        ins_type = ins[0]
        for i in ins:
            if i.interface.full_name != ins_type.interface.full_name:
                raise Exception("Inputs are not of the same type")
            if i.interface_args != ins_type.interface_args:
                raise Exception("Inputs have different interface arguments")
        outs_type = outs[0]
        for o in outs:
            if o.interface.full_name != outs_type.interface.full_name:
                raise Exception("Outputs are not of the same type")
            if o.interface_args != outs_type.interface_args:
                raise Exception("Outputs have different interface arguments")
        
        # check if AXI4
        is_AXI4 = True
        if ins_type.interface.full_name != "AXI4_Types.AXI4_Master":
            is_AXI4 = False
        if outs_type.interface.full_name != "AXI4_Types.AXI4_Slave":
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
            self.buses.add(BusInstace(ins,outs,insRanges,connection_type))
            return
        
        # if not AXI4 check for typeclass membership
        for i in ins:
            if not self.db.checkToXMembership(i.interface,self.db.getTypeclassByName("SourceSink.ToSource")):
                raise Exception("Input is not a instance of ToSource")
        for o in outs:
            if not self.db.checkToXMembership(o.interface,self.db.getTypeclassByName("SourceSink.ToSink")):
                raise Exception("Output is not a instance of ToSink")

        self.buses.add(BusInstace(ins,outs,insRanges,connection_type))
        

    def to_string(self):
        s = []
        s.append("package "+self.name + ";\n")
        self.packages.add("Connectable")
        self.packages.add("GetPut")
        for m in self.modules.values():
            self.packages.add(m.creator_func.package)
        for p in self.packages:
            s.append("import "+p+"::*;\n")
        s.append("\n")
        
        # add bus routing functions
        for bus in self.buses:
            # generate routing function
            r_s = len(bus.ins)
            s.append(f"function Vector #({r_s}, Bool) route{bus.name} (r_t x) provisos ( Bits#(r_t,{r_s}) );\n")
            s.append(f"\tBit#({r_s}) r_t_b = pack(x);\n")
            s.append(f"\tVector#({r_s}, Bool) r_t_v = replicate (False);\n")
            for i in range(len(bus.ins)):
                s.append(f"\tif (r_t_b >= {bus.insRanges[i][0]} && r_t_b <= {bus.insRanges[i][1]})\n")
                s.append(f"\t\tr_t_v[{i}] = True;\n")
            s.append(f"\treturn r_t_v;\n")
            s.append(f"endfunction\n\n")
        
        s.append("module mk"+self.name+"();\n \n")
        
        for m in self.modules.values():                
            s.append(m.type_string())
            s.append(" " + m.instance_name)
            s.append(" <- " + m.creator_func.name + "(")
            for i in range(len(m.func_args)):
                s.append(m.func_args[i])
                if i != len(m.func_args)-1:
                    s.append(", ")
            s.append(");\n")
        s.append("\n")

        for c in self.connections:
            s.append(f"\tmkConnection(toPut({c[0].instance_name}),toGet({c[1].instance_name}));\n")

        for bus in self.buses:
            s.append(f"\tVector#({len(bus.ins)}, {bus.ins[0].type_string()}) {bus.name}_ins;\n")
            for i in range(len(bus.ins)):
                s.append(f"\t{bus.name}_ins[{i}] = {bus.ins[i].instance_name};\n")
            
            s.append(f"\tVector#({len(bus.outs)}, {bus.outs[0].type_string()}) {bus.name}_outs;\n")
            for i in range(len(bus.outs)):
                s.append(f"\t{bus.name}_outs[{i}] = {bus.outs[i].instance_name};\n")
            
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
    
    def to_file(self,filename,folder="."):
        with open(os.path.join(folder,filename),'w') as f:
            f.write(self.to_string())


        
