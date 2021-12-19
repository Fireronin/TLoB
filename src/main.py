#%%
from os import read
from extractor import *
from handlerV2 import *
from bsvSynthesizer import *
from typeDatabase import typeDatabase as tdb

#%% initalize bluetcl
create_bluetcl()
add_folder("BlueStuff/build/bdir")

# initalize tdb
db = tdb()
# Read contents of package
packages_to_load = ["FIFO","FIFOF","Connectable","GetPut","AXI4_Types","AXI4_Interconnect","SourceSink","Routable"]
db.addPackages(packages_to_load)

db.writeToFile()

# todo read json file
# %% Build bluespcefile


topLevel = TopLevelModule("top",db)
ff1 = topLevel.add_module(db.getFunctionByName("FIFO.mkFIFO"),"ff1",["Bit#(8)"],[])
ff2 = topLevel.add_module(db.getFunctionByName("FIFO.mkFIFO"),"ff2",["Bit#(8)"],[])

topLevel.add_connection(ff1,ff2)

bf1 = topLevel.add_module(db.getFunctionByName("FIFOF.mkFIFOF"),"bf1",["Bit#(8)"],[])
bf2 = topLevel.add_module(db.getFunctionByName("FIFOF.mkFIFOF"),"bf2",["Bit#(8)"],[])

topLevel.add_bus([bf1],[bf2],[(0,2)])

print(topLevel.to_string())
topLevel.to_file("FIFOChain.bsv","/mnt/e/Mega/Documents/CS/TLoB/tutorial/")

# %%

