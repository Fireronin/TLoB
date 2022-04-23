import json
from django.shortcuts import render
from django.http import HttpResponse
import sys
import traceback
sys.path.append("..")
from typeDatabase import TypeDatabase as tdb
from bsvSynthesizer import *


print(os.getcwd())

db = tdb(load=True,saveLocation=os.path.join("../../saved"))
topLevel = TopLevelModule("top",db,package_name="GUITEST")
print(len(db.functions))
print

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def listFunctions(request):
    json_data = json.loads(request.body)
    kind = json_data['type']
    names = []
    if kind == 'bus':
        for key,val in db.functions.items():
            try:
                if val.arguments[1].full_name == 'Vector::Vector' and \
                     val.arguments[2].full_name == 'Vector::Vector' and\
                     val.arguments[0].return_type.full_name == 'Vector::Vector':
                    names.append(key)
                    # val = db.functions['AXI4_Interconnect::mkAXI4Bus_Sig']
                    # print(val.arguments[1].full_name == 'Vector::Vector',\
                    #  val.arguments[2].full_name == 'Vector::Vector',\
                    #  type(val.arguments[0]) == ExFunction)
            except Exception as e:
                continue
    elif kind == 'all':
        names = list(db.functions.keys())
    namesList = json.dumps({'names':names})
    return HttpResponse(namesList)

testRequestAddModule = {
    "name":"core",
    "creator":"mkCore"
}

def addModule(request):
    # parse post request with json
    
    json_data = json.loads(request.body)
    # get name of module
    name = json_data['name']
    creator = json_data['creator']
    creatorFunc = db.getFunctionByName(creator)
    print("name:",name,"creator:",creator)
    exception = ""

    response = {
        'name':name,
        'creator':creator,
        'exception':exception,
        'defaultArguments': {str(i):str(arg) for i,arg in creatorFunc.arguments.items()},
        'validArguments': topLevel.validArguments(creatorFunc),
        'interface': creatorFunc.return_type.json,
    }
    
    print(response)
    return HttpResponse(json.dumps(response))

def confirmModule(request):
    json_data = json.loads(request.body)
    name = json_data['name']
    creator = json_data['creator']
    creator_args = list( json_data['creator_args'].values())
    module_args = [evaluateCustomStart(arg) for arg in json_data['module_args']]
    context = json_data['context']
    print("name:",name,"creator:",creator,"creator_args:",creator_args,"module_args:",module_args)
    exception = ""
    try:
        module:InstanceV2 = topLevel.add_moduleV2(creator,name,module_args,creator_args,input_context=context)
    except Exception as e:
        tb = traceback.format_exc()
        print(tb)
        exception = str(e)
        print(e)
        return HttpResponse(json.dumps({'exception':str(e)}))

    response = {
        'name':name,
        'creator':creator,
        'exception':exception,
        'arguments': {f'arg_{i}':arg.json for i,arg in module.creator.arguments.items()},
        'interface': module.creator.return_type.json,
    }
    return HttpResponse(json.dumps(response))

def confirmDesign(request):
    bsvText = topLevel.to_string()
    responseJson = {"bsvText" : bsvText}
    return HttpResponse(json.dumps(responseJson))

def confirmConnection(request):
    json_data = json.loads(request.body)

    inputs = json_data['inputs']
    name = json_data['name']
    print("Connection Inputs",inputs)
    try:
        topLevel.add_connectionV2(inputs['0'],inputs['1'],name)
    except Exception as e:
        tb = traceback.format_exc()
        print(tb)
        exception = str(e)
        print(e)
        return HttpResponse(json.dumps({'exception':str(e)}))
    response = {
        'exception':"",
    }
    return HttpResponse(json.dumps(response))

def confirmBus(request):
    json_data = json.loads(request.body)
    print(json_data)
    busName = json_data['name']
    creator = json_data['creator']
    inputs = json_data['inputs']
    ranges = json_data['ranges']
    exception = ""
    try:
        print("name:",busName,"creator:",creator,"masters:",inputs,"ranges:",ranges)
        masters = {}
        slaves = {}
        for name,value in inputs.items():
            kind,id = name.split(" ")
            if kind == "master":
                masters[int(id)] = value
            else:
                slaves[int(id)] = (value,None)
        for name,range in ranges.items():
            kind,id = name.split(" ")
            if kind == "master":
                raise Exception("Master range not supported")
            else:
                #I'm using eval this is a bit sus
                slaves[int(id)] = (slaves[int(id)][0],eval(range))
        #convert masters and slaves to lists
        masters = list(masters.values())
        slaves = list(slaves.values())
        
    
        topLevel.add_busV3(busName,creator,masters,slaves)
        possibleMasters = topLevel.buses[busName].mastersV.listAddable(topLevel.knownNames.items())
        possibleSlaves = topLevel.buses[busName].slavesV.listAddable(topLevel.knownNames.items())
    except Exception as e:
        tb = traceback.format_exc()
        print(tb)
        exception = str(e)
        print(e)
        return HttpResponse(json.dumps({'exception':str(e)}))

    response = {
        'name':name,
        'creator':creator,
        'exception':exception,
        'masters':possibleMasters,
        'slaves':possibleSlaves,
    }
    return HttpResponse(json.dumps(response))

def removeNode(request):
    json_data = json.loads(request.body)
    name = json_data['name']
    print("name:",name)
    try:
        topLevel.remove(name)
    except Exception as e:
        tb = traceback.format_exc()
        print(tb)
        exception = str(e)
        print(e)
        return HttpResponse(json.dumps({'exception':str(e)}))
    response = {
        'name':name,
        'exception':"",
    }
    print(topLevel.instances)
    return HttpResponse(json.dumps(response))

def findConnections(request):
    print(request.body)
    json_data = json.loads(request.body)
    try:
        print(json_data)
        name = json_data['name']
        print("name:",name)
   
        connections = topLevel.possibleConnections[name]
        print(connections)
    except Exception as e:
        tb = traceback.format_exc()
        print(tb)
        exception = str(e)
        print(e)
        return HttpResponse(json.dumps({'exception':str(e)}))
    response = {
        'name':name,
        'exception':"",
        'connections':connections,
    }
    return HttpResponse(json.dumps(response))

def possibleConnectionStarts(request):
    names = []
    for key,value in  topLevel.possibleConnections.items():
        if value != []:
            names.append(key)
    #names = list(topLevel.knownNames.keys())
    response = {
        'names':names,
    }
    return HttpResponse(json.dumps(response))

def fullClear(request):
    global db,topLevel
    db = tdb(load=True,saveLocation=os.path.join("../../saved"))
    topLevel = TopLevelModule("top",db,package_name="GUITEST")
    response = {
        'exception':"",
    }
    return HttpResponse(json.dumps(response))

def knownNames(request):
    names = list(topLevel.knownNames.keys())
    response = {
        'names':names,
    }
    return HttpResponse(json.dumps(response))