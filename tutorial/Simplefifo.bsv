
package Simplefifo;
import GetPut :: *;
import Connectable::*;
import FIFO::*;

interface FIFOIfc#(type value_size);
    method Action enq(value_size value);
    method Action deq();
    method value_size first();
endinterface

interface FIFOIfcConnector#(type value_size);
    interface FIFOIfc#(value_size) ff1;
    interface FIFOIfc#(value_size) ff2;
endinterface

instance ToPut#(FIFOIfc#(value_size), value_size);
    function toPut (s) = interface Put;
      method put = s.enq;
    endinterface;
endinstance

instance ToGet#(FIFOIfc#(value_size), value_size);
    function toGet (s) = interface Get;
      method get = actionvalue
        s.deq;
        return s.first();
      endactionvalue;
    endinterface;
endinstance

instance Connectable#(FIFOIfc#(value_size),FIFOIfc#(value_size));
    module mkConnection#(
        FIFOIfc#(value_size) s,
        FIFOIfc#(value_size) m)
        (Empty);
        mkConnection(toGet(m), toPut(s));
    endmodule
endinstance



module mkSimpleFIFO(FIFOIfc#(value_size)) provisos(Bits#(value_size, a__), Literal#(value_size));
    Reg#(value_size) data <- mkReg(0);
    Reg#(Bool) isFull <- mkReg(False);

    FIFO#(Bit#(32)) fifo <- mkFIFO();
    FIFO#(Bit#(32)) fifo2 <- mkFIFO();
    mkConnection(fifo.enq, fifo2.first);

    method Action enq(value_size value) if (isFull==False);
        data <= value;
        isFull <= True;
    endmethod

    method Action deq() if (isFull==True);
        isFull <= False;
    endmethod

    method value_size first() if (isFull==True);
        return data;
    endmethod

endmodule

(* synthesize *)
module mkSimpleFIFO_Synth(FIFOIfc#(Bit#(32)));
    FIFOIfc#(Bit#(32)) fifo <- mkSimpleFIFO();
    method enq = fifo.enq;
    method deq = fifo.deq;
    method first = fifo.first;
endmodule

// module mkConnectionFIFOs#(FIFOIfc#(value_size) f1, FIFOIfc#(value_size) f2) (FIFOIfcConnector#(value_size));
//     interface ff1 = f1;
//     interface ff2 = f2;
//     mkConnection(f1,f2);
// endmodule

// (* synthesize *)
// module mkConnectionFIFOs_Synth (FIFOIfcConnector#(Bit#(32)));
//     interface ff1  
//     mkConnection(toGet(m), toPut(s));
// endmodule

endpackage