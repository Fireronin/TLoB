from copy import deepcopy
import enum
from math import ceil, log2
import os


from extractor import Type as ExType
from extractor import Interface as ExInterface
from extractor import Type_formal as ExType_formal
from extractor import Type_ide

from typing import List, Set, Dict, Tuple, Optional, Union, Any
from typeDatabase import TypeDatabase
from bsvSynthesizer import AccessTuple,type_string


busCounter = 0

class BusV2():
    masters: Dict[str, Type_ide]
    slaves: Dict[str, Type_ide]
    name: str
    routes: Dict[str, List[Tuple[int,int]]]

    def make_routing_function(self) -> str:
        """
        Generate a function that routes a flit from a master to a slave.
        """
        #check if there is at least one master and one slave
        if len(self.masters) == 0 or len(self.slaves) == 0:
            raise Exception(f"Bus {self.name} has no masters or slaves. Slaves: {len(self.slaves)} Masters: {len(self.masters)}")

        output_str = []
        # generate routing function
        r_s = len(self.slaves)

        # create map from slave to id
        slave_to_id = {}
        for i, slave in enumerate(self.slaves.keys()):
            slave_to_id[slave] = i

        output_str.append(f"function Vector #({r_s}, Bool) route_{self.name} (r_t x) provisos ( Bits#(r_t,r_l) );\n")
        output_str.append(f"\tBit#(r_l) adress = pack(x);\n")
        output_str.append(f"\tVector#({r_s}, Bool) oneHotAdress = replicate (False);\n")
        
        for name, route in self.routes.items():
            slave_id = slave_to_id[name]
            output_str.append(f"\t// {name} -> {slave_id}\n")
            for start, end in route:
                output_str.append(f"\tif (adress >= {start} && adress < {end})\n")
                output_str.append(f"\t\toneHotAdress[{slave_id}] = True;\n")
        output_str.append(f"\treturn oneHotAdress;\n")
        output_str.append(f"endfunction\n\n")
        return "".join(output_str)

    #region function prototypes
    def add_slave(self,slave: AccessTuple,route: List[Tuple[int,int]]):
        raise Exception("Not implemented, please use specific subclass")

    def add_master(self,master: AccessTuple,route: List[Tuple[int,int]]):
        raise Exception("Not implemented, please use specific subclass")

    def __init__(self,name: str):
        raise Exception("Not implemented, please use specific subclass")
    
    def __str__(self):
        return f"Bus {self.name}"
    
    def __repr__(self):
        return self.__str__()

    def remove_slave(self,slave: AccessTuple):
        raise Exception("Not implemented, please use specific subclass")

    def remove_master(self,master: AccessTuple):
        raise Exception("Not implemented, please use specific subclass")

    def filter_valid_slaves(self,slaves: List[AccessTuple]) -> List[AccessTuple]:
        raise Exception("Not implemented, please use specific subclass")
    
    def filter_valid_masters(self,masters: List[AccessTuple]) -> List[AccessTuple]:
        raise Exception("Not implemented, please use specific subclass")

    def make_initialization_string(self) -> str:
        raise Exception("Not implemented, please use specific subclass")
    #endregion
          
