#%%
from bsvSynthesizer import *
import json
from thefuzz import process
from typeDatabase import TypeDatabase as tdb
from handlerV2 import *
import argparse
import os

example_string = r"""{
    "aditional folders" : ["BlueStuff/build/bdir","tutorial"],
    "packages": ["FIFO","FIFOF","Connectable","AddressFlit","GetPut","AXI4_Types","AXI4_Interconnect","SourceSink","Routable"],
    "name" : "top",
    "package_name" : "fifoChain",
    "typedefs": [
        {
            "name" : "DATASIZE",
            "value" : 1
        },
        {
            "name" : "ADDRWIDTH",
            "value" : 4
        }
    ],
    "modules" : [
        {
            "name" : "ff1",
            "function": "FIFO.mkFIFO",
            "function_params": [],
            "interface_params": ["Bit#(8)"]
        },
        {
            "name" : "ff2",
            "function": "FIFO.mkFIFO",
            "function_params": [],
            "interface_params": ["Bit#(8)"]
        },
        {
            "name" : "bf3",
            "function": "FIFOF.mkFIFOF",
            "interface_params": ["AFlit#(DATASIZE, ADDRWIDTH)"]
        },
        {
            "name" : "bf4",
            "copy_from" : "bf3"
        }
    ],

    "connections": [
        {
            "from" : "ff1",
            "to" : "ff2"
        }
    ],
    
    "busses": [
        {
            "masters" : ["bf3"],
            "slaves" : ["bf4"],
            "route" : ["0-2"]
        }
    ]
}"""
example_json = json.loads(example_string)
# %%

def lookForKeyword(keyword,dictionary):
    if keyword in dictionary:
        return dictionary[keyword]
    else:
        clostestKeyword = process.extract(keyword,list(dictionary.keys()),limit=1)[0]
        if clostestKeyword[1] > 80:
            print(f"While parsing we found {clostestKeyword[2]} while looking for {keyword}, this is probably a typo")
        else:
            print(f"While parsing we exprected a keyword: {keyword}.")
        raise Exception(f"Keyword {keyword} not found")

def load_json(json_file):
    db = tdb()
    create_bluetcl()
    if "aditional folders" in json_file:  
        for folder in json_file["aditional folders"]:
            add_folder(folder)
        
    packages = lookForKeyword("packages",json_file)
    db.addPackages(packages)

    topLevel = TopLevelModule(lookForKeyword("name",json_file),db,package_name=lookForKeyword("package_name",json_file))

    if "typedefs" in json_file:
        for typedef in json_file["typedefs"]:
            topLevel.add_typedef(typedef["name"],typedef["value"])

    modules = lookForKeyword("modules",json_file)
    for module in modules:
        if "copy_from" in module:
            source = topLevel.modules[module["copy_from"]]
            topLevel.add_module(source.creator_func,lookForKeyword("name",module),source.interface_args,source.func_args)
        else:
            function_params = []
            if "function_params" in module:
                function_params = module["function_params"]
            instance_params = []
            if "interface_params" in module:
                interface_params = module["interface_params"]
            topLevel.add_module(db.getFunctionByName(lookForKeyword("function",module)),lookForKeyword("name",module),interface_params,function_params)

    if "connections" in json_file:
        for connection in json_file["connections"]:
            topLevel.add_connection(lookForKeyword("from",connection),lookForKeyword("to",connection))

    if "busses" in json_file:
        for bus in json_file["busses"]:
            masters = lookForKeyword("masters",bus)
            slaves = lookForKeyword("slaves",bus)
            route = lookForKeyword("route",bus)
            route = [x.split("-") for x in route]
            route = [(int(x[0]),int(x[1])) for x in route]
            topLevel.add_bus(masters,slaves,route)

    print(topLevel.to_string())
    topLevel.to_file(f"{lookForKeyword('package_name',json_file)}.bsv",args.output_folder)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert a json file to a bsv file')
    parser.add_argument('-json_file', type=str, help='The json file to convert')
    parser.add_argument('-of','--output_folder', type=str, help='The folder of output',default="/mnt/e/Mega/Documents/CS/TLoB/tutorial/")
    #print f as a example of how to use the json file
    parser.add_argument("-showExample",action="store_true",help="Prints the json file as a example of how to use the json file")
    args = parser.parse_args()
    if args.showExample:
        print(json.dumps(example_json,indent=4))
    else:
        #check if the json file was passed as argument
        if args.json_file == None:
            print("No json file passed as argument")
            parser.print_help()
            exit()
        with open(args.json_file) as json_file:
            load_json(json.load(json_file))
        