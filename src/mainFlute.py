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
packages_to_load =["Routable","Prelude"] # ["Core","Prelude","OneWayBus","MemUtils","Connectable","FIFO","FIFOF","GetPut","AXI4_Types","AXI4_Interconnect","SourceSink","Routable","Core_IFC","ClientServer","MasterSlave","AXI4_Common_Types","MemSim"]
db.addPackages(packages_to_load)

db.writeToFile()

# todo read json file
# %% Build bluespcefile


topLevel = TopLevelModule("top",db,package_name="FluteSoc")

td1 = evaluateCustomStart("4096","type_def_type")
td2 = evaluateCustomStart('Maybe#("xddd")',"type_def_type")
pd = evaluateCustomStart('Bit#(64)',"type_def_type")
pd2 = evaluateCustomStart('Bit#(64)',"type_def_type")

pd5 = evaluateCustomStart('AXI4Lite_Types::AXI4Lite_Slave #( 5, 64, 0, 0, 0, 0, 0)',"type_def_type")
pd6 = evaluateCustomStart('AXI4Stream_Types::AXI4Stream_Slave #(rxId, 16, rxDest, rxUser)',"type_def_type")
pd7 = evaluateCustomStart('AXI4Stream_Types::AXI4Stream_Master #(txId, 32, txDest, txUser)',"type_def_type")
pd8 = evaluateCustomStart('c',"type_def_type")

args2 = [pd5,pd7,pd6,"c"]
#db.merge(td1,td2)

rr = evaluateCustomStart('Routable::Range#(16)',"type_def_type")
InstanceV2(db,db.getFunctionByName('Routable::rangeBase'),creator_args=[rr],module_args=["a"],instance_name="vvv")
InstanceV2(db,db.getFunctionByName('Routable::rangeBase'),creator_args=[rr],module_args=["a"],instance_name="vvv")
InstanceV2(db,db.getFunctionByName('Routable::rangeBase'),creator_args=[rr],module_args=["a"],instance_name="vvv")

InstanceV2(db,db.getFunctionByName("MemUtils::mkMem"),creator_args=[td1,td2],module_args=[pd,pd2],instance_name="aaaa")
InstanceV2(db,db.getFunctionByName("AXI4_Fake_16550::mkAXI4_Fake_16550"),creator_args=[],module_args=args2,instance_name="vvv")
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

