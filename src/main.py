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
packages_to_load = ["FIFO","Connectable","GetPut","SourceSink","Routable"]
for package in packages_to_load:
    db.addPackage(package_name=package)



# todo read json file
# %% Build bluespcefile


topLevel = TopLevelModule("FIFOChain",db)
topLevel.add_module(db.getFunctionByName("mkFIFO"),["Bit#(8)"],[],"ff1")
topLevel.add_module(db.getFunctionByName("mkFIFO"),["Bit#(8)"],[],"ff2")

topLevel.add_connection("ff1","ff2")

print(topLevel.to_string())
topLevel.to_file("FIFOChain.bsv",os.path.join(os.getcwd(),"..","tutorial"))

# %%

