from copy import deepcopy
import enum
from math import ceil, log2
import os


from extractor import Type as ExType
from extractor import Interface as ExInterface
from extractor import Type_formal as ExType_formal
from extractor import Type_ide
from extractor import evaluateCustomStart
from typing import List, Set, Dict, Tuple, Optional, Union, Any
from typeDatabase import TypeDatabase
from bsvSynthesizer import AccessTuple,type_string,VectorInstance,InstanceV2


busCounter = 0

class BusV2():
    masters: VectorInstance
    slaves: VectorInstance
    name: str
    routes: Dict[str, List[Tuple[int,int]]]
    instance: InstanceV2

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

    def __init__(self, name: str, masters: VectorInstance, slaves: VectorInstance, routes: Dict[str, List[Tuple[int,int]]]):
        self.name = name
        self.masters = masters
        self.slaves = slaves
        self.routes = routes
        