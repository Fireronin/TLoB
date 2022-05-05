package FIFOChain;
// necessary packages
import Connectable::*;
import Vector::*;
import Simplefifo::*;


module top ();
 
	Simplefifo::FIFOIfc#(Bit#(32)) fifo1 <- mkSimpleFIFO();
	Simplefifo::FIFOIfc#(Bit#(32)) fifo2 <- mkSimpleFIFO();

	mkConnection(fifo1,fifo2);


endmodule
endpackage
