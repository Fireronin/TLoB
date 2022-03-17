#%%
from os import read
from extractor import *
from handlerV2 import *
from bsvSynthesizer import *
from typeDatabase import TypeDatabase as tdb

#%% initalize bluetcl
create_bluetcl()
#add_folder("BlueStuff/build/bdir")
#add_folder("tutorial")
add_folder("Flute/src_SSITH_P2/build_dir")
# initalize tdb
db = tdb()
# Read contents of package
packages_to_load = ["Core","AXI4_Fake_16550","MemUtils","Connectable","FIFO","FIFOF","GetPut","AXI4_Types","AXI4_Interconnect","SourceSink","Routable","Core_IFC","ClientServer","MasterSlave","AXI4_Common_Types","MemSim"]
db.addPackages(packages_to_load)

db.writeToFile()

# todo read json file
# %% Build bluespcefile


topLevel = TopLevelModule("top",db,package_name="FluteSoc")

# Axi4 parameters
SPARAMS = [6, 64, 64, 0, 0, 0, 0, 0]

core = topLevel.add_module(db.getFunctionByName("Core::mkCore"),"core",[],[])
memory = topLevel.add_module(db.getFunctionByName("MemUtils::mkAXI4SimpleMem"),"memory",SPARAMS,[4096,"Invalid"])
fakeAXI = topLevel.add_module(db.getFunctionByName("AXI4_Fake_16550::mkAXI4_Fake_16550_Simple"),"aXI4_Fake_16550",SPARAMS,[])

print(topLevel.list_connectable(core.get(),[core.get(),memory.get(),fakeAXI.get()]))
print(topLevel.list_connectable(fakeAXI.get(),[fakeAXI.get(),memory.get(),core.get()]))
print(topLevel.list_connectable(memory.get(),[memory.get(),fakeAXI.get(),core.get()]))

bus = topLevel.add_busV2(ConnectionType.AXI4,"axi4_bus")
bus.add_master(core.submodule("core_mem_master"))
print(bus.filter_valid_slaves([memory.get(),fakeAXI.get()]))
bus.add_slave(memory.get(),[(0,4096)])
bus.add_slave(fakeAXI.get(),[(4096,8192)])


print(topLevel.to_string())
topLevel.to_file("/mnt/d/Mega/Documents/CS/TLoB/tutorial/")

# %%

