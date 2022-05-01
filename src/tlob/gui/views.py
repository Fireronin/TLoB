import json
from tkinter import Toplevel
from django.shortcuts import render
from django.http import HttpResponse
import sys
import traceback
sys.path.append("..")
from typeDatabase import TypeDatabase as tdb
from bsvSynthesizer import *
from django.views.decorators.cache import never_cache
from jsonInterface import topLevelFromJSON
print(os.getcwd())

db = tdb(load=True,saveLocation=os.path.join("../../saved"))
topLevel = TopLevelModule("top",db,package_name="GUITEST")
print(len(db.functions))

# Create your views here.


@never_cache
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

@never_cache
def listFunctions(request):
    json_data = json.loads(request.body)
    kind = json_data['type']
    names = []
    if kind == 'bus':
        for key,val in db.functions.items():
            try:
                if val.arguments['arg0'].return_type.full_name == 'Vector::Vector' and \
                val.arguments['arg1'].full_name == 'Vector::Vector' and \
                     val.arguments['arg2'].full_name == 'Vector::Vector':
                    names.append(key)
            except Exception as e:
                continue
    elif kind == 'all':
        names = list(db.functions.keys())
    print(kind, names)
    namesList = json.dumps({'names':names})
    return HttpResponse(namesList)

testRequestAddModule = {
    "name":"core",
    "creator":"mkCore"
}

@never_cache
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

@never_cache
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
        module:InstanceV2 = topLevel.addModule(creator,name,module_args,creator_args,input_context=context)
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

@never_cache
def confirmDesign(request):
    bsvText = topLevel.__str__()
    responseJson = {"bsvText" : bsvText}
    return HttpResponse(json.dumps(responseJson))

@never_cache
def confirmConnection(request):
    json_data = json.loads(request.body)

    inputs = json_data['inputs']
    name = json_data['name']
    print("Connection Inputs",inputs)
    try:
        topLevel.addConnection(inputs['0'],inputs['1'],name)
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

@never_cache
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
        
    
        topLevel.addBus(busName,creator,masters,slaves)
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

@never_cache
def getPossible(request):
    json_data = json.loads(request.body)
    name = json_data['name']
    initalized = json_data['initalized']
    creator = json_data['creator']
    if initalized:
        possibleMasters = topLevel.buses[name].mastersV.listAddable(topLevel.knownNames.items())
        possibleSlaves = topLevel.buses[name].slavesV.listAddable(topLevel.knownNames.items())
    else:
        possibleMasters = []
        cretorFunc = topLevel.db.getFunctionByName(creator)
        for name,value in topLevel.knownNames.items():
            try:
                topLevel.db.merge(cretorFunc.arguments[1].children[1],value,{})
            except Exception as e:
                continue
            possibleMasters.append(name)
        possibleSlaves = []
        for name,value in topLevel.knownNames.items():
            try:
                topLevel.db.merge(cretorFunc.arguments[2].children[1],value,{})
            except Exception as e:
                continue
            possibleSlaves.append(name)
    response = {
        'busname':name,
        'possibleMasters':possibleMasters,
        'possibleSlaves':possibleSlaves,
        'exception':"",
    }
    return HttpResponse(json.dumps(response))

@never_cache
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

@never_cache
def findConnections(request):
    print(request.body)
    json_data = json.loads(request.body)
    try:
        print(json_data)
        name = json_data['name']
        print("name:",name)
   
        connections = topLevel.possibleConnections[name]
        connections = list(set(connections))
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

@never_cache
def possibleConnectionStarts(request):
    names = []
    for key,value in  topLevel.possibleConnections.items():
        if value != []:
            names.append(key)
    names = list(set(names))
    #names = list(topLevel.knownNames.keys())
    response = {
        'names':names,
    }
    return HttpResponse(json.dumps(response))

@never_cache
def fullClear(request):
    global db,topLevel
    del db
    del topLevel
    db = tdb(load=True,saveLocation=os.path.join("../../saved"))
    topLevel = TopLevelModule("top",db,package_name="GUITEST")
    print(topLevel.possibleConnections)
    response = {
        'exception':"",
    }
    return HttpResponse(json.dumps(response))

@never_cache
def knownNames(request):
    names = list(topLevel.knownNames.keys())
    response = {
        'names':names,
    }
    return HttpResponse(json.dumps(response))

@never_cache
def buildAndRun(request):
    try:
        buildOuput,simulationBuildOutput,simulationRunOutput = topLevel.buildAndRun(".")
    except Exception as e:
        tb = traceback.format_exc()
        print(tb)
        print(e)
        return HttpResponse(json.dumps({'exception':"Something bad happend"}))
    response = {
        'exception':"",
        'buildOutput':buildOuput,
        'simulationBuildOutput':simulationBuildOutput,
        'simulationRunOutput':simulationRunOutput,
    }
    return HttpResponse(json.dumps(response))

@never_cache
def setExportedInterface(request):
    json_data = json.loads(request.body)
    topLevelName = json_data['topLevelName']
    nameIfc = json_data['name']
    memberNames = json_data['memberNames']
    memberValues = json_data['memberValues']
    topLevel.name = topLevelName
    if len(memberValues) != 0:
        try:
            # if len(memberNames) != len(memberValues):
            #     raise Exception("memberNames and memberValues must be the same length \n probably didn't assigned names to all the values")
            assignments = []
            for slot,name in memberNames.items():
                value = memberValues[slot]
                assignments.append((name,value))
            if len(assignments) == 1:
                topLevel.setExportedInterface(nameIfc,assignments[0][1])
            else:
                topLevel.setExportedInterface(nameIfc,assignments)
        except Exception as e:
            tb = traceback.format_exc()
            print(tb)
            print(e)
            return HttpResponse(json.dumps({'exception':str(e)}))
    response = {
        'name':name,
        'exception':"",
    }
    return HttpResponse(json.dumps(response))

@never_cache
def loadFromJSON(request):
    # json file is at 'JSON' usign FromData
    json_data = json.loads(request.body)
    global topLevel
    topLevel = topLevelFromJSON(json_data,reload=False)
    return HttpResponse(json.dumps({'exception':""}))

@never_cache
def saveToJSON(request):
    json_file = json.dumps(topLevel.toJSON(),indent=4, sort_keys=True)
    #send json file to client
    return HttpResponse(json_file)
    