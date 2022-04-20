package Polyfifo;

interface FIFOIfc#(numeric type value_size);
    method Action enq(Bit#(value_size) value);
    method Action deq;
    method Bit#(value_size) first();
endinterface

// interface FIFOIfc2#(numeric type value_size);
//     method Action enq(Bit#(value_size) value);
//     method Action deq(Bit#(value_size) value, Bit#(value_size) value2);
//     method Bit#(value_size) first();
// endinterface

// typedef enum { False, True } Bool2 deriving (Bits, Eq);

// typedef enum {
//     Foo[2],
//     Bar[5:7],
//     Quux[3:2]
// } Glurph;

// typedef struct { int x; int y; } Coord;
// typedef struct { Bit#(7) pc; Bit#(3) rf; Bit#(8) mem; } Proc;

// typedef union tagged {
//     bit [4:0] Register;
//     bit [21:0] Literal;
//     struct { bit [4:0] regAddr; bit [4:0] regIndex;} Indexed;
// } InstrOperand;

// typedef union tagged {
//     struct { Bit#(4) op; Reg#(Bit#(4)) rs; Bit#(5) rt; UInt#(16) imm;} Immediate;
//     struct {
//         Bit#(4) op; 
//         UInt#(26) target;
//     } Jump;
// } Instruction deriving (Bits);



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