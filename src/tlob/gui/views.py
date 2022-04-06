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

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def listFunctions(request):
    names = list(db.functionNameCache.keys())
    # trim to fist 3 names
    #names = names[:3]
    #crate json with list of names without dumps
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
    print("name:",name,"creator:",creator)
    exception = ""
    try:
        module:InstanceV2 = topLevel.add_moduleV2(creator,name,[],None)
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
        'interface': module.creator.type_ide.json,
    }
    return HttpResponse(json.dumps(response))

def confirmModule(request):
    json_data = json.loads(request.body)
    name = json_data['name']
    creator = json_data['creator']
    creator_args = list( json_data['creator_args'].values())
    module_args = json_data['module_args']
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
        'interface': module.creator.type_ide.json,
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
    busName = json_data['name']
    creator = json_data['creator']
    inputs = json_data['inputs']
    ranges = json_data['ranges']

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
            print(eval(range))
            slaves[int(id)] = (slaves[int(id)][0],eval(range))
    #convert masters and slaves to lists
    masters = list(masters.values())
    slaves = list(slaves.values())
    exception = ""
    try:
        topLevel.add_busV3(busName,creator,masters,slaves)
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
    }
    return HttpResponse(json.dumps(response))