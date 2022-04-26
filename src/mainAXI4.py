#%%
import sys
sys.path.append("src")
from os import read
from extractor import *
from handlerV2 import *
from bsvSynthesizer import *
from typeDatabase import TypeDatabase as tdb
#%% initalize bluetcl
# initalize tdb
db = tdb(load=True)

db.addLibraryFolder("Flute/src_SSITH_P2/build_dir")
db.addLibraryFolder("tutorial")
# Read contents of package
packages_to_load = ["ExampleAXI4","AXI4_Interconnect"]

db.addPackages(packages_to_load)
db.loadDependencies()

# todo read json file
# %% Build bluespcefile


topLevel = TopLevelModule("top",db,package_name="ConnectedAXI4")

master1 = topLevel.add_moduleV2("axiMaster","master1",[],[10])
master2 = topLevel.add_moduleV2("axiMaster","master2",[],[11])

slave1 = topLevel.add_moduleV2("axiSlave","slave1",[],[12])
slave2 = topLevel.add_moduleV2("axiSlave","slave2",[],[13])

#topLevel.add_connectionV2("master1","slave1")
topLevel.add_busV3("mainBus","AXI4_Interconnect::mkAXI4Bus",["master1","master2"],[("slave1",[(0,1)]),("slave2",[(1,2)])])



print(topLevel.to_string())
topLevel.to_file("/mnt/e/Mega/Documents/CS/TLoB/tutorial/")
bO,sBO,sO = topLevel.buildAndRun(".")
print(bO,sBO,sO)


# %%

