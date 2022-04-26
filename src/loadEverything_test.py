#%%
import os
#print curent directory
print(os.getcwd())
import importlib
# load packages from /src
import sys
sys.path.append("src")


from extractor import *
from handlerV2 import *
from bsvSynthesizer import *
from typeDatabase import TypeDatabase as tdb


def loadAllAndDoQuickRun():
    #%% initalize bluetcl
    start_time = time.time()
    db = tdb(load=False)

    db.addLibraryFolder("Flute/src_SSITH_P2/build_dir")
    db.addLibraryFolder("tutorial")

    # find all folder in "/opt/tools/bsc/bsc-2021/lib/Libraries" and add them to the database
    for root, dirs, files in os.walk("/opt/tools/bsc/bsc-2021/lib/Libraries"):
        for dir in dirs:
            db.addLibraryFolder(os.path.join(root,dir))

    packages_to_load = []
    #find all packages (XXX.bo) in "Flute/src_SSITH_P2/build_dir"
    for file in os.listdir("Flute/src_SSITH_P2/build_dir"):
        if file.endswith(".bo"):
            packages_to_load.append(file[:-3])

    for file in os.listdir("/opt/tools/bsc/bsc-2021/lib/Libraries"):
        if file.endswith(".bo"):
            packages_to_load.append(file[:-3])


    db.addPackages(packages_to_load)

    print("Time to load libraries: " + str(time.time()-start_time))
    # todo read json file
    # %% Build bluespcefile


    topLevel = TopLevelModule("top",db,package_name="FIFOChain")
    SPARAMS = [6, 64, "DATASIZE", 0, 0, 0, 0, 0]

    core = topLevel.add_moduleV2("Core::mkCore","core",[],[])
    memory = topLevel.add_moduleV2("MemUtils::mkAXI4SimpleMem","memory",SPARAMS,[4096,'tagged Invalid'])

    fakeAXI = topLevel.add_moduleV2("AXI4_Fake_16550::mkAXI4_Fake_16550_Simple","aXI4_Fake_16550",SPARAMS,[])

    topLevel.add_busV3("bus1","mkAXI4Bus",["core.core_mem_master"],[("memory",[(0,4096)]),("aXI4_Fake_16550",[(4096,8192)])])


    print(topLevel.to_string())
    topLevel.to_file("/mnt/e/Mega/Documents/CS/TLoB/tutorial/")
    bO,sBO,sO = topLevel.buildAndRun()
    return sO

if __name__ == "__main__":
    loadAllAndDoQuickRun()

def test_loadEverything():
    sO =loadAllAndDoQuickRun()
    assert(sO != "")
    return

# %%

