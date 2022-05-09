#%%
from bsvSynthesizer import *
import json
from thefuzz import process
from typeDatabase import TypeDatabase as tdb
from crawler import *
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

def topLevelFromJSON(json_file,reload=False,output_dir=None,saveLocation=os.path.join(".","saved")):
    db = tdb(load=not reload,saveLocation=saveLocation,librariesRoot=os.path.join(saveLocation,".."))
    
    if "aditional folders" in json_file:  
        for folder in json_file["aditional folders"]:
            db.addLibraryFolder(folder)
    
    packages = lookForKeyword("packages",json_file)
    packages = [package for package in packages if package not in db.packages]
    db.addPackages(packages)
    db.loadDependencies()

    topLevel = TopLevelModule(lookForKeyword("name",json_file),db,package_name=lookForKeyword("package_name",json_file))

    if "typedefs" in json_file:
        for typedef in json_file["typedefs"]:
            topLevel.addTypedef(typedef["name"],typedef["value"])

    modules = lookForKeyword("modules",json_file)
    for module in modules:
        function_params = []
        if "function_params" in module:
            function_params = module["function_params"]
            for i in range(len(function_params)):
                if type(function_params[i]) == str:
                    function_params[i] = function_params[i].replace("'","\"")

        interface_params = []
        if "interface_params" in module:
            interface_params = module["interface_params"]
        topLevel.addModule(lookForKeyword("function",module),lookForKeyword("name",module),interface_params,function_params)

    if "connections" in json_file:
        for connection in json_file["connections"]:
            topLevel.addConnection(lookForKeyword("from",connection),lookForKeyword("to",connection))

    if "buses" in json_file:
        for bus in json_file["buses"]:
            name = lookForKeyword("name",bus)
            function = lookForKeyword("function",bus)
            masters = lookForKeyword("masters",bus)
            slaves = lookForKeyword("slaves",bus)
            slaves = [(slave["name"],slave["routes"]) for slave in slaves]
            topLevel.addBus(name,function,masters,slaves)

    if "interface" in json_file:
        interface = json_file["interface"]
        if type(interface) == str:
            topLevel.setExportedInterface("",interface)
        else:
            members = [(lookForKeyword("name",member),lookForKeyword("value",member)) for member in lookForKeyword("members",interface) ]
            topLevel.setExportedInterface(lookForKeyword("name",interface),members)

    print(topLevel.__str__())
    if output_dir!=None:
        topLevel.to_file(output_dir)
    return topLevel

def showPossibleConnections(topLevel):
    print(Fore.BLUE + "Potential connections:" + Fore.RESET)
    for start,ends in topLevel.possibleConnections.items():
        print(f"{start} -> {[end for end in ends]}")
    for busName,busInstance in topLevel.buses.items():
        print(f"Possible masters for {busName} {busInstance.mastersV.flit_type_ide}:")
        print(topLevel.buses[busName].mastersV.listAddable(topLevel.knownNames.items()))
        print(f"Possible slaves for {busName} {busInstance.slavesV.flit_type_ide}:")
        print(topLevel.buses[busName].slavesV.listAddable(topLevel.knownNames.items()))

def showTypes(topLevel):
    print(Fore.BLUE + "Infered Interfaces:"+ Fore.RESET)
    for name,value in topLevel.knownNames.items():
        print(f"{name} : {value}")

def showValidArguments(topLevel):
    print(Fore.BLUE + "Valid arguments:" + Fore.RESET)
    for name,instance in topLevel.instances.items():
        if type(instance) != InstanceV2 or instance.creator.name == "mkConnection":
            continue
        print(f"{name} : {topLevel.validArguments(instance.creator)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert a json file to a bsv file')
    parser.add_argument('-json_file', default="test.json", type=str, help='The json file to convert')
    parser.add_argument('-of','--output_folder', type=str, help='The folder of output',default="./tutorial")
    # argument reload values True of False
    parser.add_argument("-reload",type=bool,default=False,help="If packages haven't changed since last run, use false to skip reloading")
    #print f as a example of how to use the json file
    # parser.add_argument("-showExample",action="store_true",help="Prints the json file as a example of how to use the json file")
    parser.add_argument("-showPossibleConnections",action="store_true",default=True,help="Prints the possible connections between modules")
    parser.add_argument("-showTypes",action="store_true",default=True,help="Prints the type indentifiers of interfaces in defined modules")
    parser.add_argument("-showValidArguments",action="store_true",default=True,help="Prints the valid arguments for each instance")

    args = parser.parse_args()
    
    #check if the json file was passed as argument
    if args.json_file == None:
        print("No json file passed as argument")
        parser.print_help()
        exit()
    with open(args.json_file) as json_file:
        topLevel = topLevelFromJSON(json.load(json_file),args.reload,args.output_folder)
    if args.showPossibleConnections:
        showPossibleConnections(topLevel)
    if args.showTypes:
        showTypes(topLevel)
    if args.showValidArguments:
        showValidArguments(topLevel)

    print(Fore.GREEN + "Finished" + Fore.RESET)

    
