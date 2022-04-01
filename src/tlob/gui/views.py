import json
from django.shortcuts import render
from django.http import HttpResponse
import sys

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
    exception = ""
    try:
        module:InstanceV2 = topLevel.add_moduleV2(creator,name,[],None)
    except Exception as e:
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
    
