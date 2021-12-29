package FIFOChain;
import FIFO::*;
import Connectable::*;
import OneWayBus::*;
import GetPut::*;
import FIFOF::*;
import Vector::*;
import Routable:: *;

import Routable   :: *;
import OneWayBus  :: *;
import ListExtra  :: *;
import SourceSink :: *;

import FIFOF :: *;
import Vector :: *;
import ConfigReg :: *;

typedef struct {
  Bit#(d) data;
  Bit#(o) dest;
} AFlit#(numeric type d, numeric type o) deriving (Bits);
instance FShow#(AFlit#(a,b));
  function fshow(x) =
    $format("[data = %b, dest = %b]", x.data, x.dest);
endinstance
instance Has_routingField #(AFlit#(i,o), Bit#(o));
  function routingField (x) = x.dest;
endinstance
instance Has_isLast #(AFlit#(i,o));
  function isLast = constFn(True);
endinstance

typedef 1 DATASIZE;
typedef 1 ADDRWIDTH;

function Vector #(r_s, Bool) route__temp_1 (r_t x) provisos ( Bits#(r_t,r_s) );
	Bit#(r_s) r_t_b = pack(x);
	Vector#(r_s, Bool) r_t_v = replicate (False);
	if (r_t_b >= 0 && r_t_b <= 1)
		r_t_v[0] = True;
	return r_t_v;
endfunction

module top();
 
	FIFO#(Bit#(8)) ff1 <- mkFIFO();
	FIFO#(Bit#(8)) ff2 <- mkFIFO();
	FIFOF#(AFlit#(DATASIZE, ADDRWIDTH)) bf1 <- mkFIFOF();
	FIFOF#(AFlit#(DATASIZE, ADDRWIDTH)) bf2 <- mkFIFOF();

	mkConnection(toPut(ff1),toGet(ff2));
	Vector#(1, 	FIFOF#(AFlit#(DATASIZE, ADDRWIDTH))) __temp_1_ins;
	__temp_1_ins[0] = bf1;
	Vector#(1, 	FIFOF#(AFlit#(DATASIZE, ADDRWIDTH))) __temp_1_outs;
	__temp_1_outs[0] = bf2;
	mkOneWayBus(route__temp_1,__temp_1_ins,__temp_1_outs);

endmodule
endpackage
