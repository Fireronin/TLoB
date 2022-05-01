#%%
from os import read
from parsingFormating import *
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
# fifo3 = topLevel.add_moduleV2("mkFIFO","fifo3",["Bit#(32)"],[])
# reg = topLevel.add_moduleV2("mkRegU","reg",["Bit#(32)"],[])
# uprint = topLevel.add_moduleV2("mkReg","reg2",[],["reg._read"])
# a,b,c = topLevel.buildAndRun(".")
# print(a,b,c)    
# # topLevel.add_connectionV2("fifo3.enq","fifo3.first")

fifo1 = topLevel.addModule("mkSimpleFIFO","fifo1",["Bit#(32)"],[])
fifo2 = topLevel.addModule("mkSimpleFIFO","fifo2",["Bit#(32)"],[])
topLevel.addConnection("fifo1","fifo2")

print(topLevel.__str__())
topLevel.to_file()

# %%

