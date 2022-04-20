
package Simplefifo;
import GetPut :: *;

interface FIFOIfc;
    method Action enq(Bit#(32) value);
    method Action deq();
    method Bit#(32) first();
endinterface

instance ToPut#(FIFOIfc, Bit#(32));
    function toPut (s) = interface Put;
      method put = s.enq;
    endinterface;
endinstance

instance ToGet#(FIFOIfc, Bit#(32));
    function toGet (s) = interface Get;
      method get = actionvalue
        s.deq;
        return s.first();
      endactionvalue;
    endinterface;
endinstance


module mkSimpleFIFO(FIFOIfc);
    Reg#(Bit#(32)) data <- mkReg(0);
    Reg#(Bool) isFull <- mkReg(False);

    method Action enq(Bit#(32) value) if (isFull==False);
        data <= value;
        isFull <= True;
    endmethod

    method Action deq() if (isFull==True);
        isFull <= False;
    endmethod

    method Bit#(32) first() if (isFull==True);
        return data;
    endmethod

endmodule

endpackage