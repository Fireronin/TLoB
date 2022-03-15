#%%
from os import read
from extractor import *
from handlerV2 import *
from bsvSynthesizer import *
from typeDatabase import typeDatabase as tdb

#%% initalize bluetcl
create_bluetcl()
#add_folder("BlueStuff/build/bdir")
#add_folder("tutorial")
add_folder("Flute/src_SSITH_P2/build_dir")
# initalize tdb
db = tdb()
# Read contents of package
packages_to_load = ["Core","AXI4_Fake_16550","MemUtils","Connectable","FIFO","FIFOF","GetPut","AXI4_Types","AXI4_Interconnect","SourceSink","Routable","Core_IFC","ClientServer"]
db.addPackages(packages_to_load)

db.writeToFile()

# todo read json file
# %% Build bluespcefile


topLevel = TopLevelModule("top",db,package_name="FluteSoc")

# Axi4 parameters
MPARAMS = [5, 64, 64, 0, 0, 0, 0, 0]
SPARAMS = [5, 64, 64, 0, 0, 0, 0, 0]

core = topLevel.add_module(db.getFunctionByName("Core::mkCore"),"core",[],[])
memory = topLevel.add_module(db.getFunctionByName("MemUtils::mkAXI4SimpleMem"),"memory",SPARAMS,[32,"Invalid"])
fakeAXI = topLevel.add_module(db.getFunctionByName("AXI4_Fake_16550::mkAXI4_Fake_16550_Simple"),"aXI4_Fake_16550",SPARAMS,[])

topLevel.add_bus([core.submodule("cpu_imem_master")],[memory.get(),fakeAXI.get()],[(0,16),(16,32)])

print(topLevel.to_string())
topLevel.to_file("/mnt/d/Mega/Documents/CS/TLoB/tutorial/")

# %%

