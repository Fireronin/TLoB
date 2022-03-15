package FluteSoc;
// necessary packages
import AXI4_Interconnect::*;
import AXI4_Fake_16550::*;
import Core::*;
import Vector::*;
import OneWayBus::*;
import GetPut::*;
import Connectable::*;
import MemUtils::*;
// imported packages
import AXI4_Types::*;
import Core_IFC::*;
import FIFOF::*;
import Routable::*;
import ClientServer::*;
import FIFO::*;
import SourceSink::*;


function Vector #(2, Bool) route__temp_1 (r_t x) provisos ( Bits#(r_t,r_l) );
	Bit#(r_l) r_t_b = pack(x);
	Vector#(2, Bool) r_t_v = replicate (False);
	if (r_t_b >= 0 && r_t_b <= 16)
		r_t_v[0] = True;
	return r_t_v;
endfunction

module top();
 
	Core_IFC#(SoC_Map::N_External_Interrupt_Sources) core <- mkCore();
	AXI4_Slave#(5, 64, 64, 0, 0, 0, 0, 0) memory <- mkAXI4SimpleMem(32, Invalid);
	AXI4_Slave#(5, 64, 64, 0, 0, 0, 0, 0) aXI4_Fake_16550 <- mkAXI4_Fake_16550_Simple();

	Vector#(1, AXI4_Master#(5, 64, 64, 0, 0, 0, 0, 0)) __temp_1_ins;
	__temp_1_ins[0] = core.cpu_imem_master;
	Vector#(2, AXI4_Slave#(5, 64, 64, 0, 0, 0, 0, 0)) __temp_1_outs;
	__temp_1_outs[0] = memory;
	__temp_1_outs[1] = aXI4_Fake_16550;
	mkAXI4Bus(route__temp_1,__temp_1_ins,__temp_1_outs);

endmodule
endpackage
