export TOPMOD=top
export SOURCEFOLDER=./tutorial/
export TOPFILE=TopBus.bsv
echo $TOPMOD
if [ "$SYNTH" = "1" ]; then
    bsc $BSCFLAGS -u -verilog -g $TOPMOD $TOPFILE
else
    if bsc $BSCFLAGS -sim -g $TOPMOD -u $SOURCEFOLDER$TOPFILE; then
        if bsc $BSCFLAGS -sim -o $TOPMOD -e $TOPMOD $SOURCEFOLDER$TOPMOD.ba; then
            ./$TOPMOD
        else
            echo Failed to generate executable simulation model
        fi
    else
        echo Failed to compile
    fi
fi
