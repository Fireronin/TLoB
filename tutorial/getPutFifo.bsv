package Getputfifo;

import GetPut::*;

interface GetPutFIFOIfc#(type a);
    interface Put#(a) enq;
    interface Get#(a) first_deq;
endinterface

module mkGetPutFIFO(GetPutFIFOIfc#(a)) 
    provisos (Bits#(a, a__));
    Reg#(a) data <- mkReg(0);
    Reg#(Bool) isFull <- mkReg(False);
    interface Put enq;
        method Action put(a value) if (isFull==False);
            data <= value;
            isFull <= True;
        endmethod
    endinterface

    interface Get first_deq;
        method ActionValue#(a) get() if (isFull==True);
            isFull <= False;
            return data;
        endmethod
    endinterface

endmodule

endpackage