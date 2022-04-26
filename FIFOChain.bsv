package FIFOChain;
// necessary packages
import Connectable::*;
import Vector::*;
import FIFO::*;


module top();
 
	FIFO::FIFO#(Bit#(32)) fifo3 <- mkFIFO();
	Reg#(Bit#(32)) reg <- mkRegU();
	Reg#(Bit#(32)) reg2 <- mkReg(reg._read);


endmodule
endpackage
