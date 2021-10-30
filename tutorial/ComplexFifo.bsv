package Wirefifo;

interface FIFOIfc;
    method Action enq(Bit#(32) value);
    method Action deq();
    method Bit#(32) first();
endinterface

module mkWireFIFO(FIFOIfc);
    Reg#(Bit#(32)) data <- mkReg(0);
    Reg#(Bool) isFull <- mkReg(False);
//    PulseWire enqW <- mkPulseWire;
    PulseWire deqW <- mkPulseWire;

    method Action enq(Bit#(32) value) if (deqW || isFull==False);
        data <= value;
        isFull <= True;
    endmethod

    method Action deq() if (isFull==True);
        isFull <= False;
        deqW.send;
    endmethod

    method Bit#(32) first() if (isFull==True);
        return data;
    endmethod

endmodule


    rule conect AB:
    mkConection()
        interfaceA.put(interfaceB.get())

endpackage