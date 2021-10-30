package Rgbgreyscale;

typedef struct {
    a_type r;
    a_type g;
    a_type b;
} RgbT#(type a_type) deriving (Bits,Eq);

interface RgbGreyscaleIfc;
    method Action in(RgbT#(Bit#(8)) val);
    method ActionValue#(Bit#(8)) out();
endinterface

module mkRgbGreyscaleConverter(RgbGreyscaleIfc);
    Reg#(Maybe#(Bit#(8))) tmp <- mkReg( tagged Invalid);
    method Action in(RgbT#(Bit#(8)) val) if (!isValid(tmp));
        tmp <= tagged Valid ( (val.r>>2) + (val.g>>1) + (val.b>>3));
    endmethod

    method ActionValue#(Bit#(8)) out if (isValid(tmp));
        tmp <= tagged Invalid;
        return fromMaybe(0,tmp);
    endmethod

endmodule

endpackage