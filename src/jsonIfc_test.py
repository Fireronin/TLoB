import sys
sys.path.append("src")
import jsonInterface
import json
from parsingFormating import *
from crawler import *
from bsvSynthesizer import *
from typeDatabase import TypeDatabase as tdb

def test_example():
    jsons = ["exampleFIFOs.json","exampleFlute.json"]
    for json_name in jsons:
        with open(json_name) as json_file:
            topLevel = jsonInterface.topLevelFromJSON(json.load(json_file),True)
            jsonInterface.showTypes(topLevel)
            jsonInterface.showPossibleConnections(topLevel)
            jsonInterface.showValidArguments(topLevel)
            assert(True)


def test_buildAndRun():
    db = tdb(load=False)

    db.addLibraryFolder("Flute/src_SSITH_P2/build_dir")
    db.addLibraryFolder("tutorial")
    # Read contents of package
    packages_to_load = ["ExampleAXI4","AXI4_Interconnect"]

    db.addPackages(packages_to_load)
    db.loadDependencies()

    # todo read json file
    # %% Build bluespcefile


    topLevel = TopLevelModule("top",db,package_name="ConnectedAXI4")

    master1 = topLevel.addModule("axiMaster","master1",[],[10])
    master2 = topLevel.addModule("axiMaster","master2",[],[11])

    slave1 = topLevel.addModule("axiSlave","slave1",[],[12])
    slave2 = topLevel.addModule("axiSlave","slave2",[],[13])

    #topLevel.add_connectionV2("master1","slave1")
    topLevel.addBus("mainBus","AXI4_Interconnect::mkAXI4Bus",["master1","master2"],[("slave1",[(0,1)]),("slave2",[(1,2)])])
    bO,sBO,sO = topLevel.buildAndRun(".")
    print("bO:",bO)
    print("sBO:",sBO)
    print("sO:",sO)

    assert(sO != "","No output")

# test_example()
# test_buildAndRun()