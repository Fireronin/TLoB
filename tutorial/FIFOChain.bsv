package FIFOChain;
import FIFO::*;
import GetPut::*;
import Connectable::*;

module mkFIFOChain();
 
	FIFO#(Bit#(8)) ff2 <- mkFIFO();
	FIFO#(Bit#(8)) ff1 <- mkFIFO();

	mkConnection(toPut(ff1),toGet(ff2));

endmodule
endpackage
