#%%
from os import read
from extractor import *
from handlerV2 import *
from bsvSynthesizer import *
from typeDatabase import TypeDatabase as tdb

#%% initalize bluetcl
create_bluetcl()
add_folder("BlueStuff/build/bdir")
add_folder("tutorial")
# initalize tdb
db = tdb()
# Read contents of package
packages_to_load = ["FIFO","FIFOF","Connectable","AddressFlit","GetPut","SourceSink","Routable","AXI"]
db.addPackages(packages_to_load)
knownPackages = list_packages()
db.addPackages(knownPackages)
db.writeToFile()
#db.saveStateToPickle()
# todo read json file
# %% Build bluespcefile


topLevel = TopLevelModule("top",db,package_name="FIFOChain")
ff1 = topLevel.add_module(db.getFunctionByName("FIFO::mkFIFO"),"ff1",["Bit#(8)"],[])
ff2 = topLevel.add_module(db.getFunctionByName("FIFO::mkFIFO"),"ff2",["Bit#(8)"],[])

DATASIZE = topLevel.add_typedef("DATASIZE",1)
ADDRWIDTH = topLevel.add_typedef("ADDRWIDTH",4)

bf1 = topLevel.add_module(db.getFunctionByName("FIFOF::mkFIFOF"),"bf1",["AFlit#(Bit#(DATASIZE), ADDRWIDTH)"],[])
bf2 = topLevel.add_module(db.getFunctionByName("FIFOF::mkFIFOF"),"bf2",["AFlit#(DATASIZE, ADDRWIDTH)"],[])

busV2 = topLevel.add_busV2(ConnectionType.one_way,"bus")
print(busV2.filter_valid_slaves([bf1.get(),bf2.get()]))
busV2.add_master(bf1.get())
busV2.add_slave(bf2.get(),[(0,2)])
print("lol")
result = topLevel.list_connectable(ff1.get(),[ff1.get(),ff2.get(),bf2.get()])

print(topLevel.to_string())
topLevel.to_file("/mnt/d/Mega/Documents/CS/TLoB/tutorial/")

# %%

