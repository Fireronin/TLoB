from django.shortcuts import render
from django.http import HttpResponse
import sys
import os
sys.path.append("..")
from typeDatabase import TypeDatabase as tdb
from handlerV2 import *
from bsvSynthesizer import *


print(os.getcwd())
create_bluetcl()
add_folder("Flute/src_SSITH_P2/build_dir")
db = tdb()
topLevel = TopLevelModule("top",db,package_name="FluteSoc")

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

