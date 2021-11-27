namespace import ::Bluetcl::*
flags set -p ./tutorial:+
flags set -p ./BlueStuff/build/bdir:+
bpackage load Polyfifo
bpackage load SourceSink


type constr SourceSink::ToSource
type full SourceSink::ToSource#(a,b)

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
