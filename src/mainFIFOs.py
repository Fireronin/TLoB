#%%
from os import read
from extractor import *
from handlerV2 import *
from bsvSynthesizer import *
from typeDatabase import TypeDatabase as tdb
#%% initalize bluetcl
# initalize tdb
db = tdb(load=True)

db.addLibraryFolder("tutorial")
# Read contents of package
packages_to_load = ["Simplefifo"]

db.addPackages(packages_to_load)
db.loadDependencies()

# todo read json file
# %% Build bluespcefile


topLevel = TopLevelModule("top",db,package_name="FIFOChain")
fifo3 = topLevel.add_moduleV2("mkFIFO","fifo3",["Bit#(32)"],[])
topLevel.add_connectionV2("fifo3.enq","fifo3.first")

fifo1 = topLevel.add_moduleV2("mkSimpleFIFO","fifo1",["Bit#(32)"],[])
fifo2 = topLevel.add_moduleV2("mkSimpleFIFO","fifo2",["Bit#(32)"],[])
topLevel.add_connectionV2("fifo1","fifo2")

print(topLevel.to_string())
topLevel.to_file("/mnt/e/Mega/Documents/CS/TLoB/tutorial/")

# %%

