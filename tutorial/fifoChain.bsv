package fifoChain;
// necessary packages
import Simplefifo::*;
import Connectable::*;
import GetPut::*;


module top();
 
	Simplefifo::FIFOIfc ff1 <- mkSimpleFIFO();
	GetPut::Get#(Bit#(32)) ff1get <- toGet(ff1);
	Simplefifo::FIFOIfc ff2 <- mkSimpleFIFO();
	GetPut::Put#(Bit#(32)) ff2put <- toPut(ff2);

	mkConnection(ff1get,ff2put);

endmodule
endpackage
