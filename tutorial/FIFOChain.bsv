package FIFOChain;
import Connectable::*;
import GetPut::*;
import FIFO::*;

module mkFIFOChain();
 
	FIFO#(Bit#(8)) ff1 <- mkFIFO();
	FIFO#(Bit#(8)) ff2 <- mkFIFO();

	mkConnection(toPut(ff1),toGet(ff2));

endmodule
endpackage
