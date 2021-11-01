package Polyfifo;

interface FIFOIfc#(numeric type value_size);
    method Action enq(Bit#(value_size) value);
    method Action deq;
    method Bit#(value_size) first();
endinterface

interface FIFOIfc2#(numeric type value_size);
    method Action enq(Bit#(value_size) value);
    method Action deq(Bit#(value_size) value, Bit#(value_size) value2);
    method Bit#(value_size) first();
endinterface

interface FIFOIfc3;
    method Action enq(Bit#(4) value);
    method Action deq(Bit#(4) value, Bit#(5) value2);
    method Bit#(6) first();
endinterface

module mkPolyFIFO(FIFOIfc#(value_size));
    Reg#(Bit#(value_size)) data <- mkReg(0);
    Reg#(Bool) isFull <- mkReg(False);

    method Action enq(Bit#(value_size) value) if (isFull==False);
        data <= value;
        isFull <= True;
    endmethod

    method Action deq() if (isFull==True);
        isFull <= False;
    endmethod

    method Bit#(value_size) first() if (isFull==True);
        return data;
    endmethod

endmodule

endpackage