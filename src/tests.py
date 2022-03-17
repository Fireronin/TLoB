import os
import typeDatabase
from typeDatabase import TypeDatabase as tdb

#use whereis bsc to get the path of the bsc binary 
BSCPATH = os.popen("whereis bsc").read().split()[1][:-4]

# Get names of all libraries (.bo) in BSCPATH + /lib/Libraries 
LIBRARIES = []
for lib in os.listdir(BSCPATH + "/../lib/Libraries"):
    if lib.endswith(".bo"):
        # Get name of library without extension
        lib = lib[:-3]
        # Get name of library without version
        lib = lib.split("-")[0]
        # Add library to list of libraries
        LIBRARIES.append(lib)
    

IGNORE = ["PAClib"]
# remove libraries that are in the ignore list
for lib in IGNORE:
    if lib in LIBRARIES:
        LIBRARIES.remove(lib)


db = tdb()

db.addPackages(LIBRARIES)


db.writeToFile()
