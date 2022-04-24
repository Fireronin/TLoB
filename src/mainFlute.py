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
packages_to_load = ["Core","MemUtils","Connectable","AXI4_Fake_16550","AXI4_Interconnect"]

db.addPackages(packages_to_load)
db.loadDependencies()

# todo read json file
# %% Build bluespcefile


topLevel = TopLevelModule("top",db,package_name="FluteSoc")

topLevel.add_typedef("DATASIZE","64")
# Axi4 parameters
SPARAMS = [6, 64, "DATASIZE", 0, 0, 0, 0, 0]

tdtSPARAMS = [evaluateCustomStart(str(x),"type_def_type") for x in SPARAMS]


core = topLevel.add_moduleV2("Core::mkCore","core",[],[])
memory = topLevel.add_moduleV2("MemUtils::mkAXI4SimpleMem","memory",SPARAMS,[4096,'Maybe#("xddd")'])

fakeAXI = topLevel.add_moduleV2("AXI4_Fake_16550::mkAXI4_Fake_16550_Simple","aXI4_Fake_16550",SPARAMS,[])

topLevel.add_connectionV2("core.core_mem_master","memory")
topLevel.add_busV3("bus1","AXI4_Interconnect::mkAXI4Bus",["core.core_mem_master"],[("memory",[(0,4096)]),("aXI4_Fake_16550",[(4096,8192)])])


print(topLevel.to_string())
topLevel.to_file("/mnt/e/Mega/Documents/CS/TLoB/tutorial/")

# %%