class OneWayBusV2(BusV2):
    flit_t: ExType

    def __init__(self,db: TypeDatabase,name: str = None):
        self.masters = {}
        self.slaves = {}
        self.routes = {}
        self.flit_t = None
        self.db = db
        if name is not None:
            self.name = name
        else:
            global busCounter
            busCounter += 1
            self.name = "bus"+str(busCounter)

    def __repr__(self) -> str:
        return f"OneWayBusV2({self.name}) Flit:{self.flit_t} Connections: {','.join(self.slaves.keys())} -> {','.join(self.masters.keys())}"

    def add_slave(self,slave: AccessTuple,route: List[Tuple[int,int]]):
        slave.thing

        flit_t = self.db.toXResultingType(slave.thing,self.db.getTypeclassByName("SourceSink::ToSource"))
        if self.flit_t is None:
            self.flit_t = flit_t
        else:
            if self.flit_t != flit_t:
                raise Exception("BusV2:add_slave: flit_t is not the same")
        self.slaves[slave.access_name] = slave.thing
        # TODO: check if route is valid
        self.routes[slave.access_name] = route

    def add_master(self,master: AccessTuple):
        flit_t = self.db.toXResultingType(master.thing,self.db.getTypeclassByName("SourceSink::ToSink"))
        if self.flit_t is None:
            self.flit_t = flit_t
        else:
            if self.flit_t != flit_t:
                raise Exception("BusV2:add_master: flit_t is not the same")
        self.masters[master.access_name] = master.thing

    def reset_if_empty(self):
        if len(self.masters) == 0 and len(self.slaves) == 0:
            self.flit_t = None

    def remove_slave(self,slave: AccessTuple):
        self.slaves.pop(slave.access_name)
        self.routes.pop(slave.access_name)
        self.reset_if_empty()

    def remove_master(self,master: AccessTuple):
        self.masters.pop(master.access_name)
        self.reset_if_empty()

    def filter_valid_slaves(self,slaves: List[AccessTuple]) -> List[AccessTuple]:
        valid_slaves = []

        for slave in slaves:
            try:
                flit_t = self.db.toXResultingType(slave.thing,self.db.getTypeclassByName("SourceSink::ToSource"))
            except:
                pass

            if self.flit_t is None:
                    valid_slaves.append(slave)
            else:
                if self.flit_t == flit_t:
                    valid_slaves.append(slave)

        return valid_slaves

    def filter_valid_masters(self,masters: List[AccessTuple]) -> List[AccessTuple]:
        valid_masters = []
        
        for master in masters:
            try:
                flit_t = self.db.toXResultingType(master.thing,self.db.getTypeclassByName("SourceSink::ToSink"))
            except:
                pass

            if self.flit_t is None:
                valid_masters.append(master)
            else:
                if self.flit_t == flit_t:
                    valid_masters.append(master)
        
        return valid_masters
    
    def make_initialization_string(self) -> str:
        output_str = []
        output_str.append(f"\tVector#({len(self.masters)}, {type_string(next(iter(self.masters.values())))}) {self.name}_masters;\n")
        for i,master  in enumerate(self.masters.keys()):
            output_str.append(f"\t{self.name}_masters[{i}] = {master};\n")
            
        output_str.append(f"\tVector#({len(self.slaves)}, {type_string(next(iter(self.slaves.values())))}) {self.name}_slaves;\n")
        for i,slave  in enumerate(self.slaves.keys()):
            output_str.append(f"\t{self.name}_slaves[{i}] = {slave};\n")
            
        output_str.append(f"\tmkOneWayBus(route_{self.name},{self.name}_masters,{self.name}_slaves);\n")
        return "".join(output_str)

