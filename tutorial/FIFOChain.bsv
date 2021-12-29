package FIFOChain;
// necessary packages
import GetPut::*;
import FIFOF::*;
import FIFO::*;
import OneWayBus::*;
import Connectable::*;
import Vector::*;
// imported packages
import AddressFlit::*;
import AXI4_Interconnect::*;
import Routable::*;
import SourceSink::*;
import AXI4_Types::*;

typedef 1 DATASIZE;
typedef 4 ADDRWIDTH;

function Vector #(1, Bool) route__temp_1 (r_t x) provisos ( Bits#(r_t,r_l) );
	Bit#(r_l) r_t_b = pack(x);
	Vector#(1, Bool) r_t_v = replicate (False);
	if (r_t_b >= 0 && r_t_b <= 2)
		r_t_v[0] = True;
	return r_t_v;
endfunction

module top();
 
	FIFO#(Bit#(8)) ff1 <- mkFIFO();
	FIFO#(Bit#(8)) ff2 <- mkFIFO();
	FIFOF#(AFlit#(DATASIZE, ADDRWIDTH)) bf1 <- mkFIFOF();
	FIFOF#(AFlit#(DATASIZE, ADDRWIDTH)) bf2 <- mkFIFOF();

	mkConnection(toPut(ff1),toGet(ff2));
	mkConnection(ff1,ff2);
	Vector#(1, 	FIFOF#(AFlit#(DATASIZE, ADDRWIDTH))) __temp_1_ins;
	__temp_1_ins[0] = bf1;
	Vector#(1, 	FIFOF#(AFlit#(DATASIZE, ADDRWIDTH))) __temp_1_outs;
	__temp_1_outs[0] = bf2;
	mkOneWayBus(route__temp_1,__temp_1_ins,__temp_1_outs);

endmodule
endpackage
