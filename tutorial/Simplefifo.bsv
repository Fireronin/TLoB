
package Simplefifo;
import GetPut :: *;
import Connectable::*;

interface FIFOIfc#(type value_size);
    method Action enq(value_size value);
    method Action deq();
    method value_size first();
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

endpackage