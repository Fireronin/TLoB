package GUITEST;
// necessary packages
import Connectable::*;
import Vector::*;


module top();
 
	Reg#(Bit#(32)) instance2 <- mkRegU();
	Reg#(Bit#(32)) instance1 <- mkReg(instance2._read);


endmodule
endpackage
