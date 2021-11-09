namespace import ::Bluetcl::*
bpackage load Polyfifo
bpackage load tutorial/Polyfifo 
defs type Polyfifo

defs module Polyfifo

defs func Polyfifo

browsepackage 

browsetype list 

type constr FIFOIfc

type full FIFOIfc#(8)

bpackage clear

bpackage load Polyfifo

type full 
flags set -p ./tutorial:+