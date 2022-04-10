package FluteSoc;
// necessary packages
import MemUtils::*;
import Connectable::*;
import AXI4_Fake_16550::*;
import Core::*;
import GetPut::*;
// imported packages
import Routable::*;
import ClientServer::*;
import SourceSink::*;
import AXI4_Common_Types::*;
import AXI4_Types::*;
import Prelude::*;
import AXI4Lite_Types::*;
import AXI4_Interconnect::*;
import Core_IFC::*;
import OneWayBus::*;
import AXI4Stream_Types::*;
import FIFO::*;
import FIFOF::*;
import MemSim::*;
import MasterSlave::*;


function Vector #(2, Bool) route_bus1 (r_t x) provisos ( Bits#(r_t,r_l) );
	Bit#(r_l) adress = pack(x);
	Vector#(2, Bool) oneHotAdress = replicate (False);
	// memory -> 0
	if (adress >= 0 && adress < 4096)
		oneHotAdress[0] = True;
	// aXI4_Fake_16550 -> 1
	if (adress >= 4096 && adress < 8192)
		oneHotAdress[1] = True;
	return oneHotAdress;
endfunction

module top();
 
	Core_IFC::Core_IFC#(SoC_Map::N_External_Interrupt_Sources) core <- mkCore();
	AXI4_Types::AXI4_Slave#(6,64,64,0,0,0,0,0) memory <- mkAXI4SimpleMem(4096, Maybe#("xddd"));
	AXI4_Types::AXI4_Slave#(6,64,64,0,0,0,0,0) aXI4_Fake_16550 <- mkAXI4_Fake_16550_Simple();

	mkConnection(core.core_mem_master,memory);
	mkConnection(core.core_mem_master,memory);
	AXI4_Interconnect::mkAXI4Bus(route_bus1,bus1_masters,bus1_slaves);

endmodule
endpackage
