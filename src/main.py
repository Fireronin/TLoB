#%%
from os import read
from extractor import *
from handlerV2 import *
from bsvSynthesizer import *
from typeDatabase import typeDatabase as tdb

#%% initalize bluetcl
create_bluetcl()
add_folder("BlueStuff/build/bdir")
add_folder("tutorial")
# initalize tdb
db = tdb()
# Read contents of package
packages_to_load = ["FIFO","FIFOF","Connectable","AddressFlit","GetPut","SourceSink","Routable"]
db.addPackages(packages_to_load)

db.writeToFile()
#db.saveStateToPickle()
# todo read json file
# %% Build bluespcefile


topLevel = TopLevelModule("top",db,package_name="FIFOChain")
ff1 = topLevel.add_module(db.getFunctionByName("FIFO::mkFIFO"),"ff1",["Bit#(8)"],[])
ff2 = topLevel.add_module(db.getFunctionByName("FIFO::mkFIFO"),"ff2",["Bit#(8)"],[])

#result = topLevel.list_connectable(ff1.get(),[ff1.get(),ff2.get()])

topLevel.add_connection(ff1.get(),ff2.get())

DATASIZE = topLevel.add_typedef("DATASIZE",1)
ADDRWIDTH = topLevel.add_typedef("ADDRWIDTH",4)

bf1 = topLevel.add_module(db.getFunctionByName("FIFOF::mkFIFOF"),"bf1",["AFlit#(DATASIZE, ADDRWIDTH)"],[])
bf2 = topLevel.add_module(db.getFunctionByName("FIFOF::mkFIFOF"),"bf2",["AFlit#(DATASIZE, ADDRWIDTH)"],[])

topLevel.add_bus([bf1],[bf2],[(0,2)])

result = topLevel.list_connectable(ff1.get(),[ff1.get(),ff2.get(),bf2.get()])

print(topLevel.to_string())
topLevel.to_file("/mnt/d/Mega/Documents/CS/TLoB/tutorial/")

# %%

