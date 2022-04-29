package GUITEST;
// necessary packages
import Connectable::*;
import Vector::*;
import Simplefifo::*;


module top();
 
	Simplefifo::FIFOIfc#(Bit#(32)) fifo1 <- mkSimpleFIFO();
	Simplefifo::FIFOIfc#(Bit#(32)) fifo2 <- mkSimpleFIFO();
	Simplefifo::FIFOIfc#(Bit#(32)) fifo3 <- mkSimpleFIFO();

	mkConnection(fifo1,fifo2);
	mkConnection(fifo2,fifo3);

endmodule
endpackage
