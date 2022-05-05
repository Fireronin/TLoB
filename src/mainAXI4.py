#%%
import sys
sys.path.append("src")
from os import read
from parsingFormating import *
from bsvSynthesizer import *
from typeDatabase import TypeDatabase as tdb
#%% initalize bluetcl
# initalize tdb
db = tdb(load=False)

db.addLibraryFolder("Flute/src_SSITH_P2/build_dir")
db.addLibraryFolder("tutorial")
# Read contents of package
packages_to_load = ["ExampleAXI4","AXI4_Interconnect"]

db.addPackages(packages_to_load)
db.loadDependencies()

# todo read json file
# %% Build bluespcefile


topLevel = TopLevelModule("top",db,package_name="ConnectedAXI4")

master1 = topLevel.addModule("axiMaster","master1",[],[10])
master2 = topLevel.addModule("axiMaster","master2",[],[11])

slave1 = topLevel.addModule("axiSlave","slave1",[],[12])
slave2 = topLevel.addModule("axiSlave","slave2",[],[13])

#topLevel.add_connectionV2("master1","slave1")
topLevel.addBus("mainBus","AXI4_Interconnect::mkAXI4Bus",["master1","master2"],[("slave1",[(0,1)]),("slave2",[(1,2)])])



print(topLevel.__str__())
topLevel.to_file()
bO,sBO,sO = topLevel.buildAndRun()
print(bO,sBO,sO)


# %%

