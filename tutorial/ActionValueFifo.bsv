package Actionvaluefifo;

interface ActionValueFIFOIfc;
    method Action enq(Bit#(32) value);
    method ActionValue#(Bit#(32)) first_deq();
endinterface

module mkAvFIFO(ActionValueFIFOIfc);
    Reg#(Bit#(32)) data <- mkReg(0);
    Reg#(Bool) isFull <- mkReg(False);

    method Action enq(Bit#(32) value) if (isFull==False);
        data <= value;
        isFull <= True;
    endmethod

    method ActionValue#(Bit#(32)) first_deq() if (isFull==True);
        isFull <= False;
        return data;
    endmethod

endmodule

endpackage