class AXI4BusV2(BusV2):
    SHARED_PARAMS = ["addr_", "data_", "awuser_", "wuser_", "buser_", "aruser_", "ruser_"]
    SLAVES_ID = int
    MASTERS_ID = int
    AXI4_params: Dict[str, str]

    def __init__(self,db: TypeDatabase,name: str = None):
        self.masters = {}
        self.slaves = {}
        self.routes = {}
        self.SLAVES_ID = None
        self.MASTERS_ID = None
        self.db = db
        self.AXI4_params = None
        if name is not None:
            self.name = name
        else:
            global busCounter
            busCounter += 1
            self.name = "bus"+str(busCounter)

    def __repr__(self) -> str:
        return f"AXI4BusV2({self.name}) Connections: {','.join(self.slaves.keys())} -> {','.join(self.masters.keys())}"

    def filter_valid_slaves(self,slaves: List[AccessTuple]) -> List[AccessTuple]:
        valid_slaves = []
        
        for slave in slaves:
            if slave.thing.full_name != "AXI4_Types::AXI4_Slave":
                continue
            if self.AXI4_params is None:
                valid_slaves.append(slave)
            else:
                parametersMatching = True
                for param in self.SHARED_PARAMS:
                    if str(slave.thing.type_ide[param]) != str(self.AXI4_params[param]):
                        parametersMatching = False
                if self.SLAVES_ID is not None:    
                    parametersMatching &= self.SLAVES_ID == int(slave.thing.type_ide["id_"])
                if parametersMatching:
                    valid_slaves.append(slave)
        
        return valid_slaves

    def filter_valid_masters(self,masters: List[AccessTuple]) -> List[AccessTuple]:
        valid_masters = []
        
        for master in masters:
            if master.thing.full_name != "AXI4_Types::AXI4_Master":
                continue
            if self.AXI4_params is None:
                valid_masters.append(master)
            else:
                parametersMatching = True
                for param in self.SHARED_PARAMS:
                    if str(master.thing.type_ide[param]) != str(self.AXI4_params[param]):
                        parametersMatching = False
                if self.MASTERS_ID is not None:
                    parametersMatching &= self.MASTERS_ID == int(master.thing.type_ide["id_"])
                if parametersMatching:
                    valid_masters.append(master)
        
        return valid_masters

    def add_slave(self,slave: AccessTuple,route: List[Tuple[int,int]]):
        if self.AXI4_params is None:
            self.AXI4_params = {}
            for param in self.SHARED_PARAMS:
                self.AXI4_params[param] = str(slave.thing.type_ide[param])
            
            self.SLAVES_ID = int(slave.thing.type_ide["id_"])
        else:
            for param in self.SHARED_PARAMS:
                if str(slave.thing.type_ide[param]) != str(self.AXI4_params[param]):
                    raise Exception("AXI4BusV2:add_slave: parameters don't match"+f"{self.AXI4_params} != {slave.thing.type_ide.fields}")
            
            if self.SLAVES_ID is None:
                self.SLAVES_ID = int(slave.thing.type_ide["id_"])
            else:
                if self.SLAVES_ID != int(slave.thing.type_ide["id_"]):
                    raise Exception("AXI4BusV2:add_slave: parameters don't match")
        
        self.slaves[slave.access_name] = slave.thing
        self.routes[slave.access_name] = route
    
    def add_master(self,master: AccessTuple):
        if self.AXI4_params is None:
            self.AXI4_params = {}
            for param in self.SHARED_PARAMS:
                self.AXI4_params[param] = str(master.thing.type_ide[param])
            
            self.MASTERS_ID = int(master.thing.type_ide["id_"])
        else:
            for param in self.SHARED_PARAMS:
                if str(master.thing.type_ide[param]) != str(self.AXI4_params[param]):
                    raise Exception("AXI4BusV2:add_master: parameters don't match"+f"{self.AXI4_params} != {master.thing.type_ide.fields}")
            
            if self.MASTERS_ID is None:
                self.MASTERS_ID = int(master.thing.type_ide["id_"])
            else:
                if self.MASTERS_ID != int(master.thing.type_ide["id_"]):
                    raise Exception("AXI4BusV2:add_master: parameters don't match")
        
        self.masters[master.access_name] = master.thing

    def reset_if_empty(self):
        if len(self.masters) == 0 and len(self.slaves) == 0:
            self.AXI4_params = None
        if len(self.masters) == 0:
            self.MASTERS_ID = None
        if len(self.slaves) == 0:
            self.SLAVES_ID = None

    def remove_slave(self,slave: AccessTuple):
        if slave.access_name in self.slaves:
            del self.slaves[slave.access_name]
            del self.routes[slave.access_name]
        self.reset_if_empty()

    def remove_master(self,master: AccessTuple):
        if master.access_name in self.masters:
            del self.masters[master.access_name]
        self.reset_if_empty()
    
    def make_initialization_string(self) -> str:
        if self.MASTERS_ID + int(ceil(log2(len(self.masters)))) != self.SLAVES_ID:
            raise Exception("""AXI4BusV2:make_initialization_string: masters and slaves ids don't match,
                it's required that MASTERS_ID + celi(log2(nMasters)) = SLAVES_ID""")

        output_str = []
        output_str.append(f"\tVector#({len(self.masters)}, {type_string(next(iter(self.masters.values())))}) {self.name}_masters;\n")
        for i,master  in enumerate(self.masters.keys()):
            output_str.append(f"\t{self.name}_masters[{i}] = {master};\n")
            
        output_str.append(f"\tVector#({len(self.slaves)}, {type_string(next(iter(self.slaves.values())))}) {self.name}_slaves;\n")
        for i,slave  in enumerate(self.slaves.keys()):
            output_str.append(f"\t{self.name}_slaves[{i}] = {slave};\n")
            
        output_str.append(f"\tmkAXI4Bus(route_{self.name},{self.name}_masters,{self.name}_slaves);\n")
        return "".join(output_str)


        




