#%%
from os import read
from extractor import *
from handlerV2 import *
from bsvSynthesizer import *
from typeDatabase import TypeDatabase as tdb
#%% initalize bluetcl
# initalize tdb
db = tdb(load=True)
db.addLibraryFolder("Flute/src_SSITH_P2/build_dir")
# Read contents of package
packages_to_load = ["Core","Prelude","OneWayBus","MemUtils","Connectable","FIFO","FIFOF","GetPut","AXI4_Types","AXI4_Interconnect","SourceSink","Routable","Core_IFC","ClientServer","MasterSlave","AXI4_Common_Types","MemSim","AXI4_Fake_16550","AXI4Stream_Types","AXI4Lite_Types"]
db.addPackages(packages_to_load)


# todo read json file
# %% Build bluespcefile


topLevel = TopLevelModule("top",db,package_name="FluteSoc")


# Axi4 parameters
SPARAMS = [6, 65, 64, 0, 0, 0, 0, 0]

tdtSPARAMS = [evaluateCustomStart(str(x),"type_def_type") for x in SPARAMS]

core = topLevel.add_moduleV2("Core::mkCore","core",[],None)
core2 = topLevel.add_moduleV2("Core::mkCore","core2",[],[])
# memory = topLevel.add_moduleV2("MemUtils::mkAXI4SimpleMem","memory",SPARAMS,[4096,'Maybe#("xddd")'])
# SPARAMS = [6, 64, 64, 0, 0, 0, 0, 0]
# fakeAXI = topLevel.add_moduleV2("AXI4_Fake_16550::mkAXI4_Fake_16550_Simple","aXI4_Fake_16550",SPARAMS,[])

# try:
#     topLevel.add_connectionV2("core.core_mem_master","memory")
#     topLevel.add_busV3("bus1","mkAXI4Bus",["core.core_mem_master"],[("memory",[(0,4096)]),("aXI4_Fake_16550",[(4096,8192)])])
# except Exception as e:
#     print(e)
#     pass

# memory = topLevel.add_moduleV2("MemUtils::mkAXI4SimpleMem","memory",SPARAMS,[4096,'Maybe#("xddd")'])
memory2 = topLevel.add_moduleV2("MemUtils::mkAXI4SimpleMem","memory",[],['4096', 'Maybe#("xdd")'])

print(topLevel.to_string())
topLevel.to_file("/mnt/d/Mega/Documents/CS/TLoB/tutorial/")

# %%

