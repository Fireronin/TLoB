#%%
from os import read
from extractor import *
from handlerV2 import *
from bsvSynthesizer import *

#%% initalize bluetcl
create_bluetcl()
#add_folder()

# Read contents of package
load_package(package_name="FIFO")
load_package(package_name="Connectable")
types = read_all_types(package_name="FIFO")
funcs = list_funcs(package_name="FIFO")
funcs = funcs + list_funcs(package_name="Connectable")

#%% parse contents of package
initalize_parser(start="tcl_type_full_list") 
tt = parse_and_transform(funcs)
print(tt)

# todo read json file
# %% Build bluespcefile
def get_func(func_name):
    for func in tt:
        if func.name == func_name:
            return func
    raise Exception("Function not found")

topLevel = TopLevelModule("FIFOChain")
topLevel.add_module(get_func("mkFIFO"),["Bit#(8)"],[],"ff1")
topLevel.add_module(get_func("mkFIFO"),["Bit#(8)"],[],"ff2")

topLevel.add_connection("ff1","ff2")

print(topLevel.to_string())
topLevel.to_file("FIFOChain.bsv",os.path.join(os.getcwd(),"..","tutorial"))

# %%
