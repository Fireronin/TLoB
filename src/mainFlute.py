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
packages_to_load = ["Core","Core_IFC","FIFO","FIFOF","Connectable","GetPut","AXI4_Types","AXI4_Interconnect","SourceSink","Routable"]
db.addPackages(packages_to_load)

db.writeToFile()

# todo read json file
# %% Build bluespcefile


topLevel = TopLevelModule("top",db,package_name="FIFOChain")


print(topLevel.to_string())
topLevel.to_file("FluteSoc.bsv","/mnt/e/Mega/Documents/CS/TLoB/tutorial/")

# %%

