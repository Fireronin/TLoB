package Gcd;

interface GcdIfc;
    method Action in(UInt#(16) a, UInt#(16) b);
    method ActionValue#(UInt#(16)) out();
endinterface

module mkGcd(GcdIfc);
    Reg#(UInt#(16)) result <- mkReg(0);
    Reg#(UInt#(16)) a <- mkReg(0);
    Reg#(UInt#(16)) b <- mkReg(0);
    PulseWire enqW <- mkPulseWire;
    PulseWire deqW <- mkPulseWire;

    rule increment if (!enqW);
        UInt#(16) e = a;
        UInt#(16) f = b;
        Bool notDone = True;
        for (Integer i = 0; i < 30; i=i+1) begin
            if (result==0 && notDone ) begin
                if (f == e) begin
                    result <= e;
                    notDone = False;
                end
                else begin
                    if (e<f) begin
                        f = f-e;
                    end else begin
                        e = e-f;
                    end
                    
                end
            end
        end
    endrule  

    method Action in(UInt#(16) aIn, UInt#(16) bIn);
        enqW.send;
        a <= aIn;
        b <= bIn;
        result <= 0;
        
    endmethod

    method ActionValue#(UInt#(16)) out() if (result!=0);
        return result;
    endmethod



endmodule

endpackage