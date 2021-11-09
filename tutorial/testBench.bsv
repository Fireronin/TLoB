
package topMod;
import FIFO::*;
import Connectable::*;
import GetPut::*;
import Polyfifo::*;

module mktopMod();

    FIFOIfc#(8) f1 <- mkPolyFIFO();
    FIFOIfc#(8) f2 <- mkPolyFIFO();

    mkConnection(toGet(f1), toPut(f2));



endmodule

endpackage