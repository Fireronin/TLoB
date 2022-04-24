export TOPMOD=top
export OUTDIR=./bscBuild/
#export TOPFILE=./tutorial/TopBus.bsv
export TOPFILE2=./tutorial/ExampleAXI4.bsv
export TOPFILE=./tutorial/ConnectedAXI4.bsv
#export TOPFILE=./BlueStuff/examples/Example-OneWayBus-SingleFlit.bsv
#export TOPFILE=./Flute/libs/BlueStuff/AXI4_Fake_16550.bsv
#export TOPFILE=./Flute/libs/BlueStuff/AXI/AXI4Lite.bsv
export BSCFLAGS="-p .:./tutorial:./Flute/src_SSITH_P2/build_dir:+"
export CFILES="Flute/libs/BlueStuff/BlueUtils/MemSim.c Flute/libs/BlueStuff/BlueUtils/SimUtils.c"

echo $TOPMOD
if [ "$SYNTH" = "1" ]; then
    bsc $BSCFLAGS -u -verilog -g $TOPMOD $TOPFILE
else
    bsc $BSCFLAGS $TOPFILE2
    if bsc $BSCFLAGS -sim -bdir $OUTDIR  -g $TOPMOD -u $TOPFILE ; then
        # move TOPMOD.ba to the build directory from topfile directory
        cp ./tutorial/$TOPMOD.ba $OUTDIR
        if bsc $BSCFLAGS -sim -simdir $OUTDIR -o  $OUTDIR$TOPMOD -e $TOPMOD $OUTDIR$TOPMOD.ba $CFILES; then
            $OUTDIR$TOPMOD
        else
            echo Failed to generate executable simulation model
        fi
    else
        echo Failed to compile
    fi
fi

# bsc -p  .:./tutorial:./BlueStuff/build/bdir:+ -u ./tutorial/Simplefifo.bsv
# bsc -g mkSimpleFIFO -verilog  ./tutorial/Simplefifo.bsv
# bsc -g mkPolyFIFO -verilog  ./tutorial/Polyfifo.bsv