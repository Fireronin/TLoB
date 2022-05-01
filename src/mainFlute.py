#%%
from os import read
from parsingFormating import *
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

topLevel.addTypedef("DATASIZE","64")
# Axi4 parameters
SPARAMS = [6, 64, "DATASIZE", 0, 0, 0, 0, 0]

tdtSPARAMS = [evaluateCustomStart(str(x),"type_def_type") for x in SPARAMS]


core = topLevel.addModule("Core::mkCore","core",[],[])
memory = topLevel.addModule("MemUtils::mkAXI4SimpleMem","memory",SPARAMS,[4096,'tagged Invalid'])

fakeAXI = topLevel.addModule("AXI4_Fake_16550::mkAXI4_Fake_16550_Simple","aXI4_Fake_16550",SPARAMS,[])

topLevel.addBus("bus1","AXI4_Interconnect::mkAXI4Bus",["core.core_mem_master"],[("memory",[(0,4096)]),("aXI4_Fake_16550",[(4096,8192)])])


print(topLevel.__str__())
topLevel.to_file()
topLevel.buildAndRun()
# %%

