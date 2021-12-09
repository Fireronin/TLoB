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
packages_to_load = ["FIFO","Connectable","GetPut","AXI4_Types","SourceSink","Routable"]
for package in packages_to_load:
    db.addPackage(package_name=package)

db.writeToFile()

# todo read json file
# %% Build bluespcefile


topLevel = TopLevelModule("FIFOChain",db)
topLevel.add_module(db.getFunctionByName("FIFO.mkFIFO"),"ff1",["Bit#(8)"],[])
topLevel.add_module(db.getFunctionByName("FIFO.mkFIFO"),"ff2",["Bit#(8)"],[])

topLevel.add_connection("ff1","ff2")

print(topLevel.to_string())
topLevel.to_file("FIFOChain.bsv","/mnt/e/Mega/Documents/CS/TLoB/tutorial/")

# %%

