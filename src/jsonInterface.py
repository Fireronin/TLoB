#%%
from bsvSynthesizer import *
import json
from thefuzz import process
from typeDatabase import TypeDatabase as tdb
from handlerV2 import *
import argparse
import os
from colorama import Fore
import mock
import pytest

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

def load_json(json_file,reload=False,output_dir=None):
    db = tdb(load=not reload)
    
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
    if output_dir!=None:
        topLevel.to_file(output_dir)
    return topLevel

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert a json file to a bsv file')
    parser.add_argument('-json_file', default="example.json", type=str, help='The json file to convert')
    parser.add_argument('-of','--output_folder', type=str, help='The folder of output',default="./tutorial")
    # argument reload values True of False
    parser.add_argument("-reload",type=bool,default=False,help="If packages haven't changed since last run, use false to skip reloading")
    #print f as a example of how to use the json file
    # parser.add_argument("-showExample",action="store_true",help="Prints the json file as a example of how to use the json file")
    parser.add_argument("-showPossibleConnections",action="store_true",default=True,help="Prints the possible connections between modules")
    parser.add_argument("-showTypes",action="store_true",default=True,help="Prints the type indentifiers of interfaces in defined modules")

    args = parser.parse_args()
    
    #check if the json file was passed as argument
    if args.json_file == None:
        print("No json file passed as argument")
        parser.print_help()
        exit()
    with open(args.json_file) as json_file:
        topLevel = load_json(json.load(json_file),args.reload,args.output_folder)
    if args.showPossibleConnections:
        print(Fore.BLUE + "Potential connections:" + Fore.RESET)
        for start,ends in topLevel.possibleConnections.items():
            print(f"{start} -> {[end for end in ends]}")
        for busName,busInstance in topLevel.buses.items():
            print(f"Possible masters for {busName} {busInstance.mastersV.flit_type_ide}:")
            print(topLevel.buses['mainBus'].mastersV.listAddable(topLevel.knownNames.items()))
            print(f"Possible slaves for {busName} {busInstance.slavesV.flit_type_ide}:")
            print(topLevel.buses['mainBus'].slavesV.listAddable(topLevel.knownNames.items()))
    if args.showTypes:
        print(Fore.BLUE + "Infered Interfaces:"+ Fore.RESET)
        for name,value in topLevel.knownNames.items():
            print(f"{name} : {value}")
    if True:
        print(Fore.BLUE + "Valid arguments:" + Fore.RESET)
        for name,instance in topLevel.instances.items():
            if type(instance) != InstanceV2 or instance.creator.name == "mkConnection":
                continue
            print(f"{name} : {topLevel.validArguments(instance.creator)}")
    print(Fore.GREEN + "Finished" + Fore.RESET)

    
