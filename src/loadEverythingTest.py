#%%
import os
from extractor import *
from handlerV2 import *
from bsvSynthesizer import *
from typeDatabase import TypeDatabase

#%% initalize bluetcl
create_bluetcl()
add_folder("Flute/src_SSITH_P2/build_dir")
add_folder("tutorial")
# initalize tdb
db = TypeDatabase()

packages_to_load = []
#find all packages (XXX.bo) in "Flute/src_SSITH_P2/build_dir"
for file in os.listdir("Flute/src_SSITH_P2/build_dir"):
    if file.endswith(".bo"):
        packages_to_load.append(file[:-3])

# #remove CacheCore
# packages_to_load.remove("CacheCore")
# packages_to_load.remove("Core")

packages_to_load.insert("FIFO")

for package in packages_to_load:
    db.loadPackage(package)

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

bf1 = topLevel.add_module(db.getFunctionByName("FIFOF::mkFIFOF"),"bf1",["AFlit#(DATASIZE, ADDRWIDTH)"],[])
bf2 = topLevel.add_module(db.getFunctionByName("FIFOF::mkFIFOF"),"bf2",["AFlit#(DATASIZE, ADDRWIDTH)"],[])

busV2 = topLevel.add_busV2(ConnectionType.one_way,"bus")
print(busV2.filter_valid_slaves([bf1.get(),bf2.get()]))
busV2.add_master(bf1.get())
busV2.add_slave(bf2.get(),[(0,2)])
print("lol")
result = topLevel.list_connectable(ff1.get(),[ff1.get(),ff2.get(),bf2.get()])

print(topLevel.to_string())
topLevel.to_file("/mnt/e/Mega/Documents/CS/TLoB/tutorial/")

# %%

