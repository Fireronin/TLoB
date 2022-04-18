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
            "function": "mkFIFO",
            "function_params": [],
            "interface_params": ["Bit#(8)"]
        },
        {
            "name" : "ff1get",
            "function": "get",
            "function_params": ["ff1"]
        },
        {
            "name" : "ff2",
            "function": "mkFIFO",
            "function_params": [],
            "interface_params": ["Bit#(8)"]
        },
        {
            "name" : "ff2put",
            "function": "put",
            "function_params": ["ff2"]
        },
        {
            "name" : "core",
            "function": "mkCore"
        },
        {
            "name" : "memory",
            "function": "mkAXI4SimpleMem",
            "function_params": [4096,"Maybe#('xddd')"],
            "interface_params": [6, 64, 64, 0, 0, 0, 0, 0]
        }
    ],

    "connections": [
        {
            "from" : "ff1get",
            "to" : "ff2put"
        }
    ],
    
    "busses": [
        {
            "name" : "mainBus",
            "function": "mkAXI4Bus",
            "masters" : ["core.core_mem_master"],
            "slaves" : [{
                "name" : "memory",
                "routes" : [[0,4096],[5096,6400]]
            }]
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

def load_json(json_file,reload=False):
    db = tdb(load=reload)
    
    if "aditional folders" in json_file:  
        for folder in json_file["aditional folders"]:
            db.addLibraryFolder(folder)
    
    packages = lookForKeyword("packages",json_file)
    db.addPackages(packages)
    db.loadDependencies()

    topLevel = TopLevelModule(lookForKeyword("name",json_file),db,package_name=lookForKeyword("package_name",json_file))

    if "typedefs" in json_file:
        for typedef in json_file["typedefs"]:
            topLevel.add_typedef(typedef["name"],typedef["value"])

    modules = lookForKeyword("modules",json_file)
    for module in modules:
        # if "copy_from" in module:
        #     source = topLevel.modules[module["copy_from"]]
        #     topLevel.add_module(source.creator_func,lookForKeyword("name",module),source.interface_args,source.func_args)
        function_params = []
        if "function_params" in module:
            function_params = module["function_params"]
            for i in range(len(function_params)):
                if type(function_params[i]) == str:
                    function_params[i] = function_params[i].replace("'","\"")

        interface_params = []
        if "interface_params" in module:
            interface_params = module["interface_params"]
        topLevel.add_moduleV2(lookForKeyword("function",module),lookForKeyword("name",module),interface_params,function_params)

    if "connections" in json_file:
        for connection in json_file["connections"]:
            topLevel.add_connectionV2(lookForKeyword("from",connection),lookForKeyword("to",connection))

    if "busses" in json_file:
        for bus in json_file["busses"]:
            name = lookForKeyword("name",bus)
            function = lookForKeyword("function",bus)
            masters = lookForKeyword("masters",bus)
            slaves = lookForKeyword("slaves",bus)
            slaves = [(slave["name"],slave["routes"]) for slave in slaves]
            # route = lookForKeyword("route",bus)
            # route = [x.split("-") for x in route]
            # route = [(int(x[0]),int(x[1])) for x in route]
            topLevel.add_busV3(name,function,masters,slaves)

    print(topLevel.to_string())
    topLevel.to_file(args.output_folder)
    return topLevel

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert a json file to a bsv file')
    parser.add_argument('-json_file', default="example.json", type=str, help='The json file to convert')
    parser.add_argument('-of','--output_folder', type=str, help='The folder of output',default="./tutorial")
    # argument reload values True of False
    parser.add_argument("-reload",type=bool,default=True,help="If packages haven't changed since last run, use false to skip reloading")
    #print f as a example of how to use the json file
    parser.add_argument("-showExample",action="store_true",help="Prints the json file as a example of how to use the json file")
    parser.add_argument("-showPossibleConnections",action="store_true",help="Prints the possible connections between modules")


    args = parser.parse_args()
    if args.showExample:
        print(json.dumps(example_json,indent=4))
        exit()
    
    #check if the json file was passed as argument
    if args.json_file == None:
        print("No json file passed as argument")
        parser.print_help()
        exit()
    with open(args.json_file) as json_file:
        topLevel = load_json(json.load(json_file),args.reload)
    for start,ends in topLevel.possibleConnections.items():
        print(f"{start} -> {ends}")
    for busName,busInstance in topLevel.buses.items():
        print(f"{busName}")
    print("Hi")