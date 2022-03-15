package fifoChain;
// necessary packages
import OneWayBus::*;
import Vector::*;
import Connectable::*;
import FIFO::*;
import FIFOF::*;
import GetPut::*;
// imported packages
import AddressFlit::*;
import Routable::*;
import AXI4_Types::*;
import AXI4_Interconnect::*;
import SourceSink::*;

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
	FIFOF#(AFlit#(DATASIZE, ADDRWIDTH)) bf3 <- mkFIFOF();
	FIFOF#(AFlit#(DATASIZE, ADDRWIDTH)) bf4 <- mkFIFOF();

	mkConnection(toPut(ff1),toGet(ff2));
	Vector#(1, 	FIFOF#(AFlit#(DATASIZE, ADDRWIDTH))) __temp_1_ins;
	__temp_1_ins[0] = bf3;
	Vector#(1, 	FIFOF#(AFlit#(DATASIZE, ADDRWIDTH))) __temp_1_outs;
	__temp_1_outs[0] = bf4;
	mkOneWayBus(route__temp_1,__temp_1_ins,__temp_1_outs);

endmodule
endpackage
