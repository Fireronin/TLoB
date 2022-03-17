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
packages_to_load = ["FIFO","FIFOF","Connectable","AXIDemo","AddressFlit","GetPut","AXI4_Types","AXI4_Interconnect","SourceSink","Routable"]
db.addPackages(packages_to_load)


db.writeToFile()

# todo read json file
# %% Build bluespcefile


topLevel = TopLevelModule("top",db,package_name="FIFOChain")

# this is usually done with defines with can't be querried
PARAMS = []
for td in ["ADDR_sz","DATA_sz","AWUSER_sz","WUSER_sz","BUSER_sz","ARUSER_sz","RUSER_sz"]:
    PARAMS.append(db.evaluateTypedef("AXIDemo::"+td))

MPARAMS = [db.evaluateTypedef("AXIDemo::"+"MID_sz")]+PARAMS
SPARAMS = [db.evaluateTypedef("AXIDemo::"+"SID_sz")]+PARAMS

m1 = topLevel.add_module(db.getFunctionByName("AXIDemo::axiMaster"),"m1",MPARAMS,[])
s1 = topLevel.add_module(db.getFunctionByName("AXIDemo::axiSlave"),"s1",SPARAMS,[])

bus = topLevel.add_busV2(ConnectionType.AXI4,"axi4_bus")
bus.add_master(m1.get())
bus.add_slave(s1.get(),[(0,4096)])


print(topLevel.to_string())
topLevel.to_file("FIFOChain.bsv","/mnt/e/Mega/Documents/CS/TLoB/tutorial/")

# %%